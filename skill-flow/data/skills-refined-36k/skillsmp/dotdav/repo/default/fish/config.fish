if status is-interactive
    # Commands to run in interactive sessions can go here
end

# TeX Live Path Configuration
# 自动通过年份路径加载，方便未来无缝切换到 2026
set -l tex_year 2025
if test -d /usr/local/texlive/$tex_year/bin/x86_64-linux
    fish_add_path /usr/local/texlive/$tex_year/bin/x86_64-linux
    set -gx MANPATH /usr/local/texlive/$tex_year/texmf-dist/doc/man $MANPATH
    set -gx INFOPATH /usr/local/texlive/$tex_year/texmf-dist/doc/info $INFOPATH
end

# uv
fish_add_path "/home/yuki/.local/bin"
