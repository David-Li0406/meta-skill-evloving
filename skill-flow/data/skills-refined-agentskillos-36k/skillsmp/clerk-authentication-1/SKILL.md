---
name: clerk-authentication
description: Comprehensive implementation guide for Clerk authentication in web applications. Use when user needs to add authentication, protect routes, verify JWT tokens, manage users, or set up Clerk with React frontends and Python/FastAPI backends.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Clerk Authentication Implementation

Complete authentication solution for modern web applications using Clerk's authentication platform.

## When to Use This Skill

Use this skill when you need to:
- Set up user authentication in React, Next.js, or other frontend frameworks
- Protect backend API routes with JWT token verification
- Implement user management (sign-up, sign-in, profile management)
- Add organizations and multi-tenant features
- Integrate Clerk with FastAPI, Express, or other backend frameworks
- Verify Bearer tokens using Clerk's JWKS endpoint
- Retrieve user information from authenticated requests
- Set up social authentication providers
- Implement role-based access control

## Core Concepts

### 1. Authentication Flow
- User signs in through Clerk's pre-built UI components
- Clerk issues a JWT token stored in the client
- Client sends token as Bearer authorization header
- Backend verifies token using Clerk's public JWKS
- Backend extracts user_id and other claims from token

### 2. Key Components
- **Frontend SDK**: Pre-built UI components and hooks
- **Backend SDK**: User management and administrative operations
- **JWKS Verification**: JWT token validation using public keys
- **Session Management**: Automatic token refresh and session handling

## Quick Start

### Frontend (React)
```bash
npm install @clerk/clerk-react
```

### Backend (Python/FastAPI)
```bash
pip install fastapi uvicorn python-jose requests clerk-backend-api python-dotenv
```

## Implementation Patterns

### Pattern 1: React Frontend Authentication
Use Clerk's pre-built components for quick setup. See [react-frontend.md](resources/react-frontend.md).

### Pattern 2: FastAPI Backend Protection
Protect API endpoints with JWT verification. See [fastapi-backend.md](resources/fastapi-backend.md).

### Pattern 3: User Management
Use the Backend SDK for administrative operations. See [user-management.md](resources/user-management.md).

### Pattern 4: Organizations
Implement multi-tenant features. See [organizations.md](resources/organizations.md).

## Environment Variables

Required environment variables for different environments:

### Frontend (.env)
```bash
VITE_CLERK_PUBLISHABLE_KEY=pk_test_...
```

### Backend (.env)
```bash
CLERK_SECRET_KEY=sk_test_...
CLERK_ISSUER=https://your-clerk-instance.clerk.accounts.dev
CLERK_JWKS_URL=https://your-clerk-instance.clerk.accounts.dev/.well-known/jwks.json
```

## Best Practices

1. **Token Verification**: Always verify tokens on the backend using JWKS
2. **Error Handling**: Implement proper error handling for authentication failures
3. **Environment Security**: Never expose secret keys in client-side code
4. **Session Management**: Let Clerk handle token refresh automatically
5. **Rate Limiting**: Implement rate limiting on authentication endpoints
6. **CORS Configuration**: Properly configure CORS for your frontend domain

## Common Use Cases

### 1. Protect a Single Route
```python
from fastapi import Depends
from your_auth_module import verify_clerk_token

@app.get("/protected")
async def protected_route(auth_data = Depends(verify_clerk_token)):
    return {"user_id": auth_data["user_id"]}
```

### 2. Get Current User Information
```python
@app.get("/me")
async def get_current_user(auth_data = Depends(verify_clerk_token)):
    user_id = auth_data["user_id"]
    # Fetch additional user details if needed
    return {"user_id": user_id}
```

### 3. Role-Based Access Control
```python
async def require_admin(auth_data = Depends(verify_clerk_token)):
    # Check roles from token payload
    roles = auth_data["payload"].get("roles", [])
    if "admin" not in roles:
        raise HTTPException(status_code=403, detail="Admin access required")
    return auth_data
```

## Troubleshooting

### Common Issues

1. **"Invalid token signing key"**
   - Verify CLERK_JWKS_URL is correct
   - Check that CLERK_ISSUER matches your Clerk instance

2. **"User ID not found in token"**
   - Ensure token is being sent in Authorization header
   - Verify token hasn't expired

3. **CORS Errors**
   - Add your frontend domain to Clerk's allowed origins
   - Configure CORS middleware in your backend

4. **Import Errors**
   - Verify all dependencies are installed
   - Check Python version compatibility (3.9+)

## Additional Resources

- [Clerk Documentation](https://clerk.com/docs)
- [Clerk Python SDK](https://github.com/clerk/clerk-sdk-python)
- [FastAPI Documentation](https://fastapi.tiangolo.com)

## File References

For complete code implementations, see:
- [react-frontend.md](resources/react-frontend.md) - React frontend setup
- [fastapi-backend.md](resources/fastapi-backend.md) - FastAPI backend implementation
- [user-management.md](resources/user-management.md) - User management operations
- [organizations.md](resources/organizations.md) - Organization features
- [examples.md](resources/examples.md) - Complete working examples
