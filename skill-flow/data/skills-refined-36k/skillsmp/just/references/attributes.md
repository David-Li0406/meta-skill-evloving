# Just Recipe Attributes

Attributes modify recipe behavior. Stack vertically or comma-separate.

```just
[group('build')]
[confirm]
deploy:
    ./deploy.sh

# Or single line
[group('build'), confirm]
deploy:
    ./deploy.sh

# Colon shorthand for single arg
[group: 'build']
deploy:
    ./deploy.sh
```

## All Attributes

### Organization

| Attribute | Purpose |
|-----------|---------|
| `[group(NAME)]` | Organize in named group for `--list` |
| `[doc(TEXT)]` | Set documentation string |
| `[private]` | Hide from `--list` |
| `[default]` | Module's default recipe |

### Execution Control

| Attribute | Purpose |
|-----------|---------|
| `[confirm]` | Prompt user before running |
| `[confirm(PROMPT)]` | Custom confirmation message |
| `[no-cd]` | Don't change to justfile directory |
| `[no-exit-message]` | Suppress error messages |
| `[no-quiet]` | Force output even with `set quiet` |
| `[working-directory(PATH)]` | Custom working directory |

### Dependencies

| Attribute | Purpose |
|-----------|---------|
| `[parallel]` | Run dependencies concurrently |

### Platform-Specific

| Attribute | Purpose |
|-----------|---------|
| `[linux]` | Only run on Linux |
| `[macos]` | Only run on macOS |
| `[unix]` | Only run on Unix-like |
| `[windows]` | Only run on Windows |
| `[openbsd]` | Only run on OpenBSD |

### Script Recipes

| Attribute | Purpose |
|-----------|---------|
| `[script]` | Execute as script file |
| `[script(COMMAND)]` | Script with custom interpreter |
| `[extension(EXT)]` | File extension for script |

### Parameters

| Attribute | Purpose |
|-----------|---------|
| `[positional-arguments]` | Enable positional args |
| `[arg(ARG, help="TEXT")]` | Argument help text |
| `[arg(ARG, long="NAME")]` | Require `--NAME value` |
| `[arg(ARG, short="X")]` | Require `-X value` |
| `[arg(ARG, pattern="REGEX")]` | Validate against pattern |

## Examples

```just
# Grouped recipes
[group('dev')]
dev: setup
    ./run-dev.sh

[group('dev')]
test:
    cargo test

# Dangerous operation with confirmation
[confirm("Are you sure you want to delete everything?")]
clean-all:
    rm -rf target/ node_modules/

# Platform-specific
[linux]
install:
    apt install -y mypackage

[macos]
install:
    brew install mypackage

# Parallel dependencies
[parallel]
all: build test lint
    echo "All done"
```
