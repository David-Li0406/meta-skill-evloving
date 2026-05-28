# MCP 進階設計模式詳解

**分析日期**: 2026-01-23
**涵蓋模式**: Full AI Processing、Progressive Discovery、Code Execution

---

## 一、Full AI Processing 模式

### 1.1 核心概念

**定義**：Server 端整合 AI API（如 OpenAI、Claude API），在 Server 內部完成資料分析和處理，只回傳最終結論給 Client。

```
┌─────────────────────────────────────────────────────────────┐
│                    Client (User/App)                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  request: get_document_summary(doc_id: "123")         │  │
│  │  response: "這份文件討論了三個主要議題..."             │  │
│  └───────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 MCP Server (Full AI Processing)              │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  1. 接收請求                                         │    │
│  │  2. 從資料庫讀取原始文件（可能 50,000+ tokens）      │    │
│  │  3. 調用 OpenAI API 進行分析                        │    │
│  │  4. 回傳精簡的分析結果（~500 tokens）               │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  需要配置：OPENAI_API_KEY、模型選擇、Prompt Engineering     │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 實作範例（Go）

```go
// Full AI Processing 模式的 MCP Tool
type DocumentSummaryTool struct {
    db       *Database
    aiClient *openai.Client  // Server 持有 AI Client
}

func (t *DocumentSummaryTool) Execute(ctx context.Context, req SummaryRequest) (*SummaryResponse, error) {
    // 1. 從資料庫讀取大量原始資料
    doc, err := t.db.GetDocument(ctx, req.DocID)
    if err != nil {
        return nil, err
    }

    // 2. Server 端調用 AI API 分析
    completion, err := t.aiClient.CreateChatCompletion(ctx, openai.ChatCompletionRequest{
        Model: "gpt-4",
        Messages: []openai.ChatCompletionMessage{
            {Role: "system", Content: "你是文件分析專家，請提供簡潔摘要。"},
            {Role: "user", Content: doc.Content},  // 大量資料只在 Server 端處理
        },
    })
    if err != nil {
        return nil, err
    }

    // 3. 只回傳精簡結果給 Client
    return &SummaryResponse{
        Summary:    completion.Choices[0].Message.Content,  // ~500 tokens
        KeyPoints:  extractKeyPoints(completion),
        Confidence: 0.95,
    }, nil
}
```

### 1.3 優缺點分析

| 優點 | 詳細說明 |
|------|---------|
| **節省 Client Context** | 50,000 tokens 的文件只回傳 500 tokens 摘要 |
| **一致的分析品質** | 可控制 AI 模型版本、prompt，確保輸出穩定 |
| **支援離線查詢** | 可預先批次處理，快取分析結果 |
| **適合大資料集** | Server 可利用高效能運算資源 |
| **安全性** | 敏感資料不需傳到 Client 端 AI |

| 缺點 | 詳細說明 |
|------|---------|
| **額外 API 成本** | 每次分析都產生 AI API 費用 |
| **需管理 API Key** | Server 端敏感資訊管理負擔 |
| **分析邏輯固化** | 修改 prompt 或模型需重新部署 |
| **延遲增加** | 多一層 AI API 呼叫 |
| **複雜度高** | 需處理 AI API 的錯誤、rate limit、fallback |

### 1.4 適用場景

```
✅ 適合：
├── 企業級應用（需要一致性和安全性）
├── 大量資料的批次處理（ETL pipeline）
├── 敏感資料分析（不能傳到 Client）
├── 需要特定模型/prompt 的專業分析
└── 非對話式的背景處理任務

❌ 不適合：
├── 個人工具（成本考量）
├── 需要靈活調整分析邏輯的場景
├── 預算有限的專案
└── 本地優先的隱私敏感應用
```

### 1.5 與 Data Tools 模式對比

```
                    Data Tools                Full AI Processing
                    ──────────                ──────────────────
AI 處理位置         Client (Claude)           Server (OpenAI/etc)

MCP Server 回傳：
Data Tools:                          Full AI Processing:
{                                    {
  "entries": [...大量資料...],         "summary": "簡潔結論",
  "stats": {...}                       "confidence": 0.95
}                                    }
(Client Claude 自己分析)              (已分析完成)

Token 消耗: 高                       Token 消耗: 低
API 成本: 零                         API 成本: 每次都產生
彈性: 高                             彈性: 低
```

---

## 二、Progressive Discovery 模式（Strata Pattern）

### 2.1 核心概念

**定義**：分層揭露 Tool 資訊，讓 AI Agent 逐步縮小範圍，避免一次載入所有 Tool 定義造成 Context Window 爆炸。

**解決的問題**：
> 當你暴露更多 Tools 給 AI Agent，效能會下降。銷售 AI 可能在處理簡單的「獲取所有潛在客戶」任務時掙扎，同時燒掉昂貴的 tokens 處理不相關的 Tool 描述。

```
傳統模式：一次載入所有 Tool 定義
┌─────────────────────────────────────────────────────────────────┐
│  Context Window                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Tool 1: create_user(name, email, role, department, ...)    │ │
│  │ Tool 2: update_user(id, name, email, role, ...)            │ │
│  │ ... 還有 95 個 Tools ...                                    │ │
│  │ Tool 100: generate_report(type, range, format, ...)        │ │
│  └────────────────────────────────────────────────────────────┘ │
│  ❌ 大量 tokens 浪費在不相關的 Tool 定義                         │
└─────────────────────────────────────────────────────────────────┘

Progressive Discovery：分層按需載入
┌─────────────────────────────────────────────────────────────────┐
│  Stage 1: 只載入類別                                             │
│  │ discover_categories() → ["users", "orders", "reports"]       │
│                              ↓ Agent 選擇 "users"               │
│  Stage 2: 載入該類別的動作名稱                                   │
│  │ get_actions("users") → ["create", "update", "delete"]        │
│                              ↓ Agent 選擇 "create"              │
│  Stage 3: 載入完整參數 Schema                                    │
│  │ get_action_details("users.create") → { full JSON schema }    │
│  ✅ 只載入需要的 Tool 定義                                       │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 四階段流程

```
Stage 1: discover_server_categories()
──────────────────────────────────────
輸入: 無
輸出: ["user_management", "order_processing", "reporting"]
Token 成本: ~50 tokens

                    ↓

Stage 2: get_category_actions(category)
───────────────────────────────────────
輸入: "user_management"
輸出: [
  { "name": "create_user", "desc": "建立新用戶" },
  { "name": "update_user", "desc": "更新用戶資料" },
  { "name": "delete_user", "desc": "刪除用戶" }
]
Token 成本: ~100 tokens（無完整 schema）

                    ↓

Stage 3: get_action_details(action_name)
────────────────────────────────────────
輸入: "create_user"
輸出: {
  "name": "create_user",
  "description": "建立新用戶帳號",
  "inputSchema": {
    "type": "object",
    "properties": {
      "name": { "type": "string" },
      "email": { "type": "string", "format": "email" },
      "role": { "enum": ["admin", "user", "guest"] }
    },
    "required": ["name", "email"]
  }
}
Token 成本: ~200 tokens（完整 schema）

                    ↓

Stage 4: execute_action(action_name, params)
────────────────────────────────────────────
輸入: "create_user", { "name": "John", "email": "..." }
輸出: { "id": "usr_123", "status": "created" }
```

### 2.3 實作範例（Go）

```go
// Progressive Discovery MCP Server

type ProgressiveServer struct {
    categories map[string]Category
}

// Stage 1: 發現類別
func (s *ProgressiveServer) DiscoverCategories(ctx context.Context) ([]CategoryInfo, error) {
    var result []CategoryInfo
    for name, cat := range s.categories {
        result = append(result, CategoryInfo{
            Name:        name,
            Description: cat.Description,
            ActionCount: len(cat.Actions),
        })
    }
    return result, nil  // 只回傳名稱和描述，不回傳 schema
}

// Stage 2: 獲取類別內的動作列表
func (s *ProgressiveServer) GetCategoryActions(ctx context.Context, category string) ([]ActionInfo, error) {
    cat, ok := s.categories[category]
    if !ok {
        return nil, fmt.Errorf("category %s not found", category)
    }

    var result []ActionInfo
    for name, action := range cat.Actions {
        result = append(result, ActionInfo{
            Name:        name,
            Description: action.Description,
            // 注意：不包含 Schema！
        })
    }
    return result, nil
}

// Stage 3: 獲取特定動作的完整定義
func (s *ProgressiveServer) GetActionDetails(ctx context.Context, category, action string) (*ActionDetails, error) {
    cat := s.categories[category]
    act := cat.Actions[action]

    return &ActionDetails{
        Name:        act.Name,
        Description: act.Description,
        InputSchema: act.Schema,  // 此時才回傳完整 Schema
    }, nil
}

// Stage 4: 執行動作
func (s *ProgressiveServer) ExecuteAction(ctx context.Context, category, action string, params any) (any, error) {
    cat := s.categories[category]
    act := cat.Actions[action]
    return act.Handler(ctx, params)
}
```

### 2.4 Token 效率對比

```
場景：100 個 Tools，每個 Tool 的 Schema 約 200 tokens

傳統模式：
  載入所有 Tools = 100 × 200 = 20,000 tokens
  每次對話都消耗這些 tokens

Progressive Discovery：
  Stage 1: ~50 tokens   (類別列表)
  Stage 2: ~100 tokens  (動作列表)
  Stage 3: ~200 tokens  (單一 Schema)
  ──────────────────────
  總計:   ~350 tokens   (98% 減少！)
```

### 2.5 優缺點分析

| 優點 | 詳細說明 |
|------|---------|
| **解決 Tool 過多問題** | 避免 100+ Tools 導致的效能下降 |
| **大幅減少 Context 佔用** | 只載入需要的 Tool 定義 |
| **更好的 Tool 選擇** | 分階段縮小範圍，減少 hallucination |
| **動態擴展** | 新增 Tools 不影響現有效能 |

| 缺點 | 詳細說明 |
|------|---------|
| **增加呼叫次數** | 需要 3-4 次呼叫才能執行一個動作 |
| **實作複雜度高** | 需設計良好的分層結構 |
| **不適合簡單場景** | 10 個以下 Tools 時 overhead 大於收益 |
| **需要 AI 配合** | Agent 需理解分層探索流程 |

### 2.6 適用場景

```
✅ 適合：
├── 企業級多功能 MCP Server（100+ Tools）
├── 需要智能 Tool 選擇的複雜系統
├── 多租戶系統（不同用戶看到不同 Tools）
└── 動態 Tool 註冊的平台

❌ 不適合：
├── 小型專案（< 20 Tools）
├── 簡單的單一用途 Server
├── 需要最低延遲的場景
└── AI Agent 能力有限時
```

---

## 三、Code Execution 模式

### 3.1 核心概念

**定義**：Agent 不直接呼叫 MCP Tools，而是撰寫程式碼（TypeScript/JavaScript/Python）來操作 Tools，資料處理在執行環境中完成，只有最終結果回傳給 Model。

**來源**：Anthropic 於 2025 年提出的 "Code Execution with MCP"

### 3.2 傳統 vs Code Execution 對比

```
傳統 Tool Calling 模式：

  Model ──┬── call tool_1() ──→ result_1 (5,000 tokens) ──┐
          │                                                │
          │   ← 回傳 Model，消耗 Context ←─────────────────┘
          │
          ├── call tool_2(result_1) ──→ result_2 (3,000 tokens)
          │   ← 回傳 Model，消耗 Context ←─────────────────┘
          │
          └── ... 重複 10 次 ...

  總計：~150,000 tokens（每次結果都經過 Model）


Code Execution 模式：

  Model ──→ 生成程式碼 ──→ 執行環境
                            │
          ┌─────────────────┴─────────────────┐
          │  // 在執行環境中處理               │
          │  const data1 = await mcp.tool_1() │
          │  const data2 = await mcp.tool_2() │
          │  const filtered = data1.filter()  │
          │  const result = summarize(merged) │
          │  return result  // 只回傳最終結果 │
          └─────────────────┬─────────────────┘
                            │
                            ▼
  Model ←── 只收到精簡結果 (~2,000 tokens) ←──┘

  總計：~2,000 tokens（98.7% 減少！）
```

### 3.3 系統架構

```
┌─────────────────────────────────────────────────────────────────┐
│                        AI Agent (Claude)                         │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  理解任務 → 撰寫程式碼 → 等待執行結果 → 繼續對話          │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │ 傳送程式碼
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Code Execution Environment                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  • 安全沙箱（Sandboxed Runtime）                          │  │
│  │  • 支援 TypeScript / JavaScript / Python                  │  │
│  │  • MCP Client SDK 內建                                    │  │
│  │  • 可存取本地檔案系統（受限）                             │  │
│  └───────────────────────────────────────────────────────────┘  │
│                            │                                     │
│                            │ MCP Protocol                        │
│                            ▼                                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                    MCP Servers                             │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │  │
│  │  │ Files   │  │ Database│  │ API     │  │ Custom  │      │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.4 實作範例

**傳統 Tool Calling（對比用）**：

```typescript
// 傳統方式：每個步驟都要 Model 參與

// Step 1: Model 決定呼叫 get_orders
const orders = await mcp.call('get_orders', { limit: 1000 });
// → 1000 筆資料傳回 Model（~30,000 tokens）

// Step 2: Model 分析後決定呼叫 get_products
const products = await mcp.call('get_products', { ids: productIds });
// → 產品資料傳回 Model（~10,000 tokens）

// Step 3: Model 分析後決定呼叫 get_categories
const categories = await mcp.call('get_categories', { ids: categoryIds });
// → 類別資料傳回 Model（~5,000 tokens）

// 總計：~45,000+ tokens，多次 Model 往返
```

**Code Execution 方式**：

```typescript
// Code Execution：Model 生成一段程式碼，一次執行完成

async function analyzeOrdersByCategory() {
  // 所有資料處理都在執行環境中完成
  const orders = await mcp.call('db', 'get_orders', { limit: 1000 });
  const productIds = [...new Set(orders.map(o => o.product_id))];

  const products = await mcp.call('db', 'get_products', { ids: productIds });
  const productMap = new Map(products.map(p => [p.id, p]));

  const categoryIds = [...new Set(products.map(p => p.category_id))];
  const categories = await mcp.call('db', 'get_categories', { ids: categoryIds });
  const categoryMap = new Map(categories.map(c => [c.id, c]));

  // 複雜的資料處理邏輯
  const analysis = orders.reduce((acc, order) => {
    const product = productMap.get(order.product_id);
    const category = categoryMap.get(product?.category_id);
    const categoryName = category?.name || 'Unknown';

    if (!acc[categoryName]) {
      acc[categoryName] = { count: 0, revenue: 0, products: new Set() };
    }
    acc[categoryName].count++;
    acc[categoryName].revenue += order.amount;
    acc[categoryName].products.add(order.product_id);

    return acc;
  }, {});

  // 只回傳精簡的分析結果
  return Object.entries(analysis)
    .map(([name, data]) => ({
      category: name,
      orderCount: data.count,
      totalRevenue: data.revenue,
      uniqueProducts: data.products.size
    }))
    .sort((a, b) => b.totalRevenue - a.totalRevenue);
}

// 回傳給 Model：~500 tokens（vs 45,000+ tokens）
```

**複雜流程控制**：

```typescript
// Code Execution 的強大之處：迴圈、條件、錯誤處理

async function processAllCustomers() {
  const customers = await mcp.call('crm', 'list_customers', { status: 'active' });
  const results = [];

  for (const customer of customers) {
    try {
      // 條件邏輯
      if (customer.tier === 'enterprise') {
        const usage = await mcp.call('billing', 'get_usage', { id: customer.id });
        const forecast = await mcp.call('analytics', 'forecast', {
          customerId: customer.id,
          months: 3
        });

        if (usage.current > usage.limit * 0.8) {
          // 自動發送警告
          await mcp.call('notifications', 'send', {
            to: customer.email,
            template: 'usage_warning',
            data: { usage, forecast }
          });
          results.push({ customer: customer.id, action: 'warned' });
        }
      }
    } catch (error) {
      // 錯誤處理
      results.push({ customer: customer.id, error: error.message });
    }
  }

  return {
    processed: customers.length,
    actions: results.filter(r => r.action).length,
    errors: results.filter(r => r.error).length,
    details: results
  };
}
```

### 3.5 優缺點分析

| 優點 | 詳細說明 |
|------|---------|
| **極致 Token 節省** | 98%+ 的減少，大幅降低成本 |
| **原生控制流** | 迴圈、條件、try-catch 自然表達 |
| **減少 Model 往返** | 一次生成程式碼，一次執行完成 |
| **按需載入 Tools** | 程式碼中 import 需要的，不預載所有定義 |
| **更好的錯誤處理** | 程式碼層級的錯誤捕獲和恢復 |
| **可組合性** | 函數可重用、模組化 |
| **減少延遲** | 避免多次 Model「思考」時間 |

| 缺點 | 詳細說明 |
|------|---------|
| **需要執行環境** | 如 Claude Code、Codex、自建沙箱 |
| **安全性考量** | 執行任意程式碼的風險 |
| **AI 需寫程式能力** | 不適合簡單的 AI Agent |
| **除錯較困難** | 程式碼錯誤可能難以追蹤 |
| **不適合簡單任務** | 單一 Tool 呼叫有 overhead |
| **學習曲線** | 需要理解新的開發模式 |

### 3.6 安全性設計

```
┌─────────────────────────────────────────────────────────────────┐
│                    Security Sandbox Design                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   Sandboxed Runtime                      │    │
│  │  • 受限的檔案系統存取                                    │    │
│  │  • 網路請求白名單                                        │    │
│  │  • 執行時間限制                                          │    │
│  │  • 記憶體限制                                            │    │
│  │  • 禁止系統呼叫                                          │    │
│  │  • 只能透過 MCP 存取外部資源                             │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  允許：                                                          │
│  ✅ 資料處理和轉換                                              │
│  ✅ 透過 MCP 呼叫已授權的 Tools                                 │
│  ✅ 本地運算（排序、過濾、聚合）                                │
│                                                                  │
│  禁止：                                                          │
│  ❌ 直接網路請求（繞過 MCP）                                    │
│  ❌ 檔案系統寫入（除指定目錄）                                  │
│  ❌ 執行系統命令                                                │
│  ❌ 存取環境變數和敏感資訊                                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3.7 生態系統支援（2025-2026）

| 平台 | 支援狀態 | 說明 |
|------|---------|------|
| **Claude Code** | ✅ 官方推薦 | Anthropic 原生支援 |
| **ChatGPT Dev Mode** | ✅ 支援 | OpenAI 官方 MCP Client |
| **Gemini CLI** | ✅ 支援 | FastMCP 整合 |
| **Cursor** | ✅ 支援 | IDE 內建 |
| **自建環境** | ✅ 可行 | 使用 mcp-agent 等框架 |

### 3.8 適用場景

```
✅ 強烈推薦：
├── 多步驟資料處理流程
├── 需要迴圈處理大量項目
├── 複雜的條件分支邏輯
├── ETL 類型的資料轉換
├── 批次操作（如批次更新、批次通知）
└── 需要錯誤處理和重試邏輯

⚠️ 視情況：
├── 中等複雜度的 3-5 步驟任務
├── 需要即時互動的場景
└── 安全性要求極高的環境

❌ 不推薦：
├── 單一 Tool 呼叫
├── 簡單的 Q&A 場景
├── 沒有執行環境的情況
└── AI Agent 程式能力有限
```

---

## 四、三種模式效率對比

### 4.1 Token 效率矩陣

| 場景 | Traditional | Data Tools | Full AI | Progressive | Code Exec |
|------|-------------|------------|---------|-------------|-----------|
| 單一 Tool 呼叫 | 1x | 1x | 0.5x | 1.5x | 1.2x |
| 3 步驟工作流程 | 3x | 3x | 1x | 2.5x | 0.5x |
| 10 步驟工作流程 | 10x | 10x | 2x | 8x | 0.3x |
| 迴圈處理 100 項目 | 100x | 100x | N/A | N/A | 0.1x |
| 100+ Tools 系統 | 100x | 100x | 100x | 3x | 3x |

### 4.2 模式選擇決策樹

```
                        開始
                          │
          ┌───────────────┴───────────────┐
          │ Tools 數量超過 50 個嗎？       │
          └───────────────┬───────────────┘
                  ↙ No          Yes ↘
                  │           考慮 Progressive
                  │           Discovery
                  ↓
          ┌───────────────────────────────┐
          │ 任務涉及多步驟資料處理嗎？     │
          └───────────────┬───────────────┘
                  ↙ No          Yes ↘
                  │           ┌──────────┐
                  │           │有執行環境?│
                  │           └────┬─────┘
                  │         ↙ No    Yes ↘
                  │    Full AI    Code Execution
                  │    Processing    (最佳)
                  ↓
          ┌───────────────────────────────┐
          │ 需要 Server 端 AI 處理嗎？     │
          └───────────────┬───────────────┘
                  ↙ No          Yes ↘
           Data Tools      Full AI Processing
           (最簡單)        (一致性分析)
```

---

## 五、模式組合建議

### 5.1 常見組合

| 組合 | 適用場景 | 複雜度 |
|------|---------|--------|
| Data Tools only | 個人工具、小型專案 | ⭐ |
| Progressive + Data Tools | 中型系統、多功能工具 | ⭐⭐⭐ |
| Full AI only | 企業批次處理 | ⭐⭐ |
| Progressive + Full AI | 企業級大規模系統 | ⭐⭐⭐⭐ |
| Code Exec + Any | 需要極致優化的複雜流程 | ⭐⭐⭐ |

### 5.2 混合架構範例

```
Progressive Discovery + Full AI Processing + Code Execution

1. Agent 透過 Progressive Discovery 找到需要的 Tool
   └── discover → "analytics" → "generate_insights"

2. 該 Tool 內部使用 Full AI Processing
   └── Server 調用 AI API 分析大量資料

3. 多個 Tools 組合時使用 Code Execution
   └── Agent 寫程式碼串接多個分析結果

效果：
- Tool 發現階段：最小 token 消耗（Progressive）
- 單一分析階段：Server 端處理（Full AI）
- 組合階段：Client 端優化（Code Exec）
```

---

## 六、關鍵學習總結

| 模式 | 核心價值 | 最佳場景 | 主要限制 |
|------|---------|---------|---------|
| **Full AI Processing** | 節省 Client Context | 大資料批次處理 | API 成本 |
| **Progressive Discovery** | 解決 Tool 過多問題 | 100+ Tools 系統 | 實作複雜 |
| **Code Execution** | 98%+ Token 節省 | 多步驟資料處理 | 需執行環境 |

**2026 年趨勢**：
1. Code Execution 快速成為主流
2. 混合模式越來越常見
3. Progressive Discovery 在企業端普及

---

## 參考資源

- [Code Execution with MCP - Anthropic](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [Less is More: MCP Design Patterns - Klavis AI](https://www.klavis.ai/blog/less-is-more-mcp-design-patterns-for-ai-agents)
- [MCP Best Practices](https://modelcontextprotocol.info/docs/best-practices/)
- [15 Best Practices for MCP Servers - The New Stack](https://thenewstack.io/15-best-practices-for-building-mcp-servers-in-production/)
