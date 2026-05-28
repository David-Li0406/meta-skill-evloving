#!/usr/bin/env python3
"""
GitHub 仓库管理脚本
提供克隆、创建、列出、删除仓库等功能
"""

import sys
import os
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from github_api import GitHubAPI
from utils import (
    print_success, print_error, print_info, print_warning,
    validate_repo_name, parse_repo_identifier, confirm_action
)


def clone_repo(repo_identifier, dest=None):
    """
    克隆 GitHub 仓库

    Args:
        repo_identifier: 仓库标识符（如：username/repo-name）
        dest: 目标目录（可选）
    """
    try:
        # 解析仓库标识符
        owner, repo = parse_repo_identifier(repo_identifier)

        # 克隆 URL
        if owner:
            clone_url = f"https://github.com/{owner}/{repo}.git"
        else:
            clone_url = f"https://github.com/{repo}.git"

        print_info(f"正在克隆仓库: {clone_url}")

        # 执行克隆
        import subprocess
        if dest:
            result = subprocess.run(['git', 'clone', clone_url, dest], capture_output=False)
        else:
            result = subprocess.run(['git', 'clone', clone_url], capture_output=False)

        if result.returncode == 0:
            print_success("仓库克隆成功！")
            return True
        else:
            print_error("克隆失败")
            return False

    except Exception as e:
        print_error(f"克隆失败: {e}")
        return False


def create_repo(repo_name, description='', private=False):
    """
    创建新的 GitHub 仓库

    Args:
        repo_name: 仓库名称
        description: 仓库描述
        private: 是否为私有仓库
    """
    try:
        # 验证仓库名称
        valid, msg = validate_repo_name(repo_name)
        if not valid:
            print_error(msg)
            return False

        # 创建 API 客户端
        api = GitHubAPI()

        print_info(f"正在创建仓库: {repo_name}")

        # 创建仓库
        result = api.create_repo(repo_name, description, private)

        print_success("仓库创建成功！")
        print(f"   名称: {result.get('name')}")
        print(f"   URL: {result.get('html_url')}")
        print(f"   可见性: {result.get('visibility')}")

        return True

    except Exception as e:
        print_error(f"创建失败: {e}")
        return False


def list_repos(visibility='all'):
    """
    列出所有仓库

    Args:
        visibility: 仓库可见性（all, public, private）
    """
    try:
        api = GitHubAPI()

        print_info("正在获取仓库列表...")

        repos = api.list_repos(visibility=visibility)

        if not repos:
            print_warning("没有找到仓库")
            return

        print_success(f"共有 {len(repos)} 个仓库:\n")

        for repo in repos:
            visibility_icon = "🔒" if repo.get('private') else "🌍"
            print(f"{visibility_icon} {repo.get('full_name')}")
            print(f"   描述: {repo.get('description', '无描述')}")
            print(f"   更新: {repo.get('updated_at')}")
            print()

    except Exception as e:
        print_error(f"获取失败: {e}")


def delete_repo(repo_identifier):
    """
    删除 GitHub 仓库

    Args:
        repo_identifier: 仓库标识符（如：username/repo-name）
    """
    try:
        # 解析仓库标识符
        owner, repo = parse_repo_identifier(repo_identifier)

        if not owner:
            api = GitHubAPI()
            owner = api.get_username()

        if not owner:
            print_error("无法确定仓库所有者")
            return False

        # 确认操作
        if not confirm_action(f"确定要删除仓库 {owner}/{repo} 吗？此操作不可恢复！"):
            print_info("操作已取消")
            return False

        # 删除仓库
        api = GitHubAPI()
        api.delete_repo(owner, repo)

        print_success(f"仓库 {owner}/{repo} 已删除")
        return True

    except Exception as e:
        print_error(f"删除失败: {e}")
        return False


def show_repo_info(repo_identifier):
    """
    显示仓库详细信息

    Args:
        repo_identifier: 仓库标识符
    """
    try:
        # 解析仓库标识符
        owner, repo = parse_repo_identifier(repo_identifier)

        if not owner:
            api = GitHubAPI()
            owner = api.get_username()

        if not owner:
            print_error("无法确定仓库所有者")
            return False

        # 获取仓库信息
        api = GitHubAPI()
        info = api.get_repo(owner, repo)

        print_success(f"仓库信息: {info.get('full_name')}")
        print(f"\n📝 描述: {info.get('description', '无描述')}")
        print(f"🌍 URL: {info.get('html_url')}")
        print(f"🔒 可见性: {info.get('visibility')}")
        print(f"⭐ Stars: {info.get('stargazers_count')}")
        print(f"🍴 Forks: {info.get('forks_count')}")
        print(f"👀 Watchers: {info.get('watchers_count')}")
        print(f"📂 语言: {info.get('language')}")
        print(f"📅 创建: {info.get('created_at')}")
        print(f"🔄 更新: {info.get('updated_at')}")

        return True

    except Exception as e:
        print_error(f"获取失败: {e}")
        return False


def main():
    """命令行接口"""
    if len(sys.argv) < 2:
        print("GitHub 仓库管理工具\n")
        print("使用方法:")
        print("  python repo_manager.py 克隆 <repo> [dest]         # 克隆仓库")
        print("  python repo_manager.py 创建 <name> [desc] [--private]  # 创建仓库")
        print("  python repo_manager.py 列出 [all|public|private]  # 列出仓库")
        print("  python repo_manager.py 删除 <repo>               # 删除仓库")
        print("  python repo_manager.py 信息 <repo>               # 查看仓库信息")
        print("\n示例:")
        print("  python repo_manager.py 克隆 username/my-project")
        print("  python repo_manager.py 创建 my-repo \"我的项目\"")
        print("  python repo_manager.py 创建 my-repo \"私有项目\" --private")
        print("  python repo_manager.py 列出")
        print("  python repo_manager.py 删除 username/my-repo")
        sys.exit(1)

    command = sys.argv[1]

    if command == "克隆":
        if len(sys.argv) < 3:
            print_error("请指定要克隆的仓库")
            sys.exit(1)

        repo = sys.argv[2]
        dest = sys.argv[3] if len(sys.argv) > 3 else None

        clone_repo(repo, dest)

    elif command == "创建":
        if len(sys.argv) < 3:
            print_error("请指定仓库名称")
            sys.exit(1)

        repo_name = sys.argv[2]
        description = sys.argv[3] if len(sys.argv) > 3 else ""
        private = "--private" in sys.argv

        create_repo(repo_name, description, private)

    elif command == "列出":
        visibility = sys.argv[2] if len(sys.argv) > 2 else 'all'
        list_repos(visibility)

    elif command == "删除":
        if len(sys.argv) < 3:
            print_error("请指定要删除的仓库")
            sys.exit(1)

        repo = sys.argv[2]
        delete_repo(repo)

    elif command == "信息":
        if len(sys.argv) < 3:
            print_error("请指定仓库")
            sys.exit(1)

        repo = sys.argv[2]
        show_repo_info(repo)

    else:
        print_error(f"未知命令: {command}")


if __name__ == "__main__":
    main()
