---
name: task-breakdown
description: 分解复杂任务，拆分为多个子任务并创建任务元信息文档。当需要执行大型、复杂任务时使用
---

## 任务分解流程

### 1. 理解任务需求

首先确保完全理解用户的任务需求：
- 如果用户的请求不够清晰、完整或有歧义，**必须**先使用 `AskUserQuestion` 工具询问用户以澄清需求
- 只有在需求明确后才开始分解任务
- 记录任务的总体目标和关键约束条件

### 2. 分析项目结构

根据项目配置选择以下方式之一进行分析：

**LSP 工具**（如果启用）：
- 使用 MCP 或系统原生提供的项目符号、定义查找、引用分析等工具
- 利用 LSP 的跳转和搜索功能快速定位相关代码

**基础探索工具**（遵循全局提示词中的探索配置）：
- 使用 `Task` 工具的 Explore agent 进行代码库探索
- 或使用 `Glob` 查找相关文件和目录结构
- 使用 `Grep` 搜索代码模式和依赖关系
- 使用 `Read` 阅读关键文件了解现有实现

重点分析：
- 项目架构和目录结构
- 相关模块的现有实现
- 依赖关系和可复用代码
- 潜在的影响范围

### 3. 分解任务原则

将复杂任务拆分为多个子任务时遵循以下原则：

**粒度控制：**
- 每个子任务应尽可能简短、独立
- 单个子任务涉及的文件改动控制在 **10 个以内**
- 子任务应该可以独立验证完成状态

**任务独立性：**
- 子任务之间应尽量减少依赖关系
- 按照逻辑顺序排列：基础设施 -> 核心功能 -> 辅助功能 -> 测试 -> 文档
- 如果存在强依赖，在任务描述中说明依赖关系

**可执行性：**
- 每个子任务的描述应该是一个清晰的提示词
- 包含足够的信息让执行者理解要做什么
- 指定涉及的具体文件或目录路径

### 4. 生成任务清单文件

在项目根目录下创建任务清单文件：
- 路径：`./.claude/tasks/{yyyy-MM-dd-HH_taskName}.yml`
- 文件名中的 `taskName` 应该是任务的简短英文标识（kebab-case）
- 时间戳格式：`2025-01-12-14`

#### YAML 文件格式

```yaml
description: |
  本次任务的总体需求描述
  可以是多行文本，详细说明任务背景、目标和期望结果

# 子任务命名格式：数字序号-简短描述（kebab-case）
01-create-base-model:
  state: waiting  # waiting | running | done | failed
  task: |
    子任务的详细执行提示词，第一行为标题
    - 要做什么
    - 涉及哪些文件
    - 注意事项
  location:
    - path/to/file1.py
    - path/to/file2.py
    - path/to/directory/

02-implement-service:
  state: waiting
  task: |
    另一个子任务的描述...
  location:
    - path/to/service.py
```

**字段说明：**
- `description`: 顶层任务总体描述（必需，多行字符串）
- `state`: 子任务状态，默认 `waiting`
- `task`: 子任务的详细执行提示词（必需，多行字符串）
- `location`: 涉及的文件/文件夹路径列表（必需，数组）

### 5. 任务示例

假设用户要求"为博客系统添加评论功能"：

```yaml
description: |
  为现有博客系统添加评论功能，包括：
  - 用户可以发表评论（需要登录）
  - 评论支持 Markdown 格式
  - 博主可以删除评论
  - 发送邮件通知博主新评论

01-create-comment-model:
  state: waiting
  task: |
    创建 Comment 数据模型
    - 添加 id, content, author_id, post_id, created_at 字段
    - 定义与 Post 和 User 的关联关系
    - 添加必要的索引
  location:
    - models/comment.py
    - migrations/

02-comment-api-endpoints:
  state: waiting
  task: |
    实现评论相关的 API 端点
    - POST /api/posts/:id/comments - 创建评论
    - DELETE /api/comments/:id - 删除评论
    - GET /api/posts/:id/comments - 获取文章评论列表
    - 添加身份验证和权限检查
  location:
    - api/comments.py
    - api/__init__.py

03-comment-notification:
  state: waiting
  task: |
    实现新评论邮件通知功能
    - 当有新评论时发送邮件给文章作者
    - 邮件包含评论内容和跳转链接
    - 使用现有的邮件服务
  location:
    - services/notification.py
    - templates/email/comment_notification.html

04-add-comment-ui:
  state: waiting
  task: |
    在文章详情页添加评论组件
    - 评论列表展示
    - 评论表单（Markdown 预览）
    - 删除按钮（仅评论作者或博主可见）
  location:
    - components/CommentList.tsx
    - components/CommentForm.tsx
    - pages/PostDetail.tsx
```

### 6. 注意事项

- **不执行任务**：本 skill 仅负责创建任务清单，不执行任何实际代码修改
- **文件不存在处理**：如果 `./.claude/tasks/` 目录不存在，使用 Bash 创建：`mkdir -p ./.claude/tasks`
- **任务命名规范**：子任务键名使用 `数字序号-简短描述` 的格式，方便排序和引用
- **状态管理**：所有新建的子任务初始状态为 `waiting`
- **输出确认**：创建完成后，告知用户任务清单文件路径和子任务数量

### 7. 输出示例

完成分解后应输出类似以下信息：

```
✓ 任务分解完成

任务清单：./.claude/tasks/2025-01-12-14_add-comment-feature.yml
子任务数量：4

总体目标：为现有博客系统添加评论功能

子任务列表：
  01. 创建 Comment 数据模型
  02. 实现评论 API 端点
  03. 实现新评论邮件通知
  04. 添加评论 UI 组件

下一步：使用执行类 skill 逐个完成子任务
```
