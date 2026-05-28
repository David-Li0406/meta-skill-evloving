# Release Criteria

> verify skill 的發布許可標準

## 發布決策矩陣

### ✅ SHIP IT

所有必須條件都達標時，發布許可通過。

```yaml
ship_it:
  required:
    functional_tests: 100%
    regression_tests: 100%
    acceptance_tests: 100%
  recommended:
    edge_case_tests: 90%
    pass_at_k: true
```

### ❌ BLOCKED

任一必須條件未達標時，發布被阻擋。

```yaml
blocked:
  triggers:
    - functional_tests < 100%
    - regression_tests < 100%
    - acceptance_tests < 100%
    - critical_bug_found: true
```

## 詳細標準

### 功能測試 (Functional Tests)

| 等級 | 通過率 | 決策 |
|------|--------|------|
| ✅ 通過 | 100% | SHIP IT |
| ❌ 失敗 | < 100% | BLOCKED |

**說明**：核心功能必須 100% 通過。

### 邊界測試 (Edge Case Tests)

| 等級 | 通過率 | 決策 |
|------|--------|------|
| ✅ 優秀 | ≥ 95% | SHIP IT |
| ⚠️ 及格 | ≥ 90% | SHIP IT（建議修復） |
| ❌ 失敗 | < 90% | BLOCKED |

**說明**：允許少量邊界案例失敗，但需記錄。

### 回歸測試 (Regression Tests)

| 等級 | 通過率 | 決策 |
|------|--------|------|
| ✅ 通過 | 100% | SHIP IT |
| ❌ 失敗 | < 100% | BLOCKED |

**說明**：不允許任何回歸。

### 驗收測試 (Acceptance Tests)

| 等級 | 通過率 | 決策 |
|------|--------|------|
| ✅ 通過 | 100% | SHIP IT |
| ❌ 失敗 | < 100% | BLOCKED |

**說明**：驗收標準必須 100% 達成。

## pass@k 標準

### 計算公式

```
pass@k = 1 - C(n-c, k) / C(n, k)

n = 總嘗試次數
c = 成功次數
k = 目標嘗試次數
```

### 預設配置

```yaml
pass_at_k:
  k: 3                      # 最多 3 次嘗試
  threshold: 0.9            # 90% 成功率
  critical_paths:
    require_consecutive: true  # 關鍵路徑需連續成功
    min_consecutive: 2         # 至少連續 2 次
```

### 關鍵路徑

以下測試路徑需連續成功：

- 使用者登入流程
- 資料寫入流程
- 支付流程（如適用）
- 核心業務流程

## 不穩定測試處理

### 識別不穩定測試

```yaml
flaky_detection:
  threshold: 3               # 連續 3 次不一致即標記
  actions:
    - mark_as_flaky
    - separate_report
    - suggest_investigation
```

### 不穩定測試不阻擋發布

```yaml
flaky_tests:
  blocking: false            # 不阻擋發布
  require_investigation: true  # 但需調查
  max_allowed: 5             # 最多允許 5 個
```

## 發布類型

### 1. 正式發布 (Production)

```yaml
production:
  criteria:
    functional_tests: 100%
    edge_case_tests: 95%
    regression_tests: 100%
    acceptance_tests: 100%
  pass_at_k:
    k: 3
    threshold: 0.95
  approval: required
```

### 2. 預發布 (Staging)

```yaml
staging:
  criteria:
    functional_tests: 100%
    edge_case_tests: 90%
    regression_tests: 100%
    acceptance_tests: 100%
  pass_at_k:
    k: 3
    threshold: 0.9
  approval: optional
```

### 3. 開發發布 (Development)

```yaml
development:
  criteria:
    functional_tests: 95%
    edge_case_tests: 80%
    regression_tests: 95%
    acceptance_tests: 90%
  pass_at_k:
    k: 2
    threshold: 0.8
  approval: not_required
```

## 豁免規則

### 緊急修復 (Hotfix)

```yaml
hotfix:
  allowed_skip:
    - edge_case_tests
    - some_acceptance_tests
  required:
    - regression_tests: 100%
    - critical_path_tests: 100%
  approval: required_by_lead
```

### 功能開關 (Feature Flag)

```yaml
feature_flag:
  if_enabled: false
  allowed_skip:
    - acceptance_tests
  note: "功能未啟用，可跳過驗收"
```

## 報告格式

### 發布許可報告

```markdown
# 發布許可報告

## 決策：✅ SHIP IT / ❌ BLOCKED

## 測試摘要

| 類型 | 通過率 | 閾值 | 狀態 |
|------|--------|------|------|
| 功能測試 | 100% | 100% | ✅ |
| 邊界測試 | 94% | 90% | ✅ |
| 回歸測試 | 100% | 100% | ✅ |
| 驗收測試 | 100% | 100% | ✅ |

## pass@3 結果

| 路徑 | 成功率 | 連續成功 | 狀態 |
|------|--------|----------|------|
| 登入流程 | 100% | 3 | ✅ |
| 資料流程 | 100% | 3 | ✅ |

## 不穩定測試

- test_xxx (需調查)

## 簽核

- 日期：{date}
- 驗證者：multi-agent-verify
```

## 共用模組參考

- 交叉驗證：[shared/synthesis/cross-validation.md](../../../shared/synthesis/cross-validation.md)
- Checkpoint 整合：[shared/integration/evolve-checkpoints.md](../../../shared/integration/evolve-checkpoints.md)
