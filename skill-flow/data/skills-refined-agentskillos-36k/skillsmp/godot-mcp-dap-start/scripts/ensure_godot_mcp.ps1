param(
  [string]$ProjectPath = "C:\Users\Sam\Documents\GitHub\v2_heras_garden",
  [string]$GodotExePath = "C:\Users\Sam\Documents\GitHub\v2_heras_garden\Godot_v4.5.1-stable_win64.exe\Godot_v4.5.1-stable_win64.exe",
  [switch]$ForceRestart,
  [switch]$StartGameForDebug,
  [int]$TimeoutSec = 12,
  [int]$NpxTimeoutSec = 30
)

$ErrorActionPreference = "Stop"

function Get-GodotProcesses {
  Get-Process | Where-Object { $_.ProcessName -like "*Godot*" }
}

function Stop-GodotProcesses {
  $procs = Get-GodotProcesses
  if ($procs) {
    $procs | Stop-Process -Force
  }
}

function Wait-Port([int]$Port, [int]$WaitSec) {
  $deadline = (Get-Date).AddSeconds($WaitSec)
  while ((Get-Date) -lt $deadline) {
    $conn = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    if ($conn) {
      return $true
    }
    Start-Sleep -Milliseconds 500
  }
  return $false
}

function Wait-GodotProcess([int]$WaitSec) {
  $deadline = (Get-Date).AddSeconds($WaitSec)
  while ((Get-Date) -lt $deadline) {
    if (Get-GodotProcesses) {
      return $true
    }
    Start-Sleep -Milliseconds 500
  }
  return $false
}

function Start-GodotEditor {
  if (-not (Test-Path $GodotExePath)) {
    throw "Godot exe not found: $GodotExePath"
  }
  & cmd /c start "" "$GodotExePath" --path "$ProjectPath" -e | Out-Null
}

function Invoke-Npx {
  param(
    [string[]]$NpxArgs,
    [int]$WaitSec
  )
  if (-not $NpxArgs -or $NpxArgs.Count -eq 0) {
    throw "Invoke-Npx called with empty arguments."
  }
  $outFile = New-TemporaryFile
  $errFile = New-TemporaryFile
  $cmdArgs = "/c npx " + ($NpxArgs -join " ")
  $proc = Start-Process -FilePath "cmd.exe" -ArgumentList $cmdArgs -NoNewWindow -PassThru -RedirectStandardOutput $outFile -RedirectStandardError $errFile
  if (-not $proc.WaitForExit($WaitSec * 1000)) {
    Stop-Process -Id $proc.Id -Force
    throw "npx timed out after $WaitSec seconds."
  }
  $stdout = Get-Content $outFile -Raw
  $stderr = Get-Content $errFile -Raw
  if ($stdout) { Write-Host $stdout }
  if ($stderr) { Write-Host $stderr }
  return @{ ExitCode = $proc.ExitCode; StdOut = $stdout; StdErr = $stderr }
}

$existing = Get-GodotProcesses
if ($ForceRestart -or ($existing.Count -gt 1)) {
  Write-Host "Stopping existing Godot processes..."
  Stop-GodotProcesses
  Start-Sleep -Seconds 2
}

if (-not (Get-GodotProcesses)) {
  Write-Host "Starting Godot editor..."
  Start-GodotEditor
  if (-not (Wait-GodotProcess -WaitSec $TimeoutSec)) {
    throw "Godot process did not appear in time."
  }
}

Write-Host "Waiting for MCP port 9080..."
if (-not (Wait-Port -Port 9080 -WaitSec $TimeoutSec)) {
  throw "MCP port 9080 did not open in time."
}

$env:GODOT_PROJECT_PATH = $ProjectPath
$env:MCP_TRANSPORT = "stdio"

Write-Host "Verifying MCP handshake (list-tools)..."
$result = Invoke-Npx -NpxArgs @("-y","godot-mcp-cli@latest","--list-tools","--verbose","--timeout","7000") -WaitSec $NpxTimeoutSec
if ($result.ExitCode -ne 0) {
  $combined = ($result.StdOut + "\n" + $result.StdErr)
  $okText = ($combined -match "Ready to process commands") -or ($combined -match "WebSocket connection established")
  if (-not $okText) {
    if (-not $ForceRestart) {
      Write-Host "MCP handshake failed. Re-run with -ForceRestart."
    }
    exit 2
  }
}

if ($StartGameForDebug) {
  Write-Host "Starting game to activate debug port..."
  $result = Invoke-Npx -NpxArgs @("-y","godot-mcp-cli@latest","run_project","--timeout","7000") -WaitSec $NpxTimeoutSec
  if ($result.ExitCode -ne 0) {
    throw "Failed to run project via MCP."
  }
  Write-Host "Waiting for debug port 6007..."
  if (-not (Wait-Port -Port 6007 -WaitSec 10)) {
    Write-Warning "Debug port 6007 not active yet."
  }
}

Write-Host "MCP ready."
