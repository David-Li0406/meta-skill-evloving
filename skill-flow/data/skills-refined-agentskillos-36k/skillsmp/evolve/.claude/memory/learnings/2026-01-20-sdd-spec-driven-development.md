---
date: "2026-01-20"
tags: [sdd, spec-driven, methodology, ai-collaboration, kaochenlong]
source: https://kaochenlong.com/sdd-spec-driven-development
---

# SDD 規格驅動開發 - 高見龍

## 核心理念

> 「在開始之前，先定義什麼叫『完成』」

解決 Vibe Coding 的三大問題：
1. 程式碼風格不一致
2. AI 未主動告知漏掉的需求
3. AI 說「完成了」卻忽視測試失敗

## 三階段流程

```
Requirements (requirements.md)
    ↓ 使用者故事 + EARS 驗收標準
Design (design.md)
    ↓ 架構圖、資料模型、API 設計
Tasks (tasks.md)
    ↓ 可追蹤的小任務
實作
```

## EARS 格式

結構化的驗收標準寫法：
> 「當使用者輸入正確 Email 和密碼時，系統應將使用者導向首頁」

## 三層級分類

| 層級 | 說明 | 適用場景 |
|------|------|----------|
| Spec-first | 規格優先，完成後可丟棄 | 小型功能 |
| Spec-anchored | 規格隨專案演進更新 | 團隊協作 |
| Spec-as-source | 程式碼由規格自動生成 | 高度自動化 |

## 與 Self-Evolving Agent 整合

| SDD | Self-Evolving Agent |
|-----|---------------------|
| 先定義完成 | CP0 北極星錨定 |
| Requirements | spec-workflow: requirements.md |
| Design | spec-workflow: design.md |
| Tasks | spec-workflow: tasks.md / `--from-spec` |
| EARS 驗收 | CP2 測試驗證 |
| Spec-anchored | Git-based Memory |

## 適用情境

**適合 SDD**：
- 既有系統漸進式改進
- 複雜新專案
- 團隊協作

**可用 Vibe Coding**：
- 小型 POC
- 一次性工具

## 關鍵洞察

1. SDD 會減慢初期開發但提升長期品質
2. 工程師角色轉變：編碼者 → 規格定義者
3. 工具在演進，但 SDD 思維方式具永久價值
