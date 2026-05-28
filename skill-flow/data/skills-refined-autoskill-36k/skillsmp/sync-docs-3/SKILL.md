---
name: sync-docs
description: Synchronize documentation and skills with codebase changes. Analyzes recent git changes and suggests updates to README, CLAUDE.md, and skills to keep documentation in sync.
allowed-tools: Bash, Glob, Grep, Read, Edit
---

# Sync Documentation

Analyze recent changes and update documentation/skills to keep them synchronized with the codebase.

## Purpose

This skill helps maintain documentation consistency by:
- Detecting code changes that require documentation updates
- Identifying which documents/skills need updating
- Suggesting or applying necessary changes
- Ensuring README.md, CLAUDE.md, and skills stay in sync

## Instructions

### 1. Analyze Recent Changes

Check what has changed in the codebase:

```bash
# Check last commit
git diff HEAD~1..HEAD

# Or check staged changes
git diff --staged

# Or check unstaged changes
git diff
```

### 2. Identify Impact Areas

Based on the changes detected, determine which documentation needs updating:

**Package/Tool Changes:**
- Files: `home-manager/default.nix`, `darwin/default.nix`, `flake.nix`
- Impact: README.md (Main Tools), `/nix-operations`, `/mise-guide`

**Keybinding Changes:**
- Files: `home-manager/skhd/`, `home-manager/yabai/`, `nixos/desktop/hyprland/`, `home-manager/zellij/`
- Impact: `/services-guide`, `/hyprland-cheatsheet`, `/nixos-keybindings`, `/zellij-worktree`

**Configuration Structure Changes:**
- Files: New modules, directory reorganization
- Impact: `.claude/CLAUDE.md` (Architecture Overview, Configuration Structure)

**Command/Task Changes:**
- Files: `Makefile`, `home-manager/mise/`, scripts
- Impact: `.claude/CLAUDE.md` (Common Commands), `/nix-operations`, `/mise-guide`

**Service/Daemon Changes:**
- Files: `darwin/service/`, `nixos/services/`
- Impact: `/services-guide`, `/fileserver-guide`, `/gitserver-guide`

### 3. Detection Patterns

Look for these specific change patterns:

**New Package Added:**
```nix
# In home-manager/default.nix
packages = with pkgs; [
  ...
  newpackage  # ← New addition
];
```
→ Update: README.md Main Tools section

**New Make Task:**
```makefile
# In Makefile
new-task:
    @echo "New task"
```
→ Update: `.claude/CLAUDE.md` Common Commands

**New Keybinding:**
```nix
# In skhd/default.nix
"alt - t" = "...";  # ← New keybinding
```
→ Update: `/services-guide` Keyboard Shortcuts table

**New Nix Module:**
```nix
# In configuration.nix
imports = [
  ./new-module  # ← New import
];
```
→ Update: `.claude/CLAUDE.md` imports list

### 4. Update Documentation

For each identified change:

1. **Read the current documentation**
2. **Determine what needs to be added/modified**
3. **Update the documentation** (use Edit tool)
4. **Verify consistency** across related documents

### 5. Report to User

Provide a summary:
- List of detected changes
- Documents that were updated
- Specific sections modified
- Any manual review needed

## Common Update Scenarios

### Scenario 1: Adding a New Package

**Detected Change:**
```diff
+ ripgrep
```

**Updates Required:**
1. README.md → Add to appropriate section under Main Tools
2. Consider if usage docs needed in relevant skill

### Scenario 2: New Keybinding

**Detected Change:**
```diff
+ "alt - t" = "yabai -m window --toggle float";
```

**Updates Required:**
1. `/services-guide` → Add to Keyboard Shortcuts table
2. Ensure description matches the action

### Scenario 3: New Nix Module

**Detected Change:**
```diff
+ imports = [ ./new-feature ];
```

**Updates Required:**
1. `.claude/CLAUDE.md` → Update imports list
2. `.claude/CLAUDE.md` → Update Architecture Overview if significant
3. Consider creating new skill if feature is complex

### Scenario 4: New Make Task

**Detected Change:**
```diff
+ docker-prune:
+     docker system prune -af
```

**Updates Required:**
1. `.claude/CLAUDE.md` → Add to Development Tools commands
2. Consider adding to `/nix-operations` if Nix-related

## Usage Examples

**Check for updates needed:**
```
/sync-docs
```

**After making changes:**
```
"I just added a new package, update the docs"
```

**Specific check:**
```
"Check if documentation needs updating based on my staged changes"
```

## Important Notes

- **Always run after significant changes** to maintain doc consistency
- **Review suggested changes** before applying
- **Check cross-references** between documents
- **Verify links** and file paths are still correct
- **Test commands** mentioned in documentation

## Limitations

This skill provides **suggestions and automation** but:
- May not catch all subtle documentation needs
- Cannot determine narrative/explanation quality
- Requires human judgment for complex changes
- Should be supplemented with manual review
