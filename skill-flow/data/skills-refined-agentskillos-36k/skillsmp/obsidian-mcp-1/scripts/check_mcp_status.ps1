# Check Obsidian MCP Status
# This script displays the current MCP configuration status

$mcpConfigPath = "$PSScriptRoot\..\..\..\..\.vscode\mcp.json"

Write-Host "`n=== Obsidian MCP Status ===" -ForegroundColor Cyan

if (Test-Path $mcpConfigPath) {
    Write-Host "Config file: FOUND" -ForegroundColor Green
    Write-Host "Location: $mcpConfigPath" -ForegroundColor Gray
    
    $mcpConfig = Get-Content $mcpConfigPath | ConvertFrom-Json
    
    if ($mcpConfig.servers.PSObject.Properties.Name -contains "obsidian") {
        Write-Host "`nObsidian MCP: ENABLED" -ForegroundColor Green
        Write-Host "Command: $($mcpConfig.servers.obsidian.command)" -ForegroundColor Gray
        Write-Host "Args: $($mcpConfig.servers.obsidian.args -join ' ')" -ForegroundColor Gray
    } else {
        Write-Host "`nObsidian MCP: NOT CONFIGURED" -ForegroundColor Yellow
    }
    
    # List all configured servers
    $serverCount = $mcpConfig.servers.PSObject.Properties.Count
    if ($serverCount -gt 0) {
        Write-Host "`nConfigured servers ($serverCount):" -ForegroundColor Cyan
        $mcpConfig.servers.PSObject.Properties.Name | ForEach-Object {
            Write-Host "  - $_" -ForegroundColor Gray
        }
    }
} else {
    Write-Host "Config file: NOT FOUND" -ForegroundColor Yellow
    Write-Host "Location: $mcpConfigPath" -ForegroundColor Gray
    Write-Host "`nObsidian MCP: DISABLED" -ForegroundColor Red
}

Write-Host "`n========================`n" -ForegroundColor Cyan
