# HEREDOC Quoting in Bash

| Field | Value |
|-------|-------|
| **Created** | 2026-01-14 |
| **Sources** | 4 retrospectives (2026-01-09, 2026-01-12, 2026-01-14) |
| **Tags** | `bash` `heredoc` `security` `shell` |

---

## Key Insight

> Use quoted heredoc `<<'EOF'` when content may contain variables or special characters to prevent unintended expansion; use unquoted `<<EOF` only when you explicitly need variable substitution.

---

## The Problem

| Attempt | Result |
|---------|--------|
| `<<EOF` with `$variable` | Variable gets expanded unexpectedly |
| `<<EOF` with backticks | Command execution (security risk!) |
| `<<EOF` with user input | Shell injection vulnerability |

### Example Problem

```bash
# User comment contains: "Use $HOME for path"
gh api repos/owner/repo/pulls/1/comments/123/replies \
  -f body="Fixed! $HOME is now /Users/john"  # WRONG - $HOME expanded!
```

---

## The Solution

### Pattern: Quoted HEREDOC

```bash
# Safe - no expansion
cat <<'EOF'
This $variable will NOT be expanded
Backticks `command` will NOT execute
EOF
```

### Pattern: Unquoted HEREDOC (when expansion needed)

```bash
# Expansion happens
COMMIT_HASH=$(git rev-parse --short HEAD)
cat <<EOF
Fixed in commit $COMMIT_HASH
EOF
```

### Pattern: Safe API Calls with User Content

```bash
# Step 1: Store content in file
echo "$USER_CONTENT" > /tmp/reply.txt

# Step 2: Use -F flag with file
gh api repos/owner/repo/pulls/1/comments/123/replies \
  -F body=@/tmp/reply.txt

# Step 3: Cleanup
rm /tmp/reply.txt
```

### Pattern: Mixed - Static Template with Variables

```bash
COMMIT_HASH=$(git rev-parse --short HEAD)
ISSUE_NUM=42

# Unquoted heredoc - allows variable expansion of known-safe values
cat <<EOF
Fixed in ${COMMIT_HASH}!

Related: #${ISSUE_NUM}
EOF
```

**Why unquoted works here:**
- Variables are from controlled sources (git, hardcoded)
- No user input in the template
- Expansion is intentional and safe

**Why quoted `<<'EOF'` works for security:**
- Treats content as literal string
- No shell interpretation of special characters
- Prevents accidental code execution
- Safe for untrusted user input

---

## Anti-Patterns

| Don't Do This | Do This Instead |
|---------------|-----------------|
| `<<EOF` with user input | `<<'EOF'` or file-based approach |
| `-f body="$USER_INPUT"` | `-F body=@file` |
| String interpolation in JSON | `jq --arg` for safe JSON |
| Inline heredoc in gh commands | Temp file approach |

### Security Risk Example

```bash
# DANGEROUS - user could inject: $(rm -rf /)
gh issue comment 1 --body "$(cat <<EOF
User said: $USER_COMMENT
EOF
)"

# SAFE
gh issue comment 1 --body "$(cat <<'EOF'
User said: literal content here
EOF
)"
```

---

## When to Apply

### Use `<<'EOF'` (Quoted)
- Content from external sources (API responses, user input)
- PR review comments
- Any content with `$`, backticks, or special chars
- Default choice when unsure

### Use `<<EOF` (Unquoted)
- Need to embed variables (commit hash, date, etc.)
- Generating dynamic content from known-safe values
- Template with placeholders you control

---

## Quick Reference

| Syntax | Variables | Commands | Use When |
|--------|-----------|----------|----------|
| `<<'EOF'` | No expand | No execute | User content, security |
| `<<EOF` | Expand | Execute | Dynamic templates |
| `<<\EOF` | No expand | No execute | Same as quoted |

---

## Related

### Source Retrospectives
- `docs/retrospective/2026-01/retrospective_2026-01-09_182730.md`
- `docs/retrospective/2026-01/retrospective_2026-01-09_193400.md`
- `docs/retrospective/2026-01/retrospective_2026-01-09_203700.md`
- `docs/retrospective/2026-01/12/retrospective_2026-01-12_114152.md`

### Code References
- `assets/commands/pr-review.md` - Uses safe heredoc patterns
- `scripts/notify.sh` - Input sanitization example
