#!/usr/bin/env python3
"""
GitHub Pull Request Creator
创建 GitHub Pull Request

Usage:
    python pr_creator.py --title "PR标题" --body "PR描述" --base main --head fix/issue-123
"""

import sys
import argparse
import subprocess
from typing import Optional


def create_pr_via_gh_cli(
    title: str,
    body: str,
    base: str = "main",
    head: Optional[str] = None,
    draft: bool = False
) -> bool:
    """
    使用 GitHub CLI 创建 Pull Request
    
    Args:
        title: PR 标题
        body: PR 描述
        base: 目标分支（默认 main）
        head: 源分支（默认当前分支）
        draft: 是否创建为草稿
        
    Returns:
        成功返回 True，失败返回 False
    """
    try:
        cmd = [
            "gh", "pr", "create",
            "--title", title,
            "--body", body,
            "--base", base
        ]
        
        if head:
            cmd.extend(["--head", head])
        
        if draft:
            cmd.append("--draft")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',  # 明确指定 UTF-8 编码，解决 Windows 环境问题
            check=True
        )
        
        print("✅ PR 创建成功!")
        print(result.stdout)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ PR 创建失败: {e.stderr}", file=sys.stderr)
        return False
    except FileNotFoundError:
        print("❌ GitHub CLI (gh) 未安装，请先安装: https://cli.github.com/", file=sys.stderr)
        return False


def read_body_from_file(file_path: str) -> Optional[str]:
    """
    从文件读取 PR 描述
    
    Args:
        file_path: 文件路径
        
    Returns:
        文件内容，失败返回 None
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"❌ 读取文件失败: {e}", file=sys.stderr)
        return None


def main():
    parser = argparse.ArgumentParser(
        description="创建 GitHub Pull Request"
    )
    parser.add_argument(
        "--title",
        required=True,
        help="PR 标题"
    )
    parser.add_argument(
        "--body",
        help="PR 描述（直接提供文本）"
    )
    parser.add_argument(
        "--body-file",
        help="PR 描述文件路径"
    )
    parser.add_argument(
        "--base",
        default="main",
        help="目标分支（默认 main）"
    )
    parser.add_argument(
        "--head",
        help="源分支（默认当前分支）"
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="创建为草稿 PR"
    )
    
    args = parser.parse_args()
    
    # 获取 PR 描述
    if args.body:
        body = args.body
    elif args.body_file:
        body = read_body_from_file(args.body_file)
        if not body:
            sys.exit(1)
    else:
        print("❌ 必须提供 --body 或 --body-file 参数")
        sys.exit(1)
    
    # 创建 PR
    print(f"📤 正在创建 PR: {args.title}")
    print(f"   目标分支: {args.base}")
    if args.head:
        print(f"   源分支: {args.head}")
    if args.draft:
        print("   类型: 草稿 PR")
    
    success = create_pr_via_gh_cli(
        title=args.title,
        body=body,
        base=args.base,
        head=args.head,
        draft=args.draft
    )
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
