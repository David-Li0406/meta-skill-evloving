---
name: develop
description: "嚴謹 TDD 流程：讀取 gherkin（e2e/specs/*.feature）→ Plan mode 規劃測試 → 建立 Git 分支 → 啟動 Wallaby → Red-Green-Refactor 迴圈 → 重構（JetBrains MCP: get_file_problems, reformat_file, ESLint）→ commit（commitlint）。整合 Wallaby MCP 即時監控。觸發：「開始開發」、「進入開發模式」、「TDD」。(project)"
allowed-tools: Read, Write, Edit, Bash(git:*), Bash(npm:*), TodoWrite, mcp__wallaby__*, mcp__jetbrains__*, EnterPlanMode
---

# Develop Skill - 嚴謹 TDD 工作流程

## 概述

本 skill 引導你遵循嚴謹的 TDD 流程進行功能開發，整合 Wallaby MCP 即時測試監控和 JetBrains MCP 程式碼品質檢查。

**核心原則**:

- **Red**: 先寫失敗的測試（嚴禁異動 production code）
- **Green**: 用最少程式碼讓測試通過（嚴禁異動測試）
- **Refactor**: 反覆執行品質檢查直到成功

**必備工具**:

- Wallaby MCP (`wallaby_allTests`, `wallaby_runtimeValues`)
- JetBrains MCP (`get_file_problems`, `reformat_file`, `rename_refactoring`)

---

## 8 步驟工作流程

### Step 1: 規劃階段 📋

**目標**: 分析 gherkin 案例，規劃所有單元測試

**執行步驟**:

1. 列出所有 gherkin 檔案:
   ```json
   {
   "tool": "find_files_by_glob",
      "arguments": {
         "pattern": "e2e/specs/*.feature"
      }
   }
   ```

2. 讀取未完成的 gherkin 案例（查找 `# TODO` 或未實作的 scenarios）

3. **進入 Plan Mode** 分析該 scenario:
   ```

/plan

   ```

4. 在 plan mode 中:
    - 分析 Given-When-Then 的業務邏輯
    - 識別需要的單元測試檔案
    - 為每個測試案例規劃:
        - 測試描述
        - Input 參數
        - 預期 Output
    - 識別需要 mock 的依賴

5. 將 plan 輸出為結構化格式（詳見 [phases/1-plan.md](phases/1-plan.md)）

6. **提交給人類審查**，等待確認後繼續

**輸出範例**:

```markdown
## Gherkin: 使用者可以購買活動票券

### 單元測試計畫

#### 測試檔案: frontend/src/server/services/__tests__/order.test.ts

1. **測試案例**: 成功建立訂單
    - Input: { eventId, tickets, customer }
    - Expected: { orderId, status: 'pending' }
    - Mocks: db.insertOrder, payment.createPaymentIntent

2. **測試案例**: 庫存不足時拋出錯誤
    - Input: { quantity: 100 } (超過庫存 10)
    - Expected: throw Error('庫存不足')
    - Mocks: db.getTicketTypes

...
```

---

### Step 2: 建立 Git 分支 🌿

**目標**: 根據 Gherkin scenario 建立功能分支，遵循分支命名規範

**執行步驟**:

1. 檢查當前 Git 狀態:
   ```bash
   git status
   ```

2. 確保工作目錄乾淨（無未提交變更）:
    - 如有未提交變更，先提交或 stash
    - 確認當前在 `main` 分支

3. 拉取最新代碼:
   ```bash
   git pull origin main
   ```

4. 根據 Gherkin scenario 建立分支:

   **分支命名規則**:

   **A. 功能或 Bug 相關** - 格式: `{prefix}/{gherkin-scenario}`

   從 Gherkin scenario 標題提取關鍵字，轉換為 kebab-case:

   ```bash
   # Scenario: 使用者可以購買活動票券
   git checkout -b feature/user-can-purchase-event-tickets
   
   # Scenario: 修復結帳頁面顯示錯誤金額
   git checkout -b bugfix/fix-checkout-page-incorrect-amount
   
   # Scenario: 緊急修復生產環境登入失敗
   git checkout -b hotfix/fix-production-login-failure
   
   # Scenario: 增加單元測試覆蓋率
   git checkout -b test/increase-unit-test-coverage
   ```

   **Prefix 選擇指南**:
    - `feature/` - 新功能實作
    - `bugfix/` - Bug 修復（非緊急）
    - `hotfix/` - 緊急 Bug 修復（生產環境）
    - `test/` - 測試補充或測試重構

   **B. 非程式碼異動** - 格式: `{prefix}/{description}`

   文件、設定、維護等非 scenario 相關工作:

   ```bash
   # 更新專案文件
   git checkout -b docs/update-api-documentation
   
   # 專案維護工作
   git checkout -b chore/upgrade-dependencies
   ```

   **Prefix 選擇指南**:
    - `docs/` - 文件更新
    - `chore/` - 維護工作（依賴升級、設定調整等）

5. 驗證分支建立成功:
   ```bash
   git branch --show-current
   ```

**分支命名轉換範例**:

| Gherkin Scenario 標題 | 分支名稱                                      | Prefix 原因 |
|---------------------|-------------------------------------------|-----------|
| 使用者可以查看活動詳情         | `feature/user-can-view-event-details`     | 新功能       |
| 管理員可以編輯活動資訊         | `feature/admin-can-edit-event-info`       | 新功能       |
| 修復訂單狀態更新失敗          | `bugfix/fix-order-status-update-failure`  | Bug 修復    |
| 緊急修復支付流程中斷          | `hotfix/fix-payment-process-interruption` | 緊急修復      |
| 增加訂單服務測試覆蓋率         | `test/increase-order-service-coverage`    | 測試補充      |

**檢查清單**:

- [ ] Git 工作目錄乾淨
- [ ] 已拉取最新 main 分支
- [ ] 分支名稱符合命名規範
- [ ] 分支名稱使用 kebab-case（小寫字母 + 連字符）
- [ ] 分支名稱能清楚表達工作內容

**錯誤處理**:

- 如果工作目錄有未提交變更 → 提示使用者先提交或 stash
- 如果已存在同名分支 → 詢問使用者是否切換或使用新名稱
- 如果 git pull 失敗 → 檢查網路連線或遠端倉庫狀態

---

### Step 3: 啟動 Wallaby 🚀

**目標**: 啟動 Wallaby 即時測試監控

**執行步驟**:

1. 取得 Wallaby run configuration:
   ```typescript
   mcp__jetbrains__get_run_configurations()
   ```

2. 執行 Wallaby:
   ```typescript
   mcp__jetbrains__execute_run_configuration('wallaby')
   ```

3. 驗證 Wallaby 正常運作:
   ```typescript
   mcp__wallaby__wallaby_allTests()
   ```

**預期輸出**: 顯示所有測試的執行狀況（passing/failing/pending）

詳細指引請見 [phases/3-wallaby-setup.md](phases/3-wallaby-setup.md)

---

### Step 4-6: TDD 迴圈 🔄

#### Step 4: Red Phase ❌

**目標**: 寫一個**必須失敗**的測試

**嚴格規則**:

- ⛔ **嚴厲禁止異動主程式（production code）**
- ✅ 一次只寫**一個**測試案例
- ✅ 測試**必須失敗**
- ✅ 失敗原因必須是:
    - 找不到 function/class（尚未實作）
    - 回傳值與預期不符
- ⚠️ **不可以是**環境問題（import 錯誤、語法錯誤）

**執行步驟**:

1. 根據 Step 1 的 plan，建立或開啟測試檔案
2. 寫第一個測試案例（使用 Arrange-Act-Assert 模式）
3. 儲存檔案
4. 透過 Wallaby 確認測試失敗:
   ```typescript
   mcp__wallaby__wallaby_failingTests()
   ```
5. 檢查失敗原因是否符合預期（找不到 function 或回傳值錯誤）

詳細指引請見 [phases/4-red.md](phases/4-red.md)

---

#### Step 5: Green Phase ✅

**目標**: 用**最少的程式碼**讓測試通過

**嚴格規則**:

- ⛔ **嚴厲禁止異動測試程式**
- ✅ 只寫讓測試通過的**最少程式碼**
- ✅ 不要過度設計（YAGNI - You Aren't Gonna Need It）
- ✅ 可以寫 hardcoded 值（之後重構時改善）

**執行步驟**:

1. 開啟 production code 檔案
2. 實作最少的程式碼讓測試通過:
    - 建立 function/class（如果不存在）
    - 實作基本邏輯
    - 回傳正確的值
3. 儲存檔案
4. 透過 Wallaby 確認測試通過:
   ```typescript
   mcp__wallaby__wallaby_allTests()
   ```
5. 如果有錯誤，使用 `wallaby_runtimeValues` 除錯:
   ```typescript
   mcp__wallaby__wallaby_runtimeValues(file, line, lineContent, expression)
   ```

詳細指引請見 [phases/5-green.md](phases/5-green.md)

---

#### Step 6: Refactor Phase ♻️

**目標**: 改善程式碼品質，同時保持測試通過

**執行步驟**:

##### 5.1 審查異動

```bash
git status
```

確認哪些檔案被修改，是否需要重構

##### 5.2 重構迴圈（反覆執行直到成功）

**Loop Iteration**:

1️⃣ **檢查問題** (`get_file_problems`)

```bash
# 取得異動檔案（透過 git status）
git status --short
```

處理新增檔案:

```bash
# 如果有 ?? (Untracked files)，先 git add
git add <new-files>
```

逐一檢查每個異動檔案:

```text
mcp__jetbrains__get_file_problems(file, errorsOnly: false)
```

- 修復所有 **warnings** 和 **errors**
- 如果有問題，修復後回到此步驟

2️⃣ **格式化** (`reformat_file`)

```text
mcp__jetbrains__reformat_file(file)
```

3️⃣ **ESLint 檢查**

```bash
npm run lint -w frontend
```

- 如果有錯誤，執行:
  ```bash
  npx eslint --fix <file>
  ```
- 如果仍有錯誤，手動修復後回到 1️⃣

4️⃣ **驗證測試仍通過**

```typescript
mcp__wallaby__wallaby_allTests()
```

- 如果測試失敗，修復後回到 1️⃣

5️⃣ **重複**

- 持續執行 1️⃣ → 2️⃣ → 3️⃣ → 4️⃣
- **直到**: `get_file_problems` 無問題 + ESLint 通過 + 測試全綠

##### 5.3 程式碼改善建議

- 提取重複的程式碼為 helper function
- 重命名變數/函數以提升可讀性（使用 `rename_refactoring`）
- 移除 unused imports/variables
- 簡化複雜的條件判斷

詳細指引請見 [phases/6-refactor.md](phases/6-refactor.md)

---

### Step 7: Commit & Push 📤

**目標**: 提交乾淨的 commit，符合 commitlint 規範

**執行步驟**:

1. 確認所有測試通過:
   ```typescript
   mcp__wallaby__wallaby_allTests()
   ```

2. 查看異動:
   ```bash
   git status
   git diff
   ```

3. Stage 檔案:
   ```bash
   git add <files>
   ```

4. 撰寫 commit message（符合 Conventional Commits）:
   ```bash
   git commit -m "$(cat <<'EOF'
   <type>(<scope>): <description>

   <body>

   🤖 Generated with Claude Code
   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   EOF
   )"
   ```

   **Type 規則**:
    - `test`: 新增或修改測試
    - `feat`: 新增功能
    - `refactor`: 重構程式碼

5. Push:
   ```bash
   git push origin <branch-name>
   ```

6. **處理 Git Hooks 失敗**:
    - **測試失敗** → 回到 Step 4（TDD 迴圈 - Red Phase）
    - **品質問題**（lint/format/type errors）→ 回到 Step 6（重構迴圈）
    - 修復後重新 commit/push

   **判斷方式**: 檢查 git hook 錯誤訊息中是否包含測試失敗關鍵字（`test failed`, `FAIL`, `Error:`, Vitest/Playwright 錯誤）

詳細指引請見 [phases/7-commit.md](phases/7-commit.md)

---

### Step 8: 下一個測試案例 🔁

**判斷**:

- 如果 Step 1 plan 中還有未完成的測試案例 → 回到 Step 4（Red Phase）
- 如果所有單元測試都完成 → 驗證 BDD scenario 實作完成度

---

#### 7.1 驗證 BDD Step 實作完整性

**CRITICAL**: Gherkin scenario 的完成不只是「測試執行通過」，必須確保 **所有 BDD step 實作都已完成**。

**執行步驟**:

1. **讀取對應的 step definitions 檔案**:
   ```bash
   # 找出對應的 steps 檔案
   ls e2e/tests/bdd-steps/*.steps.ts
   ```

2. **檢查是否有未實作的 stub**:
   // 使用 search_in_files_by_text or search_in_files_by_regex 搜尋 stub 註解
   // AI 內部呼叫的 MCP 參數
   ```json
   {
      "tool": "search_in_files_by_text",
      "arguments": {
         "text": "// Stub",
         "include": "e2e/tests/bdd-steps/**"
         }
   }
   ```

3. **分析檢查結果**:

   **🔴 未完成（需繼續實作）**:
   ```typescript
   // ❌ 發現 stub 實作
   When('I view the event {string}', async (_eventTitle: string) => {
     // Stub: open event detail page in Phase 3.
   });
   ```

   **🟢 已完成**:

   ```typescript
   // ✅ 有完整實作
   When('I view the event {string}', async (eventTitle: string) => {
       const page = pageFixture.page;
       await page.goto(`/events/${eventTitle}`);
       await page.locator('h1').waitFor({state: 'visible'});
   });
   ```

4. **如果發現 stub，進入實作流程**:
    - 回到 **Step 1 (Plan Mode)** 分析該 step 需要的實作
    - 為該 step 規劃單元測試（如需要）
    - 執行 Red-Green-Refactor 流程實作功能（Step 4–6）
    - 實作 BDD step definition
    - 重新驗證實作完整性

**檢查清單**:

- [ ] 已讀取 `e2e/tests/bdd-steps/**.steps.ts` 檔案
- [ ] 已搜尋並確認無 `// Stub:` 註解
- [ ] 所有 Given/When/Then steps 都有完整實作
- [ ] 沒有空的 function body 或 placeholder 註解

---

#### 7.2 執行 BDD Scenario 測試

**只有在 7.1 確認所有 step 實作完成後**，才執行 BDD 測試:

```bash
npm run test:bdd -w e2e -- --name "<scenario name>"
```

**預期結果**:

- ✅ Scenario 執行成功
- ✅ 所有 steps 都正確執行（非 pending/skipped）
- ✅ 所有 assertions 都通過

**如果測試失敗**:

1. 檢查是單元測試問題 → 回到 Step 4（Red Phase）
2. 檢查是 BDD step 實作問題 → 修正 step definition
3. 檢查是整合問題 → 使用 Wallaby runtime values 除錯

---

#### 7.3 Scenario 完成條件

**完整完成條件**（所有項目必須全部符合）:

- ✅ 所有單元測試通過
- ✅ **所有 BDD step definitions 實作完成（無 stub）**
- ✅ Gherkin scenario 可執行並通過
- ✅ Step definitions 有適當的 assertions
- ✅ Git commit & Git push 兩者皆成功

---

**下一步**:

- 如果當前 scenario **未完全實作** → 回到 8.1 繼續實作
- 如果當前 scenario **已完全實作** → 回到 Step 1，處理下一個 gherkin scenario
- 如果**所有 scenarios 完成** → 結束 develop skill

---

## TDD 紀律守則

### 禁止事項 ⛔

1. **Red Phase 不可異動 production code**
2. **Green Phase 不可異動測試**
3. **不可跳過測試直接寫 production code**
4. **不可寫通過的測試（必須先失敗）**
5. **不可一次寫多個測試**

### 必須事項 ✅

1. **必須使用 Wallaby 即時監控**
2. **必須反覆執行重構迴圈直到成功**
3. **必須符合 commitlint 規範**
4. **必須處理 git hooks 失敗**

詳細紀律守則請見 [rules/tdd-discipline.md](rules/tdd-discipline.md)

---

## MCP Tools 參考

### Wallaby MCP

- `wallaby_allTests()` - 取得所有測試狀況
- `wallaby_failingTests()` - 取得失敗的測試
- `wallaby_runtimeValues(file, line, lineContent, expression)` - 除錯變數值
- `wallaby_coveredLinesForFile(file)` - 取得程式碼覆蓋率

詳見 [mcp-tools/wallaby-reference.md](mcp-tools/wallaby-reference.md)

### JetBrains MCP

- `get_file_problems(filePath, errorsOnly)` - 取得檔案問題
- `reformat_file(path)` - 格式化檔案
- `rename_refactoring(pathInProject, symbolName, newName)` - 重命名重構
- `get_symbol_info(filePath, line, column)` - 取得 function 說明

詳見 [mcp-tools/jetbrains-reference.md](mcp-tools/jetbrains-reference.md)

---

## 範例

### Gherkin → 測試計畫

詳見 [examples/gherkin-to-tests.md](examples/gherkin-to-tests.md)

### 完整重構迴圈

詳見 [examples/refactor-loop.md](examples/refactor-loop.md)

---

## 故障排除

### Git Hooks 失敗處理

**判斷失敗類型**:

1. **檢查錯誤訊息**
   ```bash
   # Git hook 失敗後，查看錯誤輸出
   git commit  # 如果失敗，會顯示 pre-commit hook 錯誤
   ```

2. **測試失敗** - 回到 TDD 迴圈（Step 4）

   **識別關鍵字**:
    - `FAIL` (Vitest 測試失敗)
    - `test failed` (測試失敗訊息)
    - `Error:` 搭配測試檔案路徑
    - `FAILED` (Playwright 失敗)
    - `X failed` (X 個測試失敗)

   **處理步驟**:
    - 回到 **Step 4 (Red Phase)**
    - 檢查測試是否正確
    - 檢查 production code 是否有 bug
    - 重新執行 Red-Green-Refactor 流程
    - 確保所有測試通過後再 commit

3. **品質問題** - 進入重構迴圈（Step 6）

   **識別關鍵字**:
    - `ESLint` 錯誤
    - `TypeScript` type errors
    - `Formatting` 問題
    - `Warning` (非測試相關)

   **處理步驟**:
    - 進入 **Step 6.2 (重構迴圈)**
    - 執行 get_file_problems → reformat_file → eslint
    - 修復所有品質問題
    - 重新 commit

詳見 [rules/git-hooks.md](rules/git-hooks.md)

### Wallaby 無法啟動

1. 檢查 JetBrains IDE 是否開啟
2. 檢查 run configuration 是否存在
3. 重新執行 `execute_run_configuration`

### 測試一直失敗

1. 使用 `wallaby_runtimeValues` 檢查變數值
2. 使用 `wallaby_failingTests` 取得詳細錯誤訊息
3. 檢查 mock 是否正確設定
