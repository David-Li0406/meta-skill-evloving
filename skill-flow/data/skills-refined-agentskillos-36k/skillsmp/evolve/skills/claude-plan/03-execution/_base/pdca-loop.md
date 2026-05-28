# PDCA 執行循環

## 概述

每個任務使用 PDCA (Plan-Do-Check-Act) 循環執行，確保品質和可追蹤性。

## 執行流程

```
┌─────────────────────────────────────────────────────────┐
│                    PDCA 循環                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│     ┌─────────┐         ┌─────────┐                    │
│     │  Plan   │────────→│   Do    │                    │
│     │ 規劃    │         │  執行   │                    │
│     └─────────┘         └────┬────┘                    │
│          ↑                   │                          │
│          │                   ↓                          │
│     ┌────┴────┐         ┌─────────┐                    │
│     │   Act   │←────────│  Check  │                    │
│     │  調整   │         │  驗證   │                    │
│     └─────────┘         └─────────┘                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## Phase 詳解

### Plan（規劃）

```yaml
plan_phase:
  actions:
    - 讀取任務描述和驗收標準
    - 分析技術需求
    - 設計實作方案
    - 識別風險點

  outputs:
    - implementation_approach.md
    - risk_assessment
```

### Do（執行）

```yaml
do_phase:
  actions:
    - 實作程式碼
    - 撰寫測試
    - 更新文檔

  constraints:
    - 每個變更 < 500 行
    - 遵循專案慣例
    - 保持原子性 commit
```

### Check（驗證）

```yaml
check_phase:
  validations:
    # 必須通過
    - name: "編譯通過"
      command: "npm run build"
      required: true

    - name: "測試通過"
      command: "npm test"
      required: true

    - name: "Lint 通過"
      command: "npm run lint"
      required: true

    # 選擇性
    - name: "覆蓋率檢查"
      command: "npm run coverage"
      threshold: 80

  on_failure:
    - 記錄失敗原因
    - 觸發 Act 調整
```

### Act（調整）

```yaml
act_phase:
  on_success:
    - 自動 commit
    - 更新任務狀態
    - 通知下游任務解除阻塞
    - 記錄 implementation log

  on_failure:
    strategies:
      - name: "重試"
        condition: "偶發錯誤"
        max_attempts: 3

      - name: "回滾 + 重新規劃"
        condition: "方案不可行"
        action: "回到 Plan phase"

      - name: "請求協助"
        condition: "連續失敗 3 次"
        action: "暫停 + 通知用戶"
```

## 驗證策略

### 驗證層級

```
Level 1: 基礎驗證（必須）
├── 編譯成功
├── 無 lint 錯誤
└── 單元測試通過

Level 2: 整合驗證（建議）
├── 整合測試通過
├── API 契約驗證
└── 效能基準

Level 3: 端到端驗證（選擇性）
├── E2E 測試
├── 手動驗證
└── 用戶驗收
```

### 自動 vs 手動

```yaml
verification_matrix:
  always_auto:
    - compile
    - lint
    - unit_test

  auto_if_available:
    - integration_test
    - e2e_test

  manual_required:
    - ui_review
    - security_audit
    - production_deploy
```

## 整合 Subagents

### verify-app

```yaml
verify-app:
  trigger: "Do phase 完成"
  commands:
    - "npm test"
    - "npm run build"
    - "npm start & sleep 3 && curl -f http://localhost:3000/health"
  success_criteria: "所有命令回傳 0"
  fail_action: "阻止進入下一步"
```

### build-validator

```yaml
build-validator:
  trigger: "程式碼變更"
  commands:
    - "npm run build"
    - "npm run lint"
    - "npm run typecheck"
  success_criteria: "所有命令回傳 0，無警告"
  fail_action: "阻止 commit"
```

## 失敗處理

### 失敗分類

| 類型 | 描述 | 處理 |
|------|------|------|
| 暫時性 | 網路問題、資源不足 | 重試 |
| 邏輯錯誤 | 實作 bug | 修復 + 重跑 |
| 設計問題 | 方案不可行 | 回到 Plan |
| 需求問題 | 需求不清楚 | 暫停 + 詢問 |

### 自動診斷

```python
def diagnose_failure(error):
    patterns = {
        "compilation error": "CHECK_SYNTAX",
        "test failed": "CHECK_LOGIC",
        "timeout": "CHECK_PERFORMANCE",
        "connection refused": "CHECK_DEPENDENCIES",
    }

    for pattern, diagnosis in patterns.items():
        if pattern in error.lower():
            return diagnosis

    return "NEED_HUMAN"
```

## commit 策略

### 自動 Commit

```yaml
auto_commit:
  trigger: "Check phase 全部通過"
  format: |
    {type}: {task_summary}

    Task: {task_id}
    Session: {session_id}

    Changes:
    {file_changes}

    Co-Authored-By: Claude <noreply@anthropic.com>

  types:
    - feat: 新功能
    - fix: 修復
    - refactor: 重構
    - test: 測試
    - docs: 文檔
```

### Commit 頻率

```
每個子任務完成 → 1 commit
每個主任務完成 → 1 merge commit（如果有多個子 commit）
```
