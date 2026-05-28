#!/usr/bin/env python3
"""
List records in customer service database.

Usage:
    uv run list_records.py [--type <product|customer|operator|all>] [--verbose]
"""

import sys
import json
from pathlib import Path


BASE_DIR = Path(".ezagent/database/customer_service")


def list_records(item_type: str = "all", verbose: bool = False) -> dict:
    """List records of specified type."""
    type_map = {
        'product': 'products',
        'customer': 'customers',
        'operator': 'operators'
    }

    results = {}

    types_to_list = [item_type] if item_type != "all" else ['product', 'customer', 'operator']

    for t in types_to_list:
        dir_name = type_map[t]
        dir_path = BASE_DIR / dir_name

        items = []
        if dir_path.exists():
            for item_dir in sorted(dir_path.iterdir()):
                if item_dir.is_dir():
                    info_file = item_dir / 'info.json'
                    if info_file.exists():
                        with open(info_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if verbose:
                                items.append(data)
                            else:
                                items.append({
                                    'name': data.get('name', 'unnamed'),
                                    'id': data.get('_id', ''),
                                    'created': data.get('_created', '')
                                })

        results[t] = items

    return results


def print_results(results: dict, verbose: bool = False):
    """Print results in formatted output."""
    type_labels = {
        'product': '产品/服务',
        'customer': '客户角色',
        'operator': '客服策略'
    }

    for item_type, items in results.items():
        label = type_labels.get(item_type, item_type)
        print(f"\n## {label} ({len(items)})")
        print("-" * 40)

        if not items:
            print("(空)")
            continue

        for i, item in enumerate(items, 1):
            if verbose:
                print(f"\n### {i}. {item.get('name', 'unnamed')}")
                for key, value in item.items():
                    if not key.startswith('_'):
                        if isinstance(value, list):
                            print(f"  {key}:")
                            for v in value:
                                print(f"    - {v}")
                        else:
                            print(f"  {key}: {value}")
            else:
                name = item.get('name', 'unnamed')
                item_id = item.get('id', '')
                created = item.get('created', '')[:10] if item.get('created') else ''
                print(f"  {i}. {name} (ID: {item_id}, 创建: {created})")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='List customer service records')
    parser.add_argument('--type', choices=['product', 'customer', 'operator', 'all'],
                        default='all', help='Type of records to list')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show detailed information')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')

    args = parser.parse_args()

    try:
        results = list_records(args.type, args.verbose)

        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print_results(results, args.verbose)

            # Summary
            total = sum(len(items) for items in results.values())
            print(f"\n总计: {total} 条记录")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
