#!/usr/bin/env python3
"""从任务清单文件中读取下一个 waiting 或 failed 状态的子任务，并将其状态更新为 running"""

import re
import sys
import yaml
from pathlib import Path


def read_and_update_task(task_file: str) -> dict | None:
    """
    读取任务文件中第一个 waiting 或 failed 状态的子任务，并将其状态更新为 running
    优先返回 waiting 状态的任务，如果没有 waiting 则返回 failed 状态的任务

    Args:
        task_file: 任务清单文件路径

    Returns:
        包含子任务信息的字典，如果没有找到 waiting 或 failed 任务则返回 None
        返回格式: {
            'description': '总体任务描述',
            'completed': ['01-task1: 简要描述', '02-task2: 简要描述'],
            'task_key': '03-create-model',
            'task': '任务描述',
            'location': ['file1.py', 'file2.py'],
            'tips': '给大模型的提示信息',
            'failed_reason': '失败原因（仅当任务状态为 failed 时存在）'
        }
    """
    file_path = Path(task_file)

    if not file_path.exists():
        print(f"❌ 任务文件不存在: {task_file}", file=sys.stderr)
        return None

    # 读取原始文件内容
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 解析 YAML 数据
    data = yaml.safe_load(content) or {}

    # 获取总体描述
    description = data.get("description", "")

    # 收集已完成的任务（从上往下顺序）
    completed_tasks = []
    for key, value in data.items():
        if key == "description":
            continue
        if isinstance(value, dict) and value.get("state") == "done":
            task_summary = value.get("task", "")
            # 仅取第一行内容作为简要描述
            task_summary = task_summary.split("\n")[0].strip() if task_summary else ""
            completed_tasks.append(f"{key}: {task_summary}")

    # 查找第一个 waiting 或 failed 状态的子任务
    # 优先查找 waiting 状态
    target_task = None
    target_state = None

    for key, value in data.items():
        if key == "description":
            continue

        if isinstance(value, dict):
            state = value.get("state")
            if state == "waiting":
                target_task = (key, value)
                target_state = "waiting"
                break
            elif state == "failed" and target_task is None:
                # 记录第一个 failed 任务，但继续查找 waiting
                target_task = (key, value)
                target_state = "failed"

    if not target_task:
        print("✓ 没有找到 waiting 或 failed 状态的子任务", file=sys.stderr)
        return None

    key, value = target_task

    # 直接修改原始文本内容，替换状态为 running
    pattern = rf"^({re.escape(key)}:\s*\n\s*state:\s*){target_state}"
    replacement = r"\1running"

    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)

    # 保存更新后的文件
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(new_content)

    # 构建返回结果
    result = {
        "description": description,
        "completed": completed_tasks,
        "task_key": key,
        "task": value.get("task", ""),
        "location": value.get("location", []),
        "tips": "⚠️ 重要提示：在完成代码编写后，务必检查自己生成的代码，确保代码质量、正确性和可维护性。",
    }

    # 如果是 failed 状态的任务，添加失败原因和修复提示
    if target_state == "failed":
        failed_reason = value.get("failed_reason", "")
        if failed_reason:
            result["failed_reason"] = failed_reason
            result["tips"] = (
                f"⚠️ 该任务之前执行失败，需要修复。\n\n"
                f"🔴 失败原因：{failed_reason}\n\n"
                f"📋 请根据失败原因分析问题，重新执行该任务，并在修复之后检查代码，确保代码质量、正确性和可维护性。"
            )

    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/read-task.py <task-file.yml>", file=sys.stderr)
        sys.exit(1)

    task_file = sys.argv[1]
    result = read_and_update_task(task_file)

    if result:
        # 输出 JSON 格式结果到 stdout
        import json

        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
