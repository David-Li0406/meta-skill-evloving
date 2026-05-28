---
name: address-pr-review
description: Handle PR feedback, address review comments, fix PR issues, respond to reviewer. Use when PR has comments to address, need to resolve feedback, or reviewer requested changes.
argument-hint: PR number or URL
disable-model-invocation: true
context: fork
---

# Address PR Review

Address unresolved PR review comments for pull request $ARGUMENTS.

## Process

### 1. Fetch Unresolved Comments

Parse PR number from `$ARGUMENTS` (numeric or extract from URL).

Get PR details:

```bash
gh pr view [PR_NUMBER] --json number,title,url,headRepositoryOwner,headRepository
```

Fetch unresolved threads via GraphQL:

```bash
gh api graphql -f query='
query {
  repository(owner: "OWNER", name: "REPO") {
    pullRequest(number: PR_NUMBER) {
      reviewThreads(first: 50) {
        nodes {
          isResolved
          comments(first: 10) {
            nodes {
              id
              body
              path
              line
              author {
                login
              }
              createdAt
            }
          }
        }
      }
    }
  }
}' --jq '.data.repository.pullRequest.reviewThreads.nodes[] | select(.isResolved == false) | {isResolved: .isResolved, comment: .comments.nodes[0]}'
```

### 2. Launch PR Comment Reviewer Agents

Launch one `pr-comment-reviewer` agent per unresolved comment. Use Task tool with `subagent_type: "pr-comment-reviewer"`.

**Launch all agents in parallel** using multiple Task calls in a single message.

Prompt structure:

```
Review this PR comment and evaluate whether the suggested change should be implemented:

**File**: {path}
**Line**: {line}
**Author**: {author}
**Comment**:
{body}

Provide a critical but reasonable evaluation of:
1. Whether this change is necessary
2. The proposed solution (if any) vs alternatives
3. Your recommendation
```

### 3. Generate Report

Consolidate agent responses into a summary:

```markdown
# PR Review Comment Analysis for PR #{number}

Found {N} unresolved comments.

## Summary

- **Should Fix**: {count} comments
- **Optional**: {count} comments
- **Skip**: {count} comments

---

## Comment 1: {Short description}

**File**: {path}:{line}
**Verdict**: {Should Fix / Optional / Skip}

{Agent's reasoning and recommendation}

---

## Overall Recommendation

{Synthesized recommendation across all comments}
```

## Guidelines

- Only analyze unresolved comments (`isResolved == false`)
- Launch agents in parallel for speed
- Be critical but reasonable about recommendations
- Consider CLAUDE.md principles when evaluating suggestions
- Consolidate duplicate comments
- Use clear verdicts: Should Fix, Optional, or Skip
