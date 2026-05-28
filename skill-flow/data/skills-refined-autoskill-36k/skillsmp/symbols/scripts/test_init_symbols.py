#!/usr/bin/env python3
"""
Test script for init_symbols.py wizard.

Demonstrates different usage modes and validates functionality.
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def run_test(name: str, command: list[str]) -> tuple[bool, str]:
    """Run a test command and return success status and output."""
    print(f"\n{BOLD}{BLUE}Testing: {name}{RESET}")
    print(f"Command: {' '.join(command)}")
    print("-" * 80)

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10,
        )

        output = result.stdout + result.stderr

        if result.returncode == 0:
            print(f"{GREEN}✓ Test passed{RESET}")
            return True, output
        else:
            print(f"{RED}✗ Test failed (exit code {result.returncode}){RESET}")
            return False, output

    except subprocess.TimeoutExpired:
        print(f"{RED}✗ Test timed out{RESET}")
        return False, "Timeout"
    except Exception as e:
        print(f"{RED}✗ Test error: {e}{RESET}")
        return False, str(e)


def validate_config(config_path: Path) -> tuple[bool, str]:
    """Validate a generated configuration file."""
    if not config_path.exists():
        return False, "Configuration file not found"

    try:
        with open(config_path) as f:
            config = json.load(f)

        # Check required fields
        required = ["projectName", "symbolsDir", "domains", "extraction"]
        missing = [field for field in required if field not in config]
        if missing:
            return False, f"Missing required fields: {missing}"

        # Check domains
        if not config["domains"]:
            return False, "No domains configured"

        # Check extraction
        if "python" not in config["extraction"] or "typescript" not in config["extraction"]:
            return False, "Missing extraction configuration"

        return True, "Configuration valid"

    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    except Exception as e:
        return False, f"Validation error: {e}"


def main():
    """Run all tests."""
    script_dir = Path(__file__).parent
    init_script = script_dir / "init_symbols.py"

    if not init_script.exists():
        print(f"{RED}✗ init_symbols.py not found at {init_script}{RESET}")
        return 1

    print(f"{BOLD}{'=' * 80}{RESET}")
    print(f"{BOLD}{'init_symbols.py Test Suite':^80}{RESET}")
    print(f"{BOLD}{'=' * 80}{RESET}")

    tests_passed = 0
    tests_failed = 0

    # Test 1: Help output
    success, output = run_test(
        "Help output",
        ["python", str(init_script), "--help"]
    )
    if success and "Interactive symbols configuration wizard" in output:
        tests_passed += 1
    else:
        tests_failed += 1

    # Test 2: List templates
    success, output = run_test(
        "List templates",
        ["python", str(init_script), "--list"]
    )
    if success and "react-typescript-fullstack" in output:
        tests_passed += 1
    else:
        tests_failed += 1

    # Test 3: Dry run with Python FastAPI template
    success, output = run_test(
        "Dry run - Python FastAPI",
        [
            "python", str(init_script),
            "--template=python-fastapi",
            "--name=TestProject",
            "--symbols-dir=symbols",
            "--dry-run"
        ]
    )
    if success and "Dry run mode" in output and "TestProject" in output:
        tests_passed += 1
    else:
        tests_failed += 1

    # Test 4: Quick mode with React template
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "symbols.config.json"

        success, output = run_test(
            "Quick mode - React Fullstack",
            [
                "python", str(init_script),
                "--quick",
                "--name=QuickTest",
                "--symbols-dir=ai",
                f"--output={output_path}"
            ]
        )

        if success:
            valid, msg = validate_config(output_path)
            if valid:
                print(f"{GREEN}  Configuration validated: {msg}{RESET}")
                tests_passed += 1
            else:
                print(f"{RED}  Configuration validation failed: {msg}{RESET}")
                tests_failed += 1
        else:
            tests_failed += 1

    # Test 5: Next.js template with force flag
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "symbols.config.json"

        # Create initial file
        output_path.write_text("{}")

        success, output = run_test(
            "Force overwrite - Next.js Monorepo",
            [
                "python", str(init_script),
                "--template=nextjs-monorepo",
                "--name=NextJSTest",
                "--symbols-dir=ai",
                f"--output={output_path}",
                "--force"
            ]
        )

        if success:
            valid, msg = validate_config(output_path)
            if valid:
                # Check it's not empty JSON
                with open(output_path) as f:
                    config = json.load(f)
                    if config.get("projectName") == "NextJSTest":
                        print(f"{GREEN}  Configuration validated and overwritten: {msg}{RESET}")
                        tests_passed += 1
                    else:
                        print(f"{RED}  Configuration not overwritten properly{RESET}")
                        tests_failed += 1
            else:
                print(f"{RED}  Configuration validation failed: {msg}{RESET}")
                tests_failed += 1
        else:
            tests_failed += 1

    # Test 6: Vue TypeScript template
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "symbols.config.json"

        success, output = run_test(
            "Vue TypeScript template",
            [
                "python", str(init_script),
                "--template=vue-typescript",
                "--name=VueTest",
                "--symbols-dir=ai",
                f"--output={output_path}"
            ]
        )

        if success:
            valid, msg = validate_config(output_path)
            if valid:
                print(f"{GREEN}  Configuration validated: {msg}{RESET}")
                tests_passed += 1
            else:
                print(f"{RED}  Configuration validation failed: {msg}{RESET}")
                tests_failed += 1
        else:
            tests_failed += 1

    # Test 7: Django template
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "symbols.config.json"

        success, output = run_test(
            "Django template",
            [
                "python", str(init_script),
                "--template=python-django",
                "--name=DjangoTest",
                "--symbols-dir=ai",
                f"--output={output_path}"
            ]
        )

        if success:
            valid, msg = validate_config(output_path)
            if valid:
                print(f"{GREEN}  Configuration validated: {msg}{RESET}")
                tests_passed += 1
            else:
                print(f"{RED}  Configuration validation failed: {msg}{RESET}")
                tests_failed += 1
        else:
            tests_failed += 1

    # Summary
    print(f"\n{BOLD}{'=' * 80}{RESET}")
    print(f"{BOLD}Test Summary{RESET}")
    print(f"{BOLD}{'=' * 80}{RESET}")
    print(f"Total tests: {tests_passed + tests_failed}")
    print(f"{GREEN}Passed: {tests_passed}{RESET}")
    print(f"{RED}Failed: {tests_failed}{RESET}")

    if tests_failed == 0:
        print(f"\n{GREEN}{BOLD}✓ All tests passed!{RESET}")
        return 0
    else:
        print(f"\n{RED}{BOLD}✗ Some tests failed{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
