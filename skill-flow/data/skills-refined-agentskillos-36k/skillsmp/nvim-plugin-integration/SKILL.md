---
name: nvim-plugin-integration
description: Add or debug neovim plugins with lazy.nvim
---

# Nvim Plugin Integration

Add, configure, or debug neovim plugins using lazy.nvim.

## Config Structure

| Path | Purpose |
|------|---------|
| `nvim/init.lua` | Main config, settings, general keymaps |
| `nvim/lua/plugins/plugins.lua` | Simple plugins with minimal config |
| `nvim/lua/plugins/<name>.lua` | Plugins with keymaps or complex config |
| `docs/nvim.md` | Plugin list and keymaps documentation |

## Adding a Plugin

**Simple plugins** → add to `nvim/lua/plugins/plugins.lua`:
```lua
{ "author/plugin-name", ft = "filetype", opts = {} }
```

**Complex plugins** → create `nvim/lua/plugins/<name>.lua`:
```lua
return {
  "author/plugin-name",
  ft = "filetype",        -- lazy load on filetype
  event = "BufReadPost",  -- or lazy load on event
  opts = {},
  config = function(_, opts)
    require("plugin-name").setup(opts)
  end,
}
```

Update `docs/nvim.md` with new keymaps.

## Debugging

| Command | Purpose |
|---------|---------|
| `:Lazy` | Check if plugin is loaded |
| `:verbose nmap <key>` | Find where mapping is defined |
| `:autocmd FileType <ft>` | List autocmds for filetype |
| `:Lazy reload <name>` | Force reload plugin |

## E2E Testing

See [nvim-remote-api-testing.md](../../../docs/nvim-remote-api-testing.md) for headless testing.
