---
name: sync
description: Use when user says "sync" or wants to commit, push, pull, and run the dotfiles sync script. Also use when creating migrations for one-time cleanup on existing machines, or when a migration fails.
---

# Sync

Full dotfiles sync: commit, git sync, resolve conflicts, run sync script.

For migrations (one-time cleanup scripts), see @migrations.md.

## Steps

1. **Check for changes**
   ```bash
   git status
   git diff
   ```

2. **Commit if changes exist**
   - Analyze diff for distinct semantic changes
   - Make multiple commits if changes span different scopes/concerns
   - Use conventional commit format with scope from CLAUDE.md
   - Example: fish config change + claude settings change = 2 commits

3. **Git sync**
   ```bash
   git sync  # alias for: git pull --rebase && git push
   ```

4. **Resolve conflicts if any**
   - Autostash conflicts are common with `claude/settings.json`
   - Read conflicted file, resolve intelligently, then:
     ```bash
     git add <file>
     git stash drop  # if autostash conflict
     ```
   - Commit and push resolution

5. **Run sync script** (Claude Code runs this directly)
   ```bash
   ./sync
   ```
   - Use `./sync -v` for verbose output if debugging

6. **Relay sudo reminder if shown**
   - The script auto-detects if `sync-sudo` is needed
   - If output shows "Next: Run sudo ./sync-sudo", relay that to user
   - If no reminder shown, everything is configured - done!

## What Sync Does

**`./sync`** (Claude Code runs directly):
- Symlinks config files (fish, git, zed, nvim, ssh, etc.)
- Installs Homebrew packages from Brewfile
- Sets up Node.js via pnpm
- Configures macOS defaults (keyboard, Finder, Dock)
- Installs Fisher plugins and npm global packages

**`./sync-sudo`** (user runs manually, only if needed):
- Power management (display sleep)
- Touch ID for sudo
- Fish as default shell (/etc/shells + chsh)
