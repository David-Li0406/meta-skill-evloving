# Level 5: System Design & Architecture Examples

Multi-module projects, microservices, complete applications using `gpt-5.2` model (auto-selected) with extended timeout. Full parallel execution with multi-phase task decomposition.

---

## Example 1: Authentication Microservice

Complete authentication service with JWT, OAuth2, and RBAC permission model.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: auth-service
backend: codex
workdir: /home/user/services/auth
model: gpt-5.2
timeout: 300
---CONTENT---
设计并实现用户认证微服务（Python FastAPI）：
1. JWT token生成和验证
2. OAuth2授权流程（Authorization Code）
3. RBAC权限模型（角色-权限映射）
4. 用户注册、登录、密码重置
5. 包含数据库模型、API端点、中间件
6. 添加日志和错误处理
---END---
EOF
```

### Expected Output Structure

```
services/auth/
├── main.py              # FastAPI应用入口
├── models.py            # 数据库模型（User, Role, Permission）
├── schemas.py           # Pydantic schemas
├── auth/
│   ├── jwt.py          # JWT生成和验证
│   ├── oauth2.py       # OAuth2流程
│   └── rbac.py         # 权限检查
├── api/
│   ├── users.py        # 用户管理端点
│   ├── auth.py         # 认证端点
│   └── admin.py        # 管理端点
├── middleware/
│   ├── auth_middleware.py
│   └── logging_middleware.py
├── config.py           # 配置管理
├── database.py         # 数据库连接
├── requirements.txt
└── tests/
    ├── test_auth.py
    └── test_api.py
```

### Key Features Generated

**JWT Implementation**:
```python
# auth/jwt.py
from datetime import datetime, timedelta
import jwt

def create_access_token(data: dict, expires_delta: timedelta = None):
    """生成JWT访问令牌"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    """验证JWT令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
```

**RBAC Permission Check**:
```python
# auth/rbac.py
def require_permission(permission: str):
    """装饰器：检查用户权限"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get('current_user')
            if not user.has_permission(permission):
                raise HTTPException(403, "Permission denied")
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# 使用示例
@app.delete("/users/{user_id}")
@require_permission("users.delete")
async def delete_user(user_id: int, current_user: User):
    ...
```

**API Endpoints**:
```python
# api/auth.py
@router.post("/register")
async def register(user: UserCreate):
    """用户注册"""
    ...

@router.post("/login")
async def login(credentials: OAuth2PasswordRequestForm):
    """用户登录（返回JWT）"""
    ...

@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """刷新访问令牌"""
    ...

@router.post("/reset-password")
async def reset_password(email: str):
    """发送密码重置邮件"""
    ...
```

---

## Example 2: Event-Driven System

Design event-driven architecture with message queues, event sourcing, and CQRS pattern.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: event-system
backend: codex
workdir: /home/user/services/events
model: gpt-5.2
timeout: 300
---CONTENT---
设计事件驱动架构（Python）：
1. 消息队列集成（RabbitMQ或Redis）
2. 事件溯源（Event Sourcing）
3. CQRS模式（命令查询职责分离）
4. 事件总线和事件处理器
5. 最终一致性处理
6. 包含示例：订单处理流程
---END---
EOF
```

### Expected Architecture

```
services/events/
├── event_bus.py         # 事件总线
├── event_store.py       # 事件存储
├── commands/
│   ├── create_order.py
│   └── cancel_order.py
├── events/
│   ├── order_created.py
│   └── order_cancelled.py
├── handlers/
│   ├── order_handler.py
│   ├── inventory_handler.py
│   └── notification_handler.py
├── projections/
│   ├── order_view.py    # 查询模型
│   └── inventory_view.py
└── infrastructure/
    ├── rabbitmq.py
    └── redis.py
```

### Key Concepts Generated

**Event Bus**:
```python
class EventBus:
    """事件总线"""
    def __init__(self):
        self.handlers = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable):
        """订阅事件"""
        self.handlers[event_type].append(handler)

    async def publish(self, event: Event):
        """发布事件"""
        for handler in self.handlers[event.type]:
            await handler(event)
```

**Event Sourcing**:
```python
class EventStore:
    """事件存储"""
    def append(self, aggregate_id: str, event: Event):
        """追加事件"""
        ...

    def get_events(self, aggregate_id: str) -> List[Event]:
        """获取聚合根的所有事件"""
        ...

    def rebuild_aggregate(self, aggregate_id: str) -> Aggregate:
        """从事件流重建聚合根"""
        events = self.get_events(aggregate_id)
        aggregate = Aggregate(aggregate_id)
        for event in events:
            aggregate.apply(event)
        return aggregate
```

**CQRS Pattern**:
```python
# 命令端（写）
class CreateOrderCommand:
    def execute(self, order_data):
        order = Order.create(order_data)
        event = OrderCreatedEvent(order)
        event_bus.publish(event)

# 查询端（读）
class OrderView:
    def get_order(self, order_id):
        """从投影（Projection）读取"""
        return projection_db.get(order_id)
```

---

## Example 3: Full-Stack Blog System (Parallel DAG)

Complete blog system with backend API, frontend React app, and Docker deployment.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: design
backend: codex
workdir: /home/user/blog
model: gpt-5.2
---CONTENT---
设计博客系统架构（数据库schema、API规范、前端组件结构）
---END---

---TASK---
id: backend
backend: codex
workdir: /home/user/blog/api
model: gpt-5.2
dependencies: design
timeout: 180
---CONTENT---
实现FastAPI后端：用户、文章、评论、标签CRUD，JWT认证
---END---

---TASK---
id: frontend
backend: codex
workdir: /home/user/blog/web
model: gpt-5.2
dependencies: design
timeout: 180
---CONTENT---
实现React前端：文章列表、详情页、编辑器、用户认证UI
---END---

---TASK---
id: deploy
backend: codex
workdir: /home/user/blog
dependencies: backend, frontend
---CONTENT---
生成Docker Compose配置：后端、前端、PostgreSQL、Nginx反向代理
---END---
EOF
```

### Execution Flow

```
        design
       /      \
  backend    frontend
       \      /
        deploy
```

### Generated Structure

```
blog/
├── api/                 # FastAPI后端
│   ├── main.py
│   ├── models/
│   ├── routers/
│   └── Dockerfile
├── web/                 # React前端
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── api/
│   └── Dockerfile
├── docker-compose.yml
└── nginx.conf
```

---

## Example 4: Microservices Architecture

Design a complete microservices system with API Gateway, service discovery, and distributed tracing.

### Command

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: microservices
backend: codex
workdir: /home/user/microservices
model: gpt-5.2
timeout: 600
---CONTENT---
设计并实现微服务架构：
1. API Gateway（Kong或自建）
2. 服务注册与发现（Consul）
3. 配置中心（etcd）
4. 分布式追踪（Jaeger）
5. 服务间通信（gRPC + REST）
6. 包含3个示例服务：用户服务、订单服务、支付服务
7. Docker Compose编排
---END---
EOF
```

### Generated Components

- Service mesh configuration
- gRPC service definitions (.proto files)
- API Gateway routing rules
- Health check endpoints
- Circuit breaker implementation
- Distributed logging aggregation

---

## Common Level 5 Task Patterns

### Microservices
- Service architecture design
- API gateway implementation
- Service discovery and registration
- Inter-service communication (gRPC, REST, message queues)

### Backend Systems
- Complete REST APIs (CRUD, auth, file upload)
- GraphQL servers
- Real-time systems (WebSocket, SSE)
- Background job processing (Celery, RQ)

### DevOps & Infrastructure
- Docker multi-container setups
- Kubernetes manifests
- CI/CD pipelines (GitHub Actions, Jenkins)
- Infrastructure as Code (Terraform, Ansible)

### Distributed Systems
- Consensus algorithms (Raft, Paxos)
- Distributed caching (Redis Cluster)
- Load balancing strategies
- Data sharding and replication

---

## Example 5: E-Commerce Platform with Full Auto-Decomposition

This example demonstrates L5 full capabilities: automatic multi-service decomposition, cross-service dependency analysis, and maximum parallel execution.

### Single Task Input (Auto-Decomposed into Microservices)

```bash
memex-cli run --backend codex --stdin <<'EOF'
---TASK---
id: ecommerce-platform
backend: codex
model: gpt-5.2
workdir: ./platform
timeout: 600
---CONTENT---
设计并实现电商平台微服务架构：

服务列表：
1. 用户服务 (services/user/) - 注册、登录、个人信息
2. 商品服务 (services/product/) - 商品CRUD、分类、搜索
3. 订单服务 (services/order/) - 订单创建、状态管理、历史
4. 支付服务 (services/payment/) - 支付网关集成、退款
5. 通知服务 (services/notification/) - 邮件、短信、推送

基础设施：
6. API网关 (gateway/) - 路由、限流、认证
7. 共享库 (shared/) - 通用模型、工具函数
8. 数据库迁移 (migrations/) - 所有服务的schema
9. Docker编排 (docker/) - Compose + K8s配置
10. 集成测试 (tests/) - 端到端测试

要求：
- FastAPI + SQLAlchemy
- gRPC服务间通信
- Redis缓存
- RabbitMQ消息队列
- JWT认证
---END---
EOF
```

### Auto-Decomposition Process (5-Phase Architecture)

```
▶ Task Decomposition Analysis
  Input: 1 complex task (microservices platform)
  Detected Components: 10 modules
  Generated Subtasks: 15 (some modules split further)

  Decomposition Strategy: Layered Architecture
  ┌────────────────────────────────────────────────────────────────────┐
  │ Phase 1: Foundation (No deps)                                      │
  │   - shared-models (shared/models.py)                               │
  │   - shared-utils (shared/utils.py)                                 │
  │   - shared-config (shared/config.py)                               │
  │                                                                    │
  │ Phase 2: Data Layer (Parallel, depends on Phase 1)                 │
  │   - migrations-user (migrations/user.sql)                          │
  │   - migrations-product (migrations/product.sql)                    │
  │   - migrations-order (migrations/order.sql)                        │
  │                                                                    │
  │ Phase 3: Core Services (Parallel, depends on Phase 2)              │
  │   - service-user (services/user/)                                  │
  │   - service-product (services/product/)                            │
  │   - service-payment (services/payment/)                            │
  │   - service-notification (services/notification/)                  │
  │                                                                    │
  │ Phase 4: Orchestration Services (Parallel, depends on Phase 3)     │
  │   - service-order (services/order/) - depends on user,product,pay  │
  │   - gateway (gateway/) - depends on all services                   │
  │                                                                    │
  │ Phase 5: Infrastructure & Testing (Parallel, depends on Phase 4)   │
  │   - docker-config (docker/)                                        │
  │   - integration-tests (tests/)                                     │
  └────────────────────────────────────────────────────────────────────┘
```

### Auto-Generated Dependency Graph

```
▶ Dependency Analysis
  Cross-Service Dependencies Detected:
    - order imports user, product, payment
    - gateway routes to all services
    - all services import shared/*
    - tests import all services

  Generated 5-Phase DAG:

Phase 1: Foundation (3 tasks parallel)
┌────────────┐  ┌────────────┐  ┌────────────┐
│ shared-    │  │ shared-    │  │ shared-    │
│ models     │  │ utils      │  │ config     │
│ 2.1s       │  │ 1.8s       │  │ 1.5s       │
└─────┬──────┘  └─────┬──────┘  └─────┬──────┘
      │               │               │
      └───────────────┼───────────────┘
                      ↓
Phase 2: Data Layer (3 tasks parallel)
┌────────────┐  ┌────────────┐  ┌────────────┐
│ migrations │  │ migrations │  │ migrations │
│ user       │  │ product    │  │ order      │
│ 1.2s       │  │ 1.4s       │  │ 1.6s       │
└─────┬──────┘  └─────┬──────┘  └─────┬──────┘
      │               │               │
      └───────────────┼───────────────┘
                      ↓
Phase 3: Core Services (4 tasks parallel)
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ service-    │ │ service-    │ │ service-    │ │ service-    │
│ user        │ │ product     │ │ payment     │ │ notification│
│ 8.5s        │ │ 9.2s        │ │ 7.8s        │ │ 6.4s        │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │               │
       └───────────────┼───────────────┴───────────────┘
                       ↓
Phase 4: Orchestration (2 tasks parallel)
         ┌─────────────────┐  ┌─────────────────┐
         │ service-order   │  │ gateway         │
         │ 10.3s           │  │ 8.7s            │
         └────────┬────────┘  └────────┬────────┘
                  │                    │
                  └──────────┬─────────┘
                             ↓
Phase 5: Infrastructure (2 tasks parallel)
         ┌─────────────────┐  ┌─────────────────┐
         │ docker-config   │  │ integration-    │
         │ 4.2s            │  │ tests 6.8s      │
         └─────────────────┘  └─────────────────┘
```

### Execution Output

```
▶ Executing ecommerce-platform with auto-decomposition

▶ Phase 1: Foundation (3 tasks parallel)
  » Executing 3 tasks in parallel...

  ✓ shared-models 2.1s
    » 写入 shared/models.py (User, Product, Order 基础模型)
  ✓ shared-utils 1.8s
    » 写入 shared/utils.py (JWT, 加密, 分页工具)
  ✓ shared-config 1.5s
    » 写入 shared/config.py (环境变量, 数据库配置)

▶ Phase 2: Data Layer (3 tasks parallel)
  » Executing 3 tasks in parallel...

  ✓ migrations-user 1.2s
    » 写入 migrations/001_user.sql
  ✓ migrations-product 1.4s
    » 写入 migrations/002_product.sql
  ✓ migrations-order 1.6s
    » 写入 migrations/003_order.sql

▶ Phase 3: Core Services (4 tasks parallel)
  » Executing 4 tasks in parallel...

  ✓ service-user 8.5s
    » 写入 services/user/main.py
    » 写入 services/user/routes.py
    » 写入 services/user/service.py
    » 写入 services/user/grpc_server.py
  ✓ service-product 9.2s
    » 写入 services/product/main.py
    » 写入 services/product/routes.py
    » 写入 services/product/search.py (Elasticsearch集成)
  ✓ service-payment 7.8s
    » 写入 services/payment/main.py
    » 写入 services/payment/stripe.py
    » 写入 services/payment/alipay.py
  ✓ service-notification 6.4s
    » 写入 services/notification/main.py
    » 写入 services/notification/email.py
    » 写入 services/notification/sms.py

▶ Phase 4: Orchestration (2 tasks parallel)
  » Executing 2 tasks in parallel...

  ✓ service-order 10.3s
    » 写入 services/order/main.py
    » 写入 services/order/workflow.py (状态机)
    » 写入 services/order/saga.py (分布式事务)
  ✓ gateway 8.7s
    » 写入 gateway/main.py
    » 写入 gateway/routes.py
    » 写入 gateway/middleware.py (限流, 认证)

▶ Phase 5: Infrastructure (2 tasks parallel)
  » Executing 2 tasks in parallel...

  ✓ docker-config 4.2s
    » 写入 docker/docker-compose.yml
    » 写入 docker/docker-compose.prod.yml
    » 写入 docker/k8s/ (Deployment, Service, ConfigMap)
  ✓ integration-tests 6.8s
    » 写入 tests/test_e2e.py
    » 写入 tests/test_saga.py
    » 写入 tests/conftest.py

═══════════════════════════════════════════════════════════════════════
✓ ecommerce-platform completed
  Phases: 5
  Subtasks: 15
  Total Time: 42.8s (vs 89.2s serial = 52% faster)

  Generated Structure:
  platform/
  ├── shared/
  │   ├── models.py
  │   ├── utils.py
  │   └── config.py
  ├── migrations/
  │   ├── 001_user.sql
  │   ├── 002_product.sql
  │   └── 003_order.sql
  ├── services/
  │   ├── user/
  │   ├── product/
  │   ├── order/
  │   ├── payment/
  │   └── notification/
  ├── gateway/
  ├── docker/
  │   ├── docker-compose.yml
  │   └── k8s/
  └── tests/

  Services: 5
  Files: 35+
═══════════════════════════════════════════════════════════════════════
```

### L5 Execution Features

| Feature | Description |
|---------|-------------|
| **Multi-Service Decomposition** | 1 task → 5 microservices + infra |
| **Cross-Service Dependency** | Auto-detect inter-service imports |
| **5-Phase Execution** | Foundation → Data → Core → Orchestration → Infra |
| **Maximum Parallelization** | 4 services in parallel (Phase 3) |
| **Performance Gain** | 52% faster than serial |

### Comparison: L3 vs L4 vs L5

| Feature | L3 | L4 | L5 |
|---------|:--:|:--:|:--:|
| Task Decomposition | ✅ | ✅ | ✅ |
| Dependency Analysis | ✅ | ✅ | ✅ |
| Parallel Execution | ✅ | ✅ | ✅ |
| Multi-file output | ✅ | ✅ | ✅ |
| **Multi-service decomposition** | ❌ | ❌ | ✅ |
| **Cross-service dependency** | ❌ | ❌ | ✅ |
| **5+ phase execution** | ❌ | ❌ | ✅ |
| **Infrastructure generation** | ❌ | ❌ | ✅ |

---

## Model Selection for Level 5

| Task Type | Model | Timeout | Execution |
|-----------|-------|---------|-----------|
| Microservices | `gpt-5.2` | 300-600s | Multi-phase parallel |
| Full-stack apps | `gpt-5.2` | 300s | 4-phase decomposition |
| DevOps configs | `gpt-5.2` | 180s | Parallel infrastructure |
| Distributed systems | `gpt-5.2` | 600s | Maximum parallelization |

**L5 Execution Features:**
- Automatic multi-service decomposition
- Cross-service dependency detection
- 5+ phase execution planning
- Maximum parallel execution
- Infrastructure generation (Docker, K8s)

---

## Tips for Level 5 Tasks

1. **Use DAGs**: Break into parallel subtasks (design → backend + frontend → deploy)
2. **Design first**: Always start with architecture design task
3. **Increase timeout**: Use 300-600s for multi-file generation
4. **Be specific**: Specify frameworks, databases, deployment targets
5. **Iterate**: Start with MVP, then add features in follow-up tasks
6. **Review carefully**: Check security, error handling, and configuration

---

## Advanced Workflow Example

### Multi-Phase Backend Service

```bash
memex-cli run --backend codex --stdin <<'EOF'
# Phase 1: Architecture
---TASK---
id: architecture
backend: codex
model: gpt-5.2
---CONTENT---
设计订单管理系统架构（包含数据库schema、API规范、部署架构图）
---END---

# Phase 2: Core modules (parallel)
---TASK---
id: models
backend: codex
model: gpt-5.2
dependencies: architecture
---CONTENT---
实现数据库模型和仓储模式
---END---

---TASK---
id: business-logic
backend: codex
model: gpt-5.2
dependencies: architecture
---CONTENT---
实现业务逻辑层（订单创建、支付、发货流程）
---END---

# Phase 3: API layer
---TASK---
id: api
backend: codex
model: gpt-5.2
dependencies: models, business-logic
---CONTENT---
实现REST API端点和OpenAPI文档
---END---

# Phase 4: Testing & deployment
---TASK---
id: tests
backend: codex
model: gpt-5.2
dependencies: api
---CONTENT---
编写单元测试和集成测试
---END---

---TASK---
id: deploy
backend: codex
model: gpt-5.2
dependencies: api
---CONTENT---
生成Docker、K8s、CI/CD配置
---END---
EOF
```

---

## Related Resources

- [references/complexity-guide.md](../references/complexity-guide.md) - Level 5 detailed guidance
- [examples/level4-algorithms.md](./level4-algorithms.md) - Algorithm implementation
- [skills/memex-cli/references/advanced-usage.md](../../memex-cli/references/advanced-usage.md) - DAG workflows
- [skills/memex-cli/examples/parallel-tasks.md](../../memex-cli/examples/parallel-tasks.md) - Parallel execution
