"""
Naming convention validation and auto-fixing.
Validates kebab-case for skill names, snake_case for Python files, and proper naming conventions.
"""

import re
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional


class NamingFixer:
    """Auto-fix naming convention issues."""

    def fix_naming_conventions(self, skill_path: Path, dry_run: bool = False) -> Dict[str, Any]:
        """
        Fix naming convention issues in a skill folder.

        Args:
            skill_path: Path to skill folder
            dry_run: If True, only show what would be fixed

        Returns:
            Dictionary with fix results
        """
        results = {
            'fixed': False,
            'renamed_files': [],
            'errors': [],
            'warnings': []
        }

        try:
            # Get current skill folder name
            current_folder_name = skill_path.name
            parent_path = skill_path.parent

            # Read SKILL.md to get correct YAML name
            skill_md = skill_path / 'SKILL.md'
            yaml_name = None

            if skill_md.exists():
                content = skill_md.read_text(encoding='utf-8')
                name_match = re.search(r'name:\s*(.+)', content)
                if name_match:
                    yaml_name = name_match.group(1).strip()

            # Fix 1: Rename skill folder to match YAML name (if different and YAML name is kebab-case)
            if yaml_name and yaml_name != current_folder_name and self._is_kebab_case(yaml_name):
                new_folder_path = parent_path / yaml_name

                if not dry_run:
                    # Actually rename the folder
                    skill_path.rename(new_folder_path)
                    skill_path = new_folder_path  # Update path for subsequent operations
                    results['renamed_files'].append({
                        'from': current_folder_name,
                        'to': yaml_name,
                        'type': 'folder'
                    })
                else:
                    results['renamed_files'].append({
                        'from': current_folder_name,
                        'to': yaml_name,
                        'type': 'folder',
                        'dry_run': True
                    })

                results['fixed'] = True

            # Fix 2: Rename Python files to snake_case
            python_files = list(skill_path.glob('*.py'))
            for py_file in python_files:
                current_name = py_file.name
                base_name = current_name.replace('.py', '')

                if not self._is_snake_case(base_name):
                    new_base_name = self._to_snake_case(base_name)
                    new_name = f"{new_base_name}.py"
                    new_path = py_file.parent / new_name

                    if not dry_run:
                        # Actually rename the file
                        py_file.rename(new_path)
                        results['renamed_files'].append({
                            'from': current_name,
                            'to': new_name,
                            'type': 'python_file'
                        })
                    else:
                        results['renamed_files'].append({
                            'from': current_name,
                            'to': new_name,
                            'type': 'python_file',
                            'dry_run': True
                        })

                    results['fixed'] = True

            # Fix 3: Rename other .md files to kebab-case (except SKILL.md and HOW_TO_USE.md)
            md_files = list(skill_path.glob('*.md'))
            for md_file in md_files:
                current_name = md_file.name
                if current_name in ['SKILL.md', 'HOW_TO_USE.md']:
                    continue

                base_name = current_name.replace('.md', '')

                if not self._is_kebab_case(base_name):
                    new_base_name = self._to_kebab_case(base_name)
                    new_name = f"{new_base_name}.md"
                    new_path = md_file.parent / new_name

                    if not dry_run:
                        # Actually rename the file
                        md_file.rename(new_path)
                        results['renamed_files'].append({
                            'from': current_name,
                            'to': new_name,
                            'type': 'markdown_file'
                        })
                    else:
                        results['renamed_files'].append({
                            'from': current_name,
                            'to': new_name,
                            'type': 'markdown_file',
                            'dry_run': True
                        })

                    results['fixed'] = True

            # Fix 4: Remove backup files
            backup_patterns = ['*.backup', '*.bak', '*.old', '*~']
            for pattern in backup_patterns:
                for backup_file in skill_path.glob(pattern):
                    if not dry_run:
                        backup_file.unlink()
                        results['renamed_files'].append({
                            'from': backup_file.name,
                            'to': '(deleted)',
                            'type': 'backup_file'
                        })
                    else:
                        results['renamed_files'].append({
                            'from': backup_file.name,
                            'to': '(deleted)',
                            'type': 'backup_file',
                            'dry_run': True
                        })

                    results['fixed'] = True

            # Fix 5: Remove __pycache__ directory
            pycache_dir = skill_path / '__pycache__'
            if pycache_dir.exists():
                if not dry_run:
                    shutil.rmtree(pycache_dir)
                    results['renamed_files'].append({
                        'from': '__pycache__',
                        'to': '(deleted)',
                        'type': 'pycache_dir'
                    })
                else:
                    results['renamed_files'].append({
                        'from': '__pycache__',
                        'to': '(deleted)',
                        'type': 'pycache_dir',
                        'dry_run': True
                    })

                results['fixed'] = True

        except Exception as e:
            results['errors'].append(f"Error fixing naming conventions: {str(e)}")

        return results

    def _is_kebab_case(self, text: str) -> bool:
        """Check if text is in kebab-case format."""
        if not text:
            return False

        pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'
        return bool(re.match(pattern, text))

    def _is_snake_case(self, text: str) -> bool:
        """Check if text is in snake_case format."""
        if not text:
            return False

        pattern = r'^[a-z0-9]+(_[a-z0-9]+)*$'
        return bool(re.match(pattern, text))

    def _to_kebab_case(self, text: str) -> str:
        """Convert text to kebab-case."""
        # Remove special characters, convert to lowercase
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = text.lower()

        # Replace spaces and underscores with hyphens
        text = re.sub(r'[\s_]+', '-', text)

        # Remove consecutive hyphens
        text = re.sub(r'-+', '-', text)

        # Remove hyphens from start and end
        text = text.strip('-')

        return text

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


def fix_naming_command():
    """Command-line interface for naming convention fixing."""
    import argparse

    parser = argparse.ArgumentParser(description='Fix naming convention issues')
    parser.add_argument('skill_path', help='Path to skill folder')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be fixed without making changes')

    args = parser.parse_args()

    skill_path = Path(args.skill_path).resolve()

    if not skill_path.exists():
        print(f"Error: Skill folder not found: {skill_path}")
        return

    fixer = NamingFixer()
    results = fixer.fix_naming_conventions(skill_path, args.dry_run)

    if results['errors']:
        print("Errors occurred:")
        for error in results['errors']:
            print(f"  - {error}")

    if results['renamed_files']:
        if args.dry_run:
            print("Would rename/delete the following:")
        else:
            print("Renamed/deleted the following:")

        for rename in results['renamed_files']:
            action = "Would rename" if rename.get('dry_run') else "Renamed"
            if rename['type'] == 'folder':
                print(f"  {action} folder: {rename['from']} -> {rename['to']}")
            elif rename['type'] == 'python_file':
                print(f"  {action} Python file: {rename['from']} -> {rename['to']}")
            elif rename['type'] == 'markdown_file':
                print(f"  {action} Markdown file: {rename['from']} -> {rename['to']}")
            elif rename['type'] == 'backup_file':
                action = "Would delete" if rename.get('dry_run') else "Deleted"
                print(f"  {action} backup file: {rename['from']}")
            elif rename['type'] == 'pycache_dir':
                action = "Would delete" if rename.get('dry_run') else "Deleted"
                print(f"  {action} __pycache__ directory")

        if args.dry_run:
            print("\nRun without --dry-run to apply these changes.")
    else:
        print("No naming convention issues found!")


if __name__ == '__main__':
    fix_naming_command()