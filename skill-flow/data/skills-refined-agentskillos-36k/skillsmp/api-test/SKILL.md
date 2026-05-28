---
name: api-test
version: 1.0.0
lastUpdated: 2026-01-18
description: Test Next.js Route Handlers and API endpoints using Playwright for real HTTP requests. Use when testing API endpoints, route handlers, or backend integrations.
tags: [testing, api, route-handlers, playwright, e2e]
author: Szum Tech Team
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, mcp__playwright__browser_navigate, mcp__playwright__browser_snapshot, mcp__playwright__browser_network_requests, mcp__context7__resolve-library-id, mcp__context7__get-library-docs
context: fork
agent: general-purpose
user-invocable: true
examples:
  - Test POST /api/budgets endpoint
  - Verify authentication on /api/users route
  - Test error handling for /api/expenses
  - Create API test suite for onboarding endpoints
---

# API Test Skill

Test Next.js Route Handlers with real HTTP requests using Playwright. This skill creates comprehensive API tests that verify endpoint behavior, authentication, validation, and error handling.

## First Step: Read Project Context

**IMPORTANT**: Before creating API tests, check `.claude/project-context.md` for:

- **Authentication method** (Clerk, NextAuth, JWT, API Key)
- **Auth testing pattern** (test tokens, session cookies, headers)
- **API response format** (ActionResponse, custom format)
- **Error handling patterns** (DbError codes, HTTP status mapping)

Also check `CLAUDE.md` for:
- Server Actions patterns (ActionResponse type)
- Database error handling (DbError class)

## Context

This skill helps you test:

- Route Handler responses (GET, POST, PUT, DELETE, PATCH)
- Authentication and authorization
- Request validation with Zod schemas
- Error handling and status codes
- Response body structure
- Headers and cookies

## Prerequisites

- Next.js dev server running (`npm run dev`)
- Playwright installed (included in project)
- Test files go in `tests/e2e/api/`

## Instructions

When the user requests API tests:

### 1. Analyze the Endpoint

Gather information about:
- HTTP method(s) supported
- Request body schema (if any)
- Query parameters
- Authentication requirements
- Expected response structure
- Error cases to handle

### 2. Create Test File

**File Location:** `tests/e2e/api/[endpoint-name].spec.ts`

**Test Template:**

```typescript
import { test, expect } from "@playwright/test";

/**
 * API Tests for: [Endpoint Path]
 *
 * Route Handler: app/api/[path]/route.ts
 * Methods: GET, POST, etc.
 *
 * Authentication: Required / Not Required
 */

const BASE_URL = process.env.PLAYWRIGHT_BASE_URL ?? "http://localhost:3000";
const API_ENDPOINT = "/api/endpoint-name";

test.describe("API: [Endpoint Name]", () => {
  test.describe("Authentication", () => {
    test("returns 401 for unauthenticated requests", async ({ request }) => {
      const response = await request.get(`${BASE_URL}${API_ENDPOINT}`);

      expect(response.status()).toBe(401);
      const body = await response.json();
      expect(body).toHaveProperty("error");
    });
  });

  test.describe("GET requests", () => {
    test("returns 200 with valid data", async ({ request }) => {
      const response = await request.get(`${BASE_URL}${API_ENDPOINT}`, {
        headers: {
          // Add auth headers if needed
          // "Authorization": `Bearer ${token}`
        }
      });

      expect(response.status()).toBe(200);
      const body = await response.json();

      // Verify response structure
      expect(body).toHaveProperty("data");
      expect(Array.isArray(body.data)).toBe(true);
    });

    test("supports pagination parameters", async ({ request }) => {
      const response = await request.get(
        `${BASE_URL}${API_ENDPOINT}?page=1&limit=10`
      );

      expect(response.status()).toBe(200);
      const body = await response.json();
      expect(body.data.length).toBeLessThanOrEqual(10);
    });
  });

  test.describe("POST requests", () => {
    test("creates resource with valid data", async ({ request }) => {
      const response = await request.post(`${BASE_URL}${API_ENDPOINT}`, {
        data: {
          name: "Test Resource",
          description: "Test description"
        },
        headers: {
          "Content-Type": "application/json"
        }
      });

      expect(response.status()).toBe(201);
      const body = await response.json();

      expect(body).toHaveProperty("data");
      expect(body.data).toHaveProperty("id");
      expect(body.data.name).toBe("Test Resource");
    });

    test("returns 400 for invalid data", async ({ request }) => {
      const response = await request.post(`${BASE_URL}${API_ENDPOINT}`, {
        data: {
          // Missing required fields
        },
        headers: {
          "Content-Type": "application/json"
        }
      });

      expect(response.status()).toBe(400);
      const body = await response.json();

      expect(body).toHaveProperty("error");
      // Check for validation error details
      expect(body).toHaveProperty("details");
    });

    test("returns 409 for duplicate resource", async ({ request }) => {
      // First create
      await request.post(`${BASE_URL}${API_ENDPOINT}`, {
        data: { name: "Unique Name" }
      });

      // Second create with same data
      const response = await request.post(`${BASE_URL}${API_ENDPOINT}`, {
        data: { name: "Unique Name" }
      });

      expect(response.status()).toBe(409);
    });
  });

  test.describe("Error Handling", () => {
    test("returns 404 for non-existent resource", async ({ request }) => {
      const response = await request.get(
        `${BASE_URL}${API_ENDPOINT}/non-existent-id`
      );

      expect(response.status()).toBe(404);
      const body = await response.json();
      expect(body.error).toContain("not found");
    });

    test("returns 500 for server errors gracefully", async ({ request }) => {
      // Trigger server error condition if possible
      const response = await request.post(`${BASE_URL}${API_ENDPOINT}`, {
        data: { triggerError: true }
      });

      // Should return error, not crash
      expect(response.status()).toBeGreaterThanOrEqual(400);
      const body = await response.json();
      expect(body).toHaveProperty("error");
    });
  });
});
```

### 3. Test Patterns

#### Testing with Authentication

Check `project-context.md` for your auth provider and use the appropriate pattern:

```typescript
import { test, expect } from "@playwright/test";

test.describe("Authenticated API Tests", () => {
  let authToken: string;

  test.beforeAll(async () => {
    // Get auth token from environment or test setup
    authToken = process.env.TEST_AUTH_TOKEN!;
  });

  test("authenticated request succeeds", async ({ request }) => {
    const response = await request.get(`${BASE_URL}/api/protected`, {
      headers: getAuthHeaders(authToken)
    });

    expect(response.status()).toBe(200);
  });
});

// Auth header helpers - use the one matching your provider
function getAuthHeaders(token: string): Record<string, string> {
  // Clerk:
  // return { Cookie: `__session=${token}` };

  // NextAuth:
  // return { Cookie: `next-auth.session-token=${token}` };

  // JWT Bearer:
  // return { Authorization: `Bearer ${token}` };

  // API Key:
  // return { 'X-API-Key': token };

  // Check project-context.md for your pattern
  return { Authorization: `Bearer ${token}` };
}
```

#### Testing Request Validation

```typescript
test.describe("Validation", () => {
  const invalidPayloads = [
    { payload: {}, error: "name is required" },
    { payload: { name: "" }, error: "name cannot be empty" },
    { payload: { name: "x".repeat(256) }, error: "name too long" },
    { payload: { name: "valid", amount: "not-a-number" }, error: "amount must be number" }
  ];

  for (const { payload, error } of invalidPayloads) {
    test(`rejects invalid payload: ${error}`, async ({ request }) => {
      const response = await request.post(`${BASE_URL}${API_ENDPOINT}`, {
        data: payload
      });

      expect(response.status()).toBe(400);
      const body = await response.json();
      expect(body.error).toContain(error);
    });
  }
});
```

#### Testing Response Headers

```typescript
test("returns correct headers", async ({ request }) => {
  const response = await request.get(`${BASE_URL}${API_ENDPOINT}`);

  expect(response.headers()["content-type"]).toContain("application/json");
  expect(response.headers()["cache-control"]).toBeDefined();
});
```

#### Testing Rate Limiting (if implemented)

```typescript
test("enforces rate limiting", async ({ request }) => {
  const requests = Array.from({ length: 20 }, () =>
    request.get(`${BASE_URL}${API_ENDPOINT}`)
  );

  const responses = await Promise.all(requests);
  const tooManyRequests = responses.filter((r) => r.status() === 429);

  expect(tooManyRequests.length).toBeGreaterThan(0);
});
```

### 4. Running Tests

```bash
# Run all API tests
npm run test:e2e -- tests/e2e/api/

# Run specific endpoint tests
npm run test:e2e -- tests/e2e/api/budgets.spec.ts

# Run with UI mode for debugging
npm run test:e2e:ui -- tests/e2e/api/

# Run in headed mode
npm run test:e2e -- --headed tests/e2e/api/
```

### 5. Test Organization

```
tests/e2e/api/
├── auth/
│   ├── login.spec.ts
│   └── logout.spec.ts
├── budgets/
│   ├── create-budget.spec.ts
│   ├── get-budgets.spec.ts
│   └── update-budget.spec.ts
├── health.spec.ts
└── fixtures/
    └── test-data.ts
```

## Common Test Scenarios

### Health Check Endpoint

```typescript
test("health endpoint returns ok", async ({ request }) => {
  const response = await request.get(`${BASE_URL}/api/health`);

  expect(response.status()).toBe(200);
  expect(response.ok()).toBe(true);

  const body = await response.json();
  expect(body.status).toBe("healthy");
});
```

### CRUD Operations

```typescript
// Adapt endpoint paths and payloads to your domain
test.describe("CRUD: Resources", () => {
  let createdId: string;

  test("CREATE: POST /api/resources", async ({ request }) => {
    const response = await request.post(`${BASE_URL}/api/resources`, {
      data: { name: "Test Resource", /* add required fields */ }
    });

    expect(response.status()).toBe(201);
    const { data } = await response.json();
    createdId = data.id;
    expect(createdId).toBeDefined();
  });

  test("READ: GET /api/resources/:id", async ({ request }) => {
    const response = await request.get(`${BASE_URL}/api/resources/${createdId}`);

    expect(response.status()).toBe(200);
    const { data } = await response.json();
    expect(data.name).toBe("Test Resource");
  });

  test("UPDATE: PUT /api/resources/:id", async ({ request }) => {
    const response = await request.put(`${BASE_URL}/api/resources/${createdId}`, {
      data: { name: "Updated Resource" }
    });

    expect(response.status()).toBe(200);
    const { data } = await response.json();
    expect(data.name).toBe("Updated Resource");
  });

  test("DELETE: DELETE /api/resources/:id", async ({ request }) => {
    const response = await request.delete(`${BASE_URL}/api/resources/${createdId}`);

    expect(response.status()).toBe(204);
  });
});
```

### Testing with Query Parameters

```typescript
test("filters by status", async ({ request }) => {
  const response = await request.get(`${BASE_URL}/api/resources?status=active`);

  expect(response.status()).toBe(200);
  const { data } = await response.json();

  for (const item of data) {
    expect(item.status).toBe("active");
  }
});
```

## Testing ActionResponse Pattern

If your project uses the ActionResponse pattern (check `CLAUDE.md`), use these assertions:

```typescript
// Test successful ActionResponse
test("returns ActionResponse success format", async ({ request }) => {
  const response = await request.post(`${BASE_URL}${API_ENDPOINT}`, {
    data: validPayload
  });

  expect(response.status()).toBe(200);
  const body = await response.json();

  // ActionResponse success structure
  expect(body).toMatchObject({
    success: true,
    data: expect.any(Object),
  });
  expect(body.message).toBeDefined(); // optional
});

// Test failed ActionResponse with validation errors
test("returns fieldErrors on validation failure", async ({ request }) => {
  const response = await request.post(`${BASE_URL}${API_ENDPOINT}`, {
    data: {} // missing required fields
  });

  expect(response.status()).toBe(400);
  const body = await response.json();

  // ActionResponse error structure
  expect(body).toMatchObject({
    success: false,
    error: expect.any(String),
  });

  // Check for field-level errors if applicable
  if (body.fieldErrors) {
    expect(body.fieldErrors).toEqual(
      expect.objectContaining({
        name: expect.arrayContaining([expect.any(String)])
      })
    );
  }
});

// Test database error mapping
test("maps DbError to appropriate HTTP status", async ({ request }) => {
  const response = await request.get(
    `${BASE_URL}${API_ENDPOINT}/non-existent-id`
  );

  // DbError.notFound → 404
  expect(response.status()).toBe(404);
  const body = await response.json();
  expect(body.success).toBe(false);
  expect(body.error).toContain("not found");
});
```

## Best Practices

1. **Isolate tests**: Each test should be independent
2. **Clean up**: Delete test data after tests
3. **Use fixtures**: Share test data setup across tests
4. **Test edge cases**: Empty arrays, null values, special characters
5. **Verify response shape**: Not just status codes
6. **Test error messages**: Ensure they're user-friendly
7. **Document assumptions**: Note any test dependencies

## Questions to Ask

When creating API tests:

- What HTTP methods does this endpoint support?
- What authentication is required?
- What does the request body schema look like?
- What are the possible error responses?
- Are there any rate limits or quotas?
- What headers are expected/returned?
- Are there any side effects to test?
