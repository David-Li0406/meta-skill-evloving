# Phase 2: 啟動 Wallaby - 即時測試監控

## 目標

啟動 Wallaby MCP 即時測試監控，為 TDD 流程提供即時回饋。

## 什麼是 Wallaby？

Wallaby.js 是一個智能測試執行工具，提供：

- **即時測試執行**: 檔案變更時自動執行相關測試
- **Runtime Values**: 顯示變數在測試執行時的實際值
- **程式碼覆蓋率**: 視覺化顯示哪些程式碼已被測試覆蓋
- **效能優化**: 只執行受影響的測試，節省時間

## 執行步驟

### Step 1: 取得 Wallaby Run Configuration

```typescript
mcp__jetbrains__get_run_configurations()
```

**預期輸出**:

```json
{
  "configurations": [
    {
      "name": "wallaby",
      "type": "node",
      "command": "node wallaby.js"
    }
  ]
}
```

如果找不到 `wallaby` configuration，檢查：

1. 專案根目錄是否有 `wallaby.js` 配置檔
2. JetBrains IDE 是否已安裝 Wallaby 插件

---

### Step 2: 執行 Wallaby

```typescript
mcp__jetbrains__execute_run_configuration('wallaby')
```

**預期輸出**:

```
Wallaby started successfully
Watching files for changes...
```

**等待時間**: Wallaby 需要 5-10 秒啟動並執行初始測試掃描

---

### Step 3: 驗證 Wallaby 正常運作

```typescript
mcp__wallaby__wallaby_allTests()
```

**預期輸出**:

```json
{
  "tests": [
    {
      "id": "test-1",
      "name": "should render homepage",
      "status": "passing",
      "file": "frontend/src/app/page.test.tsx",
      "line": 5
    }
  ],
  "coverage": {
    "statements": 85.5,
    "branches": 78.2,
    "functions": 90.1,
    "lines": 84.8
  }
}
```

**檢查項目**:

- [ ] `tests` 陣列包含至少 1 個測試
- [ ] 測試有 `status` 欄位（passing/failing/pending）
- [ ] 測試有 `file` 和 `line` 資訊
- [ ] `coverage` 資訊存在

---

## Wallaby 狀態檢查

### 正常運作的指標 ✅

- `wallaby_allTests()` 返回測試列表
- 測試有正確的 `status`
- 檔案變更後測試自動執行

### 異常狀態處理 ❌

#### 問題 1: `wallaby_allTests()` 返回空陣列

**原因**: Wallaby 尚未完全啟動

**解決**:

```bash
# 等待 10 秒
sleep 10

# 重新檢查
mcp__wallaby__wallaby_allTests()
```

---

#### 問題 2: 無法執行 run configuration

**錯誤訊息**: `Configuration 'wallaby' not found`

**解決**:

1. 檢查專案根目錄是否有 `wallaby.js`
2. 如果沒有，建立 `wallaby.js` 配置檔：
   ```javascript
   module.exports = function (wallaby) {
     return {
       files: [
         'frontend/src/**/*.ts',
         'frontend/src/**/*.tsx',
         '!frontend/src/**/*.test.ts',
         '!frontend/src/**/*.test.tsx'
       ],
       tests: [
         'frontend/src/**/*.test.ts',
         'frontend/src/**/*.test.tsx'
       ],
       env: {
         type: 'node',
         runner: 'node'
       },
       testFramework: 'vitest'
     };
   };
   ```
3. 重新執行 `get_run_configurations()`

---

#### 問題 3: JetBrains IDE 未開啟

**錯誤訊息**: `Cannot connect to IDE`

**解決**:

1. 開啟 JetBrains IDE (WebStorm/IntelliJ IDEA)
2. 確保專案已在 IDE 中開啟
3. 重新執行 `execute_run_configuration('wallaby')`

---

## Wallaby 啟動完成檢查清單

- [ ] `get_run_configurations()` 找到 `wallaby` configuration
- [ ] `execute_run_configuration('wallaby')` 執行成功
- [ ] `wallaby_allTests()` 返回測試列表（非空陣列）
- [ ] 測試有正確的 `status`（passing/failing/pending）
- [ ] 測試有 `file` 和 `line` 資訊
- [ ] Coverage 資訊存在

---

## 下一步

Wallaby 成功啟動後，進入 **Step 4: Red Phase** - 開始寫第一個失敗的測試

詳見 [4-red.md](4-red.md)

---

## Wallaby MCP 工具快速參考

- `wallaby_allTests()` - 取得所有測試狀況
- `wallaby_failingTests()` - 取得失敗的測試
- `wallaby_runtimeValues(file, line, lineContent, expression)` - 查看變數值
- `wallaby_coveredLinesForFile(file)` - 查看程式碼覆蓋率

完整參考請見 [../mcp-tools/wallaby-reference.md](../mcp-tools/wallaby-reference.md)
