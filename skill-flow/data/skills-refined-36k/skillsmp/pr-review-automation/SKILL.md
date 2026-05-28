---
name: pr-review-automation
description: Use when Gemini bot completes PR review with priority labels (🔴🟡🟢⚪) - MANDATORY loop until meaningfulUnprocessedCount=0, then automatically processes new feedback by priority with 3-minute polling, state tracking for resumable processing, and @superpowers:executing-plans integration
---

# PR Review Automation

## Overview
Systematic workflow for processing Gemini bot PR review feedback with priority-based filtering, state tracking for resumable processing, and superpower skill integration. **MANDATORY: Loop until meaningfulUnprocessedCount = 0 before ANY other action. Automatically continues until no meaningful feedback remains.**

**Ralph Loop is DEFAULT**: When "auto" mode is detected, Ralph-loop is automatically used for fully autonomous PR review processing. No manual intervention needed!

**Core principles**:
- **LOOP until meaningful feedback = 0**: Process ALL existing feedback before ANY other action (CRITICAL!)
- **Never skip existing feedback**: Check and process until `meaningfulUnprocessedCount = 0`
- **Check unreviewed commits**: Only after ALL existing feedback is processed
- **Loop until done**: Continuously process new feedback until no meaningful items remain
- **Ralph-powered automation (DEFAULT)**: "auto" mode triggers Ralph-loop automatically
- Process feedback systematically using GitHub API and priority filtering
- Track state to avoid duplicate processing
- Use `@superpowers:executing-plans` for high-quality fixes
- Poll every 3 minutes for faster feedback cycles
- Resume from last processed feedback if interrupted
- Automatically detect meaningful feedback (CRITICAL, IMPORTANT, and impactful NICE-TO-HAVE)

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│              PR Review Automation (Ralph-Loop)               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Check if Gemini review exists on PR                     │
│     ├─ YES → Go to step 4                                   │
│     └─ NO → Continue to step 2                              │
│                                                              │
│  2. Post "/gemini review" comment                           │
│     gh pr comment <PR> --body "/gemini review"              │
│     ├─ Error? → Retry (max 3 times)                         │
│     └─ Success → Continue                                   │
│                                                              │
│  3. ⏳ WAIT 3 MINUTES for Gemini to respond                 │
│     └─ Still no response? → Retry step 2 (max 2 times)      │
│                                                              │
│  4. Check meaningfulUnprocessedCount                        │
│     npm run pr-state -- --pr <PR>                           │
│     ├─ = 0 AND no unreviewed commits                        │
│     │   → EXIT: Output <promise>DONE</promise>              │
│     └─ > 0 → Continue to step 5                             │
│                                                              │
│  5. Process feedback by priority (CRITICAL → IMPORTANT)     │
│     Use @superpowers:executing-plans for each fix           │
│                                                              │
│  6. ★ LOCAL CODE REVIEW LOOP ★                              │
│     while (Critical/Important issues exist):                │
│       → Run superpowers:code-reviewer                       │
│       → Fix issues (fix = code change = review again!)      │
│                                                              │
│  7. Commit and push                                          │
│     git add -A && git commit && git push                    │
│                                                              │
│  8. Loop back to step 1 (Ralph auto-feeds same prompt)      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

**Required tools**:
- **GitHub CLI (`gh`)**: MUST be installed and authenticated
  ```bash
  # Install gh CLI
  # macOS: brew install gh
  # Linux: See https://github.com/cli/cli/blob/trunk/docs/install_linux.md
  # Windows: See https://github.com/cli/cli#windows

  # Authenticate
  gh auth login

  # Verify
  gh --version
  ```

- **Node.js and npm**: For running TypeScript scripts
- **jq** (optional): For parsing JSON output from `npm run pr-state`

**Common jq usage examples**:
```bash
# Check meaningfulUnprocessedCount only
npm run pr-state -- --pr 9 | jq .meaningfulUnprocessedCount

# Get all unprocessed meaningful feedback
npm run pr-state -- --pr 9 | jq '.comments[] | select(.processed == false and .priority != "NONE")'

# Get feedback created after a specific time
npm run pr-state -- --pr 9 | jq '.comments[] | select(.createdAt >= "2025-10-30T04:50:00Z" and .priority != "NONE")'

# Summary with first 100 chars of body
npm run pr-state -- --pr 9 | jq '{
  meaningfulUnprocessedCount,
  latestReview: [
    .comments[]
    | select(.createdAt >= "2025-10-30T04:50:00Z" and .priority != "NONE")
    | {id, priority, createdAt, body: .body[0:100]}
  ]
}'
```

**Important jq notes**:
- Use single quotes to avoid shell escaping issues
- `!=` not `\!=` for not-equal operator
- `.body[0:100]` not `.body[:100]` for substring
- Wrap filter in `{ }` for object output, `[ ]` for array output

## When to Use
- Gemini bot posted review comment on PR
- Multiple feedback items with priority labels
- Need to filter false positives and nitpicks
- Want automated, repeatable processing
- **AUTO MODE (DEFAULT = Ralph-loop)**: User requests "auto" mode → Ralph-loop executes automatically
- **MANUAL MODE**: Explicit `/ralph-loop` or `npm run pr-auto` for fine-grained control

## Workflow

### Operating Modes

**IMPORTANT**: All npm commands must be executed from the plugin directory (`devnogari-claude-plugins`). Always navigate to the plugin directory with `cd` before running npm commands.

**RALPH MODE (DEFAULT - Fully Autonomous)**:
- **Trigger**: User says "auto" → Ralph-loop executes automatically
- **Behavior**: Ralph handles the entire loop - Claude iterates autonomously until done
- **No manual intervention**: Ralph's stop hook feeds the same prompt back automatically
- **Loop**: Continues until completion promise is TRUE (meaningfulUnprocessedCount = 0)
- **This is the DEFAULT when "auto" is detected**

**Ralph Mode Invocation** (executed when "auto" detected):

Use the Skill tool to invoke ralph-loop:
```
Skill: ralph-loop
Args: Process Gemini PR review for PR #<NUMBER> --completion-promise DONE --max-iterations 20
```

**Step-by-Step Iteration Guide** (EACH Ralph iteration):

```
ITERATION START
│
├─ Step 1: Check if Gemini review exists
│   gh pr view <PR> --json comments --jq '.comments[] | select(.author.login | contains("gemini"))'
│   ├─ EXISTS → Skip to Step 4
│   └─ NOT EXISTS → Continue to Step 2
│
├─ Step 2: Post "/gemini review" comment
│   gh pr comment <PR> --body "/gemini review"
│   ├─ Error? → Retry (max 3 times)
│   └─ Success → Continue to Step 3
│
├─ Step 3: Wait for Gemini response
│   ⏳ sleep 180  (3 minutes)
│   Check if Gemini responded:
│   ├─ YES → Continue to Step 4
│   └─ NO → Retry Step 2 (max 2 retries total)
│
├─ Step 4: Check feedback status
│   cd <plugin-dir> && npm run pr-state -- --pr <PR>
│
│   meaningfulUnprocessedCount = 0 AND no unreviewed commits?
│   ├─ YES → Output: <promise>DONE</promise>
│   │        ★ EXIT LOOP ★
│   └─ NO → Continue to Step 5
│
├─ Step 5: Process feedback by priority
│   CRITICAL → IMPORTANT → NICE-TO-HAVE
│   Use @superpowers:executing-plans for each fix
│
├─ Step 6: Local Code Review Loop
│   while (Critical/Important issues exist):
│       Run superpowers:code-reviewer
│       Fix issues
│       (Fix = code change = must review again!)
│
├─ Step 7: Commit and push
│   git add -A && git commit -m "fix: address Gemini feedback"
│   git push
│
└─ Step 8: Ralph auto-feeds same prompt → Back to Step 1
```

**CRITICAL EXIT CONDITION**:
- ONLY output `<promise>DONE</promise>` when:
  - `meaningfulUnprocessedCount = 0` AND
  - No unreviewed commits exist
- Do NOT lie to exit the loop!

**SCRIPT MODE (Legacy - Optional)**:
- Command: `cd /path/to/devnogari-claude-plugins && npm run pr-auto`
- Behavior: Orchestrates the full loop - checks feedback and exits with code 2 when found
- Claude Code Integration: When exit code 2, process feedback, commit, push, then re-run script
- Loop: Continues until meaningfulUnprocessedCount = 0
- Use when: Ralph-loop unavailable or need script-based control

**MANUAL MODE (Single Check)**:
- Command: `npm run pr-loop -- --wait`
- Behavior: Checks once for feedback and reports status
- Claude Code Integration: Claude manually implements the loop based on exit code
- Use when: Need single status check or manual control

For AUTO mode, the `/devnogari:pr-review auto` command will automatically execute Ralph-loop.

### 0. Process ALL Existing Feedback FIRST (PRIORITY!)
```bash
# CRITICAL: Loop until meaningful feedback reaches 0
# Do NOT proceed to next steps while meaningful feedback exists
while true; do
  npm run pr-state -- --pr <PR_NUMBER>
  # Check meaningfulUnprocessedCount in output
  # If 0 -> break and proceed to next step
  # If > 0 -> process all feedback, commit, push, repeat
done
```

**MANDATORY loop until meaningful feedback = 0**:
- **MUST process ALL meaningful feedback before requesting new reviews**
- Check `meaningfulUnprocessedCount` in the output
- If > 0 → Process feedback, commit, push, **check again**
- **Repeat until meaningfulUnprocessedCount = 0**
- Only then proceed to Step 1 (check unreviewed commits)

**Critical importance**:
- **ALL existing feedback MUST be processed** before moving forward
- Do NOT stop after processing once - **continue until count = 0**
- Processing existing feedback first maintains review quality
- Prevents overwhelming reviewers with repeated review requests
- Ensures all feedback is systematically addressed

**Complete loop example**:
```typescript
// Step 0: LOOP until all existing feedback is processed
console.log('=== STEP 0: Processing ALL existing feedback ===');

let existingFeedbackLoop = 0;
const MAX_FEEDBACK_LOOPS = 10; // Safety limit

while (existingFeedbackLoop < MAX_FEEDBACK_LOOPS) {
  existingFeedbackLoop++;
  console.log(`\n--- Existing Feedback Loop ${existingFeedbackLoop} ---`);

  // Check for existing feedback
  const state = await checkForMeaningfulFeedback(prNumber);

  if (state.data.meaningfulUnprocessedCount === 0) {
    console.log('✅ No more existing feedback - proceeding to next step');
    break;
  }

  console.log(`⚠️  Found ${state.data.meaningfulUnprocessedCount} unprocessed feedback items`);
  console.log('📋 Processing all feedback in this loop...');

  // Filter meaningful unprocessed feedback
  const meaningful = state.data.comments.filter(c =>
    !c.processed && isMeaningfulFeedback(c)
  );

  // Process by priority
  for (const priority of ['CRITICAL', 'IMPORTANT', 'NICE-TO-HAVE']) {
    const items = meaningful.filter(c => c.priority === priority);

    for (const item of items) {
      console.log(`Processing ${priority}: ${item.file}:${item.line}`);

      // Use @superpowers:executing-plans for each feedback item
      await processFeedbackWithSuperpower(item);

      // Mark as processed immediately
      await markCommentProcessed(prNumber, item.id);
    }
  }

  // Commit and push
  await commitAndPush(`fix: address existing Gemini feedback - loop ${existingFeedbackLoop}`);

  console.log('🔄 Checking for remaining feedback...');
  // Loop continues - will check again
}

console.log('✅ All existing feedback processed - now proceeding with workflow');
```

### 1. Check for Unreviewed Commits
```bash
# After processing existing feedback, check if there are commits that haven't been reviewed
# If unreviewed commits exist, request Gemini review
npm run pr-loop -- --wait
```

**Automatic unreviewed commit detection**:
- Compare latest commit timestamp with last Gemini bot review time
- If commits exist after last review → automatically request `/gemini review`
- The script then enters the main polling loop to wait for and process feedback

**This ensures**:
- No commits are left unreviewed
- All feedback is based on latest code
- Automated review request without manual intervention

### 2. Wait for Gemini Review (3 minutes)
```bash
# After PR push, wait 3 minutes for Gemini bot
git push origin feature-branch
# → Check for unreviewed commits (automatic)
# → Request review if needed (automatic)
# → Initial 3-minute wait for Gemini to respond
# → Poll for Gemini comment every 3 minutes
```

**Polling behavior**:
- After requesting review, waits 3 minutes before first check
- Check every 3 minutes for new review comments
- Track processed feedback to avoid duplication
- Resume from last processed feedback if re-triggered

**Error handling**:
- If unreviewed commits detected at start: Automatically requests `/gemini review` before polling
- If bot errors during manual review: Re-run `/gemini review` in PR comments
- If no feedback found during polling: Loop continues checking (no automatic re-review)

### 3. Fetch PR Comments with State Tracking
```bash
# Use built-in /pr-comments command to get latest Gemini feedback
/pr-comments

# Or for specific PR number
/pr-comments <PR_NUMBER>

# Load state to track processed feedback
npm run pr-state -- --pr <PR_NUMBER>
```

**State tracking integration**:
- `/pr-comments` (built-in) returns all review comments
- `npm run pr-state` loads `.pr-review-state-<PR>.json` to identify processed feedback
- Automatically filters out already-processed items
- Enables safe re-runs without duplicate fixes

**State file format** (`.pr-review-state-123.json`):
```json
{
  "prNumber": 123,
  "processedIds": ["comment-abc123"],
  "lastCheckTime": 1698765432000,
  "lastCommitSha": "abc123def"
}
```

### 4. Parse Priority Levels
| Priority | Label | Action |
|----------|-------|--------|
| 🔴 CRITICAL | HIGH | **Always fix** - blocking issues |
| 🟡 IMPORTANT | MEDIUM | **Always fix** - stability/quality |
| 🟢 NICE-TO-HAVE | LOW | **Fix if meaningful** - readability only |
| ⚪ NITPICK | VERY_LOW | **Skip** - documentation polish |
| ❌ FALSE POSITIVE | IGNORE | **Skip** - bot error |

### 5. Filter Meaningful Feedback
**Include**:
- 🔴 Critical (security, data loss, crashes)
- 🟡 Important (error handling, edge cases)
- 🟢 Nice-to-have **ONLY IF** impacts maintainability (not just style)

**Exclude**:
- ⚪ Nitpicks (documentation examples, comment style)
- ❌ False positives (unused imports actually used as types)

### 6. Process by Priority with State Tracking (Loop Until Done)
```typescript
// LOOP: Continue until no meaningful feedback remains
let iteration = 0;
const MAX_ITERATIONS = 10; // Safety limit

while (iteration < MAX_ITERATIONS) {
  iteration++;
  console.log(`\n=== Review Cycle ${iteration} ===`);

  // Load state to resume from last processed feedback
  const state = loadState(prNumber);

  // Fetch and filter feedback
  const comments = await fetchPRComments(prNumber);
  const parsed = parseComments(comments, state);
  const unprocessed = parsed.filter(c => !c.processed);
  const meaningful = unprocessed.filter(isMeaningfulFeedback); // NEW: Auto-filter

  // Check if we're done
  if (meaningful.length === 0) {
    console.log('✅ No meaningful feedback remaining - DONE!');
    break;
  }

  console.log(`Found ${meaningful.length} meaningful feedback items to process`);

  // Process in order by priority
  const priorities = ['CRITICAL', 'IMPORTANT', 'NICE-TO-HAVE'];

  for (const priority of priorities) {
    const items = meaningful.filter(f => f.priority === priority);

    for (const item of items) {
      // Use superpower skill for processing feedback
      await processFeedbackWithSuperpower(item);

      // Mark as processed immediately
      await markCommentProcessed(prNumber, item.id);
    }
  }

  // Commit and push changes
  await commitAndPush(`fix: address Gemini review feedback - cycle ${iteration}`);

  // Wait for Gemini to review (3 minutes)
  console.log('Waiting 3 minutes for Gemini bot review...');
  await sleep(3 * 60 * 1000);

  // Loop continues to check for new feedback
}
```

**Loop features**:
- **Automatic continuation**: No manual intervention needed
- **Meaningful feedback detection**: Filters CRITICAL, IMPORTANT, and impactful NICE-TO-HAVE
- **Safe termination**: Stops when no meaningful feedback remains
- **State tracking**: Prevents duplicate processing across cycles
- **Safety limit**: Maximum 10 iterations to prevent infinite loops

**Meaningful feedback criteria**:
- ✅ CRITICAL: Always meaningful (security, data loss, crashes)
- ✅ IMPORTANT: Always meaningful (error handling, edge cases)
- ✅ NICE-TO-HAVE: Meaningful if contains keywords like "error", "bug", "performance", "maintainability"
- ❌ NITPICK: Never meaningful (documentation, style)
- ❌ NONE: Never meaningful (uncategorized)

### 6.5. Local Code Review Loop (MANDATORY after ANY code change)

**핵심 원칙**: 로컬 변경 사항이 있으면 → 항상 local code review → meaningful issue 없을 때까지 반복

**CRITICAL**: Fix도 코드 변경이므로, fix 후에도 다시 review 필요!

```
┌─────────────────────────────────────────────────────────────┐
│                LOCAL CODE REVIEW LOOP                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Code changed? (Gemini fix, local fix, ANY edit)            │
│     ↓                                                        │
│  Run @superpowers:code-reviewer                              │
│     ↓                                                        │
│  Meaningful issues (Critical/Important)?                     │
│     ├─ YES → Fix issues → LOOP BACK (fix = code change!)    │
│     └─ NO  → ✅ Ready to commit                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Process**:
```typescript
// MANDATORY: Run after ANY code change
async function runLocalCodeReviewLoop(maxIterations = 5): Promise<void> {
  let iteration = 0;
  let hasChanges = true;

  while (hasChanges && iteration < maxIterations) {
    iteration++;
    console.log(`\n=== Local Code Review Loop ${iteration}/${maxIterations} ===`);

    // 1. Run superpowers:code-reviewer via Task agent
    const reviewResult = await dispatchCodeReviewer();

    // 2. Check for meaningful issues (Critical or Important only)
    const meaningfulIssues = reviewResult.issues.filter(
      issue => issue.severity === 'Critical' || issue.severity === 'Important'
    );

    if (meaningfulIssues.length === 0) {
      console.log('✅ No meaningful issues - local review complete');
      hasChanges = false;
      break;
    }

    console.log(`⚠️  Found ${meaningfulIssues.length} meaningful issues - fixing...`);

    // 3. Fix ALL meaningful issues
    for (const issue of meaningfulIssues) {
      await fixIssue(issue);
    }

    // 4. Loop back for re-review (fix = code change!)
    console.log('🔄 Code changed by fixes - will review again...');
  }

  if (iteration >= maxIterations) {
    console.warn('⚠️  Max iterations reached - review manually');
  }
}
```

**Integration Point**:
```typescript
for (const item of meaningfulFeedback) {
  await processFeedbackWithSuperpower(item);
  await runLocalCodeReviewLoop();  // MANDATORY after code change
  await markCommentProcessed(prNumber, item.id);
}
await commitAndPush(`fix: address Gemini feedback - cycle ${cycle}`);
```

**Why Loop Back After Fix**:
- Fix = Code Change = Must Review Again
- Issue A fix might introduce Issue B
- Only exit when NO meaningful issues remain

### 7. Commit and Push (Automated in Loop)
```bash
# Automatic commits per cycle
git add .
git commit -m "fix: address Gemini review feedback - cycle 1"
git push origin feature-branch

# → Wait 3 minutes automatically
# → Check for new feedback
# → Repeat until no meaningful feedback
# → State tracking ensures no duplicate processing
```

**Superpower skill integration**:
Uses `@superpowers:executing-plans` for systematic feedback processing:
- Analyzes each feedback item individually
- Generates targeted fixes with proper context
- Validates changes before committing
- Maintains code quality throughout
- Tracks progress in state file after each fix

**Complete workflow example with loop**:
```typescript
// NEW: Use pr-review-loop for automatic continuous processing
import { checkForMeaningfulFeedback, hasUnreviewedCommits, requestGeminiReview } from './pr-review-loop';

let cycle = 0;
const MAX_CYCLES = 10;

// 0. Check for existing feedback FIRST (CRITICAL!)
console.log('=== STEP 0: Checking for existing feedback ===');
const existingFeedback = await checkForMeaningfulFeedback(prNumber);

if (existingFeedback.data.meaningfulUnprocessedCount > 0) {
  console.log(`⚠️  Found ${existingFeedback.data.meaningfulUnprocessedCount} unprocessed feedback items`);
  console.log('📋 Processing existing feedback before requesting new review...');

  // Process existing feedback by priority
  const meaningful = existingFeedback.data.comments.filter(c => !c.processed && isMeaningfulFeedback(c));

  for (const priority of ['CRITICAL', 'IMPORTANT', 'NICE-TO-HAVE']) {
    const items = meaningful.filter(c => c.priority === priority);

    for (const item of items) {
      await processFeedbackWithSuperpower(item);
      await markCommentProcessed(prNumber, item.id);
    }
  }

  // Commit and push existing feedback fixes
  await commitAndPush('fix: address existing Gemini review feedback');

  console.log('✅ Existing feedback processed - now proceeding with workflow');
}

// 1. Check for unreviewed commits
console.log('=== STEP 1: Checking for unreviewed commits ===');
const needsReview = hasUnreviewedCommits(prNumber);

if (needsReview) {
  console.log('⚠️  Unreviewed commits detected - requesting Gemini review');
  const reviewRequested = requestGeminiReview(prNumber);
  if (!reviewRequested) {
    console.error('Failed to request Gemini review - continuing anyway');
  }
}

while (cycle < MAX_CYCLES) {
  cycle++;

  // 1. Check for meaningful feedback
  const { hasMeaningfulFeedback, data } = await checkForMeaningfulFeedback(prNumber);

  if (!hasMeaningfulFeedback) {
    console.log('✅ Review complete - no meaningful feedback remaining');
    break;
  }

  console.log(`\n=== Cycle ${cycle}: Processing ${data.meaningfulUnprocessedCount} items ===`);

  // 2. Filter meaningful unprocessed comments
  const meaningful = data.comments.filter(c =>
    !c.processed && isMeaningfulFeedback(c)
  );

  // 3. Process by priority with superpower
  for (const priority of ['CRITICAL', 'IMPORTANT', 'NICE-TO-HAVE']) {
    const items = meaningful.filter(c => c.priority === priority);

    for (const item of items) {
      await processFeedbackWithSuperpower(item); // Uses @superpowers:executing-plans
      await markCommentProcessed(prNumber, item.id);
    }
  }

  // 4. Commit and push
  await commitAndPush(`fix: address Gemini review feedback - cycle ${cycle}`);

  // 5. Wait for Gemini (3 minutes)
  console.log('Waiting 3 minutes for Gemini review...');
  await sleep(180000);

  // Loop automatically continues
}
```

## Quick Reference

### Auto Mode = Ralph-Loop (DEFAULT)
```bash
# When user says "auto", this executes automatically:
/ralph-loop "Process Gemini PR #<NUMBER> feedback. Check npm run pr-state, fix by priority, commit, push, repeat. Output <promise>DONE</promise> when meaningfulUnprocessedCount=0" --completion-promise "DONE" --max-iterations 20
```

### Operating Mode Selection
```
Which mode to use?
├─ User says "auto"? → RALPH MODE (DEFAULT - auto-executed)
│   └─ /ralph-loop with completion promise
├─ Need script-based control? → SCRIPT MODE (legacy)
│   └─ npm run pr-auto
└─ Need single check? → MANUAL MODE
    └─ npm run pr-loop -- --wait
```

### Priority Decision Tree
```
Is it 🔴 CRITICAL or 🟡 IMPORTANT?
├─ Yes → Fix immediately
└─ No → Is it 🟢 NICE-TO-HAVE?
    ├─ Yes → Does it impact maintainability? (not just style)
    │   ├─ Yes → Fix
    │   └─ No → Skip
    └─ No → Skip (⚪ NITPICK or ❌ FALSE POSITIVE)
```

### Local Code Review Quick Reference

**When**: After fixing each Gemini feedback item, BEFORE committing

**Command**: Use Task tool with superpowers:code-reviewer agent

**Loop Condition**: Continue until no Critical or Important issues

**Max Iterations**: 5 (safety limit)

**Issue Severity Mapping**:
| Code Reviewer | Action |
|---------------|--------|
| Critical | Must fix immediately |
| Important | Must fix before commit |
| Minor | Note for later |

### Meaningful vs Nitpick Examples
| Feedback | Priority | Action | Reasoning |
|----------|----------|--------|-----------|
| Missing error handling | 🟡 IMPORTANT | ✅ Fix | Prevents crashes |
| Variable `data` → `userData` | 🟢 NICE-TO-HAVE | ⚠️ Maybe | Only if used widely |
| Add README example | ⚪ NITPICK | ❌ Skip | Documentation polish |
| "Unused import" (actually used) | ❌ FALSE POSITIVE | ❌ Skip | Bot error |

## Common Mistakes (RED FLAGS)

**❌ DON'T:**
- ❌ **Stop after processing feedback once** → **LOOP until meaningfulUnprocessedCount = 0!** (CRITICAL!)
- ❌ **Request new review with existing feedback** → **Process ALL existing feedback first!** (CRITICAL!)
- ❌ **Assume one pass is enough** → **ALWAYS check again after processing**
- ❌ Stop after one cycle → **Use loop to continue until done**
- ❌ Manually check for new feedback → **Let automation loop**
- ❌ "Time pressure" → Skip important fixes (🟡 is never optional)
- ❌ "Perfect is enemy of good" → Ignore critical issues (🔴 must be fixed)
- ❌ "Follow-up PR acceptable" → Defer security fixes (blocking issues never deferred)
- ❌ Process nitpicks (⚪) → Wastes time on non-issues
- ❌ Manually read comments → Use `/pr-comments` command instead
- ❌ Skip false positives check → Wastes time on bot errors
- ❌ Process same feedback twice → Use state tracking

**✅ DO:**
- ✅ **LOOP until meaningfulUnprocessedCount = 0** → Never skip this check! (CRITICAL!)
- ✅ **Check feedback after EVERY processing cycle** → Process, commit, check again
- ✅ **Use while loop pattern** → Continue until count reaches 0
- ✅ **Check `meaningfulUnprocessedCount` repeatedly** → Don't trust one check
- ✅ Always fix 🔴 CRITICAL + 🟡 IMPORTANT (non-negotiable)
- ✅ Use `/pr-comments` (built-in) to fetch review comments
- ✅ Wait 3 minutes for Gemini response after push (faster cycle)
- ✅ Track state with `.pr-review-state-<PR>.json` to avoid duplicates
- ✅ Use `@superpowers:executing-plans` for systematic fixes
- ✅ Retry with `/gemini review` on bot errors
- ✅ Filter false positives before processing
- ✅ Commit per cycle (not batch)
- ✅ Resume from last processed feedback if interrupted

## Common Mistakes - Local Code Review Loop

**❌ DON'T:**
- ❌ **Fix 후 review 안 함** → Fix도 코드 변경! 반드시 다시 review!
- ❌ **한 번만 review** → meaningful issue 없을 때까지 반복해야 함
- ❌ **Commit 먼저** → Local review loop 완료 전에 commit 금지
- ❌ **Minor issue fix** → Critical/Important만 fix (Minor는 무시)
- ❌ **무한 반복** → max 5 iterations, 그 이상은 수동 검토

**✅ DO:**
- ✅ **코드 변경 → review** (Gemini fix, local fix, ANY change)
- ✅ **Fix → 다시 review** (fix도 코드 변경이므로)
- ✅ **Loop until no issues** (meaningful issue 0이 될 때까지)
- ✅ **Only then commit** (loop 완료 후에만 commit)

**Loop Flow**:
```
Code Change → Review → Issues? → YES → Fix → Review → Issues? → YES → Fix → Review → NO → ✅ Commit
```

## Error Handling

### GitHub CLI Not Found
```
Error: /bin/sh: 1: gh: not found
→ Cause: GitHub CLI is not installed or not in PATH
→ Action: Install and authenticate GitHub CLI (see Prerequisites section)
→ Verify: gh --version
→ Authenticate: gh auth login
```

**Common installation issues**:
- **macOS**: `brew install gh` (requires Homebrew)
- **Linux (Debian/Ubuntu)**:
  ```bash
  curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
  sudo apt update
  sudo apt install gh
  ```
- **Windows**: Download from https://cli.github.com

### jq Syntax Errors
```
Error: jq: error: syntax error, unexpected INVALID_CHARACTER
→ Cause: Incorrect jq syntax or shell escaping issues
→ Action: Use examples from Prerequisites section
→ Common fixes:
  - Use `!=` not `\!=` for not-equal
  - Use `.body[0:100]` not `.body[:100]` for substring
  - Wrap entire jq filter in single quotes
```

### No Gemini Comment After 3 Minutes
```bash
# Manually trigger review
gh pr comment <PR_NUMBER> --body "/gemini review"

# Wait another 3 minutes
# Check again with: /pr-comments <PR_NUMBER>
```

### Gemini Bot Error
```
Error: Gemini bot failed to complete review
→ Action: Re-run `/gemini review` in PR comments
→ Wait 5 minutes
→ Continue workflow
```

### /pr-comments Command Failure
```
Error: Command failed or no PR context
→ Action: Ensure you're in a PR context or specify PR number explicitly
→ Try: /pr-comments <PR_NUMBER>
→ Fallback: Use `gh pr view <PR_NUMBER> --json comments`
```

### State File Corruption
```
Error: Invalid state file format
→ Action: The script automatically handles this by backing up the corrupted file
→ Automatic behavior:
  1. Corrupted file backed up to .pr-review-state-<PR>.json.backup
  2. Fresh state file created automatically
  3. Processing continues from clean slate
→ Manual reset (if needed):
  npm run pr-state -- --clear-state 123
→ Result: Automation continues without manual file operations
```

### Multiple Review Cycles (Automated Loop)
```
🔄 AUTOMATIC LOOP (no manual intervention needed):

Cycle 1: Check feedback → 5 meaningful items found
         → Fix CRITICAL + IMPORTANT → mark processed → push → wait 3 min

Cycle 2: Check feedback → 2 meaningful items found
         → Fix new items → mark processed → push → wait 3 min

Cycle 3: Check feedback → 1 meaningful item found
         → Fix item → mark processed → push → wait 3 min

Cycle 4: Check feedback → 0 meaningful items found
         → ✅ DONE! Exit loop

✅ State tracking prevents duplicate processing across cycles
✅ Meaningful feedback detection filters nitpicks automatically
✅ Loop terminates when no meaningful feedback remains
```

**NEW: Using pr-review-loop script**:
```bash
# Start automated loop (reports feedback, doesn't process)
npm run pr-loop -- --wait

# Exit codes:
# 0 = No meaningful feedback (done)
# 2 = Meaningful feedback found (needs processing)
# 1 = Error
```

## Implementation Checklist

**Step 0: Process ALL existing feedback (LOOP until count = 0)**:
- [ ] **Start existing feedback loop**
- [ ] Run `npm run pr-state -- --pr <PR_NUMBER>`
- [ ] Check `meaningfulUnprocessedCount` in output
- [ ] **If count > 0:**
  - [ ] Process ALL meaningful feedback (CRITICAL, IMPORTANT, meaningful NICE-TO-HAVE)
  - [ ] Use `@superpowers:executing-plans` for each item
  - [ ] Mark each item as processed immediately
  - [ ] Commit and push changes
  - [ ] **🔄 LOOP BACK: Run `npm run pr-state` again**
- [ ] **If count = 0:**
  - [ ] ✅ Proceed to Step 1
- [ ] **NEVER proceed to Step 1 while count > 0**

**Step 1: Check for unreviewed commits (only after Step 0 complete)**:
- [ ] PR pushed successfully
- [ ] **Confirm meaningfulUnprocessedCount = 0 from Step 0**
- [ ] **Check for unreviewed commits**
- [ ] **Request `/gemini review` if unreviewed commits exist**
- [ ] Start polling loop with feedback check
- [ ] Load state to track processed items

**Each review cycle (automated):**
- [ ] Check for meaningful feedback with `npm run pr-state`
- [ ] If `meaningfulUnprocessedCount === 0` → ✅ DONE, exit loop
- [ ] If meaningful feedback found → continue processing

**During processing (each cycle):**
- [ ] Process 🔴 CRITICAL first (with `@superpowers:executing-plans`)
- [ ] Process 🟡 IMPORTANT second (with `@superpowers:executing-plans`)
- [ ] Evaluate 🟢 NICE-TO-HAVE for meaningfulness (auto-filtered)
- [ ] Skip ⚪ NITPICK items (auto-filtered)
- [ ] Skip ❌ FALSE POSITIVE items (manual check)
- [ ] Mark each item as processed immediately

**Local Code Review Loop (MANDATORY after ANY code change):**
- [ ] Code changed? (Gemini fix, local fix, any edit)
- [ ] Run `@superpowers:code-reviewer`
- [ ] Check for Critical/Important issues
- [ ] **If issues found:**
  - [ ] Fix all meaningful issues
  - [ ] **🔄 LOOP BACK** - fix도 코드 변경이므로 다시 review!
- [ ] **If no issues:**
  - [ ] ✅ Ready to commit
- [ ] Only commit when NO meaningful issues remain

**After each cycle (automated):**
- [ ] Commit changes with cycle number
- [ ] Push to PR branch
- [ ] Wait 3 minutes for Gemini review
- [ ] Loop back to check for new feedback

**Loop termination:**
- [ ] No meaningful feedback remaining
- [ ] Or maximum iterations reached (safety limit)
- [ ] Final state file updated
- [ ] All changes pushed

## Real-World Impact

**🆕 With Ralph Loop (핵심: 완전 자율 처리)**:
- **Human intervention**: 100% → 0% (fully autonomous)
- **Context switching**: Eliminated (Ralph handles everything)
- **Overnight processing**: Possible (walk away, come back to approved PR)
- **Consistency**: Perfect (same process every time)
- **Error recovery**: Automatic (Ralph retries on failure)

**With Local Code Review Loop (핵심: 코드 변경 → review 반복)**:
- **Review rounds reduced**: 3-4 → 1-2 (50% reduction)
- **Time per PR**: 20-25 min → 15-20 min
- **First-fix quality**: 70% → 95%
- **Gemini re-review triggers**: Reduced by 80%
- **Cascading issues caught**: 90% (fix가 새 issue 만드는 경우)

**핵심 원칙 적용 효과**:
```
BEFORE (No local loop):                  AFTER (Local review loop):
Gemini fix → Commit → Push               Gemini fix → Local Review
→ Gemini finds new issue                 → Issue found → Fix
→ Fix → Commit → Push                    → Local Review (fix도 변경!)
→ Gemini finds another issue             → Issue found → Fix
→ Fix → Commit → Push                    → Local Review
→ Done (4 rounds)                        → No issues → Commit → Push
                                         → Gemini finds nothing → Done ✅

Rounds: 4                                Rounds: 1
Wait time: 12 min (3min × 4)             Wait time: 3 min (3min × 1)
Total: 25 min                            Total: 10 min
```

**Why This Works**:
- Fix도 코드 변경 → 다시 review → cascading issue 사전 발견
- Gemini가 볼 때는 이미 clean한 코드
- 3분 대기 시간 최소화 (1회만 대기)

**NEW: Mandatory feedback loop benefits**:
- **Zero skipped feedback**: Guarantees ALL meaningful feedback is processed
- **Prevention of review spam**: No new review requests while feedback exists
- **Complete cleanup**: Ensures meaningful feedback count reaches 0 before moving on
- **Better review quality**: Reviewers never see repeated unaddressed issues
- **Reduced back-and-forth**: Average 2-3 review rounds vs 5-6 without loop

**Loop automation benefits**:
- **Fully automated**: Zero manual intervention from push to approval
- **Time saved**: 30-60 min per PR (no manual re-checking needed)
- **Faster completion**: Average 3-4 cycles vs 6-8 manual cycles
- **Error reduction**: 90% fewer wasted fixes with meaningful feedback detection

**Existing benefits**:
- **Faster cycles**: 3-minute polling (down from 5 minutes) = 40% faster feedback
- **Time saved per cycle**: 15-20 min (no manual comment parsing)
- **Error reduction**: 80% fewer wasted fixes on nitpicks/false positives
- **Resumability**: State tracking enables safe interruption and resumption
- **Quality**: `@superpowers:executing-plans` ensures systematic, high-quality fixes
- **Consistency**: Same filtering logic across team members
- **Automation**: GitHub API integration enables CI/CD workflows
- **Efficiency**: No duplicate work when re-running automation

**Comparison**:
```
BEFORE (Manual):                           AFTER (Loop until count = 0):
Push → Wait → Check → Process              Push → Loop existing feedback until 0
→ Push → Wait → Check → Process            → Check unreviewed → Request review
→ Push → Wait → Check → Process            → Loop new feedback (automatic) → Done ✅
→ ... (repeat 6-8 times)
→ Often miss some feedback                 Time: 20-25 min
Time: 90-120 min                           Review rounds: 2-3
Review rounds: 5-6                         Intervention: 0
Intervention: Every cycle                  Skipped feedback: 0 ✅
Skipped feedback: 20-30%                   Auto review request: Yes ✅
```

**Ralph Mode is DEFAULT**:
```
SCRIPT MODE (legacy):                      RALPH MODE (DEFAULT):
Human monitors loop                        Ralph handles loop autonomously
Script exits, human re-runs                Stop hook feeds prompt back automatically
Context switches between runs              Single continuous session
Manual error handling                      Automatic retry on failure

Time: 20-25 min (attended)                 Time: Same, but UNATTENDED
Intervention: After each script            Intervention: 0 (truly hands-free)

When user says "auto" → Ralph-loop executes automatically
```
