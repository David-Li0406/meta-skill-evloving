#!/usr/bin/env python3
"""
Git 操作封装
提供常用的 Git 操作功能
"""

import sys
import os
from pathlib import Path
import subprocess

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from utils import (
    run_command, check_git_installed, is_git_repository,
    print_success, print_error, print_info
)


class GitOperations:
    """Git 操作类"""

    def __init__(self, path='.'):
        """
        初始化 Git 操作

        Args:
            path: 工作目录路径
        """
        self.path = Path(path).resolve()

    def init(self):
        """初始化 Git 仓库"""
        if is_git_repository(self.path):
            print_info("该目录已经是 Git 仓库")
            return True

        code, _, stderr = run_command(['git', 'init'], cwd=self.path)
        if code == 0:
            print_success("Git 仓库初始化成功")
            return True
        else:
            print_error(f"初始化失败: {stderr}")
            return False

    def clone(self, url, dest=None):
        """
        克隆仓库

        Args:
            url: 仓库 URL
            dest: 目标目录（可选）
        """
        if dest:
            code, _, stderr = run_command(['git', 'clone', url, dest])
        else:
            code, _, stderr = run_command(['git', 'clone', url])

        if code == 0:
            print_success("仓库克隆成功")
            return True
        else:
            print_error(f"克隆失败: {stderr}")
            return False

    def status(self):
        """查看仓库状态"""
        if not is_git_repository(self.path):
            print_error("当前目录不是 Git 仓库")
            return False

        code, stdout, stderr = run_command(['git', 'status'], cwd=self.path, capture_output=False)
        return code == 0

    def add(self, files='.'):
        """
        添加文件到暂存区

        Args:
            files: 文件路径，默认为所有文件
        """
        if not is_git_repository(self.path):
            print_error("当前目录不是 Git 仓库")
            return False

        code, _, stderr = run_command(['git', 'add', files], cwd=self.path)
        if code == 0:
            print_success(f"文件已添加到暂存区")
            return True
        else:
            print_error(f"添加失败: {stderr}")
            return False

    def commit(self, message):
        """
        提交更改

        Args:
            message: 提交信息
        """
        if not is_git_repository(self.path):
            print_error("当前目录不是 Git 仓库")
            return False

        code, _, stderr = run_command(['git', 'commit', '-m', message], cwd=self.path)
        if code == 0:
            print_success(f"提交成功: {message}")
            return True
        else:
            print_error(f"提交失败: {stderr}")
            return False

    def add_and_commit(self, message, files='.'):
        """
        添加并提交（一步完成）

        Args:
            message: 提交信息
            files: 要添加的文件，默认为所有
        """
        if self.add(files):
            return self.commit(message)
        return False

    def push(self, remote='origin', branch=None):
        """
        推送到远程仓库

        Args:
            remote: 远程仓库名称
            branch: 分支名称（可选）
        """
        if not is_git_repository(self.path):
            print_error("当前目录不是 Git 仓库")
            return False

        if branch is None:
            code, _, stderr = run_command(['git', 'push', remote], cwd=self.path)
        else:
            code, _, stderr = run_command(['git', 'push', remote, branch], cwd=self.path)

        if code == 0:
            print_success("推送成功")
            return True
        else:
            print_error(f"推送失败: {stderr}")
            return False

    def pull(self, remote='origin', branch=None):
        """
        从远程仓库拉取更新

        Args:
            remote: 远程仓库名称
            branch: 分支名称（可选）
        """
        if not is_git_repository(self.path):
            print_error("当前目录不是 Git 仓库")
            return False

        if branch is None:
            code, _, stderr = run_command(['git', 'pull', remote], cwd=self.path)
        else:
            code, _, stderr = run_command(['git', 'pull', remote, branch], cwd=self.path)

        if code == 0:
            print_success("拉取成功")
            return True
        else:
            print_error(f"拉取失败: {stderr}")
            return False

    def log(self, n=10):
        """
        查看提交历史

        Args:
            n: 显示最近 n条提交
        """
        if not is_git_repository(self.path):
            print_error("当前目录不是 Git 仓库")
            return False

        code, stdout, stderr = run_command(
            ['git', 'log', '--oneline', '-n', str(n)],
            cwd=self.path,
            capture_output=False
        )
        return code == 0

    def branch(self, action='list', branch_name=None):
        """
        分支操作

        Args:
            action: 操作类型（list, create, delete, checkout）
            branch_name: 分支名称
        """
        if not is_git_repository(self.path):
            print_error("当前目录不是 Git 仓库")
            return False

        if action == 'list':
            code, _, stderr = run_command(['git', 'branch'], cwd=self.path, capture_output=False)
            return code == 0

        elif action == 'create':
            if not branch_name:
                print_error("请指定分支名称")
                return False
            code, _, stderr = run_command(['git', 'branch', branch_name], cwd=self.path)
            if code == 0:
                print_success(f"分支 {branch_name} 创建成功")
                return True
            else:
                print_error(f"创建失败: {stderr}")
                return False

        elif action == 'checkout':
            if not branch_name:
                print_error("请指定分支名称")
                return False
            code, _, stderr = run_command(['git', 'checkout', branch_name], cwd=self.path)
            if code == 0:
                print_success(f"已切换到分支 {branch_name}")
                return True
            else:
                print_error(f"切换失败: {stderr}")
                return False

        elif action == 'delete':
            if not branch_name:
                print_error("请指定分支名称")
                return False
            code, _, stderr = run_command(['git', 'branch', '-d', branch_name], cwd=self.path)
            if code == 0:
                print_success(f"分支 {branch_name} 已删除")
                return True
            else:
                print_error(f"删除失败: {stderr}")
                return False

    def remote_add(self, name, url):
        """
        添加远程仓库

        Args:
            name: 远程仓库名称
            url: 远程仓库 URL
        """
        if not is_git_repository(self.path):
            print_error("当前目录不是 Git 仓库")
            return False

        code, _, stderr = run_command(['git', 'remote', 'add', name, url], cwd=self.path)
        if code == 0:
            print_success(f"远程仓库 {name} 已添加")
            return True
        else:
            print_error(f"添加失败: {stderr}")
            return False


def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print("Git 操作工具\n")
        print("使用方法:")
        print("  python git_operations.py 状态                    # 查看状态")
        print("  python git_operations.py 日志                    # 查看日志")
        print("  python git_operations.py 提交 <message>          # 提交更改")
        print("  python git_operations.py 推送                    # 推送")
        print("  python git_operations.py 拉取                    # 拉取")
        sys.exit(1)

    command = sys.argv[1]
    git = GitOperations()

    if command == "状态":
        git.status()

    elif command == "日志":
        git.log()

    elif command == "提交":
        if len(sys.argv) < 3:
            message = input("请输入提交信息: ")
        else:
            message = ' '.join(sys.argv[2:])

        git.add_and_commit(message)

    elif command == "推送":
        git.push()

    elif command == "拉取":
        git.pull()

    else:
        print(f"❌ 未知命令: {command}")


if __name__ == "__main__":
    main()
