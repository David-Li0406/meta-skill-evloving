# Dependencies Installation Script (Windows PowerShell)

# Exit on error
$ErrorActionPreference = "Stop"

# Get the script's directory and navigate to project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "../../../..")

# Navigate to the API directory
$ApiDir = Join-Path $ProjectRoot "apps/api"
Set-Location $ApiDir

# Check if bun is installed
if (-not (Get-Command bun -ErrorAction SilentlyContinue)) {
    Write-Error "Error: bun is not installed or not in PATH"
    Write-Host "Please install bun from https://bun.sh"
    exit 1
}

# Check if package.json exists
if (-not (Test-Path "package.json")) {
    Write-Error "Error: package.json not found in apps/api"
    exit 1
}

# Run installation
Write-Host "Installing dependencies in apps/api..."
Write-Host "Running: bun install"
Write-Host ""
bun install

# Verify installation
if (Test-Path "node_modules") {
    Write-Host ""
    Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Warning "Warning: node_modules directory not found after installation"
    exit 1
}

exit 0
