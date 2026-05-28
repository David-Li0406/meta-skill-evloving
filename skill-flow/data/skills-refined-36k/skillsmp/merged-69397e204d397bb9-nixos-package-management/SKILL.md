---
name: nixos-package-management
description: Use this skill for managing NixOS packages, dotfiles configuration, and Claude Code settings changes.
---

# NixOS Package Management & Dotfiles

Help with NixOS configuration and package management.

**User input:** $ARGUMENTS

## Style

Comment sparingly in `.nix` files. Nix is declarative, so code is self-documenting. Only add comments to:
- Delineate sections in long package lists
- Explain non-obvious workarounds
- Note dependencies between options that aren't apparent

## Instructions

1. **Read context and config:**
   - Read `~/Dotfiles/CLAUDE.md` to understand the dotfiles layout
   - Read `~/Dotfiles/configuration.nix` to see current packages
   - Read `~/Dotfiles/flake.nix` if flake changes are needed

2. **Parse the request:**
   - **Install package:** User wants to add a package (e.g., "install htop", "add nodejs")
   - **Remove package:** User wants to remove a package
   - **Search:** User wants to find a package (e.g., "search for video editor")
   - **Update:** User wants to update the system
   - **Configuration changes:** Edit appropriate module in `modules/`
   - **Claude settings changes:** Edit `~/Dotfiles/sources/claude/`

3. **For package install/remove:**
   - Search nixpkgs to confirm exact package name: `nix search nixpkgs <name>`
   - Edit `configuration.nix` or `hosts/fw13/default.nix` to add/remove from `users.users.sasha.packages` or `home.packages`
   - Show the diff to the user

4. **For search:**
   - Run `nix search nixpkgs <query>` and summarize results
   - Suggest the most relevant package(s)

5. **For updates:**
   - Run `nix flake update` in `~/Dotfiles`
   - Then rebuild

6. **Apply changes:**
   - Run: `nrs` (alias for nixos-rebuild switch)
   - If rebuild fails:
     - Analyze the error output
     - Identify the root cause (missing dependency, syntax error, etc.)
     - Fix the issue and retry
     - Repeat until successful or user asks to stop
   - Report success

7. **Update documentation:**
   - If structural changes were made (new services, major packages), update `~/Dotfiles/CLAUDE.md`

8. **Commit changes (only after successful rebuild):**
   - `cd ~/Dotfiles`
   - `git add -A`
   - `git commit` with a descriptive message (e.g., "Add htop package", "Update flake inputs")
   - Ask user: "Ready to push to remote?"
   - Only push if user confirms

## Package Locations

- **User packages:** `configuration.nix` → `users.users.sasha.packages` or `hosts/fw13/default.nix` → `home.packages`
- **System packages:** `configuration.nix` → `environment.systemPackages`
- **Flake inputs:** `flake.nix` → for adding external flakes
- **System services:** `modules/nixos/services.nix`

## Claude Code Settings

All Claude Code configuration is managed via Home Manager. **Never edit `~/.claude/` directly** - those files will be overwritten on rebuild.

**Source of truth:**
```
~/Dotfiles/sources/claude/
├── CLAUDE.md           # Global context
├── settings.json       # Claude Code settings
├── commands/           # Slash commands
├── skills/             # Skills like this one
└── context/            # Shared context files
```

**Workflow for Claude settings changes:**
1. Edit the source file in `~/Dotfiles/sources/claude/`
2. Run `nrs` to deploy

**Examples:**
- Modify settings: Edit `~/Dotfiles/sources/claude/settings.json`
- Add command: Create `~/Dotfiles/sources/claude/commands/my-command.md`
- Add skill: Create `~/Dotfiles/sources/claude/skills/skill-name/SKILL.md`