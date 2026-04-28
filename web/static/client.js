/**
 * 天道 TRPG - 客户端
 * 沉浸式跑团体验
 */

// 服务器配置
function getServerUrl() {
    const saved = localStorage.getItem('tiandao_server_url');
    if (saved) return saved;
    const params = new URLSearchParams(window.location.search);
    const urlParam = params.get('server');
    if (urlParam) {
        localStorage.setItem('tiandao_server_url', urlParam);
        return urlParam;
    }
    return window.location.origin;
}

const API_BASE = getServerUrl();
let ws = null;
let gameId = null;
let playerId = null;
let roomCode = null;
let nickname = null;
let currentGame = null;
let reconnectAttempts = 0;
const MAX_RECONNECT = 5;

// 角色创建数据
let charCreation = {
    name: '',
    appearance: '',
    background: '',
    personality: ''
};

// 角色选项映射
const APPEARANCE_EMOJI = {
    'warrior': '⚔️', 'mage': '🔮', 'rogue': '🗡️',
    'scholar': '📚', 'merchant': '💰', 'wanderer': '🌟'
};

const APPEARANCE_TITLES = {
    'warrior': '战士', 'mage': '法师', 'rogue': '刺客',
    'scholar': '学者', 'merchant': '商人', 'wanderer': '流浪者'
};

const BACKGROUND_TITLES = {
    'noble': '贵族', 'common': '平民', 'outcast': '孤儿', 'cultivator': '修士'
};

const PERSONALITY_NAMES = {
    'brave': '勇敢者', 'cunning': '智谋者', 'kind': '仁善者', 'mysterious': '神秘客'
};

// ============================================
// 初始化
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    loadSession();

    document.getElementById('message-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});

// ============================================
// 界面切换
// ============================================

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(screenId)?.classList.add('active');
}

function showModal(modalId) {
    document.getElementById(modalId)?.classList.remove('hidden');
}

function closeModal(modalId) {
    document.getElementById(modalId)?.classList.add('hidden');
}

function showCreateOptions() {
    document.getElementById('create-options').classList.toggle('hidden');
}

function showJoinForm() {
    document.getElementById('join-form').classList.toggle('hidden');
}

function showMenu() {
    showScreen('menu-screen');
}

function hideMenu() {
    showScreen('game-screen');
}

// ============================================
// 角色创建 - 沉浸式流程
// ============================================

function selectOption(type, value) {
    charCreation[type] = value;

    // 高亮选中项
    const container = event.target.closest('.option-grid');
    container.querySelectorAll('.option-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    event.target.closest('.option-btn').classList.add('selected');

    // 更新预览
    updateCharPreview();
}

function updateCharPreview() {
    if (!charCreation.name && !charCreation.appearance) return;

    const preview = document.getElementById('char-preview');
    preview.style.display = 'block';

    const emoji = APPEARANCE_EMOJI[charCreation.appearance] || '❓';
    const title = getCharTitle();

    document.getElementById('preview-avatar').textContent = emoji;
    document.getElementById('preview-name').textContent = charCreation.name || '未命名';
    document.getElementById('preview-title').textContent = title;
}

function getCharTitle() {
    const app = APPEARANCE_TITLES[charCreation.appearance] || '冒险者';
    const bg = BACKGROUND_TITLES[charCreation.background] || '';
    const pers = PERSONALITY_NAMES[charCreation.personality] || '';
    return `${bg}${app}`;
}

function nextCreationStep(nextId) {
    // 验证当前步骤
    if (document.getElementById('step-name').classList.contains('active')) {
        charCreation.name = document.getElementById('char-name').value.trim();
        if (!charCreation.name) {
            alert('请输入角色名称');
            return;
        }
        updateCharPreview();
    }

    // 隐藏当前步骤
    document.querySelectorAll('.creation-step').forEach(s => s.classList.remove('active'));
    // 显示下一步
    document.getElementById(nextId)?.classList.add('active');
}

function prevCreationStep() {
    const steps = ['step-name', 'step-appearance', 'step-background', 'step-personality'];
    const currentIndex = steps.findIndex(id => document.getElementById(id).classList.contains('active'));

    if (currentIndex > 0) {
        document.querySelectorAll('.creation-step').forEach(s => s.classList.remove('active'));
        document.getElementById(steps[currentIndex - 1]).classList.add('active');
    }
}

function confirmCharacter() {
    if (!charCreation.name) {
        charCreation.name = document.getElementById('char-name').value.trim();
    }

    if (!charCreation.name) {
        alert('请输入角色名称');
        return;
    }

    // 发送到服务器
    fetch(`${API_BASE}/api/game/${gameId}/character`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(charCreation)
    }).then(() => {
        // 跳转到等待或游戏界面
        if (currentGame && currentGame.status === 'playing') {
            showScreen('game-screen');
        } else {
            showScreen('waiting-screen');
        }
    });
}

// ============================================
// 游戏逻辑
// ============================================

async function createGame() {
    nickname = document.getElementById('nickname').value.trim() || '匿名';
    const worldType = document.getElementById('world-type').value;
    const gameName = document.getElementById('game-name').value.trim() || '冒险之旅';

    try {
        const resp = await fetch(`${API_BASE}/api/game/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                owner_nickname: nickname,
                game_name: gameName,
                world_type: worldType
            })
        });

        const data = await resp.json();
        gameId = data.game_id;
        playerId = data.owner_id;
        roomCode = data.room_code;

        currentGame = data.game;
        saveSession();

        // 更新等待界面
        document.getElementById('waiting-room-name').textContent = gameName;
        document.getElementById('waiting-room-code').textContent = roomCode;
        document.getElementById('share-code').textContent = roomCode;
        document.getElementById('player-name').textContent = nickname;

        // 显示角色创建
        showScreen('character-screen');
        document.getElementById('char-name').value = nickname;

    } catch (e) {
        alert('创建失败: ' + e);
    }
}

async function joinGame() {
    nickname = document.getElementById('nickname').value.trim() || '匿名';
    roomCode = document.getElementById('room-code').value.trim().toUpperCase();

    if (roomCode.length !== 4) {
        alert('请输入4位房间码');
        return;
    }

    try {
        const resp = await fetch(`${API_BASE}/api/game/join`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                nickname: nickname,
                room_code: roomCode
            })
        });

        if (!resp.ok) {
            const err = await resp.json();
            alert('加入失败: ' + (err.detail || '房间不存在'));
            return;
        }

        const data = await resp.json();
        gameId = data.game_id;
        playerId = data.player_id;
        currentGame = data.game;

        saveSession();

        // 检查游戏状态
        if (currentGame.status === 'waiting') {
            // 显示角色创建
            document.getElementById('char-name').value = nickname;
            showScreen('character-screen');
        } else if (currentGame.status === 'playing') {
            // 直接进入游戏
            enterGameScreen();
        }

    } catch (e) {
        alert('加入失败: ' + e);
    }
}

async function startGame() {
    try {
        const resp = await fetch(`${API_BASE}/api/game/${gameId}/start`, {
            method: 'POST'
        });

        if (resp.ok) {
            enterGameScreen();
        }
    } catch (e) {
        alert('开始游戏失败');
    }
}

function enterGameScreen() {
    showScreen('game-screen');

    // 更新界面
    document.getElementById('room-name').textContent = currentGame.name;
    document.getElementById('room-code-display').textContent = roomCode;
    document.getElementById('player-name').textContent = nickname;

    // 更新位置
    updateLocationInfo();

    // 连接WebSocket
    connectWebSocket();
}

function updateLocationInfo() {
    if (!currentGame || !currentGame.world) return;

    const loc = currentGame.world.current_location_id;
    const locations = currentGame.world.locations;
    const location = locations[loc];

    if (location) {
        document.getElementById('current-location').textContent = location.name || '未知地点';
    }

    updatePlayersList();
}

// ============================================
// WebSocket
// ============================================

function connectWebSocket() {
    const wsProtocol = API_BASE.startsWith('https://') ? 'wss://' : 'ws://';
    const wsHost = API_BASE.replace(/^https?:\/\//, '');
    const wsUrl = `${wsProtocol}${wsHost}/ws/${gameId}/${playerId}`;

    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        console.log('WebSocket connected');
        reconnectAttempts = 0;
    };

    ws.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        handleMessage(msg);
    };

    ws.onclose = () => {
        console.log('WebSocket disconnected');
        if (gameId && playerId) {
            attemptReconnect();
        }
    };

    ws.onerror = (err) => {
        console.error('WebSocket error:', err);
    };
}

function attemptReconnect() {
    if (reconnectAttempts >= MAX_RECONNECT) {
        return;
    }
    reconnectAttempts++;
    setTimeout(() => {
        if (gameId && playerId) connectWebSocket();
    }, 2000 * reconnectAttempts);
}

// ============================================
// 消息处理
// ============================================

function handleMessage(msg) {
    switch (msg.type) {
        case 'system':
            addSystemMessage(msg.content);
            break;
        case 'chat':
            addChatMessage(msg.nickname, msg.content, 'player');
            break;
        case 'action':
            addActionMessage(msg.nickname, msg.content);
            break;
        case 'dm':
            addDMMessage(msg.content);
            break;
        case 'npc':
            addNPCMessage(msg.npc_name, msg.content);
            break;
        case 'event':
            addEventMessage(msg.event.title, msg.event.description, msg.event.choices, msg.event.event_id);
            break;
        case 'location':
            // 位置变化更新
            if (msg.location) {
                document.getElementById('current-location').textContent = msg.location;
            }
            addDMMessage(msg.content);
            break;
        case 'game_state':
            currentGame = msg.game;
            updateLocationInfo();
            break;
        case 'players':
            updatePlayersList(msg.players);
            break;
    }
}

function addChatMessage(sender, content, type = 'player') {
    const div = document.createElement('div');
    div.className = `message ${type}`;
    div.innerHTML = `<div class="sender">${sender}</div><div class="content">${escapeHtml(content)}</div>`;
    appendMessage(div);
}

function addSystemMessage(content) {
    const div = document.createElement('div');
    div.className = 'message system';
    div.textContent = content;
    appendMessage(div);
}

function addActionMessage(sender, action) {
    const div = document.createElement('div');
    div.className = 'message action';
    div.innerHTML = `<div class="sender">${sender}</div><div class="content"><em>${escapeHtml(action)}</em></div>`;
    appendMessage(div);
}

function addDMMessage(content) {
    const div = document.createElement('div');
    div.className = 'message dm';
    div.innerHTML = `<div class="sender">【天道】</div><div class="content">${escapeHtml(content)}</div>`;
    appendMessage(div);
}

function addNPCMessage(npcName, content) {
    const div = document.createElement('div');
    div.className = 'message npc';
    div.innerHTML = `<div class="sender">【${npcName}】</div><div class="content">${escapeHtml(content)}</div>`;
    appendMessage(div);
}

function addEventMessage(title, description, choices = [], eventId = '') {
    const div = document.createElement('div');
    div.className = 'message event';
    div.innerHTML = `<div class="sender">⚡ ${title}</div><div class="content">${escapeHtml(description)}</div>`;

    // 添加选项按钮
    if (choices && choices.length > 0) {
        const choicesDiv = document.createElement('div');
        choicesDiv.className = 'event-choices';
        choices.forEach(choice => {
            const btn = document.createElement('button');
            btn.className = 'choice-btn';
            btn.textContent = choice.text;
            btn.onclick = () => makeChoice(eventId, choice.choice_id);
            choicesDiv.appendChild(btn);
        });
        div.querySelector('.content').appendChild(choicesDiv);
    }

    appendMessage(div);
}

function appendMessage(div) {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.appendChild(div);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// ============================================
// 发送消息
// ============================================

function sendMessage() {
    const input = document.getElementById('message-input');
    const content = input.value.trim();
    if (!content || !ws) return;

    input.value = '';

    ws.send(JSON.stringify({
        type: 'chat',
        content: content
    }));
}

function quickAction(action) {
    if (!ws) return;

    ws.send(JSON.stringify({
        type: 'action',
        content: action
    }));
}

function doAction(action) {
    closeModal('actions-modal');
    quickAction(action);
}

function makeChoice(eventId, choiceId) {
    if (!ws) return;

    ws.send(JSON.stringify({
        type: 'event_choice',
        event_id: eventId,
        choice_id: choiceId
    }));
}

// ============================================
// 状态显示
// ============================================

function showStatus() {
    showCharacterInfo();
}

function showCharacterInfo() {
    const info = `
        <p><strong>名称:</strong> ${nickname}</p>
        <p><strong>身份:</strong> ${getCharTitle()}</p>
        <p><strong>性格:</strong> ${PERSONALITY_NAMES[charCreation.personality] || '未知'}</p>
        <p><strong>背景:</strong> ${BACKGROUND_TITLES[charCreation.background] || '未知'}</p>
    `;
    document.getElementById('modal-char-name').textContent = charCreation.name || nickname;
    document.getElementById('modal-char-info').innerHTML = info;
    showModal('character-modal');
}

function showWorldInfo() {
    if (!currentGame || !currentGame.world) return;

    const world = currentGame.world;
    document.getElementById('modal-world-name').textContent = world.name || '未知世界';
    document.getElementById('modal-world-info').innerHTML = `
        <p><strong>类型:</strong> ${getWorldTypeName(world.world_type)}</p>
        <p><strong>简介:</strong> ${world.overview || '暂无描述'}</p>
    `;
    showModal('world-modal');
}

function getWorldTypeName(type) {
    const names = {
        'fantasy': '奇幻大陆',
        'urban': '现代都市',
        'sci_fi': '未来科幻'
    };
    return names[type] || type;
}

function showLocationInfo() {
    if (!currentGame || !currentGame.world) return;

    const locId = currentGame.world.current_location_id;
    const location = currentGame.world.locations[locId];
    const npcs = currentGame.world.npcs || {};

    // 找到当前位置的NPC
    const presentNpcs = Object.values(npcs).filter(n => n.location === locId);

    let npcList = '';
    if (presentNpcs.length > 0) {
        npcList = '<p><strong>在场人物:</strong></p><ul>';
        presentNpcs.forEach(npc => {
            npcList += `<li>${npc.name} - ${npc.dialogue_style || '暂无描述'}</li>`;
        });
        npcList += '</ul>';
    }

    document.getElementById('modal-char-name').textContent = location?.name || '未知地点';
    document.getElementById('modal-char-info').innerHTML = `
        <p><strong>描述:</strong> ${location?.description || '暂无描述'}</p>
        <p><strong>氛围:</strong> ${location?.atmosphere || '普通'}</p>
        <p><strong>出口:</strong> ${(location?.exits || []).join(', ') || '无'}</p>
        ${npcList}
    `;
    showModal('character-modal');
}

function showMap() {
    if (!currentGame || !currentGame.world) return;

    const locations = currentGame.world.locations || {};
    const currentLocId = currentGame.world.current_location_id;

    let locList = '<div class="location-list">';
    Object.values(locations).forEach(loc => {
        const isHere = loc.location_id === currentLocId;
        locList += `
            <div class="location-item ${isHere ? 'current' : ''}">
                <strong>${isHere ? '👉 ' : ''}${loc.name}</strong>
                <p>${loc.description || ''}</p>
            </div>
        `;
    });
    locList += '</div>';

    document.getElementById('map-content').innerHTML = `
        <p><strong>当前世界:</strong> ${currentGame.world.name}</p>
    `;
    document.getElementById('location-list').innerHTML = locList;
    showModal('map-modal');
}

function showActions() {
    showModal('actions-modal');
}

function updatePlayersList(players) {
    const list = document.getElementById('players-list');
    if (!list) return;

    if (!players && currentGame) {
        players = [...(currentGame.core_members || []), ...(currentGame.temp_members || [])];
    }

    if (!players || players.length === 0) {
        list.innerHTML = '';
        return;
    }

    list.innerHTML = players.map(p => `
        <span class="player-tag ${p.is_online ? 'online' : 'offline'}">
            ${p.nickname} ${!p.is_online ? '(离线)' : ''}
        </span>
    `).join('');
}

// ============================================
// 会话管理
// ============================================

function saveSession() {
    const session = { playerId, nickname, gameId };
    localStorage.setItem('tiandao_session', JSON.stringify(session));
}

function loadSession() {
    const saved = localStorage.getItem('tiandao_session');
    if (saved) {
        const session = JSON.parse(saved);
        if (session.nickname) {
            document.getElementById('nickname').value = session.nickname;
        }
    }
}

function clearSession() {
    localStorage.removeItem('tiandao_session');
}

function leaveGame() {
    if (ws) {
        ws.close();
        ws = null;
    }
    gameId = null;
    playerId = null;
    roomCode = null;
    currentGame = null;
    charCreation = { name: '', appearance: '', background: '', personality: '' };
    clearSession();
    showScreen('connect-screen');
    document.getElementById('messages').innerHTML = '';
}

function copyRoomCode() {
    navigator.clipboard.writeText(roomCode).then(() => {
        alert('房间码已复制');
    });
}

function showServerConfig() {
    const current = localStorage.getItem('tiandao_server_url') || window.location.origin;
    const input = prompt('请输入服务器地址:\n(直接回车使用当前地址，清空则恢复默认)', current);
    if (input === null) return;
    if (input.trim() === '') {
        localStorage.removeItem('tiandao_server_url');
        alert('已恢复默认服务器地址，刷新页面生效');
    } else {
        localStorage.setItem('tiandao_server_url', input.trim());
        alert('服务器地址已设置，刷新页面生效');
    }
}

// ============================================
// 工具
// ============================================

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
