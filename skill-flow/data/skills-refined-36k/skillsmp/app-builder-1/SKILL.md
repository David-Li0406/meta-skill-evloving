---
name: app-builder
description: |
  新規 App 基盤構築スキル。
  FastAPI + PostgreSQL + Redis + Alembic + React の完全な App 骨架を自動生成。
  ユーザーの要件に基づいてカスタマイズ可能。
version: 1.0.0
author: agentflow-team
triggers:
  - 新規アプリ作成
  - App 構築
  - 基盤作成
  - scaffold
  - テンプレート生成
  - プロジェクト初期化
requirements:
  - jinja2
  - pyyaml
  - pydantic
tags:
  - scaffolding
  - fullstack
  - docker
  - database
  - alembic
---

# App 基盤構築スキル

このスキルは新規 App の初期骨架を自動生成します。

## 構築フロー（標準手順）

### フェーズ 1: 基盤做成（Foundation）

1. **要件確認**
   - アプリ名（snake_case）
   - 表示タイトル
   - 説明文
   - DB 名
   - Redis 必要可否
   - 履歴 DB 必要可否

2. **テンプレート適用**
   ```bash
   # agentflow CLI でテンプレート生成
   python -m agentflow.cli new-app \
     --template fullstack-app \
     --name my_app \
     --title "My Application" \
     --output apps/my_app
   ```

3. **ポート自動設定（重要）**
   ```bash
   # ポート衝突を自動回避
   python -m agentflow.tools.port_manager my_app apps/my_app

   # 結果: .env ファイルが自動生成される
   # DB_MAIN_PORT=5432 (or 次の空きポート)
   # DB_HISTORY_PORT=5434
   # REDIS_PORT=6379
   # API_PORT=8000 (or 8001, 8002...)
   # FRONTEND_PORT=3000
   ```

4. **ディレクトリ構造確認**
   ```
   apps/my_app/
   ├── .env                    # ポート・認証情報（Git 除外）
   ├── .env.example            # 設定テンプレート
   ├── docker-compose.yml      # コンテナ構成
   ├── Dockerfile              # API コンテナ
   ├── alembic.ini             # DB マイグレーション
   ├── api.py                  # FastAPI エントリ
   ├── config/                 # 設定
   │   ├── __init__.py
   │   └── settings.yaml
   ├── db/init/                # 初期 SQL
   ├── migrations/             # Alembic
   ├── repositories/           # データアクセス層
   ├── routers/                # API ルーター
   ├── schemas/                # Pydantic スキーマ
   ├── services/               # ビジネスロジック
   └── tests/                  # テスト
   ```

### フェーズ 2: 式様読取・設計（Design）

1. **要件分析**
   - ユーザーストーリー抽出
   - エンティティ特定
   - API エンドポイント設計

2. **DB スキーマ設計**
   - `repositories/models.py` にモデル追加
   - `db/init/01_schema.sql` を更新

3. **API 設計**
   - `routers/` に機能別ルーター追加
   - `schemas/` にリクエスト/レスポンススキーマ追加

### フェーズ 3: 実装・テスト（Implementation）

1. **DB マイグレーション**
   ```bash
   cd apps/my_app
   docker-compose up -d postgres-main redis
   alembic revision --autogenerate -m "add_entities"
   alembic upgrade head
   ```

2. **サービス層実装**
   - `services/` にビジネスロジック追加

3. **テスト作成・実行**
   ```bash
   pytest tests/ -v
   ```

4. **ループ**: テスト失敗 → 修正 → 再テスト

## ベストプラクティス

### DB マイグレーション (Alembic)

```bash
# 新規マイグレーション作成
alembic revision --autogenerate -m "説明"

# マイグレーション適用
alembic upgrade head

# ロールバック
alembic downgrade -1

# 履歴確認
alembic history
```

### Docker 操作

```bash
# コンテナ起動
docker-compose up -d

# DB のみ起動
docker-compose up -d postgres-main redis

# ログ確認
docker-compose logs -f api

# 停止・削除
docker-compose down -v
```

### 設定管理（環境統一）

```
.env ファイル構成:
├── APP_ENV          # development / staging / production
├── HOST             # localhost / IP / ドメイン
├── DB_MAIN_PORT     # PostgreSQL メイン
├── DB_HISTORY_PORT  # PostgreSQL 履歴
├── REDIS_PORT       # Redis
├── API_PORT         # FastAPI
├── FRONTEND_PORT    # React/Next.js
└── VITE_API_URL     # フロントエンドから API への URL
```

- 機密情報は `.env` で管理（Git 除外）
- アプリ設定は `config/settings.yaml`
- 環境変数でオーバーライド可能
- **ポート衝突時**: `python -m agentflow.tools.port_manager` で自動解決

### ホスト設定（開発/本番統一）

| 環境 | HOST 設定 | 備考 |
|------|-----------|------|
| 開発（ローカル） | `localhost` | 127.0.0.1 も可 |
| Docker 内から | `host.docker.internal` | ホスト側サービスへ |
| 本番 | 実際の IP/ドメイン | 外部公開 |

## チェックリスト

- [ ] `.env` ファイルが作成されている（ポート設定済み）
- [ ] docker-compose.yml が正しく設定されている
- [ ] alembic.ini の DB URL が正しい
- [ ] models.py にエンティティが定義されている
- [ ] 初回マイグレーションが作成されている
- [ ] ヘルスチェックエンドポイントが動作する
- [ ] テストが実行可能
- [ ] 他の App とポートが衝突していない

