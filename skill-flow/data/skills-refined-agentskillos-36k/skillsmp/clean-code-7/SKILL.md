---
name: clean-code
description: "[slop] [debug] [unused] [duplicates] [all] - Cleans up code in the current branch. Removes AI artifacts, debug statements, unused code, and duplicates. Use when preparing for PR or cleaning up after AI-assisted coding."
---

# Cleaning Code

Analyzes and cleans up code changes in the current branch against main.

## Subcommands

| Command | Description |
|---------|-------------|
| `/cleaning-code slop` | Remove AI-generated artifacts (excessive comments, unnecessary checks, `any` casts) |
| `/cleaning-code debug` | Remove console.log, debugger, TODO comments, temporary code |
| `/cleaning-code unused` | Remove unused functions, variables, and imports |
| `/cleaning-code duplicates` | Consolidate duplicated code into shared utilities |
| `/cleaning-code all` | Run all cleanup checks in sequence |

## Workflow

1. **Get changed files**
   ```bash
   git diff main...HEAD --name-only
   ```

2. **For each file, analyze the diff**
   ```bash
   git diff main...HEAD -- <file>
   ```

3. **Apply cleanup based on subcommand** (see detailed guides below)

4. **Verify changes**
   ```bash
   npm run build  # or equivalent
   npm test
   ```

5. **Summarize** what was cleaned in 1-3 sentences

## Cleanup Guides

- **AI slop removal**: See [slop.md](slop.md)
- **Debug code removal**: See [debug.md](debug.md)
- **Unused code removal**: See [unused.md](unused.md)
- **Duplicate consolidation**: See [duplicates.md](duplicates.md)

## Guidelines

- **Only clean new code**: Check git blame; don't modify code that predates the branch
- **Preserve behavior**: Cleanup should be purely cosmetic
- **When in doubt, leave it**: If something might be intentional, keep it
- **Match project style**: Follow existing patterns in the codebase
