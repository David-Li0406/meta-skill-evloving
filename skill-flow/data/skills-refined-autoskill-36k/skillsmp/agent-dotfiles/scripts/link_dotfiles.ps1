param(
  [string]$DotfilesRoot = "$env:USERPROFILE\\dotfiles",
  [string]$MappingFile = "",
  [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if ([string]::IsNullOrWhiteSpace($MappingFile)) {
  $MappingFile = Join-Path $DotfilesRoot "mappings.txt"
}

if (-not (Test-Path -Path $MappingFile)) {
  Write-Error "Mapping file not found: $MappingFile"
  exit 1
}

$lines = Get-Content -Path $MappingFile
foreach ($rawLine in $lines) {
  $line = $rawLine.Trim()
  if ($line.Length -eq 0 -or $line.StartsWith("#")) {
    continue
  }

  $parts = $line.Split(":", 2)
  if ($parts.Count -ne 2) {
    Write-Warning "Skip invalid line: $rawLine"
    continue
  }

  $src = $parts[0].Trim()
  $dest = $parts[1].Trim()
  if ([string]::IsNullOrWhiteSpace($src) -or [string]::IsNullOrWhiteSpace($dest)) {
    Write-Warning "Skip invalid line: $rawLine"
    continue
  }

  $srcPath = Join-Path $DotfilesRoot $src
  if (-not (Test-Path -Path $srcPath)) {
    Write-Warning "Missing source: $srcPath"
    continue
  }

  if ($dest.StartsWith("~\\")) {
    $dest = Join-Path $HOME $dest.Substring(2)
  } elseif ($dest.StartsWith("~/")) {
    $dest = Join-Path $HOME $dest.Substring(2)
  }

  $destParent = Split-Path -Parent $dest
  if ($destParent -and -not (Test-Path -Path $destParent)) {
    New-Item -ItemType Directory -Path $destParent -Force | Out-Null
  }

  if (Test-Path -Path $dest) {
    if ($Force) {
      $backup = "$dest.bak.$(Get-Date -Format 'yyyyMMddHHmmss')"
      Move-Item -Path $dest -Destination $backup
    } else {
      Write-Host "Skip existing: $dest"
      continue
    }
  }

  if (Test-Path -Path $srcPath -PathType Container) {
    try {
      New-Item -ItemType SymbolicLink -Path $dest -Target $srcPath -ErrorAction Stop | Out-Null
    } catch {
      New-Item -ItemType Junction -Path $dest -Target $srcPath -ErrorAction Stop | Out-Null
    }
  } else {
    try {
      New-Item -ItemType SymbolicLink -Path $dest -Target $srcPath -ErrorAction Stop | Out-Null
    } catch {
      New-Item -ItemType HardLink -Path $dest -Target $srcPath -ErrorAction Stop | Out-Null
    }
  }

  Write-Host "Linked: $dest -> $srcPath"
}
