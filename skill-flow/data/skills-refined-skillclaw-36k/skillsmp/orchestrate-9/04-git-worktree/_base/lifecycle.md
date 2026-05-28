# Worktree Lifecycle

> Worktree 在工作流中的完整生命週期管理

## 概述

Worktree 從 PLAN 階段完成後創建，到 VERIFY 階段完成後清理（或保留），形成完整的生命週期。

## 生命週期狀態圖

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Worktree Lifecycle                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│                    ┌─────────────┐                                      │
│                    │   (none)    │                                      │
│                    │   未創建    │                                      │
│                    └──────┬──────┘                                      │
│                           │ PLAN 完成                                   │
│                           ↓                                              │
│                    ┌─────────────┐                                      │
│              ┌────→│   active    │←───────────┐                         │
│              │     │   活躍中    │            │                         │
│              │     └──────┬──────┘            │                         │
│              │            │                   │                         │
│              │     ┌──────┴──────┐            │                         │
│              │     ↓             ↓            │                         │
│              │  SHIP IT      BLOCKED          │                         │
│              │     │             │            │                         │
│              │     ↓             ↓            │                         │
│              │  ┌──────┐    ┌─────────┐       │                         │
│              │  │merged│    │ blocked │───────┘                         │
│              │  │已合併│    │  阻擋   │  (resume)                        │
│              │  └──────┘    └────┬────┘                                 │
│              │                   │ ABORT                                │
│              │                   ↓                                      │
│              │             ┌─────────────┐                              │
│              │             │    選項     │                              │
│              │             └──────┬──────┘                              │
│              │          ┌─────────┼─────────┐                           │
│              │          ↓         ↓         ↓                           │
│              │    ┌─────────┐ ┌───────┐ ┌───────┐                       │
│              │    │abandoned│ │locked │ │ patch │                       │
│              │    │  放棄   │ │ 鎖定  │ │ 保留  │                       │
│              │    └─────────┘ └───┬───┘ └───────┘                       │
│              │                    │                                     │
│              └────────────────────┘                                     │
│                     (unlock)                                            │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 階段與 Worktree 的關係

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    工作流階段與 Worktree                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  RESEARCH     PLAN          IMPLEMENT    REVIEW       VERIFY            │
│     │          │                │           │            │              │
│     ↓          ↓                ↓           ↓            ↓              │
│  ┌──────┐  ┌──────┐         ┌──────┐    ┌──────┐     ┌──────┐          │
│  │ main │  │ main │         │ wt   │    │ wt   │     │ wt   │          │
│  │      │  │      │         │      │    │      │     │      │          │
│  └──────┘  └──┬───┘         └──────┘    └──────┘     └──┬───┘          │
│               │                                         │               │
│               │ ← CP0.5                      CP6.5 →   │               │
│               │    創建 worktree             處理完成   │               │
│               ↓                                         ↓               │
│          ┌─────────┐                              ┌─────────┐          │
│          │ worktree│ ─────────────────────────→  │ cleanup │          │
│          │ 創建    │    程式碼在 worktree 中      │ /merge  │          │
│          └─────────┘    Memory 在 main 中         └─────────┘          │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 創建（CP0.5）

### 觸發時機

```yaml
worktree_creation:
  trigger:
    after: "PLAN 階段完成"
    before: "IMPLEMENT 階段開始"

  condition:
    - plan_completed: true
    - worktree_enabled: true  # 非 --no-worktree
    - not_already_in_worktree: true
```

### 創建步驟

```yaml
creation_steps:
  1. validate_preconditions:
      - not in existing worktree
      - plan artifacts exist
      - no uncommitted changes on main

  2. prepare_directory:
      - select worktree directory
      - ensure .gitignore includes it

  3. create_worktree:
      - git worktree add .worktrees/{id} -b feature/{id}

  4. setup_environment:
      - detect project type
      - run setup commands

  5. verify_baseline:
      - run tests
      - ensure baseline passes

  6. update_workflow:
      - set worktree.state = "active"
      - record paths
```

詳見：[../../shared/isolation/worktree-setup.md](../../../../shared/isolation/worktree-setup.md)

## 活躍使用

### IMPLEMENT 階段

```yaml
implement_in_worktree:
  working_directory: ".worktrees/{id}"

  operations:
    code_changes:
      location: worktree
      files: "src/**, tests/**, etc."

    memory_writes:
      location: main
      path: "{main}/.claude/memory/implementations/{id}/"

    git_commits:
      branch: "feature/{id}"
      location: worktree
```

### REVIEW 階段

```yaml
review_in_worktree:
  working_directory: ".worktrees/{id}"

  operations:
    code_review:
      source: "git diff main..HEAD"
      location: worktree

    memory_writes:
      location: main
      path: "{main}/.claude/memory/reviews/{id}/"
```

### VERIFY 階段

```yaml
verify_in_worktree:
  working_directory: ".worktrees/{id}"

  operations:
    test_execution:
      location: worktree
      command: "npm test"

    memory_writes:
      location: main
      path: "{main}/.claude/memory/verifications/{id}/"

    final_decision:
      output: "release-decision.md"
```

## 完成處理（CP6.5）

### 決策樹

```yaml
completion_decision:
  input: "release-decision.md"

  if_ship_it:
    action: merge_and_cleanup
    steps:
      - push branch
      - create PR (if not --auto-merge)
      - merge PR
      - delete worktree
      - delete branch

  if_blocked:
    action: preserve_for_iteration
    steps:
      - keep worktree
      - increment iteration
      - return to IMPLEMENT

  if_abort:
    action: prompt_user
    options:
      - preserve patch
      - delete all
      - lock worktree
```

詳見：[../../shared/isolation/worktree-completion.md](../../../../shared/isolation/worktree-completion.md)

## 迭代循環

### 回退時的 Worktree 處理

```yaml
rollback_worktree:
  scenario: "REVIEW 或 VERIFY 失敗"

  action:
    - keep worktree intact
    - stay in worktree directory
    - increment workflow.iteration
    - continue fixing in same worktree

  not_action:
    - do NOT delete worktree
    - do NOT create new worktree
    - do NOT switch to main

  rationale: |
    在同一個 worktree 中繼續迭代可以：
    - 保留所有工作進度
    - 避免重新 setup
    - 保持 git history 清晰
```

### 多次迭代

```
迭代 1: IMPLEMENT → REVIEW (BLOCKER)
             ↓
迭代 2: IMPLEMENT → REVIEW → VERIFY (BLOCKED)
             ↓
迭代 3: IMPLEMENT → REVIEW → VERIFY (SHIP IT)
             ↓
        Merge + Cleanup

所有迭代都在同一個 worktree 中完成
```

## 恢復機制

### 從中斷恢復

```yaml
resume_workflow:
  command: "/multi-orchestrate --resume {id}"

  detection:
    1. load workflow.yaml
    2. check worktree.state
    3. verify worktree exists

  actions:
    if_worktree_exists:
      - cd to worktree
      - continue from current_stage

    if_worktree_missing:
      - prompt: recreate or start fresh
      - if recreate: create new worktree from same branch
      - if fresh: start from PLAN
```

### 處理孤立 Worktree

```yaml
orphan_worktree:
  definition: "worktree 存在但 workflow.yaml 遺失或損壞"

  detection:
    - git worktree list
    - cross-reference with workflows/

  handling:
    options:
      1. "嘗試恢復 workflow.yaml"
      2. "手動清理 worktree"
      3. "保留 worktree 作為備份"
```

## Checkpoint 整合

| Checkpoint | 時機 | Worktree 操作 |
|------------|------|---------------|
| CP0.5 | PLAN 完成後 | 創建 worktree |
| CP2 | IMPLEMENT 中 | 在 worktree 中 build + test |
| CP6 | VERIFY 完成 | 準備完成處理 |
| CP6.5 | VERIFY 後 | 合併/保留/清理 |

## 配置選項

```yaml
worktree_config:
  # 全域配置
  defaults:
    enabled: true
    directory_prefix: ".worktrees"
    branch_prefix: "feature"
    auto_merge: false
    merge_strategy: "squash"

  # 專案級覆蓋
  project_override:
    file: ".claude/workflow-config.yaml"
    options:
      worktree:
        enabled: true | false
        directory: "custom-path"
```

## 相關資源

- [Worktree Setup](../../../../shared/isolation/worktree-setup.md)
- [Worktree Completion](../../../../shared/isolation/worktree-completion.md)
- [Path Resolution](../../../../shared/isolation/path-resolution.md)
- [Isolation Strategy](./isolation-strategy.md)
