"""
天道 TRPG Party - 服务器管理工具
通过 SSH 远程管理 Autodl 云服务器
"""

import paramiko
import time
import sys
import os
import asyncio
from pathlib import Path

# 服务器配置
SERVER_CONFIG = {
    "host": "connect.bjb1.seetacloud.com",
    "port": 38591,
    "username": "root",
    "password": "BSySqlzPfixH",
    "python_path": "/root/miniconda3/bin/python",
    "service_port": 6006,
    "service_name": "tiandao-trpg",
}

# 本地项目路径
LOCAL_PROJECT_PATH = Path(__file__).parent.parent
REMOTE_PROJECT_PATH = "/root/tiandao-trpg"


class ServerManager:
    def __init__(self):
        self.ssh = None
        self.sftp = None
        self.config = SERVER_CONFIG

    def connect(self):
        """连接服务器"""
        print(f"Connecting to {self.config['host']}:{self.config['port']}...")
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            self.config["host"],
            port=self.config["port"],
            username=self.config["username"],
            password=self.config["password"],
            timeout=15,
        )
        self.sftp = self.ssh.open_sftp()
        print("Connected!")
        return self

    def disconnect(self):
        """断开连接"""
        if self.sftp:
            self.sftp.close()
        if self.ssh:
            self.ssh.close()
        print("Disconnected")

    def run_command(self, cmd: str, timeout=30) -> tuple:
        """执行命令并返回输出"""
        stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=timeout)
        return stdout.read().decode(), stderr.read().decode()

    def is_service_running(self) -> bool:
        """检查服务是否运行"""
        out, _ = self.run_command(f"ps aux | grep {self.config['service_name']} | grep -v grep")
        return len(out.strip()) > 0

    def get_service_url(self) -> str:
        """获取服务公网地址"""
        return f"https://u892543-zjue-dc99aa16.bjb1.seetacloud.com:8443/"

    def start_service(self, detach=True):
        """启动服务"""
        if self.is_service_running():
            print("Service already running")
            return True

        print("Starting service...")
        cmd = f"cd {REMOTE_PROJECT_PATH} && nohup {self.config['python_path']} -m uvicorn src.server:app --host 0.0.0.0 --port {self.config['service_port']} > /root/tiandao_service.log 2>&1 &"
        self.run_command(cmd)
        time.sleep(2)

        if self.is_service_running():
            print(f"[OK] Service started: {self.get_service_url()}")
            return True
        else:
            print("[FAIL] Service failed to start, check logs:")
            _, err = self.run_command("cat /root/tiandao_service.log")
            print(err[-500:])
            return False

    def stop_service(self):
        """停止服务"""
        if not self.is_service_running():
            print("Service not running")
            return True

        print("Stopping service...")
        # 优雅关闭 - 发送 SIGTERM
        out, _ = self.run_command(f"pkill -f '{self.config['service_name']}'")
        time.sleep(1)

        if not self.is_service_running():
            print("[OK] Service stopped")
            return True
        else:
            # 强制杀死
            self.run_command(f"pkill -9 -f '{self.config['service_name']}'")
            time.sleep(1)
            print("[OK] Service force stopped")
            return True

    def restart_service(self):
        """重启服务"""
        self.stop_service()
        time.sleep(1)
        return self.start_service()

    def deploy_project(self):
        """部署项目到服务器"""
        print("Deploying project...")

        # 创建远程目录
        self.run_command(f"mkdir -p {REMOTE_PROJECT_PATH}")

        # 上传所有文件
        local_path = LOCAL_PROJECT_PATH
        uploaded = 0
        skipped = 0

        for root, dirs, files in os.walk(local_path):
            # 跳过 __pycache__ 和隐藏目录
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']

            for file in files:
                if file.startswith('.') or file.endswith('.pyc'):
                    skipped += 1
                    continue

                local_file = Path(root) / file
                rel_path = local_file.relative_to(local_path)
                remote_file = f"{REMOTE_PROJECT_PATH}/{rel_path}"

                # 确保远程目录存在
                remote_dir = str(Path(remote_file).parent)
                self.run_command(f"mkdir -p '{remote_dir}'")

                try:
                    self.sftp.put(str(local_file), remote_file)
                    uploaded += 1
                    if uploaded % 20 == 0:
                        print(f"  Uploaded {uploaded} files...")
                except Exception as e:
                    print(f"  Upload failed {rel_path}: {e}")

        print(f"[OK] Deploy complete: uploaded {uploaded} files, skipped {skipped}")

    def install_dependencies(self):
        """安装依赖"""
        print("Installing dependencies...")
        cmd = f"cd {REMOTE_PROJECT_PATH} && {self.config['python_path']} -m pip install -r requirements.txt -q"
        self.run_command(cmd, timeout=120)
        print("[OK] Dependencies installed")

    def get_logs(self, lines=50):
        """查看日志"""
        out, _ = self.run_command(f"tail -{lines} /root/tiandao_service.log")
        return out

    def test_service(self) -> bool:
        """测试服务是否正常响应"""
        out, _ = self.run_command(f"curl -s http://127.0.0.1:{self.config['service_port']}/")
        try:
            import json
            data = json.loads(out)
            print(f"[OK] Service OK: {data}")
            return True
        except:
            print(f"[FAIL] Service error: {out}")
            return False

    def status(self):
        """查看服务状态"""
        running = self.is_service_running()
        print(f"Service status: {'[RUNNING]' if running else '[STOPPED]'}")
        print(f"Service URL: {self.get_service_url()}")

        if running:
            self.test_service()
        else:
            print("Logs (last 20 lines):")
            print(self.get_logs(20))


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Tiandao TRPG Server Manager")
    parser.add_argument("action", choices=["start", "stop", "restart", "status", "deploy", "logs"],
                        help="Actions: start, stop, restart, status, deploy, logs")
    parser.add_argument("--no-deploy", action="store_true", help="Skip file upload on restart")

    args = parser.parse_args()

    manager = ServerManager()

    try:
        manager.connect()

        if args.action == "start":
            manager.start_service()

        elif args.action == "stop":
            manager.stop_service()

        elif args.action == "restart":
            if not args.no_deploy:
                manager.deploy_project()
            manager.restart_service()

        elif args.action == "status":
            manager.status()

        elif args.action == "deploy":
            manager.deploy_project()
            manager.install_dependencies()
            manager.restart_service()

        elif args.action == "logs":
            print(manager.get_logs())

    finally:
        manager.disconnect()


if __name__ == "__main__":
    main()
