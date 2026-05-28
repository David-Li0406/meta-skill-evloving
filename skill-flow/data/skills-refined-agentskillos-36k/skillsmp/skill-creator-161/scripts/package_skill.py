#!/usr/bin/env python3
"""
Skill 打包器 - 將 skill 資料夾建立為可分發的 zip 檔案

用法：
    python utils/package_skill.py <path/to/skill-folder> [output-directory]

範例：
    python utils/package_skill.py skills/public/my-skill
    python utils/package_skill.py skills/public/my-skill ./dist
"""

import sys
import zipfile
from pathlib import Path
from quick_validate import validate_skill


def package_skill(skill_path, output_dir=None):
    """
    將 skill 資料夾打包成 zip 檔案。

    參數：
        skill_path: skill 資料夾的路徑
        output_dir: zip 檔案的選用輸出目錄（預設為當前目錄）

    回傳：
        建立的 zip 檔案路徑，如果發生錯誤則為 None
    """
    skill_path = Path(skill_path).resolve()

    # 驗證 skill 資料夾存在
    if not skill_path.exists():
        print(f"❌ 錯誤：找不到 skill 資料夾：{skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ 錯誤：路徑不是目錄：{skill_path}")
        return None

    # 驗證 SKILL.md 存在
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ 錯誤：在 {skill_path} 中找不到 SKILL.md")
        return None

    # 打包前執行驗證
    print("🔍 正在驗證 skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ 驗證失敗：{message}")
        print("   請在打包前修復驗證錯誤。")
        return None
    print(f"✅ {message}\n")

    # 確定輸出位置
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    zip_filename = output_path / f"{skill_name}.zip"

    # 建立 zip 檔案
    try:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 遍歷 skill 目錄
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # 計算 zip 中的相對路徑
                    arcname = file_path.relative_to(skill_path.parent)
                    zipf.write(file_path, arcname)
                    print(f"  已新增：{arcname}")

        print(f"\n✅ 已成功將 skill 打包至：{zip_filename}")
        return zip_filename

    except Exception as e:
        print(f"❌ 建立 zip 檔案時發生錯誤：{e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("用法：python utils/package_skill.py <path/to/skill-folder> [output-directory]")
        print("\n範例：")
        print("  python utils/package_skill.py skills/public/my-skill")
        print("  python utils/package_skill.py skills/public/my-skill ./dist")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📦 正在打包 skill：{skill_path}")
    if output_dir:
        print(f"   輸出目錄：{output_dir}")
    print()

    result = package_skill(skill_path, output_dir)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
