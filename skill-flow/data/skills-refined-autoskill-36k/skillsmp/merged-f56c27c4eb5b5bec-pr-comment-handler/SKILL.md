---
name: pr-comment-handler
description: Use this skill when the user asks to "handle PR comments", "resolve PR review comments", or "fix PR feedback" on GitHub pull requests.
---

# PR Comment Handler

Automate the process of handling GitHub PR review comments: evaluate each comment, fix issues with atomic commits, and reply with detailed resolution information.

## Core Principles

1. **Critical Thinking First** - Evaluate whether each comment is correct before acting; reviewers can make mistakes too.
2. **Commit by Topic, Not by Comment** - Group commits by logical change, not by comment count; one commit can address multiple related comments.
3. **Atomic Commits** - Each commit should be a single logical fix; different concerns require separate commits.
4. **Human Collaboration** - Ask the user when uncertain about a fix, interpretation, or when you disagree with a comment.
5. **Detailed Replies** - Include fix explanation, commit hash, and link in every resolution.
6. **Reply to Thread** - Always reply directly to each review thread, NOT as a general PR comment at the bottom.

## Quick Start

### Interactive Mode (Default)

```
User: Handle the comments on this PR: https://github.com/owner/repo/pull/123
```

Workflow:
1. Fetch all unresolved review comments.
2. Present each comment for review.
3. For each comment, determine whether to fix or explain why no fix is needed.
4. Execute fixes with atomic commits.
5. Reply and resolve each comment.

### Auto Mode

```
User: Auto-resolve all comments on https://github.com/owner/repo/pull/123
```

Process all comments automatically, only pausing for truly ambiguous cases.

## Workflow Overview

### Phase 1: Fetch Comments

Use `gh api graphql` to retrieve all unresolved review comments:

```bash
gh api graphql -f query='
{
  repository(owner: "<OWNER>", name: "<REPO>") {
    pullRequest(number: <PR_NUMBER>) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          path
          line
          comments(first: 10) {
            nodes {
              body
              author { login }
            }
          }
        }
      }
    }
  }
}' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false)'
```

### Phase 1.5: Identify AI Comments

Determine if each comment is from an AI reviewer. **Only AI comments will be auto-resolved; human comments will only receive replies.**

#### Detection Methods

1. **Bot Account Suffix**: Check if author login ends with `[bot]`.
2. **Known AI Services**: Match against known AI code review services and LLMs.

#### Detection Logic

```bash
# AI/Bot Detection Logic (case-insensitive)
is_ai_comment=false
author_lower=$(echo "$author_login" | tr '[:upper:]' '[:lower:]')

# Combined pattern: [bot] suffix OR known AI services
ai_patterns='(\[bot\]$|coderabbitai|codiumai|sourcery-ai|deepsource|sonarcloud|codeclimate|snyk|copilot|claude|gemini|codex|openai|anthropic|chatgpt|gpt|github-actions|dependabot|renovate)'

if [[ "$author_lower" =~ $ai_patterns ]]; then
  is_ai_comment=true
fi
```

### Phase 2: Evaluate Each Comment

For each unresolved comment, **critically assess whether the suggestion is correct** before determining action:

| Decision | Criteria |
|----------|----------|
| **Needs Fix** | Valid point: actual bug, code issue, style violation, missing feature |
| **No Fix Needed** | Already addressed, misunderstanding, design choice, out of scope |
| **Disagree** | Reviewer's suggestion is incorrect, would introduce bugs, violates architecture, or is technically flawed |
| **Uncertain** | Ambiguous request, multiple interpretations, needs clarification |

### Phase 3: Execute Action

#### If Fix Needed

1. Read the relevant file(s).
2. Implement the fix.
3. Create an atomic commit with a descriptive message.
4. Push to the PR branch.
5. Reply with fix details.
6. **If AI comment**: Resolve the thread | **If human**: Leave unresolved.

#### If No Fix Needed

1. Compose explanation of why no change is required.
2. Reply with the explanation.
3. **If AI comment**: Resolve the thread | **If human**: Leave unresolved.

#### If Disagree

1. **Verify your assessment** - Double-check your reasoning against the codebase.
2. **Present to user first** - Always discuss with the user before responding to the reviewer.
3. Explain why the suggestion may be problematic.
4. Compose a polite, technical response with evidence.
5. **Do NOT auto-resolve** - Let the reviewer respond or the user decide.

#### If Uncertain

1. Present the comment to the user.
2. Explain the ambiguity.
3. Ask for guidance.
4. Proceed based on user input.

### Phase 4: Reply (and Conditionally Resolve)

After each action, reply to the comment thread. **Only auto-resolve if the comment is from an AI/bot; human comments require manual resolution.**

### Phase 5: Summary Report

After processing all comments, output a summary report.

## GitHub CLI Commands

### Fetch PR Comments

```bash
gh api graphql -f query='
{
  repository(owner: "<OWNER>", name: "<REPO>") {
    pullRequest(number: <NUMBER>) {
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          path
          line
          comments(first: 10) {
            nodes { body author { login } }
          }
        }
      }
    }
  }
}'
```

### Reply to Comment

```bash
gh api graphql -f query='
  mutation($body: String!, $threadId: ID!) {
    addPullRequestReviewThreadReply(input: {
      pullRequestReviewThreadId: $threadId,
      body: $body
    }) {
      comment { id }
    }
  }
' -f threadId="<THREAD_ID>" -f body="<REPLY_BODY>"
```

### Resolve Thread

```bash
gh api graphql -f query='
  mutation {
    resolveReviewThread(input: {
      threadId: "<THREAD_ID>"
    }) {
      thread { isResolved }
    }
  }
'
```

## Important Guidelines

### DO

- **Critically evaluate comments:** Verify the technical validity of each suggestion against the codebase before acting.
- **Check comment author type:** Determine if the comment is from AI/bot before deciding whether to auto-resolve.
- **Only auto-resolve AI comments:** After replying to an AI/bot comment, resolve the thread. Human comments should only receive replies.
- **Commit by topic:** Create atomic commits for each logical change. Group related fixes into one commit, never bundle unrelated changes.
- **Write descriptive commit messages:** Describe the *what* and *why* of the change using conventional commit format.

### DON'T

- **Blindly accept all comments** - always verify correctness first.
- **Auto-resolve human reviewer comments** - only AI/bot comments should be auto-resolved; let humans close their own threads.
- **Bundle different concerns** into one commit - separate topics need separate commits.

## Error Handling

| Error | Action |
|-------|--------|
| Comment already resolved | Skip and continue |
| File not found | Ask user for correct path |
| Commit fails | Report error, do not resolve |
| Push fails | Report error, suggest manual intervention |
| GraphQL API error | See the "Fallback Behavior" section |

## Additional Resources

### Reference Files

For detailed workflows and templates:

- **`references/workflow.md`** - Step-by-step workflow with examples
- **`references/reply-templates.md`** - Copy-paste reply templates for common scenarios

## Fallback Behavior

If the GraphQL API fails to reply to a thread:

1. **Retry once** after a brief delay.
2. **If retry fails**, fall back to `gh pr comment` with clear context.
3. **Report to user** that the reply was posted as a general comment instead of a thread reply.
4. **Continue processing** remaining comments.

> **Important:** The fallback should only be used when GraphQL truly fails. Always attempt GraphQL first.