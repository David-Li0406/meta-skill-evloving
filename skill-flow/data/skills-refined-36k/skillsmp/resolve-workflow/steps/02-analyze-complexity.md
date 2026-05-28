---
name: analyze-complexity
description: Calculate ticket complexity score and determine workflow type
order: 2

skip_if:
  - flag: "--continue"
  - flag: "--refine-plan"

next:
  default: exploration
  conditions:
    - if: "complexity == 'SIMPLE'"
      then: create-plan

tools:
  - Read
  - Write
  - AskUserQuestion
---

# Step: Analyze Complexity

<context>
This step analyzes the ticket content to determine its complexity level (SIMPLE, MEDIUM, COMPLEX)
and decides the appropriate workflow phases. The complexity determines exploration depth and
planning approach.
</context>

## Instructions

<instructions>

### 1. Apply Analysis Skill

Apply skill: `~/.claude/skills/analyze-ticket/SKILL.md`

### 2. Calculate Complexity Score

Analyze ticket content and sum points from applicable factors:

| Factor | Points | Detection Signals |
|--------|--------|-------------------|
| Multi-component changes | +2 | Multiple services, modules, layers |
| Database schema changes | +2 | migration, schema, table, column |
| API breaking changes | +3 | breaking, deprecate, remove endpoint |
| New external dependency | +2 | integrate, new library, SDK |
| Performance requirements | +2 | optimize, performance, latency |
| Security implications | +2 | auth, permission, encryption |
| Vague requirements | +2 | Ambiguous, missing criteria |
| Research needed | +2 | investigate, explore, POC |
| Well-defined scope | -1 | Clear, specific requirements |
| Single file change | -1 | Obvious single-file fix |

### 3. Determine Level

```
score <= 2  → SIMPLE
score 3-5   → MEDIUM
score >= 6  → COMPLEX
```

### 4. Confirm Workflow Type (INTERACTIVE only)

```yaml
AskUserQuestion:
  question: "Complexite detectee: {level} (score: {score}). Confirmer le workflow ?"
  header: "Workflow"
  options:
    - label: "{detected level}"
      description: "{workflow description for level}"
    - label: "Forcer SIMPLE"
      description: "Passer directement au plan sans exploration"
    - label: "Forcer COMPLEX"
      description: "Workflow complet avec AEP"
```

### 5. Save Analysis

Write to `.claude/feature/{ticket-id}/analysis.md`

Update status: `phases.analyze = "completed"`, store `complexity` level

</instructions>

## Output

<output>
- File: `.claude/feature/{ticket-id}/analysis.md`
- Status: `phases.analyze = "completed"`, `complexity = "{level}"`
</output>

## Auto Behavior

<auto_behavior>
- Use detected complexity without confirmation
</auto_behavior>

## Complexity to Workflow Mapping

<workflow_mapping>
| Level | Exploration | Planning | AEP | Architect |
|-------|-------------|----------|-----|-----------|
| SIMPLE | Skip | Basic | No | No |
| MEDIUM | 1 agent | Standard | Partial | Optional |
| COMPLEX | 3 agents | Detailed | Full | Yes |
</workflow_mapping>
