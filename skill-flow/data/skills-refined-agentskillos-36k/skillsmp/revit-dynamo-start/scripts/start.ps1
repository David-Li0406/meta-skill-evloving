param(
    [string]$RevitYear = "2024"
)

$ErrorActionPreference = "Stop"

# Paths
$ScriptDir = $PSScriptRoot
$AssetsDir = Join-Path $ScriptDir "..\assets"
$TemplateFile = Join-Path $AssetsDir "2024templaterevitskill.rte"
$JournalTemplate = Join-Path $AssetsDir "journal_template.txt"
$RunJournal = Join-Path $AssetsDir "journal_run.txt"

# Resolve absolute path for the template (Revit journals need absolute paths)
$AbsTemplatePath = (Resolve-Path $TemplateFile).Path

# Read Journal Template
$Content = Get-Content -Path $JournalTemplate -Raw

# Replace Placeholder with Actual Path
$Content = $Content.Replace("{{TEMPLATE_PATH}}", $AbsTemplatePath)

# Write Executable Journal
Set-Content -Path $RunJournal -Value $Content -Encoding ASCII

# Launch Revit
# Note: We rely on the Dynamo.addin being in the same folder as the journal or properly installed.
# Since we copied Dynamo.addin to assets/, we usually need to ensure Revit sees it.
# However, if the user installed Dynamo correctly, it should work. 
# The previous skill copied Dynamo.addin next to the journal. Let's assume that strategy.

$RevitExe = "C:\Program Files\Autodesk\Revit $RevitYear\Revit.exe"

if (-not (Test-Path $RevitExe)) {
    Write-Error "Revit executable not found at $RevitExe"
    exit 1
}

Write-Host "Launching Revit $RevitYear..."
Write-Host "Journal: $RunJournal"
Write-Host "Template: $AbsTemplatePath"

# Start Revit with the Journal
Start-Process -FilePath $RevitExe -ArgumentList "`"$RunJournal`" /nosplash" -WindowStyle Maximized
