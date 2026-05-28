# Package Manager Specifications and Dependency Resolution

A comprehensive guide to how major package managers handle dependencies, version resolution, lock files, and caching mechanisms.

## Table of Contents

- [Package Manager Comparison Matrix](#package-manager-comparison-matrix)
- [Semantic Versioning (SemVer)](#semantic-versioning-semver)
- [npm/yarn/pnpm (JavaScript/Node.js)](#npmyarnpnpm-javascriptnodejs)
- [pip/poetry (Python)](#pippoetry-python)
- [cargo (Rust)](#cargo-rust)
- [go modules (Go)](#go-modules-go)
- [Maven/Gradle (Java)](#mavengradle-java)
- [Bundler (Ruby)](#bundler-ruby)
- [Composer (PHP)](#composer-php)
- [Best Practices Summary](#best-practices-summary)

---

## Package Manager Comparison Matrix

| Feature | npm/yarn/pnpm | pip/poetry | cargo | go modules | maven/gradle | bundler | composer |
|---------|---------------|------------|-------|------------|--------------|---------|----------|
| **Manifest File** | package.json | requirements.txt, pyproject.toml | Cargo.toml | go.mod | pom.xml, build.gradle | Gemfile | composer.json |
| **Lock File** | package-lock.json, yarn.lock, pnpm-lock.yaml | poetry.lock | Cargo.lock | go.sum | gradle.lockfile (optional) | Gemfile.lock | composer.lock |
| **Lock File Format** | JSON/YAML | TOML | TOML | Text | Text | Text | JSON |
| **Default Version Strategy** | Caret (^) | Caret (^) | Caret (^) | Minimal Version Selection | Range/Latest | Pessimistic (~>) | Caret (^) |
| **Dependency Cache** | ~/.npm, ~/.cache/yarn, ~/.pnpm-store | ~/.cache/pip, ~/.cache/pypoetry | ~/.cargo/registry | $GOPATH/pkg/mod | ~/.m2, ~/.gradle | System gems or vendor/bundle | ~/.composer/cache |
| **Local Install Dir** | node_modules | site-packages (in virtualenv) | target/debug, target/release | N/A (links to cache) | target/, build/ | System or vendor/bundle | vendor/ |
| **Dev Dependencies** | devDependencies | [tool.poetry.dev-dependencies] or groups | [dev-dependencies] | N/A (uses build tags) | <scope>test</scope> | group :development | require-dev |
| **Transitive Handling** | Hoisting/Flattening | Full resolution | Full resolution | Minimal Version Selection | Nearest definition | Full resolution | Full resolution |
| **Deterministic** | Yes (with lock file) | Yes (with lock file) | Yes (with lock file) | Yes | Partial (with lock plugins) | Yes (with lock file) | Yes (with lock file) |

---

## Semantic Versioning (SemVer)

Semantic Versioning is a formal specification for version numbers used by most modern package managers.

### Version Format

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

- **MAJOR**: Increment for incompatible API changes
- **MINOR**: Increment for backwards-compatible functionality additions
- **PATCH**: Increment for backwards-compatible bug fixes
- **PRERELEASE**: Optional pre-release identifier (e.g., `-alpha`, `-beta.1`)
- **BUILD**: Optional build metadata (e.g., `+20130313144700`)

### Examples

```
1.0.0           # First stable release
1.1.0           # Added new feature (backward compatible)
1.1.1           # Bug fix (backward compatible)
2.0.0           # Breaking change
1.0.0-alpha     # Pre-release version
1.0.0-beta.2    # Pre-release with identifier
1.0.0+20130313  # With build metadata
```

### Version Constraint Operators

| Operator | Meaning | Example | Matches |
|----------|---------|---------|---------|
| `^` | Caret (compatible) | `^1.2.3` | `>=1.2.3, <2.0.0` |
| `~` | Tilde (approximately) | `~1.2.3` | `>=1.2.3, <1.3.0` |
| `>=` | Greater than or equal | `>=1.2.3` | `1.2.3` and above |
| `<=` | Less than or equal | `<=1.2.3` | `1.2.3` and below |
| `>` | Greater than | `>1.2.3` | Above `1.2.3` |
| `<` | Less than | `<1.2.3` | Below `1.2.3` |
| `=` or exact | Exact version | `1.2.3` or `=1.2.3` | Only `1.2.3` |
| `*` | Wildcard | `1.2.*` | `1.2.0`, `1.2.1`, etc. |
| `x` | X-range | `1.2.x` | Same as `1.2.*` |

---

## npm/yarn/pnpm (JavaScript/Node.js)

### Manifest File: package.json

The `package.json` file describes your project and its dependencies.

**Example:**

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "description": "My project description",
  "main": "index.js",
  "scripts": {
    "test": "jest",
    "build": "webpack"
  },
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "~4.17.21",
    "axios": "1.4.0"
  },
  "devDependencies": {
    "jest": "^29.5.0",
    "webpack": "^5.88.0"
  },
  "peerDependencies": {
    "react": "^18.0.0"
  },
  "optionalDependencies": {
    "fsevents": "^2.3.2"
  },
  "engines": {
    "node": ">=16.0.0"
  }
}
```

### Dependency Types

1. **dependencies**: Required for production runtime
2. **devDependencies**: Only needed during development (testing, building, linting)
3. **peerDependencies**: Expected to be provided by the consuming project (e.g., plugins)
4. **optionalDependencies**: Nice to have but installation can fail without breaking the build
5. **bundledDependencies**: Dependencies to bundle with your package

### Lock Files

#### package-lock.json (npm)

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "my-project",
      "version": "1.0.0",
      "dependencies": {
        "express": "^4.18.2"
      }
    },
    "node_modules/express": {
      "version": "4.18.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
      "integrity": "sha512-5/PsL6iGPdfQ/lKM1UuielYgv3BUoJfz1aUwU9vHZ+J7gyvwdQXFEBIEIaxeGf0GIcreATNyBExtalisDbuMqQ==",
      "dependencies": {
        "accepts": "~1.3.8",
        "body-parser": "1.20.1"
      },
      "engines": {
        "node": ">= 0.10.0"
      }
    }
  }
}
```

#### yarn.lock (Yarn)

```yaml
# THIS IS AN AUTOGENERATED FILE. DO NOT EDIT THIS FILE DIRECTLY.
# yarn lockfile v1

express@^4.18.2:
  version "4.18.2"
  resolved "https://registry.yarnpkg.com/express/-/express-4.18.2.tgz#3fabe08296e930c796c19e3c516979386ba9fd59"
  integrity sha512-5/PsL6iGPdfQ/lKM1UuielYgv3BUoJfz1aUwU9vHZ+J7gyvwdQXFEBIEIaxeGf0GIcreATNyBExtalisDbuMqQ==
  dependencies:
    accepts "~1.3.8"
    body-parser "1.20.1"
```

#### pnpm-lock.yaml (pnpm)

```yaml
lockfileVersion: '6.0'

settings:
  autoInstallPeers: true
  excludeLinksFromLockfile: false

dependencies:
  express:
    specifier: ^4.18.2
    version: 4.18.2

packages:
  /express@4.18.2:
    resolution: {integrity: sha512-5/PsL6iGPdfQ/lKM1UuielYgv3BUoJfz1aUwU9vHZ+J7gyvwdQXFEBIEIaxeGf0GIcreATNyBExtalisDbuMqQ==}
    engines: {node: '>= 0.10.0'}
    dependencies:
      accepts: 1.3.8
      body-parser: 1.20.1
    dev: false
```

### Version Range Specifications

#### Caret (^) - Default

Allows changes that do not modify the left-most non-zero digit.

```
^1.2.3  → >=1.2.3 <2.0.0   (any 1.x.x >= 1.2.3)
^0.2.3  → >=0.2.3 <0.3.0   (only 0.2.x >= 0.2.3)
^0.0.3  → >=0.0.3 <0.0.4   (only 0.0.3)
^1.2    → >=1.2.0 <2.0.0
^1      → >=1.0.0 <2.0.0
```

#### Tilde (~)

Allows patch-level changes if minor version is specified.

```
~1.2.3  → >=1.2.3 <1.3.0   (any 1.2.x >= 1.2.3)
~1.2    → >=1.2.0 <1.3.0   (any 1.2.x)
~1      → >=1.0.0 <2.0.0   (any 1.x.x)
```

#### Exact

```
1.2.3   → exactly 1.2.3
```

### Dependency Resolution Algorithm

npm uses a sophisticated algorithm that has evolved over time:

1. **npm v1-v2**: Nested installation - every dependency gets its own `node_modules` folder
2. **npm v3+**: Flattened/hoisted structure - dependencies are hoisted to the top-level `node_modules` when possible
3. **npm v7+**: Automatic peerDependencies installation

**Resolution Process:**

1. Read `package.json` to determine dependency requirements
2. If `package-lock.json` exists, use it to determine exact versions
3. Otherwise, resolve dependencies by fetching latest compatible versions
4. Build dependency tree with deduplication/hoisting
5. Download packages from registry
6. Extract to `node_modules`
7. Update/create `package-lock.json`

**Hoisting Example:**

```
Before Hoisting (npm v1-v2):
node_modules/
├── A/
│   └── node_modules/
│       └── C@1.0.0/
└── B/
    └── node_modules/
        └── C@1.0.0/

After Hoisting (npm v3+):
node_modules/
├── A/
├── B/
└── C@1.0.0/    # Hoisted to top level (deduplicated)
```

**Conflict Resolution:**

```
When versions conflict:
node_modules/
├── A/
├── B/
├── C@1.0.0/           # Hoisted (first encountered)
└── D/
    └── node_modules/
        └── C@2.0.0/   # Nested (incompatible with hoisted version)
```

### node_modules Structure

#### npm/Yarn (Flat Structure)

```
node_modules/
├── .bin/                    # Executable scripts
├── express/                 # Direct dependency
│   ├── package.json
│   ├── index.js
│   └── node_modules/       # Nested if version conflicts
│       └── debug@2.x/
├── debug@4.x/              # Hoisted transitive dependency
├── lodash/                  # Direct dependency
└── ...
```

#### pnpm (Symlinked Structure)

pnpm uses a unique content-addressable storage approach:

```
node_modules/
├── .pnpm/                           # Virtual store
│   ├── express@4.18.2/
│   │   └── node_modules/
│   │       ├── express/            # Hard link to store
│   │       ├── accepts/            # Hard link to store
│   │       └── body-parser/        # Hard link to store
│   └── ...
├── express/                         # Symlink → .pnpm/express@4.18.2/node_modules/express
└── lodash/                          # Symlink → .pnpm/lodash@4.17.21/node_modules/lodash
```

**Benefits:**
- Saves disk space (single copy per version across all projects)
- Prevents phantom dependencies (can't import unlisted dependencies)
- Faster installation

### Cache Locations

- **npm**: `~/.npm` (Linux/macOS), `%AppData%/npm-cache` (Windows)
- **Yarn v1**: `~/.cache/yarn` (Linux/macOS), `%LocalAppData%/Yarn/Cache` (Windows)
- **Yarn v2+ (Berry)**: `.yarn/cache` (project-local by default)
- **pnpm**: `~/.pnpm-store` (Linux/macOS), `%LocalAppData%/pnpm/store` (Windows)

### Installing Without Dev Dependencies

```bash
# npm
npm install --omit=dev
npm install --production     # Older syntax
npm ci --omit=dev           # For CI environments

# Yarn
yarn install --production

# pnpm
pnpm install --prod
```

### Transitive Dependency Handling

**Automatic Resolution:**
- npm automatically resolves transitive dependencies
- Uses hoisting to deduplicate when possible
- Handles version conflicts by nesting

**Deduplication:**

```bash
# Manually deduplicate dependencies
npm dedupe

# Yarn doesn't need manual deduplication (automatic)

# pnpm uses unique storage (no duplication)
```

**Overriding Transitive Dependencies (npm v8.3+):**

```json
{
  "overrides": {
    "foo": "1.0.0",
    "bar@2.0.0": {
      "baz": "1.1.0"
    }
  }
}
```

**Yarn Resolutions:**

```json
{
  "resolutions": {
    "package-a": "2.0.0",
    "package-b/**/package-c": "3.0.0"
  }
}
```

---

## pip/poetry (Python)

### Manifest Files

#### requirements.txt (pip)

Simple text file listing dependencies:

```txt
# Production dependencies
Django>=4.2,<5.0
requests==2.31.0
numpy~=1.24.0
pandas>=2.0.0

# With extras
celery[redis]>=5.3.0

# From git
git+https://github.com/user/repo.git@v1.0.0#egg=package-name

# With hashes for security
certifi==2023.5.7 \
    --hash=sha256:0f0d56dc5a6ad56fd4ba36484d6cc34451e1c6548c61daad8c320169f91eddc7

# Development dependencies (typically in requirements-dev.txt)
pytest>=7.4.0
black==23.7.0
```

#### pyproject.toml (Poetry / PEP 621)

Modern Python project configuration:

```toml
[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[project]
name = "my-project"
version = "1.0.0"
description = "My project description"
requires-python = ">=3.9"
dependencies = [
    "django>=4.2,<5.0",
    "requests==2.31.0",
]

[project.optional-dependencies]
dev = ["pytest>=7.4.0", "black==23.7.0"]
test = ["pytest>=7.4.0", "pytest-cov>=4.1.0"]

[tool.poetry]
# Poetry-specific configuration
name = "my-project"
version = "1.0.0"

[tool.poetry.dependencies]
python = "^3.9"
django = "^4.2"
requests = "^2.31.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
black = "^23.7.0"

[tool.poetry.group.test.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
```

### Lock File: poetry.lock

```toml
# This file is automatically @generated by Poetry 1.7.0 and should not be changed by hand.

[[package]]
name = "django"
version = "4.2.5"
description = "A high-level Python web framework"
optional = false
python-versions = ">=3.8"
files = [
    {file = "Django-4.2.5-py3-none-any.whl", hash = "sha256:..."},
    {file = "Django-4.2.5.tar.gz", hash = "sha256:..."},
]

[package.dependencies]
asgiref = ">=3.6.0,<4"
sqlparse = ">=0.3.1"
tzdata = {version = "*", markers = "sys_platform == \"win32\""}

[package.extras]
argon2 = ["argon2-cffi (>=19.1.0)"]
bcrypt = ["bcrypt"]

[[package]]
name = "requests"
version = "2.31.0"
description = "Python HTTP for Humans."
optional = false
python-versions = ">=3.7"
files = [
    {file = "requests-2.31.0-py3-none-any.whl", hash = "sha256:..."},
    {file = "requests-2.31.0.tar.gz", hash = "sha256:..."},
]

[metadata]
lock-version = "2.0"
python-versions = "^3.9"
content-hash = "abc123..."
```

### Version Constraint Specifications

Poetry supports PEP 440 version specifiers with additional syntax:

#### Caret (^)

```
^1.2.3  → >=1.2.3 <2.0.0
^0.2.3  → >=0.2.3 <0.3.0
^0.0.3  → >=0.0.3 <0.0.4
^1.2    → >=1.2.0 <2.0.0
```

#### Tilde (~)

```
~1.2.3  → >=1.2.3 <1.3.0
~1.2    → >=1.2.0 <1.3.0
~1      → >=1.0.0 <2.0.0
```

#### Wildcard (*)

```
*       → >=0.0.0 (any version)
1.*     → >=1.0.0 <2.0.0
1.2.*   → >=1.2.0 <1.3.0
```

#### Inequality

```
>=1.2.3
>1.2.3
<=1.2.3
<1.2.3
>=1.2,<1.5
```

#### Exact

```
1.2.3
==1.2.3
```

### Dependency Resolution Algorithm

**pip (Classic):**
1. Reads requirements from `requirements.txt`
2. Fetches package metadata from PyPI
3. Downloads and installs packages one by one
4. No automatic conflict resolution (may install incompatible versions)

**pip (Modern with resolver):**
1. Builds complete dependency graph
2. Attempts to find compatible versions for all dependencies
3. Backtracks if conflicts are found
4. May fail if no valid solution exists

**Poetry:**
1. Reads `pyproject.toml` and `poetry.lock` (if exists)
2. Builds dependency graph with all constraints
3. Uses SAT solver to find optimal version set
4. Ensures all dependencies are compatible
5. Writes solution to `poetry.lock`
6. Installs packages

### Package Storage Locations

#### pip with virtualenv

```
my-project/
├── venv/                        # Virtual environment
│   ├── bin/                    # Executables (Linux/macOS)
│   ├── Scripts/                # Executables (Windows)
│   ├── lib/
│   │   └── python3.9/
│   │       └── site-packages/  # Installed packages
│   └── pyvenv.cfg
└── requirements.txt
```

#### Poetry

**Virtual Environment:**
- Default: `{cache-dir}/virtualenvs/`
  - Linux: `~/.cache/pypoetry/virtualenvs/`
  - macOS: `~/Library/Caches/pypoetry/virtualenvs/`
  - Windows: `C:\Users\<user>\AppData\Local\pypoetry\Cache\virtualenvs\`
- With `virtualenvs.in-project = true`: `.venv/` in project root

**Cache:**
- Linux: `~/.cache/pypoetry/`
- macOS: `~/Library/Caches/pypoetry/`
- Windows: `C:\Users\<user>\AppData\Local\pypoetry\Cache\`

**Find current environment:**

```bash
poetry env info --path
```

### Installing Without Dev Dependencies

```bash
# pip (requires separate requirements file)
pip install -r requirements.txt  # Production only
pip install -r requirements-dev.txt  # Development

# Poetry (modern - with groups)
poetry install --without dev
poetry install --without dev,test
poetry install --only main

# Poetry (legacy)
poetry install --no-dev
```

### Transitive Dependency Handling

**pip:**
- Automatically installs transitive dependencies
- Limited conflict resolution (legacy resolver)
- Use `pip-tools` for better dependency pinning:

```bash
# requirements.in
django>=4.2

# Generate locked requirements
pip-compile requirements.in
# Creates requirements.txt with all transitive dependencies pinned
```

**Poetry:**
- Full transitive dependency resolution
- Guarantees compatible versions across all dependencies
- All transitive dependencies recorded in `poetry.lock`

---

## cargo (Rust)

### Manifest File: Cargo.toml

```toml
[package]
name = "my-project"
version = "0.1.0"
edition = "2021"
authors = ["Your Name <you@example.com>"]
license = "MIT"
description = "My Rust project"

[dependencies]
serde = "1.0"                      # Caret by default: ^1.0
tokio = { version = "1.32", features = ["full"] }
regex = "~1.9"                     # Tilde: ~1.9
rand = "0.8.5"                     # Exact: =0.8.5 (if specified)

# Git dependencies
my-lib = { git = "https://github.com/user/repo", branch = "main" }

# Path dependencies
utils = { path = "../utils" }

# Optional dependencies
log = { version = "0.4", optional = true }

[dev-dependencies]
proptest = "1.2"
criterion = "0.5"

[build-dependencies]
cc = "1.0"

[features]
default = ["logging"]
logging = ["log"]
```

### Lock File: Cargo.lock

```toml
# This file is automatically @generated by Cargo.
# It is not intended for manual editing.
version = 3

[[package]]
name = "my-project"
version = "0.1.0"
dependencies = [
 "serde",
 "tokio",
]

[[package]]
name = "serde"
version = "1.0.188"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "cf9e0fcba69a370eed61bcf2b728575f726b50b55cba78064753d708ddc7549e"
dependencies = [
 "serde_derive",
]

[[package]]
name = "serde_derive"
version = "1.0.188"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "4eca7ac642d82aa35b60049a6eccb4be6be75e599bd2e9adb5f875a737654af2"
dependencies = [
 "proc-macro2",
 "quote",
 "syn",
]

[[package]]
name = "tokio"
version = "1.32.0"
source = "registry+https://github.com/rust-lang/crates.io-index"
checksum = "17ed6077ed6cd6c74735e21f37eb16dc3935f96878b1fe961074089cc80893f9"
```

### Version Requirement Specifications

#### Caret (Default)

```
^1.2.3  → >=1.2.3, <2.0.0
^1.2    → >=1.2.0, <2.0.0
^1      → >=1.0.0, <2.0.0
^0.2.3  → >=0.2.3, <0.3.0
^0.0.3  → >=0.0.3, <0.0.4
^0.0    → >=0.0.0, <0.1.0
^0      → >=0.0.0, <1.0.0
```

**In Cargo.toml, these are equivalent:**

```toml
[dependencies]
serde = "1.0"
serde = "^1.0"
```

#### Tilde

```
~1.2.3  → >=1.2.3, <1.3.0
~1.2    → >=1.2.0, <1.3.0
~1      → >=1.0.0, <2.0.0
```

#### Wildcard

```
*       → >=0.0.0
1.*     → >=1.0.0, <2.0.0
1.2.*   → >=1.2.0, <1.3.0
```

#### Comparison Operators

```
>= 1.2.3
> 1.2.3
<= 1.2.3
< 1.2.3
= 1.2.3     # Exact version
>= 1.2, < 1.5
```

### Dependency Resolution Algorithm

Cargo uses a sophisticated resolver with multiple versions:

**Resolver Version 2 (Default for Edition 2021+):**

1. Read `Cargo.toml` to determine dependency requirements
2. If `Cargo.lock` exists and is compatible, use it
3. Otherwise, build dependency graph for entire workspace
4. Apply minimal version selection (prefers semantically highest)
5. Handle feature unification
6. Resolve conflicts and platform-specific dependencies
7. Write `Cargo.lock`

**Key Properties:**
- **Deterministic**: Same `Cargo.toml` always produces same `Cargo.lock`
- **Minimal Version Selection**: Unlike npm, Cargo prefers highest compatible version
- **Feature Unification**: Features enabled by any dependency are enabled for all

**Cargo.toml vs Cargo.lock:**

From the official Cargo Book:
> - **Cargo.toml** is about describing your dependencies in a broad sense, and is written by you.
> - **Cargo.lock** contains exact information about your dependencies. It is maintained by Cargo and should not be manually edited.

### Package Storage Locations

**Registry Cache:**
```
~/.cargo/
├── registry/
│   ├── index/                    # Registry index (git repos)
│   ├── cache/                    # Downloaded .crate files
│   └── src/                      # Extracted source code
├── git/                          # Git dependencies
│   ├── db/                       # Bare repos
│   └── checkouts/                # Checked out sources
└── bin/                          # Installed binaries
```

**Build Artifacts:**
```
my-project/
└── target/
    ├── debug/                    # Debug builds
    │   ├── deps/                # Compiled dependencies
    │   ├── build/               # Build script outputs
    │   └── my-project           # Your binary
    └── release/                  # Release builds
        └── ...
```

**Environment Variables:**
- `CARGO_HOME`: Override cargo home (default: `~/.cargo`)
- `CARGO_TARGET_DIR`: Override target directory

### Installing Without Dev Dependencies

```bash
# Build/install without dev-dependencies
cargo build
cargo build --release

# Dev dependencies are only built when:
cargo test      # Running tests
cargo bench     # Running benchmarks

# For dependencies in workspace, exclude dev deps:
cargo install --path . --locked
```

### Transitive Dependency Handling

**Automatic Resolution:**
- Cargo automatically resolves transitive dependencies
- All transitive dependencies appear in `Cargo.lock`
- Version resolution considers entire dependency graph

**Feature Propagation:**

```toml
# If crate A depends on crate B with features
[dependencies]
serde = { version = "1.0", features = ["derive"] }

# And crate C also depends on serde
[dependencies]
serde = "1.0"

# Cargo will use serde with "derive" feature for both
# (features are unified across the dependency graph)
```

**Overriding Dependencies:**

```toml
[patch.crates-io]
serde = { path = "../my-serde" }

# Or from git
[patch.crates-io]
serde = { git = "https://github.com/user/serde" }
```

---

## go modules (Go)

### Manifest File: go.mod

```go
module github.com/user/myproject

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1
    github.com/lib/pq v1.10.9
    golang.org/x/sync v0.3.0
)

require (
    // Indirect dependencies (transitive)
    github.com/bytedance/sonic v1.9.1 // indirect
    github.com/gin-contrib/sse v0.1.0 // indirect
    github.com/go-playground/validator/v10 v10.14.0 // indirect
)

// Replace directive for local development or forks
replace github.com/some/dependency => ../local-dependency

// Exclude specific versions
exclude github.com/some/package v1.2.3

// Retract your own published versions
retract v1.0.0 // Published accidentally
```

### Lock File: go.sum

```
github.com/gin-gonic/gin v1.9.1 h1:4idEAncQnU5cB7BeOkPtxjfCSye0AAm1R0RVIqJ+Jmg=
github.com/gin-gonic/gin v1.9.1/go.mod h1:hPrL7YrpYKXt5YId3A/Tnip5kqbEAP+KLuI3SUcPTeU=
github.com/lib/pq v1.10.9 h1:YXG7RB+JIjhP29X+OtkiDnYaXQwpS4JEWq7dtCCRUEw=
github.com/lib/pq v1.10.9/go.mod h1:AlVN5x4E4T544tWzH6hKfbfQvm3HdbOxrmggDNAPY9o=
golang.org/x/sync v0.3.0 h1:ftCYgMx6zT/asHUrPw8BLLscYtGznsLAnjq5RH9P66E=
golang.org/x/sync v0.3.0/go.mod h1:FU7BRWz2tNW+3quACPkgCx/L+uEAv1htQ0V83Z9Rj+Y=
```

**Format:**
Each line contains:
- Module path
- Version
- Hash algorithm and checksum (`h1:` prefix)

### Version Specification

Go modules use semantic versioning with some special conventions:

#### Semantic Import Versioning

```
v0.x.x          # Initial development
v1.x.x          # Stable API
v2.x.x          # Breaking changes require new import path
```

#### Major Version Suffixes

```go
// For v0 and v1
import "github.com/user/repo"

// For v2+, path must include major version
import "github.com/user/repo/v2"
import "github.com/user/repo/v3"
```

#### Pseudo-Versions

For commits without tags:

```
v0.0.0-20230821120329-abcd1234abcd
```

Format: `v0.0.0-timestamp-commithash`

#### Version Queries

```bash
go get github.com/user/repo@latest      # Latest version
go get github.com/user/repo@v1.2.3      # Specific version
go get github.com/user/repo@v1.2        # Latest patch of v1.2
go get github.com/user/repo@commit      # Specific commit
go get github.com/user/repo@branch      # Latest on branch
go get github.com/user/repo@upgrade     # Upgrade to latest
go get github.com/user/repo@patch       # Latest patch
```

### Dependency Resolution Algorithm: Minimal Version Selection (MVS)

Go uses a unique algorithm called **Minimal Version Selection**:

**Key Principle:**
> For each module, use the minimum (oldest) version that satisfies all requirements.

**Example:**

```
Main module requires: A v1.2, B v1.1
A v1.2 requires: D v1.0
B v1.1 requires: D v1.1

Result: D v1.1 is selected (minimum that satisfies both A and B)
```

**Benefits:**
- Highly predictable
- Reproducible builds
- No SAT solver needed
- Favor stability over latest versions

**Comparison with npm:**

| npm | Go modules |
|-----|------------|
| Prefer latest compatible version | Prefer minimum compatible version |
| Complex resolution with backtracking | Simple, deterministic MVS |
| May surprise with newer versions | Conservative, predictable |

### Module Cache Location

**GOMODCACHE:**
- Default: `$GOPATH/pkg/mod`
- If `$GOPATH` not set: `$HOME/go/pkg/mod` (Linux/macOS) or `%USERPROFILE%\go\pkg\mod` (Windows)
- Override with `GOMODCACHE` environment variable

**Structure:**

```
$GOPATH/pkg/mod/
├── cache/
│   └── download/                # Downloaded module files
│       └── github.com/
│           └── user/
│               └── repo/
│                   └── @v/
│                       ├── v1.2.3.zip
│                       ├── v1.2.3.mod
│                       └── v1.2.3.info
└── github.com/
    └── user/
        └── repo@v1.2.3/        # Extracted module source
```

**Clean Cache:**

```bash
go clean -modcache
```

### Module Graph Pruning (Go 1.17+)

For projects with `go 1.17` or higher:

- Only includes immediate dependencies of each module
- Transitive dependencies of dependencies are pruned
- Significantly reduces go.mod size in large projects
- Improves performance

### Installing Without Test Dependencies

Go doesn't have a concept of "dev dependencies". Instead:

```bash
# Build only (no test dependencies compiled)
go build

# Test (includes test dependencies)
go test

# Vendoring (includes only production dependencies)
go mod vendor
```

**Using Build Tags:**

```go
//go:build tools
// +build tools

package tools

import (
    _ "golang.org/x/tools/cmd/goimports"
    _ "github.com/golangci/golangci-lint/cmd/golangci-lint"
)
```

### Transitive Dependency Handling

**Automatic Resolution:**
- All transitive dependencies automatically added to `go.mod`
- Marked as `// indirect`
- All checksums recorded in `go.sum`

**Tidying:**

```bash
# Remove unused dependencies
go mod tidy

# Verify dependencies
go mod verify

# View dependency graph
go mod graph
```

**Example go.mod with indirect dependencies:**

```go
module myapp

go 1.21

require (
    github.com/gin-gonic/gin v1.9.1  // direct
)

require (
    github.com/bytedance/sonic v1.9.1 // indirect
    github.com/gin-contrib/sse v0.1.0 // indirect
)
```

---

## Maven/Gradle (Java)

### Maven

#### Manifest File: pom.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
                             http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>com.example</groupId>
    <artifactId>my-app</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>

    <properties>
        <maven.compiler.source>17</maven.compiler.source>
        <maven.compiler.target>17</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <!-- Production dependency -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>3.1.5</version>
        </dependency>

        <!-- With exclusions -->
        <dependency>
            <groupId>com.example</groupId>
            <artifactId>some-lib</artifactId>
            <version>2.0.0</version>
            <exclusions>
                <exclusion>
                    <groupId>log4j</groupId>
                    <artifactId>log4j</artifactId>
                </exclusion>
            </exclusions>
        </dependency>

        <!-- Test dependency -->
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.10.0</version>
            <scope>test</scope>
        </dependency>

        <!-- Optional dependency -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <version>42.6.0</version>
            <optional>true</optional>
        </dependency>
    </dependencies>

    <dependencyManagement>
        <!-- Lock versions for transitive dependencies -->
        <dependencies>
            <dependency>
                <groupId>com.fasterxml.jackson.core</groupId>
                <artifactId>jackson-core</artifactId>
                <version>2.15.3</version>
            </dependency>
        </dependencies>
    </dependencyManagement>
</project>
```

#### Lock File Support

Maven **does not** natively support lock files. However:

**Third-party solutions:**

1. **maven-lockfile plugin:**

```xml
<plugin>
    <groupId>io.github.chains-project</groupId>
    <artifactId>maven-lockfile</artifactId>
    <version>4.2.0</version>
</plugin>
```

Generates `lockfile.json`:

```json
{
  "groupId": "com.example",
  "artifactId": "my-app",
  "version": "1.0.0",
  "dependencies": {
    "org.springframework.boot:spring-boot-starter-web:jar": {
      "version": "3.1.5",
      "dependencies": {
        "org.springframework.boot:spring-boot-starter:jar": "3.1.5",
        "org.springframework.boot:spring-boot-starter-json:jar": "3.1.5"
      }
    }
  }
}
```

2. **dependencyManagement section:**

Manually specify all transitive dependency versions.

#### Version Specification

Maven uses version ranges and single versions:

```xml
<!-- Exact version -->
<version>1.2.3</version>

<!-- Soft requirement (recommendation) -->
<version>1.2</version>

<!-- Version ranges -->
<version>[1.0,2.0)</version>      <!-- 1.0 <= x < 2.0 -->
<version>[1.0,2.0]</version>      <!-- 1.0 <= x <= 2.0 -->
<version>(1.0,2.0)</version>      <!-- 1.0 < x < 2.0 -->
<version>[1.5,)</version>         <!-- x >= 1.5 -->
<version>(,1.0]</version>         <!-- x <= 1.0 -->

<!-- Multiple ranges -->
<version>(,1.0],[1.2,)</version>  <!-- x <= 1.0 or x >= 1.2 -->
```

**SNAPSHOT versions:**

```xml
<version>1.0-SNAPSHOT</version>   <!-- Development version -->
```

### Gradle

#### Build File: build.gradle (Groovy)

```groovy
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.1.5'
}

group = 'com.example'
version = '1.0.0'
sourceCompatibility = '17'

repositories {
    mavenCentral()
}

dependencies {
    // Production dependencies
    implementation 'org.springframework.boot:spring-boot-starter-web:3.1.5'
    implementation 'com.google.guava:guava:32.1.2-jre'

    // Runtime only
    runtimeOnly 'org.postgresql:postgresql:42.6.0'

    // Compile only (not in runtime classpath)
    compileOnly 'org.projectlombok:lombok:1.18.30'
    annotationProcessor 'org.projectlombok:lombok:1.18.30'

    // Test dependencies
    testImplementation 'org.junit.jupiter:junit-jupiter:5.10.0'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'

    // Exclude transitive dependency
    implementation('com.example:some-lib:2.0.0') {
        exclude group: 'log4j', module: 'log4j'
    }
}

// Force specific versions
configurations.all {
    resolutionStrategy {
        force 'com.google.guava:guava:32.1.2-jre'
        failOnVersionConflict()
    }
}
```

#### build.gradle.kts (Kotlin DSL)

```kotlin
plugins {
    java
    id("org.springframework.boot") version "3.1.5"
}

group = "com.example"
version = "1.0.0"

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web:3.1.5")
    implementation("com.google.guava:guava:32.1.2-jre")

    testImplementation("org.junit.jupiter:junit-jupiter:5.10.0")
}
```

#### Lock File: gradle.lockfile

Enable dependency locking:

```groovy
dependencyLocking {
    lockAllConfigurations()
}
```

Run to create lock files:

```bash
gradle dependencies --write-locks
```

Generates `gradle.lockfile`:

```
# This is a Gradle generated file for dependency locking.
# Manual edits can break the build and are not advised.
# This file is expected to be part of source control.

com.fasterxml.jackson.core:jackson-annotations:2.15.3=compileClasspath,runtimeClasspath
com.fasterxml.jackson.core:jackson-core:2.15.3=compileClasspath,runtimeClasspath
com.fasterxml.jackson.core:jackson-databind:2.15.3=compileClasspath,runtimeClasspath
org.springframework.boot:spring-boot-starter-web:3.1.5=compileClasspath,runtimeClasspath
```

### Dependency Scopes

**Maven Scopes:**

| Scope | Available | Transitive | Description |
|-------|-----------|------------|-------------|
| `compile` | All classpath | Yes | Default, available everywhere |
| `provided` | Compile/Test | No | Provided by runtime (e.g., servlet API) |
| `runtime` | Runtime/Test | Yes | Not needed for compilation |
| `test` | Test only | No | Only for testing |
| `system` | All classpath | No | From local filesystem (discouraged) |
| `import` | N/A | N/A | Import dependencyManagement from POM |

**Gradle Configurations:**

| Configuration | Available | Transitive | Description |
|--------------|-----------|------------|-------------|
| `implementation` | Runtime + Test | Yes (hidden from consumers) | Main dependencies |
| `api` | Runtime + Test | Yes (exposed to consumers) | Public API dependencies |
| `compileOnly` | Compile only | No | Compile-time only (e.g., annotations) |
| `runtimeOnly` | Runtime + Test | Yes | Runtime only |
| `testImplementation` | Test only | Yes (within test) | Test dependencies |
| `testCompileOnly` | Test compile | No | Test compile-time only |
| `testRuntimeOnly` | Test runtime | Yes | Test runtime only |

### Dependency Resolution

**Maven: Nearest Definition**

Maven uses "nearest wins" strategy:

```
A → B → C → D 2.0    (depth 3)
A → E → D 1.0        (depth 2)

Result: D 1.0 (closer to A)
```

If equal depth, first declared wins.

**Gradle: Newest Version**

Gradle uses newest version by default:

```
A → B → C 1.0
A → D → C 2.0

Result: C 2.0 (newest)
```

### Repository Locations

**Maven:**
- **Local Repository**: `~/.m2/repository/` (default)
  - Override with `settings.xml` or `-Dmaven.repo.local=/path`
- **Structure**: `groupId/artifactId/version/`

Example:
```
~/.m2/repository/
└── org/
    └── springframework/
        └── boot/
            └── spring-boot-starter-web/
                └── 3.1.5/
                    ├── spring-boot-starter-web-3.1.5.jar
                    ├── spring-boot-starter-web-3.1.5.pom
                    └── ...
```

**Gradle:**
- **Dependency Cache**: `~/.gradle/caches/modules-2/files-2.1/`
- **Wrapper**: `~/.gradle/wrapper/dists/`

Example:
```
~/.gradle/caches/modules-2/files-2.1/
└── org.springframework.boot/
    └── spring-boot-starter-web/
        └── 3.1.5/
            └── abc123.../
                └── spring-boot-starter-web-3.1.5.jar
```

### Installing Without Test Dependencies

**Maven:**

```bash
# Skip test compilation and execution
mvn clean install -DskipTests

# Skip both compilation and execution
mvn clean install -Dmaven.test.skip=true

# Package without tests
mvn package -DskipTests
```

**Note:** Test-scoped dependencies are still resolved, they just aren't used.

**Gradle:**

```bash
# Build without tests
gradle build -x test

# Skip test tasks
gradle assemble
```

### Transitive Dependency Handling

**Maven:**

```xml
<!-- Exclude transitive dependency -->
<dependency>
    <groupId>com.example</groupId>
    <artifactId>library</artifactId>
    <version>1.0</version>
    <exclusions>
        <exclusion>
            <groupId>commons-logging</groupId>
            <artifactId>commons-logging</artifactId>
        </exclusion>
    </exclusions>
</dependency>

<!-- Control all transitive versions -->
<dependencyManagement>
    <dependencies>
        <dependency>
            <groupId>com.fasterxml.jackson.core</groupId>
            <artifactId>jackson-core</artifactId>
            <version>2.15.3</version>
        </dependency>
    </dependencies>
</dependencyManagement>
```

**Gradle:**

```groovy
// Exclude transitive dependency
implementation('com.example:library:1.0') {
    exclude group: 'commons-logging', module: 'commons-logging'
}

// Exclude all transitives
implementation('com.example:library:1.0') {
    transitive = false
}

// Force versions
configurations.all {
    resolutionStrategy {
        force 'com.google.guava:guava:32.1.2-jre'
    }
}
```

---

## Bundler (Ruby)

### Manifest File: Gemfile

```ruby
# Specify source
source 'https://rubygems.org'

# Ruby version requirement
ruby '3.2.0'

# Production gems
gem 'rails', '~> 7.1.0'
gem 'pg', '>= 1.1', '< 2.0'
gem 'puma', '~> 6.0'
gem 'redis', '~> 5.0'

# Gems with specific source
gem 'my_gem', source: 'https://my-private-source.com'

# Git sources
gem 'rack', git: 'https://github.com/rack/rack', branch: 'main'
gem 'nokogiri', git: 'https://github.com/sparklemotion/nokogiri', tag: 'v1.15.0'

# Path dependencies
gem 'my_local_gem', path: '../my_local_gem'

# Platforms
gem 'tzinfo-data', platforms: [:mingw, :mswin, :x64_mingw, :jruby]

# Groups (similar to dev dependencies)
group :development, :test do
  gem 'rspec-rails', '~> 6.0'
  gem 'factory_bot_rails'
end

group :development do
  gem 'rubocop', require: false
  gem 'spring'
end

group :test do
  gem 'capybara'
  gem 'selenium-webdriver'
end

group :production do
  gem 'rack-timeout'
end
```

### Lock File: Gemfile.lock

```
GEM
  remote: https://rubygems.org/
  specs:
    actioncable (7.1.0)
      actionpack (= 7.1.0)
      activesupport (= 7.1.0)
      nio4r (~> 2.0)
      websocket-driver (>= 0.6.1)
      zeitwerk (~> 2.6)
    actionpack (7.1.0)
      actionview (= 7.1.0)
      activesupport (= 7.1.0)
      nokogiri (>= 1.8.5)
      rack (>= 2.2.4)
      rack-session (>= 1.0.1)
      rack-test (>= 0.6.3)
      rails-dom-testing (~> 2.2)
      rails-html-sanitizer (~> 1.6)
    activesupport (7.1.0)
      concurrent-ruby (~> 1.0, >= 1.0.2)
      connection_pool (>= 2.2.5)
      i18n (>= 1.6, < 2)
      minitest (>= 5.1)
      tzinfo (~> 2.0)
    concurrent-ruby (1.2.2)
    i18n (1.14.1)
      concurrent-ruby (~> 1.0)
    nio4r (2.5.9)
    pg (1.5.4)
    puma (6.4.0)
      nio4r (~> 2.0)
    redis (5.0.7)
      redis-client (>= 0.9.0)
    redis-client (0.17.0)
      connection_pool

GIT
  remote: https://github.com/rack/rack
  revision: 1a2b3c4d5e6f
  branch: main
  specs:
    rack (3.0.0)

PLATFORMS
  ruby
  x86_64-darwin-21
  x86_64-linux

DEPENDENCIES
  pg (>= 1.1, < 2.0)
  puma (~> 6.0)
  rack!
  rails (~> 7.1.0)
  redis (~> 5.0)

RUBY VERSION
   ruby 3.2.0p0

BUNDLED WITH
   2.4.19
```

### Version Constraint Specifications

**Pessimistic Version Constraint (~>):**

The tilde-greater-than operator, or "pessimistic version constraint", is unique to Bundler:

```ruby
~> 2.3      # Equivalent to: >= 2.3, < 3.0
~> 2.3.0    # Equivalent to: >= 2.3.0, < 2.4.0
~> 2.3.5    # Equivalent to: >= 2.3.5, < 2.4.0
```

**Other Operators:**

```ruby
gem 'rails', '7.1.0'           # Exact version
gem 'pg', '= 1.5.4'            # Exact version (explicit)
gem 'nokogiri', '>= 1.6.0'     # Greater than or equal
gem 'rack', '> 2.0'            # Greater than
gem 'thin', '<= 1.8'           # Less than or equal
gem 'json', '< 2.0'            # Less than
gem 'redis', '>= 4.0', '< 6.0' # Multiple constraints
```

### Dependency Resolution Algorithm

**Process:**

1. Read `Gemfile` to get dependency requirements
2. If `Gemfile.lock` exists, use it (skip resolution)
3. Otherwise:
   - Fetch gem metadata from sources
   - Build dependency graph
   - Resolve conflicts using backtracking algorithm
   - Find compatible version set
   - Write `Gemfile.lock`

**Key Behaviors:**

- **Conservative Updates**: `bundle update` updates only specified gems
- **Transitive Resolution**: Automatically includes dependencies of dependencies
- **Platform-Specific**: Can resolve different gems per platform

### Gem Storage Locations

**System Gems (Default):**

```
# Ruby installation location
/usr/lib/ruby/gems/3.2.0/
├── gems/                    # Installed gems
│   ├── rails-7.1.0/
│   └── redis-5.0.7/
└── specifications/          # Gem metadata
    ├── rails-7.1.0.gemspec
    └── redis-5.0.7.gemspec
```

**User Gems:**

```
~/.gem/ruby/3.2.0/
├── gems/
└── specifications/
```

**Bundler with --path or --deployment:**

```
my-project/
├── Gemfile
├── Gemfile.lock
└── vendor/
    └── bundle/
        └── ruby/
            └── 3.2.0/
                ├── gems/
                │   ├── rails-7.1.0/
                │   └── redis-5.0.7/
                └── specifications/
```

**Bundle Configuration:**

```bash
# Set local install path
bundle config set --local path 'vendor/bundle'

# View config
bundle config

# Find gem location
bundle info rails
# Or
bundle show rails
```

**Cache Location:**

```
vendor/cache/          # Cached .gem files (for offline install)
```

### Installing Without Dev Dependencies

```bash
# Install only production gems
bundle install --without development test

# Modern syntax
bundle config set --local without 'development test'
bundle install

# Deployment mode (implies --without development test)
bundle install --deployment
```

### Transitive Dependency Handling

**Automatic Resolution:**

- Bundler automatically resolves all transitive dependencies
- All dependencies (direct and transitive) appear in `Gemfile.lock`
- Version constraints from all dependencies are considered

**Example:**

```ruby
# Gemfile
gem 'rails', '~> 7.1.0'

# Gemfile.lock will include all rails dependencies:
# - actionpack
# - activerecord
# - activesupport
# - etc.
```

**Updating:**

```bash
# Update all gems
bundle update

# Update specific gem and its dependencies
bundle update rails

# Update only the gem, not dependencies
bundle update --conservative rails

# Show what would be updated
bundle outdated
```

---

## Composer (PHP)

### Manifest File: composer.json

```json
{
    "name": "vendor/my-project",
    "description": "My PHP project",
    "type": "project",
    "license": "MIT",
    "require": {
        "php": "^8.1",
        "symfony/console": "^6.3",
        "guzzlehttp/guzzle": "~7.8",
        "monolog/monolog": "2.9.*",
        "doctrine/dbal": ">=3.6 <4.0"
    },
    "require-dev": {
        "phpunit/phpunit": "^10.4",
        "squizlabs/php_codesniffer": "^3.7"
    },
    "autoload": {
        "psr-4": {
            "App\\": "src/"
        }
    },
    "autoload-dev": {
        "psr-4": {
            "App\\Tests\\": "tests/"
        }
    },
    "scripts": {
        "test": "phpunit",
        "cs-fix": "phpcbf"
    },
    "config": {
        "optimize-autoloader": true,
        "preferred-install": "dist",
        "sort-packages": true,
        "platform": {
            "php": "8.1.0"
        }
    },
    "repositories": [
        {
            "type": "vcs",
            "url": "https://github.com/user/custom-package"
        }
    ]
}
```

### Lock File: composer.lock

```json
{
    "_readme": [
        "This file locks the dependencies of your project to a known state",
        "Read more about it at https://getcomposer.org/doc/01-basic-usage.md#installing-dependencies",
        "This file is @generated automatically"
    ],
    "content-hash": "abc123def456...",
    "packages": [
        {
            "name": "symfony/console",
            "version": "v6.3.4",
            "source": {
                "type": "git",
                "url": "https://github.com/symfony/console.git",
                "reference": "eca495f2ee225819070db10b0b17f63d"
            },
            "dist": {
                "type": "zip",
                "url": "https://api.github.com/repos/symfony/console/zipball/eca495",
                "reference": "eca495f2ee225819070db10b0b17f63d",
                "shasum": ""
            },
            "require": {
                "php": ">=8.1",
                "symfony/deprecation-contracts": "^2.5|^3",
                "symfony/polyfill-mbstring": "~1.0"
            },
            "type": "library",
            "autoload": {
                "psr-4": {
                    "Symfony\\Component\\Console\\": ""
                }
            }
        }
    ],
    "packages-dev": [
        {
            "name": "phpunit/phpunit",
            "version": "10.4.1",
            "source": {
                "type": "git",
                "url": "https://github.com/sebastianbergmann/phpunit.git",
                "reference": "1c523c0da3d004029a"
            },
            "require": {
                "php": ">=8.1"
            },
            "type": "library"
        }
    ],
    "platform": {
        "php": "^8.1"
    },
    "platform-dev": []
}
```

### Version Constraint Specifications

#### Caret (^) - Default

```
^1.2.3  → >=1.2.3 <2.0.0
^0.3    → >=0.3.0 <0.4.0
^0.0.3  → >=0.0.3 <0.0.4
```

#### Tilde (~)

```
~1.2.3  → >=1.2.3 <1.3.0
~1.2    → >=1.2.0 <2.0.0
```

#### Wildcard (*)

```
1.2.*   → >=1.2.0 <1.3.0
1.*     → >=1.0.0 <2.0.0
```

#### Comparison Operators

```
>=1.2.3
>1.2.3
<=1.2.3
<1.2.3
!=1.2.3
>=1.2 <2.0
```

#### Exact

```
1.2.3
```

#### Hyphen Range

```
1.0 - 2.0   → >=1.0.0 <2.1    (includes up to 2.0.*)
1.0.0 - 2.1.0 → >=1.0.0 <=2.1.0
```

### Dependency Resolution Algorithm

**composer install:**
1. Reads `composer.lock` if it exists
2. Installs exact versions from lock file
3. If no lock file, reads `composer.json`
4. Resolves dependencies
5. Creates `composer.lock`

**composer update:**
1. Ignores `composer.lock`
2. Reads `composer.json`
3. Fetches latest versions matching constraints
4. Resolves dependency graph
5. Updates `composer.lock`

**Resolution Strategy:**
- Evaluates all version constraints
- Attempts to find latest compatible versions
- Backtracks if conflicts occur
- Prefers stable versions over dev versions

### Package Storage Locations

**Vendor Directory:**

```
my-project/
├── composer.json
├── composer.lock
└── vendor/                          # Installed packages
    ├── autoload.php                # Autoloader entry point
    ├── composer/                   # Composer internals
    │   ├── autoload_classmap.php
    │   ├── autoload_namespaces.php
    │   ├── autoload_psr4.php
    │   ├── autoload_real.php
    │   ├── autoload_static.php
    │   ├── installed.json          # Package metadata
    │   └── installed.php
    ├── symfony/
    │   └── console/
    │       ├── composer.json
    │       └── ...
    └── guzzlehttp/
        └── guzzle/
            └── ...
```

**Cache Directory:**

- **Linux**: `~/.cache/composer/` or `$XDG_CACHE_HOME/composer`
- **macOS**: `~/Library/Caches/composer/`
- **Windows**: `C:\Users\<user>\AppData\Local\Composer\` or `%LOCALAPPDATA%/Composer`

**Find cache directory:**

```bash
composer config cache-dir
```

**Cache Structure:**

```
~/.cache/composer/
├── files/              # Downloaded archives
│   ├── symfony/
│   │   └── console/
│   │       └── abc123.zip
│   └── ...
├── repo/              # Repository metadata
└── vcs/               # VCS clones
```

### Installing Without Dev Dependencies

```bash
# Install only production dependencies
composer install --no-dev

# Update without dev dependencies
composer update --no-dev

# Check what's installed
composer show --installed
composer show --installed --no-dev
```

### Transitive Dependency Handling

**Automatic Resolution:**
- Composer automatically resolves all transitive dependencies
- All dependencies appear in `composer.lock`
- Version constraints from entire graph considered

**Viewing Dependency Tree:**

```bash
# Show dependency tree
composer show --tree

# Show why a package is installed
composer why symfony/console
composer depends symfony/console

# Show what depends on a package
composer why-not symfony/console 7.0
composer prohibits symfony/console 7.0
```

**Replacing Packages:**

```json
{
    "replace": {
        "symfony/polyfill-mbstring": "*"
    }
}
```

**Conflicts:**

```json
{
    "conflict": {
        "symfony/symfony": "*"
    }
}
```

---

## Best Practices Summary

### General Principles

1. **Always Commit Lock Files**
   - Ensures reproducible builds
   - Locks transitive dependencies
   - Critical for production deployments

2. **Use Exact Versions for Applications, Ranges for Libraries**
   - Applications: Lock to exact versions
   - Libraries: Use semver ranges for compatibility

3. **Separate Dev and Production Dependencies**
   - Keep development tools out of production
   - Reduces deployment size
   - Improves security

4. **Regularly Update Dependencies**
   - Security patches
   - Bug fixes
   - Performance improvements

5. **Audit Dependencies for Security**
   - Use security scanning tools
   - Review dependency trees
   - Minimize transitive dependencies

### Package Manager Specific

#### npm/yarn/pnpm

```bash
# Lock file hygiene
npm ci              # Clean install in CI (uses lock file)
npm audit           # Security audit
npm outdated        # Check for updates

# Modern best practices
npm install --omit=dev        # Production installs
pnpm install --frozen-lockfile # Ensure lock file isn't modified
```

#### Python (pip/poetry)

```bash
# Use virtual environments ALWAYS
python -m venv venv
source venv/bin/activate

# Poetry best practices
poetry install --without dev  # Production
poetry update --dry-run       # Preview updates
poetry check                  # Validate pyproject.toml

# Pip with pip-tools
pip-compile requirements.in   # Generate locked requirements
pip-sync requirements.txt     # Install exact versions
```

#### Rust (cargo)

```bash
# Check for updates
cargo outdated

# Update conservatively
cargo update --package serde  # Update single package

# Verify lock file
cargo verify-project
cargo tree                    # View dependency tree
```

#### Go

```bash
# Keep go.mod clean
go mod tidy

# Verify integrity
go mod verify

# Vendor for reproducibility
go mod vendor

# Use specific versions
go get package@v1.2.3
```

#### Java (Maven/Gradle)

```bash
# Maven
mvn dependency:tree          # View tree
mvn versions:display-dependency-updates  # Check updates

# Gradle
gradle dependencies          # View tree
gradle dependencyInsight --dependency guava
./gradlew dependencies --write-locks  # Create lock files
```

#### Ruby (Bundler)

```bash
# Conservative updates
bundle update --conservative gem_name

# Audit
bundle audit

# Clean up
bundle clean

# Check platforms
bundle lock --add-platform x86_64-linux
```

#### PHP (Composer)

```bash
# Validate composer.json
composer validate

# Audit
composer audit

# Optimize for production
composer install --no-dev --optimize-autoloader

# Check for updates
composer outdated
```

### Security Best Practices

1. **Enable Dependency Scanning**
   - npm: `npm audit`
   - pip: `pip-audit` or `safety`
   - cargo: `cargo audit`
   - bundler: `bundle audit`
   - composer: `composer audit`

2. **Use Lock File Integrity Checks**
   - Verify checksums/hashes
   - Use `--frozen-lockfile` or equivalent in CI

3. **Minimize Dependency Depth**
   - Fewer dependencies = smaller attack surface
   - Review transitive dependencies

4. **Keep Dependencies Updated**
   - Automate security updates
   - Use tools like Dependabot, Renovate

5. **Pin Critical Dependencies**
   - Use exact versions for security-critical packages
   - Lock cryptographic libraries

### CI/CD Best Practices

1. **Use Clean Installs**
   ```bash
   npm ci                           # npm
   pip install --require-hashes     # pip
   poetry install --no-root         # poetry
   cargo build --locked             # cargo
   go mod verify                    # go
   composer install --no-dev        # composer
   bundle install --deployment      # bundler
   ```

2. **Cache Dependencies**
   - Cache `~/.npm`, `~/.cache/pip`, `~/.cargo`, etc.
   - Verify cache integrity

3. **Fail on Lock File Changes**
   - Detect unexpected modifications
   - Prevent drift between environments

4. **Reproducible Builds**
   - Use lock files
   - Pin tool versions
   - Document system dependencies

---

## References

### Official Documentation

- **Semantic Versioning**: [semver.org](https://semver.org/)
- **npm**: [docs.npmjs.com](https://docs.npmjs.com/)
- **Yarn**: [yarnpkg.com](https://yarnpkg.com/)
- **pnpm**: [pnpm.io](https://pnpm.io/)
- **pip**: [pip.pypa.io](https://pip.pypa.io/)
- **Poetry**: [python-poetry.org](https://python-poetry.org/)
- **Cargo**: [doc.rust-lang.org/cargo](https://doc.rust-lang.org/cargo/)
- **Go Modules**: [go.dev/ref/mod](https://go.dev/ref/mod)
- **Maven**: [maven.apache.org](https://maven.apache.org/)
- **Gradle**: [gradle.org](https://gradle.org/)
- **Bundler**: [bundler.io](https://bundler.io/)
- **Composer**: [getcomposer.org](https://getcomposer.org/)

### Key Articles and Resources

#### npm/yarn/pnpm
- [package-locks | npm Docs](https://docs.npmjs.com/cli/v6/configuring-npm/package-locks/)
- [package-lock.json | npm Docs](https://docs.npmjs.com/cli/v6/configuring-npm/package-lock-json/)
- [Understanding npm Package Locks](https://www.w3resource.com/npm/npm-package-locks.php)
- [The PNPM lockfile | Lockfile Explorer](https://lfx.rushstack.io/pages/concepts/pnpm_lockfile/)
- [package-lock.json vs. yarn.lock vs. pnpm-lock.yaml](https://cyberphinix.de/blog/package-lock-json-vs-yarn-lock-vs-pnpm-lock-yaml-basics/)
- [How npm3 Works](https://npm.github.io/how-npm-works-docs/npm3/how-npm3-works.html)
- [Symlinked node_modules structure | pnpm](https://pnpm.io/symlinked-node-modules-structure)

#### Python
- [Dependency specification | Poetry](https://python-poetry.org/docs/dependency-specification/)
- [The pyproject.toml file | Poetry](https://python-poetry.org/docs/pyproject/)
- [Writing your pyproject.toml - Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
- [Dependency Management With Python Poetry – Real Python](https://realpython.com/dependency-management-python-poetry/)
- [Configuration | Poetry](https://python-poetry.org/docs/configuration/)

#### Rust
- [Dependency Resolution - The Cargo Book](https://doc.rust-lang.org/cargo/reference/resolver.html)
- [Specifying Dependencies - The Cargo Book](https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html)
- [Cargo.toml vs Cargo.lock](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html)
- [Build Cache - The Cargo Book](https://doc.rust-lang.org/cargo/reference/build-cache.html)
- [Cargo Home - The Cargo Book](https://doc.rust-lang.org/cargo/guide/cargo-home.html)

#### Go
- [Go Modules Reference](https://go.dev/ref/mod)
- [Managing dependencies - Go](https://go.dev/doc/modules/managing-dependencies)
- [Mastering Go Modules: A Practical Guide](https://leapcell.medium.com/mastering-go-modules-a-practical-guide-to-dependency-management-e18eed09939c)

#### Java
- [Locking Versions - Gradle](https://docs.gradle.org/current/userguide/dependency_locking.html)
- [GitHub - chains-project/maven-lockfile](https://github.com/chains-project/maven-lockfile)
- [Where Is the Maven Local Repository? - Baeldung](https://www.baeldung.com/maven-local-repository)

#### Ruby
- [Bundler: Why Bundler exists](https://bundler.io/guides/rationale.html)
- [The Ultimate Guide to Gemfile and Gemfile.lock](https://blog.saeloun.com/2022/08/16/understanding-gemfile-and-gemfile-lock/)
- [bundle cache - Bundler](https://bundler.io/man/bundle-cache.1.html)

#### PHP
- [Basic usage - Composer](https://getcomposer.org/doc/01-basic-usage.md)
- [Config - Composer](https://getcomposer.org/doc/06-config.md)
- [Understanding composer.json and composer.lock](https://peltekis.dev/blog/understanding-composer-json-and-composer-lock/)

#### Version Specifications
- [semver | npm Docs](https://docs.npmjs.com/cli/v6/using-npm/semver/)
- [Semver: Tilde and Caret](https://nodesource.com/blog/semver-tilde-and-caret)
- [npm semantic version calculator](https://semver.npmjs.com/)

---

## Conclusion

Understanding package manager specifications and dependency resolution mechanisms is crucial for:

1. **Reproducible Builds**: Lock files ensure consistent dependency versions across environments
2. **Security**: Proper dependency management reduces supply chain attack surface
3. **Performance**: Efficient caching and resolution speeds up development
4. **Maintainability**: Clear dependency graphs make updates and debugging easier

Each package manager has evolved to solve specific ecosystem challenges:

- **npm/yarn/pnpm**: Handle the massive JavaScript ecosystem with millions of small packages
- **pip/poetry**: Manage Python's complex compatibility requirements
- **cargo**: Provide Rust's strong guarantees with safe, deterministic builds
- **Go modules**: Simplify dependency management with minimal version selection
- **Maven/Gradle**: Support Java's enterprise-scale applications
- **Bundler**: Manage Ruby gems with version constraints
- **Composer**: Handle PHP's autoloading and dependency complexities

By following best practices and understanding the underlying mechanisms, developers can build more secure, reliable, and maintainable software.
