# 多 Agent 協作研究框架 - 系統架構設計報告

**研究日期**: 2026-01-23
**研究視角**: 系統架構設計
**研究標籤**: multi-agent, collaboration, architecture, coordination, knowledge-fusion

---

## 執行摘要

本報告從系統架構視角，深入研究如何設計多 Agent 協作研究框架。基於對現有模式（Claude Code Task 工具、PAL MCP 多模型協作、Claude Plan 並行執行）的分析，提出三種協作架構模式，並推薦最適合研究場景的混合架構方案。

**核心發現**:
- 研究任務適合 **Map-Reduce 混合模式**（並行研究 + 串行整合）
- 狀態管理應採用 **分層架構**（SQLite + 共享 Context）
- 匯總 Agent 需要 **智能融合策略**，而非簡單拼接
- 與 evolve skill 整合可複用現有的 Memory 和 Checkpoint 機制

---

## 一、協作模式架構

### 1.1 並行模式（Parallel Pattern）

**核心理念**: 多個 Agent 同時獨立執行不同任務，無相互依賴。

```
┌─────────────────────────────────────────────────────────────────┐
│                    並行協作架構                                  │
│                                                                 │
│             研究主題                                             │
│                 │                                               │
│     ┌───────────┼───────────┐                                   │
│     ↓           ↓           ↓                                   │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐                            │
│ │ Agent A │ │ Agent B │ │ Agent C │                            │
│ │ 架構    │ │ 狀態    │ │ 整合    │                            │
│ │ 視角    │ │ 管理    │ │ 策略    │                            │
│ └────┬────┘ └────┬────┘ └────┬────┘                            │
│      │           │           │                                  │
│      ↓           ↓           ↓                                  │
│   結果 A       結果 B       結果 C                               │
│      │           │           │                                  │
│      └───────────┼───────────┘                                  │
│                  ↓                                              │
│          ┌──────────────┐                                       │
│          │ 匯總 Agent   │                                       │
│          │ (Aggregator) │                                       │
│          └──────┬───────┘                                       │
│                 ↓                                               │
│           最終研究報告                                           │
└─────────────────────────────────────────────────────────────────┘
```

**通訊機制**:
```typescript
interface ParallelCoordination {
  // Agent 只與協調者通訊
  coordinator: {
    assignTask(agentId: string, task: Task): void
    reportResult(agentId: string, result: Result): void
    checkStatus(agentId: string): Status
  }

  // Agent 間無直接通訊
  agents: Agent[]
}
```

**優點**:
- ✅ 最高並行度，執行速度快
- ✅ Agent 獨立性強，故障隔離好
- ✅ 易於水平擴展
- ✅ 實作簡單

**缺點**:
- ❌ 無法處理 Agent 間依賴
- ❌ 知識無法即時共享
- ❌ 可能產生重複研究
- ❌ 匯總 Agent 負擔重

**適用場景**:
- 研究子主題完全獨立
- 各視角無交集
- 時間要求高

---

### 1.2 串行模式（Sequential Pattern）

**核心理念**: Agent 依序執行，後續 Agent 可利用前者的成果。

```
┌─────────────────────────────────────────────────────────────────┐
│                    串行協作架構                                  │
│                                                                 │
│             研究主題                                             │
│                 ↓                                               │
│          ┌──────────┐                                           │
│          │ Agent A  │  ← 架構視角                              │
│          │ (先鋒)   │                                           │
│          └────┬─────┘                                           │
│               ↓                                                 │
│         共享知識庫                                              │
│               ↓                                                 │
│          ┌──────────┐                                           │
│          │ Agent B  │  ← 狀態管理（基於 A 的發現）              │
│          │ (建構)   │                                           │
│          └────┬─────┘                                           │
│               ↓                                                 │
│         共享知識庫                                              │
│               ↓                                                 │
│          ┌──────────┐                                           │
│          │ Agent C  │  ← 整合策略（基於 A+B 的成果）            │
│          │ (整合)   │                                           │
│          └────┬─────┘                                           │
│               ↓                                                 │
│          ┌──────────┐                                           │
│          │ Agent D  │  ← 匯總（融合所有發現）                  │
│          │ (匯總)   │                                           │
│          └────┬─────┘                                           │
│               ↓                                                 │
│        最終研究報告                                             │
└─────────────────────────────────────────────────────────────────┘
```

**通訊機制**:
```typescript
interface SequentialCoordination {
  // 通過共享知識庫通訊
  knowledgeBase: {
    write(agentId: string, findings: Findings): void
    readAll(): Findings[]
    query(topic: string): Findings[]
  }

  // Pipeline 控制
  pipeline: {
    next(currentAgent: Agent): Agent | null
    canProceed(): boolean
  }
}
```

**優點**:
- ✅ 知識累積性強
- ✅ 避免重複研究
- ✅ 可建立深度依賴
- ✅ 易於追蹤演進

**缺點**:
- ❌ 執行速度慢（線性時間）
- ❌ 一個 Agent 失敗會阻塞所有後續
- ❌ 前期 Agent 的錯誤會傳播
- ❌ 無法利用並行資源

**適用場景**:
- 研究有明確階段依賴
- 後續研究需要前期基礎
- 品質優先於速度

---

### 1.3 混合模式（Hybrid Pattern）— 推薦

**核心理念**: Map-Reduce 思維，並行研究 + 串行整合。

```
┌─────────────────────────────────────────────────────────────────┐
│                  混合協作架構（推薦）                             │
│                                                                 │
│                研究主題                                          │
│                    │                                            │
│            ┌───────┴────────┐                                   │
│            │   協調器        │                                  │
│            │ (Coordinator)   │                                  │
│            └───────┬────────┘                                   │
│                    │                                            │
│        ┌───────────┼───────────┐                                │
│        ↓           ↓           ↓                                │
│   ┌─────────┐ ┌─────────┐ ┌─────────┐                          │
│   │ Agent A │ │ Agent B │ │ Agent C │  ← MAP 階段（並行）      │
│   │ 架構    │ │ 狀態    │ │ 整合    │                          │
│   │ 視角    │ │ 管理    │ │ 策略    │                          │
│   └────┬────┘ └────┬────┘ └────┬────┘                          │
│        │           │           │                                │
│        └───────────┼───────────┘                                │
│                    ↓                                            │
│            ┌───────────────┐                                    │
│            │  共享知識庫    │  ← 中間狀態                       │
│            │ (Knowledge    │                                    │
│            │  Repository)  │                                    │
│            └───────┬───────┘                                    │
│                    ↓                                            │
│            ┌──────────────┐                                     │
│            │ 融合 Agent 1  │  ← REDUCE 階段（串行）             │
│            │ (交叉檢查)    │                                    │
│            └───────┬───────┘                                    │
│                    ↓                                            │
│            ┌──────────────┐                                     │
│            │ 融合 Agent 2  │                                    │
│            │ (矛盾解決)    │                                    │
│            └───────┬───────┘                                    │
│                    ↓                                            │
│            ┌──────────────┐                                     │
│            │ 融合 Agent 3  │                                    │
│            │ (報告生成)    │                                    │
│            └───────┬───────┘                                    │
│                    ↓                                            │
│             最終研究報告                                         │
└─────────────────────────────────────────────────────────────────┘
```

**架構組件**:

```typescript
interface HybridArchitecture {
  // 協調器
  coordinator: {
    decomposeResearch(topic: string): SubTopics[]
    assignTasks(agents: Agent[], tasks: Task[]): void
    monitorProgress(): Progress
    triggerReduction(): void
  }

  // Map 階段（並行研究）
  mapPhase: {
    parallelAgents: ResearchAgent[]
    taskQueue: TaskQueue
    resultCollector: ResultCollector
  }

  // 共享知識庫
  knowledgeRepository: {
    store(agentId: string, findings: Findings): void
    query(criteria: SearchCriteria): Findings[]
    detectConflicts(): Conflict[]
    findGaps(): Gap[]
  }

  // Reduce 階段（串行整合）
  reducePhase: {
    crossCheckAgent: Agent      // 交叉檢查
    conflictResolveAgent: Agent  // 矛盾解決
    reportGenerationAgent: Agent // 報告生成
  }
}
```

**通訊機制**:

```typescript
// Map 階段：中央協調
interface MapCommunication {
  // Agent → Coordinator
  reportProgress(agentId: string, progress: number): void
  submitFindings(agentId: string, findings: Findings): void

  // Coordinator → Agent
  assignTask(agentId: string, task: Task): void
  requestRevision(agentId: string, feedback: Feedback): void
}

// Reduce 階段：流水線
interface ReduceCommunication {
  // 通過知識庫傳遞
  knowledgeBase: SharedKnowledgeBase

  // 階段間協調
  pipeline: {
    stage1_crossCheck(): CrossCheckResult
    stage2_resolveConflicts(result: CrossCheckResult): ResolvedResult
    stage3_generateReport(result: ResolvedResult): FinalReport
  }
}
```

**優點**:
- ✅ 兼顧速度（Map 並行）和深度（Reduce 串行）
- ✅ 知識融合質量高
- ✅ 可檢測矛盾和遺漏
- ✅ 靈活應對不同場景

**缺點**:
- ⚠️ 實作複雜度較高
- ⚠️ 需要智能的協調邏輯
- ⚠️ Reduce 階段可能成為瓶頸

**適用場景**:
- ✅ 研究任務（本場景最佳）
- ✅ 複雜分析任務
- ✅ 需要多視角的決策

---

## 二、狀態管理架構

### 2.1 分層狀態模型

```
┌─────────────────────────────────────────────────────────────────┐
│                      狀態管理分層架構                             │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Layer 1: Agent 私有狀態 (Ephemeral)                     │   │
│  │  - 當前任務上下文                                         │   │
│  │  - 暫存的思考過程                                         │   │
│  │  - 本地緩存                                              │   │
│  │  儲存: In-Memory                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↕                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Layer 2: 協作共享狀態 (Session-Scoped)                  │   │
│  │  - 研究發現 (Findings)                                   │   │
│  │  - Agent 間的問答                                        │   │
│  │  - 工作進度                                              │   │
│  │  儲存: SQLite Context Table                             │   │
│  └─────────────────────────────────────────────────────────┘   │
│                           ↕                                     │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │  Layer 3: 持久知識庫 (Persistent)                        │   │
│  │  - 完整研究報告                                          │   │
│  │  - 學習經驗                                              │   │
│  │  - 失敗案例                                              │   │
│  │  儲存: SQLite Memory Table + Filesystem                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 共享知識庫設計

**Schema 設計**:

```sql
-- Agent 研究發現表
CREATE TABLE research_findings (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    agent_perspective TEXT NOT NULL,  -- 'architecture', 'state-management', etc.

    -- 內容
    topic TEXT NOT NULL,
    findings TEXT NOT NULL,  -- Markdown 格式
    confidence REAL DEFAULT 0.8,  -- 0.0-1.0

    -- 關聯
    references TEXT,  -- JSON array of source references
    related_findings TEXT,  -- JSON array of related finding IDs

    -- 元數據
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP,

    -- 索引
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- FTS5 全文搜尋
CREATE VIRTUAL TABLE research_findings_fts USING fts5(
    topic,
    findings,
    content=research_findings,
    content_rowid=rowid
);

-- 衝突偵測表
CREATE TABLE research_conflicts (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL,
    finding_a_id TEXT NOT NULL,
    finding_b_id TEXT NOT NULL,

    conflict_type TEXT NOT NULL,  -- 'contradiction', 'overlap', 'gap'
    description TEXT,
    resolution TEXT,

    resolved BOOLEAN DEFAULT FALSE,
    resolved_by TEXT,  -- agent_id
    resolved_at TEXT,

    FOREIGN KEY (finding_a_id) REFERENCES research_findings(id),
    FOREIGN KEY (finding_b_id) REFERENCES research_findings(id)
);

-- Session 協調表
CREATE TABLE coordination_state (
    session_id TEXT PRIMARY KEY,
    research_topic TEXT NOT NULL,

    phase TEXT NOT NULL,  -- 'map', 'reduce', 'completed'

    -- Map 階段狀態
    total_agents INTEGER,
    completed_agents INTEGER,

    -- Reduce 階段狀態
    reduce_stage TEXT,  -- 'cross-check', 'resolve', 'generate'

    -- 元數據
    started_at TEXT DEFAULT CURRENT_TIMESTAMP,
    updated_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

### 2.3 狀態同步機制

```typescript
interface StateManagement {
  // 讀取操作（高並發）
  read: {
    getFindings(agentId?: string): Findings[]
    searchFindings(query: string): Findings[]
    getConflicts(): Conflict[]
    getProgress(): Progress
  }

  // 寫入操作（需要協調）
  write: {
    submitFindings(finding: Finding): Promise<void>
    updateProgress(agentId: string, progress: number): Promise<void>
    recordConflict(conflict: Conflict): Promise<void>
  }

  // 衝突解決
  conflictResolution: {
    detectConflicts(): Promise<Conflict[]>
    resolveConflict(conflictId: string, resolution: Resolution): Promise<void>
  }
}
```

### 2.4 衝突解決機制

```typescript
// 衝突類型定義
enum ConflictType {
  CONTRADICTION = 'contradiction',  // 矛盾（A 說對，B 說錯）
  OVERLAP = 'overlap',              // 重疊（兩者研究同一點）
  GAP = 'gap',                      // 缺口（兩者之間有遺漏）
  INCONSISTENCY = 'inconsistency'   // 不一致（術語、定義不同）
}

// 衝突解決策略
interface ConflictResolver {
  // 自動解決策略
  autoResolve: {
    // 重疊 → 合併
    mergeOverlapping(findingA: Finding, findingB: Finding): Finding

    // 缺口 → 標記待補充
    markGap(findingA: Finding, findingB: Finding): GapMarker

    // 術語不一致 → 標準化
    normalizeTerminology(findings: Finding[]): Finding[]
  }

  // 需要 Agent 介入
  requireAgentIntervention: {
    // 矛盾 → 多模型驗證
    resolveContradiction(conflict: Conflict): Promise<Resolution>

    // 複雜不一致 → 深度分析
    analyzeInconsistency(conflict: Conflict): Promise<Analysis>
  }
}
```

---

## 三、整合架構設計

### 3.1 匯總 Agent 的角色定位

匯總 Agent 不應只是「拼接」結果，而是智能融合的協調者。

```
┌─────────────────────────────────────────────────────────────────┐
│                 匯總 Agent 的三重角色                            │
│                                                                 │
│  角色 1: 交叉驗證者 (Cross-Validator)                           │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ • 識別不同視角的共同發現 → 提升置信度                 │      │
│  │ • 偵測矛盾 → 觸發深入調查                            │      │
│  │ • 發現遺漏 → 補充研究                                │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
│  角色 2: 知識融合者 (Knowledge Synthesizer)                     │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ • 建立跨視角的連結                                    │      │
│  │ • 識別整體模式和趨勢                                  │      │
│  │ • 提煉核心洞察                                        │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
│  角色 3: 報告生成者 (Report Generator)                          │
│  ┌──────────────────────────────────────────────────────┐      │
│  │ • 結構化輸出                                          │      │
│  │ • 建立清晰的敘事邏輯                                  │      │
│  │ • 標註置信度和侷限性                                  │      │
│  └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 知識融合策略

**三階段融合流程**:

```
階段 1: 結構化整理
─────────────────
輸入: 各 Agent 的原始研究結果

操作:
1. 提取結構化信息
   - 關鍵論點
   - 支持證據
   - 引用來源
   - 置信度

2. 建立知識圖譜
   Node: 論點
   Edge: 關係（支持、反對、補充）

輸出: 結構化知識圖譜

階段 2: 智能融合
─────────────────
輸入: 知識圖譜

操作:
1. 置信度傳播
   - 多個 Agent 支持 → 提升置信度
   - 有反對意見 → 標記爭議點

2. 矛盾解決
   - 調用 PAL consensus 進行多模型驗證
   - 補充研究解決爭議

3. 遺漏檢測
   - 識別知識圖譜中的斷點
   - 分配補充研究任務

輸出: 融合後的知識圖譜

階段 3: 報告生成
─────────────────
輸入: 融合後的知識圖譜

操作:
1. 敘事結構設計
   - 根據知識圖譜的拓撲結構
   - 建立邏輯清晰的章節

2. 內容生成
   - 綜合各 Agent 的表述
   - 保持術語一致性
   - 標註來源和置信度

3. 品質檢查
   - 完整性檢查
   - 邏輯一致性驗證
   - 可讀性優化

輸出: 最終研究報告
```

### 3.3 輸出格式標準化

```markdown
# 研究報告標準格式

## 元數據
- 研究主題: [主題]
- 參與 Agent: [Agent A (視角1), Agent B (視角2), ...]
- 研究時間: [開始時間 - 結束時間]
- 總研究時長: [X 小時]
- 融合置信度: [0.0-1.0]

## 執行摘要
[高層次總結，200-300 字]

## 核心發現
[按重要性排序的關鍵發現，每項標註]
- 發現內容
- 支持證據
- 置信度: ★★★★☆ (4/5)
- 來源: Agent A, Agent C

## 詳細分析
### [子主題 1]
#### Agent A 視角（架構設計）
[內容]

#### Agent B 視角（狀態管理）
[內容]

#### 融合洞察
[交叉驗證後的綜合分析]

### [子主題 2]
...

## 爭議點與侷限性
[標註未解決的矛盾、低置信度的論點]

## 推薦方案
[基於研究的具體建議]

## 參考資源
[所有引用的來源]

## 附錄
### A. Agent 獨立報告
- [Agent A 完整報告連結]
- [Agent B 完整報告連結]
...

### B. 知識圖譜
[視覺化的論點關係圖]
```

---

## 四、參考現有模式分析

### 4.1 Claude Code Task 工具

**核心機制**:
```typescript
// Task 並行模式
TaskCreate()      // 建立任務
TaskUpdate()      // 更新狀態
TaskList()        // 查看全局狀態

// 適用場景
- 單一 AI Agent 管理多個任務
- 任務狀態追蹤
- 進度可視化
```

**可借鏡之處**:
- ✅ 任務狀態機設計（pending → in_progress → completed）
- ✅ 依賴關係管理（blocks, blockedBy）
- ✅ 中央化狀態追蹤

**侷限性**:
- ❌ 設計給單一 Agent 使用，非多 Agent
- ❌ 無知識融合機制
- ❌ 無衝突檢測

### 4.2 Claude Plan 並行執行

**核心機制**（來自 `skills/claude-plan/06-parallel/`）:
```typescript
// Session 並行模式
session_loop:
  while task = claim_task():
    execute_pdca(task)
    on_complete:
      - release_lock(task)
      - update_status(task)

// 關鍵特性
- 任務鎖機制（避免重複認領）
- 自動任務分配
- 衝突檢測（檔案衝突、依賴衝突）
```

**可借鏡之處**:
- ✅ 任務鎖機制（避免 Agent 搶佔）
- ✅ 自動負載均衡
- ✅ 檔案衝突處理策略

**差異點**:
- 研究任務的「衝突」是觀點差異，非檔案衝突
- 需要知識融合，而非簡單合併

### 4.3 PAL MCP 多模型協作

**核心機制**:
```typescript
// consensus 工具
mcp__pal__consensus({
  models: [
    {model: "gpt-5.2", stance: "for"},
    {model: "gemini-2.5-pro", stance: "against"}
  ]
})

// thinkdeep 工具
mcp__pal__thinkdeep({
  step: "分析問題",
  findings: "發現內容"
})
```

**可借鏡之處**:
- ✅ 多模型驗證機制
- ✅ stance（立場）設計，可用於分配不同視角
- ✅ 階段式思考（step_number, total_steps）

**如何應用**:
```typescript
// 研究 Agent = PAL 工具 + 視角約束
ResearchAgent {
  perspective: "architecture",
  tool: "thinkdeep",
  constraints: "專注於架構層面的設計"
}

// 衝突解決 = consensus 工具
ConflictResolver {
  tool: "consensus",
  stance_a: 基於 Agent A 的發現,
  stance_b: 基於 Agent B 的發現
}
```

### 4.4 MapReduce 思維

**經典 MapReduce**:
```
Map:    [Data] → Mapper → [(Key, Value)]
Reduce: [(Key, Value)] → Reducer → [Result]
```

**應用到研究場景**:
```
Map:    [研究主題] → ResearchAgent → [(視角, 發現)]
Reduce: [(視角, 發現)] → AggregatorAgent → [整合報告]
```

**關鍵適配**:
- Map 階段：並行研究（不同視角）
- Shuffle 階段：知識庫整理（檢測衝突、遺漏）
- Reduce 階段：串行融合（交叉驗證 → 矛盾解決 → 報告生成）

---

## 五、推薦架構方案

### 5.1 整體架構圖

```
┌─────────────────────────────────────────────────────────────────┐
│       多 Agent 協作研究框架 - 混合架構（推薦方案）               │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Coordinator (協調器)                                     │  │
│  │  - 研究主題分解                                           │  │
│  │  - 任務分配與調度                                         │  │
│  │  - 進度監控                                               │  │
│  │  - 階段切換控制                                           │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │                                         │
│  ═════════════════════╪═════════════════════════════════════    │
│  MAP 階段（並行）      │                                         │
│  ═════════════════════╪═════════════════════════════════════    │
│                       │                                         │
│         ┌─────────────┼─────────────┐                           │
│         ↓             ↓             ↓                           │
│    ┌─────────┐   ┌─────────┐   ┌─────────┐                     │
│    │ Agent A │   │ Agent B │   │ Agent C │                     │
│    │ (架構)  │   │ (狀態)  │   │ (整合)  │                     │
│    │         │   │         │   │         │                     │
│    │ Tool:   │   │ Tool:   │   │ Tool:   │                     │
│    │thinkdeep│   │thinkdeep│   │thinkdeep│                     │
│    └────┬────┘   └────┬────┘   └────┬────┘                     │
│         │             │             │                           │
│         └─────────────┼─────────────┘                           │
│                       ↓                                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Shared Knowledge Repository (SQLite)                     │  │
│  │                                                            │  │
│  │  ┌───────────────┐  ┌──────────────┐  ┌───────────────┐ │  │
│  │  │ Findings      │  │ Conflicts    │  │ Progress      │ │  │
│  │  │ Table         │  │ Table        │  │ Tracking      │ │  │
│  │  └───────────────┘  └──────────────┘  └───────────────┘ │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │ FTS5 Full-Text Search                            │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                       │                                         │
│  ═════════════════════╪═════════════════════════════════════    │
│  REDUCE 階段（串行）   │                                         │
│  ═════════════════════╪═════════════════════════════════════    │
│                       ↓                                         │
│              ┌──────────────────┐                               │
│              │ Fusion Agent 1   │                               │
│              │ (交叉驗證)       │                               │
│              │ Tool: analyze    │                               │
│              └────────┬─────────┘                               │
│                       ↓                                         │
│              ┌──────────────────┐                               │
│              │ Fusion Agent 2   │                               │
│              │ (矛盾解決)       │                               │
│              │ Tool: consensus  │                               │
│              └────────┬─────────┘                               │
│                       ↓                                         │
│              ┌──────────────────┐                               │
│              │ Fusion Agent 3   │                               │
│              │ (報告生成)       │                               │
│              │ Tool: chat       │                               │
│              └────────┬─────────┘                               │
│                       ↓                                         │
│              ┌──────────────────┐                               │
│              │  最終研究報告     │                               │
│              └──────────────────┘                               │
└─────────────────────────────────────────────────────────────────┘
```

### 5.2 核心組件設計

#### 組件 1: Coordinator（協調器）

```typescript
interface Coordinator {
  // 初始化
  initialize(topic: string): SessionContext

  // Map 階段
  mapPhase: {
    decomposeResearch(topic: string): ResearchTasks[]
    assignTasks(agents: Agent[], tasks: ResearchTasks[]): void
    monitorMapProgress(): MapProgress
    waitForMapCompletion(): Promise<void>
  }

  // Reduce 階段
  reducePhase: {
    triggerReduction(): void
    stage1_crossCheck(): Promise<CrossCheckResult>
    stage2_resolveConflicts(result: CrossCheckResult): Promise<ResolvedResult>
    stage3_generateReport(result: ResolvedResult): Promise<FinalReport>
  }

  // 工具
  utilities: {
    detectPhaseCompletion(): boolean
    handleAgentFailure(agentId: string): void
    saveCheckpoint(): void
    resume(checkpointId: string): void
  }
}
```

#### 組件 2: Research Agent

```typescript
interface ResearchAgent {
  id: string
  perspective: string  // 'architecture', 'state-management', etc.

  // 執行研究
  research(task: ResearchTask): Promise<Findings>

  // 內部使用 PAL thinkdeep
  internalTool: {
    tool: "thinkdeep" | "analyze",
    model: string,
    thinkingMode: "high" | "max"
  }

  // 提交結果
  submit(findings: Findings): Promise<void>
}
```

#### 組件 3: Knowledge Repository

```typescript
interface KnowledgeRepository {
  // 寫入
  write: {
    storeFindings(finding: Finding): Promise<void>
    recordConflict(conflict: Conflict): Promise<void>
    updateProgress(agentId: string, progress: Progress): Promise<void>
  }

  // 查詢
  read: {
    getAllFindings(): Promise<Finding[]>
    getFindingsByAgent(agentId: string): Promise<Finding[]>
    searchFindings(query: string): Promise<Finding[]>
    getConflicts(): Promise<Conflict[]>
  }

  // 分析
  analyze: {
    detectConflicts(): Promise<Conflict[]>
    findGaps(): Promise<Gap[]>
    calculateConfidence(findingId: string): number
  }
}
```

#### 組件 4: Fusion Agent

```typescript
interface FusionAgent {
  // Stage 1: 交叉驗證
  crossCheck(findings: Finding[]): Promise<CrossCheckResult>

  // Stage 2: 矛盾解決
  resolveConflicts(conflicts: Conflict[]): Promise<Resolution[]>

  // Stage 3: 報告生成
  generateReport(
    findings: Finding[],
    resolutions: Resolution[]
  ): Promise<Report>

  // 使用的工具
  tools: {
    crossCheck: "analyze",
    resolveConflicts: "consensus",
    generateReport: "chat"
  }
}
```

### 5.3 與 evolve skill 整合

```
┌─────────────────────────────────────────────────────────────────┐
│           與 evolve skill 的整合點                               │
│                                                                 │
│  CP0: North Star                                                │
│  ├─ 定義研究目標                                                │
│  └─ 建立研究計畫                                                │
│                                                                 │
│  CP1: Memory Search                                             │
│  ├─ 搜尋過去的研究經驗                                          │
│  ├─ 複用成功的研究模式                                          │
│  └─ 避免重複研究                                                │
│                                                                 │
│  CP2: Verification                                              │
│  ├─ Map 階段：每個 Agent 完成後驗證                             │
│  └─ Reduce 階段：最終報告生成後驗證                             │
│                                                                 │
│  CP3: Milestone Confirm                                         │
│  ├─ Map 完成確認                                                │
│  └─ Reduce 完成確認                                             │
│                                                                 │
│  CP3.5: Memory Sync                                             │
│  ├─ 更新 research memory                                        │
│  └─ 記錄成功的協作模式                                          │
│                                                                 │
│  CP4: Emergence Check                                           │
│  └─ 識別可重用的研究 Skill                                      │
│                                                                 │
│  CP5: Failure Postmortem (如果失敗)                             │
│  ├─ 記錄失敗原因                                                │
│  └─ 改進協作流程                                                │
│                                                                 │
│  Memory System Integration                                      │
│  ├─ 使用 SQLite Memory MCP                                      │
│  ├─ memory_write() 記錄研究發現                                 │
│  ├─ memory_search() 搜尋相關知識                                │
│  └─ context_set() 跨 Agent 共享狀態                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 六、架構優缺點比較

### 6.1 模式對比矩陣

| 維度 | 並行模式 | 串行模式 | 混合模式（推薦）|
|------|---------|---------|----------------|
| **執行速度** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **知識深度** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **容錯能力** | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **實作複雜度** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| **資源利用率** | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐⭐ |
| **融合品質** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **可擴展性** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |

### 6.2 混合模式的優勢

**相對並行模式**:
- ✅ 知識融合品質高（有專門的 Reduce 階段）
- ✅ 矛盾和遺漏能被檢測和解決
- ✅ 最終報告邏輯清晰、結構化

**相對串行模式**:
- ✅ 執行速度快（Map 階段並行）
- ✅ 容錯能力強（一個 Agent 失敗不阻塞其他）
- ✅ 資源利用率高（可並行利用多個模型）

**獨特優勢**:
- ✅ 兼顧速度和深度
- ✅ 適合多視角研究場景
- ✅ 可應對不同複雜度的任務

### 6.3 潛在挑戰與對策

| 挑戰 | 影響 | 對策 |
|------|------|------|
| **Reduce 階段成為瓶頸** | 串行處理慢 | • 優化融合算法<br>• 使用更快的模型<br>• 分階段並行（交叉驗證可部分並行）|
| **知識庫衝突管理複雜** | 實作難度高 | • 使用成熟的 SQLite Schema<br>• 複用 claude-plan 的衝突處理邏輯<br>• 自動化衝突偵測 |
| **Agent 間協調開銷** | 增加延遲 | • 使用輕量級通訊（SQLite）<br>• 減少同步頻率<br>• 批次處理狀態更新 |
| **融合邏輯的品質** | 報告質量 | • 使用高品質模型（gemini-2.5-pro, gpt-5.2）<br>• 多模型驗證<br>• 人工審查機制 |

---

## 七、實作路徑建議

### 7.1 MVP 版本（最小可行產品）

**目標**: 驗證混合架構的可行性

**範圍**:
- 2-3 個 Research Agent（固定視角）
- 簡化的知識庫（僅 Findings 表）
- 單一 Fusion Agent（簡單合併）

**技術選型**:
```yaml
Coordinator: 簡單的 Bash 腳本
Research Agents: 調用 PAL thinkdeep
Knowledge Repository: SQLite 單表
Fusion Agent: 調用 PAL chat
```

**驗證指標**:
- ✅ Agent 能並行執行
- ✅ 結果能正確收集
- ✅ 報告基本可讀

### 7.2 完整版本

**增強**:
- 動態視角分配（根據主題自動決定需要哪些視角）
- 完整的知識庫 Schema（Conflicts, Progress 表）
- 智能 Fusion Agent（交叉驗證、矛盾解決、報告生成）
- 與 evolve skill 深度整合（Checkpoints, Memory）

**技術選型**:
```yaml
Coordinator: TypeScript + 狀態機
Research Agents: PAL tools (thinkdeep, analyze)
Knowledge Repository: SQLite + FTS5
Fusion Agents: PAL tools (analyze, consensus, chat)
Integration: evolve skill Checkpoints
```

### 7.3 進階功能

**可選增強**:
- Agent 自適應（根據過往表現動態調整視角）
- 增量研究（基於已有研究繼續深入）
- 人機協作（人類專家可介入矛盾解決）
- 研究模板（預定義常見研究模式）

---

## 八、與其他架構模式的對比

### 8.1 微服務架構

**相似之處**:
- 分散式組件（Agent = Service）
- 中央協調（Coordinator = API Gateway）
- 狀態管理（Knowledge Repository = Database）

**差異**:
- 微服務：長期運行、RESTful API
- 本架構：任務導向、協作式、有明確終止條件

### 8.2 Actor 模型

**相似之處**:
- 獨立實體（Agent = Actor）
- 消息傳遞（Findings = Messages）
- 無共享狀態（部分）

**差異**:
- Actor：完全非同步、無中央協調
- 本架構：有協調器、有共享知識庫

### 8.3 Blackboard 系統

**相似之處**:
- 共享知識空間（Knowledge Repository = Blackboard）
- 多個專家系統（Agent = Expert）
- 協作式問題解決

**差異**:
- Blackboard：opportunistic（機會主義式觸發）
- 本架構：structured（結構化 Map-Reduce）

---

## 九、總結與建議

### 9.1 核心結論

1. **混合架構最適合研究場景**
   - Map-Reduce 思維：並行研究 + 串行整合
   - 兼顧速度（並行）和品質（深度融合）

2. **狀態管理應分層設計**
   - Agent 私有狀態（In-Memory）
   - 協作共享狀態（SQLite Context）
   - 持久知識庫（SQLite Memory + Filesystem）

3. **匯總 Agent 是智能融合者，非簡單拼接**
   - 交叉驗證 → 矛盾解決 → 報告生成
   - 使用 PAL tools（analyze, consensus, chat）

4. **可充分複用 evolve skill 現有機制**
   - Checkpoints（CP1, CP3.5）
   - Memory System（SQLite MCP）
   - PDCA 循環

### 9.2 推薦實作順序

```
Phase 1: MVP（1-2 週）
├─ 實作 Coordinator 基礎邏輯
├─ 2-3 個固定視角 Research Agent
├─ 簡化的 SQLite Knowledge Repository
└─ 單一 Fusion Agent（簡單合併）

Phase 2: 完整版（2-3 週）
├─ 完整 Knowledge Repository Schema
├─ 智能 Fusion Agent（三階段）
├─ 衝突檢測與解決
└─ 與 evolve skill 整合

Phase 3: 進階功能（按需）
├─ 動態視角分配
├─ 增量研究
├─ 人機協作
└─ 研究模板
```

### 9.3 關鍵成功因素

| 因素 | 重要性 | 建議 |
|------|--------|------|
| **知識融合品質** | ⭐⭐⭐⭐⭐ | 使用高品質模型，多模型驗證 |
| **衝突解決機制** | ⭐⭐⭐⭐ | 自動化檢測 + Agent 智能解決 |
| **狀態管理穩定性** | ⭐⭐⭐⭐ | 使用 SQLite 確保 ACID |
| **Agent 間協調效率** | ⭐⭐⭐ | 減少通訊頻率，批次更新 |
| **可觀測性** | ⭐⭐⭐ | 完整的日誌和進度追蹤 |

### 9.4 未來研究方向

1. **自適應視角分配**
   - 根據研究主題自動決定需要哪些視角
   - Agent 根據過往表現動態調整策略

2. **增量研究模式**
   - 基於已有研究繼續深入
   - 支援研究的版本管理

3. **人機協作介面**
   - 人類專家可介入關鍵決策
   - 矛盾解決時的人工審查

4. **跨語言和跨領域擴展**
   - 支援多語言研究協作
   - 不同專業領域的 Agent 協作

---

## 參考資源

### 現有實作參考
- Claude Plan 並行執行機制: `/skills/claude-plan/06-parallel/`
- PAL MCP 多模型協作: `/skills/05-integration/_base/pal-tools.md`
- SQLite Memory System: `.claude/memory/north-star/sqlite-memory-system.md`
- Task 管理模式: Claude Code 內建 TaskCreate/TaskUpdate 工具

### 學術和工業實踐
- MapReduce: Dean & Ghemawat, 2004
- Actor Model: Hewitt, 1973
- Blackboard Systems: Erman et al., 1980
- Multi-Agent Systems: Wooldridge, 2009
- Distributed Consensus: Lamport, 1998 (Paxos)

### 相關 MCP 設計模式
- Code Execution Pattern (Anthropic, 2025)
- Workflow-Based Pattern (Vercel)
- Progressive Discovery Pattern (Strata)

---

## 關鍵學習

1. **混合架構 = Map-Reduce 思維應用**
   - 並行研究（Map）+ 串行整合（Reduce）
   - 兼顧速度和品質

2. **匯總 Agent 需要智能融合，非簡單拼接**
   - 交叉驗證 → 提升置信度
   - 矛盾解決 → 多模型驗證
   - 報告生成 → 結構化敘事

3. **狀態管理分層是關鍵**
   - Agent 私有（In-Memory）
   - 協作共享（SQLite Context）
   - 持久知識（SQLite Memory）

4. **可充分複用 evolve skill 生態系**
   - Checkpoints（CP1, CP3.5）
   - Memory System（SQLite MCP）
   - PAL Tools（thinkdeep, consensus, analyze）

5. **MVP 優先，漸進增強**
   - 先驗證核心架構可行性
   - 再逐步增加複雜功能
