$ErrorActionPreference = "Stop"

$repoRoot = Get-Location

if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) {
  Write-Error "dotnet is required but not found."
  exit 1
}

$solutions = @(
  Get-ChildItem -Path $repoRoot -Recurse -Filter "*.sln" -File | ForEach-Object { $_.FullName }
  Get-ChildItem -Path $repoRoot -Recurse -Filter "*.slnx" -File | ForEach-Object { $_.FullName }
)
if (-not $solutions -or $solutions.Count -eq 0) {
  Write-Error "No .sln or .slnx files found."
  exit 1
}

$rootSolutions = @($solutions | Where-Object { (Split-Path $_ -Parent) -eq $repoRoot.Path })
if ($rootSolutions -and $rootSolutions.Count -gt 0) {
  $primarySln = @($rootSolutions | Sort-Object)[0]
} else {
  $primarySln = @($solutions | Sort-Object { $_.Length })[0]
}

$solutionDir = Split-Path $primarySln -Parent
$solutionRelative = [System.IO.Path]::GetRelativePath($repoRoot.Path, $primarySln)

$projectLines = dotnet sln $primarySln list | Select-String -Pattern "\.csproj$" | ForEach-Object { $_.Line }
if (-not $projectLines -or $projectLines.Count -eq 0) {
  Write-Error "No projects found in solution: $primarySln"
  exit 1
}

$projects = @()
foreach ($proj in $projectLines) {
  $frameworks = @()
  $isTestProject = $false

  $projectPath = $proj
  if (-not [System.IO.Path]::IsPathRooted($projectPath)) {
    $projectPath = Join-Path $solutionDir $projectPath
  }
  $projectPath = (Resolve-Path -LiteralPath $projectPath).Path

  try {
    $msbuildJson = dotnet msbuild $projectPath -nologo -getProperty:TargetFramework -getProperty:TargetFrameworks -getProperty:IsTestProject -getItem:PackageReference | Out-String
    if ($LASTEXITCODE -eq 0 -and $msbuildJson.Trim().Length -gt 0) {
      $msbuildData = $msbuildJson | ConvertFrom-Json
      $tfm = ($msbuildData.Properties.TargetFramework | ForEach-Object { $_ }) -join ""
      $tfms = ($msbuildData.Properties.TargetFrameworks | ForEach-Object { $_ }) -join ""
      if ($tfms) {
        $frameworks = $tfms.Split(';') | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
      } elseif ($tfm) {
        $frameworks = @($tfm.Trim())
      }

      $isTestProject = ($msbuildData.Properties.IsTestProject | ForEach-Object { $_ }) -join ""
      $isTestProject = $isTestProject.Trim().ToLowerInvariant() -in @("true", "1", "yes")

      if (-not $isTestProject -and $msbuildData.Items.PackageReference) {
        foreach ($pkg in $msbuildData.Items.PackageReference) {
          if ($pkg.Identity -and $pkg.Identity.ToString().ToLowerInvariant() -eq "microsoft.net.test.sdk") {
            $isTestProject = $true
            break
          }
        }
      }
    } else {
      throw "dotnet msbuild failed."
    }
  } catch {
    try {
      [xml]$xml = Get-Content -Path $projectPath
      $propertyGroups = $xml.Project.PropertyGroup

      foreach ($group in $propertyGroups) {
        if ($group.TargetFramework) {
          $frameworks = @($group.TargetFramework.ToString().Trim())
        }
        if ($group.TargetFrameworks) {
          $frameworks = $group.TargetFrameworks.ToString().Split(';') | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne "" }
        }
        if ($group.IsTestProject) {
          $value = $group.IsTestProject.ToString().Trim().ToLowerInvariant()
          if ($value -in @("true", "1", "yes")) {
            $isTestProject = $true
          }
        }
      }
    } catch {
      $frameworks = @()
      $isTestProject = $false
    }
  }

  $projects += [pscustomobject]@{
    path = [System.IO.Path]::GetRelativePath($repoRoot.Path, $projectPath)
    targetFrameworks = $frameworks
    isTestProject = $isTestProject
  }
}

$payload = [pscustomobject]@{
  solution = $solutionRelative
  projects = $projects
}

$outDir = Join-Path $repoRoot "artifacts/codex"
New-Item -Path $outDir -ItemType Directory -Force | Out-Null

$jsonPath = Join-Path $outDir "solution-map.json"
$payload | ConvertTo-Json -Depth 6 | Out-File -FilePath $jsonPath -Encoding ascii

$mdPath = Join-Path $outDir "solution-map.md"
$mdLines = @(
  "# Solution Map",
  "",
  "Solution: `"$solutionRelative`"",
  "",
  "| Project | TargetFramework(s) | IsTestProject |",
  "| --- | --- | --- |"
)

foreach ($proj in $projects) {
  $tfmText = if ($proj.targetFrameworks -and $proj.targetFrameworks.Count -gt 0) { $proj.targetFrameworks -join ", " } else { "-" }
  $isTestText = if ($proj.isTestProject) { "true" } else { "false" }
  $mdLines += "| `"$($proj.path)`" | $tfmText | $isTestText |"
}

$mdLines | Out-File -FilePath $mdPath -Encoding ascii

Write-Output "Wrote artifacts/codex/solution-map.json"
Write-Output "Wrote artifacts/codex/solution-map.md"
