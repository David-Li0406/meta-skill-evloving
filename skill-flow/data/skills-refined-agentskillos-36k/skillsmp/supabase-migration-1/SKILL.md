---
name: supabase-migration
description: Supabaseのマイグレーションファイルを作成。新しいテーブル、カラム追加、RLSポリシー、インデックス作成時に使用。
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# Supabaseマイグレーション作成スキル

Katorin2プロジェクト用のSupabaseマイグレーションを作成するガイドです。

## マイグレーションファイルの場所

```
supabase/migrations/
├── 001_mvp_schema.sql
├── 002_add_custom_fields.sql
├── 003_add_entry_limit_behavior.sql
├── 004_series.sql
├── 005_teams.sql
└── XXX_new_migration.sql  ← 新規追加
```

## 命名規則

```
{連番3桁}_{snake_case_description}.sql
例: 006_add_notification_preferences.sql
```

## マイグレーションテンプレート

```sql
-- Migration: {説明}
-- Created: {日付}

-- ============================================
-- 1. ENUM型の追加（必要な場合）
-- ============================================
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'new_enum_type') THEN
    CREATE TYPE new_enum_type AS ENUM ('value1', 'value2', 'value3');
  END IF;
END $$;

-- ============================================
-- 2. テーブル作成
-- ============================================
CREATE TABLE IF NOT EXISTS table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  -- カラム定義
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  status new_enum_type DEFAULT 'value1',
  data JSONB DEFAULT '{}',
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================
-- 3. インデックス作成
-- ============================================
CREATE INDEX IF NOT EXISTS idx_table_name_user_id
  ON table_name(user_id);

CREATE INDEX IF NOT EXISTS idx_table_name_status
  ON table_name(status);

-- ============================================
-- 4. RLS有効化
-- ============================================
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

-- ============================================
-- 5. RLSポリシー
-- ============================================

-- 閲覧ポリシー
CREATE POLICY "Anyone can view table_name"
  ON table_name FOR SELECT
  USING (true);

-- 作成ポリシー
CREATE POLICY "Authenticated users can create"
  ON table_name FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

-- 更新ポリシー
CREATE POLICY "Owners can update"
  ON table_name FOR UPDATE
  TO authenticated
  USING (auth.uid() = user_id)
  WITH CHECK (auth.uid() = user_id);

-- 削除ポリシー
CREATE POLICY "Owners can delete"
  ON table_name FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);

-- ============================================
-- 6. トリガー（必要な場合）
-- ============================================
CREATE OR REPLACE FUNCTION update_table_name_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_table_name_updated_at
  BEFORE UPDATE ON table_name
  FOR EACH ROW
  EXECUTE FUNCTION update_table_name_updated_at();

-- ============================================
-- 7. Realtime有効化（必要な場合）
-- ============================================
ALTER PUBLICATION supabase_realtime ADD TABLE table_name;

-- ============================================
-- 8. ビュー作成（必要な場合）
-- ============================================
CREATE OR REPLACE VIEW table_name_summary AS
SELECT
  user_id,
  COUNT(*) as total_count,
  MAX(created_at) as last_created
FROM table_name
GROUP BY user_id;
```

## 既存ENUM型

```sql
-- 大会関連
tournament_status, tournament_format, match_format, visibility
entry_type, result_report_mode, match_status, entry_limit_behavior

-- チーム関連
team_member_role, check_in_status, team_battle_format, team_creation_mode

-- シリーズ関連
series_status, series_point_system
```

## カラム追加のパターン

```sql
-- 新しいカラムを追加
ALTER TABLE tournaments
  ADD COLUMN IF NOT EXISTS new_column VARCHAR(100);

-- デフォルト値付き
ALTER TABLE tournaments
  ADD COLUMN IF NOT EXISTS is_featured BOOLEAN DEFAULT false;

-- NOT NULL制約付き（デフォルト値必須）
ALTER TABLE tournaments
  ADD COLUMN IF NOT EXISTS priority SMALLINT NOT NULL DEFAULT 0;
```

## 外部キー制約

```sql
-- profilesへの参照
user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE

-- tournamentsへの参照
tournament_id UUID NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE

-- 自己参照（ツリー構造）
parent_id UUID REFERENCES same_table(id) ON DELETE SET NULL
```

## マイグレーション実行コマンド

```bash
# ローカルでリセット＆適用
npx supabase db reset

# リモートに適用
npx supabase db push

# 型定義の再生成
npx supabase gen types typescript --local > src/types/database.ts
```

## チェックリスト

マイグレーション作成時の確認事項：

- [ ] テーブル・カラム名はsnake_case
- [ ] 適切な型を選択（VARCHAR長さ、JSONB等）
- [ ] 外部キー制約とON DELETE設定
- [ ] RLS有効化
- [ ] 必要なRLSポリシー（SELECT, INSERT, UPDATE, DELETE）
- [ ] インデックス（検索・結合に使うカラム）
- [ ] updated_atトリガー（更新日時自動更新）
- [ ] Realtime設定（リアルタイム更新が必要な場合）
