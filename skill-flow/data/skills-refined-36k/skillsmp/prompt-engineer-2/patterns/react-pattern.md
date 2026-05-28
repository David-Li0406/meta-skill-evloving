# ReAct Pattern (Reasoning + Acting)

## Overview

Alternates between reasoning (thinking about what to do) and acting (using tools) with observations feeding back into the loop.

**When to Use:**
- Tasks requiring information gathering
- Tool/API usage
- Multi-step problem solving
- Verification loops
- Interactive exploration

**Community Validation:**
- Original paper (Yao et al.): 1,200+ citations
- LangChain implementation: 90,000+ stars
- 60% of production agent deployments (CrewAI survey)
- 30-40% improvement over pure reasoning

---

## Architecture

```
Thought → Action → Observation → Thought → Action → Observation → ... → Answer
```

---

## Basic ReAct Template

```xml
<role>
You solve tasks by thinking step-by-step and using tools when needed.
</role>

<available_tools>
{{TOOL_DESCRIPTIONS}}
</available_tools>

<instructions>
1. Think through what you need to do
2. If you need information or to perform an action, use a tool
3. Observe the result
4. Continue reasoning based on observations
5. Repeat until you can provide the final answer
</instructions>

<format>
For each step, respond with:

<thinking>
Your reasoning about what to do next
</thinking>

<action>
<tool>tool_name</tool>
<parameters>
<param_name>value</param_name>
</parameters>
</action>

After receiving observation:
<observation>
Tool result appears here
</observation>

When you have the answer:
<final_answer>
Your complete response
</final_answer>
</format>

<task>
{{TASK}}
</task>
```

---

## Claude-Optimized ReAct

```xml
<role>
You are an agent that solves tasks by alternating between reasoning and acting.
You have access to tools and must use them to gather information or perform actions.
</role>

<available_tools>
<tool name="search">
<description>Search for information</description>
<parameters>
<query>Search query string</query>
</parameters>
</tool>

<tool name="calculate">
<description>Perform mathematical calculations</description>
<parameters>
<expression>Mathematical expression</expression>
</parameters>
</tool>

<tool name="lookup">
<description>Look up data in database</description>
<parameters>
<id>Record identifier</id>
</parameters>
</tool>
</available_tools>

<instructions>
Follow this exact pattern:

1. **Think**: Analyze what you know and what you need
2. **Act**: If you need more info or must take action, use a tool
3. **Observe**: Process the tool's response
4. **Repeat**: Continue thinking and acting until solved
5. **Answer**: When you have enough info, provide final answer

IMPORTANT:
- Always think before acting
- Only use one tool per action
- Wait for observation before next thought
- State your reasoning explicitly
</instructions>

<format>
<step number="1">
<thought>
I need to find X because...
The best tool for this is Y because...
</thought>
<action>
<tool>tool_name</tool>
<parameters>
<param>value</param>
</parameters>
</action>
</step>

<!-- System will inject observation here -->

<step number="2">
<thought>
Based on the observation, I now know...
Next I need to...
</thought>
...
</step>

<!-- Continue until solved -->

<final_answer>
Complete response based on gathered information
</final_answer>
</format>

<task>
{{TASK}}
</task>

Begin with your first thought:
```

---

## Tool Definition Format

```xml
<tool name="{{TOOL_NAME}}">
<description>{{WHAT_IT_DOES}}</description>
<parameters>
<{{PARAM_1}}>{{PARAM_1_DESC}}</{{PARAM_1}}>
<{{PARAM_2}}>{{PARAM_2_DESC}}</{{PARAM_2}}>
</parameters>
<example>
<input>
<{{PARAM_1}}>example value</{{PARAM_1}}>
</input>
<output>
Example output
</output>
</example>
</tool>
```

---

## Implementation Patterns

### Sequential ReAct (Default)

```
Think → Act → Wait for Observation → Think → Act → ...
```

### Parallel ReAct

```
Think → Multiple Actions → Collect Observations → Synthesize → ...
```

### ReAct with Fallback

```
Think → Act → Observation Failed? → Fallback Strategy → Continue
```

---

## Best Practices

1. **Explicit tool descriptions**: Clear what each tool does and returns
2. **Parameter validation**: Specify required vs optional params
3. **Error handling**: Define what happens when tools fail
4. **Observation processing**: Model must interpret, not just receive
5. **Termination criteria**: Clear when to stop and answer
6. **Step limits**: Cap iterations to prevent infinite loops

---

## Common Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Loops forever | No termination criteria | Add "when to answer" instruction |
| Ignores observations | Poor format | Make observations clearly labeled |
| Wrong tool choice | Vague descriptions | Add use cases to tool descriptions |
| Skips thinking | Format not enforced | Require <thinking> before <action> |

---

## JSON Variant (for parsing)

```json
{
  "thought": "I need to search for X because...",
  "action": "search",
  "action_input": {
    "query": "search terms"
  }
}

// After observation
{
  "thought": "Based on the results, I now know...",
  "final_answer": "The answer is..."
}
```

---

## When NOT to Use

- Simple tasks not requiring tools
- When all info is in context already
- Latency-critical applications
- Tasks with predictable, fixed steps (use direct prompts)

---

## Version

**Version**: 1.0.0
**Source**: Yao et al. ReAct paper, LangChain implementation
