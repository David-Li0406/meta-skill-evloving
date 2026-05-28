---
name: auto-commit
description: 自動分析變更、生成 commit 訊息並提交。當使用者說「提交」、「commit」或要求提交變更時使用。
---

# 自動提交

分析 git 變更，自動生成符合 Conventional Commits 規範的提交訊息，並執行提交。

## 何時使用此 Skill

- 使用者說「提交」、「commit」、「幫我提交」
- 使用者完成一個功能或修復後要求提交
- 使用者要求自動命名提交訊息

## 流程

### 步驟 1：檢查變更狀態

執行以下命令了解變更內容：

```bash
git status
git diff --staged
git diff
```

### 步驟 2：分析變更並決定提交策略

#### 2.1 判斷是否需要分類提交

根據以下條件決定：

| 情境 | 策略 | 說明 |
|------|------|------|
| 單一功能/修復 | 單次提交 | 所有變更都為同一目的服務 |
| 多個獨立功能 | 分類提交 | 變更可明確分為不相關的群組 |
| 混合變更（功能 + 修復 + 文件） | 分類提交 | 不同類型應分開提交 |
| 同一功能的多檔案變更 | 單次提交 | 雖跨多檔案但邏輯相關 |

#### 2.2 分類提交的判斷標準

**需要分類提交**（符合任一條件）：
- 變更涉及 2 種以上不同的 commit type（如 feat + fix + docs）
- 變更涉及完全不相關的功能模組
- 變更包含獨立的 chore/config 更新

**單次提交即可**（符合以下條件）：
- 所有變更都是為了完成同一個功能或修復
- 變更雖跨多檔案但邏輯緊密相關
- 變更都屬於同一個 commit type

### 步驟 3：分析變更類型

根據變更內容判斷類型：

| 類型 | 使用時機 |
|------|---------|
| `feat` | 新功能 |
| `fix` | 錯誤修復 |
| `docs` | 文件變更 |
| `style` | 格式調整（不影響程式邏輯） |
| `refactor` | 重構（不新增功能也不修復錯誤） |
| `perf` | 效能優化 |
| `test` | 新增或修改測試 |
| `chore` | 建置流程或輔助工具變更 |

### 步驟 4：向使用者呈現提交方案

#### 4.1 單次提交方案

```
📦 提交方案：單次提交

所有變更邏輯相關，建議合併為一次提交：

  <type>: <描述>

  涉及檔案：
  - file1.ts
  - file2.tsx
  - ...
```

#### 4.2 分類提交方案

```
📦 提交方案：分類提交（共 N 次）

變更可分為以下獨立群組：

[1] <type>: <描述>
    涉及檔案：
    - file1.ts
    - file2.tsx

[2] <type>: <描述>
    涉及檔案：
    - file3.ts

[3] <type>: <描述>
    涉及檔案：
    - README.md
```

#### 4.3 詢問使用者確認

呈現方案後，詢問使用者：
- 「確認此方案？」→ 執行提交
- 「合併為單次提交」→ 改用單次提交
- 「調整分類」→ 讓使用者指定

### 步驟 5：執行提交

#### 單次提交

```bash
git add -A
git commit -m "$(cat <<'EOF'
<type>: <描述>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

#### 分類提交（依序執行）

```bash
# 第 1 次提交
git add <file1> <file2>
git commit -m "$(cat <<'EOF'
<type1>: <描述1>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# 第 2 次提交
git add <file3>
git commit -m "$(cat <<'EOF'
<type2>: <描述2>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"

# ... 依此類推
```

### 步驟 6：確認結果

```bash
git log --oneline -n <提交次數>
git status
```

## 範例

### 範例 1：單次提交 - 新功能

**變更**：新增聊天機器人歡迎訊息載入邏輯

**方案呈現**：
```
📦 提交方案：單次提交

所有變更邏輯相關，建議合併為一次提交：

  feat: 優化聊天小工具的歡迎訊息載入邏輯

  涉及檔案：
  - src/components/widget/chat-widget.tsx
  - src/hooks/use-welcome-message.ts
```

### 範例 2：單次提交 - 多檔案但邏輯相關

**變更**：
- 修改 `use-doc.tsx` 的 isLoading 初始值
- 修改 `chat-widget.tsx` 的渲染條件
- 修改 `next.config.ts` 的快取設定

**分析**：雖然跨 3 個檔案，但都是為了修復同一個「載入時顯示預設值」的問題

**方案呈現**：
```
📦 提交方案：單次提交

所有變更邏輯相關，建議合併為一次提交：

  fix: 修復 Widget 載入時顯示預設值而非客製化設定的問題

  涉及檔案：
  - src/hooks/use-doc.tsx
  - src/components/widget/chat-widget.tsx
  - next.config.ts
```

### 範例 3：分類提交 - 混合變更類型

**變更**：
- 新增使用者頭像上傳功能（feat）
- 修復登入頁面的錯誤訊息（fix）
- 更新 README 文件（docs）

**分析**：三種不同類型的變更，彼此獨立無關

**方案呈現**：
```
📦 提交方案：分類提交（共 3 次）

變更可分為以下獨立群組：

[1] feat: 新增使用者頭像上傳功能
    涉及檔案：
    - src/components/profile/avatar-upload.tsx
    - src/app/api/upload/route.ts

[2] fix: 修復登入頁面錯誤訊息顯示問題
    涉及檔案：
    - src/app/login/page.tsx

[3] docs: 更新 README 安裝說明
    涉及檔案：
    - README.md
```

### 範例 4：分類提交 - 獨立功能模組

**變更**：
- 新增訂單匯出 CSV 功能
- 新增聊天室表情符號選擇器
- 更新 eslint 設定

**分析**：三個完全不相關的功能模組

**方案呈現**：
```
📦 提交方案：分類提交（共 3 次）

變更可分為以下獨立群組：

[1] feat: 新增訂單匯出 CSV 功能
    涉及檔案：
    - src/components/orders/export-button.tsx
    - src/lib/csv-generator.ts

[2] feat: 新增聊天室表情符號選擇器
    涉及檔案：
    - src/components/chat/emoji-picker.tsx

[3] chore: 更新 eslint 設定
    涉及檔案：
    - .eslintrc.json
```

## 安全注意事項

- 不提交包含敏感資訊的檔案（.env、credentials 等）
- 不執行 `--force` 或 `--no-verify`
- 不修改 git 設定
- 提交前先確認變更內容
