#!/bin/bash
# Agent Lens Activation Script
# Switches the dashboard to use the new Agent Lens dual-pane UI

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

SKILL_DIR="$HOME/.claude/skills/agent-observability"
CLIENT_DIR="$SKILL_DIR/apps/client/src"
MAIN_TS="$CLIENT_DIR/main.ts"

echo -e "${BLUE}👁️  Agent Lens Activation${NC}\n"

# Backup original main.ts
if [ ! -f "$MAIN_TS.backup" ]; then
    echo -e "${BLUE}[1/3] Backing up original main.ts...${NC}"
    cp "$MAIN_TS" "$MAIN_TS.backup"
    echo -e "  ${GREEN}✅ Backup created: main.ts.backup${NC}"
else
    echo -e "${YELLOW}[1/3] Backup already exists, skipping...${NC}"
fi

# Update main.ts to use AppAgentLens
echo -e "\n${BLUE}[2/3] Updating main.ts to use Agent Lens UI...${NC}"

cat > "$MAIN_TS" << 'EOF'
import { createApp } from 'vue'
import './styles/main.css'
import './styles/themes.css'
import './styles/compact.css'
import AppAgentLens from './AppAgentLens.vue'

createApp(AppAgentLens).mount('#app')
EOF

echo -e "  ${GREEN}✅ main.ts updated${NC}"

# Show next steps
echo -e "\n${BLUE}[3/3] Next Steps${NC}"
echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "\n${GREEN}Agent Lens UI is now active!${NC}\n"
echo -e "To start the dashboard:\n"
echo -e "  ${BLUE}Terminal 1 - Server:${NC}"
echo -e "    cd $SKILL_DIR/apps/server"
echo -e "    bun run dev\n"
echo -e "  ${BLUE}Terminal 2 - Client:${NC}"
echo -e "    cd $SKILL_DIR/apps/client"
echo -e "    bun run dev\n"
echo -e "  ${BLUE}Browser:${NC}"
echo -e "    http://localhost:5173\n"

echo -e "${YELLOW}To revert to the old UI:${NC}"
echo -e "  ./deactivate-agent-lens.sh\n"

echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}\n"
