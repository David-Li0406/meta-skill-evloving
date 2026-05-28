---
name: api-design
description: REST and HTTP API design best practices including endpoint naming, request/response formats, error handling, versioning, and documentation standards
version: 1.0.0
priority: 25
tags:
  - api
  - rest
  - http
  - design
  - builtin
triggers:
  - type: keyword
    pattern: api
  - type: keyword
    pattern: endpoint
  - type: keyword
    pattern: rest
  - type: glob
    pattern: "**/routes/**"
  - type: glob
    pattern: "**/api/**"
globs:
  - "**/routes/**/*.ts"
  - "**/api/**/*.ts"
  - "**/controllers/**/*.ts"
---

# API Design

Guidelines for designing consistent, intuitive, and maintainable HTTP APIs.

## Rules

- **Resource-Oriented URLs**: Use nouns (not verbs) for resource names
- **Consistent Naming**: Use kebab-case for URLs, camelCase for JSON properties
- **Proper HTTP Methods**: GET (read), POST (create), PUT/PATCH (update), DELETE (remove)
- **Status Codes**: Use appropriate HTTP status codes for all responses
- **Pagination**: Always paginate list endpoints; use cursor-based for large datasets
- **Versioning**: Include API version in URL path (`/v1/`) or header
- **Error Format**: Use consistent error response schema across all endpoints
- **Idempotency**: POST/PATCH/PUT should be idempotent where possible
- **Rate Limiting**: Include rate limit headers in responses

## Patterns

### URL Structure

```markdown
# Collection operations
GET    /v1/users              # List users (paginated)
POST   /v1/users              # Create user

# Resource operations
GET    /v1/users/{id}         # Get user by ID
PUT    /v1/users/{id}         # Replace user
PATCH  /v1/users/{id}         # Partial update
DELETE /v1/users/{id}         # Delete user

# Nested resources
GET    /v1/users/{id}/posts   # User's posts
POST   /v1/users/{id}/posts   # Create post for user

# Actions (when needed)
POST   /v1/users/{id}/verify  # Trigger verification
POST   /v1/orders/{id}/cancel # Cancel order

# Filtering, sorting, searching
GET    /v1/users?status=active&sort=-createdAt&q=john
```

### Response Format

```typescript
// Success response (single resource)
interface SuccessResponse<T> {
  data: T;
  meta?: {
    requestId: string;
    timestamp: string;
  };
}

// Success response (collection)
interface CollectionResponse<T> {
  data: T[];
  pagination: {
    total: number;
    page: number;
    pageSize: number;
    totalPages: number;
    hasNext: boolean;
    hasPrev: boolean;
  };
  meta?: {
    requestId: string;
    timestamp: string;
  };
}

// Example: GET /v1/users/123
{
  "data": {
    "id": "123",
    "email": "user@example.com",
    "name": "John Doe",
    "createdAt": "2024-01-15T10:30:00Z",
    "updatedAt": "2024-01-15T10:30:00Z"
  },
  "meta": {
    "requestId": "req_abc123",
    "timestamp": "2024-01-15T12:00:00Z"
  }
}
```markdown

### Error Response Format

```typescript
interface ErrorResponse {
  error: {
    code: string;           // Machine-readable error code
    message: string;        // Human-readable message
    details?: ErrorDetail[]; // Field-level errors
    requestId: string;      // For support/debugging
  };
}

interface ErrorDetail {
  field: string;
  code: string;
  message: string;
}

// Example: 400 Bad Request
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Email must be a valid email address"
      },
      {
        "field": "password",
        "code": "TOO_SHORT",
        "message": "Password must be at least 8 characters"
      }
    ],
    "requestId": "req_xyz789"
  }
}

// Example: 404 Not Found
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User not found",
    "requestId": "req_xyz789"
  }
}
```markdown

### HTTP Status Codes

```typescript
// 2xx Success
200 OK              // GET success, PUT/PATCH success with body
201 Created         // POST success (include Location header)
204 No Content      // DELETE success, PUT/PATCH success without body

// 4xx Client Errors
400 Bad Request     // Validation error, malformed request
401 Unauthorized    // Missing or invalid authentication
403 Forbidden       // Authenticated but not authorized
404 Not Found       // Resource doesn't exist
409 Conflict        // State conflict (e.g., duplicate)
422 Unprocessable   // Valid syntax but semantic errors
429 Too Many Reqs   // Rate limit exceeded

// 5xx Server Errors
500 Internal Error  // Unexpected server error
502 Bad Gateway     // Upstream service error
503 Unavailable     // Service temporarily down
504 Gateway Timeout // Upstream timeout
```markdown

### Pagination (Cursor-Based)

```typescript
// Request
GET /v1/posts?limit=20&cursor=eyJpZCI6MTIzfQ

// Response
{
  "data": [...],
  "pagination": {
    "limit": 20,
    "hasMore": true,
    "nextCursor": "eyJpZCI6MTQzfQ",
    "prevCursor": "eyJpZCI6MTAzfQ"
  }
}

// Cursor implementation
interface PaginationCursor {
  id: string;
  createdAt?: string;  // For stable sorting
}

function encodeCursor(cursor: PaginationCursor): string {
  return Buffer.from(JSON.stringify(cursor)).toString("base64url");
}

function decodeCursor(encoded: string): PaginationCursor {
  return JSON.parse(Buffer.from(encoded, "base64url").toString());
}
```markdown

### Request Validation with Zod

```typescript
import { z } from "zod";

// Define schemas
const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  role: z.enum(["user", "admin"]).default("user"),
});

const updateUserSchema = createUserSchema.partial();

const paginationSchema = z.object({
  page: z.coerce.number().int().positive().default(1),
  pageSize: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.string().optional(),
});

// Type inference
type CreateUserInput = z.infer<typeof createUserSchema>;

// Validation middleware
function validateBody<T extends z.ZodSchema>(schema: T) {
  return (req: Request, res: Response, next: NextFunction) => {
    const result = schema.safeParse(req.body);
    if (!result.success) {
      return res.status(400).json({
        error: {
          code: "VALIDATION_ERROR",
          message: "Request validation failed",
          details: result.error.errors.map((e) => ({
            field: e.path.join("."),
            code: e.code.toUpperCase(),
            message: e.message,
          })),
          requestId: req.id,
        },
      });
    }
    req.validated = result.data;
    next();
  };
}
```markdown

## Anti-Patterns

```typescript
// ❌ Verbs in URLs
GET /v1/getUsers
POST /v1/createUser
DELETE /v1/deleteUser/123

// ✅ Resource-based URLs
GET /v1/users
POST /v1/users
DELETE /v1/users/123

// ❌ Inconsistent casing
GET /v1/UserAccounts
POST /v1/user_settings
// ✅ Consistent kebab-case
GET /v1/user-accounts
POST /v1/user-settings

// ❌ Returning 200 for errors
{
  "success": false,
  "error": "User not found"
}
// ✅ Use proper status codes
// 404 Not Found with error body

// ❌ Exposing internal IDs/structure
{
  "userId": 12345,
  "mysqlRowId": 67890
}
// ✅ Use UUIDs or public identifiers
{
  "id": "usr_abc123def456"
}

// ❌ Returning unbounded lists
GET /v1/users  // Returns 100,000 users
// ✅ Always paginate
GET /v1/users?page=1&pageSize=20

// ❌ Breaking changes without versioning
// Changed field name from "userName" to "name"
// ✅ Maintain backward compatibility or version
```markdown

## Examples

### Express Router Implementation

```typescript
import { Router } from "express";
import { z } from "zod";

const router = Router();

// GET /v1/users
router.get("/users", async (req, res, next) => {
  try {
    const query = paginationSchema.parse(req.query);
    const { users, total } = await userService.list(query);

    res.json({
      data: users.map(toUserDTO),
      pagination: {
        total,
        page: query.page,
        pageSize: query.pageSize,
        totalPages: Math.ceil(total / query.pageSize),
        hasNext: query.page * query.pageSize < total,
        hasPrev: query.page > 1,
      },
    });
  } catch (error) {
    next(error);
  }
});

// POST /v1/users
router.post("/users", validateBody(createUserSchema), async (req, res, next) => {
  try {
    const user = await userService.create(req.validated);

    res.status(201)
      .header("Location", `/v1/users/${user.id}`)
      .json({ data: toUserDTO(user) });
  } catch (error) {
    if (error instanceof DuplicateError) {
      return res.status(409).json({
        error: {
          code: "DUPLICATE_RESOURCE",
          message: "User with this email already exists",
          requestId: req.id,
        },
      });
    }
    next(error);
  }
});

// DELETE /v1/users/:id
router.delete("/users/:id", async (req, res, next) => {
  try {
    const deleted = await userService.delete(req.params.id);

    if (!deleted) {
      return res.status(404).json({
        error: {
          code: "RESOURCE_NOT_FOUND",
          message: "User not found",
          requestId: req.id,
        },
      });
    }

    res.status(204).send();
  } catch (error) {
    next(error);
  }
});

export default router;
```markdown

### OpenAPI Documentation

```yaml
openapi: 3.0.3
info:
  title: User API
  version: 1.0.0

paths:
  /v1/users:
    get:
      summary: List users
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: pageSize
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
      responses:
        "200":
          description: Users list
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/UserListResponse"

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
          format: email
        name:
          type: string
        createdAt:
          type: string
          format: date-time
```

## References

- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [Google API Design Guide](https://cloud.google.com/apis/design)
- [JSON:API Specification](https://jsonapi.org/)
- [RFC 7807 - Problem Details](https://tools.ietf.org/html/rfc7807)
