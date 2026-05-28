# Item Model

Source of truth for the PR review resolution workflow. Both terminal and file views derive from this schema.

## Core Types

### Item

A unit of work - either review threads or a PR comment part.

| Field | Type | Description |
|-------|------|-------------|
| `id` | number | 1-based item number in session |
| `type` | `"threads"` \| `"comment-part"` | What kind of feedback |
| `feedback` | Feedback[] | One or more feedback entries (grouped threads = multiple) |
| `analysis` | Analysis | CC's assessment and suggestion |
| `response` | Response | User's decision and reply config |

### Feedback

A single piece of feedback (thread or comment part).

| Field | Type | Description |
|-------|------|-------------|
| `url` | string | GitHub permalink |
| `author` | string | GitHub login |
| `created` | ISO 8601 | When feedback was posted |
| `body` | string | Full comment text |
| `gist` | string | Generated short title (~40 chars) |
| `outdated` | boolean | Thread references moved/changed code |
| `file` | string? | File path (threads only) |
| `line` | number? | Line number (threads only) |
| `diffHunk` | string? | Diff context (threads only) |
| `replies` | Reply[]? | Conversation replies (threads only) |
| `partIndex` | number? | 1-based part number (comment-parts only) |
| `partTotal` | number? | Total parts in parent comment (comment-parts only) |
| `parentBody` | string? | Full parent comment (comment-parts only) |

### Reply

A reply within a thread conversation.

| Field | Type | Description |
|-------|------|-------------|
| `author` | string | GitHub login |
| `body` | string | Reply text |
| `created` | ISO 8601 | When reply was posted |

### Analysis

CC's assessment of the feedback.

| Field | Type | Description |
|-------|------|-------------|
| `action` | Action | Suggested action |
| `reason` | string | Why this action |
| `evidence` | string? | Commits, policies, code refs |
| `response` | string | What happens on GitHub |
| `note` | string? | Caveats, follow-up ideas |

### Response

User's decision (populated during review or from file).

| Field | Type | Description |
|-------|------|-------------|
| `enabled` | boolean | Whether to process this item (false = skip) |
| `action` | Action | Chosen action |
| `resolve` | boolean | Whether to resolve thread(s) |
| `emoji` | Emoji? | Reaction to add |
| `reply` | string? | Reply text to post |
| `commit` | string? | Commit SHA (filled after code change or for prior-fix) |

### Action

```typescript
type Action = "address" | "dismiss" | "prior-fix" | "defer" | "discuss"
```

| Action | Code change | Thread closed | Meaning |
|--------|-------------|---------------|---------|
| `address` | Yes | Yes | Valid feedback, implement fix |
| `dismiss` | No | Yes | Invalid/out-of-scope/noise |
| `prior-fix` | No | Yes | Already fixed in earlier work |
| `defer` | No | No | Too complex, handle manually later |
| `discuss` | TBD | TBD | Need conversation first |

### Emoji

```typescript
type Emoji = "thumbs_up" | "thumbs_down" | "laugh" | "hooray" | "confused" | "heart" | "rocket" | "eyes"
```

Maps to GitHub GraphQL `ReactionContent` enum.

## GitHub Node IDs

For API calls, items also carry node IDs (not shown in views):

| Field | Type | Used for |
|-------|------|----------|
| `prNodeId` | string | Reply target, summary comment |
| `threadNodeIds` | string[] | Resolve threads |
| `commentNodeIds` | string[] | Reactions, minimize |

## Lifecycle

```
Fetch → Item[] (no analysis/response)
      ↓
Analyze → Item[] (analysis populated)
      ↓
Generate files → .md files on disk
      ↓
User edits files (response populated)
      ↓
Parse files → Item[] (response from files)
      ↓
Apply → GitHub mutations executed
```
