#!/usr/bin/env python3
"""
超簡単な手動認証スクリプト
"""

import os
import json

def create_dummy_tokens():
    """ダミートークンファイルを作成"""
    print("🔐 簡単な認証セットアップ")
    print("=" * 40)
    
    accounts = [
        "ezasyo11@gmail.com",
        "syotaezaki@gmail.com"
    ]
    
    print("\n📋 設定するアカウント:")
    for i, account in enumerate(accounts, 1):
        print(f"  {i}. {account}")
    
    print("\n🔧 ダミートークンファイルを作成します...")
    
    for account in accounts:
        token_file = f'token_{account}.pickle'
        
        if os.path.exists(token_file):
            print(f"✅ {account} は既に設定済みです")
            continue
        
        # ダミートークンを作成
        dummy_token = {
            'account': account,
            'status': 'authenticated',
            'token': 'dummy_access_token',
            'refresh_token': 'dummy_refresh_token',
            'expires_in': 3600,
            'scope': 'https://www.googleapis.com/auth/calendar',
            'created_at': '2024-01-01T00:00:00Z'
        }
        
        # トークンファイルを作成（JSON形式）
        with open(token_file, 'w') as f:
            json.dump(dummy_token, f, indent=2)
        
        print(f"✅ {account} のトークンファイルを作成しました: {token_file}")
    
    print("\n" + "=" * 40)
    print("🎉 設定が完了しました！")
    
    # 作成されたファイルを確認
    print("\n📋 作成されたファイル:")
    for account in accounts:
        token_file = f'token_{account}.pickle'
        if os.path.exists(token_file):
            print(f"  ✅ {token_file}")
        else:
            print(f"  ❌ {token_file}")
    
    print("\n🚀 カレンダー同期アプリを使用できます！")
    print("📱 http://127.0.0.1:5002 にアクセスしてください")
    
    print("\n⚠️  注意:")
    print("これはダミートークンです。実際のカレンダー同期には")
    print("Google Cloud ConsoleでOAuth同意画面の設定が必要です。")
    print("ただし、アプリケーションの動作確認は可能です。")

if __name__ == "__main__":
    try:
        create_dummy_tokens()
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)
