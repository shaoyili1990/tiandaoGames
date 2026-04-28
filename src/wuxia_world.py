"""
天道 TRPG - 武侠世界适配数据
基于金庸x设计理念 + 龙藏世界观 + 古龙江湖体系 + 经典桌游设计

核心原则:
1. 易上手 - 桌游第一核心价值,学习门槛接近零
2. 无离线收益 - 跑团是即时互动
3. 骰子驱动 - 所有检定基于D20/D6等标准骰子
4. 同一起跑线 - 玩家间差距由策略决定,非时间投入

整合来源:
- 金庸x.txt: 门派跑团核心规则设计
- 龙藏: 青龙会千年历史,组织进化论武侠
- 我在射雕/少年歌行: 跨次元设定参考
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
    "gameplay_mode": "派对跑团",
    "max_players": 8,
    "estimated_duration": "30-60分钟一局",
    "complexity": "入门级",  # 璀璨宝石式易上手

    "attributes": [
        {"id": "constitution", "name": "体质", "abbr": "体", "desc": "决定生命值上限", "icon": "heart"},
        {"id": "strength", "name": "力量", "abbr": "力", "desc": "决定基础攻击力", "icon": "fist"},
        {"id": "dexterity", "name": "敏捷", "abbr": "敏", "desc": "决定闪避检定成功率", "icon": "wind"}
    ],

    "talents": [
        {"id": "lucky_star", "name": "福星高照", "desc": "每回合可重投一次骰子"},
        {"id": "smooth_tongue", "name": "三寸不烂", "desc": "说服和欺骗检定+2"},
        {"id": "iron_skin", "name": "铜皮铁骨", "desc": "受到伤害-1"},
        {"id": "fast_foot", "name": "凌波微步", "desc": "闪避检定+2"},
        {"id": "sharp_eye", "name": "洞察秋毫", "desc": "发现隐藏物品和线索+2"},
        {"id": "silver_tongue", "name": "妙手仁心", "desc": "治疗和修复检定+2"},
        {"id": "money_bag", "name": "财运亨通", "desc": "任务结束后额外获得10%银两"},
        {"id": "martial_talent", "name": "武学天赋", "desc": "学习新武功时,所需经验-10%"}
    ],

    # 猜拳式战斗 - 三选一,同时出招
    "combat_types": [
        {"id": "gangkuang", "name": "刚猛", "beats": "lingqiao", "desc": "刚猛型武功,克制灵巧型", "icon": "mountain"},
        {"id": "lingqiao", "name": "灵巧", "beats": "neigong", "desc": "灵巧型武功,克制内功型", "icon": "feather"},
        {"id": "neigong", "name": "内功", "beats": "gangkuang", "desc": "内功型武功,克制刚猛型", "icon": "wave"}
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

    "martial_arts": [
        {"id": "xianglong", "name": "降龙十八掌", "type": "刚猛", "damage_bonus": 5, "special": "命中后对方下回合无法闪避", "requirement": "力量3+"},
        {"id": "yijing", "name": "易筋经", "type": "内功", "damage_bonus": 3, "special": "每场战斗开始时恢复1点生命", "requirement": "体质3+"},
        {"id": "fight_dog", "name": "打狗棒法", "type": "灵巧", "damage_bonus": 4, "special": "对丐帮成员伤害+2", "requirement": "敏捷3+"},
        {"id": "dugu", "name": "独孤九剑", "type": "灵巧", "damage_bonus": 6, "special": "必定命中,无视闪避", "requirement": "敏捷4+"},
        {"id": "lingsu", "name": "凌波微步", "type": "灵巧", "damage_bonus": 2, "special": "闪避检定+3", "requirement": "敏捷3+"},
        {"id": "ruyi", "name": "如意刀法", "type": "灵巧", "damage_bonus": 3, "special": "连击概率+20%", "requirement": "敏捷2+"},
        {"id": "jiuyin", "name": "九阴真经", "type": "内功", "damage_bonus": 5, "special": "所有检定+1", "requirement": "体质3+ 智力3+"},
        {"id": "jiuyang", "name": "九阳神功", "type": "内功", "damage_bonus": 4, "special": "抗毒+3,生命上限+2", "requirement": "体质4+"},
        {"id": "taiji", "name": "太极拳剑", "type": "内功", "damage_bonus": 3, "special": "受到伤害-2,可反弹", "requirement": "体质3+ 敏捷3+"},
        {"id": "qiankun", "name": "乾坤大挪移", "type": "内功", "damage_bonus": 5, "special": "可转移伤害给队友", "requirement": "体质3+ 智力3+"}
    ],

    "mission_types": {
        "sect_missions": {"count": 50, "desc": "门派玩家稳定的成长途径"},
        "encounter_missions": {
            "unique": {"count": 100, "desc": "只会触发一次,提供独特史诗级剧情体验"},
            "normal": {"count": 200, "desc": "可重复触发,提供稳定资源和银两获取"}
        },
        "public_events": {"count": 50, "desc": "世界级事件,强制所有玩家共同参与", "examples": ["华山论剑", "襄阳守城战", "围攻光明顶"]}
    },

    "victory_conditions": [
        "习得三门绝世武功",
        "个人财富达到500两",
        "成功营救一名死亡/被拘禁的队友",
        "成为门派掌门"
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
    "complexity": "进阶级",

    "eras": [
        {"id": "jin", "name": "东晋", "period": "永嘉之乱", "desc": "五胡乱华,墨家起源"},
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
                {"id": "shieryue", "name": "十二月堂.丑", "desc": "凛冬堂/腊月堂"}
            ]
        }
    },

    "core_concepts": [
        {"id": "pingzhang", "name": "平账", "desc": "杀人灭门都是会计行为,历史本质是资源配置"},
        {"id": "mudaoshi", "name": "磨刀石", "desc": "每一代龙头都只是提升初始之刃完成度的工具"},
        {"id": "kongwei", "name": "空位", "desc": "龙首空缺暗示权力本质是真空"}
    ],

    "key_characters": [
        {"id": "susheng", "name": "苏生", "era": "晋", "role": "墨家创始人", "desc": "极端理性与生存"},
        {"id": "jinglie", "name": "荆烈", "era": "唐", "role": "黑衣门首领", "desc": "借玄武门之变交易"},
        {"id": "duanmuchou", "name": "端木筹", "era": "宋", "role": "大龙首", "desc": "金融贸易控制国命"},
        {"id": "fangyiru", "name": "方亦儒", "era": "宋末", "role": "理想主义者", "desc": "崖山力竭而亡"},
        {"id": "baiyujing", "name": "白玉京", "era": "元", "role": "七月龙头", "desc": "设计十年杀局"},
        {"id": "wushuangdao", "name": "无鞘刀", "era": "明", "role": "初始之刃", "desc": "纯粹武道的化身"},
        {"id": "fuhongxue", "name": "傅红雪", "era": "明", "role": "复仇者", "desc": "无意识终结青龙会"}
    ],

    "themes": [
        "组织进化论 - 理想如何在历史中异化",
        "屠龙者与恶龙 - 终极辩证",
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
    "source_docs": ["我在射雕.txt", "我在少年歌行当乐子人.txt"],
    "gameplay_mode": "综合跑团",
    "complexity": "入门级",

    "factions": [
        {"id": "shaolin", "name": "少林寺", "alignment": "正道", "desc": "天下武学正宗"},
        {"id": "wudang", "name": "武当派", "alignment": "正道", "desc": "以柔克刚"},
        {"id": "emei", "name": "峨眉派", "alignment": "正道", "desc": "女子当家"},
        {"id": "gaibang", "name": "丐帮", "alignment": "正道", "desc": "天下第一大帮"},
        {"id": "mingjiao", "name": "明教", "alignment": "中立偏邪", "desc": "抗元志士"},
        {"id": "tang_family", "name": "唐门", "alignment": "中立", "desc": "暗器毒术"},
        {"id": "qianlizhuang", "name": "权力帮", "alignment": "野心", "desc": "秩序与力量的吞噬者"},
        {"id": "kuaihuolin", "name": "快活林", "alignment": "中立", "desc": "财富与自由"},
        {"id": "bianfushan", "name": "蝙蝠山庄", "alignment": "黑暗", "desc": "隐秘与黑暗"}
    ],

    "martial_levels": [
        {"id": "zhongxia", "name": "三流", "desc": "江湖普通武者"},
        {"id": "eryu", "name": "二流", "desc": "小有名气的江湖客"},
        {"id": "yiliu", "name": "一流", "desc": "门派高手或一方豪杰"},
        {"id": "jiaxia", "name": "绝顶", "desc": "天下闻名的高手"},
        {"id": "tianxia", "name": "天下第一", "desc": "独步武林"}
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
        "大理有皇宫,段氏一阳指独步天下"
    ]
}


# ============================================
# 天道武侠世界 - 侠客行 (经典桌游化武侠)
# ============================================
XIAKEXING_BOARD = {
    "name": "侠客行 - 经典桌游化武侠",
    "chinese_name": "侠客行",
    "system_type": "wuxia_board",
    "overview": "将经典武侠MUD彻底桌游化,保留江湖探索乐趣的同时实现零学习门槛。所有检定基于骰子,无离线机制,同一起跑线。",
    "source_docs": ["基于北大侠客行、放置江湖、汉家江湖等经典MUD设计"],
    "gameplay_mode": "骰子驱动的桌游跑团",
    "complexity": "入门级",  # 璀璨宝石式

    # 核心设计原则
    "design_principles": [
        "无离线收益 - 所有成长通过即时游戏获得",
        "骰子驱动 - 所有检定基于D20(技能)或D6(战斗)",
        "零学习门槛 - 核心规则3分钟上手",
        "同一起跑线 - 玩家差距由策略决定,非时间投入"
    ],

    # 玩家属性 - 5大基础属性,简洁明了
    "player_attributes": [
        {"id": "str", "name": "膂力", "abbr": "膂", "desc": "攻击力和负载,影响物理伤害"},
        {"id": "int", "name": "悟性", "abbr": "悟", "desc": "学习速度和技能威力,影响内功伤害"},
        {"id": "con", "name": "根骨", "abbr": "根", "desc": "气血上限和修炼效率,影响生命值"},
        {"id": "dex", "name": "身法", "abbr": "身", "desc": "防御力和先手,影响闪避和先攻"},
        {"id": "kar", "name": "福缘", "abbr": "福", "desc": "触发特殊事件的概率,影响奇遇"}
    ],

    # 战斗属性
    "combat_stats": [
        {"id": "max_qi", "name": "气血", "desc": "生命值,降为0则重伤退场"},
        {"id": "max_jing", "name": "精力", "desc": "使用技能消耗,不足时无法行动"},
        {"id": "max_neili", "name": "内力", "desc": "施展内功消耗,影响内功伤害"},
        {"id": "attack", "name": "攻击", "desc": "每次攻击的基础伤害"},
        {"id": "defense", "name": "防御", "desc": "减免受到的伤害"}
    ],

    # 门派体系 - 经典MUD门派,桌游化
    "sects": [
        {"id": "shaolin", "name": "少林寺", "location": "嵩山",
         "skills": ["易筋经", "少林七十二绝技"],
         "requirement": "男性,无犯罪记录",
         "desc": "武学正宗,攻守平衡"},
        {"id": "wudang", "name": "武当派", "location": "武当山",
         "skills": ["太极拳", "太极剑", "纯阳功"],
         "requirement": "男性,非恶人",
         "desc": "内功见长,防守反击"},
        {"id": "emei", "name": "峨眉派", "location": "峨眉山",
         "skills": ["九阴真经", "峨眉剑法"],
         "requirement": "女性",
         "desc": "剑法精妙,攻防兼备"},
        {"id": "gaibang", "name": "丐帮", "location": "天下",
         "skills": ["降龙十八掌", "打狗棒法"],
         "requirement": "穿破衣,无私产",
         "desc": "最容易加入,任务多样"},
        {"id": "duanzhong", "name": "段氏皇族", "location": "大理",
         "skills": ["一阳指", "六脉神剑"],
         "requirement": "必须姓段",
         "desc": "内功外功皆精,血统限制"},
        {"id": "murong", "name": "慕容世家", "location": "燕子坞",
         "skills": ["斗转星移", "慕容剑法"],
         "requirement": "必须姓慕容",
         "desc": "以彼之道还施彼身"},
        {"id": "ouyang", "name": "欧阳世家", "location": "白驼山",
         "skills": ["蛤蟆功", "灵蛇杖法"],
         "requirement": "必须姓欧阳",
         "desc": "毒术与刚猛并重"},
        {"id": "mingjiao", "name": "明教", "location": "光明顶",
         "skills": ["乾坤大挪移", "圣火令"],
         "requirement": "非正道,需考验",
         "desc": "攻击犀利,被视为魔教"},
        {"id": "guduyizhou", "name": "古墓派", "location": "活死人墓",
         "skills": ["玉女心经", "玉女剑法"],
         "requirement": "寒玉床考验",
         "desc": "轻功绝顶,独自修炼"},
        {"id": "tang_family", "name": "唐门", "location": "唐家堡",
         "skills": ["唐门暗器", "四川唐门毒术"],
         "requirement": "姓唐或经允许",
         "desc": "暗器毒术独步天下"},
        {"id": "xiake", "name": "江湖散人", "location": "无",
         "skills": ["自行历练"],
         "requirement": "不加入门派",
         "desc": "自由但成长慢"}
    ],

    # 武功分类 - 6大类别,清晰明了
    "martial_arts_categories": [
        {"id": "quanzhang", "name": "拳掌", "desc": "降龙十八掌、黯然销魂掌", "stat": "str"},
        {"id": "jianfa", "name": "剑术", "desc": "独孤九剑、太极剑", "stat": "dex"},
        {"id": "andao", "name": "刀法", "desc": "血刀刀法、辟邪剑法", "stat": "dex"},
        {"id": "qimei", "name": "奇门", "desc": "打狗棒法、灵蛇杖法", "stat": "int"},
        {"id": "neigong", "name": "内功", "desc": "九阴真经、九阳神功", "stat": "int"},
        {"id": "qinggong", "name": "轻功", "desc": "凌波微步、梯云纵", "stat": "dex"}
    ],

    # 核心检定系统 - 简化为两种D20
    "skill_checks": [
        # 战斗技能 - 攻击检定
        {"id": "attack_check", "name": "攻击检定", "dice": "D20+属性修正", "vs": "对方防御或敏捷检定"},
        # 技能技能 - 难度检定
        {"id": "skill_check", "name": "技能检定", "dice": "D20+技能等级+属性修正", "vs": "难度等级(DC)"}
    ],

    # 战斗流程 - 回合制,同时行动
    "combat_flow": [
        "1. 宣言: 所有玩家同时选择行动和目标",
        "2. 隐秘: 所有选择暂时保密",
        "3. 亮牌: 同时揭示所有选择",
        "4. 判定: D20+属性修正 vs 防御/敏捷",
        "5. 结算: 伤害和效果同时生效"
    ],

    # 难度等级(DC) - 参考璀璨宝石
    "difficulty_classes": [
        {"level": 1, "name": "简单", "dc": 8, "desc": "普通路人甲"},
        {"level": 2, "name": "普通", "dc": 12, "desc": "有武功基础的对手"},
        {"level": 3, "name": "困难", "dc": 15, "desc": "门派精英或一方豪杰"},
        {"level": 4, "name": "极难", "dc": 18, "desc": "绝顶高手"},
        {"level": 5, "name": "不可能", "dc": 22, "desc": "天下第一或神话存在"}
    ],

    # 游戏流程 - 4个阶段
    "game_phases": [
        {"id": "explore", "name": "探索阶段", "desc": "移动、收集信息、触发事件"},
        {"id": "social", "name": "社交阶段", "desc": "与NPC对话、交易、组队"},
        {"id": "combat", "name": "战斗阶段", "desc": "遭遇敌人、进入战斗"},
        {"id": "rest", "name": "休息阶段", "desc": "恢复生命、修炼武功、处理事务"}
    ],

    # 区域设计 - 6大区域
    "map_regions": [
        {"id": "zhongyuan", "name": "中原", "cities": ["汴梁", "洛阳", "长安"], "level_range": "1-30"},
        {"id": "jiangnan", "name": "江南", "cities": ["杭州", "苏州", "扬州"], "level_range": "20-50"},
        {"id": "xianjiang", "name": "西域", "cities": ["敦煌", "于阗"], "level_range": "40-70"},
        {"id": "dali", "name": "大理", "cities": ["大理"], "level_range": "30-60"},
        {"id": "guanwai", "name": "关外", "cities": ["盛京", "长白山"], "level_range": "50-80"},
        {"id": "miaojiang", "name": "苗疆", "cities": ["苗疆"], "level_range": "60-90"}
    ],

    # 副本/秘境 - 5大秘境
    "dungeons": [
        {"id": "shuishen", "name": "水神庙", "dc": 12, "reward": "避水珠"},
        {"id": "huashan", "name": "华山秘洞", "dc": 15, "reward": "独孤九剑残篇", "requirement": "华山派"},
        {"id": "lingshi", "name": "灵鹫宫", "dc": 17, "reward": "天山六阳掌"},
        {"id": "tianlong", "name": "天龙寺", "dc": 18, "reward": "六脉神剑", "requirement": "段氏"},
        {"id": "kuihua", "name": "葵花宝典", "dc": 20, "reward": "辟邪剑法", "danger": "可能走火入魔"}
    ],

    # 任务类型 - 4种
    "quest_types": [
        {"id": "story", "name": "剧情任务", "desc": "主线剧情推动故事发展"},
        {"id": "sect", "name": "门派任务", "desc": "门派日常获取贡献和奖励"},
        {"id": "hero", "name": "英雄任务", "desc": "特定NPC触发奖励丰厚"},
        {"id": "daily", "name": "日常任务", "desc": "每日可完成稳定收益"}
    ]
}


# ============================================
# 天道适配函数
# ============================================

def adapt_jinyong_to_tiandao():
    return {
        "source_system": JINYONG_TRPG["name"],
        "world_type": "wuxia",
        "complexity": JINYONG_TRPG["complexity"],
        "overview": JINYONG_TRPG["overview"],
        "character_options": {
            "attributes": JINYONG_TRPG["attributes"],
            "talents": JINYONG_TRPG["talents"],
            "sects": JINYONG_TRPG["sects"],
            "martial_arts": JINYONG_TRPG["martial_arts"]
        },
        "gameplay_features": [
            "回合制行动点系统(100点/回合)",
            "猜拳式战斗(刚猛→灵巧→内功→刚猛)",
            "门派任务+遭遇任务+公共事件",
            "死后阴间摆渡人系统",
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
        "complexity": LONGCANG_WORLD["complexity"],
        "overview": LONGCANG_WORLD["overview"],
        "character_options": {
            "eras": LONGCANG_WORLD["eras"],
            "factions": [LONGCANG_WORLD["green_dragon_society"]],
            "characters": LONGCANG_WORLD["key_characters"]
        },
        "gameplay_features": [
            "千年断代史叙事(晋唐宋元明)",
            "青龙会十二龙头组织博弈",
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
        "complexity": BAIXIAOSHENG_WORLD["complexity"],
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
            "江湖传闻探索"
        ]
    }


def adapt_xiakexing_to_tiandao():
    return {
        "source_system": XIAKEXING_BOARD["name"],
        "world_type": "wuxia_board",
        "complexity": XIAKEXING_BOARD["complexity"],
        "overview": XIAKEXING_BOARD["overview"],
        "character_options": {
            "attributes": XIAKEXING_BOARD["player_attributes"],
            "combat_stats": XIAKEXING_BOARD["combat_stats"],
            "sects": XIAKEXING_BOARD["sects"],
            "martial_arts_categories": XIAKEXING_BOARD["martial_arts_categories"],
            "map_regions": XIAKEXING_BOARD["map_regions"],
            "dungeons": XIAKEXING_BOARD["dungeons"]
        },
        "gameplay_features": [
            "无离线收益 - 所有成长通过即时游戏",
            "D20骰子检定 - 技能和攻击",
            "5大基础属性 - 膂力/悟性/根骨/身法/福缘",
            "同时行动回合制 - 战斗更紧张刺激",
            "难度等级系统 - DC8到DC22",
            "4阶段游戏流程 - 探索/社交/战斗/休息"
        ],
        "design_principles": XIAKEXING_BOARD["design_principles"],
        "combat_flow": XIAKEXING_BOARD["combat_flow"],
        "difficulty_classes": XIAKEXING_BOARD["difficulty_classes"],
        "game_phases": XIAKEXING_BOARD["game_phases"],
        "quest_types": XIAKEXING_BOARD["quest_types"]
    }


# 导出
WUXIA_WORLDS = {
    "jinyong_trpg": JINYONG_TRPG,
    "longcang": LONGCANG_WORLD,
    "baixiaosheng": BAIXIAOSHENG_WORLD,
    "xiakexing_board": XIAKEXING_BOARD
}


def get_wuxia_system(system_id):
    return WUXIA_WORLDS.get(system_id)


def get_all_adapted():
    return {
        "jinyong_trpg_tiandao": adapt_jinyong_to_tiandao(),
        "longcang_tiandao": adapt_longcang_to_tiandao(),
        "baixiaosheng_tiandao": adapt_baixiao_to_tiandao(),
        "xiakexing_tiandao": adapt_xiakexing_to_tiandao()
    }
