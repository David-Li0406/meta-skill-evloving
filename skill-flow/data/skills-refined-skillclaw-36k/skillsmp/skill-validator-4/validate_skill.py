"""
Main skill validation orchestrator.
Coordinates validation across all components and handles batch processing.
"""

import os
import json
import sys
from typing import Dict, List, Any, Optional
from pathlib import Path
import csv
from datetime import datetime


class SkillValidator:
    """Main orchestrator for skill validation."""

    def __init__(self):
        """Initialize validator with component validators."""
        self.validators = {
            'structure': StructureValidator(),
            'yaml': YamlValidator(),
            'python': PythonValidator(),
            'naming': NamingValidator()
        }
        self.results = {
            'validation_date': datetime.now().isoformat(),
            'skills': {},
            'summary': {
                'total_skills': 0,
                'passed': 0,
                'failed': 0,
                'warnings': 0,
                'critical_errors': 0
            }
        }

    def validate_skill(self, skill_path: str, focus: str = 'all') -> Dict[str, Any]:
        """
        Validate a single skill folder.

        Args:
            skill_path: Path to skill folder
            focus: Validation focus ('all', 'structure', 'yaml', 'python', 'naming')

        Returns:
            Validation results dictionary
        """
        skill_path = Path(skill_path).resolve()
        skill_name = skill_path.name

        if not skill_path.exists():
            return {
                'skill': skill_name,
                'path': str(skill_path),
                'valid': False,
                'errors': [f"Skill path does not exist: {skill_path}"],
                'warnings': [],
                'fix_suggestions': []
            }

        skill_results = {
            'skill': skill_name,
            'path': str(skill_path),
            'valid': True,
            'errors': [],
            'warnings': [],
            'fix_suggestions': [],
            'validation_details': {}
        }

        # Determine which validators to run
        validators_to_run = []
        if focus == 'all':
            validators_to_run = list(self.validators.keys())
        elif focus in self.validators:
            validators_to_run = [focus]
        else:
            skill_results['errors'].append(f"Invalid validation focus: {focus}")
            skill_results['valid'] = False
            return skill_results

        # Run validators
        for validator_name in validators_to_run:
            validator = self.validators[validator_name]
            result = validator.validate(skill_path)

            skill_results['validation_details'][validator_name] = result

            if not result.get('valid', True):
                skill_results['valid'] = False
                skill_results['errors'].extend(result.get('errors', []))

            skill_results['warnings'].extend(result.get('warnings', []))
            skill_results['fix_suggestions'].extend(result.get('fix_suggestions', []))

        return skill_results

    def validate_batch(self, directory_path: str, output_format: str = 'json') -> Dict[str, Any]:
        """
        Validate all skills in a directory.

        Args:
            directory_path: Path to directory containing skill folders
            output_format: Output format ('json', 'csv', 'text', 'markdown')

        Returns:
            Batch validation results
        """
        directory = Path(directory_path).resolve()

        if not directory.exists() or not directory.is_dir():
            return {
                'valid': False,
                'error': f"Directory does not exist or is not a directory: {directory}"
            }

        # Find skill folders
        skill_folders = []
        for item in directory.iterdir():
            if item.is_dir():
                # Check if it looks like a skill folder (has SKILL.md)
                skill_md = item / 'SKILL.md'
                if skill_md.exists():
                    skill_folders.append(item)

        self.results['summary']['total_skills'] = len(skill_folders)

        # Validate each skill
        for skill_folder in skill_folders:
            skill_result = self.validate_skill(skill_folder)
            self.results['skills'][skill_folder.name] = skill_result

            # Update summary
            if skill_result['valid']:
                self.results['summary']['passed'] += 1
            else:
                self.results['summary']['failed'] += 1

            self.results['summary']['warnings'] += len(skill_result['warnings'])
            self.results['summary']['critical_errors'] += len(skill_result['errors'])

        # Generate output in requested format
        output = self._format_output(output_format)

        return {
            'results': self.results,
            'output': output,
            'output_format': output_format
        }

    def _format_output(self, format_type: str) -> str:
        """Format results in requested output format."""
        if format_type == 'json':
            return json.dumps(self.results, indent=2)

        elif format_type == 'csv':
            # Create CSV with skill summary
            output_lines = []
            output_lines.append('skill,valid,errors,warnings,fix_suggestions')

            for skill_name, skill_data in self.results['skills'].items():
                errors_count = len(skill_data['errors'])
                warnings_count = len(skill_data['warnings'])
                fixes_count = len(skill_data['fix_suggestions'])
                valid = 'YES' if skill_data['valid'] else 'NO'

                output_lines.append(
                    f'{skill_name},{valid},{errors_count},{warnings_count},{fixes_count}'
                )

            return '\n'.join(output_lines)

        elif format_type == 'markdown':
            # Create markdown report
            output_lines = []
            output_lines.append('# Skill Validation Report')
            output_lines.append(f'**Date**: {self.results["validation_date"]}')
            output_lines.append(f'**Total Skills**: {self.results["summary"]["total_skills"]}')
            output_lines.append(f'**Passed**: {self.results["summary"]["passed"]}')
            output_lines.append(f'**Failed**: {self.results["summary"]["failed"]}')
            output_lines.append(f'**Warnings**: {self.results["summary"]["warnings"]}')
            output_lines.append(f'**Critical Errors**: {self.results["summary"]["critical_errors"]}')
            output_lines.append('')

            output_lines.append('## Skills Summary')
            output_lines.append('| Skill | Status | Errors | Warnings | Fixes |')
            output_lines.append('|-------|--------|--------|----------|-------|')

            for skill_name, skill_data in self.results['skills'].items():
                status = '✅ PASS' if skill_data['valid'] else '❌ FAIL'
                errors = len(skill_data['errors'])
                warnings = len(skill_data['warnings'])
                fixes = len(skill_data['fix_suggestions'])

                output_lines.append(f'| {skill_name} | {status} | {errors} | {warnings} | {fixes} |')

            return '\n'.join(output_lines)

        else:  # text format
            output_lines = []
            output_lines.append(f'Skill Validation Report - {self.results["validation_date"]}')
            output_lines.append(f'Total Skills: {self.results["summary"]["total_skills"]}')
            output_lines.append(f'Passed: {self.results["summary"]["passed"]}')
            output_lines.append(f'Failed: {self.results["summary"]["failed"]}')
            output_lines.append(f'Warnings: {self.results["summary"]["warnings"]}')
            output_lines.append(f'Critical Errors: {self.results["summary"]["critical_errors"]}')
            output_lines.append('')

            for skill_name, skill_data in self.results['skills'].items():
                status = 'PASS' if skill_data['valid'] else 'FAIL'
                output_lines.append(f'{skill_name}: {status}')

                if skill_data['errors']:
                    output_lines.append('  Errors:')
                    for error in skill_data['errors']:
                        output_lines.append(f'    - {error}')

                if skill_data['warnings']:
                    output_lines.append('  Warnings:')
                    for warning in skill_data['warnings']:
                        output_lines.append(f'    - {warning}')

            return '\n'.join(output_lines)


class StructureValidator:
    """Validates skill file structure and organization."""

    REQUIRED_FILES = ['SKILL.md', 'HOW_TO_USE.md']
    OPTIONAL_FILES = ['*.py', 'sample_*.json', 'expected_*.json', 'config.*']

    def validate(self, skill_path: Path) -> Dict[str, Any]:
        """Validate skill file structure."""
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'fix_suggestions': []
        }

        # Check required files
        for required_file in self.REQUIRED_FILES:
            file_path = skill_path / required_file
            if not file_path.exists():
                results['valid'] = False
                results['errors'].append(f"Missing required file: {required_file}")
                results['fix_suggestions'].append(f"Create {required_file} in skill folder")

        # Check for common file organization issues
        all_files = list(skill_path.iterdir())

        # Check for backup files
        backup_files = [f for f in all_files if any(f.name.endswith(ext) for ext in ['.backup', '.bak', '.old', '~'])]
        if backup_files:
            results['warnings'].append(f"Found backup files: {[f.name for f in backup_files]}")
            results['fix_suggestions'].append(f"Remove backup files: {' '.join([f.name for f in backup_files])}")

        # Check for Python cache
        pycache_dir = skill_path / '__pycache__'
        if pycache_dir.exists():
            results['warnings'].append("Found __pycache__ directory")
            results['fix_suggestions'].append("Remove __pycache__ directory: rm -rf __pycache__")

        return results


class YamlValidator:
    """Validates YAML frontmatter in SKILL.md."""

    def validate(self, skill_path: Path) -> Dict[str, Any]:
        """Validate SKILL.md YAML frontmatter."""
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'fix_suggestions': []
        }

        skill_md = skill_path / 'SKILL.md'
        if not skill_md.exists():
            results['valid'] = False
            results['errors'].append("SKILL.md file not found")
            return results

        try:
            content = skill_md.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Check for YAML frontmatter
            if not content.startswith('---\n'):
                results['valid'] = False
                results['errors'].append("SKILL.md must start with YAML frontmatter (---)")
                results['fix_suggestions'].append("Add '---' as first line of SKILL.md")
                return results

            # Parse YAML frontmatter
            yaml_lines = []
            in_yaml = False
            yaml_end_found = False

            for i, line in enumerate(lines):
                if i == 0 and line == '---':
                    in_yaml = True
                    continue

                if in_yaml and line == '---':
                    in_yaml = False
                    yaml_end_found = True
                    break

                if in_yaml:
                    yaml_lines.append(line)

            if not yaml_end_found:
                results['valid'] = False
                results['errors'].append("YAML frontmatter not properly closed (missing '---')")
                results['fix_suggestions'].append("Add closing '---' after YAML frontmatter")
                return results

            # Parse YAML content
            yaml_content = {}
            for line in yaml_lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    yaml_content[key] = value

            # Check required fields
            if 'name' not in yaml_content:
                results['valid'] = False
                results['errors'].append("Missing required YAML field: 'name'")
                results['fix_suggestions'].append("Add 'name: skill-name-in-kebab-case' to YAML frontmatter")

            if 'description' not in yaml_content:
                results['valid'] = False
                results['errors'].append("Missing required YAML field: 'description'")
                results['fix_suggestions'].append("Add 'description: One-line description' to YAML frontmatter")

            # Validate name field format (kebab-case)
            if 'name' in yaml_content:
                name = yaml_content['name']
                if not self._is_kebab_case(name):
                    results['valid'] = False
                    results['errors'].append(f"Skill name must be kebab-case: '{name}'")
                    suggested_name = self._to_kebab_case(name)
                    results['fix_suggestions'].append(f"Change name to: '{suggested_name}'")

            # Validate description length
            if 'description' in yaml_content:
                desc = yaml_content['description']
                if len(desc) > 100:
                    results['warnings'].append(f"Description is long ({len(desc)} chars), keep under 100 chars")

        except Exception as e:
            results['valid'] = False
            results['errors'].append(f"Error parsing SKILL.md: {str(e)}")

        return results

    def _is_kebab_case(self, text: str) -> bool:
        """Check if text is in kebab-case format."""
        if not text:
            return False

        # Should be lowercase, contain only letters, numbers, and hyphens
        # Hyphens shouldn't be at start or end, and shouldn't be consecutive
        import re
        pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'
        return bool(re.match(pattern, text))

    def _to_kebab_case(self, text: str) -> str:
        """Convert text to kebab-case."""
        import re

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


class PythonValidator:
    """Validates Python file structure and imports."""

    def validate(self, skill_path: Path) -> Dict[str, Any]:
        """Validate Python files in skill."""
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'fix_suggestions': []
        }

        # Find Python files
        python_files = list(skill_path.glob('*.py'))

        if not python_files:
            # No Python files is okay for prompt-only skills
            return results

        for py_file in python_files:
            file_results = self._validate_python_file(py_file)

            if not file_results.get('valid', True):
                results['valid'] = False

            results['errors'].extend(file_results.get('errors', []))
            results['warnings'].extend(file_results.get('warnings', []))
            results['fix_suggestions'].extend(file_results.get('fix_suggestions', []))

        return results

    def _validate_python_file(self, file_path: Path) -> Dict[str, Any]:
        """Validate a single Python file."""
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'fix_suggestions': []
        }

        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Check file naming (should be snake_case)
            file_name = file_path.name
            if not self._is_snake_case(file_name.replace('.py', '')):
                results['valid'] = False
                results['errors'].append(f"Python file name should be snake_case: '{file_name}'")
                suggested_name = self._to_snake_case(file_name.replace('.py', '')) + '.py'
                results['fix_suggestions'].append(f"Rename file to: '{suggested_name}'")

            # Check for module docstring
            if not content.strip().startswith('"""') and not content.strip().startswith("'''"):
                results['warnings'].append(f"Python file '{file_name}' missing module docstring")
                results['fix_suggestions'].append(f"Add docstring to '{file_name}'")

            # Check for safe_divide function if doing calculations
            if any(keyword in content.lower() for keyword in ['divide', '/', 'ratio', 'calculate']):
                if 'def safe_divide' not in content:
                    results['warnings'].append(f"Consider adding safe_divide function to '{file_name}' for division safety")

            # Check for proper imports
            if 'import os' in content or 'import sys' in content:
                # Check if they're used
                pass  # Could add more sophisticated import validation

            # Check for type hints
            type_hint_count = content.count('->') + content.count(': Dict') + content.count(': List') + content.count(': Any')
            if type_hint_count == 0 and len(lines) > 20:
                results['warnings'].append(f"Consider adding type hints to '{file_name}'")

        except Exception as e:
            results['valid'] = False
            results['errors'].append(f"Error reading Python file '{file_path.name}': {str(e)}")

        return results

    def _is_snake_case(self, text: str) -> bool:
        """Check if text is in snake_case format."""
        if not text:
            return False

        import re
        pattern = r'^[a-z0-9]+(_[a-z0-9]+)*$'
        return bool(re.match(pattern, text))

    def _to_snake_case(self, text: str) -> str:
        """Convert text to snake_case."""
        import re

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


class NamingValidator:
    """Validates naming conventions across all files."""

    def validate(self, skill_path: Path) -> Dict[str, Any]:
        """Validate naming conventions in skill."""
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'fix_suggestions': []
        }

        # Check skill folder name (should match YAML name if possible)
        skill_folder_name = skill_path.name

        # Read SKILL.md to get YAML name
        skill_md = skill_path / 'SKILL.md'
        if skill_md.exists():
            try:
                content = skill_md.read_text(encoding='utf-8')
                # Extract YAML name
                import re
                name_match = re.search(r'name:\s*(.+)', content)
                if name_match:
                    yaml_name = name_match.group(1).strip()

                    # Compare folder name with YAML name
                    if skill_folder_name != yaml_name:
                        results['warnings'].append(
                            f"Skill folder name '{skill_folder_name}' doesn't match YAML name '{yaml_name}'"
                        )
                        results['fix_suggestions'].append(
                            f"Consider renaming folder to '{yaml_name}' for consistency"
                        )
            except:
                pass  # Skip if can't read SKILL.md

        # Check all file names
        for file_path in skill_path.iterdir():
            if file_path.is_file():
                file_name = file_path.name

                # Skip hidden files
                if file_name.startswith('.'):
                    continue

                # Check file extension
                if '.' in file_name:
                    ext = file_name.split('.')[-1].lower()
                    base_name = '.'.join(file_name.split('.')[:-1])

                    # Validate based on file type
                    if ext == 'py':
                        if not self._is_snake_case(base_name):
                            results['valid'] = False
                            results['errors'].append(f"Python file should be snake_case: '{file_name}'")
                            suggested_name = self._to_snake_case(base_name) + '.py'
                            results['fix_suggestions'].append(f"Rename to: '{suggested_name}'")

                    elif ext == 'md':
                        if file_name != 'SKILL.md' and file_name != 'HOW_TO_USE.md':
                            # Other .md files should be kebab-case
                            if not self._is_kebab_case(base_name):
                                results['warnings'].append(f"Markdown file should be kebab-case: '{file_name}'")

                    elif ext == 'json':
                        # JSON files often have prefixes like sample_, expected_
                        # Check if base name follows patterns
                        pass

                else:
                    # Files without extensions (unusual for skills)
                    results['warnings'].append(f"File without extension: '{file_name}'")

        return results

    def _is_kebab_case(self, text: str) -> bool:
        """Check if text is in kebab-case format."""
        import re
        pattern = r'^[a-z0-9]+(-[a-z0-9]+)*$'
        return bool(re.match(pattern, text))

    def _is_snake_case(self, text: str) -> bool:
        """Check if text is in snake_case format."""
        import re
        pattern = r'^[a-z0-9]+(_[a-z0-9]+)*$'
        return bool(re.match(pattern, text))

    def _to_snake_case(self, text: str) -> str:
        """Convert text to snake_case."""
        import re

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


def main():
    """Command-line interface for skill validation."""
    import argparse

    parser = argparse.ArgumentParser(description='Validate Claude Skills')
    parser.add_argument('path', help='Path to skill folder or directory')
    parser.add_argument('--focus', choices=['all', 'structure', 'yaml', 'python', 'naming'],
                       default='all', help='Validation focus')
    parser.add_argument('--output', choices=['json', 'csv', 'text', 'markdown'],
                       default='json', help='Output format')
    parser.add_argument('--batch', action='store_true',
                       help='Batch validate directory (instead of single skill)')

    args = parser.parse_args()

    validator = SkillValidator()

    if args.batch:
        result = validator.validate_batch(args.path, args.output)

        if 'error' in result:
            print(f"Error: {result['error']}")
            sys.exit(1)

        print(result['output'])

        # Exit code based on validation results
        if result['results']['summary']['failed'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)

    else:
        result = validator.validate_skill(args.path, args.focus)

        # Output in requested format
        if args.output == 'json':
            print(json.dumps(result, indent=2))
        else:
            # Simple text output for single skill
            status = '✅ VALID' if result['valid'] else '❌ INVALID'
            print(f"Skill: {result['skill']}")
            print(f"Path: {result['path']}")
            print(f"Status: {status}")

            if result['errors']:
                print("\nErrors:")
                for error in result['errors']:
                    print(f"  - {error}")

            if result['warnings']:
                print("\nWarnings:")
                for warning in result['warnings']:
                    print(f"  - {warning}")

            if result['fix_suggestions']:
                print("\nFix Suggestions:")
                for fix in result['fix_suggestions']:
                    print(f"  - {fix}")

        sys.exit(0 if result['valid'] else 1)


if __name__ == '__main__':
    main()