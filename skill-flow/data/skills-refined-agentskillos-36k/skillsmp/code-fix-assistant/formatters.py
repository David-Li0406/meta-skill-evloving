"""
Code formatting module.
Supports multiple languages: Python, JavaScript, TypeScript, Java, Go, Rust.
"""

from typing import Dict, Any, Optional
import subprocess
import tempfile
import os


class CodeFormatter:
    """Format code using language-specific tools."""

    FORMATTERS = {
        'python': {
            'tool': 'black',
            'command': ['black', '--quiet', '-'],
            'check_command': ['black', '--version']
        },
        'javascript': {
            'tool': 'prettier',
            'command': ['prettier', '--parser', 'babel'],
            'check_command': ['prettier', '--version']
        },
        'typescript': {
            'tool': 'prettier',
            'command': ['prettier', '--parser', 'typescript'],
            'check_command': ['prettier', '--version']
        },
        'java': {
            'tool': 'google-java-format',
            'command': ['google-java-format', '-'],
            'check_command': ['google-java-format', '--version']
        },
        'go': {
            'tool': 'gofmt',
            'command': ['gofmt'],
            'check_command': ['gofmt', '-h']
        },
        'rust': {
            'tool': 'rustfmt',
            'command': ['rustfmt'],
            'check_command': ['rustfmt', '--version']
        }
    }

    def __init__(self, language: str, config: Dict[str, Any] = None):
        """
        Initialize formatter.

        Args:
            language: Programming language
            config: Optional configuration overrides
        """
        self.language = language.lower()
        self.config = config or {}

        if self.language not in self.FORMATTERS:
            raise ValueError(f"Unsupported language: {language}")

        self.formatter_config = self.FORMATTERS[self.language]

    def check_tool_installed(self) -> bool:
        """Check if formatting tool is installed."""
        try:
            subprocess.run(
                self.formatter_config['check_command'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=5
            )
            return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def format(self, code: str) -> Dict[str, Any]:
        """
        Format code using language-specific formatter.

        Args:
            code: Source code to format

        Returns:
            Dictionary with formatted_code, success status, and changes_count
        """
        # Check tool installed
        if not self.check_tool_installed():
            return {
                'success': False,
                'error': f"{self.formatter_config['tool']} not installed",
                'install_command': self._get_install_command(),
                'formatted_code': code
            }

        # Run formatter
        try:
            result = subprocess.run(
                self.formatter_config['command'],
                input=code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )

            if result.returncode == 0:
                formatted_code = result.stdout.decode('utf-8')
                changes_count = self._count_changes(code, formatted_code)

                return {
                    'success': True,
                    'formatted_code': formatted_code,
                    'changes_count': changes_count
                }
            else:
                error_message = result.stderr.decode('utf-8')
                return {
                    'success': False,
                    'error': f"Formatting failed: {error_message}",
                    'formatted_code': code
                }

        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Formatting timeout (file too large or hung)',
                'formatted_code': code
            }
        except Exception as e:
            return {
                'success': False,
                'error': f"Unexpected error: {str(e)}",
                'formatted_code': code
            }

    def _count_changes(self, original: str, formatted: str) -> int:
        """Count number of line changes between original and formatted."""
        original_lines = original.splitlines()
        formatted_lines = formatted.splitlines()

        # Simple diff count (in production, use difflib for accurate count)
        changes = 0
        max_len = max(len(original_lines), len(formatted_lines))

        for i in range(max_len):
            orig_line = original_lines[i] if i < len(original_lines) else ""
            fmt_line = formatted_lines[i] if i < len(formatted_lines) else ""

            if orig_line != fmt_line:
                changes += 1

        return changes

    def _get_install_command(self) -> str:
        """Get installation command for the formatter tool."""
        install_commands = {
            'python': 'pip install black',
            'javascript': 'npm install -g prettier',
            'typescript': 'npm install -g prettier',
            'java': 'Download from https://github.com/google/google-java-format',
            'go': 'Included with Go installation',
            'rust': 'rustup component add rustfmt'
        }

        return install_commands.get(self.language, 'Check tool documentation')


class PythonFormatter(CodeFormatter):
    """Python-specific formatter with additional options."""

    def __init__(self, config: Dict[str, Any] = None):
        super().__init__('python', config)
        self.line_length = self.config.get('line_length', 88)
        self.use_isort = self.config.get('use_isort', True)

    def format(self, code: str) -> Dict[str, Any]:
        """Format Python code with Black and optionally isort."""
        # First, run Black
        result = super().format(code)

        if not result['success']:
            return result

        formatted_code = result['formatted_code']

        # Optionally run isort for import sorting
        if self.use_isort:
            isort_result = self._run_isort(formatted_code)
            if isort_result['success']:
                formatted_code = isort_result['formatted_code']

        return {
            'success': True,
            'formatted_code': formatted_code,
            'changes_count': self._count_changes(code, formatted_code)
        }

    def _run_isort(self, code: str) -> Dict[str, Any]:
        """Run isort for import sorting."""
        try:
            result = subprocess.run(
                ['isort', '-'],
                input=code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10
            )

            if result.returncode == 0:
                return {
                    'success': True,
                    'formatted_code': result.stdout.decode('utf-8')
                }
            else:
                return {
                    'success': False,
                    'formatted_code': code
                }

        except (FileNotFoundError, subprocess.TimeoutExpired):
            # isort not available or timeout, skip
            return {
                'success': False,
                'formatted_code': code
            }


class JavaScriptFormatter(CodeFormatter):
    """JavaScript/TypeScript-specific formatter with Prettier options."""

    def __init__(self, language: str = 'javascript', config: Dict[str, Any] = None):
        super().__init__(language, config)
        self.semi = self.config.get('semi', True)
        self.single_quote = self.config.get('single_quote', False)
        self.tab_width = self.config.get('tab_width', 2)

    def format(self, code: str) -> Dict[str, Any]:
        """Format with custom Prettier options."""
        command = self.formatter_config['command'].copy()

        # Add custom options
        if not self.semi:
            command.append('--no-semi')
        if self.single_quote:
            command.append('--single-quote')
        command.extend(['--tab-width', str(self.tab_width)])

        try:
            result = subprocess.run(
                command,
                input=code.encode('utf-8'),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )

            if result.returncode == 0:
                formatted_code = result.stdout.decode('utf-8')
                return {
                    'success': True,
                    'formatted_code': formatted_code,
                    'changes_count': self._count_changes(code, formatted_code)
                }
            else:
                return {
                    'success': False,
                    'error': result.stderr.decode('utf-8'),
                    'formatted_code': code
                }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'formatted_code': code
            }
