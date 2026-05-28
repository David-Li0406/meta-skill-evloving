# Phase 5: Refactor Phase – 重構迴圈

## 目標

改善程式碼品質，同時保持所有測試通過。

## 執行步驟

### Step 6.1: 審查異動

```bash
git status
```

**檢查**:

- 哪些檔案被修改？
- 是否有重複的程式碼？
- 變數/函數命名是否清晰？
- 程式邏輯是否可簡化？

### Step 6.2: 重構迴圈（反覆執行直到成功）

#### 迴圈結構

```
┌─────────────────────────────────┐
│  1. get_file_problems           │
│     ↓ 修復 warnings/errors      │
│  2. reformat_file               │
│     ↓                           │
│  3. ESLint                      │
│     ↓ 如果有錯誤 → 回到 1      │
│  4. 驗證測試通過                │
│     ↓ 如果失敗 → 回到 1        │
│  5. 檢查是否完成                │
│     ↓ 否 → 回到 1              │
│     ✓ 是 → 完成重構             │
└─────────────────────────────────┘
```

---

#### 1️⃣ 檢查問題 (get_file_problems)

##### 1.1 取得異動檔案（透過 git status）

```bash
git status --short
```

輸出範例:

```
 M frontend/src/server/services/order.ts
 M frontend/src/server/services/__tests__/order.test.ts
?? frontend/src/server/services/payment.ts
```

**處理新增檔案**:

```bash
# 如果有 ?? (Untracked files)，先 git add
git add frontend/src/server/services/payment.ts
```

##### 1.2 解析異動檔案清單

```typescript
// 解析 git status --short 輸出
const modifiedFiles = [
    'frontend/src/server/services/order.ts',
    'frontend/src/server/services/__tests__/order.test.ts',
    'frontend/src/server/services/payment.ts'  // 新增檔案（已 git add）
];
```

##### 1.3 逐一檢查每個檔案

```text
for (const file of modifiedFiles) {
    const result = await mcp__jetbrains__get_file_problems(file, errorsOnly: false);
    console.log(`檢查 ${file}:`, result);
}
```

##### 1.4 分析問題並修復

**常見問題類型**:

| 問題類型                | 範例                                                         | 修復方式                              |
|---------------------|------------------------------------------------------------|-----------------------------------|
| Type error          | `Type 'string \| undefined' is not assignable to 'string'` | 添加 type guard 或 optional chaining |
| Unused variable     | `'mockData' is declared but never used`                    | 移除或使用該變數                          |
| Missing return type | `Function lacks return type annotation`                    | 添加 return type                    |
| Complexity          | `Function has cyclomatic complexity of 12`                 | 提取 helper functions               |

**修復範例**:

```typescript
// ❌ Before (Type error)
function getCustomerEmail(customer: Customer | undefined): string {
    return customer.email; // Error: customer might be undefined
}

// ✅ After
function getCustomerEmail(customer: Customer | undefined): string | undefined {
    return customer?.email;
}
```

##### 1.5 如果有問題，修復後重新檢查

- 修復程式碼
- 儲存檔案
- 重新執行 `get_file_problems`
- 確認問題已解決

---

#### 2️⃣ 格式化 (reformat_file)

```typescript
// 使用 git status 取得的異動檔案清單
for (const file of modifiedFiles) {
    await mcp__jetbrains__reformat_file(file);
    console.log(`已格式化 ${file}`);
}
```

**格式化內容**:

- Indentation（縮排）
- Whitespace（空格）
- Line breaks（換行）
- Import statements（Import 順序）

**注意**: 格式化後可能產生新的 git diff，這是正常的。

---

#### 3️⃣ ESLint 檢查

##### 3.1 執行 ESLint

```bash
npm run lint -w frontend
```

##### 3.2 分析錯誤

**常見 ESLint 錯誤**:

| 錯誤                                   | 範例                                         | 修復             |
|--------------------------------------|--------------------------------------------|----------------|
| `no-unused-vars`                     | `'React' is defined but never used`        | 移除或使用該變數       |
| `no-console`                         | `Unexpected console statement`             | 移除 console.log |
| `prefer-const`                       | `'data' is never reassigned. Use 'const'`  | 改為 const       |
| `@typescript-eslint/no-explicit-any` | `Unexpected any. Specify a different type` | 使用具體 type      |

##### 3.3 自動修復

```bash
npx eslint --fix frontend/src/server/services/order.ts
```

##### 3.4 手動修復

如果自動修復無法解決，手動修改程式碼：

```typescript
// ❌ Before (no-explicit-any)
function processData(data: any) {
    return data.value;
}

// ✅ After
interface DataWithValue {
    value: string;
}

function processData(data: DataWithValue) {
    return data.value;
}
```

##### 3.5 重新執行 ESLint

```bash
npm run lint -w frontend
```

確認輸出為:

```
✓ No ESLint warnings or errors
```

如果仍有錯誤，**回到 1️⃣**（get_file_problems）

---

#### 4️⃣ 驗證測試仍通過

```typescript
mcp__wallaby__wallaby_allTests()
```

**預期輸出**: 所有測試為綠色

如果有測試失敗:

1. 檢查是否在重構時不小心改變了邏輯
2. 使用 `wallaby_runtimeValues` 除錯
3. 修復後**回到 1️⃣**

---

#### 5️⃣ 檢查是否完成

**完成條件** (全部必須為 ✅):

- [ ] `get_file_problems` 無 warnings/errors
- [ ] `reformat_file` 已執行
- [ ] ESLint 通過
- [ ] 所有測試通過（Wallaby 全綠）

**如果全部 ✅**: 重構完成，前往 **Step 7: Commit & Push**

**如果有任何 ❌**: **回到 1️⃣**，再執行一輪

---

### Step 6.3: 程式碼改善建議

在重構迴圈中，可進行以下改善：

#### 5.3.1 提取重複程式碼

**Before**:

```typescript
// 測試 1
const mockCustomer = {email: 'test@example.com', name: '測試'};
const mockTickets = [{ticketTypeId: 'ticket-1', quantity: 2}];
```

```typescript
// 測試 2
const mockCustomer = {email: 'test@example.com', name: '測試'};
const mockTickets = [{ticketTypeId: 'ticket-1', quantity: 100}];
```

**After**:

```typescript
// 在 describe 外層
const createMockCustomer = () => ({
    email: 'test@example.com',
    name: '測試'
});

const createMockTickets = (quantity: number) => ([
    {ticketTypeId: 'ticket-1', quantity}
]);

// 測試 1
const mockCustomer = createMockCustomer();
const mockTickets = createMockTickets(2);
```

#### 5.3.2 重命名變數/函數（使用 rename_refactoring）

**使用 JetBrains MCP**:

```typescript
mcp__jetbrains__rename_refactoring(
    'frontend/src/server/services/order.ts',
    'processOrder',  // old name
    'createOrder'    // new name
)
```

**好處**:

- 自動更新所有 references
- 保持一致性
- 避免手動 find/replace 遺漏

#### 5.3.3 移除 Unused Imports

**Before**:

```typescript
import {useState, useEffect, useMemo} from 'react';
import {formatDate} from '~/utils/date';

// 只用了 useState
```

**After**:

```typescript
import {useState} from 'react';
```

#### 5.3.4 簡化複雜邏輯

**Before** (Cyclomatic Complexity = 8):

```typescript
function validateOrder(order: Order) {
    if (order.tickets.length === 0) {
        throw new Error('No tickets');
    } else if (order.tickets.some(t => t.quantity <= 0)) {
        throw new Error('Invalid quantity');
    } else if (!order.customer.email) {
        throw new Error('Missing email');
    } else if (order.totalAmount < 0) {
        throw new Error('Invalid amount');
    }
    return true;
}
```

**After** (Cyclomatic Complexity = 4):

```typescript
function validateOrder(order: Order) {
    validateTickets(order.tickets);
    validateCustomer(order.customer);
    validateAmount(order.totalAmount);
    return true;
}

function validateTickets(tickets: Ticket[]) {
    if (tickets.length === 0) throw new Error('No tickets');
    if (tickets.some(t => t.quantity <= 0)) throw new Error('Invalid quantity');
}

function validateCustomer(customer: Customer) {
    if (!customer.email) throw new Error('Missing email');
}

function validateAmount(amount: number) {
    if (amount < 0) throw new Error('Invalid amount');
}
```

---

## 重構迴圈流程圖

```
Start
  ↓
1. get_file_problems
  ↓
  有問題? ────Yes───→ 修復問題 ──┐
  │                              │
  No                             │
  ↓                              │
2. reformat_file                 │
  ↓                              │
3. ESLint                        │
  ↓                              │
  有錯誤? ────Yes───→ 修復錯誤 ──┤
  │                              │
  No                             │
  ↓                              │
4. 驗證測試                       │
  ↓                              │
  失敗? ──────Yes───→ 修復測試 ──┤
  │                              │
  No                             │
  ↓                              │
5. 全部完成? ───No──────────────┘
  │
  Yes
  ↓
完成重構
```

---

## 重構完成檢查清單

- [ ] 所有 staged files 都通過 `get_file_problems`
- [ ] 所有 staged files 都已 `reformat_file`
- [ ] ESLint 無 warnings/errors
- [ ] Wallaby 所有測試通過（綠色）
- [ ] 沒有重複的程式碼
- [ ] 變數/函數命名清晰
- [ ] Cyclomatic Complexity ≤10
- [ ] 無 unused imports/variables

---

## 常見問題

### Q: 重構迴圈要執行幾次？

A: 直到**所有檢查清單項目都是 ✅** 為止。通常 2-3 次。

### Q: 如果 ESLint 錯誤無法自動修復怎麼辦？

A: 手動修改程式碼後，重新執行整個迴圈（從 `get_file_problems` 開始）。

### Q: 重構時測試失敗了怎麼辦？

A: 這表示重構改變了邏輯。使用 `wallaby_runtimeValues` 除錯，修復後重新執行迴圈。

### Q: 可以跳過 `reformat_file` 嗎？

A: 不可以。格式化是程式碼品質的一部分，必須執行。

---

## 下一步

重構完成後，前往 **Step 7: Commit & Push**

詳見 [7-commit.md](7-commit.md)
