# Quick Start Guide

> 3 分鐘快速上手 Multi-Agent Plan

## 最簡用法

```bash
/multi-plan 建立用戶認證系統
```

這會：
1. 啟動 4 個並行規劃 Agent
2. 從不同視角分析需求
3. 達成設計共識
4. 產出實作計劃
5. 自動存檔到 Memory

## 常用模式

### 快速規劃（2 視角）

```bash
/multi-plan --quick 新增簡單功能
```

適用：小型功能、時間有限

### 深度規劃（6 視角）

```bash
/multi-plan --deep 核心系統重構
```

適用：重大架構變更、高風險專案

### 從研究開始

```bash
# 先研究
/multi-research 微服務架構模式

# 再規劃（自動載入研究結果）
/multi-plan --from-research microservice-patterns 建立微服務架構
```

### 自訂視角

```bash
/multi-plan --custom 特定領域專案
```

會互動式詢問你想要的視角

## 輸出位置

所有規劃結果存儲在：

```
.claude/memory/plans/[feature-id]/
├── implementation-plan.md  ← 主計劃（先看這個）
├── milestones.md           ← 里程碑清單
├── overview.md             ← 一頁摘要
├── synthesis.md            ← 共識設計
└── perspectives/           ← 各視角詳細報告
    ├── architect.md
    ├── risk-analyst.md
    ├── estimator.md
    └── ux-advocate.md
```

## 復用規劃

如果之前規劃過類似功能：

```bash
# 系統會自動提示
> 發現相關規劃：auth-system (2025-01-20)
> 是否要：
>   1. 復用並調整
>   2. 重新規劃
>   3. 取消
```

## 進階技巧

### 指定視角數量

```bash
/multi-plan --perspectives 3 某功能
```

### 不存檔

```bash
/multi-plan --no-memory 臨時規劃
```

### 與 evolve 整合

規劃結果會自動與 evolve Checkpoint 同步：
- CP1: 搜尋相關 Memory
- CP1.5: 設計共識達成
- CP3.5: 規劃完成後更新 index.md

## 下一步

- [了解預設視角](../../01-perspectives/_base/default-perspectives.md)
- [自訂視角指南](../../01-perspectives/_base/custom-perspectives.md)
- [理解 Map-Reduce 流程](../../../../shared/coordination/map-phase.md)
