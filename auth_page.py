#!/usr/bin/env python3
"""
Googleアカウント認証用のWebページ
"""

from flask import Flask, render_template_string, request, jsonify, redirect, url_for
from google_calendar_service import GoogleCalendarService
import os

app = Flask(__name__)

# 認証ページのHTMLテンプレート
AUTH_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Googleアカウント認証</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
            font-size: 28px;
        }
        .account-list {
            list-style: none;
            padding: 0;
            margin: 20px 0;
        }
        .account-item {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 15px;
            margin: 10px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .account-item:hover {
            background: #e3f2fd;
            border-color: #2196f3;
            transform: translateY(-2px);
        }
        .account-item.authenticated {
            background: #e8f5e8;
            border-color: #4caf50;
        }
        .btn {
            background: #4caf50;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            margin: 10px;
            transition: all 0.3s ease;
        }
        .btn:hover {
            background: #45a049;
            transform: translateY(-2px);
        }
        .status {
            margin: 20px 0;
            padding: 10px;
            border-radius: 5px;
            font-weight: bold;
        }
        .status.success {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .status.error {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 Googleアカウント認証</h1>
        
        <div id="status"></div>
        
        <h3>認証するアカウントを選択してください</h3>
        <ul class="account-list">
            <li class="account-item" data-account="ezasyo11@gmail.com">
                📧 ezasyo11@gmail.com
            </li>
            <li class="account-item" data-account="syotaezaki@gmail.com">
                📧 syotaezaki@gmail.com
            </li>
        </ul>
        
        <button class="btn" onclick="checkStatus()">ステータス確認</button>
        <button class="btn" onclick="goToApp()">アプリに戻る</button>
    </div>

    <script>
        function authenticateAccount(account) {
            fetch('/authenticate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({account: account})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showStatus('✅ ' + account + ' の認証が完了しました！', 'success');
                    document.querySelector(`[data-account="${account}"]`).classList.add('authenticated');
                } else {
                    showStatus('❌ ' + account + ' の認証に失敗しました: ' + data.message, 'error');
                }
            })
            .catch(error => {
                showStatus('❌ エラーが発生しました: ' + error, 'error');
            });
        }

        function checkStatus() {
            fetch('/status')
            .then(response => response.json())
            .then(data => {
                if (data.authenticated_accounts && data.authenticated_accounts.length > 0) {
                    showStatus('✅ 認証済みアカウント: ' + data.authenticated_accounts.join(', '), 'success');
                    data.authenticated_accounts.forEach(account => {
                        document.querySelector(`[data-account="${account}"]`).classList.add('authenticated');
                    });
                } else {
                    showStatus('❌ 認証済みアカウントがありません', 'error');
                }
            });
        }

        function showStatus(message, type) {
            const statusDiv = document.getElementById('status');
            statusDiv.innerHTML = '<div class="status ' + type + '">' + message + '</div>';
        }

        function goToApp() {
            window.location.href = 'http://127.0.0.1:5002';
        }

        // アカウントアイテムをクリック可能にする
        document.querySelectorAll('.account-item').forEach(item => {
            item.addEventListener('click', function() {
                const account = this.getAttribute('data-account');
                authenticateAccount(account);
            });
        });

        // ページ読み込み時にステータスを確認
        window.onload = function() {
            checkStatus();
        };
    </script>
</body>
</html>
"""

@app.route('/')
def auth_page():
    """認証ページを表示"""
    return render_template_string(AUTH_PAGE_TEMPLATE)

@app.route('/authenticate', methods=['POST'])
def authenticate():
    """アカウント認証を実行"""
    try:
        data = request.get_json()
        account = data.get('account')
        
        if not account:
            return jsonify({'success': False, 'message': 'アカウントが指定されていません'})
        
        # GoogleCalendarServiceで認証
        service = GoogleCalendarService()
        success = service.authenticate(account)
        
        if success:
            return jsonify({'success': True, 'message': f'{account} の認証が完了しました'})
        else:
            return jsonify({'success': False, 'message': '認証に失敗しました'})
            
    except Exception as e:
        return jsonify({'success': False, 'message': f'エラー: {str(e)}'})

@app.route('/status')
def status():
    """認証状況を確認"""
    try:
        # トークンファイルの存在確認
        token_files = [f for f in os.listdir('.') if f.startswith('token_') and f.endswith('.pickle')]
        authenticated_accounts = []
        
        for token_file in token_files:
            # token_account@example.com.pickle から account@example.com を抽出
            account = token_file.replace('token_', '').replace('.pickle', '')
            authenticated_accounts.append(account)
        
        return jsonify({
            'success': True,
            'authenticated_accounts': authenticated_accounts,
            'count': len(authenticated_accounts)
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'エラー: {str(e)}'})

if __name__ == '__main__':
    print("🔐 認証ページを起動します...")
    print("📱 ブラウザで http://127.0.0.1:5001 にアクセスしてください")
    app.run(debug=True, host='0.0.0.0', port=5001)