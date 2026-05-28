---
name: testing-practices
description: Best practices for testing JavaScript/TypeScript applications including Remix routes, SST functions, and React components
---

# Testing Practices

This skill covers comprehensive testing strategies for modern JavaScript/TypeScript applications with Remix and SST.

## Core Philosophy

Good tests are:
- **Fast**: Run quickly to encourage frequent execution
- **Isolated**: Each test is independent
- **Readable**: Clear what's being tested and why
- **Reliable**: Same input always produces same output
- **Maintainable**: Easy to update when code changes

## Testing Pyramid

```
     /\
    /  \  E2E Tests (few)
   /____\
  /      \
 / Integr \  Integration Tests (some)
/__________\
/            \
/   Unit      \  Unit Tests (many)
/______________\
```

**Unit Tests (70%):**
- Test individual functions
- Fast, isolated
- Mock dependencies

**Integration Tests (20%):**
- Test multiple components together
- Test database queries
- Test API routes

**E2E Tests (10%):**
- Test full user workflows
- Slow but high confidence
- Critical paths only

## Test Frameworks

### Setup with Vitest

```bash
npm install -D vitest @vitest/ui
```

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    setupFiles: ["./test/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "html"],
      exclude: ["**/node_modules/**", "**/test/**"]
    }
  }
});
```

### Setup for React/Remix

```bash
npm install -D @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

```typescript
// test/setup.ts
import "@testing-library/jest-dom";
import { cleanup } from "@testing-library/react";
import { afterEach } from "vitest";

afterEach(() => {
  cleanup();
});
```

## Unit Testing Patterns

### Pattern 1: Testing Pure Functions

```typescript
// src/lib/utils.ts
export function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// test/lib/utils.test.ts
import { describe, test, expect } from "vitest";
import { calculateTotal } from "../../src/lib/utils";

describe("calculateTotal", () => {
  test("returns 0 for empty cart", () => {
    expect(calculateTotal([])).toBe(0);
  });

  test("calculates total for single item", () => {
    const items = [{ price: 10, quantity: 2 }];
    expect(calculateTotal(items)).toBe(20);
  });

  test("calculates total for multiple items", () => {
    const items = [
      { price: 10, quantity: 2 },
      { price: 5, quantity: 3 }
    ];
    expect(calculateTotal(items)).toBe(35);
  });

  test("handles decimal prices", () => {
    const items = [{ price: 9.99, quantity: 2 }];
    expect(calculateTotal(items)).toBeCloseTo(19.98);
  });
});
```

### Pattern 2: Testing with Mocks

```typescript
// src/lib/email.ts
import { SESClient, SendEmailCommand } from "@aws-sdk/client-ses";

export async function sendWelcomeEmail(email: string, name: string) {
  const ses = new SESClient({});
  
  await ses.send(new SendEmailCommand({
    Source: "noreply@example.com",
    Destination: { ToAddresses: [email] },
    Message: {
      Subject: { Data: "Welcome!" },
      Body: { Text: { Data: `Hello ${name}!` } }
    }
  }));
}

// test/lib/email.test.ts
import { describe, test, expect, vi } from "vitest";
import { sendWelcomeEmail } from "../../src/lib/email";
import { SESClient } from "@aws-sdk/client-ses";

vi.mock("@aws-sdk/client-ses", () => ({
  SESClient: vi.fn(),
  SendEmailCommand: vi.fn()
}));

describe("sendWelcomeEmail", () => {
  test("sends email with correct parameters", async () => {
    const mockSend = vi.fn().mockResolvedValue({});
    (SESClient as any).mockImplementation(() => ({
      send: mockSend
    }));

    await sendWelcomeEmail("user@example.com", "John");

    expect(mockSend).toHaveBeenCalledWith(
      expect.objectContaining({
        input: expect.objectContaining({
          Destination: { ToAddresses: ["user@example.com"] }
        })
      })
    );
  });
});
```

### Pattern 3: Testing Async Functions

```typescript
// src/lib/users.ts
export async function getUser(id: string): Promise<User | null> {
  const result = await db.query({
    TableName: Resource.Database.name,
    KeyConditionExpression: "pk = :pk",
    ExpressionAttributeValues: { ":pk": `USER#${id}` }
  });
  
  return result.Items?.[0] as User | null;
}

// test/lib/users.test.ts
import { describe, test, expect, beforeEach, vi } from "vitest";
import { getUser } from "../../src/lib/users";

// Mock the database
vi.mock("../../src/lib/db", () => ({
  db: {
    query: vi.fn()
  }
}));

import { db } from "../../src/lib/db";

describe("getUser", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  test("returns user when found", async () => {
    const mockUser = { pk: "USER#123", name: "John" };
    (db.query as any).mockResolvedValue({
      Items: [mockUser]
    });

    const user = await getUser("123");
    expect(user).toEqual(mockUser);
  });

  test("returns null when not found", async () => {
    (db.query as any).mockResolvedValue({ Items: [] });

    const user = await getUser("123");
    expect(user).toBeNull();
  });

  test("throws on database error", async () => {
    (db.query as any).mockRejectedValue(new Error("DB Error"));

    await expect(getUser("123")).rejects.toThrow("DB Error");
  });
});
```

## Testing Remix Routes

### Pattern 1: Testing Loaders

```typescript
// app/routes/posts.$id.tsx
export async function loader({ params }: LoaderFunctionArgs) {
  const post = await getPost(params.id);
  if (!post) {
    throw new Response("Not Found", { status: 404 });
  }
  return json({ post });
}

// test/routes/posts.$id.test.ts
import { describe, test, expect, vi } from "vitest";
import { loader } from "../../app/routes/posts.$id";

vi.mock("../../src/lib/posts", () => ({
  getPost: vi.fn()
}));

import { getPost } from "../../src/lib/posts";

describe("posts.$id loader", () => {
  test("returns post data when found", async () => {
    const mockPost = { id: "123", title: "Test Post" };
    (getPost as any).mockResolvedValue(mockPost);

    const response = await loader({
      params: { id: "123" },
      request: new Request("http://localhost/posts/123")
    } as any);

    const data = await response.json();
    expect(data.post).toEqual(mockPost);
  });

  test("throws 404 when post not found", async () => {
    (getPost as any).mockResolvedValue(null);

    await expect(
      loader({
        params: { id: "123" },
        request: new Request("http://localhost/posts/123")
      } as any)
    ).rejects.toThrow("Not Found");
  });
});
```

### Pattern 2: Testing Actions

```typescript
// app/routes/posts.new.tsx
export async function action({ request }: ActionFunctionArgs) {
  const formData = await request.formData();
  const title = formData.get("title");
  const content = formData.get("content");

  if (!title || !content) {
    return json({ errors: { title: "Required", content: "Required" } });
  }

  const post = await createPost({ title, content });
  return redirect(`/posts/${post.id}`);
}

// test/routes/posts.new.test.ts
import { describe, test, expect, vi } from "vitest";
import { action } from "../../app/routes/posts.new";

vi.mock("../../src/lib/posts", () => ({
  createPost: vi.fn()
}));

import { createPost } from "../../src/lib/posts";

describe("posts.new action", () => {
  test("creates post and redirects on success", async () => {
    const mockPost = { id: "123", title: "Test", content: "Content" };
    (createPost as any).mockResolvedValue(mockPost);

    const formData = new FormData();
    formData.append("title", "Test");
    formData.append("content", "Content");

    const response = await action({
      request: new Request("http://localhost/posts/new", {
        method: "POST",
        body: formData
      })
    } as any);

    expect(response.status).toBe(302);
    expect(response.headers.get("Location")).toBe("/posts/123");
  });

  test("returns errors for invalid data", async () => {
    const formData = new FormData();
    formData.append("title", "");
    formData.append("content", "");

    const response = await action({
      request: new Request("http://localhost/posts/new", {
        method: "POST",
        body: formData
      })
    } as any);

    const data = await response.json();
    expect(data.errors).toEqual({
      title: "Required",
      content: "Required"
    });
  });
});
```

## Testing React Components

### Pattern 1: Simple Component Tests

```typescript
// app/components/PostCard.tsx
export function PostCard({ post }: { post: Post }) {
  return (
    <article>
      <h2>{post.title}</h2>
      <p>{post.content}</p>
      <time>{post.createdAt}</time>
    </article>
  );
}

// test/components/PostCard.test.tsx
import { describe, test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { PostCard } from "../../app/components/PostCard";

describe("PostCard", () => {
  test("renders post information", () => {
    const post = {
      id: "123",
      title: "Test Post",
      content: "This is content",
      createdAt: "2025-01-02"
    };

    render(<PostCard post={post} />);

    expect(screen.getByText("Test Post")).toBeInTheDocument();
    expect(screen.getByText("This is content")).toBeInTheDocument();
    expect(screen.getByText("2025-01-02")).toBeInTheDocument();
  });
});
```

### Pattern 2: Interactive Components

```typescript
// app/components/Counter.tsx
import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      <button onClick={() => setCount(0)}>Reset</button>
    </div>
  );
}

// test/components/Counter.test.tsx
import { describe, test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Counter } from "../../app/components/Counter";

describe("Counter", () => {
  test("increments count", async () => {
    const user = userEvent.setup();
    render(<Counter />);

    expect(screen.getByText("Count: 0")).toBeInTheDocument();

    await user.click(screen.getByText("Increment"));
    expect(screen.getByText("Count: 1")).toBeInTheDocument();

    await user.click(screen.getByText("Increment"));
    expect(screen.getByText("Count: 2")).toBeInTheDocument();
  });

  test("resets count", async () => {
    const user = userEvent.setup();
    render(<Counter />);

    await user.click(screen.getByText("Increment"));
    await user.click(screen.getByText("Increment"));
    expect(screen.getByText("Count: 2")).toBeInTheDocument();

    await user.click(screen.getByText("Reset"));
    expect(screen.getByText("Count: 0")).toBeInTheDocument();
  });
});
```

## Testing SST Functions

### Pattern 1: Testing Lambda Handlers

```typescript
// src/api/posts.ts
import { APIGatewayProxyEventV2, APIGatewayProxyResultV2 } from "aws-lambda";
import { getPosts } from "../lib/posts";

export async function handler(
  event: APIGatewayProxyEventV2
): Promise<APIGatewayProxyResultV2> {
  const posts = await getPosts();
  
  return {
    statusCode: 200,
    body: JSON.stringify({ posts })
  };
}

// test/api/posts.test.ts
import { describe, test, expect, vi } from "vitest";
import { handler } from "../../src/api/posts";

vi.mock("../../src/lib/posts", () => ({
  getPosts: vi.fn()
}));

import { getPosts } from "../../src/lib/posts";

describe("posts handler", () => {
  test("returns posts", async () => {
    const mockPosts = [{ id: "1", title: "Post 1" }];
    (getPosts as any).mockResolvedValue(mockPosts);

    const result = await handler({} as any);

    expect(result.statusCode).toBe(200);
    expect(JSON.parse(result.body!)).toEqual({ posts: mockPosts });
  });

  test("handles errors", async () => {
    (getPosts as any).mockRejectedValue(new Error("DB Error"));

    const result = await handler({} as any);

    expect(result.statusCode).toBe(500);
  });
});
```

## Integration Testing

### Pattern 1: Testing with Real Database

```typescript
// test/integration/posts.test.ts
import { describe, test, expect, beforeAll, afterAll } from "vitest";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient } from "@aws-sdk/lib-dynamodb";
import { createPost, getPost } from "../../src/lib/posts";

// Use local DynamoDB for tests
const client = DynamoDBDocumentClient.from(
  new DynamoDBClient({ endpoint: "http://localhost:8000" })
);

describe("Post operations", () => {
  beforeAll(async () => {
    // Create test table
    await createTestTable();
  });

  afterAll(async () => {
    // Clean up test table
    await deleteTestTable();
  });

  test("creates and retrieves post", async () => {
    const postData = {
      title: "Test Post",
      content: "This is a test",
      authorId: "user123"
    };

    const created = await createPost(postData);
    expect(created.id).toBeDefined();
    expect(created.title).toBe(postData.title);

    const retrieved = await getPost(created.id);
    expect(retrieved).toEqual(created);
  });
});
```

## E2E Testing with Playwright

```typescript
// e2e/auth.spec.ts
import { test, expect } from "@playwright/test";

test("user can sign up and log in", async ({ page }) => {
  // Sign up
  await page.goto("/signup");
  await page.fill('input[name="email"]', "test@example.com");
  await page.fill('input[name="password"]', "password123");
  await page.fill('input[name="name"]', "Test User");
  await page.click('button[type="submit"]');

  // Should redirect to dashboard
  await expect(page).toHaveURL("/dashboard");
  await expect(page.locator("text=Welcome, Test User")).toBeVisible();

  // Log out
  await page.click('button:has-text("Log out")');
  await expect(page).toHaveURL("/");

  // Log in
  await page.goto("/login");
  await page.fill('input[name="email"]', "test@example.com");
  await page.fill('input[name="password"]', "password123");
  await page.click('button[type="submit"]');

  // Should be logged in
  await expect(page).toHaveURL("/dashboard");
});
```

## Test Best Practices

### 1. Use Descriptive Test Names

✅ **Do:**
```typescript
test("returns 404 when post not found", () => {});
test("creates user and sends welcome email", () => {});
```

❌ **Don't:**
```typescript
test("test1", () => {});
test("works", () => {});
```

### 2. Follow AAA Pattern

```typescript
test("updates post title", async () => {
  // Arrange
  const post = await createPost({ title: "Old Title" });

  // Act
  await updatePost(post.id, { title: "New Title" });

  // Assert
  const updated = await getPost(post.id);
  expect(updated.title).toBe("New Title");
});
```

### 3. Test One Thing Per Test

✅ **Do:**
```typescript
test("validates email format", () => {});
test("validates email uniqueness", () => {});
```

❌ **Don't:**
```typescript
test("validates email", () => {
  // Tests 5 different things
});
```

### 4. Mock External Dependencies

```typescript
// Mock AWS services
vi.mock("@aws-sdk/client-s3");

// Mock environment variables
vi.stubEnv("API_KEY", "test-key");

// Mock time
vi.useFakeTimers();
vi.setSystemTime(new Date("2025-01-02"));
```

### 5. Clean Up After Tests

```typescript
import { afterEach, beforeEach } from "vitest";

beforeEach(() => {
  // Set up test data
});

afterEach(() => {
  // Clean up
  vi.clearAllMocks();
  vi.restoreAllMocks();
});
```

## Coverage Goals

Aim for:
- **Unit tests**: 80%+ coverage
- **Integration tests**: Key workflows
- **E2E tests**: Critical user paths

```bash
# Run tests with coverage
npm test -- --coverage

# Set minimum coverage
vitest.config.ts:
coverage: {
  lines: 80,
  functions: 80,
  branches: 75,
  statements: 80
}
```

## CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm install
      - run: npm test
      - run: npm run test:e2e
```

## Further Reading

- Vitest: https://vitest.dev/
- Testing Library: https://testing-library.com/
- Playwright: https://playwright.dev/
- Test-Driven Development (TDD) principles
