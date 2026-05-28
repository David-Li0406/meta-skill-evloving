#!/usr/bin/env python3
"""
align_all.py - 全量对齐所有 Skills 的经验

遍历 Skills 目录，为所有包含 evolution.json 的 Skills 执行缝合操作。
通常在 skill-manager 批量更新后使用，恢复用户经验。

用法:
    python align_all.py <skills_dir>
    python align_all.py <skills_dir> --dry-run
    python align_all.py <skills_dir> --backup

选项:
    --dry-run   仅预览，不修改文件
    --backup    修改前备份原文件
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Tuple


def find_skills_with_evolution(skills_root: str) -> List[Path]:
    """
    查找所有包含 evolution.json 的 Skill 目录

    Args:
        skills_root: Skills 根目录

    Returns:
        list: 包含 evolution.json 的 Skill 目录列表
    """
    skills_path = Path(skills_root)
    if not skills_path.exists():
        return []

    result = []
    for item in sorted(skills_path.iterdir()):
        if not item.is_dir():
            continue
        if item.name.startswith('.'):
            continue

        evolution_json = item / "evolution.json"
        skill_md = item / "SKILL.md"

        if evolution_json.exists() and skill_md.exists():
            result.append(item)

    return result


def align_skill(skill_dir: Path, dry_run: bool = False, backup: bool = False) -> Tuple[bool, str]:
    """
    对齐单个 Skill

    Args:
        skill_dir: Skill 目录
        dry_run: 是否仅预览
        backup: 是否备份

    Returns:
        tuple: (是否成功, 消息)
    """
    stitch_script = Path(__file__).parent / "smart_stitch.py"

    if not stitch_script.exists():
        return False, f"smart_stitch.py 不存在: {stitch_script}"

    cmd = [sys.executable, str(stitch_script), str(skill_dir)]
    if dry_run:
        cmd.append('--dry-run')
    if backup:
        cmd.append('--backup')

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip() or result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "执行超时"
    except Exception as e:
        return False, str(e)


def align_all(skills_root: str, dry_run: bool = False, backup: bool = False) -> dict:
    """
    对齐所有 Skills

    Args:
        skills_root: Skills 根目录
        dry_run: 是否仅预览
        backup: 是否备份

    Returns:
        dict: 统计结果
    """
    skills_path = Path(skills_root)

    if not skills_path.exists():
        print(f"错误: 目录不存在: {skills_root}", file=sys.stderr)
        return {"total": 0, "success": 0, "failed": 0, "skipped": 0}

    # 查找需要对齐的 Skills
    skills_to_align = find_skills_with_evolution(skills_root)

    if not skills_to_align:
        print("没有找到包含 evolution.json 的 Skills")
        return {"total": 0, "success": 0, "failed": 0, "skipped": 0}

    print(f"找到 {len(skills_to_align)} 个需要对齐的 Skills")
    if dry_run:
        print("[Dry Run 模式]")
    print("-" * 40)

    stats = {"total": len(skills_to_align), "success": 0, "failed": 0, "skipped": 0}
    failed_skills = []

    for skill_dir in skills_to_align:
        skill_name = skill_dir.name
        print(f"\n处理: {skill_name}")

        success, message = align_skill(skill_dir, dry_run=dry_run, backup=backup)

        if success:
            stats["success"] += 1
            if message:
                print(f"  {message}")
        else:
            stats["failed"] += 1
            failed_skills.append((skill_name, message))
            print(f"  ❌ 失败: {message}")

    # 输出统计
    print("\n" + "=" * 40)
    print(f"对齐完成:")
    print(f"  总计: {stats['total']}")
    print(f"  成功: {stats['success']}")
    print(f"  失败: {stats['failed']}")

    if failed_skills:
        print("\n失败的 Skills:")
        for name, msg in failed_skills:
            print(f"  - {name}: {msg}")

    return stats


def main():
    import argparse

    parser = argparse.ArgumentParser(description='全量对齐所有 Skills 的经验')
    parser.add_argument('skills_dir', help='Skills 目录路径')
    parser.add_argument('--dry-run', action='store_true', help='仅预览，不修改文件')
    parser.add_argument('--backup', '-b', action='store_true', help='修改前备份原文件')

    args = parser.parse_args()

    stats = align_all(args.skills_dir, dry_run=args.dry_run, backup=args.backup)

    # 根据结果设置退出码
    if stats["failed"] > 0:
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
