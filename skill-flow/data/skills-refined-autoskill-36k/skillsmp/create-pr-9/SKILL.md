---
name: create-pr
description: Creates GitHub pull requests following project conventions. Use when the user wants to create a PR, open a pull request, or publish their changes for review.
allowed-tools: [Bash, Read, Grep]
---

# Create Pull Request Skill

Assists with creating GitHub pull requests that follow this project's conventions for PR titles, descriptions, and submission workflow.

## Instructions

**IMPORTANT: When using this skill, announce to the user**: "Using create-pr skill to create a pull request following project conventions."

### 1. Prerequisites Check

Before creating a PR, verify:

```bash
# Check current branch
git branch --show-current

# Verify commits are ready
git log origin/main..HEAD --oneline

# Ensure branch is pushed to remote
git status
```

If branch is not pushed:
```bash
git push -u origin branch-name
```

### 2. Using gh CLI

**ALWAYS use the `gh` CLI tool** for creating pull requests. Never use the web interface through automation.

### 3. PR Title Format

PR titles MUST follow the same format as commit messages:

- **ALWAYS write in English**
- Start with GitHub emoji code (`:emoji:`)
- Use imperative mood
- Be clear and descriptive
- No period at end

**Example**: `:sparkles: Add user authentication system`

### 4. PR Body Creation Methods

**CRITICAL: Choose one of these two methods. Never use inline `--body` with complex content.**

#### Method 1: Temporary File (RECOMMENDED)

```bash
# Create temporary file for PR body
cat > /tmp/pr_body.md <<'EOF'
## Summary
Brief 1-2 sentence description of what this PR does

## Changes
- Key change 1
- Key change 2
- Key change 3

## Test Plan
How to verify the changes work correctly
EOF

# Create PR using temp file
gh pr create --title ":emoji: Clear descriptive title" --body-file /tmp/pr_body.md

# Clean up
rm /tmp/pr_body.md
```

#### Method 2: Inline (simple content only)

```bash
gh pr create --title ":emoji: Update feature" --body "Brief description of changes"
```

### 5. PR Body Structure

**Required sections**:

```markdown
## Summary
Brief 1-2 sentence overview of what this PR accomplishes

## Changes
- Key change 1 (be concise)
- Key change 2
- Key change 3 (max 4-5 items)
```

**Optional sections** (add as needed):

```markdown
## Before
Description or code snippet of previous behavior

## After
Description or code snippet of new behavior

## Test Plan
Steps to verify the changes:
1. Step 1
2. Step 2

## Related Issues
Fixes #123
Related to #456
```

### 6. Content Guidelines

**Language**:
- **ALWAYS write in English** (both title and body)

**Brevity**:
- Summary: 1-2 sentences maximum
- Changes: 2-5 key items, avoid exhaustive lists
- Focus on WHAT changed and WHY, not HOW

**Issue References**:
- Use `Fixes #123` or `Closes #123` to auto-close issues
- Use `Related to #456` for references without closing

**Code Examples**:
- Use markdown code blocks with language tags
- Show before/after for behavior changes
- Keep examples minimal and focused

### 7. Complete Workflow

```bash
# 1. Verify branch and commits
git status
git log origin/main..HEAD --oneline

# 2. Ensure branch is pushed
git push -u origin branch-name

# 3. Prepare PR body
cat > /tmp/pr_body.md <<'EOF'
## Summary
Add user authentication with JWT tokens

## Changes
- Implement JWT-based authentication
- Add login/logout endpoints
- Create user session management

## Test Plan
- Run `npm test`
- Verify login at /api/auth/login
- Check token validation

Fixes #42
EOF

# 4. Create PR
gh pr create \
  --title ":sparkles: Add user authentication system" \
  --body-file /tmp/pr_body.md

# 5. Clean up
rm /tmp/pr_body.md
```

## Examples

### Example 1: Bug Fix PR

```bash
cat > /tmp/pr_body.md <<'EOF'
## Summary
Fix memory leak in cache invalidation logic

## Changes
- Properly dispose event listeners after cache clear
- Add cleanup in component unmount

## Test Plan
- Run test suite: `npm test`
- Verify no memory growth after 1000 cache clears

Fixes #123
EOF

gh pr create \
  --title ":bug: Fix memory leak in cache invalidation" \
  --body-file /tmp/pr_body.md

rm /tmp/pr_body.md
```

### Example 2: New Feature PR

```bash
cat > /tmp/pr_body.md <<'EOF'
## Summary
Add dark mode support to the application

## Changes
- Implement theme context and provider
- Add dark mode toggle component
- Update all components with theme-aware styles

## Test Plan
1. Toggle dark mode in settings
2. Verify all pages render correctly
3. Check theme persistence across sessions
EOF

gh pr create \
  --title ":sparkles: Add dark mode support" \
  --body-file /tmp/pr_body.md

rm /tmp/pr_body.md
```

### Example 3: Documentation Update

```bash
cat > /tmp/pr_body.md <<'EOF'
## Summary
Update API documentation with new authentication endpoints

## Changes
- Document JWT authentication flow
- Add examples for login/logout endpoints
- Update authentication section
EOF

gh pr create \
  --title ":memo: Update API documentation" \
  --body-file /tmp/pr_body.md

rm /tmp/pr_body.md
```

### Example 4: Performance Improvement

```bash
cat > /tmp/pr_body.md <<'EOF'
## Summary
Optimize database queries to reduce response time

## Changes
- Add database indexes on frequently queried columns
- Implement query result caching
- Use eager loading to prevent N+1 queries

## Before
- Average response time: 850ms
- 15-20 database queries per request

## After
- Average response time: 120ms
- 2-3 database queries per request

## Test Plan
- Run benchmark suite: `npm run benchmark`
- Verify all integration tests pass
EOF

gh pr create \
  --title ":zap: Optimize database query performance" \
  --body-file /tmp/pr_body.md

rm /tmp/pr_body.md
```

## Common Pitfalls to Avoid

1. **Don't use non-English**: All PR content must be in English
2. **Don't use inline --body with complex content**: Always use temp file or heredoc
3. **Don't use unquoted heredoc**: Always use `<<'EOF'` not `<<EOF`
4. **Don't use raw emojis in title**: Use `:bug:` not 🐛
5. **Don't write verbose descriptions**: Keep it concise and focused
6. **Don't forget to push branch**: PR creation fails if branch isn't on remote
7. **Don't skip issue references**: Link related issues with Fixes/Closes
8. **Don't list every file changed**: Focus on key functional changes

## Shell Safety Rules

**FORBIDDEN - These will fail or corrupt your PR**:
```bash
# ❌ NEVER use inline --body with backticks or special characters
gh pr create --title "Title" --body "Content with `backticks`"

# ❌ NEVER use unquoted heredoc
gh pr create --title "Title" --body "$(cat <<EOF
Unquoted causes variable expansion
EOF
)"

# ❌ NEVER use complex markdown inline
gh pr create --title "Title" --body "## Summary\n- Item 1\n- Item 2"
```

**REQUIRED - Use these patterns**:
```bash
# ✅ ALWAYS use temporary file for complex content
cat > /tmp/pr_body.md <<'EOF'
Your content here with `backticks` and markdown
EOF
gh pr create --title "Title" --body-file /tmp/pr_body.md
rm /tmp/pr_body.md
```

## Error Recovery

### Issue: Branch not found on remote

**Error**: `Pull request create failed: head ref not found`

**Solution**:
```bash
git push -u origin your-branch-name
```

### Issue: Backticks or special characters cause errors

**Solution**: Use temporary file method (Method 1) or ensure heredoc is quoted with `<<'EOF'`

### Issue: gh command not found

**Solution**: Install GitHub CLI:
- macOS: `brew install gh`
- Linux: See https://github.com/cli/cli#installation
- Authenticate: `gh auth login`

### Issue: PR body appears malformed

**Solution**: Always use `<<'EOF'` (with single quotes) to prevent shell variable expansion

## Best Practices

1. **Review changes first**: Use `git log` and `git diff origin/main` before creating PR
2. **Keep PRs focused**: One logical feature or fix per PR
3. **Write clear summaries**: Help reviewers understand the purpose quickly
4. **Link issues**: Always reference related issues for traceability
5. **Test before PR**: Ensure all tests pass locally
6. **Use meaningful titles**: Follow emoji conventions and be descriptive
7. **Keep descriptions concise**: Reviewers appreciate brevity
8. **Include test plan**: Make it easy for reviewers to verify changes
