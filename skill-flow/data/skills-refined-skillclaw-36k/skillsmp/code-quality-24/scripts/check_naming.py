#!/usr/bin/env python3
"""
Check naming conventions in codebase.

Validates:
1. File naming (PascalCase, camelCase, kebab-case by type)
2. Function/method naming (verbs, directional clarity)
3. Variable naming (no abbreviations, boolean prefixes)
4. Class naming (PascalCase, nouns)

Usage:
    python check_naming.py <path> [--format json|text] [--fix-suggestions]
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field

# Naming patterns
PASCAL_CASE = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
CAMEL_CASE = re.compile(r'^[a-z][a-zA-Z0-9]*$')
SNAKE_CASE = re.compile(r'^[a-z][a-z0-9_]*$')
KEBAB_CASE = re.compile(r'^[a-z][a-z0-9-]*$')
UPPER_SNAKE = re.compile(r'^[A-Z][A-Z0-9_]*$')

# Common abbreviations to flag
ABBREVIATIONS = {
    'usr': 'user',
    'btn': 'button',
    'msg': 'message',
    'pwd': 'password',
    'cfg': 'config',
    'tmp': 'temporary',
    'str': 'string',
    'num': 'number',
    'arr': 'array',
    'obj': 'object',
    'fn': 'function',
    'cb': 'callback',
    'err': 'error',
    'req': 'request',
    'res': 'response',
    'val': 'value',
    'idx': 'index',
    'cnt': 'count',
    'len': 'length',
    'pos': 'position',
    'ctx': 'context',
    'env': 'environment',
    'src': 'source',
    'dst': 'destination',
    'dir': 'directory',
    'ext': 'extension',
    'ref': 'reference',
    'doc': 'document',
    'mgr': 'manager',
    'svc': 'service',
    'repo': 'repository',
    'util': 'utility',
    'impl': 'implementation',
    'spec': 'specification',
}

# Boolean prefixes
BOOLEAN_PREFIXES = ('is', 'has', 'should', 'can', 'will', 'did', 'was', 'are')

# Verb prefixes for functions
VERB_PREFIXES = (
    'get', 'set', 'create', 'update', 'delete', 'remove', 'add', 'insert',
    'find', 'search', 'fetch', 'load', 'save', 'store', 'send', 'receive',
    'parse', 'format', 'convert', 'transform', 'validate', 'check', 'verify',
    'calculate', 'compute', 'process', 'handle', 'execute', 'run', 'start',
    'stop', 'init', 'initialize', 'build', 'render', 'display', 'show', 'hide',
    'enable', 'disable', 'open', 'close', 'read', 'write', 'log', 'register',
    'authenticate', 'authorize', 'encrypt', 'decrypt', 'encode', 'decode',
)


@dataclass
class NamingIssue:
    """Represents a naming convention issue."""
    file: str
    line: int
    name: str
    issue_type: str
    message: str
    suggestion: Optional[str] = None


@dataclass
class NamingResult:
    """Results of naming validation."""
    files_checked: int = 0
    names_checked: int = 0
    issues: List[NamingIssue] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.issues) == 0


def check_abbreviations(name: str) -> Optional[Tuple[str, str]]:
    """Check if name contains common abbreviations."""
    name_lower = name.lower()

    for abbrev, full in ABBREVIATIONS.items():
        # Check for abbreviation as whole word or at boundaries
        pattern = rf'(?:^|_|(?<=[a-z]))({abbrev})(?:$|_|(?=[A-Z]))'
        if re.search(pattern, name_lower):
            return abbrev, full

    return None


def check_boolean_naming(name: str) -> bool:
    """Check if boolean-like name has proper prefix."""
    name_lower = name.lower()

    # Skip if already has good prefix
    if name_lower.startswith(BOOLEAN_PREFIXES):
        return True

    # Flag suspicious boolean names
    boolean_indicators = ('active', 'enabled', 'disabled', 'visible', 'hidden',
                         'valid', 'invalid', 'empty', 'full', 'ready', 'done',
                         'loading', 'loaded', 'open', 'closed', 'selected')

    for indicator in boolean_indicators:
        if indicator in name_lower:
            return False

    return True


def check_function_naming(name: str) -> bool:
    """Check if function name starts with a verb."""
    name_lower = name.lower()

    # Skip private/magic methods
    if name.startswith('_'):
        return True

    # Skip React lifecycle methods
    react_methods = ('componentDidMount', 'componentWillUnmount', 'render',
                    'shouldComponentUpdate', 'getDerivedStateFromProps')
    if name in react_methods:
        return True

    # Check for verb prefix
    return name_lower.startswith(VERB_PREFIXES)


def check_file_naming(filepath: str) -> List[NamingIssue]:
    """Check file naming conventions."""
    issues = []
    path = Path(filepath)
    name = path.stem  # filename without extension
    ext = path.suffix

    # Determine expected convention based on file type/location
    is_component = 'component' in str(path).lower() or ext in ('.tsx', '.jsx')
    is_style = ext in ('.css', '.scss', '.sass', '.less')
    is_test = '.test' in name or '.spec' in name
    is_type = 'type' in name.lower() or 'interface' in name.lower()

    if is_style:
        # Styles should be kebab-case
        if not KEBAB_CASE.match(name.replace('.', '-')):
            issues.append(NamingIssue(
                file=filepath,
                line=0,
                name=name,
                issue_type='file_naming',
                message=f"Style file '{name}' should be kebab-case",
                suggestion=to_kebab_case(name)
            ))
    elif is_component or is_type:
        # Components and types should be PascalCase
        base_name = name.replace('.test', '').replace('.spec', '')
        if not PASCAL_CASE.match(base_name):
            issues.append(NamingIssue(
                file=filepath,
                line=0,
                name=name,
                issue_type='file_naming',
                message=f"Component/Type file '{name}' should be PascalCase",
                suggestion=to_pascal_case(base_name)
            ))

    return issues


def extract_names(filepath: str) -> List[Tuple[int, str, str]]:
    """Extract function, variable, and class names from a file."""
    names = []

    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')

        for line_num, line in enumerate(lines, 1):
            # Python function definitions
            match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
            if match:
                names.append((line_num, match.group(1), 'function'))

            # Python class definitions
            match = re.search(r'class\s+([a-zA-Z_][a-zA-Z0-9_]*)', line)
            if match:
                names.append((line_num, match.group(1), 'class'))

            # JavaScript/TypeScript function definitions
            match = re.search(r'(?:function|const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*[=\(]', line)
            if match:
                names.append((line_num, match.group(1), 'function'))

            # JavaScript/TypeScript class definitions
            match = re.search(r'class\s+([a-zA-Z_$][a-zA-Z0-9_$]*)', line)
            if match:
                names.append((line_num, match.group(1), 'class'))

            # Variable assignments (simple cases)
            match = re.search(r'(?:const|let|var)\s+([a-zA-Z_$][a-zA-Z0-9_$]*)\s*=', line)
            if match:
                name = match.group(1)
                # Try to detect boolean variables
                if re.search(r'=\s*(?:true|false|Boolean)', line):
                    names.append((line_num, name, 'boolean'))
                else:
                    names.append((line_num, name, 'variable'))

    except Exception:
        pass

    return names


def to_pascal_case(name: str) -> str:
    """Convert name to PascalCase."""
    words = re.split(r'[-_\s]+', name)
    return ''.join(word.capitalize() for word in words)


def to_camel_case(name: str) -> str:
    """Convert name to camelCase."""
    pascal = to_pascal_case(name)
    return pascal[0].lower() + pascal[1:] if pascal else ''


def to_kebab_case(name: str) -> str:
    """Convert name to kebab-case."""
    # Insert hyphens before capitals
    name = re.sub(r'([a-z])([A-Z])', r'\1-\2', name)
    # Replace underscores and spaces
    name = re.sub(r'[_\s]+', '-', name)
    return name.lower()


def validate_file(filepath: str, fix_suggestions: bool) -> List[NamingIssue]:
    """Validate naming in a single file."""
    issues = []

    # Check file naming
    issues.extend(check_file_naming(filepath))

    # Check names in file content
    names = extract_names(filepath)

    for line_num, name, name_type in names:
        # Check for abbreviations
        abbrev_result = check_abbreviations(name)
        if abbrev_result:
            abbrev, full = abbrev_result
            issues.append(NamingIssue(
                file=filepath,
                line=line_num,
                name=name,
                issue_type='abbreviation',
                message=f"Avoid abbreviation '{abbrev}' in '{name}'",
                suggestion=name.replace(abbrev, full) if fix_suggestions else None
            ))

        # Check boolean naming
        if name_type == 'boolean' and not check_boolean_naming(name):
            issues.append(NamingIssue(
                file=filepath,
                line=line_num,
                name=name,
                issue_type='boolean_prefix',
                message=f"Boolean '{name}' should have is/has/should/can prefix",
                suggestion=f"is{name[0].upper()}{name[1:]}" if fix_suggestions else None
            ))

        # Check function naming
        if name_type == 'function' and not check_function_naming(name):
            issues.append(NamingIssue(
                file=filepath,
                line=line_num,
                name=name,
                issue_type='function_verb',
                message=f"Function '{name}' should start with a verb",
                suggestion=None
            ))

        # Check class naming
        if name_type == 'class' and not PASCAL_CASE.match(name):
            issues.append(NamingIssue(
                file=filepath,
                line=line_num,
                name=name,
                issue_type='class_case',
                message=f"Class '{name}' should be PascalCase",
                suggestion=to_pascal_case(name) if fix_suggestions else None
            ))

    return issues


def validate_directory(path: str, fix_suggestions: bool) -> NamingResult:
    """Validate naming in all files."""
    result = NamingResult()
    extensions = {'.py', '.ts', '.tsx', '.js', '.jsx', '.css', '.scss'}

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in {
            'node_modules', '__pycache__', '.git', 'venv', 'env',
            'dist', 'build', '.next', 'coverage'
        }]

        for file in files:
            if Path(file).suffix in extensions:
                filepath = os.path.join(root, file)
                result.files_checked += 1

                issues = validate_file(filepath, fix_suggestions)
                result.issues.extend(issues)
                result.names_checked += len(extract_names(filepath))

    return result


def format_output(result: NamingResult, format_type: str) -> str:
    """Format the validation results."""
    if format_type == 'json':
        return json.dumps({
            'valid': result.is_valid,
            'files_checked': result.files_checked,
            'names_checked': result.names_checked,
            'issues': [
                {
                    'file': i.file,
                    'line': i.line,
                    'name': i.name,
                    'type': i.issue_type,
                    'message': i.message,
                    'suggestion': i.suggestion
                }
                for i in result.issues
            ]
        }, indent=2)

    # Text format
    lines = []
    lines.append("=" * 60)
    lines.append("NAMING CONVENTION VALIDATION REPORT")
    lines.append("=" * 60)
    lines.append("")

    status = "✅ VALID" if result.is_valid else "❌ ISSUES FOUND"
    lines.append(f"Status: {status}")
    lines.append(f"Files checked: {result.files_checked}")
    lines.append(f"Names checked: {result.names_checked}")
    lines.append(f"Issues found: {len(result.issues)}")
    lines.append("")

    if result.issues:
        # Group by issue type
        by_type: Dict[str, List[NamingIssue]] = {}
        for issue in result.issues:
            by_type.setdefault(issue.issue_type, []).append(issue)

        for issue_type, issues in by_type.items():
            lines.append(f"{issue_type.upper().replace('_', ' ')} ({len(issues)}):")
            lines.append("-" * 40)
            for i in issues:
                lines.append(f"  {i.file}:{i.line}")
                lines.append(f"    Name: {i.name}")
                lines.append(f"    Issue: {i.message}")
                if i.suggestion:
                    lines.append(f"    Suggestion: {i.suggestion}")
                lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='Check naming conventions in codebase'
    )
    parser.add_argument('path', help='Path to validate')
    parser.add_argument(
        '--format', choices=['json', 'text'], default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--fix-suggestions', action='store_true',
        help='Include fix suggestions in output'
    )

    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist")
        sys.exit(1)

    result = validate_directory(args.path, args.fix_suggestions)
    print(format_output(result, args.format))

    if not result.is_valid:
        sys.exit(1)


if __name__ == '__main__':
    main()
