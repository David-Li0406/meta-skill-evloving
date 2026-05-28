---
name: dspy-advanced
description: Advanced DSPy modules including ReAct agents, tool calling, output refinement (BestOfN, Refine), and adapters. Use when building agent systems, integrating external tools, or implementing multi-step reasoning.
---

# DSPy Advanced

Advanced DSPy modules for agents, tools, and output refinement.

## Quick Start

### ReAct Agent with Tools
```python
import dspy

# Define tools
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny."

def search_web(query: str) -> str:
    return f"Search results for '{query}'"

# Create ReAct agent
react = dspy.ReAct(
    signature="question -> answer",
    tools=[get_weather, search_web],
    max_iters=5
)

# Use agent
result = react(question="What's the weather in Tokyo?")
print(result.answer)
print("Tool calls:", result.trajectory)
```

### BestOfN for Multiple Attempts
```python
def one_word_answer(args, pred: dspy.Prediction) -> float:
    return 1.0 if len(pred.answer.split()) == 1 else 0.0

best_of_3 = dspy.BestOfN(
    module=dspy.ChainOfThought("question -> answer"),
    N=3,
    reward_fn=one_word_answer,
    threshold=1.0
)

result = best_of_3(question="What is the capital of Belgium?")
print(result.answer)  # Brussels
```

### Refine for Iterative Improvement
```python
refine = dspy.Refine(
    module=dspy.ChainOfThought("question -> answer"),
    N=3,
    reward_fn=one_word_answer,
    threshold=1.0
)

result = refine(question="What is the capital of Belgium?")
print(result.answer)  # Brussels
```

## When to Use This Skill

Use this skill when:
- Building ReAct agents with tool calling
- Implementing output refinement strategies
- Integrating external tools and APIs
- Using custom adapters for LM integration
- Implementing multi-step reasoning with feedback loops

## Core Concepts

### ReAct Agents
ReAct combines reasoning and action, enabling agents to use tools to answer questions.

**Key features:**
- Automatic reasoning before tool calls
- Tool trajectory tracking
- Multi-iteration tool usage
- Dynamic tool selection

**See:** [references/react-tools.md](references/react-tools.md) for:
- ReAct agent patterns
- Tool definition best practices
- Multi-tool coordination

### Output Refinement
Improve output quality through multiple attempts or iterative refinement.

**Strategies:**
- **BestOfN**: Generate N candidates and select best
- **Refine**: Iteratively improve with feedback loop

**See:** [references/output-refinement.md](references/output-refinement.md) for:
- BestOfN vs Refine comparison
- Reward function patterns
- Use cases and examples

### Adapters
Adapters bridge DSPy modules with Language Models, handling prompt formatting and output parsing.

**Adapter types:**
- **ChatAdapter**: For chat-based LMs
- **JSONAdapter**: For structured output
- **Custom adapters**: For specialized use cases

**See:** [references/adapters.md](references/adapters.md) for:
- Adapter architecture
- Custom adapter implementation
- Multi-provider configuration

## Progressive Disclosure

This skill uses progressive disclosure:

1. **SKILL.md** (this file): Quick reference and navigation
2. **references/**: Detailed technical docs loaded as needed

Load reference files only when you need detailed information on a specific topic.

## Related Skills

- **dspy-basics**: Signature design, basic modules, program composition
- **dspy-optimization**: Teleprompters, metrics, optimization workflows
- **dspy-configuration**: LM setup, caching, and version management
