---
name: keypirinha-shortcuts
description: Create and manage Keypirinha shortcuts and URL files for the Shortcuts project. Use when: (1) Creating new shortcuts, (2) Adding tool shortcuts, (3) Adding website shortcuts, (4) Organizing shortcuts in the links/ directory, (5) Setting up Keypirinha integrations.
---

# Keypirinha Shortcuts

Create and manage Keypirinha shortcuts (.url files) for quick access to tools and websites.

## Shortcut File Format

Keypirinha uses standard Windows .url files:

```ini
[InternetShortcut]
URL=https://example.com
```

## Creating Shortcuts

### Web URL Shortcut

```ini
[InternetShortcut]
URL=https://github.com
```

Save as: `links/GitHub.url`

### Application Shortcut

```ini
[InternetShortcut]
URL=C:\Program Files\App\app.exe
```

Save as: `links/MyApp.url`

### File/Folder Shortcut

```ini
[InternetShortcut]
URL=C:\Users\username\Documents
```

Save as: `links/Documents.url`

## Shortcut Organization

### Directory Structure

```
links/
├── web/
│   ├── GitHub.url
│   ├── Google.url
│   └── Gmail.url
├── tools/
│   ├── VSCode.url
│   ├── Postman.url
│   └── Docker.url
└── local/
    ├── Documents.url
    └── Projects.url
```

### Naming Conventions

- Use descriptive, searchable names
- PascalCase or Title Case
- No spaces in directory names (use subdirectories)
- Extension: `.url`

## Creating Shortcuts in PowerShell

### Manual Creation

```powershell
$shortcutContent = @"
[InternetShortcut]
URL=https://github.com
"@

$shortcutPath = Join-Path (Join-Path $PSScriptRoot "links") "GitHub.url"
Set-Content -Path $shortcutPath -Value $shortcutContent
```

### Using Helper Function

```powershell
function New-KeypirinhaShortcut {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,
        
        [Parameter(Mandatory = $true)]
        [string]$Url,
        
        [Parameter(Mandatory = $false)]
        [string]$Category = ""
    )
    
    $content = @"
[InternetShortcut]
URL=$Url
"@
    
    $linksDir = Join-Path $PSScriptRoot "links"
    
    if ($Category) {
        $categoryDir = Join-Path $linksDir $Category
        if (-not (Test-Path $categoryDir)) {
            New-Item -Path $categoryDir -ItemType Directory | Out-Null
        }
        $shortcutPath = Join-Path $categoryDir "$Name.url"
    } else {
        $shortcutPath = Join-Path $linksDir "$Name.url"
    }
    
    Set-Content -Path $shortcutPath -Value $content
    Write-Information "Created shortcut: $shortcutPath"
}

# Usage
New-KeypirinhaShortcut -Name "GitHub" -Url "https://github.com" -Category "web"
```

## Refreshing Keypirinha Catalog

After creating/modifying shortcuts, users must refresh the Keypirinha catalog:

### Reminder Pattern

Always remind users after creating shortcuts:

```powershell
Write-Host "`nKeypirinha catalog refresh required:" -ForegroundColor Yellow
Write-Host "  1. Press Win+Alt+Space" -ForegroundColor Cyan
Write-Host "  2. Type 'Refresh catalog'" -ForegroundColor Cyan
Write-Host "  3. Press Enter" -ForegroundColor Cyan
Write-Host "  4. Wait a few seconds for scan to complete" -ForegroundColor Cyan
```

### In Scripts

```powershell
# After creating shortcuts
New-KeypirinhaShortcut -Name "GitHub" -Url "https://github.com"
New-KeypirinhaShortcut -Name "Gmail" -Url "https://gmail.com"

Write-Host "`nShortcuts created successfully!" -ForegroundColor Green
Write-Host "`nIMPORTANT: Refresh Keypirinha catalog to see new shortcuts" -ForegroundColor Yellow
Write-Host "Press Win+Alt+Space and type 'Refresh catalog'" -ForegroundColor Cyan
```

## Common Shortcuts

### Development Tools

```powershell
# VS Code
New-KeypirinhaShortcut -Name "VSCode" -Url "C:\Users\$env:USERNAME\scoop\apps\vscode\current\Code.exe"

# Git Bash
New-KeypirinhaShortcut -Name "GitBash" -Url "C:\Program Files\Git\git-bash.exe"

# PowerShell
New-KeypirinhaShortcut -Name "PowerShell" -Url "pwsh.exe"
```

### Websites

```powershell
# GitHub
New-KeypirinhaShortcut -Name "GitHub" -Url "https://github.com"

# Stack Overflow
New-KeypirinhaShortcut -Name "StackOverflow" -Url "https://stackoverflow.com"

# Documentation
New-KeypirinhaShortcut -Name "PowerShellDocs" -Url "https://docs.microsoft.com/powershell"
```

### Local Folders

```powershell
# Projects
New-KeypirinhaShortcut -Name "Projects" -Url "C:\Users\$env:USERNAME\Projects"

# Downloads
New-KeypirinhaShortcut -Name "Downloads" -Url "C:\Users\$env:USERNAME\Downloads"
```

## Shortcut Templates

See `assets/shortcut-template.url` for a template file.

## Best Practices

1. **Descriptive names** - Use clear, searchable names
2. **Organize by category** - Use subdirectories for organization
3. **Test shortcuts** - Verify URLs/paths are correct
4. **Remind users to refresh** - Always include refresh reminder
5. **Use environment variables** - For user-specific paths (`$env:USERNAME`)
6. **Document shortcuts** - Comment complex shortcuts
7. **Validate paths** - Check paths exist before creating shortcuts

## Interactive Shortcut Creator

```powershell
#Requires -Version 5.1

. "$PSScriptRoot\tools\pslib\utils\utils.ps1"

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$name = Read-Host "Shortcut name"
$url = Read-Host "URL or path"
$category = Read-Host "Category (optional, press Enter to skip)"

New-KeypirinhaShortcut -Name $name -Url $url -Category $category

Write-Host "`nShortcut created!" -ForegroundColor Green
Write-Host "Remember to refresh Keypirinha catalog" -ForegroundColor Yellow
```

## Batch Shortcut Creation

```powershell
$shortcuts = @(
    @{ Name = "GitHub"; Url = "https://github.com"; Category = "web" }
    @{ Name = "Gmail"; Url = "https://gmail.com"; Category = "web" }
    @{ Name = "VSCode"; Url = "code"; Category = "tools" }
)

foreach ($shortcut in $shortcuts) {
    New-KeypirinhaShortcut @shortcut
}

Write-Host "`nAll shortcuts created!" -ForegroundColor Green
Write-Host "Refresh Keypirinha catalog to see them" -ForegroundColor Yellow
```
