---
name: nix
description: NixOS package management and dotfiles configuration. Activates for package install/remove/search, system updates, and configuration changes.
---

# NixOS Package Management

Help with NixOS configuration and package management.

**User input:** $ARGUMENTS

## Instructions

1. **Read context and config:**
   - Read `~/Dotfiles/CLAUDE.md` to understand the dotfiles layout
   - Read `~/Dotfiles/configuration.nix` to see current packages
   - Read `~/Dotfiles/flake.nix` if flake changes needed

2. **Parse the request:**
   - **Install package:** User wants to add a package (e.g., "install htop", "add nodejs")
   - **Remove package:** User wants to remove a package
   - **Search:** User wants to find a package (e.g., "search for video editor")
   - **Update:** User wants to update the system
   - **Other:** Configuration changes, services, etc.

3. **For package install/remove:**
   - Search nixpkgs to confirm exact package name: `nix search nixpkgs <name>`
   - Edit `configuration.nix` to add/remove from `users.users.sasha.packages`
   - Show the diff to user

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

- **User packages:** `configuration.nix` → `users.users.sasha.packages`
- **System packages:** `configuration.nix` → `environment.systemPackages`
- **Flake inputs:** `flake.nix` → for adding external flakes
