# CI vs Interactive Environment Patterns

Guide for writing scripts that work correctly in both CI and interactive environments.

## Detection

### Test-RunningInCIorTestEnvironment

Located in: `tools/pslib/utils/utils.ps1`

Automatically detects:
- CI environment variables (CI, GITHUB_ACTIONS, TF_BUILD, etc.)
- Pester test context

Usage:
```powershell
. "$PSScriptRoot\tools\pslib\utils\utils.ps1"

if (Test-RunningInCIorTestEnvironment) {
    # Non-interactive path
} else {
    # Interactive path
}
```

## Common Patterns

### User Confirmation

```powershell
if (Test-RunningInCIorTestEnvironment) {
    $proceed = $true
    Write-Information "Auto-confirming in CI mode"
} else {
    $response = Read-Host "Proceed with installation? (y/n)"
    $proceed = $response -eq "y"
}

if ($proceed) {
    # Continue
}
```

### Using Get-UserConfirmation

Better approach using helper function:

```powershell
$proceed = Get-UserConfirmation -Prompt "Proceed with installation?"

if ($proceed) {
    # Continue
}
```

### Input Parameters

```powershell
if (Test-RunningInCIorTestEnvironment) {
    # Use defaults or environment variables
    $targetPath = $env:INSTALL_PATH
    if (-not $targetPath) {
        $targetPath = "C:\Default\Path"
    }
} else {
    # Prompt user
    $targetPath = Read-Host "Enter installation path"
    if ([string]::IsNullOrWhiteSpace($targetPath)) {
        $targetPath = "C:\Default\Path"
    }
}
```

### Output Verbosity

```powershell
if (Test-RunningInCIorTestEnvironment) {
    # More verbose logging for CI
    Write-Information "Step 1: Checking prerequisites"
    Write-Information "Step 2: Downloading files"
    Write-Information "Step 3: Installing"
} else {
    # Concise output for interactive
    Write-Host "Installing..." -ForegroundColor Cyan
}
```

## Testing

### Test Both Paths

```powershell
Describe "Installation Script" {
    Context "When running in CI" {
        BeforeEach {
            Mock Test-RunningInCIorTestEnvironment { return $true }
        }
        
        It "Should use default path" {
            # Test automated path
        }
    }
    
    Context "When running interactively" {
        BeforeEach {
            Mock Test-RunningInCIorTestEnvironment { return $false }
            Mock Read-Host { return "C:\Custom\Path" }
        }
        
        It "Should prompt for path" {
            # Test interactive path
        }
    }
}
```

### Simulate CI Environment

For manual testing:

```bash
# Simulate CI
CI=true pwsh -File script.ps1

# Normal interactive
pwsh -File script.ps1
```

## Best Practices

1. Always handle both CI and interactive modes
2. Provide sensible defaults for CI mode
3. Use Get-UserConfirmation for yes/no questions
4. Test both code paths
5. Use Write-Information for CI logging
6. Avoid Read-Host in pure CI scripts
7. Document required environment variables
8. Fail fast if required inputs are missing

## Examples

### Installation Script

```powershell
. "$PSScriptRoot\tools\pslib\utils\utils.ps1"

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

try {
    if (Test-RunningInCIorTestEnvironment) {
        $installPath = $env:INSTALL_PATH
        if (-not $installPath) {
            $installPath = "C:\Tools"
        }
        $confirm = $true
    } else {
        $installPath = Read-Host "Enter installation path (default: C:\Tools)"
        if ([string]::IsNullOrWhiteSpace($installPath)) {
            $installPath = "C:\Tools"
        }
        $confirm = Get-UserConfirmation "Install to $installPath?"
    }
    
    if ($confirm) {
        New-Directory -Path $installPath
        Invoke-CommandLine -Command "scoop install app" -StopAtError
        Write-Information "Installation complete"
    }
} catch {
    Write-Error "Installation failed: $_"
    exit 1
}
```

### Configuration Script

```powershell
. "$PSScriptRoot\tools\pslib\utils\utils.ps1"

if (Test-RunningInCIorTestEnvironment) {
    $config = @{
        Server   = $env:SERVER_URL
        Port     = $env:SERVER_PORT
        UseSSL   = $true
        Timeout  = 30
    }
} else {
    $config = @{
        Server   = Read-Host "Server URL"
        Port     = Read-Host "Server Port"
        UseSSL   = (Get-UserConfirmation "Use SSL?")
        Timeout  = 30
    }
}

# Validate configuration
if ([string]::IsNullOrWhiteSpace($config.Server)) {
    Write-Error "Server URL is required"
    exit 1
}
```
