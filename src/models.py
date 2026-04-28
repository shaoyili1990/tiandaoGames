"""
天道 TRPG Party - 数据模型
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
import uuid


def generate_id() -> str:
    """生成短ID"""
    return str(uuid.uuid4())[:8]


def now() -> str:
    """当前时间ISO格式"""
    return datetime.now().isoformat()


# ============================================
# 用户 & 认证
# ============================================

class User(BaseModel):
    user_id: str = Field(default_factory=generate_id)
    device_id: str = ""
    nickname: str = ""
    email: Optional[str] = None
    created_at: str = Field(default_factory=now)
    last_login: str = Field(default_factory=now)


# ============================================
# 角色
# ============================================

class Character(BaseModel):
    name: str = ""
    title: str = ""
    description: str = ""

    # 基础属性 (D&D风格)
    strength: int = 10      # 力量
    dexterity: int = 10    # 敏捷
    constitution: int = 10 # 体质
    intelligence: int = 10 # 智力
    wisdom: int = 10       # 感知
    charisma: int = 10      # 魅力

    # 天道属性
    mbti: str = "INFJ"
    base_y: int = 50
    instinct_type: str = "expression"  # 本能类型
    moral_sensitivity: str = "normal"  # 道德敏感度

    # 背景
    background: str = ""
    skills: List[str] = []
    inventory: List[str] = []

    def to_dict(self) -> dict:
        return self.model_dump()


# ============================================
# 玩家
# ============================================

class Player(BaseModel):
    player_id: str = Field(default_factory=generate_id)
    user_id: Optional[str] = None
    nickname: str = ""

    # 成员类型
    is_core: bool = True  # True=核心成员, False=临时成员
    is_online: bool = False
    is_ai_controlled: bool = False

    # 角色
    character: Character = Field(default_factory=Character)

    # 天道心理状态
    y_value: int = 50
    base_y: int = 50

    # 关系 (player_id -> 关系值)
    relationships: Dict[str, int] = {}

    # 在线玩家ID列表 (用于追踪谁在这个玩家的视野里)
    visible_players: List[str] = []

    # 游戏配置
    player_count: int = 4  # 期望的玩家数量
    world_description: str = ""  # 用户描述想要的世界

    def get_display_name(self) -> str:
        """获取显示名称"""
        name = self.nickname
        if self.is_ai_controlled:
            name += " [AI托管]"
        elif not self.is_online:
            name += " [离线]"
        return name


# ============================================
# NPC
# ============================================

class NPC(BaseModel):
    npc_id: str = Field(default_factory=generate_id)
    name: str = ""
    role: str = ""  # merchant, guard, quest_giver, etc.
    disposition: str = "neutral"  # friendly, hostile, neutral

    # 外观描述
    appearance: str = ""
    personality: str = ""

    # 天道属性
    mbti: str = "ISTJ"
    y_value: int = 50
    base_y: int = 50

    # 状态
    location: str = ""
    current_goal: str = ""
    awareness_level: str = "ignorant"  # ignorant, suspicious, aware

    # 能力
    dialogue_style: str = ""
    knowledge: List[str] = []

    # 关系
    relationships: Dict[str, int] = {}  # 对玩家的关系

    def to_summary(self) -> dict:
        """返回摘要信息（用于发送给客户端）"""
        return {
            "npc_id": self.npc_id,
            "name": self.name,
            "role": self.role,
            "disposition": self.disposition,
            "appearance": self.appearance,
        }


# ============================================
# 位置/场景
# ============================================

class Location(BaseModel):
    location_id: str = Field(default_factory=generate_id)
    name: str = ""
    description: str = ""

    # 场景细节
    atmosphere: str = ""  # 氛围描述
    exits: List[str] = []  # 出口方向
    items: List[str] = []  # 可交互物品

    # 在场NPC
    present_npcs: List[str] = []

    # 在场玩家
    present_players: List[str] = []

    # 事件
    active_events: List[str] = []


# ============================================
# 世界
# ============================================

class World(BaseModel):
    world_id: str = Field(default_factory=generate_id)
    name: str = ""
    world_type: str = ""  # fantasy, urban, sci_fi, etc.

    # 设定
    overview: str = ""  # 世界概述
    geography: str = ""  # 地理
    factions: str = ""  # 势力
    rules: str = ""  # 规则

    # 氛围关键词
    atmosphere_keywords: List[str] = []

    # 位置
    locations: Dict[str, Location] = {}
    current_location_id: str = ""

    # NPC库
    npcs: Dict[str, NPC] = {}

    # 游戏时间
    game_time: str = "day"  # day, night, dawn, dusk
    game_date: str = ""

    def get_current_location(self) -> Optional[Location]:
        """获取当前位置"""
        return self.locations.get(self.current_location_id)


# ============================================
# 事件
# ============================================

class EventChoice(BaseModel):
    choice_id: str = Field(default_factory=generate_id)
    text: str = ""
    outcome: str = ""  # 描述选择后的结果
    effects: List[str] = []  # 效果列表


class GameEvent(BaseModel):
    event_id: str = Field(default_factory=generate_id)
    title: str = ""
    description: str = ""

    event_type: str = "plot"  # plot, random, trigger

    # 触发条件
    trigger_type: str = ""  # time, location, interaction, condition, random
    trigger_condition: Dict = {}

    # 选项
    choices: List[EventChoice] = []

    # 效果
    effects: List[str] = []

    # 状态
    status: str = "pending"  # pending, active, completed, failed


# ============================================
# 游戏记录
# ============================================

class Save(BaseModel):
    save_id: str = Field(default_factory=generate_id)
    created_at: str = Field(default_factory=now)
    created_by: str = ""  # player_id
    note: str = ""

    # 快照数据 (JSON)
    snapshot: Dict = {}


class GameRecord(BaseModel):
    game_id: str = Field(default_factory=generate_id)
    name: str = ""
    room_code: str = ""

    owner_id: str = ""  # 房主player_id

    # 成员
    core_members: List[Player] = []  # 核心成员（必须到场）
    temp_members: List[Player] = []  # 临时成员（可缺席）

    # 状态
    status: str = "waiting"  # waiting, playing, paused, ended
    created_at: str = Field(default_factory=now)
    last_played: str = Field(default_factory=now)

    # 世界
    world: World = Field(default_factory=World)

    # 游戏配置
    player_count: int = 4  # 期望玩家数量
    world_description: str = ""  # 用户描述想要的世界

    # 事件
    active_events: List[GameEvent] = []
    completed_event_ids: List[str] = []

    # 存档
    saves: List[Save] = []
    current_save_id: Optional[str] = None

    def get_all_players(self) -> List[Player]:
        """获取所有成员"""
        return self.core_members + self.temp_members

    def get_online_players(self) -> List[Player]:
        """获取在线成员"""
        return [p for p in self.get_all_players() if p.is_online]

    def get_offline_core_members(self) -> List[Player]:
        """获取离线核心成员"""
        return [p for p in self.core_members if not p.is_online]

    def get_player_by_id(self, player_id: str) -> Optional[Player]:
        """按ID获取玩家"""
        for p in self.get_all_players():
            if p.player_id == player_id:
                return p
        return None

    def get_npc_by_id(self, npc_id: str) -> Optional[NPC]:
        """按ID获取NPC"""
        return self.world.npcs.get(npc_id)

    def to_client_dict(self) -> dict:
        """转换为客户端可见的字典（隐藏敏感信息）"""
        data = self.model_dump()

        # 不发送给客户端的字段
        sensitive_fields = []

        return data


# ============================================
# 消息类型
# ============================================

class ChatMessage(BaseModel):
    type: str = "chat"
    player_id: str = ""
    nickname: str = ""
    content: str = ""
    timestamp: str = Field(default_factory=now)


class DMMessage(BaseModel):
    type: str = "dm"
    content: str = ""
    timestamp: str = Field(default_factory=now)


class NPCMessage(BaseModel):
    type: str = "npc"
    npc_id: str = ""
    npc_name: str = ""
    content: str = ""
    timestamp: str = Field(default_factory=now)


class EventMessage(BaseModel):
    type: str = "event"
    event_id: str = ""
    title: str = ""
    description: str = ""
    choices: List[dict] = []
    timestamp: str = Field(default_factory=now)


class SystemMessage(BaseModel):
    type: str = "system"
    content: str = ""
    timestamp: str = Field(default_factory=now)
