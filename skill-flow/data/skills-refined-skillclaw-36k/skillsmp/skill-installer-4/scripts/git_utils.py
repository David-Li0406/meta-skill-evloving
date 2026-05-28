#!/usr/bin/env python3
"""Git 操作工具函数，支持 GitHub、GitLab 和 Gitea"""

from __future__ import annotations

import os
import subprocess
import urllib.request
import urllib.error
import urllib.parse
from typing import Literal


def git_request(url: str, user_agent: str = "skill-installer", platform: str = "github") -> bytes:
    """发送 Git 平台 API 请求
    
    Args:
        url: API URL
        user_agent: User-Agent 标识
        platform: Git 平台类型 (github/gitlab/gitea)
    
    Returns:
        响应内容
    """
    headers = {"User-Agent": user_agent}
    
    # 根据平台类型添加认证令牌
    if platform == "github":
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
    elif platform == "gitlab":
        token = os.environ.get("GITLAB_TOKEN")
        if token:
            headers["PRIVATE-TOKEN"] = token
    elif platform == "gitea":
        token = os.environ.get("GITEA_TOKEN")
        if token:
            headers["Authorization"] = f"token {token}"
    
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        return resp.read()


def parse_git_url(url: str) -> dict[str, str]:
    """解析 Git 仓库 URL，支持 GitHub、GitLab 和 Gitea
    
    Args:
        url: Git 仓库 URL
    
    Returns:
        包含 platform, host, owner, repo, ref, path 的字典
    
    Raises:
        ValueError: URL 格式不正确
    """
    import urllib.parse
    
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc
    
    # 判断平台类型
    platform = "unknown"
    if "github.com" in host:
        platform = "github"
    elif "gitlab.com" in host or "gitlab" in host:
        platform = "gitlab"
    elif "gitea" in host:
        platform = "gitea"
    
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        raise ValueError("URL 格式不正确，至少需要包含 owner/repo")
    
    owner = parts[0]
    repo = parts[1]
    ref = "main"
    path = ""
    
    # 解析 tree/blob 路径
    if len(parts) > 2:
        if parts[2] in ("tree", "blob", "-"):
            if len(parts) >= 4:
                ref = parts[3]
                path = "/".join(parts[4:]) if len(parts) > 4 else ""
        else:
            path = "/".join(parts[2:])
    
    return {
        "platform": platform,
        "host": host,
        "owner": owner,
        "repo": repo,
        "ref": ref,
        "path": path
    }


def get_api_contents_url(platform: str, host: str, owner: str, repo: str, path: str, ref: str) -> str:
    """构造 API contents URL
    
    Args:
        platform: 平台类型
        host: 主机名
        owner: 所有者
        repo: 仓库名
        path: 路径
        ref: 引用（分支/标签）
    
    Returns:
        API URL
    """
    if platform == "github":
        return f"https://api.github.com/repos/{owner}/{repo}/contents/{path}?ref={ref}"
    elif platform == "gitlab":
        # GitLab API 使用 URL 编码的项目路径
        project_path = urllib.parse.quote(f"{owner}/{repo}", safe="")
        file_path = urllib.parse.quote(path, safe="")
        return f"https://{host}/api/v4/projects/{project_path}/repository/tree?path={file_path}&ref={ref}"
    elif platform == "gitea":
        return f"https://{host}/api/v1/repos/{owner}/{repo}/contents/{path}?ref={ref}"
    else:
        raise ValueError(f"不支持的平台: {platform}")


def build_repo_url(platform: str, host: str, owner: str, repo: str, protocol: Literal["https", "ssh"] = "https") -> str:
    """构造仓库克隆 URL
    
    Args:
        platform: 平台类型
        host: 主机名
        owner: 所有者
        repo: 仓库名
        protocol: 协议类型 (https/ssh)
    
    Returns:
        克隆 URL
    """
    if protocol == "https":
        return f"https://{host}/{owner}/{repo}.git"
    else:
        return f"git@{host}:{owner}/{repo}.git"


def run_git_command(args: list[str], cwd: str | None = None) -> tuple[int, str, str]:
    """运行 Git 命令
    
    Args:
        args: Git 命令参数
        cwd: 工作目录
    
    Returns:
        (返回码, 标准输出, 标准错误)
    """
    result = subprocess.run(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=cwd
    )
    return result.returncode, result.stdout, result.stderr
