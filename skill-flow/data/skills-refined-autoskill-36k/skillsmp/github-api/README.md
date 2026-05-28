# GitHub API Skill

Access plain text versions of GitHub content using URL transformations.

## What This Skill Does

Teaches Claude how to transform GitHub URLs into plain text formats:
- Pull requests → `.diff` or `.patch` files
- Commits → diffs and patches
- Files → raw content
- Comparisons → branch diffs
- Gists → raw content
- Feeds → Atom XML

## When to Use

Use this skill when:
- Users share GitHub URLs (PRs, commits, files)
- Performing code reviews
- Analyzing changes or diffs
- Reading file contents
- Comparing branches
- Monitoring releases or commits

## Quick Examples

```bash
# Pull Request Diff
https://github.com/owner/repo/pull/123
→ https://github.com/owner/repo/pull/123.diff

# Raw File Content
https://github.com/owner/repo/blob/main/README.md
→ https://raw.githubusercontent.com/owner/repo/main/README.md

# Commit Patch
https://github.com/owner/repo/commit/abc123
→ https://github.com/owner/repo/commit/abc123.patch

# Branch Comparison
https://github.com/owner/repo/compare/main...feature
→ https://github.com/owner/repo/compare/main...feature.diff

# Gist Raw
https://gist.github.com/user/123
→ https://gist.github.com/user/123/raw/
```

## Key Features

1. **Plain Text First** - Direct access without HTML scraping (when possible)
2. **Smart Fallback** - Falls back to HTML for errors or review comments
3. **No Authentication** - Works with public repos (raw content has no rate limits)
4. **Multiple Formats** - Choose diff, patch, raw, or feed formats
5. **Whitespace Control** - Add `?w=1` to ignore whitespace changes
6. **Line Numbers** - Use `#L10-L20` for specific line ranges

## Important Notes

**When to use HTML instead of plain text:**
- URL has fragment identifier (`#discussion_r123`, `#issuecomment-456`)
- .diff/.patch returns 403 Forbidden error
- Need review comments or discussion threads
- Want PR description and metadata

**Fragment identifiers require HTML:**
```bash
# Has fragment → Must use HTML
https://github.com/owner/repo/pull/123#discussion_r2506786717  ✅ HTML
https://github.com/owner/repo/pull/123.diff  ❌ Won't show comment

# No fragment → Try plain text first
https://github.com/owner/repo/pull/123  → Try .diff first
```

## URL Patterns

| Content Type | Original Pattern | Plain Text Pattern |
|--------------|------------------|-------------------|
| Pull Request | `/pull/123` | `/pull/123.diff` or `.patch` |
| Commit | `/commit/abc123` | `/commit/abc123.diff` or `.patch` |
| File Blob | `/blob/main/file.py` | `raw.githubusercontent.com/.../main/file.py` |
| Compare | `/compare/a...b` | `/compare/a...b.diff` or `.patch` |
| Gist | `gist.github.com/user/id` | Add `/raw/` suffix |
| Releases | `/releases` | `/releases.atom` |
| Commits | `/commits` | `/commits/branch.atom` |

## Workflow

When a user shares a GitHub URL:
1. **Check** for fragment identifiers (`#discussion_...`) → Use HTML if present
2. **Identify** the URL type (PR, commit, file, etc.)
3. **Transform** to plain text format (.diff, .patch, raw)
4. **Fetch** using Bash + curl (e.g., `curl -sS {url}`)
5. **Handle errors** - If 403: Fall back to HTML with curl
6. **Analyze** the content
7. **Respond** with insights

**Important:** This skill uses the Bash tool with `curl` for fetching content, not WebFetch. This works reliably in restricted environments.

## Documentation

See `SKILL.md` for complete documentation with:
- Detailed transformation patterns
- Practical examples
- Best practices
- Error handling
- API integration
- Decision trees
