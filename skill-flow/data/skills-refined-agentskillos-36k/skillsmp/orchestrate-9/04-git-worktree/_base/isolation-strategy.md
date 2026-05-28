# Isolation Strategy

> Worktree 模式下的隔離策略與狀態管理

## 概述

Worktree 模式實現兩層隔離：
1. **程式碼隔離**：feature 分支在獨立目錄中
2. **狀態隔離**：Memory 保持單一來源（main 目錄）

## 隔離架構

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          隔離架構                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────────────────┐     ┌─────────────────────────┐            │
│  │      Main Directory      │     │       Worktree          │            │
│  │      /project/           │     │   /project/.worktrees/  │            │
│  │                          │     │     {feature-id}/       │            │
│  ├─────────────────────────┤     ├─────────────────────────┤            │
│  │                          │     │                          │            │
│  │  ✅ Memory               │     │  ✅ 程式碼               │            │
│  │     .claude/memory/      │     │     src/                 │            │
│  │                          │     │     tests/               │            │
│  │  ✅ 工作流狀態            │     │     package.json         │            │
│  │     .claude/memory/      │     │                          │            │
│  │     workflows/           │     │  ✅ Git Branch           │            │
│  │                          │     │     feature/{id}         │            │
│  │  ❌ 程式碼變更            │     │                          │            │
│  │     (保持穩定)           │     │  ❌ Memory               │            │
│  │                          │     │     (不存在)             │            │
│  │                          │     │                          │            │
│  └─────────────────────────┘     └─────────────────────────┘            │
│                                                                          │
│  ───────────────────────────────────────────────────────────            │
│                        共享的 Git 物件庫                                 │
│                     /project/.git/objects/                              │
│  ───────────────────────────────────────────────────────────            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 程式碼隔離

### 分支策略

```yaml
branch_strategy:
  main:
    purpose: "穩定分支，始終可部署"
    protected: true
    direct_commits: false

  feature/{id}:
    purpose: "功能開發分支"
    created_from: main
    merge_target: main
    lifecycle:
      - created at CP0.5
      - worked on during IMPLEMENT/REVIEW/VERIFY
      - merged at SHIP IT
      - deleted after merge
```

### 目錄結構

```
/project/                        # Main directory
├── .git/                        # 共享的 Git 倉庫
│   ├── objects/                 # 所有物件（共享）
│   └── worktrees/               # Worktree 元數據
│       └── {feature-id}/
├── .worktrees/                  # Worktree 目錄
│   └── {feature-id}/            # 獨立的工作目錄
│       ├── src/
│       ├── tests/
│       └── package.json
├── .claude/
│   └── memory/                  # Memory（僅在 main）
└── src/                         # Main 的程式碼（穩定）
```

### 隔離的好處

```yaml
code_isolation_benefits:
  stability:
    - main 始終可部署
    - 失敗的 feature 不影響 main
    - 多個 feature 可並行開發

  clean_rollback:
    - 失敗時只需刪除 worktree
    - 無需 git revert
    - 無污染歷史

  clear_diff:
    - git diff main..feature/{id} 清晰顯示變更
    - 易於 code review
    - 易於理解影響範圍
```

## Memory 隔離

### 單一來源原則

```yaml
memory_single_source:
  principle: "所有 Memory 都存儲在 main 目錄中"

  rationale:
    - 避免 worktree 間的 Memory 衝突
    - 簡化 Memory 同步邏輯
    - 確保 Memory 不會隨 worktree 刪除而遺失

  implementation:
    memory_base: "{main_directory}/.claude/memory"
    never: "{worktree_directory}/.claude/memory"
```

### 路徑解析

```yaml
path_resolution:
  in_worktree:
    code_operations:
      base: "{worktree_directory}"
      example: ".worktrees/user-auth/src/auth/login.ts"

    memory_operations:
      base: "{main_directory}/.claude/memory"
      example: "/project/.claude/memory/implementations/user-auth/"

  detection:
    method: "git rev-parse --git-common-dir"
    if_in_worktree: resolve to main directory for memory
```

詳見：[../../../../shared/isolation/path-resolution.md](../../../../shared/isolation/path-resolution.md)

## 狀態追蹤

### workflow.yaml 結構

```yaml
workflow:
  id: "user-auth"
  created: "2025-01-24T10:00:00Z"
  status: "in_progress"
  current_stage: "IMPLEMENT"

  # 路徑記錄
  paths:
    main_directory: "/project"
    memory_base: "/project/.claude/memory"

  # Worktree 狀態
  worktree:
    enabled: true
    directory: "/project/.worktrees/user-auth"
    branch: "feature/user-auth"
    state: "active"
    created_at: "2025-01-24T10:30:00Z"

  # 階段狀態
  stages:
    plan:
      status: "completed"
      output: "plans/user-auth/"

    implement:
      status: "in_progress"
      iteration: 2
      output: "implementations/user-auth/"
      execution_context:
        type: "worktree"
        path: ".worktrees/user-auth"
        commits:
          - hash: "abc123"
            message: "feat: add login endpoint"
          - hash: "def456"
            message: "fix: input validation"
```

### 狀態同步

```yaml
state_synchronization:
  write_location: "{main_directory}/.claude/memory/workflows/{id}/"

  sync_points:
    - stage_start
    - stage_complete
    - iteration_increment
    - rollback
    - workflow_complete

  never_in_worktree: true
```

## 並行 Worktree

### 多功能並行開發

```yaml
parallel_worktrees:
  scenario: "同時開發多個 feature"

  structure:
    /project/
    ├── .worktrees/
    │   ├── feature-a/     # Feature A
    │   ├── feature-b/     # Feature B
    │   └── feature-c/     # Feature C
    └── .claude/memory/
        ├── workflows/
        │   ├── feature-a/
        │   ├── feature-b/
        │   └── feature-c/
        └── implementations/
            ├── feature-a/
            ├── feature-b/
            └── feature-c/

  constraints:
    - 每個 feature 獨立的 worktree
    - 每個 feature 獨立的 workflow.yaml
    - Memory 按 feature-id 分隔
    - 無交叉污染
```

### 衝突避免

```yaml
conflict_prevention:
  naming:
    - unique feature-id
    - timestamp suffix if needed

  resources:
    - 獨立的 node_modules（每個 worktree）
    - 獨立的 build artifacts
    - 共享的 Git objects

  merge_order:
    - 先完成的先合併
    - 後合併的需要 rebase 解決衝突
```

## 安全機制

### 防止誤操作

```yaml
safety_mechanisms:
  prevent_memory_in_worktree:
    check: "path resolution before write"
    action: "redirect to main directory"

  prevent_nested_worktree:
    check: "is_in_worktree() before create"
    action: "abort with error"

  prevent_main_pollution:
    check: "current branch != main in worktree"
    action: "abort if trying to modify main"

  prevent_orphan_worktree:
    check: "workflow.yaml exists and valid"
    action: "warn and offer cleanup"
```

### 鎖定機制

```yaml
worktree_locking:
  purpose: "防止意外刪除重要的 worktree"

  usage:
    lock: "git worktree lock .worktrees/{id}"
    unlock: "git worktree unlock .worktrees/{id}"

  integration:
    - ABORT 選項之一
    - 重要功能可主動鎖定
    - 清理時跳過已鎖定的 worktree
```

## 邊界情況

### 跨 Worktree 引用

```yaml
cross_worktree_reference:
  scenario: "Feature B 需要參考 Feature A 的設計"

  solution:
    - 讀取 Memory（在 main）：允許
    - 讀取程式碼（在其他 worktree）：不建議
    - 建議：先合併 Feature A，再開發 Feature B

  rationale: |
    跨 worktree 讀取程式碼可能導致：
    - 依賴未完成的功能
    - 合併順序問題
    - 難以追蹤的依賴關係
```

### Worktree 損壞

```yaml
worktree_corruption:
  detection:
    - git worktree list 顯示異常
    - 目錄存在但 Git 不識別
    - workflow.yaml 與實際狀態不符

  recovery:
    1. "嘗試 git worktree repair"
    2. "如果失敗，保存 patch"
    3. "刪除並重建 worktree"
    4. "應用 patch"
```

## 配置選項

```yaml
isolation_config:
  # 程式碼隔離
  code_isolation:
    enabled: true
    directory_prefix: ".worktrees"
    branch_prefix: "feature"

  # Memory 隔離
  memory_isolation:
    single_source: true
    base_path: ".claude/memory"

  # 並行限制
  parallel_limit:
    max_worktrees: 5
    warn_at: 3

  # 安全選項
  safety:
    prevent_nested: true
    auto_lock_important: false
    cleanup_orphans_days: 30
```

## 相關資源

- [Lifecycle](./lifecycle.md)
- [Merge Conflict](./merge-conflict.md)
- [Path Resolution](../../../../shared/isolation/path-resolution.md)
