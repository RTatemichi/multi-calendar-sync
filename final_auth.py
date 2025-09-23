#!/usr/bin/env python3
"""
最終的なGoogleアカウント認証スクリプト
"""

import os
import sys
import time
from google_calendar_service import GoogleCalendarService

def main():
    """メイン関数"""
    print("🎯 Googleアカウント認証ツール（最終版）")
    print("=" * 50)
    
    accounts = [
        "ezasyo11@gmail.com",
        "syotaezaki@gmail.com"
    ]
    
    print("\n📋 認証するアカウント:")
    for i, account in enumerate(accounts, 1):
        print(f"  {i}. {account}")
    
    print("\n🔧 設定確認:")
    print("  - ポート: 8080")
    print("  - リダイレクトURI: http://localhost:8080/")
    print("  - Google Cloud Consoleで上記URIが設定されていることを確認してください")
    
    print("\n" + "=" * 50)
    
    for i, account in enumerate(accounts, 1):
        print(f"\n📧 アカウント {i}/{len(accounts)}: {account}")
        print("-" * 40)
        
        # 既に認証済みかチェック
        token_file = f'token_{account}.pickle'
        if os.path.exists(token_file):
            print(f"✅ {account} は既に認証済みです")
            continue
        
        print(f"🔑 {account} の認証を開始します...")
        print("📱 ブラウザが自動で開きます...")
        print("🔐 Googleの認証画面でログインして権限を許可してください")
        
        try:
            service = GoogleCalendarService()
            success = service.authenticate(account)
            
            if success:
                print(f"✅ {account} の認証が完了しました！")
                
                # トークンファイルの確認
                if os.path.exists(token_file):
                    print(f"📄 トークンファイルが作成されました: {token_file}")
                else:
                    print(f"⚠️  トークンファイルが見つかりません: {token_file}")
                    
            else:
                print(f"❌ {account} の認証に失敗しました")
                print("🔧 以下の点を確認してください:")
                print("   1. Google Cloud Consoleで http://localhost:8080/ が設定されているか")
                print("   2. インターネット接続が正常か")
                print("   3. Googleアカウントでログインできているか")
                
                retry = input("\n再試行しますか？ (y/n): ").lower().strip()
                if retry == 'y':
                    print(f"🔄 {account} の認証を再試行します...")
                    success = service.authenticate(account)
                    if success:
                        print(f"✅ {account} の認証が完了しました！")
                    else:
                        print(f"❌ {account} の認証をスキップします")
                else:
                    print(f"⏭️  {account} をスキップします")
                    
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            print("🔧 エラーの詳細:")
            print(f"   エラータイプ: {type(e).__name__}")
            print(f"   エラーメッセージ: {str(e)}")
            
            retry = input("\n再試行しますか？ (y/n): ").lower().strip()
            if retry == 'y':
                try:
                    success = service.authenticate(account)
                    if success:
                        print(f"✅ {account} の認証が完了しました！")
                    else:
                        print(f"❌ {account} の認証をスキップします")
                except Exception as e2:
                    print(f"❌ 再試行でもエラーが発生しました: {e2}")
            else:
                print(f"⏭️  {account} をスキップします")
        
        # 次のアカウントの前に少し待機
        if i < len(accounts):
            print("\n⏳ 次のアカウントの認証まで3秒待機...")
            time.sleep(3)
    
    print("\n" + "=" * 50)
    print("🎉 認証処理が完了しました！")
    
    # 認証結果の確認
    print("\n📋 認証結果:")
    authenticated_count = 0
    for account in accounts:
        token_file = f'token_{account}.pickle'
        if os.path.exists(token_file):
            print(f"  ✅ {account}")
            authenticated_count += 1
        else:
            print(f"  ❌ {account}")
    
    print(f"\n認証済みアカウント数: {authenticated_count}/{len(accounts)}")
    
    if authenticated_count > 0:
        print("\n🚀 カレンダー同期アプリを使用できます！")
        print("📱 http://127.0.0.1:5002 にアクセスしてください")
        
        print("\n🔧 次のステップ:")
        print("  1. ブラウザで http://127.0.0.1:5002 にアクセス")
        print("  2. 認証されたアカウントが表示されることを確認")
        print("  3. 予定を作成・編集・削除して同期をテスト")
    else:
        print("\n⚠️  認証されたアカウントがありません")
        print("🔧 トラブルシューティング:")
        print("  1. Google Cloud ConsoleでリダイレクトURIを確認")
        print("  2. インターネット接続を確認")
        print("  3. Googleアカウントの状態を確認")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️  処理が中断されました")
    except Exception as e:
        print(f"\n❌ 予期しないエラーが発生しました: {e}")
        sys.exit(1)
