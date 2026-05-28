#!/usr/bin/env python3
"""
Validate 3-tier architecture structure.

Checks that:
1. Files are in correct tiers (01-presentation, 02-logic, 03-data)
2. Dependencies flow in valid direction (Presentation → Logic → Data)
3. No reverse imports

Usage:
    python validate_structure.py <path> [--format json|text] [--strict]
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, field

# Tier definitions
TIERS = {
    '01-presentation': 1,
    '02-logic': 2,
    '03-data': 3,
}

TIER_NAMES = {
    1: 'Presentation',
    2: 'Logic',
    3: 'Data',
}


@dataclass
class Violation:
    """Represents a dependency violation."""
    file: str
    line: int
    import_path: str
    from_tier: str
    to_tier: str
    message: str


@dataclass
class ValidationResult:
    """Results of structure validation."""
    files_checked: int = 0
    violations: List[Violation] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    tier_stats: Dict[str, int] = field(default_factory=dict)

    @property
    def is_valid(self) -> bool:
        return len(self.violations) == 0


def get_file_tier(filepath: str) -> Tuple[int, str]:
    """Determine which tier a file belongs to."""
    path = Path(filepath)
    parts = path.parts

    for part in parts:
        if part in TIERS:
            return TIERS[part], part

    return 0, 'unknown'


def extract_imports(filepath: str) -> List[Tuple[int, str]]:
    """Extract import statements from a file."""
    imports = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                # Python imports
                match = re.match(r'^(?:from|import)\s+([^\s;]+)', line.strip())
                if match:
                    imports.append((line_num, match.group(1)))

                # JavaScript/TypeScript imports
                match = re.match(r"^import\s+.*?from\s+['\"]([^'\"]+)['\"]", line.strip())
                if match:
                    imports.append((line_num, match.group(1)))

                # Require statements
                match = re.match(r".*require\(['\"]([^'\"]+)['\"]\)", line.strip())
                if match:
                    imports.append((line_num, match.group(1)))

    except Exception as e:
        pass  # Skip files we can't read

    return imports


def resolve_import_tier(import_path: str, base_path: str) -> Tuple[int, str]:
    """Resolve an import path to its tier."""
    # Check for tier references in the import path
    for tier_name, tier_num in TIERS.items():
        if tier_name in import_path:
            return tier_num, tier_name

    # Check for alias patterns
    aliases = {
        '@/presentation': ('01-presentation', 1),
        '@/logic': ('02-logic', 2),
        '@/data': ('03-data', 3),
        '@presentation': ('01-presentation', 1),
        '@logic': ('02-logic', 2),
        '@data': ('03-data', 3),
    }

    for alias, (name, num) in aliases.items():
        if import_path.startswith(alias):
            return num, name

    return 0, 'external'


def validate_dependency(from_tier: int, to_tier: int) -> bool:
    """Check if dependency direction is valid."""
    # External imports are always valid
    if to_tier == 0:
        return True

    # Valid: same tier or downward (1→2, 2→3, 1→3)
    # Invalid: upward (3→2, 2→1, 3→1)
    return from_tier <= to_tier


def validate_file(filepath: str, base_path: str) -> List[Violation]:
    """Validate a single file's imports."""
    violations = []

    from_tier, from_tier_name = get_file_tier(filepath)
    if from_tier == 0:
        return violations  # Not in a tier, skip

    imports = extract_imports(filepath)

    for line_num, import_path in imports:
        to_tier, to_tier_name = resolve_import_tier(import_path, base_path)

        if to_tier > 0 and not validate_dependency(from_tier, to_tier):
            violations.append(Violation(
                file=filepath,
                line=line_num,
                import_path=import_path,
                from_tier=from_tier_name,
                to_tier=to_tier_name,
                message=f"Invalid import: {TIER_NAMES.get(from_tier, 'Unknown')} cannot import from {TIER_NAMES.get(to_tier, 'Unknown')}"
            ))

    return violations


def validate_directory(path: str, strict: bool = False) -> ValidationResult:
    """Validate all files in a directory."""
    result = ValidationResult()
    base_path = os.path.abspath(path)

    # File extensions to check
    extensions = {'.py', '.ts', '.tsx', '.js', '.jsx'}

    for root, dirs, files in os.walk(path):
        # Skip common non-source directories
        dirs[:] = [d for d in dirs if d not in {
            'node_modules', '__pycache__', '.git', 'venv', 'env',
            'dist', 'build', '.next', 'coverage'
        }]

        for file in files:
            if Path(file).suffix in extensions:
                filepath = os.path.join(root, file)
                result.files_checked += 1

                # Track tier statistics
                tier, tier_name = get_file_tier(filepath)
                if tier_name != 'unknown':
                    result.tier_stats[tier_name] = result.tier_stats.get(tier_name, 0) + 1

                # Validate imports
                violations = validate_file(filepath, base_path)
                result.violations.extend(violations)

    # Add warnings for structural issues
    if '01-presentation' not in result.tier_stats:
        result.warnings.append("No presentation tier found (01-presentation/)")
    if '02-logic' not in result.tier_stats:
        result.warnings.append("No logic tier found (02-logic/)")
    if '03-data' not in result.tier_stats:
        result.warnings.append("No data tier found (03-data/)")

    return result


def format_output(result: ValidationResult, format_type: str) -> str:
    """Format the validation results."""
    if format_type == 'json':
        return json.dumps({
            'valid': result.is_valid,
            'files_checked': result.files_checked,
            'violations': [
                {
                    'file': v.file,
                    'line': v.line,
                    'import': v.import_path,
                    'from_tier': v.from_tier,
                    'to_tier': v.to_tier,
                    'message': v.message
                }
                for v in result.violations
            ],
            'warnings': result.warnings,
            'tier_stats': result.tier_stats
        }, indent=2)

    # Text format
    lines = []
    lines.append("=" * 60)
    lines.append("3-TIER ARCHITECTURE VALIDATION REPORT")
    lines.append("=" * 60)
    lines.append("")

    # Summary
    status = "✅ VALID" if result.is_valid else "❌ INVALID"
    lines.append(f"Status: {status}")
    lines.append(f"Files checked: {result.files_checked}")
    lines.append(f"Violations found: {len(result.violations)}")
    lines.append("")

    # Tier statistics
    if result.tier_stats:
        lines.append("Tier Distribution:")
        for tier, count in sorted(result.tier_stats.items()):
            lines.append(f"  {tier}: {count} files")
        lines.append("")

    # Warnings
    if result.warnings:
        lines.append("Warnings:")
        for warning in result.warnings:
            lines.append(f"  ⚠️  {warning}")
        lines.append("")

    # Violations
    if result.violations:
        lines.append("Violations:")
        lines.append("-" * 60)
        for v in result.violations:
            lines.append(f"  File: {v.file}:{v.line}")
            lines.append(f"  Import: {v.import_path}")
            lines.append(f"  Error: {v.message}")
            lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Validate 3-tier architecture structure'
    )
    parser.add_argument('path', help='Path to validate')
    parser.add_argument(
        '--format', choices=['json', 'text'], default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--strict', action='store_true',
        help='Exit with error code on any violation'
    )

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist")
        sys.exit(1)

    result = validate_directory(args.path, args.strict)
    print(format_output(result, args.format))

    if args.strict and not result.is_valid:
        sys.exit(1)


if __name__ == '__main__':
    main()
