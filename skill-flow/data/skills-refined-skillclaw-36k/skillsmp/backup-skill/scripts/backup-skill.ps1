param (
    [Parameter(Mandatory=$true)]
    [string]$SkillName
)

$SkillsRoot = "C:\Users\darick\.config\opencode\skills"
$SkillPath = Join-Path $SkillsRoot $SkillName

if (-not (Test-Path $SkillPath)) {
    Write-Error "Skill '$SkillName' not found at $SkillPath"
    exit 1
}

$BackupRoot = Join-Path $SkillPath "backups"
if (-not (Test-Path $BackupRoot)) {
    New-Item -ItemType Directory -Path $BackupRoot | Out-Null
    Write-Host "Created backup folder: $BackupRoot"
}

# Determine the next version number
$ExistingBackups = Get-ChildItem -Path $BackupRoot -Filter "$SkillName-v*.zip"
$MaxVersion = 0

foreach ($File in $ExistingBackups) {
    if ($File.Name -match "-v(\d+)\.zip$") {
        $Ver = [int]$matches[1]
        if ($Ver -gt $MaxVersion) { $MaxVersion = $Ver }
    }
}

$NextVersion = $MaxVersion + 1
$BackupFileName = "$SkillName-v$NextVersion.zip"
$BackupFilePath = Join-Path $BackupRoot $BackupFileName

Write-Host "Backing up $SkillName to $BackupFileName..."

# Create temporary directory for zipping (to avoid zipping the 'backups' folder itself)
$TempZipPath = Join-Path $env:TEMP "opencode_backup_$SkillName"
if (Test-Path $TempZipPath) { Remove-Item -Recurse -Force $TempZipPath }
New-Item -ItemType Directory -Path $TempZipPath | Out-Null

# Copy everything EXCEPT the backups folder
Get-ChildItem -Path $SkillPath -Exclude "backups" | Copy-Item -Destination $TempZipPath -Recurse

# Compress to the backup folder
Compress-Archive -Path "$TempZipPath\*" -DestinationPath $BackupFilePath -Force

# Cleanup
Remove-Item -Recurse -Force $TempZipPath

Write-Host "Backup completed: $BackupFilePath"
