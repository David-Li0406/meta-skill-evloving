---
name: lazyvim
description: Expert guidance for LazyVim Neovim configuration. Use when configuring Neovim with LazyVim, writing plugin specs, adding language servers, customizing keymaps, enabling extras, troubleshooting lazy-loading, or any LazyVim/lazy.nvim related task. Triggers on mentions of LazyVim, lazy.nvim, Neovim configuration, plugin specs, opts pattern, mason, lspconfig, or ~/.config/nvim.
---

# LazyVim Expert

Configure and customize LazyVim—the lazy-loading Neovim framework built on lazy.nvim.

## Core Concepts

**Philosophy**: Lazy-load everything. Plugins load on events (keys, commands, filetypes), not at startup.

**Configuration merging**: User specs deep-merge with LazyVim defaults via `opts` tables. No forking required.

**Directory structure**:
```
~/.config/nvim/
├── init.lua           # Bootstrap lazy.nvim, set leader keys
├── lazy-lock.json     # Version lock (commit to git)
└── lua/
    ├── config/
    │   ├── options.lua    # vim.opt settings (loaded first)
    │   ├── keymaps.lua    # User keymaps (loaded after defaults)
    │   ├── autocmds.lua   # User autocommands
    │   └── lazy.lua       # lazy.nvim setup options
    └── plugins/           # User plugin specs
```

**Load order**: options.lua → plugins install → LazyVim defaults → user keymaps/autocmds

## Plugin Spec Pattern

All customization happens via plugin specs in `lua/plugins/*.lua`:

```lua
return {
  "author/plugin-name",
  enabled = true,           -- false to disable a default plugin
  event = "VeryLazy",       -- load trigger: VeryLazy, BufReadPost, InsertEnter
  keys = { ... },           -- keymaps that trigger loading
  opts = { ... },           -- merged with default opts
  dependencies = { ... },
}
```

### The opts Pattern

**Merge with defaults** (most common):
```lua
return {
  "neovim/nvim-lspconfig",
  opts = {
    servers = {
      pyright = {
        settings = { python = { analysis = { typeCheckingMode = "strict" } } }
      },
    },
  },
}
```

**Function for complex logic** (modify in place):
```lua
return {
  "nvim-treesitter/nvim-treesitter",
  opts = function(_, opts)
    vim.list_extend(opts.ensure_installed, { "lua", "python", "rust" })
  end,
}
```

## Common Tasks

### Add a language server

File: `lua/plugins/lsp.lua`
```lua
return {
  "neovim/nvim-lspconfig",
  opts = {
    servers = {
      rust_analyzer = {},
      gopls = { settings = { gopls = { usePlaceholders = true } } },
    },
  },
}
```

Mason auto-installs servers listed here.

### Configure formatting

File: `lua/plugins/formatting.lua`
```lua
return {
  "stevearc/conform.nvim",
  opts = {
    formatters_by_ft = {
      python = { "black", "isort" },
      javascript = { "prettier" },
      lua = { "stylua" },
    },
  },
}
```

### Custom keymaps

File: `lua/config/keymaps.lua`
```lua
vim.keymap.set("n", "<leader>gg", "<cmd>LazyGit<cr>", { desc = "LazyGit" })

-- Delete a default keymap
vim.keymap.del("n", "<leader>L")
```

### Disable a default plugin

```lua
return {
  "folke/flash.nvim",
  enabled = false,
}
```

### Enable an Extra

In `lua/config/lazy.lua` spec list:
```lua
{ import = "lazyvim.plugins.extras.lang.typescript" },
{ import = "lazyvim.plugins.extras.lang.rust" },
{ import = "lazyvim.plugins.extras.coding.copilot" },
```

Or use `:LazyExtras` UI to toggle interactively.

## LazyVim API

Global `LazyVim` table (alias for `require("lazyvim.util")`):

| Method | Use |
|--------|-----|
| `LazyVim.has("plugin")` | Check if plugin is installed (for conditional config) |
| `LazyVim.on_load("plugin", fn)` | Run callback after plugin loads |
| `LazyVim.root()` | Get project root (detects .git, Makefile) |
| `LazyVim.toggle.diagnostics()` | Toggle diagnostics display |
| `LazyVim.config.icons` | Centralized icon table |

Example conditional keymap:
```lua
if LazyVim.has("flash.nvim") then
  vim.keymap.set("n", "s", function() require("flash").jump() end)
end
```

## Key Plugins Reference

**UI**: noice.nvim (command UI), which-key.nvim (keymap hints), snacks.nvim (dashboard/terminal/git), bufferline.nvim, lualine.nvim

**LSP**: nvim-lspconfig, mason.nvim (installs LSP/DAP/linters), nvim-treesitter

**Completion**: blink.cmp (newer) or nvim-cmp

**Formatting**: conform.nvim

## Load Events

| Event | When |
|-------|------|
| `VeryLazy` | After startup, deferred |
| `BufReadPost` | After reading any file |
| `BufReadPre` | Before reading file |
| `InsertEnter` | Entering insert mode |
| `CmdlineEnter` | Opening command line |
| `LspAttach` | LSP attaches to buffer |

## Troubleshooting

**Plugin not loading**: Check `event`, `keys`, or `cmd` triggers. Use `:Lazy log` to see load order.

**Opts not applying**: Ensure spec uses same plugin string as LazyVim default. Use function form to debug:
```lua
opts = function(_, opts)
  vim.print(opts)  -- inspect current opts
  opts.my_option = true
end,
```

**Version conflicts**: Delete `lazy-lock.json` and run `:Lazy sync` to regenerate.

**Startup slow**: Run `:Lazy profile` to identify slow plugins. Ensure `lazy = true` default is active.

For detailed plugin configurations, see references/plugins.md.
