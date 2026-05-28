---
name: migration-helper
description: データベースマイグレーションを作成する際に使用。Atlas CLI使用、master/shardingのマイグレーション、SQLite構文。DB変更、テーブル追加、カラム追加、マイグレーションファイル作成時に使用。
allowed-tools: Read, Bash(atlas:*), Bash(./scripts/migrate.sh:*)
---

# マイグレーション作成パターン

このプロジェクトのデータベースマイグレーション実装パターンを定義します。

## ディレクトリ構成

```
db/migrations/
├── master/           # マスターDB用（news, goadminテーブル等）
│   ├── atlas.sum
│   └── *.sql
├── sharding_1/       # シャーディングDB 1用
├── sharding_2/       # シャーディングDB 2用
├── sharding_3/       # シャーディングDB 3用
└── sharding_4/       # シャーディングDB 4用
```

## マイグレーションツール

- **Atlas CLI**: マイグレーション管理
- **SQLite**: 開発環境のDB

## 参照ファイル

既存マイグレーション:
- `db/migrations/master/` - マスターDBマイグレーション
- `db/migrations/sharding_1/` - シャーディングDBマイグレーション例

スクリプト:
- `scripts/migrate.sh` - マイグレーション適用スクリプト

## マイグレーション作成手順

### 1. 新しいマイグレーションファイルの作成

Atlas CLIで差分を生成:

```bash
# マスターDB用
atlas migrate diff {migration_name} \
    --dir "file://db/migrations/master" \
    --to "file://db/schema/master.sql" \
    --dev-url "sqlite://file?mode=memory"

# シャーディングDB用（4つ全てに適用）
for i in 1 2 3 4; do
    atlas migrate diff {migration_name} \
        --dir "file://db/migrations/sharding_$i" \
        --to "file://db/schema/sharding.sql" \
        --dev-url "sqlite://file?mode=memory"
done
```

### 2. マイグレーションファイルの形式

ファイル名: `{YYYYMMDDHHMMSS}_{description}.sql`

例: `20251226074846_initial.sql`

### 3. SQLite構文パターン

#### テーブル作成

```sql
-- Create "entities" table
CREATE TABLE `entities` (
  `id` integer NOT NULL PRIMARY KEY AUTOINCREMENT,
  `name` text NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
);
```

#### シャーディングテーブル作成

シャーディングDBでは、テーブル名にサフィックスが付きます:

```sql
-- DB1: entities_000 ~ entities_007
-- DB2: entities_008 ~ entities_015
-- DB3: entities_016 ~ entities_023
-- DB4: entities_024 ~ entities_031

CREATE TABLE `users_000` (
  `id` integer NOT NULL,
  `name` text NOT NULL,
  `email` text NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
);
-- 同様に users_001 ~ users_007 を作成
```

#### インデックス作成

```sql
-- Create index "idx_entities_name" to table: "entities"
CREATE INDEX `idx_entities_name` ON `entities` (`name`);
```

#### カラム追加

```sql
-- Add column "description" to table: "entities"
ALTER TABLE `entities` ADD COLUMN `description` text NULL;
```

## マイグレーション適用

```bash
# 全マイグレーション適用
./scripts/migrate.sh all

# マスターのみ
./scripts/migrate.sh master

# シャーディングのみ
./scripts/migrate.sh sharding
```

## atlas.sum の更新

マイグレーションファイルを手動で編集した場合:

```bash
atlas migrate hash --dir "file://db/migrations/master"
atlas migrate hash --dir "file://db/migrations/sharding_1"
# ... sharding_2, 3, 4 も同様
```

## 注意事項

1. **シャーディングDBは4つ全てに同じ変更を適用**
2. **テーブル名のサフィックスに注意** (`_000` ~ `_031`)
3. **SQLite構文を使用** (バッククォートでカラム名を囲む)
4. **PRIMARY KEY AUTOINCREMENT はマスターDBのみ** (シャーディングDBはアプリ側でID生成)
