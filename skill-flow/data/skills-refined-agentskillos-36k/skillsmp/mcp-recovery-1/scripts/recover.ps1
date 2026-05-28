param(
  [string]$ProjectPath = "C:\Users\Sam\Documents\GitHub\v2_heras_garden",
  [string]$GodotExePath = "C:\Users\Sam\Documents\GitHub\v2_heras_garden\Godot_v4.5.1-stable_win64.exe\Godot_v4.5.1-stable_win64.exe",
  [int]$TimeoutSec = 15,
  [switch]$Verbose
)

$ErrorActionPreference = "Stop"

function Write-Verbose-Output {
  param([string]$Message)
  if ($Verbose) { Write-Host $Message }
}

function Get-Godot-Processes {
  Get-Process | Where-Object { $_.ProcessName -like "*Godot*" }
}

function Stop-Godot-Processes {
  $procs = Get-Godot-Processes
  if ($procs) {
    Write-Host "Stopping $($procs.Count) Godot process(es)..."
    $procs | Stop-Process -Force
    Start-Sleep -Seconds 2
  } else {
    Write-Host "No Godot processes to stop."
  }
}

function Start-Godot-Editor {
  if (-not (Test-Path $GodotExePath)) {
    throw "Godot exe not found: $GodotExePath"
  }
  Write-Host "Starting Godot editor..."
  & cmd /c start "" "$GodotExePath" --path "$ProjectPath" -e | Out-Null
}

function Wait-Port {
  param([int]$Port, [int]$WaitSec)
  $deadline = (Get-Date).AddSeconds($WaitSec)
  while ((Get-Date) -lt $deadline) {
    $conn = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    if ($conn) { return $true }
    Start-Sleep -Milliseconds 500
  }
  return $false
}

function Wait-Godot-Process {
  param([int]$WaitSec)
  $deadline = (Get-Date).AddSeconds($WaitSec)
  while ((Get-Date) -lt $deadline) {
    if (Get-Godot-Processes) { return $true }
    Start-Sleep -Milliseconds 500
  }
  return $false
}

# Main recovery flow
Write-Host "`n=== MCP Heavy Recovery ===`n"

# Step 1: Check current state
$existing = Get-Godot-Processes
Write-Host "Current Godot processes: $($existing.Count)"

if ($existing.Count -gt 1) {
  Write-Host "WARNING: Multiple Godot processes detected - this causes MCP conflicts."
}

# Step 2: Stop all Godot processes
Write-Host "`nStep 1: Stopping all Godot processes..."
Stop-Godot-Processes

# Step 3: Start Godot
Write-Host "`nStep 2: Starting Godot editor..."
Start-Godot-Editor

# Step 4: Wait for Godot process
Write-Host "Waiting for Godot process..."
if (-not (Wait-Godot-Process -WaitSec $TimeoutSec)) {
  throw "Godot process did not appear within $TimeoutSec seconds."
}
Write-Host "✓ Godot process detected."

# Step 5: Wait for MCP port
Write-Host "`nStep 3: Waiting for MCP port 9080..."
if (-not (Wait-Port -Port 9080 -WaitSec $TimeoutSec)) {
  throw "MCP port 9080 did not open within $TimeoutSec seconds."
}
Write-Host "✓ MCP port 9080 is listening."

# Step 6: Verify MCP CLI
Write-Host "`nStep 4: Verifying MCP CLI..."
$env:GODOT_PROJECT_PATH = $ProjectPath
$env:MCP_TRANSPORT = "stdio"
$npxResult = npx -y godot-mcp-cli@latest get_project_info 2>&1
if ($LASTEXITCODE -eq 0) {
  Write-Host "✓ MCP CLI is responsive."
} else {
  Write-Warning "MCP CLI test returned code $LASTEXITCODE"
  if ($Verbose) { Write-Host $npxResult }
}

Write-Host "`n=== Recovery Complete ==="
Write-Host "MCP should now be available for use."
Write-Host "Run health check to verify: powershell -File scripts/mcp-health-check.ps1`n"
