#!/usr/bin/env python3
"""
日志归档器：负责将 CR 结果双向同步到被审项目和 core-foundry。
"""
import os
import sys
from datetime import datetime
from shared import get_core_foundry_root

def archive_log(project_name, target_project_root, log_content):
    """
    双存储日志归档：同时存入目标项目和 core-foundry
    """
    core_foundry_root = get_core_foundry_root()
    
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    filename_ts = now.strftime("%Y-%m-%d_%H-%M-%S")
    
    # 构造日志内容 (自动包装标题和时间)
    formatted_log = f"# Code Review - {timestamp}\n{log_content}\n"
    
    # 定义两个存储路径
    paths = [
        # 位置一：被 CR 项目
        os.path.join(target_project_root, "cr-logs", project_name, f"{filename_ts}.md"),
        # 位置二：core-foundry 归档
        os.path.join(core_foundry_root, "cr-logs", project_name, f"{filename_ts}.md")
    ]
    
    success_count = 0
    for path in paths:
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            # 总是创建新文件
            with open(path, "w", encoding="utf-8") as f:
                f.write(formatted_log)
            print(f"✅ [CHECKPOINT:LOG_SAVED] {path}")
            success_count += 1
        except Exception as e:
            print(f"❌ [ERROR] Failed to save {path}: {str(e)}", file=sys.stderr)
    
    if success_count == len(paths):
        print("\n✅ [STATUS:ARCHIVE_COMPLETE] All logs saved successfully.")
    else:
        print(f"\n⚠️ [STATUS:PARTIAL_ARCHIVE] Only {success_count}/{len(paths)} logs saved.")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python3 archive_log.py <project_name> <target_project_root> <log_content>")
        sys.exit(1)
    
    archive_log(sys.argv[1], sys.argv[2], sys.argv[3])
