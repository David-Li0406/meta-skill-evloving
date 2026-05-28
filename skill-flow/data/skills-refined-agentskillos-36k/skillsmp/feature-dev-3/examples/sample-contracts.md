# Example Auth Data Contracts

> This document defines input/output contracts for the OAuth authentication feature.

## 1. Input Contracts

### 1.1 OAuth Login Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| provider | `"google" \| "github"` | yes | OAuth provider |
| redirectUrl | string | no | Post-auth redirect URL |

### 1.2 Token Refresh Request

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| refreshToken | string | yes | Refresh token from cookie |

## 2. Output Contracts

### 2.1 Auth Response

```typescript
interface AuthResponse {
  success: boolean;
  user: {
    id: string;
    email: string;
    name: string;
    avatar?: string;
    provider: "google" | "github";
  };
  expiresAt: string; // ISO8601
}
```

### 2.2 Example Success Response

```json
{
  "success": true,
  "user": {
    "id": "usr_abc123",
    "email": "user@example.com",
    "name": "John Doe",
    "avatar": "https://example.com/avatar.jpg",
    "provider": "google"
  },
  "expiresAt": "2025-01-14T10:00:00Z"
}
```

## 3. API Contracts

### 3.1 Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/api/auth/login/:provider` | Initiate OAuth flow | No |
| GET | `/api/auth/callback/:provider` | OAuth callback | No |
| POST | `/api/auth/refresh` | Refresh access token | Cookie |
| POST | `/api/auth/logout` | Logout user | Cookie |
| GET | `/api/auth/me` | Get current user | Cookie |

### 3.2 Error Responses

| Code | Error | Description |
|------|-------|-------------|
| 400 | INVALID_PROVIDER | Unsupported OAuth provider |
| 401 | UNAUTHORIZED | Not authenticated |
| 401 | TOKEN_EXPIRED | Access token expired |
| 403 | OAUTH_DENIED | User denied OAuth permission |
| 500 | OAUTH_ERROR | OAuth provider error |

### 3.3 Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "Access token has expired",
    "details": {
      "expiredAt": "2025-01-13T10:00:00Z"
    }
  }
}
```

## 4. Cookie Contracts

### 4.1 Auth Cookies

| Name | Type | HttpOnly | Secure | SameSite | MaxAge |
|------|------|----------|--------|----------|--------|
| `access_token` | JWT | yes | yes | Strict | 1h |
| `refresh_token` | UUID | yes | yes | Strict | 7d |

### 4.2 JWT Payload

```typescript
interface JWTPayload {
  sub: string;      // user id
  email: string;
  provider: string;
  iat: number;      // issued at
  exp: number;      // expires at
}
```
