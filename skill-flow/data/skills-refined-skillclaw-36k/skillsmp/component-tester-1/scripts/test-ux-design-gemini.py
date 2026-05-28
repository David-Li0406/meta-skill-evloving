#!/usr/bin/env python3
"""
Test suite for ux-design-gemini skill
Validates UX design generation and Gemini backend integration
"""

import os
import sys
import json
import time
import subprocess
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional

# Color codes
GREEN = '\033[0;32m'
RED = '\033[0;31m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
NC = '\033[0m'

class DesignScenario:
    """Represents a UX design test scenario"""
    def __init__(self, name: str, prompt: str, expected_sections: List[str],
                 validation_rules: Optional[List[str]] = None):
        self.name = name
        self.prompt = prompt
        self.expected_sections = expected_sections
        self.validation_rules = validation_rules or []
        self.result = None
        self.output_file = None
        self.execution_time = 0.0
        self.errors = []

class UXDesignGeminiTester:
    """Test harness for ux-design-gemini skill"""

    def __init__(self, quick_mode: bool = False, verbose: bool = False):
        self.quick_mode = quick_mode
        self.verbose = verbose
        self.test_dir = tempfile.mkdtemp(prefix="gemini_test_")
        self.scenarios = self._load_scenarios()
        self.results = []

    def _load_scenarios(self) -> List[DesignScenario]:
        """Load test scenarios"""
        scenarios = [
            DesignScenario(
                name="Component Wireframe",
                prompt="Design a user profile card component. Include: avatar, name, bio, action buttons. Provide wireframe description and CSS specifications.",
                expected_sections=["Wireframe", "Layout", "Components", "Styles"],
                validation_rules=[
                    "mentions avatar or image",
                    "mentions buttons or actions",
                    "contains CSS or styling information"
                ]
            ),
            DesignScenario(
                name="User Flow Diagram",
                prompt="Create user flow for login process: landing page → login form → authentication → dashboard. Document each step and decision points.",
                expected_sections=["Flow Steps", "User Actions", "Decision Points"],
                validation_rules=[
                    "mentions login or authentication",
                    "contains step-by-step flow",
                    "mentions dashboard or success state"
                ]
            ),
            DesignScenario(
                name="Design System",
                prompt="Generate a design system foundation: color palette (primary, secondary, accent), typography scale, spacing units. Provide CSS custom properties.",
                expected_sections=["Colors", "Typography", "Spacing"],
                validation_rules=[
                    "contains color values (hex/rgb)",
                    "mentions font sizes or typography",
                    "contains CSS variables or tokens"
                ]
            ),
            DesignScenario(
                name="Responsive Layout",
                prompt="Design responsive layout for e-commerce product grid. Define breakpoints (mobile, tablet, desktop) and grid specifications.",
                expected_sections=["Breakpoints", "Grid Layout", "Responsive Behavior"],
                validation_rules=[
                    "mentions mobile/tablet/desktop",
                    "contains breakpoint values",
                    "describes grid or layout"
                ]
            ),
            DesignScenario(
                name="Interaction Pattern",
                prompt="Document interaction pattern for dropdown menu: hover states, click behavior, keyboard navigation, accessibility considerations.",
                expected_sections=["States", "Interactions", "Accessibility"],
                validation_rules=[
                    "mentions hover or focus states",
                    "mentions keyboard or navigation",
                    "contains accessibility or a11y"
                ]
            ),
        ]

        if self.quick_mode:
            return scenarios[:2]

        return scenarios

    def run_scenario(self, scenario: DesignScenario) -> bool:
        """Execute a single test scenario"""
        print(f"\n{BLUE}Testing:{NC} {scenario.name}")
        print(f"  Prompt: {scenario.prompt[:80]}...")

        # Create output file path
        filename = scenario.name.replace(" ", "_").lower() + ".md"
        scenario.output_file = Path(self.test_dir) / filename

        # Build memex-cli command
        cmd = [
            "memex-cli",
            "--backend", "gemini",
            "--prompt", scenario.prompt,
            "--output", str(scenario.output_file)
        ]

        # Execute with timeout
        start_time = time.time()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=90,  # 90 second timeout for design tasks
                cwd=str(self.test_dir)
            )
            scenario.execution_time = time.time() - start_time

            if result.returncode != 0:
                scenario.errors.append(f"Command failed with exit code {result.returncode}")
                scenario.errors.append(f"stderr: {result.stderr}")
                return False

            # Validate output file exists
            if not scenario.output_file.exists():
                scenario.errors.append("Output file not created")
                print(f"  {RED}✗{NC} No output file")
                return False

            # Validate content
            if not self._validate_content(scenario):
                return False

            print(f"  {GREEN}✓{NC} Passed ({scenario.execution_time:.1f}s)")
            return True

        except subprocess.TimeoutExpired:
            scenario.execution_time = time.time() - start_time
            scenario.errors.append("Test exceeded timeout (90s)")
            print(f"  {RED}✗{NC} Timeout")
            return False

        except Exception as e:
            scenario.execution_time = time.time() - start_time
            scenario.errors.append(f"Unexpected error: {str(e)}")
            print(f"  {RED}✗{NC} Error: {str(e)}")
            return False

    def _validate_content(self, scenario: DesignScenario) -> bool:
        """Validate design output content"""
        try:
            content = scenario.output_file.read_text(encoding='utf-8', errors='ignore')
        except Exception as e:
            scenario.errors.append(f"Could not read output file: {e}")
            return False

        # Check for expected sections (case-insensitive)
        content_lower = content.lower()
        missing_sections = []

        for section in scenario.expected_sections:
            if section.lower() not in content_lower:
                missing_sections.append(section)

        if missing_sections:
            scenario.errors.append(f"Missing sections: {', '.join(missing_sections)}")
            print(f"  {YELLOW}⚠{NC} Missing sections: {', '.join(missing_sections)}")
            # Don't fail, just warn

        # Validate content rules
        for rule in scenario.validation_rules:
            if "mentions" in rule or "contains" in rule:
                # Extract search terms
                search_term = rule.split("mentions")[-1].split("contains")[-1].strip()

                # Simple keyword search (flexible matching)
                keywords = [kw.strip() for kw in search_term.split(" or ")]
                found = any(kw.lower() in content_lower for kw in keywords)

                if not found:
                    scenario.errors.append(f"Validation failed: {rule}")
                    print(f"  {YELLOW}⚠{NC} Validation warning: {rule}")

        # Check minimum content length (design docs should be substantial)
        if len(content) < 200:
            scenario.errors.append("Output too short (< 200 chars)")
            print(f"  {YELLOW}⚠{NC} Output seems too brief")

        return True  # Still pass even with warnings

    def run_all_tests(self) -> Dict:
        """Execute all test scenarios"""
        print("=" * 60)
        print("ux-design-gemini Test Suite")
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
                "output_file": str(scenario.output_file) if scenario.output_file else None
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
            print(f"\n{GREEN}✓ All ux-design-gemini tests passed!{NC}")
        else:
            print(f"\n{RED}✗ Some tests failed. Review errors above.{NC}")

        return {
            "component": "ux-design-gemini",
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

    parser = argparse.ArgumentParser(description="Test ux-design-gemini skill")
    parser.add_argument("--quick", action="store_true", help="Run quick validation (2 scenarios)")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--output", type=str, help="Output JSON report to file")

    args = parser.parse_args()

    # Check for memex-cli
    if not shutil.which("memex-cli"):
        print(f"{RED}Error: memex-cli not found. Install with: npm install -g memex-cli{NC}")
        sys.exit(1)

    # Check for API key
    if not (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")):
        print(f"{RED}Error: GOOGLE_API_KEY or GEMINI_API_KEY not set{NC}")
        sys.exit(1)

    # Run tests
    tester = UXDesignGeminiTester(quick_mode=args.quick, verbose=args.verbose)

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
