#!/bin/bash
set -e

# ANSI Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}"
echo "      ___           ___           ___           ___           ___     "
echo "     /\  \         /\  \         /\__\         /\  \         /\  \    "
echo "    /::\  \        \:\  \       /:/  /        /::\  \       /::\  \   "
echo "   /:/\:\  \        \:\  \     /:/  /        /:/\:\  \     /:/\ \  \  "
echo "  /::\~\:\  \       /::\  \   /:/  /        /::\~\:\  \   _\:\~\ \  \ "
echo " /:/\:\ \:\__\     /:/\:\__\ /:/__/        /:/\:\ \:\__\ /\ \:\ \ \__\"
echo " \/__\:\/:/  /    /:/  \/__/ \:\  \        \/__\:\/:/  / \:\ \:\ \/__/"
echo "      \::/  /    /:/  /       \:\  \            \::/  /   \:\ \:\__\  "
echo "      /:/  /    /:/  /         \:\  \           /:/  /     \:\/:/  /  "
 echo "     /:/  /    /:/  /           \:\__\         /:/  /       \::/  /   "
echo "     \/__/     \/__/             \/__/         \/__/         \/__/    "
echo -e "${NC}"
echo -e "${CYAN}Installing Atlas Guardrails...${NC}"

# 1. Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}Node.js not found. Please install Node.js v18+ first.${NC}"
    exit 1
fi

# 2. Install Global Package
echo -e "📦 Installing via npm..."
npm install -g atlas-guardrails

# 3. Configure Claude Desktop
CLAUDE_CONFIG_DIR="$HOME/Library/Application Support/Claude"
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    CLAUDE_CONFIG_DIR="$HOME/.config/Claude"
fi

CLAUDE_CONFIG_FILE="$CLAUDE_CONFIG_DIR/claude_desktop_config.json"

if [ -d "$CLAUDE_CONFIG_DIR" ]; then
    echo -e "🤖 Configuring Claude Desktop..."
    if [ ! -f "$CLAUDE_CONFIG_FILE" ]; then
        echo '{ "mcpServers": {} }' > "$CLAUDE_CONFIG_FILE"
    fi
    
    # Simple JSON injection (requires node)
    node -e "
    const fs = require('fs');
    const path = '$CLAUDE_CONFIG_FILE';
    try {
        const conf = JSON.parse(fs.readFileSync(path, 'utf8'));
        conf.mcpServers = conf.mcpServers || {};
        conf.mcpServers.atlas = { command: 'atlas', args: ['mcp'] };
        fs.writeFileSync(path, JSON.stringify(conf, null, 2));
        console.log('✅ Added Atlas to Claude Desktop config.');
    } catch(e) { console.error('Failed to update config:', e); }
    "
else
    echo -e "${YELLOW}Claude Desktop not found. Skipping auto-config.${NC}"
fi

# 4. Configure Codex CLI
CODEX_CONFIG_DIR="$HOME/.codex"
if [ -d "$CODEX_CONFIG_DIR" ]; then
    echo -e "🧠 Configuring Codex..."
    # Add logic if Codex config format is known (assuming TOML/JSON)
    echo -e "   Run 'codex mcp install atlas' (simulated)"
fi

echo -e "${GREEN}✨ Installation Complete!${NC}"
echo -e "Run ${CYAN}atlas index${NC} in your repo to get started."
