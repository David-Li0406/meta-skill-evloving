#!/usr/bin/env python3
"""
スキルパッケージャー - スキルフォルダを配布可能な.skillファイルに変換

使用方法:
    python package_skill.py <path/to/skill-folder> [output-directory]

例:
    python package_skill.py .claude/skills/my-skill
    python package_skill.py .claude/skills/my-skill ./dist
"""

import sys
import zipfile
from pathlib import Path
from quick_validate import validate_skill


def package_skill(skill_path, output_dir=None):
    """
    スキルフォルダを.skillファイルにパッケージング

    Args:
        skill_path: スキルフォルダへのパス
        output_dir: .skillファイルの出力ディレクトリ（オプション、デフォルトはカレントディレクトリ）

    Returns:
        作成された.skillファイルへのパス、またはエラー時はNone
    """
    skill_path = Path(skill_path).resolve()

    # スキルフォルダの存在確認
    if not skill_path.exists():
        print(f"❌ エラー: スキルフォルダが見つかりません: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ エラー: パスがディレクトリではありません: {skill_path}")
        return None

    # SKILL.mdの存在確認
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ エラー: {skill_path} にSKILL.mdが見つかりません")
        return None

    # パッケージング前にバリデーションを実行
    print("🔍 スキルを検証中...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ 検証失敗: {message}")
        print("   パッケージングの前に検証エラーを修正してください。")
        return None
    print(f"✅ {message}\n")

    # 出力場所の決定
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_filename = output_path / f"{skill_name}.skill"

    # .skillファイルの作成（zip形式）
    try:
        with zipfile.ZipFile(skill_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # スキルディレクトリを走査
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # zip内の相対パスを計算
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  追加: {arcname}")

        print(f"\n✅ スキルをパッケージングしました: {skill_filename}")
        return skill_filename

    except Exception as e:
        print(f"❌ .skillファイル作成エラー: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("使用方法: python package_skill.py <path/to/skill-folder> [output-directory]")
        print("\n例:")
        print("  python package_skill.py .claude/skills/my-skill")
        print("  python package_skill.py .claude/skills/my-skill ./dist")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📦 スキルをパッケージング: {skill_path}")
    if output_dir:
        print(f"   出力ディレクトリ: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
