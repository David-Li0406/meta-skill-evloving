#!/usr/bin/env python3
"""
Save a single customer service record (product, customer, or operator) from user input.

Usage:
    uv run save_record.py --type <product|customer|operator> --data '<json_data>'
"""

import sys
import json
import hashlib
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(".ezagent/database/customer_service")


def generate_id(name: str) -> str:
    """Generate a short unique ID."""
    content = f"{name}{datetime.now().isoformat()}"
    return hashlib.md5(content.encode()).hexdigest()[:8]


def get_output_dir(item_type: str) -> Path:
    """Get output directory for item type."""
    type_map = {
        'product': 'products',
        'customer': 'customers',
        'operator': 'operators'
    }
    return BASE_DIR / type_map[item_type]


def save_record(item_type: str, data: dict) -> Path:
    """Save a record to its folder."""
    output_dir = get_output_dir(item_type)
    output_dir.mkdir(parents=True, exist_ok=True)

    name = data.get('name', data.get('product_name', data.get('customer_name', 'unnamed')))
    item_id = generate_id(name)
    folder_name = f"{item_id}_{name[:30].replace(' ', '_').replace('/', '_')}"

    item_dir = output_dir / folder_name
    item_dir.mkdir(parents=True, exist_ok=True)

    # Add metadata
    data['_id'] = item_id
    data['_type'] = item_type
    data['_created'] = datetime.now().isoformat()

    # Save as JSON
    with open(item_dir / 'info.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Save as readable markdown
    with open(item_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(f"# {name}\n\n")
        for key, value in data.items():
            if not key.startswith('_'):
                f.write(f"**{key.title()}**: {value}\n\n")

    print(f"Saved to: {item_dir}")
    return item_dir


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Save a customer service record')
    parser.add_argument('--type', choices=['product', 'customer', 'operator'], required=True)
    parser.add_argument('--data', required=True, help='JSON data string')

    args = parser.parse_args()

    try:
        data = json.loads(args.data)
        save_record(args.type, data)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
