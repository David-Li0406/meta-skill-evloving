<#
.SYNOPSIS
Synchronizes OpenCode skills with GitHub repository.

.DESCRIPTION
This script performs a bidirectional sync between local skills and GitHub:
1. Fetches latest changes from GitHub
2. Stages and commits local changes
3. Pushes local commits to GitHub
4. Pulls any remote changes
#>

$ErrorActionPreference = "Stop"

$repoRoot = "C:\Users\darick\.config\opencode"
$skillsPath = Join-Path $repoRoot "skills"
$logPath = Join-Path $repoRoot "logs\sync.log"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] $Message"
    Write-Host $logEntry
    Add-Content -Path $logPath -Value $logEntry
}

function Test-GitRepository {
    return (Test-Path (Join-Path $repoRoot ".git"))
}

function Test-GitHubAuth {
    try {
        gh auth status 2>&1 | Out-Null
        return $?
    } catch {
        return $false
    }
}

function Sync-Changes {
    param(
        [string]$RemoteName = "origin",
        [string]$BranchName = "master"
    )
    
    Write-Log "Starting sync process..."
    
    # Save current directory
    $originalLocation = Get-Location
    Set-Location $repoRoot
    
    try {
        # Fetch latest from remote
        Write-Log "Fetching changes from GitHub..."
        git fetch $RemoteName
        
        # Check for local changes
        $localChanges = git status --porcelain
        
        if ($localChanges) {
            Write-Log "Local changes detected:"
            Write-Log $localChanges
            
            # Add all changes
            git add skills/
            git add opencode.jsonc
            git add opencode.jsonc
            
            # Get current branch hash for commit message
            $commitHash = git rev-parse HEAD
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            
            # Create commit
            git commit -m "Sync skills: $timestamp ($commitHash)"
            
            # Push to remote
            Write-Log "Pushing changes to GitHub..."
            git push $RemoteName $BranchName
            Write-Log "Successfully pushed local changes"
        } else {
            Write-Log "No local changes to commit"
        }
        
        # Pull any remote changes
        Write-Log "Pulling remote changes..."
        git pull $RemoteName $BranchName --rebase
        Write-Log "Sync completed successfully"
        
    } catch {
        Write-Log "ERROR: $_"
        throw
    } finally {
        Set-Location $originalLocation
    }
}

# Main execution
Write-Log "=== Starting skills synchronization ==="

if (-not (Test-GitRepository)) {
    Write-Log "ERROR: Not a git repository. Please initialize git first."
    exit 1
}

if (-not (Test-GitHubAuth)) {
    Write-Log "WARNING: GitHub CLI not authenticated. Sync may fail for push operations."
}

Sync-Changes
Write-Log "=== Synchronization complete ==="
