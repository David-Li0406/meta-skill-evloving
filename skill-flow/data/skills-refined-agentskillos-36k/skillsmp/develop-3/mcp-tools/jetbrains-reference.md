# JetBrains MCP Tools 使用參考

## 概述

JetBrains MCP 提供程式碼品質檢查、格式化、重構等功能，整合 IDE 的智能分析能力。

**核心優勢**:
- 利用 IDE 的索引和靜態分析引擎
- 自動過濾 IDE 排除的檔案（node_modules、.git 等）
- 比 CLI 工具更快、更準確
- 符合 Claude Code 最佳實踐（避免不必要的 Bash 指令）

---

## 使用時機指南

依據 Claude Code 最佳實踐，應**優先使用 JetBrains MCP** 而非 Bash/CLI 工具。

### 1. 專案導航與結構分析 (Project Navigation)

這類指令適合在任務開始前，幫助建立「專案地圖感」。

#### ✅ 優先使用: `list_directory_tree`

**取代**: `tree` CLI 指令

**時機**: 當你剛開啟新任務，想了解特定目錄（如 `src/services`）下有哪些檔案。

**優勢**:
- 自動過濾 IDE 排除的檔案（node_modules、.git、.next）
- 尊重 .gitignore 和 IDE 設定
- 輸出更乾淨、更聚焦

**範例**:
```typescript
// ✅ Good: 使用 JetBrains MCP
mcp__jetbrains__list_directory_tree({
    directoryPath: 'frontend/src/server',
    maxDepth: 3,
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// ❌ Bad: 使用 CLI (輸出包含雜訊)
Bash({ command: 'tree frontend/src/server -L 3' });
```

**輸出範例**:
```
frontend/src/server/
├── db/
│   ├── schema.ts
│   └── index.ts
├── services/
│   ├── order.ts
│   └── ticket.ts
└── api/
    └── events.ts
```

---

#### ✅ 優先使用: `find_files_by_glob` / `find_files_by_name_keyword`

**取代**: `find` CLI 或 `ls` 指令

**時機**: 需要尋找特定類型或名稱的檔案。

**選擇策略**:
- **`find_files_by_glob`**: 已知檔案模式（如 `**/*.controller.ts`）
- **`find_files_by_name_keyword`**: 已知檔名部分片段（如 `order`）—— 速度極快

**範例**:
```typescript
// ✅ Good: 使用 glob 尋找所有測試檔案
mcp__jetbrains__find_files_by_glob({
    globPattern: '**/__tests__/**/*.test.ts',
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// ✅ Good: 使用 keyword 快速尋找檔案
mcp__jetbrains__find_files_by_name_keyword({
    nameKeyword: 'order',
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// ❌ Bad: 使用 CLI find
Bash({ command: 'find . -name "*.test.ts"' });
```

**效能對比**:
- `find_files_by_name_keyword`: ~50ms（使用 IDE 索引）
- `find` CLI: ~500ms（掃描檔案系統）

---

#### ✅ 優先使用: `get_project_modules` / `get_project_dependencies`

**時機**: 釐清專案結構或檢查安裝了哪些外部套件。

**範例**:
```typescript
// ✅ Good: 檢查專案模組
mcp__jetbrains__get_project_modules({
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// ✅ Good: 檢查專案依賴
mcp__jetbrains__get_project_dependencies({
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// ❌ Bad: 手動讀取 package.json
Read('/Users/stevencheng/codebase/Steven-cheng-porfolio/frontend/package.json');
```

**使用情境**:
- 確認是否安裝特定套件（避免重複安裝）
- 檢查專案結構（monorepo workspaces）
- 驗證依賴版本

---

#### ⛔ 避免使用: `get_all_open_file_paths`

**原因**: 使用者正在閱讀的檔案與 AI 正在處理的檔案不一樣，容易造成誤解。

**例外情況**: 僅在使用者明確要求「查看目前開啟的檔案」時使用。

---

### 2. 檔案編輯與讀取 (File Operations)

這類指令處理具體的程式碼變動，應**優先使用 JetBrains MCP** 以確保操作準確性。

#### ✅ 優先使用: `get_file_text_by_path`

**取代**: `cat` / `head` / `tail` CLI 指令，以及 Claude Code 的 `Read` 工具

**時機**: 需要讀取檔案內容進行分析或修改前。

**優勢**:
- 自動處理二進位檔案（回傳錯誤而非亂碼）
- 支援截斷選項（START、MIDDLE、END、NONE）
- 確保檔案在專案範圍內

**範例**:
```typescript
// ✅ Good: 使用 JetBrains MCP
mcp__jetbrains__get_file_text_by_path({
    pathInProject: 'frontend/src/server/services/order.ts',
    maxLinesCount: 100,
    truncateMode: 'MIDDLE',
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// ⚠️ Acceptable: 使用 Claude Code Read 工具
Read('/Users/stevencheng/codebase/Steven-cheng-porfolio/frontend/src/server/services/order.ts');

// ❌ Bad: 使用 CLI
Bash({ command: 'cat frontend/src/server/services/order.ts' });
```

**何時使用 Read vs get_file_text_by_path**:
- **JetBrains MCP**: 在 develop skill 內，與其他 MCP 工具協同使用
- **Read**: 快速讀取單一檔案，無需 JetBrains 上下文

---

#### ✅ 優先使用: `create_new_file`

**取代**: `Write` 工具或 `echo >` / `cat <<EOF` CLI 指令

**時機**: 新增 Component、Service 或配置檔。

**優勢**:
- 自動建立不存在的父目錄
- 確保檔案路徑正確（相對於專案根目錄）
- 可選覆寫保護（overwrite 參數）

**範例**:
```typescript
// ✅ Good: 使用 JetBrains MCP
mcp__jetbrains__create_new_file({
    pathInProject: 'frontend/src/server/services/payment.ts',
    text: 'export function processPayment() { ... }',
    overwrite: false,  // 避免覆寫現有檔案
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// ⚠️ Acceptable: 使用 Claude Code Write
Write('/Users/stevencheng/codebase/Steven-cheng-porfolio/frontend/src/server/services/payment.ts', '...');

// ❌ Bad: 使用 CLI
Bash({ command: 'echo "export function..." > frontend/src/server/services/payment.ts' });
```

---

#### ✅ 文字修改: `replace_text_in_file` vs 程式重構: `rename_refactoring`

**關鍵區別**:

| 操作類型 | 工具 | 適用情境 |
|---------|------|---------|
| **純文字修改** | `replace_text_in_file` | Log 訊息、註解、JSDoc、字串常數 |
| **程式碼重構** | `rename_refactoring` | 變數名稱、函式名稱、類別名稱 |

**範例 1: 純文字修改（使用 replace_text_in_file）**:
```typescript
// ✅ Good: 修改 log 訊息
mcp__jetbrains__replace_text_in_file({
    pathInProject: 'frontend/src/server/services/order.ts',
    oldText: 'console.log("Order created")',
    newText: 'console.log("Order created successfully")',
    replaceAll: true,
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// ✅ Good: 更新 JSDoc
mcp__jetbrains__replace_text_in_file({
    pathInProject: 'frontend/src/server/services/order.ts',
    oldText: '@param data - Order data',
    newText: '@param data - Order data including eventId and tickets',
    replaceAll: false,  // 只替換第一個
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});
```

**範例 2: 程式碼重構（使用 rename_refactoring）**:
```typescript
// ✅ Good: 重命名函式（自動更新所有 references）
mcp__jetbrains__rename_refactoring({
    pathInProject: 'frontend/src/server/services/order.ts',
    symbolName: 'processOrder',
    newName: 'createOrder',
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// ✅ Good: 重命名變數（跨檔案）
mcp__jetbrains__rename_refactoring({
    pathInProject: 'frontend/src/server/services/order.ts',
    symbolName: 'orderData',
    newName: 'orderPayload',
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// ❌ Bad: 使用 replace_text_in_file 重命名函式
// 這會錯過其他檔案的 references，破壞程式碼
mcp__jetbrains__replace_text_in_file({
    pathInProject: 'frontend/src/server/services/order.ts',
    oldText: 'processOrder',
    newText: 'createOrder',
    replaceAll: true,  // ⚠️ 只在單一檔案內替換，遺漏其他檔案
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});
```

**決策流程圖**:
```
需要修改程式碼？
├─ 是否改變程式邏輯或名稱？
│  ├─ 是 → 使用 rename_refactoring（變數、函式、類別）
│  └─ 否 → 使用 replace_text_in_file（文字、註解、字串）
```

---

### 3. 程式碼品質與語義 (Code Analysis)

讓 AI 借用 JetBrains 的「靜態分析引擎」，而非依賴簡單的文字搜尋。

#### ✅ 優先使用: `get_symbol_info`

**時機**: 當 AI 看到不認識的物件（如某個 SDK 的內部型別），查閱其宣告、型別細節與文件。

**優勢**:
- 提供 Quick Documentation（與 IDE 中按 Cmd+J 相同）
- 顯示型別簽章（Type Signature）
- 包含 JSDoc/TSDoc 註解
- 精準定位 declaration

**範例**:
```typescript
// ✅ Good: 查詢 function 說明
mcp__jetbrains__get_symbol_info({
    filePath: 'frontend/src/server/services/order.ts',
    line: 42,
    column: 10,
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// 輸出: "function createOrder(data: OrderData): Promise<Order>"
// 包含完整的參數說明和回傳值型別
```

**使用情境**:
- 不熟悉的第三方 API（如 AWS SDK、Stripe SDK）
- 檢查 function 參數和回傳值
- 理解複雜型別定義

---

#### ✅ 優先使用: `search_in_files_by_text` / `search_in_files_by_regex`

**取代**: `grep` / `rg` CLI 指令，以及 Claude Code 的 `Grep` 工具

**時機**: 跨檔案尋找特定的邏輯實現或字串。

**優勢**:
- 利用 IDE 索引（速度快 10 倍以上）
- 自動過濾排除的檔案
- 支援檔案遮罩（fileMask）和目錄限制
- 結果包含上下文（用 `||` 標記匹配位置）

**範例**:
```typescript
// ✅ Good: 搜尋文字（精確匹配）
mcp__jetbrains__search_in_files_by_text({
    searchText: 'createOrder',
    caseSensitive: true,
    fileMask: '*.ts',  // 只搜尋 TypeScript 檔案
    directoryToSearch: 'frontend/src',
    maxUsageCount: 50,
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// ✅ Good: 搜尋 regex 模式
mcp__jetbrains__search_in_files_by_regex({
    regexPattern: 'function\\s+\\w+Order',  // 找所有 *Order 函式
    caseSensitive: false,
    fileMask: '*.ts',
    maxUsageCount: 100,
    projectPath: '/Users/stevencheng/codebase/Steven-cheng-porfolio'
});

// ⚠️ Acceptable: 使用 Claude Code Grep
Grep({
    pattern: 'createOrder',
    glob: '*.ts',
    output_mode: 'files_with_matches'
});

// ❌ Bad: 使用 CLI grep
Bash({ command: 'grep -r "createOrder" frontend/src' });
```

**輸出範例**:
```
frontend/src/server/services/order.ts:42
  export function ||createOrder||(data: OrderData): Promise<Order> {

frontend/src/server/api/events.ts:15
  const order = await ||createOrder||({ eventId, tickets, customer });
```

**效能對比**:
- `search_in_files_by_text`: ~100ms（使用 IDE 索引）
- `Grep` (ripgrep): ~300ms（檔案掃描）
- `grep` CLI: ~800ms（未優化）

---

### 決策矩陣: JetBrains MCP vs Claude Code Tools vs CLI

| 任務 | 優先順序 1 | 優先順序 2 | 避免使用 |
|------|-----------|-----------|---------|
| **列出目錄結構** | `list_directory_tree` | - | `tree` CLI |
| **尋找檔案（模式）** | `find_files_by_glob` | `Glob` | `find` CLI |
| **尋找檔案（名稱）** | `find_files_by_name_keyword` | - | `ls` / `find` CLI |
| **讀取檔案** | `get_file_text_by_path` | `Read` | `cat` CLI |
| **新增檔案** | `create_new_file` | `Write` | `echo >` CLI |
| **修改文字** | `replace_text_in_file` | `Edit` | `sed` CLI |
| **重命名符號** | `rename_refactoring` | - | `replace_text_in_file` |
| **搜尋程式碼** | `search_in_files_by_text` | `Grep` | `grep` CLI |
| **查詢符號資訊** | `get_symbol_info` | - | 手動查閱文件 |

**原則**:
1. **在 develop skill 內**: 優先使用 JetBrains MCP（整合度高）
2. **一般情境**: Claude Code 內建工具（Read、Edit、Glob、Grep）
3. **避免**: CLI 指令用於檔案操作（違反 Claude Code 最佳實踐）

---

## 核心工具詳解

### 1. get_file_problems(filePath, errorsOnly)

**用途**: 取得檔案的問題（errors 和 warnings）

**使用時機**:

- Refactor Phase - 檢查程式碼品質
- 修復 TypeScript 錯誤
- 識別潛在問題

**參數**:

- `filePath`: 檔案路徑（相對於專案根目錄）
- `errorsOnly`: 是否只顯示 errors（true = 只顯示 errors, false = 顯示 errors + warnings）

**範例**:

```typescript
const result = await mcp__jetbrains__get_file_problems(
    'frontend/src/server/services/order.ts',
    false  // 顯示 errors 和 warnings
);
```

**輸出範例**:

```json
{
  "problems": [
    {
      "severity": "ERROR",
      "message": "Type 'string | undefined' is not assignable to type 'string'",
      "line": 42,
      "column": 10,
      "file": "frontend/src/server/services/order.ts"
    },
    {
      "severity": "WARNING",
      "message": "Variable 'mockData' is declared but never used",
      "line": 15,
      "column": 7,
      "file": "frontend/src/server/services/order.ts"
    }
  ]
}
```

---

### 2. reformat_file(path)

**用途**: 格式化檔案（縮排、空格、換行、import 順序等）

**使用時機**:

- Refactor Phase - 格式化所有修改的檔案
- Commit 前確保格式一致

**參數**:

- `path`: 檔案路徑（相對於專案根目錄）

**範例**:

```typescript
await mcp__jetbrains__reformat_file(
    'frontend/src/server/services/order.ts'
);
```

**格式化內容**:

- Indentation（縮排）
- Whitespace（空格）
- Line breaks（換行）
- Import statements（Import 順序）
- Code style（程式碼風格）

**注意**: 格式化後可能產生新的 git diff，這是正常的。

---

### 3. rename_refactoring(pathInProject, symbolName, newName)

**用途**: 重命名變數/函數/類別，自動更新所有 references

**使用時機**:

- Refactor Phase - 改善命名
- 提升程式碼可讀性

**參數**:

- `pathInProject`: 檔案路徑（相對於專案根目錄）
- `symbolName`: 舊名稱
- `newName`: 新名稱

**範例**:

```typescript
await mcp__jetbrains__rename_refactoring(
    'frontend/src/server/services/order.ts',
    'processOrder',  // 舊名稱
    'createOrder'    // 新名稱
);
```

**好處**:

- 自動更新所有 references（跨檔案）
- 保持一致性
- 避免手動 find/replace 遺漏
- 安全重構（不會破壞程式碼）

---

### 4. get_symbol_info(filePath, line, column)

**用途**: 取得 function/變數的說明文件（Quick Documentation）

**使用時機**:

- 確認 function 參數
- 檢查 function 回傳值
- 理解 API 使用方式

**參數**:

- `filePath`: 檔案路徑（相對於專案根目錄）
- `line`: 行號（1-based）
- `column`: 列號（1-based）

**範例**:

```typescript
const result = await mcp__jetbrains__get_symbol_info(
    'frontend/src/server/services/order.ts',
    42,
    10
);
```

**輸出範例**:

```json
{
  "documentation": "Creates a new order with the given data.\n\n@param data - Order data including eventId, tickets, and customer\n@returns Promise<Order> - Created order with orderId and status",
  "signature": "function createOrder(data: OrderData): Promise<Order>",
  "type": "function"
}
```

---

### 5. get_run_configurations()

**用途**: 取得專案的 run configurations

**使用時機**:

- 啟動 Wallaby
- 執行其他 run configurations

**範例**:

```typescript
const result = await mcp__jetbrains__get_run_configurations();
```

**輸出範例**:

```json
{
  "configurations": [
    {
      "name": "wallaby",
      "type": "node",
      "command": "node wallaby.js"
    },
    {
      "name": "dev",
      "type": "npm",
      "command": "npm run dev"
    }
  ]
}
```

---

### 6. execute_run_configuration(configurationName)

**用途**: 執行指定的 run configuration

**使用時機**:

- 啟動 Wallaby
- 執行開發伺服器
- 執行自訂 scripts

**參數**:

- `configurationName`: Configuration 名稱

**範例**:

```typescript
await mcp__jetbrains__execute_run_configuration('wallaby');
```

**輸出**:

```
Wallaby started successfully
```

---

## 常見使用流程

### 流程 1: 重構迴圈（完整）

```typescript
// 1. 取得異動檔案
const modifiedFiles = execSync('git status --short')
    .toString()
    .split('\n')
    .filter(line => line.trim())
    .map(line => line.substring(3));  // 去除 git status 前綴

// 2. 處理新增檔案
for (const file of modifiedFiles) {
    if (file.startsWith('??')) {
        execSync(`git add ${file.substring(3)}`);
    }
}

// 3. 檢查問題
for (const file of modifiedFiles) {
    const problems = await mcp__jetbrains__get_file_problems(file, false);

    if (problems.problems.length > 0) {
        console.log(`${file} 有 ${problems.problems.length} 個問題`);
        // 修復問題...
    }
}

// 4. 格式化
for (const file of modifiedFiles) {
    await mcp__jetbrains__reformat_file(file);
}

// 5. ESLint
execSync('npm run lint -w frontend');

// 6. 驗證測試
const allTests = await mcp__wallaby__wallaby_allTests();
const passingCount = allTests.tests.filter(t => t.status === 'passing').length;

if (passingCount === allTests.tests.length) {
    console.log('✅ 重構完成');
} else {
    console.log('❌ 測試失敗，回到步驟 1');
}
```

---

### 流程 2: 重命名重構

```typescript
// 1. 決定要重命名的 symbol
const oldName = 'processOrder';
const newName = 'createOrder';

// 2. 執行 rename refactoring
await mcp__jetbrains__rename_refactoring(
    'frontend/src/server/services/order.ts',
    oldName,
    newName
);

// 3. 驗證測試仍通過
const allTests = await mcp__wallaby__wallaby_allTests();
```

---

### 流程 3: 檢查並修復檔案問題

```typescript
// 1. 檢查檔案問題
const problems = await mcp__jetbrains__get_file_problems(
    'frontend/src/server/services/order.ts',
    false
);

// 2. 分類問題
const errors = problems.problems.filter(p => p.severity === 'ERROR');
const warnings = problems.problems.filter(p => p.severity === 'WARNING');

console.log(`Errors: ${errors.length}, Warnings: ${warnings.length}`);

// 3. 逐一修復
for (const error of errors) {
    console.log(`Line ${error.line}: ${error.message}`);
    // 根據錯誤訊息修復...
}

// 4. 重新檢查
const updatedProblems = await mcp__jetbrains__get_file_problems(
    'frontend/src/server/services/order.ts',
    false
);

if (updatedProblems.problems.length === 0) {
    console.log('✅ 所有問題已修復');
}
```

---

### 流程 4: 啟動 Wallaby

```typescript
// 1. 取得 run configurations
const configs = await mcp__jetbrains__get_run_configurations();

// 2. 尋找 wallaby configuration
const wallabyConfig = configs.configurations.find(c => c.name === 'wallaby');

if (!wallabyConfig) {
    console.error('找不到 wallaby configuration');
    return;
}

// 3. 執行 Wallaby
await mcp__jetbrains__execute_run_configuration('wallaby');

// 4. 等待啟動
await new Promise(resolve => setTimeout(resolve, 10000));

// 5. 驗證運作
const allTests = await mcp__wallaby__wallaby_allTests();
console.log(`Wallaby 已啟動，共 ${allTests.tests.length} 個測試`);
```

---

## 最佳實踐

### 1. 先檢查問題，再格式化

```typescript
// ✅ Good: 先修復問題，再格式化
const problems = await mcp__jetbrains__get_file_problems(file, false);
// 修復問題...
await mcp__jetbrains__reformat_file(file);
```

```typescript
// ❌ Bad: 先格式化，可能掩蓋問題
await mcp__jetbrains__reformat_file(file);
const problems = await mcp__jetbrains__get_file_problems(file, false);
```

### 2. 使用 rename_refactoring 而非 find/replace

```typescript
// ✅ Good: 使用 IDE 重構
await mcp__jetbrains__rename_refactoring(
    'frontend/src/server/services/order.ts',
    'oldName',
    'newName'
);

// ❌ Bad: 手動 find/replace（容易遺漏）
// 手動在所有檔案中搜尋並替換...
```

### 3. 定期檢查程式碼品質

```typescript
// 在 Refactor Phase 反覆執行
const problems = await mcp__jetbrains__get_file_problems(file, false);

while (problems.problems.length > 0) {
    // 修復問題
    // 重新檢查
    problems = await mcp__jetbrains__get_file_problems(file, false);
}
```

---

## 常見問題類型與修復

### Type Errors

**問題**:

```
Type 'string | undefined' is not assignable to type 'string'
```

**修復**:

```typescript
// ❌ Before
function getEmail(customer: Customer | undefined): string {
    return customer.email;  // Error
}

// ✅ After (使用 Optional Chaining)
function getEmail(customer: Customer | undefined): string | undefined {
    return customer?.email;
}
```

---

### Unused Variables

**問題**:

```
'mockData' is declared but never used
```

**修復**:

```typescript
// ❌ Before
const mockData = {...};  // 未使用

// ✅ After (移除)
// 直接刪除未使用的變數
```

---

### Missing Return Type

**問題**:

```
Function lacks return type annotation
```

**修復**:

```text
// ❌ Before
function calculateTotal(tickets) {
    return tickets.reduce(...);
}

// ✅ After
function calculateTotal(tickets: Ticket[]): number {
    return tickets.reduce(...);
}
```

---

## 故障排除

### Q: get_file_problems() 回傳空陣列但仍有錯誤

**原因**: IDE 尚未完成檔案分析

**解決**:

1. 等待 5 秒
2. 重新執行 `get_file_problems()`
3. 確保 IDE 已開啟專案

### Q: reformat_file() 沒有效果

**原因**: IDE 格式化設定問題

**解決**:

1. 檢查 IDE 格式化設定
2. 確保檔案類型正確（.ts, .tsx）
3. 手動在 IDE 中測試格式化功能

### Q: rename_refactoring() 失敗

**原因**: Symbol 不存在或有多個同名 symbol

**解決**:

1. 確認 symbol 名稱正確
2. 確認 symbol 在指定檔案中存在
3. 如果有多個同名，手動重構
