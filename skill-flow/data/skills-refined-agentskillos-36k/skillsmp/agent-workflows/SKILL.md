---
name: agent-workflows
description: 'Core Kyora Agent OS workflows for task routing, delegation, handoffs, and recovery. Use when: routing a new task through the OS, delegating work between agents, creating handoff packets at phase boundaries, recovering/resuming work in a new session. Keywords: route, delegate, handoff, packet, recovery, resume, continue, task, phase.'
---

# Agent Workflows

Core operational workflows for Kyora Agent OS task lifecycle: routing → delegation → phase handoffs → recovery.

**Note**: These workflows are skill-based (agent-runnable). The deprecated prompt versions (`/route-task`, `/create-delegation-packet`, etc.) should not be used by agents.

## When to Use This Skill

- **Task Routing**: Classifying and routing a new task from PO
- **Delegation**: Handing off work from Lead to Implementer (or between agents)
- **Phase Handoff**: Documenting completed phase before transitioning
- **Recovery**: Resuming unfinished work in a new session

## Prerequisites

- Familiarity with [KYORA_AGENT_OS.md](../../../KYORA_AGENT_OS.md)
- Access to workspace for codebase search (routing/recovery)

---

## Workflow 1: Task Routing

### When

- New task from PO needs classification and owner assignment
- Orchestrator receives ambiguous or cross-stack request

### Inputs Required

| Field | Description | Required |
|-------|-------------|----------|
| Title | Short task title | Yes |
| Type | feature \| bug \| refactor \| chore \| discovery \| planning \| design \| content \| i18n \| testing \| devops \| new-project | Yes |
| Scope | single-app \| cross-stack \| monorepo-wide | Yes |
| Goal | 1-3 sentence description | Yes |
| Non-goals | What is explicitly out of scope | No |
| Acceptance criteria | Bullet list of success conditions | Yes |
| Constraints | Technical/business constraints | No |
| Risk hints | auth \| payments \| PII \| schema \| dependencies \| major UX \| data migration | No |
| References | Screenshots, endpoints, files, logs | No |

### Routing Algorithm

1. **Classify Risk**:
   - `Low`: Local change, no schema/deps/auth/PII/major UX
   - `Medium`: Shared libs, minor contract changes, non-trivial UI flow
   - `High`: auth/RBAC/tenant safety/payments/PII/schema/migrations/major UX/breaking contract

2. **Select Lane**:
   - Repro unclear / unknown area → **Discovery**
   - Cross-stack / medium-high risk / needs UX spec → **Planning**
   - Clear requirements + low risk → **Implementation**

3. **Assign Owners**:
   | Scope | Primary Owner | Secondary (if cross-stack) |
   |-------|--------------|---------------------------|
   | Backend only | Backend Lead | — |
   | Portal only | Web Lead | — |
   | Cross-stack | Orchestrator coordinates | Backend Lead + Web Lead |
   | Monorepo-wide | DevOps/Platform Lead | — |

4. **Identify Gates**:
   - `High` risk → PO approval required before Implementation
   - Schema changes → PO gate
   - New dependencies → PO gate
   - Auth/RBAC/tenant changes → PO gate

### Output: TASK PACKET

```markdown
TASK PACKET

Title: [title]
Type: [type]
Scope: [scope]
Risk: [Low | Medium | High]

Goal (1-3 sentences):
[goal]

Non-goals (explicitly out of scope):
- [non-goal 1]
- [non-goal 2, or "None specified"]

Acceptance criteria (from PO):
- [ ] [criterion 1]
- [ ] [criterion 2]

Constraints:
- [constraint 1, or "None specified"]

Risk hints:
- [hint 1, or "None specified"]

Classification:
- Lane: [Discovery | Planning | Implementation]
- Primary owner: [role]
- Secondary owner: [role, or "None"]

Gates:
- [ ] [gate 1, or "None required"]

Reuse targets (search results):
- [pattern/component, or "TBD during Discovery"]

SSOT references:
- [instruction file, or "TBD"]

Assumptions:
- [assumption 1, or "None"]
```

---

## Workflow 2: Delegation

### When

- Lead delegates to Implementer
- Orchestrator delegates to Lead
- Any agent-to-agent work handoff

### Inputs Required

| Field | Description | Required |
|-------|-------------|----------|
| From | Role handing off | Yes |
| To | Role receiving | Yes |
| Objective | One sentence | Yes |
| Type | feature \| bug \| refactor \| etc. | Yes |
| Scope | single-app \| cross-stack \| monorepo-wide | Yes |
| Risk | Low \| Medium \| High | Yes |
| Acceptance criteria | From PO | Yes |
| Gates | PO approvals needed | Yes |
| Key decisions | Important decisions already made | No |
| Assumptions | Explicit assumptions | No |
| Reuse targets | Patterns/components to reuse | No |
| SSOT references | Instruction files consulted | No |
| Files/areas | Files or areas likely touched | Yes |
| Risks/watch-outs | Potential issues | No |

### Output: DELEGATION PACKET

```markdown
DELEGATION PACKET

From: [role]
To: [role]
Date: [YYYY-MM-DD]

Objective (1 sentence): [objective]

Classification:
- Type: [type]
- Scope: [scope]
- Risk: [risk]

Acceptance criteria (from PO):
- [ ] [criterion 1]
- [ ] [criterion 2]

Gates (PO approvals needed):
- [ ] [gate 1, or "None"]

Key decisions already made:
- [decision 1, or "None yet"]

Assumptions (explicit):
- [assumption 1, or "None"]

Reuse targets (patterns/components):
- [target 1, or "TBD"]

SSOT references (instruction files):
- [reference 1]

Files/areas likely touched:
- [file/area 1]

Risks/watch-outs:
- [risk 1, or "None identified"]

Validation command(s):
- [command, or "TBD"]
```

---

## Workflow 3: Phase Handoff

### When

- Completing Phase 0/1/2/3
- Transitioning between lanes
- Pausing work mid-task (token limit, time)

### Inputs Required

| Field | Description | Required |
|-------|-------------|----------|
| Phase completed | Phase 0 \| Phase 1 \| Phase 2 \| Phase 3 | Yes |
| Current lane | Discovery \| Planning \| Implementation \| Review \| Validation | Yes |
| Next lane | Discovery \| Planning \| Implementation \| Review \| Validation \| Done | Yes |
| What changed | Facts about modifications (files, endpoints) | Yes |
| What's verified | Commands run and results | Yes |
| What remains | Next 3-7 steps in order | Yes |
| Open questions | Pending gates or questions | No |
| Backend contract status | stable \| changed \| pending \| N/A | Yes |
| Portal integration status | not started \| WIP \| done \| N/A | Yes |
| i18n keys status | not started \| WIP \| done \| N/A | Yes |
| E2E/RTL validation status | not started \| WIP \| done \| N/A | Yes |

### Output: PHASE HANDOFF PACKET

```markdown
PHASE HANDOFF PACKET

Phase just completed: [phase]
Current lane: [lane]
Next lane: [lane]

What changed (facts only):
- [change 1]
- [change 2]

What's verified (commands run + result):
- [command]: [result]

What remains (next 3-7 steps in order):
1. [step 1]
2. [step 2]
3. [step 3]

Open questions / pending gates:
- [question 1, or "None"]

Status matrix:
| Area | Status |
|------|--------|
| Backend contract | [stable \| changed \| pending \| N/A] |
| Portal integration | [not started \| WIP \| done \| N/A] |
| i18n keys | [not started \| WIP \| done \| N/A] |
| E2E/RTL validation | [not started \| WIP \| done \| N/A] |

Next owner: [role]
```

---

## Workflow 4: Recovery

### When

- New session continues unfinished work
- Token limit hit mid-task
- Context loss after break

### Inputs Required

| Field | Description | Required |
|-------|-------------|----------|
| Goal | One sentence overall objective | Yes |
| Last known lane | Discovery \| Planning \| Implementation \| Review \| Validation | Yes |
| What's done | Based on git changes/tests | Yes (can be investigated) |
| What's broken | Failing tests or errors | No |
| Next step | Smallest verifiable next step | Yes |
| Commands to run first | Commands to verify state | Yes |
| Pending gates | PO approvals still needed | No |
| Assumptions to confirm | Assumptions to re-verify | No |

### Recovery Procedure

1. **Investigate state** (if inputs unclear):
   - Check git status/changes: `git status && git diff --stat`
   - Run relevant tests: `make test.quick` or `make portal.check`
   - Check for errors: `make portal.check` or `go build ./...`

2. **Reconstruct context**:
   - Read last handoff packet if available
   - Review recent git commits
   - Check TODO.md for task context

3. **Emit Recovery Packet** (required before continuing work)

### Output: RECOVERY PACKET

```markdown
RECOVERY PACKET

Goal (1 sentence): [goal]
Last known lane: [lane]

What's already done (based on git changes/tests):
- [done item 1]
- [done item 2, or "Unknown - needs investigation"]

What's broken / failing (if any):
- [failure 1, or "None known"]

Next smallest verifiable step:
- [step]

Commands to run first:
- [command 1]
- [command 2]

Pending gates (PO approvals still needed):
- [gate 1, or "None"]

Assumptions to confirm before continuing:
- [assumption 1, or "None"]

Recommended next action: [action]
```

---

## Approval Needed Template

When an agent needs PO approval during any workflow:

```markdown
---
## ⚠️ APPROVAL NEEDED

**Decision Required**: [Brief description]
**Context**: [Why this decision point was reached]
**Options**:
1. [Option A] — [pros/cons]
2. [Option B] — [pros/cons]

**Risks if proceeding without approval**: [List risks]

**To continue**: Reply with your decision or ask for more context.
---
```

---

## Success Checklist

- [ ] Correct workflow selected for the situation
- [ ] All required inputs collected (or investigated)
- [ ] Packet emitted in correct format
- [ ] No narrative/explanation added beyond the packet
- [ ] Gates identified and flagged for PO if needed
- [ ] Next owner/action clearly specified

## Deprecated Prompts

The following prompts are **deprecated** for agent use (agents cannot trigger prompts):

- `/route-task` → Use **Workflow 1** above
- `/create-delegation-packet` → Use **Workflow 2** above
- `/create-phase-handoff-packet` → Use **Workflow 3** above
- `/create-recovery-packet` → Use **Workflow 4** above

These prompts remain available for PO manual invocation but should not be referenced in agent instructions or handoffs.
