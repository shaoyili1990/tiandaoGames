"""
天道 TRPG Party - 事件系统
"""

import random
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from models import GameEvent, EventChoice, generate_id, now


class EventTrigger:
    """事件触发器"""

    TRIGGER_TYPES = ["time", "location", "interaction", "condition", "random", "story"]

    @staticmethod
    def check_time_trigger(event: GameEvent, game) -> bool:
        """检查时间触发"""
        if event.trigger_type != "time":
            return False

        condition = event.trigger_condition or {}
        required_time = condition.get("game_time")

        if required_time and game.world.game_time == required_time:
            # 每天最多触发一次
            event_id = event.event_id
            if event_id not in game.completed_event_ids:
                return True
        return False

    @staticmethod
    def check_location_trigger(event: GameEvent, game, player_location: str) -> bool:
        """检查位置触发"""
        if event.trigger_type != "location":
            return False

        condition = event.trigger_condition or {}
        required_locations = condition.get("locations", [])

        if player_location in required_locations:
            event_id = event.event_id
            if event_id not in game.completed_event_ids:
                return True
        return False

    @staticmethod
    def check_interaction_trigger(event: GameEvent, game, interacted_npc: str) -> bool:
        """检查交互触发"""
        if event.trigger_type != "interaction":
            return False

        condition = event.trigger_condition or {}
        required_npcs = condition.get("npcs", [])

        if interacted_npc in required_npcs:
            event_id = event.event_id
            if event_id not in game.completed_event_ids:
                return True
        return False

    @staticmethod
    def check_random_trigger(event: GameEvent) -> bool:
        """检查随机触发"""
        if event.trigger_type != "random":
            return False

        condition = event.trigger_condition or {}
        probability = condition.get("probability", 0.1)  # 默认10%概率

        if random.random() < probability:
            if event.event_id not in getattr(event, '_triggered_ids', set()):
                return True
        return False

    @staticmethod
    def check_condition_trigger(event: GameEvent, game) -> bool:
        """检查条件触发"""
        if event.trigger_type != "condition":
            return False

        condition = event.trigger_condition or {}

        # 检查玩家属性条件
        if "min_y" in condition:
            # 需要特定玩家Y值
            pass

        # 检查物品条件
        if "required_items" in condition:
            # 需要特定物品
            pass

        return True


class EventGenerator:
    """事件生成器"""

    @staticmethod
    def generate_location_event(location_name: str, world_type: str) -> GameEvent:
        """根据位置生成随机事件"""
        events_pool = EventGenerator.get_events_for_location(location_name, world_type)
        if events_pool:
            return random.choice(events_pool)
        return None

    @staticmethod
    def get_events_for_location(location: str, world_type: str) -> List[GameEvent]:
        """获取位置对应的事件池"""
        all_events = [
            # 都市事件
            GameEvent(
                event_id=generate_id(),
                title="神秘顾客",
                description="一个戴着墨镜的神秘人走进店，目光在四周扫视...",
                event_type="random",
                trigger_type="location",
                trigger_condition={"locations": ["街边小吃店", "主干街道"]},
                choices=[
                    EventChoice(choice_id=generate_id(), text="上前搭话", outcome="你引起了神秘人的注意"),
                    EventChoice(choice_id=generate_id(), text="假装没看见", outcome="神秘人独自离开了")
                ],
                status="pending"
            ),
            GameEvent(
                event_id=generate_id(),
                title="突发情况",
                description="突然外面传来一阵骚动...",
                event_type="random",
                trigger_type="random",
                trigger_condition={"probability": 0.05},
                choices=[
                    EventChoice(choice_id=generate_id(), text="出去查看", outcome="你看到了令人惊讶的一幕"),
                    EventChoice(choice_id=generate_id(), text="留在原地", outcome="骚动很快平息了")
                ],
                status="pending"
            ),
            # 奇幻事件
            GameEvent(
                event_id=generate_id(),
                title="灵气波动",
                description="你感到周围的灵气突然波动，似乎有什么异宝出世...",
                event_type="random",
                trigger_type="location",
                trigger_condition={"locations": ["坊市街道", "城门外"]},
                choices=[
                    EventChoice(choice_id=generate_id(), text="循着波动探寻", outcome="你发现了一处隐秘的遗迹"),
                    EventChoice(choice_id=generate_id(), text="不为所动", outcome="有人已经循迹而去")
                ],
                status="pending"
            ),
            GameEvent(
                event_id=generate_id(),
                title="门派招新",
                description="一个大宗门正在坊市招收新弟子...",
                event_type="plot",
                trigger_type="location",
                trigger_condition={"locations": ["坊市街道"]},
                choices=[
                    EventChoice(choice_id=generate_id(), text="前去报名", outcome="你成功引起了长老的注意"),
                    EventChoice(choice_id=generate_id(), text="围观看看", outcome="你见证了一场精彩的对决")
                ],
                status="pending"
            ),
            # 科幻事件
            GameEvent(
                event_id=generate_id(),
                title="黑客入侵",
                description="全息广告屏突然闪烁，显示出一串神秘的代码...",
                event_type="random",
                trigger_type="location",
                trigger_condition={"locations": ["全息酒吧", "主干道"]},
                choices=[
                    EventChoice(choice_id=generate_id(), text="尝试解读代码", outcome="你获得了一段加密坐标"),
                    EventChoice(choice_id=generate_id(), text="忽略它", outcome="代码很快消失了")
                ],
                status="pending"
            ),
            GameEvent(
                event_id=generate_id(),
                title="机甲追逐",
                description="一辆军用机甲呼啸而过，似乎在追什么人...",
                event_type="random",
                trigger_type="random",
                trigger_condition={"probability": 0.03},
                choices=[
                    EventChoice(choice_id=generate_id(), text="跟踪机甲", outcome="你发现了一个秘密据点"),
                    EventChoice(choice_id=generate_id(), text="躲避", outcome="你躲过了一劫")
                ],
                status="pending"
            ),
        ]

        return all_events

    @staticmethod
    def check_and_trigger_events(game, trigger_type: str, **kwargs) -> List[GameEvent]:
        """检查并触发符合条件的事件"""
        triggered = []

        # 获取所有待触发事件
        for event in game.active_events:
            if event.status != "pending":
                continue

            should_trigger = False

            if trigger_type == "location" and event.trigger_type in ["location", "story"]:
                should_trigger = EventTrigger.check_location_trigger(event, game, kwargs.get("location", ""))

            elif trigger_type == "interaction" and event.trigger_type in ["interaction", "story"]:
                should_trigger = EventTrigger.check_interaction_trigger(event, game, kwargs.get("npc_id", ""))

            elif trigger_type == "time" and event.trigger_type in ["time", "story"]:
                should_trigger = EventTrigger.check_time_trigger(event, game)

            elif trigger_type == "random":
                should_trigger = EventTrigger.check_random_trigger(event)

            elif trigger_type == "story":
                # 剧情事件直接触发
                should_trigger = True

            if should_trigger:
                event.status = "active"
                triggered.append(event)

        return triggered


class EventManager:
    """事件管理器"""

    def __init__(self):
        self.event_queue: List[GameEvent] = []

    def add_event(self, event: GameEvent):
        """添加事件到队列"""
        self.event_queue.append(event)

    def get_active_events(self, game_id: str) -> List[GameEvent]:
        """获取活跃事件"""
        return [e for e in self.event_queue if e.status == "active"]

    def complete_event(self, event_id: str):
        """完成事件"""
        for event in self.event_queue:
            if event.event_id == event_id:
                event.status = "completed"
                break

    def handle_player_choice(self, event: GameEvent, choice_id: str) -> str:
        """处理玩家选择"""
        for choice in event.choices:
            if choice.choice_id == choice_id:
                event.status = "completed"
                return choice.outcome

        return "你没有做出选择"


# 全局实例
event_manager = EventManager()
