#!/usr/bin/env python3
"""
Analyze code complexity metrics across multiple languages.
Measures cyclomatic complexity, function length, nesting depth.
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Dict, List, Any

def count_lines(content: str) -> int:
    """Count non-empty, non-comment lines."""
    lines = content.split('\n')
    code_lines = 0

    for line in lines:
        stripped = line.strip()
        # Skip empty lines and comments
        if stripped and not stripped.startswith(('//', '#', '/*', '*', '*/')):
            code_lines += 1

    return code_lines

def calculate_cyclomatic_complexity(content: str, language: str) -> int:
    """
    Calculate cyclomatic complexity (decision points + 1).
    Simplified heuristic based on control flow keywords.
    """
    complexity = 1  # Base complexity

    # Keywords that add to complexity
    decision_keywords = {
        'javascript': ['if', 'else if', 'for', 'while', 'case', 'catch', '&&', '||', '?'],
        'typescript': ['if', 'else if', 'for', 'while', 'case', 'catch', '&&', '||', '?'],
        'python': ['if', 'elif', 'for', 'while', 'except', 'and', 'or'],
        'rust': ['if', 'else if', 'for', 'while', 'match', '&&', '||'],
        'java': ['if', 'else if', 'for', 'while', 'case', 'catch', '&&', '||', '?'],
        'go': ['if', 'else if', 'for', 'case', '&&', '||'],
    }

    keywords = decision_keywords.get(language, decision_keywords['javascript'])

    for keyword in keywords:
        # Count occurrences (simplified)
        if keyword in ['&&', '||', '?']:
            complexity += content.count(keyword)
        else:
            # Use word boundaries for keywords
            pattern = r'\b' + re.escape(keyword) + r'\b'
            complexity += len(re.findall(pattern, content))

    return complexity

def calculate_nesting_depth(content: str) -> int:
    """Calculate maximum nesting depth."""
    max_depth = 0
    current_depth = 0

    for char in content:
        if char == '{':
            current_depth += 1
            max_depth = max(max_depth, current_depth)
        elif char == '}':
            current_depth = max(0, current_depth - 1)

    return max_depth

def analyze_function(func_content: str, func_name: str, language: str, file_path: str) -> Dict[str, Any]:
    """Analyze a single function."""
    lines = count_lines(func_content)
    complexity = calculate_cyclomatic_complexity(func_content, language)
    nesting = calculate_nesting_depth(func_content)

    issues = []

    # Flag potential issues
    if lines > 50:
        issues.append(f"Function too long ({lines} lines)")
    if complexity > 10:
        issues.append(f"High complexity ({complexity})")
    if nesting > 4:
        issues.append(f"Deep nesting ({nesting} levels)")

    return {
        'name': func_name,
        'file': file_path,
        'lines': lines,
        'complexity': complexity,
        'nesting_depth': nesting,
        'issues': issues
    }

def extract_functions_js_ts(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Extract and analyze JavaScript/TypeScript functions."""
    functions = []

    # Match function declarations and arrow functions
    patterns = [
        r'function\s+(\w+)\s*\([^)]*\)\s*\{',
        r'const\s+(\w+)\s*=\s*\([^)]*\)\s*=>\s*\{',
        r'(\w+)\s*\([^)]*\)\s*\{',  # Methods
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            func_name = match.group(1)
            start = match.start()

            # Find matching closing brace
            depth = 0
            end = start
            for i in range(start, len(content)):
                if content[i] == '{':
                    depth += 1
                elif content[i] == '}':
                    depth -= 1
                    if depth == 0:
                        end = i + 1
                        break

            func_content = content[start:end]
            functions.append(analyze_function(func_content, func_name, 'javascript', file_path))

    return functions

def extract_functions_python(content: str, file_path: str) -> List[Dict[str, Any]]:
    """Extract and analyze Python functions."""
    functions = []

    # Match function definitions
    pattern = r'def\s+(\w+)\s*\([^)]*\):'
    matches = re.finditer(pattern, content)

    lines = content.split('\n')

    for match in matches:
        func_name = match.group(1)
        start_line = content[:match.start()].count('\n')

        # Find function end (next def or class at same indentation)
        base_indent = len(lines[start_line]) - len(lines[start_line].lstrip())
        end_line = start_line + 1

        for i in range(start_line + 1, len(lines)):
            line = lines[i]
            if line.strip() and not line.strip().startswith('#'):
                indent = len(line) - len(line.lstrip())
                if indent <= base_indent and (line.strip().startswith('def ') or line.strip().startswith('class ')):
                    end_line = i
                    break
        else:
            end_line = len(lines)

        func_content = '\n'.join(lines[start_line:end_line])
        functions.append(analyze_function(func_content, func_name, 'python', file_path))

    return functions

def analyze_file(file_path: Path) -> List[Dict[str, Any]]:
    """Analyze a single file."""
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        return []

    suffix = file_path.suffix.lower()

    if suffix in ['.js', '.jsx', '.ts', '.tsx']:
        return extract_functions_js_ts(content, str(file_path))
    elif suffix == '.py':
        return extract_functions_python(content, str(file_path))
    elif suffix == '.rs':
        # Simplified Rust support
        return []  # TODO: Implement Rust parsing

    return []

def analyze_directory(target_dir: str) -> Dict[str, Any]:
    """Analyze all files in directory."""
    target_path = Path(target_dir)

    all_functions = []
    file_count = 0

    # File patterns to analyze
    patterns = ['**/*.js', '**/*.jsx', '**/*.ts', '**/*.tsx', '**/*.py', '**/*.rs']

    # Exclude patterns
    excludes = ['node_modules', 'venv', '.venv', 'dist', 'build', 'target', '.git']

    for pattern in patterns:
        for file_path in target_path.glob(pattern):
            # Check if file is in excluded directory
            if any(exclude in file_path.parts for exclude in excludes):
                continue

            file_count += 1
            functions = analyze_file(file_path)
            all_functions.extend(functions)

    # Calculate statistics
    complexities = [f['complexity'] for f in all_functions]
    line_counts = [f['lines'] for f in all_functions]

    stats = {
        'total_files': file_count,
        'total_functions': len(all_functions),
        'avg_complexity': sum(complexities) / len(complexities) if complexities else 0,
        'max_complexity': max(complexities) if complexities else 0,
        'avg_function_length': sum(line_counts) / len(line_counts) if line_counts else 0,
        'max_function_length': max(line_counts) if line_counts else 0,
    }

    # Find problematic functions
    problematic = [f for f in all_functions if f['issues']]

    return {
        'statistics': stats,
        'problematic_functions': sorted(problematic, key=lambda x: x['complexity'], reverse=True),
        'all_functions': all_functions[:100]  # Limit output
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: analyze_complexity.py <directory>")
        sys.exit(1)

    target_dir = sys.argv[1]

    if not os.path.isdir(target_dir):
        print(f"Error: {target_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    result = analyze_directory(target_dir)
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
