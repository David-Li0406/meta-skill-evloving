#!/usr/bin/env python3
"""
Detect Django-specific over-engineering patterns.
Finds: unnecessary abstractions, premature patterns, over-architected code.
"""

import argparse
import ast
import json
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class DjangoOverEngineeringIssue:
    file: str
    line: int
    issue_type: str
    name: str
    description: str
    suggestion: str
    severity: str


class DjangoProjectAnalyzer:
    def __init__(self):
        self.issues: list[DjangoOverEngineeringIssue] = []
        self.models: dict[str, dict] = {}
        self.abstract_models: set[str] = set()
        self.model_implementations: dict[str, list[str]] = defaultdict(list)
        self.custom_managers: dict[str, dict] = {}
        self.signal_receivers: list[dict] = []
        self.mixins: dict[str, dict] = {}
        self.mixin_usages: dict[str, int] = defaultdict(int)
        self.serializers: dict[str, dict] = {}
        self.forms: dict[str, dict] = {}
        self.middleware: list[dict] = []
        self.service_classes: list[dict] = []

    def analyze_file(self, filepath: Path):
        try:
            source = filepath.read_text(encoding='utf-8', errors='replace')
            if 'django' not in source.lower() and 'models' not in source:
                return
            tree = ast.parse(source, filename=str(filepath))
            visitor = DjangoOverEngineeringVisitor(str(filepath), source.splitlines(), self)
            visitor.visit(tree)
        except (SyntaxError, Exception):
            pass

    def detect_issues(self):
        # Single-implementation abstract models
        for abstract, impls in self.model_implementations.items():
            if len(impls) == 1:
                info = self.models.get(abstract, {})
                self.issues.append(DjangoOverEngineeringIssue(
                    file=info.get('file', '?'), line=info.get('line', 0),
                    issue_type="single_impl_abstract_model", name=abstract,
                    description=f"Abstract model '{abstract}' has only one child: {impls[0]}",
                    suggestion="Merge into concrete model until you need multiple",
                    severity="medium"
                ))

        # Unused abstract models
        for name, info in self.models.items():
            if info.get('is_abstract') and name not in self.model_implementations:
                self.issues.append(DjangoOverEngineeringIssue(
                    file=info.get('file', '?'), line=info.get('line', 0),
                    issue_type="unused_abstract_model", name=name,
                    description=f"Abstract model '{name}' has no implementations",
                    suggestion="Remove unused abstraction (YAGNI)",
                    severity="high"
                ))

        # Simple custom managers
        for name, info in self.custom_managers.items():
            non_dunder = [m for m in info.get('methods', []) if not m.startswith('_')]
            if len(non_dunder) <= 1:
                self.issues.append(DjangoOverEngineeringIssue(
                    file=info.get('file', '?'), line=info.get('line', 0),
                    issue_type="unnecessary_manager", name=name,
                    description=f"Manager '{name}' has only {len(non_dunder)} custom method(s)",
                    suggestion="Use QuerySet.as_manager() or model methods",
                    severity="low"
                ))

        # Signals for simple save logic
        for signal in self.signal_receivers:
            if signal.get('simple_save_signal'):
                self.issues.append(DjangoOverEngineeringIssue(
                    file=signal.get('file', '?'), line=signal.get('line', 0),
                    issue_type="unnecessary_signal", name=signal.get('name', '?'),
                    description="Signal for simple save logic",
                    suggestion="Override model.save() instead",
                    severity="medium"
                ))

        # Single-use mixins
        for name, info in self.mixins.items():
            if self.mixin_usages.get(name, 0) <= 1:
                self.issues.append(DjangoOverEngineeringIssue(
                    file=info.get('file', '?'), line=info.get('line', 0),
                    issue_type="single_use_mixin", name=name,
                    description=f"Mixin '{name}' used {self.mixin_usages.get(name, 0)} time(s)",
                    suggestion="Inline the code until reuse is needed",
                    severity="low"
                ))

        # Deep inheritance
        for name, info in {**self.serializers, **self.forms}.items():
            depth = info.get('inheritance_depth', 0)
            if depth >= 3:
                kind = 'Serializer' if name in self.serializers else 'Form'
                self.issues.append(DjangoOverEngineeringIssue(
                    file=info.get('file', '?'), line=info.get('line', 0),
                    issue_type="deep_form_inheritance", name=name,
                    description=f"{kind} '{name}' has {depth}+ levels of inheritance",
                    suggestion="Flatten hierarchy, use composition",
                    severity="medium"
                ))

        # Simple middleware
        for mw in self.middleware:
            if mw.get('simple'):
                self.issues.append(DjangoOverEngineeringIssue(
                    file=mw.get('file', '?'), line=mw.get('line', 0),
                    issue_type="unnecessary_middleware", name=mw.get('name', '?'),
                    description="Middleware with minimal logic",
                    suggestion="Use decorator or context processor",
                    severity="low"
                ))

        # Simple service layer
        for svc in self.service_classes:
            if svc.get('simple_crud'):
                self.issues.append(DjangoOverEngineeringIssue(
                    file=svc.get('file', '?'), line=svc.get('line', 0),
                    issue_type="unnecessary_service_layer", name=svc.get('name', '?'),
                    description="Service wrapping simple model operations",
                    suggestion="Use model methods or generic views",
                    severity="low"
                ))


class DjangoOverEngineeringVisitor(ast.NodeVisitor):
    def __init__(self, filename: str, source_lines: list[str], analyzer: DjangoProjectAnalyzer):
        self.filename = filename
        self.source_lines = source_lines
        self.analyzer = analyzer

    def visit_ClassDef(self, node: ast.ClassDef):
        bases = self._get_bases(node)
        methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

        # Models
        if any('Model' in b for b in bases) and not any('Manager' in b for b in bases):
            is_abstract = self._is_abstract_model(node)
            self.analyzer.models[node.name] = {
                'file': self.filename, 'line': node.lineno,
                'bases': bases, 'is_abstract': is_abstract, 'methods': methods
            }
            if is_abstract:
                self.analyzer.abstract_models.add(node.name)
            for base in bases:
                if base in self.analyzer.abstract_models or 'Abstract' in base or base.startswith('Base'):
                    self.analyzer.model_implementations[base].append(node.name)

        # Managers
        if any('Manager' in b for b in bases):
            self.analyzer.custom_managers[node.name] = {
                'file': self.filename, 'line': node.lineno, 'methods': methods
            }

        # Mixins
        if 'Mixin' in node.name:
            self.analyzer.mixins[node.name] = {
                'file': self.filename, 'line': node.lineno, 'methods': methods
            }
        for base in bases:
            if 'Mixin' in base:
                self.analyzer.mixin_usages[base] += 1

        # Serializers
        if any('Serializer' in b for b in bases):
            depth = sum(1 for b in bases if any(x in b for x in ['Base', 'Abstract', 'Serializer']))
            self.analyzer.serializers[node.name] = {
                'file': self.filename, 'line': node.lineno, 'inheritance_depth': depth
            }

        # Forms
        if any('Form' in b for b in bases):
            depth = sum(1 for b in bases if any(x in b for x in ['Base', 'Abstract', 'Form']))
            self.analyzer.forms[node.name] = {
                'file': self.filename, 'line': node.lineno, 'inheritance_depth': depth
            }

        # Middleware
        if any('Middleware' in b for b in bases) or 'Middleware' in node.name:
            self.analyzer.middleware.append({
                'file': self.filename, 'line': node.lineno,
                'name': node.name, 'simple': len(methods) <= 2
            })

        # Service classes
        if 'Service' in node.name:
            crud_names = {'create', 'get', 'update', 'delete', 'list', 'retrieve'}
            method_names = {m.lower() for m in methods}
            is_simple = method_names.issubset(crud_names | {'__init__'}) and len(methods) <= 5
            self.analyzer.service_classes.append({
                'file': self.filename, 'line': node.lineno,
                'name': node.name, 'simple_crud': is_simple
            })

        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        for decorator in node.decorator_list:
            if self._is_signal_decorator(decorator):
                is_simple = len([s for s in node.body if not isinstance(s, (ast.Pass, ast.Expr))]) <= 3
                self.analyzer.signal_receivers.append({
                    'file': self.filename, 'line': node.lineno, 'name': node.name,
                    'simple_save_signal': is_simple and self._is_save_signal(decorator)
                })
        self.generic_visit(node)

    def _get_bases(self, node: ast.ClassDef) -> list[str]:
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(base.attr)
        return bases

    def _is_abstract_model(self, node: ast.ClassDef) -> bool:
        for item in node.body:
            if isinstance(item, ast.ClassDef) and item.name == 'Meta':
                for meta_item in item.body:
                    if isinstance(meta_item, ast.Assign):
                        for target in meta_item.targets:
                            if isinstance(target, ast.Name) and target.id == 'abstract':
                                if isinstance(meta_item.value, ast.Constant):
                                    return meta_item.value.value is True
        return False

    def _is_signal_decorator(self, decorator) -> bool:
        if isinstance(decorator, ast.Call):
            if isinstance(decorator.func, ast.Name):
                return decorator.func.id == 'receiver'
        return False

    def _is_save_signal(self, decorator) -> bool:
        if isinstance(decorator, ast.Call):
            for arg in decorator.args:
                if isinstance(arg, ast.Name):
                    return arg.id in ('pre_save', 'post_save')
                if isinstance(arg, ast.Attribute):
                    return arg.attr in ('pre_save', 'post_save')
        return False


def find_python_files(path: Path) -> Iterator[Path]:
    if path.is_file() and path.suffix == '.py':
        yield path
    elif path.is_dir():
        for p in path.rglob('*.py'):
            if '.venv' not in p.parts and 'node_modules' not in p.parts:
                yield p


def main():
    parser = argparse.ArgumentParser(description="Detect Django over-engineering")
    parser.add_argument('path', nargs='?', default='.', help='File or directory')
    parser.add_argument('--format', choices=['text', 'json'], default='text')

    args = parser.parse_args()

    analyzer = DjangoProjectAnalyzer()
    for filepath in find_python_files(Path(args.path)):
        analyzer.analyze_file(filepath)
    analyzer.detect_issues()

    issues = analyzer.issues
    issues.sort(key=lambda x: (x.severity != 'high', x.severity != 'medium', x.file, x.line))

    if args.format == 'json':
        print(json.dumps({
            'issues': [asdict(i) for i in issues],
            'stats': {
                'models': len(analyzer.models),
                'abstract_models': len(analyzer.abstract_models),
                'custom_managers': len(analyzer.custom_managers),
                'mixins': len(analyzer.mixins),
                'signals': len(analyzer.signal_receivers)
            }
        }, indent=2))
    else:
        if not issues:
            print("✅ No Django over-engineering issues found!")
            print(f"\nStats: {len(analyzer.models)} models, {len(analyzer.abstract_models)} abstract")
            return

        severity_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
        by_type = defaultdict(int)
        for issue in issues:
            by_type[issue.issue_type] += 1

        print(f"Found {len(issues)} Django over-engineering issue(s):\n")
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
