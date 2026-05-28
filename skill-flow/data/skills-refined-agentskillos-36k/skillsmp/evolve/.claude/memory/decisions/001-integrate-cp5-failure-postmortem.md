---
number: 1
title: 整合 CP5 失敗後驗屍機制
date: 2026-01-12
status: accepted
tags: [checkpoint, failure-handling, learning, pdca]
---

# ADR-001: 整合 CP5 失敗後驗屍機制

## 狀態

已接受 (Accepted)

## 背景

Self-Evolving Agent 原有 4 個強制檢查點 (CP1-CP4)：
- CP1: 任務開始前搜尋 Memory
- CP2: 程式碼變更後驗證
- CP3: Milestone 完成後確認方向
- CP4: 迭代完成後涌現檢查

然而，當 PDCA Check 階段失敗時，缺乏結構化的失敗分析機制。失敗經驗雖然會記錄到 `failures/`，但格式不統一，缺乏可搜尋性和可複用性。

## 決策

新增 **Checkpoint 5 (CP5): 失敗後驗屍 (Failure Post-Mortem)**

### 觸發條件
- PDCA Check 失敗時
- 測試/構建失敗時
- 連續 2 次嘗試失敗時
- 用戶反饋「不對」時

### 強制輸出
每次觸發 CP5 必須生成結構化 Lesson 到 `.claude/memory/lessons/`，包含：
- 失敗分類 (Type A-E)
- 5 Whys 根因分析
- 可泛化的 lesson.principle
- 修正措施和結果

### 失敗分類

| Type | 名稱 | 典型修正 |
|------|------|----------|
| A | Knowledge Gap | 習得新 Skill |
| B | Execution Error | 重試、微調參數 |
| C | Environment Issue | 修復環境 |
| D | Strategy Error | 切換策略 |
| E | Resource Limit | 分解任務 |

## 理由

1. **結構化學習**: 統一的 Lesson 格式讓失敗經驗可搜尋、可複用
2. **防止重複犯錯**: 明確的 `applicable_to` 和 `not_applicable_when` 欄位
3. **量化改進**: 可追蹤 `重複失敗率` 和 `修復成功率`
4. **與 PDCA 整合**: 下一輪 Plan 自動載入相關 Lessons

## 替代方案

1. **只用現有 failures/ 目錄** - 拒絕，格式不統一
2. **外部服務記錄** - 拒絕，違反 Git-based 原則
3. **只記錄不分類** - 拒絕，缺乏診斷指導

## 後果

### 正面
- 失敗經驗成為結構化知識
- PDCA 循環更加完整
- 可追蹤學習效果指標

### 負面
- 每次失敗需要額外時間寫 Lesson
- 新增目錄 `lessons/` 增加結構複雜度

### 風險
- Lesson 品質取決於 AI 的分析能力
- 需要用戶配合觸發 CP5

## 參考

- [SAGE (Self-Attributing)](https://arxiv.org/abs/xxx) - 自我歸因框架
- [GEPA (Genetic Pareto)](https://cookbook.openai.com/examples/partners/self_evolving_agents/autonomous_agent_retraining) - 反思評估
