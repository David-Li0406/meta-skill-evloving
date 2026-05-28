# Snowflakeクエリ実行スキル

ユーザーの自然言語指示からSnowflake用のSQLクエリを自動生成・実行するClaude Codeスキルです。

## ファイル構成

- **SKILL.md** - スキルの詳細なドキュメント
- **schema.json** - 実際のSnowflakeテーブル構造（Git管理対象外）
- **schema.json.example** - サンプルテーブル定義のテンプレート（Git管理対象）
- **generate-schema.py** - Snowflakeからschema.jsonを自動生成するスクリプト
- **README.md** - このファイル

## クイックスタート

### 1. Snowflake CLIのインストール

```bash
# miseでSnowflake CLIをインストール（必要な場合）
mise install pipx:snowflake-cli

# バージョン確認
snow --version
```

### 2. schema.jsonの準備

初めて使用する際は、以下のいずれかの方法でschema.jsonを作成します：

**方法A: 自動生成（推奨）**
```bash
cd claude/skills/snowflake-query
python3 generate-schema.py --connection your_connection
```

**方法B: サンプルからコピー**
```bash
cp schema.json.example schema.json
# その後、実際のテーブル構造に合わせて編集
```

### 2. スキルの使用

Claudeに自然言語で指示するだけです：

```
「usersテーブルの25歳以上のデータを取得して」
「部署ごとの平均給与を計算して」
「ordersテーブルの最新10件を表示」
```

## generate-schema.pyの使い方

```bash
# デフォルト接続でPUBLICスキーマのすべてのテーブル
python3 generate-schema.py

# 接続名を指定
python3 generate-schema.py --connection prod_warehouse

# 特定のテーブルのみ
python3 generate-schema.py --tables users,orders,products

# スキーマを指定
python3 generate-schema.py --schema ANALYTICS

# ヘルプを表示
python3 generate-schema.py --help
```

## 重要な注意事項

### セキュリティ

- **schema.json** はGit管理対象外です（.gitignoreに追加済み）
- データベース構造は機密情報として扱われます
- 公開リポジトリにschema.jsonをコミットしないでください

### ファイルの管理

- **schema.json** - ローカル環境でのみ管理（各自で作成）
- **schema.json.example** - Git管理（テンプレートとして共有）

## 詳細情報

詳細な使い方やワークフローについては、[SKILL.md](./SKILL.md)を参照してください。
