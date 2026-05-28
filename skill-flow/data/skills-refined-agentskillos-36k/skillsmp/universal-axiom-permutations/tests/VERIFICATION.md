# Cross-Language Output Verification

This directory contains tools to verify that all language implementations of The Universal Axiom produce identical outputs, preventing formula drift between implementations.

## Overview

The verification system consists of:

1. **`canonical_test_cases.json`** - Canonical test cases with expected outputs
2. **`verify_outputs.py`** - Main verification script that runs all implementations
3. **CI/CD integration** - Automatic verification on every push

## The Problem: Formula Drift

When maintaining multiple implementations of the same mathematical formula across different languages, it's easy for implementations to diverge over time. This can happen due to:

- Different exponential bases (e^n vs 3^n)
- Different Fibonacci sequence indexing (starting at 0 vs 1)
- Rounding differences
- Implementation bugs
- Updates to one language but not others

**Formula drift** means the implementations no longer produce identical outputs for the same inputs, breaking the fundamental property that the axiom should mirror physical laws deterministically.

## The Solution: Automated Verification

The `verify_outputs.py` script:

1. Loads canonical test cases from `canonical_test_cases.json`
2. Runs each test case against all available language implementations
3. Compares outputs with numerical tolerance (default: 1e-9)
4. Reports any differences detected
5. Exits with error code 1 if any tests fail (perfect for CI/CD)

## Usage

### Run Full Verification

```bash
python verify_outputs.py
```

This tests all available languages (Python, JavaScript, Rust, Julia) and reports results.

### Verbose Mode

```bash
python verify_outputs.py --verbose
```

Shows detailed output for each test case.

### Test Specific Language

```bash
python verify_outputs.py --language python
python verify_outputs.py --language javascript
python verify_outputs.py --language rust
python verify_outputs.py --language julia
```

### Adjust Tolerance

```bash
python verify_outputs.py --tolerance 1e-6
```

Sets numerical comparison tolerance (default: 1e-9).

## Example Output

### When All Tests Pass

```
Universal Axiom - Cross-Language Output Verification
Project: /home/user/pointy-stick
Tolerance: 1e-09

=== Language Availability ===
  python       ✓ Available
  javascript   ✓ Available
  rust         ✓ Available
  julia        ✗ Not Available

=== Running Tests ===

  [✓ PASS] python       - basic_n1
  [✓ PASS] javascript   - basic_n1
  [✓ PASS] rust         - basic_n1
  ...

=== Summary ===

  [✓] javascript   9/9 tests passed
  [✓] python       9/9 tests passed
  [✓] rust         9/9 tests passed

Overall Status: ✓ ALL TESTS PASSED

All language implementations produce identical outputs!
```

### When Formula Drift is Detected

```
=== Summary ===

  [✓] javascript   9/9 tests passed
  [✓] python       9/9 tests passed
  [✗] rust         1/9 tests passed

Overall Status: ✗ SOME TESTS FAILED

⚠️  FORMULA DRIFT DETECTED!
Some implementations produce different outputs.
Review the failed tests above and sync implementations.
```

With `--verbose`, you'll see exactly which values differ:

```
[✗ FAIL] rust - basic_n1
  Error: E_n: Expected 5.0, got 2.718281828459045 (diff: 2.281718171540955)
         dynamic_product: Expected 10.0, got 5.43656365691809
         intelligence: Expected 10.0, got 5.43656365691809
```

## Canonical Test Cases

The `canonical_test_cases.json` file defines the "source of truth" for all implementations. It includes:

### Formula Specification

```json
{
  "formula": "Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)",
  "exponential_formula": "E_n = 2 * 3^n - 1",
  "base_exponential": 3.0,
  "fibonacci_indexing": "F(1) = 1, F(2) = 1, F(3) = 2, ..."
}
```

### Test Cases

Each test case specifies:

- **inputs**: All parameters (n, impulses, elements, pressure, subjectivity, purpose, time)
- **expected**: Expected output values for each component
  - `E_n` - Exponential growth value
  - `F_n` - Fibonacci value at n
  - `dynamic_product` - E_n · (1 + F_n)
  - `foundation_product` - A · B · C
  - `cognitive_product` - X · Y · Z
  - `intelligence` - Final intelligence value

Example:

```json
{
  "name": "basic_n1",
  "description": "Basic computation at n=1 with default parameters",
  "inputs": {
    "n": 1,
    "impulses": 1.0,
    "elements": 1.0,
    "pressure": 1.0,
    "subjectivity": 0.0,
    "purpose": 1.0,
    "time": 1.0
  },
  "expected": {
    "E_n": 5.0,
    "F_n": 1,
    "dynamic_product": 10.0,
    "foundation_product": 1.0,
    "cognitive_product": 1.0,
    "intelligence": 10.0
  }
}
```

## Adding New Test Cases

To add a new test case:

1. Edit `canonical_test_cases.json`
2. Add a new entry to the `test_cases` array
3. Specify all inputs and expected outputs
4. Run verification to ensure all languages pass

## CI/CD Integration

The verification runs automatically on GitHub Actions for every push and pull request.

See `.github/workflows/test.yml` for the CI configuration.

The workflow:
1. Runs individual language test suites (Python, JavaScript, Rust, Julia)
2. Builds all implementations
3. Sets up all 4 language environments
4. Runs cross-language verification against all available languages
5. Fails the build if any drift is detected

All 4 languages are now tested in CI/CD:
- Python 3.11
- Node.js 20
- Rust (latest stable)
- Julia 1.9

## How It Works

### Language Runners

The verification script includes specialized runners for each language:

#### PythonRunner
- Creates temporary Python scripts
- Imports from `src/python/universal_axiom.py`
- Captures JSON output

#### JavaScriptRunner
- Creates temporary JavaScript files
- Requires pre-built TypeScript in `dist/javascript/`
- Uses Node.js to execute

#### RustRunner
- Creates temporary Cargo projects
- Links to `src/rust` via path dependency
- Compiles and runs with `cargo run --quiet`

#### JuliaRunner
- Creates temporary Julia scripts
- Includes module from `src/julia/UniversalAxiom.jl`
- Uses JSON.jl for output

### Comparison Logic

Values are compared with configurable numerical tolerance (default: 1e-9) to account for floating-point precision differences across languages.

- Integers and floats: Absolute difference <= tolerance
- Lists: Element-wise comparison
- Nested structures: Recursive comparison

## Troubleshooting

### Language Not Available

If a language shows as "Not Available":

- **Python**: Ensure `python3` is in PATH
- **JavaScript**: Ensure `node` is in PATH and `npm install` + `npx tsc` have been run
- **Rust**: Ensure `cargo` is in PATH
- **Julia**: Ensure `julia` is in PATH

### Compilation Errors

If a language fails with compilation errors, the implementation may have API changes. Check the runner code in `verify_outputs.py` to ensure it's using the correct API for that language.

### False Positives

If tests fail due to legitimate precision differences:
- Adjust tolerance: `--tolerance 1e-6`
- Ensure all implementations use the same floating-point precision

## Maintaining the Verification System

When updating the formula:

1. **Update ALL implementations** to use the same formula
2. **Update `canonical_test_cases.json`** with new expected values
3. **Run verification** to ensure all languages pass
4. **Commit changes** to all implementations together

Never update just one implementation - this will immediately cause drift detection!

## Benefits

✅ **Early Detection**: Catch formula drift immediately, not in production
✅ **Confidence**: Know all implementations are mathematically equivalent
✅ **Documentation**: Canonical test cases serve as executable specification
✅ **Regression Prevention**: Prevent accidental formula changes
✅ **Cross-Language Consistency**: Ensure deterministic behavior across all implementations

## Related Files

- `../verify_outputs.py` - Main verification script
- `canonical_test_cases.json` - Test cases and expected outputs
- `../.github/workflows/test.yml` - CI/CD configuration
- `test_universal_axiom.py` - Python unit tests
- `universal-axiom.test.js` - JavaScript unit tests
- `test_universal_axiom.jl` - Julia unit tests
- `../src/rust/lib.rs` - Rust implementation (includes tests)

---

**Remember**: The Axiom doesn't answer questions. It generates the conditions from which answers must emerge. This verification system ensures those conditions are identical across all implementations.
