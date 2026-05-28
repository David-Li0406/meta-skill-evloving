# Language Detection Algorithms

## Overview

Comprehensive language detection for 8 programming languages using file extensions, manifest files, and content analysis.

## Detection Strategy

### Two-Phase Approach

**Phase 1: Extension-based counting**
- Fast file system scan
- Count files by extension
- Calculate percentages

**Phase 2: Manifest verification**
- Confirm presence via package managers
- Validate against known patterns
- Mark primary language

## Language-Specific Detection

### Python

**File extensions:**
- `.py` - Python source files
- `.pyw` - Python Windows files
- `.pyx` - Cython files
- `.pyi` - Python interface/stub files

**Manifest files:**
- `requirements.txt` - pip dependencies
- `setup.py` - setuptools packaging
- `pyproject.toml` - PEP 518 configuration
- `Pipfile` - Pipenv dependencies
- `poetry.lock` - Poetry lock file
- `setup.cfg` - setup configuration
- `tox.ini` - tox test automation

**Detection script:**
```bash
# Count Python files
PYTHON_COUNT=$(find . -type f \( -name "*.py" -o -name "*.pyw" \) \
  ! -path "*/venv/*" \
  ! -path "*/.venv/*" \
  ! -path "*/site-packages/*" \
  ! -path "*/__pycache__/*" | wc -l)

# Check for Python manifests
PYTHON_MANIFESTS=()
[ -f "requirements.txt" ] && PYTHON_MANIFESTS+=("requirements.txt")
[ -f "setup.py" ] && PYTHON_MANIFESTS+=("setup.py")
[ -f "pyproject.toml" ] && PYTHON_MANIFESTS+=("pyproject.toml")
[ -f "Pipfile" ] && PYTHON_MANIFESTS+=("Pipfile")

# Mark as primary if most files or manifest present
if [ $PYTHON_COUNT -gt 0 ] && [ ${#PYTHON_MANIFESTS[@]} -gt 0 ]; then
  PYTHON_PRIMARY=true
fi
```

**Content-based hints:**
- Shebang: `#!/usr/bin/env python`, `#!/usr/bin/python3`
- Imports: `import `, `from ... import`
- Syntax: `def `, `class `, `if __name__ == "__main__":`

### Rust

**File extensions:**
- `.rs` - Rust source files

**Manifest files:**
- `Cargo.toml` - Package manifest
- `Cargo.lock` - Dependency lock file
- `rust-toolchain.toml` - Toolchain specification
- `build.rs` - Build script

**Detection script:**
```bash
# Count Rust files
RUST_COUNT=$(find . -type f -name "*.rs" \
  ! -path "*/target/*" | wc -l)

# Check for Cargo workspace
if [ -f "Cargo.toml" ]; then
  # Check if workspace or package
  if grep -q '^\[workspace\]' Cargo.toml; then
    RUST_STRUCTURE="workspace"
    # Count workspace members
    MEMBERS=$(grep '^\[workspace.members\]' -A 20 Cargo.toml | grep '"' | wc -l)
  else
    RUST_STRUCTURE="package"
  fi
fi
```

**Key indicators:**
- `src/main.rs` - Binary entry point
- `src/lib.rs` - Library entry point
- `tests/` directory - Integration tests
- Workspace pattern: Multiple Cargo.toml files

### Go

**File extensions:**
- `.go` - Go source files

**Manifest files:**
- `go.mod` - Module definition
- `go.sum` - Dependency checksums
- `go.work` - Workspace file

**Detection script:**
```bash
# Count Go files
GO_COUNT=$(find . -type f -name "*.go" \
  ! -path "*/vendor/*" | wc -l)

# Detect module vs workspace
if [ -f "go.work" ]; then
  GO_STRUCTURE="workspace"
  # Parse workspace modules
  MODULES=$(grep '^use ' go.work | wc -l)
elif [ -f "go.mod" ]; then
  GO_STRUCTURE="module"
  # Extract module path
  MODULE_PATH=$(grep '^module ' go.mod | awk '{print $2}')
fi
```

**Key indicators:**
- `package main` + `func main()` - Executable entry point
- `package <name>` - Library package
- Directory structure mirrors import paths
- `_test.go` suffix for tests

### Julia

**File extensions:**
- `.jl` - Julia source files

**Manifest files:**
- `Project.toml` - Package manifest
- `Manifest.toml` - Dependency lock file
- `JuliaProject.toml` - Alternative naming

**Detection script:**
```bash
# Count Julia files
JULIA_COUNT=$(find . -type f -name "*.jl" | wc -l)

# Check for Julia project
if [ -f "Project.toml" ]; then
  # Extract package name
  JULIA_NAME=$(grep '^name = ' Project.toml | cut -d'"' -f2)
  # Extract UUID
  JULIA_UUID=$(grep '^uuid = ' Project.toml | cut -d'"' -f2)
fi
```

**Key indicators:**
- `src/<Package>.jl` - Main module file
- `test/runtests.jl` - Test entry point
- `using ` and `import ` statements
- Scientific computing libraries (LinearAlgebra, DataFrames)

### Elixir

**File extensions:**
- `.ex` - Elixir source files
- `.exs` - Elixir script files

**Manifest files:**
- `mix.exs` - Mix project configuration
- `mix.lock` - Dependency lock file

**Detection script:**
```bash
# Count Elixir files
ELIXIR_COUNT=$(find . -type f \( -name "*.ex" -o -name "*.exs" \) \
  ! -path "*/deps/*" \
  ! -path "*/_build/*" | wc -l)

# Parse mix.exs for project info
if [ -f "mix.exs" ]; then
  # Extract app name
  ELIXIR_APP=$(grep 'app:' mix.exs | head -1 | cut -d: -f2 | tr -d ', ')
  # Check for umbrella project
  if grep -q 'apps_path:' mix.exs; then
    ELIXIR_STRUCTURE="umbrella"
  else
    ELIXIR_STRUCTURE="application"
  fi
fi
```

**Key indicators:**
- `lib/<app>.ex` - Application entry point
- `lib/<app>/application.ex` - Application supervisor
- `test/` directory with `_test.exs` files
- `defmodule`, `defp`, `def` keywords

### C++

**File extensions:**
- `.cpp`, `.cc`, `.cxx` - C++ source files
- `.h`, `.hpp`, `.hxx` - Header files
- `.c` - C source files (often mixed)

**Build files:**
- `CMakeLists.txt` - CMake build system
- `Makefile` - GNU Make
- `meson.build` - Meson build system
- `configure.ac` - Autotools
- `*.vcxproj` - Visual Studio projects

**Detection script:**
```bash
# Count C++ files
CPP_COUNT=$(find . -type f \( \
  -name "*.cpp" -o -name "*.cc" -o -name "*.cxx" -o \
  -name "*.h" -o -name "*.hpp" -o -name "*.hxx" \) \
  ! -path "*/build/*" \
  ! -path "*/cmake-build-*/*" | wc -l)

# Detect build system
BUILD_SYSTEM=""
[ -f "CMakeLists.txt" ] && BUILD_SYSTEM="cmake"
[ -f "Makefile" ] && BUILD_SYSTEM="${BUILD_SYSTEM:+$BUILD_SYSTEM,}make"
[ -f "meson.build" ] && BUILD_SYSTEM="${BUILD_SYSTEM:+$BUILD_SYSTEM,}meson"
```

**Key indicators:**
- `#include <...>` - Standard library includes
- `namespace`, `class`, `template` - C++ keywords
- `src/` and `include/` directory structure
- `main()` function for executables

### Zig

**File extensions:**
- `.zig` - Zig source files

**Build files:**
- `build.zig` - Build configuration

**Detection script:**
```bash
# Count Zig files
ZIG_COUNT=$(find . -type f -name "*.zig" \
  ! -path "*/zig-cache/*" \
  ! -path "*/zig-out/*" | wc -l)

# Check for build.zig
if [ -f "build.zig" ]; then
  # Extract package name if defined
  ZIG_NAME=$(grep 'const exe = b.addExecutable' build.zig -A 5 | \
    grep '.name' | cut -d'"' -f2)
fi
```

**Key indicators:**
- `pub fn main()` - Entry point
- `const`, `var`, `pub` keywords
- `@import()` statements
- Build artifacts in `zig-out/`

### JavaScript/TypeScript

**File extensions:**
- `.js` - JavaScript
- `.jsx` - React JSX
- `.ts` - TypeScript
- `.tsx` - TypeScript JSX
- `.mjs` - ES Module
- `.cjs` - CommonJS

**Manifest files:**
- `package.json` - npm/yarn/pnpm manifest
- `package-lock.json` - npm lock file
- `yarn.lock` - Yarn lock file
- `pnpm-lock.yaml` - pnpm lock file
- `tsconfig.json` - TypeScript configuration

**Detection script:**
```bash
# Count JavaScript/TypeScript files
JS_COUNT=$(find . -type f \( \
  -name "*.js" -o -name "*.jsx" -o \
  -name "*.ts" -o -name "*.tsx" -o \
  -name "*.mjs" -o -name "*.cjs" \) \
  ! -path "*/node_modules/*" \
  ! -path "*/dist/*" \
  ! -path "*/build/*" \
  ! -path "*/.next/*" | wc -l)

# Detect package manager
PKG_MANAGER=""
[ -f "package-lock.json" ] && PKG_MANAGER="npm"
[ -f "yarn.lock" ] && PKG_MANAGER="yarn"
[ -f "pnpm-lock.yaml" ] && PKG_MANAGER="pnpm"

# Detect framework
FRAMEWORK=""
if [ -f "package.json" ]; then
  grep -q '"react"' package.json && FRAMEWORK="react"
  grep -q '"next"' package.json && FRAMEWORK="next"
  grep -q '"vue"' package.json && FRAMEWORK="vue"
  grep -q '"@angular/core"' package.json && FRAMEWORK="angular"
fi
```

**Key indicators:**
- `import`/`export` - ES modules
- `require()` - CommonJS
- Type annotations in `.ts` files
- JSX syntax in `.jsx`/`.tsx` files

## Primary Language Selection

### Algorithm

Select primary language based on:

1. **File count** - Language with most files
2. **Manifest presence** - Language with package manager config
3. **Directory structure** - Standard patterns (src/, lib/, tests/)
4. **Entry points** - Main executable or library files

### Tie-breaking Rules

When multiple languages have similar file counts:

1. Check for "main" entry point presence
2. Prefer language with more robust manifest (lock file present)
3. Consider total lines of code (if quick to calculate)
4. Default to alphabetical order if truly equal

### Example Logic

```bash
# Calculate scores for each detected language
calculate_score() {
  local lang=$1
  local count=$2
  local has_manifest=$3
  local has_entry=$4

  local score=$count
  [ "$has_manifest" = "true" ] && score=$((score + 100))
  [ "$has_entry" = "true" ] && score=$((score + 50))

  echo $score
}

# Determine primary language
PRIMARY_LANG=""
MAX_SCORE=0

for lang in "${DETECTED_LANGS[@]}"; do
  score=$(calculate_score "$lang" "${counts[$lang]}" \
    "${has_manifest[$lang]}" "${has_entry[$lang]}")
  if [ $score -gt $MAX_SCORE ]; then
    MAX_SCORE=$score
    PRIMARY_LANG=$lang
  fi
done
```

## Performance Optimization

### Ignore Patterns

Exclude common directories to speed up scanning:

```bash
IGNORE_PATTERNS=(
  "*/node_modules/*"
  "*/.git/*"
  "*/venv/*"
  "*/.venv/*"
  "*/__pycache__/*"
  "*/target/*"        # Rust build
  "*/dist/*"
  "*/build/*"
  "*/.next/*"         # Next.js
  "*/.nuxt/*"         # Nuxt.js
  "*/vendor/*"        # Go, PHP
  "*/deps/*"          # Elixir
  "*/_build/*"        # Elixir
  "*/zig-cache/*"     # Zig
  "*/zig-out/*"       # Zig
)
```

### Parallel Detection

Run language detection in parallel:

```bash
# Launch detection in background
detect_python &
detect_rust &
detect_go &
# ... all languages

# Wait for all to complete
wait
```

### Caching

Cache results for unchanged directories:

```bash
# Store checksums of manifest files
CACHE_KEY=$(md5sum Cargo.toml requirements.txt package.json 2>/dev/null | \
  md5sum | cut -d' ' -f1)

# Check cache
if [ -f ".claude/.index-cache/$CACHE_KEY" ]; then
  # Use cached results
  cat ".claude/.index-cache/$CACHE_KEY"
  exit 0
fi
```

## Edge Cases

### Monorepo Detection

Multiple languages with independent roots:

```bash
# Check for workspace markers
[ -f "Cargo.toml" ] && grep -q '^\[workspace\]' Cargo.toml && RUST_WORKSPACE=true
[ -f "go.work" ] && GO_WORKSPACE=true
[ -f "pnpm-workspace.yaml" ] && JS_WORKSPACE=true

# If any workspace detected, mark as monorepo
if [ "$RUST_WORKSPACE" = "true" ] || [ "$GO_WORKSPACE" = "true" ] || \
   [ "$JS_WORKSPACE" = "true" ]; then
  ARCHITECTURE="monorepo"
fi
```

### Mixed C/C++ Projects

Distinguish between C and C++:

```bash
# Count pure C files
C_COUNT=$(find . -type f -name "*.c" ! -path "*/build/*" | wc -l)

# Count C++ specific files
CPP_COUNT=$(find . -type f \( -name "*.cpp" -o -name "*.cc" -o -name "*.cxx" \) \
  ! -path "*/build/*" | wc -l)

# If C++ files present, classify as C++
if [ $CPP_COUNT -gt 0 ]; then
  LANG="C++"
elif [ $C_COUNT -gt 0 ]; then
  LANG="C"
fi
```

### TypeScript vs JavaScript

Prefer TypeScript if tsconfig.json present:

```bash
if [ -f "tsconfig.json" ]; then
  LANG="TypeScript"
else
  LANG="JavaScript"
fi
```

## Testing Detection Algorithms

### Validation Checklist

- [ ] Detects all 8 languages correctly
- [ ] Identifies primary language accurately
- [ ] Handles monorepos with multiple languages
- [ ] Respects ignore patterns
- [ ] Completes within 10 seconds for <1000 files
- [ ] Handles missing manifests gracefully
- [ ] Reports zero-file languages correctly
