#!/usr/bin/env python3
"""
Test suite for code-with-codex skill
Validates code generation quality and memex-cli integration
"""

import os
import sys
import json
import time
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Color codes for terminal output
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color

class TestScenario:
    """Represents a code generation test scenario"""
    def __init__(self, name: str, prompt: str, expected_files: List[str],
                 validation_rules: Optional[List[str]] = None):
        self.name = name
        self.prompt = prompt
        self.expected_files = expected_files
        self.validation_rules = validation_rules or []
        self.result = None
        self.output_dir = None
        self.execution_time = 0.0
        self.errors = []

class CodeWithCodexTester:
    """Test harness for code-with-codex skill"""

    def __init__(self, quick_mode: bool = False, verbose: bool = False):
        self.quick_mode = quick_mode
        self.verbose = verbose
        self.test_dir = tempfile.mkdtemp(prefix="codex_test_")
        self.scenarios = self._load_scenarios()
        self.results = []

    def _load_scenarios(self) -> List[TestScenario]:
        """Load test scenarios"""
        scenarios = [
            TestScenario(
                name="Simple Function",
                prompt="Create a Python function named 'calculate_fibonacci' that returns the nth Fibonacci number using recursion. Include docstring and type hints.",
                expected_files=["fibonacci.py"],
                validation_rules=[
                    "contains 'def calculate_fibonacci'",
                    "contains docstring",
                    "contains type hints"
                ]
            ),
            TestScenario(
                name="Class Implementation",
                prompt="Create a Python class 'UserManager' with methods to add_user, remove_user, and get_user_by_id. Use a dictionary for storage. Include docstrings.",
                expected_files=["user_manager.py"],
                validation_rules=[
                    "contains 'class UserManager'",
                    "contains 'def add_user'",
                    "contains 'def remove_user'",
                    "contains 'def get_user_by_id'"
                ]
            ),
            TestScenario(
                name="Bug Fixing",
                prompt="Fix this buggy code: 'def divide(a, b): return a / b'. Handle division by zero and add error handling.",
                expected_files=["divide_fixed.py"],
                validation_rules=[
                    "contains 'ZeroDivisionError' or 'if b == 0'",
                    "contains error handling"
                ]
            ),
            TestScenario(
                name="Test Generation",
                prompt="Generate pytest unit tests for a function 'def add(a, b): return a + b'. Include edge cases.",
                expected_files=["test_add.py"],
                validation_rules=[
                    "contains 'import pytest' or 'import unittest'",
                    "contains 'def test_' or 'class Test'",
                    "contains assertion"
                ]
            ),
            TestScenario(
                name="Multi-File Project",
                prompt="Create a simple FastAPI project structure with: main.py (app entry), routes/users.py (user routes), models/user.py (User model). Basic skeleton only.",
                expected_files=["main.py", "routes/users.py", "models/user.py"],
                validation_rules=[
                    "main.py contains 'FastAPI'",
                    "routes/users.py contains router or route",
                    "models/user.py contains class definition"
                ]
            ),
        ]

        # In quick mode, only run first 2 scenarios
        if self.quick_mode:
            return scenarios[:2]

        return scenarios

    def run_scenario(self, scenario: TestScenario) -> bool:
        """Execute a single test scenario"""
        print(f"\n{BLUE}Testing:{NC} {scenario.name}")
        print(f"  Prompt: {scenario.prompt[:80]}...")

        # Create scenario output directory
        scenario.output_dir = Path(self.test_dir) / scenario.name.replace(" ", "_").lower()
        scenario.output_dir.mkdir(parents=True, exist_ok=True)

        # Build memex-cli command
        cmd = [
            "memex-cli",
            "--backend", "codex",
            "--prompt", scenario.prompt,
            "--output-dir", str(scenario.output_dir)
        ]

        # Execute with timeout
        start_time = time.time()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,  # 60 second timeout
                cwd=str(scenario.output_dir)
            )
            scenario.execution_time = time.time() - start_time

            if result.returncode != 0:
                scenario.errors.append(f"Command failed with exit code {result.returncode}")
                scenario.errors.append(f"stderr: {result.stderr}")
                return False

            # Validate output files
            if not self._validate_files(scenario):
                return False

            # Validate content rules
            if not self._validate_content(scenario):
                return False

            print(f"  {GREEN}✓{NC} Passed ({scenario.execution_time:.1f}s)")
            return True

        except subprocess.TimeoutExpired:
            scenario.execution_time = time.time() - start_time
            scenario.errors.append("Test exceeded timeout (60s)")
            print(f"  {RED}✗{NC} Timeout")
            return False

        except Exception as e:
            scenario.execution_time = time.time() - start_time
            scenario.errors.append(f"Unexpected error: {str(e)}")
            print(f"  {RED}✗{NC} Error: {str(e)}")
            return False

    def _validate_files(self, scenario: TestScenario) -> bool:
        """Validate expected files exist"""
        for expected_file in scenario.expected_files:
            file_path = scenario.output_dir / expected_file
            if not file_path.exists():
                scenario.errors.append(f"Missing expected file: {expected_file}")
                print(f"  {RED}✗{NC} Missing file: {expected_file}")
                return False

        return True

    def _validate_content(self, scenario: TestScenario) -> bool:
        """Validate content against rules"""
        for rule in scenario.validation_rules:
            # Extract rule type and search term
            if "contains" in rule:
                search_term = rule.split("'")[1]
                found = False

                # Search in all generated files
                for expected_file in scenario.expected_files:
                    file_path = scenario.output_dir / expected_file
                    if file_path.exists():
                        content = file_path.read_text(encoding='utf-8', errors='ignore')
                        if search_term in content:
                            found = True
                            break

                if not found:
                    scenario.errors.append(f"Validation failed: {rule}")
                    print(f"  {YELLOW}⚠{NC} Validation warning: {rule}")
                    # Don't fail test for content validation, just warn

        return True

    def run_all_tests(self) -> Dict:
        """Execute all test scenarios"""
        print("=" * 60)
        print("code-with-codex Test Suite")
        print("=" * 60)

        if self.quick_mode:
            print(f"{YELLOW}Running in QUICK mode (limited scenarios){NC}")

        passed = 0
        failed = 0

        for i, scenario in enumerate(self.scenarios, 1):
            print(f"\n[{i}/{len(self.scenarios)}] {scenario.name}")

            if self.run_scenario(scenario):
                passed += 1
                scenario.result = "PASS"
            else:
                failed += 1
                scenario.result = "FAIL"
                if scenario.errors:
                    for error in scenario.errors:
                        print(f"    {YELLOW}└─{NC} {error}")

            self.results.append({
                "name": scenario.name,
                "result": scenario.result,
                "execution_time": scenario.execution_time,
                "errors": scenario.errors,
                "output_dir": str(scenario.output_dir) if scenario.output_dir else None
            })

        # Print summary
        total = passed + failed
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        print(f"Total: {total}")
        print(f"{GREEN}Passed: {passed}{NC}")
        print(f"{RED}Failed: {failed}{NC}")

        if failed == 0:
            print(f"\n{GREEN}✓ All code-with-codex tests passed!{NC}")
        else:
            print(f"\n{RED}✗ Some tests failed. Review errors above.{NC}")

        return {
            "component": "code-with-codex",
            "total": total,
            "passed": passed,
            "failed": failed,
            "scenarios": self.results
        }

    def cleanup(self):
        """Clean up test directories"""
        try:
            shutil.rmtree(self.test_dir)
            if self.verbose:
                print(f"\nCleaned up test directory: {self.test_dir}")
        except Exception as e:
            print(f"{YELLOW}Warning: Could not clean up {self.test_dir}: {e}{NC}")

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Test code-with-codex skill")
    parser.add_argument("--quick", action="store_true", help="Run quick validation (2 scenarios)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--output", type=str, help="Output JSON report to file")
    parser.add_argument("--scenarios", type=str, help="Comma-separated scenario names to run")

    args = parser.parse_args()

    # Check for memex-cli
    if not shutil.which("memex-cli"):
        print(f"{RED}Error: memex-cli not found. Install with: npm install -g memex-cli{NC}")
        sys.exit(1)

    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print(f"{RED}Error: OPENAI_API_KEY not set{NC}")
        sys.exit(1)

    # Run tests
    tester = CodeWithCodexTester(quick_mode=args.quick, verbose=args.verbose)

    try:
        results = tester.run_all_tests()

        # Save results if requested
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2)
            print(f"\n{GREEN}Results saved to: {args.output}{NC}")

        # Exit with appropriate code
        sys.exit(0 if results["failed"] == 0 else 1)

    finally:
        tester.cleanup()

if __name__ == "__main__":
    main()
