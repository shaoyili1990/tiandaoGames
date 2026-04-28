"""
天道 TRPG Party - AI服务
处理DM响应和世界生成
"""

import os
import json
import random
from typing import Dict, List, Optional
from datetime import datetime

# AI配置
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")


class AIService:
    """AI服务（简化版，不依赖外部API）"""

    # NPC对话模板
    NPC_TEMPLATES = {
        "innkeeper": {
            "friendly": [
                "欢迎光临！今天想来点什么？",
                "哟，贵客来了！请坐请坐！",
                "这位客官面生啊，第一次来吧？"
            ],
            "neutral": [
                "嗯...要点什么？",
                "后面排队。",
                "等着。"
            ],
            "hostile": [
                "你瞅啥？",
                "找事儿的吧？",
                "滚。"
            ]
        },
        "guard": {
            "friendly": [
                "辛苦了！请进吧。",
                "长官好！",
                "例行检查，请配合。"
            ],
            "neutral": [
                "站住，什么事？",
                "通行证。",
                "闲杂人等不得靠近。"
            ],
            "hostile": [
                "再往前一步就别怪我不客气了！",
                "想死？",
                "滚远点！"
            ]
        },
        "merchant": {
            "friendly": [
                "来来来，看看这好东西！",
                "保证正品，价格公道！",
                "童叟无欺，货真价实！"
            ],
            "neutral": [
                "买东西？自己看。",
                "价格单在那儿。",
                "不还价。"
            ],
            "hostile": [
                "穷鬼别碰！",
                "买不起别看！",
                "滚！"
            ]
        },
        "waiter": {
            "friendly": [
                "客官里边请！",
                "小二，上茶！",
                "客官要点什么？"
            ],
            "neutral": [
                "催什么催。",
                "等着。",
                "急什么。"
            ],
            "hostile": [
                "去去去，没位置了。",
                "滚出去！",
                "别烦我。"
            ]
        },
        "bartender": {
            "friendly": [
                "想喝点什么？",
                "今晚想听点什么故事？",
                "新面孔啊，第一次来？"
            ],
            "neutral": [
                "老样子？",
                "喝什么自己点。",
                "等着。"
            ],
            "hostile": [
                "我不喜欢你的态度。",
                "出去清醒清醒再来。",
                "滚。"
            ]
        },
        "default": {
            "friendly": ["你好。", "幸会幸会。", "请多指教。"],
            "neutral": ["嗯。", "是吗。", "然后呢。"],
            "hostile": ["滚。", "别烦我。", "找事儿？"]
        }
    }

    # DM描述模板 - 丰富的沉浸式描述
    DM_TEMPLATES = {
        "arrival": [
            "你来到了{location}。{description}",
            "你走进了{location}。{description}",
            "你踏入{location}，{atmosphere}。{description}"
        ],
        "atmosphere": [
            "空气中弥漫着{feeling}的气息。",
            "这里给人的感觉是{feeling}。",
            "{feeling}的气氛笼罩着整个空间。"
        ],
        "npc_present": [
            "在场的NPC有：{npcs}。他们似乎在忙着自己的事情。",
            "你注意到{npcs}也在这里，目光偶尔扫过你。",
            "{npcs}正注视着你，似乎在打量你这个外来者。"
        ],
        "npc_interaction": [
            "{npc}似乎注意到了你，抬起头来...",
            "{npc}主动向你走来，似乎有话要说...",
            "你的目光与{npc}相遇，对方微微点头示意。"
        ],
        "observation": [
            "你仔细打量着这里的一切...",
            "你的目光扫过每一个角落，注意到{details}",
            "你静静地观察着周围，{observation}"
        ],
        "time_of_day": {
            "dawn": "晨曦初现，天边泛着鱼肚白，露珠在草叶上闪烁。",
            "day": "阳光明媚，{location}里人来人往，一派热闹景象。",
            "dusk": "夕阳西下，天边染上了橙红色的晚霞，归巢的鸟儿掠过天空。",
            "night": "夜幕降临，星光点点，月光洒落，给一切都披上了一层银纱。"
        }
    }

    # 动作响应 - 沉浸式
    ACTION_RESPONSES = {
        "look_around": [
            "你环顾四周，仔细打量着这里的一切。",
            "你的目光扫过每一个角落，试图发现什么有趣的东西。",
            "你静静地观察着周围的环境和人。"
        ],
        "observe": [
            "你仔细观察着周围的一切...",
            "你的目光扫过每一个细节...",
            "你留意着周围的动静..."
        ],
        "talk": [
            "你开口说话，希望能引起别人的注意。",
            "你主动与身边的人攀谈起来。",
            "你尝试与周围的人交流。"
        ],
        "chat": [
            "你开口说话，希望能引起别人的注意。",
            "你主动与身边的人攀谈起来。",
            "你尝试与周围的人交流。"
        ],
        "explore": [
            "你决定四处走走，探索一下这个地方。",
            "你沿着街道漫步，观察着周围的一切。",
            "你深入探索这个区域的各个角落。"
        ],
        "search": [
            "你仔细搜寻可能遗漏的细节...",
            "你翻找着可能有用或有趣的东西...",
            "你的目光在搜寻任何有价值的目标..."
        ],
        "fight": [
            "你摆出战斗姿态，警惕地注视着对方！",
            "气氛骤然紧张起来，一场冲突似乎不可避免...",
            "你做好了战斗准备，随时可能出手。"
        ],
        "sneak": [
            "你放轻脚步，小心翼翼地移动，避免引起注意...",
            "你试图悄悄行动，不惊动周围的人...",
            "你隐蔽着自己的身形，悄然靠近目标..."
        ],
        "default": [
            "你做出了这个动作。",
            "你尝试着...",
            "你进行了这个行为。"
        ]
    }

    # 世界特定的观察细节
    WORLD_OBSERVATION = {
        "fantasy": {
            "details": [
                "客栈的角落里有人在低声交谈", "墙上贴着通缉令和寻人告示",
                "有人腰间佩剑，气质不凡", "柜台上的账本翻得飞快",
                "空气中隐约有灵气的波动"
            ],
            "npc_activities": [
                "有的修士在角落里打坐修炼", "几个江湖客在划拳喝酒",
                "小二忙进忙出地招呼客人", "一个神秘人独自坐在阴影中"
            ]
        },
        "urban": {
            "details": [
                "霓虹灯闪烁，车辆川流不息", "路边的小吃摊飘来阵阵香味",
                "上班族行色匆匆", "商店橱窗里陈列着各种商品",
                "地铁站入口人来人往"
            ],
            "npc_activities": [
                "有人在打电话，声音急促", "情侣手牵手漫步",
                "学生们背着书包匆匆走过", "老人在下棋聊天"
            ]
        },
        "sci_fi": {
            "details": [
                "全息广告在头顶闪烁", "飞行器在天际穿梭",
                "机器人服务员在忙碌", "人们戴着各种增强现实设备",
                "巨大的电子屏幕显示着新闻和广告"
            ],
            "npc_activities": [
                "有人正在和AI助手对话", "赏金猎人在检查武器",
                "黑客在角落里的终端上敲打", "贵族在私人包厢里交谈"
            ]
        }
    }

    @classmethod
    def get_npc_dialogue(cls, npc: dict, context: str = "neutral") -> str:
        """获取NPC对话"""
        role = npc.get("role", "default").lower()
        templates = cls.NPC_TEMPLATES.get(role, cls.NPC_TEMPLATES["default"])

        disposition = npc.get("disposition", "neutral")
        dialogues = templates.get(disposition, templates["neutral"])

        return random.choice(dialogues)

    @classmethod
    def generate_dm_description(cls, game: dict, context: dict) -> str:
        """生成天道DM描述"""
        world = game.get("world", {})
        location_id = world.get("current_location_id")
        locations = world.get("locations", {})
        npcs = world.get("npcs", {})
        game_time = world.get("game_time", "day")
        world_type = world.get("world_type", "fantasy")

        parts = []

        # 位置描述
        if location_id and location_id in locations:
            loc = locations[location_id]
            desc = loc.get("description", "")

            # 获取世界特定的观察细节
            world_obs = cls.WORLD_OBSERVATION.get(world_type, {})
            details = world_obs.get("details", ["一切都很平常"])

            template = random.choice(cls.DM_TEMPLATES["arrival"])
            parts.append(template.format(
                location=loc.get("name", "未知地点"),
                atmosphere=loc.get("atmosphere", ""),
                description=desc
            ))

            # 添加世界特定的细节
            if random.random() > 0.5:  # 50%几率添加额外细节
                parts.append(f"你注意到：{random.choice(details)}。")

        # 时间描述
        time_template = cls.DM_TEMPLATES["time_of_day"].get(game_time, "")
        if time_template and location_id and location_id in locations:
            parts.append(time_template.format(location=locations[location_id].get("name", "")))

        # NPC描述
        present_npcs = []
        for npc_id, npc in npcs.items():
            if npc.get("location") == location_id:
                present_npcs.append(npc.get("name", "某人"))

        if present_npcs:
            template = random.choice(cls.DM_TEMPLATES["npc_present"])
            nppc_str = "、".join(present_npcs[:3])
            if len(present_npcs) > 3:
                nppc_str += f"等{len(present_npcs)}人"
            parts.append(template.format(npcs=nppc_str))

            # 添加NPC活动描述
            world_obs = cls.WORLD_OBSERVATION.get(world_type, {})
            npc_activities = world_obs.get("npc_activities", [])
            if npc_activities and random.random() > 0.5:
                parts.append(random.choice(npc_activities))

        return "【天道】" + "\n\n".join(parts)

    @classmethod
    def generate_action_response(cls, action: str, player: dict, game: dict) -> str:
        """生成动作响应"""
        action_lower = action.lower()

        # 识别动作类型
        response_type = "default"
        for key in cls.ACTION_RESPONSES.keys():
            if key in action_lower:
                response_type = key
                break

        templates = cls.ACTION_RESPONSES.get(response_type, cls.ACTION_RESPONSES["default"])
        response = random.choice(templates)

        # 获取世界类型
        world_type = game.get("world", {}).get("world_type", "fantasy")
        world_obs = cls.WORLD_OBSERVATION.get(world_type, {})

        # 添加世界特定的细节
        if random.random() > 0.3:  # 70%几率添加细节
            details = world_obs.get("details", [])
            if details:
                response += f"\n{random.choice(details)}。"

        return f"【{player.get('nickname', '你')}】{action}\n\n【天道】{response}"

    @classmethod
    def generate_world(cls, world_type: str, user_prompt: str = "") -> dict:
        """生成世界（简化版）"""
        worlds = {
            "fantasy": {
                "name": random.choice(["天元大陆", "青云界", "玄黄世界", "沧溟仙域"]),
                "overview": "一个修仙者和凡人共存的世界，门派林立，机遇与危险并存。",
                "atmosphere_keywords": ["仙侠", "修炼", "门派", "冒险"]
            },
            "urban": {
                "name": random.choice(["滨海市", "江城", "龙都市", "云海市"]),
                "overview": "一个繁华的现代都市，高楼林立，车水马龙。",
                "atmosphere_keywords": ["都市", "繁华", "霓虹", "现代"]
            },
            "sci_fi": {
                "name": random.choice(["新伊甸园", "星海城", "赛博都会", "明日都市"]),
                "overview": "一个科技高度发达的未来都市，人工智能和人类共同生活。",
                "atmosphere_keywords": ["科幻", "赛博", "未来", "科技"]
            }
        }

        world = worlds.get(world_type, worlds["fantasy"])
        return world

    @classmethod
    def generate_world_ai(cls, player_count: int = 4, world_description: str = "") -> dict:
        """AI根据玩家描述生成独特世界(无固定模板)"""
        import random

        # 根据玩家数量确定世界规模
        if player_count == 1:
            scale_hints = ["适合单人探索的", "私密且聚焦的", "个人成长之旅"]
        elif player_count <= 3:
            scale_hints = ["小规模冒险的", "紧凑而精彩的", "小队闯荡的"]
        elif player_count <= 5:
            scale_hints = ["中型团队的", "有深度的", "多线叙事的"]
        else:
            scale_hints = ["大型史诗级的", "多阵营的", "宏大叙事的"]

        # 基础元素(用于组合生成)
        setting_elements = {
            "背景": ["古代江湖", "现代都市", "未来星际", "中古奇幻", "赛博朋克", "仙侠世界", "末日废土", "维多利亚时代", "战国乱世", "北宋市井", "抗日战争", "三国争霸", "赛博都市", "魔法大陆", "深海遗迹", "空中帝国"],
            "氛围": ["悬疑推理", "热血战斗", "政治阴谋", "商业博弈", "探险解谜", "浪漫情缘", "复仇史诗", "救赎之旅", "权谋斗争", "生态危机", "遗迹探索", "文明兴衰", "星际战争", "时间循环", "身份追寻", "禁忌研究"],
            "特殊元素": ["武侠门派", "侦探事务所", "星际飞船", "魔法学院", "古老神社", "跨国企业", "秘密结社", "古老遗迹", "变异生物", "AI觉醒", "时间裂隙", "镜像世界", "平行宇宙", "古代神话", "生化危机", "心灵感应"]
        }

        # 如果有用户描述,提取关键词
        user_keywords = []
        if world_description:
            user_keywords = world_description.lower().split()

        # 组合生成独特世界
        bg = random.choice(setting_elements["背景"])
        atm = random.choice(setting_elements["氛围"])
        spec = random.choice(setting_elements["特殊元素"])
        scale = random.choice(scale_hints)

        # 生成世界名
        name_templates = [
            f"{bg}{atm}世界",
            f"{atm}的{bg}",
            f"{spec}之{bg}",
            f"{bg}：{atm}纪元",
            f"{scale}{atm}{bg}"
        ]
        name = random.choice(name_templates)

        # 生成世界概述
        overview_templates = [
            f"这是一个{scale}故事。背景是{bg},主线围绕{atm}展开,玩家将遇到{spec}等元素。",
            f"在{bg}的世界里,{atm}是永恒的主题。{spec}的出现让局势变得更加复杂...",
            f"当{bg}遇上了{atm},一切开始变得不一样。玩家们将在{spec}的伴随下,经历一段难忘的旅程。",
            f"{scale}的故事正在{bg}上演。{atm}的力量在暗中涌动,而{spec}或许是改变一切的关键。",
            f"在{bg}的{bg}中,{atm}每天都在上演。某一天,{spec}的出现彻底改变了局面..."
        ]
        overview = random.choice(overview_templates)

        # 生成氛围关键词
        atmosphere_keywords = [atm, bg, spec, atm + "2.0", bg + "时代", "探索"]

        # 生成地点
        locations = []
        loc_names = [
            f"{bg}中心", f"{spec}总部", f"{atm}酒馆", f"古老遗迹",
            f"{bg}边境", f"秘密基地", f"交汇之地", f"废弃城区"
        ]
        for loc_name in loc_names[:5]:
            loc = {
                "name": loc_name,
                "description": f"位于{bg}的{loc_name},这里是{atm}的核心地带。",
                "exits": ["北方", "南方", "东方", "西方"][:random.randint(2, 4)],
                "atmosphere": atm
            }
            locations.append(loc)

        # 生成NPC
        from character_cards import generate_npc
        npcs = []
        for i in range(8):
            npc = generate_npc()
            npcs.append({
                "id": npc["id"],
                "name": npc["name"],
                "race": npc["race"],
                "class": npc["class"],
                "personality": npc["personality"],
                "appearance": npc["appearance"],
                "backstory": npc["backstory"],
                "voice_style": npc["voice_style"],
                "disposition": random.choice(["friendly", "neutral", "hostile"])
            })

        return {
            "name": name,
            "overview": overview,
            "atmosphere_keywords": atmosphere_keywords,
            "locations": locations,
            "npcs": npcs,
            "player_count": player_count,
            "generated_from": world_description or "AI自主生成"
        }


# 全局实例
ai_service = AIService()
