#!/usr/bin/env python3
"""
天道 TRPG Party - 安卓中继服务

用法:
    python relay.py                          # 启动中继服务 (默认端口8080)
    python relay.py stop                    # 停止服务
    python relay.py status                  # 查看状态
    python relay.py on                     # 开启云服务器
    python relay.py off                    # 关闭云服务器 (切换到本地模式)
    python relay.py url                     # 显示客户端访问网址
    python relay.py set <服务器地址>        # 设置云服务器地址
    python relay.py help                   # 显示帮助

手机需要:
    1. 安装Termux
    2. pip install aiohttp
    3. python relay.py [命令]
"""

import asyncio
import aiohttp
from aiohttp import web
import argparse
import logging
import sys
import json
import random
import string
import os
import signal
from datetime import datetime
from pathlib import Path

# 日志配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 默认云服务器
DEFAULT_CLOUD = "https://u892543-zjue-dc99aa16.bjb1.seetacloud.com:8443"
LOCAL_PORT = 8080
PID_FILE = "/data/data/com.termux/files/home/.tiandao_relay.pid"
CONFIG_FILE = "/data/data/com.termux/files/home/.tiandao_relay.conf"


class RelayConfig:
    """中继配置"""

    def __init__(self):
        self.cloud_server = DEFAULT_CLOUD
        self.local_port = LOCAL_PORT
        self.cloud_enabled = True
        self.load()

    def load(self):
        """加载配置"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.cloud_server = data.get('cloud_server', DEFAULT_CLOUD)
                    self.local_port = data.get('local_port', LOCAL_PORT)
                    self.cloud_enabled = data.get('cloud_enabled', True)
            except:
                pass

    def save(self):
        """保存配置"""
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump({
                    'cloud_server': self.cloud_server,
                    'local_port': self.local_port,
                    'cloud_enabled': self.cloud_enabled
                }, f)
        except:
            pass


class LocalGameServer:
    """本地简易游戏服务器 (云关闭时使用)"""

    def __init__(self, config: RelayConfig):
        self.config = config

    def generate_id(self, length=8):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    def generate_room_code(self):
        return ''.join(random.choices(string.ascii_uppercase, k=4))

    async def handle_api(self, request):
        """处理 API 请求"""
        path = request.path
        method = request.method

        # 获取状态
        if path == '/relay/status':
            return web.json_response({
                'mode': 'cloud' if self.config.cloud_enabled else 'local',
                'cloud_server': self.config.cloud_server if self.config.cloud_enabled else None,
                'cloud_enabled': self.config.cloud_enabled,
                'local_port': self.config.local_port
            })

        # 切换模式
        if path == '/relay/setMode' and method == 'POST':
            try:
                data = await request.json()
                mode = data.get('mode', 'cloud')
                self.config.cloud_enabled = (mode == 'cloud')
                self.config.save()
                return web.json_response({'ok': True})
            except:
                return web.json_response({'ok': False}, status=400)

        # 切换云服务器
        if path == '/relay/setCloud' and method == 'POST':
            try:
                data = await request.json()
                self.config.cloud_server = data.get('server', self.config.cloud_server)
                self.config.save()
                return web.json_response({'ok': True, 'cloud_server': self.config.cloud_server})
            except:
                return web.json_response({'ok': False}, status=400)

        # 代理到云服务器
        if self.config.cloud_enabled:
            return await self.proxy_to_cloud(request)

        # 本地模式处理
        return await self.handle_local(request)

    async def proxy_to_cloud(self, request):
        """转发请求到云服务器"""
        path = request.path
        cloud_url = f"{self.config.cloud_server}{path}"

        headers = dict(request.headers)
        for h in ['Connection', 'Keep-Alive', 'Transfer-Encoding', 'Host']:
            headers.pop(h, None)

        body = await request.read() if request.can_read_body else None

        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.request(
                    method=request.method,
                    url=cloud_url,
                    headers=headers,
                    data=body,
                    allow_redirects=False,
                    ssl=False
                ) as resp:
                    resp_body = await resp.read()
                    response = web.Response(
                        body=resp_body,
                        status=resp.status,
                        content_type=resp.content_type
                    )
                    for h, v in resp.headers.items():
                        if h.lower() not in ['content-encoding', 'transfer-encoding', 'host']:
                            response.headers[h] = v
                    return response
        except asyncio.TimeoutError:
            return web.Response(status=504, text="云服务器超时")
        except Exception as e:
            logger.error(f"Cloud proxy error: {e}")
            return web.Response(status=502, text=f"云服务器错误: {e}")

    async def handle_local(self, request):
        """本地模式 - 简单的游戏服务"""
        path = request.path
        method = request.method

        if path == '/health' or path == '/':
            return web.json_response({
                'status': 'ok',
                'mode': 'local',
                'service': 'tiandao-trpg-local',
                'version': '1.0.0'
            })

        return web.Response(status=404, text="本地模式暂未实现完整功能")

    async def proxy_ws(self, request):
        """WebSocket 代理"""
        if self.config.cloud_enabled:
            # 转发 WebSocket 到云服务器
            ws_path = request.path
            cloud_ws = self.config.cloud_server.replace('https://', 'wss://').replace('http://', 'ws://')
            cloud_ws_url = f"{cloud_ws}{ws_path}?{request.query_string}"

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.ws_connect(cloud_ws_url, ssl=False) as ws_cloud:
                        ws_client = web.WebSocketResponse()
                        await ws_client.prepare(request)

                        async def forward_to_cloud():
                            async for msg in ws_client:
                                if msg.type == aiohttp.WSMsgType.TEXT:
                                    await ws_cloud.send_str(msg.data)
                                elif msg.type == aiohttp.WSMsgType.BINARY:
                                    await ws_cloud.send_bytes(msg.data)
                                elif msg.type == aiohttp.WSMsgType.CLOSE:
                                    await ws_cloud.close()
                                    break

                        async def forward_to_client():
                            async for msg in ws_cloud:
                                if msg.type == aiohttp.WSMsgType.TEXT:
                                    await ws_client.send_str(msg.data)
                                elif msg.type == aiohttp.WSMsgType.BINARY:
                                    await ws_client.send_bytes(msg.data)
                                elif msg.type == aiohttp.WSMsgType.CLOSE:
                                    await ws_client.close()
                                    break

                        await asyncio.gather(forward_to_cloud(), forward_to_client())
                        return ws_client
            except Exception as e:
                return web.Response(status=500, text=f"WebSocket错误: {e}")
        else:
            return web.Response(status=501, text="本地模式WebSocket暂未实现")


class RelayServer:
    """HTTP 中继服务器"""

    def __init__(self, config: RelayConfig):
        self.config = config
        self.local_server = LocalGameServer(config)
        self.app = None
        self.runner = None

    async def handle_request(self, request):
        """处理请求"""
        path = request.path

        # API 请求
        if path.startswith('/api/') or path.startswith('/relay/') or path == '/health':
            return await self.local_server.handle_api(request)

        # WebSocket
        if path.startswith('/ws/'):
            return await self.local_server.proxy_ws(request)

        # 主页 - 返回重定向到客户端页面
        if path == '/' or path == '/index.html':
            return web.Response(
                text=self._get_status_page(),
                content_type='text/html'
            )

        # 云模式且非API请求，转发
        if self.config.cloud_enabled:
            return await self.local_server.proxy_to_cloud(request)

        return web.Response(status=404, text="Not Found")

    def _get_status_page(self):
        """返回状态页面"""
        mode = '云服务器模式' if self.config.cloud_enabled else '本地模式'

        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>天道 TRPG 中继器</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #1a1a2e; color: #eaeaea; padding: 20px; max-width: 600px; margin: 0 auto; }}
        h1 {{ color: #e94560; text-align: center; }}
        .card {{ background: #16213e; padding: 20px; border-radius: 10px; margin: 15px 0; }}
        .status {{ color: #4ecca3; font-size: 24px; font-weight: bold; }}
        .url {{ background: #0f3460; padding: 15px; border-radius: 5px; word-break: break-all; color: #4ecca3; }}
        .btn {{ background: #e94560; color: white; border: none; padding: 12px 24px; border-radius: 5px; cursor: pointer; margin: 5px; font-size: 16px; }}
        .btn-green {{ background: #4ecca3; }}
        .btn-red {{ background: #e94560; }}
        input {{ background: #0f3460; border: 1px solid #533483; color: white; padding: 12px; border-radius: 5px; width: 100%; margin: 5px 0; box-sizing: border-box;}}
        .info {{ color: #a0a0a0; font-size: 14px; }}
    </style>
</head>
<body>
    <h1>🎮 天道 TRPG 中继器</h1>

    <div class="card">
        <h3>📊 当前状态</h3>
        <p>模式: <span class="status">{mode}</span></p>
        <p>云服务器: <span class="info">{self.config.cloud_server}</span></p>
        <p>监听端口: {self.config.local_port}</p>
    </div>

    <div class="card">
        <h3>🔗 客户端访问地址</h3>
        <div class="url">http://<手机IP>:{self.config.local_port}/</div>
        <p class="info">新人连接请使用此地址</p>
    </div>

    <div class="card">
        <h3>⚡ 快速操作</h3>
        <button class="btn btn-green" onclick="setMode('cloud')">开启云服务器</button>
        <button class="btn btn-red" onclick="setMode('local')">关闭云服务器</button>
    </div>

    <div class="card">
        <h3>☁️ 云服务器设置</h3>
        <input type="text" id="cloudServer" value="{self.config.cloud_server}">
        <button class="btn" onclick="updateCloud()">更新服务器</button>
    </div>

    <div class="card">
        <h3>📱 命令行操作 (Termux)</h3>
        <div class="url">
            python relay.py on      # 开启云服务器<br>
            python relay.py off     # 关闭云服务器<br>
            python relay.py status  # 查看状态<br>
            python relay.py url     # 显示访问网址<br>
            python relay.py stop    # 停止服务
        </div>
    </div>

    <script>
        async function setMode(mode) {{
            const resp = await fetch('/relay/setMode', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{mode: mode}})
            }});
            if (resp.ok) {{ location.reload(); }}
        }}

        async function updateCloud() {{
            const server = document.getElementById('cloudServer').value;
            const resp = await fetch('/relay/setCloud', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{server: server}})
            }});
            if (resp.ok) {{ alert('已更新云服务器地址'); }}
        }}
    </script>
</body>
</html>
        """

    async def start(self):
        """启动服务"""
        self.app = web.Application()
        self.app.router.add_route('*', '/{path:.*}', self.handle_request)

        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        site = web.TCPSite(self.runner, '0.0.0.0', self.config.local_port)
        await site.start()

        # 保存PID
        with open(PID_FILE, 'w') as f:
            f.write(str(os.getpid()))

        logger.info("")
        logger.info("=" * 50)
        logger.info("🎮 天道 TRPG 中继服务已启动")
        logger.info("=" * 50)
        logger.info(f"📍 监听端口: {self.config.local_port}")
        logger.info(f"🌐 模式: {'云服务器' if self.config.cloud_enabled else '本地'}")
        logger.info(f"☁️ 云服务器: {self.config.cloud_server}")
        logger.info("")
        logger.info(f"📱 客户端访问: http://<手机IP>:{self.config.local_port}/")
        logger.info(f"📋 状态页面: http://127.0.0.1:{self.config.local_port}/")
        logger.info("")
        logger.info("💡 Termux 命令:")
        logger.info("   python relay.py status   # 查看状态")
        logger.info("   python relay.py on/off    # 开关云服务器")
        logger.info("   python relay.py url      # 显示访问网址")
        logger.info("   python relay.py stop     # 停止服务")
        logger.info("=" * 50)

    async def stop(self):
        """停止服务"""
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
        if self.runner:
            await self.runner.cleanup()
        logger.info("中继服务已停止")


# ============================================
# 命令行命令处理
# ============================================

async def cmd_status(config: RelayConfig):
    """显示状态"""
    mode = '🌐 云服务器模式' if config.cloud_enabled else '🏠 本地模式'
    print("")
    print("=" * 50)
    print("📊 天道 TRPG 中继器状态")
    print("=" * 50)
    print(f"模式: {mode}")
    print(f"云服务器: {config.cloud_server}")
    print(f"监听端口: {config.local_port}")
    print(f"云服务器: {'✅ 已开启' if config.cloud_enabled else '❌ 已关闭'}")
    print("")
    print("📱 客户端访问地址:")
    print(f"   http://<手机IP>:{config.local_port}/")
    print("")
    print("☁️ 云服务器地址:")
    print(f"   {config.cloud_server}")
    print("=" * 50)


async def cmd_on(config: RelayConfig):
    """开启云服务器"""
    config.cloud_enabled = True
    config.save()
    print(f"✅ 云服务器已开启: {config.cloud_server}")


async def cmd_off(config: RelayConfig):
    """关闭云服务器"""
    config.cloud_enabled = False
    config.save()
    print("❌ 云服务器已关闭 (切换到本地模式)")


async def cmd_url(config: RelayConfig):
    """显示访问网址"""
    print("")
    print("📱 客户端访问地址:")
    print(f"   http://<手机IP>:{config.local_port}/")
    print("")
    print("☁️ 转发到云服务器:")
    print(f"   {config.cloud_server}")
    print("")


async def cmd_set(config: RelayConfig, server: str):
    """设置云服务器"""
    if not server.startswith('http'):
        server = 'https://' + server
    config.cloud_server = server
    config.save()
    print(f"✅ 云服务器已设置为: {server}")


def cmd_stop():
    """停止服务"""
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            os.kill(pid, signal.SIGTERM)
            print("已发送停止信号")
        except ProcessLookupError:
            print("进程不存在")
        except PermissionError:
            print("需要更高权限")
        os.remove(PID_FILE)
    else:
        print("服务未运行")


def main():
    parser = argparse.ArgumentParser(
        description="天道 TRPG 中继服务",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
命令:
    python relay.py              启动中继服务 (默认端口8080)
    python relay.py start        同上
    python relay.py stop         停止服务
    python relay.py status       查看状态
    python relay.py on           开启云服务器
    python relay.py off          关闭云服务器
    python relay.py url          显示访问网址
    python relay.py set <地址>   设置云服务器

示例:
    python relay.py              # 启动服务
    python relay.py on           # 开启云服务器
    python relay.py off          # 关闭云服务器
    python relay.py set https://my-server.com:8443  # 设置服务器
        """
    )

    parser.add_argument('command', nargs='?', default='start',
                        help='命令: start, stop, status, on, off, url, set, help')
    parser.add_argument('args', nargs='*', help='命令参数')

    args = parser.parse_args()
    command = args.command.lower()
    config = RelayConfig()

    # 处理命令
    if command in ('start', 'run'):
        asyncio.run(_cmd_start(config))
    elif command == 'stop':
        cmd_stop()
    elif command == 'status':
        asyncio.run(cmd_status(config))
    elif command == 'on':
        asyncio.run(cmd_on(config))
    elif command == 'off':
        asyncio.run(cmd_off(config))
    elif command == 'url':
        asyncio.run(cmd_url(config))
    elif command == 'set':
        if not args.args:
            print("请提供服务器地址: python relay.py set <地址>")
        else:
            asyncio.run(cmd_set(config, args.args[0]))
    elif command in ('help', '--help', '-h'):
        parser.print_help()
    else:
        print(f"未知命令: {command}")
        print("输入 python relay.py help 查看帮助")


async def _cmd_start(config: RelayConfig):
    """启动服务"""
    server = RelayServer(config)

    def signal_handler(sig, frame):
        logger.info("收到停止信号...")
        asyncio.create_task(server.stop())
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        await server.start()
        # 永久运行
        while True:
            await asyncio.sleep(3600)
    except KeyboardInterrupt:
        pass
    finally:
        await server.stop()


if __name__ == "__main__":
    main()
