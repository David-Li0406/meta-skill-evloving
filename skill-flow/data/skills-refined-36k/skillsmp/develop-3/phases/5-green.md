# Phase 4: Green Phase - 寫最少的程式碼讓測試通過

## 目標

用**最少的程式碼**讓測試通過，不過度設計。

## 嚴格規則 ⛔

### 禁止事項

1. **嚴厲禁止異動測試程式**
2. **不可過度設計**（YAGNI – You Aren't Gonna Need It）
3. **不可寫超出測試需求的功能**
4. **不可在此階段重構**（重構在 Refactor Phase）

### 允許事項

1. ✅ 建立或修改 production code
2. ✅ 寫 hardcoded 值（重構時再改善）
3. ✅ 寫最簡單的實作方式
4. ✅ 只讓測試通過即可

---

## 執行步驟

### Step 1: 開啟 Production Code 檔案

根據 Red Phase 中測試的 import 路徑，建立或開啟對應的 production code 檔案。

**範例**:

```typescript
// 測試中：import { createOrder } from '../order';
// 需要建立：frontend/src/server/services/order.ts
```

---

### Step 2: 實作最少的程式碼

#### 原則：「能用 hardcoded 就用 hardcoded」

**測試需求**:

```typescript
// 測試期望：
expect(result).toEqual({
    orderId: 'order-456',
    status: 'pending'
});
```

**Green Phase 實作** (hardcoded):

```typescript
// frontend/src/server/services/order.ts
export function createOrder(data: any) {
    return {
        orderId: 'order-456',  // 先用 hardcoded
        status: 'pending'      // 先用 hardcoded
    };
}
```

**為什麼可以這樣？**

- 測試通過就好，重構階段再改善
- 避免過度設計
- 快速驗證測試邏輯正確

---

### Step 3: 逐步讓更多測試通過

當第二個測試失敗時（因為 hardcoded 值不符），才加入邏輯：

**第二個測試**:

```typescript
it('應該根據票種計算總金額', async () => {
    vi.mocked(db.getTicketTypes).mockResolvedValue([
        {id: 'ticket-1', price: 1000, inventory: 10}
    ]);

    const result = await createOrder({
        eventId: 'event-123',
        tickets: [{ticketTypeId: 'ticket-1', quantity: 3}],  // 3 張票
        customer: {email: 'test@example.com', name: '測試'}
    });

    expect(result.totalAmount).toBe(3000);  // 期望 3000
});
```

**Green Phase 實作** (加入邏輯):

```typescript
export async function createOrder(data: {
    eventId: string;
    tickets: Array<{ ticketTypeId: string; quantity: number }>;
    customer: { email: string; name: string };
}) {
    // 取得票種資訊
    const ticketTypes = await db.getTicketTypes(data.eventId);

    // 計算總金額（最簡單的 reduce）
    const totalAmount = data.tickets.reduce((sum, ticket) => {
        const ticketType = ticketTypes.find(t => t.id === ticket.ticketTypeId);
        return sum + (ticketType?.price || 0) * ticket.quantity;
    }, 0);

    return {
        orderId: crypto.randomUUID(),  // 改用真實 ID
        status: 'pending',
        totalAmount
    };
}
```

---

### Step 4: 透過 Wallaby 確認測試通過

```typescript
mcp__wallaby__wallaby_allTests()
```

**預期輸出**:

```json
{
  "tests": [
    {
      "name": "應該成功建立訂單並返回 order ID",
      "status": "passing"
    },
    {
      "name": "應該根據票種計算總金額",
      "status": "passing"
    }
  ]
}
```

**檢查項目**:

- [ ] 所有新寫的測試都通過
- [ ] 舊的測試沒有被破壞（仍然通過）
- [ ] Wallaby 顯示綠色

---

### Step 5: 除錯（如果測試失敗）

#### 使用 `wallaby_runtimeValues` 檢查變數值

**問題**: 測試失敗，不知道變數值是什麼

**解決**:

```typescript
// 從 error stack 找到問題行號
// 例如：order.ts:15

mcp__wallaby__wallaby_runtimeValues(
    'frontend/src/server/services/order.ts',
    15,
    '  const totalAmount = data.tickets.reduce(...);',
    'data.tickets'
)
```

**輸出**:

```json
{
  "values": [
    {
      "expression": "data.tickets",
      "value": "[{ ticketTypeId: 'ticket-1', quantity: 3 }]",
      "type": "Array"
    }
  ]
}
```

**根據輸出調整程式碼**:

- 檢查變數值是否符合預期
- 檢查邏輯是否正確

---

## Green Phase 完成檢查清單

- [ ] 只修改了 **production code**，沒有修改測試
- [ ] 所有測試通過（Wallaby 全綠）
- [ ] 沒有過度設計（符合 YAGNI 原則）
- [ ] 程式碼可讀性可接受（命名不要太差）
- [ ] 沒有明顯的 TypeScript 錯誤

---

## 常見錯誤

### ❌ 錯誤 1: 過度設計

**錯誤範例**:

```typescript
// 測試只需要簡單的加法
// 但你寫了一個複雜的計算引擎
class PriceCalculationEngine {
    private strategies: Map<string, PriceStrategy>;

    constructor() {
        this.strategies = new Map();
    }

    registerStrategy(name: string, strategy: PriceStrategy) {
        // 過度設計！測試不需要這些
    }

    calculate(data: OrderData): number {
        // 複雜的策略模式
    }
}
```

**正確範例**:

```typescript
// 測試只需要簡單的加法
function calculateTotal(tickets: Ticket[]): number {
    return tickets.reduce((sum, t) => sum + t.price * t.quantity, 0);
}
```

---

### ❌ 錯誤 2: 修改測試

**錯誤**: 發現測試寫錯了，直接修改測試

**正確做法**:

1. 回到 Red Phase
2. 修正測試
3. 重新執行 Green Phase

**原因**: Green Phase 只能改 production code，不能改測試。

---

### ❌ 錯誤 3: 寫超出測試需求的功能

**錯誤範例**:

```text
// 測試只需要 createOrder
// 但你還寫了 updateOrder, deleteOrder, listOrders
export function createOrder(data: OrderData) { ... }
export function updateOrder(id: string, data: OrderData) { ... }  // ❌ 測試不需要
export function deleteOrder(id: string) { ... }  // ❌ 測試不需要
export function listOrders() { ... }  // ❌ 測試不需要
```

**正確範例**:

```text
// 只寫測試需要的功能
export function createOrder(data: OrderData) { ... }  // ✅ 測試需要
```

---

## 下一步

所有測試通過後，進入 **Step 6: Refactor Phase** - 重構程式碼，改善品質

詳見 [6-refactor.md](6-refactor.md)

---

## 最佳實踐

### 1. 先讓測試通過，再考慮優化

```typescript
// ✅ Good: 先這樣寫
const total = tickets.reduce((sum, t) => sum + t.price * t.quantity, 0);

```

```typescript
// ❌ Bad: 不要在 Green Phase 做這種優化
const total = tickets
    .map(t => ({...t, subtotal: t.price * t.quantity}))
    .reduce((sum, t) => sum + t.subtotal, 0);
```

### 2. 使用 Type Guards 而非 Type Assertions

```typescript
// ✅ Good
function getPrice(ticketType: TicketType | undefined): number {
    if (!ticketType) return 0;
    return ticketType.price;
}

// ❌ Bad (使用 as 強制轉型)
function getPrice(ticketType: TicketType | undefined): number {
    return (ticketType as TicketType).price;  // 危險！
}
```

### 3. 保持函數簡短

```typescript
// ✅ Good: 一個函數做一件事
function calculateTotal(tickets: Ticket[]): number {
    return tickets.reduce((sum, t) => sum + t.price * t.quantity, 0);
}

// ❌ Bad: 函數做太多事
function processOrder(data: OrderData) {
    // 100 行程式碼...
    // 驗證、計算、資料庫操作、發送 email 全部混在一起
}
```
