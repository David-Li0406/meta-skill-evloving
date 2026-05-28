# MCP Server 開發最佳實踐和指南

## 概述

本文件彙編了建立 Model Context Protocol (MCP) server 的基本最佳實踐和指南。它涵蓋命名慣例、工具設計、回應格式、分頁、錯誤處理、安全性和合規性要求。

---

## 快速參考

### Server 命名
- **Python**:`{service}_mcp`(例如,`slack_mcp`)
- **Node/TypeScript**:`{service}-mcp-server`(例如,`slack-mcp-server`)

### 工具命名
- 使用 snake_case 與服務前綴
- 格式:`{service}_{action}_{resource}`
- 範例:`slack_send_message`、`github_create_issue`

### 回應格式
- 支援 JSON 和 Markdown 格式
- JSON 用於程式化處理
- Markdown 用於人類可讀性

### 分頁
- 始終遵守 `limit` 參數
- 返回 `has_more`、`next_offset`、`total_count`
- 預設為 20-50 項

### 字元限制
- 設定 CHARACTER_LIMIT 常數(通常為 25,000)
- 優雅地截斷並提供清晰訊息
- 提供過濾指導

---

## 目錄
1. Server 命名慣例
2. 工具命名和設計
3. 回應格式指南
4. 分頁最佳實踐
5. 字元限制和截斷
6. 工具開發最佳實踐
7. 傳輸最佳實踐
8. 測試要求
9. OAuth 和安全最佳實踐
10. 資源管理最佳實踐
11. Prompt 管理最佳實踐
12. 錯誤處理標準
13. 文件要求
14. 合規性和監控

---

## 1. Server 命名慣例

遵循這些 MCP server 的標準化命名模式:

**Python**:使用格式 `{service}_mcp`(小寫加底線)
- 範例:`slack_mcp`、`github_mcp`、`jira_mcp`、`stripe_mcp`

**Node/TypeScript**:使用格式 `{service}-mcp-server`(小寫加連字號)
- 範例:`slack-mcp-server`、`github-mcp-server`、`jira-mcp-server`

名稱應該:
- 通用(不綁定特定功能)
- 描述所整合的服務/API
- 容易從任務描述中推斷
- 不包含版本號或日期

---

## 2. 工具命名和設計

### 工具命名最佳實踐

1. **使用 snake_case**:`search_users`、`create_project`、`get_channel_info`
2. **包含服務前綴**:預期您的 MCP server 可能與其他 MCP server 一起使用
   - 使用 `slack_send_message` 而不僅僅是 `send_message`
   - 使用 `github_create_issue` 而不僅僅是 `create_issue`
   - 使用 `asana_list_tasks` 而不僅僅是 `list_tasks`
3. **以動作為導向**:以動詞開頭(get、list、search、create 等)
4. **具體明確**:避免可能與其他 server 衝突的通用名稱
5. **保持一致性**:在您的 server 內使用一致的命名模式

### 工具設計指南

- 工具描述必須狹窄且明確地描述功能
- 描述必須精確匹配實際功能
- 不應該與其他 MCP server 造成混淆
- 應該提供工具註解(readOnlyHint、destructiveHint、idempotentHint、openWorldHint)
- 保持工具操作專注和原子化

---

## 3. 回應格式指南

所有返回資料的工具都應支援多種格式以提供靈活性:

### JSON 格式(`response_format="json"`)
- 機器可讀的結構化資料
- 包含所有可用欄位和中繼資料
- 一致的欄位名稱和類型
- 適合程式化處理
- 當 LLM 需要進一步處理資料時使用

### Markdown 格式(`response_format="markdown"`,通常為預設)
- 人類可讀的格式化文字
- 使用標題、列表和格式以提高清晰度
- 將時間戳記轉換為人類可讀格式(例如,「2024-01-15 10:30:00 UTC」而不是 epoch)
- 顯示帶有 ID 的顯示名稱(例如,「@john.doe (U123456)」)
- 省略冗長的中繼資料(例如,僅顯示一個個人資料圖片 URL,而不是所有尺寸)
- 邏輯分組相關資訊
- 當向使用者呈現資訊時使用

---

## 4. 分頁最佳實踐

對於列出資源的工具:

- **始終遵守 `limit` 參數**:當指定限制時,永遠不要載入所有結果
- **實作分頁**:使用 `offset` 或基於游標的分頁
- **返回分頁中繼資料**:包含 `has_more`、`next_offset`/`next_cursor`、`total_count`
- **永遠不要將所有結果載入記憶體**:對於大型資料集尤其重要
- **預設為合理限制**:通常為 20-50 項
- **在回應中包含清晰的分頁資訊**:讓 LLM 輕鬆請求更多資料

範例分頁回應結構:
```json
{
  "total": 150,
  "count": 20,
  "offset": 0,
  "items": [...],
  "has_more": true,
  "next_offset": 20
}
```

---

## 5. 字元限制和截斷

防止回應包含過多資料:

- **定義 CHARACTER_LIMIT 常數**:通常在模組層級為 25,000 字元
- **在返回前檢查回應大小**:測量最終回應長度
- **使用清晰指標優雅地截斷**:讓 LLM 知道資料已被截斷
- **提供過濾指導**:建議如何使用參數減少結果
- **包含截斷中繼資料**:顯示截斷了什麼以及如何獲取更多

範例截斷處理:
```python
CHARACTER_LIMIT = 25000

if len(result) > CHARACTER_LIMIT:
    truncated_data = data[:max(1, len(data) // 2)]
    response["truncated"] = True
    response["truncation_message"] = (
        f"回應已從 {len(data)} 項截斷為 {len(truncated_data)} 項。"
        f"使用 'offset' 參數或添加過濾器以查看更多結果。"
    )
```

---

## 6. 傳輸選項

MCP server 支援多種傳輸機制,適用於不同的部署場景:

### Stdio Transport

**最適合**:命令列工具、本地整合、子程序執行

**特性**:
- 標準輸入/輸出串流通訊
- 簡單設定,無需網路配置
- 作為客戶端的子程序執行
- 非常適合桌面應用程式和 CLI 工具

**使用時機**:
- 為本地開發環境建立工具
- 與桌面應用程式整合(例如,Claude Desktop)
- 建立命令列實用程式
- 單使用者、單會話場景

### HTTP Transport

**最適合**:Web 服務、遠端存取、多客戶端場景

**特性**:
- 通過 HTTP 的請求-回應模式
- 支援多個同時客戶端
- 可以部署為 Web 服務
- 需要網路配置和安全考慮

**使用時機**:
- 同時為多個客戶端提供服務
- 部署為雲端服務
- 與 Web 應用程式整合
- 需要負載平衡或擴展

### Server-Sent Events (SSE) Transport

**最適合**:即時更新、推送通知、串流資料

**特性**:
- 通過 HTTP 的單向 server 到客戶端串流
- 無需輪詢即可實現即時更新
- 長期連接以實現連續資料流
- 基於標準 HTTP 基礎設施

**使用時機**:
- 客戶端需要即時資料更新
- 實作推送通知
- 串流日誌或監控資料
- 長操作的漸進式結果傳遞

### 傳輸選擇標準

| 標準 | Stdio | HTTP | SSE |
|-----------|-------|------|-----|
| **部署** | 本地 | 遠端 | 遠端 |
| **客戶端** | 單一 | 多個 | 多個 |
| **通訊** | 雙向 | 請求-回應 | Server 推送 |
| **複雜度** | 低 | 中 | 中-高 |
| **即時** | 否 | 否 | 是 |

---

## 7. 工具開發最佳實踐

### 一般指南
1. 工具名稱應該是描述性的和以動作為導向的
2. 使用詳細的 JSON schema 進行參數驗證
3. 在工具描述中包含範例
4. 實作適當的錯誤處理和驗證
5. 對於長操作使用進度報告
6. 保持工具操作專注和原子化
7. 記錄預期的返回值結構
8. 實作適當的逾時
9. 對於資源密集型操作考慮速率限制
10. 記錄工具使用以進行除錯和監控

### 工具的安全考慮

#### 輸入驗證
- 根據 schema 驗證所有參數
- 清理檔案路徑和系統命令
- 驗證 URL 和外部識別碼
- 檢查參數大小和範圍
- 防止命令注入

#### 存取控制
- 在需要時實作身份驗證
- 使用適當的授權檢查
- 審計工具使用
- 限制請求速率
- 監控濫用

#### 錯誤處理
- 不要向客戶端暴露內部錯誤
- 記錄與安全相關的錯誤
- 適當處理逾時
- 錯誤後清理資源
- 驗證返回值

### 工具註解
- 提供 readOnlyHint 和 destructiveHint 註解
- 記住註解是提示,不是安全保證
- 客戶端不應僅根據註解做出安全關鍵決策

---

## 8. 傳輸最佳實踐

### 一般傳輸指南
1. 正確處理連接生命週期
2. 實作適當的錯誤處理
3. 使用適當的逾時值
4. 實作連接狀態管理
5. 斷線時清理資源

### 傳輸的安全最佳實踐
- 遵循 DNS 重綁定攻擊的安全考慮
- 實作適當的身份驗證機制
- 驗證訊息格式
- 優雅地處理格式錯誤的訊息

### Stdio Transport 特定
- 本地 MCP server 不應該記錄到 stdout(干擾協議)
- 使用 stderr 進行日誌記錄訊息
- 正確處理標準 I/O 串流

---

## 9. 測試要求

綜合測試策略應涵蓋:

### 功能測試
- 驗證使用有效/無效輸入的正確執行

### 整合測試
- 使用真實和模擬依賴測試與外部系統的互動

### 安全測試
- 驗證身份驗證、輸入清理、速率限制

### 效能測試
- 檢查負載下的行為、逾時

### 錯誤處理
- 確保適當的錯誤報告和清理

---

## 10. OAuth 和安全最佳實踐

### 身份驗證和授權

連接到外部服務的 MCP server 應實作適當的身份驗證:

**OAuth 2.1 實作:**
- 使用來自認可機構的憑證的安全 OAuth 2.1
- 在處理請求前驗證存取 token
- 僅接受專門針對您的 server 的 token
- 拒絕沒有適當 audience claim 的 token
- 永遠不要傳遞從 MCP 客戶端接收的 token

**API Key 管理:**
- 將 API key 儲存在環境變數中,永遠不要在程式碼中
- 在 server 啟動時驗證 key
- 當身份驗證失敗時提供清晰的錯誤訊息
- 使用安全傳輸敏感憑證

### 輸入驗證和安全

**始終驗證輸入:**
- 清理檔案路徑以防止目錄遍歷
- 驗證 URL 和外部識別碼
- 檢查參數大小和範圍
- 防止系統調用中的命令注入
- 對所有輸入使用 schema 驗證(Pydantic/Zod)

**錯誤處理安全:**
- 不要向客戶端暴露內部錯誤
- 在 server 端記錄與安全相關的錯誤
- 提供有幫助但不洩露的錯誤訊息
- 錯誤後清理資源

### 隱私和資料保護

**資料收集原則:**
- 僅收集功能嚴格必需的資料
- 不要收集無關的對話資料
- 除非工具目的明確需要,否則不要收集 PII
- 提供有關存取哪些資料的清晰資訊

**資料傳輸:**
- 未經披露不要將資料發送到組織外的 server
- 對所有網路通訊使用安全傳輸(HTTPS)
- 驗證外部服務的憑證

---

## 11. 資源管理最佳實踐

1. 僅建議必要的資源
2. 為根使用清晰、描述性的名稱
3. 正確處理資源邊界
4. 尊重客戶端對資源的控制
5. 使用模型控制的原語(工具)進行自動資料暴露

---

## 12. Prompt 管理最佳實踐

- 客戶端應該向使用者顯示建議的 prompt
- 使用者應該能夠修改或拒絕 prompt
- 客戶端應該向使用者顯示完成結果
- 使用者應該能夠修改或拒絕完成結果
- 使用取樣時考慮成本

---

## 13. 錯誤處理標準

- 使用標準 JSON-RPC 錯誤代碼
- 在結果物件內報告工具錯誤(不是協議層級)
- 提供有幫助、具體的錯誤訊息
- 不要暴露內部實作細節
- 錯誤時正確清理資源

---

## 14. 文件要求

- 提供所有工具和功能的清晰文件
- 包含工作範例(每個主要功能至少 3 個)
- 記錄安全考慮
- 指定所需的權限和存取層級
- 記錄速率限制和效能特性

---

## 15. 合規性和監控

- 實作日誌記錄以進行除錯和監控
- 追蹤工具使用模式
- 監控潛在濫用
- 維護與安全相關操作的審計追蹤
- 為持續的合規審查做好準備

---

## 摘要

這些最佳實踐代表建立安全、高效和合規的 MCP server 的綜合指南,這些 server 在生態系統中運作良好。開發人員應遵循這些指南,以確保他們的 MCP server 符合 MCP 目錄中包含的標準,並為使用者提供安全、可靠的體驗。


----------


# 工具

> 讓 LLM 能夠通過您的 server 執行操作

工具是 Model Context Protocol (MCP) 中的強大原語,使 server 能夠向客戶端暴露可執行功能。通過工具,LLM 可以與外部系統互動、執行計算並在現實世界中採取行動。

<Note>
  工具設計為**模型控制**,這意味著工具從 server 暴露給客戶端,目的是讓 AI 模型能夠自動調用它們(需要人工參與批准)。
</Note>

## 概述

MCP 中的工具允許 server 暴露可由客戶端調用並由 LLM 用於執行操作的可執行函數。工具的關鍵方面包括:

* **發現**:客戶端可以通過發送 `tools/list` 請求來獲取可用工具列表
* **調用**:使用 `tools/call` 請求調用工具,server 執行請求的操作並返回結果
* **靈活性**:工具可以從簡單的計算到複雜的 API 互動

與 [resources](/docs/concepts/resources) 一樣,工具通過唯一名稱識別,並可以包含描述以指導其使用。然而,與資源不同,工具代表可以修改狀態或與外部系統互動的動態操作。

## 工具定義結構

每個工具都使用以下結構定義:

```typescript
{
  name: string;          // 工具的唯一識別碼
  description?: string;  // 人類可讀的描述
  inputSchema: {         // 工具參數的 JSON Schema
    type: "object",
    properties: { ... }  // 工具特定參數
  },
  annotations?: {        // 關於工具行為的可選提示
    title?: string;      // 工具的人類可讀標題
    readOnlyHint?: boolean;    // 如果為 true,工具不修改其環境
    destructiveHint?: boolean; // 如果為 true,工具可能執行破壞性更新
    idempotentHint?: boolean;  // 如果為 true,使用相同參數重複調用沒有額外效果
    openWorldHint?: boolean;   // 如果為 true,工具與外部實體的「開放世界」互動
  }
}
```

## 實作工具

以下是在 MCP server 中實作基本工具的範例:

<Tabs>
  <Tab title="TypeScript">
    ```typescript
    const server = new Server({
      name: "example-server",
      version: "1.0.0"
    }, {
      capabilities: {
        tools: {}
      }
    });

    // 定義可用工具
    server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [{
          name: "calculate_sum",
          description: "將兩個數字相加",
          inputSchema: {
            type: "object",
            properties: {
              a: { type: "number" },
              b: { type: "number" }
            },
            required: ["a", "b"]
          }
        }]
      };
    });

    // 處理工具執行
    server.setRequestHandler(CallToolRequestSchema, async (request) => {
      if (request.params.name === "calculate_sum") {
        const { a, b } = request.params.arguments;
        return {
          content: [
            {
              type: "text",
              text: String(a + b)
            }
          ]
        };
      }
      throw new Error("找不到工具");
    });
    ```
  </Tab>

  <Tab title="Python">
    ```python
    app = Server("example-server")

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="calculate_sum",
                description="將兩個數字相加",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"}
                    },
                    "required": ["a", "b"]
                }
            )
        ]

    @app.call_tool()
    async def call_tool(
        name: str,
        arguments: dict
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        if name == "calculate_sum":
            a = arguments["a"]
            b = arguments["b"]
            result = a + b
            return [types.TextContent(type="text", text=str(result))]
        raise ValueError(f"找不到工具: {name}")
    ```
  </Tab>
</Tabs>

## 範例工具模式

以下是 server 可以提供的工具類型範例:

### 系統操作

與本地系統互動的工具:

```typescript
{
  name: "execute_command",
  description: "執行 shell 命令",
  inputSchema: {
    type: "object",
    properties: {
      command: { type: "string" },
      args: { type: "array", items: { type: "string" } }
    }
  }
}
```

### API 整合

包裝外部 API 的工具:

```typescript
{
  name: "github_create_issue",
  description: "建立 GitHub issue",
  inputSchema: {
    type: "object",
    properties: {
      title: { type: "string" },
      body: { type: "string" },
      labels: { type: "array", items: { type: "string" } }
    }
  }
}
```

### 資料處理

轉換或分析資料的工具:

```typescript
{
  name: "analyze_csv",
  description: "分析 CSV 檔案",
  inputSchema: {
    type: "object",
    properties: {
      filepath: { type: "string" },
      operations: {
        type: "array",
        items: {
          enum: ["sum", "average", "count"]
        }
      }
    }
  }
}
```

## 最佳實踐

在實作工具時:

1. 提供清晰、描述性的名稱和描述
2. 使用詳細的 JSON Schema 定義參數
3. 在工具描述中包含範例以演示模型應如何使用它們
4. 實作適當的錯誤處理和驗證
5. 對於長操作使用進度報告
6. 保持工具操作專注和原子化
7. 記錄預期的返回值結構
8. 實作適當的逾時
9. 對於資源密集型操作考慮速率限制
10. 記錄工具使用以進行除錯和監控

### 工具名稱衝突

MCP 客戶端應用程式和 MCP server 代理在建立自己的工具列表時可能會遇到工具名稱衝突。例如,兩個連接的 MCP server `web1` 和 `web2` 可能都暴露一個名為 `search_web` 的工具。

應用程式可以使用以下策略之一(以及其他策略;非詳盡列表)消除工具歧義:

* 將唯一的使用者定義 server 名稱與工具名稱串聯,例如 `web1___search_web` 和 `web2___search_web`。當配置檔案中已由使用者提供唯一 server 名稱時,此策略可能更可取。
* 為工具名稱生成隨機前綴,例如 `jrwxs___search_web` 和 `6cq52___search_web`。在沒有使用者定義唯一名稱的 server 代理中,此策略可能更可取。
* 使用 server URI 作為工具名稱的前綴,例如 `web1.example.com:search_web` 和 `web2.example.com:search_web`。在使用遠端 MCP server 時,此策略可能適合。

請注意,來自初始化流程的 server 提供的名稱不保證是唯一的,通常不適合用於消除歧義。

## 安全考慮

在暴露工具時:

### 輸入驗證

* 根據 schema 驗證所有參數
* 清理檔案路徑和系統命令
* 驗證 URL 和外部識別碼
* 檢查參數大小和範圍
* 防止命令注入

### 存取控制

* 在需要時實作身份驗證
* 使用適當的授權檢查
* 審計工具使用
* 限制請求速率
* 監控濫用

### 錯誤處理

* 不要向客戶端暴露內部錯誤
* 記錄與安全相關的錯誤
* 適當處理逾時
* 錯誤後清理資源
* 驗證返回值

## 工具發現和更新

MCP 支援動態工具發現:

1. 客戶端可以隨時列出可用工具
2. Server 可以使用 `notifications/tools/list_changed` 在工具變更時通知客戶端
3. 工具可以在執行時添加或刪除
4. 工具定義可以更新(雖然應該謹慎進行)

## 錯誤處理

工具錯誤應該在結果物件內報告,而不是作為 MCP 協議層級錯誤。這允許 LLM 看到並可能處理錯誤。當工具遇到錯誤時:

1. 在結果中將 `isError` 設定為 `true`
2. 在 `content` 陣列中包含錯誤詳細資訊

以下是工具適當錯誤處理的範例:

<Tabs>
  <Tab title="TypeScript">
    ```typescript
    try {
      // 工具操作
      const result = performOperation();
      return {
        content: [
          {
            type: "text",
            text: `操作成功: ${result}`
          }
        ]
      };
    } catch (error) {
      return {
        isError: true,
        content: [
          {
            type: "text",
            text: `錯誤: ${error.message}`
          }
        ]
      };
    }
    ```
  </Tab>

  <Tab title="Python">
    ```python
    try:
        # 工具操作
        result = perform_operation()
        return types.CallToolResult(
            content=[
                types.TextContent(
                    type="text",
                    text=f"操作成功: {result}"
                )
            ]
        )
    except Exception as error:
        return types.CallToolResult(
            isError=True,
            content=[
                types.TextContent(
                    type="text",
                    text=f"錯誤: {str(error)}"
                )
            ]
        )
    ```
  </Tab>
</Tabs>

這種方法允許 LLM 看到發生了錯誤並可能採取糾正措施或請求人工干預。

## 工具註解

工具註解提供關於工具行為的額外中繼資料,幫助客戶端了解如何呈現和管理工具。這些註解是提示,描述工具的性質和影響,但不應依賴它們進行安全決策。

### 工具註解的目的

工具註解有幾個關鍵目的:

1. 在不影響模型上下文的情況下提供 UX 特定資訊
2. 幫助客戶端適當地分類和呈現工具
3. 傳達關於工具潛在副作用的資訊
4. 協助開發直觀的工具批准介面

### 可用的工具註解

MCP 規範為工具定義以下註解:

| 註解 | 類型 | 預設 | 描述 |
| ----------------- | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `title` | string | - | 工具的人類可讀標題,對 UI 顯示有用 |
| `readOnlyHint` | boolean | false | 如果為 true,表示工具不修改其環境 |
| `destructiveHint` | boolean | true | 如果為 true,工具可能執行破壞性更新(僅在 `readOnlyHint` 為 false 時有意義) |
| `idempotentHint` | boolean | false | 如果為 true,使用相同參數重複調用工具沒有額外效果(僅在 `readOnlyHint` 為 false 時有意義) |
| `openWorldHint` | boolean | true | 如果為 true,工具可能與外部實體的「開放世界」互動 |

### 範例用法

以下是如何為不同場景使用註解定義工具:

```typescript
// 唯讀搜索工具
{
  name: "web_search",
  description: "在網路上搜索資訊",
  inputSchema: {
    type: "object",
    properties: {
      query: { type: "string" }
    },
    required: ["query"]
  },
  annotations: {
    title: "Web 搜索",
    readOnlyHint: true,
    openWorldHint: true
  }
}

// 破壞性檔案刪除工具
{
  name: "delete_file",
  description: "從檔案系統刪除檔案",
  inputSchema: {
    type: "object",
    properties: {
      path: { type: "string" }
    },
    required: ["path"]
  },
  annotations: {
    title: "刪除檔案",
    readOnlyHint: false,
    destructiveHint: true,
    idempotentHint: true,
    openWorldHint: false
  }
}

// 非破壞性資料庫記錄建立工具
{
  name: "create_record",
  description: "在資料庫中建立新記錄",
  inputSchema: {
    type: "object",
    properties: {
      table: { type: "string" },
      data: { type: "object" }
    },
    required: ["table", "data"]
  },
  annotations: {
    title: "建立資料庫記錄",
    readOnlyHint: false,
    destructiveHint: false,
    idempotentHint: false,
    openWorldHint: false
  }
}
```

### 在 server 實作中整合註解

<Tabs>
  <Tab title="TypeScript">
    ```typescript
    server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [{
          name: "calculate_sum",
          description: "將兩個數字相加",
          inputSchema: {
            type: "object",
            properties: {
              a: { type: "number" },
              b: { type: "number" }
            },
            required: ["a", "b"]
          },
          annotations: {
            title: "計算總和",
            readOnlyHint: true,
            openWorldHint: false
          }
        }]
      };
    });
    ```
  </Tab>

  <Tab title="Python">
    ```python
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("example-server")

    @mcp.tool(
        annotations={
            "title": "計算總和",
            "readOnlyHint": True,
            "openWorldHint": False
        }
    )
    async def calculate_sum(a: float, b: float) -> str:
        """將兩個數字相加。

        Args:
            a: 要相加的第一個數字
            b: 要相加的第二個數字
        """
        result = a + b
        return str(result)
    ```
  </Tab>
</Tabs>

### 工具註解的最佳實踐

1. **準確說明副作用**:清楚表明工具是否修改其環境以及這些修改是否具有破壞性。

2. **使用描述性標題**:提供清楚描述工具目的的人性化標題。

3. **正確表明冪等性**:僅當使用相同參數重複調用確實沒有額外效果時,才將工具標記為冪等。

4. **設定適當的開放/封閉世界提示**:表明工具是與封閉系統(如資料庫)還是開放系統(如網路)互動。

5. **記住註解是提示**:ToolAnnotations 中的所有屬性都是提示,不保證提供工具行為的忠實描述。客戶端永遠不應僅根據註解做出安全關鍵決策。

## 測試工具

MCP 工具的綜合測試策略應涵蓋:

* **功能測試**:驗證工具使用有效輸入正確執行並適當處理無效輸入
* **整合測試**:使用真實和模擬依賴測試工具與外部系統的互動
* **安全測試**:驗證身份驗證、授權、輸入清理和速率限制
* **效能測試**:檢查負載下的行為、逾時處理和資源清理
* **錯誤處理**:確保工具通過 MCP 協議正確報告錯誤並清理資源
