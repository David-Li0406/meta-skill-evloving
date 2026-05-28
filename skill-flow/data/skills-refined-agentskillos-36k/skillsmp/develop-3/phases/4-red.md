# Phase 3: Red Phase – 寫失敗的測試

## 目標

寫一個**必須失敗**的測試，失敗原因必須是缺少 production code 或回傳值不符。

## 嚴格規則 ⛔

### 禁止事項

1. **嚴厲禁止異動主程式（production code）**
2. **不可一次寫多個測試**
3. **不可寫已經會通過的測試**
4. **不可跳過此步驟直接寫 production code**

### 允許事項

1. ✅ 建立或修改測試檔案
2. ✅ Import 尚未存在的 function/class（這會讓測試失敗）
3. ✅ 設定 mocks
4. ✅ 寫 assertions

## 執行步驟

### 1. 根據 Step 1 plan，確認要寫的測試案例

範例: 測試案例 1 - 成功建立訂單

### 2. 建立或開啟測試檔案

```typescript
// frontend/src/server/services/__tests__/order.test.ts
import {describe, it, expect, vi, beforeEach} from 'vitest';
import {createOrder} from '../order';  // ⚠️ 這個 function 還不存在！
import * as db from '~/server/db';
import * as payment from '../payment';
```

### 3. 設定 Mocks

```typescript
vi.mock('~/server/db');
vi.mock('../payment');

describe('createOrder', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });
});
```

### 4. 寫第一個測試（Arrange-Act-Assert 模式）

#### 4.1 Arrange（準備）

```typescript
it('應該成功建立訂單並返回 order ID', async () => {
    // Arrange
    const mockEventId = 'event-123';
    const mockTickets = [
        {ticketTypeId: 'ticket-1', quantity: 2}
    ];
    const mockCustomer = {
        email: 'test@example.com',
        name: '測試用戶'
    };

    const mockOrderId = 'order-456';
    const mockPaymentIntent = {id: 'pi_789', status: 'succeeded'};

    // Mock database operations
    vi.mocked(db.getTicketTypes).mockResolvedValue([
        {id: 'ticket-1', price: 1000, inventory: 10}
    ]);
    vi.mocked(db.insertOrder).mockResolvedValue({id: mockOrderId});

    // Mock payment service
    vi.mocked(payment.createPaymentIntent).mockResolvedValue(mockPaymentIntent);
});
```

#### 4.2 Act（執行）

```typescript
  // Act
const result = await createOrder({
    eventId: mockEventId,
    tickets: mockTickets,
    customer: mockCustomer
});
```

#### 4.3 Assert（驗證）

```typescript
  // Assert
expect(result).toEqual({
    orderId: mockOrderId,
    status: 'pending'
});

// Verify database calls
expect(db.insertOrder).toHaveBeenCalledWith({
    eventId: mockEventId,
    customerEmail: mockCustomer.email,
    totalAmount: 2000, // 2 tickets * 1000
    status: 'pending'
});

// Verify payment service calls
expect(payment.createPaymentIntent).toHaveBeenCalledWith({
    amount: 2000,
    currency: 'twd',
    metadata: {orderId: mockOrderId}
});
```

### 5. 儲存檔案

### 6. 透過 Wallaby 確認測試失敗

```typescript
mcp__wallaby__wallaby_failingTests()
```

**預期輸出**:

```
Failing Tests:
- frontend/src/server/services/__tests__/order.test.ts
  - createOrder
    - ✗ 應該成功建立訂單並返回 order ID
      Error: Cannot find module '../order' or its corresponding type declarations
```

### 7. 驗證失敗原因正確

**正確的失敗原因** ✅:

- `Cannot find module '../order'` → function 不存在
- `TypeError: createOrder is not a function` → function 未定義
- `Expected: { orderId: 'order-456' }, Received: undefined` → 回傳值不符

**錯誤的失敗原因** ❌（需修復）:

- `SyntaxError: Unexpected token` → 語法錯誤
- `Error: Cannot find module 'vitest'` → 環境問題
- `TypeError: vi.mock is not a function` → 測試框架設定錯誤

如果是環境問題，**先修復環境**，確保測試可以執行。

## Red Phase 完成檢查清單

- [ ] 只寫了**一個**測試案例
- [ ] **沒有異動** production code
- [ ] 測試**確實失敗**
- [ ] 失敗原因是 **function 不存在** 或 **回傳值不符**
- [ ] 不是語法錯誤或環境問題
- [ ] Wallaby 顯示測試為紅色

## 下一步

前往 **Step 5: Green Phase** - 寫最少的 production code 讓測試通過

詳見 [5-green.md](5-green.md)
