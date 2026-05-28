#!/bin/bash
# Start Agent Lens without file watching (avoids EMFILE errors)

PURPLE='\033[0;35m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${PURPLE}👁️  Starting Agent Lens (no-watch mode)${NC}\n"

# Kill existing processes
lsof -ti:4000 | xargs -r kill 2>/dev/null
lsof -ti:5173 | xargs -r kill 2>/dev/null

# Start server (no --watch flag)
echo -e "${GREEN}📡 Starting server on port 4000 (no auto-reload)...${NC}"
cd "$HOME/.claude/skills/agent-lens/apps/server"
bun src/index.ts > /tmp/agent-lens-server.log 2>&1 &
SERVER_PID=$!

sleep 2

# Start client
echo -e "${GREEN}🖥️  Starting client on port 5173...${NC}"
cd "$HOME/.claude/skills/agent-lens/apps/client"
bun run dev > /tmp/agent-lens-client.log 2>&1 &
CLIENT_PID=$!

sleep 3

echo ""
echo -e "${PURPLE}✅ Agent Lens started!${NC}"
echo -e "   ${BLUE}Dashboard:${NC} http://localhost:5173"
echo -e "   ${BLUE}Server:${NC} http://localhost:4000"
echo ""
echo -e "${BLUE}Logs:${NC}"
echo -e "   tail -f /tmp/agent-lens-server.log"
echo -e "   tail -f /tmp/agent-lens-client.log"
echo ""
echo -e "⚠️  Note: Server won't auto-reload on code changes"
echo -e "   Client will still hot-reload Vue components"
echo ""
