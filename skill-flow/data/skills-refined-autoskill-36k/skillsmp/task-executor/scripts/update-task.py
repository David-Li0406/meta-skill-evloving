#!/usr/bin/env python3
"""更新子任务的执行状态为 done 或 failed"""

import re
import sys
import yaml
from pathlib import Path


def update_task_status(
    task_file: str, task_key: str, status: str, failed_reason: str = ""
) -> bool:
    """
    更新指定子任务的状态

    Args:
        task_file: 任务清单文件路径
        task_key: 子任务键名（如 01-create-model）
        status: 目标状态（done 或 failed）
        failed_reason: 失败原因（仅当 status=failed 时使用）

    Returns:
        更新成功返回 True，失败返回 False
    """
    if status not in ("done", "failed"):
        print(f"❌ 无效的状态: {status}，必须是 'done' 或 'failed'", file=sys.stderr)
        return False

    file_path = Path(task_file)

    if not file_path.exists():
        print(f"❌ 任务文件不存在: {task_file}", file=sys.stderr)
        return False

    # 读取原始文件内容
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 解析 YAML 以验证任务存在
    content = "".join(lines)
    data = yaml.safe_load(content) or {}
    if task_key not in data:
        print(f"❌ 子任务不存在: {task_key}", file=sys.stderr)
        return False

    # 逐行处理
    in_target_task = False
    state_line_found = False
    failed_reason_line_index = -1

    for i, line in enumerate(lines):
        # 检查是否进入目标任务块
        if line.startswith(f"{task_key}:"):
            in_target_task = True
            continue

        # 检查是否离开目标任务块（遇到新的顶层键）
        if in_target_task and not line.startswith(" ") and not line.startswith("\t") and line.strip() and not line.startswith("#"):
            # 空行或注释不算离开
            if line.strip() and not line.startswith("#"):
                break

        # 在目标任务块中，查找并修改 state 行
        if in_target_task and re.match(r"^\s*state:\s*\w+", line):
            # 替换状态
            lines[i] = re.sub(r"(^\s*state:\s*)\w+", rf"\1{status}", line)
            state_line_found = True

        # 在目标任务块中，查找 failed_reason 行（用于删除）
        if in_target_task and re.match(r"^\s*failed_reason:", line):
            failed_reason_line_index = i

    # 处理 failed_reason
    if status == "failed" and failed_reason:
        # 在 state 行后添加 failed_reason
        if state_line_found:
            # 找到 state 行的索引
            for i, line in enumerate(lines):
                if in_target_task and re.match(rf"^\s*state:\s*{status}", line):
                    # 检查下一行是否已经是 failed_reason
                    if i + 1 < len(lines) and re.match(r"^\s*failed_reason:", lines[i + 1]):
                        # 替换现有的 failed_reason
                        lines[i + 1] = f"  failed_reason: {failed_reason}\n"
                    else:
                        # 插入新的 failed_reason 行
                        lines.insert(i + 1, f"  failed_reason: {failed_reason}\n")
                    break
    elif status == "done" and failed_reason_line_index >= 0:
        # 删除 failed_reason 行
        del lines[failed_reason_line_index]

    # 保存更新后的文件
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.writelines(lines)

    return True


def main():
    if len(sys.argv) < 4:
        print(
            "用法: python3 scripts/update-task.py <task-file.yml> <task-key> <done|failed> [failed-reason]",
            file=sys.stderr,
        )
        sys.exit(1)

    task_file = sys.argv[1]
    task_key = sys.argv[2]
    status = sys.argv[3]
    failed_reason = sys.argv[4] if len(sys.argv) > 4 else ""

    if update_task_status(task_file, task_key, status, failed_reason):
        print(f"✓ 子任务 {task_key} 状态已更新为 {status}")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
