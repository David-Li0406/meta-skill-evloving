# DAG Workflow Example

This file demonstrates a complete development workflow using DAG (Directed Acyclic Graph) dependencies.

## Usage

```bash
memex-cli run --stdin < examples/dag-workflow.md
```

## Workflow Graph

```
design-api ──┐
              ├──> implement ──> test-unit ──> test-integration ──> deploy
design-ui  ──┘
```

## Task Definitions

---TASK---
id: design-api
backend: gemini
workdir: ./ecommerce-api
---CONTENT---
设计电商 REST API 架构：

需求：
- 用户管理（注册、登录、个人资料）
- 商品管理（列表、详情、搜索、分类）
- 购物车（添加、删除、更新数量）
- 订单管理（创建订单、订单历史、订单状态）
- 支付集成（模拟支付接口）

输出：
1. API 端点列表（RESTful 设计）
2. 数据模型设计（ERD 概念图）
3. 认证方案（JWT + Refresh Token）
4. 错误处理规范
5. API 版本策略

以 Markdown 格式输出设计文档，保存到 docs/api-design.md
---END---

---TASK---
id: design-ui
backend: gemini
workdir: ./ecommerce-api
---CONTENT---
设计前端用户界面流程：

页面需求：
- 首页（商品推荐、分类导航）
- 商品列表页（搜索、筛选、排序）
- 商品详情页（图片、描述、评价、加购物车）
- 购物车页（商品列表、数量调整、结算）
- 订单页（确认订单、填写地址、选择支付方式）
- 个人中心（订单历史、个人信息）

输出：
1. 页面流程图
2. 用户交互流程
3. 关键组件设计
4. 状态管理方案（Redux/Context）
5. 路由设计

以 Markdown 格式输出设计文档，保存到 docs/ui-design.md
---END---

---TASK---
id: implement
backend: codex
workdir: ./ecommerce-api
model: gpt-5.2
dependencies: design-api,design-ui
---CONTENT---
基于设计文档实现后端 API：

参考文档：
- docs/api-design.md（API 设计）
- docs/ui-design.md（前端需求）

技术栈：
- Python 3.11 + FastAPI
- PostgreSQL + SQLAlchemy
- Redis（会话、缓存）
- Alembic（数据库迁移）

实现内容：
1. 数据库模型（SQLAlchemy models）
2. API 路由（FastAPI routes）
3. 业务逻辑（service layer）
4. 中间件（认证、日志、错误处理）
5. 数据验证（Pydantic schemas）
6. 数据库迁移脚本

生成文件：
- app/models/ - 数据库模型
- app/routes/ - API 路由
- app/services/ - 业务逻辑
- app/middlewares/ - 中间件
- app/schemas/ - Pydantic 模型
- alembic/versions/ - 迁移脚本
- app/main.py - FastAPI 应用入口
- requirements.txt - 依赖列表

确保代码符合 API 设计文档的规范。
---END---

---TASK---
id: test-unit
backend: codex
workdir: ./ecommerce-api
dependencies: implement
---CONTENT---
编写单元测试：

测试范围：
1. 数据库模型测试
   - 模型创建、更新、删除
   - 关系测试
   - 约束验证

2. 服务层测试
   - 业务逻辑正确性
   - 边界条件
   - 错误处理

3. Schema 验证测试
   - 数据验证规则
   - 序列化/反序列化

技术栈：
- pytest
- pytest-asyncio
- faker（测试数据生成）
- factory_boy（模型工厂）

生成文件：
- tests/unit/test_models.py
- tests/unit/test_services.py
- tests/unit/test_schemas.py
- tests/conftest.py（fixtures）
- tests/factories.py（数据工厂）

目标覆盖率：>80%
---END---

---TASK---
id: test-integration
backend: codex
workdir: ./ecommerce-api
dependencies: test-unit
---CONTENT---
编写集成测试：

测试场景：
1. 用户注册登录流程
   POST /api/users/register → POST /api/users/login → GET /api/users/profile

2. 商品浏览和购买流程
   GET /api/products → GET /api/products/:id → POST /api/cart/items →
   POST /api/orders → GET /api/orders/:id

3. 完整购物流程
   注册 → 登录 → 浏览商品 → 加购物车 → 创建订单 → 支付 → 查看订单

4. 错误场景
   - 未认证访问
   - 无效数据
   - 资源不存在
   - 权限不足

技术栈：
- pytest
- httpx（异步 HTTP 客户端）
- TestClient（FastAPI 测试）

生成文件：
- tests/integration/test_auth_flow.py
- tests/integration/test_shopping_flow.py
- tests/integration/test_order_flow.py
- tests/integration/test_error_cases.py

每个测试应该是端到端的完整场景。
---END---

---TASK---
id: deploy
backend: codex
workdir: ./ecommerce-api
dependencies: test-integration
---CONTENT---
配置生产部署：

部署目标：
- 云平台：AWS / Docker Swarm
- 数据库：PostgreSQL（托管服务）
- 缓存：Redis（托管服务）
- 反向代理：Nginx
- HTTPS：Let's Encrypt

生成配置：
1. Docker 配置
   - Dockerfile（多阶段构建）
   - docker-compose.yml（开发环境）
   - docker-compose.prod.yml（生产环境）

2. Nginx 配置
   - nginx.conf（反向代理、负载均衡）
   - SSL 配置

3. CI/CD 配置
   - .github/workflows/ci.yml（测试）
   - .github/workflows/deploy.yml（部署）

4. 环境配置
   - .env.example（环境变量模板）
   - deploy.sh（部署脚本）

5. 文档
   - docs/deployment.md（部署指南）
   - docs/monitoring.md（监控方案）

确保配置遵循生产最佳实践（安全、性能、可观测性）。
---END---

## Expected Execution Flow

Tasks execute in dependency order:

**Phase 1: Parallel Design** (both run simultaneously)
```
▶ design-api (gemini)
▶ design-ui (gemini)

» design-api: 写入 docs/api-design.md
✓ design-api 5.2s

» design-ui: 写入 docs/ui-design.md
✓ design-ui 4.8s
```

**Phase 2: Implementation** (waits for both designs)
```
▶ implement (codex/gpt-5.2) ← design-api,design-ui

» 写入 app/models/user.py
» 写入 app/models/product.py
» 写入 app/routes/users.py
...
✓ implement 15.3s
```

**Phase 3: Unit Testing** (waits for implementation)
```
▶ test-unit (codex) ← implement

» 写入 tests/unit/test_models.py
» 写入 tests/unit/test_services.py
...
✓ test-unit 8.1s
```

**Phase 4: Integration Testing** (waits for unit tests)
```
▶ test-integration (codex) ← test-unit

» 写入 tests/integration/test_auth_flow.py
» 写入 tests/integration/test_shopping_flow.py
...
✓ test-integration 6.5s
```

**Phase 5: Deployment Configuration** (waits for integration tests)
```
▶ deploy (codex) ← test-integration

» 写入 Dockerfile
» 写入 docker-compose.prod.yml
» 写入 nginx.conf
...
✓ deploy 4.2s
```

**Summary:**
```
───────────────────────────
✓ 完成 6/6 任务 (44.1s)

执行顺序：
1. design-api, design-ui（并行）
2. implement
3. test-unit
4. test-integration
5. deploy
```

## Benefits of DAG Execution

**Dependency Management:**
- `implement` accesses design documents from previous tasks
- `test-unit` can reference implementation code
- `deploy` uses passing tests as validation

**Parallel Optimization:**
- `design-api` and `design-ui` run in parallel (saves ~5s)
- Remaining tasks run sequentially due to dependencies

**Context Preservation:**
- Each task can reference outputs from dependencies
- Full development history maintained

## Customization

**Add parallel branches:**

```
---TASK---
id: write-docs
backend: claude
workdir: ./ecommerce-api
dependencies: implement
---CONTENT---
编写 API 文档
---END---

---TASK---
id: deploy
backend: codex
workdir: ./ecommerce-api
dependencies: test-integration,write-docs    # Wait for both
---CONTENT---
配置部署
---END---
```

**Change backend per phase:**

```
design-* tasks    → gemini   (design/architecture)
implement task    → codex    (code generation)
test-* tasks      → codex    (test generation)
deploy task       → codex    (config generation)
```

## Visualizing the DAG

Generated dependency graph:

```
       ┌─────────────┐    ┌─────────────┐
       │ design-api  │    │  design-ui  │
       └──────┬──────┘    └──────┬──────┘
              │                  │
              └────────┬─────────┘
                       │
                ┌──────▼──────┐
                │  implement  │
                └──────┬──────┘
                       │
                ┌──────▼──────┐
                │  test-unit  │
                └──────┬──────┘
                       │
             ┌─────────▼────────────┐
             │ test-integration    │
             └─────────┬────────────┘
                       │
                ┌──────▼──────┐
                │   deploy    │
                └─────────────┘
```

**Critical Path:** design → implement → test-unit → test-integration → deploy

Total time = sum of critical path tasks (≈44s in example)

## Resume from Failure

If a task fails, resume from that point:

```bash
# Original run fails at test-integration
memex-cli run --stdin < examples/dag-workflow.md
# Fails with Run ID: workflow-abc123

# Fix the issue and resume
memex-cli resume --run-id workflow-abc123 --stdin <<'EOF'
---TASK---
id: test-integration-retry
backend: codex
workdir: ./ecommerce-api
dependencies: test-unit
---CONTENT---
重新运行集成测试（已修复bug）
---END---
EOF
```

## Best Practices

1. **Keep DAG shallow** - Avoid >4 levels of dependencies
2. **Parallelize when possible** - Identify independent tasks
3. **Descriptive task IDs** - Use semantic names (design-api, not task1)
4. **Backend selection** - Match backend to task type
5. **Clear dependencies** - Explicitly declare all dependencies

This workflow demonstrates a complete development cycle from design through deployment using intelligent task orchestration.
