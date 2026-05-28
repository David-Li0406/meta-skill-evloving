#!/usr/bin/env python3
"""
Snowflakeのテーブルスキーマ情報を取得してschema.jsonを生成するスクリプト

要件:
    - Snowflake CLI (snow)がインストールされている必要があります
    - インストール: mise install pipx:snowflake-cli

使用例:
    # デフォルト接続を使用
    python3 generate-schema.py

    # 接続名を指定
    python3 generate-schema.py --connection prod_warehouse

    # 特定のスキーマを指定
    python3 generate-schema.py --schema PUBLIC

    # 特定のテーブルのみ
    python3 generate-schema.py --tables users,orders,products

    # 出力ファイルを指定
    python3 generate-schema.py --output my-schema.json
"""

import subprocess
import json
import argparse
import sys
from typing import Dict, List, Optional


def run_snowsql(query: str, connection: Optional[str] = None) -> str:
    """snow sqlコマンドを実行してJSON形式で結果を取得"""
    cmd = ["snow", "sql", "--query", query, "--format", "JSON"]
    if connection:
        cmd.extend(["--connection", connection])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"エラー: snow sqlコマンドの実行に失敗しました", file=sys.stderr)
        print(f"エラー内容: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("エラー: snowコマンドが見つかりません。Snowflake CLIをインストールしてください。", file=sys.stderr)
        print("インストール: mise install pipx:snowflake-cli", file=sys.stderr)
        sys.exit(1)


def parse_json(json_output: str) -> List[Dict[str, str]]:
    """JSON出力をパースして辞書のリストに変換"""
    if not json_output.strip():
        return []

    try:
        data = json.loads(json_output)
        # JSONデータは既に辞書のリスト形式
        return data if isinstance(data, list) else []
    except json.JSONDecodeError as e:
        print(f"警告: JSON出力のパースに失敗しました: {e}", file=sys.stderr)
        return []


def get_tables(schema: str, connection: Optional[str] = None, specific_tables: Optional[List[str]] = None) -> List[str]:
    """スキーマ内のテーブル一覧を取得"""
    if specific_tables:
        return specific_tables

    query = f"SHOW TABLES IN SCHEMA {schema};"
    json_output = run_snowsql(query, connection)
    rows = parse_json(json_output)

    # テーブル名を抽出（'name'カラムから）
    tables = [row.get('name', row.get('NAME', '')) for row in rows if row.get('name') or row.get('NAME')]
    return tables


def get_table_description(table_name: str, schema: str, connection: Optional[str] = None) -> Dict:
    """テーブルの構造情報を取得"""
    query = f"DESCRIBE TABLE {schema}.{table_name};"
    json_output = run_snowsql(query, connection)
    rows = parse_json(json_output)

    columns = {}
    for row in rows:
        column_name = row.get('name', row.get('NAME', ''))
        column_type = row.get('type', row.get('TYPE', ''))
        nullable = row.get('null?', row.get('NULL?', 'Y'))
        default = row.get('default', row.get('DEFAULT', ''))
        comment = row.get('comment', row.get('COMMENT', ''))
        primary_key = row.get('primary key', row.get('PRIMARY KEY', 'N'))

        if not column_name:
            continue

        column_info = {
            "type": column_type,
            "nullable": nullable.upper() == 'Y',
            "description": comment if comment else f"{column_name}カラム"
        }

        if default:
            column_info["default"] = default

        if primary_key.upper() == 'Y':
            column_info["primary_key"] = True

        columns[column_name.lower()] = column_info

    return columns


def generate_sample_queries(table_name: str, columns: Dict) -> List[str]:
    """テーブルの基本的なサンプルクエリを生成"""
    queries = [
        f"SELECT * FROM {table_name} LIMIT 100;",
    ]

    # 日付カラムがあればソート付きクエリを追加
    date_columns = [col for col, info in columns.items() if 'TIMESTAMP' in info['type'].upper() or 'DATE' in info['type'].upper()]
    if date_columns:
        date_col = date_columns[0]
        queries.append(f"SELECT * FROM {table_name} ORDER BY {date_col} DESC LIMIT 100;")

    # 数値カラムがあれば集計クエリを追加
    numeric_columns = [col for col, info in columns.items() if 'NUMBER' in info['type'].upper() or 'INT' in info['type'].upper()]
    if numeric_columns and len(columns) > 1:
        first_col = list(columns.keys())[0]
        queries.append(f"SELECT {first_col}, COUNT(*) FROM {table_name} GROUP BY {first_col} LIMIT 10;")

    return queries


def generate_schema_json(schema: str, tables: List[str], connection: Optional[str] = None) -> Dict:
    """schema.jsonの構造を生成"""
    schema_data = {
        "$schema": "https://json-schema.org/draft-07/schema#",
        "description": f"Snowflake {schema}スキーマのテーブル定義",
        "tables": {}
    }

    for table in tables:
        print(f"テーブル {table} のスキーマ情報を取得中...", file=sys.stderr)

        try:
            columns = get_table_description(table, schema, connection)
            sample_queries = generate_sample_queries(table, columns)

            schema_data["tables"][table.lower()] = {
                "description": f"{table}テーブル",
                "schema": schema,
                "columns": columns,
                "sample_queries": sample_queries
            }
        except Exception as e:
            print(f"警告: テーブル {table} の取得に失敗しました: {e}", file=sys.stderr)
            continue

    # notes セクションを追加
    schema_data["notes"] = {
        "usage": "このスキーマファイルはSnowflakeクエリ実行スキルが参照します。",
        "generated_by": "generate-schema.py",
        "data_types": [
            "NUMBER(precision, scale) - 数値型",
            "VARCHAR(length) - 可変長文字列",
            "TEXT - 長い文字列",
            "BOOLEAN - 真偽値",
            "TIMESTAMP_NTZ - タイムゾーンなしタイムスタンプ",
            "TIMESTAMP_LTZ - ローカルタイムゾーンタイムスタンプ",
            "TIMESTAMP_TZ - タイムゾーン付きタイムスタンプ",
            "DATE - 日付",
            "TIME - 時刻",
            "VARIANT - JSON等の半構造化データ",
            "ARRAY - 配列型",
            "OBJECT - オブジェクト型"
        ]
    }

    return schema_data


def main():
    parser = argparse.ArgumentParser(
        description="Snowflakeのテーブルスキーマ情報を取得してschema.jsonを生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # デフォルト接続、PUBLICスキーマのすべてのテーブル
  python3 generate-schema.py

  # 接続名を指定
  python3 generate-schema.py --connection prod_warehouse

  # 特定のテーブルのみ
  python3 generate-schema.py --tables users,orders,products

  # 出力ファイルを指定
  python3 generate-schema.py --output my-schema.json
        """
    )

    parser.add_argument(
        '--connection', '-c',
        help='Snowflake接続名（~/.snowflake/config.tomlで定義された接続）',
        default=None
    )

    parser.add_argument(
        '--schema', '-s',
        help='対象スキーマ名（デフォルト: PUBLIC）',
        default='PUBLIC'
    )

    parser.add_argument(
        '--tables', '-t',
        help='取得するテーブル名（カンマ区切り）。指定しない場合はすべてのテーブル',
        default=None
    )

    parser.add_argument(
        '--output', '-o',
        help='出力ファイル名（デフォルト: schema.json）',
        default='schema.json'
    )

    args = parser.parse_args()

    # テーブルリストの処理
    specific_tables = None
    if args.tables:
        specific_tables = [t.strip() for t in args.tables.split(',')]

    print(f"Snowflakeスキーマ情報を取得中...", file=sys.stderr)
    print(f"スキーマ: {args.schema}", file=sys.stderr)
    if args.connection:
        print(f"接続: {args.connection}", file=sys.stderr)

    # テーブル一覧を取得
    tables = get_tables(args.schema, args.connection, specific_tables)

    if not tables:
        print("エラー: テーブルが見つかりませんでした", file=sys.stderr)
        sys.exit(1)

    print(f"取得するテーブル数: {len(tables)}", file=sys.stderr)

    # スキーマJSONを生成
    schema_data = generate_schema_json(args.schema, tables, args.connection)

    # ファイルに出力
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(schema_data, f, ensure_ascii=False, indent=2)

    print(f"\n完了！{args.output} にスキーマ情報を保存しました。", file=sys.stderr)
    print(f"取得したテーブル数: {len(schema_data['tables'])}", file=sys.stderr)


if __name__ == '__main__':
    main()
