---
name: task-executor
description: |
  执行 task-breakdown 创建的子任务。
  从任务清单文件中读取并执行 waiting 或 failed 状态的子任务，执行完成后更新状态。
  当用户需要执行项目路径 .claude/tasks/ 中的任务清单时使用该 skill。
---

## 前置准备
 
执行 verify-tasks.py 验证用户提供的任务清单路径是否有效：

```bash
python3 scripts/verify-tasks.py <task-file.yml>
```

输出说明：
- OK：有效且存在未完成任务
- DONE：所有任务已完成，直接结束对话即可
- ERROR：文件格式错误或不存在，结束对话并提示用户

确认任务清单有效后，在项目路径中创建文件 `.claude/tasks/task-ralph.yml`，内容按以下格式填写：

```yml
tasks: ./.claude/tasks/2026-01-01-12-xxx.yml  # 任务清单文件项目相对路径
```

## 子任务执行流程

### 1. 确认任务文件

首先确认要执行的任务清单文件：
- 检查项目路径中 `./.claude/tasks/` 目录下的 `.yml` 文件
- 如果有多个任务文件，使用 `AskUserQuestion` 询问用户要执行哪个任务
- 如果用户直接指定了任务文件路径，则使用该文件

### 2. 读取下一个子任务

使用 `read-task.py` 脚本读取下一个 waiting 或 failed 状态的子任务：

```bash
python3 scripts/read-task.py <task-file.yml>
```

该脚本会：
- 按顺序查找子任务，优先返回 `state: waiting` 的任务（新任务）
- 如果没有 `waiting` 状态的任务，则返回 `state: failed` 的任务（重试失败任务）
- 读取任务后立即将其状态更新为 `running`，避免重复读取
- 返回子任务信息（JSON 格式），按顺序包括：
  1. `description`: 总体任务描述
  2. `completed`: 已完成任务列表（简要描述，从上往下顺序）
  3. `task_key`: 当前待执行任务的键名（如 01-create-model）
  4. `task`: 当前待执行任务的描述
  5. `location`: 涉及的文件/目录列表
  6. `failed_reason`: 失败原因（仅当任务状态为 failed 时存在）

**任务状态说明：**
- **waiting**: 新任务，首次执行
- **failed**: 之前执行失败的任务，需要根据失败原因进行修复
- **running**: 当前正在执行的任务（脚本会自动设置）
- **done**: 已完成的任务

**如果没有 waiting 或 failed 状态的子任务：**
- 输出提示信息：所有子任务已完成
- 退出执行流程

### 3. 执行子任务

根据读取到的子任务信息执行任务：

**解析任务信息：**
- 仔细阅读 `task` 字段中的任务描述
- 查看 `location` 字段了解涉及的文件范围
- 理解 `description` 字段中的总体目标

**执行任务：**
- 按照任务描述完成具体的代码编写、修改或其他操作
- 使用 `Read` 工具阅读相关文件
- 使用 `Write` 或 `Edit` 工具修改文件
- 遵循项目现有的代码风格和架构模式
- 如果需求不够清晰，使用 `AskUserQuestion` 询问用户

**处理失败任务：**
- 如果读取到的是 `failed` 状态的任务，会附带 `failed_reason` 字段
- 仔细阅读失败原因，分析问题所在
- 根据失败原因调整执行策略，修复问题
- 修复后重新执行任务，确保问题已解决

**注意事项：**
- 只执行当前子任务，不要跳到其他任务
- 如果发现任务依赖未完成的前置任务，告知用户
- 保持代码简洁，只做任务要求的内容
- 完成后确认代码可以正常工作

### 4. 更新任务状态

任务执行完成后，使用 `update-task.py` 脚本更新状态：

**成功完成时：**
```bash
python3 scripts/update-task.py <task-file.yml> <task-key> done
```

**执行失败时：**
```bash
python3 scripts/update-task.py <task-file.yml> <task-key> failed "失败原因描述"
```

失败原因应该清晰说明：
- 什么导致了失败
- 需要用户提供什么信息或资源
- 或者有什么前置条件未满足

### 5. 执行结束

完成一个子任务后：
- 输出完成信息，包括任务键名和任务摘要
- 结束对话
- 之后如果用户主动提示继续任务，则执行下一个任务；否则，什么也不要做

### 6. 输出格式

**读取到 waiting 状态的子任务时：**
```
📋 正在执行子任务

总体任务: 添加评论功能到博客系统

已完成任务:
✓ 01-create-comment-model: 创建 Comment 数据模型
✓ 02-setup-migration: 配置数据库迁移脚本

当前任务: 03-comment-api-endpoints
描述: 创建评论 API 端点

详细任务:
- 创建 GET /api/comments/{post_id} 获取评论列表
- 创建 POST /api/comments 创建新评论
- 添加必要的验证和权限检查

涉及文件:
- api/comments.py
- routes/
```

**读取到 failed 状态的子任务时：**
```
📋 正在修复失败的子任务

总体任务: 添加评论功能到博客系统

已完成任务:
✓ 01-create-comment-model: 创建 Comment 数据模型
✓ 02-setup-migration: 配置数据库迁移脚本

当前任务: 03-comment-api-endpoints
描述: 创建评论 API 端点

⚠️ 该任务之前执行失败，需要修复。

🔴 失败原因：需要了解现有的 API 认证机制，但未找到相关文档

📋 请根据失败原因分析问题，重新执行该任务。

详细任务:
- 创建 GET /api/comments/{post_id} 获取评论列表
- 创建 POST /api/comments 创建新评论
- 添加必要的验证和权限检查

涉及文件:
- api/comments.py
- routes/
```

**任务完成时：**
```
✓ 子任务完成: 01-create-comment-model

已创建 Comment 模型并添加了必要的字段和关联关系。

下一个子任务: 02-comment-api-endpoints
是否继续? (y/n)
```

**任务失败时：**
```
❌ 子任务失败: 02-comment-api-endpoints

失败原因: 需要了解现有的 API 认证机制，但未找到相关文档

建议: 请提供 API 认证相关的文档或代码示例，或手动完成此任务后继续
```

**所有任务完成时：**
```
🎉 所有子任务已完成!

任务文件: ./.claude/tasks/2025-01-12-14_add-comment-feature.yml
完成任务数: 4
```

### 7. 脚本使用说明

**read-task.py 参数：**
```bash
python3 scripts/read-task.py <task-file.yml>
```

**update-task.py 参数：**
```bash
# 成功完成
python3 scripts/update-task.py <task-file.yml> <task-key> done

# 执行失败
python3 scripts/update-task.py <task-file.yml> <task-key> failed "失败原因"
```

### 8. 注意事项

- **按顺序执行**：严格按照子任务的序号顺序执行，不要跳过任务
- **状态一致**：确保每次执行前先读取任务，执行后立即更新状态
- **失败处理**：如果任务失败，务必记录清晰的失败原因
- **不要修改任务文件**：不要手动编辑 yml 文件，始终使用脚本更新状态
- **确认依赖**：如果当前任务依赖前面的任务，确保前置任务已完成
- **保持沟通**：执行过程中及时向用户报告进度和遇到的问题
