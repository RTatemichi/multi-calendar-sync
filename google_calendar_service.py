import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import Config

class GoogleCalendarService:
    def __init__(self):
        self.scopes = Config.SCOPES
        self.credentials = None
        self.service = None
        
    def authenticate(self, user_id):
        """Google Calendar API認証を実行"""
        creds = None
        token_file = f'token_{user_id}.pickle'
        
        # 既存のトークンファイルがあるかチェック
        if os.path.exists(token_file):
            with open(token_file, 'rb') as token:
                creds = pickle.load(token)
        
        # トークンが無効または存在しない場合、再認証
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                # クライアントシークレットファイルが必要
                # 実際の使用時は、Google Cloud Consoleで作成したクライアントシークレットファイルを使用
                flow = InstalledAppFlow.from_client_config(
                    {
                        "web": {
                            "client_id": Config.GOOGLE_CLIENT_ID,
                            "client_secret": Config.GOOGLE_CLIENT_SECRET,
                            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                            "token_uri": "https://oauth2.googleapis.com/token",
                            "redirect_uris": [Config.GOOGLE_REDIRECT_URI]
                        }
                    },
                    self.scopes
                )
                creds = flow.run_local_server(port=0)
            
            # トークンを保存
            with open(token_file, 'wb') as token:
                pickle.dump(creds, token)
        
        self.credentials = creds
        self.service = build('calendar', 'v3', credentials=creds)
        return True
    
    def get_calendars(self):
        """カレンダー一覧を取得"""
        if not self.service:
            return []
        
        calendar_list = self.service.calendarList().list().execute()
        return calendar_list.get('items', [])
    
    def get_events(self, calendar_id='primary', max_results=100):
        """指定されたカレンダーのイベントを取得"""
        if not self.service:
            return []
        
        events_result = self.service.events().list(
            calendarId=calendar_id,
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        return events_result.get('items', [])
    
    def create_event(self, calendar_id, event_data):
        """新しいイベントを作成"""
        if not self.service:
            return None
        
        event = self.service.events().insert(
            calendarId=calendar_id,
            body=event_data
        ).execute()
        
        return event
    
    def update_event(self, calendar_id, event_id, event_data):
        """既存のイベントを更新"""
        if not self.service:
            return None
        
        event = self.service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=event_data
        ).execute()
        
        return event
    
    def delete_event(self, calendar_id, event_id):
        """イベントを削除"""
        if not self.service:
            return False
        
        self.service.events().delete(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        
        return True
