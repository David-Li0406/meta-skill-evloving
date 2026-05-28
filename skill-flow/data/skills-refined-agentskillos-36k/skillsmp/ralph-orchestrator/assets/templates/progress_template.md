# Progress: {{task-name}}

**Started**: {{timestamp}}
**Current Iteration**: 0
**Mode**: {{mode}}

## Learnings (append-only)

<!--
CRITICAL: This section is APPEND-ONLY. Each iteration adds learnings here.
Format: [Iteration N] <what you learned>

These learnings persist across iterations and help you avoid repeating mistakes.
DO NOT delete or modify previous entries - only add new ones.

Example entries:
[Iteration 1] Project uses ESM modules, need "type": "module" in package.json
[Iteration 2] Test runner expects files to match *.test.ts pattern
[Iteration 3] Database connection requires awaiting pool.connect() before queries
-->

## Current State

**Working on**: Not started
**Current Story**: {{first-story-id}}
**Blockers**: none
**Last verification**: not yet run
**Last commit**: none
**Attempts on current issue**: 0

## Story Status

<!-- Update this as stories are completed -->
{{#each stories}}
- [ ] {{id}}: {{title}}
{{/each}}

## Iteration History

<!--
Brief log of what happened each iteration.
Keep entries concise - details go in Learnings section.

Format:
### Iteration N
- **Focus**: What you worked on
- **Result**: success/failure/partial
- **Next**: What to do next iteration
-->

## Blocked Stories

<!--
Stories that couldn't be completed after 3 attempts.
Format:
- {{story-id}}: <reason blocked>
  - Attempted: <what was tried>
  - Alternative needed: <suggested approach>
-->

## Context Health

<!-- Update these metrics to monitor context window usage -->
**Progress file size**: ~50 lines
**Last major commit**: none
**Recommended action**: none

<!--
When to take action:
- If progress.md > 300 lines: Archive old iterations to progress_archive.md
- If 3+ stories complete: Create summary commit
- If stuck 3+ iterations: Use escape hatch pattern
-->
