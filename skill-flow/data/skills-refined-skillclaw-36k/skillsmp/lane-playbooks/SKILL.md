---
name: lane-playbooks
description: 'Kyora Agent OS lane workflows: Discovery, Planning, Implementation, Review, Validation, Recovery. Use when routing tasks through lanes, understanding lane-specific outputs, applying lane handoffs, or resuming work in a new session. Triggers: lane, discovery, planning, implementation, review, validation, recovery, handoff, continue.'
---

# Lane Playbooks

Operational playbooks for each lane in the Kyora Agent OS continuous cycle. Each lane has specific entry conditions, outputs, DoD, and token-efficient approaches.

## When to Use This Skill

- Routing a task to the correct lane
- Understanding what a lane should produce
- Handling lane transitions and handoffs
- Resuming unfinished work (Recovery lane)
- Ensuring correct lane DoD before handoff

## Prerequisites

- Familiarity with [KYORA_AGENT_OS.md](../../../KYORA_AGENT_OS.md) operating model
- Access to workspace for validation commands (Implementation/Validation lanes)

## Lane Overview

| Lane           | Entry Condition                          | Primary Owner        | Next Lane Default      |
|----------------|------------------------------------------|----------------------|------------------------|
| Discovery      | Unclear bug; unknown area; cross-stack   | Orchestrator / Lead  | Planning or Deferred   |
| Planning       | Medium/high risk; cross-stack; UX change | Lead                 | Implementation         |
| Implementation | Plan approved or low-risk clear change   | Implementer          | Review                 |
| Review         | Before declaring "done"                  | Lead / QA            | Validation             |
| Validation     | After changes land                       | QA / Implementer     | Release/Follow-up      |
| Recovery       | New session continues unfinished work    | Orchestrator         | Previous lane          |

## Lane Quick Reference

### Discovery

- **Entry**: unclear bug; unknown area; cross-stack unknown
- **Output**: findings + hypotheses + repro steps + next plan
- **DoD**: can explain the smallest next step with high confidence
- **Token playbook**: search first; read only relevant slices

### Planning

- **Entry**: medium/high risk; cross-stack; large refactor; UX changes
- **Output**: phased plan + acceptance checks + gates
- **DoD**: phases are verifiable; contracts and boundaries explicit
- **Token playbook**: keep plan compact; link SSOT files

### Implementation

- **Entry**: plan approved or low-risk change
- **Output**: code changes + tests; minimal notes
- **DoD**: acceptance criteria met; touched-area checks pass
- **Token playbook**: small change → validate immediately

### Review

- **Entry**: before declaring "done"
- **Output**: checklist results + fix list
- **DoD**: gates passed; consistency verified

### Validation

- **Entry**: after changes land
- **Output**: command evidence (tests/build/e2e) + any follow-ups
- **DoD**: relevant checks green; unrelated failures triaged

### Recovery

- **Entry**: new session continues an unfinished task
- **Output**: Recovery/Resume Packet (required before continuing)
- **DoD**: objective reconstructed; next smallest step identified

## References

- [Lane Discovery Details](./references/lane-discovery.md)
- [Lane Planning Details](./references/lane-planning.md)
- [Lane Recovery Details](./references/lane-recovery.md)
- [OS Examples](./references/examples.md)

## Handoff Rules (All Lanes)

Handoffs are **mandatory** when:

1. Switching lane owners (e.g., Lead → Implementer)
2. Switching scope (single-app → cross-stack)
3. Pausing mid-task (token/time)
4. Starting a new session for unfinished work

**Minimum rule**: no role starts Implementation without a task packet + a handoff packet (unless tiny, low-risk change).

Use the **agent-workflows skill** for all packet creation:

- **Delegation Packet**: Lead → Implementer (Workflow 2 in agent-workflows)
- **Phase Handoff Packet**: End of a phase (Workflow 3 in agent-workflows)
- **Recovery Packet**: New session continues unfinished work (Workflow 4 in agent-workflows)

See: [agent-workflows/SKILL.md](../agent-workflows/SKILL.md)

**Note**: The deprecated prompts (`/create-delegation-packet`, `/create-phase-handoff-packet`, `/create-recovery-packet`) are PO-only and cannot be triggered by agents.

## Success Checklist

- [ ] Correct lane selected based on risk + scope
- [ ] Lane entry conditions verified
- [ ] Lane-specific outputs produced
- [ ] DoD for lane met before handoff
- [ ] Handoff packet created when required
- [ ] No "surprise docs" generated
- [ ] Stop-and-ask triggers checked (see quality-gates)

## Stop-and-Ask Triggers

**MUST ask PO before proceeding** if any are true:

- Acceptance criteria missing and behavior ambiguous
- Schema changes or migrations needed
- Auth/RBAC/tenant boundary touched
- Breaking API contract implied
- New dependency needed

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Skill not activated | Description keywords don't match | Use explicit trigger words (lane, discovery, planning, etc.) |
| Wrong lane selected | Risk/scope misclassified | Re-evaluate using examples.md quick reference |
| Handoff packet missing context | Rushed handoff | Use handoff prompts, verify all fields completed |
| DoD unclear for lane | Lane reference not consulted | Read specific lane reference file |

## Validation Commands

Discovery/Planning lanes have no executable commands (output is plan/packet).

For Implementation/Validation lanes, run repo validation:

```bash
# Backend changes
make test.quick        # Unit tests
make openapi.check     # OpenAPI alignment

# Portal changes
make portal.check      # Lint + typecheck

# Full validation
make test              # All backend tests
make portal.build      # Portal build
```

## SSOT References

Do not duplicate these rules; link to them:

- Routing algorithm: [KYORA_AGENT_OS.md](../../../KYORA_AGENT_OS.md#L401-L575)
- Quality gates: [KYORA_AGENT_OS.md](../../../KYORA_AGENT_OS.md#L701-L789)
- Handoff templates: [KYORA_AGENT_OS.md](../../../KYORA_AGENT_OS.md#L1080-L1171)
