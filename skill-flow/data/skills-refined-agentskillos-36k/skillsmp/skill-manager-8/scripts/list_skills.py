#!/usr/bin/env python3
"""
list_skills.py - 列出所有已安装的 Skills

显示 Skills 的名称、类型、版本、描述等信息。

用法:
    python list_skills.py <skills_dir>
    python list_skills.py <skills_dir> --json
    python list_skills.py <skills_dir> --verbose

输出:
    表格格式或 JSON 格式的 Skills 列表
"""

import os
import sys
import re
import json
from pathlib import Path
from typing import Optional

# 尝试导入 yaml
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def parse_frontmatter_simple(content: str) -> dict:
    """简单的 YAML frontmatter 解析"""
    pattern = r'^---\s*\n(.*?)\n---'
    match = re.match(pattern, content, re.DOTALL)
    if not match:
        return {}

    yaml_content = match.group(1)
    result = {}

    for line in yaml_content.split('\n'):
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()

            # 移除引号
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]

            # 处理布尔值
            if value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False

            result[key] = value

    return result


def parse_frontmatter(content: str) -> dict:
    """解析 YAML frontmatter"""
    if HAS_YAML:
        pattern = r'^---\s*\n(.*?)\n---'
        match = re.match(pattern, content, re.DOTALL)
        if match:
            try:
                return yaml.safe_load(match.group(1)) or {}
            except yaml.YAMLError:
                pass
    return parse_frontmatter_simple(content)


def get_skill_type(frontmatter: dict) -> str:
    """判断 Skill 类型"""
    if frontmatter.get('source_url') or frontmatter.get('github_url'):
        return 'GitHub'
    elif frontmatter.get('evolution_enabled') is False:
        return 'Static'
    else:
        return 'Standard'


def get_dir_size(path: Path) -> int:
    """计算目录大小（字节）"""
    total = 0
    try:
        for item in path.rglob('*'):
            if item.is_file():
                total += item.stat().st_size
    except Exception:
        pass
    return total


def format_size(size: int) -> str:
    """格式化文件大小"""
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f}K"
    else:
        return f"{size / (1024 * 1024):.1f}M"


def list_skills(skills_root: str, verbose: bool = False) -> list:
    """
    列出目录中的所有 Skills

    Args:
        skills_root: Skills 根目录
        verbose: 是否包含详细信息

    Returns:
        list: Skills 信息列表
    """
    skill_list = []
    skills_path = Path(skills_root)

    if not skills_path.exists():
        print(f"错误: 目录不存在: {skills_root}", file=sys.stderr)
        return []

    for item in sorted(skills_path.iterdir()):
        if not item.is_dir():
            continue

        # 跳过隐藏目录
        if item.name.startswith('.'):
            continue

        skill_md = item / "SKILL.md"

        skill_info = {
            "name": item.name,
            "dir": str(item),
            "has_skill_md": skill_md.exists(),
        }

        if skill_md.exists():
            try:
                content = skill_md.read_text(encoding='utf-8')
                frontmatter = parse_frontmatter(content)

                skill_info.update({
                    "name": frontmatter.get('name', item.name),
                    "description": frontmatter.get('description', ''),
                    "version": frontmatter.get('version', ''),
                    "type": get_skill_type(frontmatter),
                    "source_url": frontmatter.get('source_url', frontmatter.get('github_url', '')),
                    "evolution_enabled": frontmatter.get('evolution_enabled', True),
                    "created_at": frontmatter.get('created_at', ''),
                    "updated_at": frontmatter.get('updated_at', ''),
                })

                if verbose:
                    skill_info["size"] = get_dir_size(item)
                    skill_info["size_formatted"] = format_size(skill_info["size"])

                    # 检查子目录
                    skill_info["has_scripts"] = (item / "scripts").exists()
                    skill_info["has_references"] = (item / "references").exists()
                    skill_info["has_assets"] = (item / "assets").exists()
                    skill_info["has_evolution"] = (item / "evolution.json").exists()

            except Exception as e:
                skill_info["error"] = str(e)
        else:
            skill_info["type"] = "Invalid"
            skill_info["description"] = "Missing SKILL.md"

        skill_list.append(skill_info)

    return skill_list


def format_table(skills: list, verbose: bool = False) -> str:
    """格式化表格输出"""
    if verbose:
        header = f"{'Name':<22} | {'Type':<8} | {'Ver':<8} | {'Size':<6} | {'Evo':<3} | {'Description':<30}"
        sep = "-" * 95
    else:
        header = f"{'Name':<22} | {'Type':<8} | {'Ver':<8} | {'Description':<40}"
        sep = "-" * 85

    lines = [header, sep]

    for skill in skills:
        name = skill['name'][:21]
        stype = skill.get('type', 'N/A')[:7]
        version = (skill.get('version') or 'N/A')[:7]
        desc = (skill.get('description') or '')[:39].replace('\n', ' ')

        if verbose:
            size = skill.get('size_formatted', 'N/A')[:5]
            evo = 'Yes' if skill.get('evolution_enabled', True) else 'No'
            desc = desc[:29]
            lines.append(f"{name:<22} | {stype:<8} | {version:<8} | {size:<6} | {evo:<3} | {desc:<30}")
        else:
            lines.append(f"{name:<22} | {stype:<8} | {version:<8} | {desc:<40}")

    lines.append(sep)
    lines.append(f"Total: {len(skills)} skills")

    return '\n'.join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='列出所有已安装的 Skills')
    parser.add_argument('skills_dir', help='Skills 目录路径')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')

    args = parser.parse_args()

    skills = list_skills(args.skills_dir, verbose=args.verbose)

    if not skills:
        print("未找到任何 Skills", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(skills, indent=2, ensure_ascii=False))
    else:
        print(format_table(skills, verbose=args.verbose))


if __name__ == "__main__":
    main()
