"""
天道 TRPG - 主流跑团系统适配数据
基于网络搜索获取的 D&D 5e、Pathfinder 2e、Call of Cthulhu 官方/主流信息

信息来源:
- D&D 5e: D&D Beyond, dnd-5e.fandom.com, 5e.tools
- Pathfinder 2e: Archives of Nethys (2e.aonprd.com), Pathfinder Wiki
- Call of Cthulhu: Chaosium官方Wiki, cthulhuwiki.chaosium.com

使用方法:
    from trpg_worlds import TRPG_SYSTEMS
    # 获取某个系统的完整数据用于天道适配
"""

# ============================================
# D&D 5e (龙与地下城 第五版)
# ============================================
DND_5E = {
    "name": "Dungeons & Dragons 5th Edition",
    "chinese_name": "龙与地下城 第五版",
    "system_type": "fantasy",
    "overview": "最经典的奇幻跑团系统，由Tactical Studies Rules (TSR)创建，威世智(Wizards of the Coast)发行。PHB包含12个职业、9个核心种族、12+背景。",
    "source_urls": [
        "https://www.dndbeyond.com/classes",
        "https://dnd-5e.fandom.com/wiki/Classes",
        "https://dnd-5e.fandom.com/wiki/Backgrounds"
    ],
    "ability_scores": [
        {"id": "strength", "name": "力量", "abbr": "STR", "desc": "肌肉力量和体力"},
        {"id": "dexterity", "name": "敏捷", "abbr": "DEX", "desc": "身体灵活性和反射"},
        {"id": "constitution", "name": "体质", "abbr": "CON", "desc": "耐力和健康"},
        {"id": "intelligence", "name": "智力", "abbr": "INT", "desc": "记忆和分析能力"},
        {"id": "wisdom", "name": "感知", "abbr": "WIS", "desc": "直觉、洞察和意志力"},
        {"id": "charisma", "name": "魅力", "abbr": "CHA", "desc": "社交能力和魔法亲和"}
    ],
    "skills": [
        {"id": "athletics", "name": "运动", "ability": "力量", "desc": "攀爬、跳跃、游泳"},
        {"id": "acrobatics", "name": "杂技", "ability": "敏捷", "desc": "翻滚、平衡"},
        {"id": "sleight_of_hand", "name": "手上功夫", "ability": "敏捷", "desc": "灵巧和偷窃"},
        {"id": "stealth", "name": "隐匿", "ability": "敏捷", "desc": "潜行和躲藏"},
        {"id": "arcana", "name": "奥秘", "ability": "智力", "desc": "魔法知识"},
        {"id": "history", "name": "历史", "ability": "智力", "desc": "历史事件和人物"},
        {"id": "investigation", "name": "调查", "ability": "智力", "desc": "推理和发现线索"},
        {"id": "nature", "name": "自然", "ability": "智力", "desc": "动植物和地理"},
        {"id": "religion", "name": "宗教", "ability": "智力", "desc": "神祇、宗教仪式"},
        {"id": "animal_handling", "name": "动物处理", "ability": "感知", "desc": "驯服和照顾动物"},
        {"id": "insight", "name": "洞察", "ability": "感知", "desc": "判断他人意图"},
        {"id": "medicine", "name": "医药", "ability": "感知", "desc": "治疗和诊断"},
        {"id": "perception", "name": "感知", "ability": "感知", "desc": "听觉和视觉察觉"},
        {"id": "survival", "name": "生存", "ability": "感知", "desc": "野外生存技能"},
        {"id": "deception", "name": "欺骗", "ability": "魅力", "desc": "撒谎和掩饰"},
        {"id": "intimidation", "name": "威吓", "ability": "魅力", "desc": "威胁和强迫"},
        {"id": "performance", "name": "表演", "ability": "魅力", "desc": "娱乐和展示"},
        {"id": "persuasion", "name": "说服", "ability": "魅力", "desc": "理性说服和谈判"}
    ],
    "core_classes": [
        {
            "id": "artificer",
            "name": "炼金术师",
            "chinese_name": "炼金术师",
            "hit_die": 8,
            "primary_ability": ["智力", "魅力"],
            "saving_throws": ["智力", "体质"],
            "armor_proficiency": ["轻甲", "中甲", "盾牌"],
            "weapon_proficiency": ["简易武器", "军用武器"],
            "skills": ["奥秘", "历史", "调查", "医药", "魔法"],
            "desc": "利用魔法和发明才能的创造者，用技术解锁物品的特殊能力。"
        },
        {
            "id": "barbarian",
            "name": "Barbarian",
            "chinese_name": "野蛮人",
            "hit_die": 12,
            "primary_ability": ["力量", "体质"],
            "saving_throws": ["力量", "体质"],
            "armor_proficiency": ["轻甲", "中甲", "盾牌"],
            "weapon_proficiency": ["简易武器", "军用武器"],
            "skills": ["动物处理", "运动", "威吓", "自然", "感知", "生存"],
            "desc": "狂暴的战场上不可阻挡的力量，以愤怒激发身体潜能。"
        },
        {
            "id": "bard",
            "name": "Bard",
            "chinese_name": "吟游诗人",
            "hit_die": 8,
            "primary_ability": ["魅力", "敏捷"],
            "saving_throws": ["敏捷", "魅力"],
            "armor_proficiency": ["轻甲"],
            "weapon_proficiency": ["简易武器", "手弩", "细剑", "刺剑", "单手锐器"],
            "skills": ["选择任意三种"],
            "desc": "魔法旋律的操控者，用歌声和故事改变世界。"
        },
        {
            "id": "cleric",
            "name": "Cleric",
            "chinese_name": "牧师",
            "hit_die": 8,
            "primary_ability": ["感知", "魅力"],
            "saving_throws": ["感知", "魅力"],
            "armor_proficiency": ["轻甲", "中甲", "重甲", "盾牌"],
            "weapon_proficiency": ["简易武器"],
            "skills": ["历史", "洞察", "医药", "说服", "宗教"],
            "desc": "神圣力量的代言人，神祇的仆从，能施展神术治疗或伤害。"
        },
        {
            "id": "druid",
            "name": "Druid",
            "chinese_name": "德鲁伊",
            "hit_die": 8,
            "primary_ability": ["感知", "智力"],
            "saving_throws": ["智力", "感知"],
            "armor_proficiency": ["轻甲", "中甲", "盾牌"],
            "weapon_proficiency": ["简易武器", "弯形刀"],
            "skills": ["奥秘", "动物处理", "洞察", "医药", "自然", "感知", "宗教", "生存"],
            "desc": "自然之力的守护者，能够变形成各种动物，施展自然魔法。"
        },
        {
            "id": "fighter",
            "name": "Fighter",
            "chinese_name": "战士",
            "hit_die": 10,
            "primary_ability": ["力量", "敏捷"],
            "saving_throws": ["力量", "体质"],
            "armor_proficiency": ["轻甲", "中甲", "重甲", "所有武器", "盾牌"],
            "weapon_proficiency": ["简易武器", "军用武器"],
            "skills": ["杂技", "动物处理", "运动", "历史", "洞察", "感知", "生存"],
            "desc": "战斗艺术的大师，精通各种武器和战术，战场上的多面手。"
        },
        {
            "id": "monk",
            "name": "Monk",
            "chinese_name": "武僧",
            "hit_die": 8,
            "primary_ability": ["敏捷", "感知"],
            "saving_throws": ["力量", "敏捷"],
            "armor_proficiency": [],
            "weapon_proficiency": ["简易武器", "长剑"],
            "skills": ["杂技", "运动", "历史", "洞察", "宗教"],
            "desc": "气功大师，用身体作为最强大的武器，以徒手战斗和气之力见长。"
        },
        {
            "id": "paladin",
            "name": "Paladin",
            "chinese_name": "圣武士",
            "hit_die": 10,
            "primary_ability": ["力量", "魅力"],
            "saving_throws": ["魅力", "感知"],
            "armor_proficiency": ["轻甲", "中甲", "重甲", "所有武器", "盾牌"],
            "weapon_proficiency": ["简易武器", "军用武器"],
            "skills": ["运动", "洞察", "威吓", "医药", "说服", "宗教"],
            "desc": "神圣誓言的守护者，结合战士与牧师的力量，以正义之名战斗。"
        },
        {
            "id": "ranger",
            "name": "Ranger",
            "chinese_name": "游侠",
            "hit_die": 10,
            "primary_ability": ["敏捷", "感知"],
            "saving_throws": ["敏捷", "感知"],
            "armor_proficiency": ["轻甲", "中甲", "盾牌"],
            "weapon_proficiency": ["简易武器", "军用武器"],
            "skills": ["动物处理", "运动", "洞察", "调查", "自然", "感知", "隐匿", "生存"],
            "desc": "荒野的战士，精通追踪和双持武器，是自然的守护者。"
        },
        {
            "id": "rogue",
            "name": "Rogue",
            "chinese_name": "游荡者",
            "hit_die": 8,
            "primary_ability": ["敏捷", "智力"],
            "saving_throws": ["敏捷", "智力"],
            "armor_proficiency": ["轻甲"],
            "weapon_proficiency": ["简易武器", "手弩", "长剑", "刺剑", "短剑"],
            "skills": ["杂技", "运动", "欺骗", "洞察", "威吓", "调查", "感知", "表演", "说服", "手上功夫", "隐匿"],
            "desc": "潜行和偷袭的大师，灵巧而致命，在阴影中行动。"
        },
        {
            "id": "sorcerer",
            "name": "Sorcerer",
            "chinese_name": "术士",
            "hit_die": 6,
            "primary_ability": ["魅力", "体质"],
            "saving_throws": ["魅力", "感知"],
            "armor_proficiency": [],
            "weapon_proficiency": ["匕首", "飞镖", "轻弩", "法杖", "短矛", "投石索"],
            "skills": ["奥秘", "欺骗", "洞察", "威吓", "说服", "宗教"],
            "desc": "天生魔力持有者，魔法融入血液，血脉传承的力量。"
        },
        {
            "id": "warlock",
            "name": "Warlock",
            "chinese_name": "术士契约大师",
            "hit_die": 8,
            "primary_ability": ["魅力", "智力"],
            "saving_throws": ["魅力", "感知"],
            "armor_proficiency": ["轻甲"],
            "weapon_proficiency": ["简易武器"],
            "skills": ["奥秘", "欺骗", "历史", "威吓", "调查", "自然", "宗教"],
            "desc": "与强大存在签订契约，换取魔法力量，从其他维度获得能量。"
        },
        {
            "id": "wizard",
            "name": "Wizard",
            "chinese_name": "法师",
            "hit_die": 6,
            "primary_ability": ["智力", "感知"],
            "saving_throws": ["智力", "感知"],
            "armor_proficiency": [],
            "weapon_proficiency": ["匕首", "飞镖", "轻弩", "法杖", "短矛", "投石索"],
            "skills": ["奥秘", "历史", "洞察", "调查", "医药", "宗教"],
            "desc": "学术型魔法使用者，通过学习和研究获得力量，掌握奥术知识。"
        }
    ],
    "core_races": [
        {"id": "dragonborn", "name": "Dragonborn", "chinese_name": "龙裔", "desc": "龙族传承，拥有呼吸武器和龙族抗性", "ability_bonus": {"力量": 2, "魅力": 1}},
        {"id": "dwarf", "name": "Dwarf", "chinese_name": "矮人", "desc": "坚韧不拔的地下居民，毒素抗性和黑暗视觉", "ability_bonus": {"体质": 2, "感知": 1}},
        {"id": "elf", "name": "Elf", "chinese_name": "精灵", "desc": "敏锐感官，长寿，黑暗视觉和感知陷阱", "ability_bonus": {"敏捷": 2, "魅力": 1}},
        {"id": "gnome", "name": "Gnome", "chinese_name": "侏儒", "desc": "聪明伶俐，幻术亲和，擅长发现魔法", "ability_bonus": {"智力": 2, "敏捷": 1}},
        {"id": "half_elf", "name": "Half-Elf", "chinese_name": "半精灵", "desc": "人类和精灵的血脉，兼具两者天赋", "ability_bonus": {"魅力": 2, "属性": "+1自选"}},
        {"id": "half_orc", "name": "Half-Orc", "chinese_name": "半兽人", "desc": "凶猛无比，具有野蛮力量和韧性", "ability_bonus": {"力量": 2, "体质": 1}},
        {"id": "halfling", "name": "Halfling", "chinese_name": "半身人", "desc": "灵活敏捷，运气好，难以被吓到", "ability_bonus": {"敏捷": 2, "魅力": 1}},
        {"id": "human", "name": "Human", "chinese_name": "人类", "desc": "适应力强，各项能力+1，寿命短暂但成就辉煌", "ability_bonus": {"所有属性": 1}},
        {"id": "tiefling", "name": "Tiefling", "chinese_name": "提夫林", "desc": "恶魔血脉，魔法天赋，内外皆异", "ability_bonus": {"魅力": 2, "智力": 1}}
    ],
    "backgrounds": [
        {"id": "acolyte", "name": "Acolyte", "chinese_name": "信徒", "skill1": "宗教", "skill2": "洞察", "desc": "寺庙背景，了解宗教仪式和圣地"},
        {"id": "charlatan", "name": "Charlatan", "chinese_name": "骗子", "skill1": "欺骗", "skill2": "手上功夫", "desc": "欺诈专家，擅长伪装和骗局"},
        {"id": "criminal", "name": "Criminal", "chinese_name": "罪犯", "skill1": "隐匿", "skill2": "欺骗", "desc": "地下世界关系，熟悉犯罪网络"},
        {"id": "entertainer", "name": "Entertainer", "chinese_name": "艺人", "skill1": "表演", "skill2": "杂技", "desc": "舞台经验，能歌善舞或表演杂技"},
        {"id": "folk_hero", "name": "Folk Hero", "chinese_name": "民间英雄", "skill1": "动物处理", "skill2": "生存", "desc": "平民出身，受草根爱戴"},
        {"id": "guild_artisan", "name": "Guild Artisan", "chinese_name": "行会工匠", "skill1": "Insight", "skill2": "说服", "desc": "商业行会成员，专业技能认证"},
        {"id": "hermit", "name": "Hermit", "chinese_name": "隐士", "skill1": "宗教", "skill2": "医药", "desc": "隐居修行，独处中获得智慧"},
        {"id": "noble", "name": "Noble", "chinese_name": "贵族", "skill1": "历史", "skill2": "说服", "desc": "高贵出身，了解权贵礼仪"},
        {"id": "outlander", "name": "Outlander", "chinese_name": "异乡人", "skill1": "生存", "skill2": "运动", "desc": "来自远方，熟悉异域文化和地理"},
        {"id": "sage", "name": "Sage", "chinese_name": "学者", "skill1": "奥秘", "skill2": "历史", "desc": "博学研究，学术背景深厚"},
        {"id": "sailor", "name": "Sailor", "chinese_name": "水手", "skill1": "运动", "skill2": "感知", "desc": "航海经验，熟悉船舶和海洋"},
        {"id": "soldier", "name": "Soldier", "chinese_name": "士兵", "skill1": "威吓", "skill2": "运动", "desc": "军事背景，战斗训练有素"},
        {"id": "urchin", "name": "Urchin", "chinese_name": "流浪儿", "skill1": "隐匿", "skill2": "手上功夫", "desc": "街头成长，生存技能丰富"}
    ]
}


# ============================================
# Pathfinder 2e (探索者 第二版)
# ============================================
PATHFINDER_2E = {
    "name": "Pathfinder 2nd Edition",
    "chinese_name": "探索者 第二版",
    "system_type": "fantasy",
    "overview": "由Paizo Publishing发行的奇幻跑团系统，承袭D&D 3.5版精华并持续创新。采用升级系统(Boost/Flaw)而非传统投点。",
    "source_urls": [
        "https://2e.aonprd.com/Classes.aspx",
        "https://2e.aonprd.com/Ancestries.aspx",
        "https://2e.aonprd.com/Backgrounds.aspx",
        "https://2e.aonprd.com/Skills.aspx"
    ],
    "ability_scores": [
        {"id": "strength", "name": "力量", "abbr": "STR", "desc": "肌肉力量和体力"},
        {"id": "dexterity", "name": "敏捷", "abbr": "DEX", "desc": "身体灵活性和反射"},
        {"id": "constitution", "name": "体质", "abbr": "CON", "desc": "耐力和健康"},
        {"id": "intelligence", "name": "智力", "abbr": "INT", "desc": "记忆和分析能力"},
        {"id": "wisdom", "name": "感知", "abbr": "WIS", "desc": "直觉、洞察和意志力"},
        {"id": "charisma", "name": "魅力", "abbr": "CHA", "desc": "社交能力和魔法亲和"}
    ],
    "skills": [
        {"id": "acrobatics", "name": "杂技", "ability": "敏捷", "desc": "翻滚、跳跃、平衡"},
        {"id": "arcana", "name": "奥秘", "ability": "智力", "desc": "魔法理论和奥术知识"},
        {"id": "athletics", "name": "运动", "ability": "力量", "desc": "攀爬、游泳、力量检定"},
        {"id": "crafting", "name": "工艺", "ability": "智力", "desc": "制作和修理物品"},
        {"id": "deception", "name": "欺骗", "ability": "魅力", "desc": "撒谎、伪装、洗牌"},
        {"id": "diplomacy", "name": "外交", "ability": "魅力", "desc": "社交、请求、闲聊"},
        {"id": "intimidation", "name": "威吓", "ability": "魅力", "desc": "强迫、恐吓、威胁"},
        {"id": "lore", "name": "学识", "ability": "智力", "desc": "专业领域知识"},
        {"id": "medicine", "name": "医学", "ability": "感知", "desc": "治疗、诊断、卫生"},
        {"id": "nature", "name": "自然", "ability": "智力", "desc": "动植物、生态、环境"},
        {"id": "occultism", "name": "神秘学", "ability": "智力", "desc": "神秘符号、灵异现象"},
        {"id": "performance", "name": "表演", "ability": "魅力", "desc": "戏剧、音乐、舞蹈"},
        {"id": "religion", "name": "宗教", "ability": "智力", "desc": "神祇、宗教实践、神学"},
        {"id": "society", "name": "社会", "ability": "智力", "desc": "文化、习俗、地理知识"},
        {"id": "stealth", "name": "隐匿", "ability": "敏捷", "desc": "潜行、躲藏、悄悄行动"},
        {"id": "survival", "name": "生存", "ability": "感知", "desc": "觅食、追踪、导航"},
        {"id": "thievery", "name": "盗窃", "ability": "敏捷", "desc": "偷窃、开锁、陷阱"}
    ],
    "core_classes": [
        {"id": "alchemist", "name": "Alchemist", "chinese_name": "炼金师", "hit_die": 8, "key_ability": ["智力"], "desc": "药水、炸弹和突变剂的大师，用科学创造魔法效果"},
        {"id": "barbarian", "name": "Barbarian", "chinese_name": "野蛮人", "hit_die": 12, "key_ability": ["力量", "体质"], "desc": "狂暴之力的化身，进入狂怒增强战斗能力"},
        {"id": "bard", "name": "Bard", "chinese_name": "吟游诗人", "hit_die": 8, "key_ability": ["魅力"], "desc": "魔法旋律的操控者，用歌声和表演激发力量"},
        {"id": "champion", "name": "Champion", "chinese_name": "冠军", "hit_die": 10, "key_ability": ["力量", "魅力"], "desc": "神圣誓言的践行者，擅长防御和正义行动"},
        {"id": "cleric", "name": "Cleric", "chinese_name": "牧师", "hit_die": 8, "key_ability": ["感知"], "desc": "神圣力量的管道，能施展神术并获得神恩"},
        {"id": "druid", "name": "Druid", "chinese_name": "德鲁伊", "hit_die": 8, "key_ability": ["感知"], "desc": "自然法则的守护者，能变形为动物并操控自然"},
        {"id": "fighter", "name": "Fighter", "chinese_name": "战士", "hit_die": 10, "key_ability": ["力量", "敏捷"], "desc": "武器大师，战场主宰，精通各种武器"},
        {"id": "gunslinger", "name": "Gunslinger", "chinese_name": "枪客", "hit_die": 10, "key_ability": ["敏捷"], "desc": "枪械武器专家，远程战斗大师"},
        {"id": "inventor", "name": "Inventor", "chinese_name": "发明家", "hit_die": 8, "key_ability": ["智力"], "desc": "创新装置的创造者，发明高科技装备"},
        {"id": "investigator", "name": "Investigator", "chinese_name": "调查员", "hit_die": 8, "key_ability": ["智力"], "desc": "逻辑推理和线索搜寻的大师，擅长分析"},
        {"id": "magus", "name": "Magus", "chinese_name": "魔战士", "hit_die": 8, "key_ability": ["力量", "智力"], "desc": "魔法与武器的完美结合，用剑释放法术"},
        {"id": "monk", "name": "Monk", "chinese_name": "武僧", "hit_die": 8, "key_ability": ["力量", "敏捷"], "desc": "身体即武器，以徒手格斗和气之力见长"},
        {"id": "oracle", "name": "Oracle", "chinese_name": "预言者", "hit_die": 8, "key_ability": ["魅力"], "desc": "神圣诅咒的承载者，同时承受神力与诅咒"},
        {"id": "psychic", "name": "Psychic", "chinese_name": "灵媒", "hit_die": 6, "key_ability": ["感知"], "desc": "心灵异能大师，用意识操控现实"},
        {"id": "ranger", "name": "Ranger", "chinese_name": "游侠", "hit_die": 10, "key_ability": ["敏捷", "感知"], "desc": "荒野生存和追踪专家，与自然和野兽为友"},
        {"id": "rogue", "name": "Rogue", "chinese_name": "游荡者", "hit_die": 8, "key_ability": ["敏捷"], "desc": "潜行、偷袭和灵巧的大师，在阴影中获利"},
        {"id": "sorcerer", "name": "Sorcerer", "chinese_name": "术士", "hit_die": 6, "key_ability": ["魅力"], "desc": "天生魔力血脉，魔法刻印在血液中"},
        {"id": "summoner", "name": "Summoner", "chinese_name": "召唤师", "hit_die": 8, "key_ability": ["魅力"], "desc": "与强大存在建立联系，召唤异界生物伙伴"},
        {"id": "swashbuckler", "name": "Swashbuckler", "chinese_name": "剑客", "hit_die": 10, "key_ability": ["敏捷"], "desc": "优雅而致命的战斗风格，灵活机动作战"},
        {"id": "witch", "name": "Witch", "chinese_name": "巫师", "hit_die": 6, "key_ability": ["智力"], "desc": "从精灵或邪魔处获得魔法，拥有契约魔宠"},
        {"id": "wizard", "name": "Wizard", "chinese_name": "法师", "hit_die": 6, "key_ability": ["智力"], "desc": "学术魔法的掌握者，通过学习和研究掌握奥术"}
    ],
    "core_ancestries": [
        {"id": "dwarf", "name": "Dwarf", "chinese_name": "矮人", "desc": "坚韧不拔的地下居民，平均200年寿命，毒素抗性", "ability_bonus": {"体质": 2, "感知": 2, "魅力": -2}},
        {"id": "elf", "name": "Elf", "chinese_name": "精灵", "desc": "敏锐感官的长寿种族，60年成年，擅长魔法和艺术", "ability_bonus": {"敏捷": 2, "魅力": 2, "体质": -2}},
        {"id": "gnome", "name": "Gnome", "chinese_name": "侏儒", "desc": "好奇心灵巧的种族，平均100年寿命，魔法亲和", "ability_bonus": {"智力": 2, "魅力": 2, "力量": -2}},
        {"id": "goblin", "name": "Goblin", "chinese_name": "地精", "desc": "适应力强的小型种族，恶名昭彰但正在改变形象", "ability_bonus": {"敏捷": 2, "魅力": 2, "智力": -2}},
        {"id": "halfling", "name": "Halfling", "chinese_name": "半身人", "desc": "幸运灵活的小型种族，平均150年寿命", "ability_bonus": {"敏捷": 2, "魅力": 2, "力量": -2}},
        {"id": "human", "name": "Human", "chinese_name": "人类", "desc": "适应性强，寿命短暂但成就辉煌，可选+2任意两项", "ability_bonus": {"所有属性": 1}},
        {"id": "leshy", "name": "Leshy", "chinese_name": "植物灵", "desc": "植物形态的类人种族，由植物种子创造", "ability_bonus": {"感知": 2, "智力": 2, "力量": -2}},
        {"id": "lizardfolk", "name": "Lizardfolk", "chinese_name": "蜥蜴人", "desc": "爬行动物传承，冷血生物，适应沼泽环境", "ability_bonus": {"力量": 2, "感知": 2, "魅力": -2}},
        {"id": "catfolk", "name": "Catfolk", "chinese_name": "猫人", "desc": "猫科动物特征，猫灵族后裔，灵活敏捷", "ability_bonus": {"敏捷": 2, "魅力": 2, "体质": -2}},
        {"id": "ratfolk", "name": "Ratfolk", "chinese_name": "鼠人", "desc": "鼠类特征，群居小型种族，擅长工程和交易", "ability_bonus": {"敏捷": 2, "智力": 2, "魅力": -2}},
        {"id": "orc", "name": "Orc", "chinese_name": "兽人", "desc": "强壮的战士种族，战斗血脉传承", "ability_bonus": {"力量": 2, "体质": 2, "智力": -2}}
    ],
    "backgrounds": [
        {"id": "acolyte", "name": "Acolyte", "chinese_name": "信徒", "ability_bonus": {"智力": 1, "感知": 1}, "skill1": "宗教", "skill2": "学识", "desc": "寺庙生活，了解宗教仪式"},
        {"id": "animal_whisperer", "name": "Animal Whisperer", "chinese_name": "动物之声", "ability_bonus": {"感知": 1, "魅力": 1}, "skill1": "自然", "skill2": "外交", "desc": "与动物交流的天赋"},
        {"id": "artist", "name": "Artist", "chinese_name": "艺术家", "ability_bonus": {"魅力": 1, "智力": 1}, "skill1": "表演", "skill2": "工艺", "desc": "艺术创作和展示"},
        {"id": "barkeep", "name": "Barkeep", "chinese_name": "酒保", "ability_bonus": {"魅力": 1, "感知": 1}, "skill1": "外交", "skill2": "欺骗", "desc": "社交达人，消息灵通"},
        {"id": "bounty_hunter", "name": "Bounty Hunter", "chinese_name": "赏金猎人", "ability_bonus": {"力量": 1, "感知": 1}, "skill1": "威吓", "skill2": "生存", "desc": "追踪专家，追捕逃犯"},
        {"id": "charlatan", "name": "Charlatan", "chinese_name": "骗子", "ability_bonus": {"魅力": 1, "智力": 1}, "skill1": "欺骗", "skill2": "盗窃", "desc": "欺诈专家，擅长骗局"},
        {"id": "criminal", "name": "Criminal", "chinese_name": "罪犯", "ability_bonus": {"敏捷": 1, "魅力": 1}, "skill1": "隐匿", "skill2": "欺骗", "desc": "地下经验，熟悉犯罪网络"},
        {"id": "detective", "name": "Detective", "chinese_name": "侦探", "ability_bonus": {"智力": 1, "感知": 1}, "skill1": "调查", "skill2": "威吓", "desc": "推理能力，犯罪调查专精"},
        {"id": "farmer", "name": "Farmer", "chinese_name": "农民", "ability_bonus": {"体质": 1, "感知": 1}, "skill1": "自然", "skill2": "农业学识", "desc": "耕作技能，自给自足"},
        {"id": "gambler", "name": "Gambler", "chinese_name": "赌徒", "ability_bonus": {"魅力": 1, "智力": 1}, "skill1": "欺骗", "skill2": "外交", "desc": "概率计算，街头博弈"},
        {"id": "guard", "name": "Guard", "chinese_name": "守卫", "ability_bonus": {"力量": 1, "魅力": 1}, "skill1": "威吓", "skill2": "Athletics", "desc": "执法背景，维护秩序"},
        {"id": "herbalist", "name": "Herbalist", "chinese_name": "草药师", "ability_bonus": {"感知": 1, "智力": 1}, "skill1": "医学", "skill2": "自然", "desc": "草药知识，治疗专家"},
        {"id": "hermit", "name": "Hermit", "chinese_name": "隐士", "ability_bonus": {"智力": 1, "感知": 1}, "skill1": "神秘学", "skill2": "医学", "desc": "独居修行，获得隐秘知识"},
        {"id": "hunter", "name": "Hunter", "chinese_name": "猎人", "ability_bonus": {"力量": 1, "感知": 1}, "skill1": "自然", "skill2": "生存", "desc": "狩猎技能，野外追踪"},
        {"id": "merchant", "name": "Merchant", "chinese_name": "商人", "ability_bonus": {"魅力": 1, "智力": 1}, "skill1": "外交", "skill2": "商业学识", "desc": "交易经验，商业技能"},
        {"id": "noble", "name": "Noble", "chinese_name": "贵族", "ability_bonus": {"魅力": 1, "感知": 1}, "skill1": "外交", "skill2": "历史", "desc": "上流社会，高贵出身"},
        {"id": "scholar", "name": "Scholar", "chinese_name": "学者", "ability_bonus": {"智力": 1, "感知": 1}, "skill1": "奥秘", "skill2": "宗教", "desc": "学术研究，知识渊博"},
        {"id": "sailor", "name": "Sailor", "chinese_name": "水手", "ability_bonus": {"敏捷": 1, "体质": 1}, "skill1": "运动", "skill2": "航行学识", "desc": "海上生活，航海经验"},
        {"id": "soldier", "name": "Soldier", "chinese_name": "士兵", "ability_bonus": {"力量": 1, "感知": 1}, "skill1": "运动", "skill2": "威吓", "desc": "军事背景，战斗训练"},
        {"id": "tinker", "name": "Tinker", "chinese_name": "工匠", "ability_bonus": {"敏捷": 1, "智力": 1}, "skill1": "工艺", "skill2": "杂技", "desc": "修理技能，发明小装置"}
    ]
}


# ============================================
# Call of Cthulhu (克苏鲁的呼唤)
# ============================================
CALL_OF_CTHULHU = {
    "name": "Call of Cthulhu",
    "chinese_name": "克苏鲁的呼唤",
    "system_type": "horror",
    "overview": "以H.P. Lovecraft的克苏鲁神话为背景的调查型恐怖跑团系统，由Chaosium发行。玩家扮演调查员，面对古老邪恶。",
    "source_urls": [
        "https://cthulhuwiki.chaosium.com/investigators/step-three-occupation-and-skills.html",
        "https://call-of-cthulhu-nachtstadt-berlin.fandom.com/wiki/Occupation_List",
        "https://roll20.net/compendium/coc/Index:Occupations"
    ],
    "characteristics": [
        {"id": "str", "name": "力量", "abbr": "STR", "roll": "3d6", "desc": "肌肉力量，影响伤害和负载"},
        {"id": "con", "name": "体质", "abbr": "CON", "roll": "3d6", "desc": "健康和耐力，影响生命值"},
        {"id": "siz", "name": "体型", "abbr": "SIZ", "roll": "2d6+6", "desc": "身高体重，影响生命值和体型"},
        {"id": "dex", "name": "敏捷", "abbr": "DEX", "roll": "3d6", "desc": "身体速度，影响先攻和闪避"},
        {"id": "app", "name": "外貌", "abbr": "APP", "roll": "3d6", "desc": "外表和魅力，影响社交"},
        {"id": "int", "name": "灵感", "abbr": "INT", "roll": "2d6+6", "desc": "感知和直觉，影响发现线索"},
        {"id": "pow", "name": "意志", "abbr": "POW", "roll": "3d6", "desc": "精神力量，影响魔法和理智"},
        {"id": "edu", "name": "教育", "abbr": "EDU", "roll": "2d6+6", "desc": "知识和学习，影响技能上限"},
        {"id": "luck", "name": "运气", "abbr": "LUCK", "roll": "3d6", "desc": "运气值，用于幸运检定"},
        {"id": "san", "name": "理智", "abbr": "SAN", "derived": true, "desc": "心理健康，对抗恐怖"},
        {"id": "hp", "name": "生命值", "abbr": "HP", "derived": true, "desc": "身体伤害承受力"},
        {"id": "mp", "name": "魔力值", "abbr": "MP", "derived": true, "desc": "施展魔法消耗"},
        {"id": "move", "name": "移动力", "abbr": "MOV", "derived": true, "desc": "每轮移动距离"}
    ],
    "skills": [
        {"id": "accounting", "name": "会计", "base": 5, "ability": "智力", "desc": "账目管理、财务分析"},
        {"id": "anthropology", "name": "人类学", "base": 1, "ability": "智力", "desc": "文化研究，理解异域文化"},
        {"id": "appraise", "name": "估价", "base": 20, "ability": "智力", "desc": "物品价值评估"},
        {"id": "archaeology", "name": "考古学", "base": 1, "ability": "智力", "desc": "古代遗迹研究，挖掘技术"},
        {"id": "art_craft", "name": "艺术/手艺", "base": 5, "ability": "智力", "desc": "艺术创作或专业手工艺"},
        {"id": "charm", "name": "魅惑", "base": 15, "ability": "外貌", "desc": "社交魅力，说服他人"},
        {"id": "climb", "name": "攀爬", "base": 20, "ability": "力量", "desc": "攀爬墙壁和绳索"},
        {"id": "credit_rating", "name": "信用评级", "base": 20, "ability": "外貌", "desc": "社会地位和财富水平"},
        {"id": "cthulhu_mythos", "name": "克苏鲁神话", "base": 0, "ability": "智力", "desc": "对神话的了解，每次增加理智损失"},
        {"id": "disguise", "name": "伪装", "base": 5, "ability": "外貌", "desc": "改变外貌欺骗他人"},
        {"id": "dodge", "name": "闪避", "base": "DEXx2", "ability": "敏捷", "desc": "躲避攻击，速度决定上限"},
        {"id": "drive_auto", "name": "驾驶汽车", "base": 20, "ability": "敏捷", "desc": "汽车驾驶技能"},
        {"id": "elec_repair", "name": "电器维修", "base": 10, "ability": "智力", "desc": "电器和电子产品修理"},
        {"id": "fast_talk", "name": "话术", "base": 5, "ability": "外貌", "desc": "言语操控，快速说服"},
        {"id": "fighting_brawl", "name": "格斗(肉搏)", "base": 25, "ability": "力量", "desc": "徒手战斗和近战武器"},
        {"id": "firearms_handgun", "name": "射击(手枪)", "base": 20, "ability": "敏捷", "desc": "手枪使用"},
        {"id": "firearms_rifle", "name": "射击(步枪)", "base": 20, "ability": "敏捷", "desc": "步枪和猎枪使用"},
        {"id": "firearms_smg", "name": "射击(冲锋枪)", "base": 15, "ability": "敏捷", "desc": "冲锋枪和自动武器"},
        {"id": "first_aid", "name": "急救", "base": 30, "ability": "智力", "desc": "基础医疗处理"},
        {"id": "history", "name": "历史", "base": 20, "ability": "智力", "desc": "历史知识和事件"},
        {"id": "intimidate", "name": "威吓", "base": 15, "ability": "外貌", "desc": "强迫他人服从"},
        {"id": "jump", "name": "跳跃", "base": 20, "ability": "力量", "desc": "跳跃和落地"},
        {"id": "language_other", "name": "其他语言", "base": 1, "ability": "智力", "desc": "外语能力，可多次选择"},
        {"id": "language_own", "name": "母语", "base": "EDUx2", "ability": "教育", "desc": "母语技能上限"},
        {"id": "law", "name": "法律", "base": 5, "ability": "智力", "desc": "法律知识和司法系统"},
        {"id": "library_use", "name": "图书馆使用", "base": 20, "ability": "智力", "desc": "资料研究和文献检索"},
        {"id": "listen", "name": "聆听", "base": 25, "ability": "感知", "desc": "听觉感知，发现声音"},
        {"id": "locksmith", "name": "开锁", "base": 1, "ability": "敏捷", "desc": "开锁和破解机械"},
        {"id": "mech_repair", "name": "机械维修", "base": 10, "ability": "智力", "desc": "机械设备和引擎修理"},
        {"id": "medicine", "name": "医学", "base": 1, "ability": "智力", "desc": "医疗诊断和治疗"},
        {"id": "natural_world", "name": "自然世界", "base": 10, "ability": "智力", "desc": "自然界和生物学知识"},
        {"id": "navigate", "name": "导航", "base": 10, "ability": "感知", "desc": "方向感和地图使用"},
        {"id": "occult", "name": "神秘学", "base": 5, "ability": "智力", "desc": "神秘知识和神秘学"},
        {"id": "op_hv_machine", "name": "操作重型机械", "base": 1, "ability": "力量", "desc": "重型机械和工业设备操作"},
        {"id": "persuade", "name": "说服", "base": 10, "ability": "外貌", "desc": "理性说服和谈判"},
        {"id": "pilot", "name": "驾驶(特殊载具)", "base": 1, "ability": "敏捷", "desc": "特殊载具驾驶(飞机、船舶等)"},
        {"id": "psychoanalysis", "name": "心理分析", "base": 1, "ability": "感知", "desc": "治疗理智丧失"},
        {"id": "psychology", "name": "心理学", "base": 10, "ability": "感知", "desc": "理解他人心理状态"},
        {"id": "ride", "name": "骑乘", "base": 5, "ability": "敏捷", "desc": "骑行动物"},
        {"id": "search", "name": "搜索", "base": 20, "ability": "感知", "desc": "发现隐藏物品和线索"},
        {"id": "sleight_of_hand", "name": "手上功夫", "base": 5, "ability": "敏捷", "desc": "灵巧操作和偷窃"},
        {"id": "spot_hidden", "name": "发现隐藏", "base": 25, "ability": "感知", "desc": "发现隐藏事物和秘密"},
        {"id": "survival", "name": "生存", "base": 10, "ability": "感知", "desc": "野外生存技能"},
        {"id": "swim", "name": "游泳", "base": 20, "ability": "力量", "desc": "游泳能力"},
        {"id": "throw", "name": "投掷", "base": 20, "ability": "力量", "desc": "投掷物体准确性"},
        {"id": "track", "name": "追踪", "base": 10, "ability": "感知", "desc": "追踪足迹和气味"}
    ],
    "occupations": [
        {"id": "accountant", "name": "会计", "skill_pts": 60, "credit": "20-50", "desc": "账目管理和财务分析"},
        {"id": "acrobat", "name": "杂技师", "skill_pts": 60, "credit": "10-50", "desc": "表演和身体技巧"},
        {"id": "actor", "name": "演员", "skill_pts": 60, "credit": "30-70", "desc": "表演艺术和戏剧"},
        {"id": "antiquarian", "name": "古董商", "skill_pts": 60, "credit": "50-90", "desc": "古董交易和鉴赏"},
        {"id": "archaeologist", "name": "考古学家", "skill_pts": 60, "credit": "30-70", "desc": "古代遗迹发掘和研究"},
        {"id": "artist", "name": "艺术家", "skill_pts": 60, "credit": "20-70", "desc": "视觉艺术创作"},
        {"id": "author", "name": "作家", "skill_pts": 60, "credit": "20-60", "desc": "文学创作和写作"},
        {"id": "bartender", "name": "酒保", "skill_pts": 60, "credit": "20-50", "desc": "酒吧服务和社交"},
        {"id": "burglar", "name": "窃贼", "skill_pts": 60, "credit": "10-40", "desc": "入室盗窃和潜行"},
        {"id": "clergy", "name": "神职人员", "skill_pts": 60, "credit": "20-50", "desc": "宗教服务和信仰"},
        {"id": "college_professor", "name": "大学教授", "skill_pts": 60, "credit": "50-80", "desc": "高等教育和研究"},
        {"id": "detective", "name": "侦探", "skill_pts": 60, "credit": "20-50", "desc": "犯罪调查和推理"},
        {"id": "dilettante", "name": "纨绔子弟", "skill_pts": 60, "credit": "50-90", "desc": "收藏和社交名流"},
        {"id": "doctor", "name": "医生", "skill_pts": 60, "credit": "50-80", "desc": "医疗诊断和治疗"},
        {"id": "drifter", "name": "流浪者", "skill_pts": 60, "credit": "5-30", "desc": "四处漂泊，随遇而安"},
        {"id": "engineer", "name": "工程师", "skill_pts": 60, "credit": "40-70", "desc": "技术设计和建造"},
        {"id": "entertainer", "name": "艺人", "skill_pts": 60, "credit": "20-60", "desc": "舞台表演和娱乐"},
        {"id": "federal_agent", "name": "联邦特工", "skill_pts": 60, "credit": "40-70", "desc": "政府执法工作"},
        {"id": "hacker", "name": "黑客", "skill_pts": 60, "credit": "30-60", "desc": "计算机和网络技术"},
        {"id": "journalist", "name": "记者", "skill_pts": 60, "credit": "20-60", "desc": "新闻采编和信息收集"},
        {"id": "lawyer", "name": "律师", "skill_pts": 60, "credit": "50-90", "desc": "法律服务和诉讼"},
        {"id": "librarian", "name": "图书管理员", "skill_pts": 60, "credit": "20-50", "desc": "资料管理和研究"},
        {"id": "military_officer", "name": "军官", "skill_pts": 60, "credit": "30-60", "desc": "军事指挥和战术"},
        {"id": "occultist", "name": "神秘学者", "skill_pts": 60, "credit": "20-60", "desc": "神秘学研究和实践"},
        {"id": "pilot", "name": "飞行员", "skill_pts": 60, "credit": "40-70", "desc": "飞行器和航空"},
        {"id": "police_detective", "name": "警探", "skill_pts": 60, "credit": "30-60", "desc": "执法和犯罪调查"},
        {"id": "private_eye", "name": "私家侦探", "skill_pts": 60, "credit": "20-50", "desc": "调查和跟踪服务"},
        {"id": "professor", "name": "教授", "skill_pts": 60, "credit": "50-80", "desc": "学术研究和教学"},
        {"id": "scientist", "name": "科学家", "skill_pts": 60, "credit": "40-70", "desc": "实验和研究工作"},
        {"id": "soldier", "name": "士兵", "skill_pts": 60, "credit": "10-40", "desc": "军事训练和战斗"},
        {"id": "undefined", "name": "无业游民", "skill_pts": 60, "credit": "1-10", "desc": "街头生存和零工"},
        {"id": "zealous", "name": "狂信者", "skill_pts": 60, "credit": "1-30", "desc": "极端信仰和狂热"}
    ],
    "eras": [
        {"id": "1890s", "name": "1890年代", "desc": "维多利亚时代末期，工业革命后期，神秘学流行"},
        {"id": "1920s", "name": "1920年代", "desc": "咆哮的二十年代，爵士乐时代，最经典设定"},
        {"id": "modern", "name": "现代", "desc": "当代设定，科技与古老邪恶并存"}
    ]
}


# ============================================
# 天道适配 - 将主流系统适配到天道系统
# ============================================

def adapt_to_tiandao(trpg_system, target_world_type=None):
    """
    将主流TRPG系统适配到天道系统

    Args:
        trpg_system: TRPG系统数据
        target_world_type: 目标世界类型，默认继承原系统类型
            fantasy - 奇幻世界
            urban - 现代都市
            sci_fi - 科幻世界
            horror - 恐怖世界

    Returns:
        天道格式的世界适配数据
    """
    if target_world_type is None:
        target_world_type = trpg_system.get("system_type", "fantasy")

    adapted = {
        "source_system": trpg_system.get("name"),
        "source_name_cn": trpg_system.get("chinese_name"),
        "world_type": target_world_type,
        "overview": trpg_system.get("overview", ""),
        "source_urls": trpg_system.get("source_urls", []),
        "character_options": {
            "ability_scores": trpg_system.get("ability_scores", trpg_system.get("characteristics", [])),
            "skills": trpg_system.get("skills", []),
            "classes": trpg_system.get("core_classes", []),
            "races": trpg_system.get("core_races", trpg_system.get("core_ancestries", [])),
            "backgrounds": trpg_system.get("backgrounds", trpg_system.get("occupations", []))
        },
        "gameplay_features": []
    }

    # 根据系统类型添加特定玩法特征
    if trpg_system.get("system_type") == "fantasy":
        adapted["gameplay_features"].extend([
            "经典奇幻职业体系",
            "种族/职业组合",
            "等级成长系统",
            "施法职业和法术位",
            "专长和技能熟练"
        ])
    elif trpg_system.get("system_type") == "horror":
        adapted["gameplay_features"].extend([
            "理智系统(SAN)",
            "调查推理",
            "恐怖氛围营造",
            "克苏鲁神话",
            "时代背景设定",
            "职业决定技能"
        ])

    return adapted


# 导出所有系统
TRPG_SYSTEMS = {
    "dnd_5e": DND_5E,
    "pathfinder_2e": PATHFINDER_2E,
    "call_of_cthulhu": CALL_OF_CTHULHU
}


# 获取所有系统的天道适配版本
def get_all_adapted_systems():
    """获取所有TRPG系统的天道适配版本"""
    return {
        "dnd_5e_fantasy": adapt_to_tiandao(DND_5E, "fantasy"),
        "pathfinder_2e_fantasy": adapt_to_tiandao(PATHFINDER_2E, "fantasy"),
        "coc_horror": adapt_to_tiandao(CALL_OF_CTHULHU, "horror")
    }


# 根据ID获取特定系统
def get_system(system_id):
    """根据ID获取TRPG系统"""
    return TRPG_SYSTEMS.get(system_id)


def get_adapted_system(system_id, world_type=None):
    """获取适配后的天道系统"""
    system = TRPG_SYSTEMS.get(system_id)
    if system:
        return adapt_to_tiandao(system, world_type)
    return None
