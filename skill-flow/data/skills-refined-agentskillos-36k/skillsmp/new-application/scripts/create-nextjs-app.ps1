param(
  [Parameter(Mandatory = $true, Position = 0)]
  [string]$AppName
)

$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($AppName)) {
  Write-Host "Usage: .\create-nextjs-app.ps1 <app-name>" -ForegroundColor Red
  exit 1
}

npm create cloudflare@latest -- next-cloudflare2 --framework=next --deploy --git

