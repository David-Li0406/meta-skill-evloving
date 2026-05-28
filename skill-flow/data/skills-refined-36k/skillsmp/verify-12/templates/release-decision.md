# 發布決策：{feature}

> 由 multi-verify skill 自動生成

## 決策

{decision_badge}

---

## 概覽

| 項目 | 值 |
|------|-----|
| 功能名稱 | {feature} |
| 驗證日期 | {date} |
| 視角數量 | {perspective_count} |
| 測試案例數 | {total_tests} |
| 整體通過率 | {overall_pass_rate}% |

---

## 測試結果摘要

### 通過率

| 類型 | 通過 | 總數 | 通過率 | 閾值 | 狀態 |
|------|------|------|--------|------|------|
| 功能測試 | {func_pass} | {func_total} | {func_rate}% | 100% | {func_status} |
| 邊界測試 | {edge_pass} | {edge_total} | {edge_rate}% | 90% | {edge_status} |
| 回歸測試 | {reg_pass} | {reg_total} | {reg_rate}% | 100% | {reg_status} |
| 驗收測試 | {acc_pass} | {acc_total} | {acc_rate}% | 100% | {acc_status} |

### pass@{k} 結果

| 關鍵路徑 | 嘗試次數 | 成功次數 | pass@{k} | 連續成功 | 狀態 |
|----------|----------|----------|----------|----------|------|
| {path_1} | {tries_1} | {success_1} | {pass_k_1}% | {consecutive_1} | {path_status_1} |
| {path_2} | {tries_2} | {success_2} | {pass_k_2}% | {consecutive_2} | {path_status_2} |

---

## 失敗測試

{if_has_failures}

### 功能測試失敗

| 測試名稱 | 失敗原因 | 建議 |
|----------|----------|------|
| {test_1} | {reason_1} | {suggestion_1} |

### 邊界測試失敗

| 測試名稱 | 輸入 | 預期 | 實際 |
|----------|------|------|------|
| {edge_test_1} | {input_1} | {expected_1} | {actual_1} |

{endif}

---

## 視角摘要

### 功能測試員

- **測試數**：{func_test_count}
- **通過率**：{func_pass_rate}%
- **主要發現**：{func_findings}

### 邊界獵人

- **測試數**：{edge_test_count}
- **通過率**：{edge_pass_rate}%
- **主要發現**：{edge_findings}

### 回歸檢查員

- **測試數**：{reg_test_count}
- **通過率**：{reg_pass_rate}%
- **主要發現**：{reg_findings}

### 驗收驗證員

- **測試數**：{acc_test_count}
- **通過率**：{acc_pass_rate}%
- **主要發現**：{acc_findings}

---

## 不穩定測試

{if_has_flaky}

以下測試表現不穩定，需調查：

| 測試名稱 | 不穩定率 | 建議 |
|----------|----------|------|
| {flaky_1} | {rate_1} | {action_1} |

{endif}

---

## 發布建議

### ✅ SHIP IT 情況

{if_ship_it}

**可以發布**

建議：
1. {ship_suggestion_1}
2. {ship_suggestion_2}

{endif}

### ❌ BLOCKED 情況

{if_blocked}

**需要修復後重新驗證**

必須修復：
1. {block_reason_1}
2. {block_reason_2}

修復後：
```bash
/multi-verify {feature}
```

{endif}

---

## 驗收標準確認

{acceptance_criteria_checklist}

---

## 相關連結

### 視角報告

- [功能測試](./perspectives/functional.md)
- [邊界測試](./perspectives/edge-cases.md)
- [回歸測試](./perspectives/regression.md)
- [驗收測試](./perspectives/acceptance.md)

### 測試結果

- [pass@k 統計](./test-results/pass-at-k.md)
- [失敗分析](./test-results/failures.md)

---

## 簽核

| 項目 | 值 |
|------|-----|
| 驗證時間 | {verified_at} |
| 驗證工具 | multi-agent-verify v2.0.0 |
| 決策 | {decision} |

---

*生成時間：{generated_at}*
