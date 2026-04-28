"""
天道 TRPG - 武侠世界适配数据
基于金庸x设计理念 + 龙藏世界观 + 古龙江湖体系 + MUD经典设计

整合来源:
- 金庸x.txt: 门派跑团核心规则设计
- 龙藏: 青龙会千年历史,组织进化论武侠
- 我在射雕/少年歌行: 跨次元设定参考
- 北大侠客行/放置江湖/汉家江湖: MUD和放置类武侠游戏设计参考

MUD设计理念:
- 文字驱动,想象空间无限
- 命令式交互 (look/north/fight/get等)
- 房间探索与区域导航
- 经验升级与技能修炼
- 文本战斗叙述与随机性
"""

# ============================================
# 天道武侠世界 - 金庸x (金庸武侠跑团)
# ============================================
JINYONG_TRPG = {
    "name": "金庸x - 欢乐侠客行",
    "chinese_name": "金庸武林团",
    "system_type": "wuxia",
    "overview": "以金庸武侠世界为背景的欢乐文字派对跑团。玩家扮演初入江湖的小虾米,通过文字探索、触发事件、做出抉择,共同经历一段充满变数和欢乐的江湖历程。",
    "source_docs": ["金庸x.txt"],
    "gameplay_mode": "派对跑团/文字MUD",
    "max_players": 8,
    "estimated_duration": "30-60分钟一局",

    "attributes": [
        {"id": "constitution", "name": "体质", "abbr": "体质", "desc": "决定生命值上限"},
        {"id": "strength", "name": "力量", "abbr": "力量", "desc": "决定基础攻击力"},
        {"id": "dexterity", "name": "敏捷", "abbr": "敏捷", "desc": "决定闪避检定成功率"}
    ],

    "talents": [
        {"id": "lucky_star", "name": "福星高照", "desc": "每次投掷骰子后,可大喊\"福星高照!\"并重掷一次,新结果必须接受"},
        {"id": "smooth_tongue", "name": "三寸不烂", "desc": "说服和欺骗检定+2"},
        {"id": "iron_skin", "name": "铜皮铁骨", "desc": "受到伤害-1"},
        {"id": "fast_foot", "name": "凌波微步", "desc": "闪避检定+2"},
        {"id": "sharp_eye", "name": "洞察秋毫", "desc": "发现隐藏物品和线索+2"},
        {"id": "silver_tongue", "name": "妙手仁心", "desc": "治疗和修复检定+2"},
        {"id": "money_bag", "name": "财运亨通", "desc": "每场任务结束后,额外获得10%银两"},
        {"id": "martial_talent", "name": "武学天赋", "desc": "学习新武功时,所需经验-10%"}
    ],

    "combat_types": [
        {"id": "gangkuang", "name": "刚猛", "beats": "lingqiao", "desc": "刚猛型武功,克制灵巧型"},
        {"id": "lingqiao", "name": "灵巧", "beats": "neigong", "desc": "灵巧型武功,克制内功型"},
        {"id": "neigong", "name": "内功", "beats": "gangkuang", "desc": "内功型武功,克制刚猛型"}
    ],

    "sects": [
        {"id": "shaolin", "name": "少林派", "location": "河南嵩山", "style": "刚猛", "desc": "天下武学正宗,以降魔掌、易筋经闻名"},
        {"id": "wudang", "name": "武当派", "location": "湖北武当山", "style": "内功", "desc": "以柔克刚,太极拳剑独步天下"},
        {"id": "gaibang", "name": "丐帮", "location": "天下各处", "style": "灵巧", "desc": "天下第一大帮,打狗棒法和降龙十八掌名震江湖"},
        {"id": "emei", "name": "峨眉派", "location": "四川峨眉山", "style": "内功", "desc": "女子当家,九阴真经传人或有渊源"},
        {"id": "huashan", "name": "华山派", "location": "陕西华山", "style": "灵巧", "desc": "剑宗气宗之争,独孤九剑传说所在"},
        {"id": "songshan", "name": "嵩山派", "location": "河南嵩山", "style": "刚猛", "desc": "五岳剑派之一,寒冰真气闻名"},
        {"id": "qingcheng", "name": "青城派", "location": "四川青城山", "style": "灵巧", "desc": "摧心掌名震江湖"},
        {"id": "tiandihui", "name": "天地会", "location": "天下各处", "style": "灵巧", "desc": "反清复明,秘密结社"},
        {"id": "mingjiao", "name": "明教", "location": "光明顶", "style": "刚猛", "desc": "乾坤大挪移,抗元志士"},
        {"id": "tang", "name": "唐门", "location": "四川唐家堡", "style": "灵巧", "desc": "暗器和毒术独步天下"}
    ],

    "basic_skills": [
        {"id": "punch", "name": "基础拳脚", "type": "灵巧", "damage_bonus": 0, "desc": "最基础的拳脚功夫"}
    ],

    "martial_arts": [
        {"id": "xianglong", "name": "降龙十八掌", "type": "刚猛", "damage_bonus": 5, "special": "命中后,对方下回合无法闪避", "requirement": "力量3+"},
        {"id": "yijing", "name": "易筋经", "type": "内功", "damage_bonus": 3, "special": "每场战斗开始时,恢复1点生命", "requirement": "体质3+"},
        {"id": "fight_dog", "name": "打狗棒法", "type": "灵巧", "damage_bonus": 4, "special": "对丐帮成员伤害+2", "requirement": "敏捷3+"},
        {"id": "dugu", "name": "独孤九剑", "type": "灵巧", "damage_bonus": 6, "special": "必定命中,无视闪避", "requirement": "敏捷4+"},
        {"id": "lingsu", "name": "凌波微步", "type": "灵巧", "damage_bonus": 2, "special": "闪避检定+3", "requirement": "敏捷3+"},
        {"id": "ruyi", "name": "如意刀法", "type": "灵巧", "damage_bonus": 3, "special": "连击概率+20%", "requirement": "敏捷2+"},
        {"id": "jiuyin", "name": "九阴真经", "type": "内功", "damage_bonus": 5, "special": "所有检定+1", "requirement": "体质3+ 智力3+"},
        {"id": "jiuyang", "name": "九阳神功", "type": "内功", "damage_bonus": 4, "special": "抗毒+3,生命上限+2", "requirement": "体质4+"},
        {"id": "taiji", "name": "太极拳剑", "type": "内功", "damage_bonus": 3, "special": "受到伤害-2,可反弹", "requirement": "体质3+ 敏捷3+"},
        {"id": "qiankun", "name": "乾坤大挪移", "type": "内功", "damage_bonus": 5, "special": "可转移伤害给队友", "requirement": "体质3+ 智力3+"},
        {"id": "yuehua", "name": "月华真力", "type": "内功", "damage_bonus": 4, "special": "夜间伤害+2", "requirement": "敏捷3+"}
    ],

    "mission_types": {
        "sect_missions": {"count": 50, "desc": "门派玩家稳定的成长途径"},
        "encounter_missions": {
            "unique": {"count": 100, "desc": "只会触发一次,提供独特史诗级剧情体验"},
            "normal": {"count": 200, "desc": "可重复触发,提供稳定资源和银两获取"}
        },
        "public_events": {"count": 50, "desc": "世界级事件,强制所有玩家共同参与", "examples": ["华山论剑", "襄阳守城战", "围攻光明顶"]}
    },

    "social_features": {
        "teamwork": {
            "reward_distribution": "成功后所有奖励随机平分",
            "punishment_distribution": "失败后惩罚全体队员共同承担"
        },
        "trading": {
            "free_trade": "银两、药品、材料、非绑定秘籍可自由交易",
            "restricted": "门派独门绝学不可交易,违者被缉拿"
        },
        "punishment_system": {
            "death": {
                "location": "阴间",
                "keeper": "摆渡人",
                "actions_per_turn": 3,
                "resurrection": "需活着的玩家寻找天山雪莲等天材地宝"
            },
            "imprisonment": {
                "cause": "贩卖门派武学被抓3次",
                "location": "门派牢房",
                "actions_per_turn": 3,
                "escape_options": ["疏通关系赎人", "组队劫狱"]
            }
        }
    },

    "victory_conditions": [
        "习得三门绝世武功",
        "个人财富达到500两",
        "成功营救一名死亡/被拘禁的队友",
        "成为门派掌门",
        "完成门派主线任务"
    ]
}


# ============================================
# 天道武侠世界 - 龙藏 (古龙江湖)
# ============================================
LONGCANG_WORLD = {
    "name": "龙藏 - 青龙会千年史",
    "chinese_name": "龙藏江湖",
    "system_type": "wuxia",
    "overview": "古龙同人史诗,讲述墨家尚同会异化为青龙会的千年历程。组织进化论与社会学武侠的融合。",
    "source_docs": ["龙藏.md", "龙藏大纲.md", "龙藏_小说.txt"],
    "gameplay_mode": "剧情向/组织博弈",

    "eras": [
        {"id": "jin", "name": "东晋", "period": "永嘉之乱", "desc": "五胡乱华,墨家起源,人如零件"},
        {"id": "tang", "name": "唐代", "period": "武德至麟德", "desc": "不良人共生,国家经络窃取"},
        {"id": "song", "name": "北宋", "period": "庆历至宣和", "desc": "金融霸权,金蝉脱壳"},
        {"id": "yuan", "name": "元代", "period": "至元至大德", "desc": "养蛊制度,白玉京崛起"},
        {"id": "ming_early", "name": "明初", "period": "洪武至永乐", "desc": "七种武器时代,无鞘刀屠龙"},
        {"id": "ming_late", "name": "明中后期", "period": "正德至万历", "desc": "权力帮崛起,傅红雪终结公子羽"},
        {"id": "qing", "name": "清末", "period": "康熙之后", "desc": "墨魂弥散,向死而生"}
    ],

    "green_dragon_society": {
        "original_name": "尚同会",
        "founder": "苏生",
        "ideology": "兼爱非攻",
        "history": "墨家理想主义组织,经历代龙头异化为窃国者",
        "structure": "十二堂口,沈矩创立",
        "twelve_dragon_heads": {
            "spring": [
                {"id": "zhengyue", "name": "正月堂.财神", "desc": "掌控财富与金融"},
                {"id": "eryue", "name": "二月堂.媒灵", "desc": "情报与暗杀"},
                {"id": "sanyue", "name": "三月堂.粮王", "desc": "漕运与粮食控制"}
            ],
            "summer": [
                {"id": "siyue", "name": "四月堂.礼官", "desc": "外交与礼仪"},
                {"id": "wuyue", "name": "五月堂.药师", "desc": "医术与毒术"},
                {"id": "liuyue", "name": "六月堂.工头", "desc": "机关与建造"}
            ],
            "autumn": [
                {"id": "qiyue", "name": "七月堂.杀星", "desc": "执行与清除"},
                {"id": "bayue", "name": "八月堂.镖头", "desc": "护卫与押运"},
                {"id": "jiuyue", "name": "九月堂.匠神", "desc": "武器与装备"}
            ],
            "winter": [
                {"id": "shiyue", "name": "十月堂.织女", "desc": "情报网络"},
                {"id": "shiyiyue", "name": "十一月堂.教父", "desc": "地下秩序"},
                {"id": "shieryue", "name": "十二月堂.丑", "desc": "凛冬堂(守墓人)、腊月堂(背尸人)"}
            ]
        }
    },

    "core_concepts": [
        {"id": "pingzhang", "name": "平账", "desc": "杀人、灭门、吞并在作者笔下都是会计行为,历史本质是资源配置"},
        {"id": "mudaoshi", "name": "磨刀石", "desc": "每一代龙头对主角来说都只是提升初始之刃完成度的工具"},
        {"id": "kongwei", "name": "空位", "desc": "龙首空缺或钥匙断裂,暗示权力本质是真空,引诱贪婪者前赴后继"}
    ],

    "key_characters": [
        {"id": "susheng", "name": "苏生", "era": "晋", "role": "墨家创始人", "desc": "极端理性与生存,将人变成零件"},
        {"id": "jinglie", "name": "荆烈", "era": "唐", "role": "黑衣门首领", "desc": "借玄武门之变与李世民交易"},
        {"id": "duanmuchou", "name": "端木筹", "era": "宋", "role": "大龙首", "desc": "通过金融贸易控制国命,金蝉脱壳"},
        {"id": "fangyiru", "name": "方亦儒", "era": "宋末", "role": "理想主义者", "desc": "试图救国,崖山力竭而亡"},
        {"id": "baiyujing", "name": "白玉京/长生", "era": "元", "role": "七月龙头", "desc": "设计十年杀局,写下青龙秘录后隐退"},
        {"id": "wushuangdao", "name": "无鞘刀", "era": "明", "role": "初始之刃", "desc": "纯粹武道的化身,以武力审判腐朽权谋"},
        {"id": "shenlang", "name": "沈浪", "era": "明", "role": "沈规后代", "desc": "凛冬堂人,散尽家财隐居海外"},
        {"id": "wanglianhua", "name": "王怜花", "era": "明", "role": "五月堂传人", "desc": "医术毒术真传,与沈浪亦敌亦友归隐"},
        {"id": "gongziyu", "name": "公子羽", "era": "明", "role": "沈矩后代旁支", "desc": "整合青龙会,被傅红雪所杀"},
        {"id": "fuhongxue", "name": "傅红雪", "era": "明", "role": "复仇者", "desc": "无意识终结青龙会最后希望的悲剧英雄"}
    ],

    "key_martial_arts": [
        {"id": "wushuang_blade", "name": "无鞘刀", "desc": "纯粹武道,刀出无回,极致意志的象征"},
        {"id": "changsheng_sword", "name": "长生剑", "desc": "白玉京佩剑,后传于江湖"},
        {"id": "qiankun_move", "name": "乾坤大挪移", "desc": "明教镇教之宝"},
        {"id": "secret_records", "name": "青龙秘录", "desc": "白玉京所写,记录各堂口死穴,屠龙术"}
    ],

    "themes": [
        "组织进化论 - 理想如何在历史中异化",
        "权力的寄生 - 不同时代权力的不同载体",
        "结构主义武侠 - 杀人是对结构缺陷的物理拆解",
        "屠龙者与恶龙 - 终极辩证与宿命悲观",
        "向死而生 - 墨魂以更纯粹的形态融入江湖"
    ]
}


# ============================================
# 天道武侠世界 - 江湖百晓生 (综合武侠)
# ============================================
BAIXIAOSHENG_WORLD = {
    "name": "江湖百晓生",
    "chinese_name": "综合武侠世界",
    "system_type": "wuxia",
    "overview": "整合金庸、古龙、梁羽生等主流武侠世界观,提供综合性的武侠跑团舞台。",
    "source_docs": ["我在射雕.txt", "我在少年歌行当乐子人.txt", "假说参考地图.md"],

    "factions": [
        {"id": "shaolin", "name": "少林寺", "alignment": "正道", "desc": "天下武学正宗,执武林牛耳"},
        {"id": "wudang", "name": "武当派", "alignment": "正道", "desc": "以柔克刚,道家风骨"},
        {"id": "emei", "name": "峨眉派", "alignment": "正道", "desc": "女子当家,亦正亦邪"},
        {"id": "gaibang", "name": "丐帮", "alignment": "正道", "desc": "天下第一大帮,侠义为先"},
        {"id": "mingjiao", "name": "明教", "alignment": "中立偏邪", "desc": "抗元志士,被朝廷视为魔教"},
        {"id": "xiyatu", "name": "西夏一品堂", "alignment": "邪道", "desc": "李元昊建立,收罗武林败类"},
        {"id": "tang_family", "name": "唐门", "alignment": "中立", "desc": "暗器毒术,不参与江湖纷争"},
        {"id": "qianlizhuang", "name": "权力帮", "alignment": "野心", "desc": "趁青龙会瓦解崛起"},
        {"id": "kuaihuolin", "name": "快活林", "alignment": "中立", "desc": "财富与自由的追逐者"},
        {"id": "bianfushan", "name": "蝙蝠山庄", "alignment": "黑暗", "desc": "隐秘与黑暗的扩张者"}
    ],

    "martial_levels": [
        {"id": "zhongxia", "name": "三流", "desc": "江湖普通武者"},
        {"id": "eryu", "name": "二流", "desc": "小有名气的江湖客"},
        {"id": "yiliu", "name": "一流", "desc": "门派高手或一方豪杰"},
        {"id": "jiaxia", "name": "绝顶", "desc": "天下闻名的高手"},
        {"id": "tianxia", "name": "天下第一", "desc": "独步武林,难求一败"}
    ],

    "neigong_system": [
        {"level": 1, "name": "入门", "desc": "初步掌握内息运转"},
        {"level": 2, "name": "小成", "desc": "内力量产增加"},
        {"level": 3, "name": "大成", "desc": "内力收发由心"},
        {"level": 4, "name": "化境", "desc": "内力与天地合一"},
        {"level": 5, "name": "宗师", "desc": "开宗立派,自创武学"}
    ],

    "common_skills": [
        {"id": "horse", "name": "骑术", "desc": "骑乘马匹"},
        {"id": "swim", "name": "游泳", "desc": "水中行动"},
        {"id": "climb", "name": "攀爬", "desc": "翻墙越壁"},
        {"id": "identify", "name": "鉴定", "desc": "识别物品价值"},
        {"id": "poison", "name": "用毒", "desc": "毒药配制与应用"},
        {"id": "disguise", "name": "伪装", "desc": "易容改装"},
        {"id": "escape", "name": "脱逃", "desc": "挣脱束缚"},
        {"id": "trade", "name": "议价", "desc": "买卖交易"}
    ],

    "rumors": [
        "听说华山之巅有人见过独孤求败的剑冢",
        "天山有活死人墓,里面藏着古墓派绝学",
        "逍遥派掌门虚竹子据说还活着,已有数百年高龄",
        "昆仑山有光明顶,明教总坛所在",
        "大理有皇宫,段氏一阳指独步天下",
        "桃花岛上黄药师精通奇门遁甲",
        "终南山活死人墓与全真教有旧怨"
    ]
}


# ============================================
# 天道武侠世界 - 侠客行MUD (经典MUD武侠)
# ============================================
XIAKEXING_MUD = {
    "name": "侠客行MUD - 文字江湖",
    "chinese_name": "侠客行",
    "system_type": "wuxia_mud",
    "overview": "经典MUD风格的武侠世界,玩家通过文字命令探索江湖、修炼武功、加入门派、闯荡武林。融合放置类游戏的时间积累机制。",
    "source_docs": ["基于北大侠客行、放置江湖、汉家江湖等经典MUD设计"],
    "gameplay_mode": "MUD文字冒险 + 放置修炼",

    "mud_commands": {
        "movement": ["n/s/e/w/u/d", "north/south/east/west/up/down", "go <方向>", "look", "exits"],
        "interaction": ["get/drop <物品>", "give <物品> to <人物>", "open <容器>"],
        "combat": ["fight <敌人>", "kill <敌人>", "wield <武器>", "wear <防具>"],
        "character": ["score", "inventory/i", "hp", "neili", "exp", "skills", "practice", "exercise"],
        "social": ["say <话>", "tell <人物> <话>", "shout <话>", "follow <人物>"],
        "sect": ["join <门派>", "tasks", "quest <任务>"],
        "other": ["quit", "save", "help", "who"]
    },

    "mud_attributes": [
        {"id": "str", "name": "膂力", "desc": "攻击力和负载能力"},
        {"id": "int", "name": "悟性", "desc": "学习武功速度和技能威力"},
        {"id": "con", "name": "根骨", "desc": "气血上限和修炼效率"},
        {"id": "dex", "name": "身法", "desc": "防御力和出手速度"},
        {"id": "kar", "name": "福缘", "desc": "触发特殊事件的概率"}
    ],

    "combat_attributes": [
        {"id": "qi", "name": "气血", "desc": "生命值,降为0则昏迷"},
        {"id": "jing", "name": "精力", "desc": "使用技能和特殊能力的消耗"},
        {"id": "neili", "name": "内力", "desc": "施展内功和高级武功的消耗"},
        {"id": "gongli", "name": "攻击力", "desc": "每次攻击的基础伤害"},
        {"id": "fangyu", "name": "防御力", "desc": "减免受到伤害"}
    ],

    "mud_sects": [
        {"id": "shaolin", "name": "少林寺", "location": "嵩山", "style": "刚柔并济",
         "skills": ["易筋经", "少林七十二绝技", "拈花指", "金刚不坏体"],
         "requirement": "必须是男性,无犯罪记录",
         "desc": "武学正宗,适合各种玩法,但要求严格"},
        {"id": "wudang", "name": "武当派", "location": "武当山", "style": "以柔克刚",
         "skills": ["太极拳", "太极剑", "纯阳无极功", "武当九阳功"],
         "requirement": "必须是男性,非恶人",
         "desc": "内功见长,防御强,上手较易"},
        {"id": "emei", "name": "峨眉派", "location": "峨眉山", "style": "刚柔并济",
         "skills": ["九阴真经", "峨眉剑法", "灭剑", "绝剑"],
         "requirement": "必须是女性",
         "desc": "剑法精妙,内功深厚,适合进阶玩家"},
        {"id": "gaibang", "name": "丐帮", "location": "天下各处", "style": "灵巧",
         "skills": ["降龙十八掌", "打狗棒法", "逍遥游", "擒龙手"],
         "requirement": "必须身穿破衣,无家产",
         "desc": "最容易加入的门派,任务多样"},
        {"id": "duanzhong", "name": "段氏皇族", "location": "大理", "style": "内功",
         "skills": ["一阳指", "六脉神剑", "枯荣禅功"],
         "requirement": "必须姓段,或有皇室血脉",
         "desc": "内功外功皆精,但血统限制严格"},
        {"id": "murong", "name": "慕容世家", "location": "燕子坞", "style": "灵巧",
         "skills": ["斗转星移", "慕容剑法", "参合指"],
         "requirement": "必须姓慕容",
         "desc": "以彼之道还施彼身,技巧性强"},
        {"id": "ouyang", "name": "欧阳世家", "location": "白驼山", "style": "刚猛",
         "skills": ["蛤蟆功", "灵蛇杖法", "透骨打穴"],
         "requirement": "必须姓欧阳",
         "desc": "毒术与刚猛武功并重"},
        {"id": "mingjiao", "name": "明教", "location": "光明顶", "style": "刚猛",
         "skills": ["乾坤大挪移", "圣火令"],
         "requirement": "非正道人士,需通过考验",
         "desc": "攻击犀利,但被视为魔教"},
        {"id": "guduyizhou", "name": "古墓派", "location": "活死人墓", "style": "灵巧",
         "skills": ["玉女心经", "玉女剑法", "美女拳法"],
         "requirement": "必须经过寒玉床考验",
         "desc": "轻功绝顶,但需独自修炼,孤独"},
        {"id": "tang_family", "name": "唐门", "location": "四川唐家堡", "style": "灵巧",
         "skills": ["唐门暗器", "四川唐门毒术"],
         "requirement": "必须姓唐或经唐门允许",
         "desc": "暗器毒术独步天下,但不轻易收徒"},
        {"id": "xiake", "name": "江湖散人", "location": "无", "style": "自由",
         "skills": ["自行历练或偶得秘籍"],
         "requirement": "不加入任何门派",
         "desc": "自由但成长慢,可自由探索"}
    ],

    "martial_arts_categories": [
        {"id": "quanzhang", "name": "拳掌类", "examples": ["降龙十八掌", "黯然销魂掌", "铁砂掌"]},
        {"id": "jianfa", "name": "剑术类", "examples": ["独孤九剑", "太极剑", "辟邪剑法"]},
        {"id": "andao", "name": "刀法类", "examples": ["血刀刀法", "狂风刀法", "反两仪刀法"]},
        {"id": "qimei", "name": "奇门类", "examples": ["打狗棒法", "灵蛇杖法"]},
        {"id": "neigong", "name": "内功类", "examples": ["九阴真经", "九阳神功", "易筋经"]},
        {"id": "qinggong", "name": "轻功类", "examples": ["凌波微步", "梯云纵", "神行百变"]}
    ],

    "practice_methods": [
        {"id": "practice", "name": "练习", "desc": "消耗精力,提升技能等级", "efficiency": "低"},
        {"id": "study", "name": "读书", "desc": "阅读秘籍学习,需对应悟性", "efficiency": "中"},
        {"id": "combat", "name": "实战", "desc": "战斗中磨炼,效率最高", "efficiency": "高"},
        {"id": "special", "name": "闭关", "desc": "特定地点闭关,突破瓶颈", "efficiency": "极高"}
    ],

    "idle_rewards": [
        {"id": "offline_exp", "name": "离线经验", "desc": "每分钟获得少量经验"},
        {"id": "dungeon_idle", "name": "离线修炼", "desc": "在特定地点放置获得对应属性"},
        {"id": "sect_task", "name": "离线任务", "desc": "门派任务可在离线时自动完成"}
    ],

    "map_regions": [
        {"id": "zhongyuan", "name": "中原地区", "cities": ["汴梁", "洛阳", "长安"], "level_range": "1-30"},
        {"id": "jiangnan", "name": "江南地区", "cities": ["杭州", "苏州", "扬州", "嘉兴"], "level_range": "20-50"},
        {"id": "xianjiang", "name": "西域地区", "cities": ["乌鲁木齐", "敦煌", "于阗"], "level_range": "40-70"},
        {"id": "dali", "name": "大理地区", "cities": ["大理"], "level_range": "30-60"},
        {"id": "guanwai", "name": "关外地区", "cities": ["盛京", "长白山"], "level_range": "50-80"},
        {"id": "miaojiang", "name": "苗疆地区", "cities": ["苗疆"], "level_range": "60-90"}
    ],

    "dungeons": [
        {"id": "shuishen", "name": "水神庙", "requirement": "完成特定任务", "reward": "避水珠"},
        {"id": "huashan", "name": "华山秘洞", "requirement": "华山派弟子", "reward": "独孤九剑残篇"},
        {"id": "lingshi", "name": "灵鹫宫", "requirement": "通过生死符考验", "reward": "天山六阳掌"},
        {"id": "tianlong", "name": "天龙寺", "requirement": "段氏皇族", "reward": "六脉神剑"},
        {"id": "kuihua", "name": "葵花宝典", "requirement": "无", "reward": "辟邪剑法", "danger": "极高"}
    ],

    "quest_types": [
        {"id": "story", "name": "剧情任务", "desc": "主线剧情,推动故事发展"},
        {"id": "sect", "name": "门派任务", "desc": "门派日常,获取贡献和奖励"},
        {"id": "hero", "name": "英雄任务", "desc": "特定NPC触发,奖励丰厚"},
        {"id": "daily", "name": "日常任务", "desc": "每日可完成,稳定收益"},
        {"id": "hidden", "name": "隐藏任务", "desc": "特定条件触发,奖励随机"}
    ]
}


# ============================================
# 天道适配函数
# ============================================

def adapt_jinyong_to_tiandao():
    return {
        "source_system": JINYONG_TRPG["name"],
        "world_type": "wuxia",
        "overview": JINYONG_TRPG["overview"],
        "character_options": {
            "attributes": JINYONG_TRPG["attributes"],
            "talents": JINYONG_TRPG["talents"],
            "sects": JINYONG_TRPG["sects"],
            "martial_arts": JINYONG_TRPG["martial_arts"]
        },
        "gameplay_features": [
            "回合制行动点系统(100点/回合)",
            "猜拳式战斗克制(刚猛→灵巧→内功→刚猛)",
            "门派任务+遭遇任务+公共事件",
            "死后阴间摆渡人系统",
            "门派通缉与越狱系统",
            "个人胜利目标系统"
        ],
        "combat_system": {
            "type": "rock_paper_scissors",
            "types": JINYONG_TRPG["combat_types"],
            "resolution": "同时出招→克制判定→骰子伤害→闪避检定"
        }
    }


def adapt_longcang_to_tiandao():
    return {
        "source_system": LONGCANG_WORLD["name"],
        "world_type": "wuxia",
        "overview": LONGCANG_WORLD["overview"],
        "character_options": {
            "eras": LONGCANG_WORLD["eras"],
            "factions": [LONGCANG_WORLD["green_dragon_society"]],
            "characters": LONGCANG_WORLD["key_characters"],
            "martial_arts": LONGCANG_WORLD["key_martial_arts"]
        },
        "gameplay_features": [
            "千年断代史叙事(晋唐宋元明)",
            "青龙会十二龙头组织博弈",
            "组织进化论主题",
            "无鞘刀屠龙行动",
            "傅红雪宿命悲剧线",
            "墨魂向死而生结局"
        ],
        "themes": LONGCANG_WORLD["themes"]
    }


def adapt_baixiao_to_tiandao():
    return {
        "source_system": BAIXIAOSHENG_WORLD["name"],
        "world_type": "wuxia",
        "overview": BAIXIAOSHENG_WORLD["overview"],
        "character_options": {
            "factions": BAIXIAOSHENG_WORLD["factions"],
            "martial_levels": BAIXIAOSHENG_WORLD["martial_levels"],
            "common_skills": BAIXIAOSHENG_WORLD["common_skills"]
        },
        "gameplay_features": [
            "多部武侠融合",
            "正邪阵营对立",
            "武功境界修炼体系",
            "江湖传闻探索",
            "势力争霸主线"
        ]
    }


def adapt_xiakexing_to_tiandao():
    return {
        "source_system": XIAKEXING_MUD["name"],
        "world_type": "wuxia_mud",
        "overview": XIAKEXING_MUD["overview"],
        "character_options": {
            "mud_attributes": XIAKEXING_MUD["mud_attributes"],
            "combat_attributes": XIAKEXING_MUD["combat_attributes"],
            "mud_sects": XIAKEXING_MUD["mud_sects"],
            "martial_arts_categories": XIAKEXING_MUD["martial_arts_categories"],
            "map_regions": XIAKEXING_MUD["map_regions"],
            "dungeons": XIAKEXING_MUD["dungeons"]
        },
        "gameplay_features": [
            "MUD文字命令交互(north/fight/get等)",
            "经典MUD属性系统(膂力/悟性/根骨/身法/福缘)",
            "放置修炼机制(练习/读书/实战/闭关)",
            "离线收益系统",
            "门派修炼与散人自由成长",
            "副本探索与稀有秘籍获取"
        ],
        "mud_commands": XIAKEXING_MUD["mud_commands"],
        "practice_methods": XIAKEXING_MUD["practice_methods"],
        "idle_rewards": XIAKEXING_MUD["idle_rewards"],
        "quest_types": XIAKEXING_MUD["quest_types"]
    }


# 导出
WUXIA_WORLDS = {
    "jinyong_trpg": JINYONG_TRPG,
    "longcang": LONGCANG_WORLD,
    "baixiaosheng": BAIXIAOSHENG_WORLD,
    "xiakexing_mud": XIAKEXING_MUD
}


def get_wuxia_system(system_id):
    return WUXIA_WORLDS.get(system_id)


def get_all_adapted():
    return {
        "jinyong_trpg_tiandao": adapt_jinyong_to_tiandao(),
        "longcang_tiandao": adapt_longcang_to_tiandao(),
        "baixiaosheng_tiandao": adapt_baixiao_to_tiandao(),
        "xiakexing_mud_tiandao": adapt_xiakexing_to_tiandao()
    }
