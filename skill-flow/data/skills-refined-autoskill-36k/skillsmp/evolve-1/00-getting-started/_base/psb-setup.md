# PSB 環境準備

> **P**lan → **S**etup → **B**uild：在寫第一行程式碼前，先確保環境就緒

## PSB 檢查清單

### Plan（規劃）
- [ ] **1. 目標明確性**：成功標準、範圍限定、驗收條件可量化

### Setup（環境）
- [ ] **2. Git Repo 已建立**：`git init` / `git clone` + `.gitignore`
- [ ] **3. CLAUDE.md 已配置**：專案規範、技術棧、約定
- [ ] **4. 記憶系統已初始化**：`.claude/memory/` + `index.md`
- [ ] **5. 自動化文件**（可選）：架構文件、變更日誌
- [ ] **6. MCP 連接**（可選）：context7、PAL
- [ ] **7. Slash Commands**（可選）：/evolve 等觸發詞
- [ ] **8. 權限配置**（推薦）：`/permissions` 精細管理

### Build（執行）
✓ 環境就緒，開始執行任務

## 快速檢查指令

```bash
# 檢查 Git
git status

# 檢查 CLAUDE.md
ls CLAUDE.md 2>/dev/null || echo "⚠️ 建議建立 CLAUDE.md"

# 檢查記憶系統
ls .claude/memory/ 2>/dev/null || echo "⚠️ 需要初始化記憶系統"
```

## 最小可行環境

若要快速開始，至少確保：

| 必要 | 項目 | 說明 |
|------|------|------|
| ✅ | Git Repo | 版本控制 |
| ✅ | `.claude/memory/` | 記憶儲存 |
| 建議 | `CLAUDE.md` | 專案約束 |
| 可選 | MCP 配置 | 擴展能力 |
| 可選 | 權限配置 | 減少中斷 |

## 權限配置指南（Boris Tip #6）

> 精細權限管理，預先允許安全常用命令，避免 `--dangerously-skip-permissions`

### 為什麼重要

| 方式 | 風險 | 體驗 |
|------|------|------|
| 預設（每次詢問） | ✅ 最安全 | ⚠️ 頻繁中斷 |
| `/permissions` 配置 | ✅ 可控風險 | ✅ 流暢體驗 |
| `--dangerously-skip-permissions` | ❌ 高風險 | ✅ 無中斷 |

**推薦使用 `/permissions`**：在安全和體驗之間取得平衡。

### 配置方式

**方式 1：使用 `/permissions` 命令**

```bash
# 在 Claude Code 中執行
/permissions

# 會顯示互動式介面，可以：
# - 允許特定命令模式
# - 拒絕危險操作
# - 檢視當前設定
```

**方式 2：編輯設定檔**

```json
// .claude/settings.local.json
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(npm test*)",
      "Bash(git status)",
      "Bash(git diff*)",
      "Bash(git log*)",
      "Bash(make *)",
      "Read(*)",
      "Glob(*)",
      "Grep(*)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(git push --force*)",
      "Bash(sudo *)"
    ]
  }
}
```

### 推薦的安全允許清單

| 類別 | 允許模式 | 說明 |
|------|----------|------|
| **讀取操作** | `Read(*)`, `Glob(*)`, `Grep(*)` | 無副作用，安全 |
| **Git 查詢** | `git status`, `git diff*`, `git log*` | 只讀操作 |
| **建置測試** | `npm run *`, `npm test*`, `make *` | 開發必需 |
| **專案腳本** | `./scripts/*` | 自訂安全腳本 |

### 建議禁止的操作

| 類別 | 禁止模式 | 原因 |
|------|----------|------|
| **破壞性刪除** | `rm -rf *` | 可能誤刪重要檔案 |
| **強制推送** | `git push --force*` | 可能覆蓋團隊工作 |
| **系統權限** | `sudo *` | 系統級風險 |
| **環境變數** | `export *` | 可能洩露敏感資訊 |

### 何時用什麼

| 情境 | 建議 |
|------|------|
| 日常開發 | 使用 `/permissions` 配置 |
| 敏感專案 | 維持預設（每次確認） |
| 自動化腳本 | 使用 sandbox 模式 |
| 快速探索 | 可考慮 `--permission-mode=dontAsk` |

> **Boris Tip**: 「精細權限管理 > `--dangerously-skip-permissions`」
