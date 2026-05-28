# GitHub API Patterns

| Field | Value |
|-------|-------|
| **Created** | 2026-01-14 |
| **Sources** | retrospectives (2026-01-10, 2026-01-14) |
| **Tags** | `github` `api` `graphql` `rest` `gh-cli` |

---

## Key Insight

> GitHub Discussions require GraphQL API (not REST), milestones use REST API, and `jq --arg` should be used for safe JSON construction with dynamic values.

---

## The Problem

| Attempt | Result |
|---------|--------|
| REST API for Discussions comments | 404 Not Found |
| String interpolation in JSON | Shell injection risk |
| `gh pr view --json` with missing scopes | Permission errors |
| Direct status change in Jira | Need workflow transitions |

---

## The Solution

### Pattern: Discussion Comments (GraphQL)

```bash
# 1. Get Discussion ID
DISCUSSION_ID=$(gh api graphql -f query='
query {
  repository(owner: "owner", name: "repo") {
    discussion(number: 36) {
      id
    }
  }
}' --jq '.data.repository.discussion.id')

# 2. Add Comment
# Escape content for JSON (avoid useless use of cat)
BODY=$(jq -Rs . < content.md)

gh api graphql -f query="
mutation {
  addDiscussionComment(input: {
    discussionId: \"$DISCUSSION_ID\",
    body: $BODY
  }) {
    comment { id url }
  }
}"
```

### Pattern: Milestones (REST API)

```bash
# Create milestone
gh api repos/:owner/:repo/milestones \
  --method POST \
  -f title="v1.2 - Feature Name" \
  -f state="open" \
  -f description="Description here"

# List milestones (including closed)
gh api "repos/:owner/:repo/milestones?state=all" \
  --jq '.[] | "\(.number). \(.title) [\(.state)]"'

# Assign issue to milestone
gh issue edit 42 --milestone "v1.2 - Feature Name"
```

### Pattern: Safe JSON Construction

```bash
# WRONG - shell injection risk
gh api endpoint -f body="$USER_INPUT"

# CORRECT - use jq --arg
BODY=$(jq -n --arg content "$USER_INPUT" '{body: $content}')
gh api endpoint --input - <<< "$BODY"

# Or use file-based approach
echo "$USER_INPUT" > /tmp/body.txt
gh api endpoint -F body=@/tmp/body.txt
```

### Pattern: PR Review Comments

```bash
# Get PR comments
gh api repos/{owner}/{repo}/pulls/{pr}/comments \
  --jq '.[] | {id, path, line, body, user: .user.login}'

# Reply to specific comment
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies \
  -f body="Fixed in abc123!"
```

### Pattern: Handle Token Scope Errors

```bash
# Check current scopes
gh auth status

# Refresh with additional scopes
gh auth refresh -s project,read:project,read:org

# Common scope requirements:
# - project: GitHub Projects (ProjectsV2)
# - read:org: Organization data
# - read:discussion: Discussions
```

**Why this works:**
- GraphQL provides unified access to newer GitHub features
- REST API is simpler for established endpoints
- `jq --arg` prevents shell interpretation of values
- File-based approach is safest for arbitrary content

---

## Anti-Patterns

| Don't Do This | Do This Instead |
|---------------|-----------------|
| REST API for Discussions | GraphQL mutation |
| `-f body="$var"` with user content | `-F body=@file` or `jq --arg` |
| Assume token has all scopes | Check `gh auth status` first |
| `gh pr view --json reviews` without scope | Handle scope errors gracefully |

---

## API Comparison

| Feature | API | Method |
|---------|-----|--------|
| Issues | REST | `gh issue` or `gh api` |
| Pull Requests | REST | `gh pr` or `gh api` |
| Discussions | **GraphQL** | `gh api graphql` |
| Projects V2 | **GraphQL** | Requires `project` scope |
| Milestones | REST | `gh api repos/.../milestones` |
| Releases | REST | `gh release` |

---

## When to Apply

### Use GraphQL
- GitHub Discussions (comments, mutations)
- GitHub Projects V2
- Complex queries with relationships
- When REST endpoint doesn't exist

### Use REST API
- Issues and PRs (standard operations)
- Milestones
- Releases
- Simple CRUD operations

### Use `gh` CLI Shortcuts
- `gh issue`, `gh pr` - Built-in commands
- `gh api` - Direct API access
- `gh api graphql` - GraphQL queries

---

## Quick Reference

| Task | Command |
|------|---------|
| Discussion comment | `gh api graphql -f query='mutation {...}'` |
| Create milestone | `gh api repos/:owner/:repo/milestones --method POST` |
| PR review comments | `gh api repos/.../pulls/.../comments` |
| Reply to comment | `gh api .../comments/{id}/replies -f body="..."` |
| Check token scopes | `gh auth status` |
| Add scopes | `gh auth refresh -s scope1,scope2` |

---

## Related

### Source Retrospectives
- `docs/retrospective/2026-01/retrospective_2026-01-10_092500.md`
- `docs/retrospective/2026-01/retrospective_2026-01-14_225435.md`

### Code References
- `assets/commands/pr-review.md` - PR comment handling
- `scripts/jira-client.sh` - API client patterns
