---
name: snowflake-query
description: ユーザーの自然言語指示を受け取り、Snowflakeで実行するSQLクエリを生成・実行し、結果をCSV形式で出力します。「Snowflakeで〜を取得して」「〜のデータを表示して」などのリクエストで自動的に起動します。
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Snowflakeクエリ実行スキル

このスキルは、ユーザーの自然言語指示を理解し、Snowflake用のSQLクエリを自動生成・実行して結果を返します。

**IMPORTANT: このスキルを使用する際は、必ず日本語でユーザーとコミュニケーションを取ってください。**

## ワークフロー

### 1. リクエスト内容の確認

まずユーザーの指示内容を詳しく確認します：

- **対象テーブル名**: どのテーブルからデータを取得するか
- **カラム指定**: 特定のカラムのみか、全カラムか
- **フィルター条件**: WHERE句で絞り込む条件
- **集計・グループ化**: COUNT, SUM, AVGなどの集計や、GROUP BYの必要性
- **ソート**: ORDER BYの必要性
- **行数制限**: LIMIT（指定がなければデフォルト1000行）
- **接続名**: `--connection`オプションで接続を指定するか

不明な点や曖昧な指示がある場合は、必ず日本語でユーザーに確認を取ります。

### 2. スキーマ情報の取得

クエリを正確に生成するため、スキーマ情報を取得します。

#### ローカルスキーマファイルの確認（推奨）

まず、このスキルディレクトリ内の`schema.json`ファイルを確認します：

```bash
# ローカルスキーマファイルを読み込む
cat claude/skills/snowflake-query/schema.json
```

**schema.jsonの利点**:
- Snowflakeに接続せずに高速にスキーマ情報を参照できる
- テーブル構造、カラム型、説明、サンプルクエリが記載されている
- 手動で管理するため、よく使うテーブルのみ記載可能

**schema.jsonの構造**:
```json
{
  "tables": {
    "table_name": {
      "description": "テーブルの説明",
      "columns": {
        "column_name": {
          "type": "データ型",
          "nullable": true/false,
          "description": "カラムの説明"
        }
      },
      "sample_queries": ["サンプルクエリ1", "サンプルクエリ2"]
    }
  }
}
```

**巨大なschema.jsonの扱い方**:

schema.jsonファイルが巨大で全体を読み込むのが困難な場合は、`jq`コマンドを使用して必要な情報のみを効率的に抽出できます：

```bash
# テーブル一覧を取得
jq -r '.tables | keys[]' claude/skills/snowflake-query/schema.json

# 特定のテーブルのカラム一覧を取得
jq -r '.tables.table_name.columns | keys[]' claude/skills/snowflake-query/schema.json

# 特定のテーブルの情報のみを取得
jq '.tables.table_name' claude/skills/snowflake-query/schema.json

# テーブル名と説明のリストを取得
jq -r '.tables | to_entries[] | "\(.key): \(.value.description)"' claude/skills/snowflake-query/schema.json

# 特定のテーブルのカラム情報を詳細に取得
jq '.tables.table_name.columns | to_entries[] | {name: .key, type: .value.type, description: .value.description}' claude/skills/snowflake-query/schema.json
```

この方法により、巨大なschema.jsonファイルでも必要な部分のみを効率的に参照できます。

#### Snowflakeから直接取得（schema.jsonに情報がない場合）

ローカルのschema.jsonに対象テーブルの情報がない場合、Snowflakeから直接取得します：

```bash
# テーブルの存在確認
snow sql --query "SHOW TABLES;" --format CSV

# 特定のスキーマ内のテーブルを確認（必要に応じて）
snow sql --query "SHOW TABLES IN SCHEMA schema_name;" --format CSV

# テーブルの構造を確認
snow sql --query "DESCRIBE TABLE table_name;" --format CSV
```

接続名が指定されている場合は、`--connection connection_name`オプションを追加します。

**処理内容**:
1. まず`schema.json`で対象テーブルを検索
2. schema.jsonに情報があれば、それを使用してクエリ生成
3. schema.jsonに情報がない場合は、Snowflakeから`DESCRIBE TABLE`で取得
4. テーブル名が曖昧な場合は、`SHOW TABLES`で候補を列挙
5. テーブルが存在しない場合は、エラーを日本語で説明し、利用可能なテーブル一覧を提示
6. スキーマ情報を基に適切なWHERE句やオペレータを選択

### 3. SQLクエリの生成

ユーザーの指示とスキーマ情報を基に、Snowflake用のSQLクエリを生成します。

#### 基本的なクエリ構造

**重要**: クエリ実行時にデータベースやスキーマが指定されていない場合、Snowflakeはエラーを返します。完全修飾名（`database.schema.table`）を使用してテーブルを指定する必要があります。

```sql
-- 完全修飾名を使用した全カラム取得
SELECT * FROM database_name.schema_name.table_name WHERE condition ORDER BY column LIMIT 1000;

-- 特定カラム取得
SELECT col1, col2, col3 FROM database_name.schema_name.table_name WHERE condition;

-- 集計クエリ
SELECT col1, COUNT(*), SUM(col2), AVG(col3)
FROM database_name.schema_name.table_name
GROUP BY col1
ORDER BY COUNT(*) DESC;
```

**クエリ生成時の注意事項**:
- データベース名とスキーマ名が不明な場合は、ユーザーに必ず確認する
- `schema.json`に`schema`フィールドがある場合はそれを使用

#### WHERE句の生成ガイドライン

ユーザーの自然言語指示をSQL条件に変換します：

| ユーザー指示 | SQL WHERE句 |
|------------|------------|
| 「20歳以上」（数値カラム） | `WHERE age >= 20` |
| 「名前が'太郎'」 | `WHERE name = '太郎'` |
| 「名前に'太郎'を含む」 | `WHERE name LIKE '%太郎%'` |
| 「2024年以降」（日付カラム） | `WHERE date >= '2024-01-01'` |
| 「2024年1月」 | `WHERE date >= '2024-01-01' AND date < '2024-02-01'` |
| 「タグにpythonを含む」 | `WHERE tags LIKE '%python%'` |
| 「金額が100以上500以下」 | `WHERE amount BETWEEN 100 AND 500` |
| 「ステータスがactiveまたはpending」 | `WHERE status IN ('active', 'pending')` |

#### 集計・グループ化のパターン

| ユーザー指示 | SQL変換 |
|------------|--------|
| 「ユーザーごとのアクセス数」 | `GROUP BY user_id, COUNT(*)` |
| 「部署別の平均給与」 | `GROUP BY department, AVG(salary)` |
| 「月ごとの売上合計」 | `GROUP BY DATE_TRUNC('month', date), SUM(amount)` |
| 「カテゴリごとの商品数」 | `GROUP BY category, COUNT(*)` |

#### 安全性チェック

生成したクエリは以下の安全性チェックを行います：

- **SQLインジェクション防止**: ユーザー入力値は必ずリテラル（文字列はシングルクォートで囲む）として扱う
- **予約語の処理**: カラム名が予約語の場合は必要に応じてダブルクォートで囲む
- **危険なコマンドの禁止**: SELECT以外のコマンド（DELETE, DROP, UPDATE, INSERT など）は生成しない
- **LIMIT設定**: ユーザーが明示的に行数を指定していない場合は、必ず`LIMIT 1000`を設定

複雑なクエリや曖昧な指示の場合は、生成したSQLをユーザーに表示して実行前に確認を取ります。

### 4. クエリの実行

生成したSQLクエリを`snow sql`コマンドで実行します：

```bash
# 完全修飾名を使用したクエリ実行（推奨）
snow sql --query "SELECT * FROM database_name.schema_name.table_name LIMIT 1000;" --format CSV

# データベースとスキーマをオプションで指定する場合
snow sql --query "SELECT * FROM table_name LIMIT 1000;" \
  --format CSV \
  --database my_database \
  --schema my_schema

# 接続名を指定する場合
snow sql --query "SELECT * FROM database_name.schema_name.table_name;" --format CSV --connection connection_name

# エラーハンドリング付き実行
if ! result=$(snow sql --query "$query" --format CSV 2>&1); then
    echo "エラー: クエリ実行に失敗しました"
    echo "$result"
    exit 1
fi
```

**実行時の注意点**:
- `--format CSV`オプションでCSV形式で出力を取得
- **データベースとスキーマの指定は必須**: 以下のいずれかの方法で指定する
  - クエリ内で完全修飾名（`database.schema.table`）を使用（推奨）
  - `--database`と`--schema`オプションを指定
- エラー出力（stderr）も取得してユーザーに日本語で説明
- 長時間実行されるクエリの場合は、ユーザーに実行中であることを通知

### 5. 結果の表示

クエリ実行結果をユーザーに分かりやすく表示します：

```csv
# 出力例
COLUMN1,COLUMN2,COLUMN3
value1,value2,value3
value4,value5,value6
```

**表示内容**:
1. **CSV形式の結果**: ヘッダー行（カラム名）とデータ行
2. **サマリー情報**:
   - 取得した行数
   - 実行したクエリ（複雑な場合）
   - 実行時間（オプション）

**大量データの場合**:
- 結果が100行を超える場合は、最初の50行のみ表示
- 「結果が大量です。全データを表示しますか？」とユーザーに確認
- 必要に応じてファイル出力を提案

## 重要な注意事項

1. **日本語でコミュニケーション**: すべてのメッセージ、質問、エラー説明は日本語で行う

2. **データベースとスキーマの指定は必須**: Snowflakeではデータベースとスキーマが指定されていないとクエリエラーになる
   - クエリ内で完全修飾名（`database.schema.table`）を使用するのが最も確実
   - データベース名やスキーマ名が不明な場合は、ユーザーに必ず確認する

3. **クエリ確認**: 複雑なクエリや削除的な操作が含まれる可能性がある場合は、実行前にクエリをユーザーに表示して確認を取る

4. **LIMIT設定の徹底**: ユーザーが行数制限を指定していない場合は、安全性のため必ず`LIMIT 1000`を設定する

5. **エラー時の対応**: エラーが発生した場合は、原因を日本語で詳しく説明し、解決方法を提案する

6. **不明な点の確認**: テーブル名が曖昧、カラム名が不明、条件が複雑など、不明な点がある場合は実行前に必ずユーザーに確認する

7. **スキーマ情報の活用**: WHERE句やJOIN句を正確に生成するため、必要に応じてスキーマ情報を取得する

8. **Snowflake固有の知識**:
   - Snowflakeはデフォルトで識別子を大文字に変換する
   - 日時データは`TO_TIMESTAMP`や`TO_DATE`関数で適切に変換
   - VARIANT型（JSON）は`:`演算子でアクセス

## エラーハンドリング

各エラーケースに応じた対応方法：

| エラーケース | エラーメッセージ例 | 対応方法 |
|------------|------------------|---------|
| データベース/スキーマ未指定 | `Object does not exist` または `Cannot perform SELECT` | データベースとスキーマを明示的に指定する必要があることを説明し、完全修飾名（`database.schema.table`）を使用するか、`--database`と`--schema`オプションを追加することを提案 |
| テーブルが存在しない | `SQL compilation error: object does not exist` | `SHOW TABLES`で利用可能なテーブル一覧を表示し、ユーザーに正しいテーブル名を確認 |
| カラムが存在しない | `SQL compilation error: Invalid identifier` | `DESCRIBE TABLE`で有効なカラン一覧を表示し、クエリを修正 |
| 接続失敗 | `Connection refused` または `Could not connect` | Snowflake CLIの接続設定（`~/.snowflake/config.toml`または環境変数）を確認するようユーザーに案内 |
| 認証エラー | `Authentication failed` | 認証情報（ユーザー名、パスワード、ロール）の確認をユーザーに促す |
| クエリ構文エラー | `Syntax error in SQL statement` | 生成したクエリを確認し、構文を修正してから再実行 |
| snow未インストール | `command not found: snow` | Snowflake CLIのインストール手順を案内（`mise install pipx:snowflake-cli`など） |
| タイムアウト | `Timeout` または `Query execution timed out` | クエリが複雑すぎる可能性を説明し、WHERE句で絞り込むか、LIMIT値を小さくすることを提案 |
| 権限エラー | `Insufficient privileges` | 必要な権限（SELECT権限など）がないことを説明し、管理者に問い合わせるよう案内 |

エラーが発生した場合は、以下の手順で対応します：

1. エラーメッセージを解析
2. エラーの原因を日本語で分かりやすく説明
3. 解決方法を具体的に提案
4. 必要に応じて代替案を提示

## オプション引数と`snow sql`コマンド詳細

### `snow sql`コマンドの基本構文

```bash
snow sql [OPTIONS]
```

### 主要なオプション

#### クエリ実行オプション

| オプション | 短縮形 | 説明 |
|----------|-------|------|
| `--query` | `-q` | 実行するSQLクエリを直接指定 |
| `--filename` | `-f` | SQLファイルのパスを指定してファイル内のクエリを実行 |
| `--stdin` | `-i` | 標準入力からクエリを読み込む（パイプ利用時） |

```bash
# 直接クエリを実行
snow sql --query "SELECT * FROM users LIMIT 10;"

# SQLファイルを実行
snow sql --filename queries/report.sql

# パイプでクエリを渡す
cat query.sql | snow sql --stdin
```

#### 接続設定オプション

| オプション | 短縮形 | 説明 |
|----------|-------|------|
| `--connection` | `-c` | 接続名を指定（`~/.snowflake/config.toml`に定義）。デフォルトは"default" |
| `--account` | - | Snowflakeアカウント名を直接指定 |
| `--user` | - | ユーザー名を直接指定 |
| `--password` | - | パスワードを直接指定 |
| `--database` | - | 使用するデータベースを指定 |
| `--schema` | - | 使用するスキーマを指定 |
| `--role` | - | 使用するロールを指定 |
| `--warehouse` | - | 使用するウェアハウスを指定 |

```bash
# 接続名で接続
snow sql --query "SELECT * FROM users;" --connection prod_warehouse

# 接続パラメータを直接指定
snow sql --query "SELECT * FROM users;" \
  --account my_account \
  --user my_user \
  --database my_db \
  --schema public \
  --warehouse compute_wh
```

#### 出力形式オプション

| オプション | 指定可能な値 | 説明 |
|----------|------------|------|
| `--format` | TABLE, JSON, JSON_EXT, CSV | 出力形式を指定（デフォルト: TABLE） |

```bash
# CSV形式で出力（このスキルの標準形式）
snow sql --query "SELECT * FROM users;" --format CSV

# JSON形式で出力
snow sql --query "SELECT * FROM users;" --format JSON

# テーブル形式で出力（デフォルト）
snow sql --query "SELECT * FROM users;"
```

#### 変数・テンプレートオプション

| オプション | 短縮形 | 説明 |
|----------|-------|------|
| `--variable` | `-D` | key=value形式で変数を指定。SQLテンプレート内で使用可能 |
| `--enable-templating` | - | テンプレート構文を有効化（LEGACY, STANDARD, JINJA, ALL, NONE） |

```bash
# 変数を使用したクエリ実行
snow sql --query "SELECT * FROM &{table_name} WHERE age > &{min_age};" \
  --variable "table_name=users" \
  --variable "min_age=20"
```

#### グローバル設定オプション

| オプション | 短縮形 | 説明 |
|----------|-------|------|
| `--verbose` | `-v` | 詳細なログを表示 |
| `--debug` | - | デバッグログを表示 |
| `--silent` | - | 中間出力を非表示 |

```bash
# 詳細ログを有効にして実行
snow sql --query "SELECT * FROM users;" --verbose

# デバッグモードで実行
snow sql --query "SELECT * FROM users;" --debug
```

### このスキルで推奨する使用パターン

#### 基本的なクエリ実行
```bash
snow sql --query "SELECT * FROM table_name LIMIT 1000;" --format CSV
```

#### 接続を指定したクエリ実行
```bash
snow sql --query "SELECT * FROM table_name;" --format CSV --connection prod_warehouse
```

#### エラーハンドリング付き実行
```bash
if ! result=$(snow sql --query "$query" --format CSV 2>&1); then
    echo "エラー: クエリ実行に失敗しました"
    echo "$result"
    exit 1
fi
```

## 使用例

### 例1: 基本的なデータ取得

**ユーザー指示**: 「usersテーブルの全データを10件取得して」

**実行フロー**:
1. テーブル`users`の存在を確認
2. クエリ生成: `SELECT * FROM users LIMIT 10;`
3. 実行してCSV形式で表示

### 例2: 条件付き検索

**ユーザー指示**: 「25歳以上のユーザーで、東京に住んでいる人を表示して」

**実行フロー**:
1. `users`テーブルのスキーマ確認（`age`と`city`カラムの存在を確認）
2. クエリ生成: `SELECT * FROM users WHERE age >= 25 AND city = '東京' LIMIT 1000;`
3. 実行してCSV形式で表示

### 例3: 集計クエリ

**ユーザー指示**: 「部署ごとの平均給与を計算して」

**実行フロー**:
1. `employees`テーブルのスキーマ確認
2. クエリ生成: `SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department ORDER BY avg_salary DESC;`
3. 実行してCSV形式で表示

### 例4: 接続指定

**ユーザー指示**: 「--connection prod_warehouse で ordersテーブルの最新10件を取得」

**実行フロー**:
1. 接続名`prod_warehouse`を確認
2. クエリ生成: `SELECT * FROM orders ORDER BY created_at DESC LIMIT 10;`
3. `snow sql --connection prod_warehouse --format CSV`で実行

## Snowflake固有の考慮事項

### 識別子の大文字小文字

Snowflakeはデフォルトで識別子を大文字に変換します：

```sql
-- これらは同じテーブルを参照
SELECT * FROM users;
SELECT * FROM USERS;
SELECT * FROM Users;

-- ダブルクォートで囲むと大文字小文字が区別される
SELECT * FROM "users";  -- 小文字のusersテーブル
```

### 日時データの扱い

日時データは適切な関数で変換します：

```sql
-- 日付文字列をTIMESTAMP型に変換
SELECT * FROM orders WHERE created_at >= TO_TIMESTAMP('2024-01-01 00:00:00');

-- 月ごとに集計
SELECT DATE_TRUNC('month', created_at), COUNT(*)
FROM orders
GROUP BY DATE_TRUNC('month', created_at);
```

### VARIANT型（JSON）のアクセス

VARIANT型のカラムには`:`演算子でアクセスします：

```sql
-- JSONカラムの特定フィールドを取得
SELECT data:name::STRING, data:age::NUMBER
FROM users
WHERE data:active::BOOLEAN = TRUE;
```

## schema.jsonの管理方法

### 初回セットアップ

**重要**: `schema.json`は機密情報（データベース構造）を含むため、Gitで管理されません（.gitignoreに追加済み）。

初めて使用する際は、サンプルファイルからコピーして作成します：

```bash
cd claude/skills/snowflake-query

# サンプルファイルからコピー
cp schema.json.example schema.json

# または、自動生成スクリプトで実際のSnowflakeから取得
python3 generate-schema.py --connection your_connection
```

**ファイルの違い**:
- **schema.json.example**: サンプルテーブル定義が含まれたテンプレート（Git管理対象）
- **schema.json**: 実際のSnowflakeテーブル構造（Git管理対象外、ローカルのみ）

### スキーマファイルの編集

`claude/skills/snowflake-query/schema.json`ファイルを手動で編集して、実際のSnowflakeテーブル構造を反映させます。

#### 新しいテーブルを追加する手順

1. **schema.jsonを開く**

2. **`tables`オブジェクトに新しいテーブルを追加**:

```json
{
  "tables": {
    "existing_table": { ... },
    "new_table_name": {
      "description": "テーブルの説明",
      "schema": "PUBLIC",
      "columns": {
        "column1": {
          "type": "VARCHAR(255)",
          "nullable": false,
          "description": "カラムの説明"
        },
        "column2": {
          "type": "NUMBER(10,2)",
          "nullable": true,
          "description": "別のカラム"
        }
      },
      "sample_queries": [
        "SELECT * FROM new_table_name LIMIT 100;"
      ]
    }
  }
}
```

3. **ファイルを保存**

### スキーマ情報の自動取得（推奨）

`generate-schema.py`スクリプトを使って、Snowflakeから自動的にschema.jsonを生成できます。

**要件**: Snowflake CLI (`snow`コマンド)がインストールされている必要があります。
- インストール: `mise install pipx:snowflake-cli`

```bash
# デフォルト接続でPUBLICスキーマのすべてのテーブルを取得
cd claude/skills/snowflake-query
python3 generate-schema.py

# 接続名を指定
python3 generate-schema.py --connection prod_warehouse

# 特定のテーブルのみ取得
python3 generate-schema.py --tables users,orders,products

# スキーマを指定
python3 generate-schema.py --schema ANALYTICS

# 出力ファイルを指定
python3 generate-schema.py --output custom-schema.json

# すべてのオプションを組み合わせ
python3 generate-schema.py --connection prod --schema PUBLIC --tables users,orders --output my-schema.json
```

**スクリプトの機能**:
- `snow sql`コマンドを使用してSnowflakeに接続
- `SHOW TABLES`でテーブル一覧を取得
- 各テーブルの`DESCRIBE TABLE`を実行してカラム情報を取得
- JSON形式に自動変換してschema.jsonを生成
- 基本的なサンプルクエリも自動生成

**出力例**:
```
Snowflakeスキーマ情報を取得中...
スキーマ: PUBLIC
接続: prod_warehouse
取得するテーブル数: 3
テーブル users のスキーマ情報を取得中...
テーブル orders のスキーマ情報を取得中...
テーブル products のスキーマ情報を取得中...

完了！schema.json にスキーマ情報を保存しました。
取得したテーブル数: 3
```

### 手動でのスキーマ情報取得

スクリプトを使わず手動で取得する場合：

```bash
# 1. テーブル一覧を取得
snow sql --query "SHOW TABLES IN SCHEMA PUBLIC;" --format CSV

# 2. 特定のテーブルの構造を取得
snow sql --query "DESCRIBE TABLE table_name;" --format CSV

# 3. 取得した情報をschema.jsonのフォーマットに変換して追加
```

### schema.jsonのバージョン管理

**重要**: `schema.json`はGitで管理しません（.gitignoreに追加済み）。

理由：
- データベース構造が外部に露呈するリスクを避ける
- 企業の機密情報を含む可能性がある
- 環境ごとに異なるスキーマ構成に対応

**代わりに**:
- `schema.json.example`（サンプルファイル）のみGit管理
- 実際の`schema.json`は各環境でローカルに作成・管理
- チーム内で共有する場合は、セキュアな方法（社内wiki、暗号化されたストレージなど）を使用

```bash
# schema.json.exampleは管理対象
git add claude/skills/snowflake-query/schema.json.example
git commit -m "Update schema.json.example template"

# schema.json自体は管理されない（.gitignoreで除外済み）
git status  # schema.jsonは表示されない
```

### ベストプラクティス

1. **よく使うテーブルのみ記載**: すべてのテーブルを記載する必要はありません。頻繁にクエリするテーブルのみschema.jsonに追加します。

2. **説明を充実させる**: `description`フィールドには、テーブルやカラムの用途を分かりやすく記載します。

3. **サンプルクエリを追加**: `sample_queries`には、そのテーブルでよく使うクエリのパターンを記載しておくと便利です。

4. **定期的に更新**: Snowflakeのテーブル構造が変更された場合は、schema.jsonも更新します。

5. **データ型の正確性**: Snowflakeのデータ型を正確に記載します（`NUMBER(38,0)`, `VARCHAR(255)`, `TIMESTAMP_NTZ(9)` など）。

### サンプルschema.jsonの内容

デフォルトのschema.jsonには以下のサンプルテーブルが含まれています：

- **users**: ユーザー情報テーブル
- **orders**: 注文情報テーブル
- **products**: 商品情報テーブル

これらは例として記載されているため、実際のSnowflakeデータベースに合わせて編集または削除してください。
