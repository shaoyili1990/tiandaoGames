"""
天道 TRPG Party - 主服务器

基于 FastAPI + WebSocket 的多玩家 TRPG 服务器
"""

import asyncio
import json
import uuid
import random
import string
from datetime import datetime
from typing import Dict, List, Optional, Set
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import logging

# 本地模块 (添加到路径)
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from models import (
    GameRecord, Player, Character, NPC, World, Location,
    GameEvent, Save, ChatMessage, DMMessage, NPCMessage,
    SystemMessage, EventMessage, generate_id, now
)
from game_manager import game_manager
from ai_service import AIService
from events import event_manager, EventGenerator
from persistence import SaveManager

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# FastAPI 应用
# ============================================

app = FastAPI(
    title="天道 TRPG Party",
    version="1.0.0",
    description="赛博跑团 - 老天爷当DM，多位玩家异地同屏"
)

# 挂载静态文件
app.mount("/static", StaticFiles(directory="web/static"), name="static")

# ============================================
# WebSocket 连接管理器
# ============================================

class ConnectionManager:
    """管理所有 WebSocket 连接"""

    def __init__(self):
        # game_id -> Set[WebSocket]
        self.game_connections: Dict[str, Set[WebSocket]] = {}
        # WebSocket -> player_id
        self.ws_players: Dict[WebSocket, str] = {}
        # game_id -> player_id -> WebSocket
        self.player_ws: Dict[str, Dict[str, WebSocket]] = {}

    async def connect(self, websocket: WebSocket, game_id: str, player_id: str):
        await websocket.accept()

        if game_id not in self.game_connections:
            self.game_connections[game_id] = set()
        self.game_connections[game_id].add(websocket)

        self.ws_players[websocket] = player_id

        if game_id not in self.player_ws:
            self.player_ws[game_id] = {}
        self.player_ws[game_id][player_id] = websocket

        logger.info(f"Player {player_id} connected to game {game_id}")

    def disconnect(self, websocket: WebSocket, game_id: str, player_id: str):
        self.game_connections.get(game_id, set()).discard(websocket)
        self.ws_players.pop(websocket, None)
        if game_id in self.player_ws:
            self.player_ws[game_id].pop(player_id, None)

        logger.info(f"Player {player_id} disconnected from game {game_id}")

    async def broadcast(self, game_id: str, message: dict, exclude_player: Optional[str] = None):
        """广播消息到游戏内所有玩家"""
        if game_id not in self.game_connections:
            return

        disconnected = []
        for ws in self.game_connections[game_id]:
            pid = self.ws_players.get(ws)
            if pid == exclude_player:
                continue

            try:
                await ws.send_json(message)
            except:
                disconnected.append(ws)

        # 清理断开的连接
        for ws in disconnected:
            self.game_connections[game_id].discard(ws)

    async def send_to(self, player_id: str, game_id: str, message: dict):
        """发送给特定玩家"""
        if game_id in self.player_ws and player_id in self.player_ws[game_id]:
            ws = self.player_ws[game_id][player_id]
            try:
                await ws.send_json(message)
            except:
                pass

manager = ConnectionManager()

# ============================================
# Pydantic 模型
# ============================================

class CreateGameRequest(BaseModel):
    owner_nickname: str
    game_name: str = "新游戏"
    player_count: int = 4  # 默认4人小队
    world_description: str = ""  # 用户描述想要的世界,AI生成

class JoinGameRequest(BaseModel):
    room_code: str
    nickname: str

class SendMessageRequest(BaseModel):
    content: str
    msg_type: str = "chat"  # chat, action

class CreateCharacterRequest(BaseModel):
    name: str
    description: str = ""
    mbti: str = "INFJ"
    background: str = ""

# ============================================
# HTTP 路由
# ============================================

@app.get("/")
async def root():
    """返回主页"""
    return FileResponse("web/templates/index.html")

@app.get("/api/health")
async def health():
    """健康检查"""
    return {
        "status": "ok",
        "service": "tiandao-trpg-party",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/game/create")
async def create_game(request: CreateGameRequest):
    """创建新游戏 - AI根据用户描述生成世界"""
    # 清理昵称
    nickname = request.owner_nickname.strip()[:20]
    if not nickname:
        nickname = "匿名"

    game = game_manager.create_game(nickname, request.game_name)

    # 存储玩家数量和世界描述
    game.player_count = request.player_count
    game.world_description = request.world_description

    # AI生成世界 (基于用户描述,非固定模板)
    world_data = AIService.generate_world_ai(
        player_count=request.player_count,
        world_description=request.world_description
    )

    # 应用AI生成的世界
    if world_data:
        game.world.name = world_data.get("name", game.name)
        game.world.overview = world_data.get("overview", "")
        game.world.atmosphere_keywords = world_data.get("atmosphere_keywords", [])

    return {
        "game_id": game.game_id,
        "room_code": game.room_code,
        "owner_id": game.owner_id,
        "player_count": request.player_count,
        "world_description": request.world_description,
        "game": game.model_dump()
    }

@app.post("/api/game/join")
async def join_game(request: JoinGameRequest):
    """加入游戏"""
    nickname = request.nickname.strip()[:20]
    room_code = request.room_code.strip().upper()

    if not nickname:
        raise HTTPException(status_code=400, detail="昵称不能为空")
    if len(room_code) != 4:
        raise HTTPException(status_code=400, detail="房间码为4位")

    player = game_manager.join_game(room_code, nickname, is_core=True)

    if not player:
        raise HTTPException(status_code=404, detail="房间不存在")

    game = game_manager.get_game_by_code(room_code)

    return {
        "game_id": game.game_id,
        "room_code": game.room_code,
        "player_id": player.player_id,
        "game": game.model_dump()
    }

@app.get("/api/game/{game_id}")
async def get_game(game_id: str):
    """获取游戏信息"""
    game = game_manager.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    return game.model_dump()

@app.get("/api/game/{game_id}/players")
async def get_game_players(game_id: str):
    """获取游戏成员"""
    game = game_manager.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    return {
        "core_members": [p.model_dump() for p in game.core_members],
        "temp_members": [p.model_dump() for p in game.temp_members]
    }

@app.post("/api/game/{game_id}/character")
async def create_character(game_id: str, char_data: dict):
    """创建/更新角色信息"""
    game = game_manager.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    # 找到当前玩家
    # 从 char_data 获取昵称来定位玩家
    nickname = char_data.get('name', '')
    player = None
    for p in game.core_members:
        if p.nickname == nickname:
            player = p
            break

    if not player:
        return {"error": "玩家不存在"}

    # 更新角色信息
    player.character.name = char_data.get('name', player.nickname)
    player.character.description = char_data.get('description', '')
    player.character.background = char_data.get('background', '')
    player.character.mbti = char_data.get('mbti', 'INFJ')

    return {"character": player.character.model_dump()}

# ============================================
# 用户管理
# ============================================

@app.post("/api/user/register")
async def register_user(user_id: str, device_id: str = "", nickname: str = ""):
    """注册用户（设备绑定）"""
    existing = SaveManager.get_user(user_id)
    if existing:
        return {"user": existing, "is_new": False}

    user_data = {
        "user_id": user_id,
        "device_id": device_id,
        "email": "",
        "nickname": nickname or "匿名玩家",
        "created_at": now(),
        "last_login": now()
    }
    SaveManager.save_user(user_data)
    return {"user": user_data, "is_new": True}

@app.get("/api/user/{user_id}")
async def get_user(user_id: str):
    """获取用户信息"""
    user = SaveManager.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user

@app.get("/api/user/{user_id}/games")
async def get_user_games(user_id: str):
    """获取用户参与的所有游戏"""
    games = SaveManager.get_user_games(user_id)
    return {"games": games}

@app.post("/api/game/{game_id}/save")
async def save_game(game_id: str, note: str = "", created_by: str = ""):
    """保存游戏到数据库"""
    game = game_manager.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    # 持久化到数据库
    world_data = game.model_dump().get("world")
    save_data = {
        "save_id": generate_id(),
        "game_id": game_id,
        "snapshot": game.model_dump(),
        "note": note,
        "created_by": created_by or game.owner_id,
        "created_at": now()
    }
    SaveManager.save_snapshot(save_data)

    # 同时保存到游戏管理器
    save = game_manager.save_game(game_id, note, created_by or game.owner_id)

    return {"save_id": save.save_id, "saved_at": save.created_at}

@app.get("/api/game/{game_id}/saves")
async def get_saves(game_id: str):
    """获取游戏的所有存档"""
    game = game_manager.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    saves = SaveManager.get_saves(game_id)
    return {"saves": saves}

@app.post("/api/game/{game_id}/load/{save_id}")
async def load_game(game_id: str, save_id: str):
    """加载存档"""
    save = SaveManager.get_save(save_id)
    if not save:
        raise HTTPException(status_code=404, detail="存档不存在")

    if save.get("game_id") != game_id:
        raise HTTPException(status_code=400, detail="存档与游戏不匹配")

    success = game_manager.load_save(game_id, save_id)
    if not success:
        raise HTTPException(status_code=500, detail="加载失败")

    game = game_manager.get_game_by_id(game_id)
    return {"game": game.model_dump() if game else None}

@app.post("/api/game/{game_id}/start")
async def start_game(game_id: str):
    """开始游戏"""
    game = game_manager.get_game_by_id(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    game.status = "playing"
    game.last_played = now()

    # 广播开始消息
    await manager.broadcast(game_id, {
        "type": "system",
        "content": f"游戏 '{game.name}' 正式开始！",
        "timestamp": now()
    })

    # 天道描述开场
    current_loc = game.world.get_current_location()
    if current_loc:
        dm_intro = f"""【天道】欢迎来到 {game.world.name}。

{game.world.overview}

你们现在位于 {current_loc.name}。
{current_loc.description}
"""
    else:
        dm_intro = f"""【天道】欢迎来到 {game.world.name}。

{game.world.overview}

游戏开始！
"""

    await manager.broadcast(game_id, {
        "type": "dm",
        "content": dm_intro,
        "timestamp": now()
    })

    return {"status": "started"}

# ============================================
# WebSocket 路由
# ============================================

@app.websocket("/ws/{game_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player_id: str):
    """WebSocket 连接"""

    # 验证游戏和玩家
    game = game_manager.get_game_by_id(game_id)
    if not game:
        await websocket.close(code=4001, reason="Game not found")
        return

    player = game.get_player_by_id(player_id)
    if not player:
        await websocket.close(code=4002, reason="Player not found")
        return

    # 标记上线
    game_manager.player_connect(player_id)
    player.is_online = True

    await manager.connect(websocket, game_id, player_id)

    # 广播加入消息
    await manager.broadcast(game_id, {
        "type": "system",
        "content": f"{player.nickname} 加入了游戏",
        "player_id": player_id,
        "timestamp": now()
    }, exclude_player=player_id)

    # 发送当前游戏状态给新加入的玩家
    await manager.send_to(player_id, game_id, {
        "type": "game_state",
        "game": game.model_dump(),
        "player_id": player_id,
        "timestamp": now()
    })

    # 检查是否所有核心成员都到了，触发继续
    if game.status == "paused":
        offline_cores = game_manager.get_offline_core_members(game_id)
        if not offline_cores:
            game.status = "playing"
            await manager.broadcast(game_id, {
                "type": "system",
                "content": "所有核心成员已到齐，游戏继续！",
                "timestamp": now()
            })

    try:
        while True:
            data = await websocket.receive_json()
            await handle_message(game_id, player_id, data)

    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id, player_id)
        game_manager.player_disconnect(player_id)
        player.is_online = False

        # 广播离开消息
        await manager.broadcast(game_id, {
            "type": "system",
            "content": f"{player.nickname} 离开了游戏",
            "player_id": player_id,
            "timestamp": now()
        })

        # 如果是核心成员离线，启用AI托管
        if player.is_core:
            player.is_ai_controlled = True
            await manager.broadcast(game_id, {
                "type": "system",
                "content": f"{player.nickname} 已离线，角色由天道暂时托管",
                "player_id": player_id,
                "timestamp": now()
            })

# ============================================
# 消息处理
# ============================================

async def handle_message(game_id: str, player_id: str, data: dict):
    """处理玩家消息"""
    msg_type = data.get("type", "")
    game = game_manager.get_game_by_id(game_id)
    player = game.get_player_by_id(player_id) if game else None

    if not game or not player:
        return

    if msg_type == "chat":
        # 聊天消息
        content = data.get("content", "").strip()
        if not content:
            return

        await manager.broadcast(game_id, {
            "type": "chat",
            "player_id": player_id,
            "nickname": player.nickname,
            "content": content,
            "timestamp": now()
        })

        # 天道DM响应 (简化版：直接返回预设回复)
        await generate_dm_response(game_id, player, content)

    elif msg_type == "action":
        # 动作消息
        action = data.get("content", "").strip()
        if not action:
            return

        await manager.broadcast(game_id, {
            "type": "action",
            "player_id": player_id,
            "nickname": player.nickname,
            "content": action,
            "timestamp": now()
        })

        # 使用AI服务生成动作描述
        action_response = AIService.generate_action_response(action, player.model_dump(), game.model_dump())
        await manager.broadcast(game_id, {
            "type": "dm",
            "content": action_response,
            "timestamp": now()
        })

    elif msg_type == "ping":
        # 心跳
        await manager.send_to(player_id, game_id, {"type": "pong"})

    elif msg_type == "move":
        # 移动
        location_id = data.get("location_id", "")
        if location_id and location_id in game.world.locations:
            game_manager.move_player_to_location(player_id, location_id)
            loc = game.world.locations[location_id]

            # 使用AI服务生成位置描述
            dm_desc = AIService.generate_dm_response(game.model_dump(), player.model_dump(), f"我到达了{loc.name}")

            await manager.broadcast(game_id, {
                "type": "system",
                "content": f"{player.nickname} 移动到了 {loc.name}",
                "timestamp": now()
            })
            await manager.broadcast(game_id, {
                "type": "dm",
                "content": dm_desc,
                "timestamp": now()
            })

            # 触发位置事件
            triggered_events = EventGenerator.check_and_trigger_events(game, "location", location=location_id)
            for event in triggered_events:
                await manager.broadcast(game_id, {
                    "type": "event",
                    "event": event.model_dump(),
                    "timestamp": now()
                })

    elif msg_type == "interact":
        # 与NPC交互
        npc_id = data.get("npc_id", "")
        npc = game.world.npcs.get(npc_id)
        if npc:
            await generate_npc_response(game_id, player, npc)

    elif msg_type == "create_character":
        # 创建角色
        name = data.get("name", player.nickname) or player.nickname
        mbti = data.get("mbti", "INFJ")
        if mbti == "random":
            mbtis = ['INFJ', 'INFP', 'ENFP', 'INTJ', 'INTP', 'ENTJ', 'ENTP', 'ISTJ', 'ISFJ', 'ESTJ', 'ESFJ', 'ISTP', 'ISFP', 'ESTP', 'ESFP']
            import random
            mbti = random.choice(mbtis)
        y_value = data.get("y_value", 50)
        background = data.get("background", "")

        player.character = Character(
            name=name,
            mbti=mbti,
            background=background
        )
        player.character.name = name
        player.y_value = y_value
        player.base_y = y_value

        await manager.send_to(player_id, game_id, {
            "type": "character_created",
            "character": player.character.model_dump(),
            "y_value": player.y_value,
            "timestamp": now()
        })

        # 广播角色创建成功
        await manager.broadcast(game_id, {
            "type": "system",
            "content": f"{player.nickname} 创造了角色: {name} ({mbti})",
            "timestamp": now()
        }, exclude_player=player_id)

    elif msg_type == "event_choice":
        # 处理事件选择
        choice_id = data.get("choice_id", "")
        event_id = data.get("event_id", "")

        # 在活跃事件中查找
        for event in game.active_events:
            if event.status != "active":
                continue
            if event_id and event.event_id != event_id:
                continue

            # 处理选择
            for choice in event.choices:
                if choice.choice_id == choice_id:
                    event.status = "completed"
                    await manager.broadcast(game_id, {
                        "type": "dm",
                        "content": f"【天道】{choice.outcome}",
                        "timestamp": now()
                    })
                    return

            await manager.broadcast(game_id, {
                "type": "dm",
                "content": "【天道】你没有做出选择",
                "timestamp": now()
            })
            return


# ============================================
# DM 响应生成 (简化版)
# ============================================

async def generate_dm_response(game_id: str, player: Player, content: str):
    """生成天道DM响应"""
    game = game_manager.get_game_by_id(game_id)
    if not game:
        return

    # 使用AI服务生成描述
    dm_text = AIService.generate_dm_response(game.model_dump(), player.model_dump(), content)

    # 检查随机事件触发
    triggered_events = EventGenerator.check_and_trigger_events(game, "random")
    for event in triggered_events:
        event_msg = f"\n【事件触发】{event.title}\n{event.description}"
        dm_text += event_msg
        # 广播事件给所有玩家
        await manager.broadcast(game_id, {
            "type": "event",
            "event": event.model_dump(),
            "timestamp": now()
        })

    await manager.broadcast(game_id, {
        "type": "dm",
        "content": dm_text,
        "timestamp": now()
    })


async def generate_npc_response(game_id: str, player: Player, npc: NPC):
    """生成NPC响应"""
    game = game_manager.get_game_by_id(game_id)
    if not game:
        return

    # 使用AI服务获取NPC对话
    dialogue = AIService.generate_npc_dialogue(npc.model_dump(), context)

    # 根据NPC性格选择称呼
    if npc.disposition == "friendly":
        greeting = f"{npc.name}微笑着看向你："
    elif npc.disposition == "hostile":
        greeting = f"{npc.name}警惕地盯着你："
    else:
        greeting = f"{npc.name}看了你一眼："

    full_response = f"{greeting}\n\"{dialogue}\""

    await manager.broadcast(game_id, {
        "type": "npc",
        "npc_id": npc.npc_id,
        "npc_name": npc.name,
        "content": full_response,
        "timestamp": now()
    })

    # 检查交互事件触发
    triggered_events = EventGenerator.check_and_trigger_events(game, "interaction", npc_id=npc.npc_id)
    for event in triggered_events:
        event_msg = f"\n【事件触发】{event.title}\n{event.description}"
        await manager.broadcast(game_id, {
            "type": "event",
            "event": event.model_dump(),
            "timestamp": now()
        })


# ============================================
# 启动
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6006)
