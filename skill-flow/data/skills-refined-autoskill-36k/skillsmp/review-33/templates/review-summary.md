# 審查報告：{scope}

> 由 multi-review skill 自動生成

## 概覽

| 項目 | 值 |
|------|-----|
| 審查範圍 | {scope} |
| 審查日期 | {date} |
| 視角數量 | {perspective_count} |
| 檔案數量 | {files_count} |
| 變更行數 | +{lines_added} / -{lines_removed} |

### 問題統計

| 嚴重度 | 數量 | 狀態 |
|--------|------|------|
| 🚨 CRITICAL | {critical_count} | {critical_status} |
| ⚠️ HIGH | {high_count} | {high_status} |
| 📝 MEDIUM | {medium_count} | {medium_status} |
| 💡 LOW | {low_count} | {low_status} |

### 審查結論

{review_conclusion}

---

## Blockers（必須修正）

> 以下問題必須在合併前修正

{blockers_section}

詳見：[issues/blockers.md](./issues/blockers.md)

---

## 建議修正

> 以下問題強烈建議修正

{suggestions_section}

詳見：[issues/suggestions.md](./issues/suggestions.md)

---

## 未來改進

> 以下問題可延後處理

{future_section}

詳見：[issues/future.md](./issues/future.md)

---

## 優點

> 值得肯定的設計和實現

{positives_section}

---

## 視角摘要

### 程式碼品質

- **評分**：{quality_score}/10
- **主要發現**：{quality_findings}

### 測試覆蓋

- **覆蓋率**：{coverage_rate}%
- **主要發現**：{coverage_findings}

### 文檔完整度

- **評分**：{doc_score}/10
- **主要發現**：{doc_findings}

### 整合影響

- **破壞性變更**：{breaking_changes}
- **主要發現**：{integration_findings}

---

## 修正建議順序

建議按以下順序修正問題：

1. {fix_order_1}
2. {fix_order_2}
3. {fix_order_3}

---

## 相關連結

### 視角報告

- [程式碼品質](./perspectives/code-quality.md)
- [測試覆蓋](./perspectives/test-coverage.md)
- [文檔審查](./perspectives/documentation.md)
- [整合審查](./perspectives/integration.md)

### 問題分類

- [Blockers](./issues/blockers.md)
- [Suggestions](./issues/suggestions.md)
- [Future](./issues/future.md)

---

## 下一步

{next_steps}

---

*生成時間：{generated_at}*
