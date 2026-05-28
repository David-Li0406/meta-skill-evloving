# API Documentation Patterns

## OpenAPI/Swagger

### Basic Structure

```yaml
openapi: 3.0.3
info:
  title: User API
  description: API for managing users
  version: 1.0.0
  contact:
    email: api@example.com

servers:
  - url: https://api.example.com/v1
    description: Production
  - url: https://staging-api.example.com/v1
    description: Staging

paths:
  /users:
    get:
      summary: List users
      description: Returns a paginated list of users
      operationId: listUsers
      tags:
        - Users
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
            maximum: 100
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
        '401':
          $ref: '#/components/responses/Unauthorized'
```

### Schemas and Components

```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: integer
          format: int64
          description: Unique identifier
          example: 12345
        email:
          type: string
          format: email
          description: User's email address
          example: user@example.com
        name:
          type: string
          maxLength: 100
          example: John Doe
        createdAt:
          type: string
          format: date-time
          example: "2024-01-15T10:30:00Z"

    UserList:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          example: VALIDATION_ERROR
        message:
          type: string
          example: Invalid email format

  responses:
    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: UNAUTHORIZED
            message: Invalid or missing authentication token

  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

## Docstring Patterns

### Python

```python
def create_user(email: str, name: str | None = None) -> User:
    """Create a new user account.

    Creates a user with the given email address. The email must be unique
    across all users in the system.

    Args:
        email: The user's email address. Must be a valid email format.
        name: Optional display name. Defaults to email prefix if not provided.

    Returns:
        The newly created User object with generated ID.

    Raises:
        ValidationError: If email format is invalid.
        DuplicateError: If a user with this email already exists.

    Example:
        >>> user = create_user("john@example.com", name="John Doe")
        >>> print(user.id)
        12345
    """
```

### TypeScript/JSDoc

```typescript
/**
 * Create a new user account.
 *
 * Creates a user with the given email address. The email must be unique
 * across all users in the system.
 *
 * @param email - The user's email address. Must be a valid email format.
 * @param options - Optional configuration.
 * @param options.name - Display name. Defaults to email prefix.
 * @returns The newly created user with generated ID.
 * @throws {ValidationError} If email format is invalid.
 * @throws {DuplicateError} If user with email exists.
 *
 * @example
 * ```typescript
 * const user = await createUser("john@example.com", { name: "John" });
 * console.log(user.id); // 12345
 * ```
 */
export async function createUser(
  email: string,
  options?: { name?: string }
): Promise<User> {
```

### Go

```go
// CreateUser creates a new user account with the given email.
//
// The email must be unique across all users in the system.
// If name is empty, it defaults to the email prefix.
//
// CreateUser returns an error if the email format is invalid
// or if a user with this email already exists.
//
// Example:
//
//	user, err := CreateUser("john@example.com", "John Doe")
//	if err != nil {
//	    log.Fatal(err)
//	}
//	fmt.Println(user.ID)
func CreateUser(email, name string) (*User, error) {
```

## REST API Documentation Structure

### Endpoint Documentation

```markdown
## Create User

Create a new user account.

### Request

`POST /api/v1/users`

#### Headers

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |
| Content-Type | Yes | application/json |

#### Body

```json
{
  "email": "user@example.com",
  "name": "John Doe"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| email | string | Yes | Valid email address |
| name | string | No | Display name (max 100 chars) |

### Response

#### Success (201 Created)

```json
{
  "id": 12345,
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

#### Errors

| Status | Code | Description |
|--------|------|-------------|
| 400 | VALIDATION_ERROR | Invalid input |
| 401 | UNAUTHORIZED | Missing/invalid token |
| 409 | DUPLICATE_EMAIL | Email already exists |

### Example

```bash
curl -X POST https://api.example.com/v1/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "name": "John"}'
```
```

## Common Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| No examples | Harder to understand | Include request/response examples |
| Generic descriptions | Unclear behavior | Be specific about edge cases |
| Missing error codes | Can't handle errors | Document all error responses |
| Outdated docs | Misleading | Generate from code/tests |
| No authentication examples | Integration difficult | Show full auth flow |
| Missing rate limits | Unexpected failures | Document limits clearly |

## Tools

```bash
# Generate OpenAPI from code
# Python
pip install fastapi[all]  # Auto-generates OpenAPI

# TypeScript
npx @nestjs/cli generate openapi

# Validate OpenAPI spec
npx @redocly/cli lint openapi.yaml

# Generate docs site
npx redoc-cli bundle openapi.yaml -o docs.html
npx @stoplight/prism-cli mock openapi.yaml
```
