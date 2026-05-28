# Neovim Configuration Reference

Neovim Lua configuration using lazy.nvim for this repository.

## Configuration Location

`roles/home-manager/core-apps/neovim/`
```
neovim/
├── default.nix           # Home-manager module
├── init.lua              # Main config entry point
└── lua/
    ├── config/
    │   └── lazy.lua      # lazy.nvim bootstrap
    ├── plugins/
    │   ├── plugins.lua   # Plugin definitions
    │   ├── copilot-chat.lua
    │   └── java/
    │       └── init.lua
    └── settings/
        ├── functions.lua
        ├── setup.lua
        ├── nvim-treesitter.lua
        ├── nvim-cmp.lua
        ├── nvim-metals.lua
        ├── telescope.lua
        └── emmet-ls.lua
```

## default.nix Structure

```nix
{ input, pkgs, lib, config, inputs, ... }:
{
  home.packages = with pkgs; [
    inputs.neovim-nightly-overlay.packages.${pkgs.stdenv.hostPlatform.system}.default
  ];

  home.file = {
    ".config/nvim/init.lua".source = ./init.lua;
    ".config/nvim/lua/config/lazy.lua".source = ./lua/config/lazy.lua;
    ".config/nvim/lua/plugins/plugins.lua".source = ./lua/plugins/plugins.lua;
    # ... other files
  };
}
```

## lazy.nvim Bootstrap

```lua
-- lua/config/lazy.lua
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = "https://github.com/folke/lazy.nvim.git"
  vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup({
  spec = {
    { import = "plugins" },
  },
  install = { colorscheme = { "habamax" } },
  checker = { enabled = true },
})
```

## Core Settings (init.lua)

```lua
local opt = vim.opt
local g = vim.g

-- Display
opt.colorcolumn = "80"
opt.number = true
opt.relativenumber = true
opt.termguicolors = true
opt.wrap = false

-- Indentation
opt.expandtab = true
opt.shiftwidth = 4
opt.tabstop = 4
opt.softtabstop = 4
opt.smartindent = true

-- Search
opt.hlsearch = true
opt.incsearch = true
opt.ignorecase = true
opt.smartcase = true

-- Behavior
opt.hidden = true
opt.mouse = 'a'
opt.undofile = true
opt.splitbelow = true
opt.splitright = true

-- Leader key
g['mapleader'] = ","
```

## Key Mappings

### Core Mappings
```lua
local function map(mode, lhs, rhs, opts)
  local options = {noremap = true}
  if opts then options = vim.tbl_extend('force', options, opts) end
  vim.api.nvim_set_keymap(mode, lhs, rhs, options)
end

-- Exit insert mode
map('i', 'jk', '<ESC>')
map('x', 'jk', '<ESC>')
map('v', 'jk', '<ESC>')

-- Clear search highlight
map('n', '<leader>n', '<cmd>noh<cr>')

-- Buffer management
map('n', '<leader>bd', '<cmd>bd<cr>')

-- File explorer
map('n', '<leader>e', '<cmd>Explore<cr>')

-- Splits
map('n', '<leader>hs', '<cmd>split<cr>')
map('n', '<leader>vs', '<cmd>vsplit<cr>')
map('n', '<leader>cs', '<cmd>close<cr>')

-- Resize splits
map('n', '<leader>h', '<cmd>vertical res -10<cr>')
map('n', '<leader>l', '<cmd>vertical res +10<cr>')
map('n', '<leader>j', '<cmd>res +10<cr>')
map('n', '<leader>k', '<cmd>res -10<cr>')
```

### Telescope Mappings
```lua
map('n', '<leader>ff', '<cmd>Telescope find_files<cr>')
map('n', '<leader>fg', '<cmd>Telescope live_grep<cr>')
map('n', '<leader>fb', '<cmd>Telescope buffers<cr>')
map('n', '<leader>fr', '<cmd>Telescope resume<cr>')
map('n', '<leader>cd', '<cmd>Telescope diagnostics<cr>')
```

### LSP Mappings
```lua
local keyset = vim.keymap.set
local builtin = require('telescope.builtin')

keyset('n', '<leader>gd', builtin.lsp_definitions)
keyset('n', '<leader>gr', builtin.lsp_references)
keyset("n", "K", vim.lsp.buf.hover)
keyset("n", "<leader>ca", vim.lsp.buf.code_action)
keyset("n", "<leader>sr", vim.lsp.buf.rename)
map("n", "<space>e", ":lua vim.diagnostic.open_float(0, { scope = 'line' })<CR>")
```

### Git (Fugitive) Mappings
```lua
map('n', '<leader>gs', '<cmd>Git<cr>')
map('n', '<leader>gc', '<cmd>Git commit<cr>')
map('n', '<leader>gl', '<cmd>Git log<cr>')
map('n', '<leader>gp', '<cmd>Git push<cr>')
```

## Plugin Configuration

### plugins.lua Structure
```lua
return {
  -- Colorscheme (loaded first)
  {
    'peterstorm/tomorrow-night-eighties',
    lazy = false,
    priority = 100,
    config = function()
      vim.cmd([[colorscheme tomorrow-night-eighties]])
    end
  },
  
  -- Telescope
  {
    'nvim-telescope/telescope.nvim',
    dependencies = {
      'nvim-lua/popup.nvim',
      'nvim-lua/plenary.nvim',
      'nvim-telescope/telescope-fzy-native.nvim'
    },
    lazy = false
  },
  
  -- Treesitter
  {
    'nvim-treesitter/nvim-treesitter',
    lazy = false,
    build = ':TSUpdate'
  },
  
  -- LSP
  { 'neovim/nvim-lspconfig' },
  
  -- Completion
  {
    'hrsh7th/nvim-cmp',
    dependencies = {
      'hrsh7th/cmp-buffer',
      'hrsh7th/cmp-nvim-lsp',
    },
  },
  
  -- Scala (Metals)
  {
    'scalameta/nvim-metals',
    dependencies = { "nvim-lua/plenary.nvim" }
  },
  
  -- Java
  { 'nvim-java/nvim-java' },
  
  -- TypeScript
  {
    'pmizio/typescript-tools.nvim',
    dependencies = { 'nvim-lua/plenary.nvim', 'neovim/nvim-lspconfig' },
  },
  
  -- Utilities
  { 'christoomey/vim-tmux-navigator' },
  { 'tpope/vim-surround' },
  { 'tpope/vim-fugitive' },
  { 'justinmk/vim-sneak' },
  { 'hoob3rt/lualine.nvim' },
  { 'numToStr/Comment.nvim', opts = {} },
  { 'github/copilot.vim' },
}
```

## LSP Configuration

### Haskell (HLS)
```lua
vim.lsp.config('hls', {
  filetypes = { 'haskell', 'lhaskell', 'cabal' },
  settings = {
    haskell = {
      formattingProvider = "formolu"
    }
  }
})
vim.lsp.enable('hls')

-- Format on save
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = "*.hs",
  callback = function()
    vim.cmd("silent %!fourmolu -q --stdin-input-file %:p")
  end
})
```

### Scala (Metals)
```lua
-- lua/settings/nvim-metals.lua
local M = {}

M.setup = function()
  local metals_config = require('metals').bare_config()
  metals_config.capabilities = require("cmp_nvim_lsp").default_capabilities()
  metals_config.settings = {
    enableSemanticHighlighting = false,
    showImplicitArguments = true,
    excludedPackages = { "akka.actor.typed.javadsl" },
  }
  
  vim.api.nvim_create_autocmd("FileType", {
    pattern = { "scala", "sbt" },
    callback = function()
      require("metals").initialize_or_attach(metals_config)
    end,
    group = vim.api.nvim_create_augroup("nvim-metals", { clear = true }),
  })
end

return M
```

### Java
```lua
require('java').setup({
  jdk = { auto_install = false },
})
vim.lsp.enable('jdtls')
```

### TypeScript
```lua
require("typescript-tools").setup({})
```

### Lua
```lua
vim.lsp.enable('lua_ls')
```

### Emmet
```lua
-- lua/settings/emmet-ls.lua
local capabilities = vim.lsp.protocol.make_client_capabilities()
capabilities.textDocument.completion.completionItem.snippetSupport = true

vim.lsp.config('emmet_ls', {
  capabilities = capabilities,
  filetypes = { "html", "css", "scss", "javascript", "javascriptreact", 
                "typescript", "typescriptreact", "vue" },
})
vim.lsp.enable('emmet_ls')
```

## Completion (nvim-cmp)

```lua
-- lua/settings/nvim-cmp.lua
local cmp = require('cmp')

cmp.setup({
  sources = {
    { name = 'buffer' },
    { name = 'nvim_lsp' }
  },
  snippet = {
    expand = function(args)
      vim.fn["vsnip#anonymous"](args.body)
    end,
  },
  mapping = cmp.mapping.preset.insert({
    ["<CR>"] = cmp.mapping.confirm({ select = true }),
    ["<Tab>"] = function(fallback)
      if cmp.visible() then
        cmp.select_next_item()
      else
        fallback()
      end
    end,
    ["<S-Tab>"] = function(fallback)
      if cmp.visible() then
        cmp.select_prev_item()
      else
        fallback()
      end
    end,
  }),
})
```

## Treesitter Configuration

```lua
-- lua/settings/nvim-treesitter.lua
require('nvim-treesitter.configs').setup({
  ensure_installed = {
    "scala", "nix", "kotlin", "graphql", "haskell",
    "lua", "bash", "java", "html", "css", "rust",
    "javascript", "typescript", "dockerfile", "jsonc"
  },
  highlight = { enable = true }
})
```

## Telescope Configuration

```lua
-- lua/settings/telescope.lua
local telescope = require('telescope')
local actions = require("telescope.actions")

telescope.load_extension('fzy_native')

telescope.setup({
  pickers = {
    find_files = {
      file_ignore_patterns = { 'node_modules', '%.kml' },
      path_display = { "truncate" },
    },
    buffers = {
      mappings = {
        i = {
          ["<C-d>"] = actions.delete_buffer + actions.move_to_top,
        }
      }
    }
  }
})
```

## Copilot Chat

```lua
-- lua/plugins/copilot-chat.lua
return {
  {
    "CopilotC-Nvim/CopilotChat.nvim",
    dependencies = {
      { "github/copilot.vim" },
      { "nvim-lua/plenary.nvim" },
    },
    opts = {
      window = { layout = "float", width = 0.8, height = 0.7 },
      model = "claude-opus-4.5",
      prompts = {
        Explain = { prompt = "Explain how this code works in detail." },
        Review = { prompt = "Review the code and suggest improvements." },
        Fix = { prompt = "Fix issues in this code and explain what was wrong." },
        Optimize = { prompt = "Optimize this code for better performance." },
        Tests = { prompt = "Write tests for this code." },
      },
    },
    keys = {
      { "<leader>cc", "<cmd>CopilotChatToggle<cr>", desc = "Toggle Copilot Chat" },
      { "<leader>ce", "<cmd>CopilotChatExplain<cr>", desc = "Explain Code" },
      { "<leader>cr", "<cmd>CopilotChatReview<cr>", desc = "Review Code" },
      { "<leader>cf", "<cmd>CopilotChatFix<cr>", desc = "Fix Code" },
      { "<leader>co", "<cmd>CopilotChatOptimize<cr>", desc = "Optimize Code" },
      { "<leader>ct", "<cmd>CopilotChatTests<cr>", desc = "Generate Tests" },
    },
  },
}
```

## Formatting

### Neoformat (JavaScript/TypeScript)
```lua
vim.g.neoformat_try_node_exe = 1

vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = { "*.js", "*.jsx", "*.ts", "*.tsx" },
  command = "Neoformat prettier",
})
```

### Conform (Java)
```lua
require("conform").setup({
  formatters_by_ft = {
    java = { "google-java-format" },
  },
  format_on_save = function(bufnr)
    local ignore_filetypes = { "sql" }
    if vim.tbl_contains(ignore_filetypes, vim.bo[bufnr].filetype) then
      return
    end
    return { timeout_ms = 500, lsp_format = "fallback" }
  end,
})
```

## Adding New Plugins

1. Add to `lua/plugins/plugins.lua`:
```lua
{
  'author/plugin-name',
  dependencies = { ... },
  config = function()
    require('plugin-name').setup({ ... })
  end,
  -- Optional: lazy loading
  event = "BufReadPre",
  ft = { "lua", "nix" },
  cmd = { "PluginCommand" },
  keys = { { "<leader>p", "<cmd>PluginCommand<cr>" } },
}
```

2. If complex config, create `lua/settings/plugin-name.lua`:
```lua
local M = {}
M.setup = function()
  -- Configuration
end
return M
```

3. Call from init.lua:
```lua
require('settings.plugin-name').setup()
```

## Key Binding Summary

| Category | Key | Action |
|----------|-----|--------|
| **General** | `,n` | Clear search highlight |
| | `,bd` | Delete buffer |
| | `,e` | File explorer |
| **Splits** | `,hs` | Horizontal split |
| | `,vs` | Vertical split |
| | `,cs` | Close split |
| **Telescope** | `,ff` | Find files |
| | `,fg` | Live grep |
| | `,fb` | Buffers |
| | `,fr` | Resume search |
| **LSP** | `,gd` | Go to definition |
| | `,gr` | References |
| | `K` | Hover |
| | `,ca` | Code action |
| | `,sr` | Rename symbol |
| **Git** | `,gs` | Git status |
| | `,gc` | Git commit |
| | `,gl` | Git log |
| | `,gp` | Git push |
| **Copilot** | `,cc` | Chat toggle |
| | `,ce` | Explain |
| | `,cr` | Review |
| **Metals** | `,mc` | Metals commands |
