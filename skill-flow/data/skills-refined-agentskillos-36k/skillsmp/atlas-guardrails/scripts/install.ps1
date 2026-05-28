# Atlas Guardrails Installer for Windows

Write-Host "      ___           ___           ___           ___           ___     " -ForegroundColor Cyan
Write-Host "     /\  \         /\  \         /\__\         /::\  \       /::\  \    " -ForegroundColor Cyan
Write-Host "    /::\  \        \:\  \       /:/  /        /:/\:\  \     /:/\ \  \   " -ForegroundColor Cyan
Write-Host "   /:/\:\  \        \:\  \     /:/  /        /:/\:\  \   _\:\~\ \  \ " -ForegroundColor Cyan
Write-Host "  /::\~\:\  \       /::\  \   /:/  /        /::\~\:\  \ /\ \:\ \ \__\ " -ForegroundColor Cyan
Write-Host " /:/\:\ \:\__\     /:/\:\__\ /:/__/        /:/\:\ \:\__\ /\ \:\ \ \/__/" -ForegroundColor Cyan
Write-Host " \/__\:\/:/  /    /:/  \/__/ \:\  \        \/__\:\/:/  / \:\ \:\__\  " -ForegroundColor Cyan
Write-Host "      \::/  /    /:/  /       \:\  \            \::/  /   \:\/:/  /  " -ForegroundColor Cyan
Write-Host "      /:/  /    /:/  /         \:\  \           /:/  /     \::/  /   " -ForegroundColor Cyan
Write-Host "     /:/  /    /:/  /           \:\__\         /:/  /       \::/  /    " -ForegroundColor Cyan
Write-Host "     \/__/     \/__/             \/__/         \/__/         \/__/     " -ForegroundColor Cyan
Write-Host ""
Write-Host "Installing Atlas Guardrails..." -ForegroundColor Green

# 1. Check Node
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Error "Node.js not found. Please install Node.js v18+ first."
    exit 1
}

# 2. Install Package
Write-Host "📦 Installing via npm..."
npm install -g atlas-guardrails

# 3. Configure Claude Desktop
$AppData = [Environment]::GetFolderPath("ApplicationData")
$ClaudeConfigDir = Join-Path $AppData "Claude"
$ClaudeConfigFile = Join-Path $ClaudeConfigDir "claude_desktop_config.json"

if (Test-Path $ClaudeConfigDir) {
    Write-Host "🤖 Configuring Claude Desktop..."
    if (-not (Test-Path $ClaudeConfigFile)) {
        Set-Content -Path $ClaudeConfigFile -Value '{ "mcpServers": {} }'
    }

    $nodeScript = @"
    const fs = require('fs');
    const path = '$ClaudeConfigFile'.replace(/\\/g, '\\\\');
    try {
        const conf = JSON.parse(fs.readFileSync(path, 'utf8'));
        conf.mcpServers = conf.mcpServers || {};
        conf.mcpServers.atlas = { command: 'atlas.cmd', args: ['mcp'] };
        fs.writeFileSync(path, JSON.stringify(conf, null, 2));
        console.log('✅ Added Atlas to Claude Desktop config.');
    } catch(e) { console.error('Failed to update config:', e); }
"@
    node -e $nodeScript
} else {
    Write-Host "Claude Desktop config not found. Skipping." -ForegroundColor Yellow
}

Write-Host "✨ Installation Complete!" -ForegroundColor Green
Write-Host "Run 'atlas index' in your repo to get started."
