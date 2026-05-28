# Node/TypeScript MCP Server 實作指南

## 概述

本文件提供使用 MCP TypeScript SDK 實作 MCP server 的 Node/TypeScript 特定最佳實踐和範例。它涵蓋專案結構、server 設定、工具註冊模式、使用 Zod 進行輸入驗證、錯誤處理和完整的工作範例。

---

## 快速參考

### 主要 Import
```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import axios, { AxiosError } from "axios";
```

### Server 初始化
```typescript
const server = new McpServer({
  name: "service-mcp-server",
  version: "1.0.0"
});
```

### 工具註冊模式
```typescript
server.registerTool("tool_name", {...config}, async (params) => {
  // 實作
});
```

---

## MCP TypeScript SDK

官方 MCP TypeScript SDK 提供:
- `McpServer` 類別用於 server 初始化
- `registerTool` 方法用於工具註冊
- Zod schema 整合用於執行時輸入驗證
- 類型安全的工具處理器實作

請參閱參考資料中的 MCP SDK 文件以獲取完整詳細資訊。

## Server 命名慣例

Node/TypeScript MCP server 必須遵循此命名模式:
- **格式**:`{service}-mcp-server`(小寫加連字號)
- **範例**:`github-mcp-server`、`jira-mcp-server`、`stripe-mcp-server`

名稱應該:
- 通用(不綁定特定功能)
- 描述所整合的服務/API
- 容易從任務描述中推斷
- 不包含版本號或日期

## 專案結構

為 Node/TypeScript MCP server 建立以下結構:

```
{service}-mcp-server/
├── package.json
├── tsconfig.json
├── README.md
├── src/
│   ├── index.ts          # 使用 McpServer 初始化的主入口點
│   ├── types.ts          # TypeScript 類型定義和介面
│   ├── tools/            # 工具實作(每個領域一個檔案)
│   ├── services/         # API 客戶端和共享實用程式
│   ├── schemas/          # Zod 驗證 schema
│   └── constants.ts      # 共享常數(API_URL、CHARACTER_LIMIT 等)
└── dist/                 # 建構的 JavaScript 檔案(入口點:dist/index.js)
```

## 工具實作

### 工具命名

使用 snake_case 作為工具名稱(例如,"search_users"、"create_project"、"get_channel_info"),名稱清晰且以動作為導向。

**避免命名衝突**:包含服務上下文以防止重疊:
- 使用 "slack_send_message" 而不僅僅是 "send_message"
- 使用 "github_create_issue" 而不僅僅是 "create_issue"
- 使用 "asana_list_tasks" 而不僅僅是 "list_tasks"

### 工具結構

工具使用 `registerTool` 方法註冊,具有以下要求:
- 使用 Zod schema 進行執行時輸入驗證和類型安全
- 必須明確提供 `description` 欄位 - JSDoc 註解不會自動提取
- 明確提供 `title`、`description`、`inputSchema` 和 `annotations`
- `inputSchema` 必須是 Zod schema 物件(不是 JSON schema)
- 明確為所有參數和返回值設定類型

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "example-mcp",
  version: "1.0.0"
});

// 用於輸入驗證的 Zod schema
const UserSearchInputSchema = z.object({
  query: z.string()
    .min(2, "查詢必須至少 2 個字元")
    .max(200, "查詢不得超過 200 個字元")
    .describe("用於匹配名稱/電子郵件的搜索字串"),
  limit: z.number()
    .int()
    .min(1)
    .max(100)
    .default(20)
    .describe("要返回的最大結果數"),
  offset: z.number()
    .int()
    .min(0)
    .default(0)
    .describe("用於分頁跳過的結果數"),
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("輸出格式:'markdown' 用於人類可讀或 'json' 用於機器可讀")
}).strict();

// 從 Zod schema 的類型定義
type UserSearchInput = z.infer<typeof UserSearchInputSchema>;

server.registerTool(
  "example_search_users",
  {
    title: "搜索範例使用者",
    description: `按名稱、電子郵件或團隊在範例系統中搜索使用者。

此工具在範例平台中搜索所有使用者個人資料,支援部分匹配和各種搜索過濾器。它不會建立或修改使用者,僅搜索現有使用者。

Args:
  - query (string): 用於匹配名稱/電子郵件的搜索字串
  - limit (number): 要返回的最大結果數,介於 1-100 之間(預設:20)
  - offset (number): 用於分頁跳過的結果數(預設:0)
  - response_format ('markdown' | 'json'): 輸出格式(預設:'markdown')

Returns:
  對於 JSON 格式:具有 schema 的結構化資料:
  {
    "total": number,           // 找到的匹配總數
    "count": number,           // 此回應中的結果數
    "offset": number,          // 當前分頁偏移量
    "users": [
      {
        "id": string,          // 使用者 ID(例如,"U123456789")
        "name": string,        // 全名(例如,"John Doe")
        "email": string,       // 電子郵件地址
        "team": string,        // 團隊名稱(可選)
        "active": boolean      // 使用者是否活躍
      }
    ],
    "has_more": boolean,       // 是否有更多結果可用
    "next_offset": number      // 下一頁的偏移量(如果 has_more 為 true)
  }

Examples:
  - 使用時機:「找到所有行銷團隊成員」-> 使用 query="team:marketing" 的參數
  - 使用時機:「搜索 John 的帳戶」-> 使用 query="john" 的參數
  - 不要使用時機:您需要建立使用者(改用 example_create_user)

Error Handling:
  - 如果請求過多,返回「錯誤:超過速率限制」(429 狀態)
  - 如果搜索返回空,返回「未找到與 '<query>' 匹配的使用者」`,
    inputSchema: UserSearchInputSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true
    }
  },
  async (params: UserSearchInput) => {
    try {
      // 輸入驗證由 Zod schema 處理
      // 使用驗證的參數進行 API 請求
      const data = await makeApiRequest<any>(
        "users/search",
        "GET",
        undefined,
        {
          q: params.query,
          limit: params.limit,
          offset: params.offset
        }
      );

      const users = data.users || [];
      const total = data.total || 0;

      if (!users.length) {
        return {
          content: [{
            type: "text",
            text: `未找到與 '${params.query}' 匹配的使用者`
          }]
        };
      }

      // 根據請求的格式格式化回應
      let result: string;

      if (params.response_format === ResponseFormat.MARKDOWN) {
        // 人類可讀的 markdown 格式
        const lines: string[] = [`# 使用者搜索結果:'${params.query}'`, ""];
        lines.push(`找到 ${total} 個使用者(顯示 ${users.length} 個)`);
        lines.push("");

        for (const user of users) {
          lines.push(`## ${user.name} (${user.id})`);
          lines.push(`- **電子郵件**:${user.email}`);
          if (user.team) {
            lines.push(`- **團隊**:${user.team}`);
          }
          lines.push("");
        }

        result = lines.join("\n");

      } else {
        // 機器可讀的 JSON 格式
        const response: any = {
          total,
          count: users.length,
          offset: params.offset,
          users: users.map((user: any) => ({
            id: user.id,
            name: user.name,
            email: user.email,
            ...(user.team ? { team: user.team } : {}),
            active: user.active ?? true
          }))
        };

        // 如果有更多結果,添加分頁資訊
        if (total > params.offset + users.length) {
          response.has_more = true;
          response.next_offset = params.offset + users.length;
        }

        result = JSON.stringify(response, null, 2);
      }

      return {
        content: [{
          type: "text",
          text: result
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: handleApiError(error)
        }]
      };
    }
  }
);
```

## 用於輸入驗證的 Zod Schema

Zod 提供執行時類型驗證:

```typescript
import { z } from "zod";

// 具有驗證的基本 schema
const CreateUserSchema = z.object({
  name: z.string()
    .min(1, "名稱為必填")
    .max(100, "名稱不得超過 100 個字元"),
  email: z.string()
    .email("無效的電子郵件格式"),
  age: z.number()
    .int("年齡必須是整數")
    .min(0, "年齡不能為負數")
    .max(150, "年齡不能大於 150")
}).strict();  // 使用 .strict() 禁止額外欄位

// 列舉
enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json"
}

const SearchSchema = z.object({
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("輸出格式")
});

// 具有預設值的可選欄位
const PaginationSchema = z.object({
  limit: z.number()
    .int()
    .min(1)
    .max(100)
    .default(20)
    .describe("要返回的最大結果數"),
  offset: z.number()
    .int()
    .min(0)
    .default(0)
    .describe("要跳過的結果數")
});
```

## 回應格式選項

支援多種輸出格式以提供靈活性:

```typescript
enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json"
}

const inputSchema = z.object({
  query: z.string(),
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("輸出格式:'markdown' 用於人類可讀或 'json' 用於機器可讀")
});
```

**Markdown 格式**:
- 使用標題、列表和格式以提高清晰度
- 將時間戳記轉換為人類可讀格式
- 顯示帶有 ID 的顯示名稱(括號內)
- 省略冗長的中繼資料
- 邏輯分組相關資訊

**JSON 格式**:
- 返回適合程式化處理的完整結構化資料
- 包含所有可用欄位和中繼資料
- 使用一致的欄位名稱和類型

## 分頁實作

對於列出資源的工具:

```typescript
const ListSchema = z.object({
  limit: z.number().int().min(1).max(100).default(20),
  offset: z.number().int().min(0).default(0)
});

async function listItems(params: z.infer<typeof ListSchema>) {
  const data = await apiRequest(params.limit, params.offset);

  const response = {
    total: data.total,
    count: data.items.length,
    offset: params.offset,
    items: data.items,
    has_more: data.total > params.offset + data.items.length,
    next_offset: data.total > params.offset + data.items.length
      ? params.offset + data.items.length
      : undefined
  };

  return JSON.stringify(response, null, 2);
}
```

## 字元限制和截斷

添加 CHARACTER_LIMIT 常數以防止過多回應:

```typescript
// 在 constants.ts 中的模組層級
export const CHARACTER_LIMIT = 25000;  // 回應大小的最大字元數

async function searchTool(params: SearchInput) {
  let result = generateResponse(data);

  // 檢查字元限制並在需要時截斷
  if (result.length > CHARACTER_LIMIT) {
    const truncatedData = data.slice(0, Math.max(1, data.length / 2));
    response.data = truncatedData;
    response.truncated = true;
    response.truncation_message =
      `回應已從 ${data.length} 項截斷為 ${truncatedData.length} 項。` +
      `使用 'offset' 參數或添加過濾器以查看更多結果。`;
    result = JSON.stringify(response, null, 2);
  }

  return result;
}
```

## 錯誤處理

提供清晰、可操作的錯誤訊息:

```typescript
import axios, { AxiosError } from "axios";

function handleApiError(error: unknown): string {
  if (error instanceof AxiosError) {
    if (error.response) {
      switch (error.response.status) {
        case 404:
          return "錯誤:未找到資源。請檢查 ID 是否正確。";
        case 403:
          return "錯誤:拒絕存取。您沒有存取此資源的權限。";
        case 429:
          return "錯誤:超過速率限制。請稍後再進行更多請求。";
        default:
          return `錯誤:API 請求失敗,狀態為 ${error.response.status}`;
      }
    } else if (error.code === "ECONNABORTED") {
      return "錯誤:請求逾時。請重試。";
    }
  }
  return `錯誤:發生意外錯誤:${error instanceof Error ? error.message : String(error)}`;
}
```

## 共享實用程式

將常見功能提取到可重用函數中:

```typescript
// 共享 API 請求函數
async function makeApiRequest<T>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
  data?: any,
  params?: any
): Promise<T> {
  try {
    const response = await axios({
      method,
      url: `${API_BASE_URL}/${endpoint}`,
      data,
      params,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      }
    });
    return response.data;
  } catch (error) {
    throw error;
  }
}
```

## Async/Await 最佳實踐

始終對網路請求和 I/O 操作使用 async/await:

```typescript
// 良好:非同步網路請求
async function fetchData(resourceId: string): Promise<ResourceData> {
  const response = await axios.get(`${API_URL}/resource/${resourceId}`);
  return response.data;
}

// 不良:Promise 鏈
function fetchData(resourceId: string): Promise<ResourceData> {
  return axios.get(`${API_URL}/resource/${resourceId}`)
    .then(response => response.data);  // 更難閱讀和維護
}
```

## TypeScript 最佳實踐

1. **使用嚴格 TypeScript**:在 tsconfig.json 中啟用嚴格模式
2. **定義介面**:為所有資料結構建立清晰的介面定義
3. **避免 `any`**:使用適當的類型或 `unknown` 而不是 `any`
4. **Zod 用於執行時驗證**:使用 Zod schema 驗證外部資料
5. **類型保護**:為複雜的類型檢查建立類型保護函數
6. **錯誤處理**:始終使用 try-catch 並進行適當的錯誤類型檢查
7. **Null 安全**:使用可選鏈(`?.`)和空值合併(`??`)

```typescript
// 良好:使用 Zod 和介面的類型安全
interface UserResponse {
  id: string;
  name: string;
  email: string;
  team?: string;
  active: boolean;
}

const UserSchema = z.object({
  id: z.string(),
  name: z.string(),
  email: z.string().email(),
  team: z.string().optional(),
  active: z.boolean()
});

type User = z.infer<typeof UserSchema>;

async function getUser(id: string): Promise<User> {
  const data = await apiCall(`/users/${id}`);
  return UserSchema.parse(data);  // 執行時驗證
}

// 不良:使用 any
async function getUser(id: string): Promise<any> {
  return await apiCall(`/users/${id}`);  // 沒有類型安全
}
```

## 套件配置

### package.json

```json
{
  "name": "{service}-mcp-server",
  "version": "1.0.0",
  "description": "{Service} API 整合的 MCP server",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "clean": "rm -rf dist"
  },
  "engines": {
    "node": ">=18"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.6.1",
    "axios": "^1.7.9",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^22.10.0",
    "tsx": "^4.19.2",
    "typescript": "^5.7.2"
  }
}
```

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "allowSyntheticDefaultImports": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

## 完整範例

```typescript
#!/usr/bin/env node
/**
 * 範例服務的 MCP Server。
 *
 * 此 server 提供與範例 API 互動的工具,包括使用者搜索、
 * 專案管理和資料匯出功能。
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import axios, { AxiosError } from "axios";

// 常數
const API_BASE_URL = "https://api.example.com/v1";
const CHARACTER_LIMIT = 25000;

// 列舉
enum ResponseFormat {
  MARKDOWN = "markdown",
  JSON = "json"
}

// Zod schema
const UserSearchInputSchema = z.object({
  query: z.string()
    .min(2, "查詢必須至少 2 個字元")
    .max(200, "查詢不得超過 200 個字元")
    .describe("用於匹配名稱/電子郵件的搜索字串"),
  limit: z.number()
    .int()
    .min(1)
    .max(100)
    .default(20)
    .describe("要返回的最大結果數"),
  offset: z.number()
    .int()
    .min(0)
    .default(0)
    .describe("用於分頁跳過的結果數"),
  response_format: z.nativeEnum(ResponseFormat)
    .default(ResponseFormat.MARKDOWN)
    .describe("輸出格式:'markdown' 用於人類可讀或 'json' 用於機器可讀")
}).strict();

type UserSearchInput = z.infer<typeof UserSearchInputSchema>;

// 共享實用程式函數
async function makeApiRequest<T>(
  endpoint: string,
  method: "GET" | "POST" | "PUT" | "DELETE" = "GET",
  data?: any,
  params?: any
): Promise<T> {
  try {
    const response = await axios({
      method,
      url: `${API_BASE_URL}/${endpoint}`,
      data,
      params,
      timeout: 30000,
      headers: {
        "Content-Type": "application/json",
        "Accept": "application/json"
      }
    });
    return response.data;
  } catch (error) {
    throw error;
  }
}

function handleApiError(error: unknown): string {
  if (error instanceof AxiosError) {
    if (error.response) {
      switch (error.response.status) {
        case 404:
          return "錯誤:未找到資源。請檢查 ID 是否正確。";
        case 403:
          return "錯誤:拒絕存取。您沒有存取此資源的權限。";
        case 429:
          return "錯誤:超過速率限制。請稍後再進行更多請求。";
        default:
          return `錯誤:API 請求失敗,狀態為 ${error.response.status}`;
      }
    } else if (error.code === "ECONNABORTED") {
      return "錯誤:請求逾時。請重試。";
    }
  }
  return `錯誤:發生意外錯誤:${error instanceof Error ? error.message : String(error)}`;
}

// 建立 MCP server 實例
const server = new McpServer({
  name: "example-mcp",
  version: "1.0.0"
});

// 註冊工具
server.registerTool(
  "example_search_users",
  {
    title: "搜索範例使用者",
    description: `[如上所示的完整描述]`,
    inputSchema: UserSearchInputSchema,
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: true
    }
  },
  async (params: UserSearchInput) => {
    // 如上所示的實作
  }
);

// 主函數
async function main() {
  // 如果需要,驗證環境變數
  if (!process.env.EXAMPLE_API_KEY) {
    console.error("錯誤:需要 EXAMPLE_API_KEY 環境變數");
    process.exit(1);
  }

  // 建立傳輸
  const transport = new StdioServerTransport();

  // 將 server 連接到傳輸
  await server.connect(transport);

  console.error("範例 MCP server 通過 stdio 執行");
}

// 執行 server
main().catch((error) => {
  console.error("Server 錯誤:", error);
  process.exit(1);
});
```

---

## 進階 MCP 功能

### 資源註冊

將資料公開為資源以進行高效的基於 URI 的存取:

```typescript
import { ResourceTemplate } from "@modelcontextprotocol/sdk/types.js";

// 使用 URI 模板註冊資源
server.registerResource(
  {
    uri: "file://documents/{name}",
    name: "文件資源",
    description: "按名稱存取文件",
    mimeType: "text/plain"
  },
  async (uri: string) => {
    // 從 URI 提取參數
    const match = uri.match(/^file:\/\/documents\/(.+)$/);
    if (!match) {
      throw new Error("無效的 URI 格式");
    }

    const documentName = match[1];
    const content = await loadDocument(documentName);

    return {
      contents: [{
        uri,
        mimeType: "text/plain",
        text: content
      }]
    };
  }
);

// 動態列出可用資源
server.registerResourceList(async () => {
  const documents = await getAvailableDocuments();
  return {
    resources: documents.map(doc => ({
      uri: `file://documents/${doc.name}`,
      name: doc.name,
      mimeType: "text/plain",
      description: doc.description
    }))
  };
});
```

**何時使用資源 vs 工具:**
- **資源**:用於具有簡單基於 URI 參數的資料存取
- **工具**:用於需要驗證和業務邏輯的複雜操作
- **資源**:當資料相對靜態或基於模板時
- **工具**:當操作具有副作用或複雜工作流程時

### 多種傳輸選項

TypeScript SDK 支援不同的傳輸機制:

```typescript
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

// Stdio transport(預設 - 用於 CLI 工具)
const stdioTransport = new StdioServerTransport();
await server.connect(stdioTransport);

// SSE transport(用於即時 Web 更新)
const sseTransport = new SSEServerTransport("/message", response);
await server.connect(sseTransport);

// HTTP transport(用於 Web 服務)
// 根據您的 HTTP 框架整合進行配置
```

**傳輸選擇指南:**
- **Stdio**:命令列工具、子程序整合、本地開發
- **HTTP**:Web 服務、遠端存取、多個同時客戶端
- **SSE**:即時更新、server 推送通知、Web 儀表板

### 通知支援

當 server 狀態變更時通知客戶端:

```typescript
// 當工具列表變更時通知
server.notification({
  method: "notifications/tools/list_changed"
});

// 當資源變更時通知
server.notification({
  method: "notifications/resources/list_changed"
});
```

謹慎使用通知 - 僅在 server 功能真正變更時使用。

---

## 程式碼最佳實踐

### 程式碼可組合性和可重用性

您的實作必須優先考慮可組合性和程式碼重用:

1. **提取常見功能**:
   - 為跨多個工具使用的操作建立可重用的輔助函數
   - 為 HTTP 請求建立共享 API 客戶端,而不是複製程式碼
   - 在實用程式函數中集中錯誤處理邏輯
   - 將業務邏輯提取到可以組合的專用函數中
   - 提取共享的 markdown 或 JSON 欄位選擇和格式化功能

2. **避免重複**:
   - 永遠不要在工具之間複製貼上類似的程式碼
   - 如果您發現自己編寫了兩次類似的邏輯,請將其提取到函數中
   - 分頁、過濾、欄位選擇和格式化等常見操作應該共享
   - 身份驗證/授權邏輯應該集中

## 建構和執行

在執行之前始終建構您的 TypeScript 程式碼:

```bash
# 建構專案
npm run build

# 執行 server
npm start

# 使用自動重新載入的開發
npm run dev
```

在考慮實作完成之前,始終確保 `npm run build` 成功完成。

## 品質檢查清單

在完成 Node/TypeScript MCP server 實作之前,請確保:

### 策略設計
- [ ] 工具啟用完整工作流程,而不僅僅是 API 端點包裝器
- [ ] 工具名稱反映自然任務細分
- [ ] 回應格式針對代理上下文效率進行最佳化
- [ ] 在適當的地方使用人類可讀的識別碼
- [ ] 錯誤訊息引導代理朝向正確使用

### 實作品質
- [ ] 重點實作:實作了最重要和有價值的工具
- [ ] 所有工具使用 `registerTool` 註冊,具有完整配置
- [ ] 所有工具包含 `title`、`description`、`inputSchema` 和 `annotations`
- [ ] 註解正確設定(readOnlyHint、destructiveHint、idempotentHint、openWorldHint)
- [ ] 所有工具使用 Zod schema 進行執行時輸入驗證,並強制執行 `.strict()`
- [ ] 所有 Zod schema 具有適當的約束和描述性錯誤訊息
- [ ] 所有工具具有全面的描述,包含明確的輸入/輸出類型
- [ ] 描述包含返回值範例和完整的 schema 文件
- [ ] 錯誤訊息清晰、可操作且具有教育性

### TypeScript 品質
- [ ] 為所有資料結構定義 TypeScript 介面
- [ ] 在 tsconfig.json 中啟用嚴格 TypeScript
- [ ] 不使用 `any` 類型 - 改用 `unknown` 或適當的類型
- [ ] 所有非同步函數具有明確的 Promise<T> 返回類型
- [ ] 錯誤處理使用適當的類型保護(例如,`axios.isAxiosError`、`z.ZodError`)

### 進階功能(適用時)
- [ ] 為適當的資料端點註冊資源
- [ ] 配置適當的傳輸(stdio、HTTP、SSE)
- [ ] 為動態 server 功能實作通知
- [ ] 使用 SDK 介面的類型安全

### 專案配置
- [ ] Package.json 包含所有必要的依賴項
- [ ] 建構腳本在 dist/ 目錄中產生可工作的 JavaScript
- [ ] 主入口點正確配置為 dist/index.js
- [ ] Server 名稱遵循格式:`{service}-mcp-server`
- [ ] tsconfig.json 正確配置為嚴格模式

### 程式碼品質
- [ ] 在適用的地方正確實作分頁
- [ ] 大型回應檢查 CHARACTER_LIMIT 常數並使用清晰訊息截斷
- [ ] 為可能的大型結果集提供過濾選項
- [ ] 所有網路操作優雅地處理逾時和連接錯誤
- [ ] 常見功能提取到可重用函數中
- [ ] 類似操作的返回類型一致

### 測試和建構
- [ ] `npm run build` 成功完成,沒有錯誤
- [ ] dist/index.js 已建立且可執行
- [ ] Server 執行:`node dist/index.js --help`
- [ ] 所有 import 正確解析
- [ ] 範例工具調用按預期工作
