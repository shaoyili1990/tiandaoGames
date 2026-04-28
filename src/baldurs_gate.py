"""
天道 TRPG - 博德之门世界设定
基于D&D 5e规则,最经典的CRPG跑团题材

核心特色:
- D&D 5e规则 - 完整的职业/种族/技能系统
- 队友系统 - 最多4人队伍,AI同伴
- 自由度 - 战斗/潜行/说服/欺骗/探索多路径
- 丰富职业 - 战士/法师/游贼/圣武士/野蛮人等
- 阵营系统 - 九宫格阵营影响对话和任务

设计原则:
1. D20检定为核心
2. 六面骰(D6)用于伤害和辅助
3. 优势/劣势机制
4. 即时无离线收益
"""

import random

# ============================================
# 博德之门世界 - 核心设定
# ============================================
BALDRS_GATE_3 = {
    "name": "Baldur's Gate 3",
    "chinese_name": "博德之门3",
    "system_type": "baldurs_gate",
    "overview": "基于D&D 5e规则,扮演被脑蚀寄生的冒险者,在博德之门地区展开史诗旅程。召集同伴,对抗夺心魔,探索被遗忘的国度。",
    "source_docs": ["博德之门3游戏"],
    "gameplay_mode": "D&D 5e规则跑团",
    "max_players": 4,  # 标准队伍4人
    "estimated_duration": "60-120分钟一局",
    "complexity": "进阶级",  # 需要了解D&D 5e基础

    # D&D 5e 属性
    "ability_scores": [
        {"id": "strength", "name": "力量", "abbr": "STR", "desc": "肌肉力量和体力"},
        {"id": "dexterity", "name": "敏捷", "abbr": "DEX", "desc": "身体灵活性和反射"},
        {"id": "constitution", "name": "体质", "abbr": "CON", "desc": "耐力和健康"},
        {"id": "intelligence", "name": "智力", "abbr": "INT", "desc": "记忆和分析能力"},
        {"id": "wisdom", "name": "感知", "abbr": "WIS", "desc": "直觉、洞察和意志力"},
        {"id": "charisma", "name": "魅力", "abbr": "CHA", "desc": "社交能力和魔法亲和"}
    ],

    # D&D 5e 技能
    "skills": [
        {"id": "athletics", "name": "运动", "ability": "力量"},
        {"id": "acrobatics", "name": "杂技", "ability": "敏捷"},
        {"id": "sleight_of_hand", "name": "手上功夫", "ability": "敏捷"},
        {"id": "stealth", "name": "隐匿", "ability": "敏捷"},
        {"id": "arcana", "name": "奥秘", "ability": "智力"},
        {"id": "history", "name": "历史", "ability": "智力"},
        {"id": "investigation", "name": "调查", "ability": "智力"},
        {"id": "nature", "name": "自然", "ability": "智力"},
        {"id": "religion", "name": "宗教", "ability": "智力"},
        {"id": "animal_handling", "name": "动物处理", "ability": "感知"},
        {"id": "insight", "name": "洞察", "ability": "感知"},
        {"id": "medicine", "name": "医药", "ability": "感知"},
        {"id": "perception", "name": "感知", "ability": "感知"},
        {"id": "survival", "name": "生存", "ability": "感知"},
        {"id": "deception", "name": "欺骗", "ability": "魅力"},
        {"id": "intimidation", "name": "威吓", "ability": "魅力"},
        {"id": "performance", "name": "表演", "ability": "魅力"},
        {"id": "persuasion", "name": "说服", "ability": "魅力"}
    ],

    # 种族
    "races": [
        {"id": "human", "name": "人类", "bonus": "+1到两个不同属性", "traits": ["适应力", "多才多艺"]},
        {"id": "elf", "name": "精灵", "bonus": "+2敏捷,+1魅力", "traits": ["黑暗视觉", "精类血统"]},
        {"id": "dwarf", "name": "矮人", "bonus": "+2体质,+1魅力", "traits": ["黑暗视觉", "石毒矮人"]},
        {"id": "halfling", "name": "半身人", "bonus": "+2敏捷,+1魅力", "traits": ["幸运", "勇气"]},
        {"id": "gnome", "name": "侏儒", "bonus": "+2智力,+1体质", "traits": ["黑暗视觉", "侏狡黠"]},
        {"id": "tiefling", "name": "提夫林", "bonus": "+1魅力,+2智力", "traits": ["黑暗视觉", "炼狱血脉"]},
        {"id": "half_orc", "name": "半兽人", "bonus": "+2体质,+1力量", "traits": ["黑暗视觉", "狂暴"]},
        {"id": "githyanki", "name": "吉斯洋基", "bonus": "+2力量,+1智力", "traits": ["心灵屏障", "语言"]}
    ],

    # 职业
    "classes": [
        {"id": "fighter", "name": "战士", "hit_die": 10, "primary_ability": ["力量", "敏捷"], "desc": "战斗大师,精通各种武器和盔甲"},
        {"id": "wizard", "name": "法师", "hit_die": 6, "primary_ability": ["智力"], "desc": "奥术施法者,精通各派法术"},
        {"id": "rogue", "name": "游荡者", "hit_die": 8, "primary_ability": ["敏捷", "智力"], "desc": "潜行与偷袭,偷窃与欺骗"},
        {"id": "cleric", "name": "牧师", "hit_die": 8, "primary_ability": ["感知", "魅力"], "desc": "神圣力量,治疗与护盾"},
        {"id": "paladin", "name": "圣武士", "hit_die": 10, "primary_ability": ["力量", "魅力"], "desc": "圣光战士,治疗与输出"},
        {"id": "ranger", "name": "游侠", "hit_die": 10, "primary_ability": ["力量", "敏捷"], "desc": "荒野战士,追踪与弓术"},
        {"id": "barbarian", "name": "野蛮人", "hit_die": 12, "primary_ability": ["力量", "体质"], "desc": "狂暴战士,高伤害高防御"},
        {"id": "bard", "name": "吟游诗人", "hit_die": 8, "primary_ability": ["魅力", "敏捷"], "desc": "魔法与音乐,社交与战斗"},
        {"id": "warlock", "name": "术士", "hit_die": 8, "primary_ability": ["魅力"], "desc": "契约束缚,短休高伤"},
        {"id": "monk", "name": "武僧", "hit_die": 8, "primary_ability": ["敏捷", "感知"], "desc": "武术大师,气功与闪避"}
    ],

    # 阵营九宫格
    "alignments": [
        # 守序善良
        {"id": "lg", "name": "守序善良", "abbr": "LG", "desc": "服从规则,帮助他人"},
        # 中立善良
        {"id": "ng", "name": "中立善良", "abbr": "NG", "desc": "帮助他人,不失公允"},
        # 混乱善良
        {"id": "cg", "name": "混乱善良", "abbr": "CG", "desc": "自由行动,帮助他人"},
        # 守序中立
        {"id": "ln", "name": "守序中立", "abbr": "LN", "desc": "规则至上"},
        # 绝对中立
        {"id": "tn", "name": "绝对中立", "abbr": "TN", "desc": "平衡,不做选择"},
        # 混乱中立
        {"id": "cn", "name": "混乱中立", "abbr": "CN", "desc": "自由,不受约束"},
        # 守序邪恶
        {"id": "le", "name": "守序邪恶", "abbr": "LE", "desc": "规则有利则遵守"},
        # 中立邪恶
        {"id": "ne", "name": "中立邪恶", "abbr": "NE", "desc": "自私为己,不择手段"},
        # 混乱邪恶
        {"id": "ce", "name": "混乱邪恶", "abbr": "CE", "desc": "破坏,混乱"}
    ],

    # 背景
    "backgrounds": [
        {"id": "soldier", "name": "士兵", "skills": ["athletics", "intimidation"]},
        {"id": "sage", "name": "学者", "skills": ["arcana", "history"]},
        {"id": "criminal", "name": "罪犯", "skills": ["stealth", "deception"]},
        {"id": "folk_hero", "name": "民间英雄", "skills": ["animal_handling", "survival"]},
        {"id": "noble", "name": "贵族", "skills": ["history", "persuasion"]},
        {"id": "acolyte", "name": "祭司", "skills": ["insight", "religion"]}
    ]
}


# ============================================
# 博德之门 - 地点
# ============================================
BG3_LOCATIONS = [
    {
        "id": "druids_grove",
        "name": "德鲁伊林地",
        "desc": "一个隐蔽的林间空地,德鲁伊社区的家园。这里有古老的橡树,神秘的泉眼,以及形形色色的流亡者。提夫林和受脑蚀的冒险者在此聚集。",
        "atmosphere": "神秘、自然、庇护",
        "npcs": ["拉斐尔(提夫林)","影心(暗夜之歌)","阿斯代伦(吸血鬼)"],
        "exits": ["地精营地", "高隐修道院", "蕈林"]
    },
    {
        "id": "goblin_camp",
        "name": "地精营地",
        "desc": "被地精和豺狼人占据的前Guildhall。三位地精首领:暴躁的格洛布、食妖格拉格、狡诈的明臣控制着这里。",
        "atmosphere": "危险、污秽、敌意",
        "npcs": ["地精三首领", "伯纳德"],
        "exits": ["德鲁伊林地", "SPD"]
    },
    {
        "id": "githyanki_creche",
        "name": "吉斯洋基育儿室",
        "desc": "吉斯洋基飞船内部的训练设施。残酷的教官、巨大的红龙、神秘的仪式。",
        "atmosphere": "冷酷、战争、异域",
        "npcs": ["Watcher", "歼敌者"],
        "exits": []
    },
    {
        "id": "underdark",
        "name": "幽暗地域",
        "desc": "地下世界的入口,弥漫着真菌孢子和危险气息。这里有灰矮人、蜘蛛、眼魔等恐怖生物。",
        "atmosphere": "幽闭、恐惧、未知",
        "npcs": ["布拉姬", "眼魔"],
        "exits": ["德鲁伊林地"]
    }
]


# ============================================
# 博德之门 - 队友同伴 (AI控制/玩家控制)
# ============================================
BG3_COMPANIONS = [
    {
        "id": "shadowheart",
        "name": "影心",
        "race": "精灵",
        "class": "牧师",
        "subclass": "暗夜之歌",
        "alignment": "混乱中立",
        "personality": "神秘、冷漠,但内心渴望归属",
        "abilities": {
            "strength": 8,
            "dexterity": 13,
            "constitution": 12,
            "intelligence": 10,
            "wisdom": 15,
            "charisma": 14
        },
        "skills": ["宗教", "医药"],
        " backstory": "记忆残缺的精灵牧师,信仰暗夜之女神,身上有着神秘的纹身。"
    },
    {
        "id": "astarion",
        "name": "阿斯代伦",
        "race": "提夫林",
        "class": "游荡者",
        "subclass": "窃贼",
        "alignment": "混乱善良",
        "personality": "轻浮、玩世不恭,但有深层创伤",
        "abilities": {
            "strength": 10,
            "dexterity": 16,
            "constitution": 12,
            "intelligence": 12,
            "wisdom": 10,
            "charisma": 15
        },
        "skills": ["隐匿", "欺骗", "手上功夫"],
        "backstory": "贵族出身的提夫林,被吸血鬼咬伤后成为眷属,渴望复仇。"
    },
    {
        "id": "laezel",
        "name": "拉斐尔",
        "race": "吉斯洋基",
        "class": "战士",
        "subclass": "武术宗师",
        "alignment": "守序中立",
        "personality": "强硬、骄傲、战斗民族",
        "abilities": {
            "strength": 16,
            "dexterity": 12,
            "constitution": 15,
            "intelligence": 10,
            "wisdom": 13,
            "charisma": 8
        },
        "skills": ["运动", "感知"],
        "backstory": "吉斯洋基战士,被夺心魔俘获,渴望找到育儿室。"
    },
    {
        "id": "gale",
        "name": "盖尔",
        "race": "人类",
        "class": "法师",
        "subclass": "防护系",
        "alignment": "中立善良",
        "personality": "聪明、好奇、有点自负",
        "abilities": {
            "strength": 8,
            "dexterity": 13,
            "constitution": 12,
            "intelligence": 17,
            "wisdom": 10,
            "charisma": 13
        },
        "skills": ["奥秘", "历史"],
        "backstory": "年轻法师,体内有星寸 Orb of Food,渴望找到答案。"
    },
    {
        "id": "wyll",
        "name": "威尔",
        "race": "人类",
        "class": "术士",
        "subclass": "龙裔",
        "alignment": "守序善良",
        "personality": "荣誉、理想主义,但有契约阴影",
        "abilities": {
            "strength": 12,
            "dexterity": 13,
            "constitution": 14,
            "intelligence": 10,
            "wisdom": 12,
            "charisma": 16
        },
        "skills": ["欺骗", "感知"],
        "backstory": "冒险者和英雄,但与魔鬼签下契约。"
    },
    {
        "id": "karlach",
        "name": "卡拉克",
        "race": "提夫林",
        "class": "野蛮人",
        "subclass": "狂战士",
        "alignment": "混乱善良",
        "personality": "直率、乐观、暴力倾向",
        "abilities": {
            "strength": 17,
            "dexterity": 12,
            "constitution": 16,
            "intelligence": 8,
            "wisdom": 10,
            "charisma": 12
        },
        "skills": ["运动", "威吓"],
        "backstory": "来自博德之门南部的提夫林,心脏有问题,渴望复仇。"
    }
]


# ============================================
# 博德之门 - 物品稀有度
# ============================================
ITEM_RARITIES = [
    {"id": "common", "name": "普通", "color": "#ffffff", "drop_rate": 60},
    {"id": "uncommon", "name": "优秀", "color": "#1eff00", "drop_rate": 25},
    {"id": "rare", "name": "稀有", "color": "#0070dd", "drop_rate": 10},
    {"id": "very_rare", "name": "非常稀有", "color": "#a335ee", "drop_rate": 4},
    {"id": "legendary", "name": "传说", "color": "#ff8000", "drop_rate": 1}
]


# ============================================
# 博德之门 - 战利品分配系统 (魔兽世界副本风格)
# ============================================
LOOT_DISTRIBUTION = {
    "name": "战利品分配",
    "modes": [
        {
            "id": "need_before_greed",
            "name": "需求优先于贪婪",
            "desc": "当有玩家需要某物品时,需要掷骰决定。无人需求时,所有人可贪婪掷骰。",
            "rules": [
                "需要: 适合自己职业/使用的物品,可投Need骰(1d100+职业加成)",
                "贪婪: 不适合但想要的物品,可投Greed骰(1d100)",
                "弃权: 不参与本次掷骰",
                "最高Need获得装备,若Need相同则比Greed,再相同则随机"
            ]
        },
        {
            "id": "round_robin",
            "name": "轮抓分配",
            "desc": "战利品按顺序轮转,每人有机会优先选择一件装备。",
            "rules": [
                "按房间码顺序轮转分配权",
                "有分配权者可以选择:拾取装备/跳过(下回合优先)",
                "跳过后,轮到下一人,被跳过的装备所有人可贪婪"
            ]
        },
        {
            "id": "master_looter",
            "name": "分配者决定",
            "desc": "队长/分配者决定物品归属(仅多人游戏时房主可开启)",
            "rules": [
                "仅房主有分配权",
                "所有物品需由房主手动分配",
                "房主可基于团队需求、玩家职业、历史获取等因素决定"
            ]
        }
    ],

    # 分配选择
    "roll_types": [
        {"id": "need", "name": "需求", "icon": "🎯", "desc": "我需要这个装备", "priority": 1},
        {"id": "greed", "name": "贪婪", "icon": "💰", "desc": "我也想要(不急需)", "priority": 2},
        {"id": "pass", "name": "跳过", "icon": "✋", "desc": "放弃本次掷骰", "priority": 0}
    ],

    # 分配结果消息
    "roll_results": [
        "{player}投出{roll}点(Need),获得了{item}!",
        "{player}投出{roll}点(Greed),在竞争中胜出获得了{item}!",
        "{player}选择跳过{item},物品进入下一轮贪婪。"
    ]
}


# ============================================
# 博德之门 - 任务
# ============================================
BG3_MISSIONS = [
    {
        "id": "druids_grove_defense",
        "name": "德鲁伊林地防御战",
        "desc": "地精正在计划对林地发动攻击,你需要帮助德鲁伊们准备防御,或者深入敌营斩首首领。",
        "difficulty": "C",
        "type": "story",
        "objectives": [
            "与德鲁伊领袖对话",
            "侦查地精营地",
            "选择:和平谈判还是武力解决",
            "击败地精三首领"
        ],
        "rewards": ["150 XP", "装备若干", "德鲁伊林地声望"]
    },
    {
        "id": "goblin_leaders",
        "name": "斩首行动",
        "desc": "深入地精营地,击杀三位首领:格洛布、格拉格、明臣。",
        "difficulty": "C",
        "type": "kill",
        "objectives": [
            "潜入地精营地",
            "找到格拉格",
            "找到明臣",
            "击败格洛布",
            "返回德鲁伊林地报告"
        ],
        "rewards": ["300 XP", "优秀装备", "解除林地威胁"]
    },
    {
        "id": "find_shadowheart_lady",
        "name": "寻找影心的女士",
        "desc": "影心请求你帮助寻找她记忆中的女士——暗夜之歌的神选者。",
        "difficulty": "B",
        "type": "story",
        "objectives": [
            "询问影心关于女士的线索",
            "前往被遗忘的国度",
            "找到暗夜之歌神殿",
            "击败神殿守卫",
            "解救女士"
        ],
        "rewards": ["400 XP", "暗夜祝福", "影心忠诚度大幅提升"]
    },
    {
        "id": "githyanki_creche",
        "name": "吉斯洋基育儿室",
        "desc": "拉斐尔渴望找到她的族人,育儿室或许有关于夺心魔的情报。",
        "difficulty": "B",
        "type": "explore",
        "objectives": [
            "接受拉斐尔的请求",
            "找到育儿室入口",
            "通过吉斯洋基测试",
            "找到Watcher并对抗",
            "获取红龙坐骑"
        ],
        "rewards": ["350 XP", "吉斯洋基武器", "拉斐尔忠诚提升"]
    },
    {
        "id": "underdark_alliance",
        "name": "幽暗地域联盟",
        "desc": "与幽暗地域的灰矮人建立联系,或者找到其他势力对抗眼魔。",
        "difficulty": "A",
        "type": "story",
        "objectives": [
            "进入幽暗地域",
            "找到灰矮人聚居地",
            "通过灰矮人试炼",
            "面对眼魔",
            "选择:结盟还是毁灭"
        ],
        "rewards": ["500 XP", "传说装备", "幽暗地域声望"]
    },
    {
        "id": "steal_the_artifacts",
        "name": "盗取Artifacts",
        "desc": "潜入高隐修道院,寻找被盗的Artifacts——或者摧毁它们。",
        "difficulty": "A",
        "type": "infiltrate",
        "objectives": [
            "找到修道院入口",
            "躲避或击败修道院守卫",
            "找到Artifacts",
            "选择:归还还是利用",
            "逃离修道院"
        ],
        "rewards": ["450 XP", "独特装备", "修道院关系变化"]
    }
]


# ============================================
# 获取随机同伴
# ============================================
def get_random_companion(exclude_ids: list = None) -> dict:
    """获取随机同伴"""
    exclude_ids = exclude_ids or []
    available = [c for c in BG3_COMPANIONS if c["id"] not in exclude_ids]
    return random.choice(available) if available else None


# ============================================
# 投骰结果生成
# ============================================
def roll_loot(players: list, item: dict, mode: str = "need_before_greed") -> dict:
    """模拟战利品分配投骰"""
    import random

    # 计算每个玩家的需求/贪婪骰
    rolls = []
    for player in players:
        if item.get("class_required") and player.get("class") != item.get("class_required"):
            # 不符合职业需求,只能贪婪
            roll = random.randint(1, 100)
            rolls.append({"player": player, "type": "greed", "roll": roll})
        else:
            # 可以需求
            need_roll = random.randint(1, 100) + (player.get("level", 1) * 5)
            greed_roll = random.randint(1, 100)
            rolls.append({"player": player, "type": "need", "roll": need_roll, "greed_roll": greed_roll})

    # 按类型排序:需求优先于贪婪
    rolls.sort(key=lambda x: x["roll"], reverse=True)

    winner = rolls[0]
    return {
        "item": item,
        "winner": winner["player"],
        "all_rolls": rolls,
        "narrative": f"{winner['player']['name']}投出{winner['roll']}点,获得了{item['name']}!"
    }