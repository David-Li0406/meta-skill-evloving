# Unified Deployment Script - Cloudflare Workers & Supabase Edge Functions
# Supports: Windows PowerShell

# Exit on error
$ErrorActionPreference = "Stop"

# Get the script's directory and navigate to project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "../../../..")

# Load environment variables from .env
$EnvFile = Join-Path $ProjectRoot ".env"
if (Test-Path $EnvFile) {
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.+)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"')
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }
} else {
    Write-Host "Error: .env file not found in project root" -ForegroundColor Red
    exit 1
}

# Function to check if command exists
function Test-CommandExists {
    param($Command)
    $null -ne (Get-Command $Command -ErrorAction SilentlyContinue)
}

# ═══════════════════════════════════════════════════════════════════════════════
# Branch-Based Deployment Functions
# ═══════════════════════════════════════════════════════════════════════════════

# Sanitize branch name for resource naming (DNS-safe, max 59 chars to leave room for "api-" prefix)
function Get-SanitizedBranchName {
    param($BranchName)
    $sanitized = $BranchName.ToLower()
    $sanitized = $sanitized -replace '[/_]', '-'
    $sanitized = $sanitized -replace '[^a-z0-9-]', ''
    $sanitized = $sanitized -replace '^-+|-+$', ''
    $sanitized = $sanitized -replace '-+', '-'
    if ($sanitized.Length -gt 59) {
        $sanitized = $sanitized.Substring(0, 59)
    }
    $sanitized = $sanitized -replace '-$', ''
    return $sanitized
}

# Get current git branch
function Get-GitBranch {
    try {
        $branch = git -C $ProjectRoot rev-parse --abbrev-ref HEAD 2>$null
        return $branch
    } catch {
        return ""
    }
}

# Check if branch is protected (deploys to production)
function Test-ProtectedBranch {
    param($Branch)
    return ($Branch -eq "main" -or $Branch -eq "master" -or [string]::IsNullOrEmpty($Branch))
}

# Get worker name based on branch
function Get-WorkerName {
    param($Branch)
    if (Test-ProtectedBranch $Branch) {
        return "api"
    } else {
        $sanitized = Get-SanitizedBranchName $Branch
        if (-not [string]::IsNullOrEmpty($sanitized)) {
            return "api-$sanitized"
        }
        return "api"
    }
}

# Check if Supabase preview branch exists
function Test-SupabaseBranchExists {
    param($BranchName)
    $sanitized = Get-SanitizedBranchName $BranchName
    $SupabaseProjectRef = [Environment]::GetEnvironmentVariable("SUPABASE_PROJECT_REF", "Process")

    try {
        $branchList = supabase branches list --project-ref $SupabaseProjectRef 2>$null
        if ($branchList -match $sanitized) {
            return $true
        }
    } catch {}
    return $false
}

# Get Supabase preview branch details
function Get-SupabaseBranchDetails {
    param($BranchName)
    $sanitized = Get-SanitizedBranchName $BranchName
    $SupabaseProjectRef = [Environment]::GetEnvironmentVariable("SUPABASE_PROJECT_REF", "Process")

    try {
        $branchInfo = supabase branches get $sanitized --project-ref $SupabaseProjectRef 2>$null
        # Extract branch ref (20 lowercase letters)
        if ($branchInfo -match '[a-z]{20}') {
            return $matches[0]
        }
    } catch {}
    return ""
}

# Display Supabase branch credentials info
function Show-SupabaseBranchInfo {
    param($BranchName)
    $sanitized = Get-SanitizedBranchName $BranchName
    $SupabaseProjectRef = [Environment]::GetEnvironmentVariable("SUPABASE_PROJECT_REF", "Process")

    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
    Write-Host "  Supabase Preview Branch Credentials" -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Yellow
    Write-Host "Branch: $sanitized" -ForegroundColor Blue
    Write-Host ""
    Write-Host "Note: Preview branches have their own API credentials." -ForegroundColor Yellow
    Write-Host "To get the branch-specific credentials, run:"
    Write-Host "  supabase branches get $sanitized --project-ref $SupabaseProjectRef" -ForegroundColor Green
    Write-Host ""
    Write-Host "If your Cloudflare Worker connects to Supabase, update its" -ForegroundColor Yellow
    Write-Host "environment with the branch-specific SUPABASE_URL and keys." -ForegroundColor Yellow
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Yellow
}

# Create Supabase preview branch
function New-SupabaseBranch {
    param($BranchName)
    $sanitized = Get-SanitizedBranchName $BranchName
    $SupabaseProjectRef = [Environment]::GetEnvironmentVariable("SUPABASE_PROJECT_REF", "Process")

    Write-Host "Creating Supabase preview branch: $sanitized" -ForegroundColor Yellow
    supabase branches create $sanitized --project-ref $SupabaseProjectRef
    return $LASTEXITCODE -eq 0
}

# ═══════════════════════════════════════════════════════════════════════════════
# Deployment Functions
# ═══════════════════════════════════════════════════════════════════════════════

# Function to deploy to Cloudflare Workers
function Deploy-Cloudflare {
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
    Write-Host "  Deploying to Cloudflare Workers" -ForegroundColor Blue
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Blue

    # Check if bun is installed
    if (-not (Test-CommandExists bun)) {
        Write-Host "Error: bun is not installed or not in PATH" -ForegroundColor Red
        Write-Host "Install from: https://bun.sh" -ForegroundColor Yellow
        return $false
    }

    # Navigate to API directory
    $ApiDir = Join-Path $ProjectRoot "apps/api"
    Set-Location $ApiDir

    # Check if node_modules exists
    if (-not (Test-Path "node_modules")) {
        Write-Host "Error: node_modules not found. Run 'bun install' first." -ForegroundColor Red
        return $false
    }

    # Check required environment variables
    $CloudflareApi = [Environment]::GetEnvironmentVariable("CLOUDFLARE_API", "Process")
    $CloudflareAccountId = [Environment]::GetEnvironmentVariable("CLOUDFLARE_ACCOUNT_ID", "Process")

    if ([string]::IsNullOrEmpty($CloudflareApi) -or [string]::IsNullOrEmpty($CloudflareAccountId)) {
        Write-Host "Error: Missing required environment variables" -ForegroundColor Red
        Write-Host "Required: CLOUDFLARE_API, CLOUDFLARE_ACCOUNT_ID" -ForegroundColor Yellow
        return $false
    }

    # Detect git branch and compute worker name
    $gitBranch = Get-GitBranch
    $workerName = Get-WorkerName $gitBranch

    # Display branch info
    if (Test-ProtectedBranch $gitBranch) {
        $displayBranch = if ([string]::IsNullOrEmpty($gitBranch)) { "detached HEAD" } else { $gitBranch }
        Write-Host "Branch: $displayBranch (production)" -ForegroundColor Green
        Write-Host "Worker: $workerName" -ForegroundColor Green
    } else {
        Write-Host "Branch: $gitBranch (preview)" -ForegroundColor Yellow
        Write-Host "Worker: $workerName" -ForegroundColor Yellow
    }
    Write-Host ""

    # Run deployment with branch-specific worker name
    Write-Host "Starting Cloudflare deployment..." -ForegroundColor Green
    if (Test-ProtectedBranch $gitBranch) {
        # Production deployment uses default wrangler.jsonc name
        bun run deploy
    } else {
        # Feature branch deployment uses custom worker name
        bunx wrangler deploy --minify --name $workerName
    }

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Cloudflare Workers deployment successful!" -ForegroundColor Green
        Write-Host "URL: https://$workerName.*.workers.dev" -ForegroundColor Blue
        return $true
    } else {
        Write-Host "`n✗ Cloudflare Workers deployment failed" -ForegroundColor Red
        return $false
    }
}

# Function to deploy to Supabase Edge Functions
function Deploy-Supabase {
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
    Write-Host "  Deploying to Supabase Edge Functions" -ForegroundColor Blue
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Blue

    # Check if supabase CLI is installed
    if (-not (Test-CommandExists supabase)) {
        Write-Host "Error: Supabase CLI is not installed or not in PATH" -ForegroundColor Red
        Write-Host "Install from: https://supabase.com/docs/guides/cli" -ForegroundColor Yellow
        Write-Host "  npm install -g supabase" -ForegroundColor Yellow
        Write-Host "  or: scoop bucket add supabase https://github.com/supabase/scoop-bucket.git" -ForegroundColor Yellow
        Write-Host "      scoop install supabase" -ForegroundColor Yellow
        return $false
    }

    # Navigate to project root
    Set-Location $ProjectRoot

    # Check if supabase directory exists
    if (-not (Test-Path "supabase/functions")) {
        Write-Host "Error: supabase/functions directory not found" -ForegroundColor Red
        return $false
    }

    # Check required environment variables
    $SupabaseProjectRef = [Environment]::GetEnvironmentVariable("SUPABASE_PROJECT_REF", "Process")

    if ([string]::IsNullOrEmpty($SupabaseProjectRef)) {
        Write-Host "Error: Missing SUPABASE_PROJECT_REF environment variable" -ForegroundColor Red
        Write-Host "Add to .env: SUPABASE_PROJECT_REF=your-project-ref" -ForegroundColor Yellow
        return $false
    }

    # Detect git branch
    $gitBranch = Get-GitBranch
    $functionsUrl = "https://$SupabaseProjectRef.supabase.co/functions/v1/"

    # Display branch info
    if (Test-ProtectedBranch $gitBranch) {
        $displayBranch = if ([string]::IsNullOrEmpty($gitBranch)) { "detached HEAD" } else { $gitBranch }
        Write-Host "Branch: $displayBranch (production)" -ForegroundColor Green
        Write-Host "Project: $SupabaseProjectRef" -ForegroundColor Green
    } else {
        $sanitizedBranch = Get-SanitizedBranchName $gitBranch
        Write-Host "Branch: $gitBranch (preview)" -ForegroundColor Yellow
        Write-Host "Supabase Branch: $sanitizedBranch" -ForegroundColor Yellow

        # Check if preview branch exists
        $isPreviewBranch = $true
        Write-Host "`nChecking for existing Supabase preview branch..." -ForegroundColor Blue
        if (Test-SupabaseBranchExists $gitBranch) {
            Write-Host "✓ Preview branch '$sanitizedBranch' exists" -ForegroundColor Green
            # Get the branch's project ref for the URL
            $branchRef = Get-SupabaseBranchDetails $gitBranch
            if (-not [string]::IsNullOrEmpty($branchRef)) {
                $functionsUrl = "https://$branchRef.supabase.co/functions/v1/"
            }
        } else {
            Write-Host "Preview branch '$sanitizedBranch' does not exist" -ForegroundColor Yellow
            Write-Host ""
            $createBranch = Read-Host "Create Supabase preview branch '$sanitizedBranch'? [y/N]"

            if ($createBranch -eq "y" -or $createBranch -eq "Y") {
                if (New-SupabaseBranch $gitBranch) {
                    Write-Host "✓ Preview branch created successfully" -ForegroundColor Green
                    # Get the new branch's project ref
                    $branchRef = Get-SupabaseBranchDetails $gitBranch
                    if (-not [string]::IsNullOrEmpty($branchRef)) {
                        $functionsUrl = "https://$branchRef.supabase.co/functions/v1/"
                    }
                } else {
                    Write-Host "✗ Failed to create preview branch" -ForegroundColor Red
                    Write-Host "You may need to enable branching in your Supabase project settings" -ForegroundColor Yellow
                    Write-Host "Or deploy to production instead" -ForegroundColor Yellow
                    return $false
                }
            } else {
                Write-Host "Skipping preview branch creation. Deploying to production instead." -ForegroundColor Yellow
                $isPreviewBranch = $false
            }
        }
    } else {
        $isPreviewBranch = $false
    }
    Write-Host ""

    # Check if project is linked
    if (-not (Test-Path "supabase/.temp/project-ref")) {
        Write-Host "Project not linked. Linking now..." -ForegroundColor Yellow
        supabase link --project-ref $SupabaseProjectRef
        if ($LASTEXITCODE -ne 0) {
            Write-Host "✗ Failed to link Supabase project" -ForegroundColor Red
            Write-Host "Run manually: supabase login && supabase link" -ForegroundColor Yellow
            return $false
        }
    }

    # Deploy all functions
    Write-Host "Starting Supabase Edge Functions deployment..." -ForegroundColor Green
    supabase functions deploy

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Supabase Edge Functions deployment successful!" -ForegroundColor Green
        Write-Host "Functions available at: $functionsUrl" -ForegroundColor Blue

        # Display branch credentials info if deploying to a preview branch
        if ($isPreviewBranch) {
            Show-SupabaseBranchInfo $gitBranch
        }
        return $true
    } else {
        Write-Host "`n✗ Supabase Edge Functions deployment failed" -ForegroundColor Red
        return $false
    }
}

# Main script logic
function Main {
    # Get git branch info for display
    $gitBranch = Get-GitBranch
    $branchType = "production"
    if (-not (Test-ProtectedBranch $gitBranch)) {
        $branchType = "preview"
    }
    $displayBranch = if ([string]::IsNullOrEmpty($gitBranch)) { "detached HEAD" } else { $gitBranch }

    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║   Unified Deployment - Select Platform   ║" -ForegroundColor Green
    Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "Git Branch: $displayBranch ($branchType)" -ForegroundColor Blue
    Write-Host ""

    # Check if DEPLOY_TARGET is set (for automated deployments)
    $DeployTarget = [Environment]::GetEnvironmentVariable("DEPLOY_TARGET", "Process")

    if (-not [string]::IsNullOrEmpty($DeployTarget)) {
        $PlatformChoice = $DeployTarget
        Write-Host "Using automated target: $DeployTarget" -ForegroundColor Blue
    } else {
        # Interactive platform selection
        Write-Host "Select deployment platform:"
        Write-Host "  1) Cloudflare Workers"
        Write-Host "  2) Supabase Edge Functions"
        Write-Host "  3) Both platforms"
        Write-Host ""
        $choice = Read-Host "Enter choice [1-3]"

        switch ($choice) {
            "1" { $PlatformChoice = "cloudflare" }
            "2" { $PlatformChoice = "supabase" }
            "3" { $PlatformChoice = "both" }
            default {
                Write-Host "Invalid choice. Exiting." -ForegroundColor Red
                exit 1
            }
        }
    }

    # Track deployment results
    $CfSuccess = $false
    $SbSuccess = $false

    # Deploy based on selection
    switch ($PlatformChoice) {
        "cloudflare" {
            $CfSuccess = Deploy-Cloudflare
        }
        "supabase" {
            $SbSuccess = Deploy-Supabase
        }
        "both" {
            $CfSuccess = Deploy-Cloudflare
            $SbSuccess = Deploy-Supabase
        }
    }

    # Summary
    Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
    Write-Host "  Deployment Summary" -ForegroundColor Blue
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue

    if ($PlatformChoice -eq "cloudflare" -or $PlatformChoice -eq "both") {
        if ($CfSuccess) {
            Write-Host "✓ Cloudflare Workers: SUCCESS" -ForegroundColor Green
        } else {
            Write-Host "✗ Cloudflare Workers: FAILED" -ForegroundColor Red
        }
    }

    if ($PlatformChoice -eq "supabase" -or $PlatformChoice -eq "both") {
        if ($SbSuccess) {
            Write-Host "✓ Supabase Edge Functions: SUCCESS" -ForegroundColor Green
        } else {
            Write-Host "✗ Supabase Edge Functions: FAILED" -ForegroundColor Red
        }
    }

    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Blue

    # Exit with error if any deployment failed
    if (-not $CfSuccess -or -not $SbSuccess) {
        if ($PlatformChoice -eq "cloudflare" -and -not $CfSuccess) { exit 1 }
        if ($PlatformChoice -eq "supabase" -and -not $SbSuccess) { exit 1 }
        if ($PlatformChoice -eq "both" -and (-not $CfSuccess -or -not $SbSuccess)) { exit 1 }
    }

    exit 0
}

# Run main function
Main
