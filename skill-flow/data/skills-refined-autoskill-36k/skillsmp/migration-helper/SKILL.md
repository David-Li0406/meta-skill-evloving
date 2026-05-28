---
name: migration-helper
description: Assists in creating database migrations for Sagebase using Alembic. Activates when creating migration files, modifying database schema, or adding tables/columns/indexes. Ensures proper migration structure, rollback support, and Alembic best practices.
---

# Migration Helper (Alembic)

## Purpose
Alembicを使用したデータベースマイグレーションの作成を支援します。

## When to Activate
このスキルは以下の場合に自動的にアクティベートされます：
- 新しいマイグレーションファイルを作成する時
- データベーススキーマを変更する時
- テーブル、カラム、インデックス、制約を追加する時
- ユーザーが「migration」「schema」「database change」「マイグレーション」と言及した時
- ロールバックやマイグレーション履歴について質問された時

## 🚀 Quick Start

### 新しいマイグレーションを作成

```bash
# Docker環境内で作成（推奨）
just migrate-new "add_email_to_politicians"

# または直接Alembicコマンド
docker compose exec sagebase uv run alembic revision -m "add_email_to_politicians"
```

### マイグレーションを実行

```bash
# 未適用のマイグレーションを全て適用
just migrate

# 1つ前に戻す
just migrate-rollback
```

## ⚠️ CRITICAL: 必須チェックリスト

マイグレーション作成時に必ず確認：

- [ ] **upgrade() 実装**: スキーマ変更のSQLを記述
- [ ] **downgrade() 実装**: ロールバック用のSQLを記述（必須！）
- [ ] **冪等性確保**: `IF NOT EXISTS` / `IF EXISTS` を使用
- [ ] **テスト**: `just migrate` で適用確認
- [ ] **ロールバックテスト**: `just migrate-rollback` で戻せることを確認

## コマンドリファレンス

### justfile コマンド

| コマンド | 説明 |
|---------|------|
| `just migrate` | 未適用マイグレーションを全て適用 |
| `just migrate-rollback` | 1つ前の状態に戻す |
| `just migrate-current` | 現在適用されているバージョンを表示 |
| `just migrate-history` | マイグレーション履歴を表示 |
| `just migrate-new "説明"` | 新しいマイグレーションファイルを作成 |
| `just migrate-legacy` | レガシーSQL方式で実行（互換性用） |

### sagebase CLI コマンド

```bash
sagebase migrate              # マイグレーション実行
sagebase migrate-rollback     # ロールバック（-n オプションで複数可）
sagebase migrate-status       # 現在のバージョン確認
sagebase migrate-history      # 履歴確認
sagebase migrate-new "説明"   # 新規作成
```

### 直接 Alembic コマンド

```bash
# Docker内で実行
docker compose exec sagebase uv run alembic upgrade head
docker compose exec sagebase uv run alembic downgrade -1
docker compose exec sagebase uv run alembic current
docker compose exec sagebase uv run alembic history --verbose
docker compose exec sagebase uv run alembic revision -m "説明"
```

## マイグレーションファイル構造

```python
"""Add email column to politicians table.

Revision ID: 003
Revises: 002
Create Date: 2025-01-20
"""

from alembic import op


revision = "003"
down_revision = "002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Apply migration: Add email column."""
    op.execute("""
        ALTER TABLE politicians
        ADD COLUMN IF NOT EXISTS email VARCHAR(255);

        COMMENT ON COLUMN politicians.email IS 'Politician email address';

        CREATE INDEX IF NOT EXISTS idx_politicians_email
        ON politicians(email);
    """)


def downgrade() -> None:
    """Rollback migration: Remove email column."""
    op.execute("""
        DROP INDEX IF EXISTS idx_politicians_email;

        ALTER TABLE politicians
        DROP COLUMN IF EXISTS email;
    """)
```

## 基本パターン

### カラム追加

```python
def upgrade() -> None:
    op.execute("""
        ALTER TABLE table_name
        ADD COLUMN IF NOT EXISTS column_name VARCHAR(255);
    """)

def downgrade() -> None:
    op.execute("""
        ALTER TABLE table_name
        DROP COLUMN IF EXISTS column_name;
    """)
```

### テーブル作成

```python
def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS new_table (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

def downgrade() -> None:
    op.execute("""
        DROP TABLE IF EXISTS new_table;
    """)
```

### インデックス追加

```python
def upgrade() -> None:
    op.execute("""
        CREATE INDEX IF NOT EXISTS idx_table_column
        ON table_name(column_name);
    """)

def downgrade() -> None:
    op.execute("""
        DROP INDEX IF EXISTS idx_table_column;
    """)
```

## 詳細リファレンス

- [examples.md](examples.md) - 実践的なマイグレーション例
- [reference.md](reference.md) - 詳細なパターンとベストプラクティス

## レガシーマイグレーションについて

既存の `database/migrations/` 配下の45個のSQLファイルは履歴として保持されています。
**新規マイグレーションは必ずAlembicを使用してください。**

`just migrate-legacy` は互換性のために残されていますが、通常は使用しません。
