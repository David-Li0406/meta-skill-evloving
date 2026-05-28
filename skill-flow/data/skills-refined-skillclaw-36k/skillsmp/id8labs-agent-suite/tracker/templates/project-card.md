# Project Card Template

Use this template when creating a new project via `/tracker new`.

---

## Template

```yaml
---
slug: {project-slug}
name: {Project Name}
state: CAPTURED
health: 🟢
created: {YYYY-MM-DD}
last_activity: {YYYY-MM-DD}
state_entered: {YYYY-MM-DD}
decay_percent: 0
gates_passed: []
blockers: []
---
```

```markdown
# {Project Name}

## One-Liner

{What is this project in one sentence? Who is it for and what does it do?}

---

## Current Status

| Field | Value |
|-------|-------|
| **State** | {STATE} |
| **Health** | {🟢/🟡/🔴/❄️} |
| **Days in Stage** | {N} |
| **Decay** | {X}% |
| **Next Gate** | {CURRENT} → {NEXT} |

---

## Gate Progress

### {CURRENT STATE} → {NEXT STATE}

**MUST-HAVE:**
- [ ] Requirement 1
- [ ] Requirement 2
- [x] Completed requirement

**SHOULD-HAVE:**
- [ ] Optional enhancement 1

---

## State History

| Date | From | To | Notes |
|------|------|----|-------|
| {created} | - | CAPTURED | Initial capture |

---

## Activity Log

| Date | Activity | Source |
|------|----------|--------|
| {created} | Project created | /tracker new |

---

## Key Artifacts

| Artifact | Status | Location |
|----------|--------|----------|
| Validation Report | - | - |
| Architecture Doc | - | - |
| Launch Plan | - | - |
| Growth Model | - | - |
| Ops Playbook | - | - |
| Exit Memo | - | - |

---

## Blockers

{None currently}

---

## Notes

{Free-form notes, context, decisions, ideas}

---

## If Frozen

| Field | Value |
|-------|-------|
| Freeze Date | - |
| Freeze Reason | - |
| Previous State | - |
| Thaw Conditions | - |

---

*Last updated: {timestamp}*
*Tracked by ID8TRACKER*
```

---

## Field Definitions

### Frontmatter (YAML)

| Field | Type | Description |
|-------|------|-------------|
| slug | string | URL-safe identifier (kebab-case) |
| name | string | Human-readable project name |
| state | enum | Current lifecycle state |
| health | emoji | Current health indicator |
| created | date | When project was captured |
| last_activity | date | Most recent activity (for decay) |
| state_entered | date | When current state began |
| decay_percent | number | Current decay percentage (0-100) |
| gates_passed | array | Requirements marked complete |
| blockers | array | Active blockers (objects with description, logged, type) |

### Markdown Sections

| Section | Purpose |
|---------|---------|
| One-Liner | Quick pitch, who + what |
| Current Status | Snapshot for quick scan |
| Gate Progress | What's needed for next transition |
| State History | Audit trail of transitions |
| Activity Log | All activity that reset decay |
| Key Artifacts | Links to outputs from each skill |
| Blockers | Active issues blocking progress |
| Notes | Free-form context |
| If Frozen | Only populated when state = ICE |

---

## Example: New Project

```yaml
---
slug: thought-mapper
name: Thought Mapper
state: CAPTURED
health: 🟢
created: 2025-12-21
last_activity: 2025-12-21
state_entered: 2025-12-21
decay_percent: 0
gates_passed: []
blockers: []
---
```

```markdown
# Thought Mapper

## One-Liner

A visual tool for nonlinear thinkers to map connections between ideas, for creatives who think in webs not lists.

---

## Current Status

| Field | Value |
|-------|-------|
| **State** | CAPTURED |
| **Health** | 🟢 |
| **Days in Stage** | 0 |
| **Decay** | 0% |
| **Next Gate** | CAPTURED → VALIDATING |

---

## Gate Progress

### CAPTURED → VALIDATING

**MUST-HAVE:**
- [ ] Problem statement articulated
- [ ] Target audience defined
- [ ] Solution hypothesis stated
- [ ] Success criteria sketched

**SHOULD-HAVE:**
- [ ] Personal motivation noted
- [ ] Initial assumptions listed

---

## State History

| Date | From | To | Notes |
|------|------|----|-------|
| 2025-12-21 | - | CAPTURED | Initial capture |

---

## Activity Log

| Date | Activity | Source |
|------|----------|--------|
| 2025-12-21 | Project created | /tracker new |

---

## Key Artifacts

| Artifact | Status | Location |
|----------|--------|----------|
| Validation Report | - | - |
| Architecture Doc | - | - |
| Launch Plan | - | - |
| Growth Model | - | - |
| Ops Playbook | - | - |
| Exit Memo | - | - |

---

## Blockers

None currently

---

## Notes

Initial idea sparked from frustration with linear note-taking apps. Mind maps exist but feel clunky. What if it was more like a constellation?

---

*Last updated: 2025-12-21*
*Tracked by ID8TRACKER*
```

---

## Update Patterns

### On Activity Log
```markdown
| 2025-12-22 | Completed competitor research | /scout |
```

### On State Transition
```markdown
| 2025-12-23 | CAPTURED | VALIDATING | Started validation research |
```

### On Gate Pass
```yaml
gates_passed:
  - "Problem statement articulated"
  - "Target audience defined"
```

### On Blocker Added
```yaml
blockers:
  - description: "Need API access from mapping provider"
    logged: 2025-12-22
    type: external
```

### On Freeze
```markdown
## If Frozen

| Field | Value |
|-------|-------|
| Freeze Date | 2025-12-25 |
| Freeze Reason | Holiday break, resuming in January |
| Previous State | VALIDATING |
| Thaw Conditions | After New Year |
```
