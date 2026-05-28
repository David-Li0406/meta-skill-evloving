---
name: API 設計技能
description: REST API 和 GraphQL 設計指南
---

# 🔌 API 設計技能

## REST API

### 端點設計

| 動作 | 方法 | 路徑 | 說明 |
|-----|------|-----|------|
| 列表 | GET | /users | 取得列表 |
| 建立 | POST | /users | 建立資源 |
| 取得 | GET | /users/:id | 取得單個 |
| 更新 | PUT | /users/:id | 完整更新 |
| 部分更新 | PATCH | /users/:id | 部分更新 |
| 刪除 | DELETE | /users/:id | 刪除 |

### 巢狀資源

```
GET /users/:id/posts         # 用戶的文章
POST /users/:id/posts        # 為用戶建立文章
GET /posts/:id/comments      # 文章的評論
```

---

## 回應格式

### 成功回應

```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John"
  },
  "meta": {
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

### 列表回應

```json
{
  "success": true,
  "data": [...],
  "meta": {
    "page": 1,
    "perPage": 20,
    "total": 100,
    "totalPages": 5
  }
}
```

### 錯誤回應

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "驗證失敗",
    "details": {
      "email": "格式不正確"
    }
  }
}
```

---

## HTTP 狀態碼

| 碼 | 說明 | 使用時機 |
|---|------|---------|
| 200 | OK | 成功 |
| 201 | Created | 建立成功 |
| 204 | No Content | 刪除成功 |
| 400 | Bad Request | 請求錯誤 |
| 401 | Unauthorized | 未認證 |
| 403 | Forbidden | 無權限 |
| 404 | Not Found | 找不到 |
| 422 | Unprocessable | 驗證失敗 |
| 500 | Server Error | 伺服器錯誤 |

---

## 分頁

```
GET /users?page=1&limit=20
GET /users?offset=0&limit=20
GET /users?cursor=abc123
```

## 篩選與排序

```
GET /users?role=admin&status=active
GET /users?sort=created_at&order=desc
GET /users?fields=id,name,email
```

---

## 版本控制

```
# URL 路徑
GET /api/v1/users
GET /api/v2/users

# Header
Accept: application/vnd.api+json; version=1
```

---

## 認證

### Bearer Token
```
Authorization: Bearer <token>
```

### API Key
```
X-API-Key: <key>
```
