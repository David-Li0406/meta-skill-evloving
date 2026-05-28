# ReAct (Reason + Act)

Combine reasoning with tool use. For tasks requiring external actions.

## Template

```markdown
Available tools:
- search(query): Find information
- read_file(path): Read file contents
- calculate(expression): Perform calculation
- finish(answer): Provide final answer

Format:
Thought: [What to do next and why]
Action: tool_name[input]
Observation: [Result - provided by system]

Repeat until ready, then:
Thought: I have enough information
Action: finish[final answer]
```

## Example

```markdown
Task: Find the total revenue from Q3 2024 and compare to Q2.

Available tools:
- read_file(path): Read file contents
- calculate(expression): Math operations
- finish(answer): Final answer

---

Thought: I need to find Q3 revenue data. Should check financial reports.
Action: read_file[/reports/q3-2024-financials.md]
Observation: Q3 2024 Revenue: $2.4M. Expenses: $1.8M. Net: $600K.

Thought: Now I need Q2 data for comparison.
Action: read_file[/reports/q2-2024-financials.md]
Observation: Q2 2024 Revenue: $2.1M. Expenses: $1.6M. Net: $500K.

Thought: I have both figures. Need to calculate the difference and percentage.
Action: calculate[(2.4 - 2.1) / 2.1 * 100]
Observation: 14.29

Thought: I have all the information needed.
Action: finish[Q3 2024 revenue was $2.4M, up 14.3% from Q2's $2.1M. Net income also increased from $500K to $600K (20% growth).]
```

## When to Use

- Research tasks
- Data gathering from multiple sources
- Tasks requiring verification
- Multi-step investigations
- Any task needing external tool calls

## When NOT to Use

- Pure reasoning tasks (use CoT)
- No tools available
- Simple direct questions
