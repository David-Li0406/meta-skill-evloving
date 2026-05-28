#!/usr/bin/env python3
"""
JUnit XML Log Parser

Parses PHPUnit JUnit XML logs to provide a clear summary of test failures and errors.

Usage:
    python3 qaConfig/scripts/parse-junit-logs.py [path/to/junit.xml]

    If no path provided, defaults to: var/qa/phpunit_logs/phpunit.junit.xml

Examples:
    # Parse default log location
    python3 qaConfig/scripts/parse-junit-logs.py

    # Parse specific log file
    python3 qaConfig/scripts/parse-junit-logs.py var/qa/phpunit_logs/phpunit.junit.xml

Output:
    - Summary of failures and errors
    - Breakdown by error type
    - First few unique error patterns for each type
    - Test names, file locations, and error messages
"""

import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import shutil


def parse_junit_xml(xml_path: str) -> tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Parse JUnit XML file and extract failures, errors, and risky tests.

    Args:
        xml_path: Path to JUnit XML file

    Returns:
        Tuple of (failures_list, errors_list, risky_list)
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()

    failures = []
    errors = []
    risky = []

    for testcase in root.iter('testcase'):
        test_name = testcase.get('name')
        test_class = testcase.get('class')
        test_file = testcase.get('file')
        test_time = float(testcase.get('time', 0))
        test_assertions = int(testcase.get('assertions', 0))

        for failure in testcase.findall('failure'):
            failures.append({
                'test': f"{test_class}::{test_name}",
                'file': test_file,
                'type': failure.get('type'),
                'message': failure.text[:500] if failure.text else ''
            })

        for error in testcase.findall('error'):
            errors.append({
                'test': f"{test_class}::{test_name}",
                'file': test_file,
                'type': error.get('type'),
                'message': error.text[:500] if error.text else ''
            })

        # Check for risky tests (no assertions performed)
        # Don't use time threshold - integration tests can legitimately take time
        has_no_assertions = test_assertions == 0 and not testcase.findall('error') and not testcase.findall('failure')

        if has_no_assertions:
            risky.append({
                'test': f"{test_class}::{test_name}",
                'file': test_file,
                'time': test_time,
                'assertions': test_assertions,
                'reasons': ["No assertions performed"]
            })

    return failures, errors, risky


def print_summary(failures: List[Dict], errors: List[Dict], risky: List[Dict]) -> None:
    """Print summary of test results."""
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Failures: {len(failures)}")
    print(f"Total Errors: {len(errors)}")
    print(f"Total Risky: {len(risky)}")
    print()


def print_error_breakdown(errors: List[Dict]) -> None:
    """Print detailed breakdown of errors by type."""
    if not errors:
        return

    # Group errors by type
    error_types: Dict[str, List[Dict]] = {}
    for error in errors:
        error_type = error['type']
        if error_type not in error_types:
            error_types[error_type] = []
        error_types[error_type].append(error)

    print("ERROR TYPES BREAKDOWN")
    print("=" * 80)

    for error_type, error_list in error_types.items():
        print(f"\n{error_type}: {len(error_list)} occurrences")
        print("-" * 80)

        # Show ALL errors (not just unique messages)
        for error in error_list:
            # Extract key part of error message
            msg_lines = error['message'].split('\n')
            if len(msg_lines) > 1:
                key_msg = msg_lines[1]  # Usually the actual error
            else:
                key_msg = error['message'][:200]

            print(f"  Test: {error['test']}")
            print(f"  File: {error['file']}")
            print(f"  Error: {key_msg}")
            print()


def print_failure_breakdown(failures: List[Dict]) -> None:
    """Print detailed breakdown of failures."""
    if not failures:
        return

    print("\nFAILURES BREAKDOWN")
    print("=" * 80)

    for failure in failures:
        print(f"\nTest: {failure['test']}")
        print(f"File: {failure['file']}")
        print(f"Type: {failure['type']}")
        print(f"Message: {failure['message']}")
        print("-" * 80)


def print_risky_breakdown(risky: List[Dict]) -> None:
    """Print detailed breakdown of risky tests."""
    if not risky:
        return

    print("\nRISKY TESTS BREAKDOWN")
    print("=" * 80)

    for test in risky:
        print(f"\nTest: {test['test']}")
        print(f"File: {test['file']}")
        print(f"Time: {test['time']:.2f}s")
        print(f"Assertions: {test['assertions']}")
        print(f"Reasons:")
        for reason in test['reasons']:
            print(f"  - {reason}")
        print("-" * 80)


def archive_non_timestamped_log(log_dir: Path) -> Optional[Path]:
    """
    Archive the non-timestamped phpunit.junit.xml if it exists and is newer.

    Returns:
        Path to the newly archived file if archived, None otherwise
    """
    non_timestamped = log_dir / 'phpunit.junit.xml'

    if not non_timestamped.exists():
        return None

    # Get the most recent timestamped file
    timestamped_files = sorted(log_dir.glob('phpunit.junit.*.xml'), reverse=True)

    # If no timestamped files exist, or non-timestamped is newer, archive it
    should_archive = True
    if timestamped_files:
        most_recent = timestamped_files[0]
        # Compare modification times
        if non_timestamped.stat().st_mtime <= most_recent.stat().st_mtime:
            should_archive = False

    if should_archive:
        # Create timestamped filename using file's modification time
        mtime = datetime.fromtimestamp(non_timestamped.stat().st_mtime)
        timestamp = mtime.strftime('%Y%m%d-%H%M%S')
        archived_name = f'phpunit.junit.{timestamp}.xml'
        archived_path = log_dir / archived_name

        # Copy the file to timestamped version
        shutil.copy2(non_timestamped, archived_path)
        print(f"Archived non-timestamped log: {archived_name}")
        print()

        return archived_path

    return None


def main():
    """Main entry point."""
    log_dir = Path('var/qa/phpunit_logs')

    # Check if log directory exists
    if not log_dir.exists():
        print(f"Error: PHPUnit log directory not found: {log_dir}", file=sys.stderr)
        print(f"\nNo test runs found. Run tests first with: ./bin/qa -t unit", file=sys.stderr)
        sys.exit(1)

    # Determine XML file path
    if len(sys.argv) > 1:
        provided_path = Path(sys.argv[1])

        # If user explicitly passed the non-timestamped file, archive it first
        if provided_path.name == 'phpunit.junit.xml' and provided_path.exists():
            print(f"Non-timestamped log explicitly requested, archiving first...")
            archived_path = archive_non_timestamped_log(log_dir)
            if archived_path:
                xml_path = str(archived_path)
                print(f"Parsing archived log: {archived_path.name}")
                print()
            else:
                # Already archived, find the most recent
                log_files = sorted(log_dir.glob('phpunit.junit.*.xml'), reverse=True)
                if log_files:
                    xml_path = str(log_files[0])
                    print(f"Using most recent archived log: {log_files[0].name}")
                    print()
                else:
                    print(f"Error: No archived logs found", file=sys.stderr)
                    sys.exit(1)
        else:
            xml_path = str(provided_path)
    else:
        # No specific file provided - check for non-timestamped file first
        archived_path = archive_non_timestamped_log(log_dir)

        if archived_path:
            # Use the newly archived file
            xml_path = str(archived_path)
            print(f"Parsing newly archived log: {archived_path.name}")
            print()
        else:
            # Find most recent timestamped log file
            log_files = sorted(log_dir.glob('phpunit.junit.*.xml'), reverse=True)

            if not log_files:
                print(f"Error: No PHPUnit log files found in {log_dir}", file=sys.stderr)
                print(f"\nNo test runs found. Run tests first with: ./bin/qa -t unit", file=sys.stderr)
                sys.exit(1)

            # Use the most recent (first after reverse sort)
            xml_path = str(log_files[0])
            print(f"Parsing most recent test run: {log_files[0].name}")
            print()

    xml_file = Path(xml_path)

    if not xml_file.exists():
        print(f"Error: JUnit XML file not found: {xml_path}", file=sys.stderr)
        print(f"\nUsage: {sys.argv[0]} [path/to/junit.xml]", file=sys.stderr)
        print(f"Default: Automatically finds most recent timestamped log", file=sys.stderr)
        sys.exit(1)

    try:
        failures, errors, risky = parse_junit_xml(xml_path)

        print_summary(failures, errors, risky)
        print_error_breakdown(errors)
        print_failure_breakdown(failures)
        print_risky_breakdown(risky)

        # Exit with error code if there were failures or errors
        # Risky tests are warnings, not failures
        if failures or errors:
            sys.exit(1)
        else:
            print("\n✓ All tests passed!")
            if risky:
                print(f"  (but {len(risky)} risky tests detected - see above)")
            sys.exit(0)

    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == '__main__':
    main()
