# TDD 紀律守則

## 核心原則

TDD（Test-Driven Development）的核心是**紀律**。遵循嚴格的規則可以確保：

- 高品質的測試覆蓋率
- 簡潔的程式碼設計
- 快速的回饋循環
- 可維護的程式碼庫

---

## Red-Green-Refactor 循環

```
┌──────────────────────────────────────────┐
│  RED: 寫失敗的測試                        │
│  ↓                                        │
│  GREEN: 寫最少的程式碼讓測試通過           │
│  ↓                                        │
│  REFACTOR: 重構程式碼，保持測試通過        │
│  ↓                                        │
│  回到 RED（下一個測試案例）                │
└──────────────────────────────────────────┘
```

---

## 禁止事項 ⛔

### 1. Red Phase 不可異動 Production Code

**規則**: 在寫測試時，**嚴厲禁止**修改或建立 production code。

**原因**:

- 確保測試失敗是因為缺少功能，不是因為實作錯誤
- 保持測試的獨立性
- 避免過度設計

**違規範例** ❌:

```typescript
// ❌ 在測試檔案中同時寫測試和實作
// order.test.ts
describe('createOrder', () => {
    it('should create order', () => {
        // 測試程式碼...
    });
});

// ❌ 在同一次 commit 中建立測試和實作
// 應該分兩個步驟：先寫測試（Red），再寫實作（Green）
```

**正確做法** ✅:

```typescript
// Step 1: Red Phase - 只寫測試
// order.test.ts
describe('createOrder', () => {
    it('should create order', () => {
        const result = createOrder({...});  // function 還不存在
        expect(result).toEqual({orderId: '123'});
    });
});

// 執行測試 → 失敗（Cannot find module '../order'）

// Step 2: Green Phase - 寫實作
// order.ts
export function createOrder(data: any) {
    return {orderId: '123'};
}

// 執行測試 → 通過
```

---

### 2. Green Phase 不可異動測試

**規則**: 在寫 production code 時，**嚴厲禁止**修改測試。

**原因**:

- 確保測試的穩定性
- 避免「改測試讓它通過」的惡習
- 保持測試的需求一致性

**違規範例** ❌:

```typescript
// ❌ 發現測試寫錯了，直接修改測試
it('should return order id', () => {
  const result = createOrder({ ... });
  expect(result.orderId).toBe('123');  // 原本期望 '123'
  // ❌ 發現實作回傳 '456'，直接改測試
  expect(result.orderId).toBe('456');  // 改成期望 '456'
});
```

**正確做法** ✅:

```typescript
// ✅ 如果測試確實寫錯了
// 1. 回到 Red Phase
// 2. 修正測試
// 3. 重新執行 Green Phase
it('should return order id', () => {
  const result = createOrder({ ... });
  expect(result.orderId).toBeDefined();  // 修正：只驗證存在即可
});
```

---

### 3. 不可跳過測試直接寫 Production Code

**規則**: 必須先寫測試，再寫實作。

**原因**:

- 確保測試真的有效（先失敗，再通過）
- 避免「實作導向」的測試（測試只是驗證實作）
- 保持 TDD 的紀律

**違規範例** ❌:

```typescript
// ❌ 先寫實作
// order.ts
export function createOrder(data: OrderData) {
  // 100 行程式碼...
}

// ❌ 再寫測試（這只是驗證實作，不是真正的 TDD）
// order.test.ts
it('should create order', () => {
  const result = createOrder({ ... });
  expect(result).toEqual({ ... });  // 根據實作寫測試
});
```

**正確做法** ✅:

```typescript
// ✅ 先寫測試
// order.test.ts
it('should create order', () => {
    const result = createOrder({eventId: '123', ...});
    expect(result.orderId).toBeDefined();
    expect(result.status).toBe('pending');
});

// 執行測試 → 失敗

// ✅ 再寫實作
// order.ts
export function createOrder(data: OrderData) {
    return {
        orderId: crypto.randomUUID(),
        status: 'pending'
    };
}

// 執行測試 → 通過
```

---

### 4. 不可寫通過的測試

**規則**: 測試必須先失敗，再通過。

**原因**:

- 確保測試真的在測試功能
- 避免「假陽性」測試（總是通過的測試）
- 驗證測試的有效性

**違規範例** ❌:

```typescript
// ❌ 測試一開始就通過（根本沒有測試到東西）
it('should return true', () => {
    expect(true).toBe(true);  // 這個測試永遠通過
});

// ❌ 測試不依賴 production code
it('should have valid data', () => {
    const mockData = {id: '123'};  // 測試中自己建立資料
    expect(mockData.id).toBe('123');  // 沒有測試到實際功能
});
```

**正確做法** ✅:

```typescript
// ✅ 測試必須先失敗
it('should create order with generated id', () => {
    const result = createOrder({...});
    expect(result.orderId).toBeDefined();  // 這會失敗（function 不存在）
});

// 執行測試 → 失敗（Cannot find module '../order'）

// 寫實作後再執行 → 通過
```

---

### 5. 不可一次寫多個測試

**規則**: 一次只寫一個測試案例。

**原因**:

- 保持專注
- 快速回饋
- 避免過度設計

**違規範例** ❌:

```text
// ❌ 一次寫 5 個測試
describe('createOrder', () => {
  it('should create order', () => { ... });
  it('should validate inventory', () => { ... });
  it('should calculate total', () => { ... });
  it('should handle payment', () => { ... });
  it('should send email', () => { ... });
});

// 執行測試 → 5 個全部失敗（不知道從哪裡開始）
```

**正確做法** ✅:

```text
// ✅ 一次寫一個測試
describe('createOrder', () => {
  it('should create order', () => { ... });
});

// 執行測試 → 失敗
// 寫實作 → 通過
// 再寫下一個測試...
```

---

## 必須事項 ✅

### 1. 必須使用 Wallaby 即時監控

**原因**:

- 即時回饋測試狀態
- 快速定位問題
- 提升開發效率

**使用方式**:

```typescript
// 啟動 Wallaby
await mcp__jetbrains__execute_run_configuration('wallaby');

// 每個 Phase 都檢查測試狀態
// Red Phase
await mcp__wallaby__wallaby_failingTests();

// Green Phase
await mcp__wallaby__wallaby_allTests();

// Refactor Phase
await mcp__wallaby__wallaby_allTests();
```

---

### 2. 必須反覆執行重構迴圈直到成功

**原因**:

- 確保程式碼品質
- 符合專案標準
- 避免累積技術債

**重構迴圈**:

```
1. get_file_problems
   ↓
2. reformat_file
   ↓
3. ESLint
   ↓
4. 驗證測試
   ↓
5. 如果有問題 → 回到 1
   ↓
✅ 完成
```

---

### 3. 必須符合 Commitlint 規範

**原因**:

- 保持 commit history 一致性
- 易於追蹤變更
- 支援自動化工具（changelog 生成）

**規範**:

```bash
# Type 必須小寫
test(order): add unit tests  # ✅
Test(order): add unit tests  # ❌

# Description 必須小寫開頭
test(order): add unit tests  # ✅
test(order): Add unit tests  # ❌

# 使用祈使句
test(order): add unit tests  # ✅
test(order): added unit tests  # ❌
```

---

### 4. 必須處理 Git Hooks 失敗

**原因**:

- 確保程式碼品質
- 避免破壞 CI/CD
- 保持測試通過

**處理流程**:

```
Git Hook 失敗
  ↓
檢查錯誤類型
  ↓
  ├─ 測試失敗 → 回到 TDD 迴圈（Step 4）
  └─ 品質問題 → 進入重構迴圈（Step 6）
```

---

## TDD 反模式（避免）

### 反模式 1: 寫實作導向的測試

**錯誤**:

```typescript
// ❌ 根據實作寫測試（不是 TDD）
// 先看了 production code，再寫測試驗證它
it('should call db.insert with correct params', () => {
  createOrder({ ... });
  expect(db.insert).toHaveBeenCalledWith({ ... });
});
```

**正確**:

```typescript
// ✅ 根據需求寫測試（真正的 TDD）
it('should create order and return order id', () => {
  const result = createOrder({ ... });
  expect(result.orderId).toBeDefined();
});
```

---

### 反模式 2: 過度 Mock

**錯誤**:

```typescript
// ❌ Mock 所有東西（失去測試意義）
vi.mock('../order');
vi.mock('../payment');
vi.mock('../email');
vi.mock('../notification');
// ... 10 個 mocks

it('should do something', () => {
  // 測試變成在驗證 mocks 的行為
});
```

**正確**:

```typescript
// ✅ 只 mock 外部依賴
vi.mock('~/server/db');  // 外部依賴
vi.mock('../payment');   // 外部依賴

it('should create order', () => {
    // 測試業務邏輯
});
```

---

### 反模式 3: 測試實作細節

**錯誤**:

```typescript
// ❌ 測試內部狀態
it('should set internal state', () => {
    const service = new OrderService();
    service.createOrder({...});
    expect(service._internalState).toBe('...');  // 測試私有變數
});
```

**正確**:

```typescript
// ✅ 測試行為
it('should create order', () => {
    const service = new OrderService();
    const result = service.createOrder({...});
    expect(result.orderId).toBeDefined();  // 測試公開 API
});
```

---

## 紀律檢查清單

每個 TDD 循環都應該檢查：

### Red Phase

- [ ] 只寫了測試，沒有寫實作
- [ ] 測試確實失敗
- [ ] 失敗原因正確（function 不存在或回傳值不符）

### Green Phase

- [ ] 只寫了實作，沒有修改測試
- [ ] 測試通過
- [ ] 沒有過度設計

### Refactor Phase

- [ ] 反覆執行重構迴圈
- [ ] 所有檢查通過（get_file_problems, ESLint, 測試）
- [ ] 程式碼品質改善

### Commit

- [ ] 符合 Conventional Commits
- [ ] Git hooks 通過
- [ ] Push 成功

---

## 違反紀律的後果

### 1. 跳過測試直接寫實作

**後果**:

- 測試覆蓋率降低
- 測試變成「驗證實作」而非「驗證需求」
- 難以重構（不確定測試是否有效）

### 2. 在 Green Phase 修改測試

**後果**:

- 測試失去意義（可以隨意改測試讓它通過）
- 測試與需求不一致
- 難以追蹤需求變更

### 3. 不執行重構迴圈

**後果**:

- 累積技術債
- 程式碼品質下降
- 難以維護

---

## 紀律的好處

### 1. 高品質測試覆蓋率

- 所有程式碼都有測試
- 測試真的有效（先失敗再通過）

### 2. 簡潔的程式碼設計

- YAGNI（You Aren't Gonna Need It）
- 只寫需要的功能

### 3. 快速回饋

- Wallaby 即時監控
- 立即發現問題

### 4. 可維護的程式碼

- 重構迴圈確保品質
- 測試作為安全網
