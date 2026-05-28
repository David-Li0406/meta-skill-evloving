#!/usr/bin/env python3
"""
Detect Django-specific issues and basic anti-patterns.
Finds: N+1 query risks, save-in-loop, fat views, hardcoded URLs, template issues.
"""

import argparse
import ast
import json
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class DjangoIssue:
    file: str
    line: int
    issue_type: str
    description: str
    suggestion: str
    severity: str


class DjangoDetector(ast.NodeVisitor):
    def __init__(self, filename: str, source_lines: list[str]):
        self.filename = filename
        self.source_lines = source_lines
        self.issues: list[DjangoIssue] = []
        self.in_loop = False
        self.current_function = None

    def _add(self, line: int, issue_type: str, desc: str, suggestion: str, severity: str = "medium"):
        self.issues.append(DjangoIssue(
            file=self.filename, line=line, issue_type=issue_type,
            description=desc, suggestion=suggestion, severity=severity
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

    def visit_FunctionDef(self, node: ast.FunctionDef):
        old = self.current_function
        self.current_function = node.name

        # Fat view detection
        if hasattr(node, 'end_lineno') and node.end_lineno:
            lines = node.end_lineno - node.lineno
            if lines > 100:
                if any(arg.arg == 'request' for arg in node.args.args):
                    self._add(node.lineno, "fat_view",
                        f"View {node.name} is {lines} lines - too complex",
                        "Extract business logic to services/models", "high")

        self.generic_visit(node)
        self.current_function = old

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Attribute):
            attr = node.func.attr

            # save() in loop
            if attr == 'save' and self.in_loop:
                self._add(node.lineno, "save_in_loop",
                    ".save() inside loop causes N writes",
                    "Use bulk_update() or bulk_create()", "high")

            # delete() in loop
            if attr == 'delete' and self.in_loop:
                self._add(node.lineno, "delete_in_loop",
                    ".delete() inside loop",
                    "Use QuerySet.filter().delete()", "high")

            # create() in loop
            if attr == 'create' and self.in_loop:
                self._add(node.lineno, "create_in_loop",
                    ".create() inside loop causes N inserts",
                    "Collect and use bulk_create()", "high")

            # N+1 risk
            if attr == 'all':
                self._add(node.lineno, "n_plus_one_risk",
                    "QuerySet.all() - ensure related objects are prefetched",
                    "Use select_related() or prefetch_related()", "low")

            # Hardcoded URLs
            if attr in ('redirect', 'HttpResponseRedirect'):
                if node.args:
                    arg = node.args[0]
                    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                        if arg.value.startswith('/'):
                            self._add(node.lineno, "hardcoded_url",
                                f"Hardcoded URL: {arg.value}",
                                "Use reverse() with URL name", "medium")

            # .get() without try/except
            if attr == 'get':
                if isinstance(node.func.value, ast.Attribute):
                    if node.func.value.attr == 'objects':
                        self._add(node.lineno, "unhandled_doesnotexist",
                            ".get() may raise DoesNotExist",
                            "Use get_object_or_404() or try/except", "low")

        self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        if self.in_loop:
            if isinstance(node.value, ast.Attribute):
                if node.value.attr.endswith('_set') or node.attr in ('all', 'filter', 'exclude'):
                    self._add(node.lineno, "query_in_loop",
                        f"QuerySet access (.{node.attr}) in loop - potential N+1",
                        "Use prefetch_related() before the loop", "high")
        self.generic_visit(node)


def check_template(filepath: Path) -> list[DjangoIssue]:
    issues = []
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
        lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            if '.objects.' in line:
                issues.append(DjangoIssue(
                    file=str(filepath), line=i,
                    issue_type="template_query",
                    description="Database query in template",
                    suggestion="Move query to view, pass in context",
                    severity="high"
                ))

            if line.count('{%') > 3:
                issues.append(DjangoIssue(
                    file=str(filepath), line=i,
                    issue_type="template_logic",
                    description="Complex logic in template",
                    suggestion="Move logic to view or template tag",
                    severity="medium"
                ))
    except Exception:
        pass
    return issues


def analyze_file(filepath: Path) -> list[DjangoIssue]:
    try:
        source = filepath.read_text(encoding='utf-8', errors='replace')
        if 'django' not in source.lower() and 'models' not in source:
            return []

        tree = ast.parse(source, filename=str(filepath))
        lines = source.splitlines()
        detector = DjangoDetector(str(filepath), lines)
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
    parser = argparse.ArgumentParser(description="Detect Django issues")
    parser.add_argument('path', nargs='?', default='.', help='File or directory')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    parser.add_argument('--min-severity', choices=['low', 'medium', 'high'], default='low')

    args = parser.parse_args()
    severity_order = {'low': 0, 'medium': 1, 'high': 2}
    min_sev = severity_order[args.min_severity]

    all_issues = []
    for filepath, ftype in find_files(Path(args.path)):
        if ftype == 'python':
            all_issues.extend(analyze_file(filepath))
        else:
            all_issues.extend(check_template(filepath))

    all_issues = [i for i in all_issues if severity_order[i.severity] >= min_sev]
    all_issues.sort(key=lambda x: (x.severity != 'high', x.severity != 'medium', x.file, x.line))

    if args.format == 'json':
        print(json.dumps([asdict(i) for i in all_issues], indent=2))
    else:
        if not all_issues:
            print("✅ No Django issues found!")
            return

        by_type = defaultdict(int)
        for issue in all_issues:
            by_type[issue.issue_type] += 1

        print(f"Found {len(all_issues)} Django issue(s):\n")
        print("Summary:")
        for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")
        print()

        severity_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
        for issue in all_issues:
            icon = severity_icons[issue.severity]
            print(f"{icon} [{issue.severity.upper()}] {issue.file}:{issue.line}")
            print(f"   {issue.issue_type}: {issue.description}")
            print(f"   → {issue.suggestion}\n")


if __name__ == '__main__':
    main()
