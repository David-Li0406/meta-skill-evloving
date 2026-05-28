#!/usr/bin/env python3
"""
Main test orchestrator for component-tester skill
Runs all component tests and generates comprehensive report
"""

import os
import sys
import json
import time
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
CYAN = '\033[0;36m'
NC = '\033[0m'

class ComponentTestOrchestrator:
    """Orchestrates all component tests"""

    def __init__(self, ci_mode: bool = False, verbose: bool = False,
                 profile: bool = False, fail_fast: bool = False):
        self.ci_mode = ci_mode
        self.verbose = verbose
        self.profile = profile
        self.fail_fast = fail_fast
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "environment": self._gather_environment(),
            "components": {}
        }
        self.scripts_dir = Path(__file__).parent

    def _gather_environment(self) -> Dict:
        """Gather environment information"""
        env_info = {
            "platform": sys.platform,
            "python_version": sys.version,
            "memex_cli_version": None,
            "api_keys_configured": []
        }

        # Check memex-cli version
        try:
            result = subprocess.run(
                ["memex-cli", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                env_info["memex_cli_version"] = result.stdout.strip()
        except:
            pass

        # Check API keys (don't expose values)
        if os.environ.get("ANTHROPIC_API_KEY"):
            env_info["api_keys_configured"].append("ANTHROPIC_API_KEY")
        if os.environ.get("OPENAI_API_KEY"):
            env_info["api_keys_configured"].append("OPENAI_API_KEY")
        if os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY"):
            env_info["api_keys_configured"].append("GOOGLE/GEMINI_API_KEY")

        return env_info

    def run_dependency_check(self) -> bool:
        """Phase 1: Validate dependencies"""
        print(f"\n{CYAN}{'=' * 60}{NC}")
        print(f"{CYAN}Phase 1: Dependency Check{NC}")
        print(f"{CYAN}{'=' * 60}{NC}")

        # Run test-memex-cli.sh
        script_path = self.scripts_dir / "test-memex-cli.sh"

        if not script_path.exists():
            print(f"{YELLOW}⚠ test-memex-cli.sh not found, skipping{NC}")
            return True

        try:
            result = subprocess.run(
                ["bash", str(script_path)],
                capture_output=not self.verbose,
                timeout=60
            )

            success = result.returncode == 0
            self.results["components"]["dependency_check"] = {
                "status": "PASS" if success else "FAIL",
                "exit_code": result.returncode
            }

            if not success and self.fail_fast:
                print(f"\n{RED}✗ Dependency check failed. Stopping (fail-fast mode).{NC}")
                return False

            return success

        except subprocess.TimeoutExpired:
            print(f"{RED}✗ Dependency check timeout{NC}")
            self.results["components"]["dependency_check"] = {
                "status": "TIMEOUT"
            }
            return False
        except Exception as e:
            print(f"{RED}✗ Dependency check error: {e}{NC}")
            return False

    def run_component_tests(self) -> bool:
        """Phase 2: Run individual component tests"""
        print(f"\n{CYAN}{'=' * 60}{NC}")
        print(f"{CYAN}Phase 2: Component Tests{NC}")
        print(f"{CYAN}{'=' * 60}{NC}")

        component_scripts = [
            ("code-with-codex", "test-code-with-codex.py", "OPENAI_API_KEY"),
            ("ux-design-gemini", "test-ux-design-gemini.py", "GOOGLE_API_KEY,GEMINI_API_KEY"),
        ]

        all_passed = True

        for component_name, script_name, required_keys in component_scripts:
            print(f"\n{BLUE}Testing: {component_name}{NC}")

            # Check if required API keys are available
            keys = required_keys.split(",")
            has_key = any(os.environ.get(key.strip()) for key in keys)

            if not has_key:
                print(f"{YELLOW}⚠ Skipping (no API key: {required_keys}){NC}")
                self.results["components"][component_name] = {
                    "status": "SKIPPED",
                    "reason": f"Missing API key: {required_keys}"
                }
                continue

            script_path = self.scripts_dir / script_name

            if not script_path.exists():
                print(f"{YELLOW}⚠ Script not found: {script_name}{NC}")
                self.results["components"][component_name] = {
                    "status": "SKIPPED",
                    "reason": "Script not found"
                }
                continue

            # Build command
            cmd = [sys.executable, str(script_path)]
            if self.verbose:
                cmd.append("--verbose")

            # Run with temporary output file
            output_file = Path(f"/tmp/{component_name}_test_result.json")
            cmd.extend(["--output", str(output_file)])

            try:
                start_time = time.time()
                result = subprocess.run(
                    cmd,
                    capture_output=not self.verbose,
                    timeout=300  # 5 minute timeout per component
                )
                execution_time = time.time() - start_time

                # Load results if available
                if output_file.exists():
                    with open(output_file, 'r') as f:
                        component_results = json.load(f)
                    self.results["components"][component_name] = component_results
                    self.results["components"][component_name]["execution_time"] = execution_time
                else:
                    self.results["components"][component_name] = {
                        "status": "FAIL" if result.returncode != 0 else "PASS",
                        "exit_code": result.returncode,
                        "execution_time": execution_time
                    }

                if result.returncode != 0:
                    all_passed = False
                    print(f"{RED}✗ {component_name} tests failed{NC}")

                    if self.fail_fast:
                        print(f"\n{RED}Stopping (fail-fast mode).{NC}")
                        return False
                else:
                    print(f"{GREEN}✓ {component_name} tests passed{NC}")

            except subprocess.TimeoutExpired:
                print(f"{RED}✗ {component_name} tests timeout{NC}")
                self.results["components"][component_name] = {
                    "status": "TIMEOUT"
                }
                all_passed = False

                if self.fail_fast:
                    return False

            except Exception as e:
                print(f"{RED}✗ {component_name} error: {e}{NC}")
                self.results["components"][component_name] = {
                    "status": "ERROR",
                    "error": str(e)
                }
                all_passed = False

        return all_passed

    def run_integration_tests(self) -> bool:
        """Phase 3: Integration tests (placeholder)"""
        print(f"\n{CYAN}{'=' * 60}{NC}")
        print(f"{CYAN}Phase 3: Integration Tests{NC}")
        print(f"{CYAN}{'=' * 60}{NC}")

        print(f"{YELLOW}⚠ Integration tests not yet implemented{NC}")
        self.results["components"]["integration_tests"] = {
            "status": "SKIPPED",
            "reason": "Not implemented"
        }

        return True

    def generate_summary(self):
        """Generate test summary"""
        print(f"\n{CYAN}{'=' * 60}{NC}")
        print(f"{CYAN}Test Summary{NC}")
        print(f"{CYAN}{'=' * 60}{NC}")

        total_components = len(self.results["components"])
        passed = sum(1 for c in self.results["components"].values()
                    if c.get("status") == "PASS" or c.get("passed", 0) > 0 and c.get("failed", 0) == 0)
        failed = sum(1 for c in self.results["components"].values()
                    if c.get("status") == "FAIL" or c.get("failed", 0) > 0)
        skipped = sum(1 for c in self.results["components"].values()
                     if c.get("status") == "SKIPPED")

        print(f"\nComponents tested: {total_components}")
        print(f"{GREEN}Passed: {passed}{NC}")
        print(f"{RED}Failed: {failed}{NC}")
        print(f"{YELLOW}Skipped: {skipped}{NC}")

        # Detailed component status
        print(f"\n{BLUE}Component Status:{NC}")
        for component, result in self.results["components"].items():
            status = result.get("status", "UNKNOWN")
            if status == "PASS" or (result.get("passed", 0) > 0 and result.get("failed", 0) == 0):
                status_color = GREEN
                status_icon = "✓"
            elif status == "FAIL" or result.get("failed", 0) > 0:
                status_color = RED
                status_icon = "✗"
            elif status == "SKIPPED":
                status_color = YELLOW
                status_icon = "○"
            else:
                status_color = YELLOW
                status_icon = "?"

            component_display = component.replace("_", "-")
            print(f"  {status_color}{status_icon}{NC} {component_display}")

            # Show test counts if available
            if "passed" in result and "failed" in result:
                print(f"      Tests: {result['passed']} passed, {result['failed']} failed")

        # Overall result
        print(f"\n{CYAN}{'=' * 60}{NC}")
        if failed == 0 and passed > 0:
            print(f"{GREEN}✓ All tests passed!{NC}")
            return True
        elif failed > 0:
            print(f"{RED}✗ Some tests failed.{NC}")
            return False
        else:
            print(f"{YELLOW}⚠ No tests executed successfully.{NC}")
            return False

    def run(self, output_file: str = None) -> bool:
        """Run complete test suite"""
        print(f"{CYAN}{'=' * 60}{NC}")
        print(f"{CYAN}Component Test Suite{NC}")
        print(f"{CYAN}{'=' * 60}{NC}")
        print(f"Mode: {'CI' if self.ci_mode else 'Interactive'}")
        print(f"Timestamp: {self.results['timestamp']}")

        # Phase 1: Dependencies
        if not self.run_dependency_check():
            print(f"\n{RED}✗ Dependency check failed. Cannot continue.{NC}")
            self.results["overall_status"] = "FAILED"
            if output_file:
                self._save_results(output_file)
            return False

        # Phase 2: Component tests
        if not self.run_component_tests():
            print(f"\n{RED}✗ Component tests failed.{NC}")
            self.results["overall_status"] = "FAILED"
            if output_file:
                self._save_results(output_file)
            return False

        # Phase 3: Integration tests
        self.run_integration_tests()

        # Generate summary
        success = self.generate_summary()
        self.results["overall_status"] = "PASSED" if success else "FAILED"

        # Save results
        if output_file:
            self._save_results(output_file)

        return success

    def _save_results(self, output_file: str):
        """Save test results to file"""
        try:
            with open(output_file, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"\n{GREEN}Results saved to: {output_file}{NC}")
        except Exception as e:
            print(f"\n{RED}Error saving results: {e}{NC}")

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run complete component test suite"
    )
    parser.add_argument("--output", type=str, help="Save results to JSON file")
    parser.add_argument("--ci-mode", action="store_true", help="CI-friendly mode (no interactive prompts)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--profile", action="store_true", help="Enable performance profiling")
    parser.add_argument("--fail-fast", action="store_true", help="Stop on first failure")

    args = parser.parse_args()

    orchestrator = ComponentTestOrchestrator(
        ci_mode=args.ci_mode,
        verbose=args.verbose,
        profile=args.profile,
        fail_fast=args.fail_fast
    )

    success = orchestrator.run(output_file=args.output)

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
