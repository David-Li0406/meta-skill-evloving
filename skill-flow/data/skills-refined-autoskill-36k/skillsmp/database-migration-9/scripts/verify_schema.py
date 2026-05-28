#!/usr/bin/env python3
"""
Schema Verification Tool

Verifies database schema matches expected state after migration.

Usage:
    python verify_schema.py --table users --expected-columns id,name,email,status
    python verify_schema.py --table users --expected-indexes idx_email,idx_status
    python verify_schema.py --config schema_config.json

Examples:
    # Verify specific columns exist
    python verify_schema.py --table users --expected-columns "id,name,email"

    # Verify exact column types
    python verify_schema.py --table users --verify-types '{"id": "int", "name": "varchar(100)"}'

    # Verify indexes
    python verify_schema.py --table users --expected-indexes idx_email

    # Full schema verification from config
    python verify_schema.py --config migrations/schema_users.json

Config file format (schema_users.json):
{
    "table": "users",
    "columns": {
        "id": {"type": "int", "nullable": false, "key": "PRI"},
        "name": {"type": "varchar(100)", "nullable": true},
        "email": {"type": "varchar(255)", "nullable": true},
        "status": {"type": "enum('active','inactive')", "nullable": true, "default": "active"}
    },
    "indexes": ["idx_email", "idx_status"]
}
"""

import argparse
import json
import sys
import os
from typing import Dict, List, Optional, Tuple

try:
    import pymysql
except ImportError:
    print("ERROR: pymysql not installed")
    print("Install: pip install pymysql")
    sys.exit(1)


class SchemaVerifier:
    """Verify database schema matches expected state"""

    def __init__(self, host: str = "localhost", port: int = 3307,
                 user: str = "admin", password: str = None, database: str = None):
        """Initialize database connection"""
        if not password:
            password = os.getenv("AURORA_PASSWORD")
        if not database:
            database = os.getenv("AURORA_DATABASE", "dr_daily_report")

        if not password:
            raise ValueError("Password required (set AURORA_PASSWORD env var)")

        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_table_columns(self, table: str) -> Dict[str, Dict]:
        """Get current table columns with metadata"""
        with self.conn.cursor() as cursor:
            cursor.execute(f"DESCRIBE {table}")
            columns = cursor.fetchall()

        return {
            row['Field']: {
                'type': row['Type'],
                'nullable': row['Null'] == 'YES',
                'key': row['Key'],
                'default': row['Default'],
                'extra': row['Extra']
            }
            for row in columns
        }

    def get_table_indexes(self, table: str) -> List[str]:
        """Get current table indexes"""
        with self.conn.cursor() as cursor:
            cursor.execute(f"SHOW INDEX FROM {table}")
            indexes = cursor.fetchall()

        # Return unique index names (excluding PRIMARY)
        return list(set(
            row['Key_name']
            for row in indexes
            if row['Key_name'] != 'PRIMARY'
        ))

    def verify_columns_exist(self, table: str, expected_columns: List[str]) -> Tuple[bool, List[str]]:
        """Verify expected columns exist"""
        current_columns = self.get_table_columns(table)
        missing = [col for col in expected_columns if col not in current_columns]

        if missing:
            return False, missing
        return True, []

    def verify_column_types(self, table: str, expected_types: Dict[str, str]) -> Tuple[bool, Dict]:
        """Verify column types match expected"""
        current_columns = self.get_table_columns(table)
        mismatches = {}

        for col, expected_type in expected_types.items():
            if col not in current_columns:
                mismatches[col] = {'expected': expected_type, 'actual': 'MISSING'}
            elif current_columns[col]['type'] != expected_type:
                mismatches[col] = {
                    'expected': expected_type,
                    'actual': current_columns[col]['type']
                }

        if mismatches:
            return False, mismatches
        return True, {}

    def verify_indexes_exist(self, table: str, expected_indexes: List[str]) -> Tuple[bool, List[str]]:
        """Verify expected indexes exist"""
        current_indexes = self.get_table_indexes(table)
        missing = [idx for idx in expected_indexes if idx not in current_indexes]

        if missing:
            return False, missing
        return True, []

    def verify_full_schema(self, config: Dict) -> Dict:
        """Verify complete schema from config"""
        table = config['table']
        results = {
            'table': table,
            'passed': True,
            'errors': []
        }

        # Verify table exists
        try:
            self.get_table_columns(table)
        except pymysql.err.ProgrammingError:
            results['passed'] = False
            results['errors'].append(f"Table {table} does not exist")
            return results

        # Verify columns
        if 'columns' in config:
            expected_columns = list(config['columns'].keys())
            passed, missing = self.verify_columns_exist(table, expected_columns)
            if not passed:
                results['passed'] = False
                results['errors'].append(f"Missing columns: {', '.join(missing)}")

            # Verify column types
            expected_types = {
                col: meta.get('type')
                for col, meta in config['columns'].items()
                if 'type' in meta
            }
            passed, mismatches = self.verify_column_types(table, expected_types)
            if not passed:
                results['passed'] = False
                for col, mismatch in mismatches.items():
                    results['errors'].append(
                        f"Column {col}: expected {mismatch['expected']}, "
                        f"got {mismatch['actual']}"
                    )

            # Verify nullable constraints
            current_columns = self.get_table_columns(table)
            for col, meta in config['columns'].items():
                if 'nullable' in meta and col in current_columns:
                    expected_nullable = meta['nullable']
                    actual_nullable = current_columns[col]['nullable']
                    if expected_nullable != actual_nullable:
                        results['passed'] = False
                        results['errors'].append(
                            f"Column {col}: expected nullable={expected_nullable}, "
                            f"got {actual_nullable}"
                        )

        # Verify indexes
        if 'indexes' in config:
            passed, missing = self.verify_indexes_exist(table, config['indexes'])
            if not passed:
                results['passed'] = False
                results['errors'].append(f"Missing indexes: {', '.join(missing)}")

        return results

    def print_current_schema(self, table: str):
        """Print current table schema (for debugging)"""
        print(f"\n=== Current Schema: {table} ===\n")

        # Columns
        columns = self.get_table_columns(table)
        print("Columns:")
        for col, meta in columns.items():
            nullable = "NULL" if meta['nullable'] else "NOT NULL"
            default = f"DEFAULT {meta['default']}" if meta['default'] else ""
            key = f"[{meta['key']}]" if meta['key'] else ""
            print(f"  {col}: {meta['type']} {nullable} {default} {key}")

        # Indexes
        indexes = self.get_table_indexes(table)
        print(f"\nIndexes: {', '.join(indexes) if indexes else 'None'}")

    def close(self):
        """Close database connection"""
        self.conn.close()


def main():
    parser = argparse.ArgumentParser(description="Verify database schema after migration")
    parser.add_argument('--table', help="Table name to verify")
    parser.add_argument('--expected-columns', help="Comma-separated list of expected columns")
    parser.add_argument('--expected-indexes', help="Comma-separated list of expected indexes")
    parser.add_argument('--verify-types', help="JSON dict of column:type to verify")
    parser.add_argument('--config', help="JSON config file with full schema definition")
    parser.add_argument('--show-current', action='store_true',
                        help="Print current schema (for debugging)")
    parser.add_argument('--host', default='localhost', help="Database host")
    parser.add_argument('--port', type=int, default=3307, help="Database port")
    parser.add_argument('--user', default='admin', help="Database user")
    parser.add_argument('--database', help="Database name")

    args = parser.parse_args()

    # Connect to database
    try:
        verifier = SchemaVerifier(
            host=args.host,
            port=args.port,
            user=args.user,
            database=args.database
        )
    except Exception as e:
        print(f"ERROR: Failed to connect to database: {e}")
        sys.exit(1)

    try:
        # Show current schema (debug mode)
        if args.show_current:
            if not args.table:
                print("ERROR: --table required with --show-current")
                sys.exit(1)
            verifier.print_current_schema(args.table)
            sys.exit(0)

        # Full schema verification from config
        if args.config:
            with open(args.config) as f:
                config = json.load(f)

            results = verifier.verify_full_schema(config)

            print(f"\n=== Schema Verification: {results['table']} ===\n")
            if results['passed']:
                print("✅ PASSED: Schema matches expected state")
                sys.exit(0)
            else:
                print("❌ FAILED: Schema mismatches detected\n")
                for error in results['errors']:
                    print(f"  - {error}")
                sys.exit(1)

        # Individual verifications
        if not args.table:
            print("ERROR: --table required")
            parser.print_help()
            sys.exit(1)

        failed = False

        # Verify columns exist
        if args.expected_columns:
            columns = [c.strip() for c in args.expected_columns.split(',')]
            passed, missing = verifier.verify_columns_exist(args.table, columns)
            if passed:
                print(f"✅ All expected columns exist: {', '.join(columns)}")
            else:
                print(f"❌ Missing columns: {', '.join(missing)}")
                failed = True

        # Verify column types
        if args.verify_types:
            types = json.loads(args.verify_types)
            passed, mismatches = verifier.verify_column_types(args.table, types)
            if passed:
                print(f"✅ All column types match expected")
            else:
                print(f"❌ Column type mismatches:")
                for col, mismatch in mismatches.items():
                    print(f"  {col}: expected {mismatch['expected']}, got {mismatch['actual']}")
                failed = True

        # Verify indexes exist
        if args.expected_indexes:
            indexes = [i.strip() for i in args.expected_indexes.split(',')]
            passed, missing = verifier.verify_indexes_exist(args.table, indexes)
            if passed:
                print(f"✅ All expected indexes exist: {', '.join(indexes)}")
            else:
                print(f"❌ Missing indexes: {', '.join(missing)}")
                failed = True

        sys.exit(1 if failed else 0)

    finally:
        verifier.close()


if __name__ == '__main__':
    main()
