# Neovim Configuration

## Structure

```
nvim/
├── init.lua                    # Entry point: core options, autocommands
├── install                     # Installation script
├── lazy-lock.json              # Plugin version lockfile
├── lua/
│   ├── config/
│   │   ├── lazy.lua            # Lazy.nvim bootstrap
│   │   └── mappings.lua        # All key bindings
│   ├── plugins/                # Plugin specs (one file per category)
│   │   ├── ai.lua              # Copilot
│   │   ├── lsp.lua             # LSP, Mason, none-ls
│   │   ├── telescope.lua       # Fuzzy finder
│   │   ├── treesitter.lua      # Syntax highlighting
│   │   ├── git.lua             # Git integration
│   │   ├── editor.lua          # Editor enhancements
│   │   ├── ui.lua              # UI improvements
│   │   └── ...
│   └── util/                   # Utility modules
│       ├── lsp.lua             # LSP helpers (on_attach, capabilities)
│       ├── format.lua          # Formatting utilities
│       ├── mapping.lua         # Mapping helpers
│       └── ...
└── after/ftplugin/             # Filetype-specific settings
```

## Key Concepts

### Plugin Manager: Lazy.nvim

Plugins are defined in `lua/plugins/*.lua` files. Each file returns a table of plugin specs.

```lua
-- Example: lua/plugins/example.lua
return {
    {
        "author/plugin-name",
        event = "BufReadPost",  -- Lazy load trigger
        opts = { ... },         -- Plugin options
        config = function() ... end,  -- Custom setup
    },
}
```

### Adding a Plugin

1. Create or edit a file in `lua/plugins/`
2. Add the plugin spec
3. Restart Neovim or run `:Lazy sync`

### Key Bindings

All mappings are in `lua/config/mappings.lua`, organized by mode and category.

Leader key: `<Space>`

### LSP Servers

Managed by Mason. Configured in `lua/plugins/lsp.lua`:
- `ensure_installed` list in Mason opts
- Server configs in the `servers` table

### Important Notes

- Clipboard integrates with `rdm` in Codespaces for copy/paste
- Mason binaries are added to PATH in `init.lua`
- Format on save is enabled for specific filetypes
