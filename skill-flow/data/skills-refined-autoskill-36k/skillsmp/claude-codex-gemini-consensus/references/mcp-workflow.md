# MCP Integration Workflow

Using Codex and Gemini as MCP servers for Claude Code integration.

## Codex as MCP Server

Codex can run as an MCP server, allowing other agents to consume it:

```bash
# Start Codex as MCP server
codex mcp-server
```

### Claude Code MCP Configuration

Add to your Claude Code MCP settings:

```json
{
  "mcpServers": {
    "codex-cli": {
      "command": "codex",
      "args": ["mcp-server"],
      "env": {
        "OPENAI_API_KEY": "your-key"
      }
    }
  }
}
```

## Direct Tool Invocation Pattern

When MCP servers are configured, use this pattern in Claude Code:

### Codex MCP Tool Call

```
Use mcp__codex-cli__codex with parameters:
- model: "gpt-5.2-codex"
- reasoningEffort: "high"
- sandbox: "danger-full-access"
- fullAuto: true
- workingDirectory: "/path/to/project"
- sessionId: "unique-session-id"  # For continuity
- prompt: "Your task here"
```

### Gemini MCP Tool Call

```
Use mcp__gemini-cli__gemini with parameters:
- model: "gemini-3-pro-preview"
- yolo: true
- prompt: "Your task here"
```

## Consensus Workflow with MCP

### Step 1: Claude Proposes Plan

Claude creates initial implementation plan.

### Step 2: Submit to Codex via MCP

```python
# Conceptual MCP call
codex_result = mcp__codex-cli__codex(
    model="gpt-5.2-codex",
    reasoningEffort="high",
    sandbox="danger-full-access",
    fullAuto=True,
    workingDirectory=os.getcwd(),
    sessionId="review-session-001",
    prompt=f"""
    Review this implementation plan critically for clinical research.
    
    REQUIRED CHECKS:
    1. Logical correctness
    2. Edge cases
    3. Security
    4. Performance
    5. Maintainability
    
    BE CRITICAL. DO NOT APPROVE BLINDLY.
    
    Plan:
    {plan_text}
    """
)
```

### Step 3: Submit to Gemini via MCP

```python
# Conceptual MCP call
gemini_result = mcp__gemini-cli__gemini(
    model="gemini-3-pro-preview",
    yolo=True,
    prompt=f"""
    Review this implementation plan critically for clinical research.
    
    REQUIRED CHECKS:
    1. Logical correctness
    2. Edge cases
    3. Security
    4. Performance
    5. Maintainability
    
    BE CRITICAL. DO NOT APPROVE BLINDLY.
    
    Plan:
    {plan_text}
    """
)
```

### Step 4: Synthesize and Reach Consensus

1. Compare Codex and Gemini feedback
2. Identify agreements and disagreements
3. Argue each point of contention
4. Iterate until all three agents agree

## MCP Parameters Reference

### Codex MCP Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (e.g., "gpt-5.2-codex") |
| `reasoningEffort` | string | "low", "medium", "high" |
| `sandbox` | string | "read-only", "workspace-write", "danger-full-access" |
| `fullAuto` | boolean | Skip approval prompts |
| `workingDirectory` | string | Project root path |
| `sessionId` | string | For session continuity |
| `prompt` | string | The task/question |

### Gemini MCP Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (e.g., "gemini-3-pro-preview") |
| `yolo` | boolean | Auto-approve all tools |
| `sandbox` | boolean | Run in Docker container |
| `prompt` | string | The task/question |

## Session Continuity

### Codex Sessions

Use `sessionId` to maintain context across calls:

```python
SESSION = "project-review-2024-01"

# First call
codex_result = mcp__codex-cli__codex(
    sessionId=SESSION,
    prompt="Review the architecture plan..."
)

# Follow-up call (same session context)
codex_result = mcp__codex-cli__codex(
    sessionId=SESSION,
    prompt="Now review the implementation based on your earlier feedback..."
)
```

### Gemini Sessions

Use `--resume` pattern in sequential calls:

```bash
# First call creates session
gemini --yolo -p "Review plan..."

# Resume same session
gemini --resume latest -p "Now check implementation..."
```

## Error Handling

```python
try:
    result = mcp__codex-cli__codex(...)
    if "error" in result.lower():
        # Retry or escalate
        pass
except MCPError as e:
    # Handle connection/auth errors
    print(f"Codex MCP failed: {e}")
    # Fallback to direct CLI call
    subprocess.run(["codex", "exec", "--full-auto", prompt])
```

## Best Practices

1. **Always set working directory** - Ensures consistent file access
2. **Use session IDs** - Maintains context for multi-step reviews
3. **Set high reasoning effort** - For critical clinical research code
4. **Enable full auto** - For non-interactive workflows
5. **Capture and log outputs** - For audit trail
6. **Handle failures gracefully** - Retry or use fallback
