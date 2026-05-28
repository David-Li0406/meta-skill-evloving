---
name: API Development Guide
description: REST API 設計、開發、測試與安全最佳實踐完整指南
---

# API Development Guide

本 Skill 提供 REST API 開發的完整指南，涵蓋設計原則、HTTP 方法、狀態碼、認證授權、Rate Limiting、測試除錯及安全最佳實踐。

---

## 1. REST API 基本原則

### REST 六大原則

| 原則 | 說明 |
|------|------|
| **Client-Server** | 前後端分離，各自獨立演進 |
| **Stateless** | 每個請求包含所有必要資訊，伺服器不儲存狀態 |
| **Cacheable** | 回應可標記為可快取或不可快取 |
| **Uniform Interface** | 統一的介面設計 |
| **Layered System** | 可加入中間層（如負載平衡、快取） |
| **Code on Demand** | (可選) 伺服器可傳送可執行程式碼 |

---

## 2. HTTP 方法 (Methods)

### 標準 CRUD 操作

| 方法 | 用途 | 冪等性 | 安全性 | 範例 |
|------|------|--------|--------|------|
| `GET` | 讀取資源 | ✅ 是 | ✅ 是 | `GET /users/123` |
| `POST` | 建立資源 | ❌ 否 | ❌ 否 | `POST /users` |
| `PUT` | 完整更新資源 | ✅ 是 | ❌ 否 | `PUT /users/123` |
| `PATCH` | 部分更新資源 | ❌ 否 | ❌ 否 | `PATCH /users/123` |
| `DELETE` | 刪除資源 | ✅ 是 | ❌ 否 | `DELETE /users/123` |

### 其他方法

| 方法 | 用途 |
|------|------|
| `HEAD` | 同 GET 但只回傳 headers |
| `OPTIONS` | 查詢支援的方法 (CORS preflight) |

---

## 3. URL 設計規範

### 命名規則

```
✅ 正確範例:
GET    /users                    # 取得所有使用者
GET    /users/123                # 取得特定使用者
GET    /users/123/orders         # 取得使用者的訂單
POST   /users                    # 建立使用者
PUT    /users/123                # 更新使用者
DELETE /users/123                # 刪除使用者

❌ 錯誤範例:
GET    /getUsers                 # 不要用動詞
GET    /user/123                 # 集合用複數
POST   /users/create             # 動作由 HTTP 方法決定
GET    /Users/123                # 避免大寫
```

### 設計原則

1. **使用複數名詞**: `/users` 而非 `/user`
2. **使用小寫字母**: `/users` 而非 `/Users`
3. **使用連字號**: `/user-profiles` 而非 `/user_profiles`
4. **避免動詞**: 動作由 HTTP 方法表達
5. **層級結構**: `/users/123/orders/456`

### 查詢參數

```
# 分頁
GET /users?page=1&limit=20

# 排序
GET /users?sort=created_at&order=desc

# 篩選
GET /users?status=active&role=admin

# 搜尋
GET /users?search=john

# 欄位選擇
GET /users?fields=id,name,email
```

---

## 4. HTTP 狀態碼

### 成功 (2xx)

| 狀態碼 | 名稱 | 使用情境 |
|--------|------|----------|
| `200` | OK | GET 成功、PUT/PATCH 更新成功 |
| `201` | Created | POST 建立成功 |
| `204` | No Content | DELETE 成功（無回傳內容） |

### 客戶端錯誤 (4xx)

| 狀態碼 | 名稱 | 使用情境 |
|--------|------|----------|
| `400` | Bad Request | 請求格式錯誤、驗證失敗 |
| `401` | Unauthorized | 未認證（需登入） |
| `403` | Forbidden | 無權限存取 |
| `404` | Not Found | 資源不存在 |
| `405` | Method Not Allowed | HTTP 方法不支援 |
| `406` | Not Acceptable | 不支援的回應格式 |
| `409` | Conflict | 資源衝突（如重複建立） |
| `413` | Payload Too Large | 請求內容過大 |
| `422` | Unprocessable Entity | 語法正確但語意錯誤 |
| `429` | Too Many Requests | 超過速率限制 |

### 伺服器錯誤 (5xx)

| 狀態碼 | 名稱 | 使用情境 |
|--------|------|----------|
| `500` | Internal Server Error | 伺服器內部錯誤 |
| `502` | Bad Gateway | 上游服務錯誤 |
| `503` | Service Unavailable | 服務暫時不可用 |
| `504` | Gateway Timeout | 上游服務逾時 |

---

## 5. 錯誤處理

### 標準錯誤回應格式

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "請求資料驗證失敗",
        "details": [
            {
                "field": "email",
                "message": "Email 格式不正確"
            },
            {
                "field": "password",
                "message": "密碼至少需要 8 個字元"
            }
        ]
    },
    "timestamp": "2026-01-19T10:30:00Z",
    "path": "/api/users",
    "requestId": "abc123"
}
```

### Express.js 錯誤處理範例

```typescript
// 自定義錯誤類別
class ApiError extends Error {
    constructor(
        public statusCode: number,
        public code: string,
        message: string,
        public details?: any[]
    ) {
        super(message);
    }
}

// 全域錯誤處理中間件
app.use((err: any, req: Request, res: Response, next: NextFunction) => {
    const statusCode = err.statusCode || 500;
    const code = err.code || 'INTERNAL_ERROR';

    res.status(statusCode).json({
        error: {
            code,
            message: err.message,
            details: err.details
        },
        timestamp: new Date().toISOString(),
        path: req.path,
        requestId: req.headers['x-request-id']
    });
});

// 使用範例
throw new ApiError(400, 'VALIDATION_ERROR', '請求資料驗證失敗', [
    { field: 'email', message: 'Email 格式不正確' }
]);
```

---

## 6. 認證與授權

### JWT (JSON Web Token)

#### JWT 結構
```
Header.Payload.Signature

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4ifQ.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

#### 認證流程
```
1. Client 發送 login 請求 → Server 驗證憑證
2. Server 建立 JWT → 回傳給 Client
3. Client 儲存 JWT (localStorage / httpOnly Cookie)
4. Client 每次請求帶上 JWT → Authorization: Bearer <token>
5. Server 驗證 JWT → 處理請求
```

#### Express.js JWT 實作

```typescript
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET!;
const JWT_EXPIRES_IN = '7d';

// 產生 Token
const generateToken = (userId: number): string => {
    return jwt.sign(
        { userId },
        JWT_SECRET,
        { expiresIn: JWT_EXPIRES_IN }
    );
};

// 驗證中間件
const authMiddleware = (req: Request, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;

    if (!authHeader?.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'Missing or invalid token' });
    }

    const token = authHeader.split(' ')[1];

    try {
        const decoded = jwt.verify(token, JWT_SECRET) as { userId: number };
        req.user = { id: decoded.userId };
        next();
    } catch (error) {
        return res.status(401).json({ error: 'Invalid or expired token' });
    }
};
```

#### JWT 最佳實踐

| 做法 | 說明 |
|------|------|
| ✅ 驗證 `iss`, `aud`, `exp`, `nbf` | 確保 Token 合法性 |
| ✅ 使用 HTTPS | 防止 Token 被攔截 |
| ✅ 設定適當過期時間 | Access Token: 15分鐘, Refresh Token: 7天 |
| ✅ 不儲存敏感資訊 | JWT payload 可被解碼 |
| ❌ 不要在 URL 中傳遞 | 會被記錄在 server logs |
| ❌ 不要自訂演算法選擇 | 避免 `alg: none` 攻擊 |

### API Key 認證

```typescript
// 簡單 API Key 驗證
const apiKeyMiddleware = (req: Request, res: Response, next: NextFunction) => {
    const apiKey = req.headers['x-api-key'] as string;

    if (!apiKey || !isValidApiKey(apiKey)) {
        return res.status(401).json({ error: 'Invalid API key' });
    }

    next();
};
```

---

## 7. Rate Limiting (速率限制)

### 常見演算法

| 演算法 | 說明 | 適用場景 |
|--------|------|----------|
| **Fixed Window** | 固定時間窗口重置計數 | 簡單實作 |
| **Sliding Window** | 滑動時間窗口 | 精確限制 |
| **Token Bucket** | 令牌桶，允許短期爆發 | 彈性需求 |
| **Leaky Bucket** | 漏桶，穩定輸出 | 平滑流量 |

### Express Rate Limit 實作

```typescript
import rateLimit from 'express-rate-limit';

// 一般 API 限制
const apiLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 分鐘
    max: 100, // 每個 IP 最多 100 次請求
    message: {
        error: {
            code: 'RATE_LIMIT_EXCEEDED',
            message: '請求過於頻繁，請稍後再試'
        }
    },
    standardHeaders: true, // 回傳 RateLimit-* headers
    legacyHeaders: false
});

// 登入 API 嚴格限制 (防暴力破解)
const loginLimiter = rateLimit({
    windowMs: 60 * 60 * 1000, // 1 小時
    max: 5, // 每個 IP 最多 5 次嘗試
    skipSuccessfulRequests: true
});

app.use('/api/', apiLimiter);
app.use('/api/auth/login', loginLimiter);
```

### Rate Limit Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705656000

# 超過限制時
HTTP/1.1 429 Too Many Requests
Retry-After: 3600
```

---

## 8. API 版本控制

### 版本控制策略

| 方式 | 範例 | 優點 | 缺點 |
|------|------|------|------|
| **URL Path** | `/v1/users` | 清楚明確 | URL 變長 |
| **Query Param** | `/users?version=1` | 彈性 | 可能被忽略 |
| **Header** | `Accept: application/vnd.api.v1+json` | URL 乾淨 | 不直觀 |

### 建議做法

```typescript
// URL Path 版本控制 (推薦)
app.use('/api/v1', v1Router);
app.use('/api/v2', v2Router);

// 路由結構
// /api/v1/users → 舊版 API
// /api/v2/users → 新版 API (breaking changes)
```

---

## 9. 安全最佳實踐

### 必要安全措施

#### 1. 強制 HTTPS
```typescript
// 重導向 HTTP 到 HTTPS
app.use((req, res, next) => {
    if (req.headers['x-forwarded-proto'] !== 'https') {
        return res.redirect(`https://${req.hostname}${req.url}`);
    }
    next();
});
```

#### 2. 安全 Headers (使用 Helmet)
```typescript
import helmet from 'helmet';

app.use(helmet());

// 或自定義
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            frameAncestors: ["'none'"]
        }
    },
    hsts: {
        maxAge: 31536000,
        includeSubDomains: true
    }
}));
```

#### 3. CORS 設定
```typescript
import cors from 'cors';

app.use(cors({
    origin: ['https://example.com', 'https://app.example.com'],
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
    allowedHeaders: ['Content-Type', 'Authorization'],
    credentials: true,
    maxAge: 86400
}));
```

#### 4. 輸入驗證
```typescript
import { z } from 'zod';

const createUserSchema = z.object({
    email: z.string().email(),
    password: z.string().min(8).max(100),
    name: z.string().min(1).max(50)
});

app.post('/users', (req, res) => {
    const result = createUserSchema.safeParse(req.body);

    if (!result.success) {
        return res.status(400).json({
            error: {
                code: 'VALIDATION_ERROR',
                details: result.error.errors
            }
        });
    }

    // 處理驗證後的資料
    const { email, password, name } = result.data;
});
```

### 安全檢查清單

| 項目 | 說明 |
|------|------|
| ✅ HTTPS Only | 所有 API 端點使用 HTTPS |
| ✅ 認證機制 | JWT / OAuth 2.0 / API Key |
| ✅ 輸入驗證 | 驗證所有輸入的長度、格式、類型 |
| ✅ Rate Limiting | 防止 DDoS 和暴力攻擊 |
| ✅ SQL Injection 防護 | 使用 ORM 或參數化查詢 |
| ✅ XSS 防護 | 輸出編碼、CSP headers |
| ✅ 敏感資料不記錄 | 密碼、Token 不寫入 logs |
| ✅ 錯誤訊息不洩露 | 不暴露堆疊追蹤或內部細節 |

---

## 10. API 測試與除錯

### cURL 常用指令

```bash
# GET 請求
curl -X GET https://api.example.com/users

# POST 請求 (JSON)
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John", "email": "john@example.com"}'

# 帶 Authorization Header
curl -X GET https://api.example.com/users \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..."

# 帶 API Key
curl -X GET https://api.example.com/users \
  -H "x-api-key: your-api-key"

# 查看完整回應 (headers + body)
curl -i https://api.example.com/users

# 只看 headers
curl -I https://api.example.com/users

# Verbose 模式 (除錯用)
curl -v https://api.example.com/users

# 輸出到檔案
curl -o response.json https://api.example.com/users
```

### Postman 使用技巧

#### 環境變數
```javascript
// Pre-request Script: 自動設定 Token
pm.environment.set("token", pm.response.json().token);

// Tests: 驗證回應
pm.test("Status code is 200", () => {
    pm.response.to.have.status(200);
});

pm.test("Response has user data", () => {
    const json = pm.response.json();
    pm.expect(json).to.have.property('id');
    pm.expect(json).to.have.property('email');
});
```

#### Collection Runner
```bash
# 使用 Newman CLI 執行 Postman Collection
npm install -g newman

newman run collection.json \
  --environment env.json \
  --reporters cli,html \
  --reporter-html-export report.html
```

### 本專案 API 測試

```bash
# 健康檢查
curl https://wishlist-app-production.up.railway.app/api/admin/health

# 登入取得 Token
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "password123"}'

# 使用 Token 存取受保護的 API
curl -X GET http://localhost:3000/api/wishlists \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 11. API 文件 (OpenAPI/Swagger)

### OpenAPI 3.0 範例

```yaml
openapi: 3.0.0
info:
  title: Wishlist API
  version: 1.0.0
  description: 願望清單 API 文件

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: http://localhost:3000/api
    description: Development

paths:
  /users:
    get:
      summary: 取得所有使用者
      tags: [Users]
      security:
        - BearerAuth: []
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
          description: 成功
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
        '401':
          $ref: '#/components/responses/Unauthorized'

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        email:
          type: string
          format: email
        name:
          type: string
      required:
        - id
        - email

  responses:
    Unauthorized:
      description: 未認證
      content:
        application/json:
          schema:
            type: object
            properties:
              error:
                type: string
```

---

## 12. 本專案 API 結構

### 路由檔案位置

| 檔案 | 說明 |
|------|------|
| `server/src/routes/authRoutes.ts` | 認證相關 (登入、註冊) |
| `server/src/routes/userRoutes.ts` | 使用者管理 |
| `server/src/routes/wishlistRoutes.ts` | 願望清單 CRUD |
| `server/src/routes/itemRoutes.ts` | 項目管理 |
| `server/src/routes/socialRoutes.ts` | 社交功能 |
| `server/src/routes/paymentRoutes.ts` | 支付功能 |
| `server/src/routes/aiRoutes.ts` | AI 功能 |

### API 端點總覽

```
# 認證
POST   /api/auth/register     # 註冊
POST   /api/auth/login        # 登入
POST   /api/auth/logout       # 登出

# 使用者
GET    /api/users/me          # 取得當前使用者
PUT    /api/users/me          # 更新當前使用者
DELETE /api/users/me          # 刪除帳號

# 願望清單
GET    /api/wishlists         # 取得所有清單
POST   /api/wishlists         # 建立清單
GET    /api/wishlists/:id     # 取得特定清單
PUT    /api/wishlists/:id     # 更新清單
DELETE /api/wishlists/:id     # 刪除清單

# 項目
GET    /api/items             # 取得所有項目
POST   /api/items             # 建立項目
PUT    /api/items/:id         # 更新項目
DELETE /api/items/:id         # 刪除項目

# 支付
POST   /api/payment/pay       # 執行支付
GET    /api/payment/history   # 支付歷史
```

---

## 13. 參考資源

### 設計指南
- [REST API Cheatsheet - ByteByteGo](https://bytebytego.com/guides/rest-api-cheatsheet/)
- [RESTful API Design Cheatsheet - DEV Community](https://dev.to/colinmcdermott/restful-api-design-cheatsheet-2ji6)
- [REST API Best Practices - Medium](https://medium.com/@syedabdullahrahman/mastering-rest-api-design-essential-best-practices-dos-and-don-ts-for-2024-dd41a2c59133)

### 安全
- [OWASP REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
- [JWT.io - JSON Web Tokens](https://www.jwt.io/introduction)

### 測試工具
- [Postman - API Testing](https://www.postman.com/)
- [cURL Documentation](https://curl.se/docs/)
- [Newman - Postman CLI](https://github.com/postmanlabs/newman)

### Rate Limiting
- [API Rate Limiting Best Practices - Postman](https://blog.postman.com/what-is-api-rate-limiting/)
- [Rate Limiting vs Throttling - Stoplight](https://blog.stoplight.io/best-practices-api-rate-limiting-vs-throttling)

---

**Last Updated**: 2026-01-19
**Maintainer**: Wishlist App Team
