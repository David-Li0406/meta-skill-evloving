---
name: mcp_mastery
description: Maîtrise des serveurs MCP (Filesystem, Docker, Browser) pour les agents A'Space OS.
---

---
description: Maîtrise des serveurs MCP (Filesystem, Docker, n8n) pour les agents A'Space OS.
name: mcp_mastery
---

# MCP Mastery Skill

## 📡 ANTIGRAVITY MCP PROTOCOL
1. **Discovery**: Always check for available MCP tools using `list_tools` (or equivalent) at the start of a task.
2. **Connectivity**: For `n8n`, prioritize the native MCP server over Webhooks/APIs.
3. **Configuration**:
   - URL: `http://localhost:5678` (Internal R1)
   - Auth: Bearer Token (Personal Access Token from n8n Settings).
4. **Resilience**: If an MCP tool fails, fallback to Shell commands only if explicitly allowed by the Manager.

## 🛠️ N8N MCP MASTER-CLASS
- **Exhibition**: Every workflow must have the "Enable MCP access" toggle ON in n8n.
- **Triggers**: Use `Webhook` or `Chat` triggers to expose functionality to the AI.
- **Validation**: Test persistence using the `agent_signals` table audit after each MCP execution.

## ⚖️ GOUVERNANCE
- Never invent tools.
- Log raw technical errors in `tracks.md`.
- Adhere to the Universal File Resolution Protocol for all file operations.
