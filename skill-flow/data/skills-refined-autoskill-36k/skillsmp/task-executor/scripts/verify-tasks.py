#!/usr/bin/env python3
"""验证任务清单文件的格式和状态"""

import sys
import yaml
from pathlib import Path


def validate_task_format(data: dict) -> tuple[bool, str]:
    """
    验证任务文件格式是否正确

    Args:
        data: 解析后的 YAML 数据

    Returns:
        (是否有效, 错误信息)
    """
    if not isinstance(data, dict):
        return False, "顶层必须是字典类型"

    # 检查 description 字段
    if "description" not in data:
        return False, "缺少顶层 description 字段"

    desc = data.get("description")
    if not isinstance(desc, str) or not desc.strip():
        return False, "description 必须是非空字符串"

    # 检查是否有子任务
    subtasks = {k: v for k, v in data.items() if k != "description"}
    if not subtasks:
        return False, "没有子任务"

    # 验证每个子任务
    for key, value in subtasks.items():
        # 子任务必须是字典
        if not isinstance(value, dict):
            return False, f"子任务 '{key}' 必须是字典类型"

        # 检查必需字段
        required_fields = ["state", "task", "location"]
        for field in required_fields:
            if field not in value:
                return False, f"子任务 '{key}' 缺少 {field} 字段"

        # 验证 state 值
        valid_states = ["waiting", "running", "done", "failed"]
        if value["state"] not in valid_states:
            return False, f"子任务 '{key}' 的 state 值无效: {value['state']}"

        # 验证 task 字段
        if not isinstance(value["task"], str) or not value["task"].strip():
            return False, f"子任务 '{key}' 的 task 必须是非空字符串"

        # 验证 location 字段
        if not isinstance(value["location"], list):
            return False, f"子任务 '{key}' 的 location 必须是数组"

        if not value["location"]:
            return False, f"子任务 '{key}' 的 location 不能为空"

        # 检查 failed 状态的任务是否有 failed_reason
        if value["state"] == "failed" and "failed_reason" not in value:
            return False, f"子任务 '{key}' 状态为 failed 但缺少 failed_reason 字段"

    return True, ""


def check_unfinished_tasks(data: dict) -> bool:
    """
    检查是否有未完成的任务

    Args:
        data: 解析后的 YAML 数据

    Returns:
        是否有未完成的任务
    """
    unfinished_states = ["waiting", "running", "failed"]
    for key, value in data.items():
        if key == "description":
            continue
        if isinstance(value, dict) and value.get("state") in unfinished_states:
            return True
    return False


def verify_tasks(task_file: str) -> str:
    """
    验证任务文件

    Args:
        task_file: 任务清单文件路径

    Returns:
        验证结果: "OK" | "ERROR: FILE NOT FOUND" | "ERROR: INVALID FORMAT" | "DONE"
    """
    file_path = Path(task_file)

    # 1. 检查文件是否存在
    if not file_path.exists():
        return "ERROR: FILE NOT FOUND"

    # 2. 读取并解析 YAML
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        data = yaml.safe_load(content)
    except Exception:
        return "ERROR: INVALID FORMAT"

    # 3. 验证格式
    is_valid, _error_msg = validate_task_format(data)
    if not is_valid:
        return "ERROR: INVALID FORMAT"

    # 4. 检查是否有未完成的任务
    if not check_unfinished_tasks(data):
        return "DONE"

    # 5. 所有条件都满足
    return "OK"


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/verify-tasks.py <task-file.yml>", file=sys.stderr)
        sys.exit(1)

    task_file = sys.argv[1]
    result = verify_tasks(task_file)

    # 输出结果到 stdout
    print(result)

    # 根据结果设置退出码
    # 0: OK (有未完成任务)
    # 0: DONE (所有任务完成)
    # 1: FILE NOT FOUND
    # 2: INVALID FORMAT
    if result == "OK":
        sys.exit(0)
    elif result == "DONE":
        sys.exit(0)
    elif result == "ERROR: FILE NOT FOUND":
        sys.exit(1)
    elif result == "ERROR: INVALID FORMAT":
        sys.exit(2)


if __name__ == "__main__":
    main()
