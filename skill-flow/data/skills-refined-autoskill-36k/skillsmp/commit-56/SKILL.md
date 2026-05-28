---
name: commit
description: Create a commit following COMMIT_GUIDELINES.md
argument-hint: [optional message hint]
allowed-tools: Bash, Read, Grep
---

# Commit Changes

Create a well-formatted commit following the project's COMMIT_GUIDELINES.md.

## Instructions

1. **Check Status**
   - Run `git status` to see staged and unstaged changes
   - Run `git diff --cached` to see what will be committed
   - If nothing staged, ask user what to stage or stage all with `git add -A`

2. **Analyze Changes**
   - Review the diff to understand what changed
   - Identify the primary type of change
   - Determine appropriate scope

3. **Determine Commit Type**

   | Type | Use When |
   |------|----------|
   | `feat` | New feature or functionality |
   | `fix` | Bug fix or correction |
   | `refactor` | Code restructuring, no behavior change |
   | `perf` | Performance improvements |
   | `test` | Adding or modifying tests |
   | `docs` | Documentation changes |
   | `style` | Formatting, whitespace changes |
   | `build` | Build system or dependencies |
   | `ci` | CI configuration |
   | `chore` | Maintenance tasks |

4. **Determine Scope**
   - Use the primary area affected: `finish`, `start`, `config`, `init`, etc.
   - Keep it short and consistent with existing commits

5. **Write Subject Line**
   - Maximum 50 characters
   - Imperative mood: "Add feature" not "Added feature"
   - No period at end
   - Sentence case

6. **Write Body** (if needed)
   - Explain WHAT and WHY, not HOW
   - Wrap at 72 characters
   - Use bullet points for multiple items
   - Leave blank line after subject

7. **Add Footer** (if applicable)
   - Reference issues: `Resolves #123` or `Refs #123`
   - Note breaking changes: `BREAKING CHANGE: description`

8. **Create Commit**

   Use HEREDOC format for proper formatting:
   ```bash
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <subject>

   <body>

   <footer>
   EOF
   )"
   ```

## Examples

### Feature Commit
```bash
git commit -m "$(cat <<'EOF'
feat(finish): add squash merge strategy

Implements --squash flag for finish command that performs a squash merge
instead of regular merge. Creates single commit with all branch changes.

- Add squash option to merge strategy enum
- Update finish command to handle squash flag
- Add configuration support for default squash behavior

Resolves #42
EOF
)"
```

### Bug Fix Commit
```bash
git commit -m "$(cat <<'EOF'
fix(start): validate branch name before creation

Check for invalid characters in branch name before attempting creation.
Previously git would fail with cryptic error message.

Resolves #57
EOF
)"
```

### Test Commit
```bash
git commit -m "$(cat <<'EOF'
test(finish): add merge conflict handling tests

Add comprehensive tests for finish command behavior when merge conflicts
occur during the merge step. Tests verify proper state persistence and
conflict resolution workflow.
EOF
)"
```

### Simple Refactor
```bash
git commit -m "$(cat <<'EOF'
refactor(config): extract branch validation logic

Move branch name validation from cmd/start.go to internal/util for reuse
across multiple commands.
EOF
)"
```

## Rules from COMMIT_GUIDELINES.md

### Do
- Be specific about what changed
- Reference related issues
- Group related changes
- Test before committing

### Don't
- Use vague subjects ("Fix bug", "Update code")
- Exceed line limits
- Mix unrelated changes
- Include file lists
- Add AI attribution lines
- Commit broken code

## Verification

After committing:
1. Run `git log -1` to verify message
2. Run `go test ./...` to ensure tests still pass
3. Run `go build ./...` to verify build
