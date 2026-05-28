# Git Workflow Scripts

This directory contains utility scripts for git workflow automation.

## Scripts

### validate_commit_msg.py

Validates commit messages against the Conventional Commits specification.

**Usage**:
```bash
# Validate a commit message string
python validate_commit_msg.py "feat(auth): add OAuth login"

# Validate from file (useful for git hooks)
python validate_commit_msg.py --file .git/COMMIT_EDITMSG

# Validate from stdin
echo "feat: add feature" | python validate_commit_msg.py --stdin

# Non-strict mode (warnings only)
python validate_commit_msg.py --no-strict "feat(auth): add OAuth login"
```

**Validation Rules**:
- ✅ Header matches format: `<type>(<scope>): <subject>`
- ✅ Type is valid: feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert
- ✅ Subject ≤50 characters
- ✅ Subject doesn't end with period
- ✅ Subject uses imperative mood (not past tense)
- ✅ Body lines wrap at 72 characters

**Example**:
```bash
$ python validate_commit_msg.py "feat(auth): add OAuth2 login support"
✅ Commit message is valid

$ python validate_commit_msg.py "Added new feature"
❌ Validation failed:

  ERROR: Header does not match Conventional Commits format: 'Added new feature'
  Expected: <type>(<scope>): <subject>
  Example: feat(auth): add OAuth login
```

### generate_commit_msg.py

Generates commit messages from staged git changes.

**Usage**:
```bash
# Generate commit message from staged changes
python generate_commit_msg.py

# Generate header only (no body)
python generate_commit_msg.py --no-body

# Include Claude Code attribution
python generate_commit_msg.py --include-claude-footer

# Show generated message without committing
python generate_commit_msg.py --dry-run
```

**Features**:
- Analyzes staged changes with `git diff --cached`
- Determines commit type from file patterns and diff content
- Extracts scope from directory structure
- Generates appropriate subject line
- Optionally includes body with file list and stats
- Optionally includes Claude Code attribution footer

**Example**:
```bash
$ git add src/auth/oauth.ts src/types/auth.ts
$ python generate_commit_msg.py

Generated commit message:
============================================================
feat(auth): add oauth module

Changes across 2 files:
- src/auth/oauth.ts
- src/types/auth.ts

Stats: +156 -0
============================================================

Use this message? (y/n): y
✅ Commit created successfully
```

## Integration with Git Hooks

### commit-msg Hook

Validate commit messages automatically:

```bash
# .git/hooks/commit-msg
#!/bin/bash
python3 /home/kim-asplund/.claude/skills/git-workflow-skills/scripts/validate_commit_msg.py \
  --file "$1" || exit 1
```

Make executable:
```bash
chmod +x .git/hooks/commit-msg
```

### prepare-commit-msg Hook

Generate commit message template:

```bash
# .git/hooks/prepare-commit-msg
#!/bin/bash
if [ -z "$2" ]; then
  python3 /home/kim-asplund/.claude/skills/git-workflow-skills/scripts/generate_commit_msg.py \
    --dry-run | grep -A 100 "^=" | tail -n +2 | head -n -1 > "$1"
fi
```

Make executable:
```bash
chmod +x .git/hooks/prepare-commit-msg
```

## Requirements

- Python 3.6+
- Git installed and available in PATH

## Development

Both scripts are standalone with no external dependencies beyond Python standard library and git.
