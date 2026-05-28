---
name: edge-plan
description: Create or update a structured plan in active_context.yaml. Use when starting work on a new objective or refining an existing plan.
---

# Create/Update Plan

Read the current state and help create or refine a plan.

## Current State

First, read `active_context.yaml` in the project root.

## Instructions

### 0. Check for Research Needs First

Before creating a plan, scan the objective for research needs:

**Check for these signals:**
- Complex technologies mentioned (kubernetes, websocket, CRDT, etc.)
- Ambiguity signals ("best way", "should I", "optimize", "compare")
- Explicit research verbs ("evaluate", "investigate", "research")

**If critical research needs detected:**
```
RESEARCH RECOMMENDED BEFORE PLANNING

Detected [N] research need(s) that may block planning:

CRITICAL:
  - [topic] - [reason]

Recommendation: Run $edge-research to generate prompts
for external deep research before creating the plan.

Continue anyway? (Some decisions may need to be revisited)
```

If no critical research needs, proceed with planning.

### 1. Understand the objective

What are we trying to achieve? If no objective is set, ask the user.

### 2. Break it into steps

Each step should be:
- Small enough to complete in one focused effort
- Testable (you can verify it worked)
- Independent where possible

### 3. Update active_context.yaml

```yaml
objective: "Clear statement of goal"
current_step: 1
plan:
  - description: "First step"
    status: pending
    proof: null
  - description: "Second step"
    status: pending
    proof: null
constraints:
  - "What must NOT happen"
risks:
  - risk: "What could go wrong"
    mitigation: "How to prevent/detect it"
```

### 4. Identify constraints

What should NOT change? What's off-limits?

### 5. Identify Risks (REQUIRED)

Ask yourself: "What are 3 ways this could fail?"

| Risk Type | Examples |
|-----------|----------|
| **Technical** | Wrong library, API changes, version conflicts |
| **Scope** | Feature creep, unclear requirements, missing edge cases |
| **Integration** | Breaks existing code, data format mismatch |
| **External** | Network failures, rate limits, auth issues |

```yaml
risks:
  - risk: "psycopg2 writes to PostgreSQL but app uses SQLite"
    mitigation: "Verify database connection string matches app config"
  - risk: "Sync might timeout on large datasets"
    mitigation: "Add batch processing with progress logging"
```

**Tip:** If you can't think of risks, the objective may be too vague.

## Output

After updating active_context.yaml, summarize:
- The objective
- Number of steps
- Key constraints
- **Top risks (at least 1 required)**
- Any research recommendations

Do NOT start implementation. Just plan.

## Arguments

- No arguments: Create plan for current objective, or ask for one
- `"objective text"`: Set this as the new objective and create plan
