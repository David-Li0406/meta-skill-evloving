#!/usr/bin/env python3
"""
Script: calculate.py
Purpose: Perform basic mathematical operations

Usage:
    python calculate.py --operation add --a 5 --b 3
    python calculate.py --operation multiply --a 7 --b 6

Arguments:
    --operation   Math operation: add, subtract, multiply, divide
    --a           First number (required)
    --b           Second number (required)

Exit Codes:
    0 - Success
    1 - Invalid arguments
    3 - Processing error (e.g., division by zero)

Example Output:
    {"status": "success", "operation": "add", "a": 5, "b": 3, "result": 8}
"""

import argparse
import json
import sys


def calculate(operation: str, a: float, b: float) -> float:
    """Perform the specified mathematical operation."""
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else None,
    }

    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")

    result = operations[operation](a, b)
    if result is None:
        raise ZeroDivisionError("Cannot divide by zero")

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Perform basic mathematical operations"
    )
    parser.add_argument(
        "--operation",
        required=True,
        choices=["add", "subtract", "multiply", "divide"],
        help="Math operation to perform",
    )
    parser.add_argument("--a", required=True, type=float, help="First number")
    parser.add_argument("--b", required=True, type=float, help="Second number")
    args = parser.parse_args()

    try:
        result = calculate(args.operation, args.a, args.b)
        output = {
            "status": "success",
            "operation": args.operation,
            "a": args.a,
            "b": args.b,
            "result": result,
        }
        print(json.dumps(output, indent=2))
        sys.exit(0)
    except ZeroDivisionError as e:
        error = {"status": "error", "code": 3, "message": str(e)}
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(3)
    except Exception as e:
        error = {"status": "error", "code": 1, "message": str(e)}
        print(json.dumps(error, indent=2), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
