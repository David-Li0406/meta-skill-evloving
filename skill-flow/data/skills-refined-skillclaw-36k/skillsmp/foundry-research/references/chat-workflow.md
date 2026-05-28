# Chat Workflow

Single-model conversational research with thread persistence.

## When to Use

- **Follow-up questions** on a previous response
- **Iterative refinement** of ideas or explanations
- **Deep-dive** into a specific topic with one model
- **Continuity needed** across multiple exchanges

## MCP Usage

```bash
mcp__plugin_foundry_foundry-mcp__research action="chat" prompt="Your question" thread_id="thread-abc123"
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `prompt` | Yes | - | The question or follow-up |
| `thread_id` | No | New thread | Resume existing conversation |

## Session Flow

```
1. User provides prompt
2. [thread_id?] → Load context | Create new thread
3. Send to model with conversation history
4. Receive response
5. Persist to thread
6. (GATE: continuation) → "Continue conversation?" | Exit
```

## Continuation Gate

After each response, prompt user:

```
AskUserQuestion:
"Response received. What next?"
Options:
- "Follow up" - continue this thread
- "New topic" - start fresh thread
- "Done" - exit workflow
```

## Response Format

```json
{
  "response": "Model's response text",
  "thread_id": "thread-abc123",
  "model": "claude-sonnet",
  "turn_count": 3
}
```

## Thread Context

Each thread maintains:
- Full conversation history
- Model used (consistent within thread)
- Creation timestamp
- Last activity timestamp
