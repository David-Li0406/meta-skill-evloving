---
name: ralph-loop
description: Ralph Wiggum 自主循环模式。AI 持续执行任务直到全部完成，按用户确认的节奏汇报（默认整单完成后）。触发词：ralph、ralph-loop、/ralph-loop、自主循环、autonomous、直到完成、循环执行。
---

# /ralph-loop

**模板分类**: Action
**成熟度**: L5 (Higher Order)

基于 Geoffrey Huntley 的 Ralph Wiggum 技术，实现 AI 自主循环执行直到任务完成。

## 核心理念

> "Keep feeding an AI agent a task until the job is done"

命名来源于《辛普森一家》中的 Ralph Wiggum，强调**持续迭代**而非一次性完成。

## 工作原理

```
┌──────────────────────────────────────────────────────┐
│ Ralph Loop (外层)                                    │
│ ┌────────────────────────────────────────────────┐   │
│ │ 任务执行 (内层)                                 │   │
│ │ 执行 → 测试 → 验证 → 反馈 ... 直到单任务完成   │   │
│ └────────────────────────────────────────────────┘   │
│                       ↓                              │
│ verifyCompletion: "所有任务都完成了吗？"             │
│                       ↓                              │
│ 否？→ 选择下一个任务 → 继续迭代                      │
│ 是？→ 调用 zhi 通知用户                              │
└──────────────────────────────────────────────────────┘
```

## 关键特性

### 1. 每次迭代 = 全新上下文
通过以下方式保持记忆：
- `progress.txt` - 进度和学习记录
- `prd.json` / 任务清单 - 哪些任务已完成
- Git history - 代码变更历史

### 2. 小任务原则
每个任务应小到能在一个上下文窗口内完成：
- ✅ 添加一个数据库字段和迁移
- ✅ 修复一个特定的 Bug
- ✅ 实现一个 UI 组件
- ❌ "构建整个仪表盘"（太大，需拆分）

### 3. 反馈循环
必须有自动化验证：
- 类型检查（typecheck）
- 单元测试（unit tests）
- E2E 测试（如适用）
- Lint 检查

### 4. 停止条件
- 所有任务 `passes: true`
- 达到最大迭代次数（默认 10）
- 遇到无法自动解决的问题
- 用户选择暂停或终止

## 使用方法

### 汇报节奏（必须确认）

启动前通过 zhi 询问用户选择：
- 整单完成后汇报（默认）
- 每个子任务完成后汇报

### 触发方式

```
ralph: 执行以下任务直到完成
1. 修复 P-2026-030
2. 添加回归测试
3. 更新文档
```

或：

```
pai ralph: 重构支付模块
```

### 任务清单格式

创建 `ralph-tasks.json`：

```json
{
  "name": "功能名称",
  "tasks": [
    {
      "id": "T-001",
      "description": "任务描述",
      "acceptance": ["验收条件1", "验收条件2"],
      "passes": false
    }
  ],
  "maxIterations": 10,
  "verifyCommand": "bun test"
}
```

### 进度记录

每次迭代后更新 `progress.txt`：

```
## 迭代 3 - 2026-01-18 14:30

### 完成
- T-001: 修复了白屏问题

### 学习
- 发现 useEffect 依赖数组缺少 `userId`

### 下一步
- T-002: 添加回归测试
```

## 执行流程

```python
def ralph_loop(tasks, max_iterations=10):
    report_mode = call_zhi("请选择 Ralph-loop 汇报节奏：整单完成 / 每个子任务")
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        # 1. 选择下一个未完成任务
        task = next((t for t in tasks if not t['passes']), None)
        if not task:
            break  # 全部完成
        
        # 2. 执行任务
        execute_task(task)
        
        # 3. 运行验证
        if run_verify_command():
            task['passes'] = True
            update_progress(f"✅ {task['id']} 完成")
        else:
            update_progress(f"❌ {task['id']} 失败，将重试")
        
        # 4. 保存进度
        save_tasks(tasks)
        git_commit(f"ralph: {task['id']}")
        
        # 5. 按节奏汇报
        if report_mode == "每个子任务" and not call_zhi(f"{task['id']} 已完成，是否继续下一任务？"):
            break
    
    # 6. 完成后通知用户
    call_zhi("Ralph 循环完成，请审查结果")
```

## 与 iterate/cunzhi 的集成

### 关键区别

| 普通模式 | Ralph 模式 |
|----------|-----------|
| 每步调用 zhi | 按用户选择（默认整单完成后） |
| 用户逐步审查 | 用户阶段性或最终审查 |
| 适合探索性任务 | 适合明确的任务清单 |

### 何时使用 Ralph 模式

- ✅ 有明确的任务清单
- ✅ 有自动化测试验证
- ✅ 任务之间相对独立
- ❌ 需要频繁用户确认
- ❌ 探索性/不确定的任务

### 安全机制

1. **最大迭代限制**：防止无限循环
2. **Git 提交**：每个任务完成后提交，便于回滚
3. **进度记录**：`progress.txt` 记录所有操作
4. **失败中断**：连续 3 次失败自动停止并通知用户
5. **节奏确认**：启动前通过 zhi 明确汇报节奏

## 示例

### 示例 1：批量修复 Bug

用户输入：
```
ralph: 修复以下问题
1. P-2026-030 白屏问题
2. P-2026-031 端口检测失败
3. P-2026-032 任务队列死锁
```

AI 执行：
1. 创建 `ralph-tasks.json`
2. 通过 zhi 确认汇报节奏（默认整单完成后）
3. 循环执行每个修复
4. 每个修复后运行测试
5. 按选择的节奏汇报结果

### 示例 2：功能开发

用户输入：
```
pai ralph: 实现暗黑模式
- 添加主题切换按钮
- 实现 CSS 变量
- 保存用户偏好
- 添加测试
```

AI 执行：
1. 拆分为 4 个子任务
2. 通过 zhi 确认汇报节奏（默认整单完成后）
3. 按顺序实现每个
4. 每步运行 `bun test`
5. 按选择的节奏汇报结果

## 参考

- [Geoffrey Huntley's Ralph Pattern](https://ghuntley.com/ralph/)
- [vercel-labs/ralph-loop-agent](https://github.com/vercel-labs/ralph-loop-agent)
- [snarktank/ralph](https://github.com/snarktank/ralph)
