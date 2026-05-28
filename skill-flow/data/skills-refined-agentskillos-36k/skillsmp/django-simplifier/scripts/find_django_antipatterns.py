#!/usr/bin/env python3
"""
Detect Django anti-patterns and bad practices.
Comprehensive analysis of Django-specific issues.
"""

import argparse
import ast
import json
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class DjangoAntiPattern:
    file: str
    line: int
    pattern_type: str
    description: str
    suggestion: str
    severity: str
    category: str


class DjangoAntiPatternDetector(ast.NodeVisitor):
    def __init__(self, filename: str, source_lines: list[str]):
        self.filename = filename
        self.source_lines = source_lines
        self.issues: list[DjangoAntiPattern] = []
        self.in_loop = False
        self.current_class = None
        self.current_function = None
        self.function_queries = 0

    def _add(self, line: int, pattern_type: str, desc: str, suggestion: str,
             severity: str, category: str):
        self.issues.append(DjangoAntiPattern(
            file=self.filename, line=line, pattern_type=pattern_type,
            description=desc, suggestion=suggestion, severity=severity, category=category
        ))

    def visit_For(self, node: ast.For):
        old = self.in_loop
        self.in_loop = True
        self.generic_visit(node)
        self.in_loop = old

    def visit_While(self, node: ast.While):
        old = self.in_loop
        self.in_loop = True
        self.generic_visit(node)
        self.in_loop = old

    def visit_ListComp(self, node: ast.ListComp):
        old = self.in_loop
        self.in_loop = True
        self.generic_visit(node)
        self.in_loop = old

    def visit_FunctionDef(self, node: ast.FunctionDef):
        old_func, old_queries = self.current_function, self.function_queries
        self.current_function = node.name
        self.function_queries = 0
        is_view = any(arg.arg == 'request' for arg in node.args.args)

        self.generic_visit(node)

        if self.function_queries > 5 and is_view:
            self._add(node.lineno, "excessive_queries",
                f"View '{node.name}' performs {self.function_queries}+ queries",
                "Consolidate queries, use select_related/prefetch_related",
                "medium", "performance")

        self.current_function, self.function_queries = old_func, old_queries

    def visit_ClassDef(self, node: ast.ClassDef):
        old_class = self.current_class
        self.current_class = node.name
        bases = [self._get_name(b) for b in node.bases]

        if any('Model' in str(b) for b in bases):
            self._check_model(node)
        if any(v in str(b) for b in bases for v in ['View', 'ViewSet', 'APIView']):
            self._check_view_class(node)
        if any('Form' in str(b) for b in bases):
            self._check_form(node)

        self.generic_visit(node)
        self.current_class = old_class

    def _check_model(self, node: ast.ClassDef):
        methods = [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        fields = [n.targets[0].id for n in node.body if isinstance(n, ast.Assign)
                  and n.targets and isinstance(n.targets[0], ast.Name)]

        if '__str__' not in methods and fields:
            self._add(node.lineno, "missing_str_method",
                f"Model '{node.name}' lacks __str__ method",
                "Add __str__ for better admin/debug display", "low", "model")

        non_dunder = [m for m in methods if not m.startswith('_')]
        if len(non_dunder) > 15:
            self._add(node.lineno, "fat_model",
                f"Model '{node.name}' has {len(non_dunder)} methods",
                "Extract to service layer or mixins", "medium", "model")

        if len(fields) > 20:
            self._add(node.lineno, "too_many_fields",
                f"Model '{node.name}' has {len(fields)} fields",
                "Consider splitting into related models", "low", "model")

    def _check_view_class(self, node: ast.ClassDef):
        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if hasattr(item, 'end_lineno') and item.end_lineno:
                    lines = item.end_lineno - item.lineno
                    if lines > 50:
                        self._add(item.lineno, "fat_view_method",
                            f"View method '{item.name}' is {lines} lines",
                            "Extract logic to model or service", "medium", "view")

    def _check_form(self, node: ast.ClassDef):
        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == 'clean':
                for stmt in ast.walk(item):
                    if isinstance(stmt, ast.Attribute):
                        if stmt.attr in ('filter', 'get', 'exists', 'all'):
                            self._add(item.lineno, "query_in_form_clean",
                                "Database query in form clean()",
                                "Move validation queries to view", "low", "form")
                            return

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Attribute):
            attr = node.func.attr

            if attr in ('filter', 'get', 'all', 'exclude', 'annotate', 'create', 'update', 'delete'):
                self.function_queries += 1

            if attr == 'all' and self.current_function:
                self._add(node.lineno, "unbounded_queryset",
                    "QuerySet.all() without limit",
                    "Add [:limit] or use pagination", "low", "query")

            if attr == 'count':
                self._add(node.lineno, "count_vs_exists",
                    ".count() - use .exists() if just checking presence",
                    "Use .exists() for boolean checks", "low", "query")

            if attr == 'save' and self.in_loop:
                self._add(node.lineno, "save_in_loop",
                    ".save() in loop causes N writes",
                    "Use bulk_update() or bulk_create()", "high", "performance")

            if attr == 'create' and self.in_loop:
                self._add(node.lineno, "create_in_loop",
                    ".create() in loop causes N inserts",
                    "Use bulk_create()", "high", "performance")

            if attr == 'delete' and self.in_loop:
                self._add(node.lineno, "delete_in_loop",
                    ".delete() in loop",
                    "Use QuerySet.filter().delete()", "high", "performance")

            if attr == 'update':
                self._check_update_without_f(node)

            if attr in ('redirect', 'HttpResponseRedirect'):
                if node.args and isinstance(node.args[0], ast.Constant):
                    if isinstance(node.args[0].value, str) and node.args[0].value.startswith('/'):
                        self._add(node.lineno, "hardcoded_url",
                            f"Hardcoded URL: {node.args[0].value[:30]}",
                            "Use reverse() with URL name", "medium", "view")

            if attr == 'mark_safe':
                self._add(node.lineno, "mark_safe_usage",
                    "Using mark_safe() - ensure input is sanitized",
                    "Use format_html() for safe HTML", "medium", "security")

            if attr == 'raw':
                self._add(node.lineno, "raw_sql",
                    "Using raw SQL",
                    "Prefer ORM unless performance-critical", "low", "query")

            if attr == 'extra':
                self._add(node.lineno, "deprecated_extra",
                    "Using deprecated .extra()",
                    "Use annotate() with F(), Case, When", "medium", "query")

        if isinstance(node.func, ast.Name):
            if node.func.id in ('eval', 'exec'):
                self._add(node.lineno, "eval_exec_usage",
                    f"Using {node.func.id}() - security risk",
                    "Avoid eval/exec", "high", "security")

        self.generic_visit(node)

    def _check_update_without_f(self, node: ast.Call):
        for kw in node.keywords:
            if isinstance(kw.value, ast.BinOp):
                self._add(node.lineno, "update_without_f",
                    "Update with arithmetic - use F() expression",
                    "Use F('field') + 1 to avoid race conditions", "medium", "query")
                return

    def visit_Assign(self, node: ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                if target.id == 'SECRET_KEY' and isinstance(node.value, ast.Constant):
                    self._add(node.lineno, "hardcoded_secret",
                        "SECRET_KEY hardcoded",
                        "Use environment variable", "high", "security")
                if target.id == 'DEBUG':
                    if isinstance(node.value, ast.Constant) and node.value.value is True:
                        self._add(node.lineno, "debug_true",
                            "DEBUG = True in code",
                            "Use environment variable", "medium", "security")
        self.generic_visit(node)

    def _get_name(self, node) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return node.attr
        return str(node)


def check_template(filepath: Path) -> list[DjangoAntiPattern]:
    issues = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
        lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            if '.objects.' in line or '.filter(' in line:
                issues.append(DjangoAntiPattern(
                    file=str(filepath), line=i, pattern_type="template_query",
                    description="Database query in template",
                    suggestion="Move query to view", severity="high", category="query"
                ))

            if line.count('{%') >= 3:
                issues.append(DjangoAntiPattern(
                    file=str(filepath), line=i, pattern_type="template_logic",
                    description="Complex logic in template",
                    suggestion="Move to view or template tag", severity="medium", category="view"
                ))

            if '|safe' in line:
                issues.append(DjangoAntiPattern(
                    file=str(filepath), line=i, pattern_type="template_safe_filter",
                    description="Using |safe filter",
                    suggestion="Verify input is sanitized", severity="medium", category="security"
                ))
    except Exception:
        pass
    return issues


def check_urls(filepath: Path) -> list[DjangoAntiPattern]:
    issues = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
        lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            if ('path(' in line or 'url(' in line) and 'name=' not in line:
                if 'include(' not in line:
                    issues.append(DjangoAntiPattern(
                        file=str(filepath), line=i, pattern_type="url_without_name",
                        description="URL pattern without name",
                        suggestion="Add name='...' for reverse()", severity="low", category="view"
                    ))
    except Exception:
        pass
    return issues


def analyze_file(filepath: Path) -> list[DjangoAntiPattern]:
    try:
        source = filepath.read_text(encoding='utf-8', errors='replace')
        if 'django' not in source.lower() and 'models' not in source:
            return []

        tree = ast.parse(source, filename=str(filepath))
        detector = DjangoAntiPatternDetector(str(filepath), source.splitlines())
        detector.visit(tree)
        return detector.issues
    except (SyntaxError, Exception):
        return []


def find_files(path: Path) -> Iterator[tuple[Path, str]]:
    if path.is_file():
        if path.suffix == '.py':
            yield path, 'python'
        elif path.suffix == '.html':
            yield path, 'template'
    elif path.is_dir():
        for p in path.rglob('*.py'):
            if '.venv' not in p.parts and 'node_modules' not in p.parts:
                yield p, 'python'
        for p in path.rglob('*.html'):
            if '.venv' not in p.parts and 'templates' in p.parts:
                yield p, 'template'


def main():
    parser = argparse.ArgumentParser(description="Detect Django anti-patterns")
    parser.add_argument('path', nargs='?', default='.', help='File or directory')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    parser.add_argument('--category', choices=['query', 'performance', 'view', 'model', 'form', 'security'])
    parser.add_argument('--min-severity', choices=['low', 'medium', 'high'], default='low')

    args = parser.parse_args()
    severity_order = {'low': 0, 'medium': 1, 'high': 2}
    min_sev = severity_order[args.min_severity]

    all_issues = []
    for filepath, ftype in find_files(Path(args.path)):
        if ftype == 'python':
            all_issues.extend(analyze_file(filepath))
            if filepath.name == 'urls.py':
                all_issues.extend(check_urls(filepath))
        else:
            all_issues.extend(check_template(filepath))

    if args.category:
        all_issues = [i for i in all_issues if i.category == args.category]
    all_issues = [i for i in all_issues if severity_order[i.severity] >= min_sev]
    all_issues.sort(key=lambda x: (x.severity != 'high', x.severity != 'medium', x.file, x.line))

    if args.format == 'json':
        print(json.dumps([asdict(i) for i in all_issues], indent=2))
    else:
        if not all_issues:
            print("✅ No Django anti-patterns found!")
            return

        by_category = defaultdict(int)
        by_type = defaultdict(int)
        for issue in all_issues:
            by_category[issue.category] += 1
            by_type[issue.pattern_type] += 1

        print(f"Found {len(all_issues)} Django anti-pattern(s):\n")
        print("By category:")
        for cat, count in sorted(by_category.items(), key=lambda x: -x[1]):
            print(f"  {cat}: {count}")
        print("\nBy type:")
        for t, c in sorted(by_type.items(), key=lambda x: -x[1])[:10]:
            print(f"  {t}: {c}")
        print()

        severity_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
        for issue in all_issues:
            icon = severity_icons[issue.severity]
            print(f"{icon} [{issue.severity.upper()}] {issue.file}:{issue.line}")
            print(f"   [{issue.category}] {issue.pattern_type}")
            print(f"   {issue.description}")
            print(f"   → {issue.suggestion}\n")


if __name__ == '__main__':
    main()
