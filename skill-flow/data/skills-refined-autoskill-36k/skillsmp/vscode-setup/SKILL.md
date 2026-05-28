---
name: vscode-setup
description: VSCode configuration and setup guide including settings apply/save, VSCode-Neovim synchronization, and initialization
---

# VSCode settings

## Apply VSCode settings

```sh
make vscode-apply
```

## Save VSCode settings

```sh
make vscode-save
```

## VSCode-Neovim Synchronization

### Synchronize VSCode and Neovim settings

```sh
make vscode-sync
```

This command automatically synchronizes settings between VSCode and Neovim. The following settings are mainly synchronized:

- Key bindings
- Editor appearance (font, theme, etc.)
- Basic editing behavior (tab size, word wrap, etc.)

### Setup Neovim initialization file for VSCode

```sh
make vscode-neovim-init
```

This command generates the initialization file needed to use Neovim from VSCode.
It configures the necessary settings to make Neovim mode function correctly within VSCode.
