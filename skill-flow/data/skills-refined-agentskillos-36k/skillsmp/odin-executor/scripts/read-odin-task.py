#!/usr/bin/env python3
"""从 odin plan.yml 中读取下一个待执行的任务"""

import json
import sys
from pathlib import Path

from odin_common import find_next_task, OdinYAMLHandler


def read_next_task(plan_file: str) -> dict | None:
    """
    读取 plan.yml 中下一个待执行的任务

    Args:
        plan_file: plan.yml 文件路径

    Returns:
        包含任务信息的字典，如果没有找到待执行任务则返回 None
        返回格式: {
            'plan_dir': '计划目录路径',
            'description_path': 'description.md 路径',
            'task_id': '01-task-name',
            'task_detail_path': '任务详细文档路径',
            'files': {'add': [], 'modify': [], 'delete': []}
        }
    """
    handler = OdinYAMLHandler(plan_file)

    # 读取 YAML 数据
    data = handler.read_yaml()
    if "tasks" not in data:
        return None

    # 查找下一个任务
    result = find_next_task(data)
    if not result:
        return None

    task_id, task_info = result

    # 获取计划目录路径
    plan_dir = str(Path(plan_file).parent)

    # 构建返回结果
    return {
        "plan_dir": plan_dir,
        "description_path": str(Path(plan_dir) / "description.md"),
        "task_id": task_id,
        "task_detail_path": str(Path(plan_dir) / task_info.get("detail", "")),
        "files": {
            "add": task_info.get("files", {}).get("add", []),
            "modify": task_info.get("files", {}).get("modify", []),
            "delete": task_info.get("files", {}).get("delete", []),
        },
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 read-odin-task.py <plan.yml>", file=sys.stderr)
        sys.exit(1)

    plan_file = sys.argv[1]
    result = read_next_task(plan_file)

    if result:
        # 输出 JSON 格式结果到 stdout
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
