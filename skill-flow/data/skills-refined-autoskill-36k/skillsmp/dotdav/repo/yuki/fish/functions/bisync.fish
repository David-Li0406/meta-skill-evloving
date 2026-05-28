# ~/.config/fish/functions/bisync.fish
# --- 修复 (2025-11-09): 
# ---   1. (add) 修复: Fish 'if' 语法错误 ('展开后的命令为空')
# ---   2. (add) 修复: 'rclone lsf' 添加 -R --dirs-only 以递归显示子文件夹
# ---   (保留) (add) 修复 'find' 回退命令以显示隐藏文件夹
# ---   (保留) (remove/enable/disable) 允许传递参数
# ---   (保留) (add) 强制 ASCII 名称

function bisync --description "管理 rclone bisync 的 systemd 服务"

    set -l log_base_dir /tmp
    
    # --- 帮助函数：获取所有项目名称 ---
    function _bisync_get_projects
        set -l config_dir "$HOME/.config/systemd/user"
        set -l main_service "$config_dir/rclone-bisync.service"
        
        for f in $config_dir/rclone-bisync-*.service
            if test "$f" != "$main_service"
                set -l fname (basename $f)
                set -l project_with_ext (string replace "rclone-bisync-" "" $fname)
                set -l project_name (string replace ".service" "" $project_with_ext)
                echo $project_name
            end
        end
    end

    # --- 帮助函数：使用 fzf 选择一个项目 ---
    function _bisync_select_project
        set -l project (_bisync_get_projects | fzf --prompt="选择一个同步项目> " --height=30% --reverse)
        if test $status -ne 0
            echo "未选择项目。" >&2
            return 1
        end
        echo $project
    end

    # --- 1. & 2. (list) 列出项目和状态 ---
    function _bisync_cmd_list
        set -l config_dir "$HOME/.config/systemd/user"
        set -l timer_unit_name "rclone-bisync.timer"
        
        echo (set_color blue)"--- ⌛️ 主定时器状态 ---"(set_color normal)
        systemctl --user status $timer_unit_name | string match -r 'Active:.*'
        echo ""
        echo (set_color blue)"--- 🗂️ 同步项目列表 ---"(set_color normal)
        for project in (_bisync_get_projects)
            set -l service_file "rclone-bisync-$project.service"
            set -l enabled_status (systemctl --user is-enabled $service_file 2>/dev/null)
            
            set -l display_status 
            if test "$enabled_status" = "masked"
                set display_status (set_color red)"🔴 已禁用 (masked)"(set_color normal)
            else
                set display_status (set_color green)"🟢 已启用"(set_color normal)
            end
            echo "  - $project [$display_status]"
        end
    end

    # --- 3. (add) 添加新项目 (fzf 增强版) ---
    function _bisync_cmd_add
        set -l config_dir "$HOME/.config/systemd/user"
        set -l main_service "$config_dir/rclone-bisync.service"
        
        # 1. Local Path
        set -l find_cmd "find \$HOME -type d 2>/dev/null"
        if command -v fd >/dev/null
            set find_cmd "fd --type d --hidden --no-ignore . \$HOME"
        end
        
        echo (set_color yellow)"正在搜索本地目录 (可输入 $HOME/ 或 / 搜索)..."(set_color normal)
        set -l local_path (eval $find_cmd | fzf --prompt="选择要同步的 [本地] 目录> " --height=40% --reverse)
        
        if test $status -ne 0; echo "操作已取消。" >&2; return 1; end
        if not test -d "$local_path"; echo "错误: 未选择有效目录。" >&2; return 1; end
        
        set local_path (realpath $local_path)
        echo (set_color green)"  本地路径:"(set_color normal)" $local_path"

        # 2. Project Name (强制 ASCII 验证)
        set -l default_project_name (basename $local_path)
        read -P "输入项目名称 (默认: $default_project_name): " project_name
        
        if test -z "$project_name"
            set project_name $default_project_name
        end
        
        # --- 修复点 (if 语法) ---
        while true
            # 直接使用 'if test' 和 'if string match'
            if test -z "$project_name"
                read -P "项目名称不能为空。请输入一个纯 ASCII 名称: " project_name
            else if string match -q -r '[^\x00-\x7F]' $project_name
                echo (set_color red)"错误: 项目名称 '$project_name' 包含 Unicode 字符。"(set_color normal)
                echo (set_color yellow)"systemd 无法处理此问题。请提供一个纯 ASCII 名称。"(set_color normal)
                read -P "请输入一个纯 ASCII 的项目名称 (例如: config): " project_name
            else
                break # 验证通过!
            end
        end
        # --- 修复结束 ---
        echo (set_color green)"  项目名称:"(set_color normal)" $project_name"
        
        set -l new_service_file "$config_dir/rclone-bisync-$project_name.service"
        if test -e "$new_service_file"; echo "错误: 项目 '$project_name' 已存在。" >&2; return 1; end

        # 3. Remote Path
        echo (set_color yellow)"正在获取 rclone 远程列表..."(set_color normal)
        set -l remote_list (rclone listremotes 2>/dev/null)
        if test (count $remote_list) -eq 0; echo "错误: 'rclone listremotes' 未返回任何远程。" >&2; return 1; end
        
        set -l remote (echo $remote_list | tr ' ' '\n' | fzf --prompt="选择一个 [rclone 远程]> " --height=40% --reverse)
        if test $status -ne 0; echo "操作已取消。" >&2; return 1; end
        
        echo (set_color yellow)"正在获取 '$remote' 上的路径... (这可能需要一点时间)"(set_color normal)
        
        # --- 修复点 (fzf 递归) ---
        # 使用 -R (递归) 和 --dirs-only (只显示目录)
        set -l path_in_remote (rclone lsf -R --dirs-only "$remote" 2>/dev/null | fzf --prompt="选择或输入远程路径 (留空为根目录)> " --height=40% --reverse)
        # --- 修复结束 ---
        
        if test $status -ne 0; echo "操作已取消。" >&2; return 1; end
        
        set path_in_remote (string trim -r -c / $path_in_remote)
        set -l remote_path
        if test -n "$path_in_remote"
            set remote_path "$remote$path_in_remote"
        else
            set remote_path "$remote"
        end
        echo (set_color green)"  远程路径:"(set_color normal)" $remote_path"

        # 4. 创建文件
        set -l log_file "$log_base_dir/rclone-bisync-$project_name.log"
        
        echo "正在创建: $new_service_file"
        
        echo "[Unit]
Description=Rclone bisync for $project_name

[Service]
Type=oneshot
ExecStart=/usr/bin/rclone bisync '$local_path' '$remote_path' --verbose --log-file='$log_file'
" > $new_service_file

        echo "正在更新: $main_service"
        
        set -l unit_file_name "rclone-bisync-$project_name.service"
        sed -i "/^\[Service\]/i Wants=$unit_file_name" $main_service
        
        echo "重新加载 systemd daemon..."
        systemctl --user daemon-reload
        
        echo (set_color green)"成功添加 '$project_name'."(set_color normal)
        read -P "是否立即为 '$project_name' 运行一次 --resync (初始化同步)? (y/N) " confirm
        if test "$confirm" = "y" -o "$confirm" = "Y"
            _bisync_cmd_resync $project_name
        end
    end

    # --- (remove) 移除项目 ---
    function _bisync_cmd_remove
        set -l config_dir "$HOME/.config/systemd/user"
        set -l main_service "$config_dir/rclone-bisync.service"
        
        set -l project
        if test -n "$argv[1]"
            set project $argv[1]
        else
            set project (_bisync_select_project)
            if test $status -ne 0; return 1; end
        end

        read -P "确定要移除 '$project' 吗? 这将删除其 .service 文件。 (y/N) " confirm
        if test "$confirm" != "y" -a "$confirm" != "Y"; echo "操作已取消。"; return 1; end

        set -l service_file "$config_dir/rclone-bisync-$project.service"
        
        set -l unit_file_name "rclone-bisync-$project.service"
        
        # 清理
        sed -i "/Wants=\"$unit_file_name\"/d" $main_service
        sed -i "/Wants=$unit_file_name/d" $main_service
        set -l escaped_unit_name (systemd-escape $unit_file_name 2>/dev/null)
        if test -n "$escaped_unit_name"
             sed -i "/Wants=$escaped_unit_name/d" $main_service
        end

        rm -f $service_file
        
        echo "已从 $main_service 移除。已删除 $service_file。"
        
        set -l log_file "$log_base_dir/rclone-bisync-$project.log"
        if test -e $log_file
            read -P "是否删除日志文件 $log_file? (y/N) " confirm_log
            if test "$confirm_log" = "y" -o "$confirm_log" = "Y"
                rm -f $log_file
                echo "已删除日志文件。"
            end
        end

        echo "重新加载 systemd daemon..."
        systemctl --user daemon-reload
        echo (set_color green)"成功移除 '$project'."(set_color normal)
    end

    # --- 4. (interval) 修改间隔 ---
    function _bisync_cmd_interval
        set -l timer_unit_name "rclone-bisync.timer"
        set -l main_timer "$HOME/.config/systemd/user/$timer_unit_name"
        
        set -l current_interval (grep '^OnUnitActiveSec=' $main_timer | cut -d= -f2)
        read -P "当前间隔为 '$current_interval'。输入新间隔 (例如: 5min, 1h, 30s): " new_interval
        if test -z "$new_interval"; echo "未提供间隔。操作已取消。" >&2; return 1; end
        
        sed -i "s|^OnUnitActiveSec=.*|OnUnitActiveSec=$new_interval|" $main_timer
        
        echo "间隔已更新为 $new_interval。"
        echo "正在重新加载 systemd 并重启定时器..."
        systemctl --user daemon-reload
        systemctl --user restart $timer_unit_name
        echo "完成。"
    end

    # --- 5. (log) 查看日志 ---
    function _bisync_cmd_log
        set -l project
        if test -n "$argv[1]"
            set project $argv[1]
        else
            set project (_bisync_select_project)
            if test $status -ne 0; return 1; end
        end
        
        set -l log_file "$log_base_dir/rclone-bisync-$project.log"
        if not test -e "$log_file"; echo "错误: 未找到日志文件 $log_file" >&2; return 1; end
        
        less +F $log_file
    end

    # --- 6. (resync) 初始化同步 ---
    function _bisync_cmd_resync
        set -l config_dir "$HOME/.config/systemd/user"

        set -l project
        if test -n "$argv[1]"
            set project $argv[1]
        else
            set project (_bisync_select_project)
            if test $status -ne 0; return 1; end
        end

        set -l service_file "$config_dir/rclone-bisync-$project.service"
        if not test -e "$service_file"; echo "错误: 未找到 '$project' 的服务文件。" >&2; return 1; end

        set -l exec_cmd (grep '^ExecStart=' $service_file | cut -d= -f2-)
        
        if test -z "$exec_cmd"; echo "错误: “$service_file” 中 ExecStart 命令为空。" >&2; return 1; end

        set -l resync_cmd "$exec_cmd --resync"
        
        echo "--- 正在为 '$project' 执行 --resync ---"
        echo (set_color blue)"\$ $resync_cmd"(set_color normal)
        eval $resync_cmd
        echo "--- Resync 完成 ---"
    end
    
    # --- (enable / disable) 启用/禁用 ---
    function _bisync_cmd_enable
        set -l project
        if test -n "$argv[1]"
            set project $argv[1]
        else
            set project (_bisync_select_project)
            if test $status -ne 0; return 1; end
        end

        systemctl --user unmask "rclone-bisync-$project.service"
        echo "已启用 (unmask) '$project'。正在重新加载 daemon..."
        systemctl --user daemon-reload
    end

    function _bisync_cmd_disable
        set -l project
        if test -n "$argv[1]"
            set project $argv[1]
        else
            set project (_bisync_select_project)
            if test $status -ne 0; return 1; end
        end

        systemctl --user mask "rclone-bisync-$project.service"
        echo "已禁用 (mask) '$project'。正在重新加载 daemon..."
        systemctl --user daemon-reload
    end
    
    # --- (start / stop) 启停主定时器 ---
    function _bisync_cmd_start
        set -l timer_unit_name "rclone-bisync.timer"
        echo "启动并启用 (enable) 主定时器..."
        systemctl --user enable --now $timer_unit_name
    end
    
    function _bisync_cmd_stop
        set -l timer_unit_name "rclone-bisync.timer"
        echo "停止并禁用 (disable) 主定时器..."
        systemctl --user disable --now $timer_unit_name
    end
    
    # --- (help) 帮助 ---
    function _bisync_cmd_help
        echo "Usage: bisync [command]"
        echo ""
        echo "rclone bisync 管理脚本。"
        echo "如果未提供命令，将使用 fzf 显示交互式菜单。"
        echo ""
        echo "命令:"
        echo (set_color green)"  list"(set_color normal)"      - (默认) 显示状态和所有同步项目"
        echo (set_color green)"  start"(set_color normal)"     - B"
        echo (set_color green)"  stop"(set_color normal)"      - 禁用并停止主同步定时器"
        echo (set_color green)"  add"(set_color normal)"       - 添加一个新的同步项目"
        echo (set_color green)"  remove"(set_color normal)"    - [项目] 移除一个同步项目"
        echo (set_color green)"  enable"(set_color normal)"    - [项目] 启用一个被禁用的项目 (unmask)"
        echo (set_color green)"  disable"(set_color normal)"   - [项目] 禁用一个项目 (mask)"
        echo (set_color green)"  log"(set_color normal)"       - [项目] 查看项目的日志文件 (fzf)"
        echo (set_color green)"  resync"(set_color normal)"    - [项目] 为项目执行一次 --resync (fzf)"
        echo (set_color green)"  interval"(set_color normal)"  - 更改主同步间隔"
        echo (set_color green)"  help"(set_color normal)"      - 显示此帮助信息"
    end

    # --- 7. (fzf) 主命令解析器 ---
    set -l all_commands list start stop add remove enable disable log resync interval help
    
    if test (count $argv) -eq 0
        set -l cmd (echo $all_commands | tr ' ' '\n' | fzf --prompt="选择一个操作> " --height=40% --reverse)
        if test $status -ne 0; return 0; end
        set argv $cmd
    end

    set -l command $argv[1]
    set -l cmd_args $argv[2..-1]

    switch $command
        case 'list'
            _bisync_cmd_list
        case 'add'
            _bisync_cmd_add
        case 'remove'
            _bisync_cmd_remove $cmd_args
        case 'log'
            _bisync_cmd_log $cmd_args
        case 'resync'
            _bisync_cmd_resync $cmd_args
        case 'interval'
            _bisync_cmd_interval
        case 'enable'
            _bisync_cmd_enable $cmd_args
        case 'disable'
            _bisync_cmd_disable $cmd_args
        case 'start'
            _bisync_cmd_start
        case 'stop'
            _bisync_cmd_stop
        case 'help' '-h' '--help'
            _bisync_cmd_help
        case '*'
            echo "未知命令: '$command'" >&2
            _bisync_cmd_help
            return 1
    end
end
