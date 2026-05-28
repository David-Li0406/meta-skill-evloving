---
name: update-documentation
description: >
  Trigger documentation updates based on recent code changes.
  Use when user says "update documentation" or "document [scope]".
  Assesses changes, updates README/feature docs/architecture docs, and verifies documentation builds.
---

# Update Documentation

Trigger documentation updates based on recent code changes.

**Usage**: When user says "update documentation" or "document [scope]"

## Instructions

1. **Assess Changes**:
   - Identify recent code changes (commits, modified files).
   - Determine impact on existing documentation (API references, feature guides, architecture docs).

2. **Update Documentation**:
   - Use the Documentation Agent for comprehensive updates.
   - Update `README.md` if high-level features changed.
   - Update specific feature docs in `docs/`.
   - Update architecture diagrams or descriptions if designs changed.

3. **Verify**:
   - Ensure the documentation site (if applicable) builds.
   - Verify links and references are valid.
   - Ensure consistent style and tone.

## Scopes

- `feature`: Focus on a specific feature folder.
- `api`: Focus on API reference updates.
- `global`: Review and update project-level docs (README, Architecture).
