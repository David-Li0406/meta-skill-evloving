# MCP Server 評估指南

## 概述

本文件提供建立 MCP server 綜合評估的指導。評估測試 LLM 是否能夠僅使用提供的工具,有效地使用您的 MCP server 來回答真實、複雜的問題。

---

## 快速參考

### 評估要求
- 建立 10 個人類可讀的問題
- 問題必須是唯讀、獨立、非破壞性的
- 每個問題需要多次工具調用(可能數十次)
- 答案必須是單一、可驗證的值
- 答案必須是穩定的(不會隨時間改變)

### 輸出格式
```xml
<evaluation>
   <qa_pair>
      <question>您的問題在這裡</question>
      <answer>單一可驗證答案</answer>
   </qa_pair>
</evaluation>
```

---

## 評估的目的

MCP server 品質的衡量標準不是 server 實作工具的完善或全面程度,而是這些實作(輸入/輸出 schema、文件字串/描述、功能)如何讓沒有其他上下文且僅能訪問 MCP server 的 LLM 能夠回答真實且困難的問題。

## 評估概述

建立 10 個人類可讀的問題,僅需要唯讀、獨立、非破壞性和冪等操作來回答。每個問題應該是:
- 真實的
- 清晰簡潔
- 明確無歧義
- 複雜,可能需要數十次工具調用或步驟
- 可以用您事先確定的單一、可驗證的值來回答

## 問題指南

### 核心要求

1. **問題必須是獨立的**
   - 每個問題不應該依賴於任何其他問題的答案
   - 不應假設處理另一個問題時的先前寫入操作

2. **問題必須僅需要非破壞性和冪等的工具使用**
   - 不應指示或要求修改狀態來得出正確答案

3. **問題必須是真實、清晰、簡潔和複雜的**
   - 必須需要另一個 LLM 使用多個(可能數十個)工具或步驟來回答

### 複雜度和深度

4. **問題必須需要深入探索**
   - 考慮需要多個子問題和連續工具調用的多跳問題
   - 每個步驟都應該從先前問題中發現的資訊中受益

5. **問題可能需要大量分頁**
   - 可能需要翻閱多頁結果
   - 可能需要查詢舊資料(1-2 年過時)以尋找特定資訊
   - 問題必須是困難的

6. **問題必須需要深入理解**
   - 而不是表面層次的知識
   - 可以將複雜的想法作為需要證據的真/假問題
   - 可以使用多選格式,LLM 必須搜索不同的假設

7. **問題不能用直接的關鍵字搜索解決**
   - 不要包含目標內容的特定關鍵字
   - 使用同義詞、相關概念或改述
   - 需要多次搜索、分析多個相關項目、提取上下文,然後推導答案

### 工具測試

8. **問題應該壓力測試工具返回值**
   - 可能引發工具返回大型 JSON 物件或列表,淹沒 LLM
   - 應該需要理解多種資料模式:
     - ID 和名稱
     - 時間戳記和日期時間(月、日、年、秒)
     - 檔案 ID、名稱、副檔名和 mimetype
     - URL、GID 等
   - 應該測試工具返回所有有用資料形式的能力

9. **問題應該主要反映真實的人類使用案例**
   - 由 LLM 協助的人類關心的資訊檢索任務種類

10. **問題可能需要數十次工具調用**
    - 這對上下文有限的 LLM 構成挑戰
    - 鼓勵 MCP server 工具減少返回的資訊

11. **包含模糊問題**
    - 可能是模糊的或需要對調用哪些工具做出困難的決定
    - 迫使 LLM 可能犯錯或誤解
    - 確保儘管有歧義,仍然有單一可驗證的答案

### 穩定性

12. **問題必須設計為答案不會改變**
    - 不要問依賴於動態的「當前狀態」的問題
    - 例如,不要計數:
      - 貼文的反應數量
      - 討論串的回覆數量
      - 頻道中的成員數量

13. **不要讓 MCP server 限制您建立的問題種類**
    - 建立具有挑戰性和複雜性的問題
    - 有些問題可能無法用可用的 MCP server 工具解決
    - 問題可能需要特定的輸出格式(日期時間 vs. epoch 時間、JSON vs. MARKDOWN)
    - 問題可能需要數十次工具調用才能完成

## 答案指南

### 驗證

1. **答案必須可通過直接字串比較驗證**
   - 如果答案可以用多種格式重寫,請在問題中明確指定輸出格式
   - 範例:「使用 YYYY/MM/DD。」、「回答 True 或 False。」、「回答 A、B、C 或 D,不要其他內容。」
   - 答案應該是單一可驗證的值,例如:
     - 使用者 ID、使用者名稱、顯示名稱、名字、姓氏
     - 頻道 ID、頻道名稱
     - 訊息 ID、字串
     - URL、標題
     - 數值
     - 時間戳記、日期時間
     - 布林值(對於真/假問題)
     - 電子郵件地址、電話號碼
     - 檔案 ID、檔案名稱、副檔名
     - 多選答案
   - 答案不能需要特殊格式或複雜的結構化輸出
   - 答案將使用直接字串比較進行驗證

### 可讀性

2. **答案通常應該偏好人類可讀格式**
   - 範例:名稱、名字、姓氏、日期時間、檔案名稱、訊息字串、URL、是/否、真/假、a/b/c/d
   - 而不是不透明的 ID(雖然 ID 是可以接受的)
   - 絕大多數答案應該是人類可讀的

### 穩定性

3. **答案必須是穩定/固定的**
   - 查看舊內容(例如,已結束的對話、已啟動的專案、已回答的問題)
   - 基於「已關閉」的概念建立問題,這些概念將始終返回相同的答案
   - 問題可能要求考慮固定的時間窗口,以隔離非固定答案
   - 依賴不太可能改變的上下文
   - 範例:如果尋找論文名稱,要足夠具體,使答案不會與後來發表的論文混淆

4. **答案必須清晰明確**
   - 問題必須設計為有單一、明確的答案
   - 答案可以從使用 MCP server 工具中推導出來

### 多樣性

5. **答案必須是多樣化的**
   - 答案應該是不同模式和格式的單一可驗證值
   - 使用者概念:使用者 ID、使用者名稱、顯示名稱、名字、姓氏、電子郵件地址、電話號碼
   - 頻道概念:頻道 ID、頻道名稱、頻道主題
   - 訊息概念:訊息 ID、訊息字串、時間戳記、月、日、年

6. **答案不能是複雜結構**
   - 不是值的列表
   - 不是複雜物件
   - 不是 ID 或字串的列表
   - 不是自然語言文字
   - 除非答案可以使用直接字串比較直接驗證
   - 並且可以實際重現
   - LLM 不太可能以任何其他順序或格式返回相同的列表

## 評估流程

### 步驟 1:文件檢查

閱讀目標 API 的文件以了解:
- 可用的端點和功能
- 如果存在歧義,從網路獲取額外資訊
- 盡可能並行化此步驟
- 確保每個子代理僅檢查檔案系統或網路上的文件

### 步驟 2:工具檢查

列出 MCP server 中可用的工具:
- 直接檢查 MCP server
- 了解輸入/輸出 schema、文件字串和描述
- 在此階段不調用工具本身

### 步驟 3:發展理解

重複步驟 1 和 2 直到您有良好的理解:
- 多次迭代
- 思考您想建立的任務種類
- 完善您的理解
- 在任何階段都不應該閱讀 MCP server 實作本身的程式碼
- 使用您的直覺和理解來建立合理、真實但非常具有挑戰性的任務

### 步驟 4:唯讀內容檢查

在理解 API 和工具後,使用 MCP server 工具:
- 僅使用唯讀和非破壞性操作檢查內容
- 目標:識別特定內容(例如,使用者、頻道、訊息、專案、任務)以建立真實問題
- 不應該調用任何修改狀態的工具
- 不會閱讀 MCP server 實作本身的程式碼
- 使用單獨的子代理並行化此步驟,進行獨立探索
- 確保每個子代理僅執行唯讀、非破壞性和冪等操作
- 注意:某些工具可能返回大量資料,這會導致您耗盡上下文
- 進行漸進式、小型和有針對性的工具調用進行探索
- 在所有工具調用請求中,使用 `limit` 參數限制結果(<10)
- 使用分頁

### 步驟 5:任務生成

在檢查內容後,建立 10 個人類可讀的問題:
- LLM 應該能夠使用 MCP server 回答這些問題
- 遵循上述所有問題和答案指南

## 輸出格式

每個 QA 對由一個問題和一個答案組成。輸出應該是具有此結構的 XML 檔案:

```xml
<evaluation>
   <qa_pair>
      <question>找到 2024 年第二季度建立的具有最多已完成任務的專案。專案名稱是什麼?</question>
      <answer>Website Redesign</answer>
   </qa_pair>
   <qa_pair>
      <question>搜索標記為「bug」且在 2024 年 3 月關閉的 issue。哪個使用者關閉了最多的 issue?提供他們的使用者名稱。</question>
      <answer>sarah_dev</answer>
   </qa_pair>
   <qa_pair>
      <question>尋找修改了 /api 目錄中檔案並在 2024 年 1 月 1 日至 1 月 31 日之間合併的 pull request。有多少不同的貢獻者參與了這些 PR?</question>
      <answer>7</answer>
   </qa_pair>
   <qa_pair>
      <question>找到在 2023 年之前建立的具有最多星標的儲存庫。儲存庫名稱是什麼?</question>
      <answer>data-pipeline</answer>
   </qa_pair>
</evaluation>
```

## 評估範例

### 好的問題

**範例 1:需要深入探索的多跳問題(GitHub MCP)**
```xml
<qa_pair>
   <question>找到在 2023 年第三季度歸檔且之前是組織中被 fork 最多的專案的儲存庫。該儲存庫使用的主要程式語言是什麼?</question>
   <answer>Python</answer>
</qa_pair>
```

這個問題很好,因為:
- 需要多次搜索才能找到歸檔的儲存庫
- 需要識別在歸檔前哪個具有最多 fork
- 需要檢查儲存庫詳細資訊以獲取語言
- 答案是簡單、可驗證的值
- 基於不會改變的歷史(已關閉)資料

**範例 2:需要在沒有關鍵字匹配的情況下理解上下文(專案管理 MCP)**
```xml
<qa_pair>
   <question>找到專注於改善客戶入職並在 2023 年底完成的計畫。專案負責人在完成後建立了回顧文件。當時負責人的角色職稱是什麼?</question>
   <answer>Product Manager</answer>
</qa_pair>
```

這個問題很好,因為:
- 不使用特定專案名稱(「專注於改善客戶入職的計畫」)
- 需要從特定時間範圍找到已完成的專案
- 需要識別專案負責人及其角色
- 需要從回顧文件中理解上下文
- 答案是人類可讀且穩定的
- 基於已完成的工作(不會改變)

**範例 3:需要多個步驟的複雜聚合(Issue Tracker MCP)**
```xml
<qa_pair>
   <question>在 2024 年 1 月報告的所有標記為關鍵優先級的 bug 中,哪個受讓人在 48 小時內解決了分配給他們的 bug 的最高百分比?提供受讓人的使用者名稱。</question>
   <answer>alex_eng</answer>
</qa_pair>
```

這個問題很好,因為:
- 需要按日期、優先級和狀態過濾 bug
- 需要按受讓人分組並計算解決率
- 需要理解時間戳記以確定 48 小時窗口
- 測試分頁(可能有許多 bug 需要處理)
- 答案是單一使用者名稱
- 基於特定時間段的歷史資料

**範例 4:需要跨多種資料類型合成(CRM MCP)**
```xml
<qa_pair>
   <question>找到在 2023 年第四季度從 Starter 升級到 Enterprise 方案並具有最高年度合約價值的帳戶。該帳戶經營的行業是什麼?</question>
   <answer>Healthcare</answer>
</qa_pair>
```

這個問題很好,因為:
- 需要理解訂閱層級變更
- 需要識別特定時間範圍內的升級事件
- 需要比較合約價值
- 必須存取帳戶行業資訊
- 答案簡單且可驗證
- 基於已完成的歷史交易

### 不好的問題

**範例 1:答案會隨時間改變**
```xml
<qa_pair>
   <question>目前分配給工程團隊的未解決 issue 有多少個?</question>
   <answer>47</answer>
</qa_pair>
```

這個問題不好,因為:
- 隨著 issue 的建立、關閉或重新分配,答案會改變
- 不基於穩定/固定的資料
- 依賴於動態的「當前狀態」

**範例 2:使用關鍵字搜索太容易**
```xml
<qa_pair>
   <question>找到標題為「Add authentication feature」的 pull request 並告訴我是誰建立的。</question>
   <answer>developer123</answer>
</qa_pair>
```

這個問題不好,因為:
- 可以用直接的關鍵字搜索精確標題來解決
- 不需要深入探索或理解
- 不需要合成或分析

**範例 3:答案格式模糊**
```xml
<qa_pair>
   <question>列出所有將 Python 作為主要語言的儲存庫。</question>
   <answer>repo1, repo2, repo3, data-pipeline, ml-tools</answer>
</qa_pair>
```

這個問題不好,因為:
- 答案是可以以任何順序返回的列表
- 難以用直接字串比較驗證
- LLM 可能以不同格式(JSON 陣列、逗號分隔、換行分隔)
- 更好的方法是詢問特定的聚合(計數)或最高級(最多星標)

## 驗證流程

建立評估後:

1. **檢查 XML 檔案**以了解 schema
2. **載入每個任務指令**並使用 MCP server 和工具並行嘗試自己解決任務以識別正確答案
3. **標記任何需要寫入或破壞性操作的操作**
4. **累積所有正確答案**並替換文件中任何不正確的答案
5. **刪除任何需要寫入或破壞性操作的 `<qa_pair>`**

記住並行解決任務以避免耗盡上下文,然後累積所有答案並在最後對檔案進行更改。

## 建立高品質評估的提示

1. **在生成任務前仔細思考和提前計劃**
2. **在有機會時並行化**以加速流程並管理上下文
3. **專注於真實使用案例**,人類實際上想要完成的事情
4. **建立具有挑戰性的問題**,測試 MCP server 能力的極限
5. **確保穩定性**,使用歷史資料和已關閉的概念
6. **驗證答案**,通過使用 MCP server 工具自己解決問題
7. **根據流程中學到的內容迭代和完善**

---

# 執行評估

建立評估檔案後,您可以使用提供的評估工具來測試您的 MCP server。

## 設定

1. **安裝依賴項**

   ```bash
   pip install -r scripts/requirements.txt
   ```

   或手動安裝:
   ```bash
   pip install anthropic mcp
   ```

2. **設定 API Key**

   ```bash
   export ANTHROPIC_API_KEY=your_api_key_here
   ```

## 評估檔案格式

評估檔案使用帶有 `<qa_pair>` 元素的 XML 格式:

```xml
<evaluation>
   <qa_pair>
      <question>找到 2024 年第二季度建立的具有最多已完成任務的專案。專案名稱是什麼?</question>
      <answer>Website Redesign</answer>
   </qa_pair>
   <qa_pair>
      <question>搜索標記為「bug」且在 2024 年 3 月關閉的 issue。哪個使用者關閉了最多的 issue?提供他們的使用者名稱。</question>
      <answer>sarah_dev</answer>
   </qa_pair>
</evaluation>
```

## 執行評估

評估腳本(`scripts/evaluation.py`)支援三種傳輸類型:

**重要:**
- **stdio transport**:評估腳本會自動為您啟動和管理 MCP server 程序。不要手動執行 server。
- **sse/http transports**:您必須在執行評估之前單獨啟動 MCP server。腳本會連接到指定 URL 上已執行的 server。

### 1. 本地 STDIO Server

對於本地執行的 MCP server(腳本自動啟動 server):

```bash
python scripts/evaluation.py \
  -t stdio \
  -c python \
  -a my_mcp_server.py \
  evaluation.xml
```

使用環境變數:
```bash
python scripts/evaluation.py \
  -t stdio \
  -c python \
  -a my_mcp_server.py \
  -e API_KEY=abc123 \
  -e DEBUG=true \
  evaluation.xml
```

### 2. Server-Sent Events (SSE)

對於基於 SSE 的 MCP server(您必須先啟動 server):

```bash
python scripts/evaluation.py \
  -t sse \
  -u https://example.com/mcp \
  -H "Authorization: Bearer token123" \
  -H "X-Custom-Header: value" \
  evaluation.xml
```

### 3. HTTP (Streamable HTTP)

對於基於 HTTP 的 MCP server(您必須先啟動 server):

```bash
python scripts/evaluation.py \
  -t http \
  -u https://example.com/mcp \
  -H "Authorization: Bearer token123" \
  evaluation.xml
```

## 命令列選項

```
usage: evaluation.py [-h] [-t {stdio,sse,http}] [-m MODEL] [-c COMMAND]
                     [-a ARGS [ARGS ...]] [-e ENV [ENV ...]] [-u URL]
                     [-H HEADERS [HEADERS ...]] [-o OUTPUT]
                     eval_file

positional arguments:
  eval_file             評估 XML 檔案的路徑

optional arguments:
  -h, --help            顯示幫助訊息
  -t, --transport       傳輸類型:stdio、sse 或 http(預設:stdio)
  -m, --model           要使用的 Claude 模型(預設:claude-3-7-sonnet-20250219)
  -o, --output          報告的輸出檔案(預設:列印到 stdout)

stdio options:
  -c, --command         執行 MCP server 的命令(例如,python、node)
  -a, --args            命令的參數(例如,server.py)
  -e, --env             KEY=VALUE 格式的環境變數

sse/http options:
  -u, --url             MCP server URL
  -H, --header          'Key: Value' 格式的 HTTP 標頭
```

## 輸出

評估腳本生成詳細報告,包括:

- **摘要統計**:
  - 準確率(正確/總數)
  - 每個任務的平均持續時間
  - 每個任務的平均工具調用次數
  - 總工具調用次數

- **每個任務的結果**:
  - 提示和預期回應
  - 代理的實際回應
  - 答案是否正確(✅/❌)
  - 持續時間和工具調用詳細資訊
  - 代理對其方法的總結
  - 代理對工具的反饋

### 將報告儲存到檔案

```bash
python scripts/evaluation.py \
  -t stdio \
  -c python \
  -a my_server.py \
  -o evaluation_report.md \
  evaluation.xml
```

## 完整範例工作流程

以下是建立和執行評估的完整範例:

1. **建立您的評估檔案**(`my_evaluation.xml`):

```xml
<evaluation>
   <qa_pair>
      <question>找到在 2024 年 1 月建立最多 issue 的使用者。他們的使用者名稱是什麼?</question>
      <answer>alice_developer</answer>
   </qa_pair>
   <qa_pair>
      <question>在 2024 年第一季度合併的所有 pull request 中,哪個儲存庫的數量最多?提供儲存庫名稱。</question>
      <answer>backend-api</answer>
   </qa_pair>
   <qa_pair>
      <question>找到在 2023 年 12 月完成且從開始到完成持續時間最長的專案。花了多少天?</question>
      <answer>127</answer>
   </qa_pair>
</evaluation>
```

2. **安裝依賴項**:

```bash
pip install -r scripts/requirements.txt
export ANTHROPIC_API_KEY=your_api_key
```

3. **執行評估**:

```bash
python scripts/evaluation.py \
  -t stdio \
  -c python \
  -a github_mcp_server.py \
  -e GITHUB_TOKEN=ghp_xxx \
  -o github_eval_report.md \
  my_evaluation.xml
```

4. **檢查報告**(`github_eval_report.md`)以:
   - 查看哪些問題通過/失敗
   - 閱讀代理對您工具的反饋
   - 識別需要改進的領域
   - 迭代您的 MCP server 設計

## 疑難排解

### 連接錯誤

如果遇到連接錯誤:
- **STDIO**:驗證命令和參數是否正確
- **SSE/HTTP**:檢查 URL 是否可訪問且標頭是否正確
- 確保在環境變數或標頭中設定任何必需的 API key

### 準確率低

如果許多評估失敗:
- 檢查代理對每個任務的反饋
- 檢查工具描述是否清晰且全面
- 驗證輸入參數是否有良好的文件
- 考慮工具返回的資料是太多還是太少
- 確保錯誤訊息是可操作的

### 逾時問題

如果任務逾時:
- 使用更強大的模型(例如,`claude-3-7-sonnet-20250219`)
- 檢查工具是否返回太多資料
- 驗證分頁是否正常工作
- 考慮簡化複雜問題
