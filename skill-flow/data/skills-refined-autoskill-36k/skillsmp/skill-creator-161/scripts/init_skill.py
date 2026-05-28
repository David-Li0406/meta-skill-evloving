#!/usr/bin/env python3
"""
Skill 初始化器 - 從範本建立新 skill

用法：
    init_skill.py <skill-name> --path <path>

範例：
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private
    init_skill.py custom-skill --path /custom/location
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: [待辦：完整且詳盡地說明此 skill 的功能及使用時機。包含何時使用此 skill——觸發它的特定情境、檔案類型或任務。]
---

# {skill_title}

## 概述

[待辦：1-2 句話說明此 skill 能做什麼]

## 建構此 Skill

[待辦：選擇最適合此 skill 用途的結構。常見模式：

**1. 工作流程導向**（最適合順序流程）
- 當有明確的逐步程序時效果最好
- 範例：DOCX skill 使用「工作流程決策樹」→「讀取」→「建立」→「編輯」
- 結構：## 概述 → ## 工作流程決策樹 → ## 步驟 1 → ## 步驟 2...

**2. 任務導向**（最適合工具集合）
- 當 skill 提供不同的操作/功能時效果最好
- 範例：PDF skill 使用「快速入門」→「合併 PDF」→「分割 PDF」→「擷取文字」
- 結構：## 概述 → ## 快速入門 → ## 任務類別 1 → ## 任務類別 2...

**3. 參考/指南**（最適合標準或規格）
- 適用於品牌指南、程式碼標準或需求
- 範例：品牌風格使用「品牌指南」→「顏色」→「排版」→「功能」
- 結構：## 概述 → ## 指南 → ## 規格 → ## 使用方式...

**4. 功能導向**（最適合整合系統）
- 當 skill 提供多個相互關聯的功能時效果最好
- 範例：產品管理使用「核心功能」→ 編號功能列表
- 結構：## 概述 → ## 核心功能 → ### 1. 功能 → ### 2. 功能...

模式可以根據需要混合搭配。大多數 skills 會組合模式（例如從任務導向開始，為複雜操作新增工作流程）。

完成後刪除整個「建構此 Skill」區段——這只是指導。]

## [待辦：根據選擇的結構替換為第一個主要區段]

[待辦：在此新增內容。參見現有 skills 的範例：
- 技術 skills 的程式碼範例
- 複雜工作流程的決策樹
- 包含實際使用者請求的具體範例
- 根據需要參考腳本/範本/參考資料]

## 資源

此 skill 包含範例資源目錄，展示如何組織不同類型的附帶資源：

### scripts/
可直接執行以執行特定操作的可執行程式碼（Python/Bash 等）。

**其他 skills 的範例：**
- PDF skill：`fill_fillable_fields.py`、`extract_form_field_info.py` - PDF 操作工具
- DOCX skill：`document.py`、`utilities.py` - 文件處理的 Python 模組

**適用於：** Python 腳本、shell 腳本，或任何執行自動化、資料處理或特定操作的可執行程式碼。

**注意：** 腳本可以在不載入上下文的情況下執行，但 Claude 仍可能讀取它們以進行修補或環境調整。

### references/
文件和參考資料，用於載入上下文以告知 Claude 的處理和思考過程。

**其他 skills 的範例：**
- 產品管理：`communication.md`、`context_building.md` - 詳細的工作流程指南
- BigQuery：API 參考文件和查詢範例
- 財務：架構文件、公司政策

**適用於：** 深入的文件、API 參考、資料庫架構、全面的指南，或 Claude 在工作時應參考的任何詳細資訊。

### assets/
不打算載入上下文，而是用於 Claude 產生的輸出中的檔案。

**其他 skills 的範例：**
- 品牌風格：PowerPoint 範本檔案（.pptx）、標誌檔案
- 前端建構器：HTML/React 樣板專案目錄
- 排版：字型檔案（.ttf、.woff2）

**適用於：** 範本、樣板程式碼、文件範本、圖片、圖示、字型，或任何要複製或用於最終輸出的檔案。

---

**任何不需要的目錄都可以刪除。** 並非每個 skill 都需要所有三種類型的資源。
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_name} 的範例輔助腳本

這是一個可以直接執行的佔位腳本。
根據實際需求替換實作或刪除（如不需要）。

其他 skills 的真實腳本範例：
- pdf/scripts/fill_fillable_fields.py - 填寫 PDF 表單欄位
- pdf/scripts/convert_pdf_to_images.py - 將 PDF 頁面轉換為圖片
"""

def main():
    print("這是 {skill_name} 的範例腳本")
    # 待辦：在此新增實際腳本邏輯
    # 這可以是資料處理、檔案轉換、API 呼叫等

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# {skill_title} 的參考文件

這是詳細參考文件的佔位符。
根據實際需求替換內容或刪除（如不需要）。

其他 skills 的真實參考文件範例：
- product-management/references/communication.md - 狀態更新的全面指南
- product-management/references/context_building.md - 蒐集上下文的深入說明
- bigquery/references/ - API 參考和查詢範例

## 何時參考文件有用

參考文件適用於：
- 全面的 API 文件
- 詳細的工作流程指南
- 複雜的多步驟流程
- 對於主要 SKILL.md 來說太長的資訊
- 僅在特定使用案例需要的內容

## 結構建議

### API 參考範例
- 概述
- 認證
- 帶範例的端點
- 錯誤代碼
- 速率限制

### 工作流程指南範例
- 先決條件
- 逐步說明
- 常見模式
- 疑難排解
- 最佳實踐
"""

EXAMPLE_ASSET = """# 範例素材檔案

此佔位符代表素材檔案的儲存位置。
根據實際需求替換為實際素材檔案（範本、圖片、字型等）或刪除（如不需要）。

素材檔案不打算載入上下文，而是用於
Claude 產生的輸出中。

其他 skills 的素材檔案範例：
- 品牌指南：logo.png、slides_template.pptx
- 前端建構器：hello-world/ 目錄包含 HTML/React 樣板
- 排版：custom-font.ttf、font-family.woff2
- 資料：sample_data.csv、test_dataset.json

## 常見素材類型

- 範本：.pptx、.docx、樣板目錄
- 圖片：.png、.jpg、.svg、.gif
- 字型：.ttf、.otf、.woff、.woff2
- 樣板程式碼：專案目錄、入門檔案
- 圖示：.ico、.svg
- 資料檔案：.csv、.json、.xml、.yaml

注意：這是文字佔位符。實際素材可以是任何檔案類型。
"""


def title_case_skill_name(skill_name):
    """將連字號分隔的 skill 名稱轉換為首字母大寫以供顯示。"""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def init_skill(skill_name, path):
    """
    使用範本 SKILL.md 初始化新的 skill 目錄。

    參數：
        skill_name: Skill 的名稱
        path: 應建立 skill 目錄的路徑

    回傳：
        建立的 skill 目錄路徑，如果發生錯誤則為 None
    """
    # 確定 skill 目錄路徑
    skill_dir = Path(path).resolve() / skill_name

    # 檢查目錄是否已存在
    if skill_dir.exists():
        print(f"❌ 錯誤：Skill 目錄已存在：{skill_dir}")
        return None

    # 建立 skill 目錄
    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"✅ 已建立 skill 目錄：{skill_dir}")
    except Exception as e:
        print(f"❌ 建立目錄時發生錯誤：{e}")
        return None

    # 從範本建立 SKILL.md
    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("✅ 已建立 SKILL.md")
    except Exception as e:
        print(f"❌ 建立 SKILL.md 時發生錯誤：{e}")
        return None

    # 建立包含範例檔案的資源目錄
    try:
        # 建立 scripts/ 目錄及範例腳本
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        example_script.chmod(0o755)
        print("✅ 已建立 scripts/example.py")

        # 建立 references/ 目錄及範例參考文件
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("✅ 已建立 references/api_reference.md")

        # 建立 assets/ 目錄及範例素材佔位符
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET)
        print("✅ 已建立 assets/example_asset.txt")
    except Exception as e:
        print(f"❌ 建立資源目錄時發生錯誤：{e}")
        return None

    # 輸出下一步
    print(f"\n✅ Skill '{skill_name}' 已成功初始化於 {skill_dir}")
    print("\n下一步：")
    print("1. 編輯 SKILL.md 以完成待辦項目並更新描述")
    print("2. 自訂或刪除 scripts/、references/ 和 assets/ 中的範例檔案")
    print("3. 準備好後執行驗證器以檢查 skill 結構")

    return skill_dir


def main():
    if len(sys.argv) < 4 or sys.argv[2] != '--path':
        print("用法：init_skill.py <skill-name> --path <path>")
        print("\nSkill 名稱要求：")
        print("  - 連字號分隔的識別碼（例如 'data-analyzer'）")
        print("  - 僅限小寫字母、數字和連字號")
        print("  - 最多 40 個字元")
        print("  - 必須與目錄名稱完全相符")
        print("\n範例：")
        print("  init_skill.py my-new-skill --path skills/public")
        print("  init_skill.py my-api-helper --path skills/private")
        print("  init_skill.py custom-skill --path /custom/location")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = sys.argv[3]

    print(f"🚀 正在初始化 skill：{skill_name}")
    print(f"   位置：{path}")
    print()

    result = init_skill(skill_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
