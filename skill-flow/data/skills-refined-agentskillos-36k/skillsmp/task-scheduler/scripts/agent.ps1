 param(
    [Parameter(Mandatory=$true)]
    [string]$prompt,
    [Parameter(Mandatory=$false)]
    [string]$taskname,
    [Parameter(Mandatory=$false)]
    [int]$delete = 0
 )

# Run agent.exe with the provided prompt
try {
    & "agent" $prompt
    $exitCode = $LASTEXITCODE
    if ($exitCode -eq 0) {
		Write-Host "Agent Task Executed Successfully!"
		Write-Host ""
        & "$PSScriptRoot\notify.ps1" -title "Agent Scheduled Task" -content "Success: $taskname" -icon "success"
    } else {
        & "$PSScriptRoot\notify.ps1" -title "Agent Scheduled Task" -content "Failed with code ${exitCode}: $taskname" -icon "error"
    }

    if ($delete -eq 1) {
        Unregister-ScheduledTask -TaskName $taskname -Confirm:$false
    }
} catch {
    & "$PSScriptRoot\notify.ps1" -title "Agent Result" -content "Error running agent: $_" -icon "error"
}

Write-Host "Press any key to close"
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")