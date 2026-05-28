#!/usr/bin/env python3
"""
スキル検証スクリプト - 最小バージョン

使用方法:
    python quick_validate.py <skill_directory>
"""

import sys
import re
import yaml
from pathlib import Path


def validate_skill(skill_path):
    """スキルの基本的な検証を行う"""
    skill_path = Path(skill_path)

    # SKILL.mdの存在確認
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return False, "SKILL.md が見つかりません"

    # フロントマターの読み込みと検証
    content = skill_md.read_text(encoding='utf-8')
    if not content.startswith('---'):
        return False, "YAMLフロントマターが見つかりません"

    # フロントマターを抽出
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return False, "フロントマターの形式が無効です"

    frontmatter_text = match.group(1)

    # YAMLフロントマターをパース
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        if not isinstance(frontmatter, dict):
            return False, "フロントマターはYAML辞書である必要があります"
    except yaml.YAMLError as e:
        return False, f"フロントマターのYAMLが無効です: {e}"

    # 許可されているプロパティ
    ALLOWED_PROPERTIES = {
        'name', 'description', 'license', 'allowed-tools', 'metadata',
        'user-invocable', 'argument-hint'  # Claude Code固有
    }

    # 予期しないプロパティのチェック
    unexpected_keys = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected_keys:
        return False, (
            f"SKILL.mdフロントマターに予期しないキーがあります: {', '.join(sorted(unexpected_keys))}。 "
            f"許可されているプロパティ: {', '.join(sorted(ALLOWED_PROPERTIES))}"
        )

    # 必須フィールドのチェック
    if 'name' not in frontmatter:
        return False, "フロントマターに 'name' がありません"
    if 'description' not in frontmatter:
        return False, "フロントマターに 'description' がありません"

    # 名前の検証
    name = frontmatter.get('name', '')
    if not isinstance(name, str):
        return False, f"nameは文字列である必要があります。取得した型: {type(name).__name__}"
    name = name.strip()
    if name:
        # 命名規則のチェック（ハイフンケース）
        if not re.match(r'^[a-z0-9-]+$', name):
            return False, f"名前 '{name}' はハイフンケース（小文字、数字、ハイフンのみ）である必要があります"
        if name.startswith('-') or name.endswith('-') or '--' in name:
            return False, f"名前 '{name}' はハイフンで開始/終了できず、連続するハイフンを含むことができません"
        # 名前の長さチェック（最大64文字）
        if len(name) > 64:
            return False, f"名前が長すぎます（{len(name)}文字）。最大は64文字です。"

    # 説明の検証
    description = frontmatter.get('description', '')
    if not isinstance(description, str):
        return False, f"descriptionは文字列である必要があります。取得した型: {type(description).__name__}"
    description = description.strip()
    if description:
        # 角括弧のチェック
        if '<' in description or '>' in description:
            return False, "descriptionに角括弧（< または >）を含めることはできません"
        # 説明の長さチェック（最大1024文字）
        if len(description) > 1024:
            return False, f"descriptionが長すぎます（{len(description)}文字）。最大は1024文字です。"

    # TODOが残っていないかチェック
    if '[TODO:' in content:
        return False, "SKILL.mdにまだ [TODO:] 項目が残っています。すべて完了してください。"

    return True, "✅ スキルは有効です！"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python quick_validate.py <skill_directory>")
        sys.exit(1)

    valid, message = validate_skill(sys.argv[1])
    print(message)
    sys.exit(0 if valid else 1)
