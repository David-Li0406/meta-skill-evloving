# Alembic Migration Examples

Sagebaseプロジェクトの実践的なAlembicマイグレーション例集です。

## Example 1: カラム追加（基本）

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
    """Add email column with index."""
    op.execute("""
        -- カラム追加
        ALTER TABLE politicians
        ADD COLUMN IF NOT EXISTS email VARCHAR(255);

        -- コメント追加
        COMMENT ON COLUMN politicians.email IS 'Politician email address';

        -- インデックス追加
        CREATE INDEX IF NOT EXISTS idx_politicians_email
        ON politicians(email);
    """)


def downgrade() -> None:
    """Remove email column and index."""
    op.execute("""
        DROP INDEX IF EXISTS idx_politicians_email;
        ALTER TABLE politicians DROP COLUMN IF EXISTS email;
    """)
```

## Example 2: 新しいテーブル作成

```python
"""Create audit_logs table.

Revision ID: 004
Revises: 003
Create Date: 2025-01-20
"""

from alembic import op


revision = "004"
down_revision = "003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create audit_logs table with indexes."""
    op.execute("""
        -- テーブル作成
        CREATE TABLE IF NOT EXISTS audit_logs (
            id SERIAL PRIMARY KEY,
            entity_type VARCHAR(100) NOT NULL,
            entity_id INTEGER NOT NULL,
            action VARCHAR(50) NOT NULL,
            user_id UUID,
            old_value JSONB,
            new_value JSONB,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        -- インデックス作成
        CREATE INDEX IF NOT EXISTS idx_audit_logs_entity
        ON audit_logs(entity_type, entity_id);

        CREATE INDEX IF NOT EXISTS idx_audit_logs_created
        ON audit_logs(created_at DESC);

        CREATE INDEX IF NOT EXISTS idx_audit_logs_user
        ON audit_logs(user_id);

        -- テーブルコメント
        COMMENT ON TABLE audit_logs IS 'Audit trail for entity changes';
        COMMENT ON COLUMN audit_logs.action IS 'Action type: create, update, delete';
    """)


def downgrade() -> None:
    """Drop audit_logs table."""
    op.execute("""
        DROP TABLE IF EXISTS audit_logs;
    """)
```

## Example 3: NOT NULL カラム追加（既存データ対応）

```python
"""Add status column to meetings (with default value for existing rows).

Revision ID: 005
Revises: 004
Create Date: 2025-01-20
"""

from alembic import op


revision = "005"
down_revision = "004"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add status column with safe migration for existing data."""
    op.execute("""
        -- Step 1: nullable カラムを追加
        ALTER TABLE meetings
        ADD COLUMN IF NOT EXISTS status VARCHAR(50);

        -- Step 2: 既存レコードにデフォルト値を設定
        UPDATE meetings
        SET status = 'active'
        WHERE status IS NULL;

        -- Step 3: NOT NULL 制約を追加
        ALTER TABLE meetings
        ALTER COLUMN status SET NOT NULL;

        -- Step 4: デフォルト値を設定
        ALTER TABLE meetings
        ALTER COLUMN status SET DEFAULT 'pending';

        -- コメント追加
        COMMENT ON COLUMN meetings.status IS 'Meeting status: pending, active, completed, cancelled';

        -- インデックス追加
        CREATE INDEX IF NOT EXISTS idx_meetings_status
        ON meetings(status);
    """)


def downgrade() -> None:
    """Remove status column."""
    op.execute("""
        DROP INDEX IF EXISTS idx_meetings_status;
        ALTER TABLE meetings DROP COLUMN IF EXISTS status;
    """)
```

## Example 4: 外部キー追加

```python
"""Add foreign key from speakers to conferences.

Revision ID: 006
Revises: 005
Create Date: 2025-01-20
"""

from alembic import op


revision = "006"
down_revision = "005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add conference_id foreign key to speakers."""
    op.execute("""
        -- カラム追加
        ALTER TABLE speakers
        ADD COLUMN IF NOT EXISTS conference_id INTEGER;

        -- 外部キー制約追加
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'fk_speakers_conference'
            ) THEN
                ALTER TABLE speakers
                ADD CONSTRAINT fk_speakers_conference
                FOREIGN KEY (conference_id)
                REFERENCES conferences(id)
                ON DELETE SET NULL;
            END IF;
        END $$;

        -- インデックス追加（外部キーには必須）
        CREATE INDEX IF NOT EXISTS idx_speakers_conference
        ON speakers(conference_id);

        -- コメント
        COMMENT ON COLUMN speakers.conference_id IS 'Reference to the conference where this speaker appeared';
    """)


def downgrade() -> None:
    """Remove conference_id from speakers."""
    op.execute("""
        -- 外部キー制約を削除
        ALTER TABLE speakers
        DROP CONSTRAINT IF EXISTS fk_speakers_conference;

        -- インデックスを削除
        DROP INDEX IF EXISTS idx_speakers_conference;

        -- カラムを削除
        ALTER TABLE speakers
        DROP COLUMN IF EXISTS conference_id;
    """)
```

## Example 5: 複合ユニーク制約追加

```python
"""Add unique constraint on parliamentary_group_memberships.

Revision ID: 007
Revises: 006
Create Date: 2025-01-20
"""

from alembic import op


revision = "007"
down_revision = "006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add unique constraint to prevent duplicate memberships."""
    op.execute("""
        -- 重複データを先に処理（古いレコードを保持）
        DELETE FROM parliamentary_group_memberships a
        USING parliamentary_group_memberships b
        WHERE a.id > b.id
        AND a.parliamentary_group_id = b.parliamentary_group_id
        AND a.politician_id = b.politician_id
        AND a.start_date = b.start_date;

        -- ユニーク制約を追加
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1 FROM pg_constraint
                WHERE conname = 'uq_pgm_group_politician_date'
            ) THEN
                ALTER TABLE parliamentary_group_memberships
                ADD CONSTRAINT uq_pgm_group_politician_date
                UNIQUE (parliamentary_group_id, politician_id, start_date);
            END IF;
        END $$;
    """)


def downgrade() -> None:
    """Remove unique constraint."""
    op.execute("""
        ALTER TABLE parliamentary_group_memberships
        DROP CONSTRAINT IF EXISTS uq_pgm_group_politician_date;
    """)
```

## Example 6: Enum型の作成と使用

```python
"""Add matching_method enum to extracted_conference_members.

Revision ID: 008
Revises: 007
Create Date: 2025-01-20
"""

from alembic import op


revision = "008"
down_revision = "007"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create enum type and add column."""
    op.execute("""
        -- Enum型を作成（冪等性のためDOブロック使用）
        DO $$
        BEGIN
            CREATE TYPE matching_method AS ENUM (
                'exact_match',
                'fuzzy_match',
                'llm_match',
                'manual'
            );
        EXCEPTION
            WHEN duplicate_object THEN NULL;
        END $$;

        -- カラム追加
        ALTER TABLE extracted_conference_members
        ADD COLUMN IF NOT EXISTS matching_method matching_method;

        -- 既存データを更新
        UPDATE extracted_conference_members
        SET matching_method = 'manual'
        WHERE matching_status = 'matched'
        AND matching_method IS NULL;

        -- コメント
        COMMENT ON COLUMN extracted_conference_members.matching_method IS
            'Method used for matching: exact_match, fuzzy_match, llm_match, manual';
    """)


def downgrade() -> None:
    """Remove column and enum type."""
    op.execute("""
        -- カラム削除
        ALTER TABLE extracted_conference_members
        DROP COLUMN IF EXISTS matching_method;

        -- Enum型削除
        DROP TYPE IF EXISTS matching_method;
    """)
```

## Example 7: 大量データのバッチ更新

```python
"""Backfill prefecture column for politicians.

Revision ID: 009
Revises: 008
Create Date: 2025-01-20
"""

from alembic import op


revision = "009"
down_revision = "008"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Backfill prefecture from district column."""
    op.execute("""
        -- バッチ更新（大量データ対応）
        DO $$
        DECLARE
            batch_size INTEGER := 1000;
            rows_updated INTEGER;
            total_updated INTEGER := 0;
        BEGIN
            LOOP
                -- バッチで更新
                WITH to_update AS (
                    SELECT id
                    FROM politicians
                    WHERE prefecture IS NULL
                    AND district IS NOT NULL
                    LIMIT batch_size
                    FOR UPDATE SKIP LOCKED
                )
                UPDATE politicians p
                SET prefecture = SUBSTRING(p.district FROM 1 FOR 3)
                FROM to_update
                WHERE p.id = to_update.id;

                GET DIAGNOSTICS rows_updated = ROW_COUNT;
                total_updated := total_updated + rows_updated;

                EXIT WHEN rows_updated = 0;

                -- 進捗ログ
                RAISE NOTICE 'Updated % rows (total: %)', rows_updated, total_updated;

                -- 次のバッチ前に小休止
                PERFORM pg_sleep(0.1);
            END LOOP;

            RAISE NOTICE 'Backfill completed. Total rows updated: %', total_updated;
        END $$;
    """)


def downgrade() -> None:
    """Clear backfilled prefecture values."""
    op.execute("""
        -- 自動生成された prefecture をクリア
        -- 注意: 手動設定されたものも消える可能性あり
        UPDATE politicians
        SET prefecture = NULL
        WHERE prefecture = SUBSTRING(district FROM 1 FOR 3);
    """)
```

## Example 8: パーシャルインデックス

```python
"""Add partial index for active parliamentary group memberships.

Revision ID: 010
Revises: 009
Create Date: 2025-01-20
"""

from alembic import op


revision = "010"
down_revision = "009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add partial index for active memberships (end_date IS NULL)."""
    op.execute("""
        -- 現在アクティブなメンバーシップのみのインデックス
        CREATE INDEX IF NOT EXISTS idx_pgm_active_by_group
        ON parliamentary_group_memberships(parliamentary_group_id)
        WHERE end_date IS NULL;

        -- 現在アクティブなメンバーシップのみのインデックス（政治家別）
        CREATE INDEX IF NOT EXISTS idx_pgm_active_by_politician
        ON parliamentary_group_memberships(politician_id)
        WHERE end_date IS NULL;

        -- コメント
        COMMENT ON INDEX idx_pgm_active_by_group IS
            'Partial index for active memberships only (end_date IS NULL)';
    """)


def downgrade() -> None:
    """Drop partial indexes."""
    op.execute("""
        DROP INDEX IF EXISTS idx_pgm_active_by_group;
        DROP INDEX IF EXISTS idx_pgm_active_by_politician;
    """)
```

## Example 9: JSONBカラムとGINインデックス

```python
"""Add metadata JSONB column to minutes.

Revision ID: 011
Revises: 010
Create Date: 2025-01-20
"""

from alembic import op


revision = "011"
down_revision = "010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add metadata JSONB column with GIN index."""
    op.execute("""
        -- JSONBカラム追加
        ALTER TABLE minutes
        ADD COLUMN IF NOT EXISTS processing_metadata JSONB;

        -- GINインデックス（JSONB検索用）
        CREATE INDEX IF NOT EXISTS idx_minutes_metadata_gin
        ON minutes USING GIN (processing_metadata);

        -- 特定のキーに対するインデックス
        CREATE INDEX IF NOT EXISTS idx_minutes_metadata_status
        ON minutes ((processing_metadata->>'status'));

        -- コメント
        COMMENT ON COLUMN minutes.processing_metadata IS
            'Processing metadata: {status, processor_version, extracted_at, token_count}';
    """)


def downgrade() -> None:
    """Remove metadata column and indexes."""
    op.execute("""
        DROP INDEX IF EXISTS idx_minutes_metadata_status;
        DROP INDEX IF EXISTS idx_minutes_metadata_gin;
        ALTER TABLE minutes DROP COLUMN IF EXISTS processing_metadata;
    """)
```

## Example 10: テーブル名変更（リネーム）

```python
"""Rename extracted_politicians to politician_candidates.

Revision ID: 012
Revises: 011
Create Date: 2025-01-20
"""

from alembic import op


revision = "012"
down_revision = "011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Rename table and update related objects."""
    op.execute("""
        -- テーブル名変更
        ALTER TABLE IF EXISTS extracted_politicians
        RENAME TO politician_candidates;

        -- シーケンス名変更（存在する場合）
        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'extracted_politicians_id_seq') THEN
                ALTER SEQUENCE extracted_politicians_id_seq
                RENAME TO politician_candidates_id_seq;
            END IF;
        END $$;

        -- インデックス名変更
        ALTER INDEX IF EXISTS idx_extracted_politicians_name
        RENAME TO idx_politician_candidates_name;

        ALTER INDEX IF EXISTS idx_extracted_politicians_status
        RENAME TO idx_politician_candidates_status;

        -- テーブルコメント更新
        COMMENT ON TABLE politician_candidates IS
            'Candidate politicians extracted from various sources (renamed from extracted_politicians)';
    """)


def downgrade() -> None:
    """Rename back to original names."""
    op.execute("""
        ALTER TABLE IF EXISTS politician_candidates
        RENAME TO extracted_politicians;

        DO $$
        BEGIN
            IF EXISTS (SELECT 1 FROM pg_class WHERE relname = 'politician_candidates_id_seq') THEN
                ALTER SEQUENCE politician_candidates_id_seq
                RENAME TO extracted_politicians_id_seq;
            END IF;
        END $$;

        ALTER INDEX IF EXISTS idx_politician_candidates_name
        RENAME TO idx_extracted_politicians_name;

        ALTER INDEX IF EXISTS idx_politician_candidates_status
        RENAME TO idx_extracted_politicians_status;
    """)
```

## Anti-Patterns（避けるべきパターン）

### ❌ Bad: 冪等でない

```python
def upgrade() -> None:
    # 2回実行するとエラー
    op.execute("CREATE TABLE my_table (...)")
    op.execute("ALTER TABLE my_table ADD COLUMN my_column VARCHAR(255)")
```

### ✅ Good: 冪等

```python
def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS my_table (...);
        ALTER TABLE my_table ADD COLUMN IF NOT EXISTS my_column VARCHAR(255);
    """)
```

### ❌ Bad: downgrade()がない

```python
def upgrade() -> None:
    op.execute("ALTER TABLE x ADD COLUMN y VARCHAR(255)")

def downgrade() -> None:
    pass  # ロールバック不可能！
```

### ✅ Good: downgrade()を実装

```python
def upgrade() -> None:
    op.execute("ALTER TABLE x ADD COLUMN IF NOT EXISTS y VARCHAR(255)")

def downgrade() -> None:
    op.execute("ALTER TABLE x DROP COLUMN IF EXISTS y")
```

### ❌ Bad: 外部キーにインデックスがない

```python
def upgrade() -> None:
    op.execute("""
        ALTER TABLE speakers ADD COLUMN politician_id INTEGER
        REFERENCES politicians(id);
        -- インデックスなし！JOINが遅くなる
    """)
```

### ✅ Good: 外部キーには必ずインデックス

```python
def upgrade() -> None:
    op.execute("""
        ALTER TABLE speakers ADD COLUMN IF NOT EXISTS politician_id INTEGER
        REFERENCES politicians(id);

        CREATE INDEX IF NOT EXISTS idx_speakers_politician
        ON speakers(politician_id);
    """)
```
