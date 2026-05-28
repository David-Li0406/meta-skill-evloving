# MCP Server 設計模式完整比較報告

**分析日期**: 2026-01-23
**研究重點**: MCP Data Tools 模式與其他設計模式的比較

---

## 一、MCP 設計模式總覽

根據研究，MCP Server 的設計模式可分為以下幾大類：

```
┌─────────────────────────────────────────────────────────────────┐
│                    MCP Server 設計模式                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐     │
│  │ Data Tools    │   │ Full AI       │   │ Workflow-     │     │
│  │ 模式          │   │ Processing    │   │ Based 模式    │     │
│  │ (Client AI)   │   │ 模式          │   │               │     │
│  └───────────────┘   │ (Server AI)   │   └───────────────┘     │
│                      └───────────────┘                          │
│                                                                  │
│  ┌───────────────┐   ┌───────────────┐   ┌───────────────┐     │
│  │ Code          │   │ Progressive   │   │ Gateway       │     │
│  │ Execution     │   │ Discovery     │   │ 模式          │     │
│  │ 模式          │   │ (Strata)      │   │               │     │
│  └───────────────┘   └───────────────┘   └───────────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 二、六大設計模式詳解

### 2.1 Data Tools 模式（Knowledge Nexus 採用）

**核心理念**：Server 只提供結構化資料，讓 Client 端的 AI（如 Claude）做分析和決策。

```
┌─────────────────────────────────────────────┐
│              Claude Code (Client)            │
│  ┌─────────────────────────────────────┐   │
│  │  1. 調用 get_pending_knowledge       │   │
│  │  2. 收到 raw structured data         │   │
│  │  3. Claude 自己分析、生成洞察        │   │
│  │  4. 調用 update_summary 儲存結果     │   │
│  └─────────────────────────────────────┘   │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│           MCP Server (Data Provider)         │
│  - 只負責 CRUD 操作                          │
│  - 不調用任何外部 AI API                     │
│  - 回傳結構化資料供 Client 分析              │
└─────────────────────────────────────────────┘
```

**優點**：
| 優勢 | 說明 |
|------|------|
| 零額外 API 成本 | 利用現有的 Claude 對話能力 |
| 無需管理 API Key | Server 端無敏感資訊 |
| 更靈活的分析 | Claude 可根據上下文調整分析方式 |
| 即時迭代 | 不需修改 Server 就能改變分析邏輯 |
| 本地優先 | 所有資料和處理都在本地 |

**缺點**：
| 劣勢 | 說明 |
|------|------|
| Context Window 消耗 | 大量資料需傳入 Claude |
| 依賴 Client AI 能力 | 分析品質取決於 Client AI |
| 無法離線處理 | 需要 AI 對話才能完成分析 |

**適用場景**：
- 個人知識管理工具
- 本地優先的應用程式
- 需要靈活分析邏輯的場景
- 小型到中型資料集

---

### 2.2 Full AI Processing 模式（傳統模式）

**核心理念**：Server 端調用 AI API 完成分析，回傳處理後的結果。

```
┌─────────────────────────────────────────────┐
│              Client (User/App)               │
│  ┌─────────────────────────────────────┐   │
│  │  1. 調用 get_insights()              │   │
│  │  2. 收到 AI 已分析的結論             │   │
│  │  3. 直接使用結果                     │   │
│  └─────────────────────────────────────┘   │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│        MCP Server (AI Processing)            │
│  ┌─────────────────────────────────────┐   │
│  │  1. 收到請求                         │   │
│  │  2. 調用 OpenAI/Claude API           │   │
│  │  3. 處理並回傳分析結果               │   │
│  └─────────────────────────────────────┘   │
│  - 需要 API Key 配置                        │
│  - 產生額外 API 費用                        │
└─────────────────────────────────────────────┘
```

**優點**：
| 優勢 | 說明 |
|------|------|
| 節省 Context Window | Client 只收到處理後的結果 |
| 一致的分析品質 | 可控制使用的 AI 模型和 prompt |
| 支援離線查詢 | 可預先處理並快取結果 |
| 適合大資料集 | Server 端可批次處理 |

**缺點**：
| 劣勢 | 說明 |
|------|------|
| 額外 API 成本 | 每次分析都產生費用 |
| 需管理 API Key | 安全性和配置負擔 |
| 分析邏輯固化 | 修改需重新部署 Server |
| 延遲增加 | 多一層 API 呼叫 |

**適用場景**：
- 企業級應用
- 大量資料的批次處理
- 需要一致性分析結果的場景
- 非對話式的背景處理任務

---

### 2.3 Workflow-Based 模式

**核心理念**：Tool 封裝完整工作流程，而非單一 API 操作。

```
傳統 API Mirror 模式：
  Client → create_record() → update_record() → notify() → ...
  (多次呼叫，高 token 消耗)

Workflow-Based 模式：
  Client → complete_onboarding_workflow()
  (單次呼叫，內部處理所有步驟)
```

**Vercel 團隊觀點**：
> "Think of MCP tools as tailored toolkits that help an AI achieve a particular task, not as API mirrors."

**優點**：
| 優勢 | 說明 |
|------|------|
| 大幅減少 Token 消耗 | 單次呼叫完成多步驟 |
| 更可靠的執行 | 減少失敗點 |
| 易於 AI 理解 | 語意清晰的工作流程 |
| 更好的用戶體驗 | 對話式回應 |

**缺點**：
| 劣勢 | 說明 |
|------|------|
| 彈性較低 | 工作流程固定 |
| 開發成本高 | 需預先設計工作流程 |
| 不適合探索性任務 | 非預定義場景難處理 |

**適用場景**：
- 定義良好的重複性工作流程
- 生產環境的特定用例
- 需要高可靠性的關鍵任務

---

### 2.4 Code Execution 模式（Anthropic 2025 提出）

**核心理念**：Agent 撰寫程式碼來操作 MCP Tools，而非直接呼叫。

```
傳統 Tool Calling：
  150,000 tokens（每次結果都經過 Model）

Code Execution Pattern：
  2,000 tokens（98.7% 減少）
```

```
┌─────────────────────────────────────────────┐
│              AI Agent                        │
│  ┌─────────────────────────────────────┐   │
│  │  // Agent 撰寫的程式碼               │   │
│  │  const data = await mcp.getData()    │   │
│  │  const filtered = data.filter(...)   │   │
│  │  const result = process(filtered)    │   │
│  │  return summary(result)              │   │
│  └─────────────────────────────────────┘   │
│  - 資料處理在執行環境中完成                 │
│  - 只有最終結果回傳 Model                   │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│           MCP Server (as Code API)           │
└─────────────────────────────────────────────┘
```

**優點**：
| 優勢 | 說明 |
|------|------|
| 極大 Token 節省 | 98%+ 的減少 |
| 更強的控制流 | 迴圈、條件、錯誤處理 |
| 減少延遲 | 避免多次 Model 往返 |
| 按需載入 Tools | 不預載所有定義 |

**缺點**：
| 劣勢 | 說明 |
|------|------|
| 需要 Code 執行環境 | 如 Claude Code |
| 安全性考量 | 程式碼執行風險 |
| AI 需要寫程式能力 | 不適合簡單 Agent |

**適用場景**：
- 大型資料處理任務
- 複雜的多步驟工作流程
- 需要極致 Token 優化的場景
- Claude Code 等開發環境

---

### 2.5 Progressive Discovery 模式（Strata Pattern）

**核心理念**：分層揭露 Tool 資訊，避免一次載入所有定義。

```
Stage 1: discover_server_categories()
  → 識別相關服務類別

Stage 2: get_category_actions()
  → 獲取動作名稱（無完整 schema）

Stage 3: get_action_details()
  → 選定動作後才獲取完整參數定義

Stage 4: execute_action()
  → 執行操作
```

**優點**：
| 優勢 | 說明 |
|------|------|
| 解決 Tool 過多問題 | 避免效能下降 |
| 減少 Context 佔用 | 按需載入定義 |
| 更好的 Tool 選擇 | 分階段縮小範圍 |

**缺點**：
| 劣勢 | 說明 |
|------|------|
| 增加呼叫次數 | 多階段請求 |
| 實作複雜度高 | 需設計分層結構 |
| 不適合簡單場景 | Overhead 可能大於收益 |

**適用場景**：
- 企業級多功能 MCP Server
- 數百個 Tools 的大型系統
- 需要智能 Tool 選擇的場景

---

### 2.6 Gateway 模式

**核心理念**：統一的反向代理層，管理多個 MCP Server。

```
┌─────────────────────────────────────────────┐
│              AI Agent                        │
└───────────────────┬─────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────┐
│           MCP Gateway                        │
│  - Session State 管理                        │
│  - Context 傳播                              │
│  - 路由和負載均衡                            │
│  - 認證和授權                                │
└─────┬──────────┬──────────┬─────────────────┘
      │          │          │
      ▼          ▼          ▼
┌─────────┐ ┌─────────┐ ┌─────────┐
│ MCP     │ │ MCP     │ │ MCP     │
│ Server  │ │ Server  │ │ Server  │
│ A       │ │ B       │ │ C       │
└─────────┘ └─────────┘ └─────────┘
```

**優點**：
| 優勢 | 說明 |
|------|------|
| 統一接入點 | 簡化 Agent 連接 |
| 跨 Tool Session 管理 | 維護上下文 |
| 集中安全控制 | OAuth、認證 |
| 可觀測性 | 統一監控和日誌 |

**適用場景**：
- 企業級多服務架構
- 需要跨 Tool 狀態管理
- 複雜的安全需求

---

## 三、模式對比矩陣

| 模式 | Token 效率 | 實作複雜度 | 適用規模 | AI 依賴位置 | 成本 |
|------|-----------|-----------|---------|------------|------|
| **Data Tools** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 小-中 | Client | 低 |
| **Full AI Processing** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 中-大 | Server | 高 |
| **Workflow-Based** | ⭐⭐⭐⭐ | ⭐⭐⭐ | 中 | Mixed | 中 |
| **Code Execution** | ⭐⭐⭐⭐⭐ | ⭐⭐ | 大 | Client | 低 |
| **Progressive Discovery** | ⭐⭐⭐⭐ | ⭐⭐ | 大 | N/A | 低 |
| **Gateway** | ⭐⭐⭐ | ⭐ | 企業 | Mixed | 中-高 |

---

## 四、狀態管理：Stateful vs Stateless

### Stateful 架構

```go
// Server 維護 Session
type Session struct {
    ID        string
    Context   map[string]any
    StartedAt time.Time
}
```

**優點**：多步驟工作流程、對話連續性
**缺點**：難以水平擴展、Server affinity 問題

### Stateless 架構

```go
// 每個請求自包含
type Request struct {
    Data      any
    Context   map[string]any  // 完整上下文由 Client 傳入
}
```

**優點**：易於擴展、Serverless 友好
**缺點**：複雜的狀態需外部儲存

### 混合架構（推薦）

```
Resource State → Database（持久化）
Session State  → Cache/Memory（短暫）
```

---

## 五、Data Tools 模式的定位分析

### 與其他模式的關係

```
                    AI 處理位置
                    ↑
    Full AI         │         Hybrid
    Processing      │         (Workflow)
    (Server AI)     │
                    │
    ────────────────┼────────────────→ Token 效率
                    │
    Data Tools      │         Code
    (Client AI)     │         Execution
                    │
```

### Data Tools 的獨特價值

1. **零成本 AI 分析** — 利用現有 Claude 對話
2. **最大彈性** — 分析邏輯可即時調整
3. **隱私優先** — 資料不需傳到外部 AI API
4. **簡單實作** — Server 只需 CRUD，無 AI 邏輯

### 何時選擇 Data Tools

| 場景 | 推薦模式 |
|------|---------|
| 個人工具、本地優先 | ✅ Data Tools |
| 需要離線處理 | ❌ Full AI Processing |
| 大量資料批次處理 | ❌ Code Execution |
| 企業級、一致性分析 | ❌ Full AI Processing |
| 開發者工具（如 Claude Code） | ✅ Data Tools |
| 需要快速迭代分析邏輯 | ✅ Data Tools |

---

## 六、Knowledge Nexus 的模式選擇評價

### 設計合理性：⭐⭐⭐⭐⭐

Knowledge Nexus 選擇 Data Tools 模式非常適合其定位：

1. **個人知識管理** — 小型資料集，Client AI 足夠處理
2. **本地優先** — 無需外部 API，隱私保障
3. **Claude Code 整合** — 完美利用現有 AI 能力
4. **零額外成本** — 不增加使用者負擔

### 可改進方向

1. **大型回應處理** — 已實作 50KB 限制 + 檔案落地 ✅
2. **考慮 Hybrid** — 對於頻繁查詢的洞察，可預先計算
3. **Progressive Discovery** — 當 Tools 增多時可考慮

---

## 七、綜合建議

### 選擇模式的決策樹

```
                    開始
                      │
        ┌─────────────┴─────────────┐
        │ 是否需要 Server 端 AI？    │
        └─────────────┬─────────────┘
              ↙ No          Yes ↘
    ┌────────────┐      ┌────────────┐
    │資料量大嗎？ │      │需要一致性？ │
    └──────┬─────┘      └──────┬─────┘
      ↙ No   Yes ↘        ↙ No  Yes ↘
  Data     Code        Workflow   Full AI
  Tools    Execution   Based      Processing
```

### 2026 年趨勢

1. **Code Execution** 快速普及（Claude Code、ChatGPT Dev Mode）
2. **Data Tools** 在個人工具領域成為主流
3. **Gateway** 架構在企業端成熟
4. **混合模式** 越來越常見

---

## 參考資源

- [MCP Architecture - Official](https://modelcontextprotocol.io/specification/2025-06-18/architecture)
- [Less is More: MCP Design Patterns - Klavis AI](https://www.klavis.ai/blog/less-is-more-mcp-design-patterns-for-ai-agents)
- [Code Execution with MCP - Anthropic](https://www.anthropic.com/engineering/code-execution-with-mcp)
- [MCP Best Practices](https://modelcontextprotocol.info/docs/best-practices/)
- [MCP Gateways Guide - Composio](https://composio.dev/blog/mcp-gateways-guide)
- [Serverless MCP - Workato](https://www.workato.com/the-connector/serverless-mcp-for-enterprise-ai-tools/)
- [15 Best Practices for MCP Servers - The New Stack](https://thenewstack.io/15-best-practices-for-building-mcp-servers-in-production/)

---

## 關鍵學習

1. **Data Tools 模式** — 適合本地優先、個人工具、Claude Code 整合場景
2. **Code Execution 模式** — Token 優化的未來趨勢，98%+ 節省
3. **Workflow-Based 模式** — 生產環境的可靠選擇
4. **沒有最佳模式** — 根據場景選擇，混合使用是常態
