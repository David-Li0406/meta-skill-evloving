#!/usr/bin/env python3
"""
Detect dead code and unused code in Python.
Finds: unused imports, unused variables, unreachable code, unused functions/classes.
"""

import argparse
import ast
import json
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class DeadCodeIssue:
    file: str
    line: int
    issue_type: str
    name: str
    description: str
    confidence: int


class ScopeTracker(ast.NodeVisitor):
    def __init__(self, filename: str, source_lines: list[str]):
        self.filename = filename
        self.source_lines = source_lines
        self.issues: list[DeadCodeIssue] = []
        self.imports: dict[str, int] = {}
        self.from_imports: dict[str, int] = {}
        self.used_names: set[str] = set()
        self.functions: dict[str, int] = {}
        self.classes: dict[str, int] = {}
        self.called_functions: set[str] = set()
        self.instantiated_classes: set[str] = set()

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            name = alias.asname if alias.asname else alias.name.split('.')[0]
            self.imports[name] = node.lineno
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            if alias.name == '*':
                continue
            name = alias.asname if alias.asname else alias.name
            self.from_imports[name] = node.lineno
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        if isinstance(node.ctx, ast.Load):
            self.used_names.add(node.id)
        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        if isinstance(node.value, ast.Name):
            self.used_names.add(node.value.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if node.col_offset == 0:
            self.functions[node.name] = node.lineno
        self._check_unreachable(node)
        self._check_unused_params(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        if node.col_offset == 0:
            self.functions[node.name] = node.lineno
        self._check_unreachable(node)
        self._check_unused_params(node)
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        if node.col_offset == 0:
            self.classes[node.name] = node.lineno
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Name):
            self.called_functions.add(node.func.id)
            self.instantiated_classes.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.called_functions.add(node.func.attr)
        self.generic_visit(node)

    def _check_unreachable(self, node):
        for i, stmt in enumerate(node.body):
            if isinstance(stmt, (ast.Return, ast.Raise)):
                if i < len(node.body) - 1:
                    next_stmt = node.body[i + 1]
                    self.issues.append(DeadCodeIssue(
                        file=self.filename, line=next_stmt.lineno,
                        issue_type="unreachable_code", name="statement",
                        description=f"Code after {'return' if isinstance(stmt, ast.Return) else 'raise'} is unreachable",
                        confidence=100
                    ))

    def _check_unused_params(self, node):
        if node.name.startswith('_'):
            return

        params = set()
        for arg in node.args.args:
            if arg.arg not in ('self', 'cls'):
                params.add(arg.arg)
        for arg in node.args.kwonlyargs:
            params.add(arg.arg)

        used = set()
        for child in ast.walk(node):
            if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                used.add(child.id)

        for param in params - used:
            self.issues.append(DeadCodeIssue(
                file=self.filename, line=node.lineno,
                issue_type="unused_parameter", name=param,
                description=f"Parameter '{param}' in {node.name}() is never used",
                confidence=80
            ))

    def finalize(self):
        for name, line in self.imports.items():
            if name not in self.used_names:
                self.issues.append(DeadCodeIssue(
                    file=self.filename, line=line,
                    issue_type="unused_import", name=name,
                    description=f"Import '{name}' is never used",
                    confidence=90
                ))

        for name, line in self.from_imports.items():
            if name not in self.used_names:
                self.issues.append(DeadCodeIssue(
                    file=self.filename, line=line,
                    issue_type="unused_import", name=name,
                    description=f"Import '{name}' is never used",
                    confidence=90
                ))

        for name, line in self.functions.items():
            if name not in self.called_functions and not name.startswith('_'):
                self.issues.append(DeadCodeIssue(
                    file=self.filename, line=line,
                    issue_type="unused_function", name=name,
                    description=f"Function '{name}' appears unused in this file",
                    confidence=60
                ))

        for name, line in self.classes.items():
            if name not in self.instantiated_classes and name not in self.used_names:
                if not name.startswith('_'):
                    self.issues.append(DeadCodeIssue(
                        file=self.filename, line=line,
                        issue_type="unused_class", name=name,
                        description=f"Class '{name}' appears unused in this file",
                        confidence=60
                    ))


class RedundantCodeDetector(ast.NodeVisitor):
    def __init__(self, filename: str):
        self.filename = filename
        self.issues: list[DeadCodeIssue] = []

    def visit_If(self, node: ast.If):
        if isinstance(node.test, ast.Constant):
            if node.test.value is True:
                self.issues.append(DeadCodeIssue(
                    file=self.filename, line=node.lineno,
                    issue_type="constant_condition", name="if True",
                    description="Condition is always True",
                    confidence=100
                ))
            elif node.test.value is False:
                self.issues.append(DeadCodeIssue(
                    file=self.filename, line=node.lineno,
                    issue_type="constant_condition", name="if False",
                    description="Condition is always False, code is unreachable",
                    confidence=100
                ))

        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass) and not node.orelse:
            self.issues.append(DeadCodeIssue(
                file=self.filename, line=node.lineno,
                issue_type="empty_if", name="if ... pass",
                description="Empty if block does nothing",
                confidence=90
            ))
        self.generic_visit(node)

    def visit_While(self, node: ast.While):
        if isinstance(node.test, ast.Constant) and node.test.value is False:
            self.issues.append(DeadCodeIssue(
                file=self.filename, line=node.lineno,
                issue_type="dead_loop", name="while False",
                description="Loop will never execute",
                confidence=100
            ))
        self.generic_visit(node)


def analyze_file(filepath: Path) -> list[DeadCodeIssue]:
    try:
        source = filepath.read_text(encoding='utf-8', errors='replace')
        tree = ast.parse(source, filename=str(filepath))
        lines = source.splitlines()

        tracker = ScopeTracker(str(filepath), lines)
        tracker.visit(tree)
        tracker.finalize()

        redundant = RedundantCodeDetector(str(filepath))
        redundant.visit(tree)

        return tracker.issues + redundant.issues
    except (SyntaxError, Exception):
        return []


def find_python_files(path: Path) -> Iterator[Path]:
    if path.is_file() and path.suffix == '.py':
        yield path
    elif path.is_dir():
        for p in path.rglob('*.py'):
            if '.venv' not in p.parts and 'node_modules' not in p.parts and '__pycache__' not in p.parts:
                yield p


def main():
    parser = argparse.ArgumentParser(description="Detect dead and unused code")
    parser.add_argument('path', nargs='?', default='.', help='File or directory')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    parser.add_argument('--min-confidence', type=int, default=60)

    args = parser.parse_args()

    all_issues = []
    for filepath in find_python_files(Path(args.path)):
        all_issues.extend(analyze_file(filepath))

    all_issues = [i for i in all_issues if i.confidence >= args.min_confidence]
    all_issues.sort(key=lambda x: (-x.confidence, x.file, x.line))

    if args.format == 'json':
        print(json.dumps([asdict(i) for i in all_issues], indent=2))
    else:
        if not all_issues:
            print("✅ No dead code found!")
            return

        by_type = defaultdict(int)
        for issue in all_issues:
            by_type[issue.issue_type] += 1

        print(f"Found {len(all_issues)} potential dead code issue(s):\n")
        print("Summary:")
        for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")
        print()

        conf_icon = lambda c: '🔴' if c == 100 else ('🟡' if c >= 80 else '🟢')

        for issue in all_issues:
            icon = conf_icon(issue.confidence)
            print(f"{icon} [{issue.confidence}%] {issue.file}:{issue.line}")
            print(f"   {issue.issue_type}: {issue.name}")
            print(f"   {issue.description}\n")


if __name__ == '__main__':
    main()
