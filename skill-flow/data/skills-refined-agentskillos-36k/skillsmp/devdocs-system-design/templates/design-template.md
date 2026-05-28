# System Design Document Template

Use this template to generate `docs/devdocs/02-system-design.md`.

```markdown
# 系统设计：<功能名称>

## 1. 运行平台

- **目标平台**：<Web/iOS/Android/Desktop/Server/跨平台>
- **最低版本**：<如 iOS 14+, Android 8+, Chrome 90+>
- **部署环境**：<云服务商/私有化/混合>

## 2. 架构概览

```mermaid
graph TD
    Client[Client] --> AGW[API Gateway]
    AGW --> SVC[Service Layer]
    SVC --> DB[(Database)]
```

### 分层架构 (MTE 模式)

```mermaid
graph BT
    Infra[Infrastructure Layer] -.-> Domain[Domain Layer]
    Service[Service Layer] --> Domain
    Interface[Interface Layer] --> Service
```


## 3. 技术选型

> 用户偏好：<用户指定的技术栈 / 无偏好>

| 类别 | 选择 | 理由 |
|------|------|------|
| 语言 | <tech> | <why> |
| 框架 | <tech> | <why> |
| 数据库 | <tech> | <why> |
| 缓存 | <tech> | <why> |
| 消息队列 | <tech> | <why> |
| 测试框架 | <tech> | <why> |

## 4. 模块设计

| 模块 | 职责 | 依赖 |
|------|------|------|
| <name> | <职责描述（单一职责）> | <依赖模块> |

### 4.1 <模块名称>

**职责**：<详细描述>

**关键组件**：
- 组件 A：<描述>
- 组件 B：<描述>

**可测试性**：
- 核心逻辑无外部依赖
- 外部依赖通过接口注入

## 5. 核心接口 (面向接口设计)

> **原则**：只定义方法签名、参数及返回值，**严禁包含任何实现代码或内部逻辑细节**。

### 5.1 服务层接口

#### IUserService

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `createUser` | `CreateUserDTO` | `User` | 创建用户 |
| `getUserById` | `string` | `User \| null` | 根据ID查询 |
| `updateUser` | `string, UpdateUserDTO` | `User` | 更新用户信息 |
| `deleteUser` | `string` | `void` | 删除用户 |

### 5.2 数据访问接口

#### IUserRepository

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `save` | `User` | `User` | 保存用户 |
| `findById` | `string` | `User \| null` | 根据ID查询 |
| `findByEmail` | `string` | `User \| null` | 根据邮箱查询 |
| `delete` | `string` | `void` | 删除用户 |

### 5.3 外部服务接口

#### IEmailService

| 方法 | 参数 | 返回值 | 说明 |
|------|------|--------|------|
| `send` | `EmailMessage` | `boolean` | 发送邮件 |

## 6. 设计模式

> 只在必要时使用，说明解决什么问题

| 模式 | 应用位置 | 解决的问题 |
|------|----------|------------|
| Factory | `UserFactory` | 根据类型创建不同用户对象 |
| Strategy | `PaymentStrategy` | 支持多种支付方式，运行时切换 |
| Repository | `UserRepository` | 数据访问抽象，便于测试和替换存储 |
| Observer | `EventBus` | 模块间解耦，异步事件通知 |

### 模式说明

#### Factory 模式

**问题**：需要根据用户类型创建不同的用户对象
**方案**：使用 Factory 封装创建逻辑

```
UserFactory
├── createNormalUser(dto) -> NormalUser
├── createVipUser(dto) -> VipUser
└── createAdminUser(dto) -> AdminUser
```

#### Strategy 模式

**问题**：支付方式多样，需要运行时切换
**方案**：定义 PaymentStrategy 接口，各支付方式实现该接口

```
IPaymentStrategy
├── AlipayStrategy
├── WechatPayStrategy
└── CreditCardStrategy
```

## 7. 代码结构

```
src/
├── api/                    # 接口层
│   ├── controllers/        # 控制器
│   │   └── UserController.ts
│   ├── middlewares/        # 中间件
│   │   ├── auth.ts
│   │   └── errorHandler.ts
│   └── validators/         # 请求验证
│       └── userValidator.ts
├── services/               # 服务层
│   ├── interfaces/         # 服务接口
│   │   └── IUserService.ts
│   └── impl/               # 服务实现
│       └── UserService.ts
├── domain/                 # 领域层
│   ├── entities/           # 实体
│   │   └── User.ts
│   ├── value-objects/      # 值对象
│   │   └── Email.ts
│   └── events/             # 领域事件
│       └── UserCreatedEvent.ts
├── infrastructure/         # 基础设施层
│   ├── repositories/       # 仓储实现
│   │   └── UserRepository.ts
│   ├── external/           # 外部服务
│   │   └── EmailService.ts
│   └── config/             # 配置
│       └── database.ts
└── shared/                 # 共享
    ├── types/              # 类型
    ├── utils/              # 工具
    └── constants/          # 常量
```

## 8. 数据模型

### 8.1 实体定义

#### User

| 字段 | 类型 | 说明 | 索引 |
|------|------|------|------|
| id | string/uuid | 主键 | PK |
| email | string | 邮箱 | UNIQUE |
| name | string | 用户名 | - |
| status | enum | 状态 | IDX |
| created_at | timestamp | 创建时间 | IDX |
| updated_at | timestamp | 更新时间 | - |

### 8.2 实体关系

```
User 1──* Order
Order *──* Product
```

### 8.3 索引策略

| 表 | 索引名 | 字段 | 类型 | 用途 |
|----|--------|------|------|------|
| user | idx_email | email | UNIQUE | 登录查询 |
| user | idx_status_created | status, created_at | B-tree | 列表查询 |

## 9. API 设计

### 9.1 创建用户

- **方法**：`POST`
- **路径**：`/api/v1/users`
- **描述**：创建新用户
- **认证**：需要

**请求**：
```json
{
  "email": "user@example.com",
  "name": "张三",
  "password": "******"
}
```

**响应（成功）**：
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": "usr_xxx",
    "email": "user@example.com",
    "name": "张三",
    "created_at": "2024-01-01T00:00:00Z"
  }
}
```

**响应（错误）**：
```json
{
  "code": 1001,
  "message": "邮箱已存在",
  "details": {
    "field": "email",
    "reason": "duplicate"
  }
}
```

## 10. 状态流转

### 10.1 用户状态

```
┌─────────┐   activate   ┌─────────┐
│ Pending │─────────────>│ Active  │
└─────────┘              └─────────┘
                              │
                              │ suspend
                              v
                         ┌─────────┐
                         │Suspended│
                         └─────────┘
```

| 当前状态 | 事件 | 目标状态 | 副作用 |
|----------|------|----------|--------|
| Pending | activate | Active | 发送欢迎邮件 |
| Active | suspend | Suspended | 记录日志 |

## 11. 异常处理

### 11.1 错误码设计

| 码段 | 类别 | 说明 |
|------|------|------|
| 1000-1999 | 客户端错误 | 参数校验、认证失败 |
| 2000-2999 | 业务错误 | 业务规则校验失败 |
| 3000-3999 | 系统错误 | 内部错误 |

### 11.2 错误码列表

| 错误码 | 消息 | 说明 | 处理策略 |
|--------|------|------|----------|
| 1001 | 参数无效 | 字段验证失败 | 返回字段详情 |
| 1002 | 未授权 | Token无效/过期 | 跳转登录 |
| 2001 | 资源不存在 | 实体不存在 | 返回 404 |
| 3001 | 内部错误 | 未预期错误 | 记录日志告警 |

## 12. 扩展性设计

### 12.1 当前设计限制

- 最大并发用户：<数量>
- 最大 QPS：<数量>
- 数据保留期：<周期>

### 12.2 扩展点

| 扩展点 | 当前实现 | 扩展方式 |
|--------|----------|----------|
| 支付方式 | 支付宝 | 实现 IPaymentStrategy |
| 通知渠道 | 邮件 | 实现 INotificationChannel |
| 存储方式 | MySQL | 实现 IUserRepository |

### 12.3 不做的设计

> 以下需求当前不考虑，避免过度设计

- [ ] 多租户支持（当前单租户）
- [ ] 国际化（当前中文）
- [ ] 分库分表（当前单库）

## 13. 需求追溯

> 确保每个功能点都有对应的设计实现

| 功能点 | 用户故事 | 实现模块 | 核心接口 | 数据实体 |
|--------|----------|----------|----------|----------|
| F-001 | US-001 | UserModule | IUserService.createUser | User |
| F-001 | US-002 | UserModule | IUserService.validatePassword | User |
| F-002 | US-003 | AuthModule | IAuthService.login | Session |

### 覆盖检查

- [ ] 所有功能点 (F-XXX) 都有对应模块
- [ ] 所有验收标准 (AC-XXX) 都有对应接口方法
- [ ] 无遗漏的功能点
```

## MTE 原则检查清单

设计完成后，检查是否满足 MTE 原则：

### Maintainability（可维护性）
- [ ] 每个模块职责单一
- [ ] 依赖关系清晰，无循环依赖
- [ ] 代码结构易于理解

### Testability（可测试性）
- [ ] 核心业务逻辑无外部依赖
- [ ] 外部依赖通过接口注入
- [ ] 可独立进行单元测试

### Extensibility（可扩展性）
- [ ] 预留了合理的扩展点
- [ ] 使用接口抽象，符合开闭原则
- [ ] 没有为假设需求过度设计

## Split File Guidelines

When document exceeds 300 lines, split as follows:

### 02-system-design.md (Main)
- Sections 1-7: Platform, Architecture, Tech Stack, Module, Interfaces, Patterns, Structure

### 02-system-design-api.md
- Section 9: Complete API Design
- Section 10: State Flow

### 02-system-design-data.md
- Section 8: Data Model
- Section 11: Error Handling
- Section 12: Extensibility
