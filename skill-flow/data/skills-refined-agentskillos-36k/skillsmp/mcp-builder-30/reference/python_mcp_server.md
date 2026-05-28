# Python MCP Server 實作指南

## 概述

本文件提供使用 MCP Python SDK 實作 MCP server 的 Python 特定最佳實踐和範例。它涵蓋 server 設定、工具註冊模式、使用 Pydantic 進行輸入驗證、錯誤處理和完整的工作範例。

---

## 快速參考

### 主要 Import
```python
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
```

### Server 初始化
```python
mcp = FastMCP("service_mcp")
```

### 工具註冊模式
```python
@mcp.tool(name="tool_name", annotations={...})
async def tool_function(params: InputModel) -> str:
    # 實作
    pass
```

---

## MCP Python SDK 和 FastMCP

官方 MCP Python SDK 提供 FastMCP,這是一個用於建立 MCP server 的高階框架。它提供:
- 從函數簽名和文件字串自動生成 description 和 inputSchema
- Pydantic 模型整合用於輸入驗證
- 使用 `@mcp.tool` 的裝飾器式工具註冊

**有關完整的 SDK 文件,請使用 WebFetch 載入:**
`https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`

## Server 命名慣例

Python MCP server 必須遵循此命名模式:
- **格式**:`{service}_mcp`(小寫加底線)
- **範例**:`github_mcp`、`jira_mcp`、`stripe_mcp`

名稱應該:
- 通用(不綁定特定功能)
- 描述所整合的服務/API
- 容易從任務描述中推斷
- 不包含版本號或日期

## 工具實作

### 工具命名

使用 snake_case 作為工具名稱(例如,"search_users"、"create_project"、"get_channel_info"),名稱清晰且以動作為導向。

**避免命名衝突**:包含服務上下文以防止重疊:
- 使用 "slack_send_message" 而不僅僅是 "send_message"
- 使用 "github_create_issue" 而不僅僅是 "create_issue"
- 使用 "asana_list_tasks" 而不僅僅是 "list_tasks"

### 使用 FastMCP 的工具結構

工具使用 `@mcp.tool` 裝飾器定義,使用 Pydantic 模型進行輸入驗證:

```python
from pydantic import BaseModel, Field, ConfigDict
from mcp.server.fastmcp import FastMCP

# 初始化 MCP server
mcp = FastMCP("example_mcp")

# 定義用於輸入驗證的 Pydantic 模型
class ServiceToolInput(BaseModel):
    '''服務工具操作的輸入模型。'''
    model_config = ConfigDict(
        str_strip_whitespace=True,  # 自動從字串中去除空格
        validate_assignment=True,    # 在賦值時驗證
        extra='forbid'              # 禁止額外欄位
    )

    param1: str = Field(..., description="第一個參數描述(例如,'user123'、'project-abc')", min_length=1, max_length=100)
    param2: Optional[int] = Field(default=None, description="具有約束的可選整數參數", ge=0, le=1000)
    tags: Optional[List[str]] = Field(default_factory=list, description="要應用的標籤列表", max_items=10)

@mcp.tool(
    name="service_tool_name",
    annotations={
        "title": "人類可讀的工具標題",
        "readOnlyHint": True,     # 工具不修改環境
        "destructiveHint": False,  # 工具不執行破壞性操作
        "idempotentHint": True,    # 重複調用沒有額外效果
        "openWorldHint": False     # 工具不與外部實體互動
    }
)
async def service_tool_name(params: ServiceToolInput) -> str:
    '''工具描述自動成為 'description' 欄位。

    此工具在服務上執行特定操作。它在處理之前使用
    ServiceToolInput Pydantic 模型驗證所有輸入。

    Args:
        params (ServiceToolInput): 包含以下內容的驗證輸入參數:
            - param1 (str): 第一個參數描述
            - param2 (Optional[int]): 具有預設值的可選參數
            - tags (Optional[List[str]]): 標籤列表

    Returns:
        str: 包含操作結果的 JSON 格式回應
    '''
    # 在這裡實作
    pass
```

## Pydantic v2 主要功能

- 使用 `model_config` 而不是巢狀 `Config` 類別
- 使用 `field_validator` 而不是已棄用的 `validator`
- 使用 `model_dump()` 而不是已棄用的 `dict()`
- 驗證器需要 `@classmethod` 裝飾器
- 驗證器方法需要類型提示

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict

class CreateUserInput(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    name: str = Field(..., description="使用者的全名", min_length=1, max_length=100)
    email: str = Field(..., description="使用者的電子郵件地址", pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., description="使用者的年齡", ge=0, le=150)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("電子郵件不能為空")
        return v.lower()
```

## 回應格式選項

支援多種輸出格式以提供靈活性:

```python
from enum import Enum

class ResponseFormat(str, Enum):
    '''工具回應的輸出格式。'''
    MARKDOWN = "markdown"
    JSON = "json"

class UserSearchInput(BaseModel):
    query: str = Field(..., description="搜索查詢")
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="輸出格式:'markdown' 用於人類可讀或 'json' 用於機器可讀"
    )
```

**Markdown 格式**:
- 使用標題、列表和格式以提高清晰度
- 將時間戳記轉換為人類可讀格式(例如,「2024-01-15 10:30:00 UTC」而不是 epoch)
- 顯示帶有 ID 的顯示名稱(例如,「@john.doe (U123456)」)
- 省略冗長的中繼資料(例如,僅顯示一個個人資料圖片 URL,而不是所有尺寸)
- 邏輯分組相關資訊

**JSON 格式**:
- 返回適合程式化處理的完整結構化資料
- 包含所有可用欄位和中繼資料
- 使用一致的欄位名稱和類型

## 分頁實作

對於列出資源的工具:

```python
class ListInput(BaseModel):
    limit: Optional[int] = Field(default=20, description="要返回的最大結果數", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="用於分頁跳過的結果數", ge=0)

async def list_items(params: ListInput) -> str:
    # 使用分頁進行 API 請求
    data = await api_request(limit=params.limit, offset=params.offset)

    # 返回分頁資訊
    response = {
        "total": data["total"],
        "count": len(data["items"]),
        "offset": params.offset,
        "items": data["items"],
        "has_more": data["total"] > params.offset + len(data["items"]),
        "next_offset": params.offset + len(data["items"]) if data["total"] > params.offset + len(data["items"]) else None
    }
    return json.dumps(response, indent=2)
```

## 字元限制和截斷

添加 CHARACTER_LIMIT 常數以防止過多回應:

```python
# 在模組層級
CHARACTER_LIMIT = 25000  # 回應大小的最大字元數

async def search_tool(params: SearchInput) -> str:
    result = generate_response(data)

    # 檢查字元限制並在需要時截斷
    if len(result) > CHARACTER_LIMIT:
        # 截斷資料並添加通知
        truncated_data = data[:max(1, len(data) // 2)]
        response["data"] = truncated_data
        response["truncated"] = True
        response["truncation_message"] = (
            f"回應已從 {len(data)} 項截斷為 {len(truncated_data)} 項。"
            f"使用 'offset' 參數或添加過濾器以查看更多結果。"
        )
        result = json.dumps(response, indent=2)

    return result
```

## 錯誤處理

提供清晰、可操作的錯誤訊息:

```python
def _handle_api_error(e: Exception) -> str:
    '''所有工具的一致錯誤格式。'''
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            return "錯誤:未找到資源。請檢查 ID 是否正確。"
        elif e.response.status_code == 403:
            return "錯誤:拒絕存取。您沒有存取此資源的權限。"
        elif e.response.status_code == 429:
            return "錯誤:超過速率限制。請稍後再進行更多請求。"
        return f"錯誤:API 請求失敗,狀態為 {e.response.status_code}"
    elif isinstance(e, httpx.TimeoutException):
        return "錯誤:請求逾時。請重試。"
    return f"錯誤:發生意外錯誤:{type(e).__name__}"
```

## 共享實用程式

將常見功能提取到可重用函數中:

```python
# 共享 API 請求函數
async def _make_api_request(endpoint: str, method: str = "GET", **kwargs) -> dict:
    '''所有 API 調用的可重用函數。'''
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{API_BASE_URL}/{endpoint}",
            timeout=30.0,
            **kwargs
        )
        response.raise_for_status()
        return response.json()
```

## Async/Await 最佳實踐

始終對網路請求和 I/O 操作使用 async/await:

```python
# 良好:非同步網路請求
async def fetch_data(resource_id: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/resource/{resource_id}")
        response.raise_for_status()
        return response.json()

# 不良:同步請求
def fetch_data(resource_id: str) -> dict:
    response = requests.get(f"{API_URL}/resource/{resource_id}")  # 阻塞
    return response.json()
```

## 類型提示

在整個過程中使用類型提示:

```python
from typing import Optional, List, Dict, Any

async def get_user(user_id: str) -> Dict[str, Any]:
    data = await fetch_user(user_id)
    return {"id": data["id"], "name": data["name"]}
```

## 工具文件字串

每個工具都必須有包含明確類型資訊的全面文件字串:

```python
async def search_users(params: UserSearchInput) -> str:
    '''
    按名稱、電子郵件或團隊在範例系統中搜索使用者。

    此工具在範例平台中搜索所有使用者個人資料,
    支援部分匹配和各種搜索過濾器。它不會
    建立或修改使用者,僅搜索現有使用者。

    Args:
        params (UserSearchInput): 包含以下內容的驗證輸入參數:
            - query (str): 用於匹配名稱/電子郵件的搜索字串(例如,"john"、"@example.com"、"team:marketing")
            - limit (Optional[int]): 要返回的最大結果數,介於 1-100 之間(預設:20)
            - offset (Optional[int]): 用於分頁跳過的結果數(預設:0)

    Returns:
        str: 包含以下 schema 的搜索結果的 JSON 格式字串:

        成功回應:
        {
            "total": int,           # 找到的匹配總數
            "count": int,           # 此回應中的結果數
            "offset": int,          # 當前分頁偏移量
            "users": [
                {
                    "id": str,      # 使用者 ID(例如,"U123456789")
                    "name": str,    # 全名(例如,"John Doe")
                    "email": str,   # 電子郵件地址(例如,"john@example.com")
                    "team": str     # 團隊名稱(例如,"Marketing") - 可選
                }
            ]
        }

        錯誤回應:
        "錯誤:<錯誤訊息>" 或 "未找到與 '<query>' 匹配的使用者"

    Examples:
        - 使用時機:「找到所有行銷團隊成員」-> 使用 query="team:marketing" 的參數
        - 使用時機:「搜索 John 的帳戶」-> 使用 query="john" 的參數
        - 不要使用時機:您需要建立使用者(改用 example_create_user)
        - 不要使用時機:您有使用者 ID 且需要完整詳細資訊(改用 example_get_user)

    Error Handling:
        - 輸入驗證錯誤由 Pydantic 模型處理
        - 如果請求過多,返回「錯誤:超過速率限制」(429 狀態)
        - 如果 API key 無效,返回「錯誤:無效的 API 身份驗證」(401 狀態)
        - 返回格式化的結果列表或「未找到與 'query' 匹配的使用者」
    '''
```

## 完整範例

請參閱下面的完整 Python MCP server 範例:

```python
#!/usr/bin/env python3
'''
範例服務的 MCP Server。

此 server 提供與範例 API 互動的工具,包括使用者搜索、
專案管理和資料匯出功能。
'''

from typing import Optional, List, Dict, Any
from enum import Enum
import httpx
from pydantic import BaseModel, Field, field_validator, ConfigDict
from mcp.server.fastmcp import FastMCP

# 初始化 MCP server
mcp = FastMCP("example_mcp")

# 常數
API_BASE_URL = "https://api.example.com/v1"
CHARACTER_LIMIT = 25000  # 回應大小的最大字元數

# 列舉
class ResponseFormat(str, Enum):
    '''工具回應的輸出格式。'''
    MARKDOWN = "markdown"
    JSON = "json"

# 用於輸入驗證的 Pydantic 模型
class UserSearchInput(BaseModel):
    '''使用者搜索操作的輸入模型。'''
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True
    )

    query: str = Field(..., description="用於匹配名稱/電子郵件的搜索字串", min_length=2, max_length=200)
    limit: Optional[int] = Field(default=20, description="要返回的最大結果數", ge=1, le=100)
    offset: Optional[int] = Field(default=0, description="用於分頁跳過的結果數", ge=0)
    response_format: ResponseFormat = Field(default=ResponseFormat.MARKDOWN, description="輸出格式")

    @field_validator('query')
    @classmethod
    def validate_query(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("查詢不能為空或僅包含空格")
        return v.strip()

# 共享實用程式函數
async def _make_api_request(endpoint: str, method: str = "GET", **kwargs) -> dict:
    '''所有 API 調用的可重用函數。'''
    async with httpx.AsyncClient() as client:
        response = await client.request(
            method,
            f"{API_BASE_URL}/{endpoint}",
            timeout=30.0,
            **kwargs
        )
        response.raise_for_status()
        return response.json()

def _handle_api_error(e: Exception) -> str:
    '''所有工具的一致錯誤格式。'''
    if isinstance(e, httpx.HTTPStatusError):
        if e.response.status_code == 404:
            return "錯誤:未找到資源。請檢查 ID 是否正確。"
        elif e.response.status_code == 403:
            return "錯誤:拒絕存取。您沒有存取此資源的權限。"
        elif e.response.status_code == 429:
            return "錯誤:超過速率限制。請稍後再進行更多請求。"
        return f"錯誤:API 請求失敗,狀態為 {e.response.status_code}"
    elif isinstance(e, httpx.TimeoutException):
        return "錯誤:請求逾時。請重試。"
    return f"錯誤:發生意外錯誤:{type(e).__name__}"

# 工具定義
@mcp.tool(
    name="example_search_users",
    annotations={
        "title": "搜索範例使用者",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True
    }
)
async def example_search_users(params: UserSearchInput) -> str:
    '''按名稱、電子郵件或團隊在範例系統中搜索使用者。

    [如上所示的完整文件字串]
    '''
    try:
        # 使用驗證的參數進行 API 請求
        data = await _make_api_request(
            "users/search",
            params={
                "q": params.query,
                "limit": params.limit,
                "offset": params.offset
            }
        )

        users = data.get("users", [])
        total = data.get("total", 0)

        if not users:
            return f"未找到與 '{params.query}' 匹配的使用者"

        # 根據請求的格式格式化回應
        if params.response_format == ResponseFormat.MARKDOWN:
            lines = [f"# 使用者搜索結果:'{params.query}'", ""]
            lines.append(f"找到 {total} 個使用者(顯示 {len(users)} 個)")
            lines.append("")

            for user in users:
                lines.append(f"## {user['name']} ({user['id']})")
                lines.append(f"- **電子郵件**:{user['email']}")
                if user.get('team'):
                    lines.append(f"- **團隊**:{user['team']}")
                lines.append("")

            return "\n".join(lines)

        else:
            # 機器可讀的 JSON 格式
            import json
            response = {
                "total": total,
                "count": len(users),
                "offset": params.offset,
                "users": users
            }
            return json.dumps(response, indent=2)

    except Exception as e:
        return _handle_api_error(e)

if __name__ == "__main__":
    mcp.run()
```

---

## 進階 FastMCP 功能

### Context 參數注入

FastMCP 可以自動將 `Context` 參數注入工具中,以獲得進階功能,如記錄、進度報告、資源讀取和使用者互動:

```python
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("example_mcp")

@mcp.tool()
async def advanced_search(query: str, ctx: Context) -> str:
    '''具有用於記錄和進度的上下文存取的進階工具。'''

    # 為長操作報告進度
    await ctx.report_progress(0.25, "開始搜索...")

    # 記錄資訊以進行除錯
    await ctx.log_info("處理查詢", {"query": query, "timestamp": datetime.now()})

    # 執行搜索
    results = await search_api(query)
    await ctx.report_progress(0.75, "格式化結果...")

    # 存取 server 配置
    server_name = ctx.fastmcp.name

    return format_results(results)

@mcp.tool()
async def interactive_tool(resource_id: str, ctx: Context) -> str:
    '''可以從使用者請求額外輸入的工具。'''

    # 在需要時請求敏感資訊
    api_key = await ctx.elicit(
        prompt="請提供您的 API key:",
        input_type="password"
    )

    # 使用提供的 key
    return await api_call(resource_id, api_key)
```

**Context 功能:**
- `ctx.report_progress(progress, message)` - 為長操作報告進度
- `ctx.log_info(message, data)` / `ctx.log_error()` / `ctx.log_debug()` - 記錄
- `ctx.elicit(prompt, input_type)` - 從使用者請求輸入
- `ctx.fastmcp.name` - 存取 server 配置
- `ctx.read_resource(uri)` - 讀取 MCP 資源

### 資源註冊

將資料公開為資源以進行高效的基於模板的存取:

```python
@mcp.resource("file://documents/{name}")
async def get_document(name: str) -> str:
    '''將文件公開為 MCP 資源。

    資源對於不需要複雜參數的靜態或半靜態資料很有用。
    它們使用 URI 模板進行靈活存取。
    '''
    document_path = f"./docs/{name}"
    with open(document_path, "r") as f:
        return f.read()

@mcp.resource("config://settings/{key}")
async def get_setting(key: str, ctx: Context) -> str:
    '''將配置公開為具有上下文的資源。'''
    settings = await load_settings()
    return json.dumps(settings.get(key, {}))
```

**何時使用資源 vs 工具:**
- **資源**:用於具有簡單參數(URI 模板)的資料存取
- **工具**:用於具有驗證和業務邏輯的複雜操作

### 結構化輸出類型

FastMCP 支援除字串之外的多種返回類型:

```python
from typing import TypedDict
from dataclasses import dataclass
from pydantic import BaseModel

# 用於結構化返回的 TypedDict
class UserData(TypedDict):
    id: str
    name: str
    email: str

@mcp.tool()
async def get_user_typed(user_id: str) -> UserData:
    '''返回結構化資料 - FastMCP 處理序列化。'''
    return {"id": user_id, "name": "John Doe", "email": "john@example.com"}

# 用於複雜驗證的 Pydantic 模型
class DetailedUser(BaseModel):
    id: str
    name: str
    email: str
    created_at: datetime
    metadata: Dict[str, Any]

@mcp.tool()
async def get_user_detailed(user_id: str) -> DetailedUser:
    '''返回 Pydantic 模型 - 自動生成 schema。'''
    user = await fetch_user(user_id)
    return DetailedUser(**user)
```

### 生命週期管理

初始化在請求之間持續存在的資源:

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def app_lifespan():
    '''管理 server 生命週期內的資源。'''
    # 初始化連接、載入配置等
    db = await connect_to_database()
    config = load_configuration()

    # 使所有工具可用
    yield {"db": db, "config": config}

    # 關閉時清理
    await db.close()

mcp = FastMCP("example_mcp", lifespan=app_lifespan)

@mcp.tool()
async def query_data(query: str, ctx: Context) -> str:
    '''通過上下文存取生命週期資源。'''
    db = ctx.request_context.lifespan_state["db"]
    results = await db.query(query)
    return format_results(results)
```

### 多種傳輸選項

FastMCP 支援不同的傳輸機制:

```python
# 預設:Stdio transport(用於 CLI 工具)
if __name__ == "__main__":
    mcp.run()

# HTTP transport(用於 Web 服務)
if __name__ == "__main__":
    mcp.run(transport="streamable_http", port=8000)

# SSE transport(用於即時更新)
if __name__ == "__main__":
    mcp.run(transport="sse", port=8000)
```

**傳輸選擇:**
- **Stdio**:命令列工具、子程序整合
- **HTTP**:Web 服務、遠端存取、多個客戶端
- **SSE**:即時更新、推送通知

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

### Python 特定最佳實踐

1. **使用類型提示**:始終為函數參數和返回值包含類型註解
2. **Pydantic 模型**:為所有輸入驗證定義清晰的 Pydantic 模型
3. **避免手動驗證**:讓 Pydantic 使用約束處理輸入驗證
4. **適當的 Import**:分組 import(標準庫、第三方、本地)
5. **錯誤處理**:使用特定的異常類型(httpx.HTTPStatusError,而不是通用 Exception)
6. **非同步上下文管理器**:對需要清理的資源使用 `async with`
7. **常數**:在 UPPER_CASE 中定義模組層級常數

## 品質檢查清單

在完成 Python MCP server 實作之前,請確保:

### 策略設計
- [ ] 工具啟用完整工作流程,而不僅僅是 API 端點包裝器
- [ ] 工具名稱反映自然任務細分
- [ ] 回應格式針對代理上下文效率進行最佳化
- [ ] 在適當的地方使用人類可讀的識別碼
- [ ] 錯誤訊息引導代理朝向正確使用

### 實作品質
- [ ] 重點實作:實作了最重要和有價值的工具
- [ ] 所有工具都有描述性名稱和文件
- [ ] 類似操作的返回類型一致
- [ ] 為所有外部調用實作錯誤處理
- [ ] Server 名稱遵循格式:`{service}_mcp`
- [ ] 所有網路操作使用 async/await
- [ ] 常見功能提取到可重用函數中
- [ ] 錯誤訊息清晰、可操作且具有教育性
- [ ] 輸出已正確驗證和格式化

### 工具配置
- [ ] 所有工具在裝飾器中實作 'name' 和 'annotations'
- [ ] 註解正確設定(readOnlyHint、destructiveHint、idempotentHint、openWorldHint)
- [ ] 所有工具使用 Pydantic BaseModel 進行輸入驗證,並使用 Field() 定義
- [ ] 所有 Pydantic Field 具有明確的類型和帶約束的描述
- [ ] 所有工具具有包含明確輸入/輸出類型的全面文件字串
- [ ] 文件字串包含 dict/JSON 返回的完整 schema 結構
- [ ] Pydantic 模型處理輸入驗證(不需要手動驗證)

### 進階功能(適用時)
- [ ] Context 注入用於記錄、進度或引發
- [ ] 為適當的資料端點註冊資源
- [ ] 為持久連接實作生命週期管理
- [ ] 使用結構化輸出類型(TypedDict、Pydantic 模型)
- [ ] 配置適當的傳輸(stdio、HTTP、SSE)

### 程式碼品質
- [ ] 檔案包含適當的 import,包括 Pydantic import
- [ ] 在適用的地方正確實作分頁
- [ ] 大型回應檢查 CHARACTER_LIMIT 並使用清晰訊息截斷
- [ ] 為可能的大型結果集提供過濾選項
- [ ] 所有非同步函數都使用 `async def` 正確定義
- [ ] HTTP 客戶端使用遵循具有適當上下文管理器的非同步模式
- [ ] 在整個程式碼中使用類型提示
- [ ] 常數在模組層級以 UPPER_CASE 定義

### 測試
- [ ] Server 成功執行:`python your_server.py --help`
- [ ] 所有 import 正確解析
- [ ] 範例工具調用按預期工作
- [ ] 錯誤場景優雅處理
