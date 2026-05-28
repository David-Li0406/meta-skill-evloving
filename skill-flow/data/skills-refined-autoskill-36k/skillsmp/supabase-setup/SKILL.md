---
name: supabase-setup
description: Initialize Supabase locally, manage database migrations, and configure Row Level Security. Use when setting up databases, creating tables, or managing schemas.
metadata:
  author: Bingify
  version: "1.0"
---

# Supabase Setup & Database Management

このスキルは、Bingifyプロジェクトのデータベース初期化とマイグレーション管理をカバーします。

## 概要

BingifyはSupabaseをバックエンドデータベースとして使用します。ローカル開発ではSupabase CLIで完全なPostgreSQLの環境を提供します。

## ローカルセットアップ

### Supabaseの起動

ローカル開発環境の完全なセットアップ：

```bash
pnpm local:setup
```

詳細は [development スキル](../development/SKILL.md) を参照してください。

### Supabase Studioへのアクセス

```
http://localhost:54323
```

### PostgreSQLへのアクセス

- Host: localhost
- Port: 5432
- User: PostgreSQL
- Password: PostgreSQL
- Database: PostgreSQL

## マイグレーション管理

### 重要ルール

**既存のマイグレーションファイルを編集してはいけません。**

変更が必要な場合は、新しいマイグレーションを作成してください。

### マイグレーション作成

```bash
supabase migration new migration_name
```

### マイグレーション適用

```bash
supabase db push
```

### マイグレーション確認

```bash
supabase migration list
```

## RLSポリシー

```sql
-- ユーザー自身のデータのみ表示
CREATE POLICY "Users can view own data"
  ON public.users
  FOR SELECT
  USING (auth.uid() = id);

-- 認証済みユーザーのみ挿入可能
CREATE POLICY "Authenticated users can insert"
  ON public.spaces
  FOR INSERT
  WITH CHECK (auth.role() = 'authenticated');
```

## データシード

```bash
supabase seed run
```

シードスクリプト: `supabase/seed.sql`

## 参考

- [docs/MIGRATIONS.md](../../../docs/MIGRATIONS.md) - マイグレーション運用ガイド
- [development スキル](../development/SKILL.md) - セットアップ全体の流れ
