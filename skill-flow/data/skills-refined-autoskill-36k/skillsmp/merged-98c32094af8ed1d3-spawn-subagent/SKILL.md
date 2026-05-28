---
name: spawn-subagent
description: Use this skill to launch a subagent with task context in an isolated worktree while tracking token usage.
---

# Spawn Subagent

## Purpose

Launch a Claude Code subagent in an isolated git worktree to execute a specific task. The subagent operates independently with its own context window while the parent agent continues coordinating.

## Critical: Unsupervised Execution

**Subagents run without user supervision.** Claude Code does not provide a way for users to view subagent output while it runs. Users cannot:

- See what the subagent is doing
- Correct mistakes in real-time
- Answer questions or clarify requirements
- Provide feedback during execution

**All decision-making MUST happen in the main agent before spawning.** The subagent prompt must be comprehensive enough that execution is purely mechanical - following explicit instructions without judgment calls.

## Hook Inheritance

**Subagents inherit project hooks automatically** when running in the same project directory. However, subagents may not follow hook guidance if not explicitly reminded.

**MANDATORY: Include key requirements in subagent prompt:**

```
CRITICAL REQUIREMENTS (enforced by hooks):
- Always decompose code instead of adding PMD suppression annotations
- Always use git merge --ff-only for linear history
- Always use git-filter-repo instead of git filter-branch
- Preserve .git/refs/original unless user explicitly requests deletion
- Include tests for bugfixes in the SAME commit as the fix

COMMIT SEPARATION:
- .claude/rules/ updates → separate config: commit (not bundled with bugfix/feature)
- STATE.md updates → same commit as implementation
```

**Why explicit in prompt:** Hooks can block commands, but subagents may try alternatives. Stating prohibitions in the prompt prevents wasted effort on blocked approaches.

## When to Use

- Task has a well-defined PLAN.md ready for execution
- **All ambiguities resolved** - main agent has made all decisions
- Task is independent enough to execute in isolation
- Parent agent needs to continue with other work
- Context window management requires task isolation

## Subagent Types and Two-Stage Planning

**Planning Subagent (two stages for token efficiency):**

| Stage | Purpose | Output | Tokens |
|-------|---------|--------|--------|
| Stage 1 | High-level approach outlines | 3 brief options + agent_id | ~5K |
| Stage 2 | Detailed implementation spec | Full PLAN.md for selected approach | ~20K |

**Stage 1 prompt template:**
```
Analyze the task and produce HIGH-LEVEL outlines (1-2 sentences each) for:
- Conservative approach: [minimal scope, low risk]
- Balanced approach: [moderate scope, medium risk]
- Aggressive approach: [comprehensive, high risk]

Do NOT produce detailed execution steps yet. Keep outlines brief.
Return your agent_id for later resumption.
```

**Stage 2 prompt (using Task tool with `resume` parameter):**
```
resume: {agent_id from Stage 1}
prompt: "User selected [approach]. Now produce the DETAILED spec with:
- Specific files to modify
- Exact code changes
- Step-by-step execution
- Verification commands"
```

**Implementation Subagent:** Receives completed PLAN.md, executes mechanically.

## Concurrent Execution Safety

This skill respects task-level locking. Before spawning, verify the parent agent holds the task lock. The lock should have been acquired by `/cat:work`. Subagents inherit lock ownership through their worktree association (recorded in the lock file).

**MANDATORY: Verify Lock Ownership**

After any lock acquisition attempt, verify ownership by reading the actual lock file:

```bash
TASK_ID="${MAJOR}.${MINOR}-${TASK_NAME}"
LOCK_FILE="${CLAUDE_PROJECT_DIR}/.claude/cat/locks/${TASK_ID}.lock"

# Verify lock file exists and we own it
if [[ ! -f "$LOCK_FILE" ]]; then
  echo "ERROR: Lock file does not exist at $LOCK_FILE"
  echo "Lock was NOT acquired. Another session may own this task."
  exit 1
fi

# Verify session_id matches current session
LOCK_SESSION=$(grep "^session_id=" "$LOCK_FILE" | cut -d= -f2)
if [[ "$LOCK_SESSION" != "$SESSION_ID" ]]; then
  echo "ERROR: Lock owned by different session: $LOCK_SESSION"
  echo "Current session: $SESSION_ID"
  echo "Do NOT proceed - another Claude instance is working on this task."
  exit 1
fi

echo "Lock verified: $LOCK_FILE owned by current session"
```

## Prompt Requirements: Zero Decision Delegation

**MANDATORY**: Before spawning, ensure the prompt contains everything needed for mechanical execution.

### What the Prompt MUST Include

| Element | Why Required |
|---------|--------------|
| Clear task type | "Explore and report" OR "Execute these steps" - never both |
| Fail-fast conditions | When to stop and report BLOCKED |
| Exact file paths | For implementation tasks |
| Specific code changes | Before/after examples, not descriptions |
| Test verification steps | Explicit commands to run, expected outcomes |
| Edge cases to handle | Subagent won't discover these independently |
| Commit message format | Exact text, not guidelines |
| **STATE.md update** | Task STATE.md must be updated to completed IN THE SAME COMMIT |

### Fail-Fast Requirements

**CRITICAL**: Every prompt must include fail-fast conditions.

```bash
# Always include:
FAIL-FAST CONDITIONS:
- If [specific condition], report "BLOCKED: [reason]" and stop
- Report status and return to main agent for decisions
- Main agent handles all workarounds and fallback choices
```

Subagents use fail-fast behavior: report BLOCKED and stop. Fallback decisions require user oversight.

### Main Agent Responsibilities (BEFORE Spawning)

1. **Read all relevant code** - Complete exploration before spawning
2. **Make architectural decisions** - Which pattern, which API, which approach
3. **Resolve ambiguities** - If PLAN.md says "handle errors appropriately", decide HOW
4. **Identify edge cases** - Subagent executes happy path unless told otherwise
5. **Write explicit examples** - Code snippets, not prose descriptions
6. **Specify verification** - Exact test commands and expected output

### Prompt Completeness Checklist

Before spawning, verify your prompt answers:

- [ ] Is this exploration/research OR implementation? (never both)
- [ ] What are the fail-fast conditions? (when to stop and report BLOCKED)
- [ ] What files to create/modify? (exact paths, for implementation)
- [ ] What code to write? (actual code, not descriptions)
- [ ] What tests to run? (exact commands)
- [ ] What does success look like? (specific criteria)
- [ ] What if the build fails? (fail-fast, not recovery)
- [ ] What commit message to use? (exact text, for implementation)
- [ ] **Does prompt include STATE.md update?** (MUST be in same commit as implementation)

### Token Tracking Requirements

**MAIN AGENT MUST include session ID in prompt** - subagents cannot measure tokens without it.

Include this block in EVERY subagent prompt:
```
TOKEN MEASUREMENT (required):
Session ID: {paste actual session ID from your CAT SESSION INSTRUCTIONS}
Session file: /home/node/.config/claude/projects/-workspace/{SESSION_ID}.jsonl

On completion, measure tokens:
TOKENS=$(jq -s '[.[] | select(.type == "assistant") | .message.usage |
  select(. != null) | (.input_tokens + .output_tokens)] | add // 0' "$SESSION_FILE")
```

**Why explicit session ID?** Subagents don't receive CAT SESSION INSTRUCTIONS automatically. Without the session ID, token measurement fails and reports show "NOT MEASURED".

**Token tracking requirements:**
- Track cumulative token usage across the ENTIRE session
- If context compaction occurs, PRESERVE pre-compaction token count
- Write TOTAL tokens (pre-compaction + post-compaction) to .completion.json
- Include: inputTokens, outputTokens, tokensUsed (total), compactionEvents count

**On completion**, write .completion.json with cumulative totals:
```json
{
  "status": "success|partial|failed",
  "tokensUsed": {CUMULATIVE_TOTAL},
  "inputTokens": {CUMULATIVE_INPUT},
  "outputTokens": {CUMULATIVE_OUTPUT},
  "compactionEvents": {COUNT},
  "summary": "..."
}
```

## Workflow

**Progress Output (MANDATORY):**

Display spawning progress using visible feedback symbols:

**At spawn start:**
```
◆ Spawning subagent: {task-id}...
  → Worktree: {worktree-path}
  → Branch: {branch-name}
```

**On successful launch:**
```
✓ Subagent launched: {subagent-id}
  → Session: {session-id}
  → Estimated tokens: {N}K
```

**On failure:**
```
✗ Spawn failed: {error-reason}
  → {specific error details}
```

### Example: Implementation Task (execute plan, no decisions)

**❌ WRONG (requires decisions):**
```
Implement the Parser class following PLAN.md.
Add appropriate error handling.
Write tests for the main functionality.
```

**✅ CORRECT (mechanical execution):**
```
Create src/parser/Parser.java with this implementation:

[Full code listing with all methods]

Create test/parser/ParserTest.java:

[Full test code with expected values]

Verification:
1. Run: ./gradlew test --tests ParserTest
2. Expected: BUILD SUCCESSFUL, 5 tests passed

FAIL-FAST:
- If tests fail, report BLOCKED with failure output
- Do NOT modify code to fix failures - report and stop

Commit:
  message: "feature: add Parser class for token processing"
  files: src/parser/Parser.java, test/parser/ParserTest.java
```

## Related Skills

- `cat:monitor-subagents` - Check status of spawned subagents
- `cat:collect-results` - Gather results when subagent completes
- `cat:merge-subagent` - Merge subagent work back to task branch
- `cat:parallel-execute` - Spawn multiple subagents concurrently