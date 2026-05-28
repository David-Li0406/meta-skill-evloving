---
name: autonomous-agent-patterns
description: Use this skill when building autonomous AI agents, designing tool APIs, implementing permission systems, or creating browser automation workflows.
---

# Skill body

## When to Use This Skill

Use this skill when:

- Building autonomous AI agents
- Designing tool/function calling APIs
- Implementing permission and approval systems
- Creating browser automation for agents
- Designing human-in-the-loop workflows

## 1. Core Agent Architecture

### 1.1 Agent Loop

```
┌─────────────────────────────────────────────────────────────┐
│                     AGENT LOOP                               │
│                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │  Think   │───▶│  Decide  │───▶│   Act    │              │
│  │ (Reason) │    │ (Plan)   │    │ (Execute)│              │
│  └──────────┘    └──────────┘    └──────────┘              │
│       ▲                               │                     │
│       │         ┌──────────┐          │                     │
│       └─────────│ Observe  │◀─────────┘                     │
│                 │ (Result) │                                │
│                 └──────────┘                                │
└─────────────────────────────────────────────────────────────┘
```

```python
class AgentLoop:
    def __init__(self, llm, tools, max_iterations=50):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
        self.max_iterations = max_iterations
        self.history = []

    def run(self, task: str) -> str:
        self.history.append({"role": "user", "content": task})

        for i in range(self.max_iterations):
            # Think: Get LLM response with tool options
            response = self.llm.chat(
                messages=self.history,
                tools=self._format_tools(),
                tool_choice="auto"
            )

            # Decide: Check if agent wants to use a tool
            if response.tool_calls:
                for tool_call in response.tool_calls:
                    # Act: Execute the tool
                    result = self._execute_tool(tool_call)
                    self.history.append({"role": "assistant", "content": result})
        
        return self.history[-1]["content"]

    def _format_tools(self):
        # Format tools for the LLM
        return [{"name": name, "description": tool.description} for name, tool in self.tools.items()]

    def _execute_tool(self, tool_call):
        # Execute the tool and return the result
        tool = self.tools[tool_call.name]
        return tool.execute(tool_call.args)
```