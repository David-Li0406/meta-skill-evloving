vim.g.mapleader = " "
vim.g.maplocalleader = " "

-- Disable built-ins
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

-- Editor behavior
vim.opt.mouse = "a"
vim.opt.clipboard = "unnamedplus"
vim.opt.undofile = true
vim.opt.undodir = vim.fn.stdpath("data") .. "/undo"
vim.opt.updatetime = 100
vim.opt.confirm = true
vim.opt.autoread = true

-- UI
vim.opt.termguicolors = true
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.signcolumn = "yes:1"
vim.opt.cursorline = false
vim.opt.wrap = false
vim.opt.showmode = false
vim.opt.showcmd = false
vim.opt.ruler = true
vim.opt.pumheight = 10
vim.opt.fillchars = { eob = " " }

-- Search
vim.opt.hlsearch = true
vim.opt.incsearch = true
vim.opt.ignorecase = true
vim.opt.smartcase = true

-- Indentation
vim.opt.expandtab = true
vim.opt.shiftwidth = 2
vim.opt.smartindent = true

-- Splits
vim.opt.splitbelow = true
vim.opt.splitright = true

-- Files
vim.opt.fileencoding = "utf-8"
vim.opt.backup = false
vim.opt.writebackup = false
vim.opt.swapfile = false

-- Completion
vim.opt.completeopt = { "menu", "menuone", "noselect" }

-- Filetype detection
vim.filetype.add({
    extension = { env = "dotenv" },
    filename = {
        [".env"] = "dotenv",
        [".envrc"] = "sh",
    },
})

-- ============================================================================
-- Plugin
-- ============================================================================
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.uv.fs_stat(lazypath) then
  vim.fn.system({
    "git", "clone", "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

local plugins = {
  -- Claude Code
  {
    "coder/claudecode.nvim",
    dependencies = { "folke/snacks.nvim" },
    config = true,
    opts = {
      terminal = {
        split_side = "right",
        split_width_percentage = 0.5,
      },
    },
    keys = {
      { "<leader>c", nil, desc = "Claude Code" },
      { "<leader>cc", "<cmd>ClaudeCode<cr>", desc = "Toggle Claude" },
      { "<leader>cf", "<cmd>ClaudeCodeFocus<cr>", desc = "Focus Claude" },
      { "<leader>cr", "<cmd>ClaudeCode --resume<cr>", desc = "Resume Claude" },
      { "<leader>cs", "<cmd>ClaudeCodeSend<cr>", mode = "v", desc = "Send to Claude" },
    },
  },

  -- snacks.nvim (claudecode dependency)
  {
    "folke/snacks.nvim",
    lazy = false,
    config = true,
  },

  -- Smooth scrolling
  {
    "karb94/neoscroll.nvim",
    config = function()
      local neoscroll = require("neoscroll")
      neoscroll.setup({
        hide_cursor = false,
        easing = "sine",
      })
      local modes = { "n", "v", "x" }
      vim.keymap.set(modes, "<ScrollWheelUp>", function() neoscroll.scroll(-3, { duration = 50 }) end)
      vim.keymap.set(modes, "<ScrollWheelDown>", function() neoscroll.scroll(3, { duration = 50 }) end)
    end,
  },

  -- LSP
  {
    "neovim/nvim-lspconfig",
    event = { "BufReadPre", "BufNewFile" },
    dependencies = { "mason-org/mason-lspconfig.nvim" },
    config = function()
      local lspconfig = require("lspconfig")
      local mason_lspconfig = require("mason-lspconfig")

      -- LSP keymaps
      vim.api.nvim_create_autocmd("LspAttach", {
        group = vim.api.nvim_create_augroup("UserLspConfig", { clear = true }),
        callback = function(args)
          local bufnr = args.buf
          local function map(mode, lhs, rhs, desc)
            vim.keymap.set(mode, lhs, rhs, { buffer = bufnr, desc = desc, silent = true })
          end

          map("n", "K", vim.lsp.buf.hover, "Hover")
          map("n", "<C-k>", vim.lsp.buf.signature_help, "Signature Help")
          map("n", "gd", vim.lsp.buf.definition, "Definition")
          map("n", "gi", vim.lsp.buf.implementation, "Implementation")
          map("n", "gr", vim.lsp.buf.references, "References")
          map("n", "<leader>rn", vim.lsp.buf.rename, "Rename")
          map("n", "<leader>ca", vim.lsp.buf.code_action, "Code Action")
          map("n", "[d", vim.diagnostic.goto_prev, "Prev Diagnostic")
          map("n", "]d", vim.diagnostic.goto_next, "Next Diagnostic")
        end,
      })

      -- Diagnostic config
      vim.diagnostic.config({
        virtual_text = true,
        underline = true,
        -- float = { border = "rounded" },
      })

      -- Mason setup
      mason_lspconfig.setup({
        handlers = {
          function(server_name)
            lspconfig[server_name].setup({})
          end,
        },
      })
    end,
  },

  {
    "mason-org/mason.nvim",
    lazy = false,
    config = function()
      require("mason").setup()
    end,
  },

  {
    "mason-org/mason-lspconfig.nvim",
    lazy = false,
    dependencies = { "neovim/nvim-lspconfig" },
  },

  {
    "WhoIsSethDaniel/mason-tool-installer.nvim",
    lazy = false,
    config = function()
      require("mason-tool-installer").setup({
        ensure_installed = { "pyright", "ruff" },
      })
    end,
  },

  -- Completion
  { "L3MON4D3/LuaSnip" },
  {
    "saghen/blink.cmp",
    dependencies = { "rafamadriz/friendly-snippets" },
    version = "*",
    config = function()
      require("blink.cmp").setup({
        snippets = { preset = "luasnip" },
        completion = {
          -- menu = { border = "rounded" },
          documentation = { auto_show = true },
        },
      })
    end,
  },

  -- Treesitter
  {
    "nvim-treesitter/nvim-treesitter",
    build = ":TSUpdate",
    lazy = false,
    config = function()
      require("nvim-treesitter").setup({
        ensure_installed = {
          "bash", "c", "html", "javascript", "json", "lua",
          "markdown", "python", "typescript", "vim", "yaml",
        },
      })
    end,
  },

  -- Mini.nvim
  {
    "echasnovski/mini.nvim",
    config = function()
      require("mini.ai").setup({ n_lines = 500 })
      require("mini.surround").setup()
      require("mini.pairs").setup()

      local statusline = require("mini.statusline")
      statusline.setup({
        use_icons = true,
        set_vim_settings = false,
      })
    end,
  },

  -- FZF (Fuzzy Finder)
  {
    "ibhagwan/fzf-lua",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("fzf-lua").setup({
        fzf_opts = {
          ["--layout"] = "default",
          ["--info"] = "inline-right",
        },
        files = {
          cwd_prompt = false,
          previewer = "bat",
        },
        grep = {
          previewer = "bat",
        },
      })

      local fzf = require("fzf-lua")
      vim.keymap.set("n", "<leader>ff", fzf.files, { desc = "Find files" })
      vim.keymap.set("n", "<leader>fg", fzf.live_grep, { desc = "Live grep" })
      vim.keymap.set("n", "<leader>fb", fzf.buffers, { desc = "Buffers" })
      vim.keymap.set("n", "<leader>fh", fzf.help_tags, { desc = "Help tags" })
    end,
  },

  -- File Explorer
  {
    "nvim-neo-tree/neo-tree.nvim",
    branch = "v3.x",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "nvim-tree/nvim-web-devicons",
      "MunifTanjim/nui.nvim",
    },
    config = function()
      require("neo-tree").setup({
        close_if_last_window = true,
        window = {
          width = 30,
          mappings = {
            ["<space>"] = "none", -- disable space to avoid conflict with leader
          },
        },
        filesystem = {
          follow_current_file = { enabled = true },
          use_libuv_file_watcher = true,
          filtered_items = {
            hide_dotfiles = false,
            hide_gitignored = false,
          },
        },
      })
      vim.keymap.set("n", "<leader>e", "<cmd>Neotree toggle<cr>", { desc = "Toggle Neo-tree" })
      vim.keymap.set("n", "<leader>o", "<cmd>Neotree focus<cr>", { desc = "Focus Neo-tree" })
    end,
  },

  -- LeetCode
  {
    "kawre/leetcode.nvim",
    build = ":TSUpdate html",
    dependencies = {
      "nvim-telescope/telescope.nvim",
      "nvim-lua/plenary.nvim",
      "MunifTanjim/nui.nvim",
      "nvim-treesitter/nvim-treesitter",
      "nvim-tree/nvim-web-devicons",
    },
    opts = {
      lang = "python3", -- default language
      cn = { -- leetcode.cn
        enabled = false,
      },
      storage = {
        home = vim.fn.stdpath("data") .. "/leetcode",
      },
      injector = {
        ["python3"] = {
          before = "# @lc code=start",
          after = "# @lc code=end",
        },
        ["cpp"] = {
          before = "// @lc code=start",
          after = "// @lc code=end",
        },
      },
    },
    config = function(_, opts)
      require("leetcode").setup(opts)
      vim.keymap.set("n", "<leader>ll", "<cmd>Leet<cr>", { desc = "LeetCode Menu" })
      vim.keymap.set("n", "<leader>ld", "<cmd>Leet daily<cr>", { desc = "LeetCode Daily" })
      vim.keymap.set("n", "<leader>lr", "<cmd>Leet run<cr>", { desc = "LeetCode Run" })
      vim.keymap.set("n", "<leader>ls", "<cmd>Leet submit<cr>", { desc = "LeetCode Submit" })
      vim.keymap.set("n", "<leader>lp", "<cmd>Leet list<cr>", { desc = "LeetCode Problems" })
    end,
  },

  -- Telescope (required by leetcode.nvim)
  {
    "nvim-telescope/telescope.nvim",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      require("telescope").setup({})
    end,
  },

  -- Colorscheme
  {
    "sainnhe/gruvbox-material",
    lazy = false,
    priority = 1000,
    config = function()
      vim.g.gruvbox_material_background = "hard"
      vim.g.gruvbox_material_foreground = "mix"
      vim.cmd("colorscheme gruvbox-material")
    end,
  },

  -- Dashboard
  {
    "goolord/alpha-nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      local alpha = require("alpha")
      local dashboard = require("alpha.themes.dashboard")

      -- ASCII Art Header
      dashboard.section.header.val = {
        [[                                                    ]],
        [[                                                    ]],
        [[  ███╗   ██╗███████╗ ██████╗ ██╗   ██╗██╗███╗   ███╗]],
        [[  ████╗  ██║██╔════╝██╔═══██╗██║   ██║██║████╗ ████║]],
        [[  ██╔██╗ ██║█████╗  ██║   ██║██║   ██║██║██╔████╔██║]],
        [[  ██║╚██╗██║██╔══╝  ██║   ██║╚██╗ ██╔╝██║██║╚██╔╝██║]],
        [[  ██║ ╚████║███████╗╚██████╔╝ ╚████╔╝ ██║██║ ╚═╝ ██║]],
        [[  ╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═══╝  ╚═╝╚═╝     ╚═╝]],
        [[                                                    ]],
      }

      -- Menu buttons
      dashboard.section.buttons.val = {
        dashboard.button("f", "  Find file", "<cmd>FzfLua files<cr>"),
        dashboard.button("n", "  New file", "<cmd>ene<cr>"),
        dashboard.button("r", "  Recent files", "<cmd>FzfLua oldfiles<cr>"),
        dashboard.button("g", "  Grep text", "<cmd>FzfLua live_grep<cr>"),
        dashboard.button("e", "  File explorer", "<cmd>Neotree toggle<cr>"),
        dashboard.button("l", "  LeetCode", "<cmd>Leet<cr>"),
        dashboard.button("c", "  Config", "<cmd>e $MYVIMRC<cr>"),
        dashboard.button("q", "  Quit", "<cmd>qa<cr>"),
      }

      -- Footer with keybinding hints
      dashboard.section.footer.val = {
        "",
        "──────────────────────────────────────────────────",
        "  SPC ff  Find file     SPC fg  Grep text",
        "  SPC e   File tree     SPC ll  LeetCode",
        "  Tab     Next buffer   S-Tab   Prev buffer",
        "──────────────────────────────────────────────────",
      }

      -- Colors
      dashboard.section.header.opts.hl = "Type"
      dashboard.section.buttons.opts.hl = "Keyword"
      dashboard.section.footer.opts.hl = "Comment"

      alpha.setup(dashboard.opts)

      -- Disable folding on alpha buffer
      vim.cmd([[autocmd FileType alpha setlocal nofoldenable]])
    end,
  },
}

require("lazy").setup(plugins, {
  install = { missing = true, colorscheme = { "gruvbox-material" } },
  checker = { enabled = true, notify = false },
  change_detection = { enabled = true, notify = false },
  performance = {
    rtp = {
      disabled_plugins = {
        "gzip", "tarPlugin", "tohtml", "tutor", "zipPlugin",
      },
    },
  },
})
local map = vim.keymap.set

-- Basic movement
map("n", "j", "v:count == 0 ? 'gj' : 'j'", { expr = true })
map("n", "k", "v:count == 0 ? 'gk' : 'k'", { expr = true })

-- Windows
map("n", "<leader>w", "<C-w>", { remap = true })
map("n", "<leader>d", "<C-w>c", { desc = "Close window" })
map("n", "<leader>s", "<C-w>s", { desc = "Split horizontal" })
map("n", "<leader>v", "<C-w>v", { desc = "Split vertical" })

-- Buffers
map("n", "<Tab>", ":bnext<CR>", { silent = true })
map("n", "<S-Tab>", ":bprev<CR>", { silent = true })

-- Search
map("n", "n", "nzzzv")
map("n", "N", "Nzzzv")
map("n", "<Esc>", ":nohlsearch<CR>", { silent = true })

-- Edit
map("v", "J", ":m '>+1<CR>gv=gv")
map("v", "K", ":m '<-2<CR>gv=gv")
map("i", "jj", "<Esc>")

-- Ctrl+C/V copy/paste (VSCode style)
map("v", "<C-c>", '"+y', { desc = "Copy to clipboard" })
map("n", "<C-v>", '"+p', { desc = "Paste from clipboard" })
map("i", "<C-v>", '<C-r>+', { desc = "Paste from clipboard" })
map("v", "<C-v>", '"+p', { desc = "Paste from clipboard" })

-- Page scroll with Ctrl+D/U
map("n", "<C-d>", "<C-d>zz", { desc = "Page down" })
map("n", "<C-u>", "<C-u>zz", { desc = "Page up" })

local api = vim.api

-- Highlight on yank
api.nvim_create_autocmd("TextYankPost", {
  callback = function()
    vim.hl.on_yank()
  end,
})

-- Return to last position
api.nvim_create_autocmd("BufReadPost", {
  callback = function()
    local mark = api.nvim_buf_get_mark(0, '"')
    if mark[1] > 0 and mark[1] <= api.nvim_buf_line_count(0) then
      pcall(api.nvim_win_set_cursor, 0, mark)
    end
  end,
})

-- Disable auto-comment
api.nvim_create_autocmd("BufEnter", {
  command = "set formatoptions-=cro",
})

-- Close with q
api.nvim_create_autocmd("FileType", {
  pattern = { "help", "lspinfo", "man" },
  callback = function(event)
    vim.bo[event.buf].buflisted = false
    vim.keymap.set("n", "q", "<cmd>close<cr>", { buffer = event.buf, silent = true })
  end,
})
