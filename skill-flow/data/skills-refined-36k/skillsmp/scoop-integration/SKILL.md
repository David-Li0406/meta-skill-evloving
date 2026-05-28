---
name: scoop-integration
description: Manage Scoop package integration and dependencies in the Shortcuts project. Use when: (1) Installing or managing Scoop packages, (2) Creating tool installers, (3) Updating scoopfile.json, (4) Checking if Scoop is installed, (5) Working with package dependencies. Always use Invoke-CommandLine for Scoop commands.
---

# Scoop Integration

Manage Scoop package manager integration for Windows tool installation.

## Prerequisites Check

Always verify Scoop is installed before using it:

```powershell
# Check if Scoop is installed
if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
    Write-Error "Scoop is not installed. Install from https://scoop.sh"
    exit 1
}
```

## Common Scoop Operations

### Install Package

```powershell
. "$PSScriptRoot\tools\pslib\utils\utils.ps1"

# Install a package
Invoke-CommandLine -Command "scoop install nodejs" -StopAtError

# Install multiple packages
$packages = @("git", "nodejs", "python")
foreach ($pkg in $packages) {
    Invoke-CommandLine -Command "scoop install $pkg" -StopAtError
}
```

### Update Packages

```powershell
# Update Scoop itself
Invoke-CommandLine -Command "scoop update" -StopAtError

# Update all packages
Invoke-CommandLine -Command "scoop update *" -StopAtError

# Update specific package
Invoke-CommandLine -Command "scoop update nodejs" -StopAtError
```

### Check if Package is Installed

```powershell
$result = Invoke-CommandLine -Command "scoop list nodejs"
if ($result -match "nodejs") {
    Write-Information "nodejs is installed"
} else {
    Write-Information "nodejs is not installed"
}
```

### Uninstall Package

```powershell
Invoke-CommandLine -Command "scoop uninstall nodejs" -StopAtError
```

## scoopfile.json Management

The project uses `scoopfile.json` to track managed packages.

### Structure

```json
{
  "apps": [
    {
      "Source": "main",
      "Name": "git"
    },
    {
      "Source": "extras",
      "Name": "keypirinha"
    }
  ]
}
```

### Reading scoopfile.json

```powershell
$scoopfilePath = Join-Path $PSScriptRoot "scoopfile.json"
if (Test-Path $scoopfilePath) {
    $scoopfile = Get-Content $scoopfilePath | ConvertFrom-Json
    $apps = $scoopfile.apps
}
```

### Adding to scoopfile.json

```powershell
$scoopfilePath = "scoopfile.json"
$scoopfile = Get-Content $scoopfilePath | ConvertFrom-Json

# Add new app
$newApp = @{
    Source = "main"
    Name = "nodejs"
}
$scoopfile.apps += $newApp

# Save back
$scoopfile | ConvertTo-Json -Depth 10 | Set-Content $scoopfilePath
```

## Adding Scoop Buckets

```powershell
# Add extras bucket
Invoke-CommandLine -Command "scoop bucket add extras" -StopAtError

# Add other buckets
Invoke-CommandLine -Command "scoop bucket add versions" -StopAtError
Invoke-CommandLine -Command "scoop bucket add java" -StopAtError
```

## Installation Script Pattern

```powershell
#Requires -Version 5.1

<#
.SYNOPSIS
    Install development tools via Scoop

.DESCRIPTION
    Installs required development tools using Scoop package manager
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$InformationPreference = 'Continue'

. "$PSScriptRoot\..\tools\pslib\utils\utils.ps1"

try {
    # Check if Scoop is installed
    if (-not (Get-Command scoop -ErrorAction SilentlyContinue)) {
        Write-Error "Scoop is required but not installed. Please install Scoop first."
        exit 1
    }
    
    # List of packages to install
    $packages = @("git", "nodejs", "python")
    
    Write-Information "Installing packages via Scoop..."
    
    foreach ($package in $packages) {
        Write-Information "Installing $package..."
        Invoke-CommandLine -Command "scoop install $package" -StopAtError
    }
    
    Write-Information "All packages installed successfully"
    
} catch {
    Write-Error "Installation failed: $_"
    exit 1
}
```

## Common Scoop Commands Reference

See [scoop-commands.md](references/scoop-commands.md) for detailed command reference.

## Best Practices

1. **Always use Invoke-CommandLine** - Never call scoop directly
2. **Check if Scoop exists** - Verify installation before use
3. **Handle errors** - Use -StopAtError flag
4. **Update regularly** - Keep packages up to date
5. **Track in scoopfile.json** - Document managed packages
6. **Test on clean system** - Ensure installer works from scratch
7. **Add required buckets** - Some apps need extras/versions buckets

## Integration with Keypirinha

After installing new apps:

```powershell
Write-Host "Remember to refresh Keypirinha catalog:" -ForegroundColor Yellow
Write-Host "  1. Press Win+Alt+Space" -ForegroundColor Yellow
Write-Host "  2. Type 'Refresh catalog'" -ForegroundColor Yellow
Write-Host "  3. Press Enter" -ForegroundColor Yellow
```
