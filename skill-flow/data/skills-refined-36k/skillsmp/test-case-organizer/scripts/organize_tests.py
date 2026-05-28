#!/usr/bin/env python3
"""
Test Case Organizer Script

Automates the process of finding scattered test cases in business code
and organizing them into proper test directories following standard conventions.

Usage:
    python organize_tests.py --auto              # Full automated organization
    python organize_tests.py --interactive       # Interactive mode with confirmations
    python organize_tests.py --dry-run           # Preview changes without executing
    python organize_tests.py --scan              # Only scan and report
    python organize_tests.py --classify          # Scan and classify without moving
"""

import os
import re
import sys
import json
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict


@dataclass
class TestCase:
    """Represents a discovered test case"""
    source_file: str
    function_name: str
    line_start: int
    line_end: int
    test_type: str  # unit, integration, e2e
    category: str   # business domain/module
    code_snippet: str


@dataclass
class OrganizationResult:
    """Results of test organization"""
    tests_found: int
    tests_moved: int
    test_files_created: int
    tests_passed: int
    tests_failed: int
    warnings: List[str]
    file_mappings: Dict[str, str]


class TestOrganizer:
    """Main test organization orchestrator"""

    # Common test directory patterns
    TEST_DIR_PATTERNS = ['tests', 'test', '__tests__', 'spec', 'specs']

    # Test function patterns for different languages
    TEST_PATTERNS = {
        'python': [
            r'def\s+(test_\w+)',
            r'def\s+(\w+_test)',
            r'@pytest\.mark\.\w+\s+def\s+(\w+)',
        ],
        'javascript': [
            r'(test|it)\s*\(\s*[\'"](.+?)[\'"]',
            r'describe\s*\(\s*[\'"](.+?)[\'"]',
        ],
        'java': [
            r'@Test\s+public\s+void\s+(\w+)',
        ],
        'go': [
            r'func\s+(Test\w+)',
        ],
    }

    # Assertion patterns
    ASSERTION_PATTERNS = [
        r'\bassert\s*\(',
        r'\bexpect\s*\(',
        r'\bshould\.',
        r'\.to(Equal|Be|Have)',
        r'assertEquals',
        r'assertThat',
    ]

    def __init__(self, root_dir: str = '.', test_dir: Optional[str] = None):
        self.root_dir = Path(root_dir).resolve()
        self.test_dir = Path(test_dir) if test_dir else None
        self.test_cases: List[TestCase] = []
        self.warnings: List[str] = []

    def scan_for_test_directory(self) -> Optional[Path]:
        """Scan for existing test directory"""
        print("🔍 Scanning for test directory...")

        if self.test_dir and self.test_dir.exists():
            print(f"✓ Using specified test directory: {self.test_dir}")
            return self.test_dir

        # Search for common test directory patterns
        for pattern in self.TEST_DIR_PATTERNS:
            test_path = self.root_dir / pattern
            if test_path.exists() and test_path.is_dir():
                print(f"✓ Found test directory: {test_path}")
                self.test_dir = test_path
                return test_path

        print("⚠ No test directory found")
        return None

    def detect_language(self, file_path: Path) -> Optional[str]:
        """Detect programming language from file extension"""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'javascript',
            '.tsx': 'javascript',
            '.java': 'java',
            '.go': 'go',
            '.rb': 'ruby',
        }
        return ext_map.get(file_path.suffix.lower())

    def is_test_file(self, file_path: Path) -> bool:
        """Check if file is already in test directory or named as test file"""
        file_str = str(file_path)

        # Check if in test directory
        for pattern in self.TEST_DIR_PATTERNS:
            if f'/{pattern}/' in file_str or f'\\{pattern}\\' in file_str:
                return True

        # Check test file naming
        name = file_path.stem.lower()
        if name.startswith('test_') or name.endswith('_test') or name.endswith('.test'):
            return True

        return False

    def find_scattered_tests(self) -> List[TestCase]:
        """Scan codebase for scattered test cases in business code"""
        print("\n🔍 Scanning for scattered test cases...")

        source_files = []
        exclude_dirs = {'.git', 'node_modules', 'venv', '__pycache__', 'dist', 'build'}

        # Collect source files
        for root, dirs, files in os.walk(self.root_dir):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                file_path = Path(root) / file

                # Skip if already in test directory
                if self.is_test_file(file_path):
                    continue

                lang = self.detect_language(file_path)
                if lang:
                    source_files.append((file_path, lang))

        print(f"Found {len(source_files)} source files to scan")

        # Scan each file for test patterns
        for file_path, lang in source_files:
            self._scan_file_for_tests(file_path, lang)

        print(f"✓ Found {len(self.test_cases)} scattered test cases")
        return self.test_cases

    def _scan_file_for_tests(self, file_path: Path, lang: str):
        """Scan a single file for test patterns"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Check for test patterns
            patterns = self.TEST_PATTERNS.get(lang, [])
            for pattern in patterns:
                for match in re.finditer(pattern, content, re.MULTILINE):
                    # Extract test function
                    line_num = content[:match.start()].count('\n') + 1
                    func_name = match.group(1) if match.groups() else 'unknown'

                    # Find function end (simplified - look for next function or end of file)
                    end_line = self._find_function_end(lines, line_num - 1)

                    code_snippet = '\n'.join(lines[line_num - 1:end_line])

                    # Check if has assertions
                    has_assertions = any(
                        re.search(pattern, code_snippet)
                        for pattern in self.ASSERTION_PATTERNS
                    )

                    if has_assertions or 'test' in func_name.lower():
                        test_case = TestCase(
                            source_file=str(file_path.relative_to(self.root_dir)),
                            function_name=func_name,
                            line_start=line_num,
                            line_end=end_line,
                            test_type=self._classify_test_type(func_name, code_snippet),
                            category=self._categorize_test(file_path),
                            code_snippet=code_snippet
                        )
                        self.test_cases.append(test_case)

        except Exception as e:
            self.warnings.append(f"Error scanning {file_path}: {str(e)}")

    def _find_function_end(self, lines: List[str], start_idx: int) -> int:
        """Find end of function (simplified heuristic)"""
        indent_level = len(lines[start_idx]) - len(lines[start_idx].lstrip())

        for i in range(start_idx + 1, len(lines)):
            line = lines[i]
            if line.strip() and not line.strip().startswith('#'):
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= indent_level and line.strip():
                    return i

        return len(lines)

    def _classify_test_type(self, func_name: str, code: str) -> str:
        """Classify test as unit, integration, or e2e"""
        func_lower = func_name.lower()
        code_lower = code.lower()

        if 'e2e' in func_lower or 'end_to_end' in func_lower:
            return 'e2e'
        elif 'integration' in func_lower or 'api' in code_lower:
            return 'integration'
        else:
            return 'unit'

    def _categorize_test(self, file_path: Path) -> str:
        """Determine test category based on source file location"""
        parts = file_path.relative_to(self.root_dir).parts

        # Use first non-src directory as category
        for part in parts[:-1]:
            if part not in ['src', 'lib', 'app']:
                return part

        return file_path.parent.name

    def create_test_file_structure(self) -> Dict[str, List[TestCase]]:
        """Group test cases and plan test file structure"""
        print("\n📁 Planning test file structure...")

        test_groups = defaultdict(list)

        for test in self.test_cases:
            # Group by category and test type
            group_key = f"{test.category}/{test.test_type}"
            test_groups[group_key].append(test)

        print(f"✓ Organized into {len(test_groups)} test file groups")
        return dict(test_groups)

    def generate_test_files(self, test_groups: Dict[str, List[TestCase]],
                           dry_run: bool = False) -> Dict[str, str]:
        """Generate organized test files"""
        print("\n📝 Generating test files...")

        if not self.test_dir:
            print("❌ No test directory specified")
            return {}

        file_mappings = {}

        for group_key, tests in test_groups.items():
            category, test_type = group_key.split('/')

            # Create test subdirectory
            test_subdir = self.test_dir / test_type / category

            if not dry_run:
                test_subdir.mkdir(parents=True, exist_ok=True)

            # Determine test file name
            test_file = test_subdir / f"test_{category}.py"

            # Generate test file content
            content = self._generate_test_file_content(tests, category)

            if not dry_run:
                with open(test_file, 'w', encoding='utf-8') as f:
                    f.write(content)

            # Track mappings
            for test in tests:
                file_mappings[f"{test.source_file}:{test.line_start}"] = str(test_file)

            print(f"  ✓ Created {test_file} ({len(tests)} tests)")

        return file_mappings

    def _generate_test_file_content(self, tests: List[TestCase], category: str) -> str:
        """Generate content for a test file"""
        lines = [
            '"""',
            f'Test suite for {category}',
            f'Auto-generated by test-case-organizer',
            '"""',
            '',
            '# TODO: Add necessary imports',
            '',
        ]

        for test in tests:
            lines.append('')
            lines.append(test.code_snippet)
            lines.append('')

        return '\n'.join(lines)

    def execute_tests(self) -> Tuple[int, int]:
        """Execute test suite to validate organization"""
        print("\n🧪 Executing test suite...")

        if not self.test_dir or not self.test_dir.exists():
            print("⚠ No test directory to execute")
            return 0, 0

        # Try common test runners
        runners = [
            (['pytest', str(self.test_dir), '-v'], 'pytest'),
            (['python', '-m', 'unittest', 'discover', str(self.test_dir)], 'unittest'),
            (['npm', 'test'], 'npm'),
        ]

        for cmd, runner_name in runners:
            try:
                print(f"  Trying {runner_name}...")
                result = subprocess.run(
                    cmd,
                    cwd=self.root_dir,
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if result.returncode == 0:
                    print(f"✓ Tests passed using {runner_name}")
                    # Parse output for pass/fail counts (simplified)
                    return self._parse_test_results(result.stdout)
                else:
                    print(f"⚠ Tests failed using {runner_name}")
                    self.warnings.append(f"Test execution failed: {result.stderr[:200]}")
                    return 0, len(self.test_cases)

            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue

        print("⚠ No compatible test runner found")
        return 0, 0

    def _parse_test_results(self, output: str) -> Tuple[int, int]:
        """Parse test runner output for pass/fail counts"""
        # Simplified parsing - adapt for specific test runners
        passed = len(re.findall(r'PASSED|✓|passed', output, re.IGNORECASE))
        failed = len(re.findall(r'FAILED|✗|failed', output, re.IGNORECASE))
        return passed, failed

    def generate_report(self, result: OrganizationResult, output_file: str = 'organization_report.md'):
        """Generate organization summary report"""
        print(f"\n📄 Generating report: {output_file}")

        report_lines = [
            '# Test Case Organization Report',
            '',
            f'**Date**: {self._current_datetime()}',
            '',
            '## Summary',
            '',
            f'- **Tests Found**: {result.tests_found}',
            f'- **Tests Moved**: {result.tests_moved}',
            f'- **Test Files Created**: {result.test_files_created}',
            f'- **Tests Passed**: {result.tests_passed}',
            f'- **Tests Failed**: {result.tests_failed}',
            '',
            '## File Mappings',
            '',
        ]

        for source, dest in result.file_mappings.items():
            report_lines.append(f'- `{source}` → `{dest}`')

        if result.warnings:
            report_lines.extend([
                '',
                '## Warnings',
                '',
            ])
            for warning in result.warnings:
                report_lines.append(f'- {warning}')

        report_lines.extend([
            '',
            '## Next Steps',
            '',
            '1. Review generated test files for import statements',
            '2. Fix any failing tests',
            '3. Update CI/CD configuration if needed',
            '4. Commit organized test structure',
        ])

        report_content = '\n'.join(report_lines)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"✓ Report saved to {output_file}")

    @staticmethod
    def _current_datetime() -> str:
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def main():
    parser = argparse.ArgumentParser(description='Organize scattered test cases')
    parser.add_argument('--auto', action='store_true', help='Full automated organization')
    parser.add_argument('--interactive', action='store_true', help='Interactive mode')
    parser.add_argument('--dry-run', action='store_true', help='Preview without executing')
    parser.add_argument('--scan', action='store_true', help='Only scan and report')
    parser.add_argument('--classify', action='store_true', help='Scan and classify')
    parser.add_argument('--execute', action='store_true', help='Run tests after organization')
    parser.add_argument('--test-dir', type=str, help='Test directory path')
    parser.add_argument('--root-dir', type=str, default='.', help='Project root directory')

    args = parser.parse_args()

    organizer = TestOrganizer(root_dir=args.root_dir, test_dir=args.test_dir)

    # Step 1: Find test directory
    test_dir = organizer.scan_for_test_directory()

    if not test_dir:
        print("\n❌ No test directory found!")
        print("Please create a test directory (e.g., 'tests/') and run again.")
        print("Suggested structure:")
        print("  tests/")
        print("    ├── unit/")
        print("    ├── integration/")
        print("    └── e2e/")
        sys.exit(1)

    # Step 2: Find scattered tests
    organizer.find_scattered_tests()

    if not organizer.test_cases:
        print("\n✓ No scattered test cases found - project is well organized!")
        sys.exit(0)

    if args.scan:
        print(f"\n📊 Summary: Found {len(organizer.test_cases)} scattered test cases")
        for test in organizer.test_cases[:10]:  # Show first 10
            print(f"  - {test.source_file}:{test.line_start} - {test.function_name}")
        if len(organizer.test_cases) > 10:
            print(f"  ... and {len(organizer.test_cases) - 10} more")
        sys.exit(0)

    # Step 3: Classify and organize
    test_groups = organizer.create_test_file_structure()

    if args.classify:
        print("\n📊 Classification:")
        for group, tests in test_groups.items():
            print(f"  {group}: {len(tests)} tests")
        sys.exit(0)

    # Step 4: Generate test files
    dry_run = args.dry_run or args.interactive
    file_mappings = organizer.generate_test_files(test_groups, dry_run=dry_run)

    if args.interactive:
        response = input("\n❓ Proceed with moving test cases? (yes/no): ")
        if response.lower() != 'yes':
            print("Operation cancelled")
            sys.exit(0)

        # Execute for real
        file_mappings = organizer.generate_test_files(test_groups, dry_run=False)

    # Step 5: Execute tests
    passed, failed = 0, 0
    if args.execute or args.auto:
        passed, failed = organizer.execute_tests()

    # Step 6: Generate report
    result = OrganizationResult(
        tests_found=len(organizer.test_cases),
        tests_moved=len(file_mappings),
        test_files_created=len(test_groups),
        tests_passed=passed,
        tests_failed=failed,
        warnings=organizer.warnings,
        file_mappings=file_mappings
    )

    organizer.generate_report(result)

    print("\n✅ Test organization complete!")
    print(f"   Moved {result.tests_moved} tests into {result.test_files_created} test files")

    if failed > 0:
        print(f"\n⚠ {failed} tests failed - please review and fix")
        sys.exit(1)


if __name__ == '__main__':
    main()
