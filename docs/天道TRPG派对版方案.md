# 天道 TRPG 派对版 - 最终技术方案

> 项目代号：Tiandao_TRPG_Party
> 服务器：Autodl 云GPU实例
> 日期：2026-04-28
> 版本：1.1

---

## 一、核心定位

### 1.1 项目愿景

```
赛博跑团 - 老天爷当DM，多位玩家异地同屏
```

**一句话说明**：
> 基于Autodl云GPU实例搭建天道TRPG服务器，实现多人异地同时在线游玩。玩家通过PWA（渐进式网页应用）接入，核心成员凑齐才能继续游戏，支持中途加人、AI托管等机制。

### 1.2 核心特性

| 特性 | 说明 |
|------|------|
| **Autodl云服务器** | 固定IP，按量计费（0.6-1.5元/小时），关机仅0.1元/天 |
| **PWA客户端** | 无需安装，浏览器直连，支持添加到桌面 |
| **账号系统** | 设备绑定 + 邮箱注册，数据可迁移 |
| **游戏记录制** | 核心成员凑齐才继续，中途可加新人 |
| **AI托管** | 缺席玩家由AI接管 |
| **天道DM** | 天道系统担任DM，驱动NPC和事件 |

### 1.3 成本估算

| 场景 | 时长 | 成本 |
|------|------|------|
| 日常派对 | 5小时/次 | ~8元 |
| 周末团 | 8小时/次 | ~12元 |
| 闲置成本 | 1天 | 0.1元（可忽略） |

**对比**：桌游店人均30-50元/小时，天道TRPG人均不到2元/小时。

---

## 二、系统架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────────┐
│                     Autodl 云GPU实例 (固定IP)                    │
│                     关机: 0.1元/天  |  运行: 0.6-1.5元/小时    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐  │
│   │                    天道 TRPG 服务器                      │  │
│   │                                                         │  │
│   │   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │  │
│   │   │  房间管理    │  │  消息路由   │  │  会话管理    │     │  │
│   │   │  RoomManager│  │  WebSocket │  │  SessionMgr  │     │  │
│   │   └─────────────┘  └─────────────┘  └─────────────┘     │  │
│   │                                                         │  │
│   │   ┌─────────────────────────────────────────────────┐  │  │
│   │   │              天道 DM 引擎                        │  │  │
│   │   │  ┌───────────┐  ┌───────────┐  ┌───────────┐   │  │  │
│   │   │  │ 事件触发  │  │ NPC心理   │  │ 世界状态  │   │  │  │
│   │   │  └───────────┘  └───────────┘  └───────────┘   │  │  │
│   │   └─────────────────────────────────────────────────┘  │  │
│   │                                                         │  │
│   │   ┌─────────────────────────────────────────────────┐  │  │
│   │   │           天道心理引擎 (tiandaosystem_max)        │  │  │
│   │   │  Y值 / MBTI / 记忆 / 动机 / 作者约束             │  │  │
│   │   └─────────────────────────────────────────────────┘  │  │
│   │                                                         │  │
│   │   ┌─────────────────────────────────────────────────┐  │  │
│   │   │              SQLite 数据库                         │  │  │
│   │   │  users.db  |  games.db  |  saves.db            │  │  │
│   │   └─────────────────────────────────────────────────┘  │  │
│   │                                                         │  │
│   └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                         固定IP:端口
                              │
    ┌─────────────────────────┼─────────────────────────┐
    │                         │                         │
    ▼                         ▼                         ▼
┌─────────┐             ┌─────────┐             ┌─────────┐
│玩家手机A│             │玩家手机B│             │玩家电脑C│
│(PWA)   │             │(PWA)   │             │(PWA)   │
└─────────┘             └─────────┘             └─────────┘
```

### 2.2 客户端选择

**最终方案：PWA（渐进式网页应用）**

| 方案 | 用户操作 | 开发成本 | 体验 |
|------|---------|---------|------|
| **纯浏览器** | 输入IP+房间码 | 低 | 一般 |
| **PWA** | 浏览器打开 → 存桌面 | 中 | **好** |
| **专用App** | 应用商店下载 | 高 | 好 |

**PWA优势**：
- 无需安装应用商店
- 有桌面图标，接近原生体验
- 支持离线缓存
- 自动更新

**用户操作流程**：
```
1. 浏览器打开 http://IP:端口
2. 弹出"添加到主屏幕"
3. 之后点图标直接进游戏
```

### 2.3 目录结构

```
tiandao-trpg-party/
├── SKILL.md
│
├── src/
│   ├── __init__.py
│   ├── server.py                 # FastAPI 主服务器
│   ├── models/                   # 数据模型
│   │   ├── user.py              # 用户模型
│   │   ├── game.py              # 游戏记录模型
│   │   ├── player.py            # 玩家模型
│   │   └── save.py              # 存档模型
│   ├── services/
│   │   ├── room_manager.py      # 房间/游戏管理
│   │   ├── auth_service.py      # 认证服务
│   │   └── ai_service.py        # AI调用服务
│   ├── dm/                      # DM引擎
│   │   ├── event_trigger.py     # 事件触发
│   │   ├── npc.py               # NPC控制
│   │   ├── world.py             # 世界管理
│   │   └── response_generator.py # DM响应生成
│   ├── engine/                  # 天道心理引擎
│   │   └── (软链接 tiandaosystem_max)
│   └── api/
│       ├── ws_handler.py        # WebSocket处理
│       └── http_routes.py       # HTTP路由
│
├── web/
│   ├── static/
│   │   ├── manifest.json        # PWA清单
│   │   ├── sw.js                # Service Worker
│   │   ├── style.css
│   │   └── client.js            # 前端逻辑
│   └── templates/
│       └── index.html            # 主页面
│
├── scripts/
│   ├── setup.sh                  # 服务器安装脚本
│   ├── start.sh                  # 启动脚本
│   └── docker/                   # Docker部署
│
├── config/
│   ├── server.yaml              # 服务器配置
│   └── prompts/                 # AI提示词
│       ├── world_gen.md
│       ├── dm_response.md
│       └── npc_gen.md
│
├── requirements.txt
├── Dockerfile
│
└── README.md
```

---

## 三、账号与数据系统

### 3.1 用户账号体系

**双轨制**：

```
设备账号 (必选)
  - 首次使用自动创建
  - 存储在 localStorage
  - 换手机 = 丢失

邮箱账号 (可选)
  - 绑定邮箱升级为正式账号
  - 永久保存，可跨设备
  - 可导入设备数据
```

**账号升级流程**：
```
新用户首次访问
    │
    ├─ 自动创建设备ID
    │    └─ localStorage.uuid
    │
    └─ 使用游戏
         │
         ├─ 可以一直用设备账号
         │
         └─ 可选绑定邮箱
              │
              └─ 验证通过后
                   ├─ 升级为正式账号
                   └─ 可导入设备数据
```

### 3.2 数据模型

```python
# 用户
class User:
    user_id: str              # UUID
    device_id: str            # 设备标识
    email: str | None         # 绑定邮箱
    nickname: str             # 默认昵称
    created_at: datetime
    last_login: datetime

# 游戏记录 (核心数据结构)
class GameRecord:
    game_id: str              # UUID
    name: str                  # 游戏名称
    owner_id: str             # 房主ID

    # 成员管理
    core_members: List[Player]  # 核心成员（必须到场）
    temp_members: List[Player]  # 临时成员（可缺席）

    # 状态
    status: str               # waiting / playing / paused / ended
    created_at: datetime
    last_played: datetime

    # 世界状态
    world: WorldState

    # 存档
    current_save_id: str
    saves: List[Save]

# 玩家
class Player:
    player_id: str
    user_id: str | None       # None = 匿名/游客
    nickname: str
    is_core: bool             # 是否核心成员

    # 角色
    character: Character

    # 天道心理状态
    y_value: int
    base_y: int
    psychology: PsychState

    # 状态
    is_online: bool           # 当前是否在线
    is_ai_controlled: bool     # 是否被AI托管

# 存档
class Save:
    save_id: str
    game_id: str
    created_at: datetime
    created_by: str
    note: str                  # 存档说明
    snapshot: GameSnapshot     # 完整快照
```

### 3.3 游戏记录结构

```
用户账号
  │
  └─ 参与的游戏记录
       │
       ├─ 局A: 核心成员 [A,B,C] + 临时成员 [D,E]
       │    └─ 存档列表
       │         ├─ 存档1: 2026-04-20
       │         ├─ 存档2: 2026-04-22
       │         └─ 存档3: 2026-04-25
       │
       └─ 局B: 核心成员 [A,F,G]
            └─ 存档列表
```

**核心原则**：
- 核心成员凑不齐 = 不能继续游戏（可AI托管）
- 临时成员随时可加入，不影响存档
- 中途加入的人自动成为临时成员

---

## 四、游戏流程

### 4.1 开新游戏流程

```
1. 房主创建游戏
   ├─ 设置游戏名称
   ├─ 选择世界类型
   └─ 生成游戏ID
       │
       ▼
2. 房主邀请核心成员
   ├─ 生成邀请码/链接
   └─ 分享给指定玩家
       │
       ▼
3. 核心成员加入
   ├─ 创建角色
   ├─ 设置为核心成员
   └─ 等待其他成员
       │
       ▼
4. 所有人都就绪
   ├─ 房主确认开始
   └─ 天道生成世界 + 初始事件
       │
       ▼
5. 开始游戏
```

### 4.2 继续游戏流程

```
想继续局A？
    │
    ├─ 房主进入"我的游戏"
    │    └─ 选择"局A" → "继续游戏"
    │
    ├─ 系统检查核心成员
    │    └─ [A, B, C] 是否在线？
    │
    ├─ 核心成员到场
    │    ├─ A在线 → A进入
    │    ├─ B在线 → B进入
    │    └─ C离线 → AI托管C
    │
    ├─ 临时成员
    │    ├─ D在线 → D进入
    │    └─ E离线 → 跳过
    │
    └─ 加载最新存档
         │
         ▼
      继续游戏
```

### 4.3 中途加人流程

```
场景：游戏进行中，忽然有新朋友想加入

1. 房主或成员邀请
   └─ 生成"临时邀请码"

2. 新人加入
   ├─ 自己设定基础信息
   │    ├─ 名字
   │    └─ 性格描述（影响MBTI）
   │
   └─ 其他信息由天道随机生成
        ├─ 随机MBTI
        ├─ 随机背景
        ├─ 随机初始Y值
        └─ 自动融入当前场景

3. 新人状态
   └─ 自动成为临时成员
       └─ 不在核心成员名单
           └─ 以后重开可来可不来
```

### 4.4 AI托管机制

```
核心成员缺席
    │
    ├─ 天道自动接管其角色
    │    ├─ 保持原角色性格
    │    ├─ 根据当前情境决定行动
    │    └─ 以"天道托管"标记
    │
    └─ 原玩家随时可回来
         └─ 直接接管，AI托管结束
```

**托管策略**：
- 简单响应：玩家问话时AI代回
- 行动被动：不主动行动，等场景需要
- 紧急回避：遇危险时下意识躲避

---

## 五、服务器实现

### 5.1 技术栈

| 组件 | 选择 | 说明 |
|------|------|------|
| Web框架 | FastAPI | 异步高性能 |
| WebSocket | FastAPI WebSocket | 实时通信 |
| 数据库 | SQLite | 轻量，不额外花钱 |
| AI调用 | Anthropic/ OpenAI | API KEY |
| 部署 | Docker | 环境一致 |

### 5.2 API 设计

```python
# HTTP 路由

# 认证
POST /api/auth/device          # 创建设备账号
POST /api/auth/email           # 绑定邮箱
GET  /api/auth/me              # 获取当前用户

# 游戏
GET  /api/games                # 我的游戏列表
POST /api/games                # 创建新游戏
GET  /api/games/{id}           # 获取游戏详情
POST /api/games/{id}/invite    # 生成邀请码
POST /api/games/{id}/join      # 加入游戏
POST /api/games/{id}/continue  # 继续游戏
POST /api/games/{id}/pause     # 暂停游戏

# WebSocket
WS  /ws/{game_id}/{player_id}  # 游戏连接
```

### 5.3 WebSocket 消息

```python
# 客户端 -> 服务器
class ClientMessage:
    type: str                  # chat / action / query_status

    # chat: 聊天消息
    content: str               # 消息内容

    # action: 执行动作
    action: str                # 动作描述
    target: str | None         # 目标对象

    # query_status: 查询状态
    query: str                 # status / inventory / character

# 服务器 -> 客户端
class ServerMessage:
    type: str                  # dm / npc / system / event / status

    # dm: 天道描述
    content: str               # 描述文本

    # npc: NPC行动
    npc_name: str
    npc_action: str

    # system: 系统消息
    message: str

    # event: 事件触发
    event: Event

    # status: 状态更新
    status: dict
```

---

## 六、DM引擎设计

### 6.1 消息处理流程

```
玩家消息: "我想和门口的守卫说话"
    │
    ▼
┌─────────────────────────────┐
│  意图识别                    │
│  - 动作类型: 对话            │
│  - 目标: 守卫(NPC)          │
│  - 期望结果: 获得信息        │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│  世界状态查询                │
│  - 当前位置: 城门            │
│  - 在场NPC: 守卫A            │
│  - 在场玩家: A, B (在线)     │
│  - 缺席玩家: C (AI托管)      │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│  天道DM决策                  │
│  - 守卫性格: ISTJ, Y=55     │
│  - 与玩家关系: 陌生         │
│  - 当前任务: 盘查行人        │
│  - 生成回应风格: 公事公办    │
└─────────────────────────────┘
    │
    ▼
┌─────────────────────────────┐
│  事件检查                    │
│  - 条件: 首次与守卫对话      │
│  - 触发: "初来乍到"事件      │
└─────────────────────────────┘
    │
    ▼
输出:
DM描述 + NPC回应 + 事件通知
```

### 6.2 NPC心理系统

```python
class NPC:
    npc_id: str
    name: str

    # 天道属性
    mbti: str
    y_value: int
    base_y: int

    # NPC特性
    role: str                  # merchant / guard / quest_giver...
    disposition: str            # friendly / hostile / neutral
    personality: str            # 性格描述

    # 状态
    location: str
    current_goal: str
    relationships: Dict[str, int]  # 对玩家的关系

    # 能力
    dialogue_style: str        # 说话风格
    knowledge: List[str]        # 知道的信息
```

### 6.3 事件触发器

```python
class EventTrigger:
    # 触发类型
    type: str                  # time / location / interaction / condition / random

    # 触发条件
    condition: dict

    # 事件内容
    title: str
    description: str
    choices: List[Choice]       # 玩家可选行动
    effects: List[Effect]       # 事件效果

class Event:
    event_id: str
    trigger: EventTrigger
    status: str                 # pending / active / completed / failed
    participants: List[str]     # 涉及的玩家ID
```

---

## 七、部署方案

### 7.1 Autodl 配置

| 配置项 | 推荐 | 说明 |
|--------|------|------|
| 规格 | 1元/小时档位 | RTX + 40-80G内存够用 |
| 硬盘 | 50G | SQLite数据 + Docker镜像 |
| IP | 固定（不释放实例） | 核心优势 |
| 计费 | 按量 | 不用时0.1元/天 |

### 7.2 Docker 部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制项目
COPY . .

# 安装Python依赖
RUN pip install -r requirements.txt

# 暴露端口
EXPOSE 5000

# 启动
CMD ["uvicorn", "src.server:app", "--host", "0.0.0.0", "--port", "5000"]
```

### 7.3 启动流程

```
平时（关机状态）
  └─ 0.1元/天

开团前（Autodl控制台操作）
  ├─ 点"开机"
  ├─ 等待30秒启动
  └─ 服务自动运行

游戏中
  └─ 玩家直连固定IP

结束后
  ├─ 存档自动保存
  └─ Autodl控制台点"关机"
```

---

## 八、开发优先级

### 8.1 MVP (第一阶段)

| 优先级 | 功能 | 工作量 | 说明 |
|--------|------|--------|------|
| **P0** | 服务器框架 | 1天 | FastAPI + WebSocket |
| **P0** | 设备账号 | 0.5天 | 创建设备ID |
| **P0** | 游戏创建/加入 | 1天 | 房间码机制 |
| **P0** | PWA客户端 | 1天 | manifest + sw |
| **P0** | 天道DM基础 | 2天 | AI调用 + 提示词 |
| **P1** | 核心成员管理 | 1天 | 到场检测 + AI托管 |
| **P1** | 中途加人 | 1天 | 临时邀请码 |
| **P2** | 存档系统 | 1天 | SQLite持久化 |
| **P2** | 世界生成 | 1天 | 进入前生成世界观 |

### 8.2 后续功能

| 优先级 | 功能 | 说明 |
|--------|------|------|
| **P2** | 邮箱注册 | 账号永久化 |
| **P2** | 事件系统 | 完整触发/选项/后果 |
| **P3** | 战斗系统 | DM裁决 |
| **P3** | 数据导入 | 设备→账号迁移 |
| **P3** | 存档备份 | OSS云备份 |

---

## 九、PWA 实现要点

### 9.1 manifest.json

```json
{
  "name": "天道 TRPG",
  "short_name": "天道",
  "description": "赛博跑团 - 老天爷当DM",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1a1a2e",
  "theme_color": "#16213e",
  "icons": [
    {
      "src": "/static/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/static/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
```

### 9.2 Service Worker 缓存策略

```javascript
// sw.js
const CACHE_NAME = 'tiandao-trpg-v1';
const urlsToCache = [
  '/',
  '/static/style.css',
  '/static/client.js',
  '/static/icon-192.png'
];

// 缓存优先
self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});
```

---

## 十、相关文档

| 文档 | 说明 |
|------|------|
| `独立项目.md` | 天道系统单机版 |
| `天道桌游版构思.md` | 完整TRPG版设想 |
| `天道TRPG派对版方案.md` | **本文档** - Autodl云服务器+PWA |

---

## 附录：云主机配置

### Autodl 实例信息

| 配置项 | 值 |
|--------|-----|
| 连接地址 | `connect.bjb1.seetacloud.com` |
| SSH端口 | `38591` |
| 用户名 | `root` |
| 镜像 | Ubuntu 22.04 + PyTorch 2.7.0 + Python 3.12 + CUDA 12.8 |
| 状态策略 | 每天22:00开机3分钟保持活性，关机15天后释放 |

### 连接方式

```bash
ssh -p 38591 root@connect.bjb1.seetacloud.com
# 输入密码后登录
```

### 部署检查清单

- [ ] 确认Python版本 `python3 --version`
- [ ] 确认pip版本 `pip3 --version`
- [ ] 克隆项目到 `/root/tiandao-trpg`
- [ ] 安装依赖 `pip3 install -r requirements.txt`
- [ ] 配置环境变量 `.env`
- [ ] 启动服务测试

---

## 附录：核心概念

| 概念 | 说明 |
|------|------|
| **游戏记录** | 某一局从开始到现在的所有进度 |
| **核心成员** | 原班人马，必须凑齐才能继续 |
| **临时成员** | 中途加入，可缺席，AI不托管 |
| **AI托管** | 核心成员缺席时，AI接管其角色 |
| **游戏记录制** | 换人开新局，不支持中途换人 |
| **PWA** | 渐进式网页应用，可添加到桌面 |

---

*文档版本：1.0*
*最后更新：2026-04-28*
*状态：方案确定，待实现*
