# 任務分解

## 自然語言解析流程

```
用戶輸入: "建立電商網站 MVP"
              ↓
┌─────────────────────────────────────────────────────────┐
│  Step 1: 意圖識別                                        │
│  • 類型: 軟體開發                                        │
│  • 規模: 中型專案                                        │
│  • 關鍵詞: 電商、MVP                                     │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  Step 2: 領域知識補充                                    │
│  • 電商 MVP 通常包含: 商品、購物車、結帳、用戶           │
│  • 技術選型建議（根據專案 context）                      │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  Step 3: 子目標分解                                      │
│  1. 用戶系統（註冊、登入）                               │
│  2. 商品管理（CRUD）                                     │
│  3. 購物車功能                                           │
│  4. 結帳流程                                             │
│  5. 訂單管理                                             │
└─────────────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────────────┐
│  Step 4: 依賴分析                                        │
│  • 用戶系統 → 獨立                                       │
│  • 商品管理 → 獨立                                       │
│  • 購物車 → 依賴 用戶系統 + 商品管理                     │
│  • 結帳 → 依賴 購物車                                    │
│  • 訂單 → 依賴 結帳                                      │
└─────────────────────────────────────────────────────────┘
```

## 分解原則

### 1. 可並行優先

將任務分解為最大可並行單元：

```
❌ 順序分解
Task 1 → Task 2 → Task 3 → Task 4

✅ 並行分解
┌─────────┬─────────┐
│ Task 1  │ Task 2  │  ← 可同時執行
└────┬────┴────┬────┘
     └────┬────┘
     ┌────┴────┐
     │ Task 3  │  ← 依賴 1+2
     └────┬────┘
     ┌────┴────┐
     │ Task 4  │  ← 依賴 3
     └─────────┘
```

### 2. 原子性

每個任務應該是：
- 可獨立完成
- 可獨立驗證
- 可獨立回滾

### 3. 明確完成標準

每個任務必須有：
- 輸入條件
- 輸出成果
- 驗證方法

## 任務結構

```yaml
task:
  id: "user-auth"
  name: "用戶認證系統"
  description: "實作註冊、登入、JWT 驗證"

  # 依賴
  depends_on: []
  blocks: ["shopping-cart", "checkout"]

  # 並行性
  parallelizable: true
  estimated_complexity: "medium"

  # 完成標準
  acceptance_criteria:
    - "註冊 API 回傳 201 + JWT"
    - "登入 API 驗證密碼並回傳 JWT"
    - "受保護路由需要有效 JWT"
    - "測試覆蓋率 > 80%"

  # 驗證命令
  verification:
    - "npm test -- --grep 'auth'"
    - "curl -X POST /api/register -d '...' | jq '.token'"
```

## 複雜度估算

| 等級 | 描述 | 預估 |
|------|------|------|
| trivial | 單一函數/配置 | < 30 min |
| low | 單一模組 | 30 min - 2 hr |
| medium | 多模組整合 | 2 - 8 hr |
| high | 架構變更 | 8+ hr |
| epic | 需要進一步分解 | 分解後再估 |

## 自動分解範例

### 輸入

```
"為這個 Express 專案加入 GraphQL API"
```

### 輸出

```yaml
plan:
  name: "GraphQL API 整合"
  tasks:
    - id: "setup"
      name: "環境設定"
      parallelizable: true
      subtasks:
        - "安裝 apollo-server-express"
        - "設定 TypeScript 支援"

    - id: "schema"
      name: "Schema 設計"
      parallelizable: true
      depends_on: ["setup"]
      subtasks:
        - "定義型別"
        - "設計 Query/Mutation"

    - id: "resolvers"
      name: "Resolver 實作"
      parallelizable: false  # 依序實作
      depends_on: ["schema"]
      subtasks:
        - "Query resolvers"
        - "Mutation resolvers"

    - id: "integration"
      name: "整合測試"
      depends_on: ["resolvers"]
      subtasks:
        - "撰寫整合測試"
        - "效能測試"
```
