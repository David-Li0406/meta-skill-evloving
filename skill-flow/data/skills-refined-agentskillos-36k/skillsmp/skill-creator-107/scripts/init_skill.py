#!/usr/bin/env python3
"""
スキル初期化スクリプト - テンプレートから新しいスキルを作成

使用方法:
    python init_skill.py <skill-name> --path <path>

例:
    python init_skill.py lesson-plan --path .claude/skills
    python init_skill.py report-comment --path ~/.claude/skills
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: "[TODO: スキルの説明。トリガーキーワードを含める。例：〇〇を作成するスキル。指導案、授業計画、〇〇作成の時に使用。]"
user-invocable: true
argument-hint: "[引数のヒント]"
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

---

## リソース

このスキルには以下のリソースディレクトリが含まれています：

### scripts/
実行可能コード。決定論的な処理や繰り返し使うコードを配置。

### references/
詳細ドキュメント。必要に応じてコンテキストに読み込む。

### assets/
出力用ファイル。テンプレート、画像など（コンテキストには読み込まれない）。

---

**不要なディレクトリは削除してください。** すべてのスキルが3種類のリソースを必要とするわけではありません。
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_name} 用のヘルパースクリプト

このスクリプトは直接実行できます。
実際の実装に置き換えるか、不要な場合は削除してください。
"""

def main():
    print("{skill_name} のサンプルスクリプト")
    # TODO: 実際のスクリプトロジックを追加
    # データ処理、ファイル変換、API呼び出しなど

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# {skill_title} リファレンス

詳細なリファレンスドキュメントのプレースホルダー。
実際の内容に置き換えるか、不要な場合は削除してください。

## リファレンスドキュメントが有用な場合

- 包括的なAPIドキュメント
- 詳細なワークフローガイド
- 複雑な複数ステップのプロセス
- SKILL.mdには長すぎる情報
- 特定のユースケースでのみ必要なコンテンツ

## 構成例

### APIリファレンスの場合
- 概要
- 認証
- エンドポイントと例
- エラーコード
- レート制限

### ワークフローガイドの場合
- 前提条件
- ステップバイステップの手順
- 一般的なパターン
- トラブルシューティング
- ベストプラクティス
"""

EXAMPLE_ASSET = """# サンプルアセットファイル

このプレースホルダーはアセットファイルの配置場所を示します。
実際のアセットファイル（テンプレート、画像、フォントなど）に置き換えるか、
不要な場合は削除してください。

アセットファイルはコンテキストに読み込まれず、
Claudeが生成する出力で使用されます。

## 一般的なアセットタイプ

- テンプレート: .pptx, .docx, ボイラープレートディレクトリ
- 画像: .png, .jpg, .svg, .gif
- フォント: .ttf, .otf, .woff, .woff2
- ボイラープレートコード: プロジェクトディレクトリ、スターターファイル
- アイコン: .ico, .svg
- データファイル: .csv, .json, .xml, .yaml

注意: これはテキストプレースホルダーです。実際のアセットは任意のファイルタイプにできます。
"""


def title_case_skill_name(skill_name):
    """ハイフン区切りのスキル名をタイトルケースに変換"""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    """
    テンプレートSKILL.mdで新しいスキルディレクトリを初期化

    Args:
        skill_name: スキルの名前
        path: スキルディレクトリを作成するパス

    Returns:
        作成されたスキルディレクトリへのパス、またはエラー時はNone
    """
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

    # SKILL.mdを作成
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

    # リソースディレクトリを作成
    try:
        # scripts/
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name), encoding='utf-8')
        example_script.chmod(0o755)
        print("✅ scripts/example.py を作成")

        # references/
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title), encoding='utf-8')
        print("✅ references/reference.md を作成")

        # assets/
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET, encoding='utf-8')
        print("✅ assets/example_asset.txt を作成")
    except Exception as e:
        print(f"❌ リソースディレクトリ作成エラー: {e}")
        return None

    print(f"\n✅ スキル '{skill_name}' を {skill_dir} に初期化しました")
    print("\n次のステップ:")
    print("1. SKILL.md のTODO項目を編集し、descriptionを更新")
    print("2. scripts/, references/, assets/ のサンプルファイルをカスタマイズまたは削除")
    print("3. 準備ができたらバリデーターを実行してスキル構造を確認")

    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("使用方法: python init_skill.py <skill-name> --path <path>")
        print("\nスキル名の要件:")
        print("  - ハイフンケース識別子（例: 'data-analyzer'）")
        print("  - 小文字、数字、ハイフンのみ")
        print("  - 最大64文字")
        print("\n例:")
        print("  python init_skill.py lesson-plan --path .claude/skills")
        print("  python init_skill.py report-comment --path ~/.claude/skills")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"🚀 スキルを初期化: {skill_name}")
    print(f"   場所: {path}")
    print()

    result = init_skill(skill_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
