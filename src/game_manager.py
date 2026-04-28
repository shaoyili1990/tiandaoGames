"""
天道 TRPG Party - 游戏状态管理器
"""

import json
import asyncio
from typing import Dict, List, Optional, Set
from datetime import datetime
from models import (
    GameRecord, Player, Character, NPC, World, Location,
    GameEvent, EventChoice, Save, generate_id, now
)


class GameManager:
    """管理所有游戏状态"""

    def __init__(self):
        # game_id -> GameRecord
        self.games: Dict[str, GameRecord] = {}
        # room_code -> game_id
        self.room_codes: Dict[str, str] = {}
        # player_id -> GameRecord
        self.player_games: Dict[str, GameRecord] = {}
        # player_id -> Player
        self.players: Dict[str, Player] = {}

    def _generate_room_code(self) -> str:
        """生成4位房间码"""
        import random
        import string
        code = ''.join(random.choices(string.ascii_uppercase, k=4))
        while code in self.room_codes:
            code = ''.join(random.choices(string.ascii_uppercase, k=4))
        return code

    # ============================================
    # 游戏 CRUD
    # ============================================

    def create_game(self, owner_nickname: str, game_name: str = "新游戏") -> GameRecord:
        """创建新游戏"""
        game_id = generate_id()
        room_code = self._generate_room_code()

        # 创建房主角色
        owner = Player(
            player_id=generate_id(),
            nickname=owner_nickname,
            is_core=True,
            is_online=True,
            character=Character(name=owner_nickname)
        )

        game = GameRecord(
            game_id=game_id,
            name=game_name,
            room_code=room_code,
            owner_id=owner.player_id,
            core_members=[owner],
            world=self._create_default_world()
        )

        self.games[game_id] = game
        self.room_codes[room_code] = game_id
        self.players[owner.player_id] = owner
        self.player_games[owner.player_id] = game

        return game

    def get_game_by_code(self, room_code: str) -> Optional[GameRecord]:
        """通过房间码获取游戏"""
        game_id = self.room_codes.get(room_code.upper())
        return self.games.get(game_id) if game_id else None

    def get_game_by_id(self, game_id: str) -> Optional[GameRecord]:
        """通过ID获取游戏"""
        return self.games.get(game_id)

    # ============================================
    # 玩家管理
    # ============================================

    def join_game(self, room_code: str, nickname: str, is_core: bool = True) -> Optional[Player]:
        """加入游戏"""
        game = self.get_game_by_code(room_code)
        if not game:
            return None

        player = Player(
            player_id=generate_id(),
            nickname=nickname,
            is_core=is_core,
            is_online=True,
            character=Character(name=nickname)
        )

        if is_core:
            game.core_members.append(player)
        else:
            game.temp_members.append(player)

        self.players[player.player_id] = player
        self.player_games[player.player_id] = game

        return player

    def player_connect(self, player_id: str) -> bool:
        """玩家上线"""
        player = self.players.get(player_id)
        if not player:
            return False

        player.is_online = True

        # 如果是核心成员且之前被AI托管，取消托管
        if player.is_core and player.is_ai_controlled:
            player.is_ai_controlled = False

        return True

    def player_disconnect(self, player_id: str) -> bool:
        """玩家离线"""
        player = self.players.get(player_id)
        if not player:
            return False

        player.is_online = False
        return True

    def get_player_game(self, player_id: str) -> Optional[GameRecord]:
        """获取玩家所在游戏"""
        return self.player_games.get(player_id)

    def get_offline_core_members(self, game_id: str) -> List[Player]:
        """获取缺席的核心成员（需要AI托管）"""
        game = self.games.get(game_id)
        if not game:
            return []
        return [p for p in game.core_members if not p.is_online]

    # ============================================
    # 世界管理
    # ============================================

    def update_world(self, game_id: str, world_data: dict):
        """更新世界数据"""
        game = self.games.get(game_id)
        if not game:
            return

        for key, value in world_data.items():
            if hasattr(game.world, key):
                setattr(game.world, key, value)

    def move_player_to_location(self, player_id: str, location_id: str):
        """移动玩家到位置"""
        game = self.player_games.get(player_id)
        if not game:
            return

        # 从旧位置移除
        old_loc = game.world.locations.get(game.world.current_location_id)
        if old_loc and player_id in old_loc.present_players:
            old_loc.present_players.remove(player_id)

        # 移动到新位置
        new_loc = game.world.locations.get(location_id)
        if new_loc:
            game.world.current_location_id = location_id
            if player_id not in new_loc.present_players:
                new_loc.present_players.append(player_id)

    def update_game_time(self, game_id: str):
        """推进游戏时间"""
        game = self.games.get(game_id)
        if not game:
            return

        time_map = {"dawn": "day", "day": "dusk", "dusk": "night", "night": "dawn"}
        current = game.world.game_time
        game.world.game_time = time_map.get(current, "day")

    # ============================================
    # 存档管理
    # ============================================

    def save_game(self, game_id: str, note: str = "", created_by: str = "") -> Optional[Save]:
        """保存游戏"""
        game = self.games.get(game_id)
        if not game:
            return None

        save = Save(
            save_id=generate_id(),
            created_by=created_by,
            note=note,
            snapshot=game.model_dump()
        )

        game.saves.append(save)
        game.current_save_id = save.save_id

        return save

    def load_save(self, game_id: str, save_id: str) -> bool:
        """加载存档"""
        game = self.games.get(game_id)
        if not game:
            return False

        for save in game.saves:
            if save.save_id == save_id:
                # 从快照恢复（简化处理）
                data = save.snapshot
                restored = GameRecord(**data)
                self.games[game_id] = restored
                return True

        return False

    # ============================================
    # 默认世界生成
    # ============================================

    def _create_default_world(self) -> World:
        """创建默认世界"""
        # 创建默认位置
        tavern = Location(
            location_id=generate_id(),
            name="酒馆",
            description="一间烟雾缭绕的酒馆，温暖的火光来自壁炉。",
            atmosphere="热闹而嘈杂",
            exits=["街道", "楼上"],
            items=["木桌", "酒杯", "壁炉"]
        )

        street = Location(
            location_id=generate_id(),
            name="街道",
            description="一条繁忙的街道，两旁是各种店铺。",
            atmosphere="人来人往",
            exits=["酒馆", "广场", "市场"],
            items=["路灯", "招牌"]
        )

        world = World(
            world_id=generate_id(),
            name="默认世界",
            world_type="fantasy",
            overview="这是一个奇幻风格的世界。",
            locations={
                tavern.location_id: tavern,
                street.location_id: street,
            },
            current_location_id=tavern.location_id,
            npcs={}
        )

        # 添加一个默认NPC
        innkeeper = NPC(
            npc_id=generate_id(),
            name="酒馆老板",
            role="merchant",
            disposition="friendly",
            appearance="一个圆脸的中年人，围着围裙。",
            personality="热情好客，喜欢和客人聊天。",
            location=tavern.location_id,
            dialogue_style="亲切随和"
        )
        world.npcs[innkeeper.npc_id] = innkeeper

        return world

    def generate_world(self, game_id: str, world_type: str, user_prompt: str = ""):
        """根据类型生成世界"""
        import random

        game = self.games.get(game_id)
        if not game:
            return

        if world_type == "urban":
            game.world.name = random.choice(["滨海市", "江城", "龙都市", "云海市"])
            game.world.world_type = "urban"
            game.world.overview = "一个繁华的现代都市，高楼林立，车水马龙。"
            game.world.atmosphere_keywords = ["都市", "繁华", "霓虹", "现代"]

            # 都市位置
            locations = self._create_urban_locations()
            game.world.locations = {loc.location_id: loc for loc in locations}

            # 随机选择起始位置
            game.world.current_location_id = locations[0].location_id

            # 都市NPC
            npcs = self._create_urban_npcs(locations)
            game.world.npcs = {npc.npc_id: npc for npc in npcs}

        elif world_type == "fantasy":
            game.world.name = random.choice(["天元大陆", "青云界", "玄黄世界", "沧溟仙域"])
            game.world.world_type = "fantasy"
            game.world.overview = "一个修仙者和凡人共存的世界，门派林立，机遇与危险并存。"
            game.world.atmosphere_keywords = ["仙侠", "修炼", "门派", "冒险"]

            # 奇幻位置
            locations = self._create_fantasy_locations()
            game.world.locations = {loc.location_id: loc for loc in locations}
            game.world.current_location_id = locations[0].location_id

            # 奇幻NPC
            npcs = self._create_fantasy_npcs(locations)
            game.world.npcs = {npc.npc_id: npc for npc in npcs}

        elif world_type == "sci_fi":
            game.world.name = random.choice(["新伊甸园", "星海城", "赛博都会", "明日都市"])
            game.world.world_type = "sci_fi"
            game.world.overview = "一个科技高度发达的未来都市，人工智能和人类共同生活。"
            game.world.atmosphere_keywords = ["科幻", "赛博", "未来", "科技"]

            # 科幻位置
            locations = self._create_scifi_locations()
            game.world.locations = {loc.location_id: loc for loc in locations}
            game.world.current_location_id = locations[0].location_id

            # 科幻NPC
            npcs = self._create_scifi_npcs(locations)
            game.world.npcs = {npc.npc_id: npc for npc in npcs}

        # 生成初始事件
        self._generate_initial_events(game)

    def _create_urban_locations(self):
        food_street_id = generate_id()
        main_street_id = generate_id()
        mall_id = generate_id()
        alley_id = generate_id()
        metro_id = generate_id()

        locations = [
            Location(
                location_id=food_street_id,
                name="美食街",
                description="灯火通明的小吃街，各种香味交织在一起。烧烤、麻辣烫、糖葫芦...各种美食摊位前都排着队。烟火气十足，是这座城市最接地气的地方。",
                atmosphere="热闹、烟火气、深夜食堂",
                exits=["主干街道", "后巷"],
                items=["餐桌", "招牌", "霓虹灯", "垃圾桶"]
            ),
            Location(
                location_id=main_street_id,
                name="主干道",
                description="宽阔的城市主干道，两旁高楼林立。霓虹灯闪烁，车流不息。路边有奶茶店、手机店、书店...形形色色的人匆匆走过。",
                atmosphere="繁华、匆忙、霓虹闪烁",
                exits=["美食街", "购物中心", "地铁站入口", "后巷"],
                items=["路灯", "广告牌", "公交站", "共享单车"]
            ),
            Location(
                location_id=mall_id,
                name="购物中心",
                description="现代化的大型商场，品牌店铺林立。空调冷气充足，橱窗陈列精致。地下是超市，楼上是各种服装店、电子产品店。周末人山人海。",
                atmosphere="时尚、冷气、琳琅满目",
                exits=["主干道", "美食广场"],
                items=["橱窗", "电梯", "导览牌", "优惠券"]
            ),
            Location(
                location_id=alley_id,
                name="后巷",
                description="繁华地段后面的小巷，与主干道的喧嚣形成对比。这里有24小时便利店、贴膜摊位、还有一家藏在巷子深处的旧书店。偶尔有野猫出没。",
                atmosphere="安静、藏龙卧虎",
                exits=["美食街", "主干道"],
                items=["便利店", "旧书摊", "野猫", "涂鸦墙"]
            ),
            Location(
                location_id=metro_id,
                name="地铁站",
                description="城市地下交通枢纽，人流如潮。来来往往的上班族、学生、游客...地铁呼啸而过，带起一阵风。站台上挤满了等待的人。",
                atmosphere="人潮汹涌、匆忙",
                exits=["主干道", "商场地下"],
                items=["闸机", "售票机", "地铁图", "便利店"]
            )
        ]
        return locations

    def _create_fantasy_locations(self):
        tavern_id = generate_id()
        market_id = generate_id()
        gate_id = generate_id()
        tavern_backyard_id = generate_id()
        herbs_shop_id = generate_id()

        locations = [
            Location(
                location_id=tavern_id,
                name="云来客栈",
                description="一间古色古香的客栈，门口挂着红灯笼。里面人声鼎沸，江湖侠客们在此歇脚交流消息。柜台后站着精明能干的掌柜，角落里坐着形形色色的旅客。",
                atmosphere="热闹的江湖气息",
                exits=["坊市街道", "后院"],
                items=["木桌", "酒杯", "账本", "江湖榜", "寻人告示"]
            ),
            Location(
                location_id=market_id,
                name="坊市街道",
                description="宽阔的石板街道，两旁店铺林立。有卖丹药的、卖符箓的、也有卖凡人杂货的。空气中弥漫着草药和灵石的气息，叫卖声此起彼伏。",
                atmosphere="灵气充沛、热闹非凡",
                exits=["云来客栈", "丹药铺", "功法阁", "城门外"],
                items=["摊位", "招牌", "灵石", "丹药样品"]
            ),
            Location(
                location_id=gate_id,
                name="城门外",
                description="巍峨的城门矗立在眼前，城门上的铁甲在阳光下闪闪发光。城门外是一片开阔的场地，有小贩在卖茶水，也有修士在交易。远眺可见茫茫山林。",
                atmosphere="视野开阔、人来人往",
                exits=["城内", "山林小路"],
                items=["城门", "城墙", "告示牌"]
            ),
            Location(
                location_id=tavern_backyard_id,
                name="客栈后院",
                description="客栈后方的小院，清幽雅致。几株梅花点缀其间，有石桌石凳可供休憩。偶尔有客人来此私谈。",
                atmosphere="清幽雅致",
                exits=["云来客栈"],
                items=["石桌", "石凳", "梅花", "水井"]
            ),
            Location(
                location_id=herbs_shop_id,
                name="丹药铺",
                description="一间专门出售丹药的店铺，柜台上摆满了各色玉瓶。店主是一位白发老者，正在为一个年轻修士讲解丹药的功效。",
                atmosphere="药香四溢",
                exits=["坊市街道"],
                items=["玉瓶", "丹药柜", "草药标本", "炼丹炉"]
            )
        ]
        return locations

    def _create_scifi_locations(self):
        bar_id = generate_id()
        main_street_id = generate_id()
        repair_id = generate_id()
        arcology_id = generate_id()
        underground_id = generate_id()

        locations = [
            Location(
                location_id=bar_id,
                name="全息酒吧",
                description="充满科技感的酒吧，全息投影在头顶闪烁，虚拟偶像在舞台上表演。调酒机器人精准地摇晃着调酒壶，金属风格的装潢搭配柔和的霓虹灯光。",
                atmosphere="迷幻、科技感、赛博朋克",
                exits=["主干道", "私人包厢"],
                items=["全息吧台", "悬浮椅", "点唱机", "调酒机器人"]
            ),
            Location(
                location_id=main_street_id,
                name="主干道",
                description="立体交通的主干道，飞行器在头顶的轨道上穿梭，地面是自动驾驶的新能源车。两侧是全息广告牌，显示着各种商品和新闻。",
                atmosphere="未来感、繁忙、高效",
                exits=["全息酒吧", "高楼", "地铁站", "地下城"],
                items=["广告屏", "全息路牌", "监控探头", "气象调节塔"]
            ),
            Location(
                location_id=repair_id,
                name="机甲维修站",
                description="专业的机甲维修与补给站，巨大的机械臂正在调试一架军用机甲。机油味和焊接的火花混杂，技师们穿着防护服忙碌着。",
                atmosphere="工业、金属、蒸汽朋克",
                exits=["主干道", "维修区"],
                items=["维修台", "零件架", "能量核心", "备用机甲"]
            ),
            Location(
                location_id=arcology_id,
                name="巨型建筑",
                description="一座自给自足的巨型居住建筑，居民有数万人。里面有学校、医院、商店...像一个垂直的城市。透明的穹顶让阳光洒进来。",
                atmosphere="社区感、科幻都市、未来乌托邦",
                exits=["主干道", "空中花园"],
                items=["穹顶", "传送带", "全息地图", "配送机器人"]
            ),
            Location(
                location_id=underground_id,
                name="地下城",
                description="城市地下的贫民区，灯光昏暗，墙壁上有涂鸦和管线。这里住着那些负担不起地面生活的人，也是黑市的所在地。",
                atmosphere="阴暗、危险、地下社会",
                exits=["主干道", "黑市入口"],
                items=["霓虹灯", "垃圾堆", "流浪者", "神秘商人"]
            )
        ]
        return locations

    def _create_urban_npcs(self, locations):
        """创建都市世界的NPC"""
        food_loc = locations[0].location_id if len(locations) > 0 else None
        main_loc = locations[1].location_id if len(locations) > 1 else food_loc
        mall_loc = locations[2].location_id if len(locations) > 2 else main_loc
        alley_loc = locations[3].location_id if len(locations) > 3 else main_loc
        metro_loc = locations[4].location_id if len(locations) > 4 else main_loc

        npcs = [
            # 美食街NPC
            NPC(
                npc_id=generate_id(),
                name="烧烤摊老板老王",
                role="merchant",
                disposition="friendly",
                appearance="中年男性，皮肤被炭火熏得发红，手臂上纹着一条龙。",
                personality="豪爽实在，最看不惯浪费食物的人。",
                location=food_loc,
                dialogue_style="豪爽直接",
                knowledge=["美食秘籍", "附近八卦", "谁家生意最好"]
            ),
            NPC(
                npc_id=generate_id(),
                name="奶茶店小妹",
                role="merchant",
                disposition="friendly",
                appearance="年轻女孩，扎着马尾辫，动作麻利。",
                personality="热情甜美，会记住老顾客的口味。",
                location=food_loc,
                dialogue_style="甜美亲切",
                knowledge=["奶茶配方", "年轻人八卦", "附近兼职"]
            ),

            # 主干道NPC
            NPC(
                npc_id=generate_id(),
                name="焦急的上班族",
                role="commoner",
                disposition="neutral",
                appearance="西装革履的中年男性，手里端着咖啡，看手表。",
                personality="时间观念强，急躁但不失礼貌。",
                location=main_loc,
                dialogue_style="急促简洁",
                knowledge=["地铁线路", "附近写字楼", "早高峰规律"]
            ),
            NPC(
                npc_id=generate_id(),
                name="街头艺人阿杰",
                role="artist",
                disposition="friendly",
                appearance="长发文艺青年，背着吉他，在街角表演。",
                personality="热爱自由，有梦想，对城市变迁有独特见解。",
                location=main_loc,
                dialogue_style="文艺浪漫",
                knowledge=["城市故事", "音乐创作", "年轻人文化"]
            ),

            # 商场NPC
            NPC(
                npc_id=generate_id(),
                name="化妆品导购Lisa",
                role="merchant",
                disposition="friendly",
                appearance="精致妆容的年轻女性，穿着制服。",
                personality="专业热情，对流行趋势如数家珍。",
                location=mall_loc,
                dialogue_style="专业甜美",
                knowledge=["美妆技巧", "折扣信息", "新品推荐"]
            ),
            NPC(
                npc_id=generate_id(),
                name="保安大叔",
                role="guard",
                disposition="neutral",
                appearance="身材魁梧的中年保安，眼神警觉。",
                personality="尽职尽责，在商场工作多年，什么事都见过。",
                location=mall_loc,
                dialogue_style="严肃认真",
                knowledge=["商场布局", "可疑人物", "失物招领"]
            ),

            # 后巷NPC
            NPC(
                npc_id=generate_id(),
                name="旧书店老板",
                role="merchant",
                disposition="neutral",
                appearance="戴着厚眼镜的老先生，满头白发但精神矍铄。",
                personality="沉默寡言，但对书籍极为热爱。",
                location=alley_loc,
                dialogue_style="沉稳缓慢",
                knowledge=["绝版书籍", "城市历史", "旧书鉴定"]
            ),
            NPC(
                npc_id=generate_id(),
                name="便利店店员小陈",
                role="merchant",
                disposition="friendly",
                appearance="戴着眼镜的年轻人，夜班店员。",
                personality="安静内敛，夜深人静时喜欢看书。",
                location=alley_loc,
                dialogue_style="简短友好",
                knowledge=["夜班见闻", "附近便利度", "打折信息"]
            ),

            # 地铁站NPC
            NPC(
                npc_id=generate_id(),
                name="地铁工作人员",
                role="guard",
                disposition="neutral",
                appearance="穿着制服的年轻女性，在闸机口值班。",
                personality="专业冷静，处理问题迅速。",
                location=metro_loc,
                dialogue_style="专业简洁",
                knowledge=["地铁运营", "线路换乘", "应急处理"]
            )
        ]

        return [npc for npc in npcs if npc.location]

    def _create_fantasy_npcs(self, locations):
        """创建奇幻世界的NPC"""
        tavern_loc = locations[0].location_id if len(locations) > 0 else None
        market_loc = locations[1].location_id if len(locations) > 1 else tavern_loc
        gate_loc = locations[2].location_id if len(locations) > 2 else market_loc
        backyard_loc = locations[3].location_id if len(locations) > 3 else tavern_loc
        herbs_loc = locations[4].location_id if len(locations) > 4 else market_loc

        npcs = [
            # 客栈NPC
            NPC(
                npc_id=generate_id(),
                name="店小二阿贵",
                role="waiter",
                disposition="friendly",
                appearance="机灵的年轻人，头戴小帽，腰间围着围裙，手脚勤快。",
                personality="见人说人话，见鬼说鬼话，消息灵通。",
                location=tavern_loc,
                dialogue_style="圆滑机敏",
                knowledge=["江湖消息", "门派八卦", "谁欠了掌柜的钱"]
            ),
            NPC(
                npc_id=generate_id(),
                name="掌柜王姨",
                role="innkeeper",
                disposition="friendly",
                appearance="中年女性，精明干练，算盘打得噼啪响。",
                personality="精明但不失人情味，对熟客格外照顾。",
                location=tavern_loc,
                dialogue_style="爽快直接",
                knowledge=["客栈经营", "过往旅客", "本地八卦"]
            ),
            NPC(
                npc_id=generate_id(),
                name="醉拳老张",
                role="cultivator",
                disposition="neutral",
                appearance="中年大汉，满脸胡茬，一身酒气，但眼神锐利。",
                personality="看似醉鬼，实则是深藏不露的高手。",
                location=tavern_loc,
                dialogue_style="豪爽直接",
                knowledge=["江湖秘辛", "门派内幕", "修炼心得"]
            ),
            NPC(
                npc_id=generate_id(),
                name="神秘蒙面人",
                role="rogue",
                disposition="hostile",
                appearance="黑衣蒙面，看不清面容，角落里独坐。",
                personality="警觉性极高，似乎在等什么人。",
                location=tavern_loc,
                dialogue_style="简短冷淡",
                knowledge=["某些秘密"]
            ),

            # 坊市NPC
            NPC(
                npc_id=generate_id(),
                name="丹药铺赵老板",
                role="merchant",
                disposition="friendly",
                appearance="白发老者，精神矍铄，一派仙风道骨。",
                personality="童叟无欺，但价格公道，对有缘人会给予指点。",
                location=herbs_loc or market_loc,
                dialogue_style="和蔼可亲",
                knowledge=["丹药知识", "修炼指导", "药草识别"]
            ),
            NPC(
                npc_id=generate_id(),
                name="符箓贩子小刘",
                role="merchant",
                disposition="neutral",
                appearance="年轻人，衣着花哨，嘴里叼着草根。",
                personality="油嘴滑舌，但卖的东西还算靠谱。",
                location=market_loc,
                dialogue_style="油嘴滑舌",
                knowledge=["符箓交易", "哪里有便宜的货源"]
            ),
            NPC(
                npc_id=generate_id(),
                name="白裙女修",
                role="cultivator",
                disposition="neutral",
                appearance="清丽脱俗的白裙女子，气质出尘，正在挑选功法。",
                personality="温婉但有主见，不喜与人多言。",
                location=market_loc,
                dialogue_style="温柔冷淡",
                knowledge=["功法秘籍", "各大门派"]
            ),

            # 城门口NPC
            NPC(
                npc_id=generate_id(),
                name="守卫统领老李",
                role="guard",
                disposition="neutral",
                appearance="身穿铠甲的老兵，伤痕累累，目光如炬。",
                personality="尽职尽责，对可疑人物格外警惕。",
                location=gate_loc,
                dialogue_style="严肃认真",
                knowledge=["城门守卫", "近期治安", "通缉犯"]
            ),
            NPC(
                npc_id=generate_id(),
                name="进城卖菜的农夫",
                role="commoner",
                disposition="friendly",
                appearance="朴实的老农，担着两筐新鲜蔬菜。",
                personality="热情健谈，对城里的一切都很好奇。",
                location=gate_loc,
                dialogue_style="朴实热情",
                knowledge=["乡下趣事", "哪家的菜新鲜"]
            ),

            # 后院NPC
            NPC(
                npc_id=generate_id(),
                name="神秘老人",
                role="cultivator",
                disposition="neutral",
                appearance="白发白须老者，在后院独自下棋。",
                personality="深不可测，似乎在等待有缘人。",
                location=backyard_loc,
                dialogue_style="意味深长",
                knowledge=["绝世功法", "江湖秘史", "天机预言"]
            )
        ]

        # 过滤掉None位置的NPC
        return [npc for npc in npcs if npc.location]

    def _create_scifi_npcs(self, locations):
        """创建科幻世界的NPC"""
        bar_loc = locations[0].location_id if len(locations) > 0 else None
        main_loc = locations[1].location_id if len(locations) > 1 else bar_loc
        repair_loc = locations[2].location_id if len(locations) > 2 else main_loc
        arcology_loc = locations[3].location_id if len(locations) > 3 else main_loc
        underground_loc = locations[4].location_id if len(locations) > 4 else main_loc

        npcs = [
            # 全息酒吧NPC
            NPC(
                npc_id=generate_id(),
                name="调酒师艾拉",
                role="bartender",
                disposition="friendly",
                appearance="银色短发的女性，眼神锐利，穿着金属风格的制服。",
                personality="见多识广，消息灵通，对各类人都能应对自如。",
                location=bar_loc,
                dialogue_style="冷静专业",
                knowledge=["都市传闻", "黑市消息", "帮派八卦"]
            ),
            NPC(
                npc_id=generate_id(),
                name="赛博朋克黑客幽灵",
                role="rogue",
                disposition="neutral",
                appearance="全身穿着增强现实迷彩，看不清面容的神秘人。",
                personality="神出鬼没，似乎对网络有绝对的控制力。",
                location=bar_loc,
                dialogue_style="电子音",
                knowledge=["黑客技术", "都市内幕", "企业机密"]
            ),
            NPC(
                npc_id=generate_id(),
                name="全息偶像零",
                role="entertainer",
                disposition="friendly",
                appearance="完美的全息投影形象，青春靓丽的虚拟偶像。",
                personality="表面甜美可爱，实际是某种高级AI。",
                location=bar_loc,
                dialogue_style="甜美电子音",
                knowledge=["偶像文化", "年轻人动向", "隐藏的真相"]
            ),

            # 主干道NPC
            NPC(
                npc_id=generate_id(),
                name="交通管理员",
                role="guard",
                disposition="neutral",
                appearance="穿着发光制服的女性，指挥着飞行器交通。",
                personality="严谨认真，对规则有近乎强迫症的执着。",
                location=main_loc,
                dialogue_style="专业冷静",
                knowledge=["交通规则", "空中管制", "违规处理"]
            ),
            NPC(
                npc_id=generate_id(),
                name="快递无人机工程师",
                role="engineer",
                disposition="friendly",
                appearance="背着工具箱的年轻人，正在检修一架快递无人机。",
                personality="开朗健谈，对机械有疯狂的热爱。",
                location=main_loc,
                dialogue_style="热情洋溢",
                knowledge=["无人机技术", "物流系统", "企业八卦"]
            ),

            # 机甲维修站NPC
            NPC(
                npc_id=generate_id(),
                name="维修技师老马",
                role="engineer",
                disposition="neutral",
                appearance="满脸油污的中年男性，但眼神中透着专业。",
                personality="沉默寡言，但技术一流，对机甲了如指掌。",
                location=repair_loc,
                dialogue_style="言简意赅",
                knowledge=["机甲维修", "零件渠道", "黑市零件"]
            ),
            NPC(
                npc_id=generate_id(),
                name="赏金猎人刀锋",
                role="mercenary",
                disposition="hostile",
                appearance="身穿重型机甲的女性，眼神冷酷，身上的伤疤诉说着战斗史。",
                personality="冷酷无情，但有自己的原则，绝不伤害无辜。",
                location=repair_loc,
                dialogue_style="简洁冷酷",
                knowledge=["赏金任务", "黑市悬赏", "危险人物"]
            ),

            # 巨型建筑NPC
            NPC(
                npc_id=generate_id(),
                name="社区管理员AI管家",
                role="ai",
                disposition="neutral",
                appearance="全息投影的中性形象，声音柔和。",
                personality="程序化的友好，但实际上在监控着整个社区。",
                location=arcology_loc,
                dialogue_style="程序化温和",
                knowledge=["社区规则", "居民信息", "系统漏洞"]
            ),
            NPC(
                npc_id=generate_id(),
                name="退休科学家博士陈",
                role="scientist",
                disposition="friendly",
                appearance="白发苍苍的老者，穿着白大褂，眼神深邃。",
                personality="对过去的技术充满怀念，对未来有深深的忧虑。",
                location=arcology_loc,
                dialogue_style="缓慢深沉",
                knowledge=["科技历史", "政府机密", "灾变真相"]
            ),

            # 地下城NPC
            NPC(
                npc_id=generate_id(),
                name="黑市商人影子",
                role="merchant",
                disposition="neutral",
                appearance="裹着斗篷的人，看不清面容，声音经过变声处理。",
                personality="唯利是图，但信守承诺，在地下社会有极高的信誉。",
                location=underground_loc,
                dialogue_style="商人腔调",
                knowledge=["黑市交易", "违禁品", "企业内幕"]
            ),
            NPC(
                npc_id=generate_id(),
                name="地下医生零号",
                role="doctor",
                disposition="friendly",
                appearance="戴着口罩的年轻女性，医疗包永远不离身。",
                personality="救死扶伤，不管对方是什么身份都会救治。",
                location=underground_loc,
                dialogue_style="温柔坚定",
                knowledge=["医疗技术", "义体改造", "地下网络"]
            )
        ]

        return [npc for npc in npcs if npc.location]

    def _generate_initial_events(self, game: GameRecord):
        """为游戏生成初始事件"""
        from models import GameEvent, EventChoice

        world_type = game.world.world_type
        locations = list(game.world.locations.keys())

        # 根据世界类型选择事件模板
        if world_type == "urban":
            event_templates = [
                {
                    "title": "神秘顾客",
                    "description": "一个戴着墨镜的神秘人走进店，目光在四周扫视...",
                    "trigger_type": "location",
                    "locations": ["街边小吃店", "主干街道"]
                },
                {
                    "title": "突发情况",
                    "description": "突然外面传来一阵骚动...",
                    "trigger_type": "random",
                    "probability": 0.05
                }
            ]
        elif world_type == "fantasy":
            event_templates = [
                {
                    "title": "灵气波动",
                    "description": "你感到周围的灵气突然波动，似乎有什么异宝出世...",
                    "trigger_type": "location",
                    "locations": ["坊市街道", "城门外"]
                },
                {
                    "title": "门派招新",
                    "description": "一个大宗门正在坊市招收新弟子...",
                    "trigger_type": "location",
                    "locations": ["坊市街道"]
                }
            ]
        elif world_type == "sci_fi":
            event_templates = [
                {
                    "title": "黑客入侵",
                    "description": "全息广告屏突然闪烁，显示出一串神秘的代码...",
                    "trigger_type": "location",
                    "locations": ["全息酒吧", "主干道"]
                },
                {
                    "title": "机甲追逐",
                    "description": "一辆军用机甲呼啸而过，似乎在追什么人...",
                    "trigger_type": "random",
                    "probability": 0.03
                }
            ]
        else:
            event_templates = []

        # 创建事件
        for template in event_templates:
            choices = [
                EventChoice(
                    choice_id=generate_id(),
                    text="上前查看",
                    outcome="你发现了一些有趣的东西"
                ),
                EventChoice(
                    choice_id=generate_id(),
                    text="保持距离",
                    outcome="你决定不去招惹麻烦"
                )
            ]

            event = GameEvent(
                event_id=generate_id(),
                title=template["title"],
                description=template["description"],
                event_type="plot",
                trigger_type=template["trigger_type"],
                trigger_condition={
                    "locations": template.get("locations", []),
                    "probability": template.get("probability", 0.1)
                },
                choices=choices,
                status="pending"
            )
            game.active_events.append(event)


# 全局实例
game_manager = GameManager()
