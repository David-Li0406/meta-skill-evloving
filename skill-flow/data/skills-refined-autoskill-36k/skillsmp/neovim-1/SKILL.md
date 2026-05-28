---
name: neovim
description: Configure Neovim 0.12+ with built-in features, minimal plugins, and vim.pack-based setup.
---

# Neovim Configuration Skill

Configure Neovim 0.12+ with a focus on built-in features and minimal plugins.

## Philosophy

- **Minimize plugins** - Prefer built-in Neovim features over plugins
- **Use vim.pack** - Native package manager instead of lazy.nvim
- **LSP-first** - Use built-in LSP for completions, diagnostics, folding
- **Treesitter** - For syntax highlighting and text objects

## Neovim 0.12 Features

- `vim.pack.add()` - Native plugin management
- `vim.lsp.foldexpr()` - LSP-based folding
- `vim.lsp.completion.enable()` - Built-in completion
- `vim.lsp.semantic_tokens.enable(true, { bufnr = bufnr })` - Semantic highlighting

## Config Structure

- `~/.config/nvim/init.lua` - Main config
- `~/.config/nvim/ftplugin/` - Filetype-specific configs
- `~/.config/nvim/lua/` - Custom Lua modules

## Documentation Access

Use `~/bin/nvim-doc.sh` to fetch Neovim 0.12 documentation:

```bash
~/bin/nvim-doc.sh news      # What's new in 0.12
~/bin/nvim-doc.sh lsp       # LSP documentation
~/bin/nvim-doc.sh treesitter
```

## Current Plugins (via vim.pack)

- nvim-lspconfig
- nvim-treesitter
- conform.nvim (formatting)
- fzf-lua
- oil.nvim (file explorer)
- aerial.nvim (outline)

## LSP Settings

- Rust: rust-analyzer with `check.command = "clippy"`
- Folding: `vim.lsp.foldexpr()` for LSP-capable languages

## Best Practices

- Check if a feature exists in Neovim 0.12 before suggesting a plugin
- Use ftplugin/ for language-specific settings
- Snippets go in LSP server config (e.g., rust-analyzer snippets)
