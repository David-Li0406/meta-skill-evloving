# API 文档示例文件

本目录包含通用的 API 文档模板，适用于任何后端技术栈和前端框架。

## 📁 文件说明

| 文件 | 说明 | 适用场景 |
|------|------|----------|
| **api_document_template.md** | 通用 API 文档模板 | 任何项目的 API 文档 |

## 🚀 快速开始

### 1. 复制模板

```bash
# 复制到你的项目文档目录
cp api_document_template.md docs/api-docs/user-api.md
```

### 2. 修改模板

根据你的实际接口修改以下内容：

- **Base URL**：修改为你的 API 地址
- **认证方式**：选择适合的认证方式（Bearer Token、API Key 等）
- **接口列表**：替换为你的实际接口
- **错误码**：更新为你的错误码定义
- **数据类型**：更新为你的数据模型

### 3. 保持格式一致性

确保所有接口文档遵循统一的格式：

- 接口名称
- 功能说明
- 请求方式
- 请求参数（表格格式）
- 请求示例
- 响应示例
- 错误响应示例

## 📋 文档模板结构

```
# 模块名 API

## 1. 基础信息
- Base URL
- 认证方式
- 通用响应格式

## 2. 接口列表
- POST /{module}/insert - 新增
- POST /{module}/queryByPage - 分页查询
- GET /{module}/queryAll - 查询全部
- GET /{module}/queryById - 按ID查询
- PUT /{module}/update - 更新
- DELETE /{module}/delete - 删除

## 3. 错误码定义
- 错误码表格
- 处理建议

## 4. 数据类型定义
- 数据对象说明
- 字段定义

## 5. 限制说明
- 请求频率限制
- 数据限制

## 6. 版本历史
- 版本更新记录

## 7. 常见问题
- FAQ

## 8. 附录
- 认证流程
- 签名算法（可选）
```

## 📝 模板使用指南

### 编写接口文档

每个接口文档应包含以下部分：

1. **接口描述**：简短描述接口功能
2. **功能说明**：详细描述业务用途
3. **接口地址**：完整的 URL 路径
4. **请求方式**：HTTP 方法（GET/POST/PUT/DELETE）
5. **认证要求**：是否需要 Token
6. **请求参数**：表格形式列出所有参数
7. **请求示例**：完整的 cURL 或代码示例
8. **响应示例**：成功响应 JSON 示例
9. **错误响应示例**：常见错误场景的响应

### 参数说明表格

| 参数名 | 位置 | 类型 | 必填 | 说明 | 示例值 |
|--------|------|------|------|--------|--------|
| id | Path | int | 是 | 资源 ID | 123 |
| name | Body | string | 是 | 名称 | "测试" |

**参数位置说明**：
- **Path**：URL 路径中，如 `/users/{id}`
- **Query**：URL 查询参数，如 `?page=1`
- **Body**：请求体中的 JSON 字段
- **Header**：请求头中的字段

**接口命名规范说明**：
本模板使用标准命名规范：
- `/{module}/insert` - POST 新增数据
- `/{module}/queryByPage` - POST 分页查询（参数在 Body）
- `/{module}/queryAll` - GET 查询全部数据
- `/{module}/queryById` - GET 按ID查询（参数在 Query）
- `/{module}/update` - PUT 更新数据（参数在 Body）
- `/{module}/delete` - DELETE 删除数据（参数在 Query）

### 响应示例

**成功响应**：
```json
{
  "code": 200,
  "message": "操作成功",
  "data": {
    "id": 123,
    "name": "测试"
  }
}
```

**错误响应**：
```json
{
  "code": 400,
  "message": "参数错误",
  "error": "INVALID_PARAMETER",
  "details": {
    "field": "name",
    "constraint": "NOT_NULL"
  }
}
```

## ✅ 文档质量检查清单

使用以下清单检查你的 API 文档：

- [ ] 所有接口都有完整的描述
- [ ] 请求参数都有明确的类型和说明
- [ ] 必填参数和可选参数已标注
- [ ] 提供了完整的请求示例
- [ ] 提供了完整的响应示例
- [ ] 错误码有清晰的说明
- [ ] 数据类型定义完整
- [ ] 认证方式已说明
- [ ] 版本信息已记录
- [ ] 示例代码可执行

## 🔧 自定义配置

### 技术栈适配

根据你的后端技术栈调整：

**Java (Spring Boot)**：
- 路径示例：`@GetMapping("/api/v1/users")`
- 注解：`@RequestBody`, `@PathVariable`, `@RequestParam`

**Python (Flask)**：
- 路径示例：`@app.route('/api/v1/users', methods=['GET'])`
- 参数获取：`request.json`, `request.args.get()`

**Node.js (Express)**：
- 路径示例：`app.get('/api/v1/users', handler)`
- 参数获取：`req.body`, `req.query`

### 前端适配

根据你的前端技术栈调整请求示例：

**JavaScript (Axios)**：
```javascript
axios.get('/api/v1/users', {
  params: { page: 1 },
  headers: { Authorization: `Bearer ${token}` }
})
```

**JavaScript (Fetch)**：
```javascript
fetch('/api/v1/users?page=1', {
  headers: { Authorization: `Bearer ${token}` }
})
```

**Java (OkHttp)**：
```java
Request request = new Request.Builder()
  .url("https://api.example.com/api/v1/users?page=1")
  .addHeader("Authorization", "Bearer " + token)
  .build();
```

## 🆘 常见问题

**Q: 如何处理分页？**

A: 使用标准的分页参数：
- `page`：页码（从1开始）
- `pageSize`：每页数量

响应中应包含分页信息：
```json
{
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

**Q: 如何处理认证？**

A: 在请求头中添加 Token：
```
Authorization: Bearer {token}
```

或使用 API Key：
```
X-API-Key: {api_key}
```

**Q: 错误码如何定义？**

A: 遵循以下规范：
- 200-299：成功
- 400-499：客户端错误
- 500-599：服务器错误

每个错误码应包含：
- 错误码（数字）
- 错误标识（大写下划线）
- 错误消息（用户可读）
- 详细信息（可选）

**Q: 如何处理日期时间？**

A: 推荐使用 ISO 8601 格式：
```json
{
  "createdAt": "2026-01-19T10:30:00Z",
  "updatedAt": "2026-01-19T10:30:00+08:00"
}
```

## 📚 参考资源

- [RESTful API 设计最佳实践](https://restfulapi.net/)
- [HTTP 状态码规范](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status)
- [JSON API 规范](https://jsonapi.org/)
- [OpenAPI 规范](https://swagger.io/specification/)
- [API 文档指南](https://docs.apiary.io/)

## 🎯 使用建议

1. **保持简洁**：避免冗长的描述，用户需要的是清晰的信息
2. **示例先行**：示例比说明更有用，确保所有示例可执行
3. **错误处理**：详细列出可能的错误场景和处理方式
4. **版本控制**：API 变更时及时更新文档版本
5. **用户视角**：从使用者的角度编写文档，而非开发者视角
