"""
Numeric comparison evaluators.
"""
from pathlib import Path
from typing import Dict, Any, Tuple, List

from ...registry import evaluator
from ...utils.file_utils import read_json, get_nested_value


@evaluator("json_array_length")
async def eval_json_array_length(workspace: Path, op_args: Dict[str, Any],
                                 value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Check the length of a JSON array.

    op_args:
        path: Path to JSON file
        array_path: Dot-separated path to the array (e.g., "coefficients" or "data.items")
        operator: Comparison operator ("==", ">=", "<=", ">", "<") default: "=="
        expected: Expected length value
    """
    path = op_args["path"]
    array_path = op_args["array_path"]
    operator = op_args.get("operator", "==")
    expected = op_args["expected"]

    data = read_json(workspace, path)
    if data is None:
        return False, f"Cannot read JSON: {path}"

    arr = get_nested_value(data, array_path)
    if arr is None:
        return False, f"Array path not found: {array_path}"

    if not isinstance(arr, list):
        return False, f"'{array_path}' is not an array"

    actual = len(arr)

    if operator in ("==", "eq"):
        passed = actual == expected
    elif operator in (">=", "gte"):
        passed = actual >= expected
    elif operator in ("<=", "lte"):
        passed = actual <= expected
    elif operator in (">", "gt"):
        passed = actual > expected
    elif operator in ("<", "lt"):
        passed = actual < expected
    else:
        return False, f"Unknown operator: {operator}"

    if passed:
        return True, ""
    return False, f"Array '{array_path}' has {actual} items, expected {operator} {expected}"


@evaluator("json_field_numeric_compare")
async def eval_json_field_numeric_compare(workspace: Path, op_args: Dict[str, Any],
                                          value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Compare a numeric value from a JSON field against an expected value.

    op_args:
        path: Path to JSON file
        json_path: Dot-separated path to the value (e.g., "optimal_solution.x_A")
        operator: Comparison operator ("abs_diff", "eq", "gt", "lt", "gte", "lte", "in_range")
        expected: Expected numeric value, or {"min": ..., "max": ...} for in_range
        tolerance: Tolerance for abs_diff comparison (default: 0.01)
    """
    path = op_args["path"]
    json_path = op_args["json_path"]
    operator = op_args.get("operator", "abs_diff")
    expected = op_args["expected"]
    tolerance = op_args.get("tolerance", 0.01)

    data = read_json(workspace, path)
    if data is None:
        return False, f"Cannot read JSON: {path}"

    actual = get_nested_value(data, json_path)
    if actual is None:
        return False, f"Key not found: {json_path}"

    if not isinstance(actual, (int, float)):
        return False, f"Value at {json_path} is not numeric: {type(actual).__name__}"

    if operator == "abs_diff":
        passed = abs(actual - expected) <= tolerance
        if passed:
            return True, ""
        return False, f"abs({actual} - {expected}) = {abs(actual - expected):.4f} > tolerance {tolerance}"
    elif operator in ("eq", "=="):
        passed = actual == expected
    elif operator in ("gt", ">"):
        passed = actual > expected
    elif operator in ("lt", "<"):
        passed = actual < expected
    elif operator in ("gte", ">="):
        passed = actual >= expected
    elif operator in ("lte", "<="):
        passed = actual <= expected
    elif operator == "in_range":
        min_val = expected.get("min", float("-inf"))
        max_val = expected.get("max", float("inf"))
        passed = min_val <= actual <= max_val
        if passed:
            return True, ""
        return False, f"Value {actual} not in range [{min_val}, {max_val}]"
    else:
        return False, f"Unknown operator: {operator}"

    if passed:
        return True, ""
    return False, f"Comparison failed: {actual} {operator} {expected}"
