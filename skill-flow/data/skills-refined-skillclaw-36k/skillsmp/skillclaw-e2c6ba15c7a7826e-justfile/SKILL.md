---
name: justfile
description: Use this skill when creating, editing, or understanding justfiles for the just command runner, including adding or modifying recipes, parameters, and settings.
---

# Justfile

A justfile stores project-specific commands (recipes) that can be run with `just <recipe>`.

## Quick Reference

```just
# Recipe with doc comment
recipe-name:
    echo "commands are indented with 4 spaces or 1 tab"

# Recipe with parameters
greet name="world":
    echo "Hello, {{name}}!"

# Recipe with dependencies
build: clean compile
    echo "Built!"

# Shebang recipe for multi-line scripts
test:
    #!/usr/bin/env bash
    set -euxo pipefail
    cargo test
```

## Core Syntax

### Recipes

```just
# Basic recipe
build:
    cargo build

# With parameters (with defaults)
test target="all" flags="":
    cargo test {{target}} {{flags}}

# Variadic: + = one or more, * = zero or more
backup +FILES:
    cp {{FILES}} /backup/

deploy *FLAGS:
    ./deploy.sh {{FLAGS}}

# Dependencies run before recipe
test: build
    ./test

# Sequential dependencies with &&
release: build && deploy notify
```

### Variables

```just
version := "1.0.0"
build_dir := "target"

# Backtick captures command output
git_hash := `git rev-parse --short HEAD`

# Environment variable access
home := env('HOME')
editor := env('EDITOR', 'vim')  # with default
```

### Settings

```just
set shell := ["bash", "-uc"]
set dotenv-load                    # load .env file
set positional-arguments           # pass args as $1, $2
set export                         # export all vars as env vars
set working-directory := "subdir"  # change working dir
set quiet                          # suppress command echo
```

### Attributes

```just
[group('build')]                   # group in --list output
[private]                          # hide from --list
[no-cd]                            # don't change directory
[confirm("Delete all?")]           # require confirmation
[working-directory: 'subdir']      # per-recipe working dir
[script('bash')]                   # run as bash script
[linux]                            # only run on Linux
[macos]                            # only run on macOS
[windows]                          # only run on Win
```

## Editing Workflow

1. Locate the nearest `justfile` or `.justfile` to the working directory and edit in place.
2. Read the existing `justfile` top to bottom; note `set` directives, variables, aliases, and groups.
3. Add or update recipes using the same structure and indentation.
4. Ensure dependencies and parameters are correct and consistent.
5. If a recipe should be hidden from listings, mark it private or prefix with `_`.

## Syntax Essentials

- **Recipe:**

  ```just
  build target="app": clean
      cargo build --release --bin {{target}}
  ```

- **Dependencies:** run before the recipe body; parameterized deps are wrapped in parentheses.

  ```just
  rebuild: clean build
  build arch: (clean arch)
      cargo build --target {{arch}}
  ```

- **Parameters:** defaults supported; variadics use `*` (zero or more) or `+` (one or more).

  ```just
  test suite="all":
      cargo test --tests {{suite}}

  backup *files:
      tar czf backup.tar.gz {{files}}
  ```

- **Exported parameters:** prefix with `$` to pass as environment variables.

  ```just
  test-with-env $TEST_MODE:
      echo "$TEST_MODE"
  ```

- **Variables and interpolation:**

  ```just
  app := "myapp"
  build:
      echo "{{app}}"
  ```

- **Default recipe:** place first if you want it to run with `just`.

  ```just
  default:
      @just --list
  ```

## Common Attributes and Helpers

- `[group('name')]` or `[group: 'name']` to categorize recipes in listings.
- `[working-directory('path')]` to override the cwd for one recipe.
- `[private]` to hide a recipe or alias from `just --list`.
- `[doc('description')]` to control list output text.
- `[confirm('prompt')]` to request confirmation.
- `[linux]`, `[macos]`, `[windows]` for platform-specific recipes.
- `[no-cd]` to run in the invoking directory instead of the justfile's directory.