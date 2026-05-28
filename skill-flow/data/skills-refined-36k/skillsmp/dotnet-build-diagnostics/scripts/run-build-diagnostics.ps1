$ErrorActionPreference = "Stop"

if (-not (Get-Command dotnet -ErrorAction SilentlyContinue)) {
  Write-Error "dotnet is required but not found."
  exit 1
}

$outDir = Join-Path (Get-Location) "artifacts/codex"
New-Item -Path $outDir -ItemType Directory -Force | Out-Null

$summaryPath = Join-Path $outDir "build-summary.txt"

$solutions = @(
  Get-ChildItem -Path (Get-Location) -Recurse -Filter "*.sln" -File | ForEach-Object { $_.FullName }
  Get-ChildItem -Path (Get-Location) -Recurse -Filter "*.slnx" -File | ForEach-Object { $_.FullName }
)
if (-not $solutions -or $solutions.Count -eq 0) {
  Write-Error "No .sln or .slnx files found."
  exit 1
}

$rootSolutions = @($solutions | Where-Object { (Split-Path $_ -Parent) -eq (Get-Location).Path })
if ($rootSolutions -and $rootSolutions.Count -gt 0) {
  $primarySln = @($rootSolutions | Sort-Object)[0]
} else {
  $primarySln = @($solutions | Sort-Object { $_.Length })[0]
}

$solutionRelative = [System.IO.Path]::GetRelativePath((Get-Location).Path, $primarySln)

"# Build Diagnostics Summary" | Out-File -FilePath $summaryPath -Encoding ascii
"" | Out-File -FilePath $summaryPath -Append -Encoding ascii
"Solution: `"$solutionRelative`"" | Out-File -FilePath $summaryPath -Append -Encoding ascii
"" | Out-File -FilePath $summaryPath -Append -Encoding ascii
"## dotnet --info" | Out-File -FilePath $summaryPath -Append -Encoding ascii
"" | Out-File -FilePath $summaryPath -Append -Encoding ascii

(dotnet --info 2>&1) | Out-File -FilePath $summaryPath -Append -Encoding ascii
"" | Out-File -FilePath $summaryPath -Append -Encoding ascii
"## dotnet restore" | Out-File -FilePath $summaryPath -Append -Encoding ascii
"" | Out-File -FilePath $summaryPath -Append -Encoding ascii

(dotnet restore $primarySln 2>&1) | Out-File -FilePath $summaryPath -Append -Encoding ascii
"" | Out-File -FilePath $summaryPath -Append -Encoding ascii
"## dotnet build" | Out-File -FilePath $summaryPath -Append -Encoding ascii
"" | Out-File -FilePath $summaryPath -Append -Encoding ascii

$buildOutput = dotnet build $primarySln `
  /m `
  /bl:"$outDir/build.binlog" `
  /p:ContinuousIntegrationBuild=true `
  /p:Deterministic=true `
  /p:TreatWarningsAsErrors=true `
  /p:WarningsAsErrors= `
  /p:RunAnalyzers=true `
  /p:AnalysisMode=All `
  /p:RestoreLockedMode=true `
  /p:UseSharedCompilation=false `
  /p:BuildInParallel=true `
  /p:GenerateDocumentationFile=true `
  /p:DebugType=portable `
  /p:DebugSymbols=true 2>&1

$buildOutput | Out-File -FilePath $summaryPath -Append -Encoding ascii

if ($LASTEXITCODE -ne 0) {
  "" | Out-File -FilePath $summaryPath -Append -Encoding ascii
  "Build failed with exit code $LASTEXITCODE" | Out-File -FilePath $summaryPath -Append -Encoding ascii
  exit $LASTEXITCODE
}

"" | Out-File -FilePath $summaryPath -Append -Encoding ascii
"Build succeeded" | Out-File -FilePath $summaryPath -Append -Encoding ascii
