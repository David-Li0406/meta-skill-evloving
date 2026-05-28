#!/usr/bin/env python3
"""
上传文件夹到 GitHub
将本地文件夹上传到 GitHub 仓库（会自动创建仓库）
"""

import sys
import os
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))
from github_api import GitHubAPI
from git_operations import GitOperations
from utils import (
    print_success, print_error, print_info, print_warning,
    validate_repo_name, confirm_action
)


def upload_folder(folder_path, repo_name, commit_message="初始提交", create_repo=True, private=False):
    """
    上传文件夹到 GitHub

    Args:
        folder_path: 本地文件夹路径
        repo_name: GitHub 仓库名称
        commit_message: 提交信息
        create_repo: 是否自动创建仓库
        private: 是否为私有仓库
    """
    try:
        # 检查文件夹是否存在
        folder = Path(folder_path).resolve()
        if not folder.exists():
            print_error(f"文件夹不存在: {folder}")
            return False

        if not folder.is_dir():
            print_error(f"路径不是文件夹: {folder}")
            return False

        # 验证仓库名称
        valid, msg = validate_repo_name(repo_name)
        if not valid:
            print_error(msg)
            return False

        # 获取 GitHub 用户名
        api = GitHubAPI()
        username = api.get_username()

        print_info(f"准备上传文件夹: {folder}")
        print_info(f"目标仓库: {username}/{repo_name}")

        # 创建 GitHub 仓库
        if create_repo:
            print_info("正在创建 GitHub 仓库...")
            try:
                api.create_repo(repo_name, "", private)
                print_success("仓库创建成功")
            except Exception as e:
                if "already exists" in str(e):
                    print_warning("仓库已存在，将直接上传")
                else:
                    raise e

        # 初始化 Git
        git = GitOperations(folder)
        git.init()

        # 添加远程仓库
        repo_url = f"https://github.com/{username}/{repo_name}.git"
        git.remote_add('origin', repo_url)

        # 检查是否有 .gitignore
        gitignore_path = folder / ".gitignore"
        if not gitignore_path.exists():
            print_info("创建 .gitignore 文件...")
            create_gitignore(folder)

        # 添加所有文件
        print_info("正在添加文件...")
        git.add('.')

        # 提交
        print_info("正在提交...")
        git.commit(commit_message)

        # 推送到 GitHub
        print_info("正在推送到 GitHub...")
        # 设置上游分支并推送
        import subprocess
        subprocess.run(
            ['git', 'push', '-u', 'origin', 'main'],
            cwd=folder,
            capture_output=False
        )

        print_success("\n✅ 上传成功！")
        print(f"   GitHub URL: https://github.com/{username}/{repo_name}")

        return True

    except Exception as e:
        print_error(f"上传失败: {e}")
        return False


def create_gitignore(folder_path):
    """
    创建 .gitignore 文件

    Args:
        folder_path: 文件夹路径
    """
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
.env
"""

    gitignore_path = Path(folder_path) / ".gitignore"
    with open(gitignore_path, 'w') as f:
        f.write(gitignore_content)

    print_success(".gitignore 文件已创建")


def main():
    """命令行接口"""
    if len(sys.argv) < 3:
        print("上传文件夹到 GitHub\n")
        print("使用方法:")
        print("  python upload_folder.py <folder_path> <repo_name> [commit_message] [--private]")
        print("\n参数:")
        print("  folder_path    : 本地文件夹路径")
        print("  repo_name      : GitHub 仓库名称")
        print("  commit_message : 提交信息（可选，默认为'初始提交'）")
        print("  --private      : 创建为私有仓库（可选）")
        print("\n示例:")
        print("  python upload_folder.py ~/my-project my-awesome-project")
        print("  python upload_folder.py ~/my-project my-project \"第一个版本\"")
        print("  python upload_folder.py ~/my-project my-private-repo \"私有项目\" --private")
        sys.exit(1)

    folder_path = sys.argv[1]
    repo_name = sys.argv[2]
    commit_message = sys.argv[3] if len(sys.argv) > 3 else "初始提交"
    private = "--private" in sys.argv

    upload_folder(folder_path, repo_name, commit_message, private=private)


if __name__ == "__main__":
    main()
