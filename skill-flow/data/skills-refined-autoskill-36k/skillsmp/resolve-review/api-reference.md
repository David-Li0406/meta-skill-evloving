# API Reference

GitHub GraphQL API usage for PR review resolution.

## Fetch Query

```graphql
query($owner: String!, $repo: String!, $pr: Int!) {
  viewer { login }
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      id
      reviewThreads(first: 100) {
        nodes {
          id
          isResolved
          isOutdated
          comments(first: 10) {
            nodes {
              id
              author { login }
              body
              path
              line
              originalLine
              diffHunk
              url
              createdAt
            }
          }
        }
      }
      comments(first: 100) {
        nodes {
          id
          author { login }
          body
          url
          createdAt
          isMinimized
        }
      }
    }
  }
}
```

**Limits:** 100 threads, 10 comments per thread, 100 PR comments.

## Field Mapping

| Response field | Variable | Used for |
|----------------|----------|----------|
| `pullRequest.id` | `PR_NODE_ID` | Reply target, summary comment |
| `reviewThread.id` | `THREAD_NODE_ID` | Resolve thread |
| `reviewThread.comments[0].id` | `COMMENT_NODE_ID` | Reaction, reply inReplyTo |
| `comments[].id` | `COMMENT_NODE_ID` | Reaction, minimize |
| `viewer.login` | `CURRENT_USER` | Self-exclusion filter |

## Filter Criteria

**Review threads:**
- `isResolved: false`
- Exclude `viewer.login` (unless `--self`)
- Optional author filter (case-insensitive contains)

**PR comments:**
- `isMinimized: false`
- Exclude `viewer.login` (unless `--self`)
- Optional author filter

**Line numbers:**
- Use `line` if available (current position)
- Fall back to `originalLine` (position when commented)
- If `isOutdated: true`, code may have moved

## Mutations

### Add Reaction

```graphql
mutation($subjectId: ID!, $content: ReactionContent!) {
  addReaction(input: {subjectId: $subjectId, content: $content}) {
    reaction { content }
  }
}
```

`ReactionContent` enum: `THUMBS_UP`, `THUMBS_DOWN`, `LAUGH`, `HOORAY`, `CONFUSED`, `HEART`, `ROCKET`, `EYES`

### Reply to Thread

```graphql
mutation($pullRequestId: ID!, $inReplyTo: ID!, $body: String!) {
  addPullRequestReviewComment(input: {
    pullRequestId: $pullRequestId,
    inReplyTo: $inReplyTo,
    body: $body
  }) {
    comment { id }
  }
}
```

### Resolve Thread

```graphql
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { isResolved }
  }
}
```

### Minimize PR Comment

```graphql
mutation($subjectId: ID!, $classifier: ReportedContentClassifiers!) {
  minimizeComment(input: {subjectId: $subjectId, classifier: $classifier}) {
    minimizedComment { isMinimized }
  }
}
```

`classifier`: Use `RESOLVED` for addressed comments.

### Post PR Comment (Summary)

```graphql
mutation($subjectId: ID!, $body: String!) {
  addComment(input: {subjectId: $subjectId, body: $body}) {
    commentEdge { node { id url } }
  }
}
```

`subjectId` is the PR node ID.

## Batching Mutations

Combine multiple operations in one request:

```graphql
mutation {
  r1: addReaction(input: {subjectId: "ID1", content: THUMBS_UP}) { reaction { content } }
  r2: addReaction(input: {subjectId: "ID2", content: THUMBS_UP}) { reaction { content } }
  t1: resolveReviewThread(input: {threadId: "TID1"}) { thread { isResolved } }
  t2: resolveReviewThread(input: {threadId: "TID2"}) { thread { isResolved } }
}
```

Use aliased names (`r1`, `r2`, `t1`, `t2`) for multiple same-type mutations.

## Error Handling

- **PR not found:** `pullRequest: null` in response
- **Thread already resolved:** Mutation succeeds silently (idempotent)
- **Missing permissions:** Check `gh auth status` for write access

## CLI Usage

```bash
# Get repo info
OWNER=$(gh repo view --json owner -q '.owner.login')
REPO=$(gh repo view --json name -q '.name')
PR_NUMBER=$(gh pr view --json number -q .number)

# Execute query
gh api graphql -f query='...' -f owner="$OWNER" -f repo="$REPO" -F pr="$PR_NUMBER"

# Execute mutation (--silent to suppress output)
gh api graphql -f query='mutation { ... }' --silent
```
