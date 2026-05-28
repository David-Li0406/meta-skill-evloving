# Quick Start Guide

> 3 分鐘快速上手 Multi-Agent Research

## 最簡用法

```bash
/multi-research AI Agent 最佳實踐
```

這會：
1. 啟動 4 個並行研究 Agent
2. 從不同視角分析主題
3. 匯總成一份完整報告
4. 自動存檔到 Memory

## 常用模式

### 快速研究（2 視角）

```bash
/multi-research --quick 某個技術選型問題
```

適用：時間有限、需要快速答案

### 深度研究（6 視角）

```bash
/multi-research --deep 複雜架構決策
```

適用：重大決策、需要全面分析

### 自訂視角

```bash
/multi-research --custom 特定領域問題
```

會互動式詢問你想要的視角

## 輸出位置

所有研究結果存儲在：

```
.claude/memory/research/[topic-id]/
├── synthesis.md      ← 主報告（先看這個）
├── overview.md       ← 一頁摘要
└── perspectives/     ← 各視角詳細報告
```

## 復用研究

如果之前研究過類似主題：

```bash
# 系統會自動提示
> 發現相關研究：ai-agent-patterns (2025-01-15)
> 是否要：
>   1. 復用並補充
>   2. 重新研究
>   3. 取消
```

## 進階技巧

### 指定視角數量

```bash
/multi-research --perspectives 3 某主題
```

### 不存檔

```bash
/multi-research --no-memory 臨時研究
```

### 與 evolve 整合

研究結果會自動與 evolve Checkpoint 同步：
- CP1: 搜尋相關 Memory
- CP3.5: 研究完成後更新 index.md

## 下一步

- [了解預設視角](../../01-perspectives/_base/default-perspectives.md)
- [自訂視角指南](../../01-perspectives/_base/custom-perspectives.md)
- [理解 Map-Reduce 流程](../../../../shared/coordination/map-phase.md)
