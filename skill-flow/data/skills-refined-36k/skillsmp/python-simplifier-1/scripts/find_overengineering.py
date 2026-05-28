#!/usr/bin/env python3
"""
Detect over-engineering patterns in Python code.
Finds: YAGNI violations, speculative generality, premature abstraction,
       single-implementation interfaces, excessive layering, thin wrappers.
"""

import argparse
import ast
import json
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class OverEngineeringIssue:
    file: str
    line: int
    issue_type: str
    name: str
    description: str
    suggestion: str
    severity: str


class ProjectAnalyzer:
    def __init__(self):
        self.classes: dict[str, dict] = {}
        self.abstract_classes: set[str] = set()
        self.implementations: dict[str, list[str]] = defaultdict(list)
        self.factory_classes: list[tuple[str, str, int]] = []
        self.builder_classes: list[tuple[str, str, int]] = []
        self.strategy_classes: list[tuple[str, str, int]] = []
        self.thin_wrappers: list[tuple[str, str, int, str]] = []
        self.issues: list[OverEngineeringIssue] = []

    def analyze_file(self, filepath: Path):
        try:
            source = filepath.read_text(encoding='utf-8', errors='replace')
            tree = ast.parse(source, filename=str(filepath))
            visitor = ClassCollector(str(filepath), source.splitlines(), self)
            visitor.visit(tree)
        except (SyntaxError, Exception):
            pass

    def detect_issues(self):
        # Single-implementation abstract classes
        for base, subclasses in self.implementations.items():
            if base in self.abstract_classes and len(subclasses) == 1:
                info = self.classes.get(base, {})
                self.issues.append(OverEngineeringIssue(
                    file=info.get('file', '?'), line=info.get('line', 0),
                    issue_type="single_implementation",
                    name=base,
                    description=f"Abstract class {base} has only one implementation: {subclasses[0]}",
                    suggestion="Merge abstract and implementation or wait until you need abstraction",
                    severity="medium"
                ))

        # Unused abstract classes
        for cls in self.abstract_classes:
            if cls not in self.implementations or len(self.implementations[cls]) == 0:
                info = self.classes.get(cls, {})
                self.issues.append(OverEngineeringIssue(
                    file=info.get('file', '?'), line=info.get('line', 0),
                    issue_type="unused_abstraction",
                    name=cls,
                    description=f"Abstract class {cls} has no implementations",
                    suggestion="Remove unused abstraction (YAGNI)",
                    severity="high"
                ))

        # Unnecessary factories
        for name, file, line in self.factory_classes:
            self.issues.append(OverEngineeringIssue(
                file=file, line=line,
                issue_type="unnecessary_factory",
                name=name,
                description=f"Factory class {name} may be unnecessary",
                suggestion="Use direct instantiation unless you need runtime polymorphism",
                severity="low"
            ))

        # Unnecessary builders
        for name, file, line in self.builder_classes:
            info = self.classes.get(name, {})
            if len(info.get('methods', [])) < 5:
                self.issues.append(OverEngineeringIssue(
                    file=file, line=line,
                    issue_type="unnecessary_builder",
                    name=name,
                    description=f"Builder {name} may be over-engineering for simple object",
                    suggestion="Use dataclass with defaults or simple constructor",
                    severity="low"
                ))

        # Thin wrappers
        for name, file, line, wrapped in self.thin_wrappers:
            self.issues.append(OverEngineeringIssue(
                file=file, line=line,
                issue_type="thin_wrapper",
                name=name,
                description=f"Class {name} is a thin wrapper around {wrapped}",
                suggestion="Use the wrapped class directly unless abstraction is needed",
                severity="low"
            ))

        # Premature strategy pattern
        for name, file, line in self.strategy_classes:
            self.issues.append(OverEngineeringIssue(
                file=file, line=line,
                issue_type="premature_strategy",
                name=name,
                description=f"Strategy interface {name} may be premature",
                suggestion="Implement strategies when you have multiple, not before",
                severity="low"
            ))


class ClassCollector(ast.NodeVisitor):
    def __init__(self, filename: str, source_lines: list[str], analyzer: ProjectAnalyzer):
        self.filename = filename
        self.source_lines = source_lines
        self.analyzer = analyzer

    def visit_ClassDef(self, node: ast.ClassDef):
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(base.attr)

        methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

        is_abstract = False
        for base in bases:
            if 'ABC' in base or 'Abstract' in base:
                is_abstract = True

        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for decorator in item.decorator_list:
                    if isinstance(decorator, ast.Name) and decorator.id == 'abstractmethod':
                        is_abstract = True
                    elif isinstance(decorator, ast.Attribute) and decorator.attr == 'abstractmethod':
                        is_abstract = True

        self.analyzer.classes[node.name] = {
            'bases': bases, 'methods': methods,
            'file': self.filename, 'line': node.lineno, 'is_abstract': is_abstract
        }

        if is_abstract:
            self.analyzer.abstract_classes.add(node.name)

        for base in bases:
            self.analyzer.implementations[base].append(node.name)

        # Factory pattern
        if 'Factory' in node.name or any('create' in m.lower() for m in methods):
            create_methods = [m for m in methods if 'create' in m.lower()]
            if create_methods and len(methods) <= 3:
                self.analyzer.factory_classes.append((node.name, self.filename, node.lineno))

        # Builder pattern
        if 'Builder' in node.name:
            self.analyzer.builder_classes.append((node.name, self.filename, node.lineno))

        # Strategy pattern
        if is_abstract and len(methods) == 1 and ('Strategy' in node.name or 'Policy' in node.name):
            self.analyzer.strategy_classes.append((node.name, self.filename, node.lineno))

        # Thin wrapper detection
        self._check_thin_wrapper(node)

        self.generic_visit(node)

    def _check_thin_wrapper(self, node: ast.ClassDef):
        init_method = None
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                init_method = item
                break

        if not init_method:
            return

        stored_attrs = []
        for stmt in ast.walk(init_method):
            if isinstance(stmt, ast.Assign):
                for target in stmt.targets:
                    if isinstance(target, ast.Attribute):
                        if isinstance(target.value, ast.Name) and target.value.id == 'self':
                            stored_attrs.append(target.attr)

        if len(stored_attrs) == 1:
            wrapped_attr = stored_attrs[0]
            methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name != '__init__']

            if methods:
                delegate_count = 0
                for method in methods:
                    for stmt in ast.walk(method):
                        if isinstance(stmt, ast.Attribute):
                            if isinstance(stmt.value, ast.Attribute):
                                if stmt.value.attr == wrapped_attr:
                                    delegate_count += 1
                                    break

                if delegate_count >= len(methods) * 0.7 and len(methods) > 1:
                    self.analyzer.thin_wrappers.append((node.name, self.filename, node.lineno, wrapped_attr))


def find_python_files(path: Path) -> Iterator[Path]:
    if path.is_file() and path.suffix == '.py':
        yield path
    elif path.is_dir():
        for p in path.rglob('*.py'):
            if '.venv' not in p.parts and 'node_modules' not in p.parts and '__pycache__' not in p.parts:
                yield p


def main():
    parser = argparse.ArgumentParser(description="Detect over-engineering patterns")
    parser.add_argument('path', nargs='?', default='.', help='File or directory')
    parser.add_argument('--format', choices=['text', 'json'], default='text')

    args = parser.parse_args()

    analyzer = ProjectAnalyzer()
    for filepath in find_python_files(Path(args.path)):
        analyzer.analyze_file(filepath)
    analyzer.detect_issues()

    issues = analyzer.issues
    issues.sort(key=lambda x: (x.severity != 'high', x.severity != 'medium', x.file, x.line))

    if args.format == 'json':
        print(json.dumps({
            'issues': [asdict(i) for i in issues],
            'stats': {
                'total_classes': len(analyzer.classes),
                'abstract_classes': len(analyzer.abstract_classes)
            }
        }, indent=2))
    else:
        if not issues:
            print("✅ No over-engineering issues found!")
            print(f"\nStats: {len(analyzer.classes)} classes, {len(analyzer.abstract_classes)} abstract")
            return

        severity_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
        by_type = defaultdict(int)
        for issue in issues:
            by_type[issue.issue_type] += 1

        print(f"Found {len(issues)} over-engineering issue(s):\n")
        print("Summary:")
        for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")
        print()

        for issue in issues:
            icon = severity_icons[issue.severity]
            print(f"{icon} [{issue.severity.upper()}] {issue.file}:{issue.line}")
            print(f"   {issue.issue_type}: {issue.name}")
            print(f"   {issue.description}")
            print(f"   → {issue.suggestion}\n")


if __name__ == '__main__':
    main()
