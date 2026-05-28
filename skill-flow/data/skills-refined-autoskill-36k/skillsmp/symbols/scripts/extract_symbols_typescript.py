#!/usr/bin/env python3
"""
TypeScript/JavaScript Symbol Extractor for MeatyPrompts

Extracts symbols from TypeScript and JavaScript files including interfaces, types,
functions, classes, React components, and hooks. Supports monorepo structure.

Usage:
    python extract_symbols_typescript.py <path> [--output=file.json] [--exclude-tests] [--exclude-private]

Examples:
    # Extract symbols from source directory
    python extract_symbols_typescript.py src

    # Extract from specific directory with output
    python extract_symbols_typescript.py frontend --output=frontend_symbols.json

    # Exclude test files and private symbols
    python extract_symbols_typescript.py src --exclude-tests --exclude-private

Output Format:
    {
        "symbols": [
            {
                "name": "PromptCard",
                "kind": "component",
                "path": "components/PromptCard.tsx",
                "line": 42,
                "signature": "function PromptCard(props: PromptCardProps): JSX.Element",
                "summary": "Display a prompt with metadata and actions"
            }
        ]
    }

Symbol Kinds:
    - component: React components (capitalized functions returning JSX)
    - hook: Custom React hooks (functions starting with 'use')
    - interface: TypeScript interfaces
    - type: Type aliases
    - function: Regular functions
    - class: Class declarations
"""

import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from dataclasses import dataclass
import argparse


@dataclass
class Symbol:
    """Represents a single extracted symbol (Schema v2.0)."""
    name: str
    kind: str
    path: str
    line: int
    signature: str
    summary: str
    layer: str  # Architectural layer: component, hook, page, util, router, service, test
    parent: Optional[str] = None
    docstring: Optional[str] = None  # Full JSDoc/TSDoc
    category: Optional[str] = None  # Optional file category


class TypeScriptSymbolExtractor:
    """Parser for TypeScript/JavaScript files using regex-based extraction."""

    # Regex patterns for various symbol types
    INTERFACE_PATTERN = re.compile(
        r'^\s*(?:export\s+)?interface\s+(\w+)(?:<[^>]+>)?\s*(?:extends\s+[^{]+)?\s*\{',
        re.MULTILINE
    )

    TYPE_PATTERN = re.compile(
        r'^\s*(?:export\s+)?type\s+(\w+)(?:<[^>]+>)?\s*=',
        re.MULTILINE
    )

    CLASS_PATTERN = re.compile(
        r'^\s*(?:export\s+)?(?:abstract\s+)?class\s+(\w+)(?:<[^>]+>)?(?:\s+extends\s+(\w+))?',
        re.MULTILINE
    )

    FUNCTION_PATTERN = re.compile(
        r'^\s*(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*(?:<[^>]+>)?\s*\([^)]*\)',
        re.MULTILINE
    )

    ARROW_FUNCTION_PATTERN = re.compile(
        r'^\s*(?:export\s+)?(?:const|let)\s+(\w+)\s*(?::\s*[^=]+)?\s*=\s*(?:async\s+)?\([^)]*\)\s*(?::\s*[^=]+)?\s*=>',
        re.MULTILINE
    )

    JSDOC_PATTERN = re.compile(
        r'/\*\*\s*\n([^*]|\*(?!/))*\*/',
        re.MULTILINE
    )

    def __init__(self, file_path: str, source_code: str):
        self.file_path = file_path
        self.source_code = source_code
        self.symbols: List[Symbol] = []
        self.lines = source_code.splitlines()

    def extract(self) -> List[Symbol]:
        """Extract all symbols from the source code."""
        self._extract_interfaces()
        self._extract_types()
        self._extract_classes()
        self._extract_functions()
        self._extract_arrow_functions()

        # Sort by line number
        self.symbols.sort(key=lambda s: s.line)

        return self.symbols

    def _extract_interfaces(self) -> None:
        """Extract TypeScript interface declarations."""
        for match in self.INTERFACE_PATTERN.finditer(self.source_code):
            name = match.group(1)
            line = self._get_line_number(match.start())

            # Skip private interfaces
            if name.startswith('_'):
                continue

            # Get JSDoc summary and full doc
            summary, docstring = self._get_jsdoc(match.start())

            # Build signature
            signature = f"interface {name}"

            symbol = Symbol(
                name=name,
                kind="interface",
                path=self.file_path,
                line=line,
                signature=signature,
                summary=summary,
                layer="unknown",  # Will be set by categorize_file
                docstring=docstring if docstring else None
            )
            self.symbols.append(symbol)

    def _extract_types(self) -> None:
        """Extract TypeScript type alias declarations."""
        for match in self.TYPE_PATTERN.finditer(self.source_code):
            name = match.group(1)
            line = self._get_line_number(match.start())

            # Skip private types
            if name.startswith('_'):
                continue

            # Get JSDoc summary and full doc
            summary, docstring = self._get_jsdoc(match.start())

            # Build signature
            signature = f"type {name}"

            symbol = Symbol(
                name=name,
                kind="type",
                path=self.file_path,
                line=line,
                signature=signature,
                summary=summary,
                layer="unknown",  # Will be set by categorize_file
                docstring=docstring if docstring else None
            )
            self.symbols.append(symbol)

    def _extract_classes(self) -> None:
        """Extract class declarations."""
        for match in self.CLASS_PATTERN.finditer(self.source_code):
            name = match.group(1)
            base_class = match.group(2)
            line = self._get_line_number(match.start())

            # Skip private classes
            if name.startswith('_'):
                continue

            # Get JSDoc summary and full doc
            summary, docstring = self._get_jsdoc(match.start())

            # Build signature
            if base_class:
                signature = f"class {name} extends {base_class}"
            else:
                signature = f"class {name}"

            symbol = Symbol(
                name=name,
                kind="class",
                path=self.file_path,
                line=line,
                signature=signature,
                summary=summary,
                layer="unknown",  # Will be set by categorize_file
                docstring=docstring if docstring else None
            )
            self.symbols.append(symbol)

    def _extract_functions(self) -> None:
        """Extract function declarations."""
        for match in self.FUNCTION_PATTERN.finditer(self.source_code):
            name = match.group(1)
            line = self._get_line_number(match.start())

            # Skip private functions
            if name.startswith('_'):
                continue

            # Get JSDoc summary and full doc
            summary, docstring = self._get_jsdoc(match.start())

            # Determine kind based on naming conventions
            kind = self._determine_function_kind(name, match.start())

            # Get full signature
            signature = self._extract_function_signature(match.start(), name)

            symbol = Symbol(
                name=name,
                kind=kind,
                path=self.file_path,
                line=line,
                signature=signature,
                summary=summary,
                layer="unknown",  # Will be set by categorize_file
                docstring=docstring if docstring else None
            )
            self.symbols.append(symbol)

    def _extract_arrow_functions(self) -> None:
        """Extract arrow function declarations."""
        for match in self.ARROW_FUNCTION_PATTERN.finditer(self.source_code):
            name = match.group(1)
            line = self._get_line_number(match.start())

            # Skip private functions
            if name.startswith('_'):
                continue

            # Get JSDoc summary and full doc
            summary, docstring = self._get_jsdoc(match.start())

            # Determine kind based on naming conventions
            kind = self._determine_function_kind(name, match.start())

            # Get full signature
            signature = self._extract_arrow_function_signature(match.start(), name)

            symbol = Symbol(
                name=name,
                kind=kind,
                path=self.file_path,
                line=line,
                signature=signature,
                summary=summary,
                layer="unknown",  # Will be set by categorize_file
                docstring=docstring if docstring else None
            )
            self.symbols.append(symbol)

    def _determine_function_kind(self, name: str, position: int) -> str:
        """Determine if a function is a component, hook, or regular function."""
        # Check if it's a hook (starts with 'use')
        if name.startswith('use') and len(name) > 3 and name[3].isupper():
            return "hook"

        # Check if it's a React component (capitalized and returns JSX)
        if name[0].isupper():
            # Look for JSX return in the function body
            if self._contains_jsx_return(position):
                return "component"

        return "function"

    def _contains_jsx_return(self, start_pos: int) -> bool:
        """Check if a function contains JSX return statement."""
        # Find the function body
        brace_count = 0
        in_function = False
        for i in range(start_pos, len(self.source_code)):
            char = self.source_code[i]
            if char == '{':
                brace_count += 1
                in_function = True
            elif char == '}':
                brace_count -= 1
                if brace_count == 0 and in_function:
                    # End of function body
                    function_body = self.source_code[start_pos:i]
                    # Look for JSX patterns
                    jsx_patterns = [
                        r'return\s*<',
                        r'return\s*\(',
                        r'<\w+[^>]*>',
                        r'</\w+>',
                        r'JSX\.Element',
                        r'React\.ReactElement',
                        r'ReactNode'
                    ]
                    for pattern in jsx_patterns:
                        if re.search(pattern, function_body):
                            return True
                    return False
        return False

    def _extract_function_signature(self, position: int, name: str) -> str:
        """Extract the full function signature."""
        # Find the function declaration line
        line_start = self.source_code.rfind('\n', 0, position) + 1
        line_end = self.source_code.find('{', position)

        if line_end == -1:
            line_end = self.source_code.find('\n', position)

        signature = self.source_code[line_start:line_end].strip()

        # Clean up the signature
        signature = re.sub(r'\s+', ' ', signature)

        return signature

    def _extract_arrow_function_signature(self, position: int, name: str) -> str:
        """Extract the full arrow function signature."""
        # Find the declaration
        line_start = self.source_code.rfind('\n', 0, position) + 1
        arrow_pos = self.source_code.find('=>', position)

        if arrow_pos == -1:
            arrow_pos = self.source_code.find('\n', position)
        else:
            arrow_pos += 2  # Include =>

        signature = self.source_code[line_start:arrow_pos].strip()

        # Clean up the signature
        signature = re.sub(r'\s+', ' ', signature)

        return signature

    def _get_jsdoc(self, position: int) -> tuple[str, str]:
        """
        Extract JSDoc comment summary and full docstring before a symbol.

        Returns:
            Tuple of (summary, docstring) where summary is the first line and
            docstring is the full comment text.
        """
        # Look backwards for JSDoc comment
        search_start = max(0, position - 500)  # Look back 500 chars
        search_text = self.source_code[search_start:position]

        # Find the last JSDoc comment
        jsdoc_matches = list(self.JSDOC_PATTERN.finditer(search_text))
        if not jsdoc_matches:
            return ("", "")

        last_match = jsdoc_matches[-1]
        jsdoc_text = last_match.group(0)

        # Extract full docstring (clean up comment markers)
        docstring_lines = []
        for line in jsdoc_text.split('\n'):
            cleaned = re.sub(r'^\s*/?\*+\s*', '', line).strip()
            if cleaned and cleaned != '/':
                docstring_lines.append(cleaned)

        full_docstring = '\n'.join(docstring_lines) if docstring_lines else ""

        # Extract summary (first line that's not a tag)
        summary = ""
        for line in jsdoc_text.split('\n'):
            cleaned = re.sub(r'^\s*/?\*+\s*', '', line).strip()
            if cleaned and not cleaned.startswith('@'):
                # Truncate if too long
                if len(cleaned) > 100:
                    summary = cleaned[:97] + "..."
                else:
                    summary = cleaned
                break

        return (summary, full_docstring)

    def _get_line_number(self, position: int) -> int:
        """Get line number from character position."""
        return self.source_code[:position].count('\n') + 1


def is_test_file(file_path: Path) -> bool:
    """Check if a file is a test file."""
    parts = file_path.parts
    return (
        'test' in parts or
        'tests' in parts or
        '__tests__' in parts or
        file_path.name.endswith('.test.ts') or
        file_path.name.endswith('.test.tsx') or
        file_path.name.endswith('.test.js') or
        file_path.name.endswith('.test.jsx') or
        file_path.name.endswith('.spec.ts') or
        file_path.name.endswith('.spec.tsx') or
        file_path.name.endswith('.spec.js') or
        file_path.name.endswith('.spec.jsx')
    )


def is_typescript_file(file_path: Path) -> bool:
    """Check if a file is a TypeScript or JavaScript file."""
    return file_path.suffix in ['.ts', '.tsx', '.js', '.jsx']


def categorize_file(file_path: Path) -> tuple[str, str]:
    """
    Categorize a TypeScript/JavaScript file by its architectural layer and category.

    Returns:
        Tuple of (layer, category) where:
        - layer: Architectural layer (component, hook, page, util, router, service, test)
        - category: Optional file category (ui, business_logic, test, config)
    """
    path_str = str(file_path).lower()
    parts = file_path.parts
    name = file_path.name.lower()

    # Test files
    if is_test_file(file_path):
        return ("test", "test")

    # Pages (Next.js app router or pages router)
    if 'pages' in parts or 'app' in parts and any(s in name for s in ['page.tsx', 'page.ts', 'page.jsx', 'page.js']):
        return ("page", "ui")

    # Components (React components)
    if 'components' in parts or 'component' in name:
        return ("component", "ui")

    # Hooks (React hooks)
    if name.startswith('use') and any(name.endswith(ext) for ext in ['.ts', '.tsx', '.js', '.jsx']):
        return ("hook", "ui")

    # API routes (Next.js)
    if 'api' in parts or 'route' in name:
        return ("router", "business_logic")

    # Services (business logic)
    if 'services' in parts or 'service' in name:
        return ("service", "business_logic")

    # Utils/helpers
    if any(p in parts for p in ['utils', 'helpers', 'lib', 'utilities']) or any(k in name for k in ['util', 'helper']):
        return ("util", "business_logic")

    # Config files
    if any(k in name for k in ['config', 'constant', 'env']):
        return ("util", "config")

    # Default: util layer
    return ("util", "business_logic")


def extract_symbols_from_file(file_path: Path, base_path: Path) -> List[Symbol]:
    """Extract symbols from a single TypeScript/JavaScript file."""
    try:
        source_code = file_path.read_text(encoding='utf-8')

        # Calculate relative path
        rel_path = file_path.relative_to(base_path)

        # Categorize file (layer and category)
        layer, category = categorize_file(file_path)

        # Extract symbols
        extractor = TypeScriptSymbolExtractor(str(rel_path), source_code)
        symbols = extractor.extract()

        # Add layer and category to all symbols
        for symbol in symbols:
            symbol.layer = layer
            symbol.category = category

        return symbols

    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return []


def extract_symbols_from_directory(
    directory: Path,
    exclude_tests: bool = False,
    exclude_private: bool = False
) -> List[Symbol]:
    """Extract symbols from all TypeScript/JavaScript files in a directory."""
    symbols: List[Symbol] = []

    # Find all TypeScript/JavaScript files
    patterns = ['**/*.ts', '**/*.tsx', '**/*.js', '**/*.jsx']
    files = []
    for pattern in patterns:
        files.extend(directory.glob(pattern))

    for file_path in files:
        # Skip node_modules and other special directories
        if 'node_modules' in file_path.parts or '.next' in file_path.parts:
            continue

        # Skip test files if requested
        if exclude_tests and is_test_file(file_path):
            continue

        # Extract symbols from this file
        file_symbols = extract_symbols_from_file(file_path, directory)

        # Filter private symbols if requested
        if exclude_private:
            file_symbols = [
                s for s in file_symbols
                if not s.name.startswith('_')
            ]

        symbols.extend(file_symbols)

    return symbols


def symbols_to_dict(symbols: List[Symbol]) -> Dict[str, Any]:
    """Convert symbols list to output dictionary (Schema v2.0)."""
    symbol_list = []
    for s in symbols:
        # Required fields (Schema v2.0)
        symbol_dict = {
            "name": s.name,
            "kind": s.kind,
            "path": s.path,
            "line": s.line,
            "signature": s.signature,
            "summary": s.summary,
            "layer": s.layer,
        }

        # Optional fields (Schema v2.0)
        if s.parent:
            symbol_dict["parent"] = s.parent
        if s.docstring:
            symbol_dict["docstring"] = s.docstring
        if s.category:
            symbol_dict["category"] = s.category

        symbol_list.append(symbol_dict)

    return {"symbols": symbol_list}


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Extract symbols from TypeScript/JavaScript files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'path',
        help='Path to TypeScript/JavaScript file or directory to extract symbols from'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Output JSON file path (default: stdout)'
    )
    parser.add_argument(
        '--exclude-tests',
        action='store_true',
        help='Exclude test files from extraction'
    )
    parser.add_argument(
        '--exclude-private',
        action='store_true',
        help='Exclude private symbols (starting with _)'
    )
    parser.add_argument(
        '--pretty',
        action='store_true',
        help='Pretty-print JSON output'
    )

    args = parser.parse_args()

    # Validate path
    path = Path(args.path)
    if not path.exists():
        print(f"Error: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    # Extract symbols
    if path.is_file():
        if not is_typescript_file(path):
            print(f"Error: File is not a TypeScript/JavaScript file: {path}", file=sys.stderr)
            sys.exit(1)
        symbols = extract_symbols_from_file(path, path.parent)
    else:
        symbols = extract_symbols_from_directory(
            path,
            exclude_tests=args.exclude_tests,
            exclude_private=args.exclude_private
        )

    # Convert to output format
    output = symbols_to_dict(symbols)

    # Output results
    json_kwargs = {'indent': 2} if args.pretty else {}
    json_output = json.dumps(output, **json_kwargs)

    if args.output:
        output_path = Path(args.output)
        output_path.write_text(json_output, encoding='utf-8')
        print(f"Extracted {len(symbols)} symbols to {output_path}", file=sys.stderr)
    else:
        print(json_output)

    # Print summary to stderr
    if not args.output:
        print(f"\n# Extracted {len(symbols)} symbols", file=sys.stderr)
        kind_counts = {}
        for symbol in symbols:
            kind_counts[symbol.kind] = kind_counts.get(symbol.kind, 0) + 1
        for kind, count in sorted(kind_counts.items()):
            print(f"# {kind}: {count}", file=sys.stderr)


if __name__ == '__main__':
    main()
