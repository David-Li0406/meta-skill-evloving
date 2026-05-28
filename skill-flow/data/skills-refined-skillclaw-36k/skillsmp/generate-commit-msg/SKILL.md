---
name: generate-commit-msg
description: Generate professional English commit messages with gitmoji based on git diff. Use when creating commit messages, analyzing staged changes, or formatting commits according to conventional commits + gitmoji style.
allowed-tools: Bash
---

# Generate Commit Message

Generate a professional English commit message based on the current git diff, following the project's conventional commits + gitmoji style.

## Instructions

1. **Check staged changes**
   - Run `git diff --staged` to see what will be committed
   - If no changes are staged, check unstaged changes with `git diff`
   - If nothing to commit, inform the user to stage changes first

2. **Analyze the changes**
   - Understand what was added, modified, or removed
   - Identify the primary purpose of the changes
   - Determine if changes span multiple areas (may need multiple commits)

3. **Select commit type and gitmoji**
   - **feat** `:sparkles:` - New feature or enhancement
   - **fix** `:bug:` - Bug fix
   - **refactor** `:recycle:` - Code refactoring (no functional change)
   - **docs** `:memo:` - Documentation changes
   - **style** `:art:` - Code formatting, whitespace, style
   - **test** `:white_check_mark:` - Adding or updating tests
   - **chore** `:wrench:` - Build, configuration, dependencies
   - **perf** `:zap:` - Performance improvements

4. **Format the commit message**
   - Structure: `type: :emoji: description`
   - Use imperative mood: "add feature" not "added feature"
   - Keep description concise and clear (ideally under 72 chars)
   - Do NOT include a period at the end

5. **Provide the message**
   - Show the generated commit message
   - Explain what changes it captures
   - If changes are complex, suggest splitting into multiple commits

## Example Patterns

Based on this project's commit history:

```
feat: :sparkles: add ghostty home-manager config
fix: :bug: ensure pre-commit is installed and executable
feat: :sparkles: enable zoxide for zsh and add docs
fix: :bug: align nix-darwin with nixpkgs and stabilize mise install
```

## Notes

- Multiple unrelated changes should be committed separately
- Breaking changes should be noted
- Focus on the "what" and "why", not the "how"
- Match the project's existing commit style (conventional commits + gitmoji)
