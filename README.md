# 天道 TRPG Party

> 赛博跑团 - 老天爷当DM，多位玩家异地同屏

## 快速部署

### 1. 启动服务器
```bash
python scripts/server_manager.py start
```

### 2. 打开浏览器访问
```
https://u892543-zjue-dc99aa16.bjb1.seetacloud.com:8443/
```

### 3. 停止服务器
```bash
python scripts/server_manager.py stop
```

## 功能

- [x] 创建筑/加入房间
- [x] 多玩家WebSocket实时通信
- [x] 基础天道DM响应
- [x] 位置和NPC系统
- [x] AI托管（核心成员离线时）
- [ ] 完整角色创建
- [ ] 世界生成器
- [ ] 事件触发系统
- [ ] 存档系统

## 项目结构

```
tiandao-trpg-party/
├── src/
│   ├── server.py        # 主服务器
│   ├── models.py        # 数据模型
│   └── game_manager.py  # 游戏状态管理
├── web/
│   ├── templates/       # HTML模板
│   └── static/         # CSS, JS, PWA
├── scripts/
│   └── server_manager.py # 服务器管理工具
└── requirements.txt
```

## 开发

```bash
# 安装依赖
pip install -r requirements.txt

# 本地运行
python -m uvicorn src.server:app --reload

# 部署到服务器
python scripts/server_manager.py deploy
```
