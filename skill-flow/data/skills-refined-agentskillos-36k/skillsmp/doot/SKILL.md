---
name: doot
description: >
  Manage dotfiles with doot - sync ~/.dotfiles with ~/.config and home directory.
  Triggers: adding config files, syncing dotfiles, managing symlinks, doot commands,
  or asking about dotfiles structure.
license: MIT
compatibility: opencode
---

# Doot - Dotfiles Manager

Doot is a fast dotfiles manager that creates symlinks from `~/.dotfiles` to their target locations (`~/.config`, `~/`, etc.).

## When This Skill MUST Be Used

**ALWAYS invoke this skill when:**
- Adding new configuration files to dotfiles
- Syncing changes between dotfiles and config
- Managing symlinks for config files
- Questions about dotfiles structure
- Moving existing configs into version control

## Quick Reference

| Command | Description |
|---------|-------------|
| `doot install` | Create/update symlinks (default, safe to run anytime) |
| `doot add <file>` | Move file to dotfiles and create symlink |
| `doot ls` | List all managed symlinks |
| `doot restore <file>` | Replace symlink with original file |
| `doot clean` | Remove all symlinks created by doot |

## Directory Structure

```
~/.dotfiles/
├── config/              # Maps to ~/.config/
│   ├── hypr/           # -> ~/.config/hypr/
│   ├── nvim/           # -> ~/.config/nvim/
│   ├── opencode/       # -> ~/.config/opencode/
│   └── ...
├── bashrc              # -> ~/.bashrc
├── bash_profile        # -> ~/.bash_profile
├── gitconfig-personal  # -> ~/.gitconfig-personal
├── XCompose            # -> ~/.XCompose
├── docs/               # -> ~/.docs/
└── doot/
    └── config.toml     # Doot configuration
```

## How Doot Maps Files

Doot uses simple conventions:

| Dotfiles Location | Target Location |
|-------------------|-----------------|
| `~/.dotfiles/config/*` | `~/.config/*` |
| `~/.dotfiles/bashrc` | `~/.bashrc` |
| `~/.dotfiles/XCompose` | `~/.XCompose` |
| `~/.dotfiles/docs/*` | `~/.docs/*` |

**Key insight**: Files in `config/` map to `~/.config/`. Files in root map to `~/` with a dot prefix.

## Common Workflows

### Add New Config to Dotfiles

```bash
# Move existing config and create symlink
doot add ~/.config/app-name/config.toml

# Result:
# - File moved to ~/.dotfiles/config/app-name/config.toml
# - Symlink created: ~/.config/app-name/config.toml -> ~/.dotfiles/...
```

### Add Multiple Files

```bash
# Add entire directory
doot add ~/.config/app-name/

# Add specific files
doot add ~/.config/app/config.toml ~/.config/app/themes/
```

### Sync After Manual Changes

If you manually add/edit files in `~/.dotfiles`:

```bash
# Update symlinks to reflect changes
doot install
```

**This is safe to run anytime** - it only creates missing symlinks and removes broken ones.

### Check What's Managed

```bash
# List all symlinks
doot ls

# Verbose output
doot ls -v
```

### Remove from Dotfiles

```bash
# Replace symlink with actual file (opposite of add)
doot restore ~/.config/app/config.toml
```

## Creating New Config Files

When creating new config files that should be tracked:

1. **Create in dotfiles first**:
   ```bash
   # Create the file in dotfiles
   mkdir -p ~/.dotfiles/config/new-app
   touch ~/.dotfiles/config/new-app/config.toml
   
   # Create symlinks
   doot install
   ```

2. **Or create normally, then add**:
   ```bash
   # Create config normally
   mkdir -p ~/.config/new-app
   vim ~/.config/new-app/config.toml
   
   # Move to dotfiles
   doot add ~/.config/new-app/config.toml
   ```

## OpenCode Config Structure

OpenCode configs in dotfiles:

```
~/.dotfiles/config/
├── opencode/              # Base config (all profiles)
│   ├── opencode.json      # Main config
│   ├── AGENTS.md          # Global agent instructions
│   ├── agents/            # Custom agents
│   ├── commands/          # Slash commands
│   ├── rules/             # Always-loaded rules
│   └── skills/            # On-demand skills
├── opencode-d3fvxl/       # d3fvxl profile overlay
│   ├── opencode.json
│   └── skills/
└── opencode-efg/          # efg profile overlay
    ├── opencode.json
    └── skills/
```

After editing, run `doot install` to update symlinks.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Symlink not created | Run `doot install` |
| File not in dotfiles | Use `doot add <file>` |
| Broken symlink | Run `doot install` (auto-cleans) |
| Want original file back | Use `doot restore <file>` |
| See what's tracked | Run `doot ls` |

## Best Practices

1. **Always use `doot install` after manual edits** to sync symlinks
2. **Use `doot add`** to move existing configs - don't manually copy
3. **Commit changes** to git after adding new configs
4. **Check `doot ls`** to verify symlinks are correct
5. **Keep secrets out** - don't add files with API keys/passwords

## Example Session

```bash
# Add zellij config to dotfiles
doot add ~/.config/zellij/config.kdl

# Verify it's tracked
doot ls | grep zellij

# Make changes in dotfiles
vim ~/.dotfiles/config/zellij/config.kdl

# Changes are live (symlink) - no sync needed!

# Add new file manually to dotfiles
touch ~/.dotfiles/config/zellij/layouts/default.kdl

# Create symlink for new file
doot install

# Commit to git
cd ~/.dotfiles
git add -A
git commit -m "Add zellij config"
```
