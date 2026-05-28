---
name: nix-config
description: "Declarative macOS config via Nix (packages, apps, dotfiles, system settings). Use when: (1) Permission denied or root-owned on config/dotfiles (indicates Nix-managed), (2) Adding packages or apps, (3) Configuring programs, (4) Rebuilding system (make switch)."
---

# Nix Config

Declarative macOS environment at `~/nix-config`. See the repo's CLAUDE.md for full architecture.

## Adding Packages

**CLI tools** → `users/tengjizhang/home/packages.nix`
```nix
home.packages = with pkgs; [
  ripgrep
  jq
  # ...
];
```

**GUI apps** → `users/tengjizhang/darwin.nix`
```nix
homebrew.casks = [ "raycast" "obsidian" ];
```

**Third-party taps** → Use full `tap/cask` path:
```nix
homebrew.casks = [ "steipete/tap/codexbar" ];
```

**Mac App Store** → `users/tengjizhang/darwin.nix`
```nix
homebrew.masApps = { "Things" = 904280696; };
```

## npm Package Pattern

For latest npm packages, use `pnpm dlx` wrapper:

```nix
(writeShellScriptBin "toolname" ''
  exec ${pnpm}/bin/pnpm dlx @scope/package@latest "$@"
'')
```

Examples in packages.nix: `claude`, `codex`, `gemini`, `gccli`

## Rebuild

```bash
cd ~/nix-config && make switch > /tmp/nix-switch.log 2>&1 && echo "✓ Switch succeeded" || echo "✗ Switch failed (see /tmp/nix-switch.log)"
```

## Workflow

1. Edit the appropriate .nix file
2. Commit changes (keeps git clean before rebuild)
3. `make switch` to rebuild and activate
4. Push changes

## Key Files

- `flake.nix` - Inputs/outputs, system definition
- `users/tengjizhang/home/packages.nix` - CLI packages
- `users/tengjizhang/home/programs.nix` - Program configs (git, neovim, etc.)
- `users/tengjizhang/darwin.nix` - Homebrew, macOS settings
