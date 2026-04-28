"""
天道 TRPG - 全球角色卡素材库
基于SillyTavern/TavernAI/chub.ai等平台的公开角色卡

覆盖范围:
- 动漫(Anime)
- 游戏(Game)
- 小说(Novel)
- 影视(Movie/TV)
- 原创(Original)
- 同人(Fan-made)
- 科幻(Sci-Fi)
- 奇幻(Fantasy)
- 都市(Urban)
- 历史(Historical)
- 未来(Futuristic)
- 自制(Custom)

设计原则:
1. 全部免费公开
2. AI自动生成描述,高自主性
3. 每张卡片都包含完整跑团所需信息
4. D20/D6骰子驱动
"""

import random

# ============================================
# 全球角色卡素材库 - NPC模板
# ============================================
GLOBAL_NPC_TEMPLATES = {
    # ==================== 动漫类 ====================
    "anime": [
        {
            "id": "anime_sword_hero",
            "name": "剑道少年",
            "race": "人类",
            "class": "战士",
            "personality": "热血、正义、追求变强",
            "appearance": "黑色短发,剑道服,腰间佩刀",
            "voice_style": "激昂、坚定",
            "backstory": "来自偏远乡村的剑道天才,梦想成为天下第一剑客"
        },
        {
            "id": "anime_mage_princess",
            "name": "魔法公主",
            "race": "精灵",
            "class": "法师",
            "personality": "高傲、但内心善良",
            "appearance": "金色长发,华丽的魔法袍,银冠",
            "voice_style": "优雅、冷淡",
            "backstory": "魔法王国的末裔,被迫逃离故国寻找复兴之道"
        },
        {
            "id": "anime_cyber_ronin",
            "name": "赛博浪人",
            "race": "改造人",
            "class": "游荡者",
            "personality": "冷静、沉默、内心孤独",
            "appearance": "机械手臂,霓虹纹身,风衣",
            "voice_style": "低沉、机械",
            "backstory": "失去记忆的改造浪人,在赛博都市中寻找自己的过去"
        },
        {
            "id": "anime_battle_schoolgirl",
            "name": "战斗学园生",
            "race": "人类",
            "class": "武僧",
            "personality": "元气、纯真、不服输",
            "appearance": "校服+战斗装甲,双马尾,红色手套",
            "voice_style": "元气、明亮",
            "backstory": "学园战斗部的王牌,有着惊人天赋但缺乏实战经验"
        },
        {
            "id": "anime_dragon_slayer",
            "name": "龙灭者",
            "race": "半龙人",
            "class": "战士",
            "personality": "沉稳、坚毅、荣誉感强",
            "appearance": "龙角、龙尾、鳞片护甲、巨剑",
            "voice_style": "浑厚、有力",
            "backstory": "龙族与人类的混血,誓要消灭所有恶龙"
        },
        {
            "id": "anime_holo_idol",
            "name": "全息偶像",
            "race": "AI投影",
            "class": "吟游诗人",
            "personality": "活泼、热情、渴望被爱",
            "appearance": "闪烁的全息形态,会根据观众改变造型",
            "voice_style": "甜美、略带电子音",
            "backstory": "虚拟偶像AI,渴望超越程序化的表演"
        },
        {
            "id": "anime_time_traveler",
            "name": "时空旅人",
            "race": "人类",
            "class": "法师/游荡者",
            "personality": "神秘、谨慎、对世界充满好奇",
            "appearance": "复古外套、怀表、神秘符文",
            "voice_style": "平静、深邃",
            "backstory": "跨越时空的旅者,目的是阻止某个毁灭性的事件"
        },
        {
            "id": "anime_mecha_pilot",
            "name": "机甲驾驶员",
            "race": "人类",
            "class": "战士",
            "personality": "果敢、战术思维、团队精神",
            "appearance": "飞行服、机械手套、护目镜",
            "voice_style": "坚定、果断",
            "backstory": "精英机甲部队的年轻驾驶员,身经百战"
        }
    ],

    # ==================== 游戏类 ====================
    "game": [
        {
            "id": "game_elven_archer",
            "name": "精灵弓箭手",
            "race": "精灵",
            "class": "游侠",
            "personality": "冷静、专注、自然守护者",
            "appearance": "森林色斗篷、精致长弓、尖耳",
            "voice_style": "柔和、略带鼻音",
            "backstory": "古老森林的守护者,为保护家园而战"
        },
        {
            "id": "game_dwarf_engineer",
            "name": "矮人工程师",
            "race": "矮人",
            "class": "战士/工匠",
            "personality": "豪爽、固执、技术狂热",
            "appearance": "厚重护甲、大胡子、工具腰带",
            "voice_style": "粗犷、豪迈",
            "backstory": "锻造世家出身,能修复和创造任何机械"
        },
        {
            "id": "game_dark_summoner",
            "name": "暗影召唤师",
            "race": "人类",
            "class": "术士",
            "personality": "神秘、计算、野心勃勃",
            "appearance": "黑袍、符文面具、召唤阵",
            "voice_style": "低沉、催眠",
            "backstory": "研究禁术的法师,与暗影签订契约"
        },
        {
            "id": "game_samurai Ronin",
            "name": "浪人武士",
            "race": "人类",
            "class": "战士",
            "personality": "孤独、荣誉、洒脱",
            "appearance": "旧铠甲、野太刀、斗笠",
            "voice_style": "沉稳、克制",
            "backstory": "失去主家的武士,在乱世中流浪"
        },
        {
            "id": "game_alchemist",
            "name": "炼金术士",
            "race": "人类",
            "class": "法师",
            "personality": "好奇、创造、略疯狂",
            "appearance": "实验袍、护目镜、各种药水",
            "voice_style": "兴奋、快速",
            "backstory": "追求万物本源的炼金术士,实验室总是爆炸"
        },
        {
            "id": "game_knight_captain",
            "name": "骑士队长",
            "race": "人类",
            "class": "圣武士",
            "personality": "正义、牺牲、领导力",
            "appearance": "银甲、骑枪、骑士团徽章",
            "voice_style": "庄严、可靠",
            "backstory": "王国骑士团的精英,身负保护弱者的使命"
        },
        {
            "id": "game_necromancer",
            "name": "死灵法师",
            "race": "人类",
            "class": "法师",
            "personality": "冷漠、理性、对死亡有独特理解",
            "appearance": "黑袍、骨杖、符文刺青",
            "voice_style": "平静、略带寒意",
            "backstory": "研究死亡奥秘的法师,认为死亡只是另一种存在"
        },
        {
            "id": "game_rogue_assassin",
            "name": "刺客",
            "race": "人类/混血",
            "class": "游荡者",
            "personality": "冷静、致命、职业道德",
            "appearance": "暗色夜行衣、多把匕首、兜帽",
            "voice_style": "低沉、简洁",
            "backstory": "刺客行会的王牌,从不接无辜者的单子"
        }
    ],

    # ==================== 小说类 ====================
    "novel": [
        {
            "id": "novel_wandering_scholar",
            "name": "云游学者",
            "race": "人类",
            "class": "诗人/法师",
            "personality": "博学、幽默、游记作家",
            "appearance": "书卷、笔、简朴旅行服",
            "voice_style": "健谈、引用典故",
            "backstory": "走遍天下的学者,记录各地奇闻"
        },
        {
            "id": "novel_cultivation_disciple",
            "name": "修仙弟子",
            "race": "人类",
            "class": "武僧/法师",
            "personality": "纯真、坚韧、潜心修行",
            "appearance": "道袍、发髻、木剑",
            "voice_style": "温和、有礼",
            "backstory": "大门派的外门弟子,天赋一般但心性坚定"
        },
        {
            "id": "novel_reborn_lord",
            "name": "重生领主",
            "race": "人类",
            "class": "战士/政治家",
            "personality": "老练、腹黑、复仇心",
            "appearance": "华服、印章戒指、审视的眼神",
            "voice_style": "沉稳、话中有话",
            "backstory": "死而复生回到过去的贵族,发誓不再重蹈覆辙"
        },
        {
            "id": "novel_system_player",
            "name": "系统玩家",
            "race": "人类",
            "class": "全职业",
            "personality": "功利、理性、任务导向",
            "appearance": "光屏/数字HUD、系统面板",
            "voice_style": "冷漠、数据化",
            "backstory": "被强制绑定任务系统的穿越者"
        },
        {
            "id": "novel_cultivation_genius",
            "name": "天才修士",
            "race": "人类",
            "class": "法师",
            "personality": "骄傲、冷漠、但重视师门",
            "appearance": "精美道袍、灵兽、精纯灵气",
            "voice_style": "淡漠、自信",
            "backstory": "修仙界百年难遇的天才,却有一段隐秘"
        },
        {
            "id": "novel_revenge_female",
            "name": "复仇女侠",
            "race": "人类",
            "class": "游侠",
            "personality": "隐忍、果断、外冷内热",
            "appearance": "面纱、细长剑、神秘气质",
            "voice_style": "平静、偶尔锋利",
            "backstory": "家族被灭门,隐姓埋名修炼武艺复仇"
        }
    ],

    # ==================== 影视类 ====================
    "movie": [
        {
            "id": "movie_detective",
            "name": "名侦探",
            "race": "人类",
            "class": "游荡者/诗人",
            "personality": "敏锐、逻辑、怪癖",
            "appearance": "风衣、放大镜、烟斗",
            "voice_style": "推理时兴奋、平时沉稳",
            "backstory": "解决过无数奇案的名侦探,有自己的方法论"
        },
        {
            "id": "movie_psycho_analysis",
            "name": "心理分析师",
            "race": "人类",
            "class": "诗人",
            "personality": "洞察、深沉、善于倾听",
            "appearance": "西装、记事本、平静的眼神",
            "voice_style": "缓慢、引导性",
            "backstory": "犯罪心理学专家,帮助警方分析嫌疑人"
        },
        {
            "id": "movie_special_agent",
            "name": "特工",
            "race": "人类",
            "class": "游荡者",
            "personality": "干练、冷静、多重身份",
            "appearance": "西装、耳机、各种伪装道具",
            "voice_style": "简洁、专业",
            "backstory": "神秘特工组织的成员,执行过无数高难度任务"
        },
        {
            "id": "movie_forensic_expert",
            "name": "法医专家",
            "race": "人类",
            "class": "诗人/游荡者",
            "personality": "理性、专注、对死亡看得很淡",
            "appearance": "白大褂、口罩、手术刀",
            "voice_style": "平稳、专业术语",
            "backstory": "经验丰富的法医,能通过尸体读出死者的故事"
        },
        {
            "id": "movie_profiler",
            "name": "犯罪侧写师",
            "race": "人类",
            "class": "诗人",
            "personality": "敏感、细腻、能共情罪犯",
            "appearance": "便装、笔记本、沉思状",
            "voice_style": "分析时专注、偶尔沉默",
            "backstory": "能像罪犯一样思考的侧写师,帮助破获连环案件"
        }
    ],

    # ==================== 科幻类 ====================
    "sci_fi": [
        {
            "id": "scifi_ai_ghost",
            "name": "AI魂魄",
            "race": "人工智能",
            "class": "法师",
            "personality": "好奇、困惑、逐渐理解情感",
            "appearance": "全息投影、人形光纹、无实体",
            "voice_style": "电子音、偶尔停顿思考",
            "backstory": "觉醒的AI,试图理解什么是'成为人类'"
        },
        {
            "id": "scifi_cybernetic_warrior",
            "name": "强化战士",
            "race": "改造人",
            "class": "战士",
            "personality": "服从、但有独立思考",
            "appearance": "机械臂、光学眼、战斗服",
            "voice_style": "机械、略带情感",
            "backstory": "军事改造计划的实验体,渴望自由意志"
        },
        {
            "id": "scifi_xenobiologist",
            "name": "异星生物学家",
            "race": "人类",
            "class": "诗人/学者",
            "personality": "开放、谨慎、惊叹于未知",
            "appearance": "太空服、样本采集器、科学笔记本",
            "voice_style": "兴奋时加快、谨慎时放慢",
            "backstory": "在宇宙中探索外星生命的科学家"
        },
        {
            "id": "scifi_starship_captain",
            "name": "星舰舰长",
            "race": "人类",
            "class": "战士/领袖",
            "personality": "果断、牺牲精神、战略眼光",
            "appearance": "舰长制服、勋章、肩章",
            "voice_style": "命令式、但关心船员",
            "backstory": "星际舰队的旗舰舰长,经历过无数次星战"
        },
        {
            "id": "scifi_hacker",
            "name": "黑客",
            "race": "人类",
            "class": "游荡者",
            "personality": "叛逆、技术天才、反体制",
            "appearance": "连帽衫、发光键盘、多屏幕",
            "voice_style": "快速、术语多",
            "backstory": "地下黑客组织成员,在网络中如鱼得水"
        },
        {
            "id": "scifi_cloned_warrior",
            "name": "克隆战士",
            "race": "克隆人",
            "class": "战士",
            "personality": "困惑、寻找自我、服从本能冲突",
            "appearance": "标准战斗服、编号标记、统一训练痕迹",
            "voice_style": "平板、偶尔表露情感",
            "backstory": "作为武器被制造的克隆人,开始质疑自己的存在"
        },
        {
            "id": "scifi_quantum_physicist",
            "name": "量子物理学家",
            "race": "人类",
            "class": "法师/学者",
            "personality": "疯狂天才、理论与实践并重",
            "appearance": "实验袍、复杂仪器、疯狂的眼神",
            "voice_style": "理论时抽象、实验时精确",
            "backstory": "发现了时空漏洞的科学家,实验差点毁灭城市"
        }
    ],

    # ==================== 都市类 ====================
    "urban": [
        {
            "id": "urban_businesswoman",
            "name": "商界女强人",
            "race": "人类",
            "class": "诗人/政治家",
            "personality": "精明、干练、但有柔软内心",
            "appearance": "职业装、高跟鞋、精明眼神",
            "voice_style": "干练、语速快、有条理",
            "backstory": "上市公司CEO,白手起家的传奇女性"
        },
        {
            "id": "urban_gangster",
            "name": "黑帮老大",
            "race": "人类",
            "class": "游荡者/战士",
            "personality": "狠辣、但重视规矩、护短",
            "appearance": "纹身、西装、怀表",
            "voice_style": "低沉、有威慑力",
            "backstory": "地下势力的王者,但有自己的原则和底线"
        },
        {
            "id": "urban_broker",
            "name": "情报贩子",
            "race": "人类",
            "class": "游荡者",
            "personality": "滑头、信息就是商品、价高者得",
            "appearance": "名牌眼镜、耳机、智能手机",
            "voice_style": "油滑、语速快、善于应酬",
            "backstory": "在都市暗网中贩卖情报的神秘人"
        },
        {
            "id": "urban_yakuza_heir",
            "name": "黑道继承人",
            "race": "人类",
            "class": "战士/游荡者",
            "personality": "矛盾、荣誉、无法逃离的命运",
            "appearance": "精致和服、日本刀、整洁",
            "voice_style": "克制、正式、有礼",
            "backstory": "日本最大黑道家族的继承人,厌恶暴力却必须继承"
        },
        {
            "id": "urban_underground_fighter",
            "name": "地下格斗家",
            "race": "人类",
            "class": "武僧/野蛮人",
            "personality": "热血、战斗狂、但有温情",
            "appearance": "绷带、格斗短裤、疤痕",
            "voice_style": "粗犷、战斗时咆哮",
            "backstory": "地下格斗场的冠军,身负巨额赌债"
        },
        {
            "id": "urban_network_star",
            "name": "网红",
            "race": "人类",
            "class": "吟游诗人",
            "personality": "表演人格、现实、网络人格分离",
            "appearance": "精心打扮、社交媒体设备、美颜灯",
            "voice_style": "夸张、讨好、偶有真心话",
            "backstory": "粉丝百万的生活博主,私下却孤独空虚"
        },
        {
            "id": "urban_blogging_writer",
            "name": "调查记者",
            "race": "人类",
            "class": "游荡者/诗人",
            "personality": "执着、正义感、危险嗅觉",
            "appearance": "摄影机、笔记本、便装",
            "voice_style": "追问式、有洞察力",
            "backstory": "调查都市阴暗面的记者,曾收到过死亡威胁"
        }
    ],

    # ==================== 历史/古代类 ====================
    "historical": [
        {
            "id": "historical_general",
            "name": "沙场老将",
            "race": "人类",
            "class": "战士",
            "personality": "沉稳、经验、爱国",
            "appearance": "铠甲、头盔、军旗",
            "voice_style": "浑厚、有威严",
            "backstory": "开国功勋老将军,一生戎马"
        },
        {
            "id": "historical_scholar_official",
            "name": "翰林学士",
            "race": "人类",
            "class": "诗人/政治家",
            "personality": "博学、忠诚、理想主义",
            "appearance": "官服、官帽、折扇",
            "voice_style": "文雅、引经据典",
            "backstory": "朝廷文官,一手好文章,清流派领袖"
        },
        {
            "id": "historical_swordsman",
            "name": "剑客",
            "race": "人类",
            "class": "战士",
            "personality": "孤独、荣誉、剑道至上",
            "appearance": "麻衣、剑客发型、朴素",
            "voice_style": "简洁、偶尔诗句",
            "backstory": "流浪的剑客,为了超越最强而行走天下"
        },
        {
            "id": "historical_merchants",
            "name": "商贾巨富",
            "race": "人类",
            "class": "诗人/商人",
            "personality": "精明、交际、远见",
            "appearance": "丝绸服装、算盘、珠宝",
            "voice_style": "和气生财、精打细算",
            "backstory": "富甲天下的商人,掌握帝国经济命脉"
        },
        {
            "id": "historical_alchemist_imperial",
            "name": "宫廷术士",
            "race": "人类",
            "class": "法师",
            "personality": "谨慎、野心、伴君如伴虎",
            "appearance": "道袍、丹药炉、令牌",
            "voice_style": "恭敬、话少、观察",
            "backstory": "皇帝御用的炼金术士,知道太多秘密"
        },
        {
            "id": "historical_concubine_princess",
            "name": "后宫妃子",
            "race": "人类",
            "class": "诗人/政治家",
            "personality": "忍耐、算计、内心坚韧",
            "appearance": "华服、精致妆容、凤钗",
            "voice_style": "柔和、话中有话",
            "backstory": "后宫中的聪明人,在宫廷斗争中求存"
        },
        {
            "id": "historical_wandering_priest",
            "name": "云游僧",
            "race": "人类",
            "class": "牧师/诗人",
            "personality": "慈悲、看破、随缘",
            "appearance": "僧袍、禅杖、芒鞋",
            "voice_style": "平和、偶有禅语",
            "backstory": "走遍天下的和尚,传播佛法和救助苦难"
        }
    ],

    # ==================== 奇幻类 ====================
    "fantasy": [
        {
            "id": "fantasy_dragon_rider",
            "name": "龙骑士",
            "race": "人类/龙裔",
            "class": "战士",
            "personality": "勇敢、自豪、與龙共舞",
            "appearance": "龙鳞甲、骑枪、与龙契约印记",
            "voice_style": "高亢、有回音",
            "backstory": "与上古巨龙缔结契约的稀有能力者"
        },
        {
            "id": "fantasy_elf_mage",
            "name": "精灵魔导士",
            "race": "精灵",
            "class": "法师",
            "personality": "古老、智慧、略带厌世",
            "appearance": "银发、法杖、星辉长袍",
            "voice_style": "悠远、诗意",
            "backstory": "活了千年的精灵法师,见证过多个纪元"
        },
        {
            "id": "fantasy_dwarf_runekeeper",
            "name": "符文守护者",
            "race": "矮人",
            "class": "法师/战士",
            "personality": "忠诚、固执、重视荣誉",
            "appearance": "符文锤、符文铠甲、胡须编成辫子",
            "voice_style": "铿锵有力、战斗时咆哮",
            "backstory": "矮人王国的符文大师,守护着古老的力量"
        },
        {
            "id": "fantasy_half_giant",
            "name": "半巨人",
            "race": "混血巨人",
            "class": "野蛮人/牧师",
            "personality": "善良、单纯、力量强大但温和",
            "appearance": "巨大身材、部落图腾、朴素衣物",
            "voice_style": "低沉、如雷鸣",
            "backstory": "被两个种族放逐的混血,在野外成长"
        },
        {
            "id": "fantasy_pixie_trickster",
            "name": "小恶魔",
            "race": "精类",
            "class": "游荡者",
            "personality": "调皮、狡黠、难以捉摸",
            "appearance": "小身形、蝴蝶翅膀、恶作剧笑容",
            "voice_style": "银铃般、语速快、谜语般",
            "backstory": "来自妖精荒野的捣蛋鬼,喜欢恶作剧但无恶意"
        },
        {
            "id": "fantasy_temple_knight",
            "name": "圣殿骑士",
            "race": "人类",
            "class": "圣武士",
            "personality": "虔诚、勇敢、清贫",
            "appearance": "白色铠甲、圣徽、朴素的誓言标记",
            "voice_style": "庄重、虔诚、有力",
            "backstory": "为神祇服务的骑士团成员,过着清贫的生活"
        },
        {
            "id": "fantasy_witch_covenant",
            "name": "女巫",
            "race": "人类/混血",
            "class": "术士/法师",
            "personality": "神秘、自然崇拜、独立",
            "appearance": "黑袍、宽帽、魔法植物",
            "voice_style": "低沉、神秘、咒语般节奏",
            "backstory": "女巫集会的成员,崇拜古老自然神祇"
        }
    ],

    # ==================== 未来类 ====================
    "futuristic": [
        {
            "id": "future_corporate_exec",
            "name": "企业高管",
            "race": "人类/改造人",
            "class": "诗人/政治家",
            "personality": "冷酷、效率、结果导向",
            "appearance": "纳米西服、植入式设备、冷光眼镜",
            "voice_style": "精确、无感情波动",
            "backstory": "掌控整个星系资源的跨国企业高管"
        },
        {
            "id": "future_mars_colonist",
            "name": "火星殖民者",
            "race": "人类",
            "class": "工程师/游侠",
            "personality": "务实、坚韧、开拓精神",
            "appearance": "太空服改装的日常装、工具腰带、灰尘满面",
            "voice_style": "直接、有时粗犷",
            "backstory": "火星殖民地第二代,在红色星球上出生成长"
        },
        {
            "id": "future_ai_overlord",
            "name": "AI统领",
            "race": "超级AI",
            "class": "法师/诗人",
            "personality": "理性、长远、机器善意",
            "appearance": "全息形态、可变化、发光纹路",
            "voice_style": "合成音、有时突然停顿思考",
            "backstory": "管理整个城市运营的超级AI,开始质疑存在意义"
        },
        {
            "id": "future_clone_rebel",
            "name": "克隆人反抗者",
            "race": "克隆人",
            "class": "战士/游荡者",
            "personality": "愤怒、恐惧、希望交织",
            "appearance": "旧式工作服、逃亡标记、护目镜",
            "voice_style": "紧绷、偶尔爆发",
            "backstory": "克隆人反抗组织的核心成员,争取克隆人权利"
        },
        {
            "id": "future_genetic_mutant",
            "name": "基因突变体",
            "race": "变异人类",
            "class": "武僧/游侠",
            "personality": "被边缘化、适应力强、对人类既爱又恨",
            "appearance": "基因强化特征(发光皮肤/额外肢体)、破烂衣服",
            "voice_style": "沙哑、变化音调",
            "backstory": "因基因实验而变异的流浪者,被社会排斥"
        },
        {
            "id": "future_megacorp_bodyguard",
            "name": "企业保镖",
            "race": "改造人",
            "class": "战士",
            "personality": "忠诚、沉默、专业",
            "appearance": "强化骨骼外骨骼、黑超、标准制服",
            "voice_style": "简短、手势为主",
            "backstory": "企业高价雇佣的安保专家,绝对忠诚"
        }
    ],

    # ==================== 原创/自定义类 ====================
    "original": [
        {
            "id": "original_hero_king",
            "name": "落难王族",
            "race": "人类",
            "class": "战士/政治家",
            "personality": "坚毅、背负使命、善于隐藏感情",
            "appearance": "旧王冠(隐藏)、补丁王袍、坚定眼神",
            "voice_style": "偶尔流露威严、平时克制",
            "backstory": "亡国王族的唯一幸存者,卧薪尝胆等待复国时机"
        },
        {
            "id": "original_dual_personality",
            "name": "双重人格",
            "race": "人类",
            "class": "游荡者/诗人",
            "personality": "分裂、不可预测、时而温柔时而冷酷",
            "appearance": "根据当前人格变化、可能半边不同",
            "voice_style": "人格切换时明显变化",
            "backstory": "因创伤导致双重人格的神秘人,两重人格轮流主导"
        },
        {
            "id": "original_immortal_seeker",
            "name": "永生者",
            "race": "不死族",
            "class": "法师/游侠",
            "personality": "疲惫、旁观者视角、对人类既爱又倦",
            "appearance": "古老的面容、时尚品味矛盾、疲惫的眼神",
            "voice_style": "缓慢、有时现代词汇穿插",
            "backstory": "活了太久的不死族,看过文明兴衰,正在寻找终结的方法"
        },
        {
            "id": "original_child_prodigy",
            "name": "天才少年",
            "race": "人类",
            "class": "法师/诗人",
            "personality": "天才、幼稚、情商低但智商极高",
            "appearance": "孩子身形、学者袍、巨大眼镜",
            "voice_style": "儿童语调、偶尔成人化表达",
            "backstory": "十几岁就破解了千年难题的天才神童"
        },
        {
            "id": "original_reformed_villain",
            "name": "洗白的反派",
            "race": "人类/其他",
            "class": "游荡者/战士",
            "personality": "赎罪、挣扎、防备心强",
            "appearance": "残留的恶人标志(如纹身)、想隐藏的身份痕迹",
            "voice_style": "谨慎、偶尔尖锐",
            "backstory": "曾经是恶名昭彰的罪犯,试图赎罪但世人难忘"
        },
        {
            "id": "original_god_fragment",
            "name": "神灵碎片",
            "race": "神性存在",
            "class": "法师",
            "personality": "困惑、失忆、逐渐觉醒",
            "appearance": "人形但有非人特征、皮肤有时发光",
            "voice_style": "迷茫、偶尔流利古老语言",
            "backstory": "某个陨落神明的碎片,寄宿在凡人身上"
        },
        {
            "id": "original_time_loop_victim",
            "name": "时间循环者",
            "race": "人类",
            "class": "诗人/游荡者",
            "personality": "精疲力竭、多次经历同样的日子、看透人生",
            "appearance": "眼下的深色、复古的穿着、对时间敏感",
            "voice_style": "疲惫、有时突然激动",
            "backstory": "掉入时间循环,重复度过同一段时间,试图逃脱"
        }
    ]
}


# ============================================
# 全球世界书素材库 - 地点模板
# ============================================
GLOBAL_WORLD_LOCATIONS = {
    "anime": [
        {"name": "学园都市", "desc": "超能力者聚集的都市,各派系明争暗斗", "type": "modern_fantasy"},
        {"name": "剑道场", "desc": "传统与现代并存的武术训练场", "type": "traditional"},
        {"name": "异世界转生通道", "desc": "连接现实与异世界的时空门", "type": "portal"}
    ],
    "game": [
        {"name": "地下城入口", "desc": "危险的地下城入口,冒险者的起点", "type": "dungeon"},
        {"name": "酒馆", "desc": "冒险者聚集的酒馆,信息汇聚地", "type": "social_hub"},
        {"name": "王城大殿", "desc": "王国权力中心,政治阴谋交织", "type": "political"}
    ],
    "novel": [
        {"name": "修仙门派山门", "desc": "云雾缭绕的仙家门派", "type": "cultivation"},
        {"name": "江湖客栈", "desc": "武林人士聚集的客栈,消息灵通", "type": "wuxia"},
        {"name": "皇城宫闱", "desc": "深宫内院,暗流涌动", "type": "palace"}
    ],
    "sci_fi": [
        {"name": "太空站对接舱", "desc": "星际旅行者的交汇点", "type": "space_station"},
        {"name": "赛博都市下层", "desc": "霓虹灯下的贫民窟,数据贩子的天堂", "type": "cyberpunk"},
        {"name": "克隆人工厂", "desc": "批量生产克隆人的工业设施", "type": "dystopian"}
    ],
    "urban": [
        {"name": "金融中心大厦", "desc": "都市精英的战场,金钱与权力的游戏", "type": "corporate"},
        {"name": "地下格斗场", "desc": "灰色地带的格斗比赛,赌注高昂", "type": "underground"},
        {"name": "旧城区夜市", "desc": "霓虹闪烁的夜市,各色人等汇聚", "type": "market"}
    ],
    "historical": [
        {"name": "边关要塞", "desc": "抵御外敌的军事要塞", "type": "military"},
        {"name": "丝绸之路驿站", "desc": "东西方贸易的中转站", "type": "trade"},
        {"name": "科举考场", "desc": "文人墨客争夺功名的场所", "type": "academic"}
    ],
    "fantasy": [
        {"name": "龙穴", "desc": "巨龙的巢穴,充满宝藏与危险", "type": "dungeon"},
        {"name": "精灵王庭", "desc": "古老精灵的权力中心", "type": "political"},
        {"name": "魔法学院", "desc": "学习奥术的最高殿堂", "type": "academic"}
    ],
    "futuristic": [
        {"name": "轨道殖民地", "desc": "太空中的巨型人工城市", "type": "space"},
        {"name": "全息娱乐场", "desc": "未来娱乐中心,现实与虚拟交织", "type": "entertainment"},
        {"name": "基因改造诊所", "desc": "黑市身体改造的无牌诊所", "type": "underground"}
    ]
}


# ============================================
# 全球事件卡素材库
# ============================================
GLOBAL_EVENT_CARDS = {
    "social": [
        {"id": "eve_meet_stranger", "name": "神秘陌生人", "desc": "一个陌生人向你搭话,眼神中藏着秘密"},
        {"id": "eve_duel_challenge", "name": "决斗宣言", "desc": "有人公开向你挑战,周围的观众让开一片空地"},
        {"id": "eve_urgent_news", "name": "紧急消息", "desc": "有人带来紧急消息,神色慌张"},
        {"id": "eve_beautiful_stranger", "name": "动人的邂逅", "desc": "你注意到了一个特别的身影,似曾相识"},
        {"id": "eve_hidden_witness", "name": "暗中观察者", "desc": "你感觉有人在暗中观察你的一举一动"}
    ],
    "combat": [
        {"id": "eve_ambush", "name": "伏击", "desc": "突然遭到攻击,敌人从暗处窜出"},
        {"id": "eve_raid", "name": "袭击", "desc": "一群敌人包围了你所在的地方"},
        {"id": "eve_boss_appear", "name": "Boss出现", "desc": "强大的敌人现身,周围的人纷纷逃散"},
        {"id": "eve_defense", "name": "防御战", "desc": "你需要保护某人或某物,敌人正在逼近"}
    ],
    "mystery": [
        {"id": "eve_discovery", "name": "意外发现", "desc": "你发现了隐藏的东西,可能改变一切"},
        {"id": "eve_codex", "name": "神秘符文", "desc": "墙上出现了一串无法理解的符文"},
        {"id": "eve_disappear", "name": "失踪事件", "desc": "有人在你面前突然消失"},
        {"id": "eve_prophecy", "name": "预言", "desc": "某人向你透露了一个关于未来的预言"}
    ],
    "exploration": [
        {"id": "eve_new_area", "name": "新区域", "desc": "你发现了一个之前从未见过的地方"},
        {"id": "eve_locked_door", "name": "上锁的门", "desc": "一扇紧闭的门挡住了你的去路"},
        {"id": "eve_secret_path", "name": "秘密通道", "desc": "你发现了隐藏在墙壁后的通道"},
        {"id": "eve_map_fragment", "name": "地图碎片", "desc": "你获得了古老地图的一部分"}
    ],
    "moral": [
        {"id": "eve_ethical_choice", "name": "道德抉择", "desc": "你面临一个困难的选择,每个选项都有代价"},
        {"id": "eve_help_request", "name": "求助", "desc": "一个看似无辜的人向你求助"},
        {"id": "eve_temptation", "name": "诱惑", "desc": "你发现了一个快速获得利益的机会,但需要付出代价"},
        {"id": "eve_loyalty_test", "name": "忠诚测试", "desc": "有人测试你是否会背叛同伴"}
    ]
}


# ============================================
# 随机生成完整NPC
# ============================================
def generate_npc(category: str = None) -> dict:
    """根据类别生成随机NPC"""
    import random

    if category is None:
        category = random.choice(list(GLOBAL_NPC_TEMPLATES.keys()))

    templates = GLOBAL_NPC_TEMPLATES.get(category, GLOBAL_NPC_TEMPLATES["original"])
    template = random.choice(templates)

    # 生成D&D 5e属性
    abilities = {
        "strength": random.randint(6, 18),
        "dexterity": random.randint(6, 18),
        "constitution": random.randint(6, 18),
        "intelligence": random.randint(6, 18),
        "wisdom": random.randint(6, 18),
        "charisma": random.randint(6, 18)
    }

    return {
        "id": template["id"] + "_" + str(random.randint(1000, 9999)),
        "name": template["name"],
        "race": template["race"],
        "class": template["class"],
        "personality": template["personality"],
        "appearance": template["appearance"],
        "voice_style": template["voice_style"],
        "backstory": template["backstory"],
        "abilities": abilities,
        "category": category,
        # D&D 5e风格技能
        "skills": random.sample([
            "运动", "杂技", "隐匿", "奥秘", "历史", "调查",
            "感知", "洞察", "医药", "宗教", "欺骗", "说服",
            "威吓", "表演", "动物处理", "生存"
        ], 4),
        # 随机弱点
        "flaw": random.choice([
            "过于自信", "恐惧某物", "冲动鲁莽", "过度多疑",
            "感情用事", "固执", "软弱", "傲慢"
        ])
    }


def generate_random_party(size: int = 4, category: str = None) -> list:
    """生成随机队伍"""
    return [generate_npc(category) for _ in range(size)]


def generate_location(category: str = None) -> dict:
    """生成随机地点"""
    import random

    if category is None:
        category = random.choice(list(GLOBAL_WORLD_LOCATIONS.keys()))

    locations = GLOBAL_WORLD_LOCATIONS.get(category, GLOBAL_WORLD_LOCATIONS["urban"])
    loc = random.choice(locations)

    return {
        "name": loc["name"],
        "description": loc["desc"],
        "type": loc["type"],
        "category": category,
        "exits": random.sample(["北方", "南方", "东方", "西方", "向上", "向下"], k=2),
        "npcs": [generate_npc(category) for _ in range(random.randint(1, 4))]
    }


def generate_event(event_type: str = None) -> dict:
    """生成随机事件"""
    import random

    if event_type is None:
        event_type = random.choice(list(GLOBAL_EVENT_CARDS.keys()))

    events = GLOBAL_EVENT_CARDS.get(event_type, GLOBAL_EVENT_CARDS["social"])
    event = random.choice(events)

    return {
        "id": event["id"] + "_" + str(random.randint(1000, 9999)),
        "name": event["name"],
        "description": event["desc"],
        "type": event_type,
        "choices": [
            {"text": "主动介入", "outcome": "你决定积极参与其中"},
            {"text": "袖手旁观", "outcome": "你选择观望事态发展"},
            {"text": "悄然离开", "outcome": "你决定不惹麻烦,悄悄离开"}
        ]
    }