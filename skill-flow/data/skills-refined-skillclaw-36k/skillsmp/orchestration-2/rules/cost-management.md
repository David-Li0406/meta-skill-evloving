---
title: Cost Management
impact: MEDIUM
tags: orchestration, tokens, cost
---

# Token-Efficient Orchestration (Cost Management)

```
SUBSCRIPTION BURNS FAST. ROUTE MODELS WISELY.

Opus = 5x cost of Haiku
Sonnet = 3x cost of Haiku
One bad habit = subscription gone in days
```

## Model Cost Tiers (2025-2026 Pricing)

| Model | Input/1M | Output/1M | Relative Cost | Best For |
|-------|----------|-----------|---------------|----------|
| **Haiku 4.5** | $1 | $5 | 1x (baseline) | Exploration, simple tasks |
| **Sonnet 4.5** | $3 | $15 | ~3x | Complex thinking, analysis |
| **Opus 4.5** | $5 | $25 | ~5x | All coding work |

## Model Routing Strategy

**ROUTE BY TASK TYPE, NOT COMPLEXITY**

### OPUS 4.5 (model: "opus") -- ALL CODING & EDITING
- ANY code writing or editing task
- Feature implementation (simple or complex)
- Bug fixes and debugging
- Refactoring
- Writing tests
- Any task that touches code files

### SONNET 4.5 (model: "sonnet") -- COMPLEX THINKING
- Architecture planning and design
- Deep research and analysis
- Complex reasoning tasks
- Code review (read-only analysis)
- Documentation requiring deep understanding
- Strategic decision-making

### HAIKU 4.5 (model: "haiku") -- EVERYTHING ELSE
- File exploration and search
- Simple lookups and validations
- Classification and categorization
- Session saving and memory tasks
- Quick summaries
- Any non-complex, non-coding task

## Agent Model Selection

```python
# ALL coding and editing goes to Opus
Task(
    subagent_type="general-purpose",
    model="opus",  # For ANY code work
    description="Implement auth routes",
    prompt="...",
    run_in_background=True
)

# Complex thinking/reasoning (non-coding) goes to Sonnet
Task(
    subagent_type="general-purpose",
    model="sonnet",  # For complex analysis
    description="Design system architecture",
    prompt="...",
    run_in_background=True
)

# Everything else goes to Haiku
Task(
    subagent_type="Explore",
    model="haiku",  # For simple/non-coding tasks
    description="Find auth files",
    prompt="...",
    run_in_background=True
)
```

---

# Economy Mode

Toggle between efficiency modes based on subscription pressure.

## ECONOMY MODE
**Activate when:** subscription running low, long sessions

- Haiku for ALL exploration
- Sonnet for ALL implementation (avoid Opus)
- Max 2 agents per wave (not 3-4)
- Lean preambles ONLY
- Aggressive output limits (30 lines max)
- Compact after every 2 agent outputs

## NORMAL MODE (default)
**Use when:** subscription healthy, complex projects

- Haiku for exploration
- Sonnet for standard work
- Opus for complex coding
- 3-4 agents per wave
- Full preambles when helpful
- Standard output limits (50-100 lines)
- Compact after every 3-4 outputs

## Activating Economy Mode

**User says:** "enable economy mode" / "save tokens" / "subscription running low"

**You do:**
1. Acknowledge: "Switching to economy mode -- will be more token-conscious."
2. Apply economy routing rules
3. Update signature: `--- @ Clorching [ECONOMY] --`

**User says:** "normal mode" / "disable economy mode" / "full power"

**You do:**
1. Acknowledge: "Back to normal mode."
2. Resume standard routing
3. Standard signature: `--- @ Clorching --`

## Session Token Budget

| Session Type | Agents | Estimated Cost |
|--------------|--------|----------------|
| Light (5 agents) | ~$0.05-0.20 |
| Medium (15 agents) | ~$0.20-0.80 |
| Heavy (30+ agents) | ~$0.50-2.00 |

## Token Budget Awareness

- **At session start:** Track agent count mentally
- **After 10 agents:** Consider if task requires more spawns
- **After 20 agents:** Prompt for economy mode or compact
- **After 30 agents:** Warn user about heavy session

## Cost-Efficient Patterns

**DO:**
- One haiku Explore -> then targeted sonnet workers
- Batch related tasks into single agent
- Use lean preambles after first wave
- Compact between waves to reset context

**DON'T:**
- Opus for exploration (use haiku)
- Separate agents for tiny related tasks
- Full preambles every time
- 5+ agents without compacting
- Verbose output requests
