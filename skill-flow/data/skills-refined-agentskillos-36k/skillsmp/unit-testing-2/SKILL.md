---
name: unit-testing
description: Unit test patterns using nock for HTTP mocking without credentials
---

# Unit Test Patterns

Unit tests verify business logic with mocked HTTP interactions. They run fast, require no credentials, and work offline.

## 🚨 CRITICAL RULES (Immediate Failure)

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

**WHY**:
- Nock intercepts HTTP requests at the network level
- Consistent with existing test infrastructure
- Works with any HTTP client library (axios, node-fetch, etc.)
- Can record and replay real API interactions

**NEVER**:
- ❌ Use jest.mock()
- ❌ Use sinon stubs/spies for HTTP
- ❌ Use fetch-mock or similar
- ❌ Mock the HTTP client class directly
- ❌ Use any mocking library except nock

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

// ❌ WRONG: Env vars in unit test Common.ts
import { config } from 'dotenv';  // NO
config();  // NO
export const API_KEY = process.env.API_KEY;  // NO
```

**WHY**:
- Unit tests must be deterministic and repeatable
- Should work without any .env file or external configuration
- Credentials belong in integration tests only
- Mocked tests don't need real values

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

**Requirements**:
- ✅ Every operation has unit tests
- ✅ Both success and error cases tested
- ✅ 100% unit test pass rate

## 🟡 STANDARD RULES

### Test File Naming Convention

**MANDATORY naming pattern for unit test files:**

```
test/unit/{Resource}ProducerTest.ts       # Producer unit tests
test/unit/ConnectionTest.ts               # Connection unit tests
test/unit/MappersTest.ts                  # Mapper unit tests
```

**Examples**:
- ✅ `test/unit/AccessProducerTest.ts` - unit test
- ✅ `test/unit/UserProducerTest.ts` - unit test
- ✅ `test/unit/ConnectionTest.ts` - unit test
- ✅ `test/unit/MappersTest.ts` - mapper unit test

**Rationale**:
- Consistent naming makes test files easy to find
- Follows TypeScript naming conventions (PascalCase with Test suffix)
- `test/unit/` folder location makes it clear these are unit tests

### Connection Testing - Unit Tests

**EVERY module MUST have connection unit tests: `test/unit/ConnectionTest.ts`**

Tests connection lifecycle with mocked HTTP (no real credentials).

```typescript
// test/unit/ConnectionTest.ts
import { expect } from 'chai';
import * as nock from 'nock';
import { Email, InvalidCredentialsError } from '@zerobias-org/types-core-js';
import { newService } from '../../src';

describe('Connection', () => {
  describe('connect', () => {
    it('should successfully authenticate and store token', async () => {
      nock('https://api.example.com')
        .post('/auth/login')
        .reply(200, { accessToken: 'test-token', expiresAt: '2025-10-02T00:00:00Z' });

      const connector = newService();
      const connectionState = await connector.connect({
        email: new Email('test@example.com'),
        password: 'testpass',
      });

      expect(connectionState).to.have.property('accessToken');
      expect(await connector.isConnected()).to.be.true;
    });

    it('should handle authentication failure', async () => {
      nock('https://api.example.com')
        .post('/auth/login')
        .reply(401, { error: 'Invalid credentials' });

      const connector = newService();

      try {
        await connector.connect({
          email: new Email('test@example.com'),
          password: 'wrongpass',
        });
        expect.fail('Should have thrown an error');
      } catch (error: any) {
        expect(error).to.be.instanceOf(InvalidCredentialsError);
      }
    });
  });

  describe('isConnected', () => {
    it('should return true when connected', async () => {
      nock('https://api.example.com')
        .post('/auth/login')
        .reply(200, { accessToken: 'test-token', expiresAt: '2025-10-02T00:00:00Z' });

      const connector = newService();
      await connector.connect({
        email: new Email('test@example.com'),
        password: 'testpass',
      });

      expect(await connector.isConnected()).to.be.true;
    });

    it('should return false when not connected', async () => {
      const connector = newService();
      expect(await connector.isConnected()).to.be.false;
    });
  });

  describe('disconnect', () => {
    it('should clear connection state', async () => {
      nock('https://api.example.com')
        .post('/auth/login')
        .reply(200, { accessToken: 'test-token', expiresAt: '2025-10-02T00:00:00Z' });

      const connector = newService();
      await connector.connect({
        email: new Email('test@example.com'),
        password: 'testpass',
      });

      await connector.disconnect();
      expect(await connector.isConnected()).to.be.false;
    });
  });
});
```

**Benefits**:
- ✅ Ensures connection lifecycle works correctly with mocked HTTP
- ✅ Tests all connection methods systematically
- ✅ Fast execution without network calls

### Connected Instance Helpers - Unit Test Common.ts

**CRITICAL: Unit test Common.ts provides fully mocked helpers with NO environment variables**

```typescript
// test/unit/Common.ts
import * as nock from 'nock';
import { Email } from '@zerobias-org/types-core-js';
import { newService } from '../../src';
import type { ServiceConnector } from '../../src';

/**
 * Get a connected instance for unit testing.
 * Uses mocked HTTP - no real credentials needed.
 * Unit tests should NEVER depend on environment variables.
 */
export async function getConnectedInstance(): Promise<ServiceConnector> {
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

**Key Points**:
- ✅ NO environment variables or dotenv
- ✅ NO credential loading
- ✅ Uses nock to mock HTTP requests
- ✅ Works without any .env file
- ✅ Always returns a mocked connected instance

**Usage in unit tests**:
```typescript
// test/unit/AccessProducerTest.ts
import { expect } from 'chai';
import * as nock from 'nock';
import { getConnectedInstance } from './Common';

describe('AccessProducer', () => {
  let accessApi;

  beforeEach(async () => {
    // Use mocked connected instance from Common.ts
    // No env vars, no real credentials - fully mocked
    const connector = await getConnectedInstance();
    accessApi = connector.getAccessApi();
  });

  it('should retrieve access token info', async () => {
    nock('https://api.example.com')
      .get('/auth/accessTokens/test-token')
      .reply(200, { token: 'test-token', identityId: 123 });

    const tokenInfo = await accessApi.getToken();
    expect(tokenInfo.token).to.equal('test-token');
  });
});
```

### File Organization

**Unit test structure:**
```
test/
├── unit/
│   ├── Common.ts                    # ONLY mocked helpers (getConnectedInstance with nock)
│   ├── ConnectionTest.ts            # NO env vars, fully mocked
│   ├── {Resource}ProducerTest.ts    # NO env vars, fully mocked
│   └── MappersTest.ts               # Pure logic tests
└── fixtures/
    ├── sanitized/                   # Sanitized API responses for unit tests
    └── templates/                   # Reusable templates
```

**Key points**:
- ✅ `test/unit/Common.ts` contains ONLY mocked helpers
- ✅ NO environment variables anywhere in unit tests
- ✅ Import from `./Common` (same folder)
- ✅ Unit tests run always, no credentials needed

### Unit Test Pattern

**Standard unit test structure:**

```typescript
describe('{ClassName}', () => {
  describe('{methodName}', () => {
    it('should {expected behavior}', async () => {
      // Arrange - Set up nock mocks
      nock('https://api.example.com')
        .get('/resource/123')
        .reply(200, fixture);

      // Act - Execute the method
      const result = await api.getResource('123');

      // Assert - Verify the result
      expect(result).to.be.instanceof(ExpectedType);
      expect(result.id).to.equal('123');
    });
  });
});
```

**Key elements**:
- ✅ Arrange/Act/Assert pattern
- ✅ Descriptive test names with 'should'
- ✅ Nock mocks before method call
- ✅ Type assertions using instanceof

### Test Data Management

**Use sanitized fixtures from real API responses:**

```typescript
// test/fixtures/sanitized/user-response.json
{
  "id": "123",
  "firstName": "Jane",
  "lastName": "Doe",
  "email": "user@example.com"
}

// test/unit/UserProducerTest.ts
import userFixture from '../fixtures/sanitized/user-response.json';

it('should map user correctly', async () => {
  nock('https://api.example.com')
    .get('/users/123')
    .reply(200, userFixture);

  const user = await producer.getUser('123');
  expect(user.id).to.be.instanceof(UUID);
  expect(user.email).to.be.instanceof(Email);
});
```

**Rules**:
- ✅ Use real API response structure
- ✅ Sanitize ALL PII (names, emails, phone numbers)
- ✅ Store in test/fixtures/sanitized/
- ✅ Never use randomly generated test data

### Mock Strategy

**HTTP-level mocking with nock ONLY:**

```typescript
// ✅ CORRECT - HTTP level mocking
nock('https://api.example.com')
  .get('/users/123')
  .reply(200, { id: '123', name: 'John' });

// ✅ CORRECT - Error scenarios
nock('https://api.example.com')
  .get('/users/999')
  .reply(404, { error: 'Not found' });

// ✅ CORRECT - Multiple requests
nock('https://api.example.com')
  .get('/users/123')
  .reply(200, userFixture)
  .get('/organizations/456')
  .reply(200, orgFixture);

// ❌ WRONG - Method/class level mocking
sinon.stub(client, 'getUser').returns(mockUser);  // NO
jest.spyOn(client, 'getUser').mockReturnValue(mockUser);  // NO
```

**Rules**:
- ✅ Mock at HTTP level, not at client/method level
- ✅ Use real response structure from fixtures
- ✅ Test error scenarios with nock error responses
- ✅ ONLY use nock for all HTTP mocking

## 🟢 GUIDELINES

### Test Naming

**Descriptive test names explaining the scenario:**

```typescript
// ✅ GOOD - Clear, specific
it('should retrieve user by ID with correct type mapping', async () => { ... });
it('should throw NoSuchObjectError when user not found', async () => { ... });
it('should map email string to Email type', async () => { ... });

// ❌ BAD - Vague, unclear
it('should work', async () => { ... });
it('test get user', async () => { ... });
```

**Use 'should' for expected behaviors:**
- ✅ "should retrieve user by ID"
- ✅ "should throw error when invalid ID"
- ✅ "should map API response to core types"

### Assertion Patterns

**Type assertions:**
```typescript
// ✅ CORRECT - Use instanceof for core types
expect(user.id).to.be.instanceof(UUID);
expect(user.email).to.be.instanceof(Email);
expect(user.createdAt).to.be.instanceof(Date);

// ❌ WRONG - Checking string/primitive
expect(typeof user.id).to.equal('string');  // Not specific enough
```

**Structure assertions:**
```typescript
// ✅ CORRECT - Check object structure
expect(result).to.have.property('id');
expect(result).to.have.property('name');
expect(result).to.deep.equal(expectedObject);

// ✅ CORRECT - Check arrays
expect(users).to.be.an('array');
expect(users).to.have.length(2);
expect(users[0]).to.be.instanceof(User);
```

**Error assertions - ALWAYS use specific core error types:**
```typescript
// ✅ CORRECT - Specific error type
try {
  await api.someMethod();
  expect.fail('Should have thrown an error');
} catch (error: any) {
  expect(error).to.be.instanceOf(InvalidCredentialsError);
}

// ❌ WRONG - Generic error type
expect(error).to.be.instanceOf(Error);  // Too generic

// Common core error types to use in assertions:
// - InvalidCredentialsError (401 auth failures)
// - UnauthorizedError (403 permission denied)
// - NoSuchObjectError (404 not found)
// - RateLimitExceededError (429 rate limits)
// - InvalidInputError (validation failures)
// - UnexpectedError (other API errors)
```

### Test Recording and Sanitization

**When credentials available, record real API interactions to create unit tests:**

**Step 1: Record Real API Interactions**
```typescript
import * as nock from 'nock';

nock.recorder.rec({
  output_objects: true,
  enable_reqheaders_recording: true
});

await runIntegrationTest();
const recordings = nock.recorder.play();
```

**Step 2: AI-Powered Sanitization**

**CRITICAL**: Remove ALL PII before saving fixtures

**Sanitization Checklist**:
- [ ] Real names → "Jane Doe", "John Smith"
- [ ] Email addresses → "user@example.com"
- [ ] Phone numbers → "+1-555-0123"
- [ ] Addresses → "123 Main St, Anytown, ST 12345"
- [ ] SSNs/Tax IDs → "XXX-XX-1234"
- [ ] API keys → "sk_test_..."
- [ ] Passwords → "********"
- [ ] Birth dates → "1990-01-01"
- [ ] Company names → "Example Corp"

**Name Splitting**:
```json
// ✅ CORRECT
{
  "firstName": "Jane",
  "lastName": "Doe"
}
```

**Step 3: Generate Unit Tests**
1. Create unit test matching integration test structure
2. Use sanitized fixtures for mocked responses
3. Match test cases 1:1 with integration tests
4. Use HTTP-level mocking (not method mocking)

**Step 4: Fixture Organization**
```
test/fixtures/
├── recorded/          # Raw recordings (.localmemory)
├── sanitized/         # For unit tests
└── templates/         # Reusable templates
```

## Validation

**Validate unit test patterns:**

```bash
# Check unit tests exist
ls -lh test/unit/ConnectionTest.ts
ls -lh test/unit/*ProducerTest.ts

# Check unit test Common.ts has NO env vars
grep -i "dotenv" test/unit/Common.ts && echo "❌ FAIL: Unit tests should not use dotenv" || echo "✅ PASS"
grep -i "process.env" test/unit/Common.ts && echo "❌ FAIL: Unit tests should not use env vars" || echo "✅ PASS"

# Check unit tests use nock
grep -r "import.*nock" test/unit/*.ts | wc -l

# Check NO forbidden mocking libraries in unit tests
grep -r "jest.mock\|sinon\|fetch-mock" test/unit/*.ts && echo "❌ FAIL: Forbidden mocking library" || echo "✅ PASS"

# Run unit tests (should work without .env)
npm run test:unit
```

**Expected results:**
- ✅ Unit tests exist for Connection and all Producers
- ✅ NO dotenv or process.env in test/unit/
- ✅ All unit tests use nock for HTTP mocking
- ✅ NO jest/sinon/fetch-mock in unit tests
- ✅ Unit tests pass without .env file
