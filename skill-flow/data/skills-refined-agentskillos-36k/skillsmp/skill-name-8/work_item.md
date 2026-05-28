---
template: work_item
id: {{BACKLOG_ID}}
title: "{{TITLE}}"
type: {{TYPE}}
status: active
owner: Hephaestus
created: {{DATE}}
spawned_by: {{SPAWNED_BY}}
chapter: null
arc: null
closed: null
priority: medium
effort: medium
requirement_refs: []
source_files: []
acceptance_criteria: []
blocked_by: []
blocks: []
enables: []
current_node: backlog
node_history:
  - node: backlog
    entered: {{TIMESTAMP}}
    exited: null
artifacts: []
cycle_docs: {}
memory_refs: []
extensions: {}
version: "2.0"
generated: {{DATE}}
last_updated: {{TIMESTAMP}}
---
# {{BACKLOG_ID}}: {{TITLE}}

@docs/README.md
@docs/epistemic_state.md

---

## Context

[Problem and root cause]

---

## Deliverables

<!-- VERIFICATION REQUIREMENT (Session 192 - E2-290 Learning)

     These checkboxes are the SOURCE OF TRUTH for work completion.

     During CHECK phase of implementation-cycle:
     - Agent MUST read this section
     - Agent MUST verify EACH checkbox can be marked complete
     - If ANY deliverable is incomplete, work is NOT done

     "Tests pass" ≠ "Deliverables complete"
     Tests verify code works. Deliverables verify scope is complete.

     NOTE (WORK-001): Acceptance criteria are in frontmatter (machine-parseable).
     Deliverables are implementation outputs, not requirements.
-->

- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

---

## History

### {{DATE}} - Created (Session {{SESSION}})
- Initial creation

---

## References

- [Related documents]
