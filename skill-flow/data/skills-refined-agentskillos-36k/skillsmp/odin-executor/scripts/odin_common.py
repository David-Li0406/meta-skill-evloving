#!/usr/bin/env python3
"""ODIN 任务执行共享工具模块"""

from datetime import datetime
from pathlib import Path
from typing import Any


def error_exit(message: str, exit_code: int = 1) -> None:
    """
    统一的错误处理函数

    Args:
        message: 错误消息
        exit_code: 退出代码，默认为 1
    """
    import sys

    print(f"❌ {message}", file=sys.stderr)
    sys.exit(exit_code)


class OdinYAMLHandler:
    """
    YAML 文件处理器，提供统一的读写接口
    仅使用 Python 标准库
    """

    def __init__(self, file_path: str | Path):
        """
        初始化 YAML 处理器

        Args:
            file_path: YAML 文件路径
        """
        self.file_path = Path(file_path)

    def read_yaml(self) -> dict[str, Any]:
        """
        读取 YAML 文件

        Returns:
            解析后的字典数据

        Raises:
            SystemExit: 文件不存在或解析失败
        """
        import sys

        if not self.file_path.exists():
            error_exit(f"文件不存在: {self.file_path}")

        try:
            import yaml

            with open(self.file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            error_exit(f"解析 YAML 失败: {e}")

    def write_yaml(self, data: dict[str, Any]) -> None:
        """
        写入 YAML 文件

        Args:
            data: 要写入的字典数据

        Raises:
            SystemExit: 写入失败
        """
        import sys

        try:
            import yaml

            with open(self.file_path, "w", encoding="utf-8", newline="\n") as f:
                yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
        except Exception as e:
            error_exit(f"写入 YAML 失败: {e}")


def find_next_task(data: dict[str, Any]) -> tuple[str, dict] | None:
    """
    查找下一个可以执行的任务

    规则：按序号从上往下依次查找第一个 finished=false 的任务

    Args:
        data: 解析后的 YAML 数据

    Returns:
        (task_id, task_info) 或 None
    """
    tasks = data.get("tasks", {})

    # 按序号顺序查找第一个未完成的任务
    for task_id, task_info in tasks.items():
        if not isinstance(task_info, dict):
            continue

        # 查找第一个未完成的任务
        if not task_info.get("finished", False):
            return (task_id, task_info)

    return None


def get_current_time() -> str:
    """
    获取当前时间的 ISO 格式字符串

    Returns:
        YYYY-MM-DD 格式的字符串
    """
    return datetime.now().strftime("%Y-%m-%d")
