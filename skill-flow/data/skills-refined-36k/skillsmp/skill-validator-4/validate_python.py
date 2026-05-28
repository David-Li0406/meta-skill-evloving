"""
Python code validation and auto-fixing.
Validates Python file structure, imports, and best practices.
"""

import re
import ast
from pathlib import Path
from typing import Dict, List, Any, Optional


class PythonFixer:
    """Auto-fix common Python code issues."""

    def fix_python_file(self, file_path: Path) -> Dict[str, Any]:
        """
        Auto-fix common Python code issues.

        Args:
            file_path: Path to Python file

        Returns:
            Dictionary with fix results
        """
        results = {
            'fixed': False,
            'changes': [],
            'errors': [],
            'backup_created': False
        }

        try:
            content = file_path.read_text(encoding='utf-8')
            original_content = content

            # Create backup
            backup_path = file_path.with_suffix('.py.backup')
            backup_path.write_text(content, encoding='utf-8')
            results['backup_created'] = True

            # Fix 1: Add module docstring if missing
            if not self._has_module_docstring(content):
                # Parse to find where to insert docstring
                lines = content.split('\n')

                # Skip shebang if present
                insert_line = 0
                if lines and lines[0].startswith('#!'):
                    insert_line = 1

                # Add docstring
                module_name = file_path.stem
                docstring = f'"""\n{module_name} module.\n"""'
                lines.insert(insert_line, docstring)
                content = '\n'.join(lines)
                results['changes'].append("Added missing module docstring")
                results['fixed'] = True

            # Fix 2: Add safe_divide function if doing calculations
            if self._needs_safe_divide(content) and 'def safe_divide' not in content:
                # Find a good place to insert safe_divide (after imports, before first function)
                lines = content.split('\n')
                insert_line = self._find_safe_divide_insertion_point(lines)

                safe_divide_func = [
                    '',
                    'def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:',
                    '    """Safely divide two numbers, returning default if denominator is zero."""',
                    '    if denominator == 0:',
                    '        return default',
                    '    return numerator / denominator',
                    ''
                ]

                # Insert the function
                for i, line in enumerate(safe_divide_func):
                    lines.insert(insert_line + i, line)

                content = '\n'.join(lines)
                results['changes'].append("Added safe_divide function for division safety")
                results['fixed'] = True

            # Fix 3: Fix file naming if needed (would require file rename, not content change)
            # This is handled separately

            # Write fixed content if changes were made
            if results['fixed']:
                file_path.write_text(content, encoding='utf-8')

        except Exception as e:
            results['errors'].append(f"Error fixing Python file: {str(e)}")

        return results

    def _has_module_docstring(self, content: str) -> bool:
        """Check if Python file has a module docstring."""
        try:
            tree = ast.parse(content)
            if tree.body and isinstance(tree.body[0], ast.Expr):
                if isinstance(tree.body[0].value, ast.Constant):
                    return isinstance(tree.body[0].value.value, str)
        except:
            pass

        # Fallback: check for triple quotes at start
        stripped = content.strip()
        return stripped.startswith('"""') or stripped.startswith("'''")

    def _needs_safe_divide(self, content: str) -> bool:
        """Check if file does calculations that could benefit from safe_divide."""
        content_lower = content.lower()
        calculation_keywords = ['divide', '/', 'ratio', 'calculate', 'math', 'numerator', 'denominator']

        return any(keyword in content_lower for keyword in calculation_keywords)

    def _find_safe_divide_insertion_point(self, lines: List[str]) -> int:
        """Find where to insert safe_divide function."""
        # Start after imports and module docstring
        insert_line = 0

        # Skip shebang
        if lines and lines[0].startswith('#!'):
            insert_line = 1

        # Skip module docstring
        while insert_line < len(lines) and (lines[insert_line].strip().startswith('"""') or
                                           lines[insert_line].strip().startswith("'''")):
            insert_line += 1
            # Skip until end of docstring
            while insert_line < len(lines) and not (lines[insert_line].strip().endswith('"""') or
                                                   lines[insert_line].strip().endswith("'''")):
                insert_line += 1
            if insert_line < len(lines):
                insert_line += 1

        # Skip imports
        while insert_line < len(lines) and (lines[insert_line].strip().startswith('import ') or
                                           lines[insert_line].strip().startswith('from ')):
            insert_line += 1

        # Skip blank lines
        while insert_line < len(lines) and not lines[insert_line].strip():
            insert_line += 1

        return insert_line

    def _is_snake_case(self, text: str) -> bool:
        """Check if text is in snake_case format."""
        if not text:
            return False

        pattern = r'^[a-z0-9]+(_[a-z0-9]+)*$'
        return bool(re.match(pattern, text))

    def _to_snake_case(self, text: str) -> str:
        """Convert text to snake_case."""
        # Remove special characters, convert to lowercase
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = text.lower()

        # Replace spaces and hyphens with underscores
        text = re.sub(r'[\s-]+', '_', text)

        # Remove consecutive underscores
        text = re.sub(r'_+', '_', text)

        # Remove underscores from start and end
        text = text.strip('_')

        return text


def fix_python_command():
    """Command-line interface for Python fixing."""
    import argparse

    parser = argparse.ArgumentParser(description='Fix Python code issues')
    parser.add_argument('file', help='Path to Python file')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be fixed without making changes')

    args = parser.parse_args()

    file_path = Path(args.file).resolve()

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return

    fixer = PythonFixer()

    if args.dry_run:
        # Analyze without fixing
        content = file_path.read_text(encoding='utf-8')
        print(f"Python file analysis: {file_path.name}")
        print("-" * 50)

        issues = []

        # Check module docstring
        if not fixer._has_module_docstring(content):
            issues.append("Missing module docstring")

        # Check for safe_divide need
        if fixer._needs_safe_divide(content) and 'def safe_divide' not in content:
            issues.append("Consider adding safe_divide function for division safety")

        # Check file naming
        file_name = file_path.name
        if not fixer._is_snake_case(file_name.replace('.py', '')):
            issues.append(f"File name should be snake_case: '{file_name}'")

        if issues:
            print("Issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("No issues found!")

    else:
        # Actually fix the file
        results = fixer.fix_python_file(file_path)

        if results['errors']:
            print("Errors occurred:")
            for error in results['errors']:
                print(f"  - {error}")

        if results['fixed']:
            print("Fixed the following issues:")
            for change in results['changes']:
                print(f"  - {change}")

            if results['backup_created']:
                print(f"\nBackup created at: {file_path.with_suffix('.py.backup')}")
        else:
            print("No fixes needed!")


if __name__ == '__main__':
    fix_python_command()