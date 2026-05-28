# AI Agent Patterns for PowerShell Testing

When executing PowerShell test commands through a Bash tool (Claude Code, GitHub Actions, etc.), follow these patterns.

## Path Quoting Rules

**ALWAYS quote file paths** when calling PowerShell through bash. Windows paths contain backslashes which must be properly escaped.

### Correct Usage

```bash
# PowerShell 7.x - quote the entire path
pwsh -File ".\test\bin\testrunner.ps1"
pwsh -File ".\test\bin\testrunner.ps1" -Coverage

# PowerShell 5.1 - quote the entire path
powershell -File ".\test\bin\testrunner.ps1"

# Running specific test files
pwsh -Command "Invoke-Pester -Path '.\tools\pslib\utils.Tests.ps1'"
```

### Incorrect Usage (Will Fail)

```bash
# Missing quotes - WRONG
pwsh -File .\test\bin\testrunner.ps1

# Backslashes not handled properly - WRONG
pwsh -File .testsbintestrunner.ps1
```

## PowerShell Version Selection

| Command | Version | When to Use |
|---------|---------|-------------|
| `pwsh` | PowerShell 7.x | Default, modern features |
| `powershell` | PowerShell 5.1 | Compatibility testing |

## PowerShell Piping Rules

**CRITICAL:** When using PowerShell cmdlets or piping, execute the entire pipeline within PowerShell using `-Command`, NOT by piping in bash.

### The Problem

When piping PowerShell output to a PowerShell cmdlet, the pipe happens in **bash context**, not PowerShell. Bash doesn't know about `Select-String`, `Where-Object`, etc.

### Incorrect (Will Fail)

```bash
# Tries to pipe in BASH, not PowerShell - WRONG
pwsh -File ".\test\bin\testrunner.ps1" | Select-String -Pattern "Error"
```

### Correct

```bash
# Option 1: Use -Command for entire pipeline
pwsh -Command ".\test\bin\testrunner.ps1 | Select-String -Pattern 'Error'"

# Option 2: Use bash tools for filtering
pwsh -File ".\test\bin\testrunner.ps1" | grep "Error"
```

### Cmdlets That MUST Be Inside `-Command`

- `Select-String`
- `Where-Object`
- `Select-Object`
- `ForEach-Object`
- `Measure-Object`
- Any PowerShell-specific cmdlet

## Common Test Commands via Bash

```bash
# Local development (recommended workflow):
# Step 1: Unit tests first (faster feedback)
pwsh -File ".\test\bin\testrunner.ps1" -Unit

# Step 2: Integration tests afterwards
pwsh -File ".\test\bin\testrunner.ps1" -Integration

# CI - Run all tests
pwsh -File ".\test\bin\testrunner.ps1"

# With coverage
pwsh -File ".\test\bin\testrunner.ps1" -Coverage
pwsh -File ".\test\bin\testrunner.ps1" -Unit -Coverage
pwsh -File ".\test\bin\testrunner.ps1" -Integration -Coverage

# Specific test file (PowerShell 7.x)
pwsh -File ".\test\bin\testrunner.ps1" -TestPath "tools\pslib\utils\utils.Tests.ps1"

# Specific test file (PowerShell 5.1)
powershell -File ".\test\bin\testrunner.ps1" -TestPath "tools\pslib\utils\utils.Tests.ps1"

# Run linter checks
pwsh -File ".\test\bin\linter.Tests.ps1"

# Check PowerShell version
pwsh -Command "$PSVersionTable.PSVersion"
```

## Error Prevention Checklist

1. **Always use double quotes** around file paths with `-File`
2. **Use single quotes inside double quotes** with `-Command` parameter
3. **NEVER pipe PowerShell cmdlets in bash** - use `-Command` for pipelines
4. **Verify path exists** before executing if unsure
5. **Check backslash handling** - if backslashes disappear, improve quoting

## Example Workflow in AI Agent

```text
# Step 1: Verify test script exists
Bash(Test-Path ".\test\bin\testrunner.ps1")

# Step 2: Run tests with proper quoting
Bash(pwsh -File ".\test\bin\testrunner.ps1")
```

## Handling Test Output

### Reading Test Results

```bash
# Read JUnit XML results
cat test/out/junit.xml

# Read coverage report
cat test/out/coverage.xml

# Read markdown summary
cat test/out/test-summary.md
```

### Parsing Test Output

Use bash tools (not PowerShell cmdlets) for filtering output:

```bash
# Filter for errors using grep (bash)
pwsh -File ".\test\bin\testrunner.ps1" 2>&1 | grep -i "error"

# Filter for failed tests
pwsh -File ".\test\bin\testrunner.ps1" 2>&1 | grep -i "failed"
```
