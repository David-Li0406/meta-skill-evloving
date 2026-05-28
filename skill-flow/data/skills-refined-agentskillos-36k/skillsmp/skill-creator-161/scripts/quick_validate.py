#!/usr/bin/env python3
"""
Skills 快速驗證腳本 - 精簡版本
"""

import sys
import os
import re
from pathlib import Path

def validate_skill(skill_path):
    """基本的 skill 驗證"""
    skill_path = Path(skill_path)

    # 檢查 SKILL.md 是否存在
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "找不到 SKILL.md"

    # 讀取並驗證前置資料
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "找不到 YAML 前置資料"

    # 擷取前置資料
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "前置資料格式無效"

    frontmatter = match.group(1)

    # 檢查必要欄位
    if 'name:' not in frontmatter:
        return False, "前置資料中缺少 'name'"
    if 'description:' not in frontmatter:
        return False, "前置資料中缺少 'description'"

    # 擷取名稱以進行驗證
    name_match = re.search(r'name:\s*(.+)', frontmatter)
    if name_match:
        name = name_match.group(1).strip()
        # 檢查命名慣例（連字號分隔：小寫加連字號）
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"名稱 '{name}' 應為連字號分隔格式（僅限小寫字母、數字和連字號）"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"名稱 '{name}' 不能以連字號開頭/結尾或包含連續連字號"

    # 擷取並驗證描述
    desc_match = re.search(r'description:\s*(.+)', frontmatter)
    if desc_match:
        description = desc_match.group(1).strip()
        # 檢查角括號
        if '<' in description or '>' in description:
            return False, "描述不能包含角括號（< 或 >）"

    return True, "Skill 驗證通過！"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法：python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
