---
name: git-commit
description: Use this skill when you need to create well-structured git commit messages that adhere to the Conventional Commits specification.
---

# Skill body

## When to Use This Skill

Use this skill when:
- Creating git commits
- Writing conventional commit messages
- Working with staged changes that need to be committed
- Needing guidance on commit message structure and style

## Critical Rules

1. **NEVER Stage or Unstage Files Without Explicit Permission**
   - Do NOT run any commands that modify the staging area without user permission (e.g., `git add`, `git reset`).

2. **Clean State Required**
   - Ensure there are no uncommitted changes before proceeding. Check with `git status --porcelain`.

3. **No Destructive Operations Without Approval**
   - Avoid using commands like `git reset --hard` or `git clean -f` without explicit user approval.

## Process

1. **Check Staged Files**: 
   - Use `git status` to identify staged and unstaged files. If nothing is staged, ask the user for permission to stage files.

2. **Analyze Changes**: 
   - Review the staged changes using `git diff --cached` to understand what will be committed.

3. **Draft Commit Message**:
   - Follow the Conventional Commits format:
     ```
     <type>(<scope>): <subject>

     [optional body]

     [optional footer]
     ```
   - **Types** (REQUIRED):
     - `feat`: New feature
     - `fix`: Bug fix
     - `docs`: Documentation changes
     - `style`: Formatting changes
     - `refactor`: Code restructuring
     - `perf`: Performance improvements
     - `test`: Test additions or fixes
     - `chore`: Other changes that don't modify src or test files

   - **Scope** (REQUIRED for modules):
     - Use the module name or specific resource for changes (e.g., `feat(auth): add login feature`).

   - **Subject** (REQUIRED):
     - Present tense, lowercase, under 50 characters, no period at the end.

   - **Body** (OPTIONAL):
     - Explain what and why, not how. Wrap at 72 characters.

4. **Commit Changes**:
   - Use the constructed commit message to commit the changes with `git commit -m "<message>"`.

5. **Checkpoint Commits**:
   - Create checkpoint commits before risky operations, labeled clearly (e.g., `chore: checkpoint before <operation>`).

## Examples
- **Good**: `feat(auth): implement jwt signing`
- **Bad**: `Fixed login bug.` (Not conventional, past tense, period)

## Error Handling
- If multiple unrelated changes are detected, suggest splitting the commit into smaller commits.
- If no files are staged, abort and ask the user to stage files.