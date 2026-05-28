---
name: nix
description: NixOS package management and dotfiles configuration. Activates for package install/remove/search, system updates, configuration changes, and Claude Code settings changes.
---

# NixOS Package Management & Dotfiles

**User input:** $ARGUMENTS

## Style

Comment sparingly in `.nix` files. Nix is declarative so code is self-documenting. Only add comments to:
- Delineate sections in long package lists
- Explain non-obvious workarounds
- Note dependencies between options that aren't apparent

## Instructions

1. **Read context:** `~/Dotfiles/CLAUDE.md` for layout

2. **Parse request:**
   - **Install/remove package:** Edit `hosts/fw13/default.nix`
   - **Search:** `nix search nixpkgs <query>`
   - **Update:** `nix flake update` then rebuild
   - **Config changes:** Edit appropriate module in `modules/`
   - **Claude settings:** Edit `~/Dotfiles/sources/claude/` (see below)

3. **For packages:**
   - Confirm package name: `nix search nixpkgs <name>`
   - Edit `hosts/fw13/default.nix` under `home.packages`

4. **Apply:** Run `nrs`
   - If rebuild fails, analyze error, fix, retry
   - Report success

5. **Commit (after successful rebuild):**
   - `git add -A && git commit -m "..."`
   - Ask before push

## Package Locations

- **User packages:** `hosts/fw13/default.nix` → `home.packages`
- **Flake inputs:** `flake.nix`
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
