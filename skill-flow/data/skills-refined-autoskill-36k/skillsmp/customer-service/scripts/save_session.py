#!/usr/bin/env python3
"""
Save a customer service call session review to history.

Usage:
    uv run save_session.py --session-id <id> --product <name> --customer <name> --operator <name> --review '<json>'
"""

import sys
import json
from pathlib import Path
from datetime import datetime


HISTORY_DIR = Path(".ezagent/database/customer_service/history")


def save_session(session_id: str, product: str, customer: str, operator: str, review: dict) -> Path:
    """Save session review to history."""
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    session_dir = HISTORY_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    # Build session data
    session_data = {
        'session_id': session_id,
        'product': product,
        'customer': customer,
        'operator': operator,
        'timestamp': datetime.now().isoformat(),
        'review': review
    }

    # Save JSON
    with open(session_dir / 'session.json', 'w', encoding='utf-8') as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    # Save readable markdown
    with open(session_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(f"# Customer Service Session: {session_id}\n\n")
        f.write(f"**Date**: {session_data['timestamp']}\n\n")
        f.write(f"**Product/Service**: {product}\n\n")
        f.write(f"**Customer Persona**: {customer}\n\n")
        f.write(f"**Service Strategy**: {operator}\n\n")
        f.write("## Review\n\n")

        if isinstance(review, dict):
            for key, value in review.items():
                f.write(f"### {key.replace('_', ' ').title()}\n\n")
                if isinstance(value, list):
                    for item in value:
                        f.write(f"- {item}\n")
                else:
                    f.write(f"{value}\n")
                f.write("\n")
        else:
            f.write(str(review))

    print(f"Session saved to: {session_dir}")
    return session_dir


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Save customer service session review')
    parser.add_argument('--session-id', required=True)
    parser.add_argument('--product', required=True)
    parser.add_argument('--customer', required=True)
    parser.add_argument('--operator', required=True)
    parser.add_argument('--review', required=True, help='JSON review data')

    args = parser.parse_args()

    try:
        review = json.loads(args.review)
        save_session(args.session_id, args.product, args.customer, args.operator, review)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
