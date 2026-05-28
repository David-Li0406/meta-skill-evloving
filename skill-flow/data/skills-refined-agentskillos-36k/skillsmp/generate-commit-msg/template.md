# Commit Message Template

## Format

```
type: :emoji: description
```

## Type and Gitmoji Reference

| Type | Gitmoji | Emoji | Description |
|------|---------|-------|-------------|
| feat | `:sparkles:` | ✨ | A new feature or enhancement |
| fix | `:bug:` | 🐛 | A bug fix |
| refactor | `:recycle:` | ♻️ | Code change that neither fixes a bug nor adds a feature |
| docs | `:memo:` | 📝 | Documentation only changes |
| style | `:art:` | 🎨 | Code formatting, whitespace (no functional change) |
| test | `:white_check_mark:` | ✅ | Adding or updating tests |
| chore | `:wrench:` | 🔧 | Build process, configuration, dependencies |
| perf | `:zap:` | ⚡ | Performance improvements |

## Additional Useful Gitmoji

| Gitmoji | Emoji | Use Case |
|---------|-------|----------|
| `:fire:` | 🔥 | Remove code or files |
| `:lock:` | 🔒 | Fix security issues |
| `:arrow_up:` | ⬆️ | Upgrade dependencies |
| `:arrow_down:` | ⬇️ | Downgrade dependencies |
| `:construction:` | 🚧 | Work in progress |
| `:rewind:` | ⏪ | Revert changes |

## Examples from This Project

```
feat: :sparkles: add ghostty home-manager config
fix: :bug: ensure pre-commit is installed and executable
feat: :sparkles: enable zoxide for zsh and add docs
fix: :bug: align nix-darwin with nixpkgs and stabilize mise install
```

## Guidelines

1. **Subject line**
   - Use imperative mood ("add" not "added")
   - No period at the end
   - Keep under 72 characters
   - Be specific and concise

2. **Description**
   - What changed and why
   - Clear enough for others to understand
   - Focus on the intent, not implementation details

3. **When to split commits**
   - Unrelated changes (fix + feature = 2 commits)
   - Multiple components affected independently
   - Large refactoring + new feature
