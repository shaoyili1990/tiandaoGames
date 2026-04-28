"""
天道 TRPG Party - 服务器主入口

基于 FastAPI + WebSocket 的多玩家 TRPG 服务器
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional, Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# 数据模型
# ============================================

class User(BaseModel):
    user_id: str = ""
    device_id: str = ""
    nickname: str = ""
    email: Optional[str] = None

class Player(BaseModel):
    player_id: str
    user_id: Optional[str] = None
    nickname: str
    is_core: bool = True
    is_online: bool = False
    is_ai_controlled: bool = False

    # 角色数据
    character_name: str = ""
    mbti: str = "INFJ"
    base_y: int = 50
    current_y: int = 50

    # 关系
    relationships: Dict[str, int] = {}

class GameRecord(BaseModel):
    game_id: str = ""
    name: str = ""
    owner_id: str = ""
    room_code: str = ""

    # 成员
    core_members: List[Player] = []
    temp_members: List[Player] = []

    # 状态
    status: str = "waiting"  # waiting / playing / paused / ended
    created_at: str = ""
    last_played: str = ""

    # 世界状态
    world_name: str = ""
    current_location: str = ""
    game_time: str = "day"
    npcs: List[dict] = []
    events: List[dict] = []

# ============================================
# 连接管理器
# ============================================

class ConnectionManager:
    """管理所有 WebSocket 连接"""

    def __init__(self):
        # game_id -> List[WebSocket]
        self.game_connections: Dict[str, List[WebSocket]] = {}
        # player_id -> WebSocket
        self.player_connections: Dict[str, WebSocket] = {}
        # player_id -> game_id
        self.player_games: Dict[str, str] = {}

    async def connect(self, websocket: WebSocket, game_id: str, player_id: str):
        await websocket.accept()

        if game_id not in self.game_connections:
            self.game_connections[game_id] = []
        self.game_connections[game_id].append(websocket)
        self.player_connections[player_id] = websocket
        self.player_games[player_id] = game_id

        logger.info(f"Player {player_id} connected to game {game_id}")

    def disconnect(self, game_id: str, player_id: str):
        if game_id in self.game_connections:
            ws = self.player_connections.get(player_id)
            if ws and ws in self.game_connections[game_id]:
                self.game_connections[game_id].remove(ws)

        self.player_connections.pop(player_id, None)
        self.player_games.pop(player_id, None)

        logger.info(f"Player {player_id} disconnected from game {game_id}")

    async def broadcast(self, game_id: str, message: dict, exclude: Optional[str] = None):
        if game_id not in self.game_connections:
            return

        disconnected = []
        for ws in self.game_connections[game_id]:
            # 获取该 WS 对应的 player_id
            player_id = self._find_player_by_ws(game_id, ws)
            if player_id == exclude:
                continue

            try:
                await ws.send_json(message)
            except:
                disconnected.append(ws)

        # 清理断开的连接
        for ws in disconnected:
            if ws in self.game_connections[game_id]:
                self.game_connections[game_id].remove(ws)

    def _find_player_by_ws(self, game_id: str, ws: WebSocket) -> Optional[str]:
        for pid, wsc in self.player_connections.items():
            if wsc == ws and self.player_games.get(pid) == game_id:
                return pid
        return None

    async def send_to(self, player_id: str, message: dict):
        ws = self.player_connections.get(player_id)
        if ws:
            await ws.send_json(message)

manager = ConnectionManager()

# ============================================
# 游戏状态管理
# ============================================

class GameManager:
    """管理所有游戏状态"""

    def __init__(self):
        # game_id -> GameRecord
        self.games: Dict[str, GameRecord] = {}
        # room_code -> game_id
        self.room_codes: Dict[str, str] = {}
        # player_id -> Player
        self.players: Dict[str, Player] = {}

    def generate_room_code(self) -> str:
        """生成4位房间码"""
        import random
        import string
        code = ''.join(random.choices(string.ascii_uppercase, k=4))
        while code in self.room_codes:
            code = ''.join(random.choices(string.ascii_uppercase, k=4))
        return code

    def create_game(self, owner_id: str, owner_nickname: str, game_name: str) -> GameRecord:
        """创建新游戏"""
        game_id = str(uuid.uuid4())[:8]
        room_code = self.generate_room_code()

        # 房主作为核心成员
        owner = Player(
            player_id=owner_id,
            nickname=owner_nickname,
            is_core=True,
            is_online=True
        )

        game = GameRecord(
            game_id=game_id,
            name=game_name,
            owner_id=owner_id,
            room_code=room_code,
            core_members=[owner],
            created_at=datetime.now().isoformat(),
            last_played=datetime.now().isoformat()
        )

        self.games[game_id] = game
        self.room_codes[room_code] = game_id
        self.players[owner_id] = owner

        logger.info(f"Game {game_id} created with room code {room_code}")
        return game

    def join_game(self, room_code: str, player_id: str, nickname: str, is_core: bool = True) -> Optional[GameRecord]:
        """加入游戏"""
        game_id = self.room_codes.get(room_code)
        if not game_id:
            return None

        game = self.games.get(game_id)
        if not game:
            return None

        player = Player(
            player_id=player_id,
            nickname=nickname,
            is_core=is_core,
            is_online=True
        )

        if is_core:
            game.core_members.append(player)
        else:
            game.temp_members.append(player)

        self.players[player_id] = player
        logger.info(f"Player {player_id} joined game {game_id} as {'core' if is_core else 'temp'}")

        return game

    def leave_game(self, game_id: str, player_id: str):
        """离开游戏"""
        game = self.games.get(game_id)
        if not game:
            return

        # 从核心或临时成员中移除
        game.core_members = [p for p in game.core_members if p.player_id != player_id]
        game.temp_members = [p for p in game.temp_members if p.player_id != player_id]

        # 标记离线
        if player_id in self.players:
            self.players[player_id].is_online = False

        logger.info(f"Player {player_id} left game {game_id}")

    def get_player_game(self, player_id: str) -> Optional[GameRecord]:
        """获取玩家所在游戏"""
        game_id = self.player_games.get(player_id)
        if not game_id:
            return None
        return self.games.get(game_id)

    def get_all_online_players(self, game_id: str) -> List[Player]:
        """获取游戏所有在线玩家"""
        game = self.games.get(game_id)
        if not game:
            return []

        online = []
        for p in game.core_members + game.temp_members:
            if p.is_online:
                online.append(p)
        return online

    def get_missing_core_members(self, game_id: str) -> List[Player]:
        """获取缺席的核心成员"""
        game = self.games.get(game_id)
        if not game:
            return []

        return [p for p in game.core_members if not p.is_online]

game_manager = GameManager()

# ============================================
# FastAPI 应用
# ============================================

app = FastAPI(title="天道 TRPG Party", version="1.0.0")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="web/static"), name="static")

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
    return {"status": "ok", "version": "1.0.0"}

@app.post("/api/game/create")
async def create_game(request: dict):
    """创建新游戏"""
    owner_id = request.get("owner_id", str(uuid.uuid4()))
    owner_nickname = request.get("owner_nickname", "匿名")
    game_name = request.get("game_name", "新游戏")

    game = game_manager.create_game(owner_id, owner_nickname, game_name)

    return {
        "game_id": game.game_id,
        "room_code": game.room_code,
        "owner_id": owner_id
    }

@app.post("/api/game/join")
async def join_game(request: dict):
    """加入游戏"""
    room_code = request.get("room_code", "").upper()
    player_id = request.get("player_id", str(uuid.uuid4()))
    nickname = request.get("nickname", "匿名")

    if not room_code:
        raise HTTPException(status_code=400, detail="房间码不能为空")

    game = game_manager.join_game(room_code, player_id, nickname, is_core=True)

    if not game:
        raise HTTPException(status_code=404, detail="房间不存在")

    return {
        "game_id": game.game_id,
        "room_code": game.room_code,
        "player_id": player_id,
        "game": game.model_dump()
    }

@app.get("/api/game/{game_id}")
async def get_game(game_id: str):
    """获取游戏信息"""
    game = game_manager.games.get(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="游戏不存在")

    # 不返回离线成员
    online_game = game.model_dump()
    online_game["core_members"] = [p for p in game.core_members if p.is_online]
    online_game["temp_members"] = [p for p in game.temp_members if p.is_online]

    return online_game

# ============================================
# WebSocket 路由
# ============================================

@app.websocket("/ws/{game_id}/{player_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player_id: str):
    """WebSocket 连接"""

    # 获取玩家信息
    player = game_manager.players.get(player_id)
    if not player:
        await websocket.close(code=4001, reason="Player not found")
        return

    await manager.connect(websocket, game_id, player_id)

    # 通知所有人有新玩家加入
    await manager.broadcast(game_id, {
        "type": "player_joined",
        "player_id": player_id,
        "nickname": player.nickname,
        "is_core": player.is_core,
        "message": f"{player.nickname} 加入了游戏"
    })

    try:
        while True:
            data = await websocket.receive_json()
            await handle_message(game_id, player_id, data)

    except WebSocketDisconnect:
        manager.disconnect(game_id, player_id)
        game_manager.leave_game(game_id, player_id)

        # 通知所有人
        await manager.broadcast(game_id, {
            "type": "player_left",
            "player_id": player_id,
            "nickname": player.nickname,
            "message": f"{player.nickname} 离开了游戏"
        })

async def handle_message(game_id: str, player_id: str, data: dict):
    """处理玩家消息"""
    msg_type = data.get("type", "")
    player = game_manager.players.get(player_id)

    if msg_type == "chat":
        # 聊天消息
        content = data.get("content", "")

        await manager.broadcast(game_id, {
            "type": "chat",
            "player_id": player_id,
            "nickname": player.nickname,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

        # TODO: 调用天道DM处理
        # await dm_process(game_id, player, content)

    elif msg_type == "action":
        # 动作消息
        action = data.get("action", "")

        await manager.broadcast(game_id, {
            "type": "action",
            "player_id": player_id,
            "nickname": player.nickname,
            "action": action,
            "timestamp": datetime.now().isoformat()
        })

    elif msg_type == "ping":
        # 心跳
        await manager.send_to(player_id, {"type": "pong"})

# ============================================
# 启动
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
