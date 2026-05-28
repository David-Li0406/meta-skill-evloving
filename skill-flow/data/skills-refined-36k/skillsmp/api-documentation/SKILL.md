---
name: api-documentation
description: API 文档生成工具。适用于任何后端技术栈的 API 接口文档生成和维护，确保前后端接口规范统一。
---

# API 文档生成

## 概述

本技能用于生成和维护 API 接口文档，提供标准化的文档格式和规范。适用于任何后端技术栈（Java、Python、Node.js、Go 等）和任何前端框架（React、Vue、Angular 等）。

## 适用范围

|| 后端技术栈 | 支持框架 |
||-------------|----------|
|| Java | Spring Boot, JAX-RS, Vert.x |
|| Python | Flask, FastAPI, Django |
|| JavaScript | Express, NestJS, Koa |
|| Go | Gin, Echo, Fiber |
|| 其他 | 任何支持 HTTP 的框架 |

|| 前端技术 | 支持框架 |
||----------|----------|
|| JavaScript | React, Vue, Angular |
|| 移动端 | iOS, Android, Flutter, React Native |

## 使用场景

- 从后端代码生成 API 文档
- 从前端 API 调用代码生成文档
- 前后端联调时的接口规范确认
- 维护现有 API 文档
- 新项目初始化 API 文档

---

## API 文档格式标准

### 基本文档结构

每个 API 文档应包含以下部分：

```markdown
# {模块名} API

## 1. 基础信息
- Base URL
- 认证方式
- 通用响应格式

## 2. 接口列表
- 接口1
- 接口2
- ...

## 3. 错误码
- 错误码定义
- 错误处理建议
```

### 单个接口文档格式

```markdown
## 接口名称

**接口描述：** 简短描述接口功能
**功能说明：** 详细描述接口的业务用途
**接口地址：** /api/v1/endpoint
**请求方式：** GET/POST/PUT/DELETE/PATCH
**Content-Type：** application/json

**认证要求：** 需要/不需要 Token

**请求参数**：
| 参数名 | 位置 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|--------|
| id | Path | int | 是 | 资源ID | 123 |
| name | Body | string | 是 | 名称 | "测试" |

**请求示例**：
```json
{
  "name": "测试名称",
  "value": 100
}
```

**响应示例**：
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "id": 123,
    "name": "测试名称"
  },
  "timestamp": "2026-01-19T10:30:00Z"
}
```

**响应字段说明**：
| 字段名 | 类型 | 说明 |
|--------|------|------|
| code | int | 状态码 |
| message | string | 响应消息 |
| data | object | 实际数据 |
| timestamp | string | 响应时间戳 |

**错误响应示例**：
```json
{
  "code": 400,
  "message": "参数错误：name 不能为空",
  "error": "INVALID_PARAMETER"
}
```
```

---

## RESTful API 设计原则

### HTTP 方法使用规范

|| HTTP方法 | 用途 |幂等性 | 是否安全 |
|-----------|------|--------|----------|
| GET | 获取资源（查询）| 是 | 是 |
| POST | 创建资源（新增）| 否 | 否 |
| PUT | 完整更新资源 | 是 | 否 |
| PATCH | 部分更新资源 | 否 | 否 |
| DELETE | 删除资源 | 是 | 否 |

### URL 设计规范

#### 资源命名
- 使用名词复数形式
- 使用小写字母
- 使用连字符（-）分隔单词
- 使用层级关系表示嵌套资源

**示例**：
```
✅ 正确：
GET    /api/v1/users
GET    /api/v1/users/123
POST   /api/v1/users
PUT    /api/v1/users/123
DELETE  /api/v1/users/123

❌ 错误：
GET    /api/v1/getUsers
GET    /api/v1/user
GET    /api/v1/UserList
```

#### 查询参数
- 使用 Query 参数传递筛选条件
- 使用分页参数处理列表

**示例**：
```
GET /api/v1/users?page=1&pageSize=20&status=active

参数说明：
- page: 页码（从1开始）
- pageSize: 每页数量
- status: 状态筛选
```

### 分页规范

#### 标准分页参数
|| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|----------|--------|
| page | int | 否 | 1 | 页码（从1开始） |
| pageSize | int | 否 | 20 | 每页数量 |
| sortBy | string | 否 | id | 排序字段 |
| sortOrder | string | 否 | asc | 排序方向（asc/desc） |

#### 响应格式
```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "id": 1,
      "name": "item1"
    }
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

### 标准 CRUD 接口命名

以下命名方式是业界广泛使用的标准命名规范：

||| 功能 | 路由命名 | HTTP方法 | 说明 |
||------|----------|----------|------|
|| 分页查询 | `/{module}/queryByPage` | POST | 支持分页、模糊搜索、多条件筛选 |
|| 查询全部 | `/{module}/queryAll` | GET | 查询所有数据 |
|| 按ID查询 | `/{module}/queryById` | GET | 根据ID查询单条记录 |
|| 新增 | `/{module}/insert` | POST | 新增数据 |
|| 更新 | `/{module}/update` | PUT | 更新数据（完整更新） |
|| 删除 | `/{module}/delete` | DELETE | 根据ID删除数据 |

**命名说明**：
- `{module}` 替换为你的资源名称（如 `users`, `orders`, `products`）
- POST 用于分页查询是因为查询条件可能较复杂，放在请求体中更合理

**示例**：
```
POST   /api/v1/users/queryByPage   - 分页查询用户列表
GET    /api/v1/users/queryAll      - 查询所有用户
GET    /api/v1/users/queryById?id=123  - 查询ID为123的用户
POST   /api/v1/users/insert        - 新增用户
PUT    /api/v1/users/update        - 更新用户信息
DELETE /api/v1/users/delete?id=123 - 删除ID为123的用户
```

---

## 通用响应格式

### 成功响应格式

```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    // 具体数据
  }
}
```

### 列表查询响应格式

```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    // 数据列表
  ],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

### 错误响应格式

```json
{
  "code": 400,
  "message": "参数错误：name 不能为空",
  "error": "INVALID_PARAMETER",
  "details": {
    "field": "name",
    "constraint": "NOT_NULL"
  }
}
```

---

## 状态码规范

### HTTP 状态码

|| 状态码 | 说明 | 使用场景 |
|---------|------|----------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 删除成功（无返回内容） |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 资源冲突 |
| 500 | Internal Server Error | 服务器内部错误 |

### 业务状态码（自定义）

业务状态码应在响应体的 `code` 字段中返回，而不是 HTTP 状态码。

|| code 类型 | 说明 | 示例 |
|-----------|------|------|
| 200-299 | 成功 | 200（成功）、201（创建成功） |
| 400-499 | 客户端错误 | 400（参数错误）、401（未认证） |
| 500-599 | 服务器错误 | 500（服务器错误）、503（服务不可用） |

---

## 参数传递方式

### 1. Path 参数（路径参数）

用于标识资源。

**示例**：
```
GET /api/v1/users/123
DELETE /api/v1/users/123
PUT /api/v1/users/123
```

**参数**：`123`（用户的 ID）

### 2. Query 参数（查询参数）

用于筛选、排序、分页。

**示例**：
```
GET /api/v1/users?page=1&pageSize=20&status=active&sortBy=createdAt
```

**参数**：
- `page`: 页码
- `pageSize`: 每页数量
- `status`: 状态筛选
- `sortBy`: 排序字段

### 3. Body 参数（请求体）

用于创建、更新资源。

**示例**：
```
POST /api/v1/users
Content-Type: application/json

{
  "name": "张三",
  "email": "zhangsan@example.com",
  "age": 25
}
```

### 4. Header 参数（请求头）

用于认证、传递元信息。

**示例**：
```
Authorization: Bearer {token}
Content-Type: application/json
X-Request-ID: 123456
```

---

## 认证方式

### Bearer Token（推荐）

**请求头**：
```
Authorization: Bearer {token}
```

**示例**：
```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \
  https://api.example.com/users
```

### API Key

**请求头**：
```
X-API-Key: {api_key}
```

### Basic Auth

**请求头**：
```
Authorization: Basic {base64(username:password)}
```

---

## 错误处理规范

### 错误响应必须包含

1. **错误码**：明确的错误标识
2. **错误消息**：用户可读的错误描述
3. **错误详情**（可选）：更多上下文信息

### 错误分类

|| 错误类型 | HTTP状态码 | 业务码 | 说明 |
|-----------|-------------|---------|------|
| 参数错误 | 400 | 4001 | 缺少必填参数、参数类型错误 |
| 认证错误 | 401 | 4002 | Token 无效或过期 |
| 权限错误 | 403 | 4003 | 无权限访问资源 |
| 资源不存在 | 404 | 4004 | 请求的资源不存在 |
| 资源冲突 | 409 | 4005 | 资源已存在或状态冲突 |
| 服务器错误 | 500 | 5001 | 服务器内部错误 |

### 错误响应示例

**参数错误**：
```json
{
  "code": 400,
  "message": "参数错误：email 格式不正确",
  "error": "INVALID_EMAIL_FORMAT",
  "details": {
    "field": "email",
    "value": "invalid-email",
    "constraint": "EMAIL_FORMAT"
  }
}
```

**认证错误**：
```json
{
  "code": 401,
  "message": "认证失败：Token 已过期，请重新登录",
  "error": "TOKEN_EXPIRED"
}
```

---

## 数据类型规范

### JSON 数据类型

|| JSON类型 | 说明 | 示例 |
|-----------|------|--------|
| string | 字符串 | "hello" |
| number | 数字（整数或浮点数）| 123, 3.14 |
| boolean | 布尔值 | true, false |
| array | 数组 | [1, 2, 3] |
| object | 对象 | {"key": "value"} |
| null | 空值 | null |

### 日期时间格式

推荐使用 ISO 8601 格式：

```json
{
  "createdAt": "2026-01-19T10:30:00Z",
  "updatedAt": "2026-01-19T10:30:00+08:00"
}
```

### 枚举值

文档中应明确列出所有可能的值：

```markdown
**status（状态）**：
| 值 | 说明 |
|-----|------|
| active | 激活 |
| inactive | 未激活 |
| deleted | 已删除 |
```

---

## 版本控制

### URL 版本控制（推荐）

```
/api/v1/users
/api/v2/users
```

### Header 版本控制

```
Accept: application/vnd.myapi.v1+json
```

### 向后兼容原则

- 新增接口：使用新版本号
- 修改接口：在原有接口基础上扩展，保持旧参数兼容
- 废弃接口：返回 `Warning` Header，明确废弃时间

---

## API 文档生成提示词

### 从后端代码生成 API 文档

```prompt
根据当前控制器代码生成 API 文档，要求：

1. 提取所有接口（路由、方法、参数、响应）
2. 按照标准文档格式组织内容
3. 包含完整的请求和响应示例
4. 标注认证要求
5. 列出可能的错误码
```

### 从前端代码生成 API 文档

```prompt
根据当前 API 调用代码生成接口文档，要求：

1. 提取所有 API 调用（URL、方法、参数）
2. 分析请求和响应的数据结构
3. 生成标准的接口文档格式
4. 补充业务说明和错误处理
```

### 文档质量检查

```prompt
检查 API 文档的质量：

1. 是否包含所有必需的字段（接口名称、地址、方法、参数、响应）
2. 示例是否完整且可执行
3. 错误码是否完整且有说明
4. 数据类型是否准确
5. 是否符合 RESTful 设计原则
```

---

## 文档命名规范

|| 文档类型 | 命名格式 | 示例 |
|-----------|-----------|------|
| 通用规范 | `README.md` | API 文档首页 |
| 模块文档 | `{module}-api.md` | `user-api.md` |
| 错误码 | `error-codes.md` | 错误码定义 |
| 认证说明 | `authentication.md` | 认证方式说明 |

---

## 文档维护建议

1. **保持同步**：API 变更后及时更新文档
2. **版本控制**：重要变更记录版本号和变更内容
3. **示例更新**：确保所有示例代码可执行
4. **错误码完整**：新增错误码时及时补充说明
5. **定期审查**：定期检查文档与实际接口的一致性

---

## 最佳实践

### 文档编写

- ✅ 使用简洁清晰的语言
- ✅ 提供完整的示例代码
- ✅ 标注必填参数和可选参数
- ✅ 说明参数的取值范围和默认值
- ✅ 包含错误处理说明
- ❌ 避免使用技术术语
- ❌ 避免模糊不清的描述

### 接口设计

- ✅ 遵循 RESTful 设计原则
- ✅ 使用标准的 HTTP 状态码
- ✅ 提供清晰的错误消息
- ✅ 支持分页和筛选
- ❌ 避免使用自定义动词
- ❌ 避免返回大文档对象

---

## 相关资源

- [RESTful API 设计最佳实践](https://restfulapi.net/)
- [HTTP 状态码规范](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status)
- [JSON API 规范](https://jsonapi.org/)
- [OpenAPI 规范](https://swagger.io/specification/)
