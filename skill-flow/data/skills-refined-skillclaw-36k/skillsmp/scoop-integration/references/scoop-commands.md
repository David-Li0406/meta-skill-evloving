# Scoop Commands Reference

Comprehensive reference for Scoop commands used in this project.

## Package Management

### Install
```powershell
scoop install <app>           # Install app
scoop install <app>@<version> # Install specific version
scoop install --global <app>  # Install globally (requires admin)
```

### Uninstall
```powershell
scoop uninstall <app>          # Uninstall app
scoop uninstall <app> --purge  # Uninstall and remove persist data
```

### Update
```powershell
scoop update              # Update Scoop itself
scoop update <app>        # Update specific app
scoop update *            # Update all apps
scoop update --global *   # Update all global apps
```

### List
```powershell
scoop list                # List installed apps
scoop list <app>          # Check if specific app is installed
```

### Search
```powershell
scoop search <app>        # Search for app in known buckets
scoop search               # List all available apps
```

### Info
```powershell
scoop info <app>          # Show app information
scoop cat <app>           # Show app manifest
```

## Buckets

### Add Bucket
```powershell
scoop bucket add <name>   # Add known bucket
scoop bucket add <name> <url>  # Add custom bucket
```

Common buckets:
- `main` - Default bucket (always available)
- `extras` - Additional apps
- `versions` - Apps with version selection
- `java` - Java SDKs
- `nerd-fonts` - Programming fonts

### List Buckets
```powershell
scoop bucket list         # List added buckets
scoop bucket known        # List all known buckets
```

### Remove Bucket
```powershell
scoop bucket rm <name>    # Remove bucket
```

## Cleanup

```powershell
scoop cleanup <app>       # Remove old versions of app
scoop cleanup *           # Remove old versions of all apps
scoop cleanup --all       # Remove all old versions and cache
scoop cache rm <app>      # Remove cached download for app
scoop cache rm *          # Remove all cached downloads
```

## Status

```powershell
scoop status              # Check for updates
scoop checkup             # Run scoop self-diagnostic
scoop home <app>          # Open app homepage
```

## Working with Manifests

```powershell
scoop cat <app>           # Show app manifest
scoop download <app>      # Download app (don't install)
scoop which <app>         # Show path to app executable
```

## Global Apps

```powershell
scoop install --global <app>  # Install for all users (admin)
scoop uninstall --global <app>  # Uninstall global app
scoop list --global       # List global apps
```

## Usage in Scripts

### Always use Invoke-CommandLine

```powershell
# Good
Invoke-CommandLine -Command "scoop install nodejs" -StopAtError

# Bad
scoop install nodejs
& scoop install nodejs
```

### Check Installation Status

```powershell
$result = Invoke-CommandLine -Command "scoop list nodejs"
$isInstalled = $result -match "nodejs"
```

### Silent Installation

```powershell
Invoke-CommandLine -Command "scoop install nodejs" -Silent -StopAtError
```

## Common Patterns

### Install if Not Already Installed

```powershell
$result = Invoke-CommandLine -Command "scoop list nodejs"
if ($result -notmatch "nodejs") {
    Write-Information "Installing nodejs..."
    Invoke-CommandLine -Command "scoop install nodejs" -StopAtError
} else {
    Write-Information "nodejs already installed"
}
```

### Install Multiple Packages

```powershell
$packages = @("git", "nodejs", "python", "vscode")
foreach ($pkg in $packages) {
    Write-Information "Installing $pkg..."
    Invoke-CommandLine -Command "scoop install $pkg" -StopAtError
}
```

### Add Bucket Before Install

```powershell
# Keypirinha is in extras bucket
Invoke-CommandLine -Command "scoop bucket add extras" -StopAtError
Invoke-CommandLine -Command "scoop install keypirinha" -StopAtError
```

### Update with Error Handling

```powershell
try {
    Invoke-CommandLine -Command "scoop update" -StopAtError
    Invoke-CommandLine -Command "scoop update *" -StopAtError
    Write-Information "All packages updated"
} catch {
    Write-Warning "Update failed: $_"
    Write-Information "Continuing with installation..."
}
```

## Project-Specific Usage

### scoopfile.json Apps

Main apps tracked in scoopfile.json:
- `git` - Version control
- `keypirinha` - Keyboard launcher
- `pwsh` - PowerShell Core (optional)

### Installation Order

1. Install Scoop (if not installed)
2. Add required buckets (extras for Keypirinha)
3. Install base packages (git)
4. Install Keypirinha
5. Install optional tools (pwsh, nodejs, python, etc.)

### Post-Installation

After installing apps:
1. Refresh Keypirinha catalog
2. Verify installation with `scoop list`
3. Test app launches
