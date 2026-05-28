---
name: shell-script-quality-assurance
description: Use this skill when you need to lint, format, or improve the quality of shell scripts, following best practices and style guidelines.
---

# Shell Script Quality Assurance

This skill provides comprehensive guidance for ensuring the quality of shell scripts through linting, formatting, and adherence to best practices.

## Core Principles

1. **Consistency** - Follow established patterns within each script.
2. **Safety** - Quote variables, use `[[ ]]`, check return values.
3. **Readability** - Use clear naming, maintain 2-space indents, and limit line length to 80 characters.

## Linting with Shellcheck

### Installation

```bash
# Debian/Ubuntu
apt install shellcheck

# macOS
brew install shellcheck

# From source
cabal update && cabal install ShellCheck
```

### Basic Usage

```bash
# Check single file
shellcheck <script_path>

# Check multiple files
shellcheck <script_directory>/*.sh

# Exclude specific rules
shellcheck --exclude=SC2086 <script_path>
```

### Common Shellcheck Codes

| Code   | Issue                                      | Fix                            |
| ------ | ------------------------------------------ | ------------------------------ |
| SC2086 | Double quote to prevent globbing/splitting | `"$var"`                       |
| SC2046 | Quote command substitution                 | `"$(cmd)"`                     |
| SC2006 | Use `$()` instead of backticks             | `$(cmd)`                       |
| SC2181 | Check exit status directly                 | `if cmd; then`                 |

### Shellcheck Directives

```bash
# Disable for next line
# shellcheck disable=SC2086
echo $unquoted_var
```

## Formatting with shfmt

### Installation

```bash
# macOS
brew install shfmt

# Go install
go install mvdan.cc/sh/v3/cmd/shfmt@latest
```

### Basic Usage

```bash
# Format and print to stdout
shfmt <script_path>

# Format in place
shfmt -w <script_path>

# Check formatting (exit 1 if unformatted)
shfmt -d <script_path>
```

### Formatting Options

```bash
# Indentation
shfmt -i 2 <script_path>  # 2-space indent
```

## Best Practices

1. **Run shellcheck early** - Integrate into your editor and CI/CD pipeline.
2. **Fix issues, don't suppress** - Only disable warnings with a valid reason.
3. **Document suppressions** - Explain why a rule is disabled.
4. **Consistent formatting** - Use shfmt in pre-commit hooks to maintain style.

## Error Handling

### Standard Error Function

```bash
err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}
```

### Cleanup with Traps

```bash
cleanup() {
  rm -f "${tmp_file:-}"
}
trap cleanup EXIT
```

## Issue Severity Classification

When reviewing shell scripts, classify issues by severity:

| Severity | Description | Examples |
|----------|-------------|----------|
| **Critical** | Security risks, data loss potential | Command injection, unquoted variables in `rm` |
| **Important** | Correctness issues, portability problems | Missing error handling, bashisms in `/bin/sh` scripts |
| **Minor** | Style violations, readability issues | Inconsistent indentation, long lines |

## Additional Resources

For detailed patterns, edge cases, and comprehensive examples, refer to the complete style guide and anti-pattern catalog.