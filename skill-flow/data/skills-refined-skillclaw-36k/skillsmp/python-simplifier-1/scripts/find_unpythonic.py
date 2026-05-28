#!/usr/bin/env python3
"""
Detect unpythonic patterns in Python code.
Finds: non-idiomatic patterns that have cleaner Pythonic alternatives.
"""

import argparse
import ast
import json
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class UnpythonicPattern:
    file: str
    line: int
    pattern_type: str
    description: str
    before: str
    after: str
    severity: str


class UnpythonicDetector(ast.NodeVisitor):
    def __init__(self, filename: str, source_lines: list[str]):
        self.filename = filename
        self.source_lines = source_lines
        self.issues: list[UnpythonicPattern] = []

    def _add(self, line: int, pattern_type: str, desc: str, before: str, after: str, severity: str = "low"):
        self.issues.append(UnpythonicPattern(
            file=self.filename, line=line, pattern_type=pattern_type,
            description=desc, before=before, after=after, severity=severity
        ))

    def visit_For(self, node: ast.For):
        # range(len(x)) pattern
        if isinstance(node.iter, ast.Call):
            if isinstance(node.iter.func, ast.Name) and node.iter.func.id == 'range':
                if node.iter.args:
                    first_arg = node.iter.args[0]
                    if isinstance(first_arg, ast.Call):
                        if isinstance(first_arg.func, ast.Name) and first_arg.func.id == 'len':
                            self._add(node.lineno, "range_len_loop",
                                "Using range(len()) instead of enumerate or direct iteration",
                                "for i in range(len(x)): x[i]",
                                "for item in x: ... or for i, item in enumerate(x):",
                                "medium")

        # Manual index tracking
        for stmt in node.body:
            if isinstance(stmt, ast.AugAssign):
                if isinstance(stmt.op, ast.Add):
                    if isinstance(stmt.value, ast.Constant) and stmt.value.value == 1:
                        if isinstance(stmt.target, ast.Name):
                            self._add(node.lineno, "manual_index",
                                "Manual index tracking instead of enumerate()",
                                "i = 0; for x in items: i += 1",
                                "for i, x in enumerate(items):",
                                "low")
                            break

        self.generic_visit(node)

    def visit_Compare(self, node: ast.Compare):
        for i, (op, comparator) in enumerate(zip(node.ops, node.comparators, strict=False)):
            if isinstance(op, ast.Eq):
                if isinstance(comparator, ast.Constant):
                    if comparator.value is True:
                        self._add(node.lineno, "compare_to_true",
                            "Comparing to True explicitly",
                            "if x == True:", "if x:", "low")
                    elif comparator.value is False:
                        self._add(node.lineno, "compare_to_false",
                            "Comparing to False explicitly",
                            "if x == False:", "if not x:", "low")

            if isinstance(op, (ast.Eq, ast.NotEq)):
                if isinstance(comparator, ast.Constant) and comparator.value is None:
                    op_name = '==' if isinstance(op, ast.Eq) else '!='
                    is_name = 'is' if isinstance(op, ast.Eq) else 'is not'
                    self._add(node.lineno, "compare_none_equality",
                        f"Using {op_name} None instead of {is_name} None",
                        f"if x {op_name} None:", f"if x {is_name} None:", "medium")

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr == 'keys':
                self._add(node.lineno, "dict_keys_iteration",
                    "Using .keys() is usually unnecessary",
                    "for k in d.keys():", "for k in d:", "low")

            if isinstance(node.func, ast.Name) and node.func.id == 'sorted':
                if node.args:
                    arg = node.args[0]
                    if isinstance(arg, ast.Call):
                        if isinstance(arg.func, ast.Attribute) and arg.func.attr == 'keys':
                            self._add(node.lineno, "sorted_dict_keys",
                                "sorted(d.keys()) is redundant",
                                "sorted(d.keys())", "sorted(d)", "low")

        self.generic_visit(node)

    def visit_Try(self, node: ast.Try):
        for handler in node.handlers:
            if len(handler.body) == 1 and isinstance(handler.body[0], ast.Pass):
                if handler.type is None:
                    self._add(handler.lineno, "swallowed_exception",
                        "Bare except with pass swallows all exceptions",
                        "except: pass",
                        "except SpecificError: handle_or_log()",
                        "high")
                else:
                    self._add(handler.lineno, "silent_exception",
                        "Exception caught but silently ignored",
                        "except Error: pass",
                        "except Error: logger.debug(...) or raise",
                        "medium")
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        if len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and isinstance(node.value, ast.BinOp):
                if isinstance(node.value.left, ast.Name):
                    if target.id == node.value.left.id:
                        op_map = {
                            ast.Add: '+=', ast.Sub: '-=', ast.Mult: '*=',
                            ast.Div: '/=', ast.Mod: '%=', ast.FloorDiv: '//='
                        }
                        op_type = type(node.value.op)
                        if op_type in op_map:
                            self._add(node.lineno, "augmented_assignment",
                                f"Use {op_map[op_type]} instead of explicit assignment",
                                f"x = x {op_map[op_type][0]} y",
                                f"x {op_map[op_type]} y", "low")
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import):
        if len(node.names) > 1:
            self._add(node.lineno, "multiple_imports",
                "Multiple imports on one line",
                "import os, sys",
                "import os\\nimport sys", "low")
        self.generic_visit(node)


def analyze_file(filepath: Path) -> list[UnpythonicPattern]:
    try:
        source = filepath.read_text(encoding='utf-8', errors='replace')
        tree = ast.parse(source, filename=str(filepath))
        lines = source.splitlines()
        detector = UnpythonicDetector(str(filepath), lines)
        detector.visit(tree)
        return detector.issues
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
    parser = argparse.ArgumentParser(description="Detect unpythonic patterns")
    parser.add_argument('path', nargs='?', default='.', help='File or directory')
    parser.add_argument('--format', choices=['text', 'json'], default='text')

    args = parser.parse_args()

    all_issues = []
    for filepath in find_python_files(Path(args.path)):
        all_issues.extend(analyze_file(filepath))

    all_issues.sort(key=lambda x: (x.severity != 'high', x.severity != 'medium', x.file, x.line))

    if args.format == 'json':
        print(json.dumps([asdict(i) for i in all_issues], indent=2))
    else:
        if not all_issues:
            print("✅ No unpythonic patterns found!")
            return

        by_type = defaultdict(int)
        for issue in all_issues:
            by_type[issue.pattern_type] += 1

        print(f"Found {len(all_issues)} unpythonic pattern(s):\n")
        print("Summary:")
        for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")
        print()

        severity_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}

        for issue in all_issues:
            icon = severity_icons[issue.severity]
            print(f"{icon} [{issue.severity.upper()}] {issue.file}:{issue.line}")
            print(f"   {issue.pattern_type}: {issue.description}")
            print(f"   Before: {issue.before}")
            print(f"   After:  {issue.after}\n")


if __name__ == '__main__':
    main()
