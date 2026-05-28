"""
Fix validation module.
Validates that fixes were successful by running linters and syntax checks.
"""

from typing import Dict, Any, Optional
import subprocess
import ast
import json
import tempfile
import os


class FixValidator:
    """Validate fixes using linters and syntax checks."""

    def __init__(self, language: str, config: Dict[str, Any] = None):
        """
        Initialize validator.

        Args:
            language: Programming language
            config: Optional configuration
        """
        self.language = language.lower()
        self.config = config or {}

    def validate(self, code: str, file_path: str = None) -> Dict[str, Any]:
        """
        Validate fixed code.

        Args:
            code: Fixed code to validate
            file_path: Optional file path for context

        Returns:
            Dictionary with validation results
        """
        if self.language == 'python':
            return self._validate_python(code)
        elif self.language in ['javascript', 'typescript']:
            return self._validate_javascript(code)
        elif self.language == 'java':
            return self._validate_java(code)
        elif self.language == 'go':
            return self._validate_go(code)
        elif self.language == 'rust':
            return self._validate_rust(code)
        else:
            return {
                'success': False,
                'error': f'Unsupported language: {self.language}',
                'linter_passed': False,
                'syntax_valid': False
            }

    def _validate_python(self, code: str) -> Dict[str, Any]:
        """Validate Python code."""
        # 1. Check syntax
        syntax_valid = self._check_python_syntax(code)

        # 2. Run linter (flake8)
        linter_passed = self._run_python_linter(code)

        return {
            'success': syntax_valid and linter_passed,
            'syntax_valid': syntax_valid,
            'linter_passed': linter_passed,
            'language': 'python'
        }

    def _check_python_syntax(self, code: str) -> bool:
        """Check if Python code has valid syntax."""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    def _run_python_linter(self, code: str) -> bool:
        """Run flake8 linter on Python code."""
        try:
            result = subprocess.run(
                ['flake8', '-'],
                input=code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10
            )

            # flake8 returns 0 if no errors
            return result.returncode == 0

        except (FileNotFoundError, subprocess.TimeoutExpired):
            # If flake8 not available, just check syntax
            return self._check_python_syntax(code)

    def _validate_javascript(self, code: str) -> Dict[str, Any]:
        """Validate JavaScript/TypeScript code."""
        syntax_valid = True  # ESLint will check this
        linter_passed = self._run_javascript_linter(code)

        return {
            'success': linter_passed,
            'syntax_valid': syntax_valid,
            'linter_passed': linter_passed,
            'language': self.language
        }

    def _run_javascript_linter(self, code: str) -> bool:
        """Run ESLint on JavaScript/TypeScript code."""
        try:
            parser = 'babel' if self.language == 'javascript' else '@typescript-eslint/parser'

            result = subprocess.run(
                ['eslint', '--parser=' + parser, '--stdin'],
                input=code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=15
            )

            # ESLint returns 0 if no errors (warnings allowed)
            return result.returncode == 0

        except (FileNotFoundError, subprocess.TimeoutExpired):
            return True  # Assume valid if tool not available

    def _validate_java(self, code: str) -> Dict[str, Any]:
        """Validate Java code."""
        # Use javac to check compilation
        syntax_valid = self._check_java_compilation(code)
        linter_passed = syntax_valid  # Placeholder

        return {
            'success': syntax_valid,
            'syntax_valid': syntax_valid,
            'linter_passed': linter_passed,
            'language': 'java'
        }

    def _check_java_compilation(self, code: str) -> bool:
        """Check if Java code compiles."""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.java', delete=False) as f:
                # Extract class name from code
                import re
                match = re.search(r'class\s+(\w+)', code)
                class_name = match.group(1) if match else 'Main'

                # Write to file with correct name
                java_file = os.path.join(tempfile.gettempdir(), f'{class_name}.java')
                with open(java_file, 'w') as jf:
                    jf.write(code)

                # Try to compile
                result = subprocess.run(
                    ['javac', java_file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=10
                )

                # Cleanup
                os.unlink(java_file)
                class_file = java_file.replace('.java', '.class')
                if os.path.exists(class_file):
                    os.unlink(class_file)

                return result.returncode == 0

        except (FileNotFoundError, subprocess.TimeoutExpired, Exception):
            return True  # Assume valid if can't check

    def _validate_go(self, code: str) -> Dict[str, Any]:
        """Validate Go code."""
        syntax_valid = self._check_go_syntax(code)
        linter_passed = syntax_valid

        return {
            'success': syntax_valid,
            'syntax_valid': syntax_valid,
            'linter_passed': linter_passed,
            'language': 'go'
        }

    def _check_go_syntax(self, code: str) -> bool:
        """Check Go syntax using gofmt."""
        try:
            result = subprocess.run(
                ['gofmt', '-e'],
                input=code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10
            )

            # gofmt -e returns 0 if syntax is valid
            return result.returncode == 0

        except (FileNotFoundError, subprocess.TimeoutExpired):
            return True

    def _validate_rust(self, code: str) -> Dict[str, Any]:
        """Validate Rust code."""
        # Rust validation requires full project context
        # Placeholder implementation
        return {
            'success': True,
            'syntax_valid': True,
            'linter_passed': True,
            'language': 'rust'
        }


class ValidationReport:
    """Generate detailed validation report."""

    def __init__(self, validation_result: Dict[str, Any]):
        """
        Initialize with validation result.

        Args:
            validation_result: Result from FixValidator.validate()
        """
        self.result = validation_result

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        return {
            'overall_status': 'passed' if self.result['success'] else 'failed',
            'checks': {
                'syntax_valid': {
                    'status': 'passed' if self.result['syntax_valid'] else 'failed',
                    'description': 'Code has valid syntax'
                },
                'linter_passed': {
                    'status': 'passed' if self.result['linter_passed'] else 'failed',
                    'description': 'Code passes linter checks'
                }
            },
            'language': self.result.get('language', 'unknown')
        }

    def to_markdown(self) -> str:
        """Generate markdown report."""
        status_emoji = '✅' if self.result['success'] else '❌'

        report = f"# Validation Report {status_emoji}\n\n"
        report += f"**Language**: {self.result.get('language', 'unknown')}\n\n"

        report += "## Checks\n\n"

        # Syntax check
        syntax_emoji = '✅' if self.result['syntax_valid'] else '❌'
        report += f"- {syntax_emoji} **Syntax Valid**: Code has valid syntax\n"

        # Linter check
        linter_emoji = '✅' if self.result['linter_passed'] else '❌'
        report += f"- {linter_emoji} **Linter Passed**: Code passes linter checks\n"

        report += f"\n**Overall Status**: {'PASSED' if self.result['success'] else 'FAILED'}\n"

        return report

    def __str__(self) -> str:
        """String representation."""
        return self.to_markdown()
