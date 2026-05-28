---
name: implement-ticket
description: Implement a Beads ticket with documentation grounding, correctness checks, and full landing protocol completion.
---

# Implement Beads Ticket

## Purpose
Implement a Beads ticket with documentation grounding, correctness checks, and full landing protocol completion.

## When to use
- You are asked to implement a Beads ticket end-to-end.
- You must follow the Beads workflow including docs review and landing protocol.

## When NOT to use
- There is no Beads ticket or the work is exploratory only.
- The request is only for advice, triage, or code review.

## Procedure
1. Retrieve ticket details: run `bd show <ticket-id>` and read the full description, acceptance criteria, dependencies, and context.
2. Claim the ticket: run `bd update <ticket-id> --status=in_progress`.
3. Ground on relevant documentation before touching code: identify and read relevant `docs/` (start with `docs/index.md`; add `docs/scaffa_extension_authoring_guide.md`, `docs/scaffa_extension_api.md`, `docs/scaffa_ipc_boundaries_and_sequences.md`, or component docs as needed); note anything outdated or unclear.
4. Create a todo list if the ticket has multiple subtasks (example below).
5. Plan tests for lifecycle visibility: default to adding at least one Scaffa-specific test that captures the user sequence (event → IPC → state → UI). If tests are deferred, state why and file a follow-up ticket.
6. Implement the solution: follow documented patterns, update the todo list, run builds/tests as needed, and keep scope tight to the ticket.
7. Verify the implementation: run `pnpm run build`, run tests if applicable, and confirm acceptance criteria.
8. Check for documentation issues: re-review the docs you read and identify misleading, contradictory, or now-outdated content or missing docs for new patterns.
9. Correct documentation if needed: update or add docs and include doc fixes in the implementation commit or a separate commit.
10. Invoke the Code Review skill after implementation and doc updates; address any findings before proceeding.
11. Complete the landing protocol: `git status`, `git add <files>`, commit with a descriptive message that includes `Resolves <ticket-id>` and the co-author line, `bd sync`, `git push`, then `git status` must show "up to date with origin".
12. Close the ticket: run `bd close <ticket-id>`.

## Rules / Guardrails
- Always ground on relevant docs before coding.
- Always validate and correct documentation if issues are found.
- Always run `bd sync` and then `git push`; work is not complete until `git status` shows "up to date with origin".
- Never say "ready to push when you are"; you must push.
- Never include `.beads/issues.jsonl` in code commits.

## Examples
### Example: implement a ticket
Input:
```
/implement-ticket scaffa-7iq.11
```
Output (abridged):
```
bd show scaffa-7iq.11
bd update scaffa-7iq.11 --status=in_progress
# Read docs/index.md and docs/scaffa_extension_api.md
TodoWrite({
  todos: [
    { content: "Update GraphProducer.initialize() typing", status: "pending", activeForm: "Working on typing" },
    { content: "Run build", status: "pending", activeForm: "Running build" }
  ]
})
# Implement change, run npm run build, verify acceptance criteria
# Check docs for accuracy; update if needed
git status
git add src/extension-host/extension-context.ts
git commit -m "feat(extensions): type GraphProducer.initialize() as Promise<GraphSnapshot>

Resolves scaffa-7iq.11

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
bd sync
git push
git status
bd close scaffa-7iq.11
```
