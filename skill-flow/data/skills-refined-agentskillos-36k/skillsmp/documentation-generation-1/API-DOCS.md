# API Documentation

Patterns for API documentation including JSDoc, Python docstrings, and OpenAPI specifications.

## JSDoc Patterns

### Function Documentation

```typescript
/**
 * Creates a new user in the system.
 *
 * @param userData - The user data for creation
 * @param options - Optional configuration
 * @returns The created user with generated ID
 *
 * @example
 * ```typescript
 * const user = await createUser({
 *   email: 'user@example.com',
 *   name: 'John Doe',
 * });
 * console.log(user.id); // 'usr_123abc'
 * ```
 *
 * @throws {ValidationError} If email format is invalid
 * @throws {DuplicateError} If user with email already exists
 *
 * @see {@link updateUser} for updating existing users
 * @see {@link deleteUser} for removing users
 *
 * @since 1.0.0
 */
async function createUser(
  userData: CreateUserInput,
  options?: CreateUserOptions
): Promise<User> {
  // implementation
}
```

### Class Documentation

```typescript
/**
 * HTTP client for making API requests.
 *
 * Handles authentication, retries, and error handling automatically.
 *
 * @example
 * ```typescript
 * const client = new ApiClient({
 *   baseUrl: 'https://api.example.com',
 *   apiKey: 'your-api-key',
 * });
 *
 * const users = await client.get('/users');
 * ```
 *
 * @see {@link ApiClientConfig} for configuration options
 */
class ApiClient {
  /**
   * Creates a new API client instance.
   *
   * @param config - Client configuration
   */
  constructor(config: ApiClientConfig) {
    // implementation
  }

  /**
   * Makes a GET request.
   *
   * @param path - API endpoint path
   * @param params - Query parameters
   * @returns Response data
   *
   * @example
   * ```typescript
   * const user = await client.get('/users/123');
   * ```
   */
  async get<T>(path: string, params?: Record<string, string>): Promise<T> {
    // implementation
  }
}
```

### Interface/Type Documentation

```typescript
/**
 * Configuration options for the API client.
 */
interface ApiClientConfig {
  /**
   * Base URL for API requests.
   * @example 'https://api.example.com/v1'
   */
  baseUrl: string;

  /**
   * API key for authentication.
   * Can also be set via `API_KEY` environment variable.
   */
  apiKey: string;

  /**
   * Request timeout in milliseconds.
   * @default 30000
   */
  timeout?: number;

  /**
   * Number of retry attempts for failed requests.
   * @default 3
   */
  retries?: number;

  /**
   * Custom headers to include in all requests.
   */
  headers?: Record<string, string>;
}
```

### Enum Documentation

```typescript
/**
 * HTTP methods supported by the client.
 */
enum HttpMethod {
  /** Read operations */
  GET = 'GET',
  /** Create operations */
  POST = 'POST',
  /** Full update operations */
  PUT = 'PUT',
  /** Partial update operations */
  PATCH = 'PATCH',
  /** Delete operations */
  DELETE = 'DELETE',
}
```

### Module Documentation

```typescript
/**
 * Authentication module for handling user sessions.
 *
 * @module auth
 *
 * @example
 * ```typescript
 * import { login, logout, getCurrentUser } from './auth';
 *
 * await login({ email: 'user@example.com', password: 'secret' });
 * const user = await getCurrentUser();
 * await logout();
 * ```
 */

export { login } from './login';
export { logout } from './logout';
export { getCurrentUser } from './session';
```

## JSDoc Tags Reference

| Tag | Usage | Description |
|-----|-------|-------------|
| `@param` | `@param name - Description` | Document parameter |
| `@returns` | `@returns Description` | Document return value |
| `@throws` | `@throws {Error} Description` | Document exceptions |
| `@example` | `@example code` | Provide usage example |
| `@see` | `@see {@link Other}` | Cross-reference |
| `@since` | `@since 1.0.0` | Version introduced |
| `@deprecated` | `@deprecated Use X instead` | Mark as deprecated |
| `@default` | `@default value` | Default value |
| `@readonly` | `@readonly` | Read-only property |
| `@internal` | `@internal` | Internal use only |
| `@public` | `@public` | Public API |
| `@private` | `@private` | Private member |
| `@template` | `@template T` | Generic type parameter |

## Python Docstring Patterns

### Google Style

```python
def create_user(user_data: UserInput, options: Options | None = None) -> User:
    """Create a new user in the system.

    Creates a user with the provided data and returns the created user
    object with a generated ID.

    Args:
        user_data: The user data for creation containing email and name.
        options: Optional configuration for user creation.
            Defaults to None.

    Returns:
        The created user with generated ID and timestamps.

    Raises:
        ValidationError: If the email format is invalid.
        DuplicateError: If a user with the email already exists.

    Example:
        >>> user = create_user(UserInput(email="user@example.com", name="John"))
        >>> print(user.id)
        'usr_123abc'

    Note:
        The user will receive a welcome email after creation.

    See Also:
        update_user: For updating existing users.
        delete_user: For removing users.
    """
```

### NumPy Style

```python
def calculate_statistics(data: list[float], weights: list[float] | None = None) -> Statistics:
    """Calculate weighted statistics for a dataset.

    Parameters
    ----------
    data : list[float]
        The input data values.
    weights : list[float], optional
        Weights for each data point. If None, uniform weights are used.

    Returns
    -------
    Statistics
        Object containing mean, median, std, and variance.

    Raises
    ------
    ValueError
        If data is empty or weights don't match data length.

    Examples
    --------
    >>> data = [1.0, 2.0, 3.0, 4.0, 5.0]
    >>> stats = calculate_statistics(data)
    >>> print(stats.mean)
    3.0

    >>> weights = [0.1, 0.2, 0.4, 0.2, 0.1]
    >>> weighted_stats = calculate_statistics(data, weights)
    >>> print(weighted_stats.mean)
    3.0

    See Also
    --------
    calculate_percentiles : Calculate percentile values.
    """
```

### Class Docstrings

```python
class ApiClient:
    """HTTP client for making API requests.

    Handles authentication, retries, and error handling automatically.
    Supports both sync and async operations.

    Attributes:
        base_url: The base URL for all API requests.
        timeout: Request timeout in seconds.

    Example:
        >>> client = ApiClient(
        ...     base_url="https://api.example.com",
        ...     api_key="your-key"
        ... )
        >>> users = client.get("/users")
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        timeout: int = 30,
    ) -> None:
        """Initialize the API client.

        Args:
            base_url: Base URL for API requests.
            api_key: API key for authentication.
            timeout: Request timeout in seconds. Defaults to 30.
        """
        self.base_url = base_url
        self._api_key = api_key
        self.timeout = timeout
```

## OpenAPI/Swagger Patterns

### Basic OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: User Management API
  description: |
    API for managing users in the system.

    ## Authentication
    All endpoints require an API key in the `X-API-Key` header.

    ## Rate Limiting
    Requests are limited to 100 per minute per API key.
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com
    url: https://example.com/support
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

tags:
  - name: users
    description: User management operations
  - name: auth
    description: Authentication operations

paths:
  /users:
    get:
      summary: List all users
      description: Returns a paginated list of users.
      operationId: listUsers
      tags:
        - users
      parameters:
        - name: page
          in: query
          description: Page number (1-indexed)
          schema:
            type: integer
            minimum: 1
            default: 1
        - name: limit
          in: query
          description: Items per page
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserList'
              example:
                users:
                  - id: usr_123
                    email: user@example.com
                    name: John Doe
                pagination:
                  page: 1
                  limit: 20
                  total: 45
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Create a user
      description: Creates a new user with the provided data.
      operationId: createUser
      tags:
        - users
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserInput'
            example:
              email: user@example.com
              name: John Doe
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          description: User with email already exists
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'

  /users/{userId}:
    get:
      summary: Get a user
      description: Returns a single user by ID.
      operationId: getUser
      tags:
        - users
      parameters:
        - name: userId
          in: path
          required: true
          description: User ID
          schema:
            type: string
            pattern: '^usr_[a-zA-Z0-9]+$'
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
        - createdAt
      properties:
        id:
          type: string
          description: Unique user identifier
          example: usr_123abc
        email:
          type: string
          format: email
          description: User's email address
          example: user@example.com
        name:
          type: string
          description: User's display name
          example: John Doe
        createdAt:
          type: string
          format: date-time
          description: When the user was created

    CreateUserInput:
      type: object
      required:
        - email
        - name
      properties:
        email:
          type: string
          format: email
          description: User's email address
        name:
          type: string
          minLength: 1
          maxLength: 100
          description: User's display name

    UserList:
      type: object
      properties:
        users:
          type: array
          items:
            $ref: '#/components/schemas/User'
        pagination:
          $ref: '#/components/schemas/Pagination'

    Pagination:
      type: object
      properties:
        page:
          type: integer
          description: Current page number
        limit:
          type: integer
          description: Items per page
        total:
          type: integer
          description: Total number of items

    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: Error code
        message:
          type: string
          description: Human-readable error message
        details:
          type: object
          additionalProperties: true
          description: Additional error details

  responses:
    BadRequest:
      description: Invalid request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: VALIDATION_ERROR
            message: Invalid email format

    Unauthorized:
      description: Authentication required
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: UNAUTHORIZED
            message: API key required

    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: NOT_FOUND
            message: User not found

  securitySchemes:
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key

security:
  - apiKey: []
```

### Generating OpenAPI from Code

#### TypeScript with tsoa

```typescript
// controllers/users.controller.ts
import { Controller, Get, Post, Body, Path, Query, Route, Tags, Security } from 'tsoa';

@Route('users')
@Tags('Users')
export class UsersController extends Controller {
  /**
   * List all users with pagination
   * @param page Page number
   * @param limit Items per page
   */
  @Get()
  @Security('apiKey')
  public async listUsers(
    @Query() page: number = 1,
    @Query() limit: number = 20
  ): Promise<UserListResponse> {
    // implementation
  }

  /**
   * Create a new user
   * @param body User data
   */
  @Post()
  @Security('apiKey')
  public async createUser(@Body() body: CreateUserInput): Promise<User> {
    // implementation
  }
}
```

#### Python with FastAPI

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, EmailStr

app = FastAPI(
    title="User Management API",
    description="API for managing users",
    version="1.0.0",
)


class User(BaseModel):
    """User model."""

    id: str = Field(..., description="Unique user identifier", example="usr_123")
    email: EmailStr = Field(..., description="User's email address")
    name: str = Field(..., description="User's display name")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "usr_123",
                "email": "user@example.com",
                "name": "John Doe",
            }
        }


class CreateUserInput(BaseModel):
    """Input for creating a user."""

    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


@app.get("/users", response_model=list[User], tags=["users"])
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
) -> list[User]:
    """List all users with pagination."""
    # implementation
    pass


@app.post("/users", response_model=User, status_code=201, tags=["users"])
async def create_user(user: CreateUserInput) -> User:
    """Create a new user."""
    # implementation
    pass
```

## Inline Comment Patterns

### Algorithm Explanation

```typescript
function binarySearch(arr: number[], target: number): number {
  let left = 0;
  let right = arr.length - 1;

  // Continue searching while the window is valid
  while (left <= right) {
    // Calculate mid without integer overflow
    // (left + right) / 2 could overflow in some languages
    const mid = left + Math.floor((right - left) / 2);

    if (arr[mid] === target) {
      return mid;
    }

    // Target is in the right half
    if (arr[mid] < target) {
      left = mid + 1;
    }
    // Target is in the left half
    else {
      right = mid - 1;
    }
  }

  // Target not found
  return -1;
}
```

### Business Logic Explanation

```typescript
function calculateDiscount(order: Order): number {
  let discount = 0;

  // First-time customer bonus: 10% off
  if (order.customer.isFirstOrder) {
    discount += 0.1;
  }

  // Volume discount: 5% off for orders over $100
  // This stacks with first-order discount per marketing policy
  if (order.subtotal > 100) {
    discount += 0.05;
  }

  // Holiday promotion: Additional 15% off
  // Active Dec 1-31, approved by marketing team
  if (isHolidaySeason()) {
    discount += 0.15;
  }

  // Cap total discount at 25% per finance policy
  return Math.min(discount, 0.25);
}
```

### Workaround Documentation

```typescript
function parseDate(input: string): Date {
  // WORKAROUND: Safari doesn't support YYYY-MM-DD format in Date.parse()
  // See: https://bugs.webkit.org/show_bug.cgi?id=XXXXX
  // TODO: Remove when Safari 17+ has sufficient market share
  const parts = input.split('-');
  if (parts.length === 3) {
    return new Date(
      parseInt(parts[0]),
      parseInt(parts[1]) - 1, // Month is 0-indexed
      parseInt(parts[2])
    );
  }

  return new Date(input);
}
```

## Documentation Generation Tools

| Language | Tool | Command |
|----------|------|---------|
| TypeScript | TypeDoc | `npx typedoc src/index.ts` |
| JavaScript | JSDoc | `npx jsdoc src -d docs` |
| Python | Sphinx | `sphinx-build docs docs/_build` |
| Python | pdoc | `pdoc --html src` |
| Go | godoc | `godoc -http=:6060` |
| Rust | rustdoc | `cargo doc` |
| OpenAPI | Swagger UI | Host `openapi.yaml` |
| OpenAPI | Redoc | `npx redoc-cli build openapi.yaml` |

## Best Practices

### Do

- Document public APIs thoroughly
- Include working examples
- Document exceptions/errors
- Use consistent style (JSDoc, Google, NumPy)
- Keep examples up to date
- Cross-reference related functions

### Don't

- Document internal implementation details
- Write obvious comments
- Duplicate type information available from types
- Leave TODO comments in public docs
- Include sensitive information
