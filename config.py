import os
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

class Config:
    # Google Calendar API設定
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:5000/callback')
    
    # Flask設定
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # スコープ設定（カレンダーの読み書き権限）
    SCOPES = ['https://www.googleapis.com/auth/calendar']
