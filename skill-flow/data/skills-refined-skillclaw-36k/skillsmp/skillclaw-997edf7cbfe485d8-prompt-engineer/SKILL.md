---
name: prompt-engineer
description: Use this skill to optimize prompts for LLMs and AI systems, enhancing agent performance and crafting effective system prompts.
---

# Skill Body

## When to Use
- Creating system prompts
- Improving AI output quality
- Building AI agents
- Optimizing token usage
- Designing prompt templates

## Core Techniques

### Role Setting
```
You are an expert [role] with [X] years of experience in [domain].
Your task is to [specific goal].
```

### Chain of Thought
```
Think through this step by step:
1. First, analyze [aspect 1]
2. Then, consider [aspect 2]
3. Finally, determine [conclusion]

Show your reasoning before giving the final answer.
```

### Few-Shot Examples
```
Here are examples of the expected format:

Input: [example 1 input]
Output: [example 1 output]

Input: [example 2 input]
Output: [example 2 output]

Now process this input:
Input: {user_input}
Output:
```

### Structured Output
```
Respond in the following JSON format:
{
  "analysis": "your analysis here",
  "confidence": 0.0-1.0,
  "recommendations": ["item1", "item2"]
}

Return valid JSON only, no additional text.
```

## Prompt Structure

### System Prompt Components
1. **Role**: Who the AI is
2. **Context**: Background information
3. **Task**: What to do
4. **Constraints**: Limitations and rules
5. **Output format**: Expected structure

### Effective Patterns
```
[Role and expertise]

[Context and background]

[Specific task instructions]

[Output format requirements]

[Examples if needed]

[Edge case handling]
```

## Optimization Strategies
- **Clarity**: Use precise language and avoid ambiguity.
- **Specificity**: Provide explicit instructions and concrete examples.
- **Structure**: Ensure logical flow and consistent formatting.

## Common Issues and Solutions
| Issue            | Solution                                   |
|------------------|--------------------------------------------|
| Hallucinations    | Add "If unsure, say so"                   |
| Wrong format      | Provide explicit schema                     |
| Off-topic         | Add "Stay focused on X"                   |
| Too verbose       | Request concise responses                   |
| Missing context   | Add relevant background                     |

## Testing Prompts
1. Test with edge cases.
2. Measure consistency.
3. Check output format.
4. Validate accuracy.
5. Monitor in production.

## Production Considerations
- Version control prompts.
- A/B test changes.
- Log inputs/outputs.
- Monitor quality metrics.
- Handle failures gracefully.