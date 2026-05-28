---
name: nixos-package-management
description: Use this skill for managing NixOS packages and dotfiles configuration, including installing, removing, and searching for packages, as well as system updates and configuration changes.
---

# NixOS Package Management & Dotfiles

**User input:** $ARGUMENTS

## Instructions

1. **Read context and config:**
   - Read `~/Dotfiles/CLAUDE.md` to understand the dotfiles layout.
   - Read `~/Dotfiles/configuration.nix` for current packages.
   - Read `~/Dotfiles/flake.nix` if flake changes are needed.

2. **Parse the request:**
   - **Install package:** User wants to add a package (e.g., "install htop").
   - **Remove package:** User wants to remove a package.
   - **Search:** User wants to find a package (e.g., "search for video editor").
   - **Update:** User wants to update the system.
   - **Configuration changes:** User wants to modify settings or services.

3. **For package install/remove:**
   - Confirm the exact package name: `nix search nixpkgs <name>`.
   - Edit `configuration.nix` or `hosts/fw13/default.nix` to add/remove from the appropriate package list.
   - Show the diff to the user.

4. **For search:**
   - Run `nix search nixpkgs <query>` and summarize results.
   - Suggest the most relevant package(s).

5. **For updates:**
   - Run `nix flake update` in `~/Dotfiles`.
   - Then rebuild using `nrs` (alias for `nixos-rebuild switch`).

6. **Apply changes:**
   - If rebuild fails:
     - Analyze the error output.
     - Identify the root cause (missing dependency, syntax error, etc.).
     - Fix the issue and retry until successful or user asks to stop.
   - Report success.

7. **Update documentation:**
   - If structural changes were made (new services, major packages), update `~/Dotfiles/CLAUDE.md`.

8. **Commit changes (only after successful rebuild):**
   - `cd ~/Dotfiles`
   - `git add -A`
   - `git commit` with a descriptive message (e.g., "Add htop package").
   - Ask user: "Ready to push to remote?"
   - Only push if user confirms.

## Package Locations

- **User packages:** `configuration.nix` or `hosts/fw13/default.nix` → `users.users.sasha.packages` or `home.packages`.
- **System packages:** `configuration.nix` → `environment.systemPackages`.
- **Flake inputs:** `flake.nix` → for adding external flakes.
- **Claude settings:** Managed via Home Manager in `~/Dotfiles/sources/claude/`.

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
1. Edit the source file in `~/Dotfiles/sources/claude/`.
2. Run `nrs` to deploy.