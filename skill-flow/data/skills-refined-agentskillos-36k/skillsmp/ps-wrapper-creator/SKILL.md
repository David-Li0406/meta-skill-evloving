---
name: ps-wrapper-creator
description: Create .bat wrappers for PowerShell scripts following project conventions. Use when: (1) Creating executable PowerShell scripts, (2) Making scripts launchable from command line, (3) Making scripts accessible from Keypirinha, (4) Following the PowerShell Script Wrapper Convention documented in AGENTS.md.
---

# PowerShell Script Wrapper Creator

Create .bat wrappers for PowerShell scripts to make them easily executable.

## The Wrapper Convention

Executable PowerShell scripts should have a .bat wrapper in the same directory.

### Benefits

- Users can run `script-name` instead of `pwsh -File path/to/script-name.ps1`
- Batch wrapper handles PowerShell execution policy automatically
- Arguments are passed through automatically via `%*`
- Consistent user experience across all executable scripts
- Works with Keypirinha launcher

## Wrapper Template

```batch
@echo off
pwsh -ExecutionPolicy Bypass -File "%~dp0script-name.ps1" %*
```

### Template Breakdown

- `@echo off` - Suppress command echoing
- `pwsh` - Use PowerShell 7.x (use `powershell` for 5.1 only)
- `-ExecutionPolicy Bypass` - Run without policy restrictions
- `-File` - Execute script file
- `"%~dp0script-name.ps1"` - Path to PS1 file in same directory
- `%*` - Pass all arguments to PowerShell script

## Creating Wrappers

### Manual Creation

1. Create the PowerShell script: `my-script.ps1`
2. Create the wrapper: `my-script.bat`
3. Use the template, replacing `script-name` with `my-script`

### Example Structure

```
tools/pslib/wsl/
├── wsl-manager.ps1      # PowerShell script
└── wsl-manager.bat      # Wrapper
```

Wrapper content:
```batch
@echo off
pwsh -ExecutionPolicy Bypass -File "%~dp0wsl-manager.ps1" %*
```

## PowerShell 5.1 vs 7.x

### For PowerShell 7.x Scripts

```batch
@echo off
pwsh -ExecutionPolicy Bypass -File "%~dp0script-name.ps1" %*
```

### For PowerShell 5.1 Only Scripts

```batch
@echo off
powershell -ExecutionPolicy Bypass -File "%~dp0script-name.ps1" %*
```

### For Compatible Scripts (Recommended)

Use `pwsh` by default (most users have it via Scoop), with fallback documentation:

```batch
@echo off
pwsh -ExecutionPolicy Bypass -File "%~dp0script-name.ps1" %*
```

If pwsh is not available, user can:
1. Install PowerShell 7: `scoop install pwsh`
2. Or modify wrapper to use `powershell` instead

## Automated Wrapper Creation

### PowerShell Function

```powershell
function New-BatWrapper {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory = $true)]
        [string]$ScriptPath,
        
        [Parameter(Mandatory = $false)]
        [ValidateSet("pwsh", "powershell")]
        [string]$PowerShellVersion = "pwsh"
    )
    
    # Validate script exists
    if (-not (Test-Path $ScriptPath)) {
        Write-Error "Script not found: $ScriptPath"
        return
    }
    
    # Get script name without extension
    $scriptName = [System.IO.Path]::GetFileNameWithoutExtension($ScriptPath)
    $scriptDir = Split-Path $ScriptPath -Parent
    
    # Create wrapper path
    $wrapperPath = Join-Path $scriptDir "$scriptName.bat"
    
    # Check if wrapper already exists
    if (Test-Path $wrapperPath) {
        Write-Warning "Wrapper already exists: $wrapperPath"
        $overwrite = Read-Host "Overwrite? (y/n)"
        if ($overwrite -ne "y") {
            return
        }
    }
    
    # Create wrapper content
    $wrapperContent = @"
@echo off
$PowerShellVersion -ExecutionPolicy Bypass -File "%~dp0$scriptName.ps1" %*
"@
    
    # Write wrapper
    Set-Content -Path $wrapperPath -Value $wrapperContent
    Write-Information "Created wrapper: $wrapperPath"
}

# Usage
New-BatWrapper -ScriptPath ".\tools\my-script.ps1"
```

### Batch Creation for Directory

```powershell
function New-BatWrappersForDirectory {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Directory
    )
    
    $ps1Files = Get-ChildItem -Path $Directory -Filter "*.ps1" -Recurse
    
    foreach ($ps1File in $ps1Files) {
        # Skip test files
        if ($ps1File.Name -like "*.Tests.ps1") {
            continue
        }
        
        New-BatWrapper -ScriptPath $ps1File.FullName
    }
}

# Usage
New-BatWrappersForDirectory -Directory ".\tools\pslib\wsl"
```

## When to Create Wrappers

### Create Wrapper For:

- Scripts meant to be run by users directly
- Scripts launched from command line
- Scripts accessible via Keypirinha
- Utility scripts in tools/ directory
- Management scripts (install, update, etc.)

### Don't Create Wrapper For:

- Test files (`*.Tests.ps1`)
- Library files (sourced with dot-sourcing)
- Internal helper scripts
- CI-only scripts
- Scripts in .bootstrap/ (they have their own patterns)

## Testing Wrappers

### Test from Command Line

```bash
# Test wrapper
script-name arg1 arg2

# Should be equivalent to:
pwsh -File script-name.ps1 arg1 arg2
```

### Test from Keypirinha

1. Create wrapper
2. Refresh Keypirinha catalog
3. Press Win+Alt+Space
4. Type script name
5. Press Enter

## Template Asset

See `assets/wrapper-template.bat` for a template file.

## Best Practices

1. **Same directory** - Wrapper must be in same directory as .ps1 file
2. **Same name** - Wrapper must have same name as .ps1 file (except extension)
3. **Use pwsh** - Prefer PowerShell 7.x for new scripts
4. **Pass arguments** - Always include `%*` to pass arguments
5. **Bypass execution policy** - Use `-ExecutionPolicy Bypass`
6. **Test** - Verify wrapper works before committing
7. **Commit together** - Commit .ps1 and .bat in same commit

## Troubleshooting

### Wrapper Not Found

Check:
- Wrapper is in same directory as .ps1 file
- Wrapper has correct name
- Wrapper has .bat extension

### Script Not Executing

Check:
- `%~dp0` is present (relative path to script)
- Script name matches exactly (case-sensitive on some systems)
- PowerShell version is installed (pwsh vs powershell)

### Arguments Not Passed

Check:
- `%*` is included at end of command
- Arguments are quoted if they contain spaces
