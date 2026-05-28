"""
Main code fixing engine.
Coordinates all fix steps: formatting, syntax checking, bug detection, and validation.
"""

from typing import Dict, List, Any, Optional
import json
import os
from pathlib import Path

from formatters import CodeFormatter
from syntax_checker import SyntaxChecker
from bug_detector import BugDetector
from validator import FixValidator


class CodeFixAssistant:
    """Main class for coordinating code fixing operations."""

    def __init__(self, input_data: Dict[str, Any]):
        """
        Initialize with input data.

        Args:
            input_data: Dictionary containing file_path, language, fix_types, etc.
        """
        self.file_path = input_data.get('file_path')
        self.language = input_data.get('language')
        self.fix_types = input_data.get('fix_types', ['format', 'syntax', 'bugs', 'validate'])
        self.auto_apply = input_data.get('auto_apply', False)
        self.severity_threshold = input_data.get('severity_threshold', 'warning')
        self.config = input_data.get('config', {})

        self.original_content = None
        self.fixed_content = None
        self.issues = []
        self.fixes_applied = {}

    def read_file(self) -> str:
        """Read the source file content."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError(f"File not found: {self.file_path}")
        except PermissionError:
            raise ValueError(f"Permission denied: {self.file_path}")

    def write_file(self, content: str) -> None:
        """Write fixed content back to file."""
        if not self.auto_apply:
            return

        try:
            # Create backup
            backup_path = f"{self.file_path}.backup"
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(self.original_content)

            # Write fixed content
            with open(self.file_path, 'w', encoding='utf-8') as f:
                f.write(content)

        except PermissionError:
            raise ValueError(f"Permission denied writing to: {self.file_path}")

    def format_code(self) -> Dict[str, Any]:
        """Run code formatting."""
        if 'format' not in self.fix_types:
            return {'status': 'skipped'}

        formatter = CodeFormatter(self.language, self.config)
        result = formatter.format(self.fixed_content or self.original_content)

        if result['success']:
            self.fixed_content = result['formatted_code']
            self.fixes_applied['format'] = {
                'changes': result['changes_count'],
                'status': 'success'
            }
        else:
            self.fixes_applied['format'] = {
                'status': 'failed',
                'error': result.get('error')
            }

        return self.fixes_applied['format']

    def check_syntax(self) -> Dict[str, Any]:
        """Check and fix syntax/type errors."""
        if 'syntax' not in self.fix_types:
            return {'status': 'skipped'}

        checker = SyntaxChecker(self.language, self.config)
        result = checker.check_and_fix(self.fixed_content or self.original_content)

        syntax_issues = result['issues']
        fixed_code = result.get('fixed_code')

        # Filter by severity threshold
        severity_order = {'info': 0, 'warning': 1, 'error': 2}
        threshold_level = severity_order.get(self.severity_threshold, 1)

        filtered_issues = [
            issue for issue in syntax_issues
            if severity_order.get(issue['severity'], 0) >= threshold_level
        ]

        self.issues.extend(filtered_issues)

        if fixed_code:
            self.fixed_content = fixed_code

        self.fixes_applied['syntax'] = {
            'issues_found': len(filtered_issues),
            'issues_fixed': len([i for i in filtered_issues if i.get('status') == 'fixed']),
            'status': 'success' if result['success'] else 'partial'
        }

        return self.fixes_applied['syntax']

    def detect_bugs(self) -> Dict[str, Any]:
        """Detect and fix bugs."""
        if 'bugs' not in self.fix_types:
            return {'status': 'skipped'}

        detector = BugDetector(self.language, self.config)
        result = detector.detect_and_fix(self.fixed_content or self.original_content)

        bug_issues = result['issues']
        fixed_code = result.get('fixed_code')

        self.issues.extend(bug_issues)

        if fixed_code:
            self.fixed_content = fixed_code

        fixed_count = len([i for i in bug_issues if i.get('status') == 'fixed'])
        unfixable_count = len([i for i in bug_issues if i.get('status') == 'unfixable'])

        self.fixes_applied['bugs'] = {
            'issues_found': len(bug_issues),
            'issues_fixed': fixed_count,
            'unfixable': unfixable_count,
            'status': 'success' if result['success'] else 'partial'
        }

        return self.fixes_applied['bugs']

    def validate_fixes(self) -> Dict[str, Any]:
        """Validate all fixes applied."""
        if 'validate' not in self.fix_types:
            return {'status': 'skipped'}

        validator = FixValidator(self.language, self.config)
        result = validator.validate(
            self.fixed_content or self.original_content,
            self.file_path
        )

        self.fixes_applied['validation'] = {
            'linter_passed': result['linter_passed'],
            'syntax_valid': result['syntax_valid'],
            'status': 'success' if result['success'] else 'failed'
        }

        return self.fixes_applied['validation']

    def generate_diff(self) -> str:
        """Generate diff between original and fixed content."""
        if not self.fixed_content or self.fixed_content == self.original_content:
            return ""

        # Simple diff (in production, use difflib)
        return f"--- original\n+++ fixed\n(Content changed: {len(self.original_content)} -> {len(self.fixed_content)} chars)"

    def generate_summary(self) -> str:
        """Generate human-readable summary."""
        parts = []

        if 'format' in self.fixes_applied and self.fixes_applied['format'].get('status') == 'success':
            changes = self.fixes_applied['format']['changes']
            parts.append(f"Applied {changes} formatting changes")

        if 'syntax' in self.fixes_applied:
            fixed = self.fixes_applied['syntax'].get('issues_fixed', 0)
            found = self.fixes_applied['syntax'].get('issues_found', 0)
            if found > 0:
                parts.append(f"Fixed {fixed}/{found} syntax errors")

        if 'bugs' in self.fixes_applied:
            fixed = self.fixes_applied['bugs'].get('issues_fixed', 0)
            found = self.fixes_applied['bugs'].get('issues_found', 0)
            if found > 0:
                parts.append(f"Fixed {fixed}/{found} bugs")

        if 'validation' in self.fixes_applied:
            status = "passed" if self.fixes_applied['validation']['linter_passed'] else "failed"
            parts.append(f"Validation {status}")

        return ", ".join(parts) if parts else "No changes made"

    def fix(self) -> Dict[str, Any]:
        """
        Main entry point - run all fix steps.

        Returns:
            Dictionary with fix report
        """
        # Validate inputs
        if not self.file_path or not os.path.exists(self.file_path):
            raise ValueError(f"Invalid file path: {self.file_path}")

        if not self.language:
            raise ValueError("Language must be specified")

        # Read original file
        self.original_content = self.read_file()
        self.fixed_content = self.original_content

        # Run fix pipeline
        self.format_code()
        self.check_syntax()
        self.detect_bugs()
        self.validate_fixes()

        # Write fixed file if auto_apply
        if self.auto_apply and self.fixed_content != self.original_content:
            self.write_file(self.fixed_content)

        # Generate report
        report = {
            'file': self.file_path,
            'language': self.language,
            'fixes_applied': self.fixes_applied,
            'issues': self.issues,
            'diff': self.generate_diff(),
            'summary': self.generate_summary(),
            'auto_applied': self.auto_apply and self.fixed_content != self.original_content
        }

        return report


def main():
    """Example usage."""
    input_data = {
        'file_path': 'example.py',
        'language': 'python',
        'fix_types': ['format', 'syntax', 'bugs', 'validate'],
        'auto_apply': False,
        'severity_threshold': 'warning'
    }

    assistant = CodeFixAssistant(input_data)
    report = assistant.fix()

    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
