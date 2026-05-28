##############################################################################
# Quotefix Skill - Global Installer (PowerShell)
#
# Installs the skill globally to ~/.claude/skills/ so it's available
# in ALL Claude Code sessions across all projects.
#
# Usage:
#   .\install.ps1              # Install globally
#   .\install.ps1 -Uninstall   # Remove global installation
##############################################################################

[CmdletBinding()]
param(
    [switch]$Uninstall
)

# Skill name
$SkillName = "quotefix"

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Target directory (global personal skills)
$TargetDir = Join-Path $env:USERPROFILE ".claude\skills\$SkillName"

# Function to print colored messages
function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ $Message" -ForegroundColor Blue
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠ $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

# Function to install the skill
function Install-Skill {
    Write-Info "Installing Quotefix skill globally..."
    Write-Host ""

    # Create the global skills directory if it doesn't exist
    $SkillsDir = Join-Path $env:USERPROFILE ".claude\skills"
    if (-not (Test-Path $SkillsDir)) {
        New-Item -Path $SkillsDir -ItemType Directory -Force | Out-Null
        Write-Success "Created ~/.claude/skills directory"
    }

    # Check if skill already exists
    if (Test-Path $TargetDir) {
        Write-Warning "Skill already exists at $TargetDir"
        $response = Read-Host "Do you want to overwrite it? (y/N)"
        if ($response -notmatch '^[Yy]$') {
            Write-Info "Installation cancelled."
            exit 0
        }
        Remove-Item -Path $TargetDir -Recurse -Force
        Write-Success "Removed existing installation"
    }

    # Copy the skill files
    Copy-Item -Path $ScriptDir -Destination $TargetDir -Recurse -Force
    Write-Success "Copied skill files to $TargetDir"

    # Remove the install scripts from the target (we don't need them there)
    $filesToRemove = @(
        "install.sh",
        "install.ps1",
        "INSTALL.md"
    )
    foreach ($file in $filesToRemove) {
        $filePath = Join-Path $TargetDir $file
        if (Test-Path $filePath) {
            Remove-Item -Path $filePath -Force
        }
    }

    Write-Host ""
    Write-Success "Installation complete!"
    Write-Host ""
    Write-Info "The skill is now globally available in all Claude Code sessions."
    Write-Info "Location: $TargetDir"
    Write-Host ""
    Write-Info "Files installed:"
    Write-Host "  - SKILL.md     (Main skill definition)"
    Write-Host "  - examples.md  (Practical examples)"
    Write-Host "  - README.md    (Documentation)"
    Write-Host ""
    Write-Success "You can now use Claude Code in any project, and it will automatically"
    Write-Success "apply shell environment detection and nested quoting best practices!"
}

# Function to uninstall the skill
function Uninstall-Skill {
    Write-Info "Uninstalling Quotefix skill..."
    Write-Host ""

    if (-not (Test-Path $TargetDir)) {
        Write-Warning "Skill is not installed at $TargetDir"
        exit 0
    }

    Remove-Item -Path $TargetDir -Recurse -Force
    Write-Success "Removed skill from $TargetDir"
    Write-Host ""
    Write-Success "Uninstallation complete!"
}

# Main execution
if ($Uninstall) {
    Uninstall-Skill
} else {
    Install-Skill
}
