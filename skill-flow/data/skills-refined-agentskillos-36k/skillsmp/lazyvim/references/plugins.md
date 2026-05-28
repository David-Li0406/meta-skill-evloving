# LazyVim Plugin Reference

Detailed configuration patterns for LazyVim's bundled plugins.

## Table of Contents

- [LSP Configuration](#lsp-configuration)
- [Treesitter](#treesitter)
- [Completion (blink.cmp)](#completion-blinkcmp)
- [Formatting (conform.nvim)](#formatting-conformnvim)
- [UI Plugins](#ui-plugins)
- [Extras](#extras)

## LSP Configuration

### Adding servers with custom settings

```lua
-- lua/plugins/lsp.lua
return {
  "neovim/nvim-lspconfig",
  opts = {
    servers = {
      lua_ls = {
        settings = {
          Lua = {
            workspace = { checkThirdParty = false },
            completion = { callSnippet = "Replace" },
          },
        },
      },
      tsserver = {
        settings = {
          typescript = { inlayHints = { includeInlayParameterNameHints = "all" } },
        },
      },
      jsonls = {
        settings = {
          json = {
            schemas = require("schemastore").schemas(),
            validate = { enable = true },
          },
        },
      },
    },
  },
}
```

### Custom on_attach

```lua
return {
  "neovim/nvim-lspconfig",
  opts = {
    servers = {
      gopls = {
        on_attach = function(client, bufnr)
          -- Custom keymaps for this server only
          vim.keymap.set("n", "<leader>gI", vim.lsp.buf.implementation, { buffer = bufnr })
        end,
      },
    },
  },
}
```

### Mason ensure_installed

```lua
return {
  "williamboman/mason.nvim",
  opts = {
    ensure_installed = {
      "stylua",
      "shellcheck",
      "shfmt",
      "black",
      "prettier",
    },
  },
}
```

## Treesitter

### Adding parsers

```lua
return {
  "nvim-treesitter/nvim-treesitter",
  opts = function(_, opts)
    vim.list_extend(opts.ensure_installed, {
      "bash",
      "html",
      "javascript",
      "json",
      "lua",
      "markdown",
      "markdown_inline",
      "python",
      "query",
      "regex",
      "tsx",
      "typescript",
      "vim",
      "yaml",
    })
  end,
}
```

### Textobjects configuration

```lua
return {
  "nvim-treesitter/nvim-treesitter-textobjects",
  opts = {
    textobjects = {
      select = {
        enable = true,
        keymaps = {
          ["af"] = "@function.outer",
          ["if"] = "@function.inner",
          ["ac"] = "@class.outer",
          ["ic"] = "@class.inner",
        },
      },
      move = {
        enable = true,
        goto_next_start = { ["]f"] = "@function.outer" },
        goto_previous_start = { ["[f"] = "@function.outer" },
      },
    },
  },
}
```

## Completion (blink.cmp)

### Custom sources and keymaps

```lua
return {
  "saghen/blink.cmp",
  opts = {
    keymap = {
      ["<C-space>"] = { "show", "show_documentation", "hide_documentation" },
      ["<C-e>"] = { "hide" },
      ["<CR>"] = { "accept", "fallback" },
      ["<Tab>"] = { "select_next", "snippet_forward", "fallback" },
      ["<S-Tab>"] = { "select_prev", "snippet_backward", "fallback" },
    },
    sources = {
      default = { "lsp", "path", "snippets", "buffer" },
    },
  },
}
```

## Formatting (conform.nvim)

### Full configuration example

```lua
return {
  "stevearc/conform.nvim",
  opts = {
    formatters_by_ft = {
      lua = { "stylua" },
      python = { "isort", "black" },
      javascript = { "prettier" },
      typescript = { "prettier" },
      javascriptreact = { "prettier" },
      typescriptreact = { "prettier" },
      css = { "prettier" },
      html = { "prettier" },
      json = { "prettier" },
      yaml = { "prettier" },
      markdown = { "prettier" },
      sh = { "shfmt" },
    },
    format_on_save = {
      timeout_ms = 500,
      lsp_fallback = true,
    },
  },
}
```

### Disable format on save for specific filetypes

```lua
return {
  "stevearc/conform.nvim",
  opts = {
    format_on_save = function(bufnr)
      local ignore_filetypes = { "sql", "java" }
      if vim.tbl_contains(ignore_filetypes, vim.bo[bufnr].filetype) then
        return
      end
      return { timeout_ms = 500, lsp_fallback = true }
    end,
  },
}
```

## UI Plugins

### Lualine customization

```lua
return {
  "nvim-lualine/lualine.nvim",
  opts = function(_, opts)
    opts.sections.lualine_c = {
      { "filename", path = 1 }, -- relative path
    }
    opts.sections.lualine_x = {
      { "encoding" },
      { "fileformat" },
      { "filetype" },
    }
  end,
}
```

### Bufferline configuration

```lua
return {
  "akinsho/bufferline.nvim",
  opts = {
    options = {
      mode = "tabs",
      show_buffer_close_icons = false,
      show_close_icon = false,
      separator_style = "slant",
    },
  },
}
```

### Which-key group labels

```lua
return {
  "folke/which-key.nvim",
  opts = {
    spec = {
      { "<leader>g", group = "git" },
      { "<leader>gh", group = "hunks" },
      { "<leader>t", group = "test" },
      { "<leader>d", group = "debug" },
    },
  },
}
```

### Noice customization

```lua
return {
  "folke/noice.nvim",
  opts = {
    presets = {
      bottom_search = true,
      command_palette = true,
      long_message_to_split = true,
    },
    routes = {
      -- Hide "written" messages
      { filter = { event = "msg_show", kind = "", find = "written" }, opts = { skip = true } },
    },
  },
}
```

## Extras

### Common language extras

```lua
-- lua/config/lazy.lua
spec = {
  { "LazyVim/LazyVim", import = "lazyvim.plugins" },

  -- Languages
  { import = "lazyvim.plugins.extras.lang.typescript" },
  { import = "lazyvim.plugins.extras.lang.python" },
  { import = "lazyvim.plugins.extras.lang.rust" },
  { import = "lazyvim.plugins.extras.lang.go" },
  { import = "lazyvim.plugins.extras.lang.json" },
  { import = "lazyvim.plugins.extras.lang.yaml" },
  { import = "lazyvim.plugins.extras.lang.docker" },

  -- Coding
  { import = "lazyvim.plugins.extras.coding.copilot" },
  { import = "lazyvim.plugins.extras.coding.mini-surround" },

  -- Editor
  { import = "lazyvim.plugins.extras.editor.mini-files" },
  { import = "lazyvim.plugins.extras.editor.outline" },

  -- DAP (debugging)
  { import = "lazyvim.plugins.extras.dap.core" },

  -- User plugins
  { import = "plugins" },
}
```

### Overriding extra plugins

After importing an extra, override its plugins normally:

```lua
-- Extra imports lazyvim.plugins.extras.lang.rust which enables rust-analyzer
-- Override rust-analyzer settings:
return {
  "neovim/nvim-lspconfig",
  opts = {
    servers = {
      rust_analyzer = {
        settings = {
          ["rust-analyzer"] = {
            cargo = { allFeatures = true },
            checkOnSave = { command = "clippy" },
          },
        },
      },
    },
  },
}
```
