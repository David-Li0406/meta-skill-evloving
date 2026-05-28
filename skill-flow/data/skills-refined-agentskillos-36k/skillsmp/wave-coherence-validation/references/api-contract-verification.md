# API Contract Verification

Detailed procedures for testing and verifying API endpoints before frontend integration.

---

## Priority 1: Live API Testing

### Prerequisites

```bash
# Check if development server is running
curl -s http://localhost:3000/health

# If not running, start it
npm run dev
# or
python manage.py runserver
# or
./gradlew bootRun
```

---

## REST API Testing

### GET Requests

```bash
# Basic GET request
curl -X GET http://localhost:3000/api/users/123

# GET with query parameters
curl -X GET "http://localhost:3000/api/users?page=1&limit=10"

# GET with authentication header
curl -X GET http://localhost:3000/api/users/123 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# GET with multiple headers
curl -X GET http://localhost:3000/api/users/123 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Accept: application/json"
```

**Expected Response Documentation**:
```json
{
  "status_code": 200,
  "headers": {
    "content-type": "application/json",
    "cache-control": "no-cache"
  },
  "body": {
    "id": "123",
    "name": "John Doe",
    "email": "john@example.com",
    "createdAt": "2025-01-30T12:00:00Z"
  }
}
```

---

### POST Requests

```bash
# Basic POST request
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Jane Doe","email":"jane@example.com"}'

# POST with authentication
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"name":"Jane Doe","email":"jane@example.com"}'

# POST with file upload
curl -X POST http://localhost:3000/api/users/123/avatar \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "avatar=@/path/to/image.jpg"
```

**Expected Response Documentation**:
```json
{
  "status_code": 201,
  "headers": {
    "content-type": "application/json",
    "location": "/api/users/456"
  },
  "body": {
    "id": "456",
    "name": "Jane Doe",
    "email": "jane@example.com",
    "createdAt": "2025-01-30T12:05:00Z"
  }
}
```

---

### PUT/PATCH Requests

```bash
# PUT (full update)
curl -X PUT http://localhost:3000/api/users/123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"name":"John Smith","email":"john.smith@example.com"}'

# PATCH (partial update)
curl -X PATCH http://localhost:3000/api/users/123 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -d '{"name":"John Smith"}'
```

**Expected Response Documentation**:
```json
{
  "status_code": 200,
  "body": {
    "id": "123",
    "name": "John Smith",
    "email": "john.smith@example.com",
    "updatedAt": "2025-01-30T12:10:00Z"
  }
}
```

---

### DELETE Requests

```bash
# DELETE request
curl -X DELETE http://localhost:3000/api/users/123 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# DELETE with soft delete (may return updated record)
curl -X DELETE http://localhost:3000/api/users/123 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Accept: application/json"
```

**Expected Response Documentation**:
```json
{
  "status_code": 204,
  "body": null
}

// OR (if soft delete)
{
  "status_code": 200,
  "body": {
    "id": "123",
    "deletedAt": "2025-01-30T12:15:00Z"
  }
}
```

---

## Error Response Testing

### Test Expected Errors

```bash
# Test 400 Bad Request (invalid data)
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"","email":"invalid-email"}'

# Test 401 Unauthorized (no auth token)
curl -X GET http://localhost:3000/api/users/123

# Test 403 Forbidden (insufficient permissions)
curl -X DELETE http://localhost:3000/api/users/123 \
  -H "Authorization: Bearer LIMITED_USER_TOKEN"

# Test 404 Not Found (resource doesn't exist)
curl -X GET http://localhost:3000/api/users/999999

# Test 409 Conflict (duplicate resource)
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"existing@example.com"}'

# Test 422 Unprocessable Entity (validation error)
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"A","email":"test@example.com"}'  # name too short

# Test 500 Internal Server Error (trigger error condition if possible)
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","role":"INVALID_ROLE"}'
```

**Expected Error Response Documentation**:
```json
// 400 Bad Request
{
  "status_code": 400,
  "body": {
    "error": "Bad Request",
    "message": "Invalid email format",
    "field": "email"
  }
}

// 401 Unauthorized
{
  "status_code": 401,
  "body": {
    "error": "Unauthorized",
    "message": "Authentication required"
  }
}

// 404 Not Found
{
  "status_code": 404,
  "body": {
    "error": "Not Found",
    "message": "User not found",
    "resourceId": "999999"
  }
}

// 422 Unprocessable Entity
{
  "status_code": 422,
  "body": {
    "error": "Validation Error",
    "message": "Request validation failed",
    "errors": [
      {
        "field": "name",
        "message": "Name must be at least 2 characters"
      }
    ]
  }
}
```

---

## Using HTTP Testing Tools

### HTTPie (User-Friendly)

```bash
# Install
pip install httpie

# GET request
http GET http://localhost:3000/api/users/123

# POST request
http POST http://localhost:3000/api/users \
  name="Jane Doe" \
  email="jane@example.com"

# With authentication
http GET http://localhost:3000/api/users/123 \
  Authorization:"Bearer YOUR_TOKEN"
```

### Postman (GUI Alternative)

```
1. Open Postman
2. Create new request
3. Set method: GET
4. Set URL: http://localhost:3000/api/users/123
5. Add headers if needed
6. Click "Send"
7. Document response in API contract file
```

---

## Priority 2: Code Analysis

If API cannot be tested live, analyze the source code.

### Node.js/Express Analysis

```typescript
// Read route file
// File: src/routes/users.ts

router.get('/users/:id', async (req, res) => {
  try {
    const user = await userService.getById(req.params.id);

    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    res.json(user);  // ← Document this response format
  } catch (error) {
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Document findings:
```

**API Contract from Code**:
```yaml
endpoint: GET /api/users/:id
parameters:
  path:
    - id (string, required)
responses:
  200:
    body:
      type: User
      example: { id, name, email }
  404:
    body:
      error: "User not found"
  500:
    body:
      error: "Internal server error"
```

---

### Python/FastAPI Analysis

```python
# Read route file
# File: app/routes/users.py

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str) -> User:
    user = await user_service.get_by_id(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user  # ← Pydantic model defines response structure

# Document findings:
```

**API Contract from Code**:
```yaml
endpoint: GET /api/users/{user_id}
parameters:
  path:
    - user_id (string, required)
responses:
  200:
    body:
      type: User (Pydantic model)
      schema: app/schemas/user.py
  404:
    body:
      detail: "User not found"
```

---

### Java/Spring Analysis

```java
// Read controller file
// File: src/main/java/controllers/UserController.java

@GetMapping("/{id}")
public ResponseEntity<User> getUser(@PathVariable UUID id) {
    Optional<User> user = userService.findById(id);

    if (user.isEmpty()) {
        return ResponseEntity.notFound().build();
    }

    return ResponseEntity.ok(user.get());  // ← User DTO defines structure
}

// Document findings:
```

**API Contract from Code**:
```yaml
endpoint: GET /api/users/{id}
parameters:
  path:
    - id (UUID, required)
responses:
  200:
    body:
      type: User (DTO)
      class: com.example.dto.User
  404:
    body: null (empty)
```

---

## Priority 3: Test File Analysis

If code is unclear, read existing tests.

### Jest/TypeScript Tests

```typescript
// File: src/routes/users.test.ts

describe('GET /api/users/:id', () => {
  it('should return user by id', async () => {
    const response = await request(app)
      .get('/api/users/123')
      .expect(200);

    expect(response.body).toEqual({
      id: '123',
      name: expect.any(String),
      email: expect.any(String)
    });
    // ↑ This documents expected response structure
  });

  it('should return 404 for non-existent user', async () => {
    const response = await request(app)
      .get('/api/users/999')
      .expect(404);

    expect(response.body).toEqual({
      error: 'User not found'
    });
    // ↑ This documents error response
  });
});
```

**API Contract from Tests**:
```yaml
endpoint: GET /api/users/:id
responses:
  200:
    body:
      id: string
      name: string
      email: string
  404:
    body:
      error: "User not found"
```

---

### Pytest Tests

```python
# File: tests/test_users.py

def test_get_user_success(client):
    response = client.get("/api/users/123")
    assert response.status_code == 200

    data = response.json()
    assert "id" in data
    assert "name" in data
    assert "email" in data
    # ↑ Documents expected fields

def test_get_user_not_found(client):
    response = client.get("/api/users/999")
    assert response.status_code == 404

    data = response.json()
    assert data["detail"] == "User not found"
    # ↑ Documents error response
```

**API Contract from Tests**:
```yaml
endpoint: GET /api/users/{id}
responses:
  200:
    body:
      fields: [id, name, email]
  404:
    body:
      detail: "User not found"
```

---

## Contract Validation Checklist

After testing/analyzing API, document:

- [ ] **Endpoint URL**: Full path including parameters
- [ ] **HTTP Method**: GET, POST, PUT, PATCH, DELETE
- [ ] **Request Headers**: Required headers (Content-Type, Authorization)
- [ ] **Request Body**: Structure and required fields (for POST/PUT/PATCH)
- [ ] **Response Status Codes**: All possible codes (200, 201, 400, 404, etc.)
- [ ] **Response Body**: Structure and field types
- [ ] **Error Responses**: Format and messages for each error code
- [ ] **Authentication**: Required authentication method
- [ ] **Rate Limiting**: Any rate limits or throttling

---

## API Contract Template

```yaml
# API Contract: User Management

## GET /api/users/:id

### Request
- Method: GET
- URL: /api/users/:id
- Headers:
  - Authorization: Bearer {token} (required)
  - Accept: application/json
- Parameters:
  - id (path, string, required): User ID

### Response: 200 OK
```json
{
  "id": "123",
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2025-01-30T12:00:00Z",
  "updatedAt": "2025-01-30T12:00:00Z"
}
```

### Response: 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Authentication required"
}
```

### Response: 404 Not Found
```json
{
  "error": "Not Found",
  "message": "User not found"
}
```

---

## POST /api/users

### Request
- Method: POST
- URL: /api/users
- Headers:
  - Authorization: Bearer {token} (required)
  - Content-Type: application/json
- Body:
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com"
}
```

### Response: 201 Created
```json
{
  "id": "456",
  "name": "Jane Doe",
  "email": "jane@example.com",
  "createdAt": "2025-01-30T12:05:00Z",
  "updatedAt": "2025-01-30T12:05:00Z"
}
```

### Response: 400 Bad Request
```json
{
  "error": "Validation Error",
  "message": "Invalid request body",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    }
  ]
}
```

### Response: 409 Conflict
```json
{
  "error": "Conflict",
  "message": "User with this email already exists"
}
```
```

---

## Integration Verification

After documenting API contract, verify frontend integration:

### Frontend Code Review

```typescript
// Frontend API client
// File: src/api/userApi.ts

export async function getUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`, {
    headers: {
      'Authorization': `Bearer ${getToken()}`,
      'Accept': 'application/json'
    }
  });

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error('User not found');
    }
    throw new Error('Failed to fetch user');
  }

  return response.json();
}

// Verification checklist:
// ✅ URL matches API: /api/users/:id
// ✅ Headers match API: Authorization, Accept
// ✅ Error handling covers: 404, other errors
// ✅ Response type matches: Promise<User>
// ⚠️ TODO: Verify User interface matches API response structure
```

### Type Definition Verification

```typescript
// Check if User interface matches API response
// File: src/types/user.ts

interface User {
  id: string;
  name: string;
  email: string;
  createdAt: string;  // ← Should be ISO string matching API
  updatedAt: string;
}

// Compare with actual API response:
// {
//   "id": "123",
//   "name": "John Doe",
//   "email": "john@example.com",
//   "createdAt": "2025-01-30T12:00:00Z",
//   "updatedAt": "2025-01-30T12:00:00Z"
// }

// ✅ All fields match!
```

---

## Common Integration Issues

### Issue 1: Field Name Mismatch

```typescript
// API returns:
{ user_id: "123", user_name: "John" }

// Frontend expects:
{ id: "123", name: "John" }

// Solution: Transform response
const user = await response.json();
return {
  id: user.user_id,
  name: user.user_name
};
```

### Issue 2: Date Format Mismatch

```typescript
// API returns:
{ createdAt: "2025-01-30T12:00:00Z" }  // ISO string

// Frontend expects:
{ createdAt: Date }  // Date object

// Solution: Parse dates
const user = await response.json();
return {
  ...user,
  createdAt: new Date(user.createdAt)
};
```

### Issue 3: Missing Error Handling

```typescript
// ❌ Bad: No error handling
export async function getUser(id: string) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();  // Fails silently on errors
}

// ✅ Good: Proper error handling
export async function getUser(id: string) {
  const response = await fetch(`/api/users/${id}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || 'Failed to fetch user');
  }

  return response.json();
}
```

---

**Last Updated**: 2025-01-30
