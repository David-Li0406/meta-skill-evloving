---
template: report
status: draft
date: {{DATE}}
title: "{{TITLE}}"
author: {{AUTHOR}}
session: {{SESSION}}
lifecycle_phase: capture
tags: [report, analysis]
# DAG edge fields (E2-076b) - uncomment as needed
# spawned_by:
# blocked_by: []
# related: []
# milestone:
# backlog_ids: []
version: "1.1"
---
# generated: {{DATE}}
# System Auto: last updated on: 2025-12-16 18:17:40
# {{TITLE}}

@docs/README.md
@docs/epistemic_state.md

> **Date:** {{DATE}}
> **Session:** {{SESSION}}
> **Assignee:** {{AUTHOR}}
> **Status:** Completed

---

## Verification Requirements (RFC 2119)

| Requirement | Level | Action |
|-------------|-------|--------|
| Include evidence | MUST | Link to files, screenshots, test output, or other artifacts |
| Document methodology | SHOULD | Explain how conclusions were reached |
| List artifacts | MUST | Reference all relevant files in Artifacts section |

---

## Executive Summary

[Brief high-level summary of findings and outcomes]

---

## Technical Details

[Detailed analysis, data, and evidence]

### 1. Key Finding A
*   Observation: ...
*   Data: ...
*   Implication: ...

---

## Recommendations / Next Steps

1.  Action Item 1
2.  Action Item 2

---

## Artifacts
*   [Link to relevant files]

---


<!-- VALIDATION ERRORS (2025-12-16 18:17:27):
  - ERROR: Invalid status 'completed' for report template. Allowed: draft, active, complete, archived, final, reviewed, disputed
-->
