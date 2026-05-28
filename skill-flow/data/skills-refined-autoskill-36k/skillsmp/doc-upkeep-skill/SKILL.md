---
name: doc-upkeep-skill
description: Update technical documentation by aligning with audience needs, validating workflows end-to-end, and cross-linking related resources.
---

# Documentation Upkeep Skill

Use for maintaining README, runbooks, API references, or product docs. Focus on keeping instructions accurate, reproducible, and connected to code changes.

## Workflow

1. **Audience & scope**
   - Identify the reader (operators, contributors, end users) and tailor depth, tone, and prerequisites.
   - Pin the section or file you plan to edit; note any related docs.
2. **Motivation**
   - Capture the underlying change, constraints, and trade-offs.
   - Link to commits or tickets so readers can trace the root cause quickly.
3. **Validate steps**
   - Execute commands, scripts, or API calls exactly as documented.
   - Update prerequisites, environment variables, and version pins when they drift.
4. **Highlight deltas**
   - Use tables or bullet lists for parameter changes.
   - Reference source files for verification and call out behavior impacts.
5. **Manage context**
   - Cross-link adjacent guides, deprecate stale content, and avoid duplicating canonical sources.
   - Note where further detail lives (code comments, dashboards, external docs).
6. **Review**
   - Re-read for clarity and formatting consistency.
   - Suggest reviewers or follow-up checks if additional eyes are needed.

## Output scaffold

```
### Audience
- who benefits + pain solved

### Updates
- bullets describing doc edits + why they matter

### Verification
- commands/tests/logs confirming accuracy

### Follow-ups
- remaining gaps or docs to revisit
```

## Safeguards

- Avoid inventing commands; if unsure, ask the user or flag the uncertainty.
- Do not remove warnings or caveats without confirming they are obsolete.
- Prefer linking to canonical sources rather than duplicating long reference sections.
