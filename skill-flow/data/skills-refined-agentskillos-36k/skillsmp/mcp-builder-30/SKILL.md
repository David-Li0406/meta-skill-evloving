---
name: mcp-builder
description: 建立高品質 MCP (Model Context Protocol) 伺服器的指南，使 LLM 能夠透過精心設計的工具與外部服務互動。適用於建立 MCP 伺服器以整合外部 API 或服務，無論是使用 Python (FastMCP) 或 Node/TypeScript (MCP SDK)。
license: Complete terms in LICENSE.txt
---

# MCP 伺服器開發指南

## 概述

使用此技能來建立高品質的 MCP (Model Context Protocol) 伺服器，使 LLM 能夠有效地與外部服務互動。MCP 伺服器提供工具，允許 LLM 存取外部服務和 API。MCP 伺服器的品質取決於它能多好地讓 LLM 使用提供的工具完成真實世界的任務。

---

# 流程

## 🚀 高階工作流程

建立高品質的 MCP 伺服器涉及四個主要階段：

### 階段 1：深入研究與規劃

#### 1.1 理解以代理為中心的設計原則

在深入實作之前，請先透過檢視這些原則來理解如何為 AI 代理設計工具：

**為工作流程而非僅為 API 端點建立：**
- 不要只是包裝現有的 API 端點 - 建立深思熟慮、高影響力的工作流程工具
- 整合相關操作（例如，`schedule_event` 既檢查可用性又建立事件）
- 專注於能夠完成完整任務的工具，而不僅僅是單個 API 呼叫
- 考慮代理實際需要完成的工作流程

**針對有限的上下文進行最佳化：**
- 代理的上下文視窗有限 - 讓每個 token 都有價值
- 回傳高訊號資訊，而非詳盡的資料轉儲
- 提供「簡潔」與「詳細」回應格式選項
- 預設使用人類可讀的識別符而非技術代碼（名稱而非 ID）
- 將代理的上下文預算視為稀缺資源

**設計可操作的錯誤訊息：**
- 錯誤訊息應引導代理朝向正確的使用模式
- 建議具體的下一步：「嘗試使用 filter='active_only' 來減少結果」
- 讓錯誤具有教育性，而不僅僅是診斷性
- 透過清晰的回饋幫助代理學習正確的工具使用方式

**遵循自然任務細分：**
- 工具名稱應反映人類對任務的思考方式
- 使用一致的前綴將相關工具分組以提高可發現性
- 圍繞自然工作流程設計工具，而不僅僅是 API 結構

**使用評估驅動開發：**
- 及早建立實際的評估場景
- 讓代理回饋驅動工具改進
- 快速原型製作並根據實際代理效能進行迭代

#### 1.3 研究 MCP 協定文件

**取得最新的 MCP 協定文件：**

使用 WebFetch 載入：`https://modelcontextprotocol.io/llms-full.txt`

此綜合文件包含完整的 MCP 規範和指南。

#### 1.4 研究框架文件

**載入並閱讀以下參考檔案：**

- **MCP 最佳實踐**：[📋 檢視最佳實踐](./reference/mcp_best_practices.md) - 所有 MCP 伺服器的核心指南

**對於 Python 實作，也請載入：**
- **Python SDK 文件**：使用 WebFetch 載入 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- [🐍 Python 實作指南](./reference/python_mcp_server.md) - Python 特定的最佳實踐和範例

**對於 Node/TypeScript 實作，也請載入：**
- **TypeScript SDK 文件**：使用 WebFetch 載入 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- [⚡ TypeScript 實作指南](./reference/node_mcp_server.md) - Node/TypeScript 特定的最佳實踐和範例

#### 1.5 詳盡研究 API 文件

要整合服務，請閱讀**所有**可用的 API 文件：
- 官方 API 參考文件
- 身份驗證和授權要求
- 速率限制和分頁模式
- 錯誤回應和狀態碼
- 可用的端點及其參數
- 資料模型和架構

**為了收集全面的資訊，請根據需要使用網路搜尋和 WebFetch 工具。**

#### 1.6 建立全面的實作計劃

根據您的研究，建立包含以下內容的詳細計劃：

**工具選擇：**
- 列出要實作的最有價值的端點/操作
- 優先考慮能夠實現最常見和重要用例的工具
- 考慮哪些工具可以共同實現複雜的工作流程

**共用工具和輔助程式：**
- 識別常見的 API 請求模式
- 規劃分頁輔助程式
- 設計篩選和格式化工具
- 規劃錯誤處理策略

**輸入/輸出設計：**
- 定義輸入驗證模型（Python 使用 Pydantic，TypeScript 使用 Zod）
- 設計一致的回應格式（例如 JSON 或 Markdown），以及可配置的詳細程度（例如詳細或簡潔）
- 針對大規模使用進行規劃（數千名使用者/資源）
- 實作字元限制和截斷策略（例如 25,000 個 token）

**錯誤處理策略：**
- 規劃優雅的失敗模式
- 設計清晰、可操作、LLM 友善的自然語言錯誤訊息，提示進一步的操作
- 考慮速率限制和逾時場景
- 處理身份驗證和授權錯誤

---

### 階段 2：實作

現在您已有全面的計劃，請遵循特定語言的最佳實踐開始實作。

#### 2.1 設定專案結構

**對於 Python：**
- 建立單一 `.py` 檔案，或如果複雜則組織成模組（參見 [🐍 Python 指南](./reference/python_mcp_server.md)）
- 使用 MCP Python SDK 進行工具註冊
- 定義 Pydantic 模型進行輸入驗證

**對於 Node/TypeScript：**
- 建立適當的專案結構（參見 [⚡ TypeScript 指南](./reference/node_mcp_server.md)）
- 設定 `package.json` 和 `tsconfig.json`
- 使用 MCP TypeScript SDK
- 定義 Zod 架構進行輸入驗證

#### 2.2 先實作核心基礎設施

**要開始實作，請在實作工具之前建立共用工具：**
- API 請求輔助函式
- 錯誤處理工具
- 回應格式化函式（JSON 和 Markdown）
- 分頁輔助程式
- 身份驗證/token 管理

#### 2.3 系統化地實作工具

對於計劃中的每個工具：

**定義輸入架構：**
- 使用 Pydantic（Python）或 Zod（TypeScript）進行驗證
- 包含適當的約束（最小/最大長度、regex 模式、最小/最大值、範圍）
- 提供清晰、描述性的欄位說明
- 在欄位說明中包含多樣化的範例

**撰寫全面的文件字串/說明：**
- 工具功能的單行摘要
- 目的和功能的詳細說明
- 明確的參數類型與範例
- 完整的回傳類型架構
- 使用範例（何時使用、何時不使用）
- 錯誤處理文件，概述在特定錯誤時如何處理

**實作工具邏輯：**
- 使用共用工具避免程式碼重複
- 對所有 I/O 遵循 async/await 模式
- 實作適當的錯誤處理
- 支援多種回應格式（JSON 和 Markdown）
- 尊重分頁參數
- 檢查字元限制並適當截斷

**新增工具註解：**
- `readOnlyHint`: true（用於唯讀操作）
- `destructiveHint`: false（用於非破壞性操作）
- `idempotentHint`: true（如果重複呼叫具有相同效果）
- `openWorldHint`: true（如果與外部系統互動）

#### 2.4 遵循特定語言的最佳實踐

**此時，請載入適當的語言指南：**

**對於 Python：載入 [🐍 Python 實作指南](./reference/python_mcp_server.md) 並確保以下事項：**
- 使用 MCP Python SDK 進行適當的工具註冊
- 使用 `model_config` 的 Pydantic v2 模型
- 全面使用類型提示
- 對所有 I/O 操作使用 Async/await
- 適當的 import 組織
- 模組層級常數（CHARACTER_LIMIT、API_BASE_URL）

**對於 Node/TypeScript：載入 [⚡ TypeScript 實作指南](./reference/node_mcp_server.md) 並確保以下事項：**
- 正確使用 `server.registerTool`
- 使用 `.strict()` 的 Zod 架構
- 啟用 TypeScript 嚴格模式
- 不使用 `any` 類型 - 使用適當的類型
- 明確的 Promise<T> 回傳類型
- 配置建置過程（`npm run build`）

---

### 階段 3：檢視和優化

初始實作後：

#### 3.1 程式碼品質檢視

為確保品質，請檢視程式碼的：
- **DRY 原則**：工具之間沒有重複的程式碼
- **可組合性**：將共用邏輯提取到函式中
- **一致性**：類似的操作回傳類似的格式
- **錯誤處理**：所有外部呼叫都有錯誤處理
- **類型安全**：完整的類型覆蓋（Python 類型提示、TypeScript 類型）
- **文件**：每個工具都有全面的文件字串/說明

#### 3.2 測試和建置

**重要：** MCP 伺服器是長時間執行的進程，透過 stdio/stdin 或 sse/http 等待請求。在主進程中直接執行它們（例如 `python server.py` 或 `node dist/index.js`）會導致進程無限期掛起。

**測試伺服器的安全方式：**
- 使用評估測試工具（參見階段 4）- 建議的方法
- 在 tmux 中執行伺服器，使其在主進程之外
- 測試時使用逾時：`timeout 5s python server.py`

**對於 Python：**
- 驗證 Python 語法：`python -m py_compile your_server.py`
- 透過檢視檔案來檢查 import 是否正常運作
- 手動測試：在 tmux 中執行伺服器，然後在主進程中使用評估測試工具進行測試
- 或直接使用評估測試工具（它為 stdio 傳輸管理伺服器）

**對於 Node/TypeScript：**
- 執行 `npm run build` 並確保無錯誤完成
- 驗證 dist/index.js 已建立
- 手動測試：在 tmux 中執行伺服器，然後在主進程中使用評估測試工具進行測試
- 或直接使用評估測試工具（它為 stdio 傳輸管理伺服器）

#### 3.3 使用品質檢查清單

為驗證實作品質，請從特定語言指南載入適當的檢查清單：
- Python：參見 [🐍 Python 指南](./reference/python_mcp_server.md) 中的「品質檢查清單」
- Node/TypeScript：參見 [⚡ TypeScript 指南](./reference/node_mcp_server.md) 中的「品質檢查清單」

---

### 階段 4：建立評估

實作 MCP 伺服器後，建立全面的評估來測試其效能。

**載入 [✅ 評估指南](./reference/evaluation.md) 以取得完整的評估指南。**

#### 4.1 理解評估目的

評估測試 LLM 是否能有效使用您的 MCP 伺服器來回答實際的複雜問題。

#### 4.2 建立 10 個評估問題

要建立有效的評估，請遵循評估指南中概述的流程：

1. **工具檢查**：列出可用工具並理解其功能
2. **內容探索**：使用唯讀操作探索可用資料
3. **問題生成**：建立 10 個複雜、實際的問題
4. **答案驗證**：自己解決每個問題以驗證答案

#### 4.3 評估要求

每個問題必須：
- **獨立**：不依賴其他問題
- **唯讀**：僅需要非破壞性操作
- **複雜**：需要多次工具呼叫和深入探索
- **實際**：基於人類關心的真實用例
- **可驗證**：單一、清晰的答案，可透過字串比較驗證
- **穩定**：答案不會隨時間改變

#### 4.4 輸出格式

使用此結構建立 XML 檔案：

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

---

# 參考檔案

## 📚 文件庫

在開發期間根據需要載入這些資源：

### 核心 MCP 文件（首先載入）
- **MCP 協定**：從 `https://modelcontextprotocol.io/llms-full.txt` 取得 - 完整的 MCP 規範
- [📋 MCP 最佳實踐](./reference/mcp_best_practices.md) - 通用 MCP 指南，包括：
  - 伺服器和工具命名慣例
  - 回應格式指南（JSON vs Markdown）
  - 分頁最佳實踐
  - 字元限制和截斷策略
  - 工具開發指南
  - 安全性和錯誤處理標準

### SDK 文件（在階段 1/2 期間載入）
- **Python SDK**：從 `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` 取得
- **TypeScript SDK**：從 `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` 取得

### 特定語言實作指南（在階段 2 期間載入）
- [🐍 Python 實作指南](./reference/python_mcp_server.md) - 完整的 Python/FastMCP 指南，包含：
  - 伺服器初始化模式
  - Pydantic 模型範例
  - 使用 `@mcp.tool` 進行工具註冊
  - 完整的工作範例
  - 品質檢查清單

- [⚡ TypeScript 實作指南](./reference/node_mcp_server.md) - 完整的 TypeScript 指南，包含：
  - 專案結構
  - Zod 架構模式
  - 使用 `server.registerTool` 進行工具註冊
  - 完整的工作範例
  - 品質檢查清單

### 評估指南（在階段 4 期間載入）
- [✅ 評估指南](./reference/evaluation.md) - 完整的評估建立指南，包含：
  - 問題建立指南
  - 答案驗證策略
  - XML 格式規範
  - 問題和答案範例
  - 使用提供的腳本執行評估
