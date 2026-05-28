#!/usr/bin/env python3
"""列出指定位置的可用技能"""

from __future__ import annotations

import argparse
import json
import os
import sys

from git_utils import parse_git_url, get_api_contents_url, git_request


class ListError(Exception):
    """列出技能时的错误"""
    pass


def list_local_skills(path: str) -> list[str]:
    """列出本地目录中的技能
    
    Args:
        path: 本地目录路径
    
    Returns:
        技能名称列表
    """
    if not os.path.isdir(path):
        raise ListError(f"目录不存在: {path}")
    
    skills = []
    for name in os.listdir(path):
        skill_path = os.path.join(path, name)
        if os.path.isdir(skill_path):
            skill_md = os.path.join(skill_path, "SKILL.md")
            if os.path.isfile(skill_md):
                skills.append(name)
    
    return sorted(skills)


def list_remote_skills(url: str, ref: str = "main") -> list[str]:
    """列出远程仓库中的技能
    
    Args:
        url: Git 仓库 URL
        ref: 分支或标签名
    
    Returns:
        技能名称列表
    """
    try:
        info = parse_git_url(url)
        if ref:
            info["ref"] = ref
        
        api_url = get_api_contents_url(
            info["platform"],
            info["host"],
            info["owner"],
            info["repo"],
            info["path"],
            info["ref"]
        )
        
        payload = git_request(api_url, "skill-installer", info["platform"])
        data = json.loads(payload.decode("utf-8"))
        
        if not isinstance(data, list):
            raise ListError("API 响应格式不正确")
        
        # 根据平台类型提取目录
        skills = []
        if info["platform"] == "github":
            skills = [item["name"] for item in data if item.get("type") == "dir"]
        elif info["platform"] == "gitlab":
            skills = [item["name"] for item in data if item.get("type") == "tree"]
        elif info["platform"] == "gitea":
            skills = [item["name"] for item in data if item.get("type") == "dir"]
        
        return sorted(skills)
        
    except Exception as exc:
        raise ListError(f"无法列出远程技能: {exc}") from exc


def get_installed_skills(install_dir: str) -> set[str]:
    """获取已安装的技能列表
    
    Args:
        install_dir: 安装目录路径
    
    Returns:
        已安装技能名称集合
    """
    if not install_dir or not os.path.isdir(install_dir):
        return set()
    
    skills = set()
    for name in os.listdir(install_dir):
        skill_path = os.path.join(install_dir, name)
        if os.path.isdir(skill_path):
            skill_md = os.path.join(skill_path, "SKILL.md")
            if os.path.isfile(skill_md):
                skills.add(name)
    
    return skills


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="列出指定位置的可用技能"
    )
    parser.add_argument(
        "source",
        help="技能源位置 (本地路径或 Git 仓库 URL)"
    )
    parser.add_argument(
        "--ref",
        default="main",
        help="Git 分支或标签 (默认: main)"
    )
    parser.add_argument(
        "--installed-dir",
        help="已安装技能的目录路径（用于标记已安装）"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="输出格式 (默认: text)"
    )
    
    args = parser.parse_args(argv)
    
    try:
        # 判断是本地路径还是远程 URL
        if os.path.exists(args.source):
            skills = list_local_skills(args.source)
        else:
            skills = list_remote_skills(args.source, args.ref)
        
        # 获取已安装技能
        installed = set()
        if args.installed_dir:
            installed = get_installed_skills(args.installed_dir)
        
        # 输出结果
        if args.format == "json":
            result = [
                {
                    "name": name,
                    "installed": name in installed
                }
                for name in skills
            ]
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if not skills:
                print("未找到技能")
            else:
                for idx, name in enumerate(skills, start=1):
                    suffix = " (已安装)" if name in installed else ""
                    print(f"{idx}. {name}{suffix}")
        
        return 0
        
    except ListError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"未预期的错误: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
