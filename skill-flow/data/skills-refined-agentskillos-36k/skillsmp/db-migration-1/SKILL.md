---
name: db-migration
description: |
  Alembic を使用した DB マイグレーション管理スキル。
  スキーマ変更、履歴管理、ロールバックの標準手順を提供。
version: 1.0.0
author: agentflow-team
triggers:
  - マイグレーション
  - DB スキーマ変更
  - Alembic
  - テーブル追加
  - カラム変更
  - データベース変更
requirements:
  - alembic
  - sqlalchemy
  - psycopg2-binary
tags:
  - database
  - migration
  - alembic
  - postgresql
---

# DB マイグレーション管理スキル (Alembic)

## なぜ Alembic か

| ツール | 言語 | 特徴 |
|--------|------|------|
| **Alembic** | Python | SQLAlchemy 公式、autogenerate 対応 ✅ |
| Flyway | Java | SQL ベース、多言語対応 |
| Liquibase | Java | XML/YAML/SQL、エンタープライズ向け |
| Atlas | Go | 宣言型、クラウドネイティブ |

**選定理由**: Python + SQLAlchemy プロジェクトでは Alembic が最適。

## セットアップ

### 初期化
```bash
cd apps/my_app
alembic init migrations
```

### alembic.ini 設定
```ini
# 接続 URL（psycopg2 使用 - Alembic は同期ドライバのみ）
sqlalchemy.url = postgresql+psycopg2://user:pass@localhost:5432/dbname

# ファイル命名規則
file_template = %%(year)d%%(month).2d%%(day).2d_%%(rev)s_%%(slug)s
```

### env.py 設定
```python
# モデルのインポート
from repositories.models import Base
target_metadata = Base.metadata

# asyncpg → psycopg2 変換
def get_url():
    url = config.get_main_option("sqlalchemy.url", "")
    return url.replace("+asyncpg", "+psycopg2")
```

## 基本操作

### 新規マイグレーション作成

```bash
# モデルから自動生成（推奨）
alembic revision --autogenerate -m "add_users_table"

# 空のマイグレーション作成
alembic revision -m "manual_changes"
```

### マイグレーション適用

```bash
# 最新まで適用
alembic upgrade head

# 特定バージョンまで適用
alembic upgrade abc123

# 1つ進める
alembic upgrade +1
```

### ロールバック

```bash
# 1つ戻す
alembic downgrade -1

# 特定バージョンまで戻す
alembic downgrade abc123

# 全て戻す（初期状態）
alembic downgrade base
```

### 履歴確認

```bash
# 履歴一覧
alembic history

# 現在バージョン
alembic current

# 詳細表示
alembic history --verbose
```

## マイグレーションファイル例

```python
"""add_users_table

Revision ID: 0001
Create Date: 2026-01-18
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001'
down_revision = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP')),
    )
    op.create_index('idx_users_email', 'users', ['email'])


def downgrade() -> None:
    op.drop_index('idx_users_email', 'users')
    op.drop_table('users')
```

## よくある操作

### カラム追加
```python
op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))
```

### カラム削除
```python
op.drop_column('users', 'phone')
```

### インデックス追加
```python
op.create_index('idx_users_name', 'users', ['name'])
```

### 外部キー追加
```python
op.create_foreign_key(
    'fk_orders_user_id',
    'orders', 'users',
    ['user_id'], ['id'],
    ondelete='CASCADE'
)
```

## トラブルシューティング

### 接続エラー
```
OperationalError: unable to open database file
```
→ DB コンテナが起動していない。`docker-compose up -d postgres-main`

### autogenerate が空
→ `env.py` で `target_metadata = Base.metadata` を設定

### マイグレーション競合
```bash
alembic merge -m "merge_heads" head1 head2
```

## ベストプラクティス

1. **小さく頻繁に**: 大きな変更は分割
2. **downgrade 必須**: ロールバック可能に
3. **レビュー**: autogenerate 結果を必ず確認
4. **テスト**: CI でマイグレーション実行テスト
5. **バックアップ**: 本番適用前に DB バックアップ

