#!/usr/bin/env python3
"""
Cross-Language Output Verification Script for The Universal Axiom

This script verifies that all 4 language implementations (Python, JavaScript, Rust, Julia)
produce identical outputs for the same inputs, preventing formula drift.

Usage:
    python verify_outputs.py [--verbose] [--language LANG]

Options:
    --verbose         Show detailed output for each test
    --language LANG   Only test specific language (python|javascript|rust|julia)
    --tolerance FLOAT Set numerical tolerance (default: 1e-9)
"""

import json
import sys
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


@dataclass
class TestResult:
    """Result of a single test case"""
    language: str
    test_name: str
    passed: bool
    expected: Optional[Dict[str, Any]] = None
    actual: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

    def __str__(self):
        status = f"{GREEN}✓ PASS{RESET}" if self.passed else f"{RED}✗ FAIL{RESET}"
        return f"  [{status}] {self.language:12} - {self.test_name}"


class LanguageRunner:
    """Base class for language-specific test runners"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.available = self.check_availability()

    def check_availability(self) -> bool:
        """Check if the language runtime is available"""
        raise NotImplementedError

    def run_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """Run a single test case and return the results"""
        raise NotImplementedError


class PythonRunner(LanguageRunner):
    """Python implementation runner"""

    def check_availability(self) -> bool:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def run_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        if test_case.get('type') == 'sequence':
            return self._run_sequence_test(test_case)

        inputs = test_case['inputs']

        # Create temporary Python script
        script = f"""
import sys
sys.path.insert(0, '{self.project_root}/src/python')
from universal_axiom import UniversalAxiom, fibonacci_sequence
import json

axiom = UniversalAxiom(
    n={inputs['n']},
    impulses={inputs['impulses']},
    elements={inputs['elements']},
    pressure={inputs['pressure']},
    subjectivity={inputs['subjectivity']},
    purpose={inputs['purpose']},
    time={inputs['time']}
)

state = axiom.get_state()
intelligence = axiom.compute_intelligence()

result = {{
    'E_n': state['dynamic']['E_n'],
    'F_n': state['dynamic']['F_n'],
    'dynamic_product': state['dynamic']['product'],
    'foundation_product': state['foundation']['product'],
    'cognitive_product': state['cognitive']['product'],
    'intelligence': intelligence
}}

print(json.dumps(result))
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(script)
            script_path = f.name

        try:
            result = subprocess.run(
                ['python3', script_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return json.loads(result.stdout)
        finally:
            os.unlink(script_path)

    def _run_sequence_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        script = f"""
import sys
sys.path.insert(0, '{self.project_root}/src/python')
from universal_axiom import fibonacci_sequence
import json

sequence = fibonacci_sequence(12)
print(json.dumps({{'sequence': sequence}}))
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(script)
            script_path = f.name

        try:
            result = subprocess.run(['python3', script_path], capture_output=True, text=True, check=True, timeout=10)
            return json.loads(result.stdout)
        finally:
            os.unlink(script_path)


class JavaScriptRunner(LanguageRunner):
    """JavaScript/TypeScript implementation runner"""

    def check_availability(self) -> bool:
        try:
            subprocess.run(['node', '--version'], capture_output=True, check=True)
            # Check if compiled JS exists
            js_file = self.project_root / 'dist' / 'javascript' / 'universal-axiom.js'
            return js_file.exists()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def run_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        if test_case.get('type') == 'sequence':
            return self._run_sequence_test(test_case)

        inputs = test_case['inputs']

        script = f"""
const {{ UniversalAxiom }} = require('{self.project_root}/dist/javascript/universal-axiom');

const axiom = new UniversalAxiom({{
    n: {inputs['n']},
    impulses: {inputs['impulses']},
    elements: {inputs['elements']},
    pressure: {inputs['pressure']},
    subjectivity: {inputs['subjectivity']},
    purpose: {inputs['purpose']},
    time: {inputs['time']}
}});

const state = axiom.getState();
const intelligence = axiom.computeIntelligence();

const result = {{
    E_n: state.dynamic.E_n,
    F_n: state.dynamic.F_n,
    dynamic_product: state.dynamic.product,
    foundation_product: state.foundation.product,
    cognitive_product: state.cognitive.product,
    intelligence: intelligence
}};

console.log(JSON.stringify(result));
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(script)
            script_path = f.name

        try:
            result = subprocess.run(
                ['node', script_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return json.loads(result.stdout)
        finally:
            os.unlink(script_path)

    def _run_sequence_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        script = f"""
const {{ fibonacciSequence }} = require('{self.project_root}/dist/javascript/universal-axiom');
const sequence = fibonacciSequence(12);
console.log(JSON.stringify({{ sequence: sequence }}));
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write(script)
            script_path = f.name

        try:
            result = subprocess.run(['node', script_path], capture_output=True, text=True, check=True, timeout=10)
            return json.loads(result.stdout)
        finally:
            os.unlink(script_path)


class RustRunner(LanguageRunner):
    """Rust implementation runner"""

    def check_availability(self) -> bool:
        try:
            subprocess.run(['cargo', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def run_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        if test_case.get('type') == 'sequence':
            return self._run_sequence_test(test_case)

        inputs = test_case['inputs']

        # Create a temporary Rust program
        rust_code = f"""
use universal_axiom::UniversalAxiom;
use serde_json::json;

fn main() {{
    let axiom = UniversalAxiom::with_params(
        {inputs['impulses']},  // impulses
        {inputs['elements']},  // elements
        {inputs['pressure']},  // pressure
        {inputs['subjectivity']},  // subjectivity
        {inputs['purpose']},  // purpose
        {inputs['time']},  // time
        {inputs['n']}  // n
    );

    let state = axiom.get_state();
    let intelligence = axiom.compute_intelligence();

    let result = json!({{
        "E_n": state.dynamic.e_n,
        "F_n": state.dynamic.f_n,
        "dynamic_product": state.dynamic.product,
        "foundation_product": state.foundation.product,
        "cognitive_product": state.cognitive.product,
        "intelligence": intelligence
    }});

    println!("{{}}", result);
}}
"""

        # Create temporary Cargo project
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            src_dir = tmpdir / 'src'
            src_dir.mkdir()

            # Write main.rs
            (src_dir / 'main.rs').write_text(rust_code)

            # Write Cargo.toml
            cargo_toml = f"""
[package]
name = "axiom_test"
version = "0.1.0"
edition = "2021"

[dependencies]
universal-axiom = {{ path = "{self.project_root}/src/rust" }}
serde_json = "1.0"
"""
            (tmpdir / 'Cargo.toml').write_text(cargo_toml)

            try:
                result = subprocess.run(
                    ['cargo', 'run', '--quiet'],
                    cwd=tmpdir,
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=60
                )
                return json.loads(result.stdout)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Rust execution failed: {e.stderr}")

    def _run_sequence_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        rust_code = """
use universal_axiom::fibonacci_sequence;
use serde_json::json;

fn main() {
    let sequence = fibonacci_sequence(12);
    let result = json!({ "sequence": sequence });
    println!("{}", result);
}
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            src_dir = tmpdir / 'src'
            src_dir.mkdir()

            (src_dir / 'main.rs').write_text(rust_code)
            cargo_toml = f"""
[package]
name = "axiom_test"
version = "0.1.0"
edition = "2021"

[dependencies]
universal-axiom = {{ path = "{self.project_root}/src/rust" }}
serde_json = "1.0"
"""
            (tmpdir / 'Cargo.toml').write_text(cargo_toml)

            try:
                result = subprocess.run(['cargo', 'run', '--quiet'], cwd=tmpdir, capture_output=True, text=True, check=True, timeout=60)
                return json.loads(result.stdout)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"Rust execution failed: {e.stderr}")


class JuliaRunner(LanguageRunner):
    """Julia implementation runner"""

    def check_availability(self) -> bool:
        try:
            subprocess.run(['julia', '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def run_test_case(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        if test_case.get('type') == 'sequence':
            return self._run_sequence_test(test_case)

        inputs = test_case['inputs']

        script = f"""
include("{self.project_root}/src/julia/UniversalAxiom.jl")
using .UniversalAxiom
using JSON

axiom = Axiom(
    n={inputs['n']},
    impulses={inputs['impulses']},
    elements={inputs['elements']},
    pressure={inputs['pressure']},
    subjectivity={inputs['subjectivity']},
    purpose={inputs['purpose']},
    time={inputs['time']}
)

state = get_state(axiom)
state_dict = state_to_dict(state)
intelligence = compute_intelligence(axiom)

result = Dict(
    "E_n" => state_dict["dynamic"]["E_n"],
    "F_n" => state_dict["dynamic"]["F_n"],
    "dynamic_product" => state_dict["dynamic"]["product"],
    "foundation_product" => state_dict["foundation"]["product"],
    "cognitive_product" => state_dict["cognitive"]["product"],
    "intelligence" => intelligence
)

println(JSON.json(result))
"""

        with tempfile.NamedTemporaryFile(mode='w', suffix='.jl', delete=False) as f:
            f.write(script)
            script_path = f.name

        try:
            result = subprocess.run(
                ['julia', script_path],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            return json.loads(result.stdout)
        finally:
            os.unlink(script_path)

    def _run_sequence_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        script = f"""
include("{self.project_root}/src/julia/UniversalAxiom.jl")
using .UniversalAxiom
using JSON

sequence = fibonacci_sequence(12)
println(JSON.json(Dict("sequence" => sequence)))
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.jl', delete=False) as f:
            f.write(script)
            script_path = f.name

        try:
            result = subprocess.run(['julia', script_path], capture_output=True, text=True, check=True, timeout=30)
            return json.loads(result.stdout)
        finally:
            os.unlink(script_path)


class OutputVerifier:
    """Main verification orchestrator"""

    def __init__(self, project_root: Path, tolerance: float = 1e-9, verbose: bool = False):
        self.project_root = project_root
        self.tolerance = tolerance
        self.verbose = verbose

        self.runners = {
            'python': PythonRunner(project_root),
            'javascript': JavaScriptRunner(project_root),
            'rust': RustRunner(project_root),
            'julia': JuliaRunner(project_root)
        }

    def load_test_cases(self) -> Dict[str, Any]:
        """Load canonical test cases"""
        test_file = self.project_root / 'tests' / 'canonical_test_cases.json'
        with open(test_file) as f:
            return json.load(f)

    def compare_values(self, expected: Any, actual: Any, tolerance: float) -> Tuple[bool, str]:
        """Compare expected and actual values with tolerance for floats"""
        if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
            if abs(expected - actual) <= tolerance:
                return True, ""
            else:
                return False, f"Expected {expected}, got {actual} (diff: {abs(expected - actual)})"

        elif isinstance(expected, list) and isinstance(actual, list):
            if len(expected) != len(actual):
                return False, f"List length mismatch: expected {len(expected)}, got {len(actual)}"

            for i, (exp, act) in enumerate(zip(expected, actual)):
                match, msg = self.compare_values(exp, act, tolerance)
                if not match:
                    return False, f"Element {i}: {msg}"
            return True, ""

        elif expected == actual:
            return True, ""
        else:
            return False, f"Expected {expected}, got {actual}"

    def run_verification(self, language_filter: Optional[str] = None) -> Tuple[List[TestResult], bool]:
        """Run verification across all available languages"""
        test_data = self.load_test_cases()
        results = []
        all_passed = True

        # Determine which languages to test
        if language_filter:
            languages = [language_filter]
        else:
            languages = list(self.runners.keys())

        # Check availability
        print(f"\n{BOLD}=== Language Availability ==={RESET}")
        available_languages = []
        for lang in languages:
            runner = self.runners[lang]
            status = f"{GREEN}✓ Available{RESET}" if runner.available else f"{YELLOW}✗ Not Available{RESET}"
            print(f"  {lang:12} {status}")
            if runner.available:
                available_languages.append(lang)

        if not available_languages:
            print(f"\n{RED}ERROR: No languages available for testing!{RESET}")
            return results, False

        print(f"\n{BOLD}=== Running Tests ==={RESET}\n")

        # Run tests
        for test_case in test_data['test_cases']:
            test_name = test_case['name']

            if self.verbose:
                print(f"\n{BLUE}Test: {test_name}{RESET}")
                print(f"  Description: {test_case['description']}")

            for lang in available_languages:
                runner = self.runners[lang]

                try:
                    actual = runner.run_test_case(test_case)

                    # Compare with expected
                    if test_case.get('type') == 'sequence':
                        expected_seq = test_case['expected_sequence']
                        actual_seq = actual['sequence']
                        match, msg = self.compare_values(expected_seq, actual_seq, self.tolerance)

                        result = TestResult(
                            language=lang,
                            test_name=test_name,
                            passed=match,
                            expected={'sequence': expected_seq},
                            actual=actual,
                            error=msg if not match else None
                        )
                    else:
                        expected = test_case['expected']
                        all_match = True
                        errors = []

                        for key, expected_val in expected.items():
                            if key in actual:
                                match, msg = self.compare_values(expected_val, actual[key], self.tolerance)
                                if not match:
                                    all_match = False
                                    errors.append(f"{key}: {msg}")
                            else:
                                all_match = False
                                errors.append(f"Missing key: {key}")

                        result = TestResult(
                            language=lang,
                            test_name=test_name,
                            passed=all_match,
                            expected=expected,
                            actual=actual,
                            error="; ".join(errors) if errors else None
                        )

                    if not result.passed:
                        all_passed = False

                    results.append(result)

                    if self.verbose or not result.passed:
                        print(str(result))
                        if result.error:
                            print(f"    Error: {result.error}")

                except Exception as e:
                    result = TestResult(
                        language=lang,
                        test_name=test_name,
                        passed=False,
                        error=str(e)
                    )
                    results.append(result)
                    all_passed = False

                    print(str(result))
                    if self.verbose:
                        print(f"    Exception: {e}")

        return results, all_passed

    def print_summary(self, results: List[TestResult], all_passed: bool):
        """Print summary of test results"""
        print(f"\n{BOLD}=== Summary ==={RESET}\n")

        # Group by language
        by_language = {}
        for result in results:
            if result.language not in by_language:
                by_language[result.language] = []
            by_language[result.language].append(result)

        for lang, lang_results in sorted(by_language.items()):
            passed = sum(1 for r in lang_results if r.passed)
            total = len(lang_results)
            status = f"{GREEN}✓{RESET}" if passed == total else f"{RED}✗{RESET}"
            print(f"  [{status}] {lang:12} {passed}/{total} tests passed")

        print(f"\n{BOLD}Overall Status:{RESET} ", end='')
        if all_passed:
            print(f"{GREEN}✓ ALL TESTS PASSED{RESET}")
            print(f"\n{GREEN}All language implementations produce identical outputs!{RESET}")
        else:
            print(f"{RED}✗ SOME TESTS FAILED{RESET}")
            print(f"\n{RED}⚠️  FORMULA DRIFT DETECTED!{RESET}")
            print(f"{YELLOW}Some implementations produce different outputs.{RESET}")
            print(f"{YELLOW}Review the failed tests above and sync implementations.{RESET}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Verify Universal Axiom outputs across languages')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--language', '-l', choices=['python', 'javascript', 'rust', 'julia'],
                       help='Only test specific language')
    parser.add_argument('--tolerance', '-t', type=float, default=1e-9,
                       help='Numerical tolerance for comparisons (default: 1e-9)')

    args = parser.parse_args()

    project_root = Path(__file__).parent.absolute()
    verifier = OutputVerifier(project_root, tolerance=args.tolerance, verbose=args.verbose)

    print(f"{BOLD}Universal Axiom - Cross-Language Output Verification{RESET}")
    print(f"Project: {project_root}")
    print(f"Tolerance: {args.tolerance}")

    results, all_passed = verifier.run_verification(language_filter=args.language)
    verifier.print_summary(results, all_passed)

    sys.exit(0 if all_passed else 1)


if __name__ == '__main__':
    main()
