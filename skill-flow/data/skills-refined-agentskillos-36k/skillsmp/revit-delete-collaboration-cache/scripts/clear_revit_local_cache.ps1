param(
  [string]$RootPath = "$env:LOCALAPPDATA\Autodesk\Revit",
  [string]$TargetPath = "",
  [switch]$ConfirmDeletion,
  [switch]$DeleteRoot
)

function Resolve-FullPath {
  param([string]$PathValue, [string]$BasePath)

  if ([string]::IsNullOrWhiteSpace($PathValue)) {
    return $null
  }

  $expanded = [Environment]::ExpandEnvironmentVariables($PathValue)
  if (-not [System.IO.Path]::IsPathRooted($expanded)) {
    if ([string]::IsNullOrWhiteSpace($BasePath)) {
      return $null
    }
    $expanded = Join-Path -Path $BasePath -ChildPath $expanded
  }

  try {
    return (Resolve-Path -Path $expanded -ErrorAction Stop).ProviderPath
  } catch {
    return $null
  }
}

$rootFull = Resolve-FullPath -PathValue $RootPath -BasePath ""
if (-not $rootFull) {
  Write-Error "Root path not found: $RootPath"
  exit 1
}

$targetFull = $rootFull
if (-not [string]::IsNullOrWhiteSpace($TargetPath)) {
  $resolvedTarget = Resolve-FullPath -PathValue $TargetPath -BasePath $rootFull
  if (-not $resolvedTarget) {
    Write-Error "Target path not found: $TargetPath"
    exit 2
  }
  $targetFull = $resolvedTarget
}

$rootPrefix = ($rootFull.TrimEnd('\') + '\')
$targetPrefix = ($targetFull.TrimEnd('\') + '\')
if (-not $targetPrefix.StartsWith($rootPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
  Write-Error "Target path must be inside root path. Root: $rootFull Target: $targetFull"
  exit 3
}

$items = @()
if ($targetFull -ieq $rootFull -and -not $DeleteRoot) {
  $items = Get-ChildItem -LiteralPath $rootFull -Force -ErrorAction SilentlyContinue
} else {
  if (Test-Path -LiteralPath $targetFull) {
    $items = @((Get-Item -LiteralPath $targetFull -Force -ErrorAction SilentlyContinue))
  }
}

if (-not $items -or $items.Count -eq 0) {
  Write-Host "Nothing to delete under: $targetFull"
  exit 0
}

Write-Host "Root:   $rootFull"
Write-Host "Target: $targetFull"
if ($targetFull -ieq $rootFull -and -not $DeleteRoot) {
  Write-Host "Mode:   Delete contents only (root folder is preserved)"
} else {
  Write-Host "Mode:   Delete target path"
}

if (-not $ConfirmDeletion) {
  Write-Host "Preview only. Re-run with -ConfirmDeletion to delete." 
  Write-Host "Items to delete: $($items.Count)"
  $items | ForEach-Object { $_.FullName } | Select-Object -First 200 | ForEach-Object { Write-Host " - $_" }
  if ($items.Count -gt 200) {
    Write-Host "...truncated list (showing first 200 items)."
  }
  exit 0
}

if ($ConfirmDeletion) {
  $processName = "RevitAccelerator"
  $proc = Get-Process -Name $processName -ErrorAction SilentlyContinue
  if ($proc) {
    Write-Host "Force killing process: $processName..."
    Stop-Process -Name $processName -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
  }
}

$errors = @()
foreach ($item in $items) {
  try {
    Remove-Item -LiteralPath $item.FullName -Recurse -Force -ErrorAction Stop
    Write-Host "Deleted: $($item.FullName)"
  } catch {
    $errors += "Failed to delete: $($item.FullName) :: $($_.Exception.Message)"
  }
}

if ($errors.Count -gt 0) {
  Write-Host "Completed with errors:"
  $errors | ForEach-Object { Write-Host " - $_" }
  exit 4
}

Write-Host "Delete completed successfully."
