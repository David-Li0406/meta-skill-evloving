# Wallaby MCP Tools 使用參考

## 概述
Wallaby MCP 提供即時測試監控和除錯功能，是 TDD 流程的核心工具。

---

## 核心工具

### 1. wallaby_allTests()
**用途**: 取得所有測試的執行狀況

**使用時機**:
- 啟動 Wallaby 後驗證運作
- Green Phase 後確認測試通過
- Refactor Phase 後確認測試仍通過

**範例**:
```typescript
const result = await mcp__wallaby__wallaby_allTests();
```

**輸出範例**:
```json
{
  "tests": [
    {
      "id": "test-1",
      "name": "應該成功建立訂單",
      "status": "passing",
      "file": "frontend/src/server/services/__tests__/order.test.ts",
      "line": 10
    },
    {
      "id": "test-2",
      "name": "應該在庫存不足時拋出錯誤",
      "status": "passing",
      "file": "frontend/src/server/services/__tests__/order.test.ts",
      "line": 35
    }
  ],
  "coverage": {
    "statements": 85.5,
    "branches": 78.2,
    "functions": 90.1,
    "lines": 84.8
  }
}
```

---

### 2. wallaby_failingTests()
**用途**: 取得失敗的測試詳細資訊

**使用時機**:
- Red Phase - 確認測試失敗原因正確
- 測試失敗時除錯

**範例**:
```typescript
const result = await mcp__wallaby__wallaby_failingTests();
```

**輸出範例**:
```json
{
  "failingTests": [
    {
      "id": "test-1",
      "name": "應該成功建立訂單",
      "status": "failing",
      "file": "frontend/src/server/services/__tests__/order.test.ts",
      "line": 10,
      "error": {
        "message": "Cannot find module '../order'",
        "stack": "Error: Cannot find module '../order'\\n    at order.test.ts:2:1"
      }
    }
  ]
}
```

---

### 3. wallaby_runtimeValues(file, line, lineContent, expression)
**用途**: 取得 error 發生前特定變數的值

**使用時機**:
- 測試失敗時除錯
- 確認變數值是否符合預期

**參數**:
- `file`: 檔案路徑（相對於專案根目錄）
- `line`: 行號（1-based）
- `lineContent`: 該行的完整內容
- `expression`: 要檢查的變數/表達式

**範例**:
```typescript
const result = await mcp__wallaby__wallaby_runtimeValues(
  'frontend/src/server/services/order.ts',
  42,
  '  const totalAmount = tickets.reduce((sum, t) => sum + t.price * t.quantity, 0);',
  'tickets'
);
```

**輸出範例**:
```json
{
  "values": [
    {
      "expression": "tickets",
      "value": "[{ ticketTypeId: 'ticket-1', price: 1000, quantity: 2 }]",
      "type": "Array"
    }
  ]
}
```

**實際使用流程**:
1. 測試失敗，顯示 error 在 `order.ts:42`
2. 使用 `wallaby_runtimeValues` 檢查 `tickets` 變數值
3. 發現 `tickets` 缺少 `price` 屬性
4. 修正 mock 或 production code

---

### 4. wallaby_coveredLinesForFile(file, testId?)
**用途**: 取得程式碼覆蓋率（整體或單一測試）

**使用時機**:
- 確認測試覆蓋率
- 識別未覆蓋的程式碼區域

**範例 1: 整體覆蓋率**:
```typescript
const result = await mcp__wallaby__wallaby_coveredLinesForFile(
  'frontend/src/server/services/order.ts'
);
```

**輸出範例**:
```json
{
  "coveredLines": [10, 11, 12, 15, 16, 20, 21, 22],
  "uncoveredLines": [25, 26, 30],
  "coverage": {
    "percentage": 72.7
  }
}
```

**範例 2: 單一測試覆蓋率**:
```typescript
const result = await mcp__wallaby__wallaby_coveredLinesForFile(
  'frontend/src/server/services/order.ts',
  'test-1'
);
```

---

### 5. wallaby_allTestsForFile(file)
**用途**: 取得特定檔案相關的所有測試

**使用時機**:
- 確認某個 production code 檔案被哪些測試覆蓋

**範例**:
```typescript
const result = await mcp__wallaby__wallaby_allTestsForFile(
  'frontend/src/server/services/order.ts'
);
```

**輸出範例**:
```json
{
  "tests": [
    {
      "id": "test-1",
      "name": "應該成功建立訂單",
      "status": "passing",
      "file": "frontend/src/server/services/__tests__/order.test.ts"
    },
    {
      "id": "test-2",
      "name": "應該在庫存不足時拋出錯誤",
      "status": "passing",
      "file": "frontend/src/server/services/__tests__/order.test.ts"
    }
  ]
}
```

---

## 常見使用流程

### 流程 1: 啟動 Wallaby 並驗證
```typescript
// 1. 啟動 Wallaby (透過 JetBrains MCP)
await mcp__jetbrains__execute_run_configuration('wallaby');

// 2. 驗證正常運作
const allTests = await mcp__wallaby__wallaby_allTests();
console.log(`共 ${allTests.tests.length} 個測試`);
```

---

### 流程 2: Red Phase - 確認測試失敗
```typescript
// 1. 寫完測試後，確認失敗
const failingTests = await mcp__wallaby__wallaby_failingTests();

// 2. 檢查失敗原因
failingTests.failingTests.forEach(test => {
  console.log(`Test: ${test.name}`);
  console.log(`Error: ${test.error.message}`);
});

// 3. 確認失敗原因正確（function 不存在或回傳值不符）
```

---

### 流程 3: Green Phase - 確認測試通過
```typescript
// 1. 寫完 production code 後，確認測試通過
const allTests = await mcp__wallaby__wallaby_allTests();

// 2. 檢查是否全綠
const passingCount = allTests.tests.filter(t => t.status === 'passing').length;
console.log(`${passingCount}/${allTests.tests.length} 測試通過`);
```

---

### 流程 4: 除錯失敗的測試
```typescript
// 1. 取得失敗測試
const failingTests = await mcp__wallaby__wallaby_failingTests();
const test = failingTests.failingTests[0];

// 2. 從 error stack 找到問題行號
const errorLine = 42; // 從 stack trace 解析

// 3. 檢查該行的變數值
const runtimeValues = await mcp__wallaby__wallaby_runtimeValues(
  'frontend/src/server/services/order.ts',
  errorLine,
  '  const totalAmount = tickets.reduce(...);',
  'tickets'
);

console.log('tickets 的值:', runtimeValues.values[0].value);

// 4. 根據 runtime values 修正程式碼或 mock
```

---

### 流程 5: 檢查程式碼覆蓋率
```typescript
// 1. 取得整體覆蓋率
const coverage = await mcp__wallaby__wallaby_coveredLinesForFile(
  'frontend/src/server/services/order.ts'
);

console.log(`覆蓋率: ${coverage.coverage.percentage}%`);

// 2. 識別未覆蓋的程式碼
console.log('未覆蓋的行:', coverage.uncoveredLines);

// 3. 為未覆蓋的程式碼補充測試
```

---

## 最佳實踐

### 1. 持續監控測試狀態
在 TDD 迴圈中，每個步驟都要使用 Wallaby:
- Red Phase: `wallaby_failingTests()`
- Green Phase: `wallaby_allTests()`
- Refactor Phase: `wallaby_allTests()`

### 2. 使用 runtimeValues 除錯
當測試失敗且錯誤訊息不清楚時:
1. 找到 error stack 中的行號
2. 使用 `wallaby_runtimeValues` 檢查該行的變數值
3. 根據實際值修正程式碼

### 3. 追蹤覆蓋率
定期檢查覆蓋率，確保達到專案標準（≥90% for new code）:
```typescript
const coverage = await mcp__wallaby__wallaby_coveredLinesForFile(file);
if (coverage.coverage.percentage < 90) {
  console.warn('覆蓋率不足 90%');
}
```

---

## 故障排除

### Q: wallaby_allTests() 回傳空陣列
**原因**: Wallaby 尚未完全啟動

**解決**:
1. 等待 10 秒
2. 重新執行 `wallaby_allTests()`
3. 如果仍失敗，重新啟動 Wallaby

### Q: wallaby_runtimeValues() 回傳空值
**原因**: 該行程式碼尚未執行

**解決**:
1. 確認測試有執行到該行
2. 檢查 `wallaby_coveredLinesForFile` 確認該行是否被覆蓋
3. 如果未覆蓋，調整測試案例

### Q: 覆蓋率顯示 0%
**原因**: Wallaby 設定問題或檔案路徑錯誤

**解決**:
1. 確認 Wallaby run configuration 正確
2. 確認檔案路徑相對於專案根目錄
3. 重新啟動 Wallaby
