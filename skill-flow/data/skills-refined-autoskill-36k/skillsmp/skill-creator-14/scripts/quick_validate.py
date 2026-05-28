#!/usr/bin/env python3
"""
技能快速验证脚本 - 极简版本
"""

import sys
import os
import re
import yaml
from pathlib import Path

def validate_skill(skill_path):
    """Basic validation of a skill"""
    skill_path = Path(skill_path)

    # Check SKILL.md exists
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "未找到 SKILL.md"

    # Read and validate frontmatter
    content = skill_md.read_text()
    if not content.startswith('---'):
        return False, "未找到 YAML 前置配置 (frontmatter)"

    # Extract frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "前置配置 (frontmatter) 格式无效"

    frontmatter_text = match.group(1)

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "前置配置 (frontmatter) 必须是 YAML 字典"
    except yaml.YAMLError as e:
        return False, f"前置配置 (frontmatter) 中的 YAML 无效: {e}"

    # Define allowed properties
    ALLOWED_PROPERTIES = {'name', 'description', 'license', 'allowed-tools', 'metadata'}

    # Check for unexpected properties (excluding nested keys under metadata)
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"SKILL.md 前置配置中包含未预期的键: {', '.join(sorted(unexpected_keys))}。"
            f"允许的属性为: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # Check required fields
    if 'name' not in frontmatter:
        return False, "前置配置中缺少 'name' 字段"
    if 'description' not in frontmatter:
        return False, "前置配置中缺少 'description' 字段"

    # Extract name for validation
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"Name 必须是字符串，实际得到的是 {type(name).__name__}"
    name = name.strip()
    if name:
        # Check naming convention (hyphen-case: lowercase with hyphens)
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"名称 '{name}' 应采用连字符格式（仅限小写字母、数字和连字符）"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"名称 '{name}' 不能以连字符开头/结尾，也不能包含连续的连字符"
        # Check name length (max 64 characters per spec)
        if len(name) > 64:
            return False, f"名称过长（{len(name)} 个字符）。最大长度为 64 个字符。"

    # Extract and validate description
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"Description 必须是字符串，实际得到的是 {type(description).__name__}"
    description = description.strip()
    if description:
        # Check for angle brackets
        if '<' in description or '>' in description:
            return False, "Description 不能包含尖括号 (< 或 >)"
        # Check description length (max 1024 characters per spec)
        if len(description) > 1024:
            return False, f"Description 过长（{len(description)} 个字符）。最大长度为 1024 个字符。"

    return True, "技能有效！"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python quick_validate.py <skill_directory>")
        sys.exit(1)
    
    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)