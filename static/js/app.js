// グローバル変数
let currentEvents = {};
let currentAccounts = [];

// ページ読み込み時の初期化
document.addEventListener('DOMContentLoaded', function() {
    loadAccounts();
    loadEvents();
    
    // イベントフォームの送信処理
    document.getElementById('event-form').addEventListener('submit', function(e) {
        e.preventDefault();
        createEvent();
    });
});

// アラート表示関数
function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alert-container');
    const alertId = 'alert-' + Date.now();
    
    const alertHtml = `
        <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    alertContainer.insertAdjacentHTML('beforeend', alertHtml);
    
    // 5秒後に自動で閉じる
    setTimeout(() => {
        const alertElement = document.getElementById(alertId);
        if (alertElement) {
            const bsAlert = new bootstrap.Alert(alertElement);
            bsAlert.close();
        }
    }, 5000);
}

// アカウント追加
async function addAccount() {
    const userIdInput = document.getElementById('user-id-input');
    const userId = userIdInput.value.trim();
    
    if (!userId) {
        showAlert('ユーザーIDを入力してください', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/add_account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: userId })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(result.message, 'success');
            userIdInput.value = '';
            loadAccounts();
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('アカウント追加中にエラーが発生しました', 'danger');
        console.error('Error:', error);
    }
}

// アカウント削除
async function removeAccount(userId) {
    if (!confirm(`アカウント "${userId}" を削除しますか？`)) {
        return;
    }
    
    try {
        const response = await fetch('/remove_account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id: userId })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(result.message, 'success');
            loadAccounts();
            loadEvents();
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('アカウント削除中にエラーが発生しました', 'danger');
        console.error('Error:', error);
    }
}

// アカウント一覧読み込み
async function loadAccounts() {
    try {
        const response = await fetch('/get_accounts');
        const result = await response.json();
        
        if (result.success) {
            currentAccounts = result.accounts;
            displayAccounts();
            updateAccountSelect();
        }
    } catch (error) {
        console.error('Error loading accounts:', error);
    }
}

// アカウント一覧表示
function displayAccounts() {
    const accountsList = document.getElementById('accounts-list');
    
    if (currentAccounts.length === 0) {
        accountsList.innerHTML = '<p class="text-muted">アカウントが登録されていません</p>';
        return;
    }
    
    const accountsHtml = currentAccounts.map(account => `
        <div class="account-item">
            <span class="account-name">${account}</span>
            <button class="btn btn-danger btn-sm" onclick="removeAccount('${account}')">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    `).join('');
    
    accountsList.innerHTML = accountsHtml;
}

// アカウント選択ボックス更新
function updateAccountSelect() {
    const accountSelect = document.getElementById('event-account');
    accountSelect.innerHTML = '<option value="">アカウントを選択</option>';
    
    currentAccounts.forEach(account => {
        const option = document.createElement('option');
        option.value = account;
        option.textContent = account;
        accountSelect.appendChild(option);
    });
}

// イベント作成
async function createEvent() {
    const title = document.getElementById('event-title').value;
    const description = document.getElementById('event-description').value;
    const startTime = document.getElementById('start-time').value;
    const endTime = document.getElementById('end-time').value;
    const account = document.getElementById('event-account').value;
    
    if (!title || !startTime || !endTime || !account) {
        showAlert('すべての必須項目を入力してください', 'warning');
        return;
    }
    
    if (new Date(startTime) >= new Date(endTime)) {
        showAlert('終了時刻は開始時刻より後に設定してください', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/create_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: account,
                title: title,
                description: description,
                start_time: startTime + ':00',
                end_time: endTime + ':00'
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(result.message, 'success');
            document.getElementById('event-form').reset();
            loadEvents();
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('イベント作成中にエラーが発生しました', 'danger');
        console.error('Error:', error);
    }
}

// イベント一覧読み込み
async function loadEvents() {
    try {
        const response = await fetch('/get_events');
        const result = await response.json();
        
        if (result.success) {
            currentEvents = result.events;
            displayEvents();
        }
    } catch (error) {
        console.error('Error loading events:', error);
    }
}

// イベント一覧表示
function displayEvents() {
    const eventsContainer = document.getElementById('events-container');
    
    if (Object.keys(currentEvents).length === 0) {
        eventsContainer.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-calendar-plus"></i>
                <h3>イベントがありません</h3>
                <p>新しいイベントを作成するか、アカウントを追加してください</p>
            </div>
        `;
        return;
    }
    
    let allEvents = [];
    
    // 全アカウントのイベントを統合
    Object.keys(currentEvents).forEach(account => {
        currentEvents[account].forEach(event => {
            allEvents.push({
                ...event,
                account: account
            });
        });
    });
    
    // 開始時刻でソート
    allEvents.sort((a, b) => {
        const timeA = new Date(a.start.dateTime || a.start.date);
        const timeB = new Date(b.start.dateTime || b.start.date);
        return timeA - timeB;
    });
    
    if (allEvents.length === 0) {
        eventsContainer.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-calendar-check"></i>
                <h3>イベントがありません</h3>
                <p>新しいイベントを作成してください</p>
            </div>
        `;
        return;
    }
    
    const eventsHtml = allEvents.map(event => {
        const startTime = new Date(event.start.dateTime || event.start.date);
        const endTime = new Date(event.end.dateTime || event.end.date);
        
        return `
            <div class="event-card">
                <div class="event-header">
                    <h5 class="event-title">${event.summary || 'タイトルなし'}</h5>
                    <span class="event-account">${event.account}</span>
                </div>
                <div class="event-time">
                    <i class="fas fa-clock"></i>
                    ${formatDateTime(startTime)} - ${formatDateTime(endTime)}
                </div>
                ${event.description ? `<div class="event-description">${event.description}</div>` : ''}
                <div class="event-actions">
                    <button class="btn btn-warning btn-action" onclick="editEvent('${event.id}', '${event.account}')">
                        <i class="fas fa-edit"></i> 編集
                    </button>
                    <button class="btn btn-danger btn-action" onclick="deleteEvent('${event.id}', '${event.account}', '${event.summary || ''}')">
                        <i class="fas fa-trash"></i> 削除
                    </button>
                </div>
            </div>
        `;
    }).join('');
    
    eventsContainer.innerHTML = eventsHtml;
}

// イベント編集
function editEvent(eventId, userId) {
    const event = currentEvents[userId]?.find(e => e.id === eventId);
    if (!event) return;
    
    // モーダルに値を設定
    document.getElementById('edit-event-id').value = eventId;
    document.getElementById('edit-user-id').value = userId;
    document.getElementById('edit-event-title').value = event.summary || '';
    document.getElementById('edit-event-description').value = event.description || '';
    
    // 日時の設定
    const startTime = new Date(event.start.dateTime || event.start.date);
    const endTime = new Date(event.end.dateTime || event.end.date);
    
    document.getElementById('edit-start-time').value = formatDateTimeForInput(startTime);
    document.getElementById('edit-end-time').value = formatDateTimeForInput(endTime);
    
    // モーダルを表示
    const modal = new bootstrap.Modal(document.getElementById('editEventModal'));
    modal.show();
}

// イベント更新
async function updateEvent() {
    const eventId = document.getElementById('edit-event-id').value;
    const userId = document.getElementById('edit-user-id').value;
    const title = document.getElementById('edit-event-title').value;
    const description = document.getElementById('edit-event-description').value;
    const startTime = document.getElementById('edit-start-time').value;
    const endTime = document.getElementById('edit-end-time').value;
    
    if (!title || !startTime || !endTime) {
        showAlert('すべての必須項目を入力してください', 'warning');
        return;
    }
    
    if (new Date(startTime) >= new Date(endTime)) {
        showAlert('終了時刻は開始時刻より後に設定してください', 'warning');
        return;
    }
    
    try {
        const response = await fetch('/update_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                event_id: eventId,
                title: title,
                description: description,
                start_time: startTime + ':00',
                end_time: endTime + ':00'
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(result.message, 'success');
            bootstrap.Modal.getInstance(document.getElementById('editEventModal')).hide();
            loadEvents();
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('イベント更新中にエラーが発生しました', 'danger');
        console.error('Error:', error);
    }
}

// イベント削除
async function deleteEvent(eventId, userId, eventTitle) {
    if (!confirm(`イベント "${eventTitle}" を削除しますか？`)) {
        return;
    }
    
    try {
        const response = await fetch('/delete_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                event_id: eventId,
                event_title: eventTitle
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert(result.message, 'success');
            loadEvents();
        } else {
            showAlert(result.message, 'danger');
        }
    } catch (error) {
        showAlert('イベント削除中にエラーが発生しました', 'danger');
        console.error('Error:', error);
    }
}

// イベント一覧更新
function refreshEvents() {
    loadEvents();
    showAlert('イベント一覧を更新しました', 'info');
}

// 日時フォーマット関数
function formatDateTime(date) {
    return date.toLocaleString('ja-JP', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatDateTimeForInput(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    
    return `${year}-${month}-${day}T${hours}:${minutes}`;
}
