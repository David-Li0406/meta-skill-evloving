# 階段數據傳遞

> 階段間產出物映射與傳遞機制

## 產出物映射

### RESEARCH → PLAN

```yaml
research_to_plan:
  source:
    stage: RESEARCH
    output_dir: ".claude/memory/research/{id}/"
    artifacts:
      - research-report.md      # 主報告
      - perspectives/           # 視角報告
      - synthesis.md            # 交叉驗證結果

  target:
    stage: PLAN
    usage:
      research-report.md:
        load_as: context
        sections_used:
          - "結論"
          - "建議"
          - "技術發現"

  handoff:
    method: file_reference
    validation:
      - file_exists
      - has_conclusions
```

### PLAN → IMPLEMENT

```yaml
plan_to_implement:
  source:
    stage: PLAN
    output_dir: ".claude/memory/plans/{id}/"
    artifacts:
      - implementation-plan.md  # 實作計劃（必須）
      - milestones.md           # 里程碑（可選）
      - synthesis.md            # 設計共識

  target:
    stage: IMPLEMENT
    usage:
      implementation-plan.md:
        load_as: task_list
        sections_used:
          - "任務清單"
          - "技術約束"
          - "驗收標準"

      milestones.md:
        load_as: checkpoints
        optional: true

  handoff:
    method: file_reference
    validation:
      - file_exists
      - has_tasks
      - has_acceptance_criteria
```

### IMPLEMENT → REVIEW

```yaml
implement_to_review:
  source:
    stage: IMPLEMENT
    output_dir: ".claude/memory/implementations/{id}/"
    artifacts:
      - implementation-log.md   # 實作記錄
      - perspectives/           # 視角報告
      - pass-at-k-metrics.md    # 成功率統計
      - code_changes            # Git diff（虛擬）

  target:
    stage: REVIEW
    usage:
      implementation-log.md:
        load_as: context
        sections_used:
          - "檔案變更"
          - "視角報告"

      code_changes:
        load_as: review_target
        method: git_diff

  handoff:
    method: file_reference + git
    validation:
      - file_exists
      - has_changes
      - tests_passed
```

### REVIEW → VERIFY

```yaml
review_to_verify:
  source:
    stage: REVIEW
    output_dir: ".claude/memory/reviews/{id}/"
    artifacts:
      - review-summary.md       # 審查摘要
      - issues/                 # 問題清單
      - perspectives/           # 視角報告

  target:
    stage: VERIFY
    usage:
      review-summary.md:
        load_as: context
        sections_used:
          - "審查結果"
          - "已修正問題"

  handoff:
    method: file_reference
    validation:
      - file_exists
      - no_blockers
```

### VERIFY → 完成/回退

```yaml
verify_to_complete:
  source:
    stage: VERIFY
    output_dir: ".claude/memory/verifications/{id}/"
    artifacts:
      - release-decision.md     # 發布決策
      - test-results/           # 測試結果
      - perspectives/           # 視角報告

  target:
    if_ship_it:
      action: complete_workflow
      update:
        - workflow.yaml status = completed

    if_blocked:
      action: rollback
      target_stage: IMPLEMENT
      data_to_pass:
        - failure_analysis
        - failed_tests
        - suggestions
```

## 傳遞機制

### 檔案引用

```yaml
file_reference:
  description: "直接讀取產出物檔案"

  implementation:
    1. locate_file: ".claude/memory/{stage}/{id}/{artifact}"
    2. validate: check_exists && check_format
    3. load: read_file_content
    4. parse: extract_relevant_sections

  example:
    source: ".claude/memory/plans/user-auth/implementation-plan.md"
    load_sections:
      - tasks
      - constraints
```

### Git Diff

```yaml
git_diff:
  description: "使用 Git 獲取程式碼變更"

  implementation:
    1. get_base: find_last_review_commit || find_plan_commit
    2. diff: git diff {base}..HEAD
    3. parse: extract_changed_files
    4. categorize: group_by_type

  example:
    command: "git diff main..feature/user-auth"
    output:
      added_files: [...]
      modified_files: [...]
      deleted_files: [...]
```

### 記憶體傳遞

```yaml
in_memory:
  description: "同一 session 內直接傳遞"

  use_when:
    - single_session_workflow
    - consecutive_stages

  implementation:
    1. store: save_to_session_context
    2. retrieve: get_from_session_context
```

## 數據驗證

### 必要驗證

```yaml
required_validations:
  file_exists:
    check: "os.path.exists(path)"
    on_fail: "abort with error"

  format_valid:
    check: "parse_markdown(content) != null"
    on_fail: "abort with error"

  has_required_sections:
    check: "all(section in content for section in required)"
    on_fail: "abort with error"
```

### 可選驗證

```yaml
optional_validations:
  has_optional_sections:
    check: "any(section in content for section in optional)"
    on_fail: "log warning, continue"

  quality_check:
    check: "content_quality_score > threshold"
    on_fail: "log warning, continue"
```

## 回退數據傳遞

### REVIEW BLOCKER → IMPLEMENT

```yaml
review_blocker_to_implement:
  data:
    blockers:
      source: "reviews/{id}/review-summary.md"
      section: "阻擋項"

    suggested_fixes:
      source: "reviews/{id}/issues/blockers.md"
      section: "建議修正"

  format:
    - blocker_list: array of issues
    - fix_suggestions: array of suggestions
    - affected_files: array of paths

  usage_in_implement:
    - prioritize_blockers
    - apply_suggested_fixes
    - re_run_affected_tests
```

### VERIFY BLOCKED → IMPLEMENT

```yaml
verify_blocked_to_implement:
  data:
    failure_analysis:
      source: "verifications/{id}/test-results/failures.md"

    failed_tests:
      source: "verifications/{id}/test-results/"
      files: ["functional.md", "edge-cases.md", "regression.md"]

  format:
    - failure_summary: string
    - failed_test_list: array of test names
    - failure_reasons: array of reasons

  usage_in_implement:
    - analyze_failure_patterns
    - fix_identified_issues
    - add_missing_tests
```

## 工作流狀態

### 狀態檔案

```yaml
# .claude/memory/workflows/{id}/workflow.yaml
workflow:
  id: "{id}"
  created: "{timestamp}"
  current_stage: "IMPLEMENT"
  status: "in_progress"

  stages:
    research:
      status: "completed"
      output: "research/{id}/"

    plan:
      status: "completed"
      output: "plans/{id}/"

    implement:
      status: "in_progress"
      iteration: 2
      output: "implementations/{id}/"

    review:
      status: "pending"
      output: null

    verify:
      status: "pending"
      output: null

  iterations:
    - iteration: 1
      stages: ["PLAN", "IMPLEMENT", "REVIEW"]
      rollback_reason: "BLOCKER: SQL injection"

    - iteration: 2
      stages: ["IMPLEMENT"]
      status: "in_progress"
```

### 狀態更新

```yaml
state_updates:
  on_stage_start:
    - set current_stage
    - set status = "in_progress"
    - log timestamp

  on_stage_complete:
    - set stage.status = "completed"
    - set stage.output = output_path
    - log timestamp

  on_rollback:
    - add to iterations
    - set target_stage.status = "in_progress"
    - increment iteration count
```

## Worktree 模式的數據傳遞

### 路徑解析

在 Worktree 模式下，路徑需要正確區分：

```yaml
worktree_path_resolution:
  code_operations:
    base: "{worktree_directory}"
    example: ".worktrees/user-auth/src/auth/login.ts"

  memory_operations:
    base: "{main_directory}/.claude/memory"
    example: "/project/.claude/memory/implementations/user-auth/"

  git_operations:
    diff_base: "main..HEAD"
    in_directory: "{worktree_directory}"
```

### IMPLEMENT → REVIEW（Worktree 模式）

```yaml
implement_to_review_worktree:
  source:
    stage: IMPLEMENT
    execution_context:
      type: "worktree"
      path: ".worktrees/{id}"

    code_changes:
      method: "git diff main..HEAD"
      in_directory: "{worktree_path}"

    memory_output:
      path: "{main_directory}/.claude/memory/implementations/{id}/"

  target:
    stage: REVIEW
    working_directory: "{worktree_path}"

    usage:
      code_changes:
        source: "git diff main..feature/{id}"
        note: "比較 feature 分支與 main"
```

### Worktree 狀態追蹤

```yaml
worktree_state_in_handoff:
  workflow.yaml:
    worktree:
      enabled: true
      directory: ".worktrees/{id}"
      branch: "feature/{id}"
      state: "active"

    stages:
      implement:
        execution_context:
          type: "worktree"
          path: ".worktrees/{id}"
          commits:
            - hash: "abc123"
              message: "feat: add login"
```

詳見：[../../../../shared/isolation/path-resolution.md](../../../../shared/isolation/path-resolution.md)

## 相關資源

- [階段判斷](../01-stage-detection/_base/auto-detect.md)
- [回退規則](../../03-error-handling/_base/rollback-rules.md)
- [Git Worktree 生命週期](../../04-git-worktree/_base/lifecycle.md)
