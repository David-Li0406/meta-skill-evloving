# Merge Conflict Handling

> Worktree 合併時的衝突檢測與解決

## 概述

當 feature 分支準備合併到 main 時，可能因為 main 已有新變更而產生衝突。本文檔定義衝突檢測與解決策略。

## 衝突檢測時機

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        衝突檢測點                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  VERIFY: SHIP IT                                                        │
│       ↓                                                                  │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  Pre-merge Check                                                 │   │
│  │                                                                  │   │
│  │  1. Fetch latest main                                            │   │
│  │     git fetch origin main                                        │   │
│  │                                                                  │   │
│  │  2. Check if main has advanced                                   │   │
│  │     git log HEAD..origin/main --oneline                         │   │
│  │                                                                  │   │
│  │  3. If yes, try merge                                            │   │
│  │     git merge origin/main --no-commit                           │   │
│  │                                                                  │   │
│  │  4. Check for conflicts                                          │   │
│  │     git diff --check                                             │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│       ↓                                                                  │
│  ┌──────────────────────┬───────────────────────────────────────┐      │
│  │     無衝突           │              有衝突                    │      │
│  │                      │                                        │      │
│  │  繼續合併流程         │  進入衝突解決流程                      │      │
│  └──────────────────────┴───────────────────────────────────────┘      │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 衝突類型

### 檔案級衝突

```yaml
file_level_conflicts:
  both_modified:
    description: "main 和 feature 都修改了同一檔案的同一區域"
    severity: "high"
    resolution: "manual merge required"

  deleted_modified:
    description: "一方刪除，一方修改"
    severity: "medium"
    resolution: "choose keep or delete"

  rename_conflict:
    description: "兩邊重命名為不同名稱"
    severity: "low"
    resolution: "choose name"

  add_add:
    description: "兩邊新增同名但不同內容的檔案"
    severity: "medium"
    resolution: "choose content or merge"
```

### 語義級衝突

```yaml
semantic_conflicts:
  description: "檔案不衝突但邏輯上互斥"

  examples:
    - "main 刪除了一個 API，feature 依賴該 API"
    - "main 更改了函數簽名，feature 使用舊簽名"
    - "main 更新了 schema，feature 使用舊 schema"

  detection:
    - "tests fail after merge"
    - "build fails after merge"

  resolution: "code review and manual adjustment"
```

## 衝突解決選項

### 使用者選項

```yaml
conflict_resolution_options:
  1. manual_resolve:
      description: "手動解決衝突"
      workflow:
        1. show conflict details
        2. open affected files
        3. guide user through resolution
        4. verify resolution is valid
        5. continue merge

  2. accept_main:
      description: "接受 main 的變更，放棄 feature 的衝突部分"
      command: "git checkout --theirs {files}"
      warning: "可能遺失 feature 的部分工作"

  3. accept_feature:
      description: "接受 feature 的變更，覆蓋 main 的變更"
      command: "git checkout --ours {files}"
      warning: "可能覆蓋 main 的重要更新"

  4. rebase_feature:
      description: "將 feature 變基到最新的 main"
      command: "git rebase origin/main"
      workflow:
        - may need to resolve conflicts during rebase
        - re-run tests after rebase
        - return to REVIEW if significant changes

  5. abort_merge:
      description: "放棄合併，保持現狀"
      command: "git merge --abort"
      next_steps:
        - keep worktree
        - manual investigation
        - try again later
```

### 決策流程

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      衝突解決決策流程                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  檢測到衝突                                                              │
│       ↓                                                                  │
│  衝突數量和複雜度？                                                      │
│       ↓                                                                  │
│  ┌────────────────┬─────────────────┬────────────────────┐              │
│  │   1-2 簡單     │    3-5 中等     │     >5 複雜        │              │
│  │                │                 │                    │              │
│  │  建議：        │   建議：        │   建議：           │              │
│  │  手動解決      │   rebase        │   審查後決定       │              │
│  │  或 accept     │   然後解決      │   可能需要重新     │              │
│  │                │                 │   規劃             │              │
│  └────────────────┴─────────────────┴────────────────────┘              │
│       ↓                   ↓                    ↓                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │                      顯示選項給使用者                             │ │
│  │                                                                   │ │
│  │  1. 手動解決衝突                                                  │ │
│  │  2. 接受 main 的變更                                              │ │
│  │  3. 接受 feature 的變更                                           │ │
│  │  4. Rebase feature 到 main                                        │ │
│  │  5. 放棄合併                                                      │ │
│  │                                                                   │ │
│  │  [請選擇 1-5]                                                     │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## 手動解決流程

### 詳細步驟

```yaml
manual_resolution_steps:
  1. show_conflict_summary:
      content: |
        ⚠️ 檢測到 {count} 個衝突

        衝突檔案：
        {conflict_files_list}

        main 的最新變更：
        {main_changes_summary}

  2. for_each_conflict:
      show:
        - file path
        - conflict markers location
        - both versions side by side

      actions:
        - "接受 main 版本"
        - "接受 feature 版本"
        - "手動編輯"

  3. after_resolution:
      - git add {resolved_files}
      - verify no remaining conflicts
      - run tests

  4. complete_merge:
      - git commit
      - continue to PR/merge
```

### 衝突標記說明

```
<<<<<<< HEAD (main)
// main 分支的程式碼
const apiUrl = '/api/v2/users';
=======
// feature 分支的程式碼
const apiUrl = '/api/v1/users';
>>>>>>> feature/user-auth
```

```yaml
conflict_markers:
  "<<<<<<< HEAD":
    meaning: "main 分支（當前 HEAD）的版本開始"

  "=======":
    meaning: "分隔線"

  ">>>>>>> feature/...":
    meaning: "feature 分支的版本結束"

resolution:
  - 刪除所有衝突標記
  - 保留正確的程式碼
  - 可能需要結合兩邊的變更
```

## Rebase 流程

### 執行步驟

```yaml
rebase_workflow:
  1. prepare:
      - stash uncommitted changes
      - ensure clean working directory

  2. fetch_main:
      command: "git fetch origin main"

  3. rebase:
      command: "git rebase origin/main"

      on_conflict:
        - show conflicting commit
        - resolve each commit's conflicts
        - git rebase --continue
        - repeat until done

      on_failure:
        - git rebase --abort
        - return to original state

  4. verify:
      - run full test suite
      - check for semantic conflicts

  5. force_push:
      command: "git push --force-with-lease origin feature/{id}"
      note: "需要 force push 因為歷史被重寫"

  6. re_review:
      condition: "if significant changes during rebase"
      action: "return to REVIEW stage"
```

### Rebase 注意事項

```yaml
rebase_considerations:
  pros:
    - 線性歷史
    - 清晰的變更順序
    - 每個 commit 都基於最新 main

  cons:
    - 需要 force push
    - 可能需要多次解決衝突
    - 如果分支已共享，需要協調

  best_practices:
    - 在個人分支上使用
    - 共享分支用 merge
    - 衝突多時考慮分批 rebase
```

## 語義衝突檢測

### 自動檢測

```yaml
semantic_conflict_detection:
  after_merge_or_rebase:
    1. build_check:
        command: "npm run build"
        on_fail: "語義衝突：編譯失敗"

    2. test_check:
        command: "npm test"
        on_fail: "語義衝突：測試失敗"

    3. type_check:
        command: "npm run typecheck"
        on_fail: "語義衝突：類型錯誤"

  on_semantic_conflict:
    action: "return to IMPLEMENT"
    data:
      - failure details
      - affected files
      - suggested fixes
```

### 常見語義衝突

```yaml
common_semantic_conflicts:
  api_change:
    symptom: "找不到方法/函數"
    cause: "main 更改了 API 簽名"
    resolution: "更新呼叫方式"

  schema_change:
    symptom: "資料驗證失敗"
    cause: "main 更改了資料結構"
    resolution: "更新資料處理邏輯"

  dependency_change:
    symptom: "依賴衝突"
    cause: "main 更新了依賴版本"
    resolution: "npm install 後檢查相容性"

  config_change:
    symptom: "運行時錯誤"
    cause: "main 更改了配置結構"
    resolution: "更新配置使用方式"
```

## 報告格式

### 衝突報告

```markdown
## 合併衝突報告

### 摘要
- **檢測時間**：{timestamp}
- **Feature 分支**：feature/{id}
- **目標分支**：main
- **衝突數量**：{count}

### 衝突列表

| 檔案 | 類型 | 嚴重度 | 建議 |
|------|------|--------|------|
| src/auth/login.ts | both_modified | high | 手動解決 |
| package.json | both_modified | medium | 接受 main |

### Main 分支變更
{main_changes}

### Feature 分支變更
{feature_changes}

### 建議行動
1. {suggestion_1}
2. {suggestion_2}
```

## Flags

```bash
# 衝突處理
--auto-resolve STR      # 自動解決策略：main | feature | abort
--no-rebase             # 禁用 rebase 選項
--skip-semantic-check   # 跳過語義衝突檢測

# 合併行為
--merge-strategy STR    # squash | rebase | merge
--force-merge           # 強制合併（跳過衝突檢查，危險）
```

## 相關資源

- [Lifecycle](./lifecycle.md)
- [Isolation Strategy](./isolation-strategy.md)
- [Worktree Completion](../../../../shared/isolation/worktree-completion.md)
