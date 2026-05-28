# 實作計劃：{feature}

> 由 multi-plan skill 自動生成

## 概述

| 項目 | 值 |
|------|-----|
| 功能名稱 | {feature} |
| 規劃日期 | {date} |
| 視角數量 | {perspective_count} |
| 估算工期 | {estimated_effort} |
| 相關研究 | {related_research} |

### 一句話描述

{one_line_description}

### 成功指標

- [ ] {success_criteria_1}
- [ ] {success_criteria_2}
- [ ] {success_criteria_3}

---

## 技術設計

> 信心度：{architect_confidence}

### 架構概述

{architecture_overview}

### 組件設計

| 組件 | 職責 | 技術選型 |
|------|------|----------|
| {component_1} | {responsibility_1} | {tech_1} |
| {component_2} | {responsibility_2} | {tech_2} |

### 技術決策

| 決策 | 選擇 | 理由 |
|------|------|------|
| {decision_1} | {choice_1} | {reason_1} |

### 依賴關係

- **外部依賴**：{external_deps}
- **內部依賴**：{internal_deps}

---

## 風險與緩解

> 信心度：{risk_confidence}

### 風險矩陣

| 風險 | 可能性 | 影響 | 緩解策略 |
|------|--------|------|----------|
| {risk_1} | 高/中/低 | 高/中/低 | {mitigation_1} |
| {risk_2} | 高/中/低 | 高/中/低 | {mitigation_2} |

### 關鍵風險詳述

#### {risk_name}

- **描述**：{risk_description}
- **觸發條件**：{trigger_condition}
- **緩解措施**：{mitigation_detail}
- **備援方案**：{fallback_plan}

---

## 里程碑

> 信心度：{estimator_confidence}

### 里程碑概覽

```
[M1] ──────► [M2] ──────► [M3] ──────► [M4] ──────► [完成]
{m1_name}   {m2_name}    {m3_name}    {m4_name}
{m1_time}   {m2_time}    {m3_time}    {m4_time}
```

### 詳細里程碑

#### M1: {milestone_1_name}

- **目標**：{m1_goal}
- **估算時間**：{m1_estimate}
- **驗收標準**：
  - [ ] {m1_criteria_1}
  - [ ] {m1_criteria_2}
- **輸出**：{m1_output}

#### M2: {milestone_2_name}

- **目標**：{m2_goal}
- **估算時間**：{m2_estimate}
- **依賴**：M1 完成
- **驗收標準**：
  - [ ] {m2_criteria_1}
  - [ ] {m2_criteria_2}

---

## 體驗設計

> 信心度：{ux_confidence}

### 使用者流程

```
{user_flow_diagram}
```

### API 設計

```
{api_design}
```

### 錯誤處理

| 錯誤類型 | 使用者看到 | 處理方式 |
|----------|------------|----------|
| {error_1} | {user_message_1} | {handling_1} |

### 文檔需求

- [ ] {doc_1}
- [ ] {doc_2}

---

## 任務清單

### 階段 1: {phase_1_name}

- [ ] **{task_1}** ({estimate_1})
  - {subtask_1_1}
  - {subtask_1_2}
- [ ] **{task_2}** ({estimate_2})

### 階段 2: {phase_2_name}

- [ ] **{task_3}** ({estimate_3})
- [ ] **{task_4}** ({estimate_4})

---

## 待決事項

> 以下事項需在實作前確認

### 技術待決

- [ ] {tech_pending_1}
- [ ] {tech_pending_2}

### 需求待決

- [ ] {req_pending_1}

---

## 附錄

### 視角報告連結

- [架構師視角](./perspectives/architect.md)
- [風險分析視角](./perspectives/risk-analyst.md)
- [估算專家視角](./perspectives/estimator.md)
- [UX 倡導者視角](./perspectives/ux-advocate.md)

### 相關資源

- [共識設計](./synthesis.md)
- [風險緩解策略](./risk-mitigation.md)
- [里程碑清單](./milestones.md)

---

*生成時間：{generated_at}*
*版本：v1.0*
