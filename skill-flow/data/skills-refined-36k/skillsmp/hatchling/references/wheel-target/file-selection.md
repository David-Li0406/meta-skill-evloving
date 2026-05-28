---
category: wheel-target
topics: [file-selection, patterns, glob, include, exclude, artifacts]
related: [package-discovery.md, force-include.md, sources-option.md]
---

# File Selection and Patterns

When assisting users with controlling which files are included in wheels, reference this guide to explain include/exclude patterns, glob syntax, file selection heuristics, and pattern precedence.

## Include and Exclude Patterns

The `include` and `exclude` options use Git-style glob patterns to select files for wheel distribution. When helping users:

**Example configuration:**

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
include = [
  "/docs/**/*.md",
  "/LICENSE",
]
exclude = [
  "**/*.pyc",
  "**/__pycache__",
]
```

Explain that:

- `include` explicitly adds files to the wheel
- `exclude` removes files from inclusion
- Patterns use Git-style glob syntax
- Exclusions take precedence over inclusions

## Git-Style Glob Syntax

When users ask about pattern syntax, reference these glob conventions:

| Pattern         | Matches                                    |
| --------------- | ------------------------------------------ |
| `*.py`          | Any .py file in current directory only     |
| `**/*.py`       | .py files in any directory (recursive)     |
| `src/**`        | Everything under src directory (recursive) |
| `/docs`         | docs directory at project root             |
| `tests/**/*.py` | Python files in tests subdirectories       |
| `*.{py,pyx}`    | Files ending in .py or .pyx                |
| `file-?.py`     | file-a.py, file-b.py, etc.                 |

**Important note:** The glob matching now closely resembles Git's behavior (as of Hatchling v1.9.0). Paths with leading slashes (`/`) match from the project root.

## Leading Slash Behavior

When helping users understand path patterns, explain:

```toml
# Matches only at project root
include = ["/README.md"]

# Matches in any directory
include = ["README.md"]

# Matches all md files recursively
include = ["**/*.md"]

# Matches docs directory at root only
exclude = ["/docs"]
```

Patterns without leading slashes match anywhere. Patterns with leading slashes match from project root.

## File Selection Heuristics

When users don't define explicit patterns, Hatchling applies automatic heuristics:

1. **Package discovery** - Includes detected packages (see Package Discovery guide)
2. **Associated files** - Automatically includes important files like:
   - License files (LICENSE, COPYING, etc.)
   - PEP 561 type hint files (py.typed)
   - Package metadata files
3. **Conditional inclusion** - Files ignored by VCS (.gitignore) are excluded unless:
   - Listed in `artifacts` (for build hook outputs)
   - Explicitly included via `include` patterns

## Artifacts Option

For files that build hooks generate (which are ignored by VCS), use `artifacts`:

```toml
[tool.hatch.build.targets.wheel]
artifacts = [
  "mypackage/generated.py",
  "mypackage/data/*.json",
]
```

This is semantically equivalent to `include` but clearly indicates these are build-time artifacts. Reference this when users want to ship generated code.

## Interaction with Packages Option

When users specify `packages`:

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/mypackage"]
```

Hatchling automatically:

- Uses `only-include` with the specified packages
- Sets `sources = ["src"]` for path rewriting
- Selects the full package contents (all Python files, subdirectories, etc.)

Additional `include`/`exclude` patterns refine this default selection.

## Pattern Precedence

Help users understand pattern precedence:

1. **Explicit inclusion** - `packages` and `include` patterns
2. **Artifacts** - Build hook generated files
3. **Exclusion** - `exclude` patterns override inclusion
4. **Default heuristics** - Applied if no explicit patterns defined

When users define `include` patterns and find files missing, explain that `exclude` patterns override their choices. Reorder patterns or remove conflicting exclusions.

## Only-Include Option

For targeted inclusion that prevents directory traversal:

```toml
[tool.hatch.build.targets.wheel]
only-include = [
  "src/mypackage",
  "src/data",
]
```

Unlike `packages`, `only-include` doesn't automatically apply `sources` path rewriting. Use this when:

- You need to include non-package directories
- You want to control path rewriting explicitly
- You're including multiple unrelated paths

## Default Exclusions

Explain to users that Hatchling always excludes certain directories, even without explicit `exclude` patterns:

- `__pycache__`
- `.git`, `.hg`, `.svn` (version control directories)
- `.tox`, `.nox`, `.hatch` (tool directories)
- `build`, `dist` (build output directories)
- `*.egg-info` directories

This prevents accidental inclusion of build artifacts and version control metadata.

## VCS Integration

When helping users understand file selection:

```toml
[tool.hatch.build.targets.wheel]
include = [
  "src/**/*.py",
  "src/**/*.txt",
]
```

If a file matches an `include` pattern but is listed in `.gitignore`, it will be included in the wheel anyway (explicit inclusion overrides VCS ignore). Use this when you want to distribute files normally excluded from version control.

## Examples for Common Scenarios

### Include License File

```toml
include = ["/LICENSE"]
```

### Exclude Test Files

```toml
exclude = [
  "tests/**",
  "**/*_test.py",
]
```

### Include Data Files

```toml
include = [
  "mypackage/data/**/*",
]
```

### Include Compiled Extensions

```toml
artifacts = [
  "mypackage/*.so",
  "mypackage/*.pyd",
]
```

## Performance Considerations

When assisting users with pattern matching:

- Hatchling optimizes directory traversal, avoiding directories that can't match patterns
- Longer, more specific patterns perform better than broad patterns
- Explicit `only-include` is faster than complex `include`/`exclude` combinations
- Avoid matching unnecessary directories to improve build speed
