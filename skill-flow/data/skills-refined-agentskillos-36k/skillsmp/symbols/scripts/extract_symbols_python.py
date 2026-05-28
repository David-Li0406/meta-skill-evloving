#!/usr/bin/env python3
"""
Python Symbol Extractor

Extracts symbols from Python files including modules, classes, functions, methods.
Supports batch processing for entire directories and outputs JSON-compatible metadata.

Configuration:
    Can use symbols.config.json for extraction settings (directories, excludes).
    Falls back to command-line arguments if config is not available.

Usage:
    python extract_symbols_python.py <path> [--output=file.json] [--exclude-tests] [--exclude-private]

Examples:
    # Extract symbols from backend directory
    python extract_symbols_python.py backend

    # Extract with output file
    python extract_symbols_python.py api --output=api_symbols.json

    # Exclude test files and private methods
    python extract_symbols_python.py backend --exclude-tests --exclude-private

Output Format:
    {
        "symbols": [
            {
                "name": "ClassName",
                "kind": "class",
                "path": "app/services/prompt_service.py",
                "line": 42,
                "signature": "class ClassName(BaseClass)",
                "summary": "First line of docstring or description"
            }
        ]
    }

Symbol Kinds:
    - class: Class declarations
    - function: Module-level functions
    - method: Class methods (includes class context)
    - async_function: Async functions
    - async_method: Async methods
"""

import ast
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
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
    layer: str  # Architectural layer: router, service, repository, schema, model, core
    parent: Optional[str] = None  # For methods, the class name
    docstring: Optional[str] = None  # Full docstring
    category: Optional[str] = None  # File category: business_logic, test, script, etc.


class PythonSymbolExtractor(ast.NodeVisitor):
    """AST visitor that extracts symbols from Python source code."""

    def __init__(self, file_path: str, source_code: str):
        self.file_path = file_path
        self.source_code = source_code
        self.symbols: List[Symbol] = []
        self.current_class: Optional[str] = None
        self.source_lines = source_code.splitlines()

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Extract class definitions."""
        # Skip private classes if configured
        if node.name.startswith('_'):
            return

        # Build class signature
        bases = [self._get_name(base) for base in node.bases]
        if bases:
            signature = f"class {node.name}({', '.join(bases)})"
        else:
            signature = f"class {node.name}"

        # Extract docstring
        docstring = ast.get_docstring(node)
        summary = self._extract_docstring_summary(docstring)

        symbol = Symbol(
            name=node.name,
            kind="class",
            path=self.file_path,
            line=node.lineno,
            signature=signature,
            summary=summary,
            layer="unknown",  # Will be set by categorize_file
            docstring=docstring if docstring else None
        )
        self.symbols.append(symbol)

        # Visit methods within this class
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Extract function and method definitions."""
        # Skip private functions/methods if configured
        if node.name.startswith('_') and not node.name.startswith('__'):
            return

        # Determine if this is a method or function
        if self.current_class:
            kind = "method"
            parent = self.current_class
        else:
            kind = "function"
            parent = None

        # Build signature
        signature = self._build_signature(node)

        # Extract docstring
        docstring = ast.get_docstring(node)
        summary = self._extract_docstring_summary(docstring)

        symbol = Symbol(
            name=node.name,
            kind=kind,
            path=self.file_path,
            line=node.lineno,
            signature=signature,
            summary=summary,
            layer="unknown",  # Will be set by categorize_file
            parent=parent,
            docstring=docstring if docstring else None
        )
        self.symbols.append(symbol)

        # Don't visit nested functions
        # self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Extract async function and method definitions."""
        # Skip private functions/methods if configured
        if node.name.startswith('_') and not node.name.startswith('__'):
            return

        # Determine if this is an async method or function
        if self.current_class:
            kind = "async_method"
            parent = self.current_class
        else:
            kind = "async_function"
            parent = None

        # Build signature
        signature = self._build_signature(node, is_async=True)

        # Extract docstring
        docstring = ast.get_docstring(node)
        summary = self._extract_docstring_summary(docstring)

        symbol = Symbol(
            name=node.name,
            kind=kind,
            path=self.file_path,
            line=node.lineno,
            signature=signature,
            summary=summary,
            layer="unknown",  # Will be set by categorize_file
            parent=parent,
            docstring=docstring if docstring else None
        )
        self.symbols.append(symbol)

    def _build_signature(self, node: ast.FunctionDef | ast.AsyncFunctionDef, is_async: bool = False) -> str:
        """Build function/method signature string."""
        # Get function arguments
        args = []

        # Regular arguments
        for arg in node.args.args:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {self._get_annotation(arg.annotation)}"
            args.append(arg_str)

        # Keyword-only arguments
        for arg in node.args.kwonlyargs:
            arg_str = arg.arg
            if arg.annotation:
                arg_str += f": {self._get_annotation(arg.annotation)}"
            args.append(arg_str)

        # Return type
        return_type = ""
        if node.returns:
            return_type = f" -> {self._get_annotation(node.returns)}"

        # Build signature
        async_prefix = "async " if is_async else ""
        signature = f"{async_prefix}{node.name}({', '.join(args)}){return_type}"

        return signature

    def _get_annotation(self, annotation: ast.expr) -> str:
        """Convert annotation AST node to string."""
        try:
            return ast.unparse(annotation)
        except Exception:
            return "Any"

    def _get_name(self, node: ast.expr) -> str:
        """Get name from AST node."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        else:
            try:
                return ast.unparse(node)
            except Exception:
                return "Unknown"

    def _extract_docstring_summary(self, docstring: Optional[str]) -> str:
        """Extract summary from docstring (first line or first 100 characters)."""
        if not docstring:
            return ""

        # Get first line or first 100 characters
        first_line = docstring.split('\n')[0].strip()
        if len(first_line) > 100:
            return first_line[:97] + "..."
        return first_line


def is_test_file(file_path: Path) -> bool:
    """Check if a file is a test file."""
    parts = file_path.parts
    return (
        'test' in parts or
        'tests' in parts or
        file_path.name.startswith('test_') or
        file_path.name.endswith('_test.py')
    )


def categorize_file(file_path: Path) -> tuple[str, str]:
    """
    Categorize a file by its architectural layer and optional category.

    Returns:
        Tuple of (layer, category) where:
        - layer: Architectural layer (router, service, repository, schema, model, core, middleware, auth, observability, test)
        - category: Optional file category (business_logic, test, script, config, migration)
    """
    path_str = str(file_path).lower()
    parts = file_path.parts
    name = file_path.name.lower()

    # Test files
    if is_test_file(file_path):
        return ("test", "test")

    # Routers/API endpoints
    if any(p in parts for p in ['routes', 'routers', 'api']) and ('router' in name or 'endpoint' in name):
        return ("router", "business_logic")

    # Services
    if 'services' in parts or 'service' in name:
        return ("service", "business_logic")

    # Repositories
    if 'repositories' in parts or 'repository' in name or 'repo' in name:
        return ("repository", "business_logic")

    # Schemas/DTOs
    if 'schemas' in parts or 'schema' in name or 'dto' in name:
        return ("schema", "business_logic")

    # Models (ORM definitions)
    if 'models' in parts or 'model' in name:
        return ("model", "business_logic")

    # Middleware
    if 'middleware' in parts or 'middleware' in name:
        return ("middleware", "business_logic")

    # Auth
    if 'auth' in parts or 'auth' in name:
        return ("auth", "business_logic")

    # Observability (logging, tracing, monitoring)
    if any(p in parts for p in ['observability', 'logging', 'tracing', 'monitoring']):
        return ("observability", "business_logic")

    # Migrations
    if 'migrations' in parts or 'alembic' in parts or name.startswith('migration_'):
        return ("core", "migration")

    # Scripts
    if 'scripts' in parts or file_path.parent.name == 'scripts':
        return ("core", "script")

    # Config files
    if 'config' in name or name in ['settings.py', 'constants.py', '__init__.py']:
        return ("core", "config")

    # Core (database, cache, utilities)
    if any(p in parts for p in ['core', 'db', 'cache', 'utils', 'helpers']):
        return ("core", "business_logic")

    # Default: core business logic
    return ("core", "business_logic")


def extract_symbols_from_file(file_path: Path, base_path: Path) -> List[Symbol]:
    """Extract symbols from a single Python file."""
    try:
        source_code = file_path.read_text(encoding='utf-8')

        # Parse the AST
        tree = ast.parse(source_code, filename=str(file_path))

        # Calculate relative path
        rel_path = file_path.relative_to(base_path)

        # Categorize file (layer and category)
        layer, category = categorize_file(file_path)

        # Extract symbols
        extractor = PythonSymbolExtractor(str(rel_path), source_code)
        extractor.visit(tree)

        # Add layer and category to all symbols
        for symbol in extractor.symbols:
            symbol.layer = layer
            symbol.category = category

        return extractor.symbols

    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return []


def extract_symbols_from_directory(
    directory: Path,
    exclude_tests: bool = False,
    exclude_private: bool = False
) -> List[Symbol]:
    """Extract symbols from all Python files in a directory."""
    symbols: List[Symbol] = []

    # Find all Python files
    python_files = directory.rglob('*.py')

    for file_path in python_files:
        # Skip __pycache__ and other special directories
        if '__pycache__' in file_path.parts or '.venv' in file_path.parts:
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
                if not s.name.startswith('_') or s.name.startswith('__')
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
        description="Extract symbols from Python files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument(
        'path',
        help='Path to Python file or directory to extract symbols from'
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
        help='Exclude private methods and functions (starting with _)'
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
        if not path.suffix == '.py':
            print(f"Error: File is not a Python file: {path}", file=sys.stderr)
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
