"""
天道 TRPG Party - AI服务
处理DM响应和世界生成 - 使用MiniMax API
"""

import os
import json
import httpx
from typing import Dict, List, Optional
from datetime import datetime

# MiniMax API配置
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "sk-api-GPHHQZRj34gOKsKR746ttKxFLOFULRP_GlnDnbiZpfLEpIQnkGUmjE8oMIqqfENe7kdpAy2IWJslqDcEwESU7K4M-ijZlrONyti49UxNE8hF6OMIftM50Qs")
MINIMAX_API_HOST = os.getenv("MINIMAX_API_HOST", "https://api.minimaxi.com")

class AIService:
    """AI服务 - 使用MiniMax API"""

    @classmethod
    def _call_minimax(cls, messages: list, model: str = "MiniMax-Text-01", temperature: float = 0.7, max_tokens: int = 500) -> str:
        """调用MiniMax Chat API"""
        url = f"{MINIMAX_API_HOST}/v1/text/chatcompletion_v2"

        headers = {
            "Authorization": f"Bearer {MINIMAX_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            with httpx.Client(timeout=30.0) as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            print(f"[MiniMax API Error] {e}")
            return f"【系统消息】AI服务暂时不可用: {str(e)}"

    @classmethod
    def generate_dm_response(cls, game: dict, player: dict, message: str) -> str:
        """生成天道DM响应 - 调用MiniMax"""
        world = game.get("world", {})
        world_name = world.get("name", "未知世界")
        world_overview = world.get("overview", "")
        current_location_id = world.get("current_location_id")
        locations = world.get("locations", {})
        npcs = world.get("npcs", {})

        current_location = locations.get(current_location_id, {}) if current_location_id else {}
        location_name = current_location.get("name", "酒馆")
        location_desc = current_location.get("description", "")
        location_atmosphere = current_location.get("atmosphere", "")

        # 获取在场NPC
        present_npcs = []
        for npc_id, npc in npcs.items():
            if npc.get("location") == current_location_id:
                present_npcs.append(npc.get("name", "某人"))

        npc_str = "、".join(present_npcs) if present_npcs else "暂无其他人"

        system_prompt = f"""你是天道TRPG的DM。你为玩家创造沉浸式的跑团体验。
当前世界：{world_name}
世界背景：{world_overview}
当前位置：{location_name}
地点描述：{location_desc}
场所氛围：{location_atmosphere}
在场人物：{npc_str}

玩家({player.get('nickname', '匿名冒险者')})说: {message}

请以天道DM的身份，用1-2句话沉浸式地回应玩家。保持中文，语言生动有画面感。"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]

        return cls._call_minimax(messages, temperature=0.8)

    @classmethod
    def generate_world_ai(cls, player_count: int = 4, world_description: str = "") -> dict:
        """AI生成独特世界 - 调用MiniMax"""
        scale_hints = {
            1: "适合单人探索的、私密且聚焦的、个人成长之旅",
            2: "小规模冒险的、紧凑而精彩的、小队闯荡的",
            3: "小规模冒险的、紧凑而精彩的、小队闯荡的",
            5: "中型团队的、有深度的、多线叙事的",
        }
        default_scale = "大型史诗级的、多阵营的、宏大叙事的"
        scale = scale_hints.get(player_count, default_scale)

        system_prompt = f"""你是天道TRPG的世界生成器。你根据玩家数量和描述，生成独特的游戏世界。

玩家数量：{player_count}人
世界规模感：{scale}
玩家描述：{world_description or '自由发挥'}

请生成一个独特的游戏世界，返回JSON格式：
{{
    "name": "世界名称（简洁有特色）",
    "overview": "世界观概述（2-3句话）",
    "world_type": "fantasy/urban/sci_fi/infinite_flow/baldurs_gate",
    "atmosphere_keywords": ["关键词1", "关键词2", "关键词3"],
    "locations": [
        {{"name": "地点1", "description": "描述", "atmosphere": "氛围"}},
        {{"name": "地点2", "description": "描述", "atmosphere": "氛围"}}
    ],
    "npcs": [
        {{"name": "NPC名", "role": "merchant/guard/innkeeper", "disposition": "friendly/neutral/hostile"}}
    ]
}}

只返回JSON，不要其他内容。"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"生成{player_count}人跑团的世界"}
        ]

        result = cls._call_minimax(messages, temperature=0.9, max_tokens=1000)

        # 尝试解析JSON
        try:
            # 提取JSON部分
            if "```json" in result:
                result = result.split("```json")[1].split("```")[0]
            elif "```" in result:
                result = result.split("```")[1].split("```")[0]

            return json.loads(result.strip())
        except:
            # 解析失败返回默认
            return cls._fallback_world(player_count)

    @classmethod
    def generate_npc_dialogue(cls, npc: dict, context: str = "") -> str:
        """生成NPC对话 - 调用MiniMax"""
        npc_name = npc.get("name", "某人")
        npc_role = npc.get("role", "merchant")
        npc_disposition = npc.get("disposition", "neutral")
        npc_personality = npc.get("personality", "")

        system_prompt = f"""你是{npc_name}，一个{npc_role}。
性格：{npc_personality}
态度：{npc_disposition}

请根据你的身份和性格，用1句话回应玩家的互动。
保持简洁，符合角色特点。"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context or "你好"}
        ]

        return cls._call_minimax(messages, temperature=0.7)

    @classmethod
    def generate_action_response(cls, action: str, player: dict, game: dict) -> str:
        """生成动作响应 - 调用MiniMax"""
        player_name = player.get("nickname", "冒险者")
        world = game.get("world", {})
        location_name = world.get("locations", {}).get(world.get("current_location_id"), {}).get("name", "某地")

        system_prompt = f"""你是天道TRPG的DM。玩家{player_name}在{location_name}执行了一个动作。
动作：{action}

请用1句话描述这个动作的结果，保持沉浸感和画面感。"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": action}
        ]

        return cls._call_minimax(messages, temperature=0.8)

    @classmethod
    def _fallback_world(cls, player_count: int) -> dict:
        """静态备用世界（仅在API失败时使用）"""
        return {
            "name": "天道世界",
            "overview": "天道运转的世界，一切皆有可能。",
            "world_type": "fantasy",
            "atmosphere_keywords": ["神秘", "冒险", "探索"],
            "locations": [
                {"name": "酒馆", "description": "一间烟雾缭绕的酒馆，温暖的火光来自壁炉。", "atmosphere": "热闹而嘈杂"},
                {"name": "街道", "description": "一条繁忙的街道，两旁是各种店铺。", "atmosphere": "人来人往"}
            ],
            "npcs": [
                {"name": "酒馆老板", "role": "merchant", "disposition": "friendly"}
            ]
        }
