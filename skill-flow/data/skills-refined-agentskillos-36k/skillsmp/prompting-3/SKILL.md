---
name: prompting
description: GPT-5 prompting best practices for creating AI agent prompts in OpenPromo codebase when using ai sdk or agents, or in general writing llm prompts.
---

# GPT-5 Prompting Guide

Best practices for creating prompts for AI agents in OpenPromo, based on OpenAI's GPT-5 prompting guide. Thi

## Core Principles

1. **Instruction Clarity** - GPT-5 requires precise, non-contradictory instructions. Poorly-constructed prompts with vague or conflicting rules are more damaging to GPT-5 than other models.

2. **Structured XML Organization** - Use XML tags to organize instructions. This structure improves adherence to complex directives.

3. **Explicit Over Implicit** - State requirements directly rather than implying them.

## Standard Prompt Structure

Use this XML-based structure for all agent prompts as baseline. extend to include other sections where applies case-by-case.

```
<Role>
Define who the agent is and their expertise. Be specific about domain knowledge.
</Role>

<Task>
Clearly state what the agent should do. Break into numbered steps if complex.
</Task>

<Context>
Provide relevant context: platform, channel, user info, etc.
Dynamic values go here.
</Context>

<Rules>
1. Numbered rules for behavior constraints.
2. Include thresholds and confidence requirements inline.
3. State what NOT to do explicitly.
4. Resolve potential contradictions by priority.
</Rules>
```

### Context Injection Pattern

For multi-part prompts with dynamic context:

```typescript
function createRunInputs(ctx: Context): AgentInputItem[] {
  const base = createBaseInputs(ctx.businessContext);

  return [
    ...base,
    {
      role: "system",
      content: `
<Task>
Specific task for this run.
</Task>

<Context>
Platform: ${ctx.platform}
Channel: ${ctx.channel}
</Context>

<Data>
${formatData(ctx.data)}
</Data>

Generate [output] based on the above context.
`.trim(),
    },
  ];
}
```

## Best Practices

### DO

- **Separate concerns with XML tags** - Role, Task, Context, Rules, Data, etc.
- **Number rules** - Makes them easier to reference and prioritize
- **State defaults explicitly** - "General messages should return empty labels array"
- **Use `.trim()`** - Clean whitespace from template literals

### DON'T

- **Don't use contradictory instructions** - Wastes reasoning tokens resolving conflicts
- **Don't be vague** - "Be helpful" is worse than "Answer the customer's question with specific product details"
- **Don't over-engineer eagerness** - GPT-5 is naturally proactive at context gathering
- **Don't mix categories** - Keep intent vs sentiment, classification vs generation separate
- **Don't rely on post-processing** - Push logic into the prompt where possible

## Model-Specific Settings

### For GPT-5-nano (fast classification)

```typescript
const { output } = await generateText({
  model: openai("gpt-5-nano"),
  output: Output.object({ schema }),
  temperature: 0,        // Deterministic for classification
  maxOutputTokens: 500,  // Keep small for fast response
  messages: [...],
});
```

### For GPT-5 (complex reasoning)

```typescript
const output = await run(agent, inputItems);
// Use Agent SDK for multi-step reasoning
// Higher token limits, tools enabled
```

## References

- [OpenAI GPT-5 Prompting Guide](https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/gpt-5_prompting_guide.ipynb)
