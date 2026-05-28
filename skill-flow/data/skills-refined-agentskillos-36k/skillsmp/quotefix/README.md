# Quotefix Skill

A Claude Code skill that automatically detects shell environments (PowerShell, Bash, Zsh, Fish, CMD) and provides correct quoting and escaping syntax for cross-shell command execution.

## Features

- **Shell Detection**: Automatically detects Bash, Zsh, Fish, PowerShell, CMD, and other shells
- **Quoting Rules**: Applies correct quoting rules for each shell type
- **Escape Characters**: Uses the right escape sequences (\ vs ` vs ^)
- **Nested Command Handling**: Handles SSH, Docker, and cross-shell command nesting
- **PowerShell-specific patterns**: Here-strings, stop-parsing token, and special operators

## Installation

This skill is already installed in your project at:
```
.claude/skills/quotefix/
```

Claude Code will automatically detect and use this skill when relevant.

## When This Skill Activates

The skill will be used automatically when:
- Executing shell commands that differ between shells
- Working with file paths containing spaces or special characters
- Handling nested commands (SSH, Docker, remote execution)
- Writing cross-platform scripts
- Dealing with PowerShell-specific syntax requirements

## File Structure

```
quotefix/
├── SKILL.md      # Main skill definition with detection logic
├── examples.md   # Practical examples and use cases
└── README.md     # This file
```

## Quick Start Examples

### Detect Current Shell (Bash)

```bash
# Method 1: Check environment variable
echo $SHELL

# Method 2: Check running process
ps -p $$ -o comm=

# Method 3: Check version variables
if [ -n "$BASH_VERSION" ]; then echo "bash"; fi
```

### Detect Current Shell (PowerShell)

```powershell
# Check PowerShell version
$PSVersionTable.PSVersion

# Check if running in PowerShell
if ($PSVersionTable) { Write-Host "PowerShell" }
```

### PowerShell Quoting Examples

**Using Backtick for Escaping:**
```powershell
# Escape special characters
Write-Host "Line 1`nLine 2"  # Newline
Write-Host "Tab`tSeparated"  # Tab
$path = "C:\`$temp\`"quoted`" folder"  # Escape $ and quotes
```

**Using Here-Strings:**
```powershell
# Single-quoted here-string (literal)
$text = @'
Everything in here is literal
$variables are not expanded
"Quotes" work without escaping
'@

# Double-quoted here-string (with expansion)
$name = "World"
$text = @"
Hello, $name!
Variables are expanded here
"@
```

**Using Stop-Parsing Token:**
```powershell
# Everything after --% is treated literally
icacls C:\path\to\file --% /grant *S-1-1-0:(OI)(CI)F
```

### Nested Command Examples

**SSH with Bash:**
```bash
# Simple nested command
ssh user@host 'echo "Hello from remote"'

# Double nesting
ssh user@host "bash -c 'echo \"Nested quotes\"'"

# With variables
var="test"
ssh user@host "echo \"Value: $var\""
```

**SSH from PowerShell:**
```powershell
# Simple nested command
ssh user@host 'echo "Hello from remote"'

# Double nesting with backtick escaping
ssh user@host "bash -c 'echo \`"Nested quotes\`"'"

# With variables
$var = "test"
ssh user@host "echo \`"Value: $var\`""
```

**Docker Exec:**
```bash
# Bash to Docker
docker exec container bash -c 'echo "Inside container"'

# PowerShell to Docker
docker exec container bash -c "echo `"Inside container`""
```

## Quoting Quick Reference

### Basic Quoting Rules

| Shell | Variable Expansion | Literal String | Escape Char |
|-------|-------------------|----------------|-------------|
| Bash/Zsh | `"$var"` | `'literal'` | `\` |
| PowerShell | `"$var"` | `'literal'` | `` ` `` |
| CMD | `%var%` | N/A | `^` |
| Fish | `"$var"` | `'literal'` | N/A (use quotes) |

### Escape Character Usage

| Shell | Newline | Tab | Quote | Dollar Sign |
|-------|---------|-----|-------|-------------|
| Bash | `\n` | `\t` | `\"` or `\'` | `\$` |
| PowerShell | `` `n `` | `` `t `` | `` `" `` or `'` | `` `$ `` |
| CMD | N/A | N/A | `^"` | N/A |

### PowerShell Special Operators

| Operator | Purpose | Example |
|----------|---------|---------|
| `` ` `` | Escape character | `` `n ``, `` `t ``, `` `$ `` |
| `@' ... '@` | Single-quoted here-string | Literal multi-line text |
| `@" ... "@` | Double-quoted here-string | Expanding multi-line text |
| `--%` | Stop-parsing token | Legacy command compatibility |
| `$( )` | Subexpression | `"Result: $(Get-Date)"` |
| `@( )` | Array subexpression | `$items = @(Get-ChildItem)` |

## Cross-Shell Compatibility Patterns

### Bash to PowerShell

```bash
# Bash
echo "Path: /home/user/My Documents"
var="test"
echo "Value: $var"
```

```powershell
# PowerShell equivalent
Write-Host "Path: C:\Users\user\My Documents"
$var = "test"
Write-Host "Value: $var"
```

### PowerShell to Bash

```powershell
# PowerShell
Get-Content "file with spaces.txt" | Where-Object { $_ -match "pattern" }
```

```bash
# Bash equivalent
grep "pattern" "file with spaces.txt"
```

### CMD to PowerShell

```cmd
REM CMD
set VAR=value
echo %VAR%
```

```powershell
# PowerShell equivalent
$env:VAR = "value"
Write-Host $env:VAR
```

## Common Pitfalls

1. **Not quoting variables**: Always use `"$var"` in Bash to prevent word splitting
2. **Wrong escape character**: Bash uses `\`, PowerShell uses `` ` ``, CMD uses `^`
3. **Nested quote confusion**: Each shell layer requires its own escaping strategy
4. **PowerShell string interpolation**: Use `'literal'` to prevent expansion, `"$var"` to allow it
5. **Cross-shell assumptions**: PowerShell and Bash have fundamentally different quoting models

## Platform-Specific Path Separators

- **Unix/Linux/macOS**: `/` (forward slash)
- **Windows CMD**: `\` (backslash)
- **PowerShell**: Both `/` and `\` work (PowerShell normalizes them)

## Testing the Skill

Create a test script to verify the skill works:

**Bash:**
```bash
# test_skill.sh
#!/usr/bin/env bash

echo "Testing Quotefix..."

# Test 1: Shell detection
if [ -n "$BASH_VERSION" ]; then
    echo "✓ Detected Bash"
fi

# Test 2: Nested quoting
result=$(echo "Outer 'inner' quotes")
echo "✓ Nested quotes work: $result"

# Test 3: Escaping
echo "Line 1\nLine 2"
echo "✓ Escape sequences work"
```

**PowerShell:**
```powershell
# test_skill.ps1
Write-Host "Testing Quotefix..."

# Test 1: Shell detection
if ($PSVersionTable) {
    Write-Host "✓ Detected PowerShell"
}

# Test 2: Nested quoting
$result = "Outer 'inner' quotes"
Write-Host "✓ Nested quotes work: $result"

# Test 3: Escaping
Write-Host "Line 1`nLine 2"
Write-Host "✓ Escape sequences work"
```

## See Also

- [SKILL.md](./SKILL.md) - Complete skill definition
- [examples.md](./examples.md) - Detailed examples
- [Claude Code Documentation](https://github.com/anthropics/claude-code)

## License

This skill is part of the havok-training project.

## Contributing

To improve this skill:
1. Edit `SKILL.md` for skill behavior
2. Add examples to `examples.md`
3. Update this README with any new features
4. Test on multiple platforms and shells

## Support

For issues or questions:
- Check the [examples.md](./examples.md) file
- Review the [SKILL.md](./SKILL.md) documentation
- Refer to Claude Code documentation

---

**Created for**: havok-training project
**Branch**: claude/detect-shell-environment-G4vQY
**Purpose**: Cross-platform shell command compatibility
