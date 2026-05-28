# 完整重構迴圈範例

## 情境

剛完成 Green Phase，測試全部通過。現在需要進入 Refactor Phase，改善程式碼品質。

---

## 初始狀態

### 異動的檔案

```bash
$ git status
On branch feature/event-ticketing
Changes not staged for commit:
  modified:   frontend/src/server/services/order.ts
  modified:   frontend/src/server/services/__tests__/order.test.ts

Untracked files:
  frontend/src/server/services/payment.ts
```

---

## 迴圈 Iteration 1

### Step 1: 取得異動檔案

```bash
$ git status --short
 M frontend/src/server/services/order.ts
 M frontend/src/server/services/__tests__/order.test.ts
?? frontend/src/server/services/payment.ts
```

**處理新增檔案**:

```bash
# 先 git add 新增的檔案
$ git add frontend/src/server/services/payment.ts
```

**解析檔案清單**:

```typescript
const modifiedFiles = [
    'frontend/src/server/services/order.ts',
    'frontend/src/server/services/__tests__/order.test.ts',
    'frontend/src/server/services/payment.ts'
];
```

---

### Step 2: 檢查問題 (get_file_problems)

#### 檔案 1: order.ts

```typescript
await mcp__jetbrains__get_file_problems(
    'frontend/src/server/services/order.ts',
    false
);
```

**輸出**:

```json
{
  "problems": [
    {
      "severity": "ERROR",
      "message": "Type 'string | undefined' is not assignable to type 'string'",
      "line": 42,
      "column": 10
    },
    {
      "severity": "WARNING",
      "message": "Variable 'mockData' is declared but never used",
      "line": 15,
      "column": 7
    },
    {
      "severity": "WARNING",
      "message": "Function 'calculateTotal' lacks return type annotation",
      "line": 58,
      "column": 10
    }
  ]
}
```

**修復**:

1. **Type error (line 42)**:

```typescript
// ❌ Before
function getCustomerEmail(customer: Customer | undefined): string {
    return customer.email;  // Error: customer might be undefined
}

// ✅ After
function getCustomerEmail(customer: Customer | undefined): string | undefined {
    return customer?.email;
}
```

2. **Unused variable (line 15)**:

```typescript
// ❌ Before
const mockData = {id: '123'};  // Unused

// ✅ After
// (直接刪除)
```

3. **Missing return type (line 58)**:

```text
// ❌ Before
function calculateTotal(tickets) {
  return tickets.reduce(...);
}

// ✅ After
function calculateTotal(tickets: Ticket[]): number {
  return tickets.reduce(...);
}
```

---

#### 檔案 2: order.test.ts

```typescript
await mcp__jetbrains__get_file_problems(
    'frontend/src/server/services/__tests__/order.test.ts',
    false
);
```

**輸出**:

```json
{
  "problems": []
}
```

✅ 無問題

---

#### 檔案 3: payment.ts

```typescript
await mcp__jetbrains__get_file_problems(
    'frontend/src/server/services/payment.ts',
    false
);
```

**輸出**:

```json
{
  "problems": [
    {
      "severity": "ERROR",
      "message": "Parameter 'amount' implicitly has an 'any' type",
      "line": 5,
      "column": 36
    }
  ]
}
```

**修復**:

```typescript
// ❌ Before
export function createPaymentIntent(amount) {
    return stripe.paymentIntents.create({amount});
}

// ✅ After
export function createPaymentIntent(amount: number): Promise<PaymentIntent> {
    return stripe.paymentIntents.create({amount});
}
```

---

### Step 3: 重新檢查問題

修復所有問題後，重新執行 `get_file_problems`:

```typescript
for (const file of modifiedFiles) {
    const problems = await mcp__jetbrains__get_file_problems(file, false);
    console.log(`${file}: ${problems.problems.length} 個問題`);
}
```

**輸出**:

```
frontend/src/server/services/order.ts: 0 個問題
frontend/src/server/services/__tests__/order.test.ts: 0 個問題
frontend/src/server/services/payment.ts: 0 個問題
```

✅ 所有問題已修復

---

### Step 4: 格式化 (reformat_file)

```typescript
for (const file of modifiedFiles) {
    await mcp__jetbrains__reformat_file(file);
    console.log(`✅ 已格式化 ${file}`);
}
```

**輸出**:

```
✅ 已格式化 frontend/src/server/services/order.ts
✅ 已格式化 frontend/src/server/services/__tests__/order.test.ts
✅ 已格式化 frontend/src/server/services/payment.ts
```

---

### Step 5: ESLint 檢查

```bash
$ npm run lint -w frontend
```

**輸出**:

```
✖ 2 problems (2 errors, 0 warnings)

frontend/src/server/services/order.ts
  72:20  error  Unexpected any. Specify a type  @typescript-eslint/no-explicit-any
  85:15  error  'result' is never reassigned. Use 'const' instead  prefer-const
```

**修復 error 1 (line 72)**:

```typescript
// ❌ Before
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

**修復 error 2 (line 85)**:

```typescript
// ❌ Before
let result = await createOrder(data);
```

```typescript
// ✅ After
const result = await createOrder(data);
```

---

### Step 6: 重新執行 ESLint

```bash
$ npm run lint -w frontend
```

**輸出**:

```
✓ No ESLint warnings or errors
```

✅ ESLint 通過

---

### Step 7: 驗證測試仍通過

```typescript
const allTests = await mcp__wallaby__wallaby_allTests();
```

**輸出**:

```json
{
  "tests": [
    {
      "name": "should create order successfully",
      "status": "passing"
    },
    {
      "name": "should throw error when inventory insufficient",
      "status": "passing"
    }
  ]
}
```

✅ 所有測試通過

---

### Step 8: 檢查完成條件

- ✅ `get_file_problems` 無問題
- ✅ `reformat_file` 已執行
- ✅ ESLint 通過
- ✅ 測試全通過

**結論**: Iteration 1 完成 ✅

---

## 迴圈 Iteration 2（假設）

### 情境: ESLint 發現新問題

假設在 Iteration 1 修復問題後，ESLint 發現新的問題（因為修改了程式碼）。

```bash
$ npm run lint -w frontend
```

**輸出**:

```
✖ 1 problem (0 errors, 1 warning)

frontend/src/server/services/order.ts
  92:10  warning  Unexpected console statement  no-console
```

---

### Step 1: 回到 get_file_problems

雖然 `get_file_problems` 可能不會顯示 ESLint warnings，但我們仍需修復。

**修復**:

```typescript
// ❌ Before
console.log('Order created:', orderId);  // Warning

// ✅ After
// (移除 console.log，或使用 logger)
logger.info('Order created:', orderId);
```

---

### Step 2: 重新執行 ESLint

```bash
$ npm run lint -w frontend
```

**輸出**:

```
✓ No ESLint warnings or errors
```

✅ ESLint 通過

---

### Step 3: 驗證測試

```typescript
const allTests = await mcp__wallaby__wallaby_allTests();
```

✅ 測試通過

---

### Step 4: 檢查完成條件

- ✅ ESLint 通過
- ✅ 測試通過

**結論**: Iteration 2 完成 ✅

---

## 迴圈 Iteration 3（假設）

### 情境: 測試失敗

假設在重構過程中，不小心改變了邏輯，導致測試失敗。

```typescript
const allTests = await mcp__wallaby__wallaby_allTests();
```

**輸出**:

```json
{
  "tests": [
    {
      "name": "should create order successfully",
      "status": "failing",
      "error": {
        "message": "Expected 2000, received 3000"
      }
    }
  ]
}
```

---

### Step 1: 使用 wallaby_runtimeValues 除錯

```typescript
const runtimeValues = await mcp__wallaby__wallaby_runtimeValues(
    'frontend/src/server/services/order.ts',
    58,
    '  const totalAmount = calculateTotal(tickets);',
    'tickets'
);
```

**輸出**:

```json
{
  "values": [
    {
      "expression": "tickets",
      "value": "[{ price: 1000, quantity: 2 }]",
      "type": "Array"
    }
  ]
}
```

**發現問題**: 計算邏輯錯誤

---

### Step 2: 修復邏輯

```typescript
// ❌ Before (錯誤的計算)
function calculateTotal(tickets: Ticket[]): number {
    return tickets.reduce((sum, t) => sum + t.price * t.quantity * 1.5, 0);  // 多了 1.5
}

// ✅ After
function calculateTotal(tickets: Ticket[]): number {
    return tickets.reduce((sum, t) => sum + t.price * t.quantity, 0);
}
```

---

### Step 3: 驗證測試

```typescript
const allTests = await mcp__wallaby__wallaby_allTests();
```

**輸出**:

```json
{
  "tests": [
    {
      "name": "should create order successfully",
      "status": "passing"
    }
  ]
}
```

✅ 測試通過

---

### Step 4: 重新執行完整檢查

```bash
# 1. get_file_problems
# 2. reformat_file
# 3. ESLint
# 4. 驗證測試
```

**結論**: Iteration 3 完成 ✅

---

## 最終狀態

### 完成條件確認

- ✅ `get_file_problems` 無問題（3 個檔案）
- ✅ `reformat_file` 已執行（3 個檔案）
- ✅ ESLint 通過
- ✅ 所有測試通過（Wallaby 全綠）
- ✅ 沒有 console.log
- ✅ 沒有 unused variables
- ✅ 所有 function 有 return type

---

## Commit

```bash
$ git add .
$ git commit -m "$(cat <<'EOF'
refactor(order): improve code quality

- Add type annotations
- Remove unused variables
- Fix type errors
- Extract helper functions

🤖 Generated with Claude Code
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

**輸出**:

```
[feature/event-ticketing 3a4b5c6] refactor(order): improve code quality
 3 files changed, 45 insertions(+), 30 deletions(-)
 create mode 100644 frontend/src/server/services/payment.ts
```

✅ Commit 成功

---

## Push

```bash
$ git push origin feature/event-ticketing
```

**輸出**:

```
Counting objects: 10, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (6/6), done.
Writing objects: 100% (10/10), 2.43 KiB | 2.43 MiB/s, done.
Total 10 (delta 4), reused 0 (delta 0)
To github.com:user/repo.git
   abc123..3a4b5c6  feature/event-ticketing -> feature/event-ticketing
```

✅ Push 成功

---

## 重構迴圈總結

### 執行了 3 個 Iterations

**Iteration 1**:

- 修復 TypeScript errors
- 修復 ESLint errors
- 格式化檔案

**Iteration 2**:

- 修復 console.log warning

**Iteration 3**:

- 修復測試失敗（邏輯錯誤）

### 修復的問題

| 類型                   | 數量 | 範例                                  |
|----------------------|----|-------------------------------------|
| Type errors          | 2  | `string \| undefined` assignability |
| Unused variables     | 1  | `mockData`                          |
| Missing return types | 1  | `calculateTotal`                    |
| No explicit any      | 1  | `processData` parameter             |
| Prefer const         | 1  | `result` reassignment               |
| No console           | 1  | `console.log` statement             |
| Logic error          | 1  | Incorrect calculation               |

### 關鍵學習

1. **反覆執行直到成功**: 不要只修復第一個問題就停止
2. **使用 Wallaby 即時監控**: 快速發現測試失敗
3. **系統化檢查**: get_file_problems → reformat → ESLint → tests
4. **除錯工具**: 使用 `wallaby_runtimeValues` 檢查變數值
