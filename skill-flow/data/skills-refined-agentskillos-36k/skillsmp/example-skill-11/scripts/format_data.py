#!/usr/bin/env python3
"""
Script: format_data.py
Purpose: Convert data between different formats

Usage:
    python format_data.py --input data.json --format yaml
    python format_data.py --input '{"key": "value"}' --format table
    echo '{"name": "test"}' | python format_data.py --format yaml

Arguments:
    --input   Input file path OR JSON string (optional, reads stdin if omitted)
    --format  Output format: json, yaml, table, csv (default: json)
    --pretty  Enable pretty printing (default: true)

Exit Codes:
    0 - Success
    1 - Invalid arguments
    2 - Input not found
    3 - Processing error

Example Output (table format):
    {"status": "success", "format": "table", "output": "| key   | value |\\n|-------|-------|"}
"""

import argparse
import json
import sys
from pathlib import Path


def load_input(input_arg: str | None) -> dict:
    """Load input from file, string, or stdin."""
    if input_arg is None:
        # Read from stdin
        data = sys.stdin.read().strip()
        if not data:
            raise ValueError("No input provided via stdin")
        return json.loads(data)

    # Try as file path first
    path = Path(input_arg)
    if path.exists():
        return json.loads(path.read_text())

    # Try as JSON string
    try:
        return json.loads(input_arg)
    except json.JSONDecodeError:
        raise ValueError(f"Input is neither a valid file nor JSON: {input_arg}")


def format_as_table(data: dict) -> str:
    """Convert dict to markdown table."""
    if not data:
        return "| (empty) |"

    # Handle nested data by converting to string
    rows = []
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        rows.append(f"| {key} | {value} |")

    header = "| Key | Value |"
    separator = "|-----|-------|"
    return "\n".join([header, separator] + rows)


def format_as_csv(data: dict) -> str:
    """Convert dict to CSV format."""
    if not data:
        return "key,value"

    lines = ["key,value"]
    for key, value in data.items():
        if isinstance(value, (dict, list)):
            value = json.dumps(value).replace('"', '""')
            value = f'"{value}"'
        lines.append(f"{key},{value}")
    return "\n".join(lines)


def format_as_yaml(data: dict) -> str:
    """Convert dict to YAML-like format (simple implementation)."""

    def to_yaml(obj, indent=0):
        lines = []
        prefix = "  " * indent
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{prefix}{key}:")
                    lines.append(to_yaml(value, indent + 1))
                else:
                    lines.append(f"{prefix}{key}: {value}")
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    lines.append(f"{prefix}-")
                    lines.append(to_yaml(item, indent + 1))
                else:
                    lines.append(f"{prefix}- {item}")
        return "\n".join(lines)

    return to_yaml(data)


def format_data(data: dict, output_format: str, pretty: bool = True) -> str:
    """Format data to the specified output format."""
    formatters = {
        "json": lambda d: json.dumps(d, indent=2 if pretty else None),
        "yaml": format_as_yaml,
        "table": format_as_table,
        "csv": format_as_csv,
    }

    if output_format not in formatters:
        raise ValueError(f"Unknown format: {output_format}")

    return formatters[output_format](data)


def main():
    parser = argparse.ArgumentParser(description="Convert data between formats")
    parser.add_argument(
        "--input", help="Input file path or JSON string (reads stdin if omitted)"
    )
    parser.add_argument(
        "--format",
        choices=["json", "yaml", "table", "csv"],
        default="json",
        help="Output format (default: json)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=True,
        help="Enable pretty printing",
    )
    args = parser.parse_args()

    try:
        data = load_input(args.input)
        formatted = format_data(data, args.format, args.pretty)
        result = {
            "status": "success",
            "format": args.format,
            "output": formatted,
        }
        print(json.dumps(result, indent=2))
        sys.exit(0)
    except FileNotFoundError as e:
        error = {"status": "error", "code": 2, "message": f"File not found: {e}"}
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(2)
    except json.JSONDecodeError as e:
        error = {"status": "error", "code": 3, "message": f"Invalid JSON: {e}"}
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        error = {"status": "error", "code": 3, "message": str(e)}
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(3)


if __name__ == "__main__":
    main()
