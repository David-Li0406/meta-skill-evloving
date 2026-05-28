#!/usr/bin/env python3
"""
Skill Enable/Disable Script

A script to enable or disable skills by moving them to/from .disabled directory.
"""

import argparse
import sys
import os
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description='Enable or disable skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python toggle_skill.py --enable test-skill
  python toggle_skill.py --disable test-skill
  python toggle_skill.py --enable test-skill --skills-dir ~/.config/opencode/skill
        """
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--enable',
        metavar='NAME',
        help='Enable a skill by name'
    )
    group.add_argument(
        '--disable',
        metavar='NAME',
        help='Disable a skill by name'
    )

    parser.add_argument(
        '--skills-dir',
        default=os.path.expanduser('~/.config/opencode/skill'),
        help='Skills directory path (default: ~/.config/opencode/skill)'
    )

    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)

    # Validate skills directory
    if not skills_dir.exists():
        print(f"Error: Skills directory does not exist: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    if not skills_dir.is_dir():
        print(f"Error: Skills path is not a directory: {skills_dir}", file=sys.stderr)
        sys.exit(1)

    # Execute action
    if args.enable:
        enable_skill(args.enable, skills_dir)
    elif args.disable:
        disable_skill(args.disable, skills_dir)


def enable_skill(skill_name: str, skills_dir: Path):
    """Enable a skill by moving it from .disabled to main directory."""
    disabled_dir = skills_dir / '.disabled' / skill_name
    target_dir = skills_dir / skill_name

    if not disabled_dir.exists():
        print(f"Error: {skill_name} 未被禁用或不存在", file=sys.stderr)
        sys.exit(1)

    # Check if target already exists
    if target_dir.exists():
        print(f"Error: {skill_name} 已存在于主目录中", file=sys.stderr)
        sys.exit(1)

    # Move skill from disabled to main directory
    import shutil
    shutil.move(str(disabled_dir), str(target_dir))

    # Clean up empty .disabled directory
    disabled_parent = disabled_dir.parent
    if disabled_parent.is_dir() and not any(disabled_parent.iterdir()):
        disabled_parent.rmdir()

    print(f"已启用: {skill_name}")


def disable_skill(skill_name: str, skills_dir: Path):
    """Disable a skill by moving it to .disabled directory."""
    source_dir = skills_dir / skill_name
    disabled_dir = skills_dir / '.disabled'

    if not source_dir.exists():
        print(f"Error: {skill_name} 不存在", file=sys.stderr)
        sys.exit(1)

    # Create .disabled directory if it doesn't exist
    disabled_dir.mkdir(exist_ok=True)

    # Move skill to disabled directory
    target_dir = disabled_dir / skill_name
    import shutil
    shutil.move(str(source_dir), str(target_dir))

    print(f"已禁用: {skill_name}")


if __name__ == "__main__":
    main()
