import json
from datetime import datetime, timedelta
from google_calendar_service import GoogleCalendarService

class CalendarSync:
    def __init__(self):
        self.services = {}  # ユーザーIDごとのGoogleCalendarServiceを保存
        
    def add_user(self, user_id):
        """新しいユーザーを追加"""
        service = GoogleCalendarService()
        if service.authenticate(user_id):
            self.services[user_id] = service
            return True
        return False
    
    def sync_event_to_all_accounts(self, source_user_id, event_data, exclude_user_id=None):
        """1つのアカウントのイベントを他の全アカウントに同期"""
        synced_events = []
        
        for user_id, service in self.services.items():
            if user_id == source_user_id or user_id == exclude_user_id:
                continue
                
            try:
                # イベントを他のアカウントに作成
                created_event = service.create_event('primary', event_data)
                if created_event:
                    synced_events.append({
                        'user_id': user_id,
                        'event_id': created_event['id'],
                        'event': created_event
                    })
            except Exception as e:
                print(f"ユーザー {user_id} への同期でエラー: {e}")
                
        return synced_events
    
    def sync_event_update_to_all_accounts(self, source_user_id, event_id, event_data, exclude_user_id=None):
        """1つのアカウントのイベント更新を他の全アカウントに同期"""
        updated_events = []
        
        for user_id, service in self.services.items():
            if user_id == source_user_id or user_id == exclude_user_id:
                continue
                
            try:
                # 同期されたイベントを検索して更新
                events = service.get_events()
                for event in events:
                    # 元のイベントIDまたはタイトルでマッチング
                    if (event.get('id') == event_id or 
                        event.get('summary') == event_data.get('summary')):
                        
                        updated_event = service.update_event('primary', event['id'], event_data)
                        if updated_event:
                            updated_events.append({
                                'user_id': user_id,
                                'event_id': updated_event['id'],
                                'event': updated_event
                            })
                        break
            except Exception as e:
                print(f"ユーザー {user_id} の更新でエラー: {e}")
                
        return updated_events
    
    def sync_event_deletion_to_all_accounts(self, source_user_id, event_id, event_title=None, exclude_user_id=None):
        """1つのアカウントのイベント削除を他の全アカウントに同期"""
        deleted_events = []
        
        for user_id, service in self.services.items():
            if user_id == source_user_id or user_id == exclude_user_id:
                continue
                
            try:
                # 同期されたイベントを検索して削除
                events = service.get_events()
                for event in events:
                    # 元のイベントIDまたはタイトルでマッチング
                    if (event.get('id') == event_id or 
                        (event_title and event.get('summary') == event_title)):
                        
                        if service.delete_event('primary', event['id']):
                            deleted_events.append({
                                'user_id': user_id,
                                'event_id': event['id']
                            })
                        break
            except Exception as e:
                print(f"ユーザー {user_id} の削除でエラー: {e}")
                
        return deleted_events
    
    def get_all_events(self):
        """全アカウントのイベントを取得"""
        all_events = {}
        
        for user_id, service in self.services.items():
            try:
                events = service.get_events()
                all_events[user_id] = events
            except Exception as e:
                print(f"ユーザー {user_id} のイベント取得でエラー: {e}")
                all_events[user_id] = []
                
        return all_events
    
    def remove_user(self, user_id):
        """ユーザーを削除"""
        if user_id in self.services:
            del self.services[user_id]
            return True
        return False
