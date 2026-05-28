---
name: nix-operations
description: Complete guide for Nix operations including home-manager apply, nix-darwin apply, package installation, rollback procedures, architecture support (Apple Silicon/Intel Mac), and NixOS configuration
---

# Nix operations

Basic operations are performed using `make`.

- [Architecture Support](#architecture-support)
- [Nix](#nix)
  - [Apply home-manager settings](#apply-home-manager-settings)
  - [Apply all nix-darwin settings](#apply-all-nix-darwin-settings)
  - [Apply nix-darwin-homebrew settings](#apply-nix-darwin-homebrew-settings)
  - [Apply all nix settings](#apply-all-nix-settings)
  - [Install a new package](#install-a-new-package)
  - [Rollback](#rollback)

## Architecture Support

This repository supports both Apple Silicon and Intel Mac. The architecture is auto-detected at build time.

| Architecture | nixpkgs | nix-darwin | home-manager |
|--------------|---------|------------|--------------|
| Apple Silicon (aarch64-darwin) | unstable | unstable | unstable |
| Intel Mac (x86_64-darwin) | 24.11 | 24.11 | 24.11 |

### Version-specific Settings

Version-specific settings are isolated in `compat/` directories:

- `darwin/compat/unstable.nix`: unstable-only darwin options (`system.primaryUser`, `homebrew.user`)
- `darwin/compat/nixpkgs-2411.nix`: 24.11-only settings (Homebrew package exclusions for macOS 13 compatibility)
- `home-manager/compat/unstable.nix`: unstable-only packages (`nerd-fonts.hack`, `xan`, `nil`, `nil_ls`)
- `home-manager/compat/nixpkgs-2411.nix`: 24.11-only packages (`nerdfonts.override`)

### Intel Mac (24.11) Limitations

Due to macOS 13 (Tier 3) and older Xcode limitations, the following Homebrew packages are excluded on Intel Mac:

- **brews**: `aqua`, `im-select`, `mas`, `mise`, `uv`, `skhd`, `yabai` (require Xcode 15.2+ or build from source)
- **casks**: `lm-studio` (ARM64 only)

These tools can be installed via nixpkgs or alternative methods if needed.

## Nix

### Apply home-manager settings

```sh
make home-manager-apply
```

### Apply all nix-darwin settings

```sh
make nix-darwin-apply
```

#### Apply nix-darwin-homebrew settings

```sh
make nix-darwin-homebrew-apply
```

#### Apply nix-darwin-system settings

```sh
make nix-darwin-system-apply
```

#### Apply nix-darwin-service settings

```sh
make nix-darwin-service-apply
```

### Apply all nix settings

```sh
make nix-update-all
```

### Install a new package

```sh
# search package: https://search.nixos.org/packages

# install package
nix profile install nixpkgs#hoge
```

### Upgrade a package

```sh
nix profile upgrade hoge
```

### Rollback

#### 1. Check generations

```sh
nix-env --list-generations
```

```
1   2024-10-17 10:19:29
2   2024-10-17 11:55:16
3   2024-10-17 19:19:37
4   2024-11-06 18:37:37
5   2024-11-06 18:52:58   (current)
```

#### 2. Rollback

```sh
nix-env --rollback

# or

nix-env --switch-generation 3
```

## Special Configuration Handling

### Claude Configuration

While most dotfiles configurations are managed through the Nix store for reproducibility and immutability, the Claude configuration is handled as an exception using direct symbolic links.

**Rationale:**
- Claude Desktop application modifies its configuration files directly during runtime
- The Nix store approach would prevent Claude from updating its own settings
- Direct symbolic links allow bidirectional synchronization between the application and dotfiles

**Implementation:**
The Claude configuration files are linked directly from the dotfiles repository:
```sh
~/.claude/CLAUDE.md → ~/git_repos/github.com/barleytea/dotfiles/home-manager/claude/config/CLAUDE.md
~/.claude/settings.json → ~/git_repos/github.com/barleytea/dotfiles/home-manager/claude/config/settings.json
```

This approach enables:
- Claude to modify its configuration files as needed
- Changes to persist in the dotfiles repository automatically
- Version control of Claude settings through git

**Configuration Location:**
- Dotfiles: `home-manager/claude/default.nix`
- Target directory: `~/.claude/`

### NixOS: Running Generic Linux Binaries

If you install pre-built binaries that target "generic" Linux environments (for example the Claude CLI), NixOS will refuse to start them with an error like:

```
Could not start dynamically linked executable: claude
NixOS cannot run dynamically linked executables intended for generic linux environments out of the box.
```

The `nixos/system/default.nix` module now enables `programs.nix-ld` with the common runtime libraries (`glibc`, `libstdc++`, `openssl`, `zlib`, `libX11`, etc.) so these binaries can locate their dependencies. After updating the flake, rebuild the machine to pick up the loader:

```sh
sudo nixos-rebuild switch --flake .#desktop
```

If a third-party binary still complains about missing libraries, extend the `programs.nix-ld.libraries` list in `nixos/system/default.nix` with the required packages and rebuild again.
