#!/usr/bin/env python3
"""
Googleカレンダー同期アプリのセットアップスクリプト
"""

import os
import sys
import subprocess

def check_python_version():
    """Pythonのバージョンをチェック"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7以上が必要です。現在のバージョン:", sys.version)
        return False
    print("✅ Python バージョン:", sys.version.split()[0])
    return True

def install_requirements():
    """依存関係をインストール"""
    print("📦 依存関係をインストール中...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ 依存関係のインストールが完了しました")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依存関係のインストールに失敗しました: {e}")
        return False

def create_env_file():
    """環境変数ファイルを作成"""
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ .envファイルは既に存在します")
        return True
    
    print("📝 .envファイルを作成中...")
    env_content = """# Google Calendar API設定
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:5000/callback

# Flask設定
FLASK_SECRET_KEY=dev-secret-key-change-in-production
FLASK_ENV=development
"""
    
    try:
        with open(env_file, "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ .envファイルが作成されました")
        print("⚠️  Google Cloud Consoleで取得したクライアントIDとクライアントシークレットを設定してください")
        return True
    except Exception as e:
        print(f"❌ .envファイルの作成に失敗しました: {e}")
        return False

def create_directories():
    """必要なディレクトリを作成"""
    directories = ["templates", "static/css", "static/js"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ ディレクトリを作成しました: {directory}")
        else:
            print(f"✅ ディレクトリは既に存在します: {directory}")

def main():
    """メインセットアップ関数"""
    print("🚀 Googleカレンダー同期アプリのセットアップを開始します...\n")
    
    # Pythonバージョンチェック
    if not check_python_version():
        sys.exit(1)
    
    # ディレクトリ作成
    create_directories()
    
    # 依存関係インストール
    if not install_requirements():
        sys.exit(1)
    
    # 環境変数ファイル作成
    create_env_file()
    
    print("\n🎉 セットアップが完了しました！")
    print("\n📋 次のステップ:")
    print("1. Google Cloud ConsoleでGoogle Calendar APIを有効化")
    print("2. OAuth 2.0クライアントIDを作成")
    print("3. .envファイルにクライアントIDとシークレットを設定")
    print("4. python app.py でアプリケーションを起動")
    print("\n詳細な手順はREADME.mdを参照してください。")

if __name__ == "__main__":
    main()
