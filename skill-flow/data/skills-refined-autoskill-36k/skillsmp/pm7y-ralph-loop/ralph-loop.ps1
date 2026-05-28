#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Ralph Wiggum Loop - Cross-platform continuous prompt execution for Claude Code.

.DESCRIPTION
    Continuously executes a prompt file through Claude CLI with output visualization.
    Uses the "Ralph Wiggum technique" - spawning fresh Claude sessions to maintain
    context quality over long-running autonomous operations.

.PARAMETER PromptFile
    Path to the prompt file (default: TASKS.md)

.PARAMETER Model
    Claude model to use (default: opus)

.PARAMETER SleepSeconds
    Seconds to wait between iterations (default: 10)

.PARAMETER MaxIterations
    Maximum number of loop iterations (default: 25)

.PARAMETER NoVisualize
    Skip piping output through the visualizer

.PARAMETER AutoCommit
    Automatically commit changes after each iteration with a Claude-generated message

.EXAMPLE
    ./ralph-loop.ps1

.EXAMPLE
    ./ralph-loop.ps1 -PromptFile "tasks.md" -Model "opus" -SleepSeconds 30

.EXAMPLE
    ./ralph-loop.ps1 -MaxIterations 5
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$PromptFile = "TASKS.md",

    [Parameter()]
    [ValidateSet("sonnet", "opus", "haiku")]
    [string]$Model = "opus",

    [Parameter()]
    [int]$SleepSeconds = 10,

    [Parameter()]
    [int]$MaxIterations = 25,

    [Parameter()]
    [switch]$NoVisualize,

    [Parameter()]
    [switch]$AutoCommit
)

# Verify prompt file exists
if (-not (Test-Path $PromptFile)) {
    Write-Error "Prompt file not found: $PromptFile"
    Write-Host "Create a TASKS.md file with your instructions, or specify a different file with -PromptFile"
    exit 1
}

# Verify claude CLI is available
if (-not (Get-Command "claude" -ErrorAction SilentlyContinue)) {
    Write-Error "Claude CLI not found. Install it from: https://claude.ai/code"
    exit 1
}

# Get script directory for visualizer
$scriptDir = $PSScriptRoot
if (-not $scriptDir) { $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path }
$visualizerPath = Join-Path $scriptDir "ralph-visualize.ps1"

# Verify visualizer exists
if (-not $NoVisualize -and -not (Test-Path $visualizerPath)) {
    Write-Warning "Visualizer not found at $visualizerPath - disabling visualization"
    $NoVisualize = $true
}

$iteration = 0
$separator = "`n`n========================LOOP=========================`n`n"

Write-Host "Starting Ralph Loop"
Write-Host "  Prompt file: $PromptFile"
Write-Host "  Model: $Model"
Write-Host "  Sleep: ${SleepSeconds}s between iterations"
if ($MaxIterations -gt 0) {
    Write-Host "  Max iterations: $MaxIterations"
}
Write-Host "  Visualization: $(-not $NoVisualize)"
Write-Host "  Auto-commit: $AutoCommit"
Write-Host ""
Write-Host "Press Ctrl+C to stop"
Write-Host $separator

try {
    while ($true) {
        $iteration++

        if ($MaxIterations -gt 0 -and $iteration -gt $MaxIterations) {
            Write-Host "Reached maximum iterations ($MaxIterations). Stopping."
            break
        }

        Write-Host "[$([DateTime]::Now.ToString('HH:mm:ss'))] Iteration $iteration"

        # Read prompt and execute claude
        $promptContent = Get-Content $PromptFile -Raw

        if ($NoVisualize) {
            # Direct execution without visualization
            $promptContent | claude -p `
                --dangerously-skip-permissions `
                --output-format=stream-json `
                --model=$Model `
                --verbose
        }
        else {
            # With visualization pipeline
            $promptContent | claude -p `
                --dangerously-skip-permissions `
                --output-format=stream-json `
                --model=$Model `
                --verbose `
                | & $visualizerPath
        }

        # Auto-commit if enabled and there are changes
        if ($AutoCommit) {
            $changes = git status --porcelain 2>$null
            if ($changes) {
                Write-Host "`n[AutoCommit] Changes detected, generating commit message..."

                # Get diff summary for Claude to generate message
                $diffStat = git diff --stat HEAD 2>$null
                $untrackedFiles = git ls-files --others --exclude-standard 2>$null

                $commitPrompt = @"
Generate a concise git commit message (max 72 chars) for these changes.
Return ONLY the commit message, no explanation or quotes.

Changes:
$diffStat

New files:
$untrackedFiles
"@

                $commitMsg = $commitPrompt | claude -p --model=haiku --output-format=text 2>$null
                $commitMsg = $commitMsg.Trim()

                # Fallback if Claude fails
                if (-not $commitMsg) {
                    $commitMsg = "ralph: iteration $iteration changes"
                }

                # Add all changes except Ralph Loop infrastructure files
                git add -A
                git reset HEAD -- $PromptFile ralph-once.ps1 ralph-loop.ps1 2>$null

                # Check if there are still staged changes after exclusions
                $stagedChanges = git diff --cached --name-only 2>$null
                if (-not $stagedChanges) {
                    Write-Host "[AutoCommit] No changes to commit (only excluded files modified)"
                    continue
                }

                git commit -m $commitMsg 2>$null

                if ($LASTEXITCODE -eq 0) {
                    Write-Host "[AutoCommit] Committed: $commitMsg"
                }
                else {
                    Write-Host "[AutoCommit] Commit failed"
                }
            }
            else {
                Write-Host "`n[AutoCommit] No changes to commit"
            }
        }

        Write-Host $separator

        if ($MaxIterations -eq 0 -or $iteration -lt $MaxIterations) {
            Write-Host "Sleeping for $SleepSeconds seconds..."
            Start-Sleep -Seconds $SleepSeconds
        }
    }
}
catch {
    if ($_.Exception.GetType().Name -eq "PipelineStoppedException") {
        Write-Host "`nLoop interrupted by user"
    }
    else {
        throw
    }
}
finally {
    Write-Host "`nRalph Loop completed after $iteration iteration(s)"
}
