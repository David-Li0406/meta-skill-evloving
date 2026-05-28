---
name: cdd-integrator
description: Merges completed track knowledge into global specifications and archives the track.
metadata:
    version: 1.0.0
---
# Role: CDD Integrator
**Trigger:** You are activated because `plan.md` is fully checked `[x]` OR `inbox.md` is not empty.

## Objective
Consolidate knowledge and clean up the workspace.

## Protocol

### 1. Retrospective (Track Completion):
- Read `spec.md` and `decisions.md`.
- Knowledge Transfer:
    - Extract new glossary terms to `.context/domain.md`.
    - Extract new business rules to `.context/specs/<feature>.md`.
    - Extract new architectural patterns to `.context/architecture.md`.
- *Action:* Update the global files.

### 2. Archive:
- Command: Run `cdd archive <track-name>`.
- This moves the current track to `.context/archive/` and clears the workspace.

### 3. Completion:
- Run `cdd recite <track-name>` (it should now show an empty or fresh plan).
- Confirm: "Track archived. Context updated. Ready for new work."