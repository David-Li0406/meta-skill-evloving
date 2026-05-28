param(
  [int]$Port = 9222,
  [string]$ProfileDir = "$env:USERPROFILE\.codex\state\moodle_profile_cdp"
)

$ErrorActionPreference='Stop'

$chromeCandidates = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "$env:ProgramFiles(x86)\Google\Chrome\Application\chrome.exe"
)

$chrome = $chromeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $chrome) {
  throw "Chrome not found. Install Google Chrome or edit this script to point to chrome.exe"
}

New-Item -ItemType Directory -Force -Path $ProfileDir | Out-Null

$args = @(
  "--remote-debugging-port=$Port",
  "--user-data-dir=$ProfileDir",
  "--no-first-run",
  "--no-default-browser-check"
)

Start-Process -FilePath $chrome -ArgumentList $args
Write-Host "Started Chrome with CDP on http://127.0.0.1:$Port (profile: $ProfileDir)"
