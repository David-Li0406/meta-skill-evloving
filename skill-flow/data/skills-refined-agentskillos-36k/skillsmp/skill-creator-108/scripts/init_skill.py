#!/usr/bin/env python3
"""
スキル初期化スクリプト - テンプレートから新しいスキルを作成（Antigravity用）

使用方法:
    python init_skill.py <skill-name> --path <path>

例:
    python init_skill.py lesson-plan --path .agent/skills
    python init_skill.py report-comment --path ~/.gemini/antigravity/skills
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: |
  [TODO: スキルの説明]
  Use when: [TODO: トリガーキーワード1, キーワード2, キーワード3]
  Do not use when: [TODO: 除外条件1, 除外条件2]
---

# {skill_title}

[TODO: 1-2文でこのスキルが何を可能にするか説明]

## このスキルを使用する時

- [TODO: 使用条件1]
- [TODO: 使用条件2]

## このスキルを使用しない時

- [TODO: 除外条件1]
- [TODO: 除外条件2]

---

## 対応タスク

1. [TODO: タスク1]
2. [TODO: タスク2]

---

## ワークフロー

[TODO: 具体的な手順を記載]

### Step 1: [ステップ名]

[内容]

### Step 2: [ステップ名]

[内容]

---

## ヒアリング項目

実装前に確認：

1. [TODO: 確認事項1]
2. [TODO: 確認事項2]

---

## 出力形式

[TODO: どのような形式で出力するか]
"""


def title_case_skill_name(skill_name):
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    skill_dir = Path(path).resolve() / skill_name

    if skill_dir.exists():
        print(f"❌ エラー: スキルディレクトリが既に存在します: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ スキルディレクトリを作成: {skill_dir}")
    except Exception as e:
        print(f"❌ ディレクトリ作成エラー: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content, encoding='utf-8')
        print("✅ SKILL.md を作成")
    except Exception as e:
        print(f"❌ SKILL.md作成エラー: {e}")
        return None

    print(f"\n✅ スキル '{skill_name}' を {skill_dir} に初期化しました")
    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("使用方法: python init_skill.py <skill-name> --path <path>")
        print("\n例:")
        print("  python init_skill.py lesson-plan --path .agent/skills")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"🚀 スキルを初期化: {skill_name}")
    print(f"   場所: {path}")
    print()

    result = init_skill(skill_name, path)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
