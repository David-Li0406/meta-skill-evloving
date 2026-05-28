# Feedback Loop

> 即時回饋循環配置

## 回饋循環概述

```
┌─────────────────────────────────────────────────────────────┐
│                    回饋循環架構                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  主 Agent                    4 視角                         │
│  ┌──────┐                   ┌──────────────────────┐        │
│  │ 寫   │ ──── 程式碼 ────► │ TDD  Perf  Sec  Mnt │        │
│  │ 程   │                   │  ↓    ↓    ↓    ↓   │        │
│  │ 式   │ ◄─── 回饋 ─────── │ [回饋收集與整合]    │        │
│  │ 碼   │                   └──────────────────────┘        │
│  └──────┘                                                    │
│     ↓                                                        │
│  [根據回饋修正]                                              │
│     ↓                                                        │
│  繼續下一段                                                  │
└─────────────────────────────────────────────────────────────┘
```

## 回饋觸發條件

### 自動觸發

```yaml
auto_triggers:
  # 函數完成
  function_complete:
    condition: "function definition closed"
    trigger: true

  # 類別完成
  class_complete:
    condition: "class definition closed"
    trigger: true

  # 模組完成
  module_complete:
    condition: "file saved with new exports"
    trigger: true

  # 測試添加
  test_added:
    condition: "test file modified"
    trigger: true
```

### 手動觸發

```yaml
manual_triggers:
  # 主 Agent 請求審查
  request_review:
    command: "請求視角審查"
    trigger: immediate

  # 強制同步
  force_sync:
    command: "強制同步所有視角"
    trigger: immediate
```

## 回饋處理流程

### Step 1: 收集

```yaml
collection:
  method: parallel          # 並行收集
  timeout: 30s              # 超時設定
  retry: 1                  # 重試次數
  on_timeout: proceed       # 超時後繼續
```

### Step 2: 標準化

```yaml
normalization:
  format:
    status: "✅ | ⚠️ | ❌"
    category: "string"
    message: "string"
    suggestion: "string (optional)"
    location: "file:line (optional)"

  example:
    status: "❌"
    category: "security"
    message: "用戶輸入未經驗證"
    suggestion: "使用 sanitize(input) 處理"
    location: "src/auth.ts:45"
```

### Step 3: 優先排序

```yaml
priority_order:
  1: security_block      # 安全阻擋
  2: tdd_block          # 測試阻擋
  3: performance_block  # 效能阻擋
  4: maintainability_block  # 維護性阻擋
  5: security_warning   # 安全警告
  6: tdd_warning        # 測試警告
  7: performance_warning  # 效能警告
  8: maintainability_warning  # 維護性警告
  9: suggestions        # 建議
```

### Step 4: 去重

```yaml
deduplication:
  strategy: semantic      # 語義去重
  similarity_threshold: 0.8
  keep: highest_priority  # 保留最高優先級
```

### Step 5: 呈現

```yaml
presentation:
  format: grouped         # 按類型分組
  max_items_per_group: 5  # 每組最多 5 項
  show_location: true     # 顯示位置
  show_suggestion: true   # 顯示建議
```

## 回饋響應規則

### 阻擋處理

```yaml
block_response:
  action: must_fix
  workflow:
    1: pause_implementation
    2: display_block_reason
    3: wait_for_fix
    4: re_trigger_review
    5: if_pass_continue
```

### 警告處理

```yaml
warning_response:
  action: log_and_continue
  workflow:
    1: log_warning
    2: add_to_report
    3: continue_implementation
    4: remind_at_sync_point
```

### 建議處理

```yaml
suggestion_response:
  action: optional
  workflow:
    1: display_suggestion
    2: user_decides
    3: if_accepted_apply
    4: continue
```

## 回饋模板

### 單一視角回饋

```markdown
## {視角名稱} 回饋

### 審查範圍
- 檔案：{file_path}
- 函數：{function_name}
- 行數：{line_range}

### 結果

| 檢查項 | 狀態 | 說明 |
|--------|------|------|
| {check_1} | {status} | {description} |
| {check_2} | {status} | {description} |

### 詳細發現

{if_has_blocks}
#### ❌ 阻擋項
- {block_description}
  - 原因：{reason}
  - 修正：{fix_suggestion}
{endif}

{if_has_warnings}
#### ⚠️ 警告項
- {warning_description}
{endif}

{if_has_suggestions}
#### 💡 建議
- {suggestion}
{endif}
```

### 整合回饋

```markdown
## 綜合回饋報告

### 審查摘要

| 視角 | 通過 | 警告 | 阻擋 |
|------|------|------|------|
| TDD | {n} | {n} | {n} |
| Performance | {n} | {n} | {n} |
| Security | {n} | {n} | {n} |
| Maintainer | {n} | {n} | {n} |

### 必須修正（阻擋項）

{if_has_blocks}
1. **[{perspective}]** {description}
   - 位置：{location}
   - 修正建議：{suggestion}
{else}
無阻擋項 ✅
{endif}

### 建議修正（警告項）

{if_has_warnings}
1. **[{perspective}]** {description}
{else}
無警告項 ✅
{endif}

### 下一步

{if_blocked}
請修正上述阻擋項後，系統將自動重新審查。
{else}
所有檢查通過，可繼續下一個任務。
{endif}
```

## 回饋統計

### 實時統計

```yaml
realtime_stats:
  track:
    - total_reviews        # 總審查次數
    - blocks_found         # 阻擋數量
    - blocks_fixed         # 已修正阻擋
    - warnings_found       # 警告數量
    - average_review_time  # 平均審查時間
```

### 會話統計

```yaml
session_stats:
  at_end:
    - pass_rate            # 通過率
    - block_fix_rate       # 阻擋修正率
    - most_common_issues   # 最常見問題
    - perspective_scores   # 視角評分
```

## 配置選項

### 全域配置

```yaml
global:
  feedback_enabled: true
  auto_trigger: true
  parallel_review: true
  show_suggestions: true
  log_all_feedback: true
```

### 視角特定配置

```yaml
perspectives:
  tdd-enforcer:
    priority: high
    block_threshold: strict

  performance-optimizer:
    priority: medium
    block_threshold: normal

  security-auditor:
    priority: critical
    block_threshold: strict

  maintainer:
    priority: low
    block_threshold: relaxed
```

## 相關資源

- [監督模式說明](./supervision-mode.md)
- [pass@k 重試機制](./pass-at-k-retry.md)
- [預設視角配置](../01-perspectives/_base/default-perspectives.md)
