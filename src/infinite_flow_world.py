"""
天道 TRPG - 无限流世界设定
基于用户提供的超次元公会等无限流小说设定

核心概念:
- 诸神空间/任务大厅 - 玩家聚集地
- 任务世界 - 玩家被传送到各种电影/动漫/游戏/小说世界
- 轮回者 - 完成任务获得奖励
- 深渊轮回者 - 选择破坏世界,获得更强大但危险的力量
- 高自主性 - AI自主生成任务,无固定模板

设计原则:
1. 任务大厅机制 - 玩家选择任务或自由行动
2. 难度分级 - 不同难度对应不同奖励和风险
3. 轮回者/深渊轮回者阵营选择
4. 世界穿越 - 覆盖电影/动漫/游戏/小说世界观
5. 即时无离线收益 - 所有奖励通过任务获得
"""

import random

# ============================================
# 无限流世界 - 诸神空间核心设定
# ============================================
INFINITE_FLOW_CORE = {
    "name": "Infinite Flow - 无限流",
    "chinese_name": "诸神空间",
    "system_type": "infinite_flow",
    "overview": "玩家被神秘空间选中,穿越到各种电影、动漫、游戏、小说世界完成任务。完成任务获得奖励,拒绝任务降低评价,破坏世界则可能堕入深渊。轮回者与深渊轮回者,一线之隔。",
    "source_docs": ["超次元公会.txt", "无限流小说设定"],
    "gameplay_mode": "任务驱动型跑团",
    "max_players": 8,
    "estimated_duration": "30-60分钟一局任务",
    "complexity": "入门级",  # 璀璨宝石式易上手

    # 核心机制 - 猜拳式阵营选择
    "player_types": [
        {
            "id": "cyclic_reincarnation",
            "name": "轮回者",
            "name_cn": "轮回者",
            "desc": "遵守空间规则,完成任务获取奖励,走正道",
            "alignment": "neutral_good",
            "bonus": "+1 任务奖励获取",
            "penalty": "无法使用深渊技能"
        },
        {
            "id": "abyss_reincarnation",
            "name": "深渊轮回者",
            "name_cn": "深渊轮回者",
            "desc": "破坏世界获取更强大的力量,但会逐渐失控",
            "alignment": "chaotic_evil",
            "bonus": "+2 击杀奖励,解锁深渊技能",
            "penalty": "每破坏一个世界,理智-1,失控风险+1"
        }
    ],

    # 任务难度等级
    "difficulty_levels": [
        {
            "id": "e",
            "name": "E级",
            "desc": "新手任务",
            "risk": "极低",
            "reward": "10-30 积分, 1-2 技能点",
            "examples": ["寻找丢失的猫", "送一封信"]
        },
        {
            "id": "d",
            "name": "D级",
            "desc": "简单任务",
            "risk": "低",
            "reward": "30-50 积分, 2-3 技能点",
            "examples": ["护送任务", "收集物品"]
        },
        {
            "id": "c",
            "name": "C级",
            "desc": "普通任务",
            "risk": "中等",
            "reward": "50-100 积分, 3-5 技能点",
            "examples": ["击杀小型怪物", "潜入调查"]
        },
        {
            "id": "b",
            "name": "B级",
            "desc": "困难任务",
            "risk": "高",
            "reward": "100-200 积分, 5-8 技能点",
            "examples": ["Boss战", "大事件参与"]
        },
        {
            "id": "a",
            "name": "A级",
            "desc": "噩梦任务",
            "risk": "极高",
            "reward": "200-500 积分, 8-15 技能点",
            "examples": ["改变剧情走向", "击杀主角/反派"]
        },
        {
            "id": "s",
            "name": "S级",
            "desc": "传说任务",
            "risk": "死亡级",
            "reward": "500+ 积分, 15+ 技能点, 稀有技能/装备",
            "examples": ["毁灭世界", "击杀神明"]
        }
    ],

    # 任务类型
    "mission_types": [
        {"id": "kill", "name": "击杀任务", "desc": "击杀指定目标", "icon": "sword"},
        {"id": "protect", "name": "保护任务", "desc": "保护指定目标存活", "icon": "shield"},
        {"id": "collect", "name": "收集任务", "desc": "收集指定物品", "icon": "gem"},
        {"id": "infiltrate", "name": "潜入任务", "desc": "潜入指定地点", "icon": "eye"},
        {"id": "escort", "name": "护送任务", "desc": "护送目标到达目的地", "icon": "map"},
        {"id": "story", "name": "剧情任务", "desc": "触发/推动/改变剧情", "icon": "book"},
        {"id": "survival", "name": "生存任务", "desc": "在危险环境存活", "icon": "heart"},
        {"id": "sabotage", "name": "破坏任务", "desc": "破坏世界规则/结构(深渊)", "icon": "skull"}
    ],

    # 任务选择
    "mission_actions": [
        {"id": "accept", "name": "接受任务", "desc": "接受任务并前往任务世界", "icon": "check"},
        {"id": "reject", "name": "拒绝任务", "desc": "拒绝任务,降低空间评价", "icon": "x"},
        {"id": "negotiate", "name": "协商任务", "desc": "尝试降低难度或增加奖励", "icon": "speech"},
        {"id": "sabotage", "name": "破坏世界", "desc": "在任务世界进行破坏(深渊)", "icon": "fire"}
    ],

    # 奖励类型
    "reward_types": [
        {"id": "points", "name": "积分", "desc": "空间通用货币,可兑换一切"},
        {"id": "skill_points", "name": "技能点", "desc": "强化技能和能力"},
        {"id": "equipment", "name": "装备", "desc": "来自任务世界的装备"},
        {"id": "skill", "name": "技能", "desc": "技能卡,可学习新能力"},
        {"id": "title", "name": "称号", "desc": "特殊称号,提供被动效果"},
        {"id": "abyss_power", "name": "深渊之力", "desc": "深渊轮回者专属,强大的禁忌力量", "icon": "demon"}
    ],

    # 任务大厅位置
    "hall_locations": [
        {"id": "mission_board", "name": "任务板", "desc": "发布各种任务"},
        {"id": "reward_store", "name": "奖励商店", "desc": "用积分兑换奖励"},
        {"id": "training_room", "name": "训练室", "desc": "提升技能"},
        {"id": "lounge", "name": "休息区", "desc": "玩家交流区域"},
        {"id": "transfer_circle", "name": "传送阵", "desc": "前往任务世界"}
    ]
}


# ============================================
# 无限流世界 - 影视世界库 (电影)
# ============================================
MOVIE_WORLDS = [
    {
        "id": "inception",
        "name": "盗梦空间",
        "source": "电影",
        "difficulty_range": ["C", "B", "A"],
        "desc": "潜入梦境,盗取或植入信息",
        "keywords": ["梦境", "潜意识", "多层梦", "图腾"],
        "missions": [
            "潜入目标梦境,获取机密信息",
            "在梦境中植入一个想法",
            "抵抗梦境的扭曲和防御",
            "在深层梦境找到失落的记忆"
        ]
    },
    {
        "id": "matrix",
        "name": "黑客帝国",
        "source": "电影",
        "difficulty_range": ["B", "A", "S"],
        "desc": "真实与虚拟的边界",
        "keywords": ["矩阵", "子弹时间", "觉醒", "锡安"],
        "missions": [
            "在矩阵中执行秘密任务",
            "帮助觉醒一个被矩阵控制的人",
            "破坏矩阵的某个核心程序",
            "对抗特工,保护觉醒者"
        ]
    },
    {
        "id": "interstellar",
        "name": "星际穿越",
        "source": "电影",
        "difficulty_range": ["B", "A", "S"],
        "desc": "星际旅行,黑洞与五维空间",
        "keywords": ["虫洞", "黑洞", "时间膨胀", "父女羁绊"],
        "missions": [
            "探索宜居星球",
            "收集星球数据",
            "在时间膨胀中存活",
            "对抗曼恩博士的背叛"
        ]
    },
    {
        "id": "potter",
        "name": "哈利波特",
        "source": "电影",
        "difficulty_range": ["D", "C", "B"],
        "desc": "魔法世界,霍格沃茨",
        "keywords": ["魔法", "霍格沃茨", "魁地奇", "食死徒"],
        "missions": [
            "在霍格沃茨学习魔法",
            "对抗伏地魔和食死徒",
            "寻找魂器",
            "参加三强争霸赛"
        ]
    },
    {
        "id": "avatar",
        "name": "阿凡达",
        "source": "电影",
        "difficulty_range": ["C", "B", "A"],
        "desc": "潘多拉星球,纳美族",
        "keywords": ["纳美族", "灵魂树", "人类入侵", "天空人"],
        "missions": [
            "与纳美族建立联系",
            "帮助对抗RDA公司入侵",
            "骑乘斑溪兽",
            "连接灵魂树"
        ]
    },
    {
        "id": "zombie_apocalypse",
        "name": "僵尸世界大战",
        "source": "电影",
        "difficulty_range": ["C", "B", "A"],
        "desc": "全球僵尸爆发",
        "keywords": ["僵尸", "末日", "逃亡", "病毒"],
        "missions": [
            "在僵尸爆发中存活",
            "寻找幸存者聚居地",
            "寻找僵尸疫情的源头",
            "护送幸存者到安全区"
        ]
    },
    {
        "id": "john_wick",
        "name": "疾速追杀",
        "source": "电影",
        "difficulty_range": ["C", "B", "A"],
        "desc": "杀手的世界,高台桌",
        "keywords": ["杀手", "高台桌", "金币", " Continental"],
        "missions": [
            "完成高台桌的任务",
            "对抗俄罗斯黑帮",
            "在酒店中寻求庇护",
            "参与大陆酒店的竞技"
        ]
    }
]


# ============================================
# 无限流世界 - 动漫世界库
# ============================================
ANIME_WORLDS = [
    {
        "id": "one_piece",
        "name": "海贼王",
        "source": "动漫",
        "difficulty_range": ["D", "C", "B", "A"],
        "desc": "大海贼时代,伟大航路",
        "keywords": ["海贼", "恶魔果实", "草帽一伙", "四皇"],
        "missions": [
            "在伟大航路冒险",
            "寻找ONE PIECE",
            "对抗七武海和海军",
            "参加世界会议"
        ]
    },
    {
        "id": "naruto",
        "name": "火影忍者",
        "source": "动漫",
        "difficulty_range": ["D", "C", "B", "A", "S"],
        "desc": "忍者的世界,查克拉",
        "keywords": ["忍者", "查克拉", "尾兽", "忍界大战"],
        "missions": [
            "在忍者学校修行",
            "执行S级任务",
            "对抗晓组织",
            "参与第四次忍界大战"
        ]
    },
    {
        "id": "attack_on_titan",
        "name": "进击的巨人",
        "source": "动漫",
        "difficulty_range": ["C", "B", "A", "S"],
        "desc": "巨人与人类的战争",
        "keywords": ["巨人", "城墙", "地下室", "始祖巨人"],
        "missions": [
            "在城墙内生存",
            "调查巨人的起源",
            "参与玛利亚之墙夺回战",
            "对抗兽之巨人"
        ]
    },
    {
        "id": "death_note",
        "name": "死亡笔记",
        "source": "动漫",
        "difficulty_range": ["D", "C", "B"],
        "desc": "笔记与智慧的对决",
        "keywords": ["死亡笔记", "L", "夜神月", "推理"],
        "missions": [
            "调查笔记的使用者",
            "与L斗智斗勇",
            "在笔记上写下名字",
            "逃避笔记的追踪"
        ]
    },
    {
        "id": "sword_art_online",
        "name": "刀剑神域",
        "source": "动漫",
        "difficulty_range": ["C", "B", "A"],
        "desc": "VRMMO死亡游戏",
        "keywords": ["VR", "SAO", "攻略", "茅场晶彦"],
        "missions": [
            "攻略SAO的楼层",
            "在死亡游戏中存活",
            "对抗Boss",
            "找到茅场晶彦的真相"
        ]
    },
    {
        "id": "demon_slayer",
        "name": "鬼灭之刃",
        "source": "动漫",
        "difficulty_range": ["D", "C", "B", "A"],
        "desc": "炭治郎与鬼杀队",
        "keywords": ["鬼杀队", "呼吸法", "十二鬼月", "上弦"],
        "missions": [
            "与鬼战斗",
            "调查十二鬼月",
            "对抗上弦鬼",
            "寻找无惨的弱点"
        ]
    },
    {
        "id": "chainsaw_man",
        "name": "链锯人",
        "source": "动漫",
        "difficulty_range": ["C", "B", "A", "S"],
        "desc": "恶魔与契约者",
        "keywords": ["恶魔", "公安", "契约", "电次"],
        "missions": [
            "狩猎恶魔",
            "对抗魔人",
            "参与公安的行动",
            "与强大的恶魔缔结契约"
        ]
    },
    {
        "id": "jujutsu_kaisen",
        "name": "咒术回战",
        "source": "动漫",
        "difficulty_range": ["C", "B", "A", "S"],
        "desc": "咒术师与咒灵",
        "keywords": ["咒术", "咒灵", "宿傩", "五条悟"],
        "missions": [
            "执行咒术任务",
            "对抗特级咒灵",
            "参与涩谷事变",
            "寻找虎杖的伙伴"
        ]
    },
    {
        "id": "violet_evergarden",
        "name": "紫罗兰永恒花园",
        "source": "动漫",
        "difficulty_range": ["D", "C", "B"],
        "desc": "战争后的和平年代",
        "keywords": ["自动手记人偶", "战争创伤", "书信", "爱"],
        "missions": [
            "作为人偶完成委托",
            "理解'爱'的含义",
            "参与战争后的重建",
            "寻找战后失踪的人"
        ]
    },
    {
        "id": "steins_gate",
        "name": "命运石之门",
        "source": "动漫",
        "difficulty_range": ["C", "B", "A"],
        "desc": "时间旅行与因果律",
        "keywords": ["时间机器", "世界线", "SERN", "椎名里由"],
        "missions": [
            "发明时间机器",
            "阻止SERN的阴谋",
            "穿越世界线",
            "拯救牧濑红莉栖"
        ]
    }
]


# ============================================
# 无限流世界 - 游戏世界库
# ============================================
GAME_WORLDS = [
    {
        "id": "zelda_breath",
        "name": "塞尔达传说:旷野之息",
        "source": "游戏",
        "difficulty_range": ["D", "C", "B", "A"],
        "desc": "海拉鲁大陆的开放世界",
        "keywords": ["海拉鲁", "神兽", "盖侬", "大师之剑"],
        "missions": [
            "在海拉鲁大陆探索",
            "解放四神兽",
            "对抗加农",
            "收集900个克洛格果实"
        ]
    },
    {
        "id": "elden_ring",
        "name": "艾尔登法环",
        "source": "游戏",
        "difficulty_range": ["B", "A", "S"],
        "desc": "交界地的史诗冒险",
        "keywords": ["交界地", "半神", "艾尔登之兽", "魂类"],
        "missions": [
            "挑战各个半神",
            "收集大卢恩",
            "对抗艾尔登之兽",
            "成为艾尔登之王"
        ]
    },
    {
        "id": "witcher3",
        "name": "巫师3:狂猎",
        "source": "游戏",
        "difficulty_range": ["C", "B", "A"],
        "desc": "猎魔人的史诗旅程",
        "keywords": ["猎魔人", "杰洛特", "凯尔莫罕", "狂猎"],
        "missions": [
            "狩猎怪物",
            "寻找女儿希里",
            "对抗狂猎军队",
            "参与血腥男爵的任务"
        ]
    },
    {
        "id": "mass_effect",
        "name": "质量效应",
        "source": "游戏",
        "difficulty_range": ["B", "A", "S"],
        "desc": "银河系的史诗冒险",
        "keywords": ["薛帕德", "收割者", "诺曼底", "赛拉睿"],
        "missions": [
            "对抗收割者",
            "完成银河议会任务",
            "与外星种族建立联盟",
            "进入奥RCU的真相"
        ]
    },
    {
        "id": "resident_evil4",
        "name": "生化危机4",
        "source": "游戏",
        "difficulty_range": ["C", "B", "A"],
        "desc": "浣熊市的恐怖逃生",
        "keywords": ["丧尸", "保护伞", "里昂", "碍事莉"],
        "missions": [
            "在村落中逃生",
            "对抗村长和寄生虫",
            "拯救阿什莉",
            "调查Las Plagas"
        ]
    },
    {
        "id": "god_of_war",
        "name": "战神",
        "source": "游戏",
        "difficulty_range": ["C", "B", "A", "S"],
        "desc": "奎托斯的北欧之旅",
        "keywords": ["战神", "北欧神话", "奥丁", "九界"],
        "missions": [
            "在九界冒险",
            "对抗北欧诸神",
            "寻找约顿海姆",
            "揭开巨人的预言"
        ]
    },
    {
        "id": "horizon_zero_dawn",
        "name": "地平线:零之曙光",
        "source": "游戏",
        "difficulty_range": ["C", "B", "A"],
        "desc": "机械兽横行的未来世界",
        "keywords": ["埃洛伊", "机械兽", "APEX", "零之曙光"],
        "missions": [
            "在机械兽中生存",
            "调查世界的真相",
            "对抗哈迪斯",
            "寻找伊莉莎白"
        ]
    }
]


# ============================================
# 无限流世界 - 小说世界库
# ============================================
NOVEL_WORLDS = [
    {
        "id": "lord_of_the_rings",
        "name": "魔戒",
        "source": "小说",
        "difficulty_range": ["C", "B", "A", "S"],
        "desc": "中土世界的史诗",
        "keywords": ["魔戒", "弗罗多", "索伦", "至尊魔戒"],
        "missions": [
            "护送魔戒到瑞文戴尔",
            "对抗戒灵",
            "进入摩多",
            "在末日山销毁魔戒"
        ]
    },
    {
        "id": "harry_potter_novel",
        "name": "哈利波特小说",
        "source": "小说",
        "difficulty_range": ["D", "C", "B", "A"],
        "desc": "魔法世界的冒险",
        "keywords": ["魔法", "霍格沃茨", "食死徒", "伏地魔"],
        "missions": [
            "参与三强争霸赛",
            "对抗食死徒",
            "找到并销毁魂器",
            "参与霍格沃茨大战"
        ]
    },
    {
        "id": "worm",
        "name": "战锤40K",
        "source": "小说",
        "difficulty_range": ["A", "S"],
        "desc": "太空中的永恒战争",
        "keywords": ["战锤", "星际战士", "泰伦虫族", "帝皇"],
        "missions": [
            "在泰伦虫族入侵中存活",
            "对抗混沌军团",
            "寻找帝皇的真相",
            "参与大远征"
        ]
    }
]


# ============================================
# 所有世界汇总
# ============================================
ALL_WORLDS = MOVIE_WORLDS + ANIME_WORLDS + GAME_WORLDS + NOVEL_WORLDS


# ============================================
# 无限流世界 - 技能系统
# ============================================
INFINITE_FLOW_SKILLS = {
    "common_skills": [
        {"id": "quick_reflex", "name": "快速反射", "desc": "闪避攻击+1", "cost": 5},
        {"id": "sharp_sense", "name": "敏锐感知", "desc": "发现隐藏+1", "cost": 5},
        {"id": "iron_will", "name": "钢铁意志", "desc": "抗诱惑+1", "cost": 5},
        {"id": "survival_instinct", "name": "生存本能", "desc": "危机时自动判定重投", "cost": 10},
        {"id": "language_genius", "name": "语言天才", "desc": "快速学习任何语言", "cost": 8}
    ],
    "cyclic_skills": [
        {"id": "task_insight", "name": "任务洞察", "desc": "任务奖励+10%", "cost": 15},
        {"id": "safe_approach", "name": "稳妥行事", "desc": "任务失败时保留50%积分", "cost": 15},
        {"id": "ally_support", "name": "队友支援", "desc": "可为队友承担伤害", "cost": 20},
        {"id": "learning_speed", "name": "学习加速", "desc": "技能升级费用-20%", "cost": 25}
    ],
    "abyss_skills": [
        {"id": "soul_harvest", "name": "灵魂收割", "desc": "击杀目标获得额外积分", "cost": 15, "abyss_only": True},
        {"id": "world_break", "name": "世界崩坏", "desc": "破坏任务世界结构,奖励翻倍", "cost": 20, "abyss_only": True},
        {"id": "dark_regen", "name": "深渊再生", "desc": "战斗后恢复生命", "cost": 15, "abyss_only": True},
        {"id": "fear_aura", "name": "恐惧光环", "desc": "敌人判定-1", "cost": 20, "abyss_only": True},
        {"id": "instability", "name": "失控冲动", "desc": "下一回合伤害x2,但有几率伤害自己", "cost": 25, "abyss_only": True}
    ]
}


# ============================================
# 无限流世界 - 称号系统
# ============================================
INFINITE_FLOW_TITLES = [
    {"id": "newcomer", "name": "新手轮回者", "requirement": "完成第一个任务", "bonus": "无"},
    {"id": "task_master", "name": "任务达人", "requirement": "连续完成5个任务", "bonus": "任务积分+5%"},
    {"id": "world_breaker", "name": "世界破坏者", "requirement": "破坏一个世界", "bonus": "解锁深渊技能", "abyss_only": True},
    {"id": "survivor", "name": "幸存者", "requirement": "在S级任务中存活", "bonus": "所有检定+1"},
    {"id": "hero", "name": "英雄", "requirement": "在任务中拯救10名NPC", "bonus": "NPC好感度+1"},
    {"id": "shadow", "name": "暗影", "requirement": "完美完成潜入任务", "bonus": "隐匿检定+2"},
    {"id": "boss_killer", "name": "Boss克星", "requirement": "击杀10个Boss", "bonus": "Boss战伤害+2"},
    {"id": "wanderer", "name": "漂泊者", "requirement": "进入20个不同世界", "bonus": "世界知识+1"},
    {"id": "abyss_touched", "name": "深渊之触", "requirement": "堕入深渊后仍保持理智", "bonus": "深渊技能伤害+1", "abyss_only": True},
    {"id": "space_favorite", "name": "空间宠儿", "requirement": "获得空间意志认可", "bonus": "每日任务奖励+1"}
]


# ============================================
# 生成随机任务描述
# ============================================
def generate_mission_description(world_id: str, difficulty: str, mission_type: str) -> str:
    """AI生成任务描述(高自主性,无固定模板)"""
    import random

    world = next((w for w in ALL_WORLDS if w["id"] == world_id), None)
    if not world:
        world = random.choice(ALL_WORLDS)

    # 基础任务模板 - 由AI自主填充
    mission_templates = [
        f"你被传送到【{world['name']}】世界。作为轮回者,你需要完成一项{difficulty}级任务。",
        f"【紧急任务】{world['name']}世界出现了异常波动,空间召唤你前往调查。",
        f"诸神空间发布了一则{difficulty}级悬赏任务,目标位于【{world['name']}】世界。",
        f"你收到了来自【{world['name']}】的召唤。作为被选中的轮回者,你别无选择...",
        f"空间意志传递给你一段信息:\"{world['name']}世界正面临危机,需要你的介入。\""
    ]

    mission_type_texts = {
        "kill": "击杀目标",
        "protect": "保护目标",
        "collect": "收集物品",
        "infiltrate": "潜入调查",
        "escort": "护送目标",
        "story": "推动剧情",
        "survival": "生存挑战",
        "sabotage": "破坏任务"
    }

    base = random.choice(mission_templates)
    mission_desc = mission_type_texts.get(mission_type, "执行任务")

    # AI会进一步生成具体目标细节
    detail_hints = [
        "具体目标和细节将由空间意志在进入世界后揭示。",
        "你的任务情报有限,需要进入世界后自行探索。",
        "任务可能有隐藏条件,谨慎行动。",
        "情报显示这个任务存在变数,做好应变准备。",
        "诸神空间提示:某些任务存在'完美完成'条件..."
    ]

    return f"{base}\n\n任务类型: {mission_desc}\n\n{random.choice(detail_hints)}"


# ============================================
# 获取随机世界
# ============================================
def get_random_world(difficulty_filter: list = None) -> dict:
    """获取随机世界(可选难度过滤)"""
    import random

    if difficulty_filter:
        candidates = [w for w in ALL_WORLDS if any(d in w["difficulty_range"] for d in difficulty_filter)]
        if candidates:
            return random.choice(candidates)

    return random.choice(ALL_WORLDS)


# ============================================
# 阵营行动结果
# ============================================
MISSION_OUTCOMES = {
    "accept_success": [
        "任务完成!你获得了任务奖励。",
        "干得漂亮!诸神空间对你的表现很满意。",
        "任务成功,积分和技能点已发放。"
    ],
    "accept_failure": [
        "任务失败...你保住了性命,但没有奖励。",
        "任务未完成,诸神空间降低了你的评价。",
        "任务失败,空间正在重新评估你的能力..."
    ],
    "reject": [
        "你拒绝了任务。诸神空间记录了你的行为,评价下降。",
        "退缩了吗?空间不会强迫任何人,但代价是真实的。",
        "你选择了放弃。这次可以,但下次呢?"
    ],
    "sabotage_success": [
        "世界被你破坏了。深渊之力在体内涌动...",
        "崩坏即是力量。你感受到了前所未有的强大。",
        "你选择了黑暗。诸神空间在注视着你..."
    ],
    "sabotage_failure": [
        "破坏失败。你的行为触怒了空间。",
        "你没能破坏世界,但深渊已经注意到了你。",
        "代价...是沉重的。你的理智在动摇。"
    ],
    "sabotage_critical": [
        "你堕入深渊太深了...失控。",
        "深渊力量反噬。你的意识开始模糊..."
    ]
}
