---
name: github
description: GitHub Copilot skills 路由器與專案整合指引 - 提供 skills 自動載入、README.md 強制維護、軟路由機制
license: MIT
---

# GitHub Copilot Skills 整合指南

GitHub Copilot 自動 skills 載入與專案管理的核心指南。

## 🤖 Copilot Skills 自動載入

### 路由機制

**根據 GitHub 官方文件（2025-12-18），GitHub Copilot 會自動：**

- ✅ 檢測並載入 `.claude/skills/` 目錄
- ✅ 檢測並載入 `.opencode/skills/` 目錄
- ✅ 根據使用者 prompt 內容**智能選擇**相關 skill
- ✅ 支援跨平台：Copilot CLI、VS Code Insiders Agent Mode、Copilot Coding Agent

### 軟路由（Soft Routing）策略

**智能載入邏輯：**

| 使用者 Prompt 關鍵詞                                                | 自動載入的 Skill   |
| ------------------------------------------------------------------- | ------------------ |
| 「git」、「commit」、「branch」                                     | `git-workflow`     |
| 「component」、「vue」、「composable」                              | `vue`              |
| 「code-standards」、「coding」、「development」、「規範」、「開發」 | `code-standards`   |
| 「程式碼品質」、「最佳實踐」、「技術棧」                            | `code-standards`   |
| 「測試」、「test」、「spec」、「test-driven」                       | `vue/testing`      |
| 「README」、「文檔」、「更新」、「文檔維護」                        | `github/README.md` |
| 「AI」、「copilot」、「agent」、「智慧助理」                        | `agent`            |

## 📋 強制 README.md 維護機制

### 🔥 執行流程（強制執行）

**任何專案變更完成後，必須執行以下四步驟：**

#### 1️⃣ 立即檢查 README.md 影響

```bash
# 檢查受影響的 README 區段
git diff --name-only HEAD~1
```

**需要檢查的 README 檔案：**

- 專案根目錄 `README.md`
- `.opencode/skills/README.md`
- `docs/` 目錄下的所有 README.md
- 各模組的 README.md（如 `src/components/README.md`）

#### 2️⃣ 立即更新對應區段

**必須立即更新的內容：**

| 變更類型   | README 區段 | 更新要求                       |
| ---------- | ----------- | ------------------------------ |
| 新增組件   | 組件列表    | 新增組件名稱、功能描述         |
| 修改 Store | 狀態管理    | 更新 Store 結構說明            |
| 新增 Skill | Skills 說明 | 更新 skills 目錄結構和使用說明 |
| 更新依賴   | 安裝說明    | 更新套件版本和安裝指令         |
| 修改配置   | 開發設定    | 更新配置檔案說明               |

#### 3️⃣ 完整驗證更新內容

```bash
# 驗證 README 格式
npx markdownlint README.md

# 驗證連結有效性
npx markdown-link-check README.md

# 本地預覽
pnpm run docs:dev  # 如果有
```

**驗證項目清單：**

- [ ] 所有新增功能都有對應說明
- [ ] 安裝/運行指令正確
- [ ] 目錄結構是最新的
- [ ] 版本號同步更新
- [ ] 連結都能正常點擊
- [ ] 程式碼範例可正常執行

#### 4️⃣ 提交包含 README.md 更新的 commit

**Commit 訊息規範：**

```bash
# 功能開發
feat: 新增 [功能名稱] 並更新 README.md

# 修復問題
fix: 修復 [問題描述] 並更新相關文檔

# 文檔更新
docs: 更新 [模組] README.md 說明
```

**🚨 重要：絕不單獨提交 README.md 更新！**

所有 README.md 變更**必須**與功能變更在同一個 commit 中。

## 🎯 Lucky50 專案 Skills 整合

### 可用的 Skills

| Skill          | 描述                                       | 自動載入觸發詞                 |
| -------------- | ------------------------------------------ | ------------------------------ |
| `lucky50-dev`  | Lucky50 專案開發規範與最佳實踐             | lucky50, 專案規範, 開發指南    |
| `git-workflow` | Git 分支命名與工作流程規範                 | git, commit, branch, pr        |
| `vue`          | Vue 3 Composition API 開發指南             | vue, component, composable     |
| `github`       | GitHub Copilot skills 路由與整合（本檔案） | github, copilot, skill, README |

### 智能載入範例

**使用者輸入：**

```
「幫我建立一個新的使用者認證組件，並更新相關文檔」
```

**GitHub Copilot 自動載入：**

1. ✅ 載入 `code-standards`（了解專案規範）
2. ✅ 載入 `vue`（獲取 Vue 組件開發模式）
3. ✅ 載入 `github/README.md`（執行強制維護流程）

## 🔄 Cross-Platform 支援

### 支援的環境

- ✅ **GitHub Copilot CLI** - 命令列界面
- ✅ **VS Code Insiders** - Agent Mode
- ✅ **Copilot Coding Agent** - Web 界面
- ✅ **Visual Studio Code Stable** - 2026年1月支援

### 相容性保證

**OpenCode ↔ GitHub Copilot 雙重支援：**

- ✅ 同時符合 OpenCode skill 格式（YAML frontmatter）
- ✅ 同時符合 GitHub Copilot skill 格式
- ✅ 保持現有 OpenCode 功能完整性
- ✅ 自動支援 GitHub Copilot 的智能載入

## 🔧 GitHub Copilot 軟路由機制

### 詳細路由策略

**完整的智慧載入系統詳見：[soft-routing.md](soft-routing.md)**

**快速載入規則：**

1. **分析請求類型**：識別關鍵詞與意圖
2. **計算複雜度**：決定是否需要多技能組合
3. **情境感知**：考慮當前專案狀態
4. **動態載入**：按需載入最適合的技能組合

### 常見載入場景

```typescript
// 範例：複雜的開發請求
request: "幫我建立一個使用者認證組件，整合 Pinia Store，並更新相關文檔"

// AI 智慧載入順序
1. code-standards (了解專案規範）
2. vue (獲取 Vue 組件開發模式）
3. vue/composables (如果需要自訂 composable）
4. github/README.md (執行強制文檔維護）
```

## 🛠️ 最佳實踐

### Skill 開發規範

1. **統一 YAML frontmatter**：

   ```yaml
   ---
   name: skill-name
   description: 技能描述
   license: MIT
   ---
   ```

2. **檔案命名規範**：
   - 主檔案：`SKILL.md`
   - 參考檔案：`references/` 目錄
   - 資源檔案：`resources/` 目錄

3. **模組化載入**：
   - 基礎檔案 ~250 tokens
   - 子檔案 ~500-1500 tokens
   - 按需載入，避免浪費 context

### README.md 維護規範

**🔴 強制要求：**

1. **任何程式碼變更都必須包含 README 更新**
2. **README 更新必須在同一個 commit**
3. **更新後必須驗證連結和格式**
4. **保持文檔與程式碼同步**

**檢查清單：**

- [ ] 新增功能有說明？
- [ ] 更新指令正確？
- [ ] 目錄結構同步？
- [ ] 版本號一致？
- [ ] 連結可點擊？

## 📚 參考資源

- [GitHub Copilot Skills 官方文件](https://docs.github.com/copilot)
- [GitHub Changelog - Skills 支援公告](https://github.blog/changelog/2025-12-18-github-copilot-now-supports-agent-skills/)
- [OpenCode Skills 文檔](https://opencode.ai/docs/skills/)
- [anthropics/skills](https://github.com/anthropics/skills) - 社群 skills 範例
- [github/awesome-copilot](https://github.com/github/awesome-copilot) - 精選 skills 收集
