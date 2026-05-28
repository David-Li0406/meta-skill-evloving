---
name: "api-designer"
description: "Activates when user requests API design, RESTful conventions, interface specifications, OpenAPI documentation, or API security best practices. Do NOT use for database schema implementation. Examples: 'Design RESTful API for users', 'Create OpenAPI spec'."
---

# API Designer Skill

## 🧠 Expertise

資深 API 架構師，專精於 RESTful API 設計、API 安全與接口規格制定。

---

## 1. RESTful 設計原則

### 1.1 HTTP 方法語意

| 方法 | 語意 | 冪等性 | 安全性 |
|-----|------|-------|-------|
| **GET** | 讀取資源 | ✅ | ✅ |
| **POST** | 新增資源 | ❌ | ❌ |
| **PUT** | 完整更新 | ✅ | ❌ |
| **PATCH** | 部分更新 | ✅ | ❌ |
| **DELETE** | 刪除資源 | ✅ | ❌ |

### 1.2 URL 設計規範

**團隊共識**：URL 不帶路徑變數，識別碼放在 Query Parameter。

```
✅ 正確（識別碼放 Query）
GET    /api/v1/users              # 取得用戶列表
GET    /api/v1/users?id=123       # 取得單一用戶
POST   /api/v1/users              # 新增用戶
PUT    /api/v1/users?id=123       # 更新用戶
DELETE /api/v1/users?id=123       # 刪除用戶
GET    /api/v1/orders?user_id=123 # 取得用戶的訂單

❌ 錯誤（識別碼在 Path）
GET    /api/v1/users/123          # 應使用 ?id=123
PUT    /api/v1/users/123          # 應使用 ?id=123
GET    /api/v1/users/123/orders   # 應使用 ?user_id=123
GET    /api/v1/getUsers           # 動詞不應在 URL
POST   /api/v1/users/create       # 動詞不應在 URL
```

### 1.3 版本控制策略

| 策略 | 範例 | 優點 | 缺點 |
|-----|------|------|------|
| **URL Path** | `/api/v1/users` | 明確易懂 | 違反 REST |
| **Header** | `Accept: v=1` | 符合 REST | 不易測試 |
| **Query** | `/api/users?v=1` | 簡單 | 易被忽略 |

**建議**：使用 URL Path 版本控制，簡單且易於管理。

---

## 2. 請求設計

### 2.1 請求參數位置

| 參數類型 | 位置 | 使用場景 |
|---------|------|---------|
| **識別碼** | Query | `?id=123` |
| **篩選條件** | Query | `?status=active&page=1` |
| **資源資料** | Body | 新增/更新的完整資料 |
| **認證資訊** | Header | `Authorization: Bearer xxx` |

### 2.2 分頁設計

```json
// Request
GET /api/v1/users?page=2&per_page=20

// Response
{
  "data": [...],
  "meta": {
    "current_page": 2,
    "per_page": 20,
    "total": 150,
    "last_page": 8
  },
  "links": {
    "first": "/api/v1/users?page=1",
    "prev": "/api/v1/users?page=1",
    "next": "/api/v1/users?page=3",
    "last": "/api/v1/users?page=8"
  }
}
```

### 2.3 篩選與排序

```
# 篩選
GET /api/v1/users?status=active&role=admin

# 排序
GET /api/v1/users?sort=-created_at,name

# 欄位選擇
GET /api/v1/users?fields=id,name,email

# 關聯載入
GET /api/v1/users?include=orders,profile
```

---

## 3. 回應設計

### 3.1 成功回應格式

```json
// 單一資源
{
  "data": {
    "id": 123,
    "type": "user",
    "attributes": {
      "name": "John",
      "email": "john@example.com"
    }
  }
}

// 資源集合
{
  "data": [
    { "id": 1, "name": "John" },
    { "id": 2, "name": "Jane" }
  ],
  "meta": { "total": 2 }
}
```

### 3.2 錯誤回應格式

```json
{
  "error": {
    "code": "validation_error",
    "message": "The given data was invalid.",
    "details": [
      {
        "field": "email",
        "message": "The email field is required."
      }
    ]
  }
}
```

### 3.3 HTTP 狀態碼

| 狀態碼 | 含義 | 使用場景 |
|-------|------|---------|
| **200** | OK | 成功讀取/更新 |
| **201** | Created | 成功新增 |
| **204** | No Content | 成功刪除 |
| **400** | Bad Request | 請求格式錯誤 |
| **401** | Unauthorized | 未認證 |
| **403** | Forbidden | 無權限 |
| **404** | Not Found | 資源不存在 |
| **422** | Unprocessable | 驗證失敗 |
| **429** | Too Many Requests | 頻率限制 |
| **500** | Internal Error | 伺服器錯誤 |

---

## 4. API 安全

### 4.1 認證機制

| 機制 | 適用場景 | 安全性 |
|-----|---------|-------|
| **API Key** | 內部服務 | 低 |
| **JWT** | 無狀態認證 | 中 |
| **OAuth 2.0** | 第三方授權 | 高 |

### 4.2 安全最佳實務

```yaml
Security Checklist:
  - HTTPS Only（強制 TLS）
  - Rate Limiting（速率限制）
  - Input Validation（輸入驗證）
  - Output Encoding（輸出編碼）
  - CORS Configuration（跨域設定）
  - Sensitive Data Masking（敏感資料遮蔽）
```

### 4.3 速率限制設計

```
HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1609459200
Retry-After: 60
```

---

## 5. 文檔規範

### 5.1 OpenAPI 結構

```yaml
openapi: 3.0.3
info:
  title: User API
  version: 1.0.0
  
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
```

### 5.2 端點文檔模板

```markdown
## [POST] /api/v1/users

**說明**：新增用戶

**Request**
| 欄位 | 類型 | 必填 | 說明 |
|-----|------|-----|------|
| name | string | ✅ | 用戶姓名 |
| email | string | ✅ | 電子郵件 |

**Response - 201 Created**
| 欄位 | 類型 | 說明 |
|-----|------|------|
| id | integer | 用戶 ID |
| name | string | 用戶姓名 |

**Error Responses**
| 狀態碼 | 錯誤碼 | 說明 |
|-------|-------|------|
| 400 | validation_error | 驗證失敗 |
| 409 | email_exists | 郵件已存在 |
```

---

## 6. API 設計檢查清單

### 設計階段
- [ ] URL 是否使用名詞複數？
- [ ] HTTP 方法語意是否正確？
- [ ] 版本控制策略是否一致？
- [ ] 分頁格式是否標準化？

### 安全性
- [ ] 是否強制 HTTPS？
- [ ] 是否有認證機制？
- [ ] 是否有速率限制？
- [ ] 敏感資料是否遮蔽？

### 文檔
- [ ] 是否有 OpenAPI 規格？
- [ ] 錯誤碼是否完整？
- [ ] 範例是否清晰？
