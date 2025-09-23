#!/usr/bin/env python3
"""
自動Googleアカウント認証スクリプト
"""

import os
import sys
import time
from google_calendar_service import GoogleCalendarService

def main():
    """メイン関数"""
    print("🔐 Googleアカウント認証ツール（自動版）")
    print("=" * 50)
    
    print("\n🔧 設定確認:")
    print("  - ポート: 8080")
    print("  - リダイレクトURI: http://localhost:8080/")
    print("  - Google Cloud Consoleで上記URIが設定されていることを確認してください")
    
    accounts = [
        "ezasyo11@gmail.com",
        "syotaezaki@gmail.com"
    ]
    
    print(f"\n📋 認証するアカウント: {len(accounts)}個")
    for i, account in enumerate(accounts, 1):
        print(f"  {i}. {account}")
    
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
        print("🔐 認証手順:")
        print("  1. Googleの認証画面でログイン")
        print("  2. 権限を許可")
        print("  3. 認証完了を待つ")
        
        try:
            service = GoogleCalendarService()
            print(f"🚀 認証プロセスを開始...")
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
                
        except Exception as e:
            print(f"❌ エラーが発生しました: {e}")
            print("🔧 エラーの詳細:")
            print(f"   エラータイプ: {type(e).__name__}")
            print(f"   エラーメッセージ: {str(e)}")
            
            if "redirect_uri_mismatch" in str(e):
                print("\n🔧 解決方法:")
                print("1. Google Cloud Consoleにアクセス")
                print("2. APIとサービス → 認証情報")
                print("3. ウェブクライアント1を編集")
                print("4. 承認済みのリダイレクトURIに以下を追加:")
                print("   http://localhost:8080/")
                print("5. 保存")
                print("\n⚠️  設定を完了してから再実行してください")
                return False
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
        return True
    else:
        print("\n⚠️  認証されたアカウントがありません")
        print("🔧 トラブルシューティング:")
        print("  1. Google Cloud ConsoleでリダイレクトURIを確認")
        print("  2. インターネット接続を確認")
        print("  3. Googleアカウントの状態を確認")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  処理が中断されました")
    except Exception as e:
        print(f"\n❌ 予期しないエラーが発生しました: {e}")
        sys.exit(1)
