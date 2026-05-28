# 實作記錄：{feature}

> 由 multi-implement skill 自動生成

## 概覽

| 項目 | 值 |
|------|-----|
| 功能名稱 | {feature} |
| 實作日期 | {date} |
| 視角數量 | {perspective_count} |
| 任務數量 | {task_count} |
| pass@{k} | {pass_at_k}% |
| 總變更 | +{lines_added} / -{lines_removed} |

---

## 來源計劃

- **計劃 ID**：{plan_id}
- **計劃連結**：[implementation-plan.md](../../plans/{plan_id}/implementation-plan.md)
- **驗收標準**：{acceptance_criteria_summary}

---

## 實作摘要

### 完成任務

| # | 任務 | 狀態 | 嘗試次數 | 視角評分 |
|---|------|------|----------|----------|
| 1 | {task_1} | {status} | {attempts} | {score}/10 |
| 2 | {task_2} | {status} | {attempts} | {score}/10 |
| ... | ... | ... | ... | ... |

### 檔案變更

| 檔案 | 類型 | 變更 |
|------|------|------|
| {file_1} | {type} | +{added}/-{removed} |
| {file_2} | {type} | +{added}/-{removed} |
| ... | ... | ... |

---

## 視角報告

### TDD 守護者

**評分**：{tdd_score}/10

**測試覆蓋**：

| 類型 | 數量 | 覆蓋率 |
|------|------|--------|
| 單元測試 | {n} | {coverage}% |
| 整合測試 | {n} | {coverage}% |
| 邊界案例 | {n} | - |

**主要發現**：
- {tdd_finding_1}
- {tdd_finding_2}

**詳細報告**：[tdd-report.md](./perspectives/tdd-report.md)

---

### 效能優化師

**評分**：{perf_score}/10

**效能分析**：

| 模組 | 時間複雜度 | 空間複雜度 | 狀態 |
|------|------------|------------|------|
| {module_1} | {time} | {space} | {status} |
| {module_2} | {time} | {space} | {status} |

**主要發現**：
- {perf_finding_1}
- {perf_finding_2}

**詳細報告**：[performance-report.md](./perspectives/performance-report.md)

---

### 安全審計員

**評分**：{sec_score}/10

**安全檢查**：

| OWASP | 檢查項 | 狀態 |
|-------|--------|------|
| A1 | Injection | {status} |
| A2 | Broken Auth | {status} |
| A3 | Sensitive Data | {status} |
| A7 | XSS | {status} |

**主要發現**：
- {sec_finding_1}
- {sec_finding_2}

**詳細報告**：[security-report.md](./perspectives/security-report.md)

---

### 維護性專家

**評分**：{maint_score}/10

**程式碼品質**：

| 指標 | 值 | 閾值 | 狀態 |
|------|-----|------|------|
| 平均函數長度 | {n} 行 | < 50 | {status} |
| 循環複雜度 | {n} | < 10 | {status} |
| 程式碼重複率 | {n}% | < 10% | {status} |

**主要發現**：
- {maint_finding_1}
- {maint_finding_2}

**詳細報告**：[maintainability.md](./perspectives/maintainability.md)

---

## pass@k 統計

### 整體結果

| 指標 | 值 |
|------|-----|
| 總任務數 | {total_tasks} |
| pass@1 | {pass_at_1}% |
| pass@{k} | {pass_at_k}% |
| 平均嘗試 | {avg_attempts} |

### 失敗分析

{if_has_failures}

| 任務 | 失敗類型 | 解決方法 |
|------|----------|----------|
| {task} | {failure_type} | {resolution} |

{else}
所有任務均在預期嘗試次數內完成 ✅
{endif}

**詳細統計**：[pass-at-k-metrics.md](./pass-at-k-metrics.md)

---

## 監督回饋歷史

### 阻擋項修正記錄

{if_had_blocks}

| 時間 | 視角 | 問題 | 修正 |
|------|------|------|------|
| {time} | {perspective} | {issue} | {fix} |

{else}
無阻擋項 ✅
{endif}

### 警告項記錄

{if_had_warnings}

| 視角 | 警告 | 處理 |
|------|------|------|
| {perspective} | {warning} | {action} |

{endif}

---

## 同步檢查點

### S1 (50% 完成)

- **時間**：{s1_time}
- **狀態**：{s1_status}
- **備註**：{s1_notes}

### S2 (80% 完成)

- **時間**：{s2_time}
- **狀態**：{s2_status}
- **備註**：{s2_notes}

---

## 教訓與改進

### 有效做法

- {what_worked_1}
- {what_worked_2}

### 改進空間

- {improvement_1}
- {improvement_2}

### 未來建議

- {suggestion_1}
- {suggestion_2}

---

## 相關連結

### 視角報告

- [TDD 報告](./perspectives/tdd-report.md)
- [效能報告](./perspectives/performance-report.md)
- [安全報告](./perspectives/security-report.md)
- [維護性報告](./perspectives/maintainability.md)

### 其他

- [pass@k 統計](./pass-at-k-metrics.md)
- [變更摘要](./changes-summary.md)
- [原始計劃](../../plans/{plan_id}/implementation-plan.md)

---

## 簽核

| 項目 | 值 |
|------|-----|
| 完成時間 | {completed_at} |
| 實作工具 | multi-agent-implement v2.0.0 |
| 視角模式 | {mode} |

---

*生成時間：{generated_at}*
