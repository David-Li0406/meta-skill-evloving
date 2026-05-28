---
name: kanban-batch
description: Code Kanban 任务批量编排器。读取本地 Kanban 的 todo 任务，分析优先级和依赖关系，生成执行计划，然后并行执行。用于自动化处理大量待办任务，数据不暴露到公开 GitHub。
---

# kanban-batch (本地 Kanban 批量编排器)

从 Code Kanban 读取任务，按优先级和依赖关系并行执行。

## 环境配置

```bash
# 设置 API 地址 (默认 3007 端口)
export KANBAN_URL="${KANBAN_URL:-http://127.0.0.1:3007}"
API="${KANBAN_URL}/api/v1"
```

## 触发方式

```bash
/kanban-batch                     # 处理当前项目所有 todo 任务
/kanban-batch --priority=0        # 只处理 P0 任务
/kanban-batch --dry-run           # 只生成计划，不执行
/kanban-batch --max=5             # 最多并行 5 个
/kanban-batch --project=<id>      # 指定项目 ID
```

## 工作流程

### Phase 1: 获取任务

```bash
# 自动检测当前项目
curl "${API}/projects" | jq '.items[] | select(.path == "'"$(pwd)"'")'

# 获取项目任务
curl "${API}/projects/{projectId}/tasks"
```

### Phase 2: 依赖分析

从任务描述中解析依赖关系：

```markdown
## Dependencies
- [task-id-xxx] (blocked by)
- #task-title (依赖标题匹配)
```

或使用优先级：
- priority: 0 (P0), 1 (P1), 2 (P2), 3 (P3)

### Phase 3: 构建执行图

```
输入: Tasks + 依赖关系
输出: DAG (有向无环图)

示例:
  Task A (P0, no deps)     ─┐
  Task B (P0, no deps)     ─┼─→ Wave 0 (可并行)
  Task C (P1, no deps)     ─┘
  Task D (P1, depends A)   ─→ Wave 1 (等待 A)
  Task E (P2, depends D)   ─→ Wave 2 (等待 D)
```

### Phase 4: 执行计划

```json
{
  "project": {
    "id": "dTw1ipjEiTer2WA8",
    "name": "Burner X"
  },
  "waves": [
    {
      "level": 0,
      "tasks": ["task-id-1", "task-id-2"],
      "parallel": true
    },
    {
      "level": 1,
      "tasks": ["task-id-3"],
      "parallel": false,
      "note": "依赖 task-id-1"
    }
  ]
}
```

### Phase 5: 并行执行

使用 Task 工具并行启动多个 `kanban-implement` agent：

```javascript
for (const wave of plan.waves) {
  // 同一 wave 内的任务并行执行
  await Promise.all(
    wave.tasks.map(taskId =>
      Task({
        subagent_type: "general-purpose",
        prompt: `执行 /kanban-implement ${taskId}`,
        run_in_background: true, // 后台运行
      })
    )
  );
  // 等待当前 wave 完成后再执行下一个 wave
}
```

每个 `kanban-implement` agent 负责：
1. 获取任务详情
2. 创建独立 Worktree (可选)
3. 实现功能并测试
4. 提交代码
5. 更新任务状态为 done

### Phase 6: 状态更新

执行完成后更新 Kanban 状态：

```bash
# 标记为进行中
curl -X PUT "${API}/tasks/{id}/update" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'

# 标记为完成
curl -X PUT "${API}/tasks/{id}/update" \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
```

## API 参考

### 项目列表

```bash
GET ${API}/projects
```

### 项目任务

```bash
GET ${API}/projects/{projectId}/tasks
```

### 创建任务

```bash
POST ${API}/projects/{projectId}/tasks/create
Content-Type: application/json

{
  "title": "任务标题",
  "description": "任务描述\n\nDepends on: [task-id-xxx]",
  "status": "todo",
  "priority": 0,
  "tags": ["type/bugfix", "epic/lifecycle"],
  "worktreeId": null,
  "dueDate": null
}
```

### 更新任务

```bash
PUT ${API}/tasks/{id}/update
Content-Type: application/json

{
  "status": "done"
}
```

## 优先级定义

| Priority | 含义 | 说明 |
|----------|------|------|
| 0 | P0 | 紧急，必须立即处理 |
| 1 | P1 | 高优先级 |
| 2 | P2 | 中优先级 |
| 3 | P3 | 低优先级 |

## 依赖解析规则

### 从描述解析

```markdown
Depends on: [task-id-xxx]
Blocked by: [task-id-yyy]
After: "任务标题关键词"
```

正则模式：
- `\[([a-zA-Z0-9]+)\]` → 任务 ID
- `depends on[:\s]+(.+)` → 依赖声明
- `blocked by[:\s]+(.+)` → 阻塞声明

### 排序规则

1. P0 优先于 P1 优先于 P2 优先于 P3
2. 无依赖的优先于有依赖的
3. 依赖数少的优先于依赖数多的

## 执行策略

### 并行控制

```yaml
max_parallel: 3          # 最多同时执行 3 个
wave_timeout: 30m        # 单 wave 最大时间
task_timeout: 15m        # 单任务最大时间
```

### 失败处理

- **单个失败**: 记录错误，继续执行同 wave 的其他任务
- **依赖失败**: 跳过所有依赖该任务的后续任务
- **全部失败**: 输出失败报告

### 执行报告

```markdown
## Batch Execution Report

### Summary
- Total: 10 tasks
- Success: 8
- Failed: 1
- Skipped: 1 (dependency failed)

### Wave 0 (Parallel)
- [x] Task A - StateEngine dispose
- [x] Task B - 常量化魔法数字
- [ ] Task C - 沙箱隔离 (Error: test failed)

### Wave 1
- [~] Task D - Skipped (depends on failed Task C)
```

## Worktree 集成

任务可以绑定独立 worktree：

```bash
# 创建 worktree
POST ${API}/projects/{projectId}/worktrees/create
{
  "branchName": "fix/task-xxx"
}

# 绑定到任务
PUT ${API}/tasks/{id}/bind-worktree
{
  "worktreeId": "worktree-id"
}
```

## 使用示例

### 处理所有 P0 任务

```
User: /kanban-batch --priority=0
Agent:
1. 检测当前项目: Burner X
2. 获取 P0 任务: 3 个
3. 分析依赖: Task C depends on Task A
4. 执行计划:
   - Wave 0: Task A, Task B (并行)
   - Wave 1: Task C (等待 Task A)
5. 开始执行...
```

### Dry-run 模式

```
User: /kanban-batch --dry-run
Agent:
[DRY RUN] 执行计划如下，不会实际执行:

Wave 0 (并行):
  - [P0] StateEngine dispose
  - [P0] 沙箱隔离增强

Wave 1:
  - [P1] DeepSearchState dispose (depends: StateEngine)

确认执行请运行: /kanban-batch
```

## 与 GitHub Issues 对比

| 特性 | GitHub Issues | Code Kanban |
|------|---------------|-------------|
| 可见性 | 公开 | 本地私有 |
| 依赖关系 | 手动 #引用 | 结构化 |
| Worktree | 需脚本 | 原生支持 |
| 状态管理 | Label | 内置 Kanban |
| AI 集成 | 无 | 原生支持 |

## 参考

- `kanban-implement` - 单任务实现 (开发总监)
- `kanban` - 任务管理 CLI
- `kanban-planner.js` - 本 skill 的辅助脚本

## 执行指令

当用户调用此 skill 时：

### Step 1: 检测项目

```bash
node ~/.claude/skills/kanban-batch/kanban-planner.js --detect
```

### Step 2: 生成计划

```bash
node ~/.claude/skills/kanban-batch/kanban-planner.js [options]
```

### Step 3: 确认执行

向用户展示执行计划，询问是否继续。

### Step 4: 并行执行

使用 Claude Task 工具并行启动 agent。

### Step 5: 状态更新

更新 Kanban 任务状态为 done。

### Step 6: 生成报告

汇总执行结果。
