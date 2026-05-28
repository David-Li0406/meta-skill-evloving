#!/usr/bin/env python3
"""
delete_skill.py - 删除指定的 Skill

安全地删除 Skill 目录，支持备份选项。

用法:
    python delete_skill.py <skill_name> <skills_dir>
    python delete_skill.py <skill_name> <skills_dir> --backup
    python delete_skill.py <skill_name> <skills_dir> --force

选项:
    --backup    删除前备份到 .skill-backup 目录
    --force     跳过确认提示
"""

import os
import sys
import shutil
import datetime
from pathlib import Path


def backup_skill(skill_dir: Path, backup_root: Path) -> str:
    """
    备份 Skill 目录

    Args:
        skill_dir: Skill 目录路径
        backup_root: 备份根目录

    Returns:
        str: 备份路径
    """
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_name = f"{skill_dir.name}_{timestamp}"
    backup_path = backup_root / backup_name

    backup_root.mkdir(parents=True, exist_ok=True)
    shutil.copytree(skill_dir, backup_path)

    return str(backup_path)


def delete_skill(
    skill_name: str,
    skills_root: str,
    backup: bool = False,
    force: bool = False
) -> bool:
    """
    删除 Skill

    Args:
        skill_name: Skill 名称
        skills_root: Skills 根目录
        backup: 是否备份
        force: 是否跳过确认

    Returns:
        bool: 是否成功删除
    """
    skills_path = Path(skills_root)
    skill_dir = skills_path / skill_name

    # 检查 Skill 是否存在
    if not skill_dir.exists():
        print(f"错误: Skill '{skill_name}' 不存在于 {skills_root}", file=sys.stderr)
        return False

    if not skill_dir.is_dir():
        print(f"错误: '{skill_name}' 不是目录", file=sys.stderr)
        return False

    # 检查是否有 SKILL.md
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"警告: '{skill_name}' 没有 SKILL.md 文件", file=sys.stderr)

    # 计算目录大小
    total_size = 0
    file_count = 0
    for item in skill_dir.rglob('*'):
        if item.is_file():
            total_size += item.stat().st_size
            file_count += 1

    # 显示信息
    print(f"Skill: {skill_name}")
    print(f"路径: {skill_dir}")
    print(f"文件数: {file_count}")
    print(f"大小: {total_size / 1024:.1f} KB")

    # 确认删除
    if not force:
        print()
        confirm = input(f"确定要删除 '{skill_name}'? [y/N]: ").strip().lower()
        if confirm not in ('y', 'yes'):
            print("已取消删除")
            return False

    # 备份
    if backup:
        backup_root = skills_path / ".skill-backup"
        try:
            backup_path = backup_skill(skill_dir, backup_root)
            print(f"已备份到: {backup_path}")
        except Exception as e:
            print(f"备份失败: {e}", file=sys.stderr)
            if not force:
                return False

    # 删除
    try:
        shutil.rmtree(skill_dir)
        print(f"✅ 已删除 Skill: {skill_name}")
        return True
    except Exception as e:
        print(f"删除失败: {e}", file=sys.stderr)
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(description='删除指定的 Skill')
    parser.add_argument('skill_name', help='要删除的 Skill 名称')
    parser.add_argument('skills_dir', help='Skills 目录路径')
    parser.add_argument('--backup', '-b', action='store_true', help='删除前备份')
    parser.add_argument('--force', '-f', action='store_true', help='跳过确认提示')

    args = parser.parse_args()

    success = delete_skill(
        args.skill_name,
        args.skills_dir,
        backup=args.backup,
        force=args.force
    )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
