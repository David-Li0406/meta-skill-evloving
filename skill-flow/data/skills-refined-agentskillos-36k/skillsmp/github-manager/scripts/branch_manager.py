#!/usr/bin/env python3
"""
分支管理脚本
提供 Git 分支的创建、切换、合并、删除等功能
"""

import sys
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from git_operations import GitOperations
from utils import print_success, print_error, print_info


def list_branches(path='.'):
    """列出所有分支"""
    try:
        git = GitOperations(path)
        print_info("本地分支:")
        git.branch('list')
        return True
    except Exception as e:
        print_error(f"列出分支失败: {e}")
        return False


def create_branch(branch_name, path='.'):
    """
    创建新分支

    Args:
        branch_name: 分支名称
        path: 仓库路径
    """
    try:
        git = GitOperations(path)
        return git.branch('create', branch_name)
    except Exception as e:
        print_error(f"创建分支失败: {e}")
        return False


def switch_branch(branch_name, path='.'):
    """
    切换分支

    Args:
        branch_name: 分支名称
        path: 仓库路径
    """
    try:
        git = GitOperations(path)
        return git.branch('checkout', branch_name)
    except Exception as e:
        print_error(f"切换分支失败: {e}")
        return False


def create_and_switch(branch_name, path='.'):
    """
    创建并切换到新分支

    Args:
        branch_name: 分支名称
        path: 仓库路径
    """
    try:
        git = GitOperations(path)

        print_info(f"创建新分支: {branch_name}")
        if not git.branch('create', branch_name):
            return False

        print_info(f"切换到分支: {branch_name}")
        return git.branch('checkout', branch_name)

    except Exception as e:
        print_error(f"操作失败: {e}")
        return False


def delete_branch(branch_name, force=False, path='.'):
    """
    删除分支

    Args:
        branch_name: 分支名称
        force: 是否强制删除
        path: 仓库路径
    """
    try:
        git = GitOperations(path)

        if force:
            import subprocess
            result = subprocess.run(
                ['git', 'branch', '-D', branch_name],
                cwd=path,
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print_success(f"分支 {branch_name} 已强制删除")
                return True
            else:
                print_error(f"删除失败: {result.stderr}")
                return False
        else:
            return git.branch('delete', branch_name)

    except Exception as e:
        print_error(f"删除分支失败: {e}")
        return False


def merge_branch(source_branch, path='.'):
    """
    合并分支到当前分支

    Args:
        source_branch: 要合并的源分支
        path: 仓库路径
    """
    try:
        import subprocess
        result = subprocess.run(
            ['git', 'merge', source_branch],
            cwd=path,
            capture_output=False
        )

        if result.returncode == 0:
            print_success(f"分支 {source_branch} 已合并到当前分支")
            return True
        else:
            print_error("合并失败")
            return False

    except Exception as e:
        print_error(f"合并失败: {e}")
        return False


def show_current_branch(path='.'):
    """显示当前分支"""
    try:
        from utils import get_current_branch
        branch = get_current_branch(path)
        if branch:
            print_success(f"当前分支: {branch}")
        else:
            print_error("无法获取当前分支")
        return branch is not None
    except Exception as e:
        print_error(f"获取失败: {e}")
        return False


def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print("Git 分支管理工具\n")
        print("使用方法:")
        print("  python branch_manager.py 列出                    # 列出所有分支")
        print("  python branch_manager.py 创建 <branch>           # 创建新分支")
        print("  python branch_manager.py 切换 <branch>           # 切换分支")
        print("  python branch_manager.py 新建 <branch>           # 创建并切换")
        print("  python branch_manager.py 删除 <branch> [--force] # 删除分支")
        print("  python branch_manager.py 合并 <branch>           # 合并分支")
        print("  python branch_manager.py 当前                    # 查看当前分支")
        print("\n示例:")
        print("  python branch_manager.py 创建 feature-login")
        print("  python branch_manager.py 切换 main")
        print("  python branch_manager.py 新建 feature-payment")
        print("  python branch_manager.py 合并 feature-login")
        sys.exit(1)

    command = sys.argv[1]

    if command == "列出":
        list_branches()

    elif command == "创建":
        if len(sys.argv) < 3:
            print_error("请指定分支名称")
            sys.exit(1)
        create_branch(sys.argv[2])

    elif command == "切换":
        if len(sys.argv) < 3:
            print_error("请指定分支名称")
            sys.exit(1)
        switch_branch(sys.argv[2])

    elif command == "新建":
        if len(sys.argv) < 3:
            print_error("请指定分支名称")
            sys.exit(1)
        create_and_switch(sys.argv[2])

    elif command == "删除":
        if len(sys.argv) < 3:
            print_error("请指定分支名称")
            sys.exit(1)
        force = "--force" in sys.argv
        delete_branch(sys.argv[2], force=force)

    elif command == "合并":
        if len(sys.argv) < 3:
            print_error("请指定要合并的分支")
            sys.exit(1)
        merge_branch(sys.argv[2])

    elif command == "当前":
        show_current_branch()

    else:
        print_error(f"未知命令: {command}")


if __name__ == "__main__":
    main()
