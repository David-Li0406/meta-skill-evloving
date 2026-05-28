# Git Hooks 失敗處理指南

## 概述

專案的 git hooks（pre-commit, pre-push）會執行測試和品質檢查。根據失敗原因，需要選擇不同的處理流程。

---

## Git Hooks 類型

### Pre-commit Hook

在 `git commit` 執行前觸發，通常包含：

- ESLint 檢查
- TypeScript type checking
- 格式化檢查
- 單元測試

### Pre-push Hook

在 `git push` 執行前觸發，通常包含：

- 完整測試套件（unit + integration）
- E2E 測試（可選）
- Build 驗證

---

## 失敗類型判斷

### 判斷流程

```
Git Hook 失敗
  ↓
檢查錯誤訊息
  ↓
  ├─ 包含測試失敗關鍵字？
  │    ├─ "FAIL"
  │    ├─ "test failed"
  │    ├─ "Error:" + 測試檔案路徑
  │    ├─ "FAILED"
  │    └─ "X failed"
  │    ↓
  │   YES → 測試失敗
  │          回到 TDD 迴圈（Step 4）
  │
  └─ 包含品質問題關鍵字？
       ├─ "ESLint"
       ├─ "TypeScript"
       ├─ "Formatting"
       └─ "Warning"
       ↓
      YES → 品質問題
             進入重構迴圈（Step 6）
```

---

## 類型 1: 測試失敗

### 識別關鍵字

| 關鍵字             | 來源          | 範例                                                          |
|-----------------|-------------|-------------------------------------------------------------|
| `FAIL`          | Vitest      | `FAIL frontend/src/server/services/__tests__/order.test.ts` |
| `test failed`   | 通用          | `1 test failed`                                             |
| `Error:` + 測試路徑 | Vitest/Jest | `Error: Expected orderId to be defined`                     |
| `FAILED`        | Playwright  | `[chromium] › order.spec.ts:42:5 › FAILED`                  |
| `X failed`      | 測試框架        | `3 tests failed, 10 passed`                                 |

### 錯誤範例

#### Vitest 測試失敗

```
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
FAIL  frontend/src/server/services/__tests__/order.test.ts > createOrder > should create order
Error: expect(received).toEqual(expected)

Expected: {"orderId": "order-456", "status": "pending"}
Received: undefined

 ❯ frontend/src/server/services/__tests__/order.test.ts:25:20
```

#### Playwright E2E 失敗

```
Running 5 tests using 1 worker

  ✓ [chromium] › homepage.spec.ts:3:1 › should render homepage (1s)
  ✗ [chromium] › order.spec.ts:42:5 › should create order (25ms)

Error: Timeout 30000ms exceeded.
```

### 處理步驟

#### 1. 回到 TDD 迴圈（Step 4: Red Phase）

```
測試失敗
  ↓
分析失敗原因
  ↓
  ├─ 測試寫錯了？
  │    ↓
  │   回到 Red Phase
  │   修正測試
  │   重新執行 Green Phase
  │
  └─ Production code 有 bug？
       ↓
      回到 Green Phase
      修復 bug
      確認測試通過
```

#### 2. 使用 Wallaby 除錯

```typescript
// 1. 取得失敗測試詳細資訊
const failingTests = await mcp__wallaby__wallaby_failingTests();

// 2. 分析錯誤訊息
failingTests.failingTests.forEach(test => {
    console.log(`Test: ${test.name}`);
    console.log(`Error: ${test.error.message}`);
    console.log(`Stack: ${test.error.stack}`);
});

// 3. 使用 runtimeValues 檢查變數值
const runtimeValues = await mcp__wallaby__wallaby_runtimeValues(
    'frontend/src/server/services/order.ts',
    42,
    '  const result = await createOrder(data);',
    'data'
);

console.log('data 的值:', runtimeValues.values[0].value);
```

#### 3. 修復並重新測試

```bash
# 修復程式碼後，重新執行測試
npm run test:unit -w frontend

# 確認所有測試通過
mcp__wallaby__wallaby_allTests()

# 重新 commit
git add .
git commit -m "fix(order): correct order creation logic"
```

---

## 類型 2: 品質問題

### 識別關鍵字

| 關鍵字          | 來源         | 範例                                              |
|--------------|------------|-------------------------------------------------|
| `ESLint`     | ESLint     | `Error: 3 ESLint errors found`                  |
| `TypeScript` | tsc        | `error TS2322: Type 'string' is not assignable` |
| `Formatting` | Prettier   | `Code style issues found`                       |
| `Warning`    | 各種 linters | `Warning: unused variable 'data'`               |

### 錯誤範例

#### ESLint 錯誤

```
✖ 3 problems (3 errors, 0 warnings)

frontend/src/server/services/order.ts
  42:5   error  'data' is declared but never used  @typescript-eslint/no-unused-vars
  58:12  error  Missing return type on function     @typescript-eslint/explicit-function-return-type
  72:20  error  Unexpected any. Specify a type      @typescript-eslint/no-explicit-any
```

#### TypeScript 錯誤

```
frontend/src/server/services/order.ts:42:10 - error TS2322: Type 'string | undefined' is not assignable to type 'string'.

42   const email: string = customer.email;
            ~~~~~

Found 1 error.
```

### 處理步驟

#### 1. 進入重構迴圈（Step 6.2）

```
品質問題
  ↓
進入重構迴圈
  ↓
1. get_file_problems
   ↓
2. 修復問題
   ↓
3. reformat_file
   ↓
4. ESLint
   ↓
5. 驗證測試
   ↓
6. 全部通過？
   ├─ NO → 回到步驟 1
   └─ YES → 重新 commit
```

#### 2. 使用 JetBrains MCP 修復

```typescript
// 1. 取得異動檔案
const modifiedFiles = execSync('git status --short')
    .toString()
    .split('\n')
    .filter(line => line.trim())
    .map(line => line.substring(3));

// 2. 檢查問題
for (const file of modifiedFiles) {
    const problems = await mcp__jetbrains__get_file_problems(file, false);

    if (problems.problems.length > 0) {
        console.log(`${file} 有 ${problems.problems.length} 個問題`);

        // 逐一修復
        problems.problems.forEach(problem => {
            console.log(`Line ${problem.line}: ${problem.message}`);
        });
    }
}

// 3. 格式化
for (const file of modifiedFiles) {
    await mcp__jetbrains__reformat_file(file);
}

// 4. 重新檢查 ESLint
execSync('npm run lint -w frontend');
```

#### 3. 修復並重新 Commit

```bash
# 修復所有品質問題後，重新 commit
git add .
git commit -m "refactor(order): fix eslint warnings and type errors"
```

---

## 混合失敗（測試 + 品質問題）

### 處理順序

```
1. 先處理測試失敗
   ↓
   回到 TDD 迴圈
   確保所有測試通過
   ↓
2. 再處理品質問題
   ↓
   進入重構迴圈
   修復所有品質問題
   ↓
3. 重新 commit
```

**原因**: 測試失敗表示功能邏輯有問題，必須優先修復。

---

## 常見錯誤與解決方案

### 錯誤 1: 忽略 Hook 失敗

**錯誤做法**:

```bash
# ❌ 使用 --no-verify 跳過 hooks
git commit --no-verify -m "quick fix"
git push --no-verify
```

**後果**:

- 破壞 CI/CD
- 累積技術債
- 影響團隊其他成員

**正確做法**:

```bash
# ✅ 修復問題後再 commit
# 檢查錯誤類型
# 修復問題
# 重新 commit
git commit -m "fix: correct implementation"
```

---

### 錯誤 2: 修改測試讓 Hook 通過

**錯誤做法**:

```typescript
// ❌ 測試失敗，直接改測試
it('should return order id', () => {
    const result = createOrder({...});
    expect(result.orderId).toBe('123');  // 改成符合實作的值
});
```

**正確做法**:

```typescript
// ✅ 修復 production code
export function createOrder(data: OrderData) {
    // 修正邏輯，讓測試通過
    return {
        orderId: crypto.randomUUID(),
        status: 'pending'
    };
}
```

---

### 錯誤 3: 只修復錯誤訊息中的第一個問題

**錯誤做法**:

```bash
# ❌ 只修復第一個 ESLint 錯誤
# 修復後重新 commit
# 又遇到第二個錯誤
# 再修復...
# 重複多次
```

**正確做法**:

```bash
# ✅ 修復所有問題後再 commit
# 1. 取得所有問題
npm run lint -w frontend

# 2. 逐一修復所有問題
# ...

# 3. 確認全部通過
npm run lint -w frontend  # ✓ No errors

# 4. commit
git commit -m "refactor: fix all eslint errors"
```

---

## Git Hooks 失敗處理流程圖

```
Git Commit/Push 失敗
  ↓
檢查 Hook 錯誤輸出
  ↓
  ┌─────────────────────────────────────┐
  │  包含測試失敗關鍵字？               │
  │  (FAIL, test failed, FAILED, etc.)  │
  └─────────────────────────────────────┘
         │
         ├─ YES → 測試失敗
         │         ↓
         │        回到 TDD 迴圈（Step 4）
         │         ↓
         │        1. 分析失敗原因
         │        2. 使用 Wallaby 除錯
         │        3. 修復測試或 production code
         │        4. 確認測試通過
         │        5. 重新 commit
         │
         └─ NO  → 品質問題
                   ↓
                  進入重構迴圈（Step 6）
                   ↓
                  1. get_file_problems
                  2. 修復問題
                  3. reformat_file
                  4. ESLint
                  5. 驗證測試
                  6. 重新 commit
```

---

## 最佳實踐

### 1. 在 Commit 前先執行測試

```bash
# 避免 commit 失敗，先手動執行測試
npm run test:unit -w frontend

# 確認通過後再 commit
git commit -m "feat: add order creation"
```

### 2. 使用 Wallaby 即時監控

```typescript
// Wallaby 會即時顯示測試狀態
// 可以在 commit 前就發現問題
await mcp__wallaby__wallaby_allTests();
```

### 3. 定期執行重構迴圈

```bash
# 不要等到 commit 才發現品質問題
# 在開發過程中定期執行
npm run lint -w frontend
```

### 4. 理解錯誤訊息

```bash
# 仔細閱讀錯誤訊息
# 判斷是測試失敗還是品質問題
# 選擇正確的處理流程
```

---

## 檢查清單

### Commit 前檢查

- [ ] 所有測試通過（Wallaby 全綠）
- [ ] 沒有 ESLint 錯誤
- [ ] 沒有 TypeScript 錯誤
- [ ] 程式碼已格式化
- [ ] Commit message 符合規範

### Hook 失敗後檢查

- [ ] 已識別失敗類型（測試 vs 品質）
- [ ] 已選擇正確的處理流程
- [ ] 已修復所有問題（不只是第一個）
- [ ] 已驗證修復有效
- [ ] 已重新執行 hooks 確認通過
