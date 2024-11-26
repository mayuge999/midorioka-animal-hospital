# みどりおか動物病院 Webサイト

## 概要
緑を基調とした清潔感のある架空の動物病院のWebサイトです。予約システムを備え、飼い主様が簡単に診療予約を行えます。

## 主な機能
- オンライン予約システム
- 診療案内・料金表
- お問い合わせフォーム
- 管理者ダッシュボード（予約管理・お問い合わせ管理）

## 技術スタック
Python 3.11, Flask, PostgreSQL, Bootstrap 5, FullCalendar

## セットアップ
リポジトリのクローン: git clone https://github.com/mayuge999/midorioka-animal-hospital.git  
依存パッケージのインストール: pip install -r requirements.txt  
環境変数の設定: DATABASE_URL（PostgreSQLデータベースのURL）, FLASK_SECRET_KEY（Flaskアプリケーションのシークレットキー）, ADMIN_USERNAME（管理者アカウントのユーザー名, オプション）, ADMIN_PASSWORD（管理者アカウントのパスワード, オプション）  
データベースの初期化: flask db init → flask db migrate -m "初期設定" → flask db upgrade  
管理者アカウントの作成: python create_admin.py 初期認証情報（ユーザー名: admin, パスワード: admin123）

## 起動方法
python main.py  
サーバーは http://localhost:5000 で起動します。

## データベース
マイグレーション: flask db init → flask db migrate -m "変更の説明" → flask db upgrade  
バックアップとリストア: pg_dump -U $PGUSER -h $PGHOST $PGDATABASE > backup.sql → psql -U $PGUSER -h $PGHOST $PGDATABASE < backup.sql

## 開発環境
必要なソフトウェア: Python 3.11以上, PostgreSQL 14以上, Node.js 18以上（フロントエンド開発用）  
推奨開発ツール: VSCode, Python拡張機能, SQLTools拡張機能, Prettier拡張機能, pgAdmin 4（データベース管理）, Postman（API開発・テスト）

## プロジェクト構造
.  
├── static/ # 静的ファイル（CSS, JavaScript, 画像）  
│   ├── css/ # スタイルシート  
│   └── js/ # JavaScriptファイル  
├── templates/ # HTMLテンプレート  
│   └── admin/ # 管理画面テンプレート  
├── app.py # メインアプリケーション  
├── models.py # データベースモデル  
├── forms.py # フォーム定義  
├── create_admin.py # 管理者アカウント作成スクリプト  
└── main.py # アプリケーション起動スクリプト

## トラブルシューティング
アプリケーションが起動しない場合: 環境変数の確認、依存パッケージの再インストール（pip install -r requirements.txt）、ログファイルの確認  
予約システムのエラー: タイムゾーン設定の確認、データベース接続の確認、予約枠の重複チェック  
データベース接続エラー: DATABASE_URLの形式確認、PostgreSQLサービスの起動確認、ファイアウォール設定の確認  
マイグレーションエラー: alembic_versionテーブルの確認、マイグレーションファイルの競合解決、データベーススキーマの手動修正

## テスト
テスト環境のセットアップ: pip install pytest pytest-flask pytest-cov → createdb midorioka_test → 環境変数の設定（export TESTING=True, export DATABASE_URL=postgresql://localhost/midorioka_test）  
テストの実行: pytest（全テスト実行）, pytest --cov=app tests/（カバレッジレポート生成）, pytest tests/test_appointments.py（特定のテストファイル実行）  
テストカテゴリー: ユニットテスト、統合テスト、エンドツーエンドテスト

## 管理者ダッシュボードアクセス方法
ホームサイトのURL末尾に /admin を追加してアクセスしてください。
