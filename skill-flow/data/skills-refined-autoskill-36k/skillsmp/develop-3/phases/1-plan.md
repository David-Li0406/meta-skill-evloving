# Phase 1: 規劃階段詳細指引

## 目標

分析 Gherkin scenario，規劃所有需要的單元測試案例。

## 前置條件

- Feature branch 已建立（透過 `/feature-start`）
- Gherkin 檔案已存在於 `e2e/specs/`

## 執行步驟

### 1. 列出所有 Gherkin 檔案

   ```json
   {
  "tool": "find_files_by_glob",
  "arguments": {
    "pattern": "e2e/specs/*.feature"
  }
}
   ```

### 2. 讀取目標 Scenario

選擇未完成的 scenario（標記 `# TODO` 或未實作）

範例:

```gherkin
# e2e/specs/event-ticketing.feature
Feature: 活動票務系統

  Scenario: 使用者可以購買活動票券
    Given 活動 "2024 音樂節" 有 10 張一般票可售
    When 使用者購買 2 張一般票
    Then 訂單狀態為 "pending"
    And 庫存剩餘 8 張
```

### 3. 進入 Plan Mode 分析

```
/plan
```

在 plan mode 中，進行以下分析：

#### 3.1 業務邏輯分解

- **Given** (前置條件) → 需要設定什麼資料？
    - 建立活動記錄
    - 設定票種和庫存

- **When** (執行動作) → 需要呼叫哪個 function？
    - `createOrder({ eventId, tickets, customer })`

- **Then** (預期結果) → 需要驗證什麼？
    - Order status 為 "pending"
    - 庫存正確扣減

#### 3.2 識別測試檔案

根據業務邏輯，識別需要測試的檔案：

- Service layer: `frontend/src/server/services/order.ts`
- Repository layer: `frontend/src/server/db/queries.ts`
- API route: `frontend/src/app/api/orders/route.ts`

#### 3.3 規劃測試案例

為每個測試檔案規劃測試案例：

**檔案**: `frontend/src/server/services/__tests__/order.test.ts`

1. **測試案例**: 成功建立訂單
    - **描述**: 當購買票券時，應該建立訂單並返回 order ID
    - **Input**:
      ```typescript
      const order ={
        eventId: 'event-123',
        tickets: [{ ticketTypeId: 'ticket-1', quantity: 2 }],
        customer: { email: 'test@example.com', name: '測試' }
      }
      ```
    - **Expected Output**:
      ```typescript
      const expectedOrder ={
        orderId: 'order-456',
        status: 'pending'
      }
      ```
    - **Mocks**:
        - `db.getTicketTypes()` → 回傳 `[{ id: 'ticket-1', price: 1000, inventory: 10 }]`
        - `db.insertOrder()` → 回傳 `{ id: 'order-456' }`
        - `payment.createPaymentIntent()` → 回傳 `{ id: 'pi_789' }`

2. **測試案例**: 庫存不足時拋出錯誤
    - **描述**: 當購買數量超過庫存時，應該拋出錯誤
    - **Input**:
      ```typescript
      {
        tickets: [{ ticketTypeId: 'ticket-1', quantity: 100 }]
      }
      ```
    - **Expected Output**:
      ```typescript
      throw new Error('庫存不足')
      ```
    - **Mocks**:
        - `db.getTicketTypes()` → 回傳 `[{ id: 'ticket-1', inventory: 10 }]`

3. **測試案例**: 支付失敗時回滾訂單
    - **描述**: 當支付失敗時，應該刪除已建立的訂單
    - **Input**: 同測試案例 1
    - **Expected Output**: 拋出支付錯誤
    - **Mocks**:
        - `db.getTicketTypes()` → 正常
        - `db.insertOrder()` → 正常
        - `payment.createPaymentIntent()` → 拋出錯誤
    - **驗證**: `db.deleteOrder()` 被呼叫

### 4. 輸出計畫

將分析結果輸出為結構化格式：

```markdown
## Gherkin Scenario: 使用者可以購買活動票券

### 測試檔案: frontend/src/server/services/__tests__/order.test.ts

#### 測試案例 1: 成功建立訂單

- **Input**: { eventId, tickets: [{ ticketTypeId, quantity: 2 }], customer }
- **Expected**: { orderId, status: 'pending' }
- **Mocks**: db.getTicketTypes, db.insertOrder, payment.createPaymentIntent

#### 測試案例 2: 庫存不足時拋出錯誤

- **Input**: { tickets: [{ quantity: 100 }] }
- **Expected**: throw Error('庫存不足')
- **Mocks**: db.getTicketTypes → inventory: 10

#### 測試案例 3: 支付失敗時回滾訂單

- **Input**: 同測試案例 1
- **Expected**: throw PaymentError
- **Verify**: db.deleteOrder called

### 實作順序

1. 測試案例 1（Happy path）
2. 測試案例 2（Error handling – 業務邏輯）
3. 測試案例 3（Error handling – 外部依賴）
```

### 5. 檢查 BDD Step Definitions 狀態

**IMPORTANT**: 在規劃階段就要檢查 BDD step definitions 的實作狀態。

**執行步驟**:

1. **找出對應的 steps 檔案**:
      ```json
   {
   "tool": "find_files_by_glob",
      "arguments": {
         "pattern": "e2e/tests/bdd-steps/*.steps.ts"
      }
   }
   ```


2. **檢查 stub 實作**:
      ```json
   {
      "tool": "search_in_files_by_text",
      "arguments": {
         "text": "// Stub",
         "include": "e2e/tests/bdd-steps/<feature-name>.steps.ts"
         }
   }
   ```


3. **識別需要實作的 steps**:
    - 列出所有包含 `// Stub:` 註解的 steps
    - 記錄每個 step 需要的功能

4. **在 plan 中加入 BDD step 實作規劃**:
   ```markdown
   ### BDD Step Definitions 待實作

   #### Step: `When I view the event {string}`
   - **需要的功能**: 事件詳情頁面
   - **需要的單元測試**:
     - `frontend/src/app/events/[slug]/__tests__/page.test.tsx`
     - `frontend/src/server/services/__tests__/event.test.ts`
   - **Step 實作**: 導航到事件頁面 + 驗證頁面加載

   #### Step: `Then I should see ticket type {string} with availability {int}`
   - **需要的功能**: 票種資訊顯示
   - **需要的單元測試**:
     - `frontend/src/components/__tests__/TicketTypeCard.test.tsx`
   - **Step 實作**: 驗證票種和庫存顯示正確
   ```

### 6. 提交給人類審查

在 plan mode 中，將計畫輸出給用戶：

- 詢問是否需要調整測試案例
- 確認 mocks 是否合理
- 確認測試順序是否正確
- **確認 BDD step 實作規劃是否完整**

### 7. 用戶確認後，退出 Plan Mode

```
/exitplan
```

## 常見問題

### Q: 如何決定測試案例的順序？

A: 優先順序如下：

1. Happy path（成功案例）
2. 業務邏輯 edge cases
3. 外部依賴失敗處理

### Q: 如何決定需要哪些 mocks？

A: 識別所有外部依賴：

- Database operations
- API calls
- Payment services
- Email services

### Q: 是否需要為每個 function 都寫測試？

A: 根據 Gherkin scenario 的需求決定，不要過度測試：

- ✅ 測試業務邏輯
- ✅ 測試錯誤處理
- ❌ 不測試 framework 本身（Next.js, Drizzle ORM）

### Q: 什麼時候應該實作 BDD step definitions？

A: 遵循 TDD 流程：

1. 先完成相關功能的**單元測試**（Red-Green-Refactor）
2. 確保功能邏輯正確後，再實作 **BDD step definition**
3. 最後執行 BDD scenario 驗證整體流程

**錯誤做法** ❌:

- 在功能未實作前就寫 BDD step（會導致 E2E 測試失敗）
- 用 stub 暫時通過 BDD 測試（無法真正驗證功能）

**正確做法** ✅:

- 單元測試 → 功能實作 → BDD step 實作 → BDD scenario 驗證

### Q: 如何確保 BDD scenario 真正完成？

A: 使用以下檢查清單：

- [ ] 所有單元測試通過
- [ ] 所有相關功能已實作
- [ ] **所有 BDD step definitions 實作完成（無 stub）**
- [ ] Gherkin scenario 可執行並通過
- [ ] Step definitions 有適當的 assertions

**驗證指令**:

檢查是否有未實作的 stub

```json
   {
  "tool": "search_in_files_by_text",
  "arguments": {
    "text": "// Stub",
    "include": "e2e/tests/bdd-steps/**"
  }
}
   ```

預期結果: 無任何輸出（所有 stub 都已移除）
