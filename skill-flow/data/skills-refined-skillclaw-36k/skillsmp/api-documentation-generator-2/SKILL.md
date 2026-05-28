---
name: api-documentation-generator
description: 自动生成 API 文档。从代码中提取 API 定义，生成 OpenAPI/Swagger 规范和交互式文档。
trigger: 当用户需要生成或更新 API 文档时使用
---

# API Documentation Generator

自动化 API 文档生成工具，从代码中提取 API 定义并生成标准化文档。

## 功能特性

- 自动提取 API 端点
- 生成 OpenAPI 3.0 规范
- 创建交互式文档
- 示例代码生成
- 类型定义导出
- 版本管理

## 支持的框架

- Express.js
- Fastify
- NestJS
- Koa
- Hapi
- Next.js API Routes

## 使用场景

1. **新 API 开发**: 自动生成初始文档
2. **API 更新**: 同步代码和文档
3. **团队协作**: 共享 API 规范
4. **客户端生成**: 生成 SDK 和类型定义

## 核心功能

### 文档生成
- OpenAPI/Swagger 规范
- Markdown 文档
- HTML 交互式文档
- Postman Collection
- GraphQL Schema

### 代码分析
- 路由提取
- 参数解析
- 响应类型推断
- 认证方式识别
- 错误码提取

### 文档增强
- 示例请求/响应
- 认证说明
- 错误处理文档
- 速率限制说明
- 版本变更记录

## 使用方法

```bash
# 生成完整 API 文档
/api-documentation-generator

# 生成特定路由的文档
/api-documentation-generator --routes /api/users

# 生成 OpenAPI 规范
/api-documentation-generator --format openapi

# 生成 Postman Collection
/api-documentation-generator --format postman

# 生成 TypeScript 类型定义
/api-documentation-generator --types

# 更新现有文档
/api-documentation-generator --update

# 生成客户端 SDK
/api-documentation-generator --sdk typescript
```

## 文档结构

### OpenAPI 规范

```yaml
openapi: 3.0.0
info:
  title: AI Innovation Hub API
  version: 1.0.0
  description: Enterprise AI platform API

servers:
  - url: https://api.aizcspace.com
    description: Production
  - url: http://localhost:8051
    description: Development

paths:
  /api/models:
    get:
      summary: List AI models
      tags: [Models]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Model'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

components:
  schemas:
    Model:
      type: object
      properties:
        id:
          type: string
        name:
          type: string
        description:
          type: string
        category:
          type: string
          enum: [LLM, Vision, Audio]

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Markdown 文档

```markdown
# AI Innovation Hub API Documentation

## Authentication

All API requests require authentication using JWT tokens.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.aizcspace.com/api/models
```

## Endpoints

### List Models

`GET /api/models`

Retrieve a paginated list of AI models.

**Query Parameters:**
- `page` (integer, optional): Page number (default: 1)
- `limit` (integer, optional): Items per page (default: 20)
- `category` (string, optional): Filter by category

**Response:**
```json
{
  "data": [
    {
      "id": "model-123",
      "name": "GPT-4",
      "description": "Advanced language model",
      "category": "LLM"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or missing token
- `403 Forbidden`: Insufficient permissions
- `500 Internal Server Error`: Server error
```

## 配置

在 `.claude/settings.json` 中配置文档生成：

```json
{
  "apiDocGenerator": {
    "format": "openapi",
    "outputDir": "docs/api",
    "includeExamples": true,
    "generateTypes": true,
    "languages": ["typescript", "python"],
    "excludeRoutes": ["/internal/*"],
    "customTemplates": {
      "markdown": "templates/api-doc.md"
    }
  }
}
```

## 文档模板

### 端点文档模板

```markdown
## {{method}} {{path}}

{{description}}

**Authentication:** {{authType}}

**Parameters:**
{{#parameters}}
- `{{name}}` ({{type}}, {{required}}): {{description}}
{{/parameters}}

**Request Body:**
```json
{{requestExample}}
```

**Response:**
```json
{{responseExample}}
```

**Error Codes:**
{{#errors}}
- `{{code}}`: {{message}}
{{/errors}}
```

## 最佳实践

1. **保持同步**: 代码变更后立即更新文档
2. **详细示例**: 提供真实的请求/响应示例
3. **错误文档**: 完整记录所有错误码
4. **版本管理**: 维护 API 版本历史
5. **交互测试**: 提供可测试的文档界面

## 输出格式

生成的文档包括：

- `openapi.yaml`: OpenAPI 3.0 规范
- `README.md`: API 概览和快速开始
- `endpoints/`: 各端点详细文档
- `types/`: TypeScript 类型定义
- `examples/`: 示例代码
- `postman/`: Postman Collection

## 集成

与其他 Skills 配合使用：

- `api-integration`: API 集成最佳实践
- `typescript-standards`: 类型定义规范
- `doc-coauthoring`: 文档协作编写
- `code-review-checklist`: API 设计审查
