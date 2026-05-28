---
name: setup-dotfiles
description: 一键配置开发环境 dotfiles。配置 Neovim、Ghostty、Tmux、Zsh。支持 macOS 和 Linux。当用户说"配置开发环境"、"setup dotfiles"、"安装 neovim 配置"时使用。
user-invocable: true
---

# Setup Dotfiles

一键配置跨平台开发环境 (macOS & Linux)。

## 技术栈

- **Shell**: Zsh
- **Editor**: Neovim (with LSP, Treesitter, fzf-lua, neo-tree, leetcode.nvim, alpha-nvim dashboard)
- **Terminal**: Ghostty
- **Multiplexer**: Tmux
- **Theme**: Gruvbox

## 使用方式

当用户请求配置开发环境时，执行以下步骤：

### 步骤 1: 检测系统

```bash
uname -s
```

- `Darwin` = macOS
- `Linux` = Linux

### 步骤 2: 安装依赖

**macOS (Homebrew):**
```bash
brew install neovim fzf eza tmux
brew install --cask ghostty
# 安装 Nerd Font
brew install --cask font-sf-mono-nerd-font
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt update
sudo apt install -y neovim fzf tmux zsh
# eza 需要从 GitHub releases 安装
# Ghostty: https://ghostty.org/download
```

**Linux (Arch):**
```bash
sudo pacman -S neovim fzf eza tmux zsh ghostty
```

### 步骤 3: 创建配置文件

读取以下模板文件并写入用户系统：

| 模板文件 | 目标位置 |
|---------|---------|
| [configs/zshrc](configs/zshrc) | `~/.zshrc` |
| [configs/tmux.conf](configs/tmux.conf) | `~/.tmux.conf` |
| [configs/init.lua](configs/init.lua) | `~/.config/nvim/init.lua` |
| [configs/ghostty](configs/ghostty) | `~/.config/ghostty/config` |

### 步骤 4: 创建必要目录

```bash
mkdir -p ~/.config/nvim
mkdir -p ~/.config/ghostty
```

### 步骤 5: 设置默认 Shell (可选)

如果用户当前不是 zsh：
```bash
chsh -s $(which zsh)
```

### 步骤 6: 安装 Neovim 插件

首次打开 Neovim 会自动安装 lazy.nvim 和所有插件：
```bash
nvim --headless "+Lazy! sync" +qa
```

## 配置说明

### Dashboard 欢迎界面

启动 Neovim 时显示 ASCII 艺术欢迎界面，按对应字母快速操作：

| 按键 | 功能 |
|-----|------|
| `f` | 查找文件 |
| `n` | 新建文件 |
| `r` | 最近文件 |
| `g` | 全局搜索 |
| `e` | 文件树 |
| `l` | LeetCode |
| `c` | 编辑配置 |
| `q` | 退出 |

### Neovim 快捷键

| 按键 | 功能 |
|-----|------|
| `Space` | Leader 键 |
| `<leader>ff` | 查找文件 |
| `<leader>fg` | 全局搜索 |
| `<leader>fb` | 切换 Buffer |
| `Tab` / `S-Tab` | 下一个/上一个 Buffer |
| `jj` | 退出插入模式 |
| `gd` | 跳转定义 |
| `gr` | 查找引用 |
| `K` | 悬浮文档 |

### Neo-tree 文件树

| 按键 | 功能 |
|-----|------|
| `<leader>e` | 切换文件树 |
| `<leader>o` | 聚焦文件树 |

### LeetCode

| 按键 | 功能 |
|-----|------|
| `<leader>ll` | LeetCode 菜单 |
| `<leader>ld` | 每日一题 |
| `<leader>lr` | 运行代码 |
| `<leader>ls` | 提交代码 |
| `<leader>lp` | 题目列表 |

### Tmux 快捷键

| 按键 | 功能 |
|-----|------|
| `` ` `` | 前缀键 (替代 Ctrl-B) |
| `Space` | 切换上一个窗口 |
| `r` | 重载配置 |

### Zsh 别名

| 别名 | 命令 |
|-----|------|
| `v` | `nvim` |
| `g` | `git` |
| `la` | `ls -A` |
| `ll` | `ls -lA` |
| `lsa` | `eza --long` |
| `con` | `tmux attach-session -t` |

## 注意事项

1. 备份现有配置文件再覆盖
2. Ghostty 目前主要支持 macOS，Linux 支持在开发中
3. 首次启动 Neovim 需要等待插件安装完成
