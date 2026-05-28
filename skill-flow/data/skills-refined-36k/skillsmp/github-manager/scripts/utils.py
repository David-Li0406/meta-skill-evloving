#!/usr/bin/env python3
"""
工具函数模块
提供通用的辅助功能
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, cwd=None, capture_output=True):
    """
    执行 shell 命令

    Args:
        command: 命令列表或字符串
        cwd: 工作目录
        capture_output: 是否捕获输出

    Returns:
        (return_code, stdout, stderr)
    """
    try:
        if isinstance(command, str):
            command = command.split()

        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            check=False
        )

        if capture_output:
            return result.returncode, result.stdout, result.stderr
        else:
            return result.returncode, "", ""

    except Exception as e:
        return -1, "", str(e)


def check_git_installed():
    """检查是否安装了 Git"""
    code, _, _ = run_command(["git", "--version"])
    return code == 0


def is_git_repository(path):
    """检查目录是否是 Git 仓库"""
    git_dir = Path(path) / ".git"
    return git_dir.exists()


def get_current_branch(path="."):
    """获取当前分支名称"""
    code, stdout, _ = run_command(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=path
    )
    if code == 0:
        return stdout.strip()
    return None


def get_git_remote(path="."):
    """获取 Git 远程仓库 URL"""
    code, stdout, _ = run_command(
        ["git", "config", "--get", "remote.origin.url"],
        cwd=path
    )
    if code == 0:
        return stdout.strip()
    return None


def print_success(message):
    """打印成功消息"""
    print(f"✅ {message}")


def print_error(message):
    """打印错误消息"""
    print(f"❌ {message}")


def print_info(message):
    """打印信息消息"""
    print(f"ℹ️  {message}")


def print_warning(message):
    """打印警告消息"""
    print(f"⚠️  {message}")


def confirm_action(message):
    """
    请求用户确认

    Args:
        message: 提示消息

    Returns:
        bool: 用户是否确认
    """
    response = input(f"{message} (y/n): ").strip().lower()
    return response in ['y', 'yes']


def validate_repo_name(repo_name):
    """
    验证仓库名称是否合法

    Args:
        repo_name: 仓库名称

    Returns:
        (bool, str): (是否合法, 错误消息)
    """
    if not repo_name:
        return False, "仓库名称不能为空"

    # GitHub 仓库名规则：
    # - 只能包含字母、数字、- 和 _
    # - 不能以 . 结尾
    # - 不能连续使用 --

    import re
    if not re.match(r'^[a-zA-Z0-9._-]+$', repo_name):
        return False, "仓库名称只能包含字母、数字、.-_"

    if repo_name.endswith('.'):
        return False, "仓库名称不能以 . 结尾"

    if '..' in repo_name:
        return False, "仓库名称不能包含 .."

    return True, ""


def parse_repo_identifier(repo):
    """
    解析仓库标识符

    Args:
        repo: 仓库标识符（如：username/repo 或 repo）

    Returns:
        (owner, repo_name): 所有者和仓库名
    """
    if '/' in repo:
        parts = repo.split('/')
        if len(parts) == 2:
            return parts[0], parts[1]

    return None, repo


if __name__ == "__main__":
    # 测试代码
    print("测试工具函数...")

    # 检查 Git
    if check_git_installed():
        print("✅ Git 已安装")
    else:
        print("❌ Git 未安装")

    # 测试仓库名验证
    test_names = ["valid-name", "invalid..name", "name.", ""]
    for name in test_names:
        valid, msg = validate_repo_name(name)
        print(f"{name}: {'✅' if valid else '❌'} {msg}")
