---
title: Set max_turns to Prevent Infinite Loops
impact: HIGH
impactDescription: Prevents runaway agent execution
tags: runner, max-turns, safety, limits
---

## Set max_turns to Prevent Infinite Loops

**Impact: HIGH (prevents runaway agent execution)**

Always set `max_turns` to prevent agents from running indefinitely due to tool loops or handoff cycles.

**Incorrect (no limit - potential infinite loop):**

```python
from agents import Agent, Runner

agent = Agent(
    name="Research Agent",
    instructions="Keep researching until you find the answer",
    tools=[web_search, analyze_data],
)

# Could run forever if agent keeps calling tools
result = await Runner.run(agent, "Research everything about AI")
```

**Correct (with max_turns):**

```python
from agents import Agent, Runner
from agents.exceptions import MaxTurnsExceeded

agent = Agent(
    name="Research Agent", 
    instructions="Research the topic. Complete within a few steps.",
    tools=[web_search, analyze_data],
)

try:
    result = await Runner.run(
        agent, 
        "Research AI trends",
        max_turns=10,  # Limit total iterations
    )
    print(result.final_output)
except MaxTurnsExceeded:
    print("Agent took too long - consider simplifying the task")
```

**What counts as a turn:**

Each iteration of the agent loop counts as a turn:
1. LLM call produces output
2. If tool calls → run tools, increment turn, loop back
3. If handoff → switch agent, increment turn, loop back
4. If final output → done

**Recommended limits:**

| Use case | Suggested max_turns |
|----------|---------------------|
| Simple Q&A | 3-5 |
| Tool-using agent | 5-15 |
| Complex multi-agent | 10-30 |
| Research/analysis | 15-50 |

**Handle the exception:**

```python
from agents.exceptions import MaxTurnsExceeded

try:
    result = await Runner.run(agent, input, max_turns=10)
except MaxTurnsExceeded as e:
    # Access partial results
    print(f"Stopped after {e.last_result.new_items} items")
    # Optionally continue with a different approach
```

Reference: [Running Agents Documentation - The Agent Loop](https://openai.github.io/openai-agents-python/running_agents/#the-agent-loop)
