#!/usr/bin/env python3
"""
GitHub Issue Fetcher
获取 GitHub Issue 详细信息

Usage:
    python issue_fetcher.py owner/repo issue_number
    python issue_fetcher.py chuanminglu/product-service 123
"""

import sys
import json
import subprocess
from typing import Dict, Any, Optional


def fetch_issue_via_gh_cli(owner_repo: str, issue_number: int) -> Optional[Dict[str, Any]]:
    """
    使用 GitHub CLI 获取 Issue 详情
    
    Args:
        owner_repo: 仓库路径（如 "owner/repo"）
        issue_number: Issue 编号
        
    Returns:
        Issue 详情字典，失败则返回 None
    """
    try:
        cmd = [
            "gh", "issue", "view", str(issue_number),
            "--repo", owner_repo,
            "--json", "title,body,labels,state,comments,author,createdAt,updatedAt"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',  # 明确指定 UTF-8 编码，解决 Windows 环境问题
            check=True
        )
        
        issue_data = json.loads(result.stdout)
        return issue_data
        
    except subprocess.CalledProcessError as e:
        print(f"❌ 获取 Issue 失败: {e.stderr}", file=sys.stderr)
        return None
    except json.JSONDecodeError as e:
        print(f"❌ 解析 JSON 失败: {e}", file=sys.stderr)
        return None
    except FileNotFoundError:
        print("❌ GitHub CLI (gh) 未安装，请先安装: https://cli.github.com/", file=sys.stderr)
        return None


def format_issue_info(issue: Dict[str, Any]) -> str:
    """
    格式化 Issue 信息为 Markdown
    
    Args:
        issue: Issue 数据字典
        
    Returns:
        格式化的 Markdown 字符串
    """
    labels = ", ".join([label["name"] for label in issue.get("labels", [])])
    
    comments_text = ""
    if issue.get("comments"):
        comments_text = "\n\n**评论**:\n"
        for i, comment in enumerate(issue["comments"], 1):
            author = comment["author"]["login"]
            body = comment["body"][:200]  # 限制长度
            comments_text += f"{i}. @{author}: {body}...\n"
    
    output = f"""
# Issue 详情

**标题**: {issue['title']}

**状态**: {issue['state']}

**标签**: {labels or '无'}

**创建者**: @{issue['author']['login']}

**创建时间**: {issue['createdAt']}

**更新时间**: {issue['updatedAt']}

---

## 描述

{issue.get('body', '（无描述）')}

{comments_text}
"""
    return output.strip()


def main():
    if len(sys.argv) != 3:
        print("Usage: python issue_fetcher.py owner/repo issue_number")
        print("Example: python issue_fetcher.py chuanminglu/product-service 123")
        sys.exit(1)
    
    owner_repo = sys.argv[1]
    try:
        issue_number = int(sys.argv[2])
    except ValueError:
        print(f"❌ Issue 编号必须是数字: {sys.argv[2]}")
        sys.exit(1)
    
    print(f"🔍 正在获取 Issue #{issue_number} from {owner_repo}...")
    
    issue_data = fetch_issue_via_gh_cli(owner_repo, issue_number)
    
    if issue_data:
        print("\n✅ 成功获取 Issue 详情:\n")
        print(format_issue_info(issue_data))
        
        # 保存到文件（可选）
        output_file = f"issue-{issue_number}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(issue_data, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Issue 数据已保存到: {output_file}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
