param(
    [Parameter(Mandatory=$true)]
    [string]$PromptFile,
    
    [string]$TargetPath = ".",
    
    [int]$Timeout = 300
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] [$Level] $Message"
}

$cursorPath = (Get-Command cursor-agent -ErrorAction SilentlyContinue).Source

if (-not $cursorPath) {
    Write-Log "cursor-agent not found in PATH" "ERROR"
    Write-Log "Please install Cursor CLI: https://docs.cursor.com/cli/installation" "ERROR"
    exit 1
}

if (-not (Test-Path $PromptFile)) {
    Write-Log "Prompt file not found: $PromptFile" "ERROR"
    exit 1
}

$promptContent = Get-Content $PromptFile -Raw -Encoding UTF8

Write-Log "Starting cursor-agent..."
Write-Log "Target: $TargetPath"
Write-Log "Timeout: ${Timeout}s"

try {
    $process = Start-Process -FilePath $cursorPath `
        -ArgumentList "--prompt", "`"$promptContent`"", "--path", $TargetPath `
        -NoNewWindow -PassThru -Wait

    if ($process.ExitCode -eq 0) {
        Write-Log "cursor-agent completed successfully" "SUCCESS"
    } else {
        Write-Log "cursor-agent failed with exit code: $($process.ExitCode)" "ERROR"
        exit $process.ExitCode
    }
} catch {
    Write-Log "Error executing cursor-agent: $_" "ERROR"
    exit 1
}
