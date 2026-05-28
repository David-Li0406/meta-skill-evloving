"""
Bug detection module using static analysis.
Detects common bugs: null references, array bounds, resource leaks, logic errors.
"""

from typing import Dict, List, Any, Optional
import re
import ast
import subprocess


class BugDetector:
    """Detect and fix common bugs using static analysis."""

    def __init__(self, language: str, config: Dict[str, Any] = None):
        """
        Initialize bug detector.

        Args:
            language: Programming language
            config: Optional configuration
        """
        self.language = language.lower()
        self.config = config or {}
        self.issues = []

    def detect_and_fix(self, code: str) -> Dict[str, Any]:
        """
        Detect bugs and attempt fixes.

        Args:
            code: Source code to analyze

        Returns:
            Dictionary with issues and optionally fixed_code
        """
        if self.language == 'python':
            return self._detect_python_bugs(code)
        elif self.language in ['javascript', 'typescript']:
            return self._detect_javascript_bugs(code)
        elif self.language == 'java':
            return self._detect_java_bugs(code)
        elif self.language == 'go':
            return self._detect_go_bugs(code)
        elif self.language == 'rust':
            return self._detect_rust_bugs(code)
        else:
            return {
                'success': False,
                'error': f'Unsupported language: {self.language}',
                'issues': []
            }

    def _detect_python_bugs(self, code: str) -> Dict[str, Any]:
        """Detect Python bugs using AST analysis and pattern matching."""
        issues = []
        fixed_code = code

        try:
            tree = ast.parse(code)
            visitor = PythonBugVisitor()
            visitor.visit(tree)
            issues.extend(visitor.issues)

            # Pattern-based detection
            pattern_issues = self._detect_python_patterns(code)
            issues.extend(pattern_issues)

            # Apply fixes
            if issues:
                fixed_code = self._apply_python_bug_fixes(code, issues)

        except SyntaxError:
            # Can't analyze if syntax is broken
            pass

        return {
            'success': True,
            'issues': issues,
            'fixed_code': fixed_code if fixed_code != code else None
        }

    def _detect_python_patterns(self, code: str) -> List[Dict[str, Any]]:
        """Detect bugs using regex patterns."""
        issues = []
        lines = code.splitlines()

        for line_num, line in enumerate(lines, start=1):
            # Detect: Mutable default arguments
            if re.search(r'def\s+\w+\([^)]*=\s*(\[\]|\{\})', line):
                issues.append({
                    'type': 'bug',
                    'severity': 'warning',
                    'line': line_num,
                    'message': 'Mutable default argument (list/dict)',
                    'suggestion': 'Use None and initialize inside function',
                    'status': 'detected'
                })

            # Detect: Bare except clause
            if re.match(r'\s*except\s*:', line):
                issues.append({
                    'type': 'bug',
                    'severity': 'warning',
                    'line': line_num,
                    'message': 'Bare except clause catches all exceptions',
                    'suggestion': 'Specify exception type',
                    'status': 'detected'
                })

            # Detect: == comparison with None
            if re.search(r'\w+\s*==\s*None', line):
                issues.append({
                    'type': 'bug',
                    'severity': 'info',
                    'line': line_num,
                    'message': 'Use "is None" instead of "== None"',
                    'fix': 'Replace with "is None"',
                    'status': 'fixable'
                })

            # Detect: Division without zero check
            if '/' in line and 'if' not in line and 'try' not in line.lower():
                # Simple heuristic - real check would need context
                if re.search(r'/\s*\w+(?!\s*[!=<>])', line):
                    issues.append({
                        'type': 'bug',
                        'severity': 'warning',
                        'line': line_num,
                        'message': 'Potential division by zero',
                        'suggestion': 'Add zero check or try/except',
                        'status': 'detected'
                    })

        return issues

    def _apply_python_bug_fixes(self, code: str, issues: List[Dict[str, Any]]) -> str:
        """Apply automated fixes for Python bugs."""
        lines = code.splitlines()
        fixed_lines = lines.copy()

        for issue in issues:
            line_idx = issue['line'] - 1
            if line_idx < 0 or line_idx >= len(fixed_lines):
                continue

            line = fixed_lines[line_idx]

            # Fix: == None -> is None
            if 'is None' in issue.get('fix', ''):
                fixed_lines[line_idx] = re.sub(r'(\w+)\s*==\s*None', r'\1 is None', line)
                issue['status'] = 'fixed'

            # Fix: != None -> is not None
            if 'is not None' in issue.get('fix', ''):
                fixed_lines[line_idx] = re.sub(r'(\w+)\s*!=\s*None', r'\1 is not None', line)
                issue['status'] = 'fixed'

        return '\n'.join(fixed_lines)

    def _detect_javascript_bugs(self, code: str) -> Dict[str, Any]:
        """Detect JavaScript/TypeScript bugs."""
        issues = []

        # Use ESLint for bug detection
        try:
            result = subprocess.run(
                ['eslint', '--format=json', '--stdin'],
                input=code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=15
            )

            import json
            output = result.stdout.decode('utf-8')
            if output:
                eslint_results = json.loads(output)

                for file_result in eslint_results:
                    for message in file_result.get('messages', []):
                        # Filter for bug-related rules
                        rule_id = message.get('ruleId', '')
                        if any(keyword in rule_id for keyword in ['null', 'undefined', 'no-unused', 'no-undef']):
                            issues.append({
                                'type': 'bug',
                                'severity': 'error' if message['severity'] == 2 else 'warning',
                                'line': message['line'],
                                'column': message['column'],
                                'message': message['message'],
                                'rule': rule_id,
                                'status': 'detected'
                            })

        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
            pass

        return {
            'success': True,
            'issues': issues,
            'fixed_code': None
        }

    def _detect_java_bugs(self, code: str) -> Dict[str, Any]:
        """Detect Java bugs using SpotBugs or similar."""
        issues = []

        # Placeholder - real implementation would use SpotBugs
        # Pattern-based detection for demo
        lines = code.splitlines()
        for line_num, line in enumerate(lines, start=1):
            # Detect: Potential null dereference
            if '.' in line and 'if' not in line.lower() and '!= null' not in line:
                if re.search(r'\w+\.(?:get|set|toString|equals)\(', line):
                    issues.append({
                        'type': 'bug',
                        'severity': 'warning',
                        'line': line_num,
                        'message': 'Potential null pointer dereference',
                        'suggestion': 'Add null check',
                        'status': 'detected'
                    })

        return {
            'success': True,
            'issues': issues,
            'fixed_code': None
        }

    def _detect_go_bugs(self, code: str) -> Dict[str, Any]:
        """Detect Go bugs using golangci-lint."""
        issues = []

        try:
            import tempfile
            import os

            with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
                f.write(code)
                temp_path = f.name

            # Run golangci-lint
            result = subprocess.run(
                ['golangci-lint', 'run', '--out-format=json', temp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=15
            )

            import json
            output = result.stdout.decode('utf-8')
            if output:
                lint_results = json.loads(output)
                for issue_data in lint_results.get('Issues', []):
                    issues.append({
                        'type': 'bug',
                        'severity': 'warning',
                        'line': issue_data.get('Pos', {}).get('Line', 0),
                        'message': issue_data.get('Text', ''),
                        'status': 'detected'
                    })

            os.unlink(temp_path)

        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
            pass

        return {
            'success': True,
            'issues': issues,
            'fixed_code': None
        }

    def _detect_rust_bugs(self, code: str) -> Dict[str, Any]:
        """Detect Rust bugs using Clippy."""
        issues = []

        # Note: Clippy requires full Cargo project context
        # Placeholder implementation
        return {
            'success': True,
            'issues': issues,
            'fixed_code': None
        }


class PythonBugVisitor(ast.NodeVisitor):
    """AST visitor to detect Python bugs."""

    def __init__(self):
        self.issues = []
        self.current_function = None

    def visit_FunctionDef(self, node):
        """Visit function definition."""
        self.current_function = node.name

        # Check for mutable default arguments
        for arg, default in zip(node.args.args[-len(node.args.defaults):], node.args.defaults):
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self.issues.append({
                    'type': 'bug',
                    'severity': 'warning',
                    'line': node.lineno,
                    'message': f'Mutable default argument in function {node.name}',
                    'status': 'unfixable'
                })

        self.generic_visit(node)

    def visit_Compare(self, node):
        """Visit comparison operations."""
        # Check for identity comparison with constants
        for op, comparator in zip(node.ops, node.comparators):
            if isinstance(op, ast.Eq) and isinstance(comparator, ast.Constant):
                if comparator.value is None:
                    self.issues.append({
                        'type': 'bug',
                        'severity': 'info',
                        'line': node.lineno,
                        'message': 'Use "is None" instead of "== None"',
                        'fix': 'Replace with "is None"',
                        'status': 'fixable'
                    })

        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        """Visit except handler."""
        # Check for bare except
        if node.type is None:
            self.issues.append({
                'type': 'bug',
                'severity': 'warning',
                'line': node.lineno,
                'message': 'Bare except clause catches all exceptions',
                'status': 'unfixable'
            })

        self.generic_visit(node)
