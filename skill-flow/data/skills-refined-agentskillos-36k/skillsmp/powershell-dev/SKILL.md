---
name: powershell-dev
description: Streamline PowerShell development following Shortcuts project conventions. Use when: (1) Implementing new PowerShell functions or scripts, (2) Modifying existing PowerShell code, (3) Creating executable scripts with .bat wrappers, (4) Working with pslib library functions, (5) Setting up error handling and CI/interactive awareness, (6) Structuring PowerShell scripts with proper templates.
---

# PowerShell Development

Streamline PowerShell development following Shortcuts project conventions including TDD, pslib usage, error handling, and script structure.

## Pre-Implementation Checklist

Before writing any PowerShell code:

1. **Check pslib for existing utilities** - Search `tools/pslib/` for similar functionality
   - Read library files in `tools/pslib/utils/` and `tools/pslib/wsl/`
   - Check function documentation (synopsis and examples)
   - Look at test files (`*.Tests.ps1`) for usage patterns
   - See [pslib-quick-reference.md](references/pslib-quick-reference.md) for available functions

2. **Understand the requirement** - Is this a new function, script, or modification?

3. **Plan the approach** - Identify reusable components and dependencies

## Development Workflow

### 1. Write Tests First (TDD)

Create the test file before implementation:

```powershell
# For new function in tools/pslib/utils/utils.ps1
# Create: tools/pslib/utils.Tests.ps1 (or edit existing)

Describe "New-FunctionName" {
    Context "When given valid input" {
        It "Should return expected result" {
            $result = New-FunctionName -Parameter "test"
            $result | Should -Be "expected"
        }
    }

    Context "When given invalid input" {
        It "Should throw error" {
            { New-FunctionName -Parameter $null } | Should -Throw
        }
    }
}
```

### 2. Implement the Function/Script

Follow the standard script structure:

```powershell
#Requires -Version 5.1

<#
.SYNOPSIS
    Brief description

.DESCRIPTION
    Detailed description

.PARAMETER ParameterName
    Description of parameter

.EXAMPLE
    New-FunctionName -Parameter "value"
    Description of example

.NOTES
    Author: [Your name or "Generated with Claude Code"]
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $false)]
    [string]$Parameter = "default"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$InformationPreference = 'Continue'

# Source dependencies if needed
. "$PSScriptRoot\tools\pslib\utils\utils.ps1"

# Helper functions (private to script)
function Private-Helper {
    param([string]$Value)
    # Implementation
}

# Main logic
try {
    # Implementation here

    # Use pslib functions
    Invoke-CommandLine -Command "scoop list" -StopAtError

    # CI/Interactive awareness
    if (Test-RunningInCIorTestEnvironment) {
        # Non-interactive path
        $confirm = $true
    } else {
        # Interactive path
        $confirm = Get-UserConfirmation "Proceed?"
    }

} catch {
    Write-Error "Error: $_"
    exit 1
}
```

### 3. Key Patterns

**Error Handling:**
- Always use `Set-StrictMode -Version Latest`
- Set `$ErrorActionPreference = 'Stop'`
- Set `$InformationPreference = 'Continue'`
- Wrap main logic in try/catch

**External Commands:**
- Always use `Invoke-CommandLine` from pslib
- Never use direct command execution

```powershell
# Good
Invoke-CommandLine -Command "scoop install nodejs" -StopAtError

# Bad
& scoop install nodejs
```

**Path Handling:**
- Use `Join-Path` for combining paths
- Validate paths with `Test-Path`
- Use `$PSScriptRoot` for relative paths

**Environment Awareness:**
```powershell
if (Test-RunningInCIorTestEnvironment) {
    # Non-interactive: use defaults
} else {
    # Interactive: prompt user
}
```

### 4. Create .bat Wrapper (for executable scripts)

For scripts meant to be run directly, create a .bat wrapper:

```batch
@echo off
pwsh -ExecutionPolicy Bypass -File "%~dp0script-name.ps1" %*
```

Save as `script-name.bat` in the same directory.

### 5. Run Tests

```bash
# Unit tests (fast feedback)
pwsh -File ".\test\bin\testrunner.ps1" -Unit

# Integration tests (if you modified integration points)
pwsh -File ".\test\bin\testrunner.ps1" -Integration

# All tests
pwsh -File ".\test\bin\testrunner.ps1"
```

### 6. Verify PowerShell 5.1 Compatibility

Test on PowerShell 5.1:

```bash
powershell -File ".\test\bin\testrunner.ps1"
```

Avoid PowerShell 6.0+ features:
- `ErrorMessage` in `ValidateScript`
- Ternary operator `? :`
- Null-coalescing `??`, `??=`

## Common Tasks

### Creating a New Function in pslib

1. Check if similar function exists
2. Write tests in appropriate `*.Tests.ps1` file
3. Implement function in `tools/pslib/utils/utils.ps1` or `tools/pslib/wsl/wsl.ps1`
4. Run unit tests
5. Commit test and implementation together

### Modifying Existing Function

**CRITICAL: Never modify implementation without updating tests!**

1. Read tests first to understand current behavior
2. Update tests to expect new behavior (Red phase)
3. Run tests - confirm they fail
4. Modify implementation (Green phase)
5. Run tests - confirm they pass
6. Commit test and implementation together

### Creating Executable Script

1. Create `script-name.ps1` with standard structure
2. Create `script-name.bat` wrapper
3. Create `script-name.Tests.ps1` for tests
4. Implement and test
5. Update `AGENTS.md` if it's a new pattern

## Pre-Commit Checklist

Before every commit:

- [ ] All unit tests pass: `pwsh -File ".\test\bin\testrunner.ps1" -Unit`
- [ ] Integration tests pass (if modified): `pwsh -File ".\test\bin\testrunner.ps1" -Integration`
- [ ] Tests and implementation committed together
- [ ] PowerShell 5.1 compatible (no 6.0+ features)
- [ ] PSScriptAnalyzer passes (runs automatically with tests)

## Resources

### scripts/

Contains helper scripts for PowerShell development:

- `create-function-scaffold.ps1` - Scaffold new function with test file
- `validate-ps-script.ps1` - Validate script compliance with project standards

### references/

Detailed reference documentation:

- `pslib-quick-reference.md` - Quick reference of pslib functions
- `testing-patterns.md` - Common Pester testing patterns
- `error-handling.md` - Error handling best practices
- `ci-interactive.md` - CI vs interactive environment patterns

See these files for in-depth examples and patterns.
