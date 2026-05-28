---
name: ralph-invoke
description: Allows Claude to directly start Ralph-Wiggum autonomous loops without user commands. Use when user asks to "start a ralph loop", "run ralph", wants autonomous iteration, says "keep working until done", or when a complex task would benefit from multiple iterations.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
  - Task
---

# Ralph Invoke Skill

**Allows Claude to directly start Ralph-Wiggum autonomous loops without user commands.**

## CRITICAL: Interactive Planning Phase

**BEFORE starting any Ralph loop, you MUST complete the planning phase:**

### Step 1: Research the Codebase

Use Glob, Grep, Read, and Task (with Explore agent) to understand:
- Relevant files and structure
- Existing patterns and conventions
- Dependencies and constraints
- Potential challenges

### Step 2: Design a Plan

Create a clear plan with:
- Specific steps to complete the task
- Files that will be modified
- Success criteria
- Potential risks or blockers

### Step 3: Ask Clarifying Questions

Use `AskUserQuestion` to clarify:
- Ambiguous requirements
- Technical approach choices
- Scope boundaries
- Priority of sub-tasks

**Ask at least 2-3 questions** even if the task seems clear. Users appreciate being consulted.

### Step 4: Ask Yolo vs Review Mode

**ALWAYS ask this question before starting:**

```
AskUserQuestion:
  question: "How much autonomy should Ralph have?"
  header: "Mode"
  options:
    - label: "Yolo Mode (Recommended)"
      description: "Ralph works autonomously, only stops at completion or max iterations"
    - label: "Review Mode"
      description: "Ralph asks you questions at decision points throughout the task"
```

### Step 5: Ask Context Type (Fresh vs Persistent)

**ALWAYS ask this to prevent context pollution in long tasks:**

```
AskUserQuestion:
  question: "Should each iteration start with a fresh context?"
  header: "Context Type"
  options:
    - label: "Persistent Context (Standard)"
      description: "Fastest, keeps history in one session. Good for small/medium tasks."
    - label: "Fresh Context (Recommended for long tasks)"
      description: "Starts a NEW session per iteration. Prevents history-based confusion."
```

### Step 6: Confirm and Start

Summarize the plan and get final confirmation before invoking the loop.

---

## Example Planning Flow

**User says:** "Start a ralph loop to add user authentication"

**Claude does:**

1. **Research** (uses Task/Explore agent):
   - Finds existing auth patterns in codebase
   - Identifies relevant files (routes, middleware, models)
   - Notes existing session/token handling

2. **Presents plan:**
   > Here's my plan for adding authentication:
   > 1. Create User model with password hashing
   > 2. Add login/register API endpoints
   > 3. Create JWT middleware for protected routes
   > 4. Update existing routes to use auth middleware

3. **Asks clarifying questions:**
   ```
   AskUserQuestion:
     questions:
       - question: "What authentication method should we use?"
         header: "Auth Type"
         options:
           - label: "JWT tokens (Recommended)"
             description: "Stateless, good for APIs"
           - label: "Session cookies"
             description: "Traditional, requires session store"
       - question: "Should we add OAuth providers (Google, GitHub)?"
         header: "OAuth"
         options:
           - label: "No, just email/password"
             description: "Simple auth only"
           - label: "Yes, add OAuth"
             description: "Social login support"
   ```

4. **Asks mode:**
   ```
   AskUserQuestion:
     question: "How much autonomy should Ralph have?"
     header: "Mode"
     options:
       - label: "Yolo Mode"
         description: "Works autonomously until done"
       - label: "Review Mode"
         description: "Asks questions at decision points"
   ```

5. **Asks context type:**
   ```
   AskUserQuestion:
     question: "Should each iteration start with a fresh context?"
     header: "Context Type"
     options:
       - label: "Persistent Context"
         description: "Keeps history in one session"
       - label: "Fresh Context"
         description: "New session per iteration"
   ```

6. **Confirms and starts:**
   > Great! Starting Ralph with:
   > - JWT authentication
   > - Email/password only (no OAuth)
   > - Yolo mode, 50 max iterations
   > - Fresh context (New session per iteration)
   > - Completion promise: "AUTH_COMPLETE"

---

## Prerequisites

The Ralph loop scripts are included in the `skills/ralph-loop/` folder (forked from the plugin for persistence).

### Verify scripts are available:
```bash
ls "$HOME/.claude/skills/ralph-loop/scripts/setup-ralph-loop.sh" 2>/dev/null && echo "PERSISTENT_READY"
ls "$HOME/.claude/skills/ralph-loop/scripts/setup-fresh-loop.sh" 2>/dev/null && echo "FRESH_READY"
```

If NOT_FOUND, the skills folder may not be properly mounted.

## Triggers

Use this skill when:
- User asks to "start a ralph loop" or "run ralph"
- User wants autonomous iteration on a task
- User says "keep working until done" or "iterate until complete"
- A complex task would benefit from multiple iterations
- User explicitly requests Claude to invoke ralph

**Remember: Always complete the Interactive Planning Phase first!**

## How to Start a Ralph Loop

### Option A: Persistent Context (In-Session) - RECOMMENDED FOR MOST TASKS

Use this when you want quick iteration in the current session:

```bash
"$HOME/.claude/skills/ralph-loop/scripts/setup-ralph-loop.sh" \
  "<TASK_DESCRIPTION>" \
  --task-id "<UNIQUE_ID>" \
  --max-iterations <N> \
  --completion-promise "<PROMISE_TEXT>" \
  --mode <yolo|review>
```

### Option B: Fresh Context via `ralph` Command - FOR LONG/COMPLEX TASKS

**IMPORTANT**: Fresh context loops cannot be started from within a Claude session (Claude blocks concurrent instances). Instead, Claude prepares a spec file and the USER runs the `ralph` command in a separate terminal.

**Step 1: Claude creates the spec file**

```bash
mkdir -p .claude
cat > .claude/ralph-spec-<TASK_ID>.md << 'EOF'
---
max_iterations: 50
completion_promise: "TASK_COMPLETE"
mode: yolo
---

<FULL TASK DESCRIPTION HERE>

Include:
- What needs to be done
- Success criteria
- File paths involved
- Any constraints
EOF
```

**Step 2: Claude tells user to run the command**

Output this message to the user:
```
📋 Ralph spec prepared! To start the fresh context loop, run this in a NEW terminal:

    cd /path/to/project && ralph <TASK_ID>

This will start an interactive Claude session that loops until completion.
```

**Step 3: User runs `ralph <task-id>` in external terminal**

The `ralph` command:
1. Reads the spec file (.claude/ralph-spec-{task-id}.md)
2. Creates a logs directory (.claude/ralph-logs-{task-id}/)
3. Runs Claude in print mode (`claude -p`) for each iteration
4. Checks for completion promise in output between iterations

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| TASK_DESCRIPTION | Yes | - | The task to work on |
| --task-id | **REQUIRED** | - | Descriptive ID (e.g., "polymarket-alpha", "auth-refactor") |
| --max-iterations | Recommended | unlimited | Safety limit (use 20-100) |
| --completion-promise | Recommended | null | Text to output when truly done |
| --mode | Optional | yolo | `yolo` = autonomous, `review` = ask questions |

**IMPORTANT:** Always provide a descriptive `--task-id`. Never omit it or use generic names like "default" or "task". Use project/feature specific names like "polymarket-alpha", "trading-bot", "zone-completion".

### Example Invocations

**Simple task:**
```bash
"$HOME/.claude/skills/ralph-loop/scripts/setup-ralph-loop.sh" \
  "Fix all TypeScript type errors" \
  --task-id "type-fixes" \
  --max-iterations 50 \
  --completion-promise "ALL_ERRORS_FIXED"
```

**Complex refactor:**
```bash
"$HOME/.claude/skills/ralph-loop/scripts/setup-ralph-loop.sh" \
  "Migrate all API handlers to the new v2 pattern" \
  --task-id "api-migration" \
  --max-iterations 100 \
  --completion-promise "MIGRATION_COMPLETE"
```

**With review mode (asks questions):**
```bash
"$HOME/.claude/skills/ralph-loop/scripts/setup-ralph-loop.sh" \
  "Refactor auth system" \
  --task-id "auth-refactor" \
  --max-iterations 50 \
  --completion-promise "AUTH_COMPLETE" \
  --mode review
```

## Concurrent Loops (Multi-Ralph)

**Run multiple Ralph loops in parallel** using different `--task-id` values:

```bash
# Terminal 1: Trading system
/ralph-loop --task-id trading "Build trading system" --max-iterations 50

# Terminal 2: Zone completion
/ralph-loop --task-id zones "Complete zone design" --max-iterations 50

# Terminal 3: Bug fixes
/ralph-loop --task-id bugfix "Fix auth bugs" --max-iterations 30
```

Each loop:
- Has its own state file: `.claude/ralph-loop-{task-id}.local.md`
- Binds to the first Claude session that claims it
- Runs independently without interfering with other loops

### List Active Loops
```bash
ls .claude/ralph-loop-*.local.md 2>/dev/null
```

### Monitor Specific Loop
```bash
head -15 .claude/ralph-loop-{task-id}.local.md
```

### Cancel Specific Loop
```bash
rm .claude/ralph-loop-{task-id}.local.md
```

## Fresh Context Loops (Out-of-Session)

For tasks where you want **truly fresh context** (new Claude session per iteration), use the `ralph` command. This MUST be run from an external terminal, not from within Claude.

### When to use Fresh Context:
- Avoiding history-based hallucinations
- Large tasks where context window fills up
- Resetting the "mental state" of the agent at each step
- Long-running tasks (>20 iterations)

### How to Set Up (Claude prepares, User executes):

**Claude creates the spec:**
```bash
cat > .claude/ralph-spec-myfeature.md << 'EOF'
---
max_iterations: 50
completion_promise: "FEATURE_COMPLETE"
mode: yolo
---

Implement the new feature...
(full task description)
EOF
```

**Claude tells user:**
```
To start the fresh loop, run in a NEW terminal:
    cd ~/projects/myproject && ralph myfeature
```

**User runs externally** - this spawns fresh Claude sessions in a loop, checking for completion between iterations.

---

## Fresh Context Spec Best Practices (CRITICAL)

When writing specs for fresh context loops, follow these rules to prevent premature loop termination:

### 1. NEVER Include Promise Text in Spec Body

The `ralph` script echoes the spec to Claude, then checks the output for the promise. If the promise text appears in the spec body, it gets detected immediately and the loop exits after one iteration.

**BAD** - Promise visible in spec (loop exits after 1 iteration):
```markdown
When done, output: TASK_COMPLETE
```

**GOOD** - Promise only in frontmatter, referenced indirectly:
```markdown
---
completion_promise: "TASK_COMPLETE_XYZ123"
---

When all conditions are met, output the completion promise on its own line.
```

### 2. Frame Spec as Single Iteration

Fresh loops spawn a NEW Claude for each iteration. The spec should be written as if each Claude is doing ONE iteration of work:

**BAD** - Implies continuous work:
```markdown
Keep iterating until all tests pass...
```

**GOOD** - Frames as single iteration:
```markdown
You are running ONE iteration of this task.
After your work, the loop will spawn a NEW Claude to continue.
Just do this iteration's work and end your response normally.
```

### 3. Require Audit Before Promise Output

The Claude should verify completion before outputting the promise:

```markdown
## CRITICAL: When to Output the Completion Promise

ONLY output the promise if ALL of these are true:
1. [Specific condition 1]
2. [Specific condition 2]
3. All changes committed and pushed

If ANY condition is NOT met, do NOT output the promise.
Just end your response normally and let the next iteration continue.

## AUDIT CHECKLIST (Required before promise)

Before outputting the promise, run these verification commands:
1. Verify condition 1: `command`
2. Verify condition 2: `command`
3. Verify git status: `git status`

Only AFTER completing this audit AND confirming all conditions, output the promise.
```

### 4. Make Stop Conditions Explicit

Be crystal clear about when the loop should stop:

```markdown
## When to Stop (Output Promise)

ONLY stop if:
- System is paused, OR
- Budget is exhausted, OR
- All tasks are genuinely complete

If budget available and work remains, let the loop continue naturally.
```

### 5. Use Unique Promise Strings

Avoid common words that might appear in normal output:

**BAD**: `DONE`, `COMPLETE`, `FINISHED`
**GOOD**: `TASK_XYZ_AUDIT_COMPLETE_ALL_DONE`, `AUTH_REFACTOR_VERIFIED_COMPLETE`

### Example: Well-Structured Fresh Context Spec

```markdown
---
max_iterations: 100
completion_promise: "MYPROJECT_AUDIT_COMPLETE_ALL_DONE"
mode: yolo
---

# MyProject Autonomous Loop

You are running ONE iteration of the MyProject system.

This is a CONTINUOUS LOOP with fresh Claude sessions. After you complete
your work, the loop will spawn a NEW Claude to continue. You do NOT need
to stop - just do your iteration's work.

## Your Iteration Tasks

1. Check system status
2. Do the work
3. Commit and push progress

## CRITICAL: When to Output the Completion Promise

ONLY output the completion promise if ALL of these are true:

1. System status shows Paused: YES OR budget exhausted
2. All work is complete
3. All changes committed and pushed

If ANY of the above are NOT met, do NOT output the promise.
Just end your response normally.

## AUDIT CHECKLIST (Required before promise)

If system should stop, perform this audit:
1. Verify status: `command`
2. Verify git clean: `git status`
3. Verify pushed: `git log origin/master -1`

Only AFTER completing this audit, output the promise text on its own line.
```

---

## How the Loops Work

### Persistent Context (`/ralph-loop`)

1. **Claude runs the setup script** → Creates state file at `.claude/ralph-loop-{task-id}.local.md`
2. **Claude works on the task** → Normal operation
3. **Claude tries to exit** → Stop hook intercepts
4. **Hook re-injects prompt** → Claude continues with same task
5. **Repeat** until max iterations or completion promise

### Fresh Context (`ralph` command)

1. **User runs `ralph <task-id>`** → Reads spec file
2. **Script spawns `claude -p`** → Fresh Claude session for iteration
3. **Claude outputs response** → Script captures and logs it
4. **Script checks for promise** → If found, loop ends
5. **Repeat** until max iterations or completion promise

## Completing the Loop

When the task is genuinely complete, output the completion promise in XML tags:

```
<promise>ALL_ERRORS_FIXED</promise>
```

**CRITICAL RULES:**
- Only output the promise when the statement is TRUE
- Do NOT lie to exit the loop
- Do NOT output false promises even if stuck
- Trust the process - if stuck, iterate and try differently

---

## Steering Questions (User Guidance)

When the Ralph sub-agent needs clarification, guidance, or approval before proceeding, it can surface questions to the user through the **steering file**.

**IMPORTANT: All steering/progress/summary files are task-id specific to support multi-ralph:**
- `.claude/ralph-steering-{task-id}.md`
- `.claude/ralph-progress-{task-id}.md`
- `.claude/ralph-summary-{task-id}.md`

### How Steering Works

1. **Ralph writes a question** → Creates/updates `.claude/ralph-steering-{task-id}.md`
2. **Orchestrator monitors** → Reads steering file between iterations
3. **Orchestrator relays** → Shows questions to user
4. **User responds** → Orchestrator writes response to steering file
5. **Ralph reads response** → Continues with guidance

### Steering File Format

```markdown
---
status: pending | answered
iteration: <N>
timestamp: <ISO8601>
---

## Question

<The question Ralph needs answered>

## Context

<Why this matters for the task>

## Options (if applicable)

1. Option A - description
2. Option B - description

---

## Response

<User's answer goes here - filled in by orchestrator>
```

### For the Ralph Sub-Agent

When you need user input, write to the steering file (replace `{task-id}` with your actual task ID):

```bash
# Example for task-id "trading"
cat > .claude/ralph-steering-trading.md << 'EOF'
---
status: pending
iteration: 5
timestamp: 2025-01-08T12:00:00Z
---

## Question

Should I use Redis or PostgreSQL for the session store?

## Context

Both would work but have different tradeoffs. Redis is faster but PostgreSQL keeps everything in one place.

## Options

1. Redis - faster, ephemeral by nature
2. PostgreSQL - simpler ops, already in stack

---

## Response

EOF
```

Then **continue working on other aspects** of the task. Check for responses at the start of each iteration:

```bash
# Replace TASK_ID with your actual task ID (e.g., "trading")
TASK_ID="trading"
STEERING_FILE=".claude/ralph-steering-${TASK_ID}.md"

if [[ -f "$STEERING_FILE" ]]; then
  STATUS=$(grep '^status:' "$STEERING_FILE" | sed 's/status: *//')
  if [[ "$STATUS" == "answered" ]]; then
    # Read the response and incorporate it
    RESPONSE=$(sed -n '/^## Response/,$ p' "$STEERING_FILE" | tail -n +2)
    echo "User responded: $RESPONSE"
    # Clear the steering file after reading
    rm "$STEERING_FILE"
  fi
fi
```

### For the Orchestrating Claude

When monitoring a Ralph loop, check for steering questions:

```bash
TASK_ID="trading"  # The task you're monitoring
STEERING_FILE=".claude/ralph-steering-${TASK_ID}.md"

# Check for pending questions
if [[ -f "$STEERING_FILE" ]]; then
  STATUS=$(grep '^status:' "$STEERING_FILE" | sed 's/status: *//')
  if [[ "$STATUS" == "pending" ]]; then
    echo "⚠️ Ralph [$TASK_ID] has a steering question:"
    cat "$STEERING_FILE"
  fi
fi
```

When you receive a response from the user, update the file:

```bash
TASK_ID="trading"
STEERING_FILE=".claude/ralph-steering-${TASK_ID}.md"

# Add user response to steering file
sed -i 's/^status: pending/status: answered/' "$STEERING_FILE"
cat >> "$STEERING_FILE" << 'EOF'

Use PostgreSQL - we want to minimize infrastructure complexity.
EOF
```

### Steering Best Practices

1. **Non-blocking questions** - Ralph should continue on other work while waiting
2. **Clear options** - Provide 2-3 concrete choices when possible
3. **Context matters** - Explain why you need this decision
4. **One question at a time** - Don't overwhelm with multiple steering questions
5. **Check early** - Check for steering responses at the start of each iteration

### Example: Orchestrated Ralph with Steering

```bash
# Orchestrator script (conceptual) - monitors a specific task
TASK_ID="trading"
STATE_FILE=".claude/ralph-loop-${TASK_ID}.local.md"
STEERING_FILE=".claude/ralph-steering-${TASK_ID}.md"

while true; do
  # Check for steering questions
  if [[ -f "$STEERING_FILE" ]]; then
    STATUS=$(grep '^status:' "$STEERING_FILE" | sed 's/status: *//')
    if [[ "$STATUS" == "pending" ]]; then
      QUESTION=$(sed -n '/^## Question/,/^## Context/ p' "$STEERING_FILE" | head -n -1 | tail -n +2)
      echo "🔔 Ralph [$TASK_ID] asks: $QUESTION"
      read -p "Your response: " USER_RESPONSE
      sed -i 's/^status: pending/status: answered/' "$STEERING_FILE"
      echo -e "\n$USER_RESPONSE" >> "$STEERING_FILE"
    fi
  fi

  # Check Ralph loop status
  if [[ ! -f "$STATE_FILE" ]]; then
    echo "Ralph [$TASK_ID] loop complete!"
    break
  fi

  sleep 5
done
```

---

## Progress Reporting & Milestone Commits

Ralph should commit progress at meaningful milestones and report status for the orchestrator to relay.

### Progress File Format

Write progress updates to `.claude/ralph-progress-{task-id}.md`:

```markdown
---
iteration: <N>
timestamp: <ISO8601>
---

## Milestone: <short title>

### Completed
- Item 1
- Item 2

### Files Changed
- path/to/file1.ts
- path/to/file2.ts

### Next Steps
- What's coming next

### Blockers (if any)
- Issues that may need user input
```

### When to Commit Progress

Commit at natural milestones:

```bash
# After completing a logical unit of work
TASK_ID="trading"  # Your task ID
ITERATION=$(grep '^iteration:' ".claude/ralph-loop-${TASK_ID}.local.md" | sed 's/iteration: *//')

git add -A && git commit -m "$(cat <<EOF
[Ralph ${TASK_ID} #${ITERATION}] Milestone: <title>

- What was done
- Key changes
EOF
)"
```

**Commit prefix format:** `[Ralph {task-id} #N]` - includes task ID and iteration number.

**Commit triggers:**
- Completed a feature/component
- Fixed a bug and verified
- Finished refactoring a module
- Tests passing after changes
- Before asking a steering question

### Progress Reporting Pattern

At the end of each iteration (or after milestones), update progress:

```bash
TASK_ID="trading"  # Your task ID
STATE_FILE=".claude/ralph-loop-${TASK_ID}.local.md"
PROGRESS_FILE=".claude/ralph-progress-${TASK_ID}.md"

ITERATION=$(grep '^iteration:' "$STATE_FILE" | sed 's/iteration: *//')
cat > "$PROGRESS_FILE" << EOF
---
iteration: $ITERATION
timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)
---

## Milestone: Completed auth refactor

### Completed
- Migrated session handling to JWT
- Updated all protected routes
- Added refresh token logic

### Files Changed
- src/auth/session.ts
- src/middleware/auth.ts
- src/routes/protected/*.ts

### Next Steps
- Add rate limiting
- Update tests

### Blockers
- None currently
EOF
```

### For the Orchestrating Claude

Monitor progress and relay to user:

```bash
TASK_ID="trading"  # The task you're monitoring
PROGRESS_FILE=".claude/ralph-progress-${TASK_ID}.md"

# Check for progress updates
if [[ -f "$PROGRESS_FILE" ]]; then
  TIMESTAMP=$(grep '^timestamp:' "$PROGRESS_FILE" | sed 's/timestamp: *//')
  echo "📊 Ralph [$TASK_ID] progress update ($TIMESTAMP):"
  cat "$PROGRESS_FILE"
fi

# Check git log for milestone commits
git log --oneline -5 --grep='\[Ralph\]' 2>/dev/null
```

### Example: Full Orchestrator Loop

```bash
#!/bin/bash
# Orchestrator that monitors a specific Ralph loop and relays to user

TASK_ID="${1:-trading}"  # Pass task ID as argument, default "trading"
STATE_FILE=".claude/ralph-loop-${TASK_ID}.local.md"
PROGRESS_FILE=".claude/ralph-progress-${TASK_ID}.md"
STEERING_FILE=".claude/ralph-steering-${TASK_ID}.md"

echo "Monitoring Ralph loop: $TASK_ID"
LAST_PROGRESS=""

while [[ -f "$STATE_FILE" ]]; do
  # Check for new progress
  if [[ -f "$PROGRESS_FILE" ]]; then
    CURRENT=$(cat "$PROGRESS_FILE")
    if [[ "$CURRENT" != "$LAST_PROGRESS" ]]; then
      echo ""
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      echo "📊 RALPH [$TASK_ID] PROGRESS UPDATE"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      cat "$PROGRESS_FILE"
      LAST_PROGRESS="$CURRENT"
    fi
  fi

  # Check for steering questions
  if [[ -f "$STEERING_FILE" ]]; then
    STATUS=$(grep '^status:' "$STEERING_FILE" | sed 's/status: *//')
    if [[ "$STATUS" == "pending" ]]; then
      echo ""
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      echo "❓ RALPH [$TASK_ID] NEEDS YOUR INPUT"
      echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
      # Extract and show question
      sed -n '/^## Question/,/^## Context/p' "$STEERING_FILE" | head -n -1
      sed -n '/^## Options/,/^---/p' "$STEERING_FILE" | head -n -1
      echo ""
      read -p "Your response: " USER_RESPONSE
      # Write response
      sed -i 's/^status: pending/status: answered/' "$STEERING_FILE"
      echo -e "\n$USER_RESPONSE" >> "$STEERING_FILE"
      echo "✅ Response recorded"
    fi
  fi

  sleep 3
done

echo ""
echo "✅ Ralph [$TASK_ID] loop complete!"
echo ""
echo "Recent commits:"
git log --oneline -10 --grep='\[Ralph\]'
```

### Summary Files

At completion, Ralph should create `.claude/ralph-summary-{task-id}.md`:

```markdown
---
task: <original task>
iterations: <total>
duration: <start to end>
status: complete | max_iterations | error
---

## Summary

Brief description of what was accomplished.

## Key Changes
- Major change 1
- Major change 2

## Files Modified
- file1.ts - description
- file2.ts - description

## Commits
- abc123 - Milestone: X
- def456 - Milestone: Y

## Notes for User
Any important follow-up items or things to review.
```

---

## Canceling a Loop

If needed, cancel with:
```bash
rm .claude/ralph-loop-{task-id}.local.md
```

Replace `{task-id}` with your actual task ID (e.g., `rm .claude/ralph-loop-polymarket-alpha.local.md`).

## Best Practices

1. **Always use descriptive --task-id** - Use project names like "polymarket-alpha", never "default"
2. **Always set --max-iterations** - Prevents runaway costs (50-100 is reasonable)
3. **Use specific completion promises** - "ALL_TESTS_PASS" not "DONE"
4. **Include success criteria in task** - Be explicit about what "done" means
5. **Monitor progress** - `head -10 .claude/ralph-loop-{task-id}.local.md`
6. **Start small** - Test with 3-5 iterations first
7. **Use steering for decisions** - Don't guess on ambiguous requirements
8. **Commit at milestones** - Use `[Ralph {task-id} #N]` prefix for tracking
9. **Update progress file** - Keep orchestrator informed via `.claude/ralph-progress-{task-id}.md`
10. **Create summary on completion** - Write `.claude/ralph-summary-{task-id}.md` when done

## Cost Warning

Autonomous loops consume tokens rapidly. A 50-iteration loop can cost $50-100+ in API usage. Always use --max-iterations as a safety net.

## Why This Skill Exists

The official ralph-wiggum plugin requires users to run `/ralph-loop` commands. This skill enables Claude to invoke loops directly, enabling:
- Claude-initiated iteration on complex tasks
- Programmatic loop triggers from other skills/agents
- Automated workflows without manual commands
- **User steering** for guidance on ambiguous decisions
