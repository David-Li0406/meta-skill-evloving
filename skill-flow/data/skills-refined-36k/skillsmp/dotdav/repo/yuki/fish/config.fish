if status is-interactive
    # Commands to run in interactive sessions can go here
end

# 为 fzf 补全设置自定义选项
# --layout=reverse-list 强制使用纵向列表
# --height=40% 设置列表的高度
set -x FZF_COMPLETION_OPTS --layout=reverse-list --height=40%

# --- 设置一些环境变量 ---
set EDITOR nvim
set VISUAL nvim

alias vim nvim
# --- TeX Live 路径 (为 Fish Shell 添加) ---

# 使用 fish_add_path 添加 bin 路径
fish_add_path /usr/local/texlive/2025/bin/x86_64-linux

# MANPATH 和 INFOPATH 需要手动设置
# '$MANPATH' 会保留系统已有的路径
set -gx MANPATH /usr/local/texlive/2025/texmf-dist/doc/man $MANPATH
set -gx INFOPATH /usr/local/texlive/2025/texmf-dist/doc/info $INFOPATH

# uv
fish_add_path "/home/yuki/.local/bin"
