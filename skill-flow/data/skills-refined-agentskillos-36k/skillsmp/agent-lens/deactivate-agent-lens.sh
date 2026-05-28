#!/bin/bash
# Agent Lens Deactivation Script
# Reverts to the original UI

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SKILL_DIR="$HOME/.claude/skills/agent-observability"
CLIENT_DIR="$SKILL_DIR/apps/client/src"
MAIN_TS="$CLIENT_DIR/main.ts"
BACKUP="$MAIN_TS.backup"

echo -e "${BLUE}Reverting to Original UI${NC}\n"

if [ ! -f "$BACKUP" ]; then
    echo -e "${YELLOW}⚠️  No backup found. Creating default App.vue version...${NC}"

    cat > "$MAIN_TS" << 'EOF'
import { createApp } from 'vue'
import './styles/main.css'
import './styles/themes.css'
import './styles/compact.css'
import App from './App.vue'

createApp(App).mount('#app')
EOF

else
    echo -e "${BLUE}Restoring from backup...${NC}"
    cp "$BACKUP" "$MAIN_TS"
    echo -e "  ${GREEN}✅ Restored main.ts from backup${NC}"
fi

echo -e "\n${GREEN}✅ Reverted to original UI${NC}"
echo -e "   Restart the dev server to see changes.\n"
