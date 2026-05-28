---
name: kanban-implement
description: 资深开发总监 (Senior Developer Director) 技能。当用户认领一个 Kanban 任务并准备开始开发时触发。该技能通过 Code Kanban API 管理 Worktree，提供隔离的开发沙盒，并在完成后自动更新任务状态。
---

# kanban-implement (开发总监)

主导从 Kanban 任务到代码交付的完整闭环。利用隔离的工作区环境，安全进行并发开发。

## 环境配置

```bash
# 设置 API 地址 (默认 3007 端口)
export KANBAN_URL="${KANBAN_URL:-http://127.0.0.1:3007}"
API="${KANBAN_URL}/api/v1"
```

## 触发方式

```bash
/kanban-implement <task-id>              # 实现指定任务
/kanban-implement <task-id> --no-worktree # 不创建 worktree (在当前分支开发)
/kanban-implement <task-id> --dry-run    # 只展示计划，不执行
```

## 交付工作流

### Phase 1: 任务获取

```bash
# 获取任务详情
curl -s "${API}/tasks/${TASK_ID}"
```

解析任务信息：
- 标题和描述
- 验收标准 (从描述中提取)
- 依赖关系
- 关联文件

### Phase 2: 沙盒隔离 (Sandboxing)

通过 Code Kanban API 创建独立 Worktree：

```bash
# 创建 worktree
curl -X POST "${API}/projects/${PROJECT_ID}/worktrees/create" \
  -H "Content-Type: application/json" \
  -d '{
    "branchName": "task/${TASK_ID}",
    "baseBranch": "main"
  }'

# 绑定到任务
curl -X PUT "${API}/tasks/${TASK_ID}/bind-worktree" \
  -H "Content-Type: application/json" \
  -d '{"worktreeId": "${WORKTREE_ID}"}'

# 更新任务状态为进行中
curl -X PUT "${API}/tasks/${TASK_ID}/update" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

命名规范：`task/<task-id>` 或 `fix/<task-id>-<short-desc>`

### Phase 3: 精益开发

1. **解析验收标准**
   - 从任务描述中提取 `## 验收标准` 部分
   - 转换为开发 checklist

2. **实现功能**
   - 遵循项目 `CLAUDE.md` 规范
   - 使用项目测试框架进行即时验证
   - 保持最小化变更原则

3. **质量验证**
   - 运行相关测试: `npm run test:agents` 或项目配置的测试命令
   - 确保测试通过

### Phase 4: 提交与合并

```bash
# 在 Worktree 中提交
curl -X POST "${API}/worktrees/${WORKTREE_ID}/commit" \
  -H "Content-Type: application/json" \
  -d '{"message": "fix: implement ${TASK_TITLE}"}'

# 合并到主分支
curl -X POST "${API}/worktrees/${WORKTREE_ID}/merge" \
  -H "Content-Type: application/json" \
  -d '{"targetBranch": "main"}'
```

### Phase 5: 状态更新

```bash
# 标记任务完成
curl -X PUT "${API}/tasks/${TASK_ID}/update" \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'

# 添加完成评论 (可选)
curl -X POST "${API}/tasks/${TASK_ID}/comments/create" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "## 完成报告\n\n- 变更文件: ...\n- 测试结果: PASS\n- 提交: ..."
  }'
```

## 开发质量自检 (Quality Pulse)

| 检查项 | 说明 |
|--------|------|
| AC 闭环 | 是否逐一核对并完成了所有验收标准？ |
| 环境纯净 | 是否在独立的分支和工作区中完成？ |
| 测试通过 | 是否运行了相关测试并全部通过？ |
| 最小变更 | 是否只修改了必要的代码？ |

## 验收标准解析

从任务描述中自动提取验收标准：

```markdown
## 验收标准
- [ ] 条件 1
- [ ] 条件 2
- [ ] 测试覆盖 >= 90%
```

正则模式：
- `## 验收标准` 或 `## Acceptance Criteria`
- `- \[ \] (.+)` → 未完成项
- `- \[x\] (.+)` → 已完成项

## 失败处理

### 测试失败
1. 记录失败日志
2. 保持任务状态为 `in_progress`
3. 在任务评论中添加失败信息
4. 不合并代码

### 合并冲突
1. 尝试自动解决简单冲突
2. 复杂冲突标记为 `blocked`
3. 添加评论说明冲突文件

## API 参考

### 获取任务详情
```bash
GET ${API}/tasks/{taskId}
```

### 创建 Worktree
```bash
POST ${API}/projects/{projectId}/worktrees/create
{
  "branchName": "task/xxx",
  "baseBranch": "main"
}
```

### 绑定 Worktree
```bash
PUT ${API}/tasks/{taskId}/bind-worktree
{
  "worktreeId": "xxx"
}
```

### 更新任务状态
```bash
PUT ${API}/tasks/{taskId}/update
{
  "status": "in_progress" | "done" | "blocked"
}
```

### Worktree 提交
```bash
POST ${API}/worktrees/{worktreeId}/commit
{
  "message": "commit message"
}
```

### Worktree 合并
```bash
POST ${API}/worktrees/{worktreeId}/merge
{
  "targetBranch": "main"
}
```

## 执行指令

当用户调用此 skill 时：

### Step 1: 获取任务信息

```bash
TASK=$(curl -s "${API}/tasks/${TASK_ID}")
```

展示任务摘要：标题、描述、验收标准、依赖。

### Step 2: 创建开发环境

如果不是 `--no-worktree` 模式：
1. 创建 Worktree
2. 绑定到任务
3. 切换到 Worktree 目录

### Step 3: 更新状态

```bash
curl -X PUT "${API}/tasks/${TASK_ID}/update" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'
```

### Step 4: 实现功能

根据任务描述和验收标准进行开发。

### Step 5: 验证测试

运行项目测试命令，确保通过。

### Step 6: 提交代码

使用 Git 提交代码，遵循 Conventional Commits。

### Step 7: 完成任务

```bash
curl -X PUT "${API}/tasks/${TASK_ID}/update" \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

### Step 8: 生成报告

输出完成报告：变更文件、测试结果、提交信息。

## 与 gh-issue-implement 对比

| 特性 | gh-issue-implement | kanban-implement |
|------|-------------------|------------------|
| 数据源 | GitHub Issues | Code Kanban API |
| Worktree | scripts/worktree_manager.js | Kanban API |
| 交付物 | Pull Request | Git Commit |
| 可见性 | 公开 | 私有 |
| 状态管理 | GitHub Labels | Kanban Status |

## 提交规范

- 使用 Conventional Commits 格式
- 禁止添加 Co-Authored-By 行
- 提交信息引用任务 ID: `fix(agents): implement X [task-id]`
