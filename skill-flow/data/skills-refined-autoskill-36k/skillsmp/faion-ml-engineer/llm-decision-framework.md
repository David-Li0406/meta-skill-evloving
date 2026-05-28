# LLM Decision Framework

## Problem

When to use prompting vs RAG vs fine-tuning?

## Solution: Progressive Enhancement

```
Start: Prompt Engineering (hours/days, $0)
         |
Need external data? -> RAG ($70-1000/month)
         |
Need specialized behavior? -> Fine-tuning (months, 6x inference cost)
```

**Decision Matrix:**

| Need | Solution |
|------|----------|
| Better instructions | Prompt engineering |
| Real-time/private data | RAG |
| Specific output format | Structured output |
| Domain expertise | Fine-tuning |
| Cost reduction | Smaller model + fine-tuning |

**Cost Comparison:**

| Approach | Setup Cost | Ongoing Cost | Time to Deploy |
|----------|------------|--------------|----------------|
| Prompting | Low | Per-token | Hours |
| RAG | Medium | Infrastructure + tokens | Days-weeks |
| Fine-tuning | High | Higher per-token | Weeks-months |

---

*AI/ML Best Practices 2026*
