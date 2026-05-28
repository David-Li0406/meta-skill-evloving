# Skill Selection: SDD vs Context-Aware-SDD vs Context-Engineering

Use this flowchart to decide which skill to invoke.

## Quick Decision

```
Have an implementation plan?
├── No → Don't use SDD skills
│   └── Use: superpowers:brainstorming → superpowers:writing-plans
│
└── Yes → How many tasks?
    ├── 1-2 tasks → Manual execution (no SDD needed)
    │
    ├── 3-4 tasks, small specs → superpowers:subagent-driven-development
    │
    └── 5+ tasks OR large specs → context-aware-sdd
        │
        └── Context problems detected? → context-engineering for diagnosis
```

## Detailed Decision Matrix

| Condition | Use This Skill |
|-----------|---------------|
| No plan yet | `superpowers:brainstorming` → `superpowers:writing-plans` |
| Plan with 1-2 simple tasks | Manual execution |
| Plan with 3-4 tasks, small specs (<200 words each) | `superpowers:subagent-driven-development` |
| Plan with 5+ tasks | `context-aware-sdd` |
| Any plan with large specs (>500 words each) | `context-aware-sdd` |
| Subagent asking many questions | `context-engineering` (diagnose) |
| Multiple review iterations | `context-engineering` (diagnose) |
| Building/debugging agent systems | `context-engineering` |
| Cross-session work | `episodic-memory:search-conversations` first |

## Skill Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                     context-engineering                          │
│  (Principles: Write, Select, Compress, Isolate)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Implements principles
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              superpowers:subagent-driven-development            │
│  (Fresh subagent per task + two-stage review)                   │
│  Implicit: Isolate                                              │
│  Partial: Select, Write                                         │
│  Missing: Compress, budget checks                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Extends with explicit checkpoints
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     context-aware-sdd                           │
│  (SDD + context engineering checkpoints)                        │
│  Full: Write, Select, Compress, Isolate                         │
│  Added: Budget checks, degradation detection, minimal-context   │
└─────────────────────────────────────────────────────────────────┘
```

## When to Escalate to context-engineering

During SDD or context-aware-sdd execution, escalate if:

| Signal | Threshold | Action |
|--------|-----------|--------|
| Subagent questions | >3 per task | Invoke `context-engineering` |
| Review iterations | >2 per stage | Invoke `context-engineering` |
| Same mistake twice | Any | Invoke `context-engineering` |
| Token warnings | >80% | Invoke `context-engineering` |
| Unexplained failures | Any | Invoke `context-engineering` |

## Skill Invocation Examples

### Starting fresh (no plan)
```
User: "Add user authentication to the app"
→ Invoke: superpowers:brainstorming
→ Then: superpowers:writing-plans
→ Then: context-aware-sdd (if 5+ tasks)
```

### Small plan
```
User: "Execute this 3-task plan"
→ Invoke: superpowers:subagent-driven-development
```

### Large plan
```
User: "Execute this 8-task feature plan"
→ Invoke: context-aware-sdd
→ Create prior_work_summary.md
→ Apply checkpoints
```

### Debugging context issues
```
User: "The subagent keeps missing requirements"
→ Invoke: context-engineering
→ Diagnose: Check context size, quality, positioning
→ Fix: Apply compression, restructure context
```

## File Locations

| Skill | Location |
|-------|----------|
| `context-engineering` | `.claude/skills/context-engineering/skill.md` |
| `context-aware-sdd` | `.claude/skills/context-aware-sdd/skill.md` |
| `superpowers:subagent-driven-development` | superpowers plugin (external) |
