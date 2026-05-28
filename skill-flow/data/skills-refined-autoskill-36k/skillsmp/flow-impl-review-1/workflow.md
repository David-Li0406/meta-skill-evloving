# Implementation Review Workflow

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

## Phase 0: Parse Arguments and Detect Backend

**Run this first. Do not skip.**

### Parse Arguments

Parse arguments for:
- `--base <commit>` -> `BASE_COMMIT` (if provided, use for scoped diff)
- First positional arg matching `fn-*` -> `TASK_ID`
- Remaining args -> focus areas

If `--base` not provided, `BASE_COMMIT` stays empty (will fall back to main/master).

### Backend Detection

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

### Phase 1: Identify Changes

```bash
BRANCH="$(git branch --show-current)"

# Use BASE_COMMIT from arguments if provided (task-scoped review)
# Otherwise fall back to main/master (full branch review)
if [[ -z "$BASE_COMMIT" ]]; then
  DIFF_BASE="main"
  git rev-parse main >/dev/null 2>&1 || DIFF_BASE="master"
else
  DIFF_BASE="$BASE_COMMIT"
fi

# Get commit info
COMMITS="$(git log ${DIFF_BASE}..HEAD --oneline)"
CHANGED_FILES="$(git diff ${DIFF_BASE}..HEAD --name-only)"

echo "Reviewing changes: ${DIFF_BASE}..HEAD"
echo "Commits: $COMMITS"
echo "Changed files: $CHANGED_FILES"
```

### Phase 2: Build Review Instructions

Build XML-structured instructions for the builder review mode:

```bash
cat > /tmp/review-instructions.txt << EOF
<task>Review changes from ${DIFF_BASE}..HEAD for correctness, simplicity, and potential issues.

Focus on:
- Correctness - Logic errors, spec compliance
- Simplicity - Over-engineering, unnecessary complexity
- Edge cases - Failure modes, boundary conditions
- Security - Injection, auth gaps

Only flag issues in the changed code - not pre-existing patterns.
</task>

<context>
Branch: $BRANCH
Commits:
$COMMITS

Changed files:
$CHANGED_FILES
$([ -n "$TASK_ID" ] && echo "Task: $TASK_ID")
$([ -n "$FOCUS_AREAS" ] && echo "Focus areas: $FOCUS_AREAS")
</context>

<discovery_agent-guidelines>
Focus on directories containing the changed files. Include git diffs for the commits.
</discovery_agent-guidelines>
EOF
```

### Phase 3: Atomic Setup and Execute Review

Use `setup-review` with builder review mode:

```bash
# Run builder review mode
eval "$($FLOWCTL rp setup-review \
  --repo-root "$REPO_ROOT" \
  --summary "$(cat /tmp/review-instructions.txt)")"

# Verify we have W and T
if [[ -z "${W:-}" || -z "${T:-}" ]]; then
  echo "Error: setup-review failed. Ensure RepoPrompt is running."
  exit 1
fi

echo "Setup complete: W=$W T=$T"
```

### Phase 4: Augment Selection and Send Review

Add changed files to selection:
```bash
# Add all changed files
for f in $CHANGED_FILES; do
  [[ -f "$f" ]] && $FLOWCTL rp select-add --window "$W" --tab "$T" "$f"
done

# Add task spec if available
if [[ -n "$TASK_ID" ]]; then
  task_spec=".flow/tasks/${TASK_ID}.md"
  [[ -f "$task_spec" ]] && $FLOWCTL rp select-add --window "$W" --tab "$T" "$task_spec"
fi
```

Build and send review prompt:
```bash
cat > /tmp/review-prompt.md << 'EOF'
## Implementation Review Request

I need you to review the code changes on this branch.

## IMPORTANT: File Contents
RepoPrompt includes the actual source code of selected files in a `<file_contents>` XML section at the end of this message. You MUST:
1. Locate the `<file_contents>` section
2. Read and analyze the actual source code within it
3. Base your review on the code, not summaries or descriptions

If you cannot find `<file_contents>`, ask for the files to be re-attached before proceeding.

## Review Criteria

Conduct a John Carmack-level review:

1. **Correctness** - Logic errors, spec compliance
2. **Simplicity** - Over-engineering, unnecessary complexity
3. **Edge cases** - Failure modes, boundary conditions
4. **Security** - Injection, auth gaps
5. **Performance** - Hot paths, resource usage
6. **Maintainability** - Readability, documentation

**Only flag issues in the changed code - not pre-existing patterns.**

## Output Format

For each issue:
- **Severity**: Critical / Major / Minor / Nitpick
- **Location**: File and line (e.g., "src/auth.ts:42")
- **Problem**: What's wrong
- **Suggestion**: How to fix

**REQUIRED**: You MUST end your response with exactly one verdict tag. This is mandatory:
`<verdict>SHIP</verdict>` or `<verdict>NEEDS_WORK</verdict>` or `<verdict>MAJOR_RETHINK</verdict>`

Do NOT skip this tag. The automation depends on it.
EOF

$FLOWCTL rp chat-send --window "$W" --tab "$T" --message-file /tmp/review-prompt.md --new-chat --chat-name "Impl Review: $BRANCH"
```

**WAIT** for response. Takes 1-5+ minutes.

### Phase 5: Extract Verdict

Extract verdict from response. If no verdict tag, ask reviewer to clarify.

---

## Fix Loop

**CRITICAL: Do NOT ask user for confirmation. Automatically fix ALL valid issues and re-review.**

**CRITICAL: You MUST fix the code BEFORE re-reviewing. Never re-review without making changes.**

**MAX ITERATIONS**: Limit fix+re-review cycles to 3 iterations. If still NEEDS_WORK after max rounds, inform user and stop.

If verdict is NEEDS_WORK:

1. **Parse issues** - Extract ALL issues by severity (Critical -> Major -> Minor)

2. **Fix the code** - Address each issue in order

3. **Run tests/lints** - Verify fixes don't break anything

4. **Commit fixes** (MANDATORY before re-review):
   ```bash
   git add -A
   git commit -m "fix: address review feedback"
   ```
   **If you skip this and re-review without committing changes, reviewer will return NEEDS_WORK again.**

5. **Request re-review** (only AFTER step 4):

   ```bash
   cat > /tmp/re-review.md << 'EOF'
   Issues addressed. Please re-review.

   **REQUIRED**: End with `<verdict>SHIP</verdict>` or `<verdict>NEEDS_WORK</verdict>` or `<verdict>MAJOR_RETHINK</verdict>`
   EOF

   $FLOWCTL rp chat-send --window "$W" --tab "$T" --message-file /tmp/re-review.md
   ```

6. **Repeat** until SHIP

**Note**: RP auto-refreshes file contents on every message. No need to re-add files to selection.

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
- **Missing changed files** - Add ALL changed files to selection
- **Re-reviewing without committing** - Wastes reviewer time and loops forever
