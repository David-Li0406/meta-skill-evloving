# Environment Variables Checker Script (Windows PowerShell)

# Exit on error
$ErrorActionPreference = "Stop"

# Get the script's directory and navigate to project root
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Resolve-Path (Join-Path $ScriptDir "../../../..")

# Define required and optional environment variables
$RequiredVars = @("CLOUDFLARE_API", "CLOUDFLARE_ACCOUNT_ID")
$OptionalVars = @("SUPABASE_URL", "SUPABASE_ANON_KEY", "SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_PROJECT_REF")

# Counters
$RequiredSet = 0
$RequiredTotal = $RequiredVars.Count
$OptionalSet = 0
$OptionalTotal = $OptionalVars.Count
$HasPlaceholders = $false

# Function to check if value is a placeholder
function Test-IsPlaceholder {
    param($Value)
    if ($Value -match "(your-.*-here|your_.*_here|<.*>|xxxxx|abcdefg)") {
        return $true
    }
    return $false
}

# Function to check environment variable
function Test-EnvVar {
    param(
        [string]$VarName,
        [bool]$IsRequired
    )

    $Value = [Environment]::GetEnvironmentVariable($VarName, "Process")

    if ([string]::IsNullOrEmpty($Value)) {
        Write-Host "❌ ${VarName}: Not set" -ForegroundColor Red
        if ($IsRequired) {
            Write-Host "   → This variable is required for deployment" -ForegroundColor Yellow
        }
        return 1
    }
    elseif (Test-IsPlaceholder $Value) {
        Write-Host "⚠️  ${VarName}: Placeholder value detected" -ForegroundColor Yellow
        Write-Host "   → Replace with actual value" -ForegroundColor Cyan
        $script:HasPlaceholders = $true
        return 2
    }
    else {
        # Mask sensitive values in output
        $DisplayValue = $Value.Substring(0, [Math]::Min(20, $Value.Length))
        if ($Value.Length -gt 20) {
            $DisplayValue = $DisplayValue + "..."
        }
        Write-Host "✅ ${VarName}: Set" -ForegroundColor Green
        return 0
    }
}

# Main function
function Main {
    Write-Host ""
    Write-Host "╔═══════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║   Environment Variables Check             ║" -ForegroundColor Cyan
    Write-Host "╚═══════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""

    # Check if .env file exists
    $EnvFile = Join-Path $ProjectRoot ".env"
    if (-not (Test-Path $EnvFile)) {
        Write-Host "❌ Error: .env file not found in project root`n" -ForegroundColor Red
        Write-Host "To create your .env file:" -ForegroundColor Yellow
        Write-Host "  1. Copy .env.example: " -NoNewline
        Write-Host "copy .env.example .env" -ForegroundColor Cyan
        Write-Host "  2. Edit .env and add your credentials"
        Write-Host "`nSee README.md for instructions on obtaining credentials.`n" -ForegroundColor Yellow
        exit 1
    }

    # Load environment variables
    Get-Content $EnvFile | ForEach-Object {
        if ($_ -match '^([^#][^=]+)=(.+)$') {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim().Trim('"')
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
        }
    }

    # Check Cloudflare variables (Required)
    Write-Host "Cloudflare Workers (Required)" -ForegroundColor Blue
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
    foreach ($var in $RequiredVars) {
        $result = Test-EnvVar -VarName $var -IsRequired $true
        if ($result -eq 0) {
            $script:RequiredSet++
        }
    }

    # Check Supabase variables (Optional)
    Write-Host "`nSupabase (Optional)" -ForegroundColor Blue
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
    foreach ($var in $OptionalVars) {
        $result = Test-EnvVar -VarName $var -IsRequired $false
        if ($result -eq 0 -or $result -eq 2) {
            $script:OptionalSet++
        }
    }

    # Summary
    Write-Host "`nSummary" -ForegroundColor Blue
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue

    if ($RequiredSet -eq $RequiredTotal) {
        Write-Host "✅ Required variables: $RequiredSet/$RequiredTotal configured" -ForegroundColor Green
    }
    else {
        Write-Host "❌ Required variables: $RequiredSet/$RequiredTotal configured" -ForegroundColor Red
        $missing = $RequiredTotal - $RequiredSet
        Write-Host "   Missing: $missing required variable(s)" -ForegroundColor Yellow
    }

    if ($OptionalSet -gt 0) {
        Write-Host "ℹ️  Optional variables: $OptionalSet/$OptionalTotal configured" -ForegroundColor Cyan
    }
    else {
        Write-Host "ℹ️  Optional variables: None configured (Supabase features disabled)" -ForegroundColor Cyan
    }

    # Setup instructions if needed
    if ($RequiredSet -lt $RequiredTotal -or $HasPlaceholders) {
        Write-Host "`nSetup Instructions:" -ForegroundColor Yellow
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue

        if ($RequiredSet -lt $RequiredTotal) {
            Write-Host "`nCloudflare Credentials:" -ForegroundColor Yellow
            Write-Host "  1. Dashboard: " -NoNewline
            Write-Host "https://dash.cloudflare.com" -ForegroundColor Cyan
            Write-Host "  2. Get Account ID from Workers & Pages section"
            Write-Host "  3. API Tokens: " -NoNewline
            Write-Host "https://dash.cloudflare.com/profile/api-tokens" -ForegroundColor Cyan
            Write-Host "  4. Create token using 'Edit Cloudflare Workers' template"
        }

        if ($HasPlaceholders) {
            Write-Host "`nSupabase Credentials (if using):" -ForegroundColor Yellow
            Write-Host "  1. Dashboard: " -NoNewline
            Write-Host "https://supabase.com/dashboard" -ForegroundColor Cyan
            Write-Host "  2. Select your project > Settings > API"
            Write-Host "  3. Copy Project URL, Project Ref, and API keys"
        }

        Write-Host "`nAfter updating .env, run this check again:" -ForegroundColor Cyan
        Write-Host "  /check-envs" -ForegroundColor Cyan
        Write-Host ""
    }

    # Exit status
    if ($RequiredSet -eq $RequiredTotal) {
        Write-Host "`n✅ Environment configuration is valid for deployment!`n" -ForegroundColor Green
        exit 0
    }
    else {
        Write-Host "`n❌ Environment configuration is incomplete." -ForegroundColor Red
        Write-Host "Please configure missing required variables before deploying.`n" -ForegroundColor Yellow
        exit 1
    }
}

# Run main function
Main
