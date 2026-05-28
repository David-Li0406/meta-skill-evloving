#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Ralph Once - Single execution of a prompt through Claude Code.

.DESCRIPTION
    Executes a prompt file through Claude CLI once with optional visualization.
    Useful for testing prompts before running them in a loop, or for one-off
    autonomous tasks.

.PARAMETER PromptFile
    Path to the prompt file (default: TASKS.md)

.PARAMETER Model
    Claude model to use (default: opus)

.PARAMETER NoVisualize
    Skip piping output through the visualizer

.PARAMETER Quiet
    Suppress status messages, only show Claude output

.PARAMETER AutoCommit
    Automatically commit changes after execution with a Claude-generated message

.EXAMPLE
    ./ralph-once.ps1

.EXAMPLE
    ./ralph-once.ps1 -PromptFile "task.md" -Model "sonnet"

.EXAMPLE
    ./ralph-once.ps1 -NoVisualize -Quiet
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$PromptFile = "TASKS.md",

    [Parameter()]
    [ValidateSet("sonnet", "opus", "haiku")]
    [string]$Model = "opus",

    [Parameter()]
    [switch]$NoVisualize,

    [Parameter()]
    [switch]$Quiet,

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
    if (-not $Quiet) {
        Write-Warning "Visualizer not found at $visualizerPath - disabling visualization"
    }
    $NoVisualize = $true
}

if (-not $Quiet) {
    Write-Host "Ralph Once"
    Write-Host "  Prompt file: $PromptFile"
    Write-Host "  Model: $Model"
    Write-Host "  Visualization: $(-not $NoVisualize)"
    Write-Host "  Auto-commit: $AutoCommit"
    Write-Host ""
}

$startTime = Get-Date

# Read prompt and execute claude
$promptContent = Get-Content $PromptFile -Raw

if ($NoVisualize) {
    $promptContent | claude -p `
        --dangerously-skip-permissions `
        --output-format=stream-json `
        --model=$Model `
        --verbose
}
else {
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
        if (-not $Quiet) {
            Write-Host "`n[AutoCommit] Changes detected, generating commit message..."
        }

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
            $commitMsg = "ralph: automated changes"
        }

        # Add all changes except Ralph Loop infrastructure files
        git add -A
        git reset HEAD -- $PromptFile ralph-once.ps1 ralph-loop.ps1 2>$null

        # Check if there are still staged changes after exclusions
        $stagedChanges = git diff --cached --name-only 2>$null
        if (-not $stagedChanges) {
            if (-not $Quiet) {
                Write-Host "[AutoCommit] No changes to commit (only excluded files modified)"
            }
            return
        }

        git commit -m $commitMsg 2>$null

        if (-not $Quiet) {
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[AutoCommit] Committed: $commitMsg"
            }
            else {
                Write-Host "[AutoCommit] Commit failed"
            }
        }
    }
    elseif (-not $Quiet) {
        Write-Host "`n[AutoCommit] No changes to commit"
    }
}

$duration = (Get-Date) - $startTime

if (-not $Quiet) {
    Write-Host ""
    Write-Host "Completed in $($duration.ToString('mm\:ss'))"
}
