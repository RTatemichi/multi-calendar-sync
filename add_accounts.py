#!/usr/bin/env python3
"""
Googleアカウントを自動で追加するスクリプト
"""

from calendar_sync import CalendarSync
import sys

def add_accounts():
    """指定されたGoogleアカウントを追加"""
    
    # カレンダー同期インスタンスを作成
    calendar_sync = CalendarSync()
    
    # 追加するアカウントのリスト
    accounts = [
        "ezasyo11@gmail.com",
        "syotaezaki@gmail.com"
    ]
    
    print("Googleアカウントの追加を開始します...")
    
    for account in accounts:
        print(f"\nアカウント追加中: {account}")
        
        try:
            # アカウントを追加
            success = calendar_sync.add_user(account)
            
            if success:
                print(f"✅ {account} の追加が完了しました")
            else:
                print(f"❌ {account} の追加に失敗しました")
                
        except Exception as e:
            print(f"❌ {account} の追加でエラーが発生しました: {e}")
    
    print(f"\n追加されたアカウント数: {len(calendar_sync.services)}")
    print("追加されたアカウント:")
    for account in calendar_sync.services.keys():
        print(f"  - {account}")
    
    return calendar_sync

if __name__ == "__main__":
    try:
        calendar_sync = add_accounts()
        print("\n🎉 アカウント追加処理が完了しました！")
    except KeyboardInterrupt:
        print("\n⏹️  処理が中断されました")
    except Exception as e:
        print(f"\n❌ エラーが発生しました: {e}")
        sys.exit(1)