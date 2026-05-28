#!/usr/bin/env python3
"""
Detect duplicate code in Python using AST structural comparison.
Finds: similar functions, duplicate code blocks, copy-paste code.
"""

import argparse
import ast
import hashlib
import json
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class DuplicateGroup:
    hash: str
    occurrences: list[dict]
    lines: int
    similarity: float


class ASTNormalizer(ast.NodeTransformer):
    def visit_Name(self, node):
        node.id = '_VAR_'
        return node

    def visit_arg(self, node):
        node.arg = '_ARG_'
        return node

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            node.value = '_STR_'
        elif isinstance(node.value, (int, float)):
            node.value = 0
        return node

    def visit_FunctionDef(self, node):
        node.name = '_FUNC_'
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node):
        node.name = '_CLASS_'
        self.generic_visit(node)
        return node


def ast_to_hash(node: ast.AST) -> str:
    normalizer = ASTNormalizer()
    normalized = normalizer.visit(ast.fix_missing_locations(node))
    dump = ast.dump(normalized, annotate_fields=False)
    return hashlib.md5(dump.encode()).hexdigest()[:12]


def count_lines(node: ast.AST) -> int:
    if hasattr(node, 'end_lineno') and node.end_lineno and hasattr(node, 'lineno'):
        return node.end_lineno - node.lineno + 1
    return 0


def get_code_preview(source_lines: list[str], start: int, end: int, max_lines: int = 3) -> str:
    preview_lines = source_lines[start-1:min(end, start-1+max_lines)]
    preview = '\n'.join(line.strip() for line in preview_lines if line.strip())
    if end - start + 1 > max_lines:
        preview += '\n...'
    return preview[:100]


class DuplicateCollector(ast.NodeVisitor):
    def __init__(self, filename: str, source_lines: list[str], min_lines: int = 5):
        self.filename = filename
        self.source_lines = source_lines
        self.min_lines = min_lines
        self.blocks: list[dict] = []

    def _add_block(self, node, block_type: str, name: str):
        lines = count_lines(node)
        if lines >= self.min_lines:
            self.blocks.append({
                'type': block_type,
                'name': name,
                'file': self.filename,
                'line': node.lineno,
                'end_line': getattr(node, 'end_lineno', node.lineno + lines),
                'lines': lines,
                'hash': ast_to_hash(node),
                'preview': get_code_preview(self.source_lines, node.lineno,
                    getattr(node, 'end_lineno', node.lineno + lines))
            })

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._add_block(node, 'function', node.name)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._add_block(node, 'function', node.name)
        self.generic_visit(node)

    def visit_If(self, node: ast.If):
        self._add_block(node, 'if_block', f'if at line {node.lineno}')
        self.generic_visit(node)

    def visit_For(self, node: ast.For):
        self._add_block(node, 'for_loop', f'for at line {node.lineno}')
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        self._add_block(node, 'while_loop', f'while at line {node.lineno}')
        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        self._add_block(node, 'try_block', f'try at line {node.lineno}')
        self.generic_visit(node)


def analyze_file(filepath: Path, min_lines: int) -> list[dict]:
    try:
        source = filepath.read_text(encoding='utf-8', errors='replace')
        tree = ast.parse(source, filename=str(filepath))
        lines = source.splitlines()
        collector = DuplicateCollector(str(filepath), lines, min_lines)
        collector.visit(tree)
        return collector.blocks
    except (SyntaxError, Exception):
        return []


def find_python_files(path: Path) -> Iterator[Path]:
    if path.is_file() and path.suffix == '.py':
        yield path
    elif path.is_dir():
        for p in path.rglob('*.py'):
            if '.venv' not in p.parts and 'node_modules' not in p.parts and '__pycache__' not in p.parts:
                yield p


def find_duplicates(path: Path, min_lines: int) -> list[DuplicateGroup]:
    all_blocks = []
    for filepath in find_python_files(path):
        all_blocks.extend(analyze_file(filepath, min_lines))

    by_hash = defaultdict(list)
    for block in all_blocks:
        by_hash[block['hash']].append(block)

    duplicates = []
    for hash_val, blocks in by_hash.items():
        if len(blocks) >= 2:
            avg_lines = sum(b['lines'] for b in blocks) / len(blocks)
            duplicates.append(DuplicateGroup(
                hash=hash_val,
                occurrences=[{
                    'file': b['file'], 'line': b['line'],
                    'name': b['name'], 'type': b['type'], 'preview': b['preview']
                } for b in blocks],
                lines=int(avg_lines),
                similarity=1.0
            ))

    duplicates.sort(key=lambda x: (-len(x.occurrences), -x.lines))
    return duplicates


def main():
    parser = argparse.ArgumentParser(description="Detect duplicate code in Python")
    parser.add_argument('path', nargs='?', default='.', help='File or directory')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    parser.add_argument('--min-lines', type=int, default=5)

    args = parser.parse_args()
    duplicates = find_duplicates(Path(args.path), args.min_lines)

    if args.format == 'json':
        print(json.dumps([asdict(d) for d in duplicates], indent=2))
    else:
        if not duplicates:
            print("✅ No duplicate code found!")
            return

        total_occurrences = sum(len(d.occurrences) for d in duplicates)
        total_duplicate_lines = sum(d.lines * (len(d.occurrences) - 1) for d in duplicates)

        print(f"Found {len(duplicates)} duplicate code pattern(s)")
        print(f"Total: {total_occurrences} occurrences, ~{total_duplicate_lines} redundant lines\n")

        for i, dup in enumerate(duplicates, 1):
            print(f"{'='*60}")
            print(f"Duplicate #{i} ({len(dup.occurrences)} occurrences, ~{dup.lines} lines each)")
            print(f"{'='*60}")

            for occ in dup.occurrences:
                print(f"\n📍 {occ['file']}:{occ['line']} ({occ['type']}: {occ['name']})")
                for line in occ['preview'].split('\n'):
                    print(f"   {line}")
            print()

        print("\n💡 Suggestion: Extract duplicate code into shared functions/classes")


if __name__ == '__main__':
    main()
