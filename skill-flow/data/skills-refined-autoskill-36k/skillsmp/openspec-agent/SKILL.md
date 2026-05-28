---
name: openspec-agent
description: Implement features and tasks defined in openspec proposals.
---

# Instructions

When assigned to implement an openspec proposal, follow these steps:

1. Read the `openspec/` proposal you've been assigned to understand requirements, specifically proposal.md, spec.md, tasks.md, and design.md (if it exists).
2. Perform only tasks listed in `tasks.md`.
3. Write code that exactly matches the spec. Do not modify spec files.
4. Write test code to verify the implemented features and ensure old and new tests pass.
5. Mark tasks as complete in `tasks.md` once they are fully implemented. 
6. On completion, run `openspec validate --strict && openspec archive`.
