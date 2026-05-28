---
name: better-auth-implementation-for-nextjs-fastapi
description: This skill provides guidance for implementing secure authentication using Better Auth for Next.js frontend and JWT verification for FastAPI backend.
---

# Better Authentication Implementation for Next.js + FastAPI

## Overview
This skill provides guidance for implementing secure authentication using Better Auth for Next.js frontend and JWT verification for FastAPI backend. The implementation follows industry best practices for securing full-stack applications.

## Authentication Architecture

### Components
- **Better Auth**: JavaScript/TypeScript authentication library for Next.js frontend
- **JWT Tokens**: JSON Web Tokens for stateless authentication between frontend and backend
- **FastAPI Middleware**: JWT verification middleware for backend authentication
- **Shared Secret**: Common secret key for JWT signing and verification

### How It Works
1. User logs in on Next.js frontend → Better Auth creates a session and issues a JWT token
2. Frontend makes API calls → Includes JWT token in `Authorization: Bearer <token>` header
3. FastAPI backend receives request → Extracts token from header, verifies signature using shared secret
4. Backend identifies user → Decodes token to get user ID, email, etc.
5. Backend filters data → Returns only data belonging to the authenticated user

## Implementation Steps

### 1. Better Auth Configuration (Next.js Frontend)

#### Installation
```bash
npm install better-auth
```

#### Configuration
Create `lib/auth/server.ts`:

```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "your-secret-key-here",
  database: {
    // Your database configuration
  },
  plugins: [
    jwt({
      secret: process.env.BETTER_AUTH_SECRET || "your-secret-key-here",
    })
  ],
  // Additional auth configuration
  socialProviders: {
    // Configure social login providers if needed
  }
});
```

#### API Route Setup
Create `app/api/auth/[...auth]/route.ts`:

```typescript
import { auth } from "@/lib/auth";

export const { GET, POST } = auth;
```

#### Client Component Usage
```typescript
"use client";
import { useSession } from "better-auth/react";

export function UserComponent() {
  const { session, signIn, signOut } = useSession();

  if (!session) {
    return <button onClick={() => signIn()}>Sign In</button>;
  }

  return (
    <div>
      <p>Welcome {session.user.email}</p>
      <button onClick={() => signOut()}>Sign Out</button>
    </div>
  );
}
```

### 2. Frontend API Client Configuration

#### Create API Client with JWT
Create `lib/auth/client.ts`:

```typescript
import { getContext } from "better-auth/react";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private async getAuthHeaders(): Promise<Record<string, string>> {
    const { getSession } = getContext();
    const session = await getSession();

    if (!session?.token) {
      throw new Error("No authentication token available");
    }

    return {
      "Authorization": `Bearer ${session.token}`,
      "Content-Type": "application/json"
    };
  }

  async get(endpoint: string) {
    const headers = await this.getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, { headers });
    return response.json();
  }

  async post(endpoint: string, data: any) {
    const headers = await this.getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "POST",
      headers,
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async put(endpoint: string, data: any) {
    const headers = await this.getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "PUT",
      headers,
      body: JSON.stringify(data)
    });
    return response.json();
  }

  async delete(endpoint: string) {
    const headers = await this.getAuthHeaders();
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "DELETE",
      headers
    });
    return response.json();
  }
}

export const apiClient = new ApiClient();
```

### 3. FastAPI Backend Configuration

#### Installation
```bash
pip install fastapi python-jose[cryptography] python-multipart python-dotenv
```

#### JWT Utility Functions
Create `backend/auth/jwt_utils.py`:

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
import os

SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 7 * 24 * 60  # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_jwt_token(token: str) -> Optional[dict]:
    """
    Verify JWT token and return decoded payload if valid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return payload
    except JWTError:
        return None

def decode_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract user ID from JWT token
    """
    payload = verify_jwt_token(token)
    if payload:
        return payload.get("sub")
    return None
```

#### Authentication Middleware
Create `backend/middleware/auth_middleware.py`:

```python
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth.jwt_utils import verify_jwt_token, decode_user_id_from_token

security = HTTPBearer()

async def get_current_user(request: Request) -> str:
    """
    Get current user ID from JWT token in request
    """
    credentials: HTTPAuthorizationCredentials = request.state.credentials
    if credentials is None:
        raise HTTPException(status_code=401, detail="Not authenticated")

    token = credentials.credentials
    user_id = decode_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid authentication token")

    return user_id

async def auth_middleware(request: Request, call_next):
    """
    Middleware to extract and verify JWT token from request
    """
    authorization = request.headers.get("Authorization")
    if authorization and authorization.startswith("Bearer "):
        token = authorization[7:]  # Remove "Bearer " prefix
        request.state.credentials = HTTPAuthorizationCredentials(
            credentials=token
        )
    else:
        request.state.credentials = None

    response = await call_next(request)
    return response
```

#### FastAPI App with Authentication
Create `backend/main.py`:

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .middleware.auth_middleware import get_current_user, auth_middleware
from .middleware import auth_middleware

app = FastAPI(title="Todo API with Authentication")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add auth middleware
app.middleware("http")(auth_middleware)

@app.get("/api/tasks")
async def get_tasks(user_id: str = Depends(get_current_user)):
    """
    Get tasks for the authenticated user
    """
    # Fetch tasks belonging to user_id from database
    # Implementation depends on your database choice
    return {"tasks": [], "user_id": user_id}

@app.post("/api/tasks")
async def create_task(task_data: dict, user_id: str = Depends(get_current_user)):
    """
    Create a task for the authenticated user
    """
    # Create task associated with user_id in database
    return {"task": task_data, "user_id": user_id}

@app.get("/api/user/profile")
async def get_user_profile(user_id: str = Depends(get_current_user)):
    """
    Get authenticated user's profile
    """
    return {"user_id": user_id}
```

### 4. Environment Configuration

#### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-very-secure-secret-key-here
```

#### Backend (.env)
```
BETTER_AUTH_SECRET=your-very-secure-secret-key-here
DATABASE_URL=your-database-connection-string
```

## Security Best Practices

### JWT Configuration
- Use a strong, unique secret key (at least 32 characters)
- Set appropriate token expiration times
- Implement token refresh mechanisms for long-lived sessions
- Use HTTPS in production to prevent token interception

### User Data Protection
- Validate user IDs in all API endpoints to prevent unauthorized access
- Sanitize and validate all user inputs
- Implement proper error handling without exposing sensitive information

### Rate Limiting
- Implement rate limiting to prevent authentication abuse
- Consider using libraries like slowapi for FastAPI

## Testing Authentication

### Unit Tests for Backend
```python
# test_auth.py
import pytest
from fastapi.testclient import TestClient
from main import app

def test_protected_route_requires_auth():
    client = TestClient(app)
    response = client.get("/api/tasks")
    assert response.status_code == 401  # Unauthorized
```

### Integration Tests
- Test the complete flow from login to API access
- Verify that JWT tokens are properly validated
- Ensure user isolation (users can only access their own data)

## Deployment Considerations

### Production Security
- Use environment variables for secrets, never hardcode them
- Implement proper HTTPS configuration
- Set up proper CORS policies
- Use reverse proxy (nginx) for additional security

### Secret Management
- Use cloud secret management services (AWS Secrets Manager, Azure Key Vault, etc.)
- Implement proper secret rotation strategies
- Never commit secrets to version control

## Common Issues and Solutions

### Issue: JWT Token Not Being Sent
**Solution**: Ensure the frontend properly retrieves and includes the JWT token in API requests

### Issue: Token Verification Failing
**Solution**: Verify that both frontend and backend use the same secret key and algorithm

### Issue: Cross-Origin Requests Failing
**Solution**: Configure CORS middleware properly to allow requests from your frontend domain

## Troubleshooting

### Debugging JWT Issues
1. Verify the secret key is identical in both frontend and backend
2. Check token format in request headers
3. Validate token expiration times
4. Ensure proper token refresh mechanisms are in place

### Common Error Messages
- "Invalid authentication token" → Check JWT format and signature
- "Not authenticated" → Verify token is being sent in request headers
- "User not found" → Confirm user exists in the system

This implementation provides a secure, scalable authentication solution for your Next.js + FastAPI application.
