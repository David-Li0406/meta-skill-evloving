---
name: skill-evolution-engine
description: Proposes creation, modification, or retirement of skills based on recurring user needs and system friction.
triggers: [repeated-patterns, manual-corrections, orchestration-overrides]
outputs: [skill-proposal, evolution-report]
depends_on: [user-intent-pattern-analyzer, workspace-orchestrator-adapter]
---

# Skill Evolution Engine

## Purpose

Enables the system to **evolve its own skill set** by identifying recurring patterns, friction points, and gaps. Proposes new skills, refinements, or deprecations to better serve user workflows.

---

## Triggers

This skill activates when observing:

- Repeated ad-hoc reasoning for the same task
- Repeated manual user corrections
- Repeated orchestration overrides
- Gaps between user intent and available skills
- Skills that are never invoked

---

## What This Skill Can Propose

| Action | When | Example |
|--------|------|---------|
| **New GLOBAL skill** | Cross-project pattern | "API versioning guardian" |
| **New WORKSPACE skill** | Project-specific need | "Django migration checker" |
| **Skill refinement** | Unclear scope | Narrow "test-generator" to "unit-test-generator" |
| **Skill deprecation** | Obsolete/redundant | Remove duplicate skills |
| **Skill merge** | Overlapping skills | Combine related skills |

---

## Evolution Process

### 1. Observe Patterns

```markdown
## Pattern Observed

**Pattern ID:** PAT-042
**Occurrences:** 7 times in last 30 days
**Context:** User repeatedly asks for database migration safety checks

**Evidence:**
- 2026-01-05: "Check if migration is reversible"
- 2026-01-08: "Verify migration won't drop data"
- 2026-01-12: "Is this migration safe to run?"
...
```

### 2. Analyze Friction

```markdown
## Friction Analysis

**Current State:** 
No skill handles database migration safety

**User Impact:**
- Manual reasoning each time (~15 min)
- Inconsistent checks across instances
- Risk of missed validations

**Friction Cost:** HIGH
```

### 3. Propose Skill

```markdown
## Skill Proposal

**Proposed Name:** database-migration-safety-checker
**Scope:** WORKSPACE (project-specific)

**Responsibility:**
- Validate migrations are reversible
- Check for data loss risks
- Verify foreign key constraints
- Flag long-running migrations

**Draft Instructions:**
1. Parse migration files
2. Identify irreversible operations (DROP, TRUNCATE)
3. Flag data type changes that lose precision
4. Check for missing down migrations

**Risk Assessment:**
- False negative risk: MEDIUM (could miss edge cases)
- Maintenance burden: LOW (stable domain)

**Approval Level:** Human approval recommended
```

### 4. Submit for Approval

| Approval Level | When | Authority |
|----------------|------|-----------|
| Auto-apply | Workspace skill, low risk | System |
| Human approval | Global skill or high impact | User |
| Skip | Pattern not strong enough | System |

---

## Output Format

Each proposal MUST include:

```markdown
# Skill Evolution Proposal

## 1. Observed Behavior Pattern
[What was observed, with evidence]

## 2. Current Friction Cost
[Impact on user/system]

## 3. Proposed Skill
- Name: [name]
- Scope: GLOBAL | WORKSPACE
- Description: [one line]

## 4. Draft Responsibility
[What the skill will do]

## 5. Risk Assessment
- Accuracy risk: LOW/MEDIUM/HIGH
- Maintenance risk: LOW/MEDIUM/HIGH
- Breaking change risk: LOW/MEDIUM/HIGH

## 6. Approval Required
- [ ] Auto-apply (workspace, low risk)
- [ ] Human approval required
```

---

## Deprecation Criteria

A skill should be deprecated when:

- Never invoked in 90 days
- Superseded by another skill
- Scope too broad (split instead)
- Requirements no longer exist

---

## Integration

- **Triggered by:** `user-intent-pattern-analyzer`, `workspace-orchestrator-adapter`
- **Outputs to:** Skill proposal queue
- **Approved by:** Human or system (based on risk)

---

## Constraints

- Evidence-based proposals only (no speculation)
- Minimum 3 occurrences before proposing
- Must not create skill sprawl
- Deprecation requires migration path

Evolution must be incremental and justified.
