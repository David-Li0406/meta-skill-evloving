---
id: ai-agent-patterns
name: "AI Agent Patterns"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

## AI Agent Patterns

### Problem

Simple prompt->response insufficient for complex tasks.

### Solution: Agent Design Patterns

**1. Chain of Thought (CoT)**
```
Prompt: "Let's think step by step..."
Output: Reasoning -> Intermediate steps -> Final answer
```

**2. ReAct (Reason + Act)**
```
Thought: What do I need to find out?
Action: search(query)
Observation: [search results]
Thought: Now I know X, but need Y
Action: lookup(Y)
...
Answer: [final response]
```

**3. Plan-and-Execute**
```
1. Create plan with subtasks
2. Execute each subtask
3. Verify results
4. Adjust plan if needed
5. Synthesize final output
```

**4. Tool Use Pattern**
```python
tools = [
    {"name": "search", "description": "Search the web"},
    {"name": "calculate", "description": "Math operations"},
    {"name": "code_exec", "description": "Run Python code"}
]

# Agent decides which tool to use based on task
```

**Frameworks:**
| Framework | Strengths |
|-----------|-----------|
| LangGraph | State machines, complex flows |
| AutoGen | Multi-agent conversations |
| CrewAI | Role-based agent teams |
| OpenAI Agents SDK | Official OpenAI support |
