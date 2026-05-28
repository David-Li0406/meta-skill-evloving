# Git Commit Message Format

## Commit Message Structure

Use the **Conventional Commits** format:

```
type(scope): description

[optional body]

[optional footer]
```

### Type

Must be one of the following:

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning (formatting, whitespace, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding or modifying tests
- **build**: Changes to build system or dependencies
- **ci**: Changes to CI configuration files and scripts
- **chore**: Other changes that don't modify src or test files

### Scope

- **Optional but recommended**: Specify the component or module affected
- **Examples**: `network`, `database`, `ui`, `auth`, `api`
- **Format**: Lowercase, single word or hyphenated phrase

### Description

- **Language**: English only
- **Tense**: Imperative mood (e.g., "add", not "added" or "adds")
- **Length**: 50 characters or less
- **Capitalization**: Lowercase first letter
- **No period**: Don't end with a period

### Body (Optional)

- **Purpose**: Explain what and why, not how
- **Line length**: Wrap at 72 characters
- **Separation**: Blank line between description and body

### Footer (Optional)

- **Breaking changes**: `BREAKING CHANGE: description`
- **Issue references**: `Closes #123`, `Fixes #456`

## AI Reference Policy

**Remove all AI-related references** from commit messages:

❌ **Don't include**:
- "🤖 Generated with Claude Code"
- "Generated with Claude Code"
- "Co-Authored-By: Claude <noreply@anthropic.com>"
- "Co-Authored-By: Claude"
- Any AI assistant mentions
- Tool attribution in commit messages
- **All emojis** (🔧, 📊, ✅, 🚀, etc.)

✅ **Do include**:
- Actual technical changes
- Business rationale
- Issue/ticket references
- Plain text descriptions without decorative symbols

## Examples

### Good Commit Messages

```
feat(auth): add JWT token refresh mechanism

Implement automatic token refresh before expiration to improve
user experience and reduce re-authentication requests.

Closes #234
```

```
fix(network): resolve connection timeout on slow networks

Increase default timeout from 5s to 30s and add retry logic
with exponential backoff.
```

```
refactor(database): simplify query builder interface

Remove redundant methods and consolidate common patterns.
This improves maintainability without changing functionality.
```

### Bad Commit Messages

```
❌ update stuff
❌ Fixed bug
❌ WIP
❌ minor changes
❌ Added new feature for user authentication 🤖 Generated with Claude Code
❌ feat(auth): add JWT token refresh 🚀
❌ fix: resolve timeout issue ✅
❌ refactor(db): improve performance 🔧

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Why these are bad**:
- No proper type/format
- Capitalization errors
- Contains emojis
- Contains Claude attribution
- Too vague or generic

## Git User Identity

Use the git identity configured on your system. See `~/.claude/git-identity.md` for details.

Claude Code automatically detects and uses your system's git configuration:
```bash
git config user.name   # Your configured name
git config user.email  # Your configured email
```

## Automated Claude Reference Removal

### Git Hook Setup

To automatically remove Claude-related content from commit messages, set up a `commit-msg` hook:

**Create the hook**:
```bash
# Create hooks directory if it doesn't exist
mkdir -p .git/hooks

# Create commit-msg hook
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
# Remove Claude-related references and emojis from commit messages

COMMIT_MSG_FILE=$1

# Remove Claude Code attribution
sed -i '' '/🤖 Generated with \[Claude Code\]/d' "$COMMIT_MSG_FILE"
sed -i '' '/Generated with Claude Code/d' "$COMMIT_MSG_FILE"

# Remove Co-Authored-By: Claude
sed -i '' '/Co-Authored-By: Claude/d' "$COMMIT_MSG_FILE"

# Remove common AI assistant references
sed -i '' '/AI-assisted/d' "$COMMIT_MSG_FILE"
sed -i '' '/Anthropic Claude/d' "$COMMIT_MSG_FILE"
sed -i '' '/claude.ai/d' "$COMMIT_MSG_FILE"

# Remove all emojis (Unicode ranges for common emojis)
perl -i -pe 's/[\x{1F300}-\x{1F9FF}]|[\x{2600}-\x{26FF}]|[\x{2700}-\x{27BF}]|[\x{1F1E0}-\x{1F1FF}]//g' "$COMMIT_MSG_FILE"

# Remove empty lines at the end
sed -i '' -e :a -e '/^\s*$/d;N;ba' "$COMMIT_MSG_FILE"
EOF

# Make executable
chmod +x .git/hooks/commit-msg
```

**For Linux/WSL** (use `sed -i` instead of `sed -i ''`):
```bash
cat > .git/hooks/commit-msg << 'EOF'
#!/bin/bash
# Remove Claude-related references and emojis from commit messages

COMMIT_MSG_FILE=$1

sed -i '/🤖 Generated with \[Claude Code\]/d' "$COMMIT_MSG_FILE"
sed -i '/Generated with Claude Code/d' "$COMMIT_MSG_FILE"
sed -i '/Co-Authored-By: Claude/d' "$COMMIT_MSG_FILE"
sed -i '/AI-assisted/d' "$COMMIT_MSG_FILE"
sed -i '/Anthropic Claude/d' "$COMMIT_MSG_FILE"
sed -i '/claude.ai/d' "$COMMIT_MSG_FILE"

# Remove all emojis
perl -i -pe 's/[\x{1F300}-\x{1F9FF}]|[\x{2600}-\x{26FF}]|[\x{2700}-\x{27BF}]|[\x{1F1E0}-\x{1F1FF}]//g' "$COMMIT_MSG_FILE"

sed -i -e :a -e '/^\s*$/d;N;ba' "$COMMIT_MSG_FILE"
EOF

chmod +x .git/hooks/commit-msg
```

### CI/CD Verification

Add this check to your CI pipeline to ensure no Claude references slip through:

```yaml
# .github/workflows/commit-verification.yml
name: Verify Commit Messages

on: [push, pull_request]

jobs:
  verify-commits:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check for Claude references and emojis
        run: |
          # Check last 10 commits for Claude references
          if git log -10 --pretty=format:"%B" | grep -i -E "(claude|anthropic|ai-assisted|co-authored-by: claude)"; then
            echo "ERROR: Found Claude references in commit messages"
            exit 1
          fi

          # Check for emojis (using perl to detect Unicode emoji ranges)
          if git log -10 --pretty=format:"%B" | perl -ne 'exit 1 if /[\x{1F300}-\x{1F9FF}]|[\x{2600}-\x{26FF}]|[\x{2700}-\x{27BF}]|[\x{1F1E0}-\x{1F1FF}]/'; then
            echo "ERROR: Found emojis in commit messages"
            exit 1
          fi

          echo "No Claude references or emojis found"
```

### Pre-commit Hook Template

For teams, provide a template that can be shared:

```bash
# scripts/setup-git-hooks.sh
#!/bin/bash

HOOKS_DIR=".git/hooks"
COMMIT_MSG_HOOK="$HOOKS_DIR/commit-msg"

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]] || [[ "$OSTYPE" == "freebsd"* ]]; then
    SED_INPLACE="sed -i ''"
else
    SED_INPLACE="sed -i"
fi

cat > "$COMMIT_MSG_HOOK" << 'HOOKEOF'
#!/bin/bash
# Auto-remove Claude references and emojis from commit messages

COMMIT_MSG_FILE=$1

# Pattern list
PATTERNS=(
    "🤖 Generated with \[Claude Code\]"
    "Generated with Claude Code"
    "Co-Authored-By: Claude"
    "AI-assisted"
    "Anthropic Claude"
    "claude.ai"
    "claude code"
)

# Remove each pattern
for pattern in "${PATTERNS[@]}"; do
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "/$pattern/d" "$COMMIT_MSG_FILE"
    else
        sed -i "/$pattern/d" "$COMMIT_MSG_FILE"
    fi
done

# Remove all emojis (Unicode ranges for common emojis)
perl -i -pe 's/[\x{1F300}-\x{1F9FF}]|[\x{2600}-\x{26FF}]|[\x{2700}-\x{27BF}]|[\x{1F1E0}-\x{1F1FF}]//g' "$COMMIT_MSG_FILE"

# Remove trailing empty lines
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' -e :a -e '/^\s*$/d;N;ba' "$COMMIT_MSG_FILE"
else
    sed -i -e :a -e '/^\s*$/d;N;ba' "$COMMIT_MSG_FILE"
fi
HOOKEOF

chmod +x "$COMMIT_MSG_HOOK"
echo "✓ Git hooks installed successfully"
```

**Install hooks for all team members**:
```bash
chmod +x scripts/setup-git-hooks.sh
./scripts/setup-git-hooks.sh
```

## Verification

Before committing, verify:

```bash
# Check commit message format
git log --oneline -1

# Verify author
git log -1 --format='%an <%ae>'

# Verify no Claude references
git log -1 --pretty=format:"%B" | grep -i "claude\|anthropic\|ai-assisted"
# Should return nothing (exit code 1)
```

Expected author: Your configured git identity (`git config user.name` / `git config user.email`)
Expected result: No Claude references in commit message
