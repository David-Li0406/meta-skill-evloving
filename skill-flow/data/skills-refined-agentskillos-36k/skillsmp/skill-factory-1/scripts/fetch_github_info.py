#!/usr/bin/env python3
"""
fetch_github_info.py - 获取 GitHub 仓库信息

通过 git ls-remote 和 HTTP 请求获取仓库元数据，无需完整 clone。

用法:
    python fetch_github_info.py <github_url>

输出:
    JSON 格式的仓库信息
"""

import sys
import json
import subprocess
import urllib.request
import urllib.error
import re
from typing import Optional


def normalize_url(url: str) -> str:
    """标准化 GitHub URL"""
    clean_url = url.strip().rstrip('/')
    if clean_url.endswith('.git'):
        clean_url = clean_url[:-4]
    return clean_url


def extract_repo_parts(url: str) -> tuple[str, str]:
    """从 URL 提取 owner 和 repo 名称"""
    clean_url = normalize_url(url)
    parts = clean_url.split('/')
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    return '', parts[-1] if parts else ''


def get_remote_hash(url: str) -> str:
    """通过 git ls-remote 获取远程 HEAD hash（轻量级，无需 clone）"""
    try:
        result = subprocess.run(
            ['git', 'ls-remote', url, 'HEAD'],
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )
        if result.stdout:
            return result.stdout.split()[0]
    except subprocess.TimeoutExpired:
        print("Warning: git ls-remote timed out", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Warning: git ls-remote failed: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Warning: unexpected error: {e}", file=sys.stderr)
    return ""


def fetch_readme(url: str) -> tuple[str, str]:
    """
    获取 README 内容

    Returns:
        tuple: (readme_content, branch_name)
    """
    clean_url = normalize_url(url)
    raw_base = clean_url.replace("github.com", "raw.githubusercontent.com")

    # 尝试不同的分支和文件名组合
    attempts = [
        ("main", "README.md"),
        ("master", "README.md"),
        ("main", "readme.md"),
        ("master", "readme.md"),
        ("main", "Readme.md"),
        ("master", "Readme.md"),
    ]

    for branch, filename in attempts:
        try:
            readme_url = f"{raw_base}/{branch}/{filename}"
            req = urllib.request.Request(
                readme_url,
                headers={'User-Agent': 'skill-factory/1.0'}
            )
            with urllib.request.urlopen(req, timeout=15) as response:
                content = response.read().decode('utf-8')
                return content, branch
        except urllib.error.HTTPError:
            continue
        except urllib.error.URLError:
            continue
        except Exception:
            continue

    return "", ""


def fetch_repo_description(owner: str, repo: str) -> str:
    """通过 GitHub API 获取仓库描述（可选，可能受限流）"""
    try:
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
        req = urllib.request.Request(
            api_url,
            headers={
                'User-Agent': 'skill-factory/1.0',
                'Accept': 'application/vnd.github.v3+json'
            }
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('description', '') or ''
    except Exception:
        return ""


def extract_description_from_readme(readme: str) -> str:
    """从 README 中提取描述（第一段非标题文本）"""
    if not readme:
        return ""

    lines = readme.split('\n')
    description_lines = []
    in_description = False
    in_html_block = False

    for line in lines:
        stripped = line.strip()

        # 跟踪 HTML 块
        if '<div' in stripped.lower() or '<table' in stripped.lower():
            in_html_block = True
            continue
        if '</div>' in stripped.lower() or '</table>' in stripped.lower():
            in_html_block = False
            continue

        # 跳过 HTML 块内容
        if in_html_block:
            continue

        # 跳过空行
        if not stripped:
            if in_description and description_lines:
                break
            continue

        # 跳过标题行
        if stripped.startswith('#'):
            if in_description and description_lines:
                break
            continue

        # 跳过徽章行
        if stripped.startswith('[![') or stripped.startswith('!['):
            continue

        # 跳过 HTML 注释
        if stripped.startswith('<!--') or stripped.endswith('-->'):
            continue

        # 跳过纯 HTML 标签行
        if stripped.startswith('<') and stripped.endswith('>'):
            continue

        # 跳过包含大量 HTML 的行
        if stripped.count('<') > 2 or stripped.count('>') > 2:
            continue

        in_description = True
        description_lines.append(stripped)

        # 限制描述长度
        if len(' '.join(description_lines)) > 300:
            break

    result = ' '.join(description_lines)[:500]

    # 清理残留的 HTML 标签
    result = re.sub(r'<[^>]+>', '', result)

    return result.strip()


def get_repo_info(url: str) -> dict:
    """
    获取 GitHub 仓库的完整信息

    Args:
        url: GitHub 仓库 URL

    Returns:
        dict: 包含仓库元数据的字典
    """
    clean_url = normalize_url(url)
    owner, repo_name = extract_repo_parts(url)

    # 1. 获取 commit hash
    latest_hash = get_remote_hash(url)

    # 2. 获取 README
    readme_content, default_branch = fetch_readme(url)

    # 3. 获取描述
    description = fetch_repo_description(owner, repo_name)
    if not description:
        description = extract_description_from_readme(readme_content)

    # 4. 构建结果
    result = {
        "name": repo_name,
        "owner": owner,
        "url": clean_url,
        "latest_hash": latest_hash,
        "default_branch": default_branch or "main",
        "description": description,
        "readme": readme_content[:15000] if readme_content else "",  # 限制大小
        "readme_truncated": len(readme_content) > 15000 if readme_content else False
    }

    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python fetch_github_info.py <github_url>", file=sys.stderr)
        print("示例: python fetch_github_info.py https://github.com/yt-dlp/yt-dlp", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]

    # 验证 URL 格式
    if not re.match(r'https?://(www\.)?github\.com/', url):
        print(f"错误: 不是有效的 GitHub URL: {url}", file=sys.stderr)
        sys.exit(1)

    info = get_repo_info(url)

    # 输出 JSON
    print(json.dumps(info, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
