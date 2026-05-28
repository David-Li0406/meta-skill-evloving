---
name: dotfiles
description: Navigate, modify, and manage Luan's dotfiles repository from any directory. Use when adding or configuring development tools, updating shell/editor/terminal settings, creating cross-platform install scripts (macOS, Arch Linux, GitHub Codespaces), or understanding dotfiles organization. Repo is at ~/dotfiles.
---

# Dotfiles Management

## Repository Location

- **macOS/Arch**: `~/dotfiles`
- **Codespaces**: `/workspaces/.codespaces/.persistedshare/dotfiles` (GitHub implementation detail, may change)

**Debugging**: Installation output is logged to `~/dotfiles_install.log`

## Structure

The repo follows a **one directory per tool** pattern. To see the current structure:

```bash
tree ~/dotfiles -L 2 -d   # or: ls -la ~/dotfiles
```

Each tool directory should contain:
1. **`install`** script with `install()` and `configure()` functions
2. **Config files** to be symlinked to appropriate locations

See [references/tool-template.md](references/tool-template.md) for the install script template.

## Quick Reference

| Tool | Directory | Config Location | Has Install Script |
|------|-----------|-----------------|-------------------|
| Neovim | `nvim/` | `~/.config/nvim` | Yes |
| Tmux | `tmux/` | `~/.tmux.conf` | Yes |
| Zsh | `zsh/` | `~/.zshrc`, `~/.zsh/` | Yes (`install.zsh`) |
| Git | `git/` | `~/.gitconfig` | Yes |
| Ghostty | `ghostty/` | `~/.config/ghostty` | No |
| Helix | `helix/` | `~/.config/helix` | Yes (builds from source) |
| Whisper | `whisper/` | N/A | Yes (macOS/Arch only) |
| OpenCode | `opencode/` | `~/.config/opencode/` | Yes |
| Skills | `skills/` | `~/.config/opencode/skill/`, `~/.claude/skills/` | Yes |
| Rust | `rust/` | N/A | Yes (rustup) |
| Go | `go/` | N/A | Yes (Go tools: gopls, gofumpt, etc.) |
| Node | `node/` | N/A | Yes (fnm + TypeScript tools) |
| Bin | `bin/` | `~/bin` | Yes (custom scripts) |
| jj | `jj/` | `~/.jjconfig.toml` | Yes (Jujutsu VCS) |

## Platform Support

| Platform | Detection | Package Manager | Notes |
|----------|-----------|-----------------|-------|
| GitHub Codespaces | `$CODESPACES` set | `apt` | Debian-based, **read-only for push** (use `dot patch`) |
| macOS | `uname == Darwin` | `brew` | Personal machines |
| Arch/Omarchy | `command -v pacman` | `pacman`/`yay` | Arch + Hyprland |
| Omarchy | `~/.local/share/omarchy` exists | `pacman`/`yay` | Uses default configs, skip apply() |

See [references/platform-detection.md](references/platform-detection.md) for detection code snippets.

## Important Constraints

### Always Modify Dotfiles, Not Config Targets

Never create or edit files directly in config target directories like `~/.config/` or `~/bin/`. These locations contain symlinks to `~/dotfiles/`, so changes made there are either not version controlled or will be overwritten by install scripts.

Always make changes in `~/dotfiles/` so they are:
1. Version controlled (git)
2. Propagated to other machines via `dot pull`
3. Not overwritten by install scripts

Common mistakes to avoid:
- Creating skills in `~/.config/opencode/skill/` instead of `~/dotfiles/skills/`
- Editing nvim config in `~/.config/nvim/` instead of `~/dotfiles/nvim/`
- Adding scripts to `~/bin/` instead of `~/dotfiles/bin/`

After creating or modifying files in `~/dotfiles/`, run the appropriate install script to create symlinks (e.g., `dot install skills`, `dot install nvim`).

### Codespaces: Read-Only for Pushing

**You cannot push dotfiles changes directly from GitHub Codespaces.**

Why:
- Codespaces use a scoped `GITHUB_TOKEN` that only has access to the workspace repository (e.g., `github/github`), not your personal `luanzeba/dotfiles` repo
- Pushing changes would require setting up SSH keys or manually providing a PAT

**Workaround - Use `dot patch`:**

```bash
# 1. In Codespace: Create a patch from your changes
dot patch create

# 2. On local machine: Pull and apply the patch
dot patch pull

# 3. On local: Review, commit, and push
cd ~/dotfiles
git diff
git add -A && git commit -m "Fix from Codespace"
git push

# 4. In Codespace: Pull the committed changes
dot pull
```

This uses `gh cs cp` to transfer a patch file, authenticating through GitHub's Codespace infrastructure rather than requiring repo-specific credentials.

## Key Principles

- **Always install latest versions**: Install scripts should always fetch the latest stable/LTS version of tools, not pin to specific versions. Use `@latest` tags, `--lts` flags, or omit version specifiers where possible.
- **Idempotent scripts**: Install scripts must be safe to run multiple times without side effects.
- **Platform-aware**: Use platform detection to handle differences between Codespaces, macOS, and Arch.
- **Script pattern**: Each tool script should have `install()`, `configure()`, and optionally `apply()` and `update()` functions.

### Idempotency Guidelines

Scripts should produce the same result whether run once or many times:

1. **Check before installing**: Use `command -v <tool>` to skip if already installed
   ```bash
   if command -v rustc &>/dev/null; then
       echo "Rust already installed"
       return
   fi
   ```

2. **Use `-sf` for symlinks**: The `-f` flag overwrites existing symlinks safely
   ```bash
   ln -sf "$SCRIPT_DIR/.config" "$HOME/.config/tool"
   ```

3. **Handle existing directories**: Check and backup if needed
   ```bash
   if [[ -e "$target" && ! -L "$target" ]]; then
       mv "$target" "$target.backup"
   fi
   ```

4. **Use `--noconfirm` for package managers**: Avoid interactive prompts
   ```bash
   sudo pacman -S --noconfirm package
   brew install package  # Already non-interactive
   ```

## dotfiles CLI

The `dotfiles` command (in `~/bin/dotfiles`) provides easy management:

```bash
dotfiles status   # Show VCS status of dotfiles repo
dotfiles pull     # Pull latest and apply changes (skipped on Omarchy)
dotfiles edit     # Open dotfiles in $EDITOR
dotfiles update   # Update tools (brew, nvim plugins, rustup, etc.)
dotfiles doctor   # Check if everything is set up correctly
```

The CLI uses jj (Jujutsu) if available, falling back to git.

## Common Tasks

### Adding a New Tool

1. Create `<tool>/` directory at repo root
2. Create `<tool>/install` script using the template with:
   - `install()` - Install the tool binary/package
   - `configure()` - Symlink configs, set up environment
   - `apply()` (optional) - Reload config after `dotfiles pull`
   - `update()` (optional) - Update tool for `dotfiles update`
3. Add config files to the directory
4. Test on each platform
5. Optionally integrate with main `./install` script

### Modifying Neovim Config

See [references/nvim-config.md](references/nvim-config.md) for structure details.

Key locations:
- Plugins: `nvim/lua/plugins/<name>.lua`
- Key bindings: `nvim/lua/config/mappings.lua`
- Core options: `nvim/init.lua`

### Running Install Scripts

```bash
# Main install (dispatches to platform-specific script)
~/dotfiles/install

# Platform-specific scripts (called by main install)
~/dotfiles/install-codespaces   # GitHub Codespaces
~/dotfiles/install-local        # macOS and Arch

# Tool-specific installs
~/dotfiles/nvim/install
~/dotfiles/zsh/install.zsh
~/dotfiles/skills/install
~/dotfiles/node/install
~/dotfiles/rust/install
~/dotfiles/go/install
~/dotfiles/jj/install
```

## Shared Utilities

The `lib/common.sh` file provides shared functions for all scripts:

```bash
source "$DOTFILES_DIR/lib/common.sh"

dotfiles_dir    # Get dotfiles path (handles Codespaces)
is_codespaces   # Check if running in Codespaces
is_macos        # Check if running on macOS
is_arch         # Check if running on Arch Linux
is_omarchy      # Check if running on Omarchy
vcs_cmd         # Run jj or git command
log_info/log_success/log_warn/log_error  # Logging helpers
```
