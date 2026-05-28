# File View

How Items are serialized to markdown files for user review and editing.

## Directory Structure

```
<tmp>/<owner>-<repo>/<pr>/<date>/
├── 01-null-check-missing.md
├── 02-type-cast-needed.md
├── 03-aria-labels.md
└── ...
```

- `<owner>-<repo>`: Repository identifier
- `<pr>`: PR number
- `<date>`: Session date (YYYY-MM-DD)
- Filename: `<NN>-<gist-slug>.md` where NN is zero-padded item id

## File Format

### Frontmatter

```yaml
---
item: 1
type: threads
urls:
  - https://github.com/owner/repo/pull/123#discussion_r456
  - https://github.com/owner/repo/pull/123#discussion_r789
authors: [copilot]
created: 2026-01-16T10:30:00Z
outdated: false
---
```

| Field      | Source              | Notes                            |
| ---------- | ------------------- | -------------------------------- |
| `item`     | Item.id             | Item number                      |
| `type`     | Item.type           | `threads` or `comment-part`      |
| `urls`     | Feedback[].url      | All feedback URLs                |
| `authors`  | Feedback[].author   | Unique authors                   |
| `created`  | Feedback[0].created | Earliest feedback timestamp      |
| `outdated` | Feedback[].outdated | True if any feedback is outdated |

For comment-parts, add:

```yaml
part: 1
partTotal: 3
```

### Feedback Section

````markdown
# Feedback

## <gist>

@<author> · <file>:<line> · [link](url)

> <body>

```diff
<diffHunk>
```
````

### <reply author>

> <reply body>

````

**Threads:** Include file, line, diffHunk, and any replies.

**Comment-parts:** No file/line/diffHunk. Show parent body then "This part:" with extracted body.

```markdown
# Feedback

## Add loading state

@reviewer · [link](url)

Full comment:
> Can we add a loading state? Also the error handling
> seems incomplete. And should we add types?

This part:
> Can we add a loading state?
````

### Analysis Section

```markdown
# Analysis

ADDRESS

- reason: Valid - null check is missing before property access
- evidence: Line 45 accesses user.name without guard
- response: Fix, resolve with thumbs up
- note: Consider adding similar check on line 52
```

Fields map directly from Analysis schema. Omit fields with no value.

### Response Section

````markdown
# Response

```yaml
enabled: true
action: address
resolve: true
emoji: thumbs_up
reply: |
  Added null checks before property access.
commit: null
```
````

User notes here are ignored by apply.
Can discuss reasoning, alternatives, etc.

```

The yaml codeblock is the machine-readable config. Text after it is for human notes.

**Response fields:**

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `enabled` | boolean | `true` | Set `false` to skip without deleting file |
| `action` | Action | from analysis | User's chosen action |
| `resolve` | boolean | `true` | Whether to resolve thread(s) |
| `emoji` | Emoji | `thumbs_up` | Reaction to add |
| `reply` | string | from analysis | Reply text (use `null` for no reply) |
| `commit` | string | `null` | Filled by CC after code change, or manually for prior-fix |

## Parsing Rules

1. Parse YAML frontmatter between `---` markers
2. Extract `# Feedback` section (informational, not parsed back to model)
3. Extract `# Analysis` section (informational, not parsed back to model)
4. Extract `# Response` section, find yaml codeblock
5. Parse yaml codeblock as Response
6. Ignore text outside/after yaml codeblock

## Serialization Notes

- Frontmatter uses YAML flow style for arrays: `urls: [url1, url2]`
- Body text uses blockquotes with `>` prefix
- Diff hunks use fenced code blocks with `diff` language
- Response yaml uses block style for `reply:` (multiline)
- Gist generation: First ~40 chars of first feedback body, or summarize if too long/unclear
```
