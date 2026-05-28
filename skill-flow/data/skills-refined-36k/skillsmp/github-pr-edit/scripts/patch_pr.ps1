Param(
  [Parameter(Mandatory = $true)]
  [string]$Owner,

  [Parameter(Mandatory = $true)]
  [string]$Repo,

  [Parameter(Mandatory = $true)]
  [int]$Number,

  [Parameter(Mandatory = $false)]
  [string]$Title,

  [Parameter(Mandatory = $false)]
  [string]$BodyFile,

  [Parameter(Mandatory = $false)]
  [switch]$Draft,

  [Parameter(Mandatory = $false)]
  [switch]$ValidateOnly
)

$ErrorActionPreference = "Stop"

function Get-GitHubToken {
  $token = ""
  if ($env:GITHUB_TOKEN) {
    $token = $env:GITHUB_TOKEN
  }
  elseif ($env:GH_TOKEN) {
    $token = $env:GH_TOKEN
  }

  $token = $token.Trim()
  if ($token) {
    return $token
  }

  $cred = "protocol=https`nhost=github.com`n`n" | git credential fill
  $tokenLine = ($cred | Select-String -Pattern '^password=' -ErrorAction SilentlyContinue).Line
  if (-not $tokenLine) {
    throw "No GitHub token found. Set GITHUB_TOKEN/GH_TOKEN, or authenticate git with a PAT."
  }
  return $tokenLine.Substring(9)
}

function Invoke-GitHubJson {
  param(
    [Parameter(Mandatory = $true)][string]$Method,
    [Parameter(Mandatory = $true)][string]$Uri,
    [Parameter(Mandatory = $false)][object]$Payload
  )

  $headers = @{
    Authorization = "token $script:Token"
    "User-Agent"  = "codex-cli"
    Accept        = "application/vnd.github+json"
  }

  if ($null -eq $Payload) {
    return Invoke-RestMethod -Method $Method -Uri $Uri -Headers $headers
  }

  $json = $Payload | ConvertTo-Json -Depth 8
  $bytes = [System.Text.Encoding]::UTF8.GetBytes($json)

  return Invoke-RestMethod -Method $Method `
    -Uri $Uri `
    -Headers $headers `
    -ContentType "application/json; charset=utf-8" `
    -Body $bytes
}

$script:Token = Get-GitHubToken
$baseUri = "https://api.github.com/repos/$Owner/$Repo"

if ($ValidateOnly) {
  $repoInfo = Invoke-GitHubJson -Method Get -Uri "$baseUri"
  $repoInfo | Select-Object full_name, private
  exit 0
}

$body = $null
if ($BodyFile) {
  if (-not (Test-Path $BodyFile)) {
    throw "Body file not found: $BodyFile"
  }
  $body = Get-Content -Raw -Encoding UTF8 $BodyFile
}

$payload = @{}
if ($Title) { $payload.title = $Title }
if ($body -ne $null) { $payload.body = $body }
if ($PSBoundParameters.ContainsKey("Draft")) { $payload.draft = [bool]$Draft }

if ($payload.Count -eq 0) {
  throw "Nothing to update. Provide -Title and/or -BodyFile."
}

$pr = Invoke-GitHubJson -Method Patch -Uri "$baseUri/pulls/$Number" -Payload $payload
$pr.html_url

