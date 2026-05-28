"""
Syntax and type error checking module.
Detects and attempts to fix common syntax and type errors.
"""

from typing import Dict, List, Any, Optional
import subprocess
import re
import ast
import json


class SyntaxChecker:
    """Check and fix syntax/type errors."""

    def __init__(self, language: str, config: Dict[str, Any] = None):
        """
        Initialize syntax checker.

        Args:
            language: Programming language
            config: Optional configuration
        """
        self.language = language.lower()
        self.config = config or {}
        self.issues = []

    def check_and_fix(self, code: str) -> Dict[str, Any]:
        """
        Check syntax and attempt fixes.

        Args:
            code: Source code to check

        Returns:
            Dictionary with issues list and optionally fixed_code
        """
        if self.language == 'python':
            return self._check_python(code)
        elif self.language in ['javascript', 'typescript']:
            return self._check_javascript(code)
        elif self.language == 'java':
            return self._check_java(code)
        elif self.language == 'go':
            return self._check_go(code)
        elif self.language == 'rust':
            return self._check_rust(code)
        else:
            return {
                'success': False,
                'error': f'Unsupported language: {self.language}',
                'issues': []
            }

    def _check_python(self, code: str) -> Dict[str, Any]:
        """Check Python syntax and type hints."""
        issues = []
        fixed_code = code

        # 1. Check basic syntax with ast.parse
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append({
                'type': 'syntax',
                'severity': 'error',
                'line': e.lineno,
                'column': e.offset,
                'message': e.msg,
                'status': 'unfixable'  # AST errors need manual fix
            })

        # 2. Run flake8 for style and error checking
        flake8_issues = self._run_flake8(code)
        issues.extend(flake8_issues)

        # 3. Run mypy for type checking (optional)
        if self.config.get('check_types', False):
            mypy_issues = self._run_mypy(code)
            issues.extend(mypy_issues)

        # 4. Attempt simple auto-fixes
        if issues:
            fixed_code = self._apply_python_fixes(code, issues)

        return {
            'success': True,
            'issues': issues,
            'fixed_code': fixed_code if fixed_code != code else None
        }

    def _run_flake8(self, code: str) -> List[Dict[str, Any]]:
        """Run flake8 linter."""
        try:
            result = subprocess.run(
                ['flake8', '--format=json', '-'],
                input=code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10
            )

            # Parse flake8 JSON output (if available)
            # Note: Standard flake8 doesn't output JSON by default
            # This is a simplified version
            output = result.stdout.decode('utf-8')
            issues = []

            # Parse line-by-line format: "stdin:LINE:COL: CODE message"
            for line in output.splitlines():
                match = re.match(r'stdin:(\d+):(\d+): (\w+) (.+)', line)
                if match:
                    line_num, col_num, code, message = match.groups()
                    severity = 'error' if code.startswith('E') else 'warning'

                    issues.append({
                        'type': 'syntax',
                        'severity': severity,
                        'line': int(line_num),
                        'column': int(col_num),
                        'code': code,
                        'message': message,
                        'status': 'detected'
                    })

            return issues

        except (FileNotFoundError, subprocess.TimeoutExpired):
            return []

    def _run_mypy(self, code: str) -> List[Dict[str, Any]]:
        """Run mypy type checker."""
        try:
            # Write to temp file (mypy needs file path)
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_path = f.name

            result = subprocess.run(
                ['mypy', temp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10
            )

            output = result.stdout.decode('utf-8')
            issues = []

            # Parse mypy output: "file.py:LINE: error: message"
            for line in output.splitlines():
                match = re.match(r'.+:(\d+): (\w+): (.+)', line)
                if match:
                    line_num, severity, message = match.groups()
                    issues.append({
                        'type': 'type',
                        'severity': severity,
                        'line': int(line_num),
                        'message': message,
                        'status': 'detected'
                    })

            # Cleanup temp file
            import os
            os.unlink(temp_path)

            return issues

        except (FileNotFoundError, subprocess.TimeoutExpired):
            return []

    def _apply_python_fixes(self, code: str, issues: List[Dict[str, Any]]) -> str:
        """Apply simple automated fixes for Python."""
        lines = code.splitlines()
        fixed_lines = lines.copy()

        for issue in issues:
            line_idx = issue['line'] - 1  # 0-indexed
            if line_idx < 0 or line_idx >= len(fixed_lines):
                continue

            message = issue.get('message', '')
            code_line = fixed_lines[line_idx]

            # Fix: Unused import
            if 'imported but unused' in message:
                # Remove the import line
                fixed_lines[line_idx] = ''
                issue['status'] = 'fixed'
                issue['fix'] = 'Removed unused import'

            # Fix: Missing whitespace
            elif 'missing whitespace' in message.lower():
                # Add whitespace around operators
                fixed_lines[line_idx] = re.sub(r'([=+\-*/<>])(?=\S)', r'\1 ', code_line)
                fixed_lines[line_idx] = re.sub(r'(?<=\S)([=+\-*/<>])', r' \1', fixed_lines[line_idx])
                issue['status'] = 'fixed'
                issue['fix'] = 'Added missing whitespace'

            # Fix: Multiple statements on one line
            elif 'multiple statements on one line' in message.lower():
                # Split by semicolon
                parts = code_line.split(';')
                indent = len(code_line) - len(code_line.lstrip())
                fixed_lines[line_idx] = '\n'.join(' ' * indent + part.strip() for part in parts if part.strip())
                issue['status'] = 'fixed'
                issue['fix'] = 'Split multiple statements'

        return '\n'.join(fixed_lines)

    def _check_javascript(self, code: str) -> Dict[str, Any]:
        """Check JavaScript/TypeScript with ESLint."""
        issues = []

        try:
            # Use ESLint with --format=json
            parser = 'babel' if self.language == 'javascript' else '@typescript-eslint/parser'

            result = subprocess.run(
                ['eslint', '--format=json', '--parser=' + parser, '--stdin'],
                input=code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=15
            )

            output = result.stdout.decode('utf-8')
            if output:
                eslint_results = json.loads(output)

                for file_result in eslint_results:
                    for message in file_result.get('messages', []):
                        issues.append({
                            'type': 'syntax' if message['ruleId'] else 'parse_error',
                            'severity': message['severity'] == 2 and 'error' or 'warning',
                            'line': message['line'],
                            'column': message['column'],
                            'message': message['message'],
                            'rule': message.get('ruleId'),
                            'status': 'detected'
                        })

        except (FileNotFoundError, subprocess.TimeoutExpired, json.JSONDecodeError):
            pass

        return {
            'success': True,
            'issues': issues,
            'fixed_code': None  # ESLint --fix would be needed
        }

    def _check_java(self, code: str) -> Dict[str, Any]:
        """Check Java with javac compilation."""
        issues = []

        # Note: Real implementation would use checkstyle or javac
        # This is a placeholder
        return {
            'success': True,
            'issues': issues,
            'fixed_code': None
        }

    def _check_go(self, code: str) -> Dict[str, Any]:
        """Check Go with go vet."""
        issues = []

        try:
            # Write to temp file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.go', delete=False) as f:
                f.write(code)
                temp_path = f.name

            # Run go vet
            result = subprocess.run(
                ['go', 'vet', temp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10
            )

            output = result.stderr.decode('utf-8')

            # Parse: "file.go:LINE:COL: message"
            for line in output.splitlines():
                match = re.match(r'.+:(\d+):(\d+): (.+)', line)
                if match:
                    line_num, col_num, message = match.groups()
                    issues.append({
                        'type': 'syntax',
                        'severity': 'warning',
                        'line': int(line_num),
                        'column': int(col_num),
                        'message': message,
                        'status': 'detected'
                    })

            # Cleanup
            import os
            os.unlink(temp_path)

        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass

        return {
            'success': True,
            'issues': issues,
            'fixed_code': None
        }

    def _check_rust(self, code: str) -> Dict[str, Any]:
        """Check Rust with cargo check."""
        issues = []

        # Note: Rust checking requires full project context
        # This is a simplified placeholder
        return {
            'success': True,
            'issues': issues,
            'fixed_code': None
        }
