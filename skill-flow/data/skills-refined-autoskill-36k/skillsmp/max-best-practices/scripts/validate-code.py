#!/usr/bin/env python3
"""
MAX Configuration Validator
Validates MAX Serve configurations and deployment files for common issues.

Usage:
    python validate-code.py <config.yaml>
    python validate-code.py <directory>
    python validate-code.py --json <config.yaml>
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@dataclass
class Issue:
    """Represents a configuration issue found during validation."""
    file: str
    line: int
    severity: str  # error, warning, info
    code: str
    message: str
    suggestion: Optional[str] = None
    pattern: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of validating a file or directory."""
    files_checked: int = 0
    issues: List[Issue] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == "warning")


# CLI flag validation patterns
CLI_RULES = [
    # Deprecated flags
    {
        "pattern": r"--max-ce-batch-size\b",
        "code": "DEPRECATED_CE_BATCH_SIZE",
        "severity": "warning",
        "message": "--max-ce-batch-size is deprecated in nightly",
        "suggestion": "Use --max-batch-size instead",
        "related_pattern": "serve-configuration"
    },
    {
        "pattern": r"--prefill-chunk-size\b",
        "code": "DEPRECATED_PREFILL_CHUNK",
        "severity": "info",
        "message": "--prefill-chunk-size renamed in nightly",
        "suggestion": "Use --max-batch-input-tokens in v26.1+",
        "related_pattern": "serve-configuration"
    },
    {
        "pattern": r"--max-batch-context-length\b",
        "code": "DEPRECATED_CONTEXT_LENGTH",
        "severity": "info",
        "message": "--max-batch-context-length renamed in nightly",
        "suggestion": "Use --max-batch-total-tokens in v26.1+",
        "related_pattern": "serve-configuration"
    },

    # Configuration best practices
    {
        "pattern": r"--kv-cache-page-size\s+(\d+)",
        "code": "KV_CACHE_ALIGNMENT",
        "severity": "info",
        "message": "KV cache page size should be multiple of 128",
        "suggestion": "Use values like 128, 256, 512 for optimal performance",
        "related_pattern": "serve-kv-cache",
        "validator": lambda m: int(m.group(1)) % 128 != 0
    },
    {
        "pattern": r"--devices\s+gpu:(\d+)",
        "code": "SINGLE_GPU",
        "severity": "info",
        "message": "Using single GPU",
        "suggestion": "For multi-GPU, use --devices gpu:0,1,... See multigpu-scaling pattern",
        "related_pattern": "multigpu-scaling"
    },

    # Common errors
    {
        "pattern": r"--quantization-encoding\s+(?!float8|gptq|none)",
        "code": "INVALID_QUANTIZATION",
        "severity": "error",
        "message": "Invalid quantization encoding",
        "suggestion": "Valid options: float8, gptq, none",
        "related_pattern": "engine-quantization"
    },
]

# YAML configuration rules
YAML_RULES = [
    {
        "key_path": "serve.kv_cache.strategy",
        "invalid_values": ["naive"],
        "code": "SUBOPTIMAL_KV_STRATEGY",
        "severity": "warning",
        "message": "Naive KV cache strategy is not recommended for production",
        "suggestion": "Use 'paged' strategy for better memory efficiency",
        "related_pattern": "serve-kv-cache"
    },
    {
        "key_path": "serve.batch.max_size",
        "validator": lambda v: v is not None and v > 512,
        "code": "LARGE_BATCH_SIZE",
        "severity": "warning",
        "message": "Very large batch size may cause memory issues",
        "suggestion": "Consider batch size <= 512 for most models",
        "related_pattern": "serve-configuration"
    },
]


def validate_cli_file(file_path: Path) -> List[Issue]:
    """Validate a file containing CLI commands or scripts."""
    issues = []

    try:
        content = file_path.read_text()
    except Exception as e:
        issues.append(Issue(
            file=str(file_path),
            line=0,
            severity="error",
            code="READ_ERROR",
            message=f"Could not read file: {e}"
        ))
        return issues

    for rule in CLI_RULES:
        pattern = re.compile(rule["pattern"])

        for match in pattern.finditer(content):
            # Check custom validator if present
            if "validator" in rule:
                if not rule["validator"](match):
                    continue

            line_num = content[:match.start()].count('\n') + 1

            issues.append(Issue(
                file=str(file_path),
                line=line_num,
                severity=rule["severity"],
                code=rule["code"],
                message=rule["message"],
                suggestion=rule.get("suggestion"),
                pattern=rule.get("related_pattern")
            ))

    return issues


def get_nested_value(data: Dict[str, Any], key_path: str) -> Any:
    """Get a nested dictionary value by dot-separated path."""
    keys = key_path.split('.')
    value = data

    for key in keys:
        if isinstance(value, dict) and key in value:
            value = value[key]
        else:
            return None

    return value


def validate_yaml_file(file_path: Path) -> List[Issue]:
    """Validate a YAML configuration file."""
    issues = []

    if not YAML_AVAILABLE:
        issues.append(Issue(
            file=str(file_path),
            line=0,
            severity="warning",
            code="YAML_NOT_AVAILABLE",
            message="PyYAML not installed, skipping YAML validation",
            suggestion="Install with: pip install pyyaml"
        ))
        return issues

    try:
        content = file_path.read_text()
        data = yaml.safe_load(content)
    except Exception as e:
        issues.append(Issue(
            file=str(file_path),
            line=0,
            severity="error",
            code="YAML_PARSE_ERROR",
            message=f"Could not parse YAML: {e}"
        ))
        return issues

    if not isinstance(data, dict):
        return issues

    for rule in YAML_RULES:
        value = get_nested_value(data, rule["key_path"])

        if value is None:
            continue

        should_report = False

        if "invalid_values" in rule and value in rule["invalid_values"]:
            should_report = True
        elif "validator" in rule and rule["validator"](value):
            should_report = True

        if should_report:
            issues.append(Issue(
                file=str(file_path),
                line=0,  # YAML doesn't easily give line numbers
                severity=rule["severity"],
                code=rule["code"],
                message=rule["message"],
                suggestion=rule.get("suggestion"),
                pattern=rule.get("related_pattern")
            ))

    # Also check for CLI patterns in YAML string values
    issues.extend(validate_cli_file(file_path))

    return issues


def validate_file(file_path: Path) -> List[Issue]:
    """Validate a single file based on its extension."""
    suffix = file_path.suffix.lower()

    if suffix in ['.yaml', '.yml']:
        return validate_yaml_file(file_path)
    elif suffix in ['.sh', '.bash', '.py', '.txt', '']:
        return validate_cli_file(file_path)
    else:
        return validate_cli_file(file_path)


def validate_directory(dir_path: Path) -> ValidationResult:
    """Validate all configuration files in a directory."""
    result = ValidationResult()

    # File patterns to check
    patterns = ['*.yaml', '*.yml', '*.sh', 'Dockerfile*', 'docker-compose*']

    for pattern in patterns:
        for config_file in dir_path.rglob(pattern):
            result.files_checked += 1
            result.issues.extend(validate_file(config_file))

    return result


def format_issue(issue: Issue, use_color: bool = True) -> str:
    """Format an issue for terminal output."""
    colors = {
        "error": "\033[91m",
        "warning": "\033[93m",
        "info": "\033[94m",
        "reset": "\033[0m"
    }

    if not use_color:
        colors = {k: "" for k in colors}

    severity_color = colors.get(issue.severity, "")
    reset = colors["reset"]

    output = f"{severity_color}{issue.severity.upper()}{reset} [{issue.code}] {issue.file}"
    if issue.line > 0:
        output += f":{issue.line}"
    output += f"\n  {issue.message}\n"

    if issue.suggestion:
        output += f"  Suggestion: {issue.suggestion}\n"

    if issue.pattern:
        output += f"  See pattern: {issue.pattern}\n"

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Validate MAX configuration files"
    )
    parser.add_argument("path", help="File or directory to validate")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output")

    args = parser.parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"Error: Path not found: {path}", file=sys.stderr)
        sys.exit(1)

    if path.is_file():
        result = ValidationResult(files_checked=1)
        result.issues = validate_file(path)
    else:
        result = validate_directory(path)

    if args.json:
        output = {
            "files_checked": result.files_checked,
            "error_count": result.error_count,
            "warning_count": result.warning_count,
            "issues": [
                {
                    "file": i.file,
                    "line": i.line,
                    "severity": i.severity,
                    "code": i.code,
                    "message": i.message,
                    "suggestion": i.suggestion,
                    "pattern": i.pattern
                }
                for i in result.issues
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        use_color = not args.no_color and sys.stdout.isatty()

        print(f"\nValidated {result.files_checked} file(s)")
        print(f"Found {result.error_count} error(s), {result.warning_count} warning(s)\n")

        for issue in result.issues:
            print(format_issue(issue, use_color))

    sys.exit(1 if result.error_count > 0 else 0)


if __name__ == "__main__":
    main()
