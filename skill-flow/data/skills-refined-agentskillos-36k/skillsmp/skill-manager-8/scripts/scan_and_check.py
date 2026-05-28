#!/usr/bin/env python3
"""
scan_and_check.py - 扫描并检查 Skills 更新状态

并发检查所有带有 source_url 元数据的 Skills 的更新状态。

用法:
    python scan_and_check.py <skills_dir>
    python scan_and_check.py <skills_dir> --json
    python scan_and_check.py <skills_dir> --summary

输出:
    JSON 格式的状态报告
"""

import os
import sys
import re
import json
import subprocess
import concurrent.futures
import datetime
from typing import Optional
from pathlib import Path


class DateTimeEncoder(json.JSONEncoder):
    """自定义 JSON 编码器，处理日期类型"""
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super().default(obj)

# 尝试导入 yaml，如果不可用则使用简单解析
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def parse_frontmatter_simple(content: str) -> dict:
    """简单的 YAML frontmatter 解析（不依赖 pyyaml）"""
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


def get_remote_hash(url: str, timeout: int = 15) -> Optional[str]:
    """通过 git ls-remote 获取远程 HEAD hash"""
    try:
        result = subprocess.run(
            ['git', 'ls-remote', url, 'HEAD'],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout.split()[0]
    except subprocess.TimeoutExpired:
        pass
    except Exception:
        pass
    return None


def scan_skills(skills_root: str) -> list:
    """
    扫描目录中的所有 Skills

    Args:
        skills_root: Skills 根目录

    Returns:
        list: 包含 Skills 元数据的列表
    """
    skill_list = []
    skills_path = Path(skills_root)

    if not skills_path.exists():
        print(f"错误: 目录不存在: {skills_root}", file=sys.stderr)
        return []

    for item in skills_path.iterdir():
        if not item.is_dir():
            continue

        skill_md = item / "SKILL.md"
        if not skill_md.exists():
            continue

        try:
            content = skill_md.read_text(encoding='utf-8')
            frontmatter = parse_frontmatter(content)

            if not frontmatter.get('name'):
                continue

            # 获取 source_hash，确保转换为字符串
            source_hash = frontmatter.get('source_hash', '')
            if source_hash is not None:
                source_hash = str(source_hash)
            else:
                source_hash = ''

            skill_info = {
                "name": frontmatter.get('name', item.name),
                "dir": str(item),
                "description": frontmatter.get('description', '')[:100],
                "version": str(frontmatter.get('version', '')),
                "source_url": frontmatter.get('source_url', ''),
                "local_hash": source_hash,
                "evolution_enabled": frontmatter.get('evolution_enabled', True),
                "created_at": frontmatter.get('created_at', ''),
                "updated_at": frontmatter.get('updated_at', ''),
            }

            # 兼容旧格式（github_url/github_hash）
            if not skill_info['source_url']:
                skill_info['source_url'] = frontmatter.get('github_url', '')
            if not skill_info['local_hash']:
                skill_info['local_hash'] = frontmatter.get('github_hash', '')

            skill_list.append(skill_info)

        except Exception as e:
            print(f"警告: 解析 {item.name} 失败: {e}", file=sys.stderr)

    return skill_list


def check_updates(skills: list, max_workers: int = 5) -> list:
    """
    并发检查 Skills 更新状态

    Args:
        skills: Skills 列表
        max_workers: 最大并发数

    Returns:
        list: 添加了状态信息的 Skills 列表
    """
    results = []

    # 筛选有 source_url 的 Skills
    managed_skills = [s for s in skills if s.get('source_url')]
    unmanaged_skills = [s for s in skills if not s.get('source_url')]

    # 标记非托管 Skills
    for skill in unmanaged_skills:
        skill['status'] = 'unmanaged'
        skill['message'] = 'No source_url configured'
        skill['remote_hash'] = ''
        results.append(skill)

    if not managed_skills:
        return results

    # 并发检查托管 Skills
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_skill = {
            executor.submit(get_remote_hash, skill['source_url']): skill
            for skill in managed_skills
        }

        for future in concurrent.futures.as_completed(future_to_skill):
            skill = future_to_skill[future]
            try:
                remote_hash = future.result()
                skill['remote_hash'] = remote_hash or ''

                if not remote_hash:
                    skill['status'] = 'error'
                    skill['message'] = 'Could not reach remote repository'
                elif not skill['local_hash']:
                    skill['status'] = 'unknown'
                    skill['message'] = 'No local hash recorded'
                elif remote_hash != skill['local_hash']:
                    skill['status'] = 'outdated'
                    skill['message'] = 'New commits available'
                else:
                    skill['status'] = 'current'
                    skill['message'] = 'Up to date'

            except Exception as e:
                skill['status'] = 'error'
                skill['message'] = str(e)
                skill['remote_hash'] = ''

            results.append(skill)

    return results


def format_summary(results: list) -> str:
    """格式化摘要输出"""
    total = len(results)
    outdated = [s for s in results if s['status'] == 'outdated']
    current = [s for s in results if s['status'] == 'current']
    unmanaged = [s for s in results if s['status'] == 'unmanaged']
    errors = [s for s in results if s['status'] == 'error']

    lines = [
        f"Skills 状态摘要",
        f"=" * 40,
        f"总计: {total} 个 Skills",
        f"  - 最新: {len(current)}",
        f"  - 需更新: {len(outdated)}",
        f"  - 非托管: {len(unmanaged)}",
        f"  - 错误: {len(errors)}",
        "",
    ]

    if outdated:
        lines.append("需要更新的 Skills:")
        for s in outdated:
            lines.append(f"  - {s['name']}: {s['message']}")
            lines.append(f"    本地: {s['local_hash'][:8]}...")
            lines.append(f"    远程: {s['remote_hash'][:8]}...")
        lines.append("")

    if errors:
        lines.append("检查失败的 Skills:")
        for s in errors:
            lines.append(f"  - {s['name']}: {s['message']}")
        lines.append("")

    return '\n'.join(lines)


def format_table(results: list) -> str:
    """格式化表格输出"""
    lines = [
        f"{'Skill Name':<25} | {'Status':<10} | {'Version':<10} | {'Message':<30}",
        "-" * 80,
    ]

    for skill in sorted(results, key=lambda x: x['name']):
        name = skill['name'][:24]
        status = skill['status'][:9]
        version = (skill.get('version') or 'N/A')[:9]
        message = skill['message'][:29]
        lines.append(f"{name:<25} | {status:<10} | {version:<10} | {message:<30}")

    return '\n'.join(lines)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='扫描并检查 Skills 更新状态')
    parser.add_argument('skills_dir', help='Skills 目录路径')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--summary', action='store_true', help='输出摘要格式')
    parser.add_argument('--table', action='store_true', help='输出表格格式')
    parser.add_argument('--workers', type=int, default=5, help='并发检查数（默认: 5）')

    args = parser.parse_args()

    # 扫描 Skills
    skills = scan_skills(args.skills_dir)

    if not skills:
        print("未找到任何 Skills", file=sys.stderr)
        sys.exit(1)

    # 检查更新
    results = check_updates(skills, max_workers=args.workers)

    # 输出结果
    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False, cls=DateTimeEncoder))
    elif args.summary:
        print(format_summary(results))
    elif args.table:
        print(format_table(results))
    else:
        # 默认输出 JSON
        print(json.dumps(results, indent=2, ensure_ascii=False, cls=DateTimeEncoder))


if __name__ == "__main__":
    main()
