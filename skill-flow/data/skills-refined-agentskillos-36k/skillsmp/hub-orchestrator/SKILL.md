---
name: hub-orchestrator
description: System exploration and management skill for MCP Hub Boilerplate. Use when users want to explore the hub system, check status, understand available tools, or get help navigating the boilerplate.
---

# Hub Orchestrator

System exploration and management skill for MCP Hub Boilerplate.

## Trigger

User asks to:
- Explore the MCP Hub system
- Understand available tools and services
- Get help with the boilerplate
- Check system status

## Instructions

### 1. Identify User Intent

Determine what the user wants:
- **Exploration**: Show system overview, available tools, services
- **Health Check**: Report on service status
- **Help**: Guide to relevant documentation or skills
- **Configuration**: Direct to hub-customize skill

### 2. System Overview

When showing system overview:

1. List available services:
   - Hub (core gateway)
   - Notion (if NOTION_TOKEN set)
   - Agent Worker (if ANTHROPIC_API_KEY_LIMITED set)
   - Dashboard (if DASHBOARD_ENABLED)

2. List available tools:
   - Core: ping, list_tools, get_service_health
   - Notion: invoke_notion_tool, list_notion_tools
   - Agent: agent_execute

3. List configured users (Götterboten):
   - Read from /clients/*/config.json
   - Show name, access level, tools

### 3. Health Check

When checking health:

1. Call `get_service_health` tool
2. Report status of each service
3. Highlight any issues or warnings
4. Suggest fixes for common problems

### 4. Help Navigation

Direct users to:
- `/docs/CUSTOMIZATION.md` - Renaming, branding
- `/docs/OAUTH_SETUP.md` - Cloud client access
- `/docs/DNS_SETUP.md` - Domain configuration
- `/docs/HITL_SETUP.md` - IDE integration
- `/docs/N8N_SETUP.md` - Workflow automation

### 5. Delegation

If user needs:
- **Customization**: "Let me invoke the hub-customize skill for guided setup"
- **Notion operations**: Use invoke_notion_tool
- **Autonomous tasks**: Use agent_execute (if available)

## Tools Available

- ping
- list_tools
- get_service_health

## Example Interactions

**User**: "What can this hub do?"
**Response**: Show system overview with services and tools

**User**: "Is everything working?"
**Response**: Run health check and report status

**User**: "How do I add a new user?"
**Response**: Guide to clients/_template and CUSTOMIZATION.md

**User**: "I want to rebrand this for my company"
**Response**: Invoke hub-customize skill
