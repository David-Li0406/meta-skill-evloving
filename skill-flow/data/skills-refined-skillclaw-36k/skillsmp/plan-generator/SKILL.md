---
name: plan-generator
description: Creates structured fix plans in standardized format for GitHub issue comments.
---

## Purpose

Given code exploration results, generate a comprehensive plan that:
- Explains root cause clearly
- Specifies exact changes needed
- Sets scope boundaries (what we won't do)
- Provides testing approach
- Looks professional in GitHub comments

## Usage

Include this file when generating plans:

```
Use lib/plan-generator to create fix plan from exploration results
```

## Template Structure

```markdown
## 🤖 Automated Fix Plan for Issue #<NUMBER>

**Summary:** [One clear sentence: what's broken and how we'll fix it]

**Estimated scope:** X files changed, Y tests added/modified

**Confidence:** [High/Medium/Low based on exploration clarity]

<details>
<summary>📋 Detailed Plan</summary>

### 🔍 Root Cause Analysis
[Technical explanation of what's causing the issue]

### ✅ What We'll Do
- [ ] Change 1 (`file.ts:line`)
- [ ] Change 2 (`file.ts:line`)
- [ ] Add test for scenario X

### ❌ What We Won't Do
- Explanation of what's out of scope and why

### 📝 Files to Change
- `path/to/file1.ts` - Description of change
- `path/to/file2.ts` - Description of change
- `tests/file.test.ts` - Add test for X

### ✅ Testing Approach
- Unit test strategy
- Integration test needs
- Manual verification steps

### ⚠️ Risks & Considerations
[Things to watch during implementation]

</details>

---
**Next Steps:**
- 👍 React with thumbs up if this plan looks good
- 💬 Comment "approve" or "lgtm" to proceed
- ✏️ Comment with feedback if changes needed

Once approved, run: `/continue-issue <NUMBER>`
```

## Input Format

Expects exploration results:

```typescript
interface ExplorationResults {
  rootCause: string;           // What's causing the issue
  relevantFiles: FileInfo[];   // Files to modify
  confidence: 'High' | 'Medium' | 'Low';
  understanding: string;        // How the code works
}

interface FileInfo {
  path: string;                // e.g., "src/auth/config.ts"
  lines?: string;              // e.g., "12-15"
  reason: string;              // Why this file matters
}
```

## Generation Steps

### Step 1: Write Summary

One sentence combining problem and solution:

**Format:** "[Problem] by [Solution]"

**Examples:**
- ✅ "Fix login timeout by increasing session duration from 30s to 5min"
- ✅ "Resolve null pointer error by adding validation check before access"
- ✅ "Prevent crash on empty input by handling edge case"
- ❌ "Fix authentication issue" (too vague)
- ❌ "Update config file" (doesn't explain problem)

### Step 2: Estimate Scope

Count files and tests:

```
Files changed = len(relevantFiles)
Tests = 1 per bug fix (minimum) + integration tests if needed

"3 files changed, 2 tests added"
```

### Step 3: Write Root Cause

Technical but readable explanation:

**Template:**
```
The [specific code/function] in `file.ts:line` [what it does wrong].

When [trigger condition], the code [incorrect behavior] because [underlying reason].

This causes [observable symptom] that users reported.
```

**Example:**
```
The session timeout in `auth/config.ts:12` is hardcoded to 30 seconds.

When users perform actions that take longer than 30 seconds, the code
throws "Session expired" because the timeout check in `auth/middleware.ts:45`
compares against this hardcoded value.

This causes users to be logged out during normal operations, as reported in the issue.
```

### Step 4: Define What We'll Do

Specific, actionable items with file locations:

**Format:** `- [ ] [Action verb] [what] in [file:line]`

**Examples:**
- ✅ `- [ ] Update timeout constant from 30s to 300s in auth/config.ts:12`
- ✅ `- [ ] Add validation check for empty input in utils/parser.ts:34`
- ✅ `- [ ] Extract hardcoded value to environment variable`
- ❌ `- [ ] Fix the code` (not specific)
- ❌ `- [ ] Make it better` (not actionable)

**Always include tests:**
```
- [ ] Add unit test for timeout behavior
- [ ] Add integration test for login flow
- [ ] Verify existing tests still pass
```

### Step 5: Define What We Won't Do

Important for scope control:

**Why this matters:**
- Prevents scope creep
- Manages expectations
- Shows you've considered broader impact

**Examples:**
```
### ❌ What We Won't Do
- Won't refactor the entire auth system (only fixing timeout)
- Won't change session storage mechanism (out of scope)
- Won't add configurable timeout UI (can be done separately)
- Won't backport to older API versions (v1 is deprecated)
```

### Step 6: List Files to Change

With brief descriptions:

```
### 📝 Files to Change
- `src/auth/config.ts` - Update SESSION_TIMEOUT constant
- `src/auth/middleware.ts` - Use new timeout value
- `tests/auth/session.test.ts` - Add timeout test cases
- `README.md` - Document new default timeout (optional)
```

### Step 7: Define Testing Approach

Specific to the fix:

```
### ✅ Testing Approach
**Unit tests:**
- Test session timeout at boundary (29s pass, 31s fail before fix)
- Test new timeout works (299s pass, 301s fail after fix)

**Integration tests:**
- Full login flow with long-running action
- Verify session doesn't expire during valid activity

**Manual verification:**
- Run `npm test` - all existing tests should pass
- Start dev server, login, wait 60 seconds, verify still logged in
```

### Step 8: Note Risks

Honest assessment of what could go wrong:

```
### ⚠️ Risks & Considerations
- Longer timeout means more memory used for session storage
- Need to verify 5 minutes is acceptable for security policy
- May need to adjust other timeout-related code (will check during implementation)
- Existing tests may assume 30s timeout and need updating
```

## Confidence Levels

**High Confidence:**
- Found exact bug location
- Clear root cause
- Straightforward fix
- Similar fixes exist in codebase

**Medium Confidence:**
- Found likely location
- Understand general cause
- Fix approach clear but may need refinement
- Some uncertainty about side effects

**Low Confidence:**
- Found general area
- Multiple possible causes
- Will need investigation during implementation
- Recommend manual review even after auto-fix

**Include confidence in plan:**
```
**Confidence:** Medium

Root cause identified, but implementation may uncover edge cases.
Recommend reviewing PR carefully before merge.
```

## Output Generation

```typescript
function generatePlan(
  issueNumber: number,
  exploration: ExplorationResults,
  parsedIssue: ParsedIssue
): string {
  const plan = `
## 🤖 Automated Fix Plan for Issue #${issueNumber}

**Summary:** ${generateSummary(exploration)}

**Estimated scope:** ${countFiles(exploration)} files changed, ${estimateTests(exploration)} tests added

**Confidence:** ${exploration.confidence}

<details>
<summary>📋 Detailed Plan</summary>

### 🔍 Root Cause Analysis
${exploration.rootCause}

### ✅ What We'll Do
${generateActionItems(exploration)}

### ❌ What We Won't Do
${generateOutOfScope(exploration)}

### 📝 Files to Change
${listFiles(exploration)}

### ✅ Testing Approach
${generateTestStrategy(exploration)}

### ⚠️ Risks & Considerations
${generateRisks(exploration)}

</details>

---
**Next Steps:**
- 👍 React with thumbs up if this plan looks good
- 💬 Comment "approve" or "lgtm" to proceed
- ✏️ Comment with feedback if changes needed

Once approved, run: \`/continue-issue ${issueNumber}\`
  `;

  return plan;
}
```

## Example: Complete Plan

**Input:**
- Issue #42: "Login timeout after 30 seconds"
- Found: `auth/config.ts:12` has `SESSION_TIMEOUT = 30000`
- Confidence: High

**Output:**

```markdown
## 🤖 Automated Fix Plan for Issue #42

**Summary:** Fix login timeout by increasing session duration from 30s to 5min

**Estimated scope:** 2 files changed, 1 test added

**Confidence:** High

<details>
<summary>📋 Detailed Plan</summary>

### 🔍 Root Cause Analysis

The session timeout in `auth/config.ts:12` is hardcoded to 30 seconds (30000ms).

When users perform actions that take longer than 30 seconds, the session middleware
in `auth/middleware.ts:45-50` checks against this timeout and throws "Session expired"
error.

This causes users to be logged out during normal operations like filling forms or
reading documentation.

### ✅ What We'll Do
- [ ] Update SESSION_TIMEOUT from 30000 to 300000 (5 minutes) in `auth/config.ts:12`
- [ ] Verify middleware correctly uses updated constant in `auth/middleware.ts:45`
- [ ] Add test case for 5-minute session timeout in `tests/auth/session.test.ts`

### ❌ What We Won't Do
- Won't add UI for configurable timeout (can be future enhancement)
- Won't change session storage mechanism (SQLite is fine)
- Won't refactor entire auth system (only fixing timeout value)
- Won't backport to v1 API (deprecated, not maintained)

### 📝 Files to Change
- `src/auth/config.ts` - Update SESSION_TIMEOUT constant to 300000
- `tests/auth/session.test.ts` - Add test verifying 5-minute timeout works

### ✅ Testing Approach

**Unit tests:**
- Add test: session valid at 4min 59s, expires at 5min 1s
- Verify existing timeout tests updated or removed

**Integration tests:**
- Full login flow with 2-minute delay between requests
- Verify session remains active

**Manual verification:**
- Run `npm test` - all tests should pass
- Start server, login, wait 2 minutes, make request - should succeed
- Wait 6 minutes, make request - should fail with session expired

### ⚠️ Risks & Considerations
- Longer timeout = more memory for session storage (acceptable trade-off)
- Security policy may have max timeout requirements (verify 5min is ok)
- Existing tests assume 30s timeout - will need updating
- Users with very slow connections might still experience issues (rare edge case)

</details>

---
**Next Steps:**
- 👍 React with thumbs up if this plan looks good
- 💬 Comment "approve" or "lgtm" to proceed
- ✏️ Comment with feedback if changes needed

Once approved, run: `/continue-issue 42`
```

## Integration with handle-issue

```markdown
1. Parse issue (lib/issue-parser)
2. Explore code (lib/code-explorer)
3. Generate plan (lib/plan-generator) ← YOU ARE HERE
4. Post to GitHub (handle-issue command)
```

## YAGNI Notes

**Not included:**
- Multiple plan options (single recommended approach)
- Cost estimation (time estimates)
- Assignee suggestions (let users decide)
- Related issue linking (focus on current issue)

Keep it simple: one clear plan with scope and testing.
