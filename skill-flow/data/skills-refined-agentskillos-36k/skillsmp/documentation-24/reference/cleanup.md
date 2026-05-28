# Cleanup and Finalization

## Remove Temporary Files

### Identify Temporary Files

Common temporary files to remove:
- Build artifacts (`*.o`, `*.obj`, `*.exe`)
- Test outputs
- Temporary scripts created during development
- Cache files
- Log files from development/testing
- Generated documentation (if it can be regenerated)

### Cleanup Script Example

```bash
#!/bin/bash
# cleanup.sh - Remove temporary and build files

echo "Cleaning up temporary files..."

# Remove build artifacts
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

# Remove compiled Python files
find . -type f -name "*.pyc" -delete
find . -type d -name "__pycache__" -delete

# Remove test coverage files
rm -rf htmlcov/
rm -f .coverage
rm -f coverage.xml

# Remove temporary test files
rm -f test_*.tmp
rm -rf /tmp/test_*

# Remove editor temporary files
find . -type f -name "*~" -delete
find . -type f -name "*.swp" -delete
find . -type f -name ".DS_Store" -delete

# Remove log files
rm -f *.log
rm -rf logs/*.log

echo "Cleanup complete!"
```

### CMake Cleanup

```cmake
# Add clean-all target to CMakeLists.txt
add_custom_target(clean-all
    COMMAND ${CMAKE_BUILD_TOOL} clean
    COMMAND ${CMAKE_COMMAND} -E remove_directory ${CMAKE_BINARY_DIR}/CMakeFiles
    COMMAND ${CMAKE_COMMAND} -E remove ${CMAKE_BINARY_DIR}/CMakeCache.txt
    COMMAND ${CMAKE_COMMAND} -E remove ${CMAKE_BINARY_DIR}/cmake_install.cmake
    COMMAND ${CMAKE_COMMAND} -E remove ${CMAKE_BINARY_DIR}/Makefile
    COMMENT "Removing all build files and CMake cache"
)
```

```bash
# Use the target
cmake --build build --target clean-all
```

## .gitignore Management

### Comprehensive .gitignore

Keep build outputs and logs out of version control:

```gitignore
# Build directories
build/
dist/
out/
target/
bin/
obj/

# Compiled files
*.o
*.obj
*.exe
*.dll
*.so
*.dylib
*.a
*.lib

# Language-specific
# C++
*.gch
*.pch

# Python
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
.Python
venv/
env/
.env

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
package-lock.json
yarn.lock

# Kotlin/Java
*.class
*.jar
*.war
.gradle/
gradle-app.setting

# IDE files
.vscode/
.idea/
*.sublime-*
*.swp
*~
.DS_Store

# Test coverage
htmlcov/
.coverage
coverage.xml
*.cover

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp
*.bak
tmp/
temp/

# OS files
Thumbs.db
.DS_Store

# Secrets and credentials
.env
.env.local
secrets.json
credentials.json
*.pem
*.key

# Documentation builds (can be regenerated)
docs/_build/
site/

# Database files (local development)
*.db
*.sqlite
*.sqlite3
```

### Project-Specific Ignore

Add project-specific patterns as needed:

```gitignore
# Example: ignore generated protocol buffers
*.pb.h
*.pb.cc

# Example: ignore downloaded dependencies
third_party/
external/

# Example: ignore large data files
data/*.csv
data/*.parquet
models/*.bin
```

## Code Formatting and Linting

### C++ Formatting

**clang-format**:

```yaml
# .clang-format
---
Language: Cpp
BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 100
PointerAlignment: Left
AccessModifierOffset: -4
AllowShortFunctionsOnASingleLine: Empty
AlwaysBreakTemplateDeclarations: Yes
```

```bash
# Format all C++ files
find src include -name "*.cpp" -o -name "*.h" | xargs clang-format -i

# Check formatting (CI)
find src include -name "*.cpp" -o -name "*.h" | xargs clang-format --dry-run --Werror
```

**clang-tidy** (linting):

```yaml
# .clang-tidy
---
Checks: >
  clang-diagnostic-*,
  clang-analyzer-*,
  cppcoreguidelines-*,
  modernize-*,
  performance-*,
  readability-*,
  -modernize-use-trailing-return-type,
  -readability-magic-numbers
```

```bash
# Run clang-tidy
clang-tidy src/*.cpp -- -Iinclude -std=c++20

# Auto-fix issues
clang-tidy -fix src/*.cpp -- -Iinclude -std=c++20
```

### Kotlin Formatting

**ktlint**:

```bash
# Install ktlint
brew install ktlint

# Check formatting
ktlint

# Auto-format
ktlint -F

# Install git hook
ktlint installGitPreCommitHook
```

```kotlin
// build.gradle.kts
plugins {
    id("org.jlleitschuh.gradle.ktlint") version "11.6.0"
}

ktlint {
    version.set("1.0.0")
    android.set(false)
    outputColorName.set("RED")
}
```

### Python Formatting

**black** (formatter):

```bash
# Format code
black src/ tests/

# Check without modifying
black --check src/ tests/
```

**isort** (import sorting):

```bash
# Sort imports
isort src/ tests/

# Check
isort --check-only src/ tests/
```

```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 100
```

**flake8** (linting):

```bash
# Lint code
flake8 src/ tests/
```

```ini
# .flake8
[flake8]
max-line-length = 100
extend-ignore = E203, W503
exclude = .git,__pycache__,build,dist
```

**mypy** (type checking):

```bash
# Type check
mypy src/
```

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
```

### TypeScript/JavaScript Formatting

**Prettier**:

```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2
}
```

```bash
# Format
npx prettier --write "src/**/*.ts"

# Check
npx prettier --check "src/**/*.ts"
```

**ESLint**:

```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "rules": {
    "no-console": "warn",
    "@typescript-eslint/no-unused-vars": "error"
  }
}
```

```bash
# Lint
npx eslint "src/**/*.ts"

# Auto-fix
npx eslint "src/**/*.ts" --fix
```

## Pre-Commit Hooks

Automate formatting and linting before commits:

```bash
# Install pre-commit
pip install pre-commit

# Create configuration
cat > .pre-commit-config.yaml << 'EOF'
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black

  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/PyCQA/flake8
    rev: 6.1.0
    hooks:
      - id: flake8
EOF

# Install hooks
pre-commit install
```

## Documentation Deviations

### Document Non-Standard Code

When you must deviate from guidelines:

```cpp
// DEVIATION: Using raw pointer instead of unique_ptr here because
// this code interfaces with legacy C library that expects raw pointers.
// TODO: Wrap in RAII class after migrating to new library version 2.0
void* rawPtr = malloc(size);
```

### Migration Plans

Document plans to bring legacy code up to standard:

```markdown
# Legacy Code Migration Plan

## Phase 1: Database Layer (Q1 2026)
- [ ] Replace raw SQL strings with prepared statements
- [ ] Add connection pooling
- [ ] Implement transaction management

## Phase 2: API Layer (Q2 2026)
- [ ] Migrate from callbacks to coroutines
- [ ] Add request validation middleware
- [ ] Implement rate limiting

## Phase 3: Business Logic (Q3 2026)
- [ ] Extract services from monolithic class
- [ ] Add unit tests (target: 80% coverage)
- [ ] Refactor error handling to use Result types
```

### Third-Party Integration Notes

```cpp
/**
 * THIRD-PARTY INTEGRATION: ExternalLibrary v1.2.3
 *
 * Deviations from coding standards:
 * - Uses macro-based error handling (library requirement)
 * - Global state for initialization (library limitation)
 *
 * Migration plan:
 * - Switch to modern alternative library in v2.0
 * - Wrap current usage in facade pattern to isolate deviations
 *
 * Last reviewed: 2025-11-02
 */
```
