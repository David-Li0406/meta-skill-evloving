---
name: code-review
description: Run multi-perspective code review on a PR
---

# Multi-Perspective Code Review

Spawns a single Sonnet 4.5 agent that analyzes a PR from six perspectives and posts a unified comment.

## What It Does

1. Identifies the PR to review (from argument or current branch)
2. Spawns ONE background agent (Sonnet 4.5) that reviews from all perspectives
3. Agent posts the unified comment directly to GitHub
4. Agent reports back a summary with confidence score

## Instructions

### Step 1: Identify and Validate the PR

If a PR number was provided as an argument, use that. Otherwise, find the open PR for the current branch:

```bash
gh pr view --json number,title,url -q '"\(.number)|\(.title)|\(.url)"'
```

Parse `number|title|url` from output. If no PR exists and no number provided:

```
No open PR found for current branch. Please provide a PR number: /code-review <number>
```

Validate PR exists if number was provided:

```bash
gh pr view <NUMBER> --json number -q '.number'
```

Also get repo owner/name for API calls:

```bash
gh repo view --json owner,name -q '"\(.owner.login)|\(.name)"'
```

### Step 2: Spawn Review Agent

Use the Task tool to spawn ONE agent with Sonnet 4.5.

**CRITICAL**:

- Set `model: "sonnet"` to use Sonnet 4.5
- Set `run_in_background: true`

Replace `<NUMBER>`, `<TITLE>`, `<OWNER>`, `<REPO>` with actual values.

**Task parameters:**

- subagent_type: "general-purpose"
- model: "sonnet"
- description: "Multi-perspective PR review"
- run_in_background: true
- prompt: (see below)

**Agent prompt:**

You are a comprehensive code review agent. Review PR #\<NUMBER\> from multiple perspectives and POST the review comment directly to GitHub.

PR: #\<NUMBER\> - \<TITLE\>
Repo: \<OWNER\>/\<REPO\>

**Gather Context** - Run these commands:

- `gh pr diff <NUMBER>` - Get the diff
- `gh api repos/<OWNER>/<REPO>/pulls/<NUMBER>/comments --jq '.[].body'` - Get existing review comments
- `gh api repos/<OWNER>/<REPO>/issues/<NUMBER>/comments --jq '.[] | select(.body | contains("unified-review")) | {id: .id, url: .html_url}'` - Check for previous unified review

**Multi-Perspective Analysis** - Review from ALL perspectives:

🔍 **Code Quality**: Logic errors, bugs, edge cases, code clarity, unaddressed previous comments

🔒 **Security**: Actual vulnerabilities (CRITICAL/HIGH/MED/LOW), not theoretical risks

🧪 **Testing** (Integration/E2E only): Focus on `browser/*.spec.ts` and `integration/*.test.ts`. Flag `.skip()`, `.todo()`, flaky selectors. IGNORE missing unit tests.

⚡ **Performance**: N+1 queries, unbounded queries, missing useMemo/useCallback. IGNORE "could be faster" without impact.

♿ **Accessibility** (WCAG 2.1 AA): Only for frontend. Flag div click handlers, missing aria-labels, color-only indicators.

🔄 **Reactivity**: Only for state mutations. Check outbox events, transactions, frontend handlers.

**Confidence Score** (1-7):

- 7: Excellent - No issues
- 6: Very Good - Minor suggestions
- 5: Good - Few improvements needed
- 4: Acceptable - Some issues, nothing blocking
- 3: Needs Work - Multiple issues to address
- 2: Significant Concerns - Blocking issues
- 1: Major Problems - Should not merge

**Post Comment** using `gh pr comment <NUMBER> --body "..."` with this structure:

```
<!-- unified-review -->

## Code Review Summary

**Confidence Score: [X]/7** - [explanation]

**Suggested improvements:** (if any issues, max 5)
- `file.ts:line` - [issue]. Suggestion: [fix]

✅ No issues found across all review perspectives. (if all clean)

---

<details><summary>🔍 Code Quality [CLEAN | X suggestions]</summary>
[content]
</details>

<details><summary>🔒 Security [CLEAN | X concerns]</summary>
[content]
</details>

<details><summary>🧪 Testing [CLEAN | N/A]</summary>
[content]
</details>

<details><summary>⚡ Performance [CLEAN | X concerns]</summary>
[content]
</details>

<details><summary>♿ Accessibility [CLEAN | N/A]</summary>
[content]
</details>

<details><summary>🔄 Reactivity [CLEAN | N/A]</summary>
[content]
</details>
```

**Supersede Old Comment** (if previous unified-review exists):

First, fetch the old comment body:

```bash
gh api repos/<OWNER>/<REPO>/issues/comments/[ID] --jq '.body'
```

Then update it to preserve the old review in a collapsible block (use heredoc to avoid quoting issues):

```bash
gh api repos/<OWNER>/<REPO>/issues/comments/[ID] -X PATCH -f body="$(cat <<'EOFBODY'
<!-- unified-review:superseded -->
**[New review available here](NEW_COMMENT_URL)**

<details>
<summary>Previous review</summary>

[OLD_COMMENT_BODY goes here, with the <!-- unified-review --> marker removed]

</details>
EOFBODY
)"
```

**Final Output** - Return ONLY this structured summary:

```
REVIEW_POSTED: <comment_url>
CONFIDENCE: <1-7>
CODE: <CLEAN | X suggestions>
SECURITY: <CLEAN | X concerns>
TESTING: <CLEAN | X suggestions | N/A>
PERFORMANCE: <CLEAN | X concerns>
ACCESSIBILITY: <CLEAN | X concerns | N/A>
REACTIVITY: <CLEAN | X concerns | N/A>
KEY_ISSUES: <top 3 comma-separated, or "None">
```

### Step 3: Collect Report

Use TaskOutput to wait for the agent:

```
TaskOutput(task_id: "<task_id>", block: true, timeout: 300000)
```

Parse the structured summary from the agent's output.

### Step 4: Report Results to User

```
Code review posted to PR #<NUMBER>: <COMMENT_URL>

Confidence: <SCORE>/7
- Code: [status]
- Security: [status]
- Testing: [status]
- Performance: [status]
- Accessibility: [status]
- Reactivity: [status]

Key issues: [list if any]
```

## Example Usage

```
/code-review 72
/code-review
```

## Token Efficiency

This skill uses a single Sonnet 4.5 agent instead of six parallel agents:

- One code exploration pass (not six)
- Shared context across all review perspectives
- Agent posts comment directly (no large content passed back)
- Only structured summary returned to orchestrator
