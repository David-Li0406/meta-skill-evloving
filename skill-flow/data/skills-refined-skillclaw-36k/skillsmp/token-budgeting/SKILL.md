---
name: token-budgeting
description: Best practices for managing token usage and budgets
tags: [tokens, cost, budgeting, llm]
---

# Token Budgeting Skill

Use this skill to manage and optimize LLM token usage.

## Commands

- `/token-summary` - Get daily token usage summary
- `/token-budget` - Check budget status

## Best Practices

1. **Monitor daily usage**: Check summary regularly to track costs
2. **Set budgets**: Configure limits to prevent unexpected costs
3. **Optimize prompts**: Shorter prompts = fewer tokens = lower cost
4. **Cache responses**: Avoid repeated identical queries

## Cost Estimation

Approximate costs per 1K tokens (varies by model):

- GPT-4o: ~$0.03 input, ~$0.06 output
- GPT-4o-mini: ~$0.0015 input, ~$0.006 output
- Claude 3.5: ~$0.003 input, ~$0.015 output
