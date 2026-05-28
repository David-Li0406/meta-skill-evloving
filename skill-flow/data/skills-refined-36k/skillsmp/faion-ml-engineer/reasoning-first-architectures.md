---
id: reasoning-first-architectures
name: "Reasoning-First Architectures"
domain: ML
skill: faion-ml-engineer
category: "best-practices-2026"
---

## Reasoning-First Architectures

### Problem

Agents act before thinking, leading to suboptimal outcomes.

### Solution: Think-Before-Act Patterns

**Core Reasoning Patterns:**

| Pattern | Description |
|---------|-------------|
| ReAct | Interleaved reasoning and acting |
| Reflexion | Self-evaluation and improvement |
| Tree-of-Thought | Explore multiple reasoning paths |
| Planning Loops | Plan -> Execute -> Verify -> Adjust |
| Critique & Revise | Generate -> Critique -> Improve |

**ReAct Implementation:**
```
Thought: I need to find the company's Q4 revenue
Action: search("Company X Q4 2025 revenue report")
Observation: [search results]
Thought: Found $4.2B revenue, but need YoY comparison
Action: search("Company X Q4 2024 revenue")
Observation: [search results showing $3.8B]
Thought: Can now calculate growth rate
Answer: Q4 2025 revenue was $4.2B, representing 10.5% YoY growth
```

**Tree-of-Thought:**
```
Query
    - Path A: Direct approach
        - Evaluate: Score 0.6
        - Continue or prune
    - Path B: Step-by-step
        - Evaluate: Score 0.8
        - Expand further
    - Path C: Tool-assisted
        - Evaluate: Score 0.9
        - Select as best path
```

**Reflexion Loop:**
```
Generate response
    |
Self-evaluate quality
    |
Identify weaknesses
    |
Generate improved response
    |
Repeat until satisfactory
```
