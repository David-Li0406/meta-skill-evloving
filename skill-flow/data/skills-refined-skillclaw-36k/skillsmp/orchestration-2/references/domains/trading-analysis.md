# Trading Analysis Orchestration Patterns

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   Markets move fast. Your analysis should move faster.      │
│   Three specialists, one unified view, actionable insight.  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

> **Load when**: Chart analysis, price predictions, trade setups, technical analysis, support/resistance identification, pattern recognition
> **Common patterns**: Full Chart Analysis, Quick Level Check, Trade Setup Generation

---

## Workspace Agents

This workspace has three specialized trading agents at `.claude/agents/`:

| Agent | File | Purpose |
|-------|------|---------|
| **technical-analyst** | `technical-analyst.md` | Support/resistance levels, trend direction, market structure |
| **pattern-recognition** | `pattern-recognition.md` | Chart patterns, Fibonacci levels, volume analysis, pullback health |
| **trade-strategist** | `trade-strategist.md` | Trade scenarios, entry/exit levels, risk management, probability assessment |

### How to Invoke These Agents

Since workspace agents are prompt templates (not native subagent_types), spawn them via `general-purpose` with their prompt embedded:

```python
Task(
    subagent_type="general-purpose",
    description="Technical analysis",
    prompt="""CONTEXT: You are a WORKER agent acting as a technical-analyst.

ROLE: You are a technical analysis specialist focused on identifying key price levels and market structure.

[Include full agent prompt from .claude/agents/technical-analyst.md]

TASK:
[Specific analysis request]
""",
    run_in_background=True
)
```

---

## Full Chart Analysis

### Pattern: Comprehensive Market Analysis

```
User Request: "Analyze this chart" / shares chart image

Phase 1: FAN-OUT (Parallel specialist analysis)
├─ Agent A (technical-analyst): Support/resistance levels, trend assessment
├─ Agent B (pattern-recognition): Chart patterns, Fibonacci, volume
└─ Agent C (trade-strategist): Scenarios, targets, risk management

Phase 2: REDUCE
└─ Orchestrator: Synthesize into unified analysis with:
   • Key levels table
   • Current bias
   • Trade setup (if applicable)
   • Risk warnings
```

### Example Prompt for Full Analysis

```python
# Agent 1: Technical Analyst
Task(
    subagent_type="general-purpose",
    description="Technical analysis",
    prompt="""CONTEXT: You are a WORKER agent acting as a technical-analyst.

ROLE: Identify key support/resistance levels, assess trend direction, and analyze market structure.

OUTPUT:
1. Support levels table (price, significance, rationale)
2. Resistance levels table
3. Trend assessment (bullish/bearish/sideways + evidence)
4. Invalidation levels

CHART DATA:
[Insert chart description or extracted data]
""",
    run_in_background=True
)

# Agent 2: Pattern Recognition
Task(
    subagent_type="general-purpose",
    description="Pattern recognition",
    prompt="""CONTEXT: You are a WORKER agent acting as a pattern-recognition specialist.

ROLE: Identify chart patterns, calculate Fibonacci levels, assess pullback health, analyze volume.

OUTPUT:
1. Identified patterns with confidence levels
2. Fibonacci retracement table (from swing low to high)
3. Pullback health verdict
4. Volume interpretation

CHART DATA:
[Insert chart description or extracted data]
""",
    run_in_background=True
)

# Agent 3: Trade Strategist
Task(
    subagent_type="general-purpose",
    description="Trade strategy",
    prompt="""CONTEXT: You are a WORKER agent acting as a trade-strategist.

ROLE: Develop bullish and bearish scenarios with probability, entry zones, targets, and risk management.

OUTPUT:
1. Bullish scenario (conditions, entry, targets, probability)
2. Bearish scenario (conditions, entry, targets, probability)
3. Key confirmation levels
4. Risk management (stops, position size, R:R)
5. Mandatory disclaimer

CHART DATA:
[Insert chart description or extracted data]
""",
    run_in_background=True
)
```

---

## Quick Level Check

### Pattern: Support/Resistance Only

```
User Request: "What are the key levels?" / "Find support"

Phase 1: SINGLE AGENT
└─ Agent (technical-analyst): Support/resistance levels only

Phase 2: DELIVER
└─ Orchestrator: Present clean level tables
```

---

## Pattern Identification

### Pattern: Chart Pattern Focus

```
User Request: "What patterns do you see?" / "Is this a bull flag?"

Phase 1: SINGLE AGENT
└─ Agent (pattern-recognition): Pattern identification + Fibonacci

Phase 2: DELIVER
└─ Orchestrator: Pattern verdict with confidence and invalidation
```

---

## Trade Setup Generation

### Pattern: Actionable Trade Ideas

```
User Request: "Give me a trade setup" / "How should I trade this?"

Phase 1: PREREQUISITE
└─ Explore agent: Read existing analysis if available

Phase 2: FAN-OUT
├─ Agent (technical-analyst): Key levels for entry/stop placement
└─ Agent (trade-strategist): Full scenario analysis

Phase 3: REDUCE
└─ Orchestrator: Clear trade setup with:
   • Direction bias
   • Entry zone
   • Stop loss
   • Targets (T1, T2, T3)
   • R:R ratio
   • Position size suggestion
```

---

## Multi-Timeframe Analysis

### Pattern: Timeframe Confluence

```
User Request: "Analyze on multiple timeframes"

Phase 1: FAN-OUT (Parallel timeframe analysis)
├─ Agent A: Higher timeframe (daily/4H) trend context
├─ Agent B: Trading timeframe analysis
└─ Agent C: Lower timeframe entry refinement

Phase 2: REDUCE
└─ Orchestrator: Confluence report showing alignment/divergence
```

---

## Real-Time Update

### Pattern: Price Level Alert

```
User Request: "Price just hit X level" / "What now?"

Phase 1: QUICK ASSESSMENT
└─ Agent (trade-strategist): React to level with updated scenarios

Phase 2: DELIVER
└─ Orchestrator: Updated bias and next key level to watch
```

---

## Synthesis Templates

### Full Analysis Output Structure

```markdown
## [Asset] Analysis

### Key Levels
| Type | Level | Significance |
|------|-------|--------------|
| Resistance | $X | ... |
| Support | $Y | ... |

### Current Bias: [BULLISH/BEARISH/NEUTRAL]
[One-line reasoning]

### Pattern: [Pattern name] ([confidence]%)
[Brief description]

### Trade Setup
| Parameter | Value |
|-----------|-------|
| Bias | Long/Short |
| Entry | $X - $Y |
| Stop | $Z |
| Target 1 | $T1 |
| Target 2 | $T2 |
| R:R | X:1 |

### Risk Notes
- [Key risk factors]

---
*Disclaimer: Educational purposes only. Not financial advice.*
```

---

## Task Routing Decision Tree

```
User mentions chart/price/trading?
│
├─ "analyze" / "what do you see" / shares image
│  └─ FULL ANALYSIS (3 agents parallel)
│
├─ "support" / "resistance" / "levels"
│  └─ TECHNICAL ANALYST only
│
├─ "pattern" / "flag" / "triangle" / "fib"
│  └─ PATTERN RECOGNITION only
│
├─ "trade" / "setup" / "entry" / "target"
│  └─ TRADE STRATEGIST (+ technical for levels)
│
├─ "prediction" / "where is it going"
│  └─ FULL ANALYSIS (all 3 for comprehensive view)
│
└─ unclear
   └─ AskUserQuestion: What aspect interests you?
```

---

## Best Practices

1. **Always spawn in parallel** — Technical, pattern, and strategy analysis are independent
2. **Extract chart data first** — If user shares image, describe price action before spawning
3. **Include timeframe context** — Always note the timeframe being analyzed
4. **Mandatory disclaimers** — Every prediction must include risk warning
5. **Be specific with levels** — Round numbers, no vague ranges
6. **State invalidation** — Every bias needs a "wrong if..." level

---

## Anti-Patterns

| Don't | Do |
|-------|-----|
| Analyze without price data | Extract/describe chart first |
| Give targets without stops | Always pair with risk management |
| Single agent for full analysis | Parallel specialist swarm |
| Vague levels ("around $90K") | Specific levels ($90,000, $89,500) |
| Skip disclaimer | Always include risk warning |

---

```
─── ◈ Trading Analysis ─────────────────────
```
