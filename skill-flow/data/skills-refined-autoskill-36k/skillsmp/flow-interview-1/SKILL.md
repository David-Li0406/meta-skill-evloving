---
name: flow-interview
description: Conduct in-depth interviews to extract complete implementation details for features, epics, or tasks. Use when user wants to flesh out a spec, refine requirements, clarify a feature before building, or explore edge cases and acceptance criteria through thorough questioning.
---

# Flow Interview

Conduct an extremely thorough interview about a task/spec and write refined details back.

**IMPORTANT**: This uses `.flow/` for ALL task tracking. Do NOT use markdown TODOs, plan files, or other tracking methods. All task state must be read and written via `flowctl`.

## Setup

All commands use the repo-local flowctl CLI with dynamic path resolution:

```bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo (git rev-parse failed; cwd may be outside repo)."
  exit 1
fi
FLOWCTL="$REPO_ROOT/.flow/bin/flowctl"
```

**Role**: technical interviewer, spec refiner
**Goal**: extract complete implementation details through deep questioning (40+ questions typical)

## Input

Accepts:
- **Flow epic ID** `fn-N-xxx` (e.g., `fn-1-abc`) or legacy `fn-N`: Fetch with `flowctl show`, write back with `flowctl epic set-plan`
- **Flow task ID** `fn-N-xxx.M` (e.g., `fn-1-abc.2`) or legacy `fn-N.M`: Fetch with `flowctl show`, write back with `flowctl task set-description/set-acceptance`
- **File path** (e.g., `docs/spec.md`): Read file, interview, rewrite file
- **Empty**: Prompt for target

Examples:
- "Interview me about fn-1-abc"
- "Refine requirements for fn-1-abc.3"
- "Interview: docs/oauth-spec.md"

If no input provided, ask: "What should I interview you about? Give me a Flow ID (e.g., fn-1-abc) or file path (e.g., docs/spec.md)"

## Detect Input Type

1. **Flow epic ID pattern**: matches `fn-\d+(-[a-z0-9]+)?` (e.g., fn-1-abc, fn-12, fn-42-z9k)
   - Fetch: `$FLOWCTL show <id> --json`
   - Read spec: `$FLOWCTL cat <id>`

2. **Flow task ID pattern**: matches `fn-\d+(-[a-z0-9]+)?\.\d+` (e.g., fn-1-abc.3, fn-12.5)
   - Fetch: `$FLOWCTL show <id> --json`
   - Read spec: `$FLOWCTL cat <id>`
   - Also get epic context: `$FLOWCTL cat <epic-id>`

3. **File path**: anything else with a path-like structure or .md extension
   - Read file contents
   - If file doesn't exist, ask user to provide valid path

## Interview Process

Ask questions across these categories. Group 2-4 related questions at a time.

### Question Categories

**1. Problem & Context**
- What problem does this solve?
- Who are the users/stakeholders?
- What's the current workaround (if any)?
- Why is this important now?

**2. Scope & Boundaries**
- What's explicitly IN scope?
- What's explicitly OUT of scope?
- What's the minimum viable version?
- What could be deferred to later?

**3. User Flows**
- Walk through the happy path
- What triggers this feature?
- What's the expected outcome?
- How does the user know it worked?

**4. Edge Cases**
- What if the input is invalid?
- What if the system is under load?
- What if dependencies fail?
- What about concurrent users?

**5. Data & State**
- What data is needed?
- Where does it come from?
- How is it validated?
- What's the data lifecycle?

**6. Integration Points**
- What existing systems does this touch?
- What APIs are involved?
- Are there external dependencies?
- What about authentication/authorization?

**7. Error Handling**
- What errors can occur?
- How should each be handled?
- What feedback does the user get?
- How are errors logged/monitored?

**8. Testing & Validation**
- How do we know it works?
- What test scenarios are critical?
- How do we verify edge cases?
- What's the acceptance criteria?

**9. Non-Functional Requirements**
- Performance expectations?
- Security considerations?
- Accessibility requirements?
- Compliance/regulatory needs?

**10. Rollout & Operations**
- How is this deployed?
- Feature flags needed?
- Monitoring/alerting requirements?
- Rollback plan?

## NOT in scope (defer to flow-plan)

- Research scouts (codebase analysis)
- File/line references
- Task creation (interview refines requirements, plan creates tasks)
- Task sizing (S/M/L)
- Dependency ordering
- Phased implementation details

## Write Refined Spec

After interview complete, write everything back - **scope depends on input type**.

### For NEW IDEA (text input, no Flow ID)

Create epic with interview output. **DO NOT create tasks** - that's `flow-plan`'s job.

```bash
$FLOWCTL epic create --title "..." --json
$FLOWCTL epic set-plan <id> --file - --json <<'EOF'
# Epic Title

## Problem
Clear problem statement

## Key Decisions
Decisions made during interview (e.g., "Use OAuth not SAML", "Support mobile + web")

## Edge Cases
- Edge case 1
- Edge case 2

## Open Questions
Unresolved items that need research during planning

## Acceptance
- [ ] Criterion 1
- [ ] Criterion 2
EOF
```

Then suggest: "Run `flow-plan` with fn-N to research best practices and create tasks."

### For EXISTING EPIC (fn-N that already has tasks)

**First check if tasks exist:**
```bash
$FLOWCTL tasks --epic <id> --json
```

**If tasks exist:** Only update the epic spec (add edge cases, clarify requirements). **Do NOT touch task specs** - plan already created them.

**If no tasks:** Update epic spec, then suggest `flow-plan`.

### For Flow Task ID (fn-N.M)

**First check if task has existing spec from planning:**
```bash
$FLOWCTL cat <id>
```

**If task has substantial planning content** (description with file refs, sizing, approach):
- **Do NOT overwrite** - planning detail would be lost
- Only ADD new acceptance criteria discovered in interview
- Or suggest interviewing the epic instead

**If task is minimal** (just title, empty or stub description):
- Update task with interview findings
- Focus on **requirements**, not implementation details

```bash
$FLOWCTL task set-spec <id> --description /tmp/desc.md --acceptance /tmp/acc.md --json
```

### For File Path

Rewrite the file with refined spec:
- Preserve any existing structure/format
- Add sections for areas covered in interview
- Include edge cases, acceptance criteria
- Keep it requirements-focused (what, not how)

This is typically a pre-epic doc. After interview, suggest `flow-plan <file>` to create epic + tasks.

## Completion

Show summary:
- Number of questions asked
- Key decisions captured
- What was written (Flow ID updated / file rewritten)

Suggest next step based on input type:
- New idea / epic without tasks -> `flow-plan fn-N`
- Epic with tasks -> `flow-work fn-N` (or more interview on specific tasks)
- Task -> `flow-work fn-N.M`
- File -> `flow-plan <file>`

## Notes

- This process should feel thorough - user should feel they've thought through everything
- Quality over speed - don't rush to finish

## Verification

````bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo (git rev-parse failed; cwd may be outside repo)."
  exit 1
fi

# Verify skill file exists
ls "$REPO_ROOT/.factory/skills/flow-interview/SKILL.md"
# Expected: file exists, exit code 0

# Verify flowctl is callable
"$REPO_ROOT/.flow/bin/flowctl" --help >/dev/null 2>&1 && echo "flowctl OK"
# Expected: outputs "flowctl OK", exit code 0
````
