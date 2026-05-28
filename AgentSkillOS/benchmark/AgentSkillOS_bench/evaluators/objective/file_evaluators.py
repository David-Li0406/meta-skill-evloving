"""
File-related objective evaluators.
"""
from pathlib import Path
from typing import Dict, Any, Tuple, List
import re

from ...registry import evaluator
from ...utils.file_utils import (
    resolve_path,
    check_file_exists,
    read_file,
    read_json,
    list_files,
    get_nested_value,
)


@evaluator("file_exists")
async def eval_file_exists(workspace: Path, op_args: Dict[str, Any],
                           value: Any = None, **kwargs) -> Tuple[bool, str]:
    """Check if one or more files exist and are not trivially small.

    op_args.path can be a single string or a list of strings.
    Also verifies file size > min_size (default 1KB) to reject empty or
    placeholder files. Use op_args.min_size to override the threshold in bytes,
    or set it to 0 to skip the size check.
    """
    paths = op_args["path"]
    if isinstance(paths, str):
        paths = [paths]

    min_size = op_args.get("min_size", 1)  # default 1B
    missing = []
    too_small = []

    for path in paths:
        resolved = resolve_path(workspace, path)
        if resolved is None:
            missing.append(path)
            continue
        size = resolved.stat().st_size
        if min_size and size < min_size:
            too_small.append(f"{path}({size}B)")

    errors = []
    if missing:
        errors.append(f"Files not found: {missing}")
    if too_small:
        errors.append(f"Files too small (need >= {min_size}B): {too_small}")

    if errors:
        return False, "; ".join(errors)
    return True, ""


@evaluator("file_content_check")
async def eval_file_content_check(workspace: Path, op_args: Dict[str, Any],
                                  value: Any = None, **kwargs) -> Tuple[bool, str]:
    """
    Unified file content checker supporting both contains and regex modes.

    op_args:
        path: File path to check
        mode: "contains" | "regex" (default: inferred from value type)
        min_matches: Minimum matches required (regex mode only, default 1)

    value:
        For "contains" mode: List of strings that must all be present
        For "regex" mode: Regex pattern string
    """
    path = op_args["path"]
    mode = op_args.get("mode")

    # Infer mode from value type if not specified
    if mode is None:
        if isinstance(value, list):
            mode = "contains"
        else:
            mode = "regex"

    content = read_file(workspace, path)
    if content is None:
        return False, f"Cannot read file: {path}"

    if mode == "contains":
        if not isinstance(value, list):
            value = [value]
        content_lower = content.lower()
        missing = [s for s in value if s.lower() not in content_lower]
        if not missing:
            return True, ""
        return False, f"Missing content in {path}: {missing[:3]}"

    elif mode == "regex":
        pattern = value
        min_matches = op_args.get("min_matches", 1)
        matches = re.findall(pattern, content)
        if len(matches) >= min_matches:
            return True, ""
        return False, f"Pattern '{pattern}' found {len(matches)} times, need {min_matches}"

    else:
        return False, f"Unknown mode: {mode}"


@evaluator("files_match_pattern")
async def eval_files_match_pattern(workspace: Path, op_args: Dict[str, Any],
                                   value: Any = None, **kwargs) -> Tuple[bool, str]:
    """Check if all files in directory match a pattern."""
    directory = op_args["directory"]
    pattern = op_args["pattern"]
    min_count = op_args.get("min_count", 1)
    allow_extra = op_args.get("allow_extra", False)

    all_files = list_files(workspace, directory)
    if not all_files:
        return False, f"No files found in {directory}"

    regex = re.compile(pattern)
    matching = [f for f in all_files if regex.match(f)]
    non_matching = [f for f in all_files if not regex.match(f)]

    if len(matching) < min_count:
        return False, f"Only {len(matching)} files match pattern, need {min_count}"

    if not allow_extra and non_matching:
        return False, f"Files don't match pattern: {non_matching[:5]}"

    return True, ""



