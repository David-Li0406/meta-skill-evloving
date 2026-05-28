"""
Format validation evaluators.
"""
import math
from pathlib import Path
from typing import Dict, Any, Tuple, List, Optional

from ...registry import evaluator
from ...utils.file_utils import read_json, get_nested_value


@evaluator("json_valid")
async def eval_json_valid(workspace: Path, op_args: Dict[str, Any],
                          value: Any = None, **kwargs) -> Tuple[bool, str]:
    """Check if file is valid JSON."""
    path = op_args["path"]
    data = read_json(workspace, path)

    if data is not None:
        return True, ""
    return False, f"Invalid or missing JSON: {path}"


@evaluator("json_schema_valid")
async def eval_json_schema_valid(workspace: Path, op_args: Dict[str, Any],
                                 value: Dict[str, Any], **kwargs) -> Tuple[bool, str]:
    """
    Check if JSON file conforms to a JSON Schema.

    value: JSON Schema dictionary
    """
    try:
        import jsonschema
    except ImportError:
        return False, "jsonschema package not installed"

    path = op_args["path"]
    schema = value

    data = read_json(workspace, path)
    if data is None:
        return False, f"Cannot read JSON: {path}"

    try:
        jsonschema.validate(instance=data, schema=schema)
        return True, ""
    except jsonschema.ValidationError as e:
        return False, f"Schema validation failed: {e.message}"


@evaluator("json_has_keys")
async def eval_json_has_keys(workspace: Path, op_args: Dict[str, Any],
                             value: List[str], **kwargs) -> Tuple[bool, str]:
    """Check if JSON has all required keys."""
    path = op_args["path"]
    required_keys = value

    data = read_json(workspace, path)
    if data is None:
        return False, f"Cannot read JSON: {path}"

    if not isinstance(data, dict):
        return False, f"JSON root is not an object"

    missing = [k for k in required_keys if k not in data]
    if not missing:
        return True, ""
    return False, f"Missing keys: {missing}"


def _parse_complex(val) -> Optional[complex]:
    """Parse a complex number from various JSON representations."""
    if isinstance(val, (int, float)):
        return complex(val, 0)
    if isinstance(val, dict):
        re_part = val.get("real", val.get("re", 0))
        im_part = val.get("imag", val.get("im", val.get("imaginary", 0)))
        if isinstance(re_part, (int, float)) and isinstance(im_part, (int, float)):
            return complex(re_part, im_part)
    if isinstance(val, str):
        val = val.strip().replace(" ", "").replace("j", "i")
        if val.endswith("i"):
            num = val[:-1]
            if num in ("", "+"):
                return complex(0, 1)
            if num == "-":
                return complex(0, -1)
            try:
                return complex(0, float(num))
            except ValueError:
                pass
        s = val.replace("i", "j")
        try:
            return complex(s)
        except ValueError:
            pass
    if isinstance(val, list) and len(val) == 2:
        try:
            return complex(float(val[0]), float(val[1]))
        except (ValueError, TypeError):
            pass
    return None


def _match_item(item: dict, match: dict) -> bool:
    """Check if a dict item matches all criteria in match."""
    for field_path, condition in match.items():
        actual = get_nested_value(item, field_path)
        if actual is None:
            return False
        if isinstance(condition, dict) and "near" in condition:
            tol = condition.get("tolerance", 0.01)
            try:
                if abs(float(actual) - condition["near"]) > tol:
                    return False
            except (TypeError, ValueError):
                return False
        else:
            if actual != condition:
                return False
    return True


def _run_check(item: dict, check: dict) -> Tuple[bool, str]:
    """Run a single check against a matched item."""
    field = check.get("field")
    check_type = check["type"]
    expected = check.get("expected")
    tolerance = check.get("tolerance", 0.01)

    val = get_nested_value(item, field) if field else item
    if val is None:
        return False, f"Field '{field}' not found"

    if check_type == "contains":
        if expected in str(val).lower():
            return True, ""
        return False, f"'{field}' does not contain '{expected}', got '{val}'"

    elif check_type == "equals":
        if val == expected:
            return True, ""
        return False, f"'{field}' != {expected}, got {val}"

    elif check_type == "near":
        try:
            if abs(float(val) - expected) <= tolerance:
                return True, ""
            return False, f"'{field}' = {val}, expected ~{expected} (tol={tolerance})"
        except (TypeError, ValueError):
            return False, f"'{field}' is not numeric: {val}"

    elif check_type == "array_length":
        if not isinstance(val, list):
            return False, f"'{field}' is not an array"
        if len(val) == expected:
            return True, ""
        return False, f"'{field}' has {len(val)} items, expected {expected}"

    elif check_type == "sorted_reals_near":
        if not isinstance(val, list):
            return False, f"'{field}' is not an array"
        parsed = [_parse_complex(v) for v in val]
        parsed = [v for v in parsed if v is not None]
        if len(parsed) < len(expected):
            return False, f"Could not parse enough values from '{field}': {val}"
        reals = sorted([v.real for v in parsed])
        exp_sorted = sorted(expected)
        for i, (r, e) in enumerate(zip(reals, exp_sorted)):
            if abs(r - e) > tolerance:
                return False, f"Sorted real[{i}] = {r:.4f}, expected ~{e} (tol={tolerance})"
        if not all(abs(v.imag) < tolerance for v in parsed):
            return False, f"Values have non-zero imaginary parts: {[v.imag for v in parsed]}"
        return True, ""

    elif check_type == "purely_imaginary_magnitude_near":
        if not isinstance(val, list):
            return False, f"'{field}' is not an array"
        parsed = [_parse_complex(v) for v in val]
        parsed = [v for v in parsed if v is not None]
        if len(parsed) < 2:
            return False, f"Need at least 2 values, got {len(parsed)} from '{field}'"
        real_tol = check.get("real_tolerance", tolerance)
        if not all(abs(v.real) < real_tol for v in parsed):
            return False, f"Not purely imaginary - real parts: {[v.real for v in parsed]}"
        magnitudes = sorted([abs(v.imag) for v in parsed])
        for mag in magnitudes:
            if abs(mag - expected) > tolerance:
                return False, f"Imaginary magnitude {mag:.4f} not near {expected} (tol={tolerance})"
        return True, ""

    else:
        return False, f"Unknown check type: {check_type}"


@evaluator("json_array_item_check")
async def eval_json_array_item_check(workspace: Path, op_args: Dict[str, Any],
                                     value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Find an item in a JSON array by matching criteria, then run checks on it.

    op_args:
        path: Path to JSON file
        array_path: Dot-separated path to the array (e.g., "equilibria")
        match: Dict of field conditions to locate the target element.
            Keys are dot-separated field paths relative to array items.
            Values are either:
              - {"near": <number>, "tolerance": <number>} for approximate match
              - A literal value for exact match
        checks: List of check dicts, each with:
            - field: Dot-separated path relative to the matched item
            - type: One of "contains", "equals", "near", "array_length",
                    "sorted_reals_near", "purely_imaginary_magnitude_near"
            - expected: Expected value
            - tolerance: Optional tolerance (default 0.01)
    """
    path = op_args["path"]
    array_path = op_args["array_path"]
    match = op_args.get("match", {})
    checks = op_args.get("checks", [])

    data = read_json(workspace, path)
    if data is None:
        return False, f"Cannot read JSON: {path}"

    arr = get_nested_value(data, array_path)
    if arr is None:
        return False, f"Array path not found: {array_path}"
    if not isinstance(arr, list):
        return False, f"'{array_path}' is not an array"

    # Find matching item
    found = None
    for item in arr:
        if isinstance(item, dict) and _match_item(item, match):
            found = item
            break

    if found is None:
        return False, f"No item in '{array_path}' matches {match}"

    # Run checks
    failures = []
    for check in checks:
        passed, msg = _run_check(found, check)
        if not passed:
            failures.append(msg)

    if not failures:
        return True, ""
    return False, "; ".join(failures)
