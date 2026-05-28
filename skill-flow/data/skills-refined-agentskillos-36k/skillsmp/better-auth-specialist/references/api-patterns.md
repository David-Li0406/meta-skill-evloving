# API Patterns for Better Auth

Authentication API endpoint patterns and middleware for Node.js and FastAPI backends.

## Table of Contents
- Authentication Endpoints
- Session Management
- Middleware Patterns
- Error Handling
- Rate Limiting
- Security Best Practices

## Authentication Endpoints

### Signup (Email/Password)

**Node.js/Express**
```typescript
router.post("/signup", async (req, res) => {
  try {
    const { email, password, name } = req.body;

    // Validation
    if (!email || !password) {
      return res.status(400).json({ error: "Email and password required" });
    }

    const result = await auth.api.signUpEmail({
      body: { email, password, name },
      headers: req.headers,
    });

    return res.status(201).json(result);
  } catch (error) {
    return res.status(400).json({ error: error.message });
  }
});
```

**FastAPI**
```python
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: SignUpRequest, request: Request):
    try:
        result = await auth.sign_up_email(
            email=data.email,
            password=data.password,
            name=data.name,
            headers=dict(request.headers),
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Signin (Email/Password)

**Node.js/Express**
```typescript
router.post("/signin", async (req, res) => {
  try {
    const { email, password, rememberMe } = req.body;

    const result = await auth.api.signInEmail({
      body: { email, password },
      headers: req.headers,
    });

    // Set longer expiry if remember me
    if (rememberMe) {
      res.cookie("session", result.token, {
        maxAge: 30 * 24 * 60 * 60 * 1000, // 30 days
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
      });
    }

    return res.json(result);
  } catch (error) {
    return res.status(401).json({ error: "Invalid credentials" });
  }
});
```

**FastAPI**
```python
@router.post("/signin")
async def signin(
    data: SignInRequest,
    request: Request,
    response: Response
):
    try:
        result = await auth.sign_in_email(
            email=data.email,
            password=data.password,
            headers=dict(request.headers),
        )

        # Set cookie
        response.set_cookie(
            key="session",
            value=result["token"],
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=60 * 60 * 24 * 7,  # 7 days
        )

        return result
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
```

### Signout

**Node.js/Express**
```typescript
router.post("/signout", async (req, res) => {
  await auth.api.signOut({
    headers: req.headers,
  });

  res.clearCookie("session");
  return res.json({ success: true });
});
```

**FastAPI**
```python
@router.post("/signout")
async def signout(request: Request, response: Response):
    await auth.sign_out(headers=dict(request.headers))
    response.delete_cookie("session")
    return {"success": True}
```

### Get Session

**Node.js/Express**
```typescript
router.get("/session", async (req, res) => {
  const session = await auth.api.getSession({
    headers: req.headers,
  });

  if (!session) {
    return res.status(401).json({ error: "Not authenticated" });
  }

  return res.json(session);
});
```

**FastAPI**
```python
@router.get("/session")
async def get_session(request: Request):
    session = await auth.get_session(headers=dict(request.headers))

    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return session
```

## Session Management

### Refresh Session

**Node.js/Express**
```typescript
router.post("/refresh", async (req, res) => {
  try {
    const result = await auth.api.refreshSession({
      headers: req.headers,
    });

    return res.json(result);
  } catch (error) {
    return res.status(401).json({ error: "Invalid or expired session" });
  }
});
```

**FastAPI**
```python
@router.post("/refresh")
async def refresh_session(request: Request):
    try:
        result = await auth.refresh_session(headers=dict(request.headers))
        return result
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
```

### Revoke Session

**Node.js/Express**
```typescript
router.post("/revoke/:sessionId", requireAuth, async (req, res) => {
  const { sessionId } = req.params;

  // Ensure user can only revoke their own sessions
  const session = await prisma.session.findUnique({
    where: { id: sessionId },
  });

  if (!session || session.userId !== req.user.id) {
    return res.status(403).json({ error: "Forbidden" });
  }

  await prisma.session.delete({
    where: { id: sessionId },
  });

  return res.json({ success: true });
});
```

**FastAPI**
```python
@router.post("/revoke/{session_id}")
async def revoke_session(
    session_id: str,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == user["id"]
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()

    return {"success": True}
```

## Middleware Patterns

### Authentication Middleware

**Node.js/Express**
```typescript
// middleware/auth.ts
export async function requireAuth(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const session = await auth.api.getSession({
      headers: req.headers,
    });

    if (!session) {
      return res.status(401).json({ error: "Authentication required" });
    }

    req.user = session.user;
    req.session = session.session;
    next();
  } catch (error) {
    return res.status(401).json({ error: "Invalid session" });
  }
}

// Optional auth (doesn't fail if not authenticated)
export async function optionalAuth(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const session = await auth.api.getSession({
      headers: req.headers,
    });

    if (session) {
      req.user = session.user;
      req.session = session.session;
    }
  } catch (error) {
    // Continue without auth
  }

  next();
}
```

**FastAPI**
```python
# dependencies.py
from fastapi import Depends, HTTPException, Request
from typing import Optional

async def get_current_user(request: Request) -> dict:
    """Require authentication"""
    session = await auth.get_session(headers=dict(request.headers))

    if not session:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return session["user"]

async def get_optional_user(request: Request) -> Optional[dict]:
    """Optional authentication"""
    try:
        session = await auth.get_session(headers=dict(request.headers))
        return session["user"] if session else None
    except:
        return None
```

### Role-Based Middleware

**Node.js/Express**
```typescript
export function requireRole(...roles: string[]) {
  return async (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: "Authentication required" });
    }

    const userRoles = await prisma.userRole.findMany({
      where: { userId: req.user.id },
      include: { role: true },
    });

    const hasRole = userRoles.some((ur) =>
      roles.includes(ur.role.name)
    );

    if (!hasRole) {
      return res.status(403).json({ error: "Insufficient permissions" });
    }

    req.userRoles = userRoles.map((ur) => ur.role);
    next();
  };
}

// Usage
router.get("/admin", requireAuth, requireRole("admin"), (req, res) => {
  res.json({ message: "Admin only content" });
});
```

**FastAPI**
```python
def require_role(*roles: str):
    """Dependency to check user roles"""
    async def role_checker(
        user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        user_roles = db.query(UserRole).filter(
            UserRole.user_id == user["id"]
        ).join(Role).all()

        user_role_names = [ur.role.name for ur in user_roles]

        if not any(role in user_role_names for role in roles):
            raise HTTPException(
                status_code=403,
                detail="Insufficient permissions"
            )

        return user

    return role_checker

# Usage
@router.get("/admin")
async def admin_route(user: dict = Depends(require_role("admin"))):
    return {"message": "Admin only content"}
```

### Permission-Based Middleware

**Node.js/Express**
```typescript
export function requirePermission(resource: string, action: string) {
  return async (req: Request, res: Response, next: NextFunction) => {
    if (!req.user) {
      return res.status(401).json({ error: "Authentication required" });
    }

    const hasPermission = await checkUserPermission(
      req.user.id,
      resource,
      action
    );

    if (!hasPermission) {
      return res.status(403).json({
        error: `Permission denied: ${resource}:${action}`,
      });
    }

    next();
  };
}

async function checkUserPermission(
  userId: string,
  resource: string,
  action: string
): Promise<boolean> {
  const permissions = await prisma.permission.findMany({
    where: {
      resource,
      action,
      rolePermissions: {
        some: {
          role: {
            userRoles: {
              some: { userId },
            },
          },
        },
      },
    },
  });

  return permissions.length > 0;
}
```

**FastAPI**
```python
def require_permission(resource: str, action: str):
    """Dependency to check user permissions"""
    async def permission_checker(
        user: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        has_permission = await check_user_permission(
            db, user["id"], resource, action
        )

        if not has_permission:
            raise HTTPException(
                status_code=403,
                detail=f"Permission denied: {resource}:{action}"
            )

        return user

    return permission_checker

async def check_user_permission(
    db: Session,
    user_id: str,
    resource: str,
    action: str
) -> bool:
    permissions = db.query(Permission).filter(
        Permission.resource == resource,
        Permission.action == action
    ).join(RolePermission).join(Role).join(UserRole).filter(
        UserRole.user_id == user_id
    ).all()

    return len(permissions) > 0
```

## Error Handling

### Centralized Error Handler

**Node.js/Express**
```typescript
export class AuthError extends Error {
  constructor(
    message: string,
    public statusCode: number = 401
  ) {
    super(message);
    this.name = "AuthError";
  }
}

export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  if (err instanceof AuthError) {
    return res.status(err.statusCode).json({
      error: err.message,
    });
  }

  console.error(err);
  return res.status(500).json({
    error: "Internal server error",
  });
}
```

**FastAPI**
```python
from fastapi import Request, status
from fastapi.responses import JSONResponse

class AuthError(Exception):
    def __init__(self, message: str, status_code: int = 401):
        self.message = message
        self.status_code = status_code

@app.exception_handler(AuthError)
async def auth_error_handler(request: Request, exc: AuthError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )
```

## Rate Limiting

**Node.js/Express**
```typescript
import rateLimit from "express-rate-limit";

export const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // 5 requests per window
  message: "Too many authentication attempts, please try again later",
  standardHeaders: true,
  legacyHeaders: false,
});

// Apply to auth routes
router.post("/signin", authLimiter, async (req, res) => {
  // ...
});
```

**FastAPI**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@router.post("/signin")
@limiter.limit("5/15minutes")
async def signin(request: Request, data: SignInRequest):
    # ...
```

## Security Best Practices

### Password Requirements

```typescript
function validatePassword(password: string): boolean {
  const minLength = 8;
  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const hasSpecialChar = /[!@#$%^&*]/.test(password);

  return (
    password.length >= minLength &&
    hasUpperCase &&
    hasLowerCase &&
    hasNumbers &&
    hasSpecialChar
  );
}
```

### Email Validation

```typescript
function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

### CSRF Protection

**Node.js/Express**
```typescript
import csrf from "csurf";

const csrfProtection = csrf({ cookie: true });

app.use(csrfProtection);

router.get("/csrf-token", (req, res) => {
  res.json({ csrfToken: req.csrfToken() });
});
```

### Secure Headers

**Node.js/Express**
```typescript
import helmet from "helmet";

app.use(helmet());
app.use(
  helmet.contentSecurityPolicy({
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
    },
  })
);
```

**FastAPI**
```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "*.example.com"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
