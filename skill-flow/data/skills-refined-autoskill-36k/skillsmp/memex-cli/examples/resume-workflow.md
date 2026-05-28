# Resume Workflow Example

This file demonstrates iterative development using memex-cli's resume functionality to maintain context across multiple sessions.

## Scenario

Building a blog application incrementally:
1. Day 1: Initial implementation
2. Day 2: Add commenting feature (resume from Day 1)
3. Day 3: Bug fixes and optimization (resume from Day 2)

## Usage

Run each phase separately, saving the run ID between sessions.

---

## Phase 1: Initial Implementation

```bash
# Run initial implementation
memex-cli run --stdin < examples/resume-workflow-phase1.md

# Save the Run ID from output
# Example output: Run ID: blog-run-20260110120000
```

### Phase 1 Task Definition

---TASK---
id: blog-initial-implementation
backend: codex
workdir: ./blog-app
model: gpt-5.2
timeout: 600
---CONTENT---
实现博客应用基础功能：

技术栈：
- Python 3.11 + FastAPI
- SQLAlchemy + PostgreSQL
- Pydantic schemas

核心功能：
1. 用户管理
   - 注册 (POST /api/users/register)
   - 登录 (POST /api/users/login)
   - 个人资料 (GET/PUT /api/users/profile)

2. 文章管理
   - 创建文章 (POST /api/posts)
   - 列表文章 (GET /api/posts - 分页，搜索)
   - 文章详情 (GET /api/posts/:id)
   - 更新文章 (PUT /api/posts/:id)
   - 删除文章 (DELETE /api/posts/:id)

3. 基础设施
   - JWT 认证中间件
   - 数据库模型（User, Post）
   - API 路由组织
   - 错误处理

生成文件：
- app/models/user.py
- app/models/post.py
- app/routes/users.py
- app/routes/posts.py
- app/middlewares/auth.py
- app/schemas/user.py
- app/schemas/post.py
- app/main.py
- requirements.txt

确保代码包含完整的类型注解和文档字符串。
---END---

**Expected Output:**

```
▶ blog-initial-implementation (codex/gpt-5.2)

生成用户模型...
» 写入 app/models/user.py

生成文章模型...
» 写入 app/models/post.py

实现用户路由...
» 写入 app/routes/users.py

实现文章路由...
» 写入 app/routes/posts.py

配置认证中间件...
» 写入 app/middlewares/auth.py

生成 Pydantic schemas...
» 写入 app/schemas/user.py
» 写入 app/schemas/post.py

配置 FastAPI 应用...
» 写入 app/main.py
» 写入 requirements.txt

✓ blog-initial-implementation 45.3s

Run ID: blog-run-20260110120000
```

**Save the Run ID:**

```bash
echo "blog-run-20260110120000" > .memex-run-id
```

---

## Phase 2: Add Commenting Feature

**Resume from Phase 1 context:**

```bash
# Load saved Run ID
RUN_ID=$(cat .memex-run-id)

# Resume with new task
memex-cli resume --run-id $RUN_ID --stdin <<'EOF'
---TASK---
id: blog-add-comments
backend: codex
workdir: ./blog-app
model: gpt-5.2
---CONTENT---
基于现有代码添加评论功能：

参考现有文件：
- app/models/ - 参考现有模型设计
- app/routes/ - 参考现有路由模式
- app/schemas/ - 参考现有 schema 结构

新增功能：
1. 评论数据模型
   - 关联到 User 和 Post
   - 支持嵌套评论（parent_id）
   - 时间戳（created_at, updated_at）

2. 评论 API
   - 创建评论 (POST /api/posts/:post_id/comments)
   - 获取评论列表 (GET /api/posts/:post_id/comments)
   - 更新评论 (PUT /api/comments/:id)
   - 删除评论 (DELETE /api/comments/:id)

3. 评论验证
   - 只有评论作者可以编辑/删除
   - 验证文章存在
   - 嵌套评论深度限制（最多3层）

生成文件：
- app/models/comment.py
- app/routes/comments.py
- app/schemas/comment.py

更新文件：
- app/main.py（注册新路由）
- app/models/post.py（添加 comments 关系）

保持与现有代码风格一致。
---END---
EOF

# Save new Run ID
# Output: Run ID: blog-run-20260110150000
echo "blog-run-20260110150000" > .memex-run-id
```

**Expected Output:**

```
▶ blog-add-comments (codex/gpt-5.2)

分析现有模型结构...
📄 加载 app/models/user.py
📄 加载 app/models/post.py

创建评论模型...
» 写入 app/models/comment.py

实现评论路由...
» 写入 app/routes/comments.py

生成评论 schemas...
» 写入 app/schemas/comment.py

更新文章模型（添加关系）...
» 更新 app/models/post.py

注册评论路由...
» 更新 app/main.py

✓ blog-add-comments 28.7s

Run ID: blog-run-20260110150000
```

**Context Benefits:**
- AI remembers Phase 1 code structure
- Maintains consistent coding style
- References existing models/routes
- Follows established patterns

---

## Phase 3: Bug Fixes and Optimization

**Resume from Phase 2 context:**

```bash
# Load saved Run ID
RUN_ID=$(cat .memex-run-id)

# Resume with bug fixes
memex-cli resume --run-id $RUN_ID --stdin <<'EOF'
---TASK---
id: blog-bugfixes-optimization
backend: codex
workdir: ./blog-app
model: gpt-5.2
files: app/**/*.py
files-mode: ref
---CONTENT---
审查现有代码并进行 bug 修复和性能优化：

Bug 修复：
1. 检查所有 API 路由的错误处理
   - 添加缺失的 try-except 块
   - 返回适当的 HTTP 状态码
   - 详细的错误消息

2. 数据验证
   - 确保所有输入都经过 Pydantic 验证
   - 添加缺失的字段验证（邮箱格式、长度限制等）
   - 检查边界条件（空字符串、None 值）

3. 认证和授权
   - 修复潜在的认证绕过问题
   - 确保所有受保护路由都有中间件
   - 验证 token 过期时间

性能优化：
1. 数据库查询优化
   - 添加缺失的数据库索引
   - 使用 select_related/joinedload 避免 N+1 查询
   - 分页查询优化

2. 响应优化
   - 添加适当的缓存头
   - 压缩响应（gzip）
   - 限流中间件

3. 代码优化
   - 移除重复代码
   - 提取公共函数
   - 添加类型提示

输出文件：
- BUGFIXES.md（修复清单）
- OPTIMIZATIONS.md（优化说明）
- 更新相关代码文件

列出所有修改的文件和具体改进。
---END---
EOF
```

**Expected Output:**

```
▶ blog-bugfixes-optimization (codex/gpt-5.2)

加载现有代码进行分析...
📄 加载 app/routes/users.py (ref)
📄 加载 app/routes/posts.py (ref)
📄 加载 app/routes/comments.py (ref)
📄 加载 app/models/*.py (ref)

识别问题：
⚠ app/routes/posts.py:45 - 缺少异常处理
⚠ app/models/post.py - 缺少标题长度索引
⚠ app/routes/comments.py:23 - N+1 查询问题

应用修复...
» 更新 app/routes/users.py（添加错误处理）
» 更新 app/routes/posts.py（添加错误处理，查询优化）
» 更新 app/routes/comments.py（修复 N+1 查询）
» 更新 app/models/post.py（添加索引）
» 更新 app/models/user.py（添加索引）
» 更新 app/middlewares/auth.py（增强安全性）

生成文档...
» 写入 BUGFIXES.md
» 写入 OPTIMIZATIONS.md

✓ blog-bugfixes-optimization 32.1s

修复总结：
- 15 个错误处理改进
- 8 个数据库索引添加
- 5 个 N+1 查询优化
- 3 个安全性增强
```

**Context Accumulation:**
- AI has full history from Phase 1 and Phase 2
- Understands entire codebase structure
- Can identify issues across all files
- Maintains coding consistency

---

## Complete Workflow Summary

**Timeline:**

```
Day 1 (Phase 1):
  blog-initial-implementation
  → Run ID: blog-run-20260110120000

Day 2 (Phase 2):
  resume --run-id blog-run-20260110120000
  → blog-add-comments
  → Run ID: blog-run-20260110150000

Day 3 (Phase 3):
  resume --run-id blog-run-20260110150000
  → blog-bugfixes-optimization
  → Final application
```

**Context Chain:**

```
Phase 1 Context
    ↓
Phase 2 Context (includes Phase 1)
    ↓
Phase 3 Context (includes Phase 1 + 2)
```

**Files Generated:**

```
blog-app/
├── app/
│   ├── models/
│   │   ├── user.py          # Phase 1
│   │   ├── post.py          # Phase 1, updated Phase 2, 3
│   │   └── comment.py       # Phase 2
│   ├── routes/
│   │   ├── users.py         # Phase 1, updated Phase 3
│   │   ├── posts.py         # Phase 1, updated Phase 3
│   │   └── comments.py      # Phase 2, updated Phase 3
│   ├── schemas/
│   │   ├── user.py          # Phase 1
│   │   ├── post.py          # Phase 1
│   │   └── comment.py       # Phase 2
│   ├── middlewares/
│   │   └── auth.py          # Phase 1, updated Phase 3
│   └── main.py              # Phase 1, updated Phase 2, 3
├── requirements.txt         # Phase 1
├── BUGFIXES.md             # Phase 3
└── OPTIMIZATIONS.md        # Phase 3
```

---

## Advanced Resume Patterns

### Pattern 1: Branching Development

Start from the same base run and explore different directions:

```bash
# Base implementation
memex-cli run --stdin < base.md
# Run ID: base-001

# Branch A: Add feature X
memex-cli resume --run-id base-001 --stdin < feature-x.md
# Run ID: branch-a-001

# Branch B: Add feature Y (also from base)
memex-cli resume --run-id base-001 --stdin < feature-y.md
# Run ID: branch-b-001
```

### Pattern 2: Checkpoint and Retry

Save checkpoints, retry from stable points:

```bash
# Phase 1 success
memex-cli run --stdin < phase1.md
# Run ID: checkpoint-1

# Phase 2 attempt (fails)
memex-cli resume --run-id checkpoint-1 --stdin < phase2-v1.md
# Failed

# Retry Phase 2 with different approach
memex-cli resume --run-id checkpoint-1 --stdin < phase2-v2.md
# Success! Run ID: checkpoint-2
```

### Pattern 3: Multi-Day Project

Long-term project with daily progress:

```bash
# Monday: Project setup
memex-cli run --stdin < day1-setup.md
echo "day1-run-id" > .memex-project-id

# Tuesday: Core features
memex-cli resume --run-id $(cat .memex-project-id) --stdin < day2-core.md
# Update .memex-project-id with new run ID

# Wednesday: Testing
memex-cli resume --run-id $(cat .memex-project-id) --stdin < day3-tests.md
# Update .memex-project-id

# Thursday: Deployment
memex-cli resume --run-id $(cat .memex-project-id) --stdin < day4-deploy.md
```

---

## Best Practices for Resume Workflows

**1. Save Run IDs systematically:**

```bash
# Timestamped log
echo "$(date -Iseconds) base-run-id" >> .memex-history
echo "$(date -Iseconds) feature-run-id" >> .memex-history

# Named checkpoints
echo "base-run-id" > .memex-checkpoint-base
echo "feature-run-id" > .memex-checkpoint-feature
```

**2. Describe context in resume prompts:**

```
基于之前的实现（用户认证模块）添加密码重置功能
```

Better than:
```
添加密码重置
```

**3. Reference previous outputs:**

```
参考 Phase 1 生成的 app/models/user.py 结构
```

**4. Keep resume prompts focused:**

Each resume task should have a clear, single purpose.

**5. Use file loading strategically:**

```bash
# Load specific files for context
---TASK---
files: app/models/*.py,app/routes/users.py
files-mode: ref
---CONTENT---
基于现有模型和用户路由添加管理员功能
---END---
```

---

## Troubleshooting Resume Issues

**Issue: "Run ID not found"**

```bash
# List available runs
memex-cli runs list

# Verify run ID exists
memex-cli runs show <run-id>
```

**Issue: Context too large**

```bash
# Start fresh branch from earlier checkpoint
memex-cli resume --run-id <earlier-checkpoint> --stdin < task.md
```

**Issue: Lost context**

```bash
# View run history
memex-cli runs show <run-id>

# Check previous task outputs
cat .memex-output/<run-id>.log
```

---

## Summary

Resume workflows enable:
- **Incremental development** across multiple sessions
- **Context preservation** from previous tasks
- **Iterative refinement** without restarting
- **Branching exploration** from stable checkpoints
- **Long-term projects** maintained over days/weeks

Key to success:
1. Save run IDs systematically
2. Reference previous work in prompts
3. Use descriptive task IDs
4. Keep each resume task focused
5. Load relevant files for context

Start small, build incrementally, maintain continuity with resume!
