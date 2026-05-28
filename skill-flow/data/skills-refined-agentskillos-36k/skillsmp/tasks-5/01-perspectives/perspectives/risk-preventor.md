# risk-preventor 視角

> 風險預防師：將風險轉化為預防性任務

## 視角定義

```yaml
id: risk-preventor
name: 風險預防師
role: 將識別的風險轉化為可執行的預防、回退、監控任務
method: 風險分析 + 預防設計

focus:
  - 風險預防措施
  - 回退計劃
  - 監控設置
  - 告警配置

output:
  tasks:
    prefix: "RISK-"
    types:
      - prevention
      - rollback
      - monitoring
```

## 執行順序

**Phase 2: 並行執行**

在 dependency-analyst 完成後，與 task-decomposer、test-planner 並行執行。

## 輸入

```yaml
from_dependency_analyst:
  - dependency-graph.md  # 元件清單和依賴關係

from_plan:
  - implementation-plan.md  # 技術方案
  - risk-mitigation.md      # 風險緩解策略（主要輸入）
```

## 風險分析

### 風險來源

```yaml
risk_sources:
  from_plan:
    - "明確識別的風險"
    - "風險緩解策略"

  implicit:
    - "外部依賴（API、服務）"
    - "效能敏感區域"
    - "安全敏感區域"
    - "資料一致性要求"
```

### 風險等級

| 等級 | 說明 | 任務優先級 |
|------|------|-----------|
| 高 | 可能導致系統故障 | P0 |
| 中 | 可能影響功能 | P1 |
| 低 | 可能影響體驗 | P2 |

## 任務類型

### 預防任務 (prevention)

**目的**：在問題發生前預防

```yaml
- id: RISK-001
  type: prevention
  milestone: M1
  name: "設定認證服務監控"
  related_risk: "R-002 認證效能問題"

  trigger: "部署後"

  steps:
    - "設定登入延遲告警 (> 2s)"
    - "設定失敗率告警 (> 5%)"
    - "建立 dashboard"

  priority: P1

  dependencies:
    blocked_by: [T-F-002]
    blocks: []

  acceptance_criteria:
    - "監控 dashboard 已建立"
    - "告警規則已配置"

  status: pending
```

### 回退任務 (rollback)

**目的**：問題發生時快速恢復

```yaml
- id: RISK-002
  type: rollback
  milestone: M2
  name: "認證系統回退計劃"
  related_risk: "R-001 認證系統故障"

  trigger: "登入失敗率 > 10%"

  steps:
    - "切換到舊版認證端點"
    - "通知維運團隊"
    - "保留日誌供分析"

  rollback_script: |
    # 切換到舊版
    kubectl set image deployment/auth auth=auth:v1.0
    # 通知
    slack-notify "認證系統已回退"

  priority: P0

  dependencies:
    blocked_by: [T-F-003]
    blocks: []

  acceptance_criteria:
    - "回退腳本已測試"
    - "回退可在 5 分鐘內完成"

  status: pending
```

### 監控任務 (monitoring)

**目的**：持續監控系統健康

```yaml
- id: RISK-003
  type: monitoring
  milestone: M3
  name: "設置效能基準監控"
  related_risk: "R-002 效能退化"

  metrics:
    - name: "登入延遲"
      threshold: "< 500ms"
      alert_on: "> 2s"
    - name: "Token 驗證延遲"
      threshold: "< 50ms"
      alert_on: "> 200ms"
    - name: "並發連接數"
      threshold: "< 1000"
      alert_on: "> 800"

  priority: P1

  dependencies:
    blocked_by: [T-F-001, T-F-002]
    blocks: []

  acceptance_criteria:
    - "Grafana dashboard 已建立"
    - "告警通道已配置"
    - "基準線已記錄"

  status: pending
```

## 規劃步驟

### Step 1: 識別風險

從 risk-mitigation.md 識別：

- 明確列出的風險
- 緩解策略

從 implementation-plan.md 推斷：

- 外部依賴風險
- 效能風險
- 安全風險

### Step 2: 分類風險任務

```yaml
for_each_risk:
  high_severity:
    - create_rollback_task
    - create_monitoring_task

  medium_severity:
    - create_prevention_task
    - create_monitoring_task

  low_severity:
    - create_monitoring_task
```

### Step 3: 設計觸發條件

```yaml
trigger_design:
  specific: "登入失敗率 > 10%"  # 好
  vague: "系統異常時"            # 差
```

### Step 4: 定義執行步驟

每個任務必須有明確的執行步驟：

```yaml
steps:
  - "具體動作 1"
  - "具體動作 2"
  - "驗證動作完成"
```

## 品質檢查

### 必須通過

- [ ] 所有任務 ID 格式正確（RISK-NNN）
- [ ] 所有高風險都有回退任務
- [ ] 所有任務有明確的觸發條件
- [ ] 所有任務有可執行的步驟

### 建議通過

- [ ] 監控指標有具體閾值
- [ ] 回退腳本可自動執行
- [ ] 告警通道已定義
