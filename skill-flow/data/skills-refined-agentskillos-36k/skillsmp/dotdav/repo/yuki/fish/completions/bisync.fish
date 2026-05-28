# ~/.config/fish/completions/bisync.fish
# --- 修正: 使用 -f 标志来阻止默认的文件补全 ---

set -l bisync_cmds list start stop add remove enable disable log resync interval help

# --- 帮助函数 (不变) ---
function __bisync_comp_get_projects
    set -l config_dir ~/.config/systemd/user
    set -l main_service $config_dir/rclone-bisync.service
    for f in $config_dir/rclone-bisync-*.service
        if test "$f" != "$main_service"
            set -l fname (basename $f)
            set -l project_with_ext (string replace "rclone-bisync-" "" $fname)
            set -l project_name (string replace ".service" "" $project_with_ext)
            echo $project_name
        end
    end
end

# --- 规则 1: 补全子命令 ---
# (当没有输入子命令时)
# 添加 -f 来阻止文件补全
complete -c bisync -n "not __fish_seen_subcommand_from $bisync_cmds" -a "$bisync_cmds" -d "bisync 子命令" -f

# --- 规则 2: 补全项目名称 ---
# (当输入了 'log', 'resync', 'enable', 'disable', 'remove' 时)
# 添加 -f 来阻止文件补全, 只显示项目
set -l project_cmds log resync enable disable remove
complete -c bisync -n "__fish_seen_subcommand_from $project_cmds" -a "(__bisync_comp_get_projects)" -d "同步项目" -f

# --- 规则 3: 阻止后续参数 ---
# (当输入了 'list', 'add', 'start' 等不需要参数的命令时)
# -f 阻止文件补全, 没有 -a 意味着不补全任何东西
set -l no_arg_cmds list add start stop interval help
complete -c bisync -n "__fish_seen_subcommand_from $no_arg_cmds" -f
