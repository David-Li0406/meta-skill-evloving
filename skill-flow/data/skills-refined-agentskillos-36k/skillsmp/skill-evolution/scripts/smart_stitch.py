#!/usr/bin/env python3
"""
smart_stitch.py - 智能缝合经验到 SKILL.md

读取 evolution.json 并将其内容转换为 Markdown，
自动插入或更新 SKILL.md 中的专用章节。

用法:
    python smart_stitch.py <skill_dir>
    python smart_stitch.py <skill_dir> --dry-run
    python smart_stitch.py <skill_dir> --backup

选项:
    --dry-run   仅显示将要生成的内容，不修改文件
    --backup    修改前备份原文件
"""

import os
import sys
import re
import json
import datetime
import shutil
from pathlib import Path


# 章节标题（用于匹配和替换）
SECTION_TITLE = "## User-Learned Best Practices & Constraints"

# 章节开始的正则模式
SECTION_PATTERN = r'(\n+## User-Learned Best Practices & Constraints.*?)(?=\n## |\Z)'


def load_evolution(evolution_path: Path) -> dict:
    """加载 evolution.json"""
    if not evolution_path.exists():
        return {}
    try:
        return json.loads(evolution_path.read_text(encoding='utf-8'))
    except (json.JSONDecodeError, IOError):
        return {}


def generate_evolution_section(data: dict) -> str:
    """
    根据 evolution.json 生成 Markdown 章节

    Args:
        data: evolution.json 内容

    Returns:
        str: Markdown 格式的章节内容
    """
    lines = [
        "",
        "",
        SECTION_TITLE,
        "",
        "> **Auto-Generated Section**: 此章节由 skill-evolution 自动维护，请勿手动编辑。",
        ""
    ]

    # User Preferences
    if data.get("preferences"):
        lines.append("### User Preferences")
        lines.append("")
        for item in data["preferences"]:
            lines.append(f"- {item}")
        lines.append("")

    # Known Fixes & Workarounds
    if data.get("fixes"):
        lines.append("### Known Fixes & Workarounds")
        lines.append("")
        for item in data["fixes"]:
            lines.append(f"- {item}")
        lines.append("")

    # Context-Specific Notes
    if data.get("contexts"):
        lines.append("### Context-Specific Notes")
        lines.append("")
        for item in data["contexts"]:
            lines.append(f"- {item}")
        lines.append("")

    # Custom Instruction Injection
    if data.get("custom_prompts"):
        lines.append("### Custom Instruction Injection")
        lines.append("")
        lines.append(data["custom_prompts"])
        lines.append("")

    # 元信息
    if data.get("last_updated"):
        lines.append(f"*Last updated: {data['last_updated']}*")

    return "\n".join(lines)


def stitch_skill(skill_dir: str, dry_run: bool = False, backup: bool = False) -> bool:
    """
    将 evolution.json 缝合到 SKILL.md

    Args:
        skill_dir: Skill 目录路径
        dry_run: 是否仅预览
        backup: 是否备份原文件

    Returns:
        bool: 是否成功
    """
    skill_path = Path(skill_dir)
    skill_md_path = skill_path / "SKILL.md"
    evolution_path = skill_path / "evolution.json"

    # 检查 SKILL.md
    if not skill_md_path.exists():
        print(f"错误: SKILL.md 不存在: {skill_md_path}", file=sys.stderr)
        return False

    # 检查 evolution.json
    if not evolution_path.exists():
        print(f"信息: 没有 evolution.json，跳过: {skill_path.name}")
        return True

    # 加载数据
    data = load_evolution(evolution_path)
    if not data:
        print(f"信息: evolution.json 为空，跳过: {skill_path.name}")
        return True

    # 检查是否有实际内容
    has_content = any(data.get(k) for k in ['preferences', 'fixes', 'contexts', 'custom_prompts'])
    if not has_content:
        print(f"信息: 没有可缝合的内容，跳过: {skill_path.name}")
        return True

    # 生成新章节
    evolution_section = generate_evolution_section(data)

    # 读取原始内容
    content = skill_md_path.read_text(encoding='utf-8')

    # 查找并替换或追加
    match = re.search(SECTION_PATTERN, content, re.DOTALL)

    if match:
        # 替换现有章节
        new_content = content[:match.start()] + evolution_section
        action = "更新"
    else:
        # 追加到末尾
        new_content = content.rstrip() + evolution_section
        action = "追加"

    if dry_run:
        print(f"[Dry Run] 将要{action}章节到: {skill_path.name}")
        print("-" * 40)
        print(evolution_section)
        print("-" * 40)
        return True

    # 备份
    if backup:
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = skill_md_path.with_suffix(f'.md.bak.{timestamp}')
        shutil.copy2(skill_md_path, backup_path)
        print(f"已备份到: {backup_path}")

    # 写入
    skill_md_path.write_text(new_content, encoding='utf-8')
    print(f"✅ 已{action}经验章节: {skill_path.name}")

    return True


def main():
    import argparse

    parser = argparse.ArgumentParser(description='智能缝合经验到 SKILL.md')
    parser.add_argument('skill_dir', help='Skill 目录路径')
    parser.add_argument('--dry-run', action='store_true', help='仅预览，不修改文件')
    parser.add_argument('--backup', '-b', action='store_true', help='修改前备份原文件')

    args = parser.parse_args()

    success = stitch_skill(args.skill_dir, dry_run=args.dry_run, backup=args.backup)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
