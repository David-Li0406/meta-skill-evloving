# Code Tour Patterns

Patterns for creating guided codebase walkthroughs.

## Tour Structure

### 1. Overview Tour

Start with the big picture:

```markdown
# Codebase Tour

## Project Structure

```
├── src/
│   ├── api/              # REST API endpoints
│   ├── services/         # Business logic
│   ├── models/           # Data models
│   ├── lib/              # Shared utilities
│   └── config/           # Configuration
├── tests/
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── scripts/              # Build/deploy scripts
└── docs/                 # Documentation
```

## Key Entry Points

| What | Where | Description |
|------|-------|-------------|
| API Server | `src/index.ts` | Application entry point |
| Routes | `src/api/routes.ts` | All API route definitions |
| Models | `src/models/index.ts` | Database models |
| Config | `src/config/index.ts` | Environment configuration |
```

### 2. Feature-Based Tours

Organize tours around features:

```markdown
# Tour: User Authentication

This tour walks through how authentication works.

## Stop 1: Login Endpoint

**File:** `src/api/auth/login.ts`

```typescript
// This endpoint handles user login
export async function login(req: Request, res: Response) {
  const { email, password } = req.body;

  // 1. Find user by email
  const user = await UserService.findByEmail(email);

  // 2. Verify password
  const valid = await user.verifyPassword(password);

  // 3. Generate JWT token
  const token = generateToken(user);

  return res.json({ token });
}
```

**Key points:**
- Password verification uses bcrypt (see `src/lib/crypto.ts`)
- Token includes user ID and roles
- Token expires in 24 hours (configurable)

**Next:** See how `UserService.findByEmail` works →

---

## Stop 2: User Service

**File:** `src/services/user-service.ts`

```typescript
export class UserService {
  static async findByEmail(email: string): Promise<User | null> {
    return await prisma.user.findUnique({
      where: { email: email.toLowerCase() },
      include: { roles: true }
    });
  }
}
```

**Key points:**
- Emails are normalized to lowercase
- Roles are eager-loaded for permission checks
- Returns null if user not found (handled by caller)

**Next:** See how tokens are generated →
```

### 3. Request Flow Tour

Follow a request through the system:

```markdown
# Tour: API Request Lifecycle

Follow a request from client to response.

## 1. Entry Point

**File:** `src/index.ts:45`

```typescript
app.use('/api', apiRouter);
```

All requests to `/api/*` are handled by the API router.

## 2. Middleware Chain

**File:** `src/api/middleware/index.ts`

```typescript
export const middleware = [
  cors(),           // 1. Handle CORS
  helmet(),         // 2. Security headers
  requestId(),      // 3. Add request ID
  logger(),         // 4. Log request
  authenticate(),   // 5. Verify JWT (if present)
  rateLimit(),      // 6. Rate limiting
];
```

Each request passes through this chain in order.

## 3. Route Handler

**File:** `src/api/users/get-user.ts`

```typescript
export async function getUser(req: Request, res: Response) {
  // req.user is set by authenticate() middleware
  const userId = req.params.id;

  // Authorization check
  if (req.user.id !== userId && !req.user.isAdmin) {
    throw new ForbiddenError();
  }

  const user = await UserService.findById(userId);
  return res.json(user);
}
```

## 4. Error Handling

**File:** `src/api/middleware/error-handler.ts`

```typescript
export function errorHandler(err, req, res, next) {
  // Log error with request context
  logger.error({ err, requestId: req.id });

  // Map to HTTP response
  const status = err.status || 500;
  const message = err.expose ? err.message : 'Internal Error';

  return res.status(status).json({
    error: { message, code: err.code }
  });
}
```

Errors thrown anywhere in the chain are caught here.
```

## Interactive Code Tours

### VS Code CodeTour Format

```json
// .tours/authentication.tour
{
  "title": "Authentication Flow",
  "description": "How user authentication works",
  "steps": [
    {
      "file": "src/api/auth/login.ts",
      "line": 15,
      "description": "## Login Handler\n\nThis is where login requests arrive. The handler:\n1. Extracts email and password\n2. Validates credentials\n3. Returns a JWT token"
    },
    {
      "file": "src/services/user-service.ts",
      "line": 42,
      "description": "## User Lookup\n\nThe `findByEmail` method queries the database for the user record."
    },
    {
      "file": "src/lib/jwt.ts",
      "line": 8,
      "description": "## Token Generation\n\nJWT tokens are created here with a 24-hour expiration."
    }
  ]
}
```

### Tour Index

```markdown
# Available Code Tours

## Beginner Tours
| Tour | Duration | Description |
|------|----------|-------------|
| [Project Overview](./tours/overview.md) | 10 min | High-level structure |
| [First Request](./tours/first-request.md) | 15 min | Follow a request |
| [Adding a Feature](./tours/add-feature.md) | 20 min | End-to-end feature |

## Feature Tours
| Tour | Duration | Description |
|------|----------|-------------|
| [Authentication](./tours/auth.md) | 15 min | Login/logout flow |
| [Authorization](./tours/authz.md) | 15 min | Permissions system |
| [Data Pipeline](./tours/pipeline.md) | 20 min | ETL processing |

## Deep Dives
| Tour | Duration | Description |
|------|----------|-------------|
| [Database Layer](./tours/database.md) | 25 min | ORM and migrations |
| [Testing Strategy](./tours/testing.md) | 20 min | Test patterns |
| [Error Handling](./tours/errors.md) | 15 min | Error management |
```

## Tour Best Practices

### Keep Tours Focused

```markdown
✓ Good: "How user authentication works" (single topic)
✗ Bad: "Everything about users" (too broad)
```

### Include Working Examples

```markdown
✓ Good: Link to actual file locations
✓ Good: Show real code snippets
✓ Good: Include commands to run

✗ Bad: Describe without showing
✗ Bad: Use pseudo-code
✗ Bad: Reference outdated code
```

### Update with Code Changes

```markdown
When modifying toured code:
1. Run tours to verify they still work
2. Update line references
3. Update code snippets
4. Test tour flow makes sense
```

### Multiple Entry Points

```markdown
Different developers need different tours:
- New hire → Full overview tour
- Backend developer → API and services tour
- Frontend developer → UI and state tour
- DevOps → Infrastructure and deploy tour
```
