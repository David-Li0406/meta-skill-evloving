Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = (Resolve-Path (Join-Path $scriptDir '..\..\..\..')).Path
$artifactsDir = Join-Path $repoRoot 'artifacts\codex'
$report = Join-Path $artifactsDir 'format-report.txt'
$target = if ($env:DOTNET_FORMAT_TARGET) { $env:DOTNET_FORMAT_TARGET } else { 'infra-monitor.slnx' }
$extraArgs = $args

New-Item -ItemType Directory -Force -Path $artifactsDir | Out-Null

@(
  'dotnet format verification report',
  "Target: $target",
  "Args: $($extraArgs -join ' ')",
  '',
  '== dotnet format (verify-no-changes) =='
) | Set-Content -Path $report -Encoding UTF8

$formatStatus = 0
$analyzerStatus = 0
try {
  & dotnet format $target --verify-no-changes @extraArgs *>> $report
} catch {
  $formatStatus = 1
}

@(
  '',
  '== dotnet format analyzers (verify-no-changes) =='
) | Add-Content -Path $report -Encoding UTF8

try {
  & dotnet format analyzers $target --verify-no-changes @extraArgs *>> $report
} catch {
  $analyzerStatus = 1
}

if ($formatStatus -ne 0 -or $analyzerStatus -ne 0) {
  Write-Error "One or more checks failed. See $report for details."
  exit 1
}

Write-Host "All format/analyzer checks passed. Report: $report"
