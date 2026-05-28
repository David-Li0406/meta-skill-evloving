# Contributing to The Universal Axiom

Thank you for your interest in contributing to The Universal Axiom! This guide will help you get started with development.

## Table of Contents

- [Quick Start](#quick-start)
- [Development Environment](#development-environment)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Submitting Changes](#submitting-changes)
- [Project Structure](#project-structure)

---

## Quick Start

### Prerequisites

Make sure you have the following installed:

- **Node.js** 16+ (for JavaScript/TypeScript)
- **Python** 3.11+ (for Python implementation)
- **Rust** (latest stable) (for Rust implementation)
- **Julia** 1.9+ (optional, for Julia implementation)
- **Make** (for unified build commands)

### One-Command Setup

```bash
make install
```

This will install all JavaScript and Python dependencies.

---

## Development Environment

### Using Make (Recommended)

We provide a comprehensive Makefile for unified development across all languages.

**View all available commands:**
```bash
make help
```

**Common commands:**
```bash
make install          # Install all dependencies
make build            # Build all projects
make test             # Run all tests
make lint             # Lint all code
make clean            # Clean build artifacts
```

### Manual Setup

If you prefer manual setup:

**JavaScript/TypeScript:**
```bash
npm install
npm run build
npm test
```

**Python:**
```bash
pip install -r requirements.txt
python -m pytest tests/test_universal_axiom.py -v
```

**Rust:**
```bash
cd src/rust
cargo build --release
cargo test
```

---

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Edit the relevant files in:
- `src/javascript/` for TypeScript/JavaScript
- `src/python/` for Python
- `src/rust/` for Rust
- `src/julia/` for Julia

### 3. Run Tests Continuously

**JavaScript (watch mode):**
```bash
make test-watch
# or
npm test -- --watch
```

**Build in watch mode:**
```bash
make dev
# or
npm run build:watch
```

### 4. Pre-Commit Checks

Before committing, we automatically run:
- ✅ TypeScript type checking
- ✅ ESLint on staged files
- ✅ All tests
- ✅ Python compilation checks

These run automatically via Husky git hooks when you commit.

**Manual pre-commit check:**
```bash
make check
# or for quick checks without tests
make check-quick
```

### 5. Format Code

**Format all code:**
```bash
make format
```

**Format Python only:**
```bash
make format-python
# or
black src/python tests/*.py
```

---

## Testing

### Run All Tests

```bash
make test
```

This runs tests for JavaScript, Python, and Rust in parallel.

### Run Tests for Specific Language

```bash
make test-js        # JavaScript/TypeScript tests
make test-python    # Python tests
make test-rust      # Rust tests
make test-julia     # Julia tests (optional)
```

### Test Coverage

```bash
make test-coverage
```

This generates coverage reports for JavaScript and Python.

### Golden Test Cases

All implementations must pass the golden test cases in `tests/golden_cases.csv`. These ensure cross-language consistency.

**Verify cross-language parity:**
```bash
python verify_outputs.py --verbose
```

---

## Code Quality

### Linting

**Lint all code:**
```bash
make lint
```

**Lint specific language:**
```bash
make lint-js        # JavaScript/TypeScript
make lint-python    # Python (black + mypy)
make lint-rust      # Rust (clippy)
```

### Type Checking

**TypeScript type checking:**
```bash
make type-check
# or
npm run type-check
```

**Python type checking:**
```bash
mypy src/python
```

### Code Style

We follow these style guidelines:

**JavaScript/TypeScript:**
- ESLint with TypeScript strict mode
- Prettier-compatible formatting
- No `any` types

**Python:**
- Black formatter (line length: 88)
- Type hints required
- PEP 8 compliant

**Rust:**
- Clippy warnings as errors in CI
- Standard rustfmt formatting
- No unsafe code without justification

---

## Submitting Changes

### Before Submitting

1. **Ensure all tests pass:**
   ```bash
   make test
   ```

2. **Lint your code:**
   ```bash
   make lint
   ```

3. **Check cross-language consistency** (if you modified the formula):
   ```bash
   python verify_outputs.py --verbose
   ```

4. **Update documentation** if needed

### Commit Message Guidelines

Use clear, descriptive commit messages:

**Good examples:**
```
Add Fibonacci memoization for performance optimization
Fix subjectivity clamping edge case in Rust implementation
Update documentation for new API methods
```

**Bad examples:**
```
fix bug
update code
wip
```

### Pull Request Process

1. **Push your branch:**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** on GitHub

3. **Fill out the PR template:**
   - Describe what changed
   - Link to relevant issues
   - Add screenshots if UI changes
   - List any breaking changes

4. **Wait for CI checks** to pass (automatic)

5. **Request review** from maintainers

6. **Address feedback** if any

7. **Merge** once approved!

---

## Project Structure

```
pointy-stick/
├── src/
│   ├── javascript/           # TypeScript/JavaScript implementation
│   │   └── universal-axiom.ts
│   ├── python/               # Pure Python implementation
│   │   └── universal_axiom.py
│   ├── rust/                 # Rust implementation
│   │   └── lib.rs
│   └── julia/                # Julia implementation
│       └── UniversalAxiom.jl
│
├── tests/                    # Test suites
│   ├── universal-axiom.test.js
│   ├── test_universal_axiom.py
│   ├── golden_cases.csv      # Golden test data
│   └── canonical_test_cases.json
│
├── examples/                 # Usage examples
│   ├── javascript/
│   ├── python/
│   ├── rust/
│   └── julia/
│
├── mcp-server/              # Model Context Protocol server
│   └── index.ts
│
├── docs/                    # Documentation
│   ├── IMPLEMENTATION.md
│   ├── API_REFERENCE.md
│   └── BENCHMARKS.md
│
├── benchmarks/              # Performance benchmarking
│   ├── benchmark-javascript.js
│   ├── benchmark_python.py
│   └── compare_all.py
│
└── .github/
    └── workflows/
        └── test.yml         # CI/CD pipeline
```

---

## Language-Specific Guidelines

### Adding a Feature

When adding a feature, you must:

1. **Implement it in all languages** (JavaScript, Python, Rust)
2. **Add tests** for each implementation
3. **Update golden test cases** if formula changes
4. **Update API documentation**
5. **Add usage examples** if it's a public API

### Maintaining Parity

The three core implementations must remain mathematically consistent:

- JavaScript: `src/javascript/universal-axiom.ts`
- Python: `src/python/universal_axiom.py`
- Rust: `src/rust/lib.rs`

**Verify parity after changes:**
```bash
python verify_outputs.py --verbose
```

---

## Common Tasks

### Adding a New Method

1. **Define the method** in all three implementations
2. **Add tests** in all three test suites
3. **Update TypeScript types** if needed
4. **Run cross-language verification**

Example workflow:
```bash
# Edit implementations
vim src/javascript/universal-axiom.ts
vim src/python/universal_axiom.py
vim src/rust/lib.rs

# Add tests
vim tests/universal-axiom.test.js
vim tests/test_universal_axiom.py
vim src/rust/lib.rs  # (tests are inline in Rust)

# Verify
make test
python verify_outputs.py --verbose
```

### Running Benchmarks

```bash
make benchmark              # Run all benchmarks
make benchmark-js           # JavaScript only
make benchmark-python       # Python only
make benchmark-rust         # Rust only
make benchmark-compare      # Compare results
```

### Running Examples

```bash
make run-examples           # Run all examples
make example-js             # JavaScript example
make example-python         # Python example
make example-rust           # Rust example
```

---

## Troubleshooting

### Tests Failing After Update

```bash
# Rebuild everything
make clean
make install
make build
make test
```

### TypeScript Errors

```bash
# Clean TypeScript cache
rm -rf dist/
npm run build
```

### Pre-commit Hook Issues

```bash
# Reinstall hooks
rm -rf .husky
npm run prepare
```

### Python Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## Getting Help

- **Documentation:** See `docs/` directory
- **Issues:** Open an issue on GitHub
- **Discussions:** Use GitHub Discussions for questions
- **Philosophy:** Read `CLAUDE.md`, `PROMPT.md`, `SKILL.md`

---

## Code of Conduct

Be respectful, inclusive, and constructive. We're building something meaningful together.

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to The Universal Axiom!** 🌟
