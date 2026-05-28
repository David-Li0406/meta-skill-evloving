---
name: flow-next-interview
description: Use this skill to conduct in-depth interviews about an epic, task, or spec file to extract complete implementation details, refine requirements, or clarify features before building.
---

# Flow Interview

Conduct a thorough interview about a task/spec and write refined details back.

**IMPORTANT**: This plugin uses `.flow/` for ALL task tracking. Do NOT use markdown TODOs, plan files, TodoWrite, or other tracking methods. All task state must be read and written via `flowctl`.

**CRITICAL**: `flowctl` is BUNDLED — NOT installed globally. Always use:
```bash
ROOT="$(git rev-parse --show-toplevel)"
FLOWCTL="$ROOT/plugins/flow-next/scripts/flowctl"
$FLOWCTL <command>
```

**Role**: Technical interviewer, spec refiner  
**Goal**: Extract complete implementation details through deep questioning (40+ questions typical).

## Input

Full request: `$ARGUMENTS`

Accepts:
- **Flow epic ID** `fn-N` or `fn-N-xxx`: Fetch with `flowctl show`, write back with `flowctl epic set-plan`.
- **Flow task ID** `fn-N.M` or `fn-N-xxx.M`: Fetch with `flowctl show`, write back with `flowctl task set-description/set-acceptance`.
- **File path** (e.g., `docs/spec.md`): Read file, interview, rewrite file.
- **Empty**: Prompt for target.

Examples:
- `/flow-next:interview fn-1`
- `/flow-next:interview fn-1.3`
- `/flow-next:interview docs/oauth-spec.md`

If empty, ask: "What should I interview you about? Give me a Flow ID (e.g., fn-1) or file path (e.g., docs/spec.md)."

## Setup

```bash
ROOT="$(git rev-parse --show-toplevel)"
FLOWCTL="$ROOT/plugins/flow-next/scripts/flowctl"
```

## Detect Input Type

1. **Flow epic ID pattern**: matches `fn-\d+(-[a-z0-9]+)?` (e.g., fn-1, fn-1-abc).
   - Fetch: `$FLOWCTL show <id> --json`.
   - Read spec: `$FLOWCTL cat <id>`.

2. **Flow task ID pattern**: matches `fn-\d+(-[a-z0-9]+)?\.\d+` (e.g., fn-1.3, fn-1-abc.2).
   - Fetch: `$FLOWCTL show <id> --json`.
   - Read spec: `$FLOWCTL cat <id>`.
   - Also get epic context: `$FLOWCTL cat <epic-id>`.

3. **File path**: anything else with a path-like structure or `.md` extension.
   - Read file contents.
   - If file doesn't exist, ask user to provide a valid path.

## Interview Process

Use the **question** tool for all questions. Group 2-4 questions per tool call. Expect 40+ total for complex specs. Wait for answers before continuing.

Rules:
- Each question must include: `header` (<=12 chars), `question`, and `options` (2-5).
- `custom` defaults to true, so users can type a custom answer.
- Keep option labels short (1-5 words) and add a brief `description`.
- Prefer concrete options; include “Not sure” when ambiguous.

Example tool call (schema only):
```json
question({
  "questions": [
    {
      "header": "Header",
      "question": "Where should the badge appear?",
      "options": [
        {"label": "Left", "description": "Near logo"},
        {"label": "Right", "description": "Near user menu"},
        {"label": "Center", "description": "Centered"},
        {"label": "Not sure", "description": "Decide based on layout"}
      ]
    }
  ]
})
```

## Write Refined Spec

After the interview is complete, write everything back.

### For Flow Epic ID

1. Create a temp file with the refined epic spec including:
   - Clear problem statement.
   - Technical approach with specifics.
   - Key decisions made during the interview.
   - Edge cases to handle.
   - Quick commands section (required).
   - Acceptance criteria.

2. Update epic spec:
```bash
$FLOWCTL epic set-plan <id> --file <temp-md> --json
```

3. Create/update tasks if the interview revealed breakdown:
```bash
$FLOWCTL task create --epic <id> --title "..." --json
$FLOWCTL task set-description <task-id> --file <temp-md> --json
$FLOWCTL task set-acceptance <task-id> --file <temp-md> --json
```

### For Flow Task ID

1. Write description to temp file with:
   - Clear task description.
   - Technical details from the interview.
   - Edge cases.

2. Write acceptance to temp file with:
   - Checkboxes for acceptance criteria.
   - Specific, testable conditions.

3. Update task:
```bash
$FLOWCTL task set-description <id> --file <desc-temp.md> --json
$FLOWCTL task set-acceptance <id> --file <acc-temp.md> --json
```

### For File Path

Rewrite the file with refined spec:
- Preserve any existing structure/format.
- Add sections for areas covered in the interview.
- Include technical details, edge cases, acceptance criteria.
- Keep it actionable and specific.

## Completion

Show summary:
- Number of questions asked.
- Key decisions captured.
- What was written (Flow ID updated / file rewritten).
- Suggest next step: `/flow-next:plan` or `/flow-next:work`.

## Notes

- This process should feel thorough - the user should feel they've thought through everything.
- Quality over speed - don't rush to finish.