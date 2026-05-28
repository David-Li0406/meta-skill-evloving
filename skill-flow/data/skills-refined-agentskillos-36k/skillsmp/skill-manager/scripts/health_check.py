#!/usr/bin/env python3
"""
Skill Health Checker

Scan skills directory and generate health status report.
"""

import argparse
import sys
import os
import json
import subprocess
from datetime import datetime
from pathlib import Path
from utils.frontmatter_parser import parse_frontmatter


def main():
    parser = argparse.ArgumentParser(
        description='Check health status of all skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python health_check.py
  python health_check.py --skills-dir ~/.config/opencode/skill
  python health_check.py --format json
  python health_check.py --format table
        """
    )

    parser.add_argument(
        '--skills-dir',
        default=os.path.expanduser('~/.config/opencode/skill'),
        help='Skills directory path (default: ~/.config/opencode/skill)'
    )

    parser.add_argument(
        '--format',
        choices=['json', 'table'],
        default='json',
        help='Output format (default: json)'
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

    # Scan skills
    skills = scan_skills(skills_dir)

    # Calculate statistics
    total_skills = len(skills)
    invalid_skills = sum(1 for s in skills if not s['has_skill_md'])
    outdated_skills = sum(1 for s in skills if s.get('is_outdated', False))

    # Generate report
    report = {
        'timestamp': datetime.now().isoformat(),
        'total': total_skills,
        'invalid': invalid_skills,
        'outdated': outdated_skills,
        'skills': skills
    }

    # Output report
    if args.format == 'json':
        print(json.dumps(report, indent=2))
    else:
        print_table_report(report)


def scan_skills(skills_dir: Path) -> list:
    """Scan skills directory and return skill list with health status."""
    skills = []

    for item in skills_dir.iterdir():
        # Skip hidden directories
        if item.name.startswith('.'):
            continue

        if not item.is_dir():
            continue

        # Check if skill directory contains SKILL.md
        skill_md = item / 'SKILL.md'
        has_skill_md = skill_md.exists()

        skill_info = {
            'name': item.name,
            'has_skill_md': has_skill_md
        }

        # Check GitHub hash if skill is valid
        if has_skill_md:
            frontmatter = parse_frontmatter(str(skill_md))
            github_url = frontmatter.get('github_url')
            local_hash = frontmatter.get('github_hash')

            if github_url and local_hash:
                remote_hash = get_remote_hash(github_url)
                if remote_hash and remote_hash != local_hash:
                    skill_info['is_outdated'] = True
                else:
                    skill_info['is_outdated'] = False

        skills.append(skill_info)

    return skills


def print_table_report(report: dict):
    """Print report in table format."""
    print(f"Skill 健康检查报告")
    print(f"{'='*60}")
    print(f"总计: {report['total']} 个 skill")
    print(f"✅ 健康: {report['total'] - report['invalid'] - report['outdated']} 个")
    print(f"⚠️  过期: {report['outdated']} 个")
    print(f"❌ 无效: {report['invalid']} 个")
    print(f"时间: {report['timestamp']}")
    print()

    if report['skills']:
        print("技能列表:")
        for skill in report['skills']:
            if not skill['has_skill_md']:
                status = "❌"
            elif skill.get('is_outdated', False):
                status = "⚠️"
            else:
                status = "✅"
            print(f"  {status} {skill['name']}")
    else:
        print("未找到任何 skill")


def get_remote_hash(github_url: str):
    """Fetch latest commit hash from GitHub repository."""
    try:
        result = subprocess.run(
            ['git', 'ls-remote', github_url, 'HEAD'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode != 0:
            return None
        parts = result.stdout.split()
        if parts:
            return parts[0]
        return None
    except subprocess.TimeoutExpired:
        return None
    except subprocess.CalledProcessError:
        return None
    except FileNotFoundError:
        return None
    except Exception:
        return None


if __name__ == "__main__":
    main()
