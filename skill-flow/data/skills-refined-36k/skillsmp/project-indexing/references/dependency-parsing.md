# Dependency Parsing Techniques

## Overview

Extract dependencies from 8 package managers across multiple languages. Parse manifest files to build comprehensive dependency graphs.

## Package Manager Support

### Python Package Managers

#### requirements.txt (pip)

**Format:** Plain text with package==version syntax

**Parsing strategy:**
```bash
# Basic parsing
grep -v '^#' requirements.txt | # Remove comments
  grep -v '^$' | # Remove empty lines
  cut -d'=' -f1 | # Extract package name before ==
  cut -d'>' -f1 | # Extract before >=
  cut -d'<' -f1 | # Extract before <=
  cut -d'[' -f1 | # Remove extras [dev,test]
  tr -d ' ' # Remove whitespace

# Handle various formats
# package==1.0.0
# package>=1.0.0
# package<2.0.0
# package[extra]==1.0.0
# -e git+https://github.com/user/repo.git@branch#egg=package
```

**Edge cases:**
- Comments: `# This is a comment`
- Blank lines
- Git URLs: `-e git+https://...`
- Extras: `package[dev,test]==1.0.0`
- Platform markers: `package==1.0.0; python_version >= "3.8"`

#### pyproject.toml (Poetry, Flit, PDM)

**Format:** TOML with [tool.poetry.dependencies] section

**Parsing with grep/awk:**
```bash
# Poetry dependencies
sed -n '/^\[tool.poetry.dependencies\]/,/^\[/p' pyproject.toml | \
  grep '=' | \
  grep -v '^\[' | \
  cut -d'=' -f1 | \
  tr -d ' "'

# Example output from:
# [tool.poetry.dependencies]
# python = "^3.8"
# requests = "^2.28.0"
# pandas = {version = "^1.5.0", optional = true}
```

**Parsing with Python (more robust):**
```python
import tomli  # or tomllib in Python 3.11+

with open("pyproject.toml", "rb") as f:
    data = tomli.load(f)

# Poetry dependencies
deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
packages = [k for k in deps.keys() if k != "python"]

# PEP 621 dependencies
pep621_deps = data.get("project", {}).get("dependencies", [])
```

#### Pipfile (Pipenv)

**Format:** TOML with [packages] and [dev-packages] sections

**Parsing:**
```bash
# Production dependencies
sed -n '/^\[packages\]/,/^\[/p' Pipfile | \
  grep '=' | \
  grep -v '^\[' | \
  cut -d'=' -f1 | \
  tr -d ' "'

# Development dependencies
sed -n '/^\[dev-packages\]/,/^\[/p' Pipfile | \
  grep '=' | \
  grep -v '^\[' | \
  cut -d'=' -f1 | \
  tr -d ' "'
```

### Rust Package Manager

#### Cargo.toml

**Format:** TOML with [dependencies], [dev-dependencies], [build-dependencies]

**Parsing dependencies:**
```bash
# Regular dependencies
sed -n '/^\[dependencies\]/,/^\[/p' Cargo.toml | \
  grep '=' | \
  grep -v '^\[' | \
  cut -d'=' -f1 | \
  tr -d ' "'

# Development dependencies
sed -n '/^\[dev-dependencies\]/,/^\[/p' Cargo.toml | \
  grep '=' | \
  grep -v '^\[' | \
  cut -d'=' -f1 | \
  tr -d ' "'

# Build dependencies
sed -n '/^\[build-dependencies\]/,/^\[/p' Cargo.toml | \
  grep '=' | \
  grep -v '^\[' | \
  cut -d'=' -f1 | \
  tr -d ' "'
```

**Handle various dependency formats:**
```toml
# Simple version
serde = "1.0"

# Detailed specification
tokio = { version = "1.35", features = ["full"] }

# Git dependency
my-lib = { git = "https://github.com/user/repo", branch = "main" }

# Path dependency
local-crate = { path = "../local-crate" }

# Workspace dependency
shared = { workspace = true }
```

**Robust parsing with regex:**
```bash
# Extract package names handling all formats
grep -E '^[a-zA-Z0-9_-]+ = ' Cargo.toml | \
  cut -d'=' -f1 | \
  tr -d ' '
```

#### Cargo.lock

**Purpose:** Exact dependency versions for reproducible builds

**Parsing (if needed for version info):**
```bash
# Extract all packages with versions
grep -A 1 '^\[\[package\]\]' Cargo.lock | \
  grep '^name = ' | \
  cut -d'"' -f2
```

### Go Module System

#### go.mod

**Format:** Go module file with require directives

**Parsing direct dependencies:**
```bash
# Simple require statements
grep '^[[:space:]]*require ' go.mod | \
  awk '{print $2}' | \
  cut -d' ' -f1

# Require block
sed -n '/^require (/,/^)/p' go.mod | \
  grep -v 'require (' | \
  grep -v '^)' | \
  awk '{print $1}'
```

**Handle both formats:**
```go
// Single line
require github.com/gin-gonic/gin v1.9.1

// Block format
require (
    github.com/gin-gonic/gin v1.9.1
    github.com/sirupsen/logrus v1.9.3
)
```

**Exclude indirect dependencies:**
```bash
# Only direct dependencies (no // indirect comment)
sed -n '/^require (/,/^)/p' go.mod | \
  grep -v '// indirect' | \
  grep -v 'require (' | \
  grep -v '^)' | \
  awk '{print $1}'
```

### Julia Package Manager

#### Project.toml

**Format:** TOML with [deps] section

**Parsing:**
```bash
# Extract package names
sed -n '/^\[deps\]/,/^\[/p' Project.toml | \
  grep '=' | \
  grep -v '^\[' | \
  cut -d'=' -f1 | \
  tr -d ' "'

# Alternative: just get values (UUIDs)
sed -n '/^\[deps\]/,/^\[/p' Project.toml | \
  grep '=' | \
  grep -v '^\[' | \
  cut -d'=' -f2 | \
  tr -d ' "'
```

**Example:**
```toml
[deps]
DataFrames = "a93c6f00-e57d-5684-b7b6-d8193f3e46c0"
Plots = "91a5bcdd-55d7-5caf-9e0b-520d859cae80"
```

### Elixir Package Manager

#### mix.exs

**Format:** Elixir code with defp deps function

**Parsing (complex due to code format):**
```bash
# Extract dependencies from deps function
sed -n '/defp deps do/,/end/p' mix.exs | \
  grep '{:' | \
  cut -d'{' -f2 | \
  cut -d',' -f1 | \
  tr -d ': '
```

**Example:**
```elixir
defp deps do
  [
    {:phoenix, "~> 1.7.0"},
    {:phoenix_live_view, "~> 0.18.0"},
    {:ecto, "~> 3.10"}
  ]
end
```

**Better: Use Elixir to parse:**
```bash
# If Elixir available
mix deps | grep '*' | awk '{print $2}'
```

### C++ Build Systems

#### CMakeLists.txt

**No standard dependency format** - Various patterns:

**find_package:**
```cmake
find_package(Boost REQUIRED)
find_package(OpenCV REQUIRED)
```

**Parsing:**
```bash
grep 'find_package(' CMakeLists.txt | \
  sed 's/find_package(//' | \
  sed 's/ .*//' | \
  sed 's/)//'
```

**FetchContent:**
```cmake
FetchContent_Declare(
  googletest
  GIT_REPOSITORY https://github.com/google/googletest.git
)
```

**Parsing:**
```bash
grep 'FetchContent_Declare(' CMakeLists.txt -A 3 | \
  grep -v 'FetchContent_Declare' | \
  grep -v 'GIT_REPOSITORY' | \
  grep -v ')' | \
  tr -d ' '
```

### Zig Build System

#### build.zig

**No standard dependency format** - Zig package manager is experimental

**Current pattern (Zig 0.11+):**
```zig
const dep = b.dependency("package-name", .{
    .target = target,
    .optimize = optimize,
});
```

**Parsing:**
```bash
grep 'b.dependency(' build.zig | \
  sed 's/.*b.dependency("//' | \
  cut -d'"' -f1
```

### JavaScript/TypeScript Package Managers

#### package.json (npm/yarn/pnpm)

**Format:** JSON with dependencies and devDependencies

**Parsing with jq:**
```bash
# Production dependencies
jq -r '.dependencies | keys[]' package.json

# Development dependencies
jq -r '.devDependencies | keys[]' package.json

# Peer dependencies
jq -r '.peerDependencies | keys[]' package.json

# Optional dependencies
jq -r '.optionalDependencies | keys[]' package.json

# All dependencies combined
jq -r '.dependencies, .devDependencies, .peerDependencies, .optionalDependencies | keys[]' package.json 2>/dev/null | sort -u
```

**Without jq (grep/cut):**
```bash
# Extract dependency names (fragile, prefers jq)
grep -A 1000 '"dependencies"' package.json | \
  grep -B 1000 '^  }' | \
  grep '"' | \
  cut -d'"' -f2 | \
  grep -v '^dependencies$'
```

## Dependency Classification

### Production vs Development

Classify dependencies by type:

**Production (runtime required):**
- Python: requirements.txt, [tool.poetry.dependencies]
- Rust: [dependencies]
- Go: require (no // indirect)
- Julia: [deps]
- Elixir: deps (non-optional)
- JavaScript: dependencies

**Development (testing/building):**
- Python: requirements-dev.txt, [tool.poetry.dev-dependencies]
- Rust: [dev-dependencies]
- Go: require with // indirect or in tests
- JavaScript: devDependencies

**Build-time:**
- Rust: [build-dependencies]
- C++: find_package for build tools

### Version Constraints

Extract version information when needed:

**Python:**
```bash
# Get package with version
grep -v '^#' requirements.txt | grep '==' | head -5
# Output: requests==2.28.0
```

**Rust:**
```bash
# Get version from Cargo.toml
grep '^serde = ' Cargo.toml
# Output: serde = "1.0.195"
```

**Go:**
```bash
# Versions in go.mod
grep 'github.com/gin-gonic/gin' go.mod
# Output: github.com/gin-gonic/gin v1.9.1
```

## Dependency Counts and Statistics

### Calculate Metrics

**Total dependency count:**
```bash
# Count unique dependencies across all languages
{
  parse_python_deps
  parse_rust_deps
  parse_go_deps
  # ... all languages
} | sort -u | wc -l
```

**Per-language breakdown:**
```json
{
  "dependencies": {
    "Python": {
      "production": 45,
      "development": 12,
      "total": 57
    },
    "Rust": {
      "dependencies": 23,
      "dev_dependencies": 8,
      "build_dependencies": 2,
      "total": 33
    },
    "JavaScript": {
      "dependencies": 18,
      "devDependencies": 25,
      "total": 43
    }
  },
  "total_unique": 133
}
```

## Error Handling

### Missing Manifests

Handle projects without dependency files:

```bash
if [ ! -f "requirements.txt" ] && [ ! -f "pyproject.toml" ]; then
  echo "No Python dependencies found"
  PYTHON_DEPS=0
else
  PYTHON_DEPS=$(parse_python_deps | wc -l)
fi
```

### Malformed Files

Skip and log parse errors:

```bash
parse_cargo_toml() {
  if ! grep -q '^\[dependencies\]' Cargo.toml; then
    echo "Warning: No [dependencies] section in Cargo.toml" >&2
    return 0
  fi

  # Parse with error handling
  sed -n '/^\[dependencies\]/,/^\[/p' Cargo.toml 2>/dev/null || {
    echo "Error parsing Cargo.toml" >&2
    return 1
  }
}
```

### Tool Availability

Check for required tools:

```bash
# Check jq for JSON parsing
if ! command -v jq &>/dev/null; then
  echo "Warning: jq not found, using fallback JSON parsing" >&2
  USE_JQ=false
else
  USE_JQ=true
fi
```

## Performance Optimization

### Parallel Parsing

Parse manifests in parallel:

```bash
# Launch parsers in background
parse_python_deps > /tmp/python_deps &
parse_rust_deps > /tmp/rust_deps &
parse_go_deps > /tmp/go_deps &
parse_js_deps > /tmp/js_deps &

# Wait for completion
wait

# Combine results
cat /tmp/{python,rust,go,js}_deps | sort -u
```

### Caching

Cache dependency lists:

```bash
# Generate cache key from manifest checksums
CACHE_KEY=$(md5sum {requirements.txt,Cargo.toml,go.mod,package.json} 2>/dev/null | \
  md5sum | cut -d' ' -f1)

CACHE_FILE=".claude/.deps-cache/$CACHE_KEY"

if [ -f "$CACHE_FILE" ] && [ $(find "$CACHE_FILE" -mmin -60 2>/dev/null) ]; then
  # Use cache if less than 60 minutes old
  cat "$CACHE_FILE"
  exit 0
fi

# Parse and cache
parse_all_deps | tee "$CACHE_FILE"
```

## Testing Dependency Parsing

### Validation Checklist

- [ ] Parses all 8 language package managers
- [ ] Handles missing manifest files gracefully
- [ ] Correctly extracts package names (no version strings)
- [ ] Distinguishes production vs development deps
- [ ] Handles edge cases (comments, blank lines, complex formats)
- [ ] Completes within 5 seconds for typical projects
- [ ] Produces valid JSON output
- [ ] Reports zero dependencies correctly
