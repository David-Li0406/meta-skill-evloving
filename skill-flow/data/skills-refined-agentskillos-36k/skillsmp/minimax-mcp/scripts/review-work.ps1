# MiniMax Work Reviewer (PowerShell version)
# Usage: .\review-work.ps1 "Context: what I did" "Question/Decision (optional)"

param(
    [Parameter(Mandatory=$true)]
    [string]$Context,

    [Parameter(Mandatory=$false)]
    [string]$Question = "Review this work for potential issues."
)

$ApiKey = "sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c"
$ApiHost = "https://api.minimax.io"

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  MiniMax Work Reviewer" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Context: $Context" -ForegroundColor Yellow
Write-Host "Question: $Question" -ForegroundColor Yellow
Write-Host ""
Write-Host "Searching documentation standards..." -ForegroundColor Gray

# Search for relevant documentation standards
$Query = "site:docs.anthropic.com OR site:godotengine.org code review documentation standards"
$Body = @{ q = $Query } | ConvertTo-Json

$Response = Invoke-RestMethod -Uri "$ApiHost/v1/coding_plan/search" `
    -Method POST `
    -Headers @{
        "Authorization" = "Bearer $ApiKey"
        "Content-Type" = "application/json"
        "MM-API-Source" = "Minimax-MCP"
    } `
    -Body $Body

Write-Host ""
Write-Host "Found $($Response.organic.Count) relevant documentation references" -ForegroundColor Green
Write-Host ""

# Extract and display top 3 results
Write-Host "Top References:" -ForegroundColor Cyan
Write-Host "-------------" -ForegroundColor Gray
for ($i = 0; $i -lt [Math]::Min(3, $Response.organic.Count); $i++) {
    Write-Host "$($i+1). $($Response.organic[$i].title)" -ForegroundColor White
}
Write-Host ""

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Review Summary" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "WORK UNDER REVIEW:" -ForegroundColor Yellow
Write-Host "  $Context"
Write-Host ""
Write-Host "QUESTION:" -ForegroundColor Yellow
Write-Host "  $Question"
Write-Host ""
Write-Host "REVIEW CONSIDERATIONS:" -ForegroundColor Yellow
Write-Host "  1. Does this change align with documentation standards?"
Write-Host "  2. Are all cross-references and links correct?"
Write-Host "  3. Is terminology consistent with other files?"
Write-Host "  4. What edge cases might occur?"
Write-Host ""
Write-Host "RECOMMENDATION:" -ForegroundColor Yellow
Write-Host "  [PROCEED / REVISE / RECONSIDER]"
Write-Host ""
Write-Host "Note: Use judgment in applying this review feedback." -ForegroundColor Gray
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
