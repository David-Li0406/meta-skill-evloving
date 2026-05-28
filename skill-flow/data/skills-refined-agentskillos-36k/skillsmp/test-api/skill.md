---
name: test-api
description: Test API endpoints manually or create test scripts
allowed-tools: [Bash, Write, Read]
---

## Purpose
Test API routes to verify authentication, authorization, validation, and data operations work correctly.

## Testing Methods

### 1. Using curl
```bash
# GET request
curl http://localhost:3000/api/domains

# POST request with JSON body
curl -X POST http://localhost:3000/api/domains \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Domain","description":"Test"}'

# With authentication cookie
curl http://localhost:3000/api/domains \
  -H "Cookie: next-auth.session-token=YOUR_TOKEN"

# PATCH request
curl -X PATCH http://localhost:3000/api/domains/1 \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Name"}'

# DELETE request
curl -X DELETE "http://localhost:3000/api/domains?id=1"
```

### 2. Using fetch in Node.js
```typescript
// tools/test-api.ts
async function testAPI() {
  // Test GET
  const response = await fetch('http://localhost:3000/api/domains');
  const data = await response.json();
  console.log('Domains:', data);

  // Test POST
  const createResponse = await fetch('http://localhost:3000/api/domains', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: 'Test Domain',
      description: 'Test Description',
    }),
  });

  const created = await createResponse.json();
  console.log('Created:', created);

  // Check response status
  if (!createResponse.ok) {
    console.error('Error:', created.error);
  }
}

testAPI();
```

### 3. Test Script Template
```typescript
// tools/test-<feature>-api.ts
import { getServerSession } from 'next-auth';

interface TestResult {
  name: string;
  passed: boolean;
  error?: string;
}

async function runTests(): Promise<TestResult[]> {
  const results: TestResult[] = [];
  const baseUrl = 'http://localhost:3000/api';

  // Test 1: GET all items
  try {
    const res = await fetch(`${baseUrl}/items`);
    const data = await res.json();

    results.push({
      name: 'GET /api/items',
      passed: res.ok && Array.isArray(data),
      error: res.ok ? undefined : data.error,
    });
  } catch (error) {
    results.push({
      name: 'GET /api/items',
      passed: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    });
  }

  // Test 2: POST create item
  try {
    const res = await fetch(`${baseUrl}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Test Item' }),
    });
    const data = await res.json();

    results.push({
      name: 'POST /api/items',
      passed: res.ok && data.id !== undefined,
      error: res.ok ? undefined : data.error,
    });
  } catch (error) {
    results.push({
      name: 'POST /api/items',
      passed: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    });
  }

  // Test 3: Validation error
  try {
    const res = await fetch(`${baseUrl}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}), // Missing required fields
    });
    const data = await res.json();

    results.push({
      name: 'POST /api/items validation',
      passed: res.status === 400, // Should fail validation
      error: res.status === 400 ? undefined : 'Should return 400',
    });
  } catch (error) {
    results.push({
      name: 'POST /api/items validation',
      passed: false,
      error: error instanceof Error ? error.message : 'Unknown error',
    });
  }

  return results;
}

async function main() {
  console.log('=== API Tests ===\n');
  console.log('Starting tests...\n');

  const results = await runTests();

  // Print results
  results.forEach((result) => {
    const icon = result.passed ? '✓' : '✗';
    const status = result.passed ? 'PASS' : 'FAIL';
    console.log(`${icon} ${result.name}: ${status}`);
    if (result.error) {
      console.log(`  Error: ${result.error}`);
    }
  });

  // Summary
  const passed = results.filter((r) => r.passed).length;
  const failed = results.filter((r) => !r.passed).length;
  console.log(`\n${passed} passed, ${failed} failed`);

  // Exit with error if any failed
  process.exit(failed > 0 ? 1 : 0);
}

main();
```

### 4. Testing with Authentication

**Get session token:**
```typescript
// tools/get-session-token.ts
import Database from 'better-sqlite3';
import path from 'path';

const db = new Database(path.join(process.cwd(), 'data', 'learning-cards.db'));

const session = db.prepare(`
  SELECT token FROM sessions
  WHERE user_id = ? AND expires > datetime('now')
  LIMIT 1
`).get(1); // User ID

console.log('Session token:', session?.token);
db.close();
```

**Use token in requests:**
```typescript
const token = 'your-session-token';

const response = await fetch('http://localhost:3000/api/protected', {
  headers: {
    Cookie: `next-auth.session-token=${token}`,
  },
});
```

### 5. Testing Authorization

```typescript
// Test different user roles
const tests = [
  { role: 'user', endpoint: '/api/admin/stats', shouldFail: true },
  { role: 'admin', endpoint: '/api/admin/stats', shouldFail: false },
  { role: 'teacher', endpoint: '/api/flashcards', shouldFail: false },
];

for (const test of tests) {
  // Get session for user with role
  const token = getTokenForRole(test.role);

  const res = await fetch(`http://localhost:3000${test.endpoint}`, {
    headers: { Cookie: `next-auth.session-token=${token}` },
  });

  const passed = test.shouldFail ? res.status === 403 : res.ok;
  console.log(`${test.role} -> ${test.endpoint}: ${passed ? 'PASS' : 'FAIL'}`);
}
```

### 6. Load Testing

```typescript
// tools/load-test.ts
async function loadTest(url: string, requests: number) {
  console.log(`Running ${requests} requests to ${url}...\n`);

  const startTime = Date.now();
  const promises: Promise<Response>[] = [];

  for (let i = 0; i < requests; i++) {
    promises.push(fetch(url));
  }

  const results = await Promise.allSettled(promises);
  const endTime = Date.now();

  const successful = results.filter((r) => r.status === 'fulfilled').length;
  const failed = results.filter((r) => r.status === 'rejected').length;
  const duration = endTime - startTime;
  const rps = (requests / duration) * 1000;

  console.log(`Completed in ${duration}ms`);
  console.log(`Successful: ${successful}`);
  console.log(`Failed: ${failed}`);
  console.log(`Requests/sec: ${rps.toFixed(2)}`);
}

loadTest('http://localhost:3000/api/domains', 100);
```

## Common Test Scenarios

### Test CRUD Operations
```bash
# Create
ID=$(curl -s -X POST http://localhost:3000/api/domains \
  -H "Content-Type: application/json" \
  -d '{"name":"Test"}' | jq -r '.id')

echo "Created ID: $ID"

# Read
curl -s http://localhost:3000/api/domains/$ID

# Update
curl -s -X PATCH http://localhost:3000/api/domains/$ID \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated"}'

# Delete
curl -s -X DELETE "http://localhost:3000/api/domains?id=$ID"
```

### Test Validation
```bash
# Should fail - missing required field
curl -X POST http://localhost:3000/api/domains \
  -H "Content-Type: application/json" \
  -d '{}'

# Should fail - invalid email
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"email":"invalid","password":"test123"}'
```

### Test Error Handling
```bash
# 404 - Not found
curl -i http://localhost:3000/api/domains/999999

# 401 - Unauthorized
curl -i http://localhost:3000/api/admin/stats

# 403 - Forbidden (need admin role)
curl -i http://localhost:3000/api/admin/users \
  -H "Cookie: next-auth.session-token=user-token"
```

## Best Practices
- ✅ Test all HTTP methods (GET, POST, PATCH, DELETE)
- ✅ Test with and without authentication
- ✅ Test different user roles
- ✅ Test validation errors
- ✅ Test edge cases (empty data, large payloads)
- ✅ Verify response status codes
- ✅ Check response data structure
- ✅ Test concurrent requests
- ⚠️ Don't test against production database
- ⚠️ Clean up test data after tests
- ⚠️ Use proper authentication in tests
