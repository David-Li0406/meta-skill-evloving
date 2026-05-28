---
name: git-commit
description: Use this skill when you need to create meaningful commits with appropriate messages after reviewing changes in your code.
---

# Git Commit

## Workflow

### 1. Pre-commit Checks

Before committing, ensure code quality by running formatting, static analysis, and tests:

```bash
mise run fix
mise run check
mise run test
```

### 2. Check Staged Changes

Verify staged changes to ensure there are modifications to commit:

```bash
git diff --cached --stat
```

If there are no changes, prompt the user to stage changes using `git add`.

### 3. Analyze Diff

Review the detailed changes:

```bash
git diff --cached
```

### 4. Generate Commit Message

Follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format to create a commit message.

#### Format

```
<type>[(scope)]: <subject>

[body]
```

#### Types

- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code refactoring
- `docs:` - Documentation changes
- `style:` - Formatting changes (no impact on functionality)
- `perf:` - Performance improvements
- `test:` - Test additions or modifications
- `chore:` - Maintenance tasks

**Common Scopes**: `server`, `config`, `chroma-cli`, `chromad-cli`, `deps`

#### Subject Guidelines

- Start with a present tense imperative (e.g., `add`, `implement`, `fix`).
- Keep the title within 50 characters.
- Do not start with a capital letter or end with a period.
- Avoid vague messages (e.g., `update`, `fix bugs`).

### 5. Commit Changes

Use the generated commit message to commit the changes:

```bash
# Simple
git commit -m "<type>[(scope)]: <subject>"
```

```bash
# With Body
git commit -m "$(cat <<'EOF'
<type>[(scope)]: <subject>

[body]
EOF
)"
```

## Commit Message Examples

- `feat(chroma-cli): add new options for foobar`
- `fix(server): resolve validation issue in user input`
- `chore(deps): update Deno to X.Y.Z`

## Additional Guidelines

- Only commit when:
  1. All tests pass.
  2. All compiler/linter warnings are resolved.
  3. Changes represent a single logical unit of work.
  4. The commit message clearly indicates structural or functional changes.
- Prefer small, frequent commits over large, infrequent ones.
- Exclude files containing sensitive information (e.g., `.env`).
- Suggest splitting large changes into smaller commits.
- Use `--amend` only when explicitly instructed.
- Do not automatically push; do so only when explicitly instructed.

## Arguments

If `$ARGUMENTS` are specified:
- Use them as specific messages or scopes.
- Example: `/commit auth` → `feat(auth): ...` for setting the scope.