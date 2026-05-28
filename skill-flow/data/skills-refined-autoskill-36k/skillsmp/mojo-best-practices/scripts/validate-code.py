#!/usr/bin/env python3
"""
Mojo Code Validator
Basic static analysis for common anti-patterns and deprecated syntax.

Usage:
    python validate-code.py <file.mojo>
    python validate-code.py <directory>
    python validate-code.py --json <file.mojo>
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class Issue:
    """Represents a code issue found during validation."""
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


# Validation rules
RULES = [
    # Deprecated syntax
    {
        "pattern": r"@value\b",
        "code": "DEPRECATED_VALUE",
        "severity": "error",
        "message": "@value decorator is deprecated",
        "suggestion": "Use @fieldwise_init instead",
        "related_pattern": "struct-design"
    },
    {
        "pattern": r"\bowned\s+\w+",
        "code": "DEPRECATED_OWNED",
        "severity": "error",
        "message": "'owned' keyword is deprecated",
        "suggestion": "Use 'var' instead: var x = value^",
        "related_pattern": "memory-ownership"
    },
    {
        "pattern": r"Stringable\b",
        "code": "DEPRECATED_STRINGABLE",
        "severity": "warning",
        "message": "Stringable trait is deprecated",
        "suggestion": "Use Writable trait instead",
        "related_pattern": "type-traits"
    },
    {
        "pattern": r"fn\s+__str__\s*\(",
        "code": "DEPRECATED_STR",
        "severity": "warning",
        "message": "__str__ method is deprecated",
        "suggestion": "Implement write_to(self, mut writer: Writer) instead",
        "related_pattern": "type-traits"
    },

    # Memory safety issues
    {
        "pattern": r"UnsafePointer\[.*\]\(\)",
        "code": "UNSAFE_NULL_POINTER",
        "severity": "warning",
        "message": "Creating null UnsafePointer - ensure proper initialization",
        "suggestion": "Consider using Optional or ensure pointer is set before use",
        "related_pattern": "memory-safety"
    },
    {
        "pattern": r"\.unsafe_ptr\(\)",
        "code": "UNSAFE_PTR_ESCAPE",
        "severity": "warning",
        "message": "Unsafe pointer escaping - verify lifetime",
        "suggestion": "Ensure pointer doesn't outlive the source object",
        "related_pattern": "memory-safety"
    },

    # Performance anti-patterns
    {
        "pattern": r"for\s+\w+\s+in\s+range\(.*\):\s*\n\s+[^@]*$",
        "code": "UNVECTORIZED_LOOP",
        "severity": "info",
        "message": "Loop may benefit from vectorization",
        "suggestion": "Consider using @parameter for compile-time unrolling or vectorize[]",
        "related_pattern": "perf-vectorization"
    },
    {
        "pattern": r"String\s*\+\s*String",
        "code": "STRING_CONCAT",
        "severity": "info",
        "message": "String concatenation in loop may be slow",
        "suggestion": "Use String.write() or StringSlice for better performance",
        "related_pattern": "perf-memory"
    },

    # GPU patterns
    {
        "pattern": r"@__gpu__",
        "code": "DEPRECATED_GPU_DECORATOR",
        "severity": "error",
        "message": "@__gpu__ decorator syntax may be outdated",
        "suggestion": "Check gpu-fundamentals pattern for current GPU kernel syntax",
        "related_pattern": "gpu-fundamentals"
    },

    # Type system
    {
        "pattern": r"fn\s+\w+\s*\[.*\]\s*\(.*\)\s*->\s*\w+:",
        "code": "MISSING_PARAMETER_DECORATOR",
        "severity": "info",
        "message": "Parametric function - consider if @parameter is needed",
        "suggestion": "Use @parameter for compile-time evaluation where applicable",
        "related_pattern": "meta-comptime"
    },

    # Nightly-specific (context-dependent)
    {
        "pattern": r"\balias\s+\w+\s*=",
        "code": "ALIAS_USAGE",
        "severity": "info",
        "message": "Using 'alias' for constants - deprecated in nightly",
        "suggestion": "Use 'comptime' instead if targeting nightly (v0.26.1+)",
        "related_pattern": "meta-comptime"
    },
]


def validate_file(file_path: Path) -> List[Issue]:
    """Validate a single Mojo file."""
    issues = []

    try:
        content = file_path.read_text()
        lines = content.split('\n')
    except Exception as e:
        issues.append(Issue(
            file=str(file_path),
            line=0,
            severity="error",
            code="READ_ERROR",
            message=f"Could not read file: {e}"
        ))
        return issues

    for rule in RULES:
        pattern = re.compile(rule["pattern"], re.MULTILINE)

        for match in pattern.finditer(content):
            # Find line number
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


def validate_directory(dir_path: Path) -> ValidationResult:
    """Validate all Mojo files in a directory."""
    result = ValidationResult()

    for mojo_file in dir_path.rglob("*.mojo"):
        result.files_checked += 1
        result.issues.extend(validate_file(mojo_file))

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

    output = f"{severity_color}{issue.severity.upper()}{reset} [{issue.code}] {issue.file}:{issue.line}\n"
    output += f"  {issue.message}\n"

    if issue.suggestion:
        output += f"  Suggestion: {issue.suggestion}\n"

    if issue.pattern:
        output += f"  See pattern: {issue.pattern}\n"

    return output


def main():
    parser = argparse.ArgumentParser(
        description="Validate Mojo code for anti-patterns and deprecated syntax"
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

    # Exit with error if errors found
    sys.exit(1 if result.error_count > 0 else 0)


if __name__ == "__main__":
    main()
