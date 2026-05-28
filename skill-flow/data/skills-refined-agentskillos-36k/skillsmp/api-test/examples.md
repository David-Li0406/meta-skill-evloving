# API Test - Examples

## Example 1: Testing POST Endpoint

**Scenario:** Test the POST /api/budgets endpoint that creates a new budget.

**Route Handler:**
```typescript
// app/api/budgets/route.ts
import { NextResponse } from "next/server";
import { auth } from "@clerk/nextjs/server";
import { createBudgetSchema } from "~/features/budget/schemas/budget";

export async function POST(request: Request) {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const parsed = createBudgetSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json(
      { error: "Validation failed", details: parsed.error.flatten() },
      { status: 400 }
    );
  }

  const [error, budget] = await createBudget(userId, parsed.data);
  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ data: budget }, { status: 201 });
}
```

**Test File:**
```typescript
// tests/e2e/api/budgets.spec.ts
import { test, expect } from "@playwright/test";

test.describe("POST /api/budgets", () => {
  test("creates budget with valid data", async ({ request }) => {
    const response = await request.post("http://localhost:3000/api/budgets", {
      headers: {
        "Content-Type": "application/json",
        // Add auth cookie/header based on your auth setup
        "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
      },
      data: {
        name: "Monthly Budget",
        amount: 5000,
        currency: "PLN",
        period: "monthly"
      }
    });

    expect(response.status()).toBe(201);

    const body = await response.json();
    expect(body).toHaveProperty("data");
    expect(body.data).toMatchObject({
      name: "Monthly Budget",
      amount: 5000,
      currency: "PLN",
      period: "monthly"
    });
    expect(body.data).toHaveProperty("id");
    expect(body.data).toHaveProperty("createdAt");
  });

  test("returns 401 for unauthenticated request", async ({ request }) => {
    const response = await request.post("http://localhost:3000/api/budgets", {
      headers: {
        "Content-Type": "application/json"
        // No auth cookie
      },
      data: {
        name: "Monthly Budget",
        amount: 5000
      }
    });

    expect(response.status()).toBe(401);

    const body = await response.json();
    expect(body).toEqual({ error: "Unauthorized" });
  });

  test("returns 400 for invalid data", async ({ request }) => {
    const response = await request.post("http://localhost:3000/api/budgets", {
      headers: {
        "Content-Type": "application/json",
        "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
      },
      data: {
        name: "", // Invalid: empty name
        amount: -100 // Invalid: negative amount
      }
    });

    expect(response.status()).toBe(400);

    const body = await response.json();
    expect(body).toHaveProperty("error", "Validation failed");
    expect(body).toHaveProperty("details");
    expect(body.details).toHaveProperty("fieldErrors");
  });
});
```

---

## Example 2: Testing GET Endpoint with Query Parameters

**Scenario:** Test GET /api/expenses endpoint with filtering.

**Route Handler:**
```typescript
// app/api/expenses/route.ts
export async function GET(request: Request) {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { searchParams } = new URL(request.url);
  const categoryId = searchParams.get("categoryId");
  const startDate = searchParams.get("startDate");
  const endDate = searchParams.get("endDate");

  const [error, expenses] = await getExpenses(userId, {
    categoryId,
    startDate: startDate ? new Date(startDate) : undefined,
    endDate: endDate ? new Date(endDate) : undefined
  });

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ data: expenses });
}
```

**Test File:**
```typescript
// tests/e2e/api/expenses.spec.ts
import { test, expect } from "@playwright/test";

test.describe("GET /api/expenses", () => {
  test("returns all expenses without filters", async ({ request }) => {
    const response = await request.get("http://localhost:3000/api/expenses", {
      headers: {
        "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
      }
    });

    expect(response.status()).toBe(200);

    const body = await response.json();
    expect(body).toHaveProperty("data");
    expect(Array.isArray(body.data)).toBe(true);
  });

  test("filters expenses by categoryId", async ({ request }) => {
    const categoryId = "food-category-id";

    const response = await request.get(
      `http://localhost:3000/api/expenses?categoryId=${categoryId}`,
      {
        headers: {
          "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
        }
      }
    );

    expect(response.status()).toBe(200);

    const body = await response.json();
    expect(body.data.every((expense: any) => expense.categoryId === categoryId)).toBe(true);
  });

  test("filters expenses by date range", async ({ request }) => {
    const startDate = "2026-01-01";
    const endDate = "2026-01-31";

    const response = await request.get(
      `http://localhost:3000/api/expenses?startDate=${startDate}&endDate=${endDate}`,
      {
        headers: {
          "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
        }
      }
    );

    expect(response.status()).toBe(200);

    const body = await response.json();
    body.data.forEach((expense: any) => {
      const expenseDate = new Date(expense.date);
      expect(expenseDate >= new Date(startDate)).toBe(true);
      expect(expenseDate <= new Date(endDate)).toBe(true);
    });
  });
});
```

---

## Example 3: Testing PATCH/PUT Endpoint

**Scenario:** Test PATCH /api/budgets/[id] endpoint.

**Route Handler:**
```typescript
// app/api/budgets/[id]/route.ts
export async function PATCH(
  request: Request,
  { params }: { params: { id: string } }
) {
  const { userId } = await auth();
  if (!userId) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const body = await request.json();
  const parsed = updateBudgetSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json(
      { error: "Validation failed", details: parsed.error.flatten() },
      { status: 400 }
    );
  }

  const [error, budget] = await updateBudget(params.id, userId, parsed.data);

  if (error) {
    if (error.isNotFound) {
      return NextResponse.json({ error: "Budget not found" }, { status: 404 });
    }
    return NextResponse.json({ error: error.message }, { status: 500 });
  }

  return NextResponse.json({ data: budget });
}
```

**Test File:**
```typescript
// tests/e2e/api/budgets-update.spec.ts
import { test, expect } from "@playwright/test";

test.describe("PATCH /api/budgets/[id]", () => {
  let budgetId: string;

  test.beforeEach(async ({ request }) => {
    // Create budget for testing
    const response = await request.post("http://localhost:3000/api/budgets", {
      headers: {
        "Content-Type": "application/json",
        "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
      },
      data: {
        name: "Test Budget",
        amount: 1000,
        currency: "PLN"
      }
    });

    const body = await response.json();
    budgetId = body.data.id;
  });

  test("updates budget successfully", async ({ request }) => {
    const response = await request.patch(
      `http://localhost:3000/api/budgets/${budgetId}`,
      {
        headers: {
          "Content-Type": "application/json",
          "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
        },
        data: {
          name: "Updated Budget",
          amount: 2000
        }
      }
    );

    expect(response.status()).toBe(200);

    const body = await response.json();
    expect(body.data).toMatchObject({
      id: budgetId,
      name: "Updated Budget",
      amount: 2000
    });
  });

  test("returns 404 for non-existent budget", async ({ request }) => {
    const response = await request.patch(
      "http://localhost:3000/api/budgets/non-existent-id",
      {
        headers: {
          "Content-Type": "application/json",
          "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
        },
        data: {
          name: "Updated Budget"
        }
      }
    );

    expect(response.status()).toBe(404);

    const body = await response.json();
    expect(body).toEqual({ error: "Budget not found" });
  });
});
```

---

## Example 4: Testing DELETE Endpoint

**Scenario:** Test DELETE /api/expenses/[id] endpoint.

**Test File:**
```typescript
// tests/e2e/api/expenses-delete.spec.ts
import { test, expect } from "@playwright/test";

test.describe("DELETE /api/expenses/[id]", () => {
  test("deletes expense successfully", async ({ request }) => {
    // First, create an expense
    const createResponse = await request.post("http://localhost:3000/api/expenses", {
      headers: {
        "Content-Type": "application/json",
        "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
      },
      data: {
        amount: 50,
        categoryId: "food",
        description: "Lunch"
      }
    });

    const { data: expense } = await createResponse.json();

    // Then delete it
    const deleteResponse = await request.delete(
      `http://localhost:3000/api/expenses/${expense.id}`,
      {
        headers: {
          "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
        }
      }
    );

    expect(deleteResponse.status()).toBe(204);

    // Verify it's gone
    const getResponse = await request.get(
      `http://localhost:3000/api/expenses/${expense.id}`,
      {
        headers: {
          "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
        }
      }
    );

    expect(getResponse.status()).toBe(404);
  });

  test("returns 404 when deleting non-existent expense", async ({ request }) => {
    const response = await request.delete(
      "http://localhost:3000/api/expenses/non-existent-id",
      {
        headers: {
          "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
        }
      }
    );

    expect(response.status()).toBe(404);
  });
});
```

---

## Example 5: Testing with Response Headers

**Scenario:** Verify CORS headers and caching headers.

**Test File:**
```typescript
// tests/e2e/api/headers.spec.ts
import { test, expect } from "@playwright/test";

test.describe("API Headers", () => {
  test("includes correct CORS headers", async ({ request }) => {
    const response = await request.get("http://localhost:3000/api/public-data");

    expect(response.headers()["access-control-allow-origin"]).toBeDefined();
    expect(response.headers()["access-control-allow-methods"]).toContain("GET");
  });

  test("includes cache headers for static endpoint", async ({ request }) => {
    const response = await request.get("http://localhost:3000/api/config");

    expect(response.headers()["cache-control"]).toBeDefined();
    expect(response.headers()["cache-control"]).toContain("max-age");
  });

  test("includes content-type header", async ({ request }) => {
    const response = await request.get("http://localhost:3000/api/budgets", {
      headers: {
        "Cookie": `__session=${process.env.TEST_SESSION_TOKEN}`
      }
    });

    expect(response.headers()["content-type"]).toContain("application/json");
  });
});
```

---

## Test Utilities

### Auth Helper
```typescript
// tests/utils/auth.ts
export async function getAuthHeaders() {
  // For Clerk
  const token = process.env.TEST_SESSION_TOKEN;
  return {
    "Cookie": `__session=${token}`
  };
}

// Usage
const headers = await getAuthHeaders();
const response = await request.get("http://localhost:3000/api/budgets", { headers });
```

### Base URL Helper
```typescript
// tests/utils/api.ts
export const API_BASE_URL = process.env.API_BASE_URL || "http://localhost:3000";

export function apiUrl(path: string) {
  return `${API_BASE_URL}${path}`;
}

// Usage
const response = await request.get(apiUrl("/api/budgets"));
```

### Response Assertion Helpers
```typescript
// tests/utils/assertions.ts
export async function expectSuccessResponse(response: any, status = 200) {
  expect(response.status()).toBe(status);
  const body = await response.json();
  expect(body).toHaveProperty("data");
  return body.data;
}

export async function expectErrorResponse(response: any, status: number, errorMessage?: string) {
  expect(response.status()).toBe(status);
  const body = await response.json();
  expect(body).toHaveProperty("error");
  if (errorMessage) {
    expect(body.error).toBe(errorMessage);
  }
  return body;
}

// Usage
const data = await expectSuccessResponse(response, 201);
await expectErrorResponse(response, 400, "Validation failed");
```

---

## Running Tests

```bash
# Run all API tests
npm run test:e2e -- tests/e2e/api

# Run specific test file
npm run test:e2e -- tests/e2e/api/budgets.spec.ts

# Run in UI mode
npm run test:e2e:ui -- tests/e2e/api

# Run with debugging
PWDEBUG=1 npm run test:e2e -- tests/e2e/api/budgets.spec.ts
```

## Best Practices

1. **Use descriptive test names** - Clearly state what is being tested
2. **Test happy path and error cases** - Don't just test success
3. **Clean up after tests** - Delete created resources in afterEach
4. **Use beforeEach for setup** - Create necessary test data
5. **Assert on response structure** - Verify shape, not just success
6. **Test authentication** - Verify auth is enforced
7. **Test validation** - Ensure bad input is rejected
8. **Use env variables** - Don't hardcode URLs or tokens
