#!/usr/bin/env python3
"""
Analyze Python code complexity using AST.
Detects: cyclomatic complexity, cognitive complexity, nesting depth,
         function length, parameter count, class size.
"""

import argparse
import ast
import json
from collections.abc import Iterator
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class ComplexityIssue:
    file: str
    line: int
    name: str
    issue_type: str
    value: int
    threshold: int
    severity: str
    suggestion: str


@dataclass
class Config:
    max_complexity: int = 10
    max_cognitive: int = 15
    max_nesting: int = 4
    max_function_lines: int = 50
    max_params: int = 5
    max_class_methods: int = 20
    max_class_lines: int = 300


class ComplexityVisitor(ast.NodeVisitor):
    """AST visitor that calculates complexity metrics."""

    def __init__(self, filename: str, source_lines: list[str], config: Config):
        self.filename = filename
        self.source_lines = source_lines
        self.config = config
        self.issues: list[ComplexityIssue] = []
        self.current_class = None

    def _severity(self, value: int, threshold: int) -> str:
        ratio = value / threshold
        if ratio >= 2.0:
            return "high"
        elif ratio >= 1.5:
            return "medium"
        return "low"

    def _cyclomatic(self, node: ast.AST) -> int:
        """Calculate cyclomatic complexity (McCabe)."""
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
            elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                complexity += sum(1 for _ in child.generators)
            elif isinstance(child, ast.Assert):
                complexity += 1
        return complexity

    def _cognitive(self, node: ast.AST, depth: int = 0) -> int:
        """Calculate cognitive complexity (Sonar-style)."""
        total = 0
        for child in ast.iter_child_nodes(node):
            increment = 0
            nesting_inc = 0
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                increment = 1
                nesting_inc = depth
            elif isinstance(child, ast.BoolOp):
                increment = len(child.values) - 1
            elif isinstance(child, (ast.Lambda, ast.ListComp, ast.SetComp, ast.DictComp)):
                increment = 1
                nesting_inc = depth

            total += increment + nesting_inc

            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.With)):
                total += self._cognitive(child, depth + 1)
            else:
                total += self._cognitive(child, depth)
        return total

    def _max_nesting(self, node: ast.AST, depth: int = 0) -> int:
        """Find maximum nesting depth."""
        max_depth = depth
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                max_depth = max(max_depth, self._max_nesting(child, depth + 1))
            else:
                max_depth = max(max_depth, self._max_nesting(child, depth))
        return max_depth

    def _function_lines(self, node) -> int:
        """Count non-empty, non-comment lines in function."""
        if not hasattr(node, 'end_lineno') or node.end_lineno is None:
            return 0
        count = 0
        for i in range(node.lineno - 1, node.end_lineno):
            if i < len(self.source_lines):
                line = self.source_lines[i].strip()
                if line and not line.startswith('#'):
                    count += 1
        return count

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self._analyze_function(node)
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        self._analyze_function(node)
        self.generic_visit(node)

    def _analyze_function(self, node):
        name = f"{self.current_class}.{node.name}" if self.current_class else node.name

        # Cyclomatic complexity
        cc = self._cyclomatic(node)
        if cc > self.config.max_complexity:
            self.issues.append(ComplexityIssue(
                file=self.filename, line=node.lineno, name=name,
                issue_type="cyclomatic_complexity", value=cc,
                threshold=self.config.max_complexity,
                severity=self._severity(cc, self.config.max_complexity),
                suggestion="Extract methods or simplify conditionals"
            ))

        # Cognitive complexity
        cog = self._cognitive(node)
        if cog > self.config.max_cognitive:
            self.issues.append(ComplexityIssue(
                file=self.filename, line=node.lineno, name=name,
                issue_type="cognitive_complexity", value=cog,
                threshold=self.config.max_cognitive,
                severity=self._severity(cog, self.config.max_cognitive),
                suggestion="Reduce nesting and boolean operations"
            ))

        # Nesting depth
        nesting = self._max_nesting(node)
        if nesting > self.config.max_nesting:
            self.issues.append(ComplexityIssue(
                file=self.filename, line=node.lineno, name=name,
                issue_type="nesting_depth", value=nesting,
                threshold=self.config.max_nesting,
                severity=self._severity(nesting, self.config.max_nesting),
                suggestion="Use early returns or extract nested logic"
            ))

        # Function length
        lines = self._function_lines(node)
        if lines > self.config.max_function_lines:
            self.issues.append(ComplexityIssue(
                file=self.filename, line=node.lineno, name=name,
                issue_type="function_length", value=lines,
                threshold=self.config.max_function_lines,
                severity=self._severity(lines, self.config.max_function_lines),
                suggestion="Break into smaller functions"
            ))

        # Parameter count
        params = len(node.args.args) + len(node.args.kwonlyargs)
        if node.args.vararg:
            params += 1
        if node.args.kwarg:
            params += 1
        if params > self.config.max_params:
            self.issues.append(ComplexityIssue(
                file=self.filename, line=node.lineno, name=name,
                issue_type="parameter_count", value=params,
                threshold=self.config.max_params,
                severity=self._severity(params, self.config.max_params),
                suggestion="Use a config object or dataclass"
            ))

    def visit_ClassDef(self, node: ast.ClassDef):
        old_class = self.current_class
        self.current_class = node.name

        methods = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
        if len(methods) > self.config.max_class_methods:
            self.issues.append(ComplexityIssue(
                file=self.filename, line=node.lineno, name=node.name,
                issue_type="class_methods", value=len(methods),
                threshold=self.config.max_class_methods,
                severity=self._severity(len(methods), self.config.max_class_methods),
                suggestion="Split into smaller focused classes"
            ))

        if hasattr(node, 'end_lineno') and node.end_lineno:
            lines = node.end_lineno - node.lineno
            if lines > self.config.max_class_lines:
                self.issues.append(ComplexityIssue(
                    file=self.filename, line=node.lineno, name=node.name,
                    issue_type="class_size", value=lines,
                    threshold=self.config.max_class_lines,
                    severity=self._severity(lines, self.config.max_class_lines),
                    suggestion="Extract responsibilities into separate classes"
                ))

        self.generic_visit(node)
        self.current_class = old_class


def analyze_file(filepath: Path, config: Config) -> list[ComplexityIssue]:
    try:
        source = filepath.read_text(encoding='utf-8', errors='replace')
        tree = ast.parse(source, filename=str(filepath))
        lines = source.splitlines()
        visitor = ComplexityVisitor(str(filepath), lines, config)
        visitor.visit(tree)
        return visitor.issues
    except SyntaxError as e:
        return [ComplexityIssue(
            file=str(filepath), line=e.lineno or 0, name="<parse>",
            issue_type="syntax_error", value=0, threshold=0,
            severity="high", suggestion=f"Fix syntax: {e.msg}"
        )]
    except Exception:
        return []


def find_python_files(path: Path) -> Iterator[Path]:
    if path.is_file() and path.suffix == '.py':
        yield path
    elif path.is_dir():
        for p in path.rglob('*.py'):
            if '.venv' not in p.parts and 'node_modules' not in p.parts and '__pycache__' not in p.parts:
                yield p


def main():
    parser = argparse.ArgumentParser(description="Analyze Python code complexity")
    parser.add_argument('path', nargs='?', default='.', help='File or directory')
    parser.add_argument('--format', choices=['text', 'json'], default='text')
    parser.add_argument('--max-complexity', type=int, default=10)
    parser.add_argument('--max-nesting', type=int, default=4)
    parser.add_argument('--max-function-lines', type=int, default=50)
    parser.add_argument('--max-params', type=int, default=5)

    args = parser.parse_args()

    config = Config(
        max_complexity=args.max_complexity,
        max_nesting=args.max_nesting,
        max_function_lines=args.max_function_lines,
        max_params=args.max_params
    )

    all_issues = []
    for filepath in find_python_files(Path(args.path)):
        all_issues.extend(analyze_file(filepath, config))

    all_issues.sort(key=lambda x: (x.severity != 'high', x.severity != 'medium', x.file, x.line))

    if args.format == 'json':
        print(json.dumps([asdict(i) for i in all_issues], indent=2))
    else:
        if not all_issues:
            print("✅ No complexity issues found!")
            return

        severity_icons = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}
        print(f"Found {len(all_issues)} complexity issue(s):\n")
        for issue in all_issues:
            icon = severity_icons[issue.severity]
            print(f"{icon} [{issue.severity.upper()}] {issue.file}:{issue.line}")
            print(f"   {issue.name}: {issue.issue_type} = {issue.value} (threshold: {issue.threshold})")
            print(f"   → {issue.suggestion}\n")


if __name__ == '__main__':
    main()
