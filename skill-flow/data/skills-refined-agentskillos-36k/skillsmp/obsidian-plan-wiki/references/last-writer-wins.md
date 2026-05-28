# Last-Writer-Wins Source-of-Truth Model

This model decides whether **docs** or **code** is the current authority when they diverge. It applies per feature, not globally. The newest authoritative change wins.

---

## Definition

**Last-Writer-Wins (LWW) Source-of-Truth** means: for each feature or spec, the **most recent authoritative artifact** supersedes older artifacts. The authoritative artifact can be either a doc/spec or code, depending on which changed most recently.

- If the newest change is in **docs/specs**, docs are authoritative and **code must be rewritten** to match.
- If the newest change is in **code**, code is authoritative and **docs must be updated** to match.

This model treats docs and code as two competing versions of the same behavior. The most recent one wins by default.

---

## What Counts as an Authoritative Change

An authoritative change is a deliberate design or behavior decision, not a formatting tweak.

**Docs/spec authoritative changes include:**
- Behavior changes in workstream specs
- New UI/UX flows, layouts, or constraints
- Updated success criteria or failure modes
- Changes to contracts, inputs/outputs, or integration rules
- Complete revision of the whole workstream

**Code authoritative changes include:**
- Behavior changes visible to users
- New API/bridge behavior
- New lifecycle or state transitions
- Changes to default configuration or UX flow

Non-authoritative changes that **do not** flip source of truth:
- Typos, formatting, or copy edits
- Pure refactors with no behavior change
- Build script changes unrelated to user behavior

---

## Scope: Per Feature, Not Global

Source of truth is decided per feature or spec. You might have:
- Preferences: docs ahead → code must change
- Command Palette: code ahead → docs must change

Never apply one decision across the whole repo without checking each area.

---

## Decision Procedure (Use Git History)

1. **Identify the feature or spec**
   - Example: "Preferences pane layout" or "Context menu behavior"

2. **Locate primary docs**
   - Workstream README and relevant spec files in `docs/workstreams/`

3. **Locate primary code**
   - Find the implementation files for that feature

4. **Compare recency**
   - Check the most recent commit that changes behavior in docs vs code.
   - The newer authoritative change wins.

5. **Tag the drift**
   - **DOCS-ahead** → rewrite code to match docs
   - **CODE-ahead** → update docs to match code

---

## How to Deal With Drift (Action Rules)

### Case A: DOCS-ahead (Docs are newer)

1. **Treat docs as the spec**
2. **Rewrite code** to match the described behavior
3. **Remove or deprecate old code paths**
4. **Update tests** to enforce the new behavior
5. **Mark doc change as implemented**
6. **Update changelog** with the implementation change

### Case B: CODE-ahead (Code is newer)

1. **Treat code as reality**
2. **Update docs/specs** to match the implemented behavior
3. **Revise success criteria or failure modes** if needed
4. **Update changelog** with the doc update

---

## Required Output for Each Drift Finding

For every drift item, record:
- **Feature name**
- **Docs location** (file path)
- **Code location** (file path)
- **Which is newer** (docs or code)
- **Action** (rewrite code or update docs)
- **Notes** (what behavior differs)

Example:
```
Feature: Preferences Pane Layout
Docs: docs/workstreams/04-preferences/4.2-layout.md
Code: src/preferences/PreferencesController.swift
Newer: Docs (2026-01-15)
Action: Rewrite code to match spec
Notes: Spec defines 2-column layout with sidebar; code uses tabbed view.
```

---

## Escalation Rules

If both sides changed recently and intent is unclear:
1. Check related workstream README notes and changelog
2. Look for explicit ADRs or decisions
3. Ask for a decision; do not guess

---

## Enforcement Checklist (Per Feature)

- [ ] Compare docs vs code behavior
- [ ] Identify which changed last (authoritative)
- [ ] Tag as DOCS-ahead or CODE-ahead
- [ ] Apply the correct action rule
- [ ] Update changelog
