# Lane: Discovery

Detailed reference for the Discovery lane in Kyora Agent OS.

## Entry Conditions

Start in Discovery when:

- Bug repro is unclear or inconsistent
- Area of code is unknown to the current agent
- Cross-stack unknowns exist (unclear which side owns what)
- Requirements are vague and need investigation

## Owner

- **Primary**: Orchestrator or relevant Domain Lead
- **Supporting**: QA/Test Specialist (for repro), relevant Implementers (for codebase knowledge)

## Outputs (Required)

1. **Findings summary** — What was discovered (facts only)
2. **Hypotheses** — Potential causes or approaches (ranked by likelihood)
3. **Repro steps** — If applicable, exact steps to reproduce
4. **Next plan** — What should happen next (route to Planning, Implementation, or Deferred)

## Definition of Done

- Can explain the smallest next step with high confidence
- Either: route to next lane with clear handoff, OR defer with structured backlog item

## Token Playbook

1. **Search first**: Use grep/semantic search before reading full files
2. **Read only relevant slices**: Don't read entire large files
3. **Document as you go**: Keep findings in a compact format
4. **Stop after 3 failed searches**: Ask for hints (file/feature name) or escalate to Lead

## Tool Allowlist

| Tool | When to Use |
|------|-------------|
| `read` | Read specific file sections |
| `search` | Find patterns, symbols, usages |
| `grep_search` | Exact string matching |
| `semantic_search` | Fuzzy concept matching |
| `GitHub MCP` | Only for issue/PR context (not local codebase) |

**Forbidden**: `edit`, `execute` (Discovery is read-only)

## Output Format

```
DISCOVERY OUTPUT

Objective investigated:
-

Findings (facts):
-

Hypotheses (ranked):
1.
2.

Repro steps (if applicable):
-

Recommended next lane:
- [ ] Planning (medium/high risk, needs phased plan)
- [ ] Implementation (low risk, clear next step)
- [ ] Deferred (needs PO prioritization)

Handoff notes:
-
```

## Common Failure Modes

| Failure | Prevention |
|---------|------------|
| Reading too much, burning tokens | Search first, read slices only |
| Jumping to implementation | Stay in Discovery until DoD met |
| Vague findings | Use facts-only format |
| Forgetting cross-stack | Check if both backend + portal involved |

## Escalation Triggers

Escalate to PO if:

- Cannot find repro after 3 attempts
- Issue involves auth/RBAC/payments/PII
- Multiple hypotheses with significant blast radius
- Issue may be "by design" (needs product decision)
