---
name: mcp-progress-reporting
description: "MCP progress updates for long operations. Use when asking 'MCP progress', 'progress reporting', 'long operation', 'progress updates', or 'mcp streaming'."
---

# MCP Progress Reporting

Report progress for long-running MCP operations.

> **Skill Metadata**
> Category: `mcp`
> Priority: `LOW`
> SDK Version: `0.9.25+`
> Related Skills: [`mcp-resources`](mcp-resources.md), [`mcp-integration-guide`](../../01-core-sdk/mcp-integration-guide.md)
> Related Subagents: `mcp-specialist` (streaming patterns)

## Quick Reference

- **Progress**: Real-time updates during tool execution
- **Use Cases**: File uploads, data processing, long queries
- **WebSocket**: Best transport for progress streaming

## Basic Progress Reporting

```python
from kailash.workflow.builder import WorkflowBuilder

workflow = WorkflowBuilder()

workflow.add_node("IterativeLLMAgentNode", "agent", {
    "provider": "openai",
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Process large dataset"}],
    "mcp_servers": [{
        "name": "processor",
        "transport": "websocket",
        "url": "wss://api.company.com/mcp",
        "tools": [
            {
                "name": "process_data",
                "progress_reporting": True,  # Enable progress
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "dataset_url": {"type": "string"}
                    }
                }
            }
        ]
    }]
})
```

## Related Patterns

- **Resources**: [`mcp-resources`](mcp-resources.md)
- **MCP Integration**: [`mcp-integration-guide`](../../01-core-sdk/mcp-integration-guide.md)

<!-- Trigger Keywords: MCP progress, progress reporting, long operation, progress updates, mcp streaming -->
