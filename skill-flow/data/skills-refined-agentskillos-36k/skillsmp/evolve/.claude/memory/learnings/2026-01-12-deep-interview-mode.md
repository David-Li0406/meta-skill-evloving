---
date: 2026-01-12
tags: [goal-analysis, deep-interview, spec, requirements, benson-sun]
task: 整合深度訪談模式到目標分析流程
status: resolved
source: https://x.com/BensonTWN/status/2010319050099110270
---

# 深度訪談模式 - 從 Benson Sun 學到的技巧

## 情境

在 X (Twitter) 上看到 Benson Sun (@BensonTWN) 分享的 Claude Code prompt 技巧。

## 核心洞察

> 寫 spec 最大的問題是「你不知道自己漏了什麼」

這正好補足 evolve 原本的盲點：
- 我們有「失敗後學習」(CP5 Failure Post-Mortem)
- 但缺少「開始前預防」的深度訪談機制

## 解決方案

整合「深度訪談模式」到 `01-core/_base/goal-analysis.md`：

### 1. 訪談執行邏輯

讓 Claude 扮演資深技術顧問，用 AskUserQuestion 進行多輪訪談。

### 2. Ultrathink 分析（每個問題前）

- 這個規格可能隱藏的假設是什麼？
- 哪些邊界情況沒有被考慮到？
- 技術債務可能在哪裡累積？
- 這個設計決策的二階、三階效應是什麼？

### 3. 觸發條件

| 條件 | 是否觸發 |
|------|----------|
| 架構等級 Level 2 | 強制觸發 |
| 架構等級 Level 1 + 目標模糊 | 建議觸發 |
| 架構等級 Level 0 | 跳過 |
| spec-workflow requirements 階段 | 強制觸發 |

### 4. 訪談問題類型

- 隱藏假設探索
- 邊界情況
- 技術債務預防
- 二階/三階效應

## 驗證

✅ 已更新 `skills/01-core/_base/goal-analysis.md`
✅ 新增完整的深度訪談流程、問題範本、結束條件、產出格式

## 注意事項

- 問題要深入且不流於表面
- 設定 10 個問題上限避免疲勞
- 訪談產出應整理為結構化的 goal_specification

## 原始 Prompt（Benson Sun 版本）

```
閱讀這份 SPEC 文件，然後使用 AskUserQuestionTool 對我進行深度訪談，
涵蓋所有面向：技術實作、UI/UX、潛在疑慮、設計取捨等。
問題必須深入且不流於表面。

請啟用 ultrathink 模式：在每個問題之前，先進行深度思考分析，包括：
- 這個規格可能隱藏的假設是什麼？
- 哪些邊界情況沒有被考慮到？
- 技術債務可能在哪裡累積？
- 這個設計決策的二階、三階效應是什麼？

持續訪談直到所有關鍵面向都被釐清，然後將完整的規格寫入檔案。
```
