function init_project
    # --- 1. 定义路径 ---
    set -l source_truth ".github/skills"
    set -l agent_compat ".agent/skills"
    set -l target_rel_path "../.github/skills" # 相对路径，用于软链接
    set -l gitignore_file ".gitignore"

    echo "🚀 Initializing Project Environment..."

    # --- 2. 确保真值源 (Source of Truth) 存在 ---
    if not test -d $source_truth
        mkdir -p $source_truth
        echo "✅ Created directory: $source_truth"
    end

    # --- 3. 处理 Antigravity 路径 (.agent/skills) ---
    # 确保父目录存在
    mkdir -p (dirname $agent_compat)

    if test -L $agent_compat
        # 情况 A: 已经是软链接
        # 强制更新链接以确保指向正确（防止坏链）
        ln -sf $target_rel_path $agent_compat
        echo "🔗 Verified symlink: $agent_compat -> $source_truth"

    else if test -d $agent_compat
        # 情况 B: 是一个真实目录
        echo "⚠️  Detected existing directory: $agent_compat"
        
        # 检查是否为空
        if test (count (ls -A $agent_compat)) -gt 0
            echo "📦 Moving existing skills to $source_truth..."
            # 移动文件，-n 防止覆盖已存在的文件
            mv -n $agent_compat/* $source_truth/
        end

        # 尝试删除目录（只有目录为空时才会成功，这是一种安全机制）
        rmdir $agent_compat 2>/dev/null

        if test -d $agent_compat
            echo "❌ Error: $agent_compat is not empty (duplicate file names?). Manual merge required."
            return 1
        else
            # 目录已清理，建立链接
            ln -s $target_rel_path $agent_compat
            echo "🔄 Migrated & Linked: $agent_compat -> $source_truth"
        end

    else
        # 情况 C: 路径不存在，直接创建链接
        ln -s $target_rel_path $agent_compat
        echo "🔗 Created symlink: $agent_compat -> $source_truth"
    end

    # --- 4. 处理 .gitignore ---
    set -l ignore_content \
    "" \
    "# AI Agent Compatibility Layers" \
    ".agent/" \
    ".claude/" \
    "" \
    "# Keep the source of truth" \
    "!.github/skills/"

    if test -f $gitignore_file
        # 如果文件存在，检查是否已经包含标记，避免重复添加
        if not grep -q "AI Agent Compatibility Layers" $gitignore_file
            echo "📄 Appending rules to existing .gitignore..."
            for line in $ignore_content
                echo $line >> $gitignore_file
            end
        else
            echo "✅ .gitignore already contains AI rules."
        end
    else
        # 如果文件不存在，创建并写入
        echo "📄 Creating new .gitignore with rules..."
        for line in $ignore_content
            echo $line >> $gitignore_file
        end
    end

    echo "🎉 Project initialization complete."
end
