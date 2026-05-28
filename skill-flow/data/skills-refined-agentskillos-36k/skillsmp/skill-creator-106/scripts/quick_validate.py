#!/usr/bin/env python3
"""
スキル検証スクリプト（Antigravity用）

使用方法:
    python quick_validate.py <skill_directory>
"""

import sys
import re
import yaml
from pathlib import Path


def validate_skill(skill_path):
    skill_path = Path(skill_path)

    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md が見つかりません"

    content = skill_md.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return False, "YAMLフロントマターが見つかりません"

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "フロントマターの形式が無効です"

    try:
        frontmatter = yaml.safe_load(match.group(1))
        if not isinstance(frontmatter, dict):
            return False, "フロントマターはYAML辞書である必要があります"
    except yaml.YAMLError as e:
        return False, f"フロントマターのYAMLが無効です: {e}"

    if 'name' not in frontmatter:
        return False, "フロントマターに 'name' がありません"
    if 'description' not in frontmatter:
        return False, "フロントマターに 'description' がありません"

    name = frontmatter.get('name', '').strip()
    if name and not re.match(r'^[a-z0-9-]+$', name):
        return False, f"名前 '{name}' はハイフンケースである必要があります"

    if '[TODO:' in content:
        return False, "SKILL.mdにまだ [TODO:] 項目が残っています"

    return True, "✅ スキルは有効です！"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
