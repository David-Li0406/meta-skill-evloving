#!/usr/bin/env python3
"""
Analyze class coupling and cohesion metrics.
Finds: Feature Envy, Low Cohesion (LCOM), Message Chains, Middle Man.
"""

import argparse
import ast
import json
from collections import defaultdict
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class CouplingIssue:
    file: str
    line: int
    issue_type: str
    name: str
    description: str
    metric_value: float
    suggestion: str
    severity: str


class ClassAnalyzer(ast.NodeVisitor):
    def __init__(self, filename: str, source_lines: list[str]):
        self.filename = filename
        self.source_lines = source_lines
        self.issues: list[CouplingIssue] = []
        self.current_class = None
        self.current_method = None
        self.class_methods: dict[str, list[str]] = defaultdict(list)
        self.class_attributes: dict[str, set[str]] = defaultdict(set)
        self.method_accesses_self: dict[str, set[str]] = defaultdict(set)
        self.method_accesses_other: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.method_calls: dict[str, list[str]] = defaultdict(list)

    def visit_ClassDef(self, node: ast.ClassDef):
        old_class = self.current_class
        self.current_class = node.name

        for item in node.body:
            if isinstance(item, ast.FunctionDef) and item.name == '__init__':
                for stmt in ast.walk(item):
                    if isinstance(stmt, ast.Assign):
                        for target in stmt.targets:
                            if isinstance(target, ast.Attribute):
                                if isinstance(target.value, ast.Name) and target.value.id == 'self':
                                    self.class_attributes[node.name].add(target.attr)

        self.generic_visit(node)
        self._analyze_class(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node: ast.FunctionDef):
        if self.current_class:
            self.class_methods[self.current_class].append(node.name)
            old_method = self.current_method
            self.current_method = f"{self.current_class}.{node.name}"
            self.generic_visit(node)
            self.current_method = old_method
        else:
            self.generic_visit(node)

    def visit_Attribute(self, node: ast.Attribute):
        if self.current_method:
            if isinstance(node.value, ast.Name):
                if node.value.id == 'self':
                    self.method_accesses_self[self.current_method].add(node.attr)
                else:
                    self.method_accesses_other[self.current_method][node.value.id] += 1

            chain_length = self._get_chain_length(node)
            if chain_length >= 3:
                self.method_calls[self.current_method].append(f"chain_{chain_length}")

        self.generic_visit(node)

    def _get_chain_length(self, node: ast.Attribute) -> int:
        length = 1
        current = node.value
        while isinstance(current, ast.Attribute):
            length += 1
            current = current.value
        return length

    def _analyze_class(self, node: ast.ClassDef):
        class_name = node.name
        methods = self.class_methods[class_name]
        attrs = self.class_attributes[class_name]

        if not methods or len(methods) < 2:
            return

        # LCOM calculation
        method_attrs = {}
        for method in methods:
            full_name = f"{class_name}.{method}"
            method_attrs[method] = self.method_accesses_self.get(full_name, set())

        pairs_sharing = 0
        pairs_not_sharing = 0
        method_list = list(method_attrs.keys())

        for i in range(len(method_list)):
            for j in range(i + 1, len(method_list)):
                m1, m2 = method_list[i], method_list[j]
                if method_attrs[m1] & method_attrs[m2]:
                    pairs_sharing += 1
                else:
                    pairs_not_sharing += 1

        lcom = max(0, pairs_not_sharing - pairs_sharing)
        if lcom > len(methods):
            self.issues.append(CouplingIssue(
                file=self.filename, line=node.lineno,
                issue_type="low_cohesion", name=class_name,
                description=f"Class has low cohesion (LCOM={lcom})",
                metric_value=lcom,
                suggestion="Methods don't share attributes - consider splitting class",
                severity="medium" if lcom < len(methods) * 2 else "high"
            ))

        # Feature Envy
        for method in methods:
            full_name = f"{class_name}.{method}"
            self_accesses = len(self.method_accesses_self.get(full_name, set()))
            other_accesses = self.method_accesses_other.get(full_name, {})

            for other_obj, count in other_accesses.items():
                if count > self_accesses and count >= 3:
                    self.issues.append(CouplingIssue(
                        file=self.filename, line=node.lineno,
                        issue_type="feature_envy",
                        name=f"{class_name}.{method}",
                        description=f"Method accesses '{other_obj}' ({count}x) more than self ({self_accesses}x)",
                        metric_value=count,
                        suggestion=f"Consider moving method to {other_obj}'s class",
                        severity="medium"
                    ))

        # Message Chains
        for method in methods:
            full_name = f"{class_name}.{method}"
            chains = [c for c in self.method_calls.get(full_name, []) if c.startswith('chain_')]
            if chains:
                max_chain = max(int(c.split('_')[1]) for c in chains)
                if max_chain >= 4:
                    self.issues.append(CouplingIssue(
                        file=self.filename, line=node.lineno,
                        issue_type="message_chain",
                        name=f"{class_name}.{method}",
                        description=f"Long message chain (depth={max_chain})",
                        metric_value=max_chain,
                        suggestion="Add delegate method or restructure",
                        severity="low" if max_chain < 5 else "medium"
                    ))

        # Middle Man
        non_dunder_methods = [m for m in methods if not m.startswith('_')]
        if non_dunder_methods:
            total_delegation = sum(
                sum(self.method_accesses_other.get(f"{class_name}.{m}", {}).values())
                for m in non_dunder_methods
            )
            total_self = sum(
                len(self.method_accesses_self.get(f"{class_name}.{m}", set()))
                for m in non_dunder_methods
            )

            if total_delegation > total_self * 3 and total_delegation > 5:
                self.issues.append(CouplingIssue(
                    file=self.filename, line=node.lineno,
                    issue_type="middle_man", name=class_name,
                    description=f"Class mostly delegates ({total_delegation} vs {total_self} self accesses)",
                    metric_value=total_delegation,
                    suggestion="Remove middle man and call delegate directly",
                    severity="low"
                ))


def analyze_file(filepath: Path) -> list[CouplingIssue]:
    try:
        source = filepath.read_text(encoding='utf-8', errors='replace')
        tree = ast.parse(source, filename=str(filepath))
        lines = source.splitlines()
        analyzer = ClassAnalyzer(str(filepath), lines)
        analyzer.visit(tree)
        return analyzer.issues
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
    parser = argparse.ArgumentParser(description="Analyze class coupling and cohesion")
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
            print("✅ No coupling/cohesion issues found!")
            return

        by_type = defaultdict(int)
        for issue in all_issues:
            by_type[issue.issue_type] += 1

        print(f"Found {len(all_issues)} coupling/cohesion issue(s):\n")
        print("Summary:")
        for t, c in sorted(by_type.items(), key=lambda x: -x[1]):
            print(f"  {t}: {c}")
        print()

        severity_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}

        for issue in all_issues:
            icon = severity_icons[issue.severity]
            print(f"{icon} [{issue.severity.upper()}] {issue.file}:{issue.line}")
            print(f"   {issue.issue_type}: {issue.name}")
            print(f"   {issue.description}")
            print(f"   → {issue.suggestion}\n")


if __name__ == '__main__':
    main()
