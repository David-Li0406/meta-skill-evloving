# Skill Inventory

complete catalog of available skills with triggers and composition hints.

## meta/ - skills about skills

| skill | triggers | chains with |
|-------|----------|-------------|
| skill-create | "create skill", "new skill", "scaffold skill" | ask-deep (intake), pair (validate) |
| skill-improve | "improve skill", "enhance skill", "skill to 10/10" | pair (validate), skill-audit (batch) |
| skill-audit | "audit skills", "review all skills", "skill health" | skill-improve (fix issues) |
| skill-compose | "compose skills", "chain skills", "which skills", "suggest skills" | any skill combination |
| metaprompt-factory | "create prompt", "metaprompt", "XML prompt" | pair (review) |

## orchestration/ - autonomous work

| skill | triggers | chains with |
|-------|----------|-------------|
| loop | "work on issue", "autonomous loop", "implement X", "complex task" | issue-context (prep), pr-audit (post), pair (checkpoints + delegation) |

## context/ - context preservation

| skill | triggers | chains with |
|-------|----------|-------------|
| context | "save context", "checkpoint", "handoff to agent", modes: journal, checkpoint, handoff | loop (persistence), pair (handoffs) |

## review/ - external validation

| skill | triggers | chains with |
|-------|----------|-------------|
| pair | "pair with codex", "get second opinion", "delegate this", "consult", "quick check", "thorough review" | any (unified validation + delegation) |
| pr-audit | "review PR", "audit PR", "pre-merge check" | loop (post-implementation) |
| project-review | "audit project", "check patterns", "align with standards" | loop (pre-work) |

## connections/ - external CLIs

| skill | triggers | chains with |
|-------|----------|-------------|
| slack | "slack message", "notify via slack", "slack audit" | loop (notifications), pair (results) |
| imessage | "send message", "text luke", "iMessage" | loop (notifications) |

## clarify/ - question flows

| skill | triggers | chains with |
|-------|----------|-------------|
| ask-deep | "ask me questions", "help me think through", "clarify requirements" | skill-create (intake), loop (planning) |

## enrich/ - context augmentation

| skill | triggers | chains with |
|-------|----------|-------------|
| issue-context | "enrich issue", "add context to issue", "prep issue for agent" | loop (pre-work), linear (post) |

## persona/ - design voices

| skill | triggers | chains with |
|-------|----------|-------------|
| emil-kowalski | "linear style", "tasteful animation", "emil design" | dashboard, loop (UI work) |

## scaffold/ - app scaffolding

| skill | triggers | chains with |
|-------|----------|-------------|
| dashboard | "scaffold dashboard", "admin dashboard", "convex dashboard" | emil-kowalski (styling) |

## docs/ - documentation maintenance

| skill | triggers | chains with |
|-------|----------|-------------|
| agent-docs-audit | "audit AGENTS.md", "maintain agent docs", "check CLAUDE.md" | project-review |

---

## trigger priority

when multiple skills match, prioritize:

1. **explicit mention**: user names the skill
2. **strong trigger**: exact phrase match
3. **context fit**: working directory, recent actions
4. **composition**: skill that chains well with context

## composition compatibility

```
high compatibility:
├── issue-context → loop (prep for autonomous work)
├── ask-deep → skill-create (intake → scaffold)
├── skill-improve → pair (improve → validate)
├── loop → pr-audit (implement → review)
├── pair quick → pair thorough (escalation within pair)
└── context checkpoint → loop (persistence for long runs)

low compatibility:
├── imessage → slack (choose one notification channel)
└── skill-create → skill-improve (create first, then improve)
```

## skill complexity scores

| skill | complexity | typical depth |
|-------|------------|---------------|
| imessage | low | < 1 min |
| slack | low-medium | 1-3 min |
| skill-compose (plan) | low | instant |
| ask-deep | medium | 3-8 rounds |
| issue-context | medium | 10-15 min |
| skill-create | medium | 15-30 min |
| pr-audit | medium | 5-15 min |
| metaprompt-factory | medium | 10-20 min |
| dashboard | medium-high | 20-40 min |
| emil-kowalski | medium | design decisions |
| context | medium | varies by mode |
| project-review | medium-high | 15-30 min |
| agent-docs-audit | medium | 10-20 min |
| skill-improve | high | 20-60 min |
| pair | varies | 1 min (quick) to 30+ min (thorough) |
| skill-compose (execute) | high | varies |
| skill-audit | high | 30-60 min |
| loop | very high | 30 min - hours |
