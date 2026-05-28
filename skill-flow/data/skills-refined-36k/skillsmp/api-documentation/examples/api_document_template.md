# 用户管理 API

## 1. 基础信息

### Base URL
```
https://api.example.com/api/v1
```

### 认证方式
- Bearer Token（推荐）
- API Key

### Content-Type
```
application/json
```

### 通用响应格式

**成功响应**：
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    // 具体数据
  }
}
```

**错误响应**：
```json
{
  "code": 400,
  "message": "参数错误",
  "error": "INVALID_PARAMETER"
}
```

---

## 2. 接口列表

### 2.1 创建用户

**接口描述**：创建新用户账号

**功能说明**：根据提供的信息创建用户，创建成功后返回用户 ID

**接口地址**：`/api/v1/users/insert`

**请求方式**：`POST`

**认证要求**：需要 Token

**请求参数**：

|| 参数名 | 位置 | 类型 | 必填 | 说明 | 示例值 |
||--------|------|------|------|--------|--------|
|| username | Body | string | 是 | 用户名（3-50个字符） | "zhangsan" |
|| email | Body | string | 是 | 邮箱地址 | "zhangsan@example.com" |
|| password | Body | string | 是 | 密码（至少8个字符） | "password123" |
|| age | Body | int | 否 | 年龄 | 25 |
|| role | Body | string | 否 | 角色（user/admin） | "user" |

**请求示例**：
```bash
curl -X POST https://api.example.com/api/v1/users/insert \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "password": "password123",
    "age": 25,
    "role": "user"
  }'
```

**响应示例**：
```json
{
  "code": 200,
  "message": "用户创建成功",
  "data": {
    "id": 123,
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "age": 25,
    "role": "user",
    "createdAt": "2026-01-19T10:30:00Z"
  }
}
```

**错误响应示例**：

**邮箱已存在**：
```json
{
  "code": 409,
  "message": "邮箱已被使用",
  "error": "EMAIL_ALREADY_EXISTS"
}
```

**参数错误**：
```json
{
  "code": 400,
  "message": "参数错误：邮箱格式不正确",
  "error": "INVALID_EMAIL_FORMAT",
  "details": {
    "field": "email",
    "value": "invalid-email",
    "constraint": "EMAIL_FORMAT"
  }
}
```

---

### 2.2 分页查询用户列表

**接口描述**：分页查询用户列表

**功能说明**：支持分页、筛选、模糊搜索和排序

**接口地址**：`/api/v1/users/queryByPage`

**请求方式**：`POST`

**认证要求**：需要 Token

**请求参数**：

|| 参数名 | 位置 | 类型 | 必填 | 默认值 | 说明 | 示例值 |
||--------|------|------|------|----------|--------|--------|
|| page | Body | int | 否 | 1 | 页码（从1开始） | 1 |
|| pageSize | Body | int | 否 | 20 | 每页数量 | 20 |
|| role | Body | string | 否 | - | 角色筛选 | "admin" |
|| status | Body | string | 否 | - | 状态筛选（active/inactive） | "active" |
|| sortBy | Body | string | 否 | createdAt | 排序字段 | "username" |
|| sortOrder | Body | string | 否 | desc | 排序方向（asc/desc） | "asc" |
|| keyword | Body | string | 否 | - | 模糊搜索关键词 | "zhang" |

**请求示例**：
```bash
curl -X POST https://api.example.com/api/v1/users/queryByPage \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "page": 1,
    "pageSize": 20,
    "role": "admin",
    "status": "active",
    "sortBy": "username",
    "sortOrder": "asc"
  }'
```

**响应示例**：
```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin",
      "status": "active",
      "createdAt": "2026-01-01T00:00:00Z"
    },
    {
      "id": 2,
      "username": "user1",
      "email": "user1@example.com",
      "role": "user",
      "status": "active",
      "createdAt": "2026-01-05T10:00:00Z"
    }
  ],
  "total": 50
}
```

---

### 2.3 查询所有用户

**接口描述**：查询所有用户

**功能说明**：获取系统中所有用户（不分页）

**接口地址**：`/api/v1/users/queryAll`

**请求方式**：`GET`

**认证要求**：需要 Token

**请求示例**：
```bash
curl -X GET https://api.example.com/api/v1/users/queryAll \
  -H "Authorization: Bearer {token}"
```

**响应示例**：
```json
{
  "code": 200,
  "message": "查询成功",
  "data": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin",
      "status": "active",
      "createdAt": "2026-01-01T00:00:00Z"
    }
  ]
}
```

---

### 2.4 按ID查询用户

**接口描述**：根据 ID 查询用户详情

**功能说明**：获取指定用户的详细信息

**接口地址**：`/api/v1/users/queryById`

**请求方式**：`GET`

**认证要求**：需要 Token

**请求参数**：

|| 参数名 | 位置 | 类型 | 必填 | 说明 | 示例值 |
||--------|------|------|------|--------|--------|
|| id | Query | int | 是 | 用户 ID | 123 |

**请求示例**：
```bash
curl -X GET "https://api.example.com/api/v1/users/queryById?id=123" \
  -H "Authorization: Bearer {token}"
```

**响应示例**：
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "id": 123,
    "username": "zhangsan",
    "email": "zhangsan@example.com",
    "age": 25,
    "role": "user",
    "status": "active",
    "createdAt": "2026-01-19T10:30:00Z",
    "updatedAt": "2026-01-19T15:00:00Z"
  }
}
```

**错误响应示例**：

**用户不存在**：
```json
{
  "code": 404,
  "message": "用户不存在",
  "error": "USER_NOT_FOUND",
  "details": {
    "userId": 123
  }
}
```

---

### 2.5 更新用户

**接口描述**：更新用户信息

**功能说明**：更新指定用户的信息（完整更新）

**接口地址**：`/api/v1/users/update`

**请求方式**：`PUT`

**认证要求**：需要 Token

**请求参数**：

|| 参数名 | 位置 | 类型 | 必填 | 说明 | 示例值 |
||--------|------|------|------|--------|--------|
|| id | Body | int | 是 | 用户 ID | 123 |
|| username | Body | string | 否 | 用户名 | "zhangsan2" |
|| email | Body | string | 否 | 邮箱地址 | "newemail@example.com" |
|| age | Body | int | 否 | 年龄 | 26 |
|| status | Body | string | 否 | 状态 | "inactive" |

**请求示例**：
```bash
curl -X PUT https://api.example.com/api/v1/users/update \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "id": 123,
    "username": "zhangsan2",
    "email": "newemail@example.com",
    "age": 26
  }'
```

**响应示例**：
```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "id": 123,
    "username": "zhangsan2",
    "email": "newemail@example.com",
    "age": 26,
    "updatedAt": "2026-01-19T16:00:00Z"
  }
}
```

---

### 2.6 删除用户

**接口描述**：删除指定用户

**功能说明**：根据 ID 删除用户（软删除）

**接口地址**：`/api/v1/users/delete`

**请求方式**：`DELETE`

**认证要求**：需要 Token

**请求参数**：

|| 参数名 | 位置 | 类型 | 必填 | 说明 | 示例值 |
||--------|------|------|------|--------|--------|
|| id | Query | int | 是 | 用户 ID | 123 |

**请求示例**：
```bash
curl -X DELETE "https://api.example.com/api/v1/users/delete?id=123" \
  -H "Authorization: Bearer {token}"
```

**响应示例**：
```json
{
  "code": 200,
  "message": "删除成功"
}
```

**错误响应示例**：

**用户不存在**：
```json
{
  "code": 404,
  "message": "用户不存在",
  "error": "USER_NOT_FOUND",
  "details": {
    "userId": 123
  }
}
```

---

## 3. 错误码定义

|| 错误码 | HTTP状态 | 错误标识 | 说明 | 处理建议 |
||---------|-----------|-----------|------|----------|
|| 4001 | 400 | INVALID_PARAMETER | 参数错误 | 检查请求参数 |
|| 4002 | 401 | UNAUTHORIZED | 未认证 | 重新登录获取 Token |
|| 4003 | 403 | FORBIDDEN | 无权限 | 联系管理员授权 |
|| 4004 | 404 | NOT_FOUND | 资源不存在 | 检查资源 ID |
|| 4005 | 409 | CONFLICT | 资源冲突 | 检查资源状态 |
|| 4006 | 400 | INVALID_EMAIL_FORMAT | 邮箱格式错误 | 检查邮箱格式 |
|| 4007 | 409 | EMAIL_ALREADY_EXISTS | 邮箱已存在 | 更换邮箱地址 |
|| 5001 | 500 | INTERNAL_ERROR | 服务器内部错误 | 稍后重试或联系技术支持 |
|| 5002 | 503 | SERVICE_UNAVAILABLE | 服务不可用 | 稍后重试 |

---

## 4. 数据类型定义

### User（用户对象）

|| 字段名 | 类型 | 必填 | 说明 |
||--------|------|------|------|
|| id | int | 是 | 用户 ID |
|| username | string | 是 | 用户名（3-50个字符） |
|| email | string | 是 | 邮箱地址 |
|| age | int | 否 | 年龄（18-120） |
|| role | string | 是 | 角色（user/admin） |
|| status | string | 是 | 状态（active/inactive/deleted） |
|| createdAt | string | 是 | 创建时间（ISO 8601格式） |
|| updatedAt | string | 否 | 更新时间（ISO 8601格式） |

---

## 5. 限制说明

### 请求频率限制

- 普通用户：100次/分钟
- 超出限制返回：`429 Too Many Requests`

### 数据限制

- 用户名长度：3-50个字符
- 密码长度：至少8个字符
- 年龄范围：18-120岁

---

## 6. 版本历史

### v1.0.0 (2026-01-19)
- 初始版本
- 支持用户 CRUD 操作
- 实现分页查询

---

## 7. 常见问题

**Q: Token 过期后如何处理？**
A: Token 过期后会返回 `401 Unauthorized`，需要重新登录获取新 Token。

**Q: 分页查询的最大 pageSize 是多少？**
A: 最大 pageSize 为 100，超过限制会自动调整为 100。

**Q: 删除用户后能否恢复？**
A: 删除为软删除，可以通过后台操作恢复。

**Q: 邮箱修改是否需要验证？**
A: 修改邮箱后会发送验证邮件，需要点击验证链接完成修改。

---

## 8. 附录

### 认证流程

1. 用户使用用户名和密码登录
2. 服务器验证成功后返回 Token
3. 后续请求在 Header 中携带 Token
4. Token 有效期为 24 小时
5. Token 过期后重新登录获取新 Token
