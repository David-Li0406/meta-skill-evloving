"""
YAML frontmatter validation and auto-fixing.
Specialized validation for SKILL.md YAML frontmatter.
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional


class YamlFixer:
    """Auto-fix common YAML frontmatter issues."""

    def fix_yaml_frontmatter(self, file_path: Path) -> Dict[str, Any]:
        """
        Auto-fix YAML frontmatter issues in SKILL.md.

        Args:
            file_path: Path to SKILL.md file

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
            backup_path = file_path.with_suffix('.md.backup')
            backup_path.write_text(content, encoding='utf-8')
            results['backup_created'] = True

            # Fix 1: Ensure file starts with ---
            if not content.startswith('---\n'):
                content = '---\n' + content
                results['changes'].append("Added missing YAML opening '---'")
                results['fixed'] = True

            # Fix 2: Ensure proper YAML closure
            lines = content.split('\n')
            yaml_open_found = False
            yaml_close_found = False
            yaml_end_line = -1

            for i, line in enumerate(lines):
                if i == 0 and line == '---':
                    yaml_open_found = True
                elif line == '---' and i > 0:
                    yaml_close_found = True
                    yaml_end_line = i
                    break

            if yaml_open_found and not yaml_close_found:
                # Add closing --- after first non-empty line that's not a YAML key
                insert_line = 1
                while insert_line < len(lines) and lines[insert_line].strip() and ':' in lines[insert_line]:
                    insert_line += 1

                lines.insert(insert_line, '---')
                content = '\n'.join(lines)
                results['changes'].append("Added missing YAML closing '---'")
                results['fixed'] = True

            # Fix 3: Ensure name field exists and is kebab-case
            name_match = re.search(r'name:\s*(.+)', content)
            if not name_match:
                # Add name field after opening ---
                lines = content.split('\n')
                if len(lines) > 1:
                    lines.insert(1, 'name: skill-name')
                    content = '\n'.join(lines)
                    results['changes'].append("Added missing 'name' field")
                    results['fixed'] = True
            else:
                # Check and fix name format
                name_line = name_match.group(0)
                name_value = name_match.group(1).strip()

                if not self._is_kebab_case(name_value):
                    fixed_name = self._to_kebab_case(name_value)
                    content = content.replace(name_line, f'name: {fixed_name}')
                    results['changes'].append(f"Fixed name format: '{name_value}' -> '{fixed_name}'")
                    results['fixed'] = True

            # Fix 4: Ensure description field exists
            desc_match = re.search(r'description:\s*(.+)', content)
            if not desc_match:
                # Add description field
                lines = content.split('\n')

                # Find where to insert (after name if exists, otherwise after opening ---)
                insert_line = 1
                for i, line in enumerate(lines):
                    if line.startswith('name:'):
                        insert_line = i + 1
                        break

                lines.insert(insert_line, 'description: One-line description of skill')
                content = '\n'.join(lines)
                results['changes'].append("Added missing 'description' field")
                results['fixed'] = True

            # Write fixed content if changes were made
            if results['fixed']:
                file_path.write_text(content, encoding='utf-8')

        except Exception as e:
            results['errors'].append(f"Error fixing YAML: {str(e)}")

        return results

    def _is_kebab_case(self, text: str) -> bool:
        """Check if text is in kebab-case format."""
        if not text:
            return False

        pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'
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


def fix_yaml_command():
    """Command-line interface for YAML fixing."""
    import argparse

    parser = argparse.ArgumentParser(description='Fix YAML frontmatter in SKILL.md')
    parser.add_argument('file', help='Path to SKILL.md file')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be fixed without making changes')

    args = parser.parse_args()

    file_path = Path(args.file).resolve()

    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        return

    fixer = YamlFixer()

    if args.dry_run:
        # Analyze without fixing
        content = file_path.read_text(encoding='utf-8')
        print("Current YAML frontmatter analysis:")
        print("-" * 50)
        print(content[:500])  # Show first 500 chars
        print("-" * 50)

        # Check for issues
        issues = []

        if not content.startswith('---\n'):
            issues.append("Missing opening '---'")

        lines = content.split('\n')
        yaml_close_found = False
        for i, line in enumerate(lines):
            if i > 0 and line == '---':
                yaml_close_found = True
                break

        if not yaml_close_found:
            issues.append("Missing closing '---'")

        if 'name:' not in content:
            issues.append("Missing 'name:' field")
        else:
            name_match = re.search(r'name:\s*(.+)', content)
            if name_match:
                name = name_match.group(1).strip()
                if not fixer._is_kebab_case(name):
                    issues.append(f"Name not kebab-case: '{name}'")

        if 'description:' not in content:
            issues.append("Missing 'description:' field")

        if issues:
            print("Issues found:")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("No issues found!")

    else:
        # Actually fix the file
        results = fixer.fix_yaml_frontmatter(file_path)

        if results['errors']:
            print("Errors occurred:")
            for error in results['errors']:
                print(f"  - {error}")

        if results['fixed']:
            print("Fixed the following issues:")
            for change in results['changes']:
                print(f"  - {change}")

            if results['backup_created']:
                print(f"\nBackup created at: {file_path.with_suffix('.md.backup')}")
        else:
            print("No fixes needed!")


if __name__ == '__main__':
    fix_yaml_command()