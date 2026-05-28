---
name: aerospace
description: Help with AeroSpace window manager configuration, keybindings, and workspace management. Use when the user asks about AeroSpace, window management, workspaces, or tiling configurations.
---

# AeroSpace Window Manager Skill

## Configuration Location

The main AeroSpace configuration file is located at:

- **Primary config**: `/Users/trent/.aerospace.toml`
- **Chezmoi source**: `/Users/trent/.local/share/chezmoi/dot_aerospace.toml`

## Official Documentation

Always reference the official AeroSpace documentation when helping with configuration:

- **Main Guide**: https://nikitabobko.github.io/AeroSpace/guide
- **Commands**: https://nikitabobko.github.io/AeroSpace/commands
- **Configuration**: https://nikitabobko.github.io/AeroSpace/guide#configuring

## Key Concepts

AeroSpace is a tiling window manager for macOS that uses:

- TOML configuration format
- Workspace-based organization
- Vim-style keybindings
- Tree-based window layouts

## When Helping Users

1. Always read the current config at `/Users/trent/.aerospace.toml` first
2. Reference the official documentation for correct syntax and options
3. Explain changes clearly with examples
4. Preserve existing user customizations
5. Test configurations are valid TOML format

## Common Tasks

- Adding/modifying keybindings
- Configuring workspaces
- Setting up window rules
- Adjusting layout behavior
- Managing gaps and padding
