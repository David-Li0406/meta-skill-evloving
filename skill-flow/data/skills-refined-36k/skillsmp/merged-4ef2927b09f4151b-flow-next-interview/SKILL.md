---
name: flow-next-interview
description: Use this skill to conduct in-depth interviews about an epic, task, or spec file to extract complete implementation details, refine requirements, or clarify features before building. Triggers on /flow-next:interview with Flow IDs (fn-1, fn-1-abc, fn-1.2) or file paths.
---

# Flow Interview

Conduct a thorough interview about a task/spec and write refined details back.

**IMPORTANT**: This plugin uses `.flow/` for ALL task tracking. Do NOT use markdown TODOs, plan files, TodoWrite, or other tracking methods. All task state must be read and written via `flowctl`.

**CRITICAL**: `flowctl` is BUNDLED — NOT installed globally. Always use:
```bash
FLOWCTL="${CLAUDE_PLUGIN_ROOT}/scripts/flowctl"
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
- `/flow-next:interview fn-1-abc`
- `/flow-next:interview docs/oauth-spec.md`

If empty, ask: "What should I interview you about? Give me a Flow ID (e.g., fn-1) or file path (e.g., docs/spec.md)."

## Setup

```bash
FLOWCTL="${CLAUDE_PLUGIN_ROOT}/scripts/flowctl"
```

## Detect Input Type

1. **Flow epic ID pattern**: matches `fn-\d+(-[a-z0-9]+)?` (e.g., fn-1-abc, fn-12).
   - Fetch: `$FLOWCTL show <id> --json`.
   - Read spec: `$FLOWCTL cat <id>`.

2. **Flow task ID pattern**: matches `fn-\d+(-[a-z0-9]+)?\.\d+` (e.g., fn-1-abc.3).
   - Fetch: `$FLOWCTL show <id> --json`.
   - Read spec: `$FLOWCTL cat <id>`.
   - Also get epic context: `$FLOWCTL cat <epic-id>`.

3. **File path**: anything else with a path-like structure or .md extension.
   - Read file contents.
   - If file doesn't exist, ask user to provide a valid path.

## Interview Process

**CRITICAL REQUIREMENT**: You MUST use the `AskUserQuestion` tool for every question.

- DO NOT output questions as text.
- DO NOT list questions in your response.
- ONLY ask questions via `AskUserQuestion` tool calls.
- Group 2-4 related questions per tool call.
- Expect 40+ questions total for complex specs.

## Question Categories

Read [questions.md](questions.md) for all question categories and interview guidelines.

## Write Refined Spec

After the interview is complete, write everything back — **scope depends on input type**.

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

3. Create/update tasks if the interview revealed a breakdown:
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

- This process should feel thorough — the user should feel they've thought through everything.
- Quality over speed — don't rush to finish.