$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillName = 'grok-search'
$destRoot = Join-Path $env:USERPROFILE '.codex\skills'
$dest = Join-Path $destRoot $skillName

New-Item -ItemType Directory -Force -Path $destRoot | Out-Null

$preserve = @{}
foreach ($name in @('config.json','config.local.json')) {
  $p = Join-Path $dest $name
  if (Test-Path $p) {
    $preserve[$name] = Get-Content -Raw $p
  }
}

if (Test-Path $dest) {
  Remove-Item -Recurse -Force $dest
}

New-Item -ItemType Directory -Force -Path $dest | Out-Null

Copy-Item -Force -Path (Join-Path $repoRoot 'SKILL.md') -Destination $dest
Copy-Item -Force -Path (Join-Path $repoRoot 'README.md') -Destination $dest
Copy-Item -Force -Path (Join-Path $repoRoot 'install.ps1') -Destination $dest
Copy-Item -Force -Path (Join-Path $repoRoot 'configure.ps1') -Destination $dest
Copy-Item -Force -Path (Join-Path $repoRoot 'config.json') -Destination $dest
Copy-Item -Recurse -Force -Path (Join-Path $repoRoot 'scripts') -Destination $dest

foreach ($kvp in $preserve.GetEnumerator()) {
  $kvp.Value | Set-Content -Encoding utf8 (Join-Path $dest $kvp.Key)
}

Write-Output "Installed to: $dest"
