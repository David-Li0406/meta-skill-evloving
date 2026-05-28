# Parallel Tasks Example

This file demonstrates parallel execution of independent tasks using memex-cli.

## Usage

```bash
memex-cli run --stdin < examples/parallel-tasks.md
```

## Task Definitions

---TASK---
id: implement-api
backend: codex
workdir: ./fullstack-app
model: gpt-5.2
---CONTENT---
实现后端 REST API：

技术栈：
- Node.js + Express
- PostgreSQL + Prisma ORM
- JWT 认证

API 端点：
- POST /api/users/register
- POST /api/users/login
- GET /api/users/profile
- PUT /api/users/profile
- GET /api/posts (分页, 搜索)
- POST /api/posts
- PUT /api/posts/:id
- DELETE /api/posts/:id

生成文件：
- src/server.js - Express 服务器
- src/routes/users.js - 用户路由
- src/routes/posts.js - 文章路由
- src/middlewares/auth.js - 认证中间件
- prisma/schema.prisma - 数据库模型
---END---

---TASK---
id: implement-frontend
backend: codex
workdir: ./fullstack-app
model: gpt-5.2
---CONTENT---
实现前端应用：

技术栈：
- React 18 + TypeScript
- React Router v6
- Axios
- Tailwind CSS

页面：
- /login - 登录页面
- /register - 注册页面
- / - 文章列表（首页）
- /posts/:id - 文章详情
- /profile - 用户个人资料
- /create - 创建文章

生成文件：
- src/App.tsx - 主应用组件
- src/pages/Login.tsx
- src/pages/Register.tsx
- src/pages/PostList.tsx
- src/pages/PostDetail.tsx
- src/pages/Profile.tsx
- src/pages/CreatePost.tsx
- src/services/api.ts - API 调用封装
- src/contexts/AuthContext.tsx - 认证上下文
---END---

---TASK---
id: setup-deployment
backend: codex
workdir: ./fullstack-app
---CONTENT---
配置部署文件：

1. Docker 配置：
   - Dockerfile（后端 Node.js）
   - Dockerfile.frontend（前端 React 构建）
   - docker-compose.yml（完整栈：postgres, backend, frontend）

2. CI/CD 配置：
   - .github/workflows/deploy.yml
   - 自动测试
   - 自动部署到生产环境

3. 环境配置：
   - .env.example（环境变量模板）
   - README.md（部署说明）

生成完整的部署工作流。
---END---

## Expected Behavior

All three tasks run **simultaneously**:
- `implement-api` (backend code generation)
- `implement-frontend` (frontend code generation)
- `setup-deployment` (deployment configs)

Total execution time ≈ slowest task duration (not sum of all tasks).

## Expected Output

```
▶ 并行执行 3 个任务...

  ▶ implement-api (codex/gpt-5.2)
  ▶ implement-frontend (codex/gpt-5.2)
  ▶ setup-deployment (codex)

  » implement-api: 写入 src/server.js
  » implement-api: 写入 src/routes/users.js
  » implement-frontend: 写入 src/App.tsx
  » setup-deployment: 写入 Dockerfile
  » implement-api: 写入 prisma/schema.prisma

  ✓ implement-api 8.5s
  ✓ setup-deployment 4.2s
  ✓ implement-frontend 9.1s

───────────────────────────
✓ 完成 3/3 任务 (9.1s, 并行加速 2.4x)
```

## Benefits of Parallel Execution

**Time Savings:**
- Sequential: 8.5s + 9.1s + 4.2s = 21.8s
- Parallel: max(8.5s, 9.1s, 4.2s) = 9.1s
- **Speedup: 2.4x**

**Use Cases:**
- Generating independent components
- Multi-language code generation
- Separate frontend/backend/infrastructure tasks

## Customization

**Add more parallel tasks:**

```
---TASK---
id: write-tests
backend: codex
workdir: ./fullstack-app
---CONTENT---
编写端到端测试用例
---END---
```

**Use different backends:**

```
---TASK---
id: design-ui
backend: gemini
workdir: ./fullstack-app
files: mockups/*.png
---CONTENT---
审查 UI 设计稿
---END---
```

## Converting to Sequential (DAG)

To make tasks sequential, add dependencies:

```
---TASK---
id: implement-frontend
backend: codex
workdir: ./fullstack-app
dependencies: implement-api    # Wait for API to finish
---CONTENT---
实现前端（基于后端 API）
---END---
```

See `examples/dag-workflow.md` for full DAG example.
