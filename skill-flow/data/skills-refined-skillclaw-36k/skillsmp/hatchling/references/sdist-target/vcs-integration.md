---
name: sdist-vcs-integration
description: Guide to configuring file selection for source distributions using version control system integration, including .gitignore patterns, explicit include/exclude rules, and troubleshooting file inclusion issues
---

# VCS Integration and File Selection in Sdist

Configure Hatchling's source distribution builder to leverage version control systems for intelligent file selection. This integration automatically excludes development artifacts while including all necessary source files based on VCS ignore patterns.

## How VCS Integration Works

### Default Behavior

When building sdists, Hatchling follows this process:

1. **Detects VCS system** in the project root
2. **Reads ignore patterns** from `.gitignore` or `.hgignore`
3. **Includes all tracked files** (not ignored)
4. **Excludes all ignored files** (per VCS rules)
5. **Always includes mandatory files** (even if ignored)

This approach provides:

- Automatic respect for existing VCS configuration
- Prevention of build artifact inclusion
- Zero additional configuration for most projects
- Consistency between repository and distribution

### Supported VCS Systems

| System    | Ignore File  | Pattern Syntax        | Support |
| --------- | ------------ | --------------------- | ------- |
| Git       | `.gitignore` | Full glob syntax      | Full    |
| Mercurial | `.hgignore`  | Glob only (not regex) | Limited |
| No VCS    | N/A          | Include all           | Full    |

## Git Integration

### .gitignore Recognition

Hatchling searches for `.gitignore` starting from the project root and moving up directory tree:

```text
project/
├── .gitignore          ← Checked first
├── src/
│   └── module.py
└── pyproject.toml

../../.gitignore        ← Checked if not found above
```

### Git Pattern Syntax

Full Git-style glob patterns are supported:

```gitignore
# Exclude compiled Python files
*.pyc
__pycache__/

# Exclude build directories
build/
dist/
*.egg-info/

# Exclude editor files
.vscode/
.idea/
*.swp

# Exclude virtual environments
venv/
.venv/

# Include specific files (negation)
!important.txt

# Exclude with wildcards
tests/**/fixtures/generated/
docs/**/*.build/

# Exclude by extension in specific directory
wheels/*.so
```

### Negation Patterns

Use `!` to include files otherwise excluded:

```gitignore
# Exclude everything in test data
test_data/
# But include this specific file
!test_data/important.json
```

Note: Negation only works for files not already excluded by previous patterns.

## Mercurial Integration

### .hgignore Recognition

Hatchling recognizes `.hgignore` in Mercurial projects:

```text
project/
├── .hgignore           ← Used by Hatchling
├── .hg/
└── src/
```

### Mercurial Pattern Limitations

Hatchling supports **glob syntax only** for `.hgignore`:

```hgignore
# Glob patterns work
*.pyc
__pycache__
build/
dist/

# Regex syntax is NOT supported
# Unlike Mercurial itself which supports regex
```

If your `.hgignore` uses regex, Hatchling will only use glob-compatible patterns.

## Explicit File Selection

When implicit VCS-based selection isn't sufficient, use explicit patterns:

### Include Patterns

Force inclusion of specific files or directories:

```toml
[tool.hatch.build.targets.sdist]
include = [
  "/src",           # Include src directory
  "/tests",         # Include tests directory
  "/docs",          # Include documentation
  "*.md",           # Include all markdown files
  "/examples",      # Include examples directory
]
```

### Exclude Patterns

Remove files from the distribution:

```toml
[tool.hatch.build.targets.sdist]
exclude = [
  "*.pyc",          # Exclude compiled Python
  "__pycache__",    # Exclude Python cache
  ".pytest_cache",  # Exclude pytest cache
  ".tox",           # Exclude tox directory
  "htmlcov",        # Exclude coverage reports
  "docs/_build",    # Exclude built docs
]
```

### Only-Include Mode

Explicitly list only the files/directories to include:

```toml
[tool.hatch.build.targets.sdist]
only-include = [
  "src/my_package",
  "tests",
  "pyproject.toml",
  "README.md",
  "LICENSE",
]
```

When using `only-include`:

- Directory traversal from project root is disabled
- Only listed paths are included
- Even tracked VCS files are excluded unless listed
- More explicit but more verbose

## Pattern Matching Rules

All patterns follow **Git-style glob syntax**:

### Pattern Elements

| Pattern  | Meaning                                          |
| -------- | ------------------------------------------------ |
| `*`      | Match any characters except `/`                  |
| `**`     | Match any characters including `/` (multi-level) |
| `?`      | Match any single character                       |
| `[abc]`  | Match any character in brackets                  |
| `[a-z]`  | Match character range                            |
| `[!abc]` | Match any character NOT in brackets              |
| `/`      | Path separator                                   |
| `!`      | Negate pattern (exclude from exclusion)          |

### Common Patterns

```toml
[tool.hatch.build.targets.sdist]
exclude = [
  # Python artifacts
  "*.py[cod]",           # .pyc, .pyo, .pyd
  "__pycache__/",
  "*.egg-info/",
  ".Python",
  "pip-log.txt",

  # Build outputs
  "build/",
  "dist/",
  "wheels/",

  # Testing
  ".tox/",
  ".coverage",
  ".pytest_cache/",
  "htmlcov/",

  # IDE/Editor
  ".vscode/",
  ".idea/",
  "*.swp",
  "*.swo",
  "*~",
  ".DS_Store",

  # Documentation
  "docs/_build/",
  "docs/.buildinfo",

  # Virtual environments
  "venv/",
  ".venv/",
  "env/",
  ".env",

  # Development
  ".git/",
  ".hg/",
  ".tox/",
  "*.sqlite",
  "*.db",
]
```

## Mandatory Files

These files are **always included** regardless of VCS configuration or exclusion rules:

```text
/pyproject.toml       # Project configuration (always)
/hatch.toml           # Hatch configuration (if present)
/hatch_build.py       # Custom build script (if present)
/.gitignore           # Git ignore rules (if present)
/.hgignore            # Mercurial ignore rules (if present)
<readme files>        # Files specified in [project] readme
<license-files>       # Files specified in license-files glob patterns
```

These are essential for:

- Rebuilding the package from sdist
- Proper metadata interpretation
- Correct dependency resolution

## Disabling VCS Integration

To ignore VCS rules and rely only on explicit configuration:

```toml
[tool.hatch.build.targets.sdist]
ignore-vcs = true
```

When `ignore-vcs = true`:

- `.gitignore` and `.hgignore` are completely ignored
- Only explicitly configured files are included
- Mandatory files are still included
- More verbose but completely explicit

### When to Use ignore-vcs = true

Use when:

- VCS configuration doesn't match distribution needs
- You want absolute control over distribution contents
- Mixing VCS patterns causes confusion
- Building in unusual environments
- Special distribution requirements

Example:

```toml
[tool.hatch.build.targets.sdist]
ignore-vcs = true
include = [
  "/src",
  "/README.md",
  "/LICENSE",
  "/CHANGELOG.md",
]
exclude = [
  "*.pyc",
  "__pycache__",
]
```

## Combining VCS and Explicit Patterns

Mix automatic VCS detection with explicit patterns:

```toml
[tool.hatch.build.targets.sdist]
# ignore-vcs is false (default)
# So .gitignore is respected

# Additional explicit inclusions
include = [
  "/examples",        # Ensure examples are included even if .gitignore excludes them
  "/docs",            # Ensure documentation is included
]

# Additional explicit exclusions
exclude = [
  "*.tmp",            # Exclude temp files not in .gitignore
  "test_output/",     # Exclude test outputs
]
```

Precedence:

1. Start with VCS rules (if `ignore-vcs = false`)
2. Apply explicit `include` patterns
3. Apply explicit `exclude` patterns (takes precedence)

## Common VCS Configuration Patterns

### Typical .gitignore for Python Projects

```gitignore
# Byte-compiled Python
*.py[cod]
__pycache__/
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.tox/
.coverage
.pytest_cache/
htmlcov/

# Misc
.DS_Store
.env
*.db
*.sqlite
*.log
```

### Minimal .gitignore

```gitignore
*.pyc
__pycache__/
*.egg-info/
dist/
build/
```

## Debugging File Selection

### Check What's Included

Build with verbose output:

```bash
hatch build -v
```

### Verify Git Tracking

```bash
# Check if Git ignores a file
git check-ignore -v filename

# List tracked files
git ls-files

# List ignored files (with -o option)
git status --short --ignored
```

### Test Sdist Contents

```bash
# List files in generated sdist
tar -tzf dist/package-1.0.0.tar.gz | sort

# Compare with repository files
git ls-files | sort
```

### Verify Pattern Matching

Test glob patterns locally:

```bash
# Using shell globbing (be careful with escaping)
ls -la src/**/*.py

# Or use Python
python -c "import glob; print(glob.glob('src/**/*.py', recursive=True))"
```

## Migration Guide

### From Manual MANIFEST.in to VCS-Based Selection

Old approach (legacy setuptools):

```text
# MANIFEST.in
include README.md
include LICENSE
recursive-include src *.py
recursive-include tests *.py
exclude build
exclude dist
```

Modern approach (Hatchling with VCS):

```toml
# .gitignore handles most exclusions
# Hatchling uses it automatically

[tool.hatch.build.targets.sdist]
# Explicitly ensure important files are included
include = [
  "/tests",
]
```

The `.gitignore` replaces MANIFEST.in for most use cases.

## See Also

- [Git .gitignore Documentation](https://git-scm.com/docs/gitignore)
- [Mercurial .hgignore Documentation](https://www.mercurial-scm.org/wiki/Ignore)
- [Gitignore Best Practices](https://github.com/github/gitignore)
- [Python .gitignore Template](https://github.com/github/gitignore/blob/main/Python.gitignore)
