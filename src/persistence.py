"""
天道 TRPG Party - 存档系统
支持 SQLite 持久化存储
"""

import json
import os
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
import threading

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "tiandao.db")


def get_db():
    """获取数据库连接"""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库"""
    conn = get_db()
    cursor = conn.cursor()

    # 用户表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            device_id TEXT,
            email TEXT,
            nickname TEXT,
            created_at TEXT,
            last_login TEXT
        )
    """)

    # 游戏记录表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS games (
            game_id TEXT PRIMARY KEY,
            name TEXT,
            room_code TEXT,
            owner_id TEXT,
            status TEXT,
            world_data TEXT,
            created_at TEXT,
            last_played TEXT
        )
    """)

    # 玩家表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id TEXT PRIMARY KEY,
            game_id TEXT,
            user_id TEXT,
            nickname TEXT,
            is_core INTEGER,
            character_data TEXT,
            y_value INTEGER,
            FOREIGN KEY (game_id) REFERENCES games(game_id)
        )
    """)

    # 存档表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saves (
            save_id TEXT PRIMARY KEY,
            game_id TEXT,
            snapshot TEXT,
            note TEXT,
            created_by TEXT,
            created_at TEXT,
            FOREIGN KEY (game_id) REFERENCES games(game_id)
        )
    """)

    conn.commit()
    conn.close()


class SaveManager:
    """存档管理器"""

    _lock = threading.Lock()

    @classmethod
    def init(cls):
        """初始化数据库"""
        init_db()

    @classmethod
    def save_user(cls, user_data: dict) -> bool:
        """保存用户"""
        with cls._lock:
            conn = get_db()
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO users (user_id, device_id, email, nickname, created_at, last_login)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                user_data.get("user_id"),
                user_data.get("device_id"),
                user_data.get("email"),
                user_data.get("nickname"),
                user_data.get("created_at"),
                user_data.get("last_login", datetime.now().isoformat())
            ))

            conn.commit()
            conn.close()
            return True

    @classmethod
    def get_user(cls, user_id: str) -> Optional[dict]:
        """获取用户"""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)
        return None

    @classmethod
    def save_game(cls, game_data: dict) -> bool:
        """保存游戏"""
        with cls._lock:
            conn = get_db()
            cursor = conn.cursor()

            world_data = json.dumps(game_data.get("world_data", {}), ensure_ascii=False)

            cursor.execute("""
                INSERT OR REPLACE INTO games (game_id, name, room_code, owner_id, status, world_data, created_at, last_played)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                game_data.get("game_id"),
                game_data.get("name"),
                game_data.get("room_code"),
                game_data.get("owner_id"),
                game_data.get("status"),
                world_data,
                game_data.get("created_at"),
                game_data.get("last_played", datetime.now().isoformat())
            ))

            conn.commit()
            conn.close()
            return True

    @classmethod
    def get_game(cls, game_id: str) -> Optional[dict]:
        """获取游戏"""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM games WHERE game_id = ?", (game_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            data = dict(row)
            data["world_data"] = json.loads(data.get("world_data", "{}"))
            return data
        return None

    @classmethod
    def save_snapshot(cls, save_data: dict) -> bool:
        """保存存档快照"""
        with cls._lock:
            conn = get_db()
            cursor = conn.cursor()

            snapshot = json.dumps(save_data.get("snapshot", {}), ensure_ascii=False)

            cursor.execute("""
                INSERT INTO saves (save_id, game_id, snapshot, note, created_by, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                save_data.get("save_id"),
                save_data.get("game_id"),
                snapshot,
                save_data.get("note", ""),
                save_data.get("created_by", ""),
                save_data.get("created_at", datetime.now().isoformat())
            ))

            conn.commit()
            conn.close()
            return True

    @classmethod
    def get_saves(cls, game_id: str) -> List[dict]:
        """获取游戏的所有存档"""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM saves
            WHERE game_id = ?
            ORDER BY created_at DESC
        """, (game_id,))

        rows = cursor.fetchall()
        conn.close()

        saves = []
        for row in rows:
            data = dict(row)
            data["snapshot"] = json.loads(data.get("snapshot", "{}"))
            saves.append(data)

        return saves

    @classmethod
    def get_save(cls, save_id: str) -> Optional[dict]:
        """获取存档"""
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM saves WHERE save_id = ?", (save_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            data = dict(row)
            data["snapshot"] = json.loads(data.get("snapshot", "{}"))
            return data
        return None

    @classmethod
    def get_user_games(cls, user_id: str) -> List[dict]:
        """获取用户参与的所有游戏"""
        conn = get_db()
        cursor = conn.cursor()

        # 通过玩家表查找用户参与的游戏
        cursor.execute("""
            SELECT DISTINCT g.* FROM games g
            INNER JOIN players p ON g.game_id = p.game_id
            WHERE p.user_id = ?
            ORDER BY g.last_played DESC
        """, (user_id,))

        rows = cursor.fetchall()
        conn.close()

        games = []
        for row in rows:
            data = dict(row)
            data["world_data"] = json.loads(data.get("world_data", "{}"))
            games.append(data)

        return games

    @classmethod
    def delete_game(cls, game_id: str) -> bool:
        """删除游戏及所有关联数据"""
        with cls._lock:
            conn = get_db()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM saves WHERE game_id = ?", (game_id,))
            cursor.execute("DELETE FROM players WHERE game_id = ?", (game_id,))
            cursor.execute("DELETE FROM games WHERE game_id = ?", (game_id,))

            conn.commit()
            conn.close()
            return True


# 初始化数据库
SaveManager.init()
