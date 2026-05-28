# TASKS Skill 預設視角配置

> 4 視角分工：依賴分析 + 任務分解 + 測試規劃 + 風險預防

## 視角總覽

| ID | 名稱 | 聚焦領域 | 執行順序 | 產出 |
|----|------|----------|----------|------|
| `dependency-analyst` | 依賴分析師 | 依賴關係、執行順序、並行機會 | 先行 | dependency-graph.md |
| `task-decomposer` | 任務分解師 | 實作任務、估算、驗收標準 | 並行 | T-F-*, T-R-* 任務 |
| `test-planner` | 測試規劃師 | 測試任務、TDD 案例、邊界條件 | 並行 | TEST-* 任務 |
| `risk-preventor` | 風險預防師 | 風險任務、回退點、監控任務 | 並行 | RISK-* 任務 |

## 協作模式

```
Phase 1: 依賴分析（先行）
┌──────────────────────────────────────────────────┐
│  dependency-analyst                               │
│  產出：dependency-graph.md（含 DAG 和 Wave 分組） │
└──────────────────────────────────────────────────┘
         ↓ 依賴圖作為輸入
Phase 2: 並行任務分解
┌──────────────┬──────────────┬──────────────┐
│ task-        │ test-        │ risk-        │
│ decomposer   │ planner      │ preventor    │
│              │              │              │
│ T-F-*, T-R-* │ TEST-*       │ RISK-*       │
└──────────────┴──────────────┴──────────────┘
         ↓
Phase 3: REDUCE 整合
┌──────────────────────────────────────────────────┐
│  合併任務清單 → 應用依賴 → 生成 Wave → tasks.yaml │
└──────────────────────────────────────────────────┘
```

## 執行模式

### 快速模式 (--quick)

使用 2 視角：

| 視角 | 說明 |
|------|------|
| `dependency-analyst` | 依賴分析 |
| `task-decomposer` | 任務分解 |

適用場景：小功能、快速迭代

### 標準模式（預設）

使用 4 視角：全部預設視角

適用場景：標準功能開發

### 深度模式 (--deep)

使用 6 視角：

| 視角 | 說明 |
|------|------|
| 4 個預設視角 | 同上 |
| `parallel-optimizer` | 並行效率優化 |
| `doc-planner` | 文檔任務規劃 |

適用場景：大型功能、重構

## 視角詳細定義

各視角的詳細定義見：

- [dependency-analyst.md](../perspectives/dependency-analyst.md)
- [task-decomposer.md](../perspectives/task-decomposer.md)
- [test-planner.md](../perspectives/test-planner.md)
- [risk-preventor.md](../perspectives/risk-preventor.md)

## 視角輸出要求

### 通用要求

1. 任務 ID 格式正確（T-F-001, TEST-001, RISK-001）
2. 每個任務有明確的驗收標準
3. 任務粒度在 10-60 分鐘範圍
4. 優先級標記（P0/P1/P2）
5. 依賴關係明確

### 視角專屬要求

| 視角 | 專屬要求 |
|------|----------|
| dependency-analyst | DAG 無循環、Wave 分組合理 |
| task-decomposer | 估算完整、files 欄位填寫 |
| test-planner | test_cases 完整、TDD 順序正確 |
| risk-preventor | related_risk 關聯、trigger 明確 |
