# Phase 6: Commit & Push – 提交乾淨的 Commit

## 目標

提交符合 commitlint 規範的 commit，並正確處理 git hooks 失敗。

## 執行步驟

### Step 1: 確認所有測試通過

```typescript
mcp__wallaby__wallaby_allTests()
```

**檢查項目**:

- [ ] 所有測試狀態為 `passing`
- [ ] 沒有 `failing` 或 `pending` 測試
- [ ] Coverage 達到合理水平（建議 ≥90% for new code）

**如果有測試失敗**:

- 回到 **Step 4 (Red Phase)** 或 **Step 5 (Green Phase)**
- 修復測試後再繼續

---

### Step 2: 查看異動

```bash
git status
```

**預期輸出**:

```
On branch feature/event-ticketing
Changes not staged for commit:
  modified:   frontend/src/server/services/order.ts
  modified:   frontend/src/server/services/__tests__/order.test.ts

Untracked files:
  frontend/src/server/services/payment.ts
```

**查看詳細變更**:

```bash
git diff
```

**審查重點**:

- [ ] 沒有不必要的變更（console.log、註解、TODO）
- [ ] 沒有敏感資訊（API keys、passwords）
- [ ] 變更符合預期

---

### Step 3: Stage 檔案

```bash
git add <files>
```

**範例**:

```bash
# 加入所有修改的檔案
git add frontend/src/server/services/order.ts
git add frontend/src/server/services/__tests__/order.test.ts
git add frontend/src/server/services/payment.ts
```

**或一次加入所有變更**:

```bash
git add .
```

---

### Step 4: 撰寫 Commit Message

遵循 **Conventional Commits** 規範。

#### Commit Message 格式

```
<type>(<scope>): <description>

<body>

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

#### Type 規則

| Type       | 用途      | 範例                                                  |
|------------|---------|-----------------------------------------------------|
| `test`     | 新增或修改測試 | `test(order): add unit tests for order creation`    |
| `feat`     | 新增功能    | `feat(ticketing): implement order creation service` |
| `refactor` | 重構程式碼   | `refactor(order): extract price calculation logic`  |
| `fix`      | 修復 bug  | `fix(order): prevent negative inventory`            |
| `docs`     | 文件變更    | `docs(readme): update testing instructions`         |

#### 規則限制

- Type 必須是小寫
- Description 必須是小寫開頭
- Description 不能以句號結尾
- 使用祈使句（add, change, fix - 非 added, changed, fixed）
- Header 最長 100 字元

---

### Step 5: 執行 Commit

```bash
git commit -m "$(cat <<'EOF'
test(order): add unit tests for order creation

Implemented tests for:
- Successful order creation
- Inventory validation
- Payment failure handling

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

**注意事項**:

- 使用 `cat <<'EOF'` 確保多行格式正確
- 不要手動輸入多行，使用 HEREDOC

---

### Step 6: 處理 Git Hooks 失敗

專案的 git hooks 會執行測試和品質檢查。根據失敗原因，選擇不同的處理流程。

#### 6.1 判斷失敗類型

**檢查 hook 錯誤輸出**:

```bash
# Commit 失敗後會顯示 pre-commit hook 錯誤
```

---

#### 6.2 測試失敗 → 回到 TDD 迴圈（Step 4）

**識別關鍵字**:

- `FAIL` (Vitest 測試失敗)
- `test failed` (測試失敗訊息)
- `Error:` 搭配測試檔案路徑
- `FAILED` (Playwright 失敗)
- `X failed` (X 個測試失敗)

**錯誤範例**:

```
FAIL frontend/src/server/services/__tests__/order.test.ts
  ✗ 應該成功建立訂單 (25ms)

Error: Expected orderId to be defined
```

**處理步驟**:

1. **回到 Step 4 (Red Phase)**
2. 檢查測試是否正確
3. 檢查 production code 是否有 bug
4. 重新執行 Red-Green-Refactor 流程
5. 確保所有測試通過後再 commit

---

#### 6.3 品質問題 → 進入重構迴圈（Step 6）

**識別關鍵字**:

- `ESLint` 錯誤
- `TypeScript` type errors
- `Formatting` 問題
- `Warning` (非測試相關)

**錯誤範例**:

```
ESLint found 3 errors:
  frontend/src/server/services/order.ts:42:5 - 'data' is never used
  frontend/src/server/services/order.ts:58:12 - Missing return type
```

**處理步驟**:

1. **進入 Step 6.2 (重構迴圈)**
2. 執行 `get_file_problems` → `reformat_file` → `eslint`
3. 修復所有品質問題
4. 重新 commit

---

### Step 7: Push 到 Remote

```bash
git push origin <branch-name>
```

**範例**:

```bash
git push origin feature/event-ticketing
```

**首次 push 需要設定 upstream**:

```bash
git push -u origin feature/event-ticketing
```

---

## Commit 完成檢查清單

- [ ] 所有測試通過（Wallaby 全綠）
- [ ] Git hooks 執行成功（pre-commit, pre-push）
- [ ] Commit message 符合 Conventional Commits
- [ ] Commit message 包含 `🤖 Generated with Claude Code`
- [ ] Push 成功
- [ ] 沒有 force push（除非明確需要）

---

## 常見問題

### Q: Commit message 格式錯誤怎麼辦？

**錯誤**:

```
⧗   input: Test: add order tests  # ❌ Type 首字母大寫
✖   type must be lower-case [type-case]
```

**修正**:

```bash
# 重新 commit（會開啟編輯器）
git commit --amend

# 或直接修改 message
git commit --amend -m "test: add order tests"  # ✅ 小寫
```

---

### Q: 忘記加入某個檔案怎麼辦？

```bash
# 加入遺漏的檔案
git add forgotten-file.ts

# 修改上一個 commit（不建立新 commit）
git commit --amend --no-edit
```

**注意**: 只有在**尚未 push** 的情況下才能使用 `--amend`

---

### Q: Push 被拒絕（remote ahead）

**錯誤**:

```
! [rejected]        feature/event-ticketing -> feature/event-ticketing (non-fast-forward)
```

**解決**:

```bash
# 拉取 remote 變更
git pull origin feature/event-ticketing --rebase

# 解決衝突（如果有）
# ...

# 重新 push
git push origin feature/event-ticketing
```

---

### Q: 不小心 commit 到錯誤的分支

```bash
# 取消上一個 commit（保留變更）
git reset --soft HEAD~1

# 切換到正確的分支
git checkout correct-branch

# 重新 commit
git add .
git commit -m "..."
```

---

## Git Hooks 失敗處理流程圖

```
Commit 失敗
  ↓
檢查錯誤訊息
  ↓
  ├─ 包含 "FAIL", "test failed"? ────Yes───→ 測試失敗
  │                                          ↓
  │                                    回到 Step 4 (Red Phase)
  │                                    修復測試或 production code
  │                                    重新執行 TDD 迴圈
  │
  └─ 包含 "ESLint", "TypeScript"? ───Yes───→ 品質問題
                                             ↓
                                       回到 Step 6 (Refactor Loop)
                                       執行 get_file_problems
                                       修復品質問題
                                       重新 commit
```

---

## Commit Message 範例

### 範例 1: 測試 Commit

```bash
git commit -m "$(cat <<'EOF'
test(order): add unit tests for order service

Implemented tests for:
- Order creation with valid data
- Inventory validation
- Payment failure handling

Coverage: 95%

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### 範例 2: 功能 Commit

```bash
git commit -m "$(cat <<'EOF'
feat(ticketing): implement order creation service

Added createOrder function that:
- Validates ticket inventory
- Calculates total amount
- Creates payment intent
- Inserts order to database

Related to: e2e/specs/event-ticketing.feature

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

### 範例 3: 重構 Commit

```bash
git commit -m "$(cat <<'EOF'
refactor(order): extract price calculation logic

Extracted calculateTotalAmount to improve readability
and testability. No functional changes.

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

---

## 下一步

Commit 成功後：

### 選項 1: 繼續下一個測試案例

- 如果 Step 1 plan 中還有未完成的測試案例
- 回到 **Step 4 (Red Phase)**

### 選項 2: 執行 Gherkin Scenario

- 如果所有單元測試都完成
- 執行:
  ```bash
  npm run test:bdd -w e2e -- --name "<scenario name>"
  ```

### 選項 3: 處理下一個 Gherkin Scenario

- 如果當前 scenario 完成
- 回到 **Step 1 (Plan Phase)**

### 選項 4: 結束 Develop Skill

- 如果所有 scenarios 完成
- 執行

```bash
git push
```

- 結束 develop skill session
