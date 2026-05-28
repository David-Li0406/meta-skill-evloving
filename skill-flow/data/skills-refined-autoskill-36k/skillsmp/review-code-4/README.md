Markdown

# 🚀 Claude Code: review-code Skill

這是一個為 Claude Code 量身打造的高級代碼審查技能。它結合了 **Clean Code 原則** 與 **專案架構分析**，支援 Python, JavaScript/TypeScript 與 Java。

## 🌟 核心功能

- **Clean Code 診斷**：自動檢查變數命名、函式長度（限制 20-25 行）及冗餘註釋。
- **專案級掃描**：自動識別專案類型（如 Web 形象站、Python 工具），並進行跨檔案邏輯審查。
- **雙模式支持**：
  - **單檔模式**：針對目前開啟的檔案進行精準修復建議。
  - **路徑模式**：掃描指定目錄，產出整合性的品質報告。
- **智能排除**：自動忽略 `node_modules`, `.git`, `__pycache__` 等無關目錄。

## 📂 檔案結構關連

此技能由以下兩部分組成，必須成對安裝：
- `review-code.skill`: 系統指令入口檔。
- `review-code/`: 包含 `SKILL.md` (規則定義) 與參考文件的核心目錄。

## 🛠️ 使用說明

在 Claude Code 終端機中，您可以使用以下指令：

### 1. 審查當前代碼
```bash
/review-code
2. 審查特定專案目錄
Bash

/review-code ./your-project-path
📏 審查標準 (SOP)
本技能嚴格遵循以下規範：

命名：禁止單字母變數（i, j, k 除外）與模糊命名（如 tmp, data）。

長度：Python/JS 函式 > 20 行即標註為需重構。

註釋：移除「解釋程式碼在做什麼」的冗餘註釋，僅保留「解釋為什麼這樣做」的註釋。