---
name: REST API 設計
description: REST API 設計詳細指南
---

# REST API 設計指南

## URL 設計

### 資源命名
```
# 使用名詞複數
GET /users
GET /posts
GET /comments

# 巢狀資源
GET /users/123/posts
GET /posts/456/comments

# 避免動詞
❌ GET /getUsers
❌ POST /createUser
✅ GET /users
✅ POST /users
```

### 查詢參數
```
# 分頁
GET /users?page=1&limit=20

# 排序
GET /users?sort=created_at&order=desc

# 篩選
GET /users?role=admin&status=active

# 選擇欄位
GET /users?fields=id,name,email

# 搜尋
GET /users?search=john
```

---

## HTTP 方法

| 方法 | 用途 | 冪等 |
|-----|------|-----|
| GET | 讀取資源 | ✅ |
| POST | 建立資源 | ❌ |
| PUT | 完整更新 | ✅ |
| PATCH | 部分更新 | ✅ |
| DELETE | 刪除資源 | ✅ |

---

## 狀態碼

### 成功
- `200 OK` - 成功
- `201 Created` - 建立成功
- `204 No Content` - 成功但無內容

### 客戶端錯誤
- `400 Bad Request` - 請求格式錯誤
- `401 Unauthorized` - 未認證
- `403 Forbidden` - 無權限
- `404 Not Found` - 找不到資源
- `422 Unprocessable` - 驗證失敗
- `429 Too Many Requests` - 速率限制

### 伺服器錯誤
- `500 Internal Server Error` - 伺服器錯誤
- `503 Service Unavailable` - 服務不可用

---

## 回應格式

### 成功回應
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com"
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
    "per_page": 20,
    "total": 100,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
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
      "email": ["格式不正確"],
      "password": ["至少需要 8 個字元"]
    }
  }
}
```

---

## 版本控制

```
# URL 路徑版本
GET /api/v1/users
GET /api/v2/users

# Header 版本
Accept: application/vnd.api+json; version=1
```

---

## 最佳實踐

1. 使用 HTTPS
2. 回傳適當狀態碼
3. 統一回應格式
4. 分頁大量資料
5. 速率限制
6. 版本控制
7. 詳細文件
