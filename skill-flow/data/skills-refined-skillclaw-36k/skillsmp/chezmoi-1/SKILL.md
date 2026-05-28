---
name: chezmoi
description: Help with chezmoi dotfile management, ansible playbooks, and syncing configs to the dotfiles repository. Use when modifying configuration files in ~/.config, ~/, ansible playbooks, or other managed locations. ALWAYS prompt the user about syncing to chezmoi after making config changes. Please use this anytime I mention configuration for my computer
---

# Chezmoi Dotfile Management Skill

## Overview

Chezmoi manages dotfiles and system configuration, syncing them to a Git repository for version control and portability across machines. This includes ansible playbooks for system package installation.

## Key Locations

- **Chezmoi source**: `/Users/trent/.local/share/chezmoi/`
- **Git repository**: `https://github.com/trentshaines/dotfiles.git`
- **Home directory**: `~/` (managed files)
- **Config directory**: `~/.config/` (managed files)
- **Ansible playbooks**: `~/ansible/` (managed via chezmoi)

## Managed Files

Important files tracked by chezmoi (in source directory):

### Dotfiles

- `dot_zshrc` → `~/.zshrc`
- `dot_tmux.conf` → `~/.tmux.conf`
- `dot_gitconfig` → `~/.gitconfig`
- `dot_gitignore_global` → `~/.gitignore_global`
- `dot_fzf.zsh` → `~/.fzf.zsh`
- `dot_ideavimrc` → `~/.ideavimrc`
- `dot_aerospace.toml` → `~/.aerospace.toml`

### Directories

- `dot_config/` → `~/.config/` (includes tmuxinator, gh, etc.)
- `dot_claude/` → `~/.claude/` (skills, settings, etc.)
- `dot_cursor/` → `~/.cursor/`
- `dot_local/` → `~/.local/`
- `ansible/` → `~/ansible/` (ansible playbooks for package installation)
- `private_Documents/` → `~/Documents/` (private, encrypted)
- `private_Library/` → `~/Library/` (private, encrypted)

## Common Commands

### User's Aliases (from ~/.zshrc)

```bash
cadd      # chezmoi re-add (sync changes back to source)
capply    # chezmoi apply (apply changes from source to home)
```

### CRITICAL: `add` vs `re-add`

**This is the most important distinction:**

- `chezmoi add <file>` - Add a NEW file that's NOT YET managed by chezmoi
- `chezmoi re-add <file>` - Update an EXISTING file that's ALREADY managed
- `chezmoi re-add <directory>` - Update directory AND pick up new files within it

**How to know which to use:**

```bash
chezmoi managed | grep filename   # If it shows up → use re-add
                                  # If it doesn't → use add
```

**SHORTCUT for managed directories:**

If the parent directory is already managed, `re-add` on the directory picks up new files!

```bash
# These directories are ALREADY managed:
chezmoi re-add ~/.claude/skills/          # Picks up new AND modified skills
chezmoi re-add ~/.config/tmuxinator/      # Picks up new AND modified templates

# So you DON'T need 'add' for new skills or templates - just re-add the directory!
```

**IMPORTANT: `chezmoi re-add` with NO arguments**

Running `chezmoi re-add` without any arguments will re-add **ALL modified managed files**:

```bash
chezmoi re-add    # Re-add everything that changed
```

**When to use this:**

- After making multiple config changes across different files
- When you're unsure what you modified
- To catch any manual edits you forgot about

**⚠️ CRITICAL: Always check what changed before committing!**

```bash
chezmoi re-add                    # Re-add all changes
cd ~/.local/share/chezmoi
git status                        # See what files changed
git diff                          # Review the actual changes
```

**Why this matters:**

- You might have accidentally modified a managed file
- Ensures you don't commit unwanted changes
- Helps you write accurate commit messages
- Catches any test/debug changes you forgot to revert

### Essential Chezmoi Commands

```bash
# Sync changes FROM home TO chezmoi source
chezmoi add ~/.new-file           # Add NEW file (first time)
chezmoi re-add ~/.zshrc           # Re-add EXISTING managed file
chezmoi re-add ~/.config/tmuxinator/admin.yml  # Re-add EXISTING config
chezmoi re-add                    # Re-add ALL modified managed files (no args!)

# Apply changes FROM chezmoi source TO home
chezmoi apply                     # Apply all changes
chezmoi apply ~/.zshrc            # Apply specific file

# View changes
chezmoi diff                      # See what would change
chezmoi status                    # See modified files
chezmoi managed                   # List all managed files

# Git operations (in chezmoi source)
chezmoi cd                        # cd to source directory
chezmoi git -- status             # Git status
chezmoi git -- add .              # Git add
chezmoi git -- commit -m "msg"    # Git commit
chezmoi git -- push               # Git push
exit                              # Exit chezmoi source directory
```

## Claude's Recommended Workflow (SIMPLE & FOOLPROOF)

**When you modify or create config files, use this workflow:**

```bash
# Step 1: Re-add managed directories or files
chezmoi re-add ~/.claude/skills/         # For skills (new OR modified)
chezmoi re-add ~/.config/tmuxinator/     # For tmuxinator (new OR modified)
chezmoi re-add ~/.zshrc                  # For individual files

# Step 2: Work directly in the chezmoi source directory
cd ~/.local/share/chezmoi

# Step 3: Use git commands directly
git add .                              # Stage everything
git status                             # Review what's changed
git commit -m "Descriptive message"    # Commit
git push                               # Push to GitHub

# Step 4: Return to previous directory
cd -
```

**Key insight:** For `~/.claude/skills/` and `~/.config/tmuxinator/`, just use `re-add` on the directory - it picks up new AND modified files!

**Even simpler alternative (when unsure):**

```bash
# Just work directly in the chezmoi source!
cd ~/.local/share/chezmoi
git add .
git status    # See what changed
git commit -m "Update configs"
git push
cd -
```

This avoids confusion about add vs re-add since git will show you exactly what changed.

## Typical Workflow After Config Changes

When Claude (or the user) modifies a config file like `~/.zshrc`, `~/.config/tmuxinator/admin.yml`, or any other managed file:

### Step 1: Sync the file to chezmoi source

```bash
# For NEW files (not yet managed):
chezmoi add ~/.config/tmuxinator/config.yml

# For EXISTING managed files:
chezmoi re-add ~/.zshrc
chezmoi re-add ~/.config/tmuxinator/admin.yml
```

### Step 2: Check for unexpected changes and commit

```bash
cd ~/.local/share/chezmoi
git status  # ⚠️ ALWAYS check what files changed
git diff    # Review the actual changes (optional but recommended)
git add .
git commit -m "Description of changes"
git push
cd -
```

**⚠️ IMPORTANT:** Always run `git status` before committing to catch:

- Unintended modifications to managed files
- Leftover test/debug changes
- Files you modified but forgot about

## Claude's Responsibility

**IMPORTANT**: After making ANY configuration changes to managed files, Claude should:

1. ✅ **Inform the user** that changes were made to a managed file
2. ✅ **Prompt the user** if they want to sync to chezmoi:

   ```
   I've updated ~/.zshrc. Would you like me to sync this to your dotfiles repo?
   This involves:
   1. chezmoi re-add ~/.zshrc
   2. Commit and push to github.com/trentshaines/dotfiles
   ```

3. ✅ **Offer global re-add option** when appropriate:
   - If multiple files were changed, or
   - If there might be other uncommitted changes, or
   - After syncing specific files

   Ask: "Would you like to run `chezmoi re-add` (no args) to sync ALL modified managed files?"

   This is useful because:
   - It catches any other changes the user made manually
   - It's simpler than specifying individual files
   - It ensures everything is in sync

4. ⚠️ **Wait for user confirmation** before running chezmoi commands
5. ✅ If user confirms, execute the re-add and git workflow
6. ⚠️ **ALWAYS check git status** before committing:

   ```bash
   cd ~/.local/share/chezmoi
   git status  # Show user what files changed
   ```

   - If unexpected files appear, inform the user
   - Ask if they want to review changes with `git diff`
   - Only proceed with commit if changes look correct

### Example Prompt Template

After modifying a config file:

```
Updated: ~/.config/tmuxinator/admin.yml

Would you like to sync this change to your dotfiles repo?
- Run: chezmoi re-add ~/.config/tmuxinator/admin.yml
- Commit and push to github.com/trentshaines/dotfiles.git
```

## Chezmoi File Naming Convention

Chezmoi uses special prefixes in the source directory:

- `dot_` → `.` (hidden files)
  - Example: `dot_zshrc` → `~/.zshrc`
  - Example: `dot_config/` → `~/.config/`

- `private_` → Private files (can be encrypted)
  - Example: `private_Documents/` → `~/Documents/`

- Combined: `private_dot_` → Private hidden files
  - Example: `private_dot_ssh/` → `~/.ssh/`

## Checking What's Managed

```bash
chezmoi managed                   # List all managed files
chezmoi managed | grep tmux       # Find tmux-related managed files
```

## Ansible Playbooks

### Overview

Ansible playbooks in `~/ansible/` define system package installation and configuration. These are managed by chezmoi and synced to the dotfiles repo.

### Location

- `~/ansible/playbooks/packages.yml` - Main package installation playbook

### What It Installs

- **Homebrew** packages (formulae and casks)
- **Homebrew taps** (custom repositories)
- **Oh My Zsh** (if not already installed)
- **TPM** (Tmux Plugin Manager)
- **npm global packages** (like Claude Code)

### Running the Playbook

```bash
cd ~/ansible
ansible-playbook playbooks/packages.yml
```

### After Modifying Ansible Playbooks

```bash
# Option 1: Re-add ansible directory
chezmoi re-add ~/ansible/

# Option 2: Re-add specific playbook
chezmoi re-add ~/ansible/playbooks/packages.yml

# Then commit and push
cd ~/.local/share/chezmoi
git add ansible/
git commit -m "Update ansible packages playbook"
git push
cd -
```

### Common Ansible Modifications

1. **Adding new brew packages**: Add to `name:` list under `Install brew formulae`
2. **Adding new casks**: Add to `name:` list under `Install brew casks`
3. **Adding new taps**: Add to `name:` list under `Add brew taps`
4. **Adding new tasks**: Add new task blocks for additional setup steps

## Common Scenarios

### 1. Modified an existing dotfile (e.g., .zshrc)

```bash
chezmoi re-add ~/.zshrc           # Re-add existing managed file
cd ~/.local/share/chezmoi
git add .
git commit -m "Update zshrc: describe changes"
git push
cd -
```

### 2. Created NEW tmuxinator template

```bash
# EASY: Just re-add the directory (it's already managed!)
chezmoi re-add ~/.config/tmuxinator/
cd ~/.local/share/chezmoi
git add .
git commit -m "Add new tmuxinator template: newtemplate"
git push
cd -
```

### 3. Created NEW Claude skill

```bash
# EASY: Just re-add the directory (it's already managed!)
chezmoi re-add ~/.claude/skills/
cd ~/.local/share/chezmoi
git add .
git status                                # Verify the new files
git commit -m "Add my-skill Claude skill"
git push
cd -
```

### 4. Modified multiple existing config files

```bash
chezmoi re-add                    # Re-add all changed managed files
cd ~/.local/share/chezmoi
git add .
git status                        # Review all changes
git commit -m "Update multiple configs"
git push
cd -
```

### 5. Mixed: new skills + modified configs (EASIEST)

```bash
# Re-add managed directories (picks up new AND modified files)
chezmoi re-add ~/.claude/skills/
chezmoi re-add ~/.config/tmuxinator/

# Re-add individual modified files
chezmoi re-add ~/.zshrc

# Then commit everything
cd ~/.local/share/chezmoi
git add .
git status  # Review everything
git commit -m "Add new skills and update existing configs"
git push
cd -
```

### 6. Modified ansible playbook

```bash
chezmoi re-add ~/ansible/playbooks/packages.yml
cd ~/.local/share/chezmoi
git add ansible/
git commit -m "Add fd, btop, oh-my-zsh, TPM, and Claude Code to ansible"
git push
cd -
```

### 7. Want to see what changed

```bash
chezmoi diff                      # See what would change
cd ~/.local/share/chezmoi && git status  # See what's uncommitted
```

## Files NOT Managed by Chezmoi

Some config files are NOT tracked (check `.chezmoiignore`):

- Temporary files
- Cache directories
- Machine-specific configs (if marked)
- Secrets (should use encrypted templates)

## Best Practices

1. **Always re-add after editing**: Run `chezmoi re-add <file>` after modifying managed files
2. **Commit frequently**: Keep dotfiles repo up to date with descriptive commits
3. **Review diffs**: Use `chezmoi diff` before applying to see what will change
4. **Test changes**: Modify in home directory first, test, then re-add to chezmoi
5. **Use meaningful commit messages**: Describe what changed and why

## Troubleshooting

### File not syncing?

- Check if it's managed: `chezmoi managed | grep filename`
- Check `.chezmoiignore` for exclusions
- Ensure you used `chezmoi re-add` after editing

### Conflicts between source and home?

```bash
chezmoi diff        # See differences
chezmoi apply -v    # Apply with verbose output
chezmoi re-add      # Or re-add to update source
```

### Lost changes?

- Source of truth is in `~/.local/share/chezmoi/`
- Git history: `chezmoi cd && git log`
- Can recover from Git history if needed

## Integration with Other Tools

- **tmuxinator**: Templates in `~/.config/tmuxinator/` are managed
- **Claude skills**: Skills in `~/.claude/skills/` are managed via `dot_claude/`
- **zsh**: `.zshrc` is managed as `dot_zshrc`
- **git**: `.gitconfig` is managed as `dot_gitconfig`

## Security Note

- Private files use `private_` prefix
- Sensitive data should be encrypted (chezmoi supports encryption)
- Never commit secrets in plain text
- Use chezmoi templates for machine-specific values
