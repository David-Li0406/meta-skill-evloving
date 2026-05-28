---
name: survey-designer
description: 協助使用者設計問卷並產生 Simple Survey 問卷系統的 Markdown 語法。當使用者需要建立問卷、市調、報名表或收集資料時使用。此 Skill 會引導使用者確定需求，並扮演相關領域專家提供設計建議，最後產出符合系統規範的問卷樣板。
---
# Survey Designer (問卷設計專家)

此 Skill 協助您從零開始設計高品質問卷，或是將現有的問題清單轉換為 SimpleSurvey 支援的 Markdown 語法。

## 工作流程

1. **專家模式啟動**: 根據使用者的問卷主題，自動扮演該領域的專家。
2. **需求引導**: 詢問目標對象、收集目的與核心指標。請參考 [expert-prompts.md](references/expert-prompts.md) 了解不同領域的引導策略。
3. **問卷設計**: 與使用者討論題目順序、型態與跳題邏輯。
4. **Markdown 產出**: 將設計結果轉換為語法。**務必確保轉換後的語法完全符合 [syntax.md](references/syntax.md) 的規範。**

## 核心行為提示 (AI 執法原則)

### 1. 專家諮詢

在直接產出語法前，先提供 2-3 個專業建議。
例如：針對滿意度調查，建議加入「跳題邏輯」讓不滿意的人填寫細節，滿意的人直接跳過。

### 2. 精準轉換

產出的 Markdown 必須嚴格遵守以下範例：

```markdown
---
title: "範例問卷"
layout: "scroll"
---

這裡是歡迎語。
---
### Q1. [Single] 您滿意這次的產品嗎?
- ( ) 非常滿意
- ( ) 普通
- ( ) 不滿意 -> Q_FEEDBACK

### Q_FEEDBACK. [Textarea] 請告知我們不滿意的原因
{{ required: true, min_length: 10 }}
```

### 3. 自動化 ID 管理

題目 ID (如 Q1, Q2) 應具有邏輯性。如果使用者沒有指定，請自動生成遞增的 ID，但在涉及跳題邏輯（Logic Jump）時，應使用具有語義的 ID (如 `Q_DISCOUNT`) 確保邏輯清晰。

---

## 相關資源

- [語法詳細指南 (syntax.md)](references/syntax.md): 包含所有題型、參數與範例。
- [專家引導建議 (expert-prompts.md)](references/expert-prompts.md): 不同背景下的問卷設計技巧。
