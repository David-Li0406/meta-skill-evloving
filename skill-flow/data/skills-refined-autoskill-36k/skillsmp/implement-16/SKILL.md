---
name: implement
description: The workflow for implementing new features via sub-agents.
license: MIT
compatibility: opencode
---

## What I do
Break down the task into smaller sub-tasks. Considering this is an architect, please handle it with great care.
Do this breakdown yourself—don't hand it off to sub-agents.

For each breakdowned task, follow this workflow:
1. Think architect: Get the architect to think about how to implement this feature.
2. Design Types:    Define the type system or interface for the requested feature.
3. Implement Tests: Instruct `editor` to write unit tests based on the design. You MUST follow TDD style.
4. Implement Code:  Instruct `editor` to write the code to pass the tests.
5. Review:
   - Ask `reviewer` to check the diff.
   - If bugs are found, instruct `editor` to fix them.


## When to use me
Use this when you are ordered to implement a new feature.
Ask clarifying questions if the feature request is vague or incomplete.
