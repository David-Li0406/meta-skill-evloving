# Escalation Patterns

decision trees for escalating between agents and to HIL.

## agent escalation

```
copilot result received
├── confidence >= 8
│   └── accept result, no escalation
├── confidence 5-7
│   ├── task is blocking → escalate to codex
│   ├── task is exploratory → accept with caution
│   └── conflicting signals → escalate to codex
├── confidence < 5
│   ├── codex available → escalate to codex
│   └── codex unavailable → escalate to HIL
└── explicit uncertainty ("I'm not sure", "need more context")
    └── always escalate to codex
```

## codex escalation

```
codex result received
├── confidence >= 8
│   └── accept result
├── confidence 5-7
│   ├── implementation task → iterate once with more context
│   └── consultation → accept with documented uncertainty
├── confidence < 5
│   └── escalate to HIL
└── blocking issue stated
    └── escalate to HIL
```

## HIL escalation triggers

**always escalate when:**

| trigger | reason |
|---------|--------|
| confidence < 5 from codex | fundamental uncertainty |
| security/secrets involved | high risk |
| infra/deploy decisions | irreversible impact |
| conflicting requirements | human judgment needed |
| scope creep detected | confirm expanded scope |
| agent explicitly asks | respect agent uncertainty |

**escalation format:**

```markdown
## HIL Needed

**Task:** {what was being done}
**Agent:** {copilot | codex}
**Confidence:** {score}/10

**Blocking issue:**
{specific question or problem}

**Context:**
{relevant session state}

**Options considered:**
1. {option A} - {tradeoffs}
2. {option B} - {tradeoffs}
```

## iteration vs escalation

```
Agent output has issues
├── Minor issues (typos, small logic fixes)
│   └── iterate: "Please also fix X"
│   └── max 2 iterations for codex, 3 for copilot
├── Structural issues (wrong approach)
│   ├── clear correct approach known → re-prompt with direction
│   └── unclear correct approach → escalate to higher tier
├── Fundamental problems (wrong understanding)
│   ├── copilot → escalate to codex
│   └── codex → escalate to HIL
└── No improvement after iteration
    └── escalate to next tier
```

## graceful degradation

```
Preferred agent unavailable
├── codex unavailable, task is thorough
│   ├── copilot can handle → use with extra validation
│   └── too complex → claude implements directly
├── copilot unavailable, task is quick
│   ├── codex available → use (overkill but works)
│   └── neither available → claude implements directly
└── both unavailable
    └── claude implements with explicit limitations noted
```

## confidence calibration

| confidence | meaning | typical action |
|------------|---------|----------------|
| 9-10 | high certainty | proceed |
| 8 | confident with minor caveats | proceed, note caveats |
| 7 | reasonably confident | proceed for non-critical |
| 6 | moderate confidence | escalate for critical |
| 5 | uncertain | always escalate |
| 1-4 | low confidence | escalate + document |

## escalation anti-patterns

| pattern | problem | fix |
|---------|---------|-----|
| escalating on first uncertainty | wastes higher-tier resources | try iteration first |
| never escalating | misses blocking issues | respect confidence scores |
| escalating without context | forces re-investigation | include full context packet |
| skipping tiers | wastes resources | copilot → codex → HIL |
| escalating style issues | not worth HIL time | iterate or accept |
