---
name: http-mocking-and-unit-testing
description: Use this skill for unit testing patterns with HTTP mocking using nock, ensuring no credentials are required.
---

# HTTP Mocking and Unit Testing Patterns

## Critical Rules

### 1. HTTP Mocking - ONLY Use Nock

**🚨 CRITICAL: Use ONLY `nock` for HTTP mocking in unit tests**

```typescript
// ✅ CORRECT - Using nock
import * as nock from 'nock';

describe('UserProducer', () => {
  it('should get user', async () => {
    nock('https://api.example.com')
      .get('/users/123')
      .reply(200, { id: '123', name: 'John' });

    const user = await producer.getUser('123');
    expect(user.id).to.be.instanceof(UUID);
  });
});

// ❌ FORBIDDEN - Other mocking libraries
import { jest } from '@jest/globals';  // NO
import sinon from 'sinon';  // NO
import fetchMock from 'fetch-mock';  // NO
```

### 2. NO Environment Variables in Unit Tests

**🚨 CRITICAL: Unit tests NEVER depend on environment variables**

```typescript
// ✅ CORRECT: Unit test Common.ts - NO env vars
import * as nock from 'nock';
import { Email } from '@zerobias-org/types-core-js';
import { newService } from '../../src';

export async function getConnectedInstance() {
  nock('https://api.example.com')
    .post('/auth/login')
    .reply(200, {
      accessToken: 'test-token-123',
      expiresAt: '2025-10-02T00:00:00Z',
    });

  const connector = newService();
  await connector.connect({
    email: new Email('test@example.com'),
    password: 'testpass',
  });

  return connector;
}
```

### 3. Test Coverage Requirements

**🚨 CRITICAL: ALL new operations MUST have unit tests**

```typescript
// ✅ CORRECT: Unit test for each operation
describe('UserProducer', () => {
  describe('getUser', () => {
    it('should retrieve user by ID', async () => {
      nock('https://api.example.com')
        .get('/users/123')
        .reply(200, fixture);

      const user = await producer.getUser('123');
      expect(user.id).to.be.instanceof(UUID);
    });

    it('should handle user not found', async () => {
      nock('https://api.example.com')
        .get('/users/999')
        .reply(404, { error: 'Not found' });

      try {
        await producer.getUser('999');
        expect.fail('Should have thrown an error');
      } catch (error: any) {
        expect(error).to.be.instanceOf(NoSuchObjectError);
      }
    });
  });
});
```

## Core Principles for HTTP Mocking

1. **Mock at HTTP level** - Mock the network request, not internal methods.
2. **Match requests accurately** - Include method, path, headers, and query params.
3. **Return realistic responses** - Use response formats matching real API.
4. **Clean up after tests** - Use `afterEach(() => nock.cleanAll())`.
5. **Verify mocks called** - Assert `expect(nock.isDone()).toBe(true)`.

## Basic HTTP Mock Pattern

```typescript
import nock from 'nock';

describe('WebhookProducer', () => {
  afterEach(() => {
    nock.cleanAll();  // Clean up after each test
  });

  it('should list webhooks successfully', async () => {
    nock('https://api.github.com')
      .get('/repos/octocat/Hello-World/hooks')
      .reply(200, [mockWebhookResponse]);

    const producer = new WebhookProducer(httpClient);
    const webhooks = await producer.list('octocat', 'Hello-World');

    expect(webhooks).toHaveLength(1);
    expect(webhooks[0].id).toBeDefined();
    expect(nock.isDone()).toBe(true);  // Verify mock was called
  });
});
```

## Validation Checklist

```bash
# Verify ONLY nock is used
grep "from ['\"]nock['\"]" test/unit/*.ts
# Should show nock imports

# Ensure NO forbidden mocking libraries
grep -E "jest\.mock|sinon|fetch-mock" test/*.ts
# Should return nothing (exit code 1)

# Verify mock cleanup present
grep "nock.cleanAll()" test/unit/*.ts
# Should show in afterEach blocks

# Verify mock verification present
grep "nock.isDone()" test/unit/*.ts
# Should show in test assertions
```

## Anti-Patterns: What NOT to Do

### ❌ WRONG: Using jest.mock

```typescript
// ❌ NO! Don't mock at method level
jest.mock('./WebhookProducer');
```

### ❌ WRONG: Using sinon

```typescript
// ❌ NO! Don't use sinon
import sinon from 'sinon';
const stub = sinon.stub(producer, 'list');
```

### ❌ WRONG: Using fetch-mock

```typescript
// ❌ NO! Use nock instead
import fetchMock from 'fetch-mock';
```

## Standard Output Format

When documenting HTTP mocking strategy:

```markdown
# HTTP Mocking Strategy: {ProducerName}

## Mock Library
✅ **nock** (ONLY allowed library)

## Mock Patterns Created

### List Operation
```typescript
nock('https://api.github.com')
  .get('/repos/octocat/Hello-World/hooks')
  .reply(200, [mockWebhookResponse]);
```

### Get Operation
```typescript
nock('https://api.github.com')
  .get('/repos/octocat/Hello-World/hooks/12345678')
  .reply(200, mockWebhookResponse);
```

### Error Case
```typescript
nock('https://api.github.com')
  .get('/repos/octocat/Hello-World/hooks/999')
  .reply(404, { message: 'Not Found' });
```

## Success Criteria

HTTP mocking implementation MUST meet all criteria:

- ✅ Only nock library used (no jest.mock, sinon, fetch-mock)
- ✅ All HTTP requests mocked at network level
- ✅ Realistic mock responses (match API format)
- ✅ Proper cleanup after tests (`nock.cleanAll()`)
- ✅ Mock verification in tests (`nock.isDone()`)
- ✅ Reusable mock patterns/fixtures where appropriate
- ✅ Request matching includes method, path, headers (when relevant)