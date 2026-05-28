# GitHub 全自動整合

## 設計理念

**零干預 Git 工作流** — 從 commit 到 PR，全自動完成。

## 自動化層級

```
┌─────────────────────────────────────────────────────────┐
│  Level 1: 自動 Commit                                   │
│  每個任務完成 → 自動 commit                              │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│  Level 2: 自動 Push                                     │
│  Milestone 完成 → 自動 push 到 remote                   │
└─────────────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────────────┐
│  Level 3: 自動 PR                                       │
│  功能完成 → 自動開 PR 到 main/master                    │
└─────────────────────────────────────────────────────────┘
```

## Commit 自動化

### 觸發條件

```yaml
auto_commit_triggers:
  - "PDCA Check 階段全部通過"
  - "子任務完成"
  - "用戶明確請求"
```

### Commit Message 格式

```
{type}({scope}): {subject}

{body}

Task: {task_id}
Session: {session_id}
Plan: {plan_name}

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 範例

```
feat(auth): implement user registration API

- Add POST /api/register endpoint
- Implement password hashing with bcrypt
- Add JWT token generation
- Write unit tests (coverage: 85%)

Task: user-auth-1
Session: session-001
Plan: ecommerce-mvp

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Type 自動判斷

```python
def determine_commit_type(task, changes):
    # 根據任務類型
    if task.type == "feature":
        return "feat"
    if task.type == "bugfix":
        return "fix"
    if task.type == "refactor":
        return "refactor"

    # 根據變更內容
    if all(f.endswith('.test.ts') for f in changes):
        return "test"
    if all(f.endswith('.md') for f in changes):
        return "docs"

    return "chore"
```

## Push 自動化

### 觸發條件

```yaml
auto_push_triggers:
  # 主要觸發
  - name: "Milestone 完成"
    condition: "所有子任務完成"

  # 安全觸發
  - name: "定期推送"
    condition: "累積 5+ commits 且 > 30 分鐘"

  # 手動觸發
  - name: "用戶請求"
    condition: "--push flag"
```

### Push 前檢查

```yaml
pre_push_checks:
  - name: "遠端同步"
    action: "git fetch && git rebase origin/main"

  - name: "衝突檢查"
    action: "git diff --check"

  - name: "CI 預檢"
    action: "npm test && npm run build"
```

### 衝突處理

```
偵測到衝突
    ↓
┌─────────────────────────────────────────────────────────┐
│  自動解決策略                                            │
│  • package-lock.json → 重新生成                         │
│  • 配置檔案 → 保留雙方變更                               │
│  • 程式碼 → 嘗試智能合併                                │
└─────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────┐
│  無法自動解決                                            │
│  • 保存衝突狀態                                          │
│  • 通知用戶                                              │
│  • 暫停自動 push                                         │
└─────────────────────────────────────────────────────────┘
```

## PR 自動化

### 觸發條件

```yaml
auto_pr_triggers:
  - name: "功能分支完成"
    condition: "feature/* 分支所有任務完成"

  - name: "達到 PR 大小閾值"
    condition: "累積變更 > 1000 行 或 > 10 commits"
```

### PR 格式

```markdown
## Summary
{AI 生成的變更摘要}

## Changes
{按類別分組的檔案列表}

## Tasks Completed
- [x] {task_1}
- [x] {task_2}
- [x] {task_3}

## Test Plan
{驗證步驟}

## Screenshots
{如有 UI 變更}

---
🤖 Generated by Claude Plan
Plan: {plan_name}
Sessions: {session_list}
```

### PR 範例

```markdown
## Summary
Implement user authentication system with registration, login, and JWT-based session management.

## Changes
### Added
- `src/api/auth.ts` - Authentication endpoints
- `src/middleware/jwt.ts` - JWT validation middleware
- `src/models/user.ts` - User model with password hashing
- `tests/auth.test.ts` - Comprehensive test suite

### Modified
- `src/app.ts` - Added auth routes
- `package.json` - Added bcrypt, jsonwebtoken dependencies

## Tasks Completed
- [x] user-auth-1: Registration API
- [x] user-auth-2: Login API
- [x] user-auth-3: JWT Middleware
- [x] user-auth-4: Unit Tests

## Test Plan
1. Run `npm test` - All 24 tests pass
2. Manual test registration: `curl -X POST /api/register`
3. Manual test login: `curl -X POST /api/login`
4. Verify protected routes require valid JWT

---
🤖 Generated by Claude Plan
Plan: ecommerce-mvp
Sessions: session-001, session-002
```

## 分支策略

### 預設策略

```
main
  └── feature/{plan-name}
        ├── task/{task-id}-1
        ├── task/{task-id}-2
        └── ...
```

### 工作流程

```
1. 計畫開始 → 創建 feature/{plan-name} 分支
2. 每個任務 → 在 feature 分支上直接 commit
3. 功能完成 → PR 到 main
4. PR 合併 → 刪除 feature 分支
```

### 多 Session 分支

```
當多個 Session 並行工作時：

feature/ecommerce-mvp
  ├── session-001 commits (task: backend-api)
  ├── session-002 commits (task: frontend-ui)
  └── session-003 commits (task: checkout)

所有 commit 在同一分支，透過 task 標籤區分
```

## 安全機制

### 敏感檔案檢查

```yaml
sensitive_patterns:
  - ".env*"
  - "*secret*"
  - "*password*"
  - "*.pem"
  - "*.key"
  - "credentials*"

action: "阻止 commit，警告用戶"
```

### 大檔案檢查

```yaml
size_limits:
  single_file: 10MB
  total_commit: 50MB

action: "建議使用 Git LFS 或排除"
```

### Force Push 保護

```yaml
force_push_policy:
  main: "禁止"
  feature/*: "僅限 rebase 後"
  task/*: "允許"
```

## 配置選項

```yaml
# .claude/plans/{plan}/config.yaml

github:
  auto_commit: true
  auto_push: true
  auto_pr: true

  commit:
    sign: false  # GPG 簽名
    co_author: true

  push:
    force: false
    interval: "milestone"  # milestone | hourly | manual

  pr:
    auto_merge: false
    reviewers: []
    labels: ["auto-generated"]
    draft: false
```
