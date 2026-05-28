#!/usr/bin/env python3
"""更新 odin plan.yml 中指定任务的完成状态"""

import sys

from odin_common import get_current_time, OdinYAMLHandler


def update_task_status(plan_file: str, task_id: str) -> bool:
    """
    更新指定任务的完成状态

    将任务的 finished 字段设置为 true，并更新 plan.yml 的 updated_at 元数据

    Args:
        plan_file: plan.yml 文件路径
        task_id: 任务 ID（如 01-task-name）

    Returns:
        更新成功返回 True，失败返回 False
    """
    handler = OdinYAMLHandler(plan_file)

    # 读取 YAML 数据
    data = handler.read_yaml()

    # 检查任务是否存在
    tasks = data.get("tasks", {})
    if task_id not in tasks:
        print(f"❌ 任务不存在: {task_id}", file=sys.stderr)
        return False

    # 更新任务状态
    task = tasks[task_id]
    task["finished"] = True

    # 更新 plan.yml 的元数据
    data["updated_at"] = get_current_time()

    # 保存更新后的文件
    handler.write_yaml(data)

    return True


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 update-odin-task.py <plan.yml> <task-id>", file=sys.stderr)
        sys.exit(1)

    plan_file = sys.argv[1]
    task_id = sys.argv[2]

    if update_task_status(plan_file, task_id):
        print(f"✓ 任务 {task_id} 已标记为完成")
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
