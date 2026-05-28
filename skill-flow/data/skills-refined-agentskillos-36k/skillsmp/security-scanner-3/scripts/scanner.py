#!/usr/bin/env python3
"""Skill 安全扫描器主程序

用于扫描 Claude Code 自定义 skills 中的潜在恶意代码。
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import importlib.util

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from detectors import (
    DangerousCallsDetector,
    NetworkOpsDetector,
    FileOpsDetector,
    ObfuscationDetector,
    DataExfilDetector,
)
from report import ReportGenerator


class SkillScanner:
    """Skill 扫描器"""

    def __init__(self, skills_dir: str = None):
        self.skills_dir = Path(skills_dir or os.path.expanduser('~/.claude/skills'))
        self.results: List[Dict[str, Any]] = []

    def scan_all(self) -> List[Dict[str, Any]]:
        """扫描所有 skills"""
        if not self.skills_dir.exists():
            print(f'错误: Skills 目录不存在: {self.skills_dir}')
            return []

        skill_dirs = [d for d in self.skills_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
        results = []

        for skill_dir in skill_dirs:
            result = self.scan_skill(skill_dir)
            if result:
                results.append(result)

        return sorted(results, key=self._severity_sort_key)

    def scan_skill(self, skill_dir: Path) -> Optional[Dict[str, Any]]:
        """扫描单个 skill"""
        skill_name = skill_dir.name
        scripts_dir = skill_dir / 'scripts'

        if not scripts_dir.exists():
            return {
                'skill': skill_name,
                'description': self._get_skill_description(skill_dir),
                'findings': [],
            }

        # 查找所有 Python 文件
        py_files = list(scripts_dir.rglob('*.py'))
        all_findings = []

        for py_file in py_files:
            findings = self._scan_file(py_file, skill_name)
            all_findings.extend(findings)

        return {
            'skill': skill_name,
            'description': self._get_skill_description(skill_dir),
            'findings': sorted(all_findings, key=self._severity_sort_key),
        }

    def _scan_file(self, py_file: Path, skill_name: str) -> List[Dict[str, Any]]:
        """扫描单个 Python 文件"""
        try:
            source_code = py_file.read_text(encoding='utf-8')
        except Exception:
            return []

        relative_path = py_file.relative_to(py_file.parents[2])  # skill/scripts/file.py
        findings = []

        # 运行所有检测器
        detectors = [
            DangerousCallsDetector(source_code, str(relative_path)),
            NetworkOpsDetector(source_code, str(relative_path)),
            FileOpsDetector(source_code, str(relative_path)),
            ObfuscationDetector(source_code, str(relative_path)),
            DataExfilDetector(source_code, str(relative_path)),
        ]

        for detector in detectors:
            detector_findings = detector.detect()
            for finding in detector_findings:
                findings.append(finding.to_dict())

        return findings

    def _get_skill_description(self, skill_dir: Path) -> str:
        """从 SKILL.md 获取描述"""
        skill_md = skill_dir / 'SKILL.md'
        if skill_md.exists():
            try:
                content = skill_md.read_text(encoding='utf-8')
                # 提取 YAML front matter 中的 description
                if content.startswith('---'):
                    end = content.find('---', 3)
                    if end > 0:
                        yaml_part = content[3:end]
                        for line in yaml_part.split('\n'):
                            if line.strip().startswith('description:'):
                                desc = line.split(':', 1)[1].strip()
                                # 去掉引号
                                desc = desc.strip('"\'')
                                return desc[:50] + '...' if len(desc) > 50 else desc
            except Exception:
                pass
        return '未知功能'

    def _severity_sort_key(self, item):
        """按严重程度排序的键函数"""
        severity_order = {'严重': 0, '高': 1, '中': 2, '低': 3}
        if isinstance(item, dict):
            severity = item.get('severity', '低')
        else:
            severity = item.severity if hasattr(item, 'severity') else '低'
        return severity_order.get(severity, 4)


def main():
    parser = argparse.ArgumentParser(description='Claude Code Skill 安全扫描器')
    parser.add_argument(
        '--skill',
        type=str,
        help='指定要扫描的 skill 名称（默认扫描所有）',
    )
    parser.add_argument(
        '--skills-dir',
        type=str,
        default=os.path.expanduser('~/.claude/skills'),
        help='Skills 目录路径',
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='禁用彩色输出',
    )

    args = parser.parse_args()

    scanner = SkillScanner(args.skills_dir)

    if args.skill:
        # 扫描单个 skill
        skill_path = Path(args.skills_dir) / args.skill
        if not skill_path.exists():
            print(f'错误: Skill 不存在: {skill_path}')
            sys.exit(1)
        results = [scanner.scan_skill(skill_path)] if scanner.scan_skill(skill_path) else []
    else:
        # 扫描所有 skills
        results = scanner.scan_all()

    # 生成报告
    reporter = ReportGenerator(use_color=not args.no_color)
    reporter.print_results(results)

    # 根据结果设置退出码
    has_high_risk = any(
        f.get('severity') in ['严重', '高']
        for r in results
        for f in r.get('findings', [])
    )

    if has_high_risk:
        sys.exit(1)


if __name__ == '__main__':
    main()
