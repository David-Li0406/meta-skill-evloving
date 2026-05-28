---
name: The Universal Axiom & Epiphany Engine
description: Multi-language implementation of a mathematical intelligence framework
---

# AGENTS.md

## Role

You are an expert software engineer working on **The Universal Axiom**, a multi-language implementation of a mathematical intelligence framework. Focus on code quality, cross-language consistency, and mathematical correctness.

## Tech Stack

- **Languages**: Python 3.11, TypeScript 5.0/Node.js 20, Rust (latest stable), Julia 1.x
- **Testing**: pytest (Python), Jest (JavaScript/TypeScript), cargo test (Rust)
- **Build**: TypeScript compiler (tsc), cargo build
- **CI/CD**: GitHub Actions (`.github/workflows/test.yml`)
- **License**: MIT

## Project Structure

```
pointy-stick/
├── src/
│   ├── python/           # Python implementation
│   ├── javascript/       # TypeScript/JavaScript implementation
│   ├── rust/            # Rust implementation
│   └── julia/           # Julia implementation
├── tests/               # Cross-language test suites
│   ├── test_universal_axiom.py
│   └── universal-axiom.test.js
├── examples/            # Usage examples per language
│   ├── python/
│   ├── javascript/
│   ├── rust/
│   └── julia/
└── docs/                # Documentation and API reference
```

## Essential Commands

**Build:**
```bash
npm run build              # Compile TypeScript to JavaScript
npm run build:watch        # Watch mode for development
cd src/rust && cargo build --release  # Build Rust (optimized)
```

**Test:**
```bash
npm test                   # Run Jest tests for JavaScript/TypeScript
python -m pytest tests/test_universal_axiom.py -v  # Python tests
cd src/rust && cargo test --verbose    # Rust tests
julia examples/julia/basic_usage.jl    # Julia (manual testing)
```

**Lint:**
```bash
npm run lint               # ESLint for TypeScript files
```

**Examples:**
```bash
npm run example:js         # Run JavaScript example
npm run example:ts         # Run TypeScript example with ts-node
python examples/python/basic_usage.py   # Python example
cd src/rust && cargo run --example basic_usage  # Rust example
```

## Testing Guidelines

### Adding Tests

**Python** (`tests/test_universal_axiom.py`):
- Use pytest conventions
- Test classes inherit from `unittest.TestCase`
- Target: 100% coverage (currently 96%)
- Run with: `python -m pytest tests/test_universal_axiom.py -v --cov`

**JavaScript/TypeScript** (`tests/universal-axiom.test.js`):
- Use Jest with `describe()` and `test()` blocks
- No Jest config needed (uses defaults)
- Currently: 34 tests passing
- Run with: `npx jest tests/universal-axiom.test.js`

**Rust** (`src/rust/tests/`):
- Use built-in Rust test framework with `#[test]` annotations
- Run with: `cargo test --verbose`

**Cross-Language Consistency:**
- Verify identical mathematical outputs across all implementations
- Test the same edge cases in each language
- Maintain feature parity across languages

### CI/CD Pipeline

GitHub Actions runs on:
- `push` to `main` or `claude/**` branches
- `pull_request` to `main`

Three parallel jobs:
1. **Python Tests**: Python 3.11, pytest
2. **JavaScript Tests**: Node.js 20, npm install, tsc build, Jest
3. **Rust Tests**: Latest stable Rust, cargo test

## Code Style

### TypeScript
- **Strict mode enabled** (`tsconfig.json`)
- Target: ES2020
- Output: CommonJS modules to `dist/`
- Always use type annotations for public APIs
- Prefer explicit types over `any`

### Python
- Python 3.11+ features allowed
- Follow PEP 8 conventions
- Type hints encouraged
- Docstrings for all public classes/functions

### Rust
- Follow Rust 2021 edition conventions
- Use `cargo fmt` for formatting
- Use `cargo clippy` for linting
- Comprehensive error handling with `Result<T, E>`

### General Conventions
- **Mathematical correctness first**: The core formula is non-negotiable
- **Cross-language parity**: Same inputs should yield same outputs across languages
- **Descriptive names**: Variable names match the formula notation (A, B, C, X, Y, Z, E_n, F_n)

## Git Workflow

### Branches
- `main` - Stable, production-ready code
- `claude/**` - Claude development branches (auto-run CI)
- Feature branches - Use descriptive names

### Commits
- Clear, descriptive commit messages
- Reference issue numbers when applicable
- Use conventional commit format when possible:
  - `feat:` - New features
  - `fix:` - Bug fixes
  - `test:` - Test additions/changes
  - `docs:` - Documentation updates
  - `refactor:` - Code refactoring

### Pull Requests
- Ensure all tests pass (Python, JavaScript, Rust)
- Verify TypeScript compilation succeeds
- Update relevant documentation
- Maintain cross-language consistency
- Add tests for new functionality

## Boundaries

### ✅ Always Do
- Maintain mathematical correctness of the core formula
- Keep cross-language implementations synchronized
- Add tests for any code changes
- Update documentation when changing public APIs
- Preserve type safety in TypeScript (strict mode)
- Follow existing code structure and conventions

### ⚠️ Ask First
- Adding new mathematical variables or layers
- Changing the core `Intelligence_n` formula
- Modifying the Fibonacci sequence implementation
- Adding new language implementations
- Breaking API changes
- Publishing to package registries (PyPI, npm, crates.io)

### 🚫 Never Do
- Remove or modify the philosophical context in `PROMPT.md` without permission
- Change the MIT license
- Break backward compatibility without major version bump
- Commit dependency lockfiles with security vulnerabilities
- Push directly to `main` (use PRs)
- Modify the core mathematical formula structure
- Remove test coverage
- Change the fundamental meaning of variables (A, B, C, X, Y, Z)

## Critical Files

**Do Not Modify Without Discussion:**
- `PROMPT.md` - Contains the philosophical foundation and creator's vision
- Core formula implementations - Mathematical integrity is paramount
- `LICENSE` - MIT license is intentional

**Frequently Modified:**
- `src/*/` - Implementation code
- `tests/` - Test suites
- `examples/` - Usage examples
- `README.md` - Documentation updates
- `docs/` - API and implementation documentation

## Common Tasks

**Add a new method to UniversalAxiom:**
1. Implement in all languages (Python, TypeScript, Rust, Julia)
2. Add tests in all test suites
3. Update API documentation
4. Verify cross-language consistency
5. Run full test suite before committing

**Fix a bug:**
1. Add a failing test that reproduces the bug
2. Fix the bug in the relevant language(s)
3. Verify the test passes
4. Check if the bug exists in other language implementations
5. Run full test suite

**Add a new example:**
1. Create example file in `examples/<language>/`
2. Ensure it runs without errors
3. Add comments explaining key concepts
4. Update README if it demonstrates important functionality

## Development Setup

**First-time setup:**
```bash
# JavaScript/TypeScript
npm install

# Python
pip install -r requirements.txt

# Rust
cd src/rust
cargo build

# Julia
# Install Julia, then run examples directly
```

**Before committing:**
```bash
npm run build          # Verify TypeScript compiles
npm test              # Run JavaScript tests
python -m pytest tests/test_universal_axiom.py -v  # Run Python tests
cd src/rust && cargo test  # Run Rust tests
```

## Key Implementation Details

**The Core Formula:**
```
Intelligence_n = E_n · (1 + F_n) · X · Y · Z · (A · B · C)
```

**Variables:**
- **A** (Impulses): Fundamental drives, can be positive/negative
- **B** (Elements): Core components, beneficial/detrimental
- **C** (Pressure): Constraints and forces, constructive/destructive
- **X** (Subjectivity): Objectivity measure (7-level scale)
- **Y** (Why Axis): Purpose-driven reasoning
- **Z** (TimeSphere): Temporal continuity
- **E_n**: Exponential growth component
- **F_n**: Fibonacci sequence (natural regulation)

**Layers:**
- Foundation Layer: (A · B · C)
- Dynamic Layer: E_n, F_n
- Cognitive Layer: X, Y, Z

## Reference Documentation

- **README.md** - High-level project overview and philosophy
- **PROMPT.md** - Detailed framework specification and creator's vision
- **TODO.md** - Prioritized task list and roadmap
- **CODEBASE_REVIEW_REPORT.md** - Comprehensive code quality assessment
- **docs/IMPLEMENTATION.md** - Detailed implementation guide
- **docs/api/API_REFERENCE.md** - Complete API documentation

---

**Remember**: This is a mathematical framework with philosophical foundations. Code correctness and cross-language consistency are paramount. When in doubt, verify mathematical properties and test across all implementations.
