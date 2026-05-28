# Dotfiles

Cross-platform development environment configuration for **macOS** and **Linux**.

![Neovim](https://img.shields.io/badge/Neovim-0.9+-green?logo=neovim)
![Ghostty](https://img.shields.io/badge/Terminal-Ghostty-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

```
  ███╗   ██╗███████╗ ██████╗ ██╗   ██╗██╗███╗   ███╗
  ████╗  ██║██╔════╝██╔═══██╗██║   ██║██║████╗ ████║
  ██╔██╗ ██║█████╗  ██║   ██║██║   ██║██║██╔████╔██║
  ██║╚██╗██║██╔══╝  ██║   ██║╚██╗ ██╔╝██║██║╚██╔╝██║
  ██║ ╚████║███████╗╚██████╔╝ ╚████╔╝ ██║██║ ╚═╝ ██║
  ╚═╝  ╚═══╝╚══════╝ ╚═════╝   ╚═══╝  ╚═╝╚═╝     ╚═╝
```

## Stack

| Component | Tool |
|-----------|------|
| Shell | Zsh |
| Editor | Neovim |
| Terminal | Ghostty |
| Multiplexer | Tmux |
| Theme | Gruvbox |

## Neovim Plugins

- **LSP**: nvim-lspconfig + Mason (auto language server management)
- **Completion**: blink.cmp + LuaSnip
- **Fuzzy Finder**: fzf-lua
- **File Explorer**: neo-tree
- **Syntax**: Treesitter
- **Dashboard**: alpha-nvim
- **LeetCode**: leetcode.nvim
- **Utilities**: mini.nvim (statusline, surround, pairs, ai)

## Quick Install

```bash
# Clone
git clone https://github.com/YiyangZhou/dotfiles ~/.dotfiles
cd ~/.dotfiles

# Run install script
./scripts/install.sh
```

## Manual Install

```bash
# Create directories
mkdir -p ~/.config/nvim ~/.config/ghostty

# Symlink configs
ln -sf ~/.dotfiles/configs/zshrc ~/.zshrc
ln -sf ~/.dotfiles/configs/tmux.conf ~/.tmux.conf
ln -sf ~/.dotfiles/configs/init.lua ~/.config/nvim/init.lua
ln -sf ~/.dotfiles/configs/ghostty ~/.config/ghostty/config

# Install Neovim plugins
nvim --headless "+Lazy! sync" +qa
```

## Dependencies

**macOS (Homebrew):**
```bash
brew install neovim fzf eza tmux
brew install --cask ghostty font-sf-mono-nerd-font
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install neovim fzf tmux zsh
```

**Linux (Arch):**
```bash
sudo pacman -S neovim fzf eza tmux zsh
```

## Keybindings

### Dashboard (on startup)

| Key | Action |
|-----|--------|
| `f` | Find file |
| `n` | New file |
| `r` | Recent files |
| `g` | Grep text |
| `e` | File explorer |
| `l` | LeetCode |
| `c` | Edit config |
| `q` | Quit |

### Neovim

| Key | Action |
|-----|--------|
| `Space` | Leader key |
| `<leader>ff` | Find files |
| `<leader>fg` | Live grep |
| `<leader>fb` | Buffers |
| `<leader>e` | Toggle file tree |
| `Tab` / `S-Tab` | Next/Prev buffer |
| `jj` | Exit insert mode |
| `gd` | Go to definition |
| `gr` | Find references |
| `K` | Hover docs |
| `<leader>rn` | Rename |
| `<leader>ca` | Code action |

### LeetCode

| Key | Action |
|-----|--------|
| `<leader>ll` | LeetCode menu |
| `<leader>ld` | Daily challenge |
| `<leader>lp` | Problem list |
| `<leader>lr` | Run code |
| `<leader>ls` | Submit code |

### Tmux

| Key | Action |
|-----|--------|
| `` ` `` | Prefix key (instead of Ctrl-B) |
| `Space` | Last window |
| `r` | Reload config |

### Zsh Aliases

| Alias | Command |
|-------|---------|
| `v` | `nvim` |
| `g` | `git` |
| `la` | `ls -A` |
| `ll` | `ls -lA` |
| `lsa` | `eza --long` |
| `con` | `tmux attach-session -t` |

## Claude Code Skill

This repo also works as a [Claude Code](https://claude.ai/claude-code) skill. Copy to your skills directory:

```bash
cp -r ~/.dotfiles ~/.claude/skills/setup-dotfiles
```

Then use `/setup-dotfiles` in Claude Code for one-click setup.

## License

MIT
