#!/usr/bin/env python3
"""
Detect common code smells across multiple languages.
Finds duplicated code, long parameter lists, god objects, etc.
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict

def detect_long_parameter_list(content: str, file_path: str, language: str) -> List[Dict[str, Any]]:
    """Detect functions with too many parameters."""
    issues = []

    if language in ['javascript', 'typescript']:
        # Match function declarations
        pattern = r'(?:function\s+(\w+)|const\s+(\w+)\s*=\s*(?:async\s*)?\()\s*([^)]+)\)'
        matches = re.finditer(pattern, content)

        for match in matches:
            func_name = match.group(1) or match.group(2)
            params = match.group(3) if len(match.groups()) >= 3 else ''

            if params:
                param_count = len([p.strip() for p in params.split(',') if p.strip()])

                if param_count > 5:
                    issues.append({
                        'type': 'long_parameter_list',
                        'severity': 'medium',
                        'file': file_path,
                        'function': func_name,
                        'message': f'Function has {param_count} parameters (recommended: ≤5)',
                        'suggestion': 'Consider using an options object or breaking into smaller functions'
                    })

    elif language == 'python':
        pattern = r'def\s+(\w+)\s*\(([^)]+)\)'
        matches = re.finditer(pattern, content)

        for match in matches:
            func_name = match.group(1)
            params = match.group(2)

            # Count parameters (excluding self)
            param_list = [p.strip() for p in params.split(',') if p.strip() and p.strip() != 'self']
            param_count = len(param_list)

            if param_count > 5:
                issues.append({
                    'type': 'long_parameter_list',
                    'severity': 'medium',
                    'file': file_path,
                    'function': func_name,
                    'message': f'Function has {param_count} parameters (recommended: ≤5)',
                    'suggestion': 'Consider using **kwargs or dataclass for parameters'
                })

    return issues

def detect_magic_numbers(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Detect magic numbers in code."""
    issues = []

    # Find numeric literals (excluding 0, 1, -1, 100)
    pattern = r'\b(?<![\w.])((?:[2-9]|[1-9]\d+)(?:\.\d+)?)\b'
    matches = re.finditer(pattern, content)

    line_numbers = {}
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        if re.search(pattern, line):
            # Skip if in comment
            if '//' in line or '#' in line:
                continue

            numbers = re.findall(pattern, line)
            if numbers:
                if file_path not in line_numbers:
                    line_numbers[file_path] = []

                line_numbers[file_path].append({
                    'line': i,
                    'numbers': numbers[:3]  # Limit examples
                })

    for file, occurrences in line_numbers.items():
        if len(occurrences) > 5:  # Only report if multiple magic numbers
            issues.append({
                'type': 'magic_numbers',
                'severity': 'low',
                'file': file,
                'message': f'Found {len(occurrences)} lines with magic numbers',
                'suggestion': 'Extract magic numbers to named constants',
                'examples': occurrences[:3]
            })

    return issues

def detect_duplicated_code(files_content: Dict[str, str]) -> List[Dict[str, Any]]:
    """Detect duplicated code blocks."""
    issues = []

    # Simple heuristic: look for identical lines of code appearing in multiple files
    line_hashes = defaultdict(list)

    for file_path, content in files_content.items():
        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Skip empty lines, comments, and single characters
            if len(stripped) < 20:
                continue

            if stripped.startswith(('//', '#', '/*', '*')):
                continue

            line_hashes[stripped].append((file_path, i))

    # Find duplicates
    for line_content, occurrences in line_hashes.items():
        if len(occurrences) >= 3:  # Appears 3+ times
            unique_files = set(f[0] for f in occurrences)

            if len(unique_files) > 1:  # In different files
                issues.append({
                    'type': 'duplicated_code',
                    'severity': 'medium',
                    'message': f'Code appears in {len(unique_files)} different files',
                    'occurrences': len(occurrences),
                    'files': list(unique_files)[:5],
                    'suggestion': 'Extract to shared function or module',
                    'sample': line_content[:100]
                })

    return issues[:10]  # Limit to top 10

def detect_deep_nesting(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Detect deeply nested code blocks."""
    issues = []
    lines = content.split('\n')

    for i, line in enumerate(lines, 1):
        # Count indentation level
        stripped = line.lstrip()
        if not stripped or stripped.startswith(('//', '#')):
            continue

        indent_level = (len(line) - len(stripped)) // 2  # Assuming 2-space indent

        if indent_level > 4:
            issues.append({
                'type': 'deep_nesting',
                'severity': 'medium',
                'file': file_path,
                'line': i,
                'nesting_level': indent_level,
                'message': f'Deep nesting ({indent_level} levels) detected',
                'suggestion': 'Extract nested logic into separate functions'
            })

    return issues[:5]  # Limit to first 5 occurrences

def detect_god_class(content: str, file_path: str, language: str) -> List[Dict[str, Any]]:
    """Detect classes with too many methods or responsibilities."""
    issues = []

    if language in ['javascript', 'typescript']:
        # Count methods in classes
        class_pattern = r'class\s+(\w+)'
        method_pattern = r'^\s+(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{'

        classes = re.finditer(class_pattern, content)

        for class_match in classes:
            class_name = class_match.group(1)
            class_start = class_match.start()

            # Find class end (simplified)
            class_content = content[class_start:]
            brace_depth = 0
            class_end = class_start

            for i, char in enumerate(class_content):
                if char == '{':
                    brace_depth += 1
                elif char == '}':
                    brace_depth -= 1
                    if brace_depth == 0:
                        class_end = class_start + i
                        break

            class_body = content[class_start:class_end]
            method_count = len(re.findall(method_pattern, class_body, re.MULTILINE))

            if method_count > 10:
                issues.append({
                    'type': 'god_class',
                    'severity': 'high',
                    'file': file_path,
                    'class': class_name,
                    'method_count': method_count,
                    'message': f'Class has {method_count} methods (recommended: ≤10)',
                    'suggestion': 'Consider splitting into multiple classes with single responsibilities'
                })

    return issues

def analyze_file(file_path: Path, language: str) -> List[Dict[str, Any]]:
    """Analyze a single file for code smells."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception:
        return []

    issues = []

    issues.extend(detect_long_parameter_list(content, str(file_path), language))
    issues.extend(detect_magic_numbers(content, str(file_path)))
    issues.extend(detect_deep_nesting(content, str(file_path)))
    issues.extend(detect_god_class(content, str(file_path), language))

    return issues

def analyze_directory(target_dir: str) -> Dict[str, Any]:
    """Analyze all files in directory."""
    target_path = Path(target_dir)

    all_issues = []
    files_content = {}

    # File patterns and language mapping
    language_map = {
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.py': 'python',
        '.rs': 'rust',
    }

    excludes = ['node_modules', 'venv', '.venv', 'dist', 'build', 'target', '.git']

    for suffix, language in language_map.items():
        for file_path in target_path.rglob(f'*{suffix}'):
            # Check if file is in excluded directory
            if any(exclude in file_path.parts for exclude in excludes):
                continue

            content = file_path.read_text(encoding='utf-8', errors='ignore')
            files_content[str(file_path)] = content

            issues = analyze_file(file_path, language)
            all_issues.extend(issues)

    # Detect duplicated code across files
    duplication_issues = detect_duplicated_code(files_content)
    all_issues.extend(duplication_issues)

    # Group by severity
    by_severity = defaultdict(list)
    for issue in all_issues:
        by_severity[issue['severity']].append(issue)

    return {
        'total_issues': len(all_issues),
        'by_severity': {
            'high': len(by_severity['high']),
            'medium': len(by_severity['medium']),
            'low': len(by_severity['low']),
        },
        'issues': all_issues
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: detect_code_smells.py <directory>")
        sys.exit(1)

    target_dir = sys.argv[1]

    if not os.path.isdir(target_dir):
        print(f"Error: {target_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    result = analyze_directory(target_dir)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
