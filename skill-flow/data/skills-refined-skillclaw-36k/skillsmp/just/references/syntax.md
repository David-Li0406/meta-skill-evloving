# Just Syntax Reference

## Variables

```just
# Simple assignment
name := "value"

# From environment (compile-time)
home := env("HOME")

# From command output (backticks)
version := `git describe --tags`
branch := `git branch --show-current`

# Export to recipe environment
export DATABASE_URL := "postgres://localhost/db"
```

### CLI Override

```bash
just name=value recipe
just --set name value recipe
```

## Strings

```just
# Single quotes: literal, no escapes
path := '/path/to/file'

# Double quotes: escape sequences work
msg := "Hello\nWorld"     # \n, \t, \\, \", \u{1F600}

# Triple quotes: multiline, strips common indent
script := '''
    line 1
    line 2
'''

# Shell expansion (x prefix)
home := x'$HOME'
user := x'${USER:-default}'
path := x'~/projects'

# Format strings (f prefix)
greeting := f'Hello, {{name}}!'
```

## Interpolation

Use `{{expression}}` in strings and recipe lines:

```just
version := "1.0"

build:
    echo "Building version {{version}}"
    tar -czf app-{{version}}.tar.gz ./dist
```

## Conditionals

```just
# Equality
mode := if env("CI") == "true" { "release" } else { "debug" }

# Inequality
msg := if version != "0.0.0" { "stable" } else { "dev" }

# Regex match
is_valid := if name =~ '^[a-z]+$' { "yes" } else { "no" }

# In recipes
build:
    {{ if os() == "windows" { "build.bat" } else { "./build.sh" } }}
```

## Imports

```just
# Include another file
import 'path/to/file.just'

# Optional import (no error if missing)
import? 'optional.just'

# Home directory
import '~/shared/common.just'
```

Rules:
- Order independent (can reference before/after)
- Top-level overrides imported
- Shallower overrides deeper

## Comments

```just
# Line comment

# Comments before recipes show in `just --list`
build:
    # This comment is part of the recipe
    echo "building"
```

## Operators

| Op | Purpose |
|----|---------|
| `:=` | Assignment |
| `+` | String concatenation |
| `/` | Path join |
| `==` | Equality |
| `!=` | Inequality |
| `=~` | Regex match |

## Examples

```just
# Variables with fallbacks
port := env("PORT", "3000")
host := env("HOST", "localhost")

# Conditional compilation target
target := if os() == "windows" { "x86_64-pc-windows-msvc" } else { "" }

# Path construction
dist := justfile_directory() / "dist"
bin := dist / "bin"

# Dynamic recipe
serve:
    ./server --port {{port}} --host {{host}}
```
