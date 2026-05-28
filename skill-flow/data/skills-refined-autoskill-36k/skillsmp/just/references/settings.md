# Just Settings Reference

Settings configure justfile behavior. Declare at top of justfile.

## Syntax

```just
set NAME              # Boolean shorthand (= true)
set NAME := true      # Boolean explicit
set NAME := "value"   # String
set NAME := ["a", "b"] # Array
```

## All Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `quiet` | bool | false | Suppress command echoing |
| `dotenv-load` | bool | false | Load `.env` file if present |
| `dotenv-filename` | string | — | Custom `.env` filename |
| `dotenv-path` | string | — | Custom `.env` path (errors if missing) |
| `dotenv-required` | bool | false | Error if `.env` not found |
| `dotenv-override` | bool | false | Override existing env vars from `.env` |
| `export` | bool | false | Export all variables as env vars |
| `positional-arguments` | bool | false | Pass args positionally to recipes |
| `fallback` | bool | false | Search parent dirs for justfile |
| `ignore-comments` | bool | false | Ignore `#` lines in recipes |
| `allow-duplicate-recipes` | bool | false | Later recipes override earlier |
| `allow-duplicate-variables` | bool | false | Later variables override earlier |
| `shell` | array | — | Command for recipes/backticks |
| `windows-shell` | array | — | Windows-specific shell |
| `script-interpreter` | array | `['sh', '-eu']` | Interpreter for `[script]` recipes |
| `tempdir` | string | — | Custom temp directory |
| `working-directory` | string | — | Working dir for recipes |
| `unstable` | bool | false | Enable experimental features |

## Common Patterns

```just
# Recommended defaults
set quiet
set dotenv-load

# Custom shell
set shell := ["bash", "-euo", "pipefail", "-c"]

# Windows PowerShell
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# Export all vars to environment
set export
```
