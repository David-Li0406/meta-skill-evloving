---
name: gh-gist
description: Local-first workflow for iterative document building with GitHub gists
---

## What I do

- Guide local file creation and editing before pushing to gist
- Provide gh CLI commands for gist create/update/view operations
- Optimize for token efficiency by recommending Edit tool for iterations

## When to use me

Use this when building documents iteratively (analysis reports, proposals, design docs) that need
external sharing via gist. The local-first approach avoids full-content tool calls on every edit.

## Workflow

1. Create/edit file locally in workspace root or `/tmp/`
2. Use Edit tool for incremental changes (offset edits, not full rewrites)
3. Push to gist only when ready for external review

## Commands

### Create gist from local file

```sh
gh gist create <file> --desc "description"
gh gist create <file> --public --desc "description"
```

Returns gist URL on success.

### Update existing gist

```sh
gh gist edit <gist-id> --add <file>
```

The `<gist-id>` is the hash from the URL (e.g., `abc123def456` from
`https://gist.github.com/user/abc123def456`).

### View gist content

```sh
gh gist view <gist-id>
gh gist view <gist-id> --raw
```

### List your gists

```sh
gh gist list
gh gist list --public
gh gist list --secret
```

## Key Constraints

- Gists don't support partial updates - always full file replacement
- Use local Edit tool for iterations, not gist updates (token-efficient)
- Secret gists are unlisted but accessible to anyone with the URL
- Multi-file gists: `gh gist create file1.md file2.md`

## Example Session

```sh
# 1. Create local file (use Write tool)
# 2. Iterate with Edit tool (incremental changes)

# 3. When ready, create gist
gh gist create /tmp/analysis.md --desc "Q4 performance analysis"
# Returns: https://gist.github.com/user/abc123

# 4. After more local edits, update gist
gh gist edit abc123 --add /tmp/analysis.md
```
