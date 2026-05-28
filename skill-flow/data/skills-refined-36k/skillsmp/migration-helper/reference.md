# Alembic Migration Reference

Sagebaseのデータベースマイグレーションに関する詳細リファレンスです。

## マイグレーションシステムの概要

### ディレクトリ構造

```
alembic/
├── versions/              # マイグレーションファイル
│   ├── 001_baseline.py    # ベースライン（既存スキーマ）
│   ├── 002_example.py     # サンプル
│   └── 003_xxx.py         # 新規マイグレーション
├── env.py                 # 環境設定
├── script.py.mako         # テンプレート
└── README

alembic.ini                # Alembic設定ファイル

database/                  # レガシーファイル（参照用）
├── init.sql              # 初期スキーマ
├── migrations/           # 旧マイグレーション（45個）
└── 02_run_migrations.sql # 旧実行スクリプト
```

### バージョン管理

Alembicは `alembic_version` テーブルで適用済みマイグレーションを追跡します：

```sql
-- Alembicが自動作成
CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
```

## コマンドリファレンス

### マイグレーション実行

```bash
# 全ての未適用マイグレーションを適用
just migrate
# または
docker compose exec sagebase uv run alembic upgrade head

# 特定バージョンまで適用
docker compose exec sagebase uv run alembic upgrade 003

# 相対的に進める（現在+2）
docker compose exec sagebase uv run alembic upgrade +2
```

### ロールバック

```bash
# 1つ前に戻す
just migrate-rollback
# または
docker compose exec sagebase uv run alembic downgrade -1

# 特定バージョンまで戻す
docker compose exec sagebase uv run alembic downgrade 002

# ベースラインまで戻す（注意！）
docker compose exec sagebase uv run alembic downgrade 001
```

### 状態確認

```bash
# 現在のバージョン
just migrate-current
# または
docker compose exec sagebase uv run alembic current

# 履歴表示
just migrate-history
# または
docker compose exec sagebase uv run alembic history --verbose

# 未適用マイグレーション確認
docker compose exec sagebase uv run alembic heads
```

### 新規マイグレーション作成

```bash
# 新しいマイグレーションファイルを作成
just migrate-new "add_email_to_politicians"
# または
docker compose exec sagebase uv run alembic revision -m "add_email_to_politicians"
```

## データベース設計概要

### マスターデータ

シードファイルで事前に投入される固定データ：

| テーブル | 説明 |
|---------|------|
| `governing_bodies` | 統治組織（国、都道府県、市町村） |
| `conferences` | 会議体（国会、地方議会、委員会） |
| `political_parties` | 政党マスターデータ |

### コアテーブル

| テーブル | 説明 |
|---------|------|
| `meetings` | 個別の会議セッション |
| `minutes` | 議事録 |
| `speakers` | 発言者 |
| `politicians` | 政治家情報 |
| `conversations` | 発言内容 |
| `proposals` | 議案 |
| `parliamentary_groups` | 議員団/会派 |
| `parliamentary_group_memberships` | 議員団メンバーシップ |

### 抽出・ステージングテーブル

| テーブル | 説明 |
|---------|------|
| `extracted_conference_members` | 会議メンバー抽出結果 |
| `extracted_parliamentary_group_members` | 議員団メンバー抽出結果 |
| `extraction_logs` | 抽出処理ログ |

## 詳細パターン

### テーブル作成

```python
def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS table_name (
            -- 主キー
            id SERIAL PRIMARY KEY,

            -- 必須フィールド
            name VARCHAR(255) NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'pending',

            -- オプションフィールド
            description TEXT,
            metadata JSONB,

            -- タイムスタンプ
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        -- コメント
        COMMENT ON TABLE table_name IS 'テーブルの説明';
        COMMENT ON COLUMN table_name.status IS 'ステータス: pending, active, inactive';
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS table_name;")
```

### 外部キー付きテーブル

```python
def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS child_table (
            id SERIAL PRIMARY KEY,
            parent_id INTEGER NOT NULL,
            name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

            -- 外部キー制約
            CONSTRAINT fk_child_parent
                FOREIGN KEY (parent_id)
                REFERENCES parent_table(id)
                ON DELETE CASCADE
        );

        -- 外部キーインデックス（必須！）
        CREATE INDEX IF NOT EXISTS idx_child_parent_id
            ON child_table(parent_id);
    """)


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS child_table;")
```

### カラム追加

```python
def upgrade() -> None:
    op.execute("""
        ALTER TABLE table_name
        ADD COLUMN IF NOT EXISTS column_name VARCHAR(255);

        COMMENT ON COLUMN table_name.column_name IS 'カラムの説明';
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE table_name
        DROP COLUMN IF EXISTS column_name;
    """)
```

### NOT NULL カラム追加（安全なパターン）

```python
def upgrade() -> None:
    op.execute("""
        -- Step 1: nullableカラムを追加
        ALTER TABLE table_name
        ADD COLUMN IF NOT EXISTS email VARCHAR(255);

        -- Step 2: 既存データを更新
        UPDATE table_name
        SET email = CONCAT(LOWER(name), '@example.com')
        WHERE email IS NULL;

        -- Step 3: NOT NULL制約を追加
        ALTER TABLE table_name
        ALTER COLUMN email SET NOT NULL;

        -- コメント
        COMMENT ON COLUMN table_name.email IS 'メールアドレス';
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE table_name
        DROP COLUMN IF EXISTS email;
    """)
```

### インデックス作成

```python
def upgrade() -> None:
    op.execute("""
        -- 単一カラムインデックス
        CREATE INDEX IF NOT EXISTS idx_table_column
            ON table_name(column_name);

        -- 複合インデックス
        CREATE INDEX IF NOT EXISTS idx_table_column1_column2
            ON table_name(column1, column2);

        -- パーシャルインデックス
        CREATE INDEX IF NOT EXISTS idx_table_active
            ON table_name(created_at)
            WHERE status = 'active';

        -- ユニークインデックス
        CREATE UNIQUE INDEX IF NOT EXISTS idx_table_unique_column
            ON table_name(column_name);
    """)


def downgrade() -> None:
    op.execute("""
        DROP INDEX IF EXISTS idx_table_column;
        DROP INDEX IF EXISTS idx_table_column1_column2;
        DROP INDEX IF EXISTS idx_table_active;
        DROP INDEX IF EXISTS idx_table_unique_column;
    """)
```

### 外部キー追加

```python
def upgrade() -> None:
    op.execute("""
        -- 外部キー追加（冪等）
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'fk_child_parent'
            ) THEN
                ALTER TABLE child_table
                ADD CONSTRAINT fk_child_parent
                FOREIGN KEY (parent_id)
                REFERENCES parent_table(id)
                ON DELETE CASCADE;
            END IF;
        END $$;

        -- インデックス追加
        CREATE INDEX IF NOT EXISTS idx_child_parent
            ON child_table(parent_id);
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE child_table
        DROP CONSTRAINT IF EXISTS fk_child_parent;

        DROP INDEX IF EXISTS idx_child_parent;
    """)
```

### Enum型

```python
def upgrade() -> None:
    op.execute("""
        -- Enum型作成（冪等）
        DO $$
        BEGIN
            CREATE TYPE status_type AS ENUM (
                'pending',
                'active',
                'inactive'
            );
        EXCEPTION
            WHEN duplicate_object THEN NULL;
        END $$;

        -- カラム追加
        ALTER TABLE table_name
        ADD COLUMN IF NOT EXISTS status status_type DEFAULT 'pending';
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE table_name
        DROP COLUMN IF EXISTS status;

        DROP TYPE IF EXISTS status_type;
    """)
```

## 冪等性の確保

**全てのマイグレーションは冪等でなければなりません**（複数回実行しても安全）。

### 使用するべき構文

```sql
-- ✅ テーブル
CREATE TABLE IF NOT EXISTS ...
DROP TABLE IF EXISTS ...

-- ✅ カラム
ALTER TABLE t ADD COLUMN IF NOT EXISTS ...
ALTER TABLE t DROP COLUMN IF EXISTS ...

-- ✅ インデックス
CREATE INDEX IF NOT EXISTS ...
DROP INDEX IF EXISTS ...

-- ✅ 制約
ALTER TABLE t DROP CONSTRAINT IF EXISTS ...
-- 制約追加は DO $$ ブロックで存在チェック

-- ✅ Enum
DO $$ BEGIN CREATE TYPE ... EXCEPTION WHEN duplicate_object THEN NULL; END $$;
DROP TYPE IF EXISTS ...
```

### 複雑なロジックの冪等化

```python
def upgrade() -> None:
    op.execute("""
        DO $$
        BEGIN
            -- カラム存在チェック
            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'table_name'
                AND column_name = 'new_column'
            ) THEN
                ALTER TABLE table_name ADD COLUMN new_column VARCHAR(255);
                RAISE NOTICE 'Added new_column';
            ELSE
                RAISE NOTICE 'Column already exists, skipping';
            END IF;
        END $$;
    """)
```

## パフォーマンス考慮事項

### 大量データの更新

```python
def upgrade() -> None:
    op.execute("""
        -- バッチ更新
        DO $$
        DECLARE
            batch_size INTEGER := 1000;
            rows_updated INTEGER;
        BEGIN
            LOOP
                UPDATE table_name
                SET new_field = old_field
                WHERE new_field IS NULL
                AND id IN (
                    SELECT id FROM table_name
                    WHERE new_field IS NULL
                    LIMIT batch_size
                    FOR UPDATE SKIP LOCKED
                );

                GET DIAGNOSTICS rows_updated = ROW_COUNT;
                EXIT WHEN rows_updated = 0;

                PERFORM pg_sleep(0.1);  -- 小休止
            END LOOP;
        END $$;
    """)
```

### インデックス作成（大規模テーブル）

```python
def upgrade() -> None:
    op.execute("""
        -- CONCURRENTLY: テーブルをロックせずにインデックス作成
        -- 注意: トランザクション内では使用不可
        CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_table_column
            ON table_name(column_name);
    """)
```

## よくある間違い

### 1. downgrade()を実装しない

```python
# ❌ Bad
def downgrade() -> None:
    pass

# ✅ Good
def downgrade() -> None:
    op.execute("ALTER TABLE t DROP COLUMN IF EXISTS c;")
```

### 2. 外部キーにインデックスがない

```python
# ❌ Bad: JOINが遅くなる
def upgrade() -> None:
    op.execute("""
        ALTER TABLE speakers
        ADD COLUMN politician_id INTEGER REFERENCES politicians(id);
    """)

# ✅ Good
def upgrade() -> None:
    op.execute("""
        ALTER TABLE speakers
        ADD COLUMN IF NOT EXISTS politician_id INTEGER REFERENCES politicians(id);

        CREATE INDEX IF NOT EXISTS idx_speakers_politician
        ON speakers(politician_id);
    """)
```

### 3. NOT NULL カラムを直接追加

```python
# ❌ Bad: 既存データがあると失敗
def upgrade() -> None:
    op.execute("""
        ALTER TABLE t ADD COLUMN email VARCHAR(255) NOT NULL;
    """)

# ✅ Good: 3ステップで追加
def upgrade() -> None:
    op.execute("""
        ALTER TABLE t ADD COLUMN IF NOT EXISTS email VARCHAR(255);
        UPDATE t SET email = 'default@example.com' WHERE email IS NULL;
        ALTER TABLE t ALTER COLUMN email SET NOT NULL;
    """)
```

### 4. 制約削除前のテーブル削除

```python
# ❌ Bad: 依存関係でエラー
def upgrade() -> None:
    op.execute("DROP TABLE IF EXISTS politicians;")

# ✅ Good: 先に制約を削除
def upgrade() -> None:
    op.execute("""
        ALTER TABLE speakers DROP CONSTRAINT IF EXISTS fk_speakers_politicians;
        DROP TABLE IF EXISTS politicians;
    """)
```

## テスト方法

### ローカルテスト

```bash
# マイグレーション適用
just migrate

# テーブル確認
just db
\d table_name
\d+ table_name  # 詳細表示

# インデックス確認
\di+ table_name*

# ロールバックテスト
just migrate-rollback
just migrate  # 再適用
```

### CI/CD統合

```yaml
# GitHub Actions例
- name: Run migrations
  run: |
    docker compose exec sagebase uv run alembic upgrade head

- name: Verify migrations
  run: |
    docker compose exec sagebase uv run alembic current
```

## PostgreSQL固有の機能

### JSONB

```sql
-- カラム追加
ALTER TABLE t ADD COLUMN IF NOT EXISTS metadata JSONB;

-- GINインデックス
CREATE INDEX IF NOT EXISTS idx_t_metadata_gin
    ON t USING GIN (metadata);

-- 特定キーのインデックス
CREATE INDEX IF NOT EXISTS idx_t_metadata_status
    ON t ((metadata->>'status'));

-- クエリ例
SELECT * FROM t WHERE metadata->>'key' = 'value';
SELECT * FROM t WHERE metadata @> '{"key": "value"}';
```

### 配列

```sql
-- カラム追加
ALTER TABLE t ADD COLUMN IF NOT EXISTS tags TEXT[];

-- クエリ例
SELECT * FROM t WHERE 'tag1' = ANY(tags);
SELECT * FROM t WHERE tags @> ARRAY['tag1', 'tag2'];
```

### 全文検索

```sql
-- tsvectorカラム追加
ALTER TABLE t ADD COLUMN IF NOT EXISTS search_vector tsvector;

-- データ更新
UPDATE t SET search_vector = to_tsvector('japanese', name || ' ' || description);

-- GINインデックス
CREATE INDEX IF NOT EXISTS idx_t_search
    ON t USING GIN (search_vector);

-- クエリ例
SELECT * FROM t WHERE search_vector @@ to_tsquery('japanese', '検索語');
```

## 参考リンク

- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- Sagebase内部: `docs/DATABASE_SCHEMA.md`
