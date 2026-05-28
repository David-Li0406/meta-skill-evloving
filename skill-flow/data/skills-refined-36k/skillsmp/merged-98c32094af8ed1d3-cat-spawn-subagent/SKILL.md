---
name: cat:spawn-subagent
description: Launch a subagent with task context in an isolated worktree with token tracking.
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

### Mandatory Subagent Prompt Checklist

**CRITICAL: Cross-reference recent learnings before spawning.**

Every subagent prompt MUST include these items based on past mistakes:

**STATE.md Requirements:**
```
STATE.md UPDATE (required in SAME commit as implementation):
- Path: .claude/cat/v{major}/v{major}.{minor}/{task-name}/STATE.md
- Set: Status: completed
- Set: Progress: 100%
- Set: Resolution: implemented (MANDATORY - not optional)
- Set: Completed: {YYYY-MM-DD HH:MM}
- Set: Tokens Used: {tokensUsed from .completion.json}
- Include STATE.md in git add before commit
```

**Token Tracking Requirements:**

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

If compaction occurred, the pre-compaction tokens are NOT lost - they must be preserved and added to post-compaction usage for accurate reporting.

**Context Limit Enforcement:**

**MANDATORY: Validate task size BEFORE spawning subagent.**

```bash
# Values from agent-architecture.md § Context Limit Constants
CONTEXT_LIMIT=...
HARD_LIMIT_PCT=...
SOFT_TARGET_PCT=...
SOFT_TARGET=$((CONTEXT_LIMIT * SOFT_TARGET_PCT / 100))
HARD_LIMIT=$((CONTEXT_LIMIT * HARD_LIMIT_PCT / 100))
```

**Limit Hierarchy:**

| Limit | Percentage | Tokens (200K) | Purpose |
|-------|------------|---------------|---------|
| Soft target | 40% | 80,000 | Recommended task size for optimal quality |
| Hard limit | 80% | 160,000 | Maximum allowed - MANDATORY decomposition above this |
| Context limit | 100% | 200,000 | Absolute ceiling - compaction occurs |

**Pre-Spawn Validation Requirement:**

BEFORE spawning ANY subagent, the main agent MUST:

1. Calculate estimated tokens for the task (from analyze_task_size)
2. Use fixed HARD_LIMIT: 160,000 tokens (80% of 200K)
3. Compare estimate against hard limit:
   - If estimate >= HARD_LIMIT: **MANDATORY decomposition** (do NOT spawn)
   - If estimate > soft target but < hard limit: Recommend decomposition (optional)
   - If estimate <= soft target: Proceed with spawn

```bash
# Pre-spawn validation
# Values from agent-architecture.md § Context Limit Constants
CONTEXT_LIMIT=...
HARD_LIMIT_PCT=...
HARD_LIMIT=$((CONTEXT_LIMIT * HARD_LIMIT_PCT / 100))
SOFT_TARGET=$((CONTEXT_LIMIT * 40 / 100))

if [ "${ESTIMATED_TOKENS}" -ge "${HARD_LIMIT}" ]; then
  echo "ERROR: Task estimate (${ESTIMATED_TOKENS}) exceeds hard limit (${HARD_LIMIT})"
  echo "MANDATORY: Decompose task before spawning. Use /cat:decompose-task"
  exit 1
fi
```

**Post-Execution Limit Check:**

After subagent completes, verify actual usage:

```bash
ACTUAL_TOKENS={from .completion.json}
if [ "${ACTUAL_TOKENS}" -ge "${HARD_LIMIT}" ]; then
  echo "EXCEEDED: Subagent used ${ACTUAL_TOKENS} tokens (hard limit: ${HARD_LIMIT})"
  # Trigger learn-from-mistakes with A018 reference
fi
```

## Verification

Before invoking Task tool, confirm:

| Checklist Item | Required For |
|----------------|--------------|
| STATE.md path specified | All implementation tasks |
| Resolution field mentioned | All implementation tasks |
| CRITICAL PROHIBITIONS block | All tasks |
| Exact code examples | Non-trivial changes |
| Fail-fast conditions | All tasks |
| **Session ID in prompt** | All tasks |
| Token measurement instructions | All tasks |
| **Pre-spawn limit validation** | All tasks |

**Anti-pattern:** Spawning subagent without reviewing this checklist against your prompt.

## Examples

### Basic Spawn

```bash
# Parent agent: First create worktree
TASK="1.2-implement-parser"
UUID="a1b2c3d4"
WORKTREE=".worktrees/${TASK}-sub-${UUID}"

git worktree add -b "${TASK}-sub-${UUID}" "${WORKTREE}" HEAD
```

Then use the Task tool to launch the subagent:

```
Task tool invocation:
  description: "Execute parser task"
  subagent_type: "general-purpose"
  model: "haiku"
  prompt: |
    Execute task 1.2 PLAN.md.

    WORKING DIRECTORY: .worktrees/1.2-implement-parser-sub-a1b2c3d4

    VERIFICATION:
    1. Run tests
    2. Run style checks

    ON COMPLETION: Report summary.
```

### Spawn for Complex Implementation

```
Task tool invocation:
  description: "Implement feature X"
  subagent_type: "general-purpose"
  model: "haiku"
  prompt: |
    Implement feature X following PLAN.md.

    WORKING DIRECTORY: ${WORKTREE_PATH}

    CRITICAL REQUIREMENTS:
    - Decompose code instead of adding PMD suppression annotations
    - Include tests in SAME commit as implementation

    EXACT CHANGES:
    1. Create src/Feature.java with: [code listing]
    2. Create test/FeatureTest.java with: [test code]

    VERIFICATION:
    1. ./mvnw test -Dtest=FeatureTest
    2. ./mvnw checkstyle:check pmd:check

    FAIL-FAST: If any check fails, report BLOCKED

    COMMIT: git commit -m "feature: add X"
```

## Anti-Patterns

### Main agent makes all decisions before spawning

```
# ❌ WRONG - Requires subagent to make decisions
Task prompt: "Implement error handling for the parser. Choose appropriate exception types."

# ✅ CORRECT - All decisions made by main agent
Task prompt: |
  Add error handling to Parser.java:
  - Line 45: wrap in try-catch, throw ParseException("Invalid token at position " + pos)
  - Line 72: add null check, throw IllegalArgumentException("Input cannot be null")
  - All exceptions must include position information for debugging
```

### Always provide concrete PLAN.md reference

```
# ❌ WRONG - Vague instructions
Task prompt: "Work on the parser"

# ✅ CORRECT - Concrete plan reference
Task prompt: |
  Execute PLAN.md at .claude/cat/tasks/1.2-implement-parser/PLAN.md.
  WORKING DIRECTORY: .worktrees/1.2-implement-parser-sub-a1b2c3d4
```

### Provide explicit code examples for required changes

When specific API usage or patterns are required, provide explicit before/after code examples:

```
# ❌ WRONG - Vague instruction, subagent may find different solution
Task prompt: "Remove the unnecessary cast in LexerTest.java"

# ✅ CORRECT - Explicit code example showing expected change
Task prompt: |
  Change LexerTest.java line 625:
    FROM: requireThat(token.text() == token.decodedText(), "sameInstance").isTrue();
    TO:   requireThat(token.text(), "token.text()").isReferenceEqualTo(token.decodedText(), "token.decodedText()");
```

**Why**: Subagents optimize for passing tests/builds. Without explicit examples, they may find alternative solutions (e.g., @SuppressWarnings) that technically work but don't match the intended approach.

### Require manual derivation of test expected values

For parser/test tasks, include manual derivation requirement in prompt:

```
# ❌ WRONG - Missing test derivation guidance
Task prompt: "Add parser tests for new feature"

# ✅ CORRECT - Explicit manual derivation requirement
Task prompt: |
  Add parser tests for new feature.

  CRITICAL: Test expected values MUST be manually derived:
  1. Analyze source string character by character
  2. Determine expected node types from Java grammar
  3. Use (0, 0) placeholders for positions initially
  4.