#!/usr/bin/env python3
"""
Extract domain-specific glossary terms from codebase.

This tool:
- Scans source files for identifiers (classes, functions, variables)
- Filters generic/common terms
- Identifies domain-specific terminology
- Extracts context from comments and usage
- Ranks terms by relevance and frequency

Returns structured JSON with glossary terms and contexts.
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import Counter


# Common generic terms to filter out
GENERIC_TERMS = {
    # Generic programming terms
    'data', 'info', 'config', 'options', 'params', 'args', 'result', 'response',
    'request', 'error', 'exception', 'value', 'key', 'item', 'element', 'list',
    'array', 'map', 'object', 'string', 'number', 'boolean', 'function', 'method',
    'class', 'interface', 'type', 'props', 'state', 'context', 'provider',
    'component', 'container', 'wrapper', 'helper', 'util', 'utils', 'handler',
    'manager', 'service', 'controller', 'model', 'view', 'router', 'route',
    'middleware', 'validator', 'formatter', 'parser', 'builder', 'factory',
    'repository', 'entity', 'schema', 'migration', 'seeder',

    # Common action verbs
    'get', 'set', 'create', 'update', 'delete', 'fetch', 'load', 'save',
    'add', 'remove', 'find', 'search', 'filter', 'sort', 'validate', 'check',
    'is', 'has', 'can', 'should', 'will', 'to', 'from', 'with', 'without',

    # Common adjectives
    'new', 'old', 'current', 'previous', 'next', 'first', 'last', 'main',
    'default', 'custom', 'public', 'private', 'protected', 'static', 'async',

    # Test-related
    'test', 'spec', 'mock', 'stub', 'fixture', 'assert', 'expect', 'describe',

    # Common abbreviations
    'id', 'url', 'api', 'http', 'json', 'xml', 'html', 'css', 'sql', 'db'
}


def extract_camel_case_words(identifier: str) -> List[str]:
    """Split camelCase or PascalCase identifier into words."""
    # Insert space before uppercase letters
    spaced = re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', identifier))
    words = spaced.split()
    return [w.lower() for w in words if len(w) > 2]


def extract_snake_case_words(identifier: str) -> List[str]:
    """Split snake_case identifier into words."""
    words = identifier.split('_')
    return [w.lower() for w in words if len(w) > 2]


def is_domain_specific(term: str) -> bool:
    """Check if a term is domain-specific (not generic)."""
    term_lower = term.lower()

    # Filter out generic terms
    if term_lower in GENERIC_TERMS:
        return False

    # Filter out very short terms (likely abbreviations or generic)
    if len(term) < 3:
        return False

    # Filter out common prefixes/suffixes alone
    generic_affixes = {'get', 'set', 'is', 'has', 'can', 'use', 'with', 'by', 'to', 'from'}
    if term_lower in generic_affixes:
        return False

    return True


def extract_class_names(content: str, file_path: str) -> List[Tuple[str, int, str]]:
    """Extract class names from source code."""
    classes = []

    # TypeScript/JavaScript class
    for match in re.finditer(r'class\s+([A-Z][a-zA-Z0-9]+)', content):
        line_num = content[:match.start()].count('\n') + 1
        classes.append((match.group(1), line_num, file_path))

    # Python class
    for match in re.finditer(r'class\s+([A-Z][a-zA-Z0-9]+)\s*[\(:]', content):
        line_num = content[:match.start()].count('\n') + 1
        classes.append((match.group(1), line_num, file_path))

    # TypeScript interface
    for match in re.finditer(r'interface\s+([A-Z][a-zA-Z0-9]+)', content):
        line_num = content[:match.start()].count('\n') + 1
        classes.append((match.group(1), line_num, file_path))

    # TypeScript type alias
    for match in re.finditer(r'type\s+([A-Z][a-zA-Z0-9]+)\s*=', content):
        line_num = content[:match.start()].count('\n') + 1
        classes.append((match.group(1), line_num, file_path))

    return classes


def extract_function_names(content: str, file_path: str) -> List[Tuple[str, int, str]]:
    """Extract function names from source code."""
    functions = []

    # JavaScript/TypeScript functions
    for match in re.finditer(r'function\s+([a-z][a-zA-Z0-9]+)', content):
        line_num = content[:match.start()].count('\n') + 1
        functions.append((match.group(1), line_num, file_path))

    # Arrow functions and const declarations
    for match in re.finditer(r'const\s+([a-z][a-zA-Z0-9]+)\s*=\s*(?:async\s+)?\(', content):
        line_num = content[:match.start()].count('\n') + 1
        functions.append((match.group(1), line_num, file_path))

    # Python functions
    for match in re.finditer(r'def\s+([a-z][a-zA-Z0-9_]+)\s*\(', content):
        line_num = content[:match.start()].count('\n') + 1
        functions.append((match.group(1), line_num, file_path))

    return functions


def extract_context_around_term(content: str, term: str, context_lines: int = 2) -> List[str]:
    """Extract context (comments, docstrings) around a term."""
    contexts = []

    # Find all occurrences of the term
    for match in re.finditer(rf'\b{re.escape(term)}\b', content, re.IGNORECASE):
        start_pos = match.start()
        line_num = content[:start_pos].count('\n')

        # Get surrounding lines
        lines = content.split('\n')
        start_line = max(0, line_num - context_lines)
        end_line = min(len(lines), line_num + context_lines + 1)

        surrounding = lines[start_line:end_line]

        # Extract comments
        for line in surrounding:
            # Single-line comments
            if '//' in line or '#' in line:
                comment = re.sub(r'.*?(?://|#)\s*', '', line).strip()
                if comment and len(comment) > 10:
                    contexts.append(comment)

            # JSDoc style comments
            if '/**' in line or '*' in line:
                comment = re.sub(r'/?\*+/?\s*', '', line).strip()
                if comment and len(comment) > 10:
                    contexts.append(comment)

    return contexts[:3]  # Limit to 3 contexts


def scan_file(file_path: Path, project_path: Path) -> Dict:
    """Scan a single file for domain-specific terms."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError):
        return {"terms": {}, "classes": [], "functions": []}

    relative_path = str(file_path.relative_to(project_path))

    # Extract identifiers
    classes = extract_class_names(content, relative_path)
    functions = extract_function_names(content, relative_path)

    # Collect all potential terms
    all_identifiers = set()

    for class_name, _, _ in classes:
        all_identifiers.add(class_name)
        all_identifiers.update(extract_camel_case_words(class_name))

    for func_name, _, _ in functions:
        all_identifiers.add(func_name)
        all_identifiers.update(extract_camel_case_words(func_name))
        all_identifiers.update(extract_snake_case_words(func_name))

    # Filter to domain-specific terms
    domain_terms = {term for term in all_identifiers if is_domain_specific(term)}

    # Extract contexts
    terms_with_context = {}
    for term in domain_terms:
        contexts = extract_context_around_term(content, term)
        if contexts or term in [c[0] for c in classes]:
            terms_with_context[term] = {
                "contexts": contexts,
                "file": relative_path
            }

    return {
        "terms": terms_with_context,
        "classes": classes,
        "functions": functions
    }


def aggregate_terms(scan_results: List[Dict]) -> Dict[str, Dict]:
    """Aggregate terms from multiple files."""
    term_data = {}

    for result in scan_results:
        for term, data in result["terms"].items():
            if term not in term_data:
                term_data[term] = {
                    "occurrences": 0,
                    "contexts": [],
                    "files": set()
                }

            term_data[term]["occurrences"] += 1
            term_data[term]["contexts"].extend(data["contexts"])
            term_data[term]["files"].add(data["file"])

    # Convert sets to lists for JSON serialization
    for term in term_data:
        term_data[term]["files"] = sorted(list(term_data[term]["files"]))
        # Deduplicate contexts
        term_data[term]["contexts"] = list(set(term_data[term]["contexts"]))[:3]

    return term_data


def rank_terms(term_data: Dict[str, Dict], min_occurrences: int = 2) -> List[Dict]:
    """Rank and filter terms by relevance."""
    ranked = []

    for term, data in term_data.items():
        # Filter by minimum occurrences
        if data["occurrences"] < min_occurrences:
            continue

        # Calculate relevance score
        # Higher score = more domain-specific
        score = 0

        # Frequency matters
        score += min(data["occurrences"], 10) * 2

        # Having context is good
        score += len(data["contexts"]) * 5

        # Being in multiple files suggests importance
        score += len(data["files"]) * 3

        # Longer terms are often more specific
        score += min(len(term), 20)

        # Uppercase terms (like acronyms) might be important
        if term.isupper() and len(term) >= 2:
            score += 10

        ranked.append({
            "term": term,
            "occurrences": data["occurrences"],
            "contexts": data["contexts"],
            "files": data["files"],
            "score": score
        })

    # Sort by score (descending)
    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked


def main():
    """Main glossary extraction function."""
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Project path required"}))
        sys.exit(1)

    project_path = Path(sys.argv[1]).resolve()

    if not project_path.exists():
        print(json.dumps({"error": f"Project path not found: {project_path}"}))
        sys.exit(1)

    # Optional: file patterns to include
    patterns = ['**/*.ts', '**/*.tsx', '**/*.js', '**/*.jsx', '**/*.py']
    if len(sys.argv) >= 3:
        patterns = sys.argv[2].split(',')

    # Optional: minimum occurrences
    min_occurrences = 2
    if len(sys.argv) >= 4:
        min_occurrences = int(sys.argv[3])

    # Scan files
    scan_results = []
    scanned_files = 0

    for pattern in patterns:
        for file_path in project_path.glob(pattern):
            # Skip node_modules, venv, etc.
            if any(skip in str(file_path) for skip in [
                'node_modules', '.venv', 'venv', 'dist', 'build',
                '.git', '__pycache__', '.next', '.pytest_cache'
            ]):
                continue

            # Skip test files
            if any(test in file_path.name.lower() for test in ['.test.', '.spec.', 'test_']):
                continue

            result = scan_file(file_path, project_path)
            if result["terms"]:
                scan_results.append(result)
                scanned_files += 1

    # Aggregate and rank
    term_data = aggregate_terms(scan_results)
    ranked_terms = rank_terms(term_data, min_occurrences)

    output = {
        "total_terms": len(ranked_terms),
        "scanned_files": scanned_files,
        "min_occurrences": min_occurrences,
        "terms": ranked_terms[:50],  # Limit to top 50
        "project_path": str(project_path)
    }

    print(json.dumps(output, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
