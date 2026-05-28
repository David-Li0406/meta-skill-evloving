---
name: agent-sdk-usage-guide
permissionMode: bypassPermissions
description: Umfassende Referenzdokumentation für Claude Agent SDK. Konzepte, Patterns, Best Practices - KEINE Skill-Erstellung.
---

# Agent SDK Usage Guide

Referenz-Skill für Fragen zum Claude Agent SDK. Beantwortet Konzeptfragen, erklärt Patterns und verweist auf offizielle Dokumentation.

**Abgrenzung:**
- **Dieser Skill**: Konzepterklärungen, Referenz, Troubleshooting, Best Practices
- **n8n-workflow-builder**: n8n Integration und Workflow-Design

---

## 1. Konzepte & Terminologie

### Claude Agent SDK

Die offizielle TypeScript-Bibliothek von Anthropic für agentic workflows:

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

for await (const message of query({ prompt, options })) {
  // Handle streaming messages
}
```

**Kernkonzepte:**

| Begriff | Bedeutung |
|---------|-----------|
| `query()` | Asynchroner Iterator für Agent-Ausführung |
| `bypassPermissions` | Headless Mode für Server (keine interaktiven Prompts) |
| `mcpServers` | MCP Server-Konfiguration (SSE/stdio) |
| `tools` | Available tools (preset oder custom) |
| `allowedTools` | Tool-Filter pro Request |
| `maxTurns` | Maximum Agent-Iterationen |

### Agent Worker

HTTP Service der das SDK als `/execute` Endpoint exposed:

```
POST /execute → SDK query() → MCP Hub Tools → Response
```

### Skills System

SKILL.md-Dateien die als System Prompt geladen werden:

```
skills/
├── my-skill/
│   └── SKILL.md              # System Prompt
└── agent-sdk-usage-guide/
    └── SKILL.md              # Dieser Skill
```

---

## 2. Architektur-Optionen

### Option A: n8n-Triggered (Empfohlen)

```
External Event → n8n (OAuth, Events, Secrets) → Agent Worker → MCP Hub
```

**Vorteile:**
- n8n handled OAuth & Event Subscriptions
- Visual Workflow Editor
- Built-in Retry Logic & Monitoring
- Execution History

### Option B: Standalone SDK (Advanced)

```
External Event → Agent Worker (direct webhook) → MCP Hub
```

**Wann nutzen:**
- Interne APIs ohne OAuth
- Scheduled Tasks (Cron)
- Performance-kritische Paths
- Keine komplexen Event Subscriptions

---

## 3. bypassPermissions Mode

**Was ist das?**

Mode für headless Server-Betrieb ohne interaktive CLI-Prompts.

**Konfiguration:**
```typescript
options: {
  permissionMode: 'bypassPermissions',
  allowDangerouslySkipPermissions: true
}
```

**WICHTIG - Root User Restriction:**

Das SDK verweigert bypassPermissions als root User. Dockerfile MUSS enthalten:

```dockerfile
USER node  # REQUIRED!
```

**Symptome ohne USER node:**
- SIGTERM crashes
- "bypassPermissions refused" Fehler
- Container startet, stirbt sofort

---

## 4. MCP Hub Integration

### SSE Connection

```typescript
mcpServers: {
  'hub': {
    type: 'sse',
    url: 'http://hub:8080/mcp/sse',
    headers: {
      'Authorization': `Bearer ${MCP_HUB_AUTH_TOKEN}`
    }
  }
}
```

### Tool Scoping

Per-Request Tool-Einschränkung:

```json
{
  "allowedTools": ["mcp__hub__notion_*", "mcp__hub__slack_*"]
}
```

**Scope-Strategien:**

| Use Case | allowedTools |
|----------|--------------|
| Capture Workflow | `["mcp__hub__notion_*", "mcp__hub__slack_*"]` |
| Research | `["WebSearch", "WebFetch", "mcp__hub__notion_*"]` |
| Minimal | `["mcp__hub__notion_API-create-a-page"]` |
| All (default) | _(parameter weglassen)_ |

---

## 5. Request/Response Contract

### POST /execute

**Request:**
```typescript
interface ExecuteRequest {
  prompt: string;              // Task description
  context?: object;            // Trigger data, metadata
  skill?: string;              // Skill name (loads SKILL.md)
  systemPrompt?: string;       // Alternative to skill
  maxTurns?: number;           // Default: 15
  model?: string;              // Default: claude-3-5-haiku-latest
  allowedTools?: string[];     // Tool scoping
}
```

**Response:**
```typescript
interface ExecuteResponse {
  success: boolean;
  result?: string;             // Agent's final output
  error?: string;              // Error message if failed
  skill?: string;
  model?: string;
  turns?: number;              // Agent turns used
  usage?: object;              // Token usage
  total_cost_usd?: number;
  duration_ms?: number;
}
```

---

## 6. Skill Authoring

### SKILL.md Template

```markdown
# Skill Name

[Clear description of what this agent does]

## Task

[Specific instructions for the agent]

## Tools Available

- `mcp__hub__notion_*` - Notion operations
- `mcp__hub__slack_*` - Slack operations

## Output Format

[Specify expected output structure]

## Error Handling

[How to handle failures gracefully]
```

### Best Practices

**Do:**
- Keep n8n minimal (trigger + HTTP request only)
- Put all logic in SKILL.md
- Use tool scoping for security
- Test with Haiku first (cost optimization)

**Don't:**
- Store secrets in skills (use n8n or env vars)
- Hardcode URLs in skills (use context)
- Skip tool scoping for production
- Use Sonnet/Opus unless needed

### Live Updates

Skills werden bei jedem `/execute` Call neu geladen:

```bash
# Update skill
vim skills/my-skill/SKILL.md

# No restart needed - next /execute uses new version
```

---

## 7. Error Handling & Debugging

### Result Subtype

**Korrekt:**
```typescript
const isSuccess = message.subtype === 'success';
```

### Common Issues

| Issue | Ursache | Fix |
|-------|---------|-----|
| SIGTERM crash | Running as root | `USER node` in Dockerfile |
| MCP tools 404 | Wrong SSE URL | Use `/mcp/sse` not `/mcp` |
| Skill not found | Wrong path | Check `/app/skills/{name}/SKILL.md` |
| Timeout | Too many turns | Reduce `maxTurns` or use Haiku |

---

## 8. Model Selection

### Model-Strategie

| Task Type | Model | Rationale |
|-----------|-------|-----------|
| Simple capture | `claude-3-5-haiku-latest` | Cost-effective (~50% savings) |
| Research + synthesis | `claude-sonnet-4-20250514` | Better reasoning |
| Complex orchestration | `claude-opus-4-5-20251101` | Highest capability |

### Per-Request Override

```json
{
  "model": "claude-sonnet-4-20250514"
}
```

---

## 9. Deployment

### Docker Compose

```yaml
agent-worker:
  build: ./services/agent-worker
  ports:
    - "3007:3007"
  environment:
    - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    - MCP_HUB_URL=http://hub:8080/mcp/sse
    - MCP_HUB_AUTH_TOKEN=${MCP_HUB_AUTH_TOKEN}
    - CLAUDE_MODEL=claude-3-5-haiku-latest
  volumes:
    - ./skills:/app/skills:ro
  user: node  # IMPORTANT!
```

### Dockerfile Critical Lines

```dockerfile
RUN mkdir -p /home/node/.claude && chown -R node:node /home/node
RUN chown -R node:node /app
USER node  # REQUIRED for bypassPermissions!
```

### Environment Variables

| Env Var | Default | Required |
|---------|---------|----------|
| `ANTHROPIC_API_KEY` | - | Yes |
| `CLAUDE_MODEL` | `claude-3-5-haiku-latest` | No |
| `MCP_HUB_URL` | `http://hub:8080/mcp/sse` | No |
| `MCP_HUB_AUTH_TOKEN` | - | No |
| `SKILLS_PATH` | `/app/skills` | No |

---

## Referenzen

### Offizielle Dokumentation

- [Claude Agent SDK Overview](https://docs.anthropic.com/en/docs/agents-and-tools/claude-agent-sdk/overview)
- [TypeScript SDK Reference](https://docs.anthropic.com/en/docs/agents-and-tools/claude-agent-sdk/typescript)
- [NPM: @anthropic-ai/claude-agent-sdk](https://www.npmjs.com/package/@anthropic-ai/claude-agent-sdk)
