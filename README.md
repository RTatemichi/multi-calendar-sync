# Googleカレンダー同期アプリ

複数のGoogleアカウント間で予定を自動同期するWebアプリケーションです。1つのアカウントで予定を追加・編集・削除すると、他のアカウントにも自動的に反映されます。

## 機能

- 🔐 複数のGoogleアカウント認証
- 📅 予定の追加・編集・削除
- 🔄 リアルタイム同期
- 🎨 モダンで使いやすいWebインターフェース
- 📱 レスポンシブデザイン

## 必要な環境

- Python 3.7以上
- Google Cloud Console アカウント
- 複数のGoogleアカウント

## セットアップ手順

### 1. プロジェクトのクローンと依存関係のインストール

```bash
# プロジェクトディレクトリに移動
cd /Users/shotaezaki/Desktop/test

# 依存関係をインストール
pip install -r requirements.txt
```

### 2. Google Cloud Console での設定

1. [Google Cloud Console](https://console.cloud.google.com/) にアクセス
2. 新しいプロジェクトを作成または既存のプロジェクトを選択
3. 「APIとサービス」→「ライブラリ」で「Google Calendar API」を有効化
4. 「APIとサービス」→「認証情報」で「認証情報を作成」→「OAuth 2.0 クライアント ID」
5. アプリケーションの種類を「ウェブアプリケーション」に設定
6. 承認済みのリダイレクト URI に `http://localhost:5000/callback` を追加
7. クライアント ID とクライアントシークレットを取得

### 3. 環境変数の設定

`.env` ファイルを作成し、以下の内容を設定してください：

```env
# Google Calendar API設定
GOOGLE_CLIENT_ID=your_google_client_id_here
GOOGLE_CLIENT_SECRET=your_google_client_secret_here
GOOGLE_REDIRECT_URI=http://localhost:5000/callback

# Flask設定
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
```

**重要**: `your_google_client_id_here` と `your_google_client_secret_here` を実際の値に置き換えてください。

### 4. アプリケーションの起動

```bash
python app.py
```

ブラウザで `http://localhost:5000` にアクセスしてアプリケーションを使用できます。

## 使用方法

### 1. アカウントの追加

1. 左サイドバーの「アカウント管理」セクションで、ユーザーIDを入力
2. 「追加」ボタンをクリック
3. ブラウザが開き、Googleアカウントの認証画面が表示されます
4. 同期したいGoogleアカウントでログインし、権限を許可
5. 認証が完了すると、アカウントが追加されます

### 2. イベントの作成

1. 左サイドバーの「イベント作成」セクションで以下を入力：
   - タイトル（必須）
   - 説明（任意）
   - 開始時刻（必須）
   - 終了時刻（必須）
   - アカウント（必須）
2. 「イベント作成」ボタンをクリック
3. 指定したアカウントにイベントが作成され、他のアカウントにも自動同期されます

### 3. イベントの編集・削除

1. メイン画面のイベント一覧から、編集または削除したいイベントを選択
2. 「編集」ボタンでイベントの詳細を変更
3. 「削除」ボタンでイベントを削除
4. 変更は他のアカウントにも自動的に反映されます

## ファイル構成

```
test/
├── app.py                      # メインのFlaskアプリケーション
├── config.py                   # 設定ファイル
├── google_calendar_service.py  # Google Calendar API連携
├── calendar_sync.py            # カレンダー同期ロジック
├── requirements.txt            # Python依存関係
├── README.md                   # このファイル
├── templates/
│   └── index.html             # メインのHTMLテンプレート
└── static/
    ├── css/
    │   └── style.css          # カスタムスタイル
    └── js/
        └── app.js             # フロントエンドJavaScript
```

## トラブルシューティング

### 認証エラーが発生する場合

1. Google Cloud Console でAPIが有効化されているか確認
2. リダイレクト URI が正しく設定されているか確認
3. クライアント ID とクライアントシークレットが正しいか確認

### イベントが同期されない場合

1. 各アカウントが正しく認証されているか確認
2. インターネット接続を確認
3. ブラウザのコンソールでエラーメッセージを確認

### アプリケーションが起動しない場合

1. Python のバージョンが 3.7 以上か確認
2. 依存関係が正しくインストールされているか確認
3. ポート 5000 が他のアプリケーションで使用されていないか確認

## セキュリティに関する注意事項

- `.env` ファイルには機密情報が含まれているため、Gitにコミットしないでください
- 本番環境では、強力な `FLASK_SECRET_KEY` を設定してください
- Google Cloud Console で適切な権限設定を行ってください

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## サポート

問題が発生した場合は、以下の手順で対処してください：

1. エラーメッセージを確認
2. ログファイルをチェック
3. 必要に応じて開発者に連絡

---

**注意**: このアプリケーションは教育目的で作成されています。本番環境で使用する場合は、セキュリティとパフォーマンスの観点から追加の検討が必要です。
