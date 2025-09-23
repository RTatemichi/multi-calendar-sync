#!/usr/bin/env python3
"""
簡単なGoogleアカウント認証スクリプト
"""

import os
import sys
import time
from google_calendar_service import GoogleCalendarService

def authenticate_accounts():
    """指定されたアカウントを自動認証"""
    
    accounts = [
        "ezasyo11@gmail.com",
        "syotaezaki@gmail.com"
    ]
    
    print("🔐 Googleアカウントの自動認証を開始します...")
    print("=" * 50)
    
    for i, account in enumerate(accounts, 1):
        print(f"\n📧 アカウント {i}/{len(accounts)}: {account}")
        print("-" * 30)
        
        try:
            # GoogleCalendarServiceインスタンスを作成
            service = GoogleCalendarService()
            
            # 認証を実行
            print(f"🔑 {account} の認証を開始...")
            success = service.authenticate(account)
            
            if success:
                print(f"✅ {account} の認証が完了しました！")
                
                # トークンファイルの存在確認
                token_file = f'token_{account}.pickle'
                if os.path.exists(token_file):
                    print(f"📄 トークンファイルが作成されました: {token_file}")
                else:
                    print(f"⚠️  トークンファイルが見つかりません: {token_file}")
                    
            else:
                print(f"❌ {account} の認証に失敗しました")
                
        except Exception as e:
            print(f"❌ {account} の認証でエラーが発生しました: {e}")
            
        # 次のアカウントの前に少し待機
        if i < len(accounts):
            print("⏳ 次のアカウントの認証まで5秒待機...")
            time.sleep(5)
    
    print("\n" + "=" * 50)
    print("🎉 認証処理が完了しました！")
    
    # 作成されたトークンファイルを確認
    print("\n📋 作成されたトークンファイル:")
    token_files = [f for f in os.listdir('.') if f.startswith('token_') and f.endswith('.pickle')]
    if token_files:
        for token_file in token_files:
            print(f"  ✅ {token_file}")
    else:
        print("  ❌ トークンファイルが見つかりません")

if __name__ == "__main__":
    try:
        authenticate_accounts()
    except KeyboardInterrupt:
        print("\n⏹️  処理が中断されました")
    except Exception as e:
        print(f"\n❌ 予期しないエラーが発生しました: {e}")
        sys.exit(1)