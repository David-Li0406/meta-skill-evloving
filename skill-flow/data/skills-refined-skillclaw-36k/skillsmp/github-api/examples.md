# GitHub API Skill - Examples

Practical examples of using GitHub's plain text URL transformations.

## Example 1: Code Review (Simple PR)

**User Request:**
> "Can you review this PR? https://github.com/franklinbaldo/egregora/pull/600"

**Claude Workflow:**

1. **Check**: No fragment identifier → Try plain text
2. **Identify**: This is a pull request URL
3. **Transform**: Add `.diff` suffix
4. **Fetch**: Use Bash + curl:
   ```bash
   curl -sS https://github.com/franklinbaldo/egregora/pull/600.diff
   ```
5. **Handle errors**: If 403 → Fall back to HTML with curl
6. **Analyze**: Review the unified diff
7. **Respond**: Provide code review feedback

**Why `.diff` instead of `.patch`?**
- `.diff` is lighter weight (just the changes)
- `.patch` includes commit metadata (author, message, date)
- For code review, just the diff is usually sufficient

## Example 1b: PR Review Comment

**User Request:**
> "Check this review comment: https://github.com/franklinbaldo/egregora/pull/628#discussion_r2506786717"

**Claude Workflow:**

1. **Check**: Fragment identifier detected (`#discussion_r2506786717`) → Use HTML
2. **Fetch**: Use Bash + curl to get HTML page:
   ```bash
   curl -sS https://github.com/franklinbaldo/egregora/pull/628
   ```
3. **Analyze**: Extract PR info, code changes, and specific review comment
4. **Respond**: Provide context about the comment and related code

**Why HTML instead of `.diff`?**
- Review comments are only visible in the HTML page
- `.diff` format shows code changes but not discussion threads
- Fragment identifiers (`#discussion_...`) require HTML rendering

**Example response:**
```
PR #628: "Simplify avatar to accept only URL format"

The review comment (discussion_r2506786717) is a P1 priority issue from Codex:

Issue: The new `update_profile_avatar()` signature only accepts `avatar_url`
and timestamp, but existing callers still pass the old parameters (avatar_uuid,
avatar_path, moderation_status). This will cause TypeErrors.

Code context:
- File: profiler.py
- Function: update_profile_avatar()
- Change: Simplified from 5 params to 2 params (URL + timestamp)

Recommendation: Update all callers to use the new URL-only interface.
```

## Example 2: Understanding a File

**User Request:**
> "What does this file do? https://github.com/franklinbaldo/egregora/blob/main/src/egregora/privacy/anonymizer.py"

**Claude Workflow:**

1. **Identify**: This is a file blob URL
2. **Transform**:
   - Original: `github.com/franklinbaldo/egregora/blob/main/src/egregora/privacy/anonymizer.py`
   - Raw: `raw.githubusercontent.com/franklinbaldo/egregora/main/src/egregora/privacy/anonymizer.py`
3. **Fetch**: The raw Python file with curl:
   ```bash
   curl -sS https://raw.githubusercontent.com/franklinbaldo/egregora/main/src/egregora/privacy/anonymizer.py
   ```
4. **Analyze**: Read and understand the code
5. **Respond**: Explain the anonymizer's functionality

**Alternative**: Add `?raw=1` to the original URL (redirects to raw.githubusercontent.com)

## Example 3: Comparing Branches

**User Request:**
> "What's different between main and my feature branch?"

**Claude Workflow:**

1. **Create compare URL**:
   ```
   https://github.com/franklinbaldo/egregora/compare/main...feature-branch
   ```
2. **Transform**: Add `.diff`
   ```
   https://github.com/franklinbaldo/egregora/compare/main...feature-branch.diff
   ```
3. **Fetch**: The complete diff with curl:
   ```bash
   curl -sS https://github.com/franklinbaldo/egregora/compare/main...feature-branch.diff
   ```
4. **Analyze**: Summarize changes by file
5. **Respond**: Explain what changed

**With whitespace ignored:**
```
https://github.com/franklinbaldo/egregora/compare/main...feature-branch.diff?w=1
```

## Example 4: Investigating a Commit

**User Request:**
> "What did commit dee113a do?"

**Claude Workflow:**

1. **Identify**: This is a commit SHA
2. **Create URL**:
   ```
   https://github.com/franklinbaldo/egregora/commit/dee113a
   ```
3. **Transform**: Add `.patch` (to get metadata)
   ```
   https://github.com/franklinbaldo/egregora/commit/dee113a.patch
   ```
4. **Fetch**: Patch file with curl (includes commit message, author, date):
   ```bash
   curl -sS https://github.com/franklinbaldo/egregora/commit/dee113a.patch
   ```
5. **Analyze**: Parse the changes
6. **Respond**: Explain the commit's purpose

**Why `.patch` instead of `.diff`?**
- Includes commit message (explains the "why")
- Shows author and date
- Better context for understanding the change

## Example 5: Reading Configuration

**User Request:**
> "What's in your pyproject.toml?"

**Claude Workflow:**

1. **Create blob URL**:
   ```
   https://github.com/franklinbaldo/egregora/blob/main/pyproject.toml
   ```
2. **Transform to raw**:
   ```
   https://raw.githubusercontent.com/franklinbaldo/egregora/main/pyproject.toml
   ```
3. **Fetch**: Raw TOML content with curl:
   ```bash
   curl -sS https://raw.githubusercontent.com/franklinbaldo/egregora/main/pyproject.toml
   ```
4. **Analyze**: Parse configuration
5. **Respond**: Explain dependencies and settings

## Example 6: Gist Analysis

**User Request:**
> "Check out this script: https://gist.github.com/user/abc123"

**Claude Workflow:**

1. **Identify**: This is a gist URL
2. **Transform**:
   ```
   https://gist.github.com/user/abc123/raw/
   ```
   Or for specific file:
   ```
   https://gist.githubusercontent.com/user/abc123/raw/script.py
   ```
3. **Fetch**: Raw content with curl:
   ```bash
   curl -sS https://gist.github.com/user/abc123/raw/
   ```
4. **Analyze**: Review the code
5. **Respond**: Provide feedback

## Example 7: Markdown Source

**User Request:**
> "Is there a typo in line 42 of your README?"

**Claude Workflow:**

1. **Create blob URL**:
   ```
   https://github.com/franklinbaldo/egregora/blob/main/README.md
   ```
2. **Transform with line numbers**:
   ```
   https://github.com/franklinbaldo/egregora/blob/main/README.md?plain=1#L40-L45
   ```
3. **Fetch**: HTML page with curl (fragment requires HTML):
   ```bash
   curl -sS "https://github.com/franklinbaldo/egregora/blob/main/README.md?plain=1#L40-L45"
   ```
4. **Analyze**: Check for typos
5. **Respond**: Confirm or correct

**Why `?plain=1`?**
- Shows source markdown (not rendered HTML)
- Line numbers are accurate
- Can link to specific lines

## Example 8: Release Monitoring

**User Request:**
> "What are the recent releases?"

**Claude Workflow:**

1. **Create feed URL**:
   ```
   https://github.com/franklinbaldo/egregora/releases.atom
   ```
2. **Fetch**: Atom XML feed with curl:
   ```bash
   curl -sS https://github.com/franklinbaldo/egregora/releases.atom
   ```
3. **Parse**: Extract release names, dates, descriptions
4. **Respond**: Summarize recent releases

**Useful for:**
- Monitoring dependencies
- Tracking project updates
- Building release notifications
- RSS/feed readers

## Example 9: Commit History

**User Request:**
> "What are the latest commits on the main branch?"

**Claude Workflow:**

1. **Create feed URL**:
   ```
   https://github.com/franklinbaldo/egregora/commits/main.atom
   ```
2. **Fetch**: Atom XML feed of commits with curl:
   ```bash
   curl -sS https://github.com/franklinbaldo/egregora/commits/main.atom
   ```
3. **Parse**: Extract commit messages, authors, dates
4. **Respond**: List recent activity

**Per branch:**
```
# Main branch
/commits/main.atom

# Feature branch
/commits/feature-branch.atom

# Release branch
/commits/release-v1.0.atom
```

## Example 10: Whitespace-Clean Diff

**User Request:**
> "Show me the real changes, ignore formatting"

**Claude Workflow:**

1. **Get PR URL**:
   ```
   https://github.com/franklinbaldo/egregora/pull/600
   ```
2. **Transform with whitespace filter**:
   ```
   https://github.com/franklinbaldo/egregora/pull/600.diff?w=1
   ```
3. **Fetch**: Diff without whitespace changes with curl:
   ```bash
   curl -sS "https://github.com/franklinbaldo/egregora/pull/600.diff?w=1"
   ```
4. **Analyze**: Focus on logic changes only
5. **Respond**: Explain substantive changes

**Why `?w=1`?**
- Ignores indentation changes
- Filters out formatting commits
- Shows only meaningful code changes
- Useful for repos with mixed tabs/spaces

## Complete URL Transformation Reference

```bash
# Pull Requests
https://github.com/owner/repo/pull/123
→ https://github.com/owner/repo/pull/123.diff        # Unified diff
→ https://github.com/owner/repo/pull/123.patch       # With metadata
→ https://github.com/owner/repo/pull/123.diff?w=1    # Ignore whitespace

# Commits
https://github.com/owner/repo/commit/abc123
→ https://github.com/owner/repo/commit/abc123.diff
→ https://github.com/owner/repo/commit/abc123.patch

# Files
https://github.com/owner/repo/blob/main/file.py
→ https://raw.githubusercontent.com/owner/repo/main/file.py
→ https://github.com/owner/repo/blob/main/file.py?raw=1  # Redirects

# Comparisons
https://github.com/owner/repo/compare/main...feature
→ https://github.com/owner/repo/compare/main...feature.diff
→ https://github.com/owner/repo/compare/main...feature.patch
→ https://github.com/owner/repo/compare/main...feature.diff?w=1

# Gists
https://gist.github.com/user/abc123
→ https://gist.github.com/user/abc123/raw/                    # Latest
→ https://gist.githubusercontent.com/user/abc123/raw/file.py  # Specific

# Markdown
https://github.com/owner/repo/blob/main/README.md
→ https://github.com/owner/repo/blob/main/README.md?plain=1           # Unrendered
→ https://github.com/owner/repo/blob/main/README.md?plain=1#L10-L20   # Lines 10-20

# Feeds
https://github.com/owner/repo
→ https://github.com/owner/repo/releases.atom         # Releases
→ https://github.com/owner/repo/commits/main.atom     # Commits
```

## Decision Matrix

| User Request | URL Type | Transform | Format | Reason |
|--------------|----------|-----------|--------|--------|
| "Review this PR" | Pull Request | Add `.diff` | Diff | Code changes only |
| "What changed in this commit?" | Commit | Add `.patch` | Patch | Need commit message |
| "Read this file" | Blob | Convert to raw | Raw | Direct content |
| "Compare branches" | N/A | Create compare + `.diff` | Diff | Show differences |
| "Check this gist" | Gist | Add `/raw/` | Raw | Script content |
| "Is there a typo?" | Blob (markdown) | Add `?plain=1#L...` | Plain | Exact source |
| "Recent releases?" | Repo | Add `/releases.atom` | Atom | Structured feed |
| "Latest commits?" | Repo | Add `/commits/branch.atom` | Atom | Commit history |

## Common Patterns

### Pattern 1: PR Review
```
User shares PR → Add .diff → Fetch → Analyze → Review
```

### Pattern 2: File Reading
```
User shares file → Convert to raw → Fetch → Read → Explain
```

### Pattern 3: Commit Investigation
```
User shares commit → Add .patch → Fetch → Parse → Summarize
```

### Pattern 4: Branch Comparison
```
User mentions branches → Create compare URL → Add .diff → Fetch → Summarize
```

### Pattern 5: Configuration Check
```
User asks about config → Find file → Convert to raw → Fetch → Parse → Explain
```

## Tips for Claude

1. **Always transform first** - Don't try to parse HTML
2. **Choose the right format**:
   - `.diff` for code changes
   - `.patch` for metadata + changes
   - `raw` for complete files
   - `?plain=1` for markdown source
   - `.atom` for feeds
3. **Use `?w=1`** - When formatting noise is hiding real changes
4. **Fetch efficiently** - Raw URLs have no rate limits
5. **Context matters**:
   - Code review → `.diff`
   - Understanding history → `.patch`
   - Reading files → `raw`
   - Checking syntax → `?plain=1`

## Testing Your Transformations

Try these URLs yourself:

```bash
# Small PR (easy to test)
https://github.com/franklinbaldo/egregora/pull/600.diff

# Recent commit
https://github.com/franklinbaldo/egregora/commit/dee113a.patch

# README file
https://raw.githubusercontent.com/franklinbaldo/egregora/main/README.md

# Compare branches (if you have a feature branch)
https://github.com/franklinbaldo/egregora/compare/main...feature.diff

# Releases
https://github.com/franklinbaldo/egregora/releases.atom
```

## Summary

GitHub makes it easy to access plain text content—you just need to know the URL patterns. This skill teaches Claude to automatically transform user-provided URLs into the most useful format for analysis.

**Key takeaway**: When a user shares a GitHub URL, don't visit it directly. Transform it first, fetch the plain text, then analyze!
