---
name: new-agent
description: Create a new backend agent for the Claude Assistant Platform. Use when adding a new specialized agent, scaffolding an agent, or when the user says "create agent", "add agent", "new agent", or "scaffold agent".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Create New Agent

This skill scaffolds a new specialized agent following the established patterns.

## Prerequisites

Before creating an agent, gather:
1. **Agent name** (snake_case, e.g., `slack_agent`)
2. **Agent purpose** (what domain it handles)
3. **MCP server URL** (if connecting to external service)

## Complete Steps

### Step 1: Create Agent File

Create `Backend/src/agents/{name}_agent.py` using the template in [TEMPLATE.md](TEMPLATE.md).

**Key points:**
- Use `input_data` and `output_data` parameters for `log_tool_call()` (NOT `tool_input`/`tool_output`)
- Follow the pattern from existing agents like `gmail_agent.py` or `google_drive_agent.py`

### Step 2: Register in `__init__.py`

Add to `Backend/src/agents/__init__.py`:

```python
from src.agents.{name}_agent import {Name}Agent

__all__ = [
    # ... existing exports ...
    "{Name}Agent",
]
```

### Step 3: Register in `main.py`

Add to `Backend/src/api/main.py`:

1. Add import at top:
```python
from src.agents.{name}_agent import {Name}Agent
```

2. Add registration in `lifespan()` function (after other agent registrations):
```python
# Register {Name} Agent if configured
if settings.{name}_is_configured:
    {name}_agent = {Name}Agent(
        api_key=settings.anthropic_api_key,
        model=settings.claude_model,
        mcp_url=settings.{name}_mcp_url,
    )
    orchestrator.register_agent({name}_agent)
    logger.info(
        f"Registered {Name}Agent with orchestrator "
        f"(MCP: {settings.{name}_mcp_url})"
    )
else:
    logger.info(
        "{Name} integration disabled - {Name}Agent not registered"
    )
```

### Step 4: Add Settings Configuration

Add to `Backend/src/config/settings.py`:

```python
# {Name} MCP Configuration
{name}_mcp_host: str = Field(
    default="{name}-mcp",
    description="Hostname of the {Name} MCP server.",
)
{name}_mcp_port: int = Field(
    default=808X,
    description="Port of the {Name} MCP server.",
)
{name}_enabled: bool = Field(
    default=False,
    description="Whether {Name} integration is enabled.",
)

@property
def {name}_is_configured(self) -> bool:
    """Check if {Name} integration is configured."""
    return self.{name}_enabled

@property
def {name}_mcp_url(self) -> str:
    """Get the full {Name} MCP URL."""
    return f"http://{self.{name}_mcp_host}:{self.{name}_mcp_port}"
```

### Step 5: Update Orchestrator System Prompt

Edit `Backend/src/agents/orchestrator.py`:

Add to the routing guidelines section:
```
X. **{Name} Operations** → Delegate to `{name}` agent (when available)
   - {Capability 1}
   - {Capability 2}
   - {Capability 3}
```

### Step 6: Add Environment Variables

Add to `.env.example`:
```env
# {Name} Integration
{NAME}_ENABLED=true
{NAME}_MCP_HOST=localhost
{NAME}_MCP_PORT=808X
```

Add to your `.env`:
```env
{NAME}_ENABLED=true
{NAME}_MCP_HOST=localhost
{NAME}_MCP_PORT=808X
```

### Step 7: Add to Routing Database (CRITICAL!)

Insert agent into `routing.agents` table:

```sql
INSERT INTO routing.agents (name, display_name, description, keywords, regex_patterns, enabled, priority)
VALUES (
    '{name}',
    '{Name} Agent',
    '{Description of what the agent does. Be specific about when to use it.}',
    ARRAY['keyword1', 'keyword2', 'keyword3', ...],
    ARRAY[
        '\b(pattern1|pattern2)\b',
        '\b(action).*(noun)\b'
    ],
    true,
    {priority}  -- Lower = higher priority (github=10, todo=20, email=30, etc.)
);
```

### Step 8: Add to AGENT_PATTERNS (Tier 1 Routing)

**CRITICAL:** Add regex patterns to `Backend/src/services/router_service.py` for fast Tier 1 routing:

```python
AGENT_PATTERNS: dict[str, list[str]] = {
    # ... existing agents ...
    "{name}": [
        r"\b({keyword1}|{keyword2})\b",
        r"\b({action}).{0,20}({noun})\b",
        # Add patterns that uniquely identify requests for this agent
    ],
}
```

**Pattern Guidelines:**
- Use word boundaries `\b` to avoid partial matches
- Use `.{0,20}` for flexible word gaps (not `.*` which is greedy)
- Test patterns with the message text before adding
- Multiple matches increase confidence

### Step 9: Generate Embeddings

After adding to database, restart backend OR call:

```bash
curl -X POST http://localhost:8000/api/router/generate-embeddings
```

This generates vector embeddings for the hybrid router to route requests correctly.

## Verification Checklist

After creation, verify:

- [ ] Agent file created at `Backend/src/agents/{name}_agent.py`
- [ ] Agent extends `BaseAgent`
- [ ] `name`, `description`, and `tools` properties defined
- [ ] System prompt describes all available tools
- [ ] Tool definitions use JSON schema format
- [ ] Tool handlers use `input_data`/`output_data` params (NOT `tool_input`/`tool_output`)
- [ ] MCP URL passed via constructor
- [ ] Agent exported in `__init__.py`
- [ ] Agent registered in `main.py` lifespan
- [ ] Settings added to `settings.py`
- [ ] Orchestrator system prompt updated
- [ ] Environment variables added to `.env.example` and `.env`
- [ ] Agent inserted into `routing.agents` table
- [ ] **AGENT_PATTERNS updated in `router_service.py`** (Tier 1 routing)
- [ ] Embeddings generated (check "X agents, X embeddings" in logs)
- [ ] Backend restarted and healthy
- [ ] Test routing works (use NEW message text to avoid cache)

## File Locations

| File | Purpose |
|------|---------|
| `Backend/src/agents/{name}_agent.py` | Agent implementation |
| `Backend/src/agents/__init__.py` | Agent export |
| `Backend/src/api/main.py` | Agent registration |
| `Backend/src/config/settings.py` | Settings configuration |
| `Backend/src/agents/orchestrator.py` | Routing guidelines |
| `Backend/src/services/router_service.py` | AGENT_PATTERNS for Tier 1 routing |
| `.env.example` | Environment variable template |
| `.env` | Environment variables |
| `routing.agents` table | Hybrid router configuration |

## Troubleshooting

### "No specialized agents registered"
- The chat route was creating a new orchestrator. Fixed by using `request.app.state.orchestrator`
- Check that agents are registered during startup in logs

### Router not routing to new agent
- Agent missing from `routing.agents` database table
- Embeddings not generated - call `/api/router/generate-embeddings`
- Check logs for "X agents, X embeddings" - numbers should match
- **AGENT_PATTERNS missing** - Add patterns to `router_service.py` for Tier 1 matching

### Routing to wrong agent (cached routing)
- **Routing decisions are cached in Redis for 5 minutes**
- During testing, use different message text to avoid cache hits
- Or refresh the router cache:
  ```bash
  curl -X POST http://localhost:8000/api/router/refresh
  ```
- Check logs for "Direct routing to 'X' (tier=Y)" to see routing decisions

### "log_tool_call() got unexpected keyword argument"
- Use `input_data` and `output_data`, NOT `tool_input` and `tool_output`

### Agent not listed in orchestrator
- Check `main.py` registration is inside the correct `if` block
- Verify environment variable `{NAME}_ENABLED=true` is set

## Reference

- [TEMPLATE.md](TEMPLATE.md) - Full agent code template
- `.claude/rules/backend/agents.md` - Agent patterns and anti-patterns
- `Backend/src/agents/google_drive_agent.py` - Real-world example
- `Backend/src/agents/gmail_agent.py` - Another example
