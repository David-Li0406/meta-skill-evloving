#!/usr/bin/env python3
"""
Quality Gate Tool

Runs lint, build, and optional test checks to enforce code quality.

Usage:
    python quality_gate.py /path/to/project [--test]

Returns JSON with quality check results.
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class QualityGate:
    """Enforces code quality standards through automated checks."""

    def __init__(self, project_path: Path, run_tests: bool = False):
        self.project_path = project_path
        self.run_tests = run_tests
        self.results = {
            "lint": {"passed": False, "output": "", "errors": []},
            "build": {"passed": False, "output": "", "errors": []},
            "test": {"passed": None, "output": "", "errors": []}
        }

    def run_all_checks(self) -> Dict:
        """Run all quality checks."""

        # Check if package.json exists
        package_json = self.project_path / "package.json"
        if not package_json.exists():
            return {
                "passed": False,
                "error": "No package.json found. Not a Node.js project?",
                "checks": self.results
            }

        # Run checks in sequence
        self._run_lint()
        self._run_build()

        if self.run_tests:
            self._run_test()

        # Determine overall pass/fail
        all_passed = self.results["lint"]["passed"] and self.results["build"]["passed"]

        if self.run_tests:
            all_passed = all_passed and (self.results["test"]["passed"] or False)

        return {
            "passed": all_passed,
            "checks": self.results,
            "summary": self._generate_summary()
        }

    def _run_lint(self):
        """Run linting checks."""
        # Try different lint commands
        lint_commands = [
            ["npm", "run", "lint"],
            ["yarn", "lint"],
            ["npx", "eslint", "."],
        ]

        for cmd in lint_commands:
            if self._check_command_exists(cmd[0]):
                result = self._execute_command(cmd, timeout=120)
                if result is not None:
                    self.results["lint"]["passed"] = result["returncode"] == 0
                    self.results["lint"]["output"] = result["output"]
                    self.results["lint"]["errors"] = self._parse_lint_errors(result["output"])
                    return

        # No lint command available
        self.results["lint"]["passed"] = False
        self.results["lint"]["output"] = "No lint command available (tried: npm run lint, yarn lint, npx eslint)"
        self.results["lint"]["errors"] = ["Lint command not found"]

    def _run_build(self):
        """Run build checks."""
        # Try different build commands
        build_commands = [
            ["npm", "run", "build"],
            ["yarn", "build"],
            ["npx", "tsc", "--noEmit"],
        ]

        for cmd in build_commands:
            if self._check_command_exists(cmd[0]):
                result = self._execute_command(cmd, timeout=300)
                if result is not None:
                    self.results["build"]["passed"] = result["returncode"] == 0
                    self.results["build"]["output"] = result["output"]
                    self.results["build"]["errors"] = self._parse_build_errors(result["output"])
                    return

        # No build command available
        self.results["build"]["passed"] = False
        self.results["build"]["output"] = "No build command available (tried: npm run build, yarn build, npx tsc)"
        self.results["build"]["errors"] = ["Build command not found"]

    def _run_test(self):
        """Run test checks (optional)."""
        # Try different test commands
        test_commands = [
            ["npm", "test", "--", "--passWithNoTests"],
            ["yarn", "test", "--passWithNoTests"],
            ["npx", "jest", "--passWithNoTests"],
        ]

        for cmd in test_commands:
            if self._check_command_exists(cmd[0]):
                result = self._execute_command(cmd, timeout=300)
                if result is not None:
                    self.results["test"]["passed"] = result["returncode"] == 0
                    self.results["test"]["output"] = result["output"]
                    self.results["test"]["errors"] = self._parse_test_errors(result["output"])
                    return

        # No test command available
        self.results["test"]["passed"] = None
        self.results["test"]["output"] = "No test command available"
        self.results["test"]["errors"] = []

    def _check_command_exists(self, command: str) -> bool:
        """Check if a command exists."""
        try:
            subprocess.run(
                ["which", command],
                capture_output=True,
                check=False,
                timeout=5
            )
            return True
        except:
            return False

    def _execute_command(self, cmd: List[str], timeout: int = 120) -> Dict | None:
        """Execute a command and capture output."""
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=timeout
            )

            return {
                "returncode": result.returncode,
                "output": result.stdout + "\n" + result.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": 1,
                "output": f"Command timed out after {timeout} seconds"
            }
        except FileNotFoundError:
            return None
        except Exception as e:
            return {
                "returncode": 1,
                "output": f"Error executing command: {str(e)}"
            }

    def _parse_lint_errors(self, output: str) -> List[str]:
        """Parse lint errors from output."""
        errors = []

        # Common lint error patterns
        for line in output.split('\n'):
            line = line.strip()

            # ESLint format: path/file.ts:line:col - message
            if '.ts:' in line or '.tsx:' in line or '.js:' in line or '.jsx:' in line:
                if 'error' in line.lower() or 'warning' in line.lower():
                    errors.append(line)

            # Alternative format: error message (no path)
            elif line.startswith('✖') or 'error' in line.lower():
                errors.append(line)

        return errors[:10]  # Limit to first 10 errors

    def _parse_build_errors(self, output: str) -> List[str]:
        """Parse build errors from output."""
        errors = []

        # Common build error patterns
        for line in output.split('\n'):
            line = line.strip()

            # TypeScript errors: path/file.ts(line,col): error TS1234:
            if 'error TS' in line:
                errors.append(line)

            # Generic error messages
            elif 'error' in line.lower() and len(line) > 20:
                errors.append(line)

            # Module not found
            elif 'module not found' in line.lower():
                errors.append(line)

        return errors[:10]  # Limit to first 10 errors

    def _parse_test_errors(self, output: str) -> List[str]:
        """Parse test errors from output."""
        errors = []

        # Common test error patterns
        for line in output.split('\n'):
            line = line.strip()

            # Jest/Vitest: FAIL test/file.test.ts
            if line.startswith('FAIL') or line.startswith('●'):
                errors.append(line)

            # Test failure messages
            elif 'expected' in line.lower() and 'received' in line.lower():
                errors.append(line)

        return errors[:10]  # Limit to first 10 errors

    def _generate_summary(self) -> Dict:
        """Generate summary of quality checks."""
        summary = {
            "total_checks": 2,  # lint + build
            "passed_checks": 0,
            "failed_checks": 0
        }

        if self.results["lint"]["passed"]:
            summary["passed_checks"] += 1
        else:
            summary["failed_checks"] += 1

        if self.results["build"]["passed"]:
            summary["passed_checks"] += 1
        else:
            summary["failed_checks"] += 1

        if self.run_tests:
            summary["total_checks"] += 1
            if self.results["test"]["passed"]:
                summary["passed_checks"] += 1
            else:
                summary["failed_checks"] += 1

        return summary


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print(json.dumps({
            "passed": False,
            "error": "Usage: python quality_gate.py /path/to/project [--test]",
            "checks": {}
        }, indent=2))
        sys.exit(1)

    project_path = Path(sys.argv[1])

    if not project_path.exists():
        print(json.dumps({
            "passed": False,
            "error": f"Project path not found: {project_path}",
            "checks": {}
        }, indent=2))
        sys.exit(1)

    # Check for --test flag
    run_tests = "--test" in sys.argv

    # Run quality gate
    gate = QualityGate(project_path, run_tests)
    result = gate.run_all_checks()

    # Output JSON
    print(json.dumps(result, indent=2))

    # Exit with error code if quality gate failed
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
