---
name: update-prd
description: Sync prd.md with current specs and implementation. Use when the user asks to update PRD or sync prd, or when new changes should be reflected in prd.md and related doc references.
---

# Update Prd

## Overview

Keep `prd.md` aligned with the latest requirements and behavior. Update any references in other docs so filenames and terminology stay consistent.

## Workflow

1. Identify deltas
- Read `openspec/specs/**` for authoritative requirements.
- Scan relevant code (`wrestlegm/ui.py`, `wrestlegm/state.py`, `data/*.json`) for behavior changes.
- Check recent archived changes in `openspec/changes/archive/` for newly added requirements.

2. Map deltas to PRD sections
- UI changes: update UX sections, indicators, widget mapping, and mockups.
- Simulation/data changes: update domain model or simulation sections.
- Navigation/flow changes: update the core loop and screen list.

3. Apply edits
- Keep changes tightly scoped to the deltas found.
- Match the current UI formatting (tables, headers, emoji markers).
- Keep examples and mockups consistent with real formatting rules.

4. Consistency pass
- Update references to the PRD filename (now `prd.md`) in README/docs.
- Ensure alignment emojis, fatigue/booked markers, and truncation rules match spec.

## References

Load `references/prd-sources.md` for a checklist of common files to compare.
