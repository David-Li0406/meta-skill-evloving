# Plan Review Workflow

## Philosophy

The reviewer model only sees selected files. RepoPrompt's Builder discovers context you'd miss. You coordinate - the backend reviews.

---

## Setup

```bash
REPO_ROOT="${REPO_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || true)}"
if [ -z "$REPO_ROOT" ]; then
  echo "Error: Set REPO_ROOT=/absolute/path/to/repo (git rev-parse failed; cwd may be outside repo)."
  exit 1
fi
FLOWCTL="$REPO_ROOT/.flow/bin/flowctl"
```

---

## Phase 0: Backend Detection

**Run this first. Do not skip.**

```bash
# Priority: --review flag > env > config
BACKEND=$($FLOWCTL review-backend)

if [[ "$BACKEND" == "ASK" ]]; then
  echo "Error: No review backend configured."
  echo "Configure review.backend in .flow/config.json, or pass --review=rp|none"
  exit 1
fi

echo "Review backend: $BACKEND (override: --review=rp|none)"
```

**If backend is "none"**: Skip review, inform user, and exit cleanly (no error).

**Then branch to backend-specific workflow below.**

---

## RepoPrompt Backend Workflow

Use when `BACKEND="rp"`.

### Phase 1: Read the Plan

```bash
EPIC_ID="${1:-}"

# Get epic details
$FLOWCTL show "$EPIC_ID" --json
$FLOWCTL cat "$EPIC_ID"
```

Save output for inclusion in review prompt. Compose a 1-2 sentence summary for the setup-review command.

### Phase 2: Atomic Setup

```bash
# Atomic: pick-window + builder
eval "$($FLOWCTL rp setup-review --repo-root "$REPO_ROOT" --summary "Review plan for $EPIC_ID: <summary>")"

# Verify we have W and T
if [[ -z "${W:-}" || -z "${T:-}" ]]; then
  echo "Error: setup-review failed. Ensure RepoPrompt is running."
  exit 1
fi

echo "Setup complete: W=$W T=$T"
```

If this block fails, inform user and stop. Do not improvise.

### Phase 3: Augment Selection

Builder selects context automatically. Review and add must-haves:

```bash
# See what builder selected
$FLOWCTL rp select-get --window "$W" --tab "$T"

# Always add the epic spec
$FLOWCTL rp select-add --window "$W" --tab "$T" .flow/specs/${EPIC_ID}.md

# Always add ALL task specs for this epic
for task_spec in .flow/tasks/${EPIC_ID}.*.md; do
  [[ -f "$task_spec" ]] && $FLOWCTL rp select-add --window "$W" --tab "$T" "$task_spec"
done

# Add PRD/architecture docs if found
[[ -f docs/prd.md ]] && $FLOWCTL rp select-add --window "$W" --tab "$T" docs/prd.md
```

**Why this matters:** Chat only sees selected files. Reviewer needs both epic spec AND task specs to check for consistency.

### Phase 4: Build and Send Review Prompt

Get builder's handoff:
```bash
HANDOFF="$($FLOWCTL rp prompt-get --window "$W" --tab "$T")"
```

Write combined prompt:
```bash
cat > /tmp/review-prompt.md << 'EOF'
[PASTE HANDOFF HERE]

---

## IMPORTANT: File Contents
RepoPrompt includes the actual source code of selected files in a `<file_contents>` XML section at the end of this message. You MUST:
1. Locate the `<file_contents>` section
2. Read and analyze the actual source code within it
3. Base your review on the code, not summaries or descriptions

If you cannot find `<file_contents>`, ask for the files to be re-attached before proceeding.

## Plan Under Review
[PASTE flowctl show OUTPUT]

## Review Focus
[USER'S FOCUS AREAS]

## Review Scope

You are reviewing:
1. **Epic spec** - The high-level plan
2. **Task specs** - Individual task breakdowns

**CRITICAL**: Check for consistency between epic and tasks. Flag if:
- Task specs contradict or miss epic requirements
- Task acceptance criteria don't align with epic acceptance criteria
- Task approaches would need to change based on epic design decisions
- Epic mentions states/enums/types that tasks don't account for

## Review Criteria

Conduct a John Carmack-level review:

1. **Completeness** - All requirements covered? Missing edge cases?
2. **Feasibility** - Technically sound? Dependencies clear?
3. **Clarity** - Specs unambiguous? Acceptance criteria testable?
4. **Architecture** - Right abstractions? Clean boundaries?
5. **Risks** - Blockers identified? Security gaps? Mitigation?
6. **Scope** - Right-sized? Over/under-engineering?
7. **Testability** - How will we verify this works?
8. **Consistency** - Do task specs align with epic spec?

## Output Format

For each issue:
- **Severity**: Critical / Major / Minor / Nitpick
- **Location**: Which task or section (e.g., "fn-1-abc.3 Description" or "Epic Acceptance #2")
- **Problem**: What's wrong
- **Suggestion**: How to fix

**REQUIRED**: You MUST end your response with exactly one verdict tag. This is mandatory:
`<verdict>SHIP</verdict>` or `<verdict>NEEDS_WORK</verdict>` or `<verdict>MAJOR_RETHINK</verdict>`

Do NOT skip this tag. The automation depends on it.
EOF
```

Send to RepoPrompt:
```bash
$FLOWCTL rp chat-send --window "$W" --tab "$T" --message-file /tmp/review-prompt.md --new-chat --chat-name "Plan Review: $EPIC_ID"
```

**WAIT** for response. Takes 1-5+ minutes.

### Phase 5: Extract Verdict and Update Status

Extract verdict from response, then:
```bash
# If SHIP
$FLOWCTL epic set-plan-review-status "$EPIC_ID" --status ship --json

# If NEEDS_WORK or MAJOR_RETHINK
$FLOWCTL epic set-plan-review-status "$EPIC_ID" --status needs_work --json
```

If no verdict tag in response, ask reviewer to clarify.

---

## Fix Loop

**CRITICAL: Do NOT ask user for confirmation. Automatically fix ALL valid issues and re-review.**

**CRITICAL: You MUST fix the plan BEFORE re-reviewing. Never re-review without making changes.**

If verdict is NEEDS_WORK:

1. **Parse issues** - Extract ALL issues by severity (Critical -> Major -> Minor)

2. **Fix the epic spec** - Address each issue:
   ```bash
   # Use stdin heredoc (preferred, no temp file)
   $FLOWCTL epic set-plan "$EPIC_ID" --file - --json <<'EOF'
   <updated epic spec content>
   EOF
   ```
   **If you skip this and re-review with same content, reviewer will return NEEDS_WORK again.**

3. **Sync affected task specs** - If epic changes affect task specs, update them:
   ```bash
   $FLOWCTL task set-spec <TASK_ID> --file - --json <<'EOF'
   <updated task spec content>
   EOF
   ```
   Task specs need updating when epic changes affect:
   - State/enum values referenced in tasks
   - Acceptance criteria that tasks implement
   - Approach/design decisions tasks depend on
   - Lock/retry/error handling semantics
   - API signatures or type definitions

4. **Request re-review** (only AFTER steps 2-3):

   **IMPORTANT**: Do NOT re-add files already in the selection. RepoPrompt auto-refreshes file contents on every message. Only use `select-add` for NEW files created during fixes.

   **CRITICAL: Do NOT summarize fixes.** RP auto-refreshes file contents - reviewer sees your changes automatically. Just request re-review.

   ```bash
   cat > /tmp/re-review.md << 'EOF'
   Issues addressed. Please re-review.

   **REQUIRED**: End with `<verdict>SHIP</verdict>` or `<verdict>NEEDS_WORK</verdict>` or `<verdict>MAJOR_RETHINK</verdict>`
   EOF

   $FLOWCTL rp chat-send --window "$W" --tab "$T" --message-file /tmp/re-review.md
   ```

5. **Repeat** until SHIP

---

## Anti-patterns

**All backends:**
- **Reviewing yourself** - You coordinate; the backend reviews
- **Ignoring verdict** - Must extract and act on verdict tag
- **Mixing backends** - Stick to one backend for the entire review session

**RP backend only:**
- **Calling builder directly** - Must use `setup-review` which wraps it
- **Skipping setup-review** - Window selection MUST happen via this command
- **Hard-coding window IDs** - Never write `--window 1`
- **Re-adding files before re-review** - RP auto-refreshes; re-adding can cause issues
- **Re-reviewing without fixing** - Wastes reviewer time and loops forever
- **Updating epic without syncing tasks** - Causes reviewer to flag consistency issues again
