---
name: upstream-evaluation
description: Evaluate upstream changes using Navigator's design frameworks to decide what to adopt, skip, or adapt
triggers:
  - evaluate upstream
  - assess changes
  - integration decisions
  - what should we adopt
archetype: analysis
user_invocable: false
---

# Upstream Evaluation Skill

Systematic evaluation of upstream changes using Navigator's design frameworks. This skill focuses purely on **decision-making** — what to adopt, skip, or adapt — not execution.

## Primary Reference

**Read first:** [docs/architecture/DESIGN.md](../../../docs/architecture/DESIGN.md)

This document defines Navigator's:
- Layer model (user surface vs. internals)
- Decision frameworks (A-E)
- Naming conventions
- Consolidation patterns
- Historical decisions as precedent

## Evaluation Process

### Step 1: Categorize Each Change

For each upstream change, determine its type:

| Type | Examples | Primary Framework |
|------|----------|-------------------|
| New feature/action | `styles`, `recording_start` | Framework A |
| Renamed API | `snapshot` → `capture` | Framework B |
| Upstream adopts our concept | They add element refs | Framework C |
| Multiple related actions | `getByText`, `getByRole`, etc. | Framework D |
| Bug fix, security patch | Any fix commit | Framework E (always adopt) |
| Branding/vendor-specific | Marketplace plugins | Framework E (always skip) |

### Step 2: Apply Decision Framework

#### Framework A: New Upstream Feature

```
Does it benefit agents?
├─ NO → Skip or defer
└─ YES → Does Navigator have existing concept?
    ├─ YES → Extend existing (don't duplicate)
    └─ NO → Add new action
        └─ Is upstream naming agent-friendly?
            ├─ YES → Adopt (camelCase conversion)
            └─ NO → Create Navigator name
```

**Output format:**
```markdown
### [feature-name]
- **Decision**: Adopt / Skip / Defer / Extend existing
- **Navigator name**: `camelCaseName` (if adopting)
- **Category**: Navigation / Interaction / Capture / etc.
- **Rationale**: Why this decision
```

#### Framework B: Upstream Renames Something

```
Which layer affected?
├─ INTERNAL → Align with upstream (no user impact)
└─ USER SURFACE → Is new name objectively better?
    ├─ NO → Keep Navigator name (stability wins)
    └─ YES → Migration with deprecation
```

**Output format:**
```markdown
### [renamed-thing]
- **Decision**: Align internally / Keep Navigator name / Migrate with deprecation
- **Layer affected**: Internal / User surface
- **Rationale**: Why this decision
```

#### Framework C: Upstream Catches Up

```
Upstream adopts our concept
└─ Is naming identical?
    ├─ YES → Simplify executor (remove translation)
    └─ NO → Keep Navigator name, simplify mapping
```

#### Framework D: Consolidate vs. Mirror

```
Multiple upstream actions with related purpose
└─ Are they cognitively distinct for agents?
    ├─ YES → Mirror as separate actions
    └─ NO → Consolidate with parameters
```

#### Framework E: Quick Classification

| Classification | Action | Examples |
|----------------|--------|----------|
| Bug fix | Always adopt | Crash fixes, edge cases |
| Security patch | Always adopt immediately | Auth fixes, XSS prevention |
| Performance | Usually adopt | Unless invasive |
| Branding | Always skip | Vendor plugins, marketplace |
| Dev tooling | Evaluate | May not benefit agents |

### Step 3: Check Naming Conventions

For each adopted feature, verify naming follows conventions:

| Layer | Convention | Check |
|-------|------------|-------|
| MCP action | camelCase | `recordingStart` not `recording_start` |
| CLI command | verb-noun | `nav recording start` |
| Parameters | camelCase | `colorScheme` not `color_scheme` |

**Reordering rule:** Verb should come first for CLI-friendly naming.
- `tab_new` → `newTab` (verb-noun in camelCase)
- `recording_start` → `recordingStart` (verb already first)

### Step 4: Identify Schema Changes

For each adopted feature, specify:

```markdown
### Schema Changes Required

#### [action-name]
**File**: `packages/core/src/schema/index.ts`
**Type**: New action / Extend existing / Modify parameters

```typescript
// Proposed schema
export const actionNameSchema = baseActionSchema.extend({
  action: z.literal('actionName'),
  // parameters...
})
```

**Executor mapping**: `actionName` → upstream `action_name`
```

### Step 5: Document Decisions

Compile all decisions into a structured format:

```markdown
## Evaluation Summary

### Adopt
| Feature | Navigator Name | Category | Schema Change |
|---------|---------------|----------|---------------|
| styles | `styles` | Capture | New action |
| recording_* | `recordingStart/Stop/Restart` | Capture | 3 new actions |

### Skip
| Feature | Reason |
|---------|--------|
| marketplace plugin | Branding-specific (Framework E) |

### Defer
| Feature | Reason | Revisit When |
|---------|--------|--------------|
| feature-x | Unclear agent benefit | When use case emerges |

### Extend Existing
| Feature | Existing Action | Change |
|---------|-----------------|--------|
| tab_new url param | `newTab` | Add optional `url` parameter |
```

## Evaluation Checklist

Before completing evaluation:

- [ ] Every change categorized (new/rename/catchup/multiple/fix/branding)
- [ ] Appropriate framework applied to each
- [ ] Naming conventions verified for all adoptions
- [ ] Schema changes specified with code snippets
- [ ] Decisions documented with rationale
- [ ] Historical precedents checked in DESIGN.md

## Invocation

This skill is loaded by the `/agent-browser:integrate-changes` command.

## Handoff

After evaluation completes, hand off to:

- **Documentation**: `/agent-browser:issue` to create tracking issue
- **Execution**: `/agent-browser:update` for merge/sync steps
- **Implementation**: `senior-dev` agent for schema changes

The evaluation output becomes the "what and why" — other commands handle "how."
