$ErrorActionPreference = 'Stop'

param(
  [switch]$Global
)

function Resolve-GrokConfigPath {
  $custom = $env:GROK_CONFIG_PATH
  if ($custom -and $custom.Trim()) { return $custom.Trim() }
  if ($Global) {
    return (Join-Path $env:USERPROFILE '.codex\config\grok-search.json')
  }
  return (Join-Path $PSScriptRoot 'config.json')
}

$path = Resolve-GrokConfigPath
$dir = Split-Path -Parent $path
New-Item -ItemType Directory -Force -Path $dir | Out-Null

$existing = $null
if (Test-Path $path) {
  try { $existing = Get-Content -Raw $path | ConvertFrom-Json } catch { $existing = $null }
}

function Read-Default([string]$prompt, [string]$defaultValue) {
  $suffix = ''
  if ($defaultValue) { $suffix = " [$defaultValue]" }
  $v = Read-Host "$prompt$suffix"
  if (-not $v) { return $defaultValue }
  return $v
}

$baseUrl = Read-Default 'Grok base URL' ($existing.base_url)
if (-not $baseUrl) { $baseUrl = 'https://your-grok-endpoint.example' }

$apiKey = Read-Default 'Grok API key' ($existing.api_key)
$model = Read-Default 'Model' ($existing.model)
if (-not $model) { $model = 'grok-2-latest' }

$timeout = Read-Default 'Timeout seconds' ([string]($existing.timeout_seconds))
if (-not $timeout) { $timeout = '60' }

$config = [ordered]@{
  base_url = $baseUrl
  api_key = $apiKey
  model = $model
  timeout_seconds = [int]$timeout
  extra_body = @{}
  extra_headers = @{}
}

$config | ConvertTo-Json -Depth 10 | Set-Content -Encoding utf8 $path
Write-Output "Wrote config: $path"
