---
name: integration-testing
description: Integration test patterns using real API calls with credentials from .env
---

# Integration Test Patterns

Integration tests verify real API interactions with live credentials. They test authentication, network communication, and API behavior.

## 🚨 CRITICAL RULES (Immediate Failure)

### 1. Test Data Configuration - NEVER Hardcode Values

**🚨 CRITICAL: ALL integration test values MUST be in .env, NEVER hardcoded**

When user provides test values (IDs, names, etc.), they MUST go in `.env`:

```bash
# ✅ CORRECT - Test values in .env
SERVICE_API_KEY=your-api-key
SERVICE_TEST_USER_ID=12345
SERVICE_TEST_ORGANIZATION_ID=1067
SERVICE_TEST_RESOURCE_NAME=test-resource

# ❌ WRONG - Hardcoding in test files
const userId = '12345';  // NO!
const orgId = '1067';    // NO!
```

**RULE**:
1. User gives you test values → Add to `.env` immediately
2. Export from `test/integration/Common.ts`
3. Import and use in integration tests
4. NEVER hardcode any test data values

**Example**:

```typescript
// .env
AVIGILON_ALTA_ACCESS_TEST_ORGANIZATION_ID=1067

// test/integration/Common.ts
export const AVIGILON_ALTA_ACCESS_TEST_ORGANIZATION_ID =
  process.env.AVIGILON_ALTA_ACCESS_TEST_ORGANIZATION_ID || '';

// test/integration/OrganizationProducerTest.ts
import { AVIGILON_ALTA_ACCESS_TEST_ORGANIZATION_ID } from './Common';

it('should retrieve organization', async () => {
  const organizationId = AVIGILON_ALTA_ACCESS_TEST_ORGANIZATION_ID;  // ✅ From .env
  // NOT: const organizationId = '1067';  // ❌ Hardcoded

  const org = await api.get(organizationId);
  expect(org.id).to.equal(organizationId);
});
```

**WHY**:
- Test values are configuration, not code
- Different developers may need different test IDs
- Makes tests portable across environments
- Easy to update without touching code
- Consistent with credential management

### 2. Credential Loading for Integration Tests

**🚨 CRITICAL: Automatic credential loading with dotenv**

Integration tests need credentials and test values from `.env` file. Configure automatic loading:

**Step 0: Create .env file after scaffolding**

**IMMEDIATELY after running module scaffolding**, create a `.env` file in the module root with credentials from the user's initial request:

```bash
# Example: User said "credentials are in .env: SERVICE_EMAIL and SERVICE_PASSWORD"
# Create module/.env with:
SERVICE_EMAIL=user@example.com
SERVICE_PASSWORD=their-password
SERVICE_API_KEY=their-api-key
```

**Important**: Extract credentials from wherever user specified in their request:
- Module root `.env`
- Repository root `.env`
- `.connectionProfile.json`
- User message directly
- System environment

**Step 1: Install dotenv**
```bash
npm install --save-dev dotenv
```

**Step 2: Configure .mocharc.json**
```json
{
  "extension": ["ts"],
  "require": ["ts-node/register", "dotenv/config"]
}
```

**Step 3: Load dotenv explicitly in test/integration/Common.ts**
```typescript
// test/integration/Common.ts - ONLY file allowed to access process.env
import { config } from 'dotenv';

// Load .env file explicitly to ensure credentials are available
config();

export const SERVICE_API_KEY = process.env.SERVICE_API_KEY || '';
export const SERVICE_BASE_URL = process.env.SERVICE_BASE_URL || 'https://api.example.com';

export function hasCredentials(): boolean {
  return !!SERVICE_API_KEY;
}
```

**Why explicit config()?**
- .mocharc.json `"require": ["dotenv/config"]` loads dotenv, BUT
- Environment variables in Common.ts are evaluated at module load time
- Explicit `config()` ensures .env is loaded BEFORE env vars are accessed
- This guarantees integration tests can detect credentials properly

**Step 4: Use in integration tests**
```typescript
import { hasCredentials, SERVICE_API_KEY } from './Common';

describe('Service Integration Tests', function () {
  before(function () {
    if (!hasCredentials()) {
      this.skip(); // Skip entire suite if no credentials
    }
  });

  it('should connect with real API', async function () {
    // Test with real credentials
  });
});
```

**Benefits**:
- ✅ Credentials automatically loaded from `.env`
- ✅ No manual process.env access in test files
- ✅ Graceful skipping when credentials unavailable
- ✅ Consistent credential management across all modules

**Document in USERGUIDE.md**:
```markdown
### Setting Up Credentials for Testing

Create a `.env` file in the module root:

\`\`\`bash
SERVICE_API_KEY=your-api-key
SERVICE_SECRET=your-secret
\`\`\`

The test suite automatically loads credentials using `dotenv`.
```

### 3. Debug Logging is MANDATORY

**🚨 CRITICAL: All integration tests MUST include debug logging**

```typescript
import { getLogger, hasCredentials } from './Common';

const logger = getLogger('{Resource}ProducerTest');

describe('{Resource} Producer Integration', function () {
  before(function () {
    if (!hasCredentials()) {
      this.skip();
    }
  });

  it('should perform operation with real API', async function () {
    const connector = newService();

    logger.debug('connector.connect(email, password)');
    await connector.connect({ email, password });
    logger.debug('→', JSON.stringify(connectionState, null, 2));

    const api = connector.getResourceApi();

    logger.debug('api.getResource(id)');
    const result = await api.getResource('123');
    logger.debug('→', JSON.stringify(result, null, 2));

    expect(result).to.have.property('id');
  });
});
```

**Debug Logging Requirements**:
- ✅ Import getLogger from `./Common` (not from @zerobias-org/logger directly)
- ✅ Create logger with test file name: `const logger = getLogger('{Resource}ProducerTest')`
- ✅ Log operation call BEFORE execution: `logger.debug('api.methodName(param1, param2)')`
- ✅ Log result AFTER execution: `logger.debug('→', JSON.stringify(result, null, 2))`
- ✅ Use arrow `→` to indicate result
- ✅ Always use `JSON.stringify(result, null, 2)` for consistent formatting

**Why debug logging?**
- Visible when log level set to debug via `LOG_LEVEL=debug npm run test:integration`
- Shows exact operation calls with parameters
- Shows complete API responses for debugging
- Helps diagnose integration issues without re-running tests

## 🟡 STANDARD RULES

### Test File Naming Convention

**MANDATORY naming pattern for integration test files:**

```
test/integration/{Resource}ProducerTest.ts # Producer integration tests
test/integration/ConnectionTest.ts         # Connection integration tests
```

**Examples**:
- ✅ `test/integration/AccessProducerTest.ts` - integration test
- ✅ `test/integration/UserProducerTest.ts` - integration test
- ✅ `test/integration/ConnectionTest.ts` - integration test

**Rationale**:
- Consistent naming makes test files easy to find
- Integration tests use SAME names as unit tests - folder location distinguishes them
- No need for `IntegrationTest` suffix since `test/integration/` folder makes it clear

### Connection Testing - Integration Tests

**EVERY module MUST have connection integration tests: `test/integration/ConnectionTest.ts`**

Tests with real API and credentials.

```typescript
// test/integration/ConnectionTest.ts
import { expect } from 'chai';
import { LoggerEngine } from '@zerobias-org/logger';
import { Email } from '@zerobias-org/types-core-js';
import { newService } from '../../src';
import { SERVICE_EMAIL, SERVICE_PASSWORD, hasCredentials } from './Common';

const logger = LoggerEngine.root().get('ConnectionTest');

describe('Connection Integration Tests', function () {
  this.timeout(30000);

  before(function () {
    if (!hasCredentials()) {
      this.skip();
    }
  });

  describe('connect', () => {
    it('should successfully connect to real API', async () => {
      const connector = newService();

      logger.debug('connector.connect(email, password)');
      const connectionState = await connector.connect({
        email: new Email(SERVICE_EMAIL),
        password: SERVICE_PASSWORD,
      });
      logger.debug('→', JSON.stringify(connectionState, null, 2));

      expect(connectionState).to.have.property('accessToken');
    });

    it('should fail with invalid credentials', async () => {
      const connector = newService();

      logger.debug('connector.connect(invalid credentials)');
      try {
        await connector.connect({
          email: new Email('invalid@example.com'),
          password: 'wrongpassword',
        });
        expect.fail('Should have thrown an error');
      } catch (error: any) {
        logger.debug('→ error', JSON.stringify({ name: error.name }, null, 2));
        expect(error).to.exist;
      }
    });
  });

  describe('isConnected', () => {
    it('should return true when connected', async () => {
      const connector = newService();

      await connector.connect({
        email: new Email(SERVICE_EMAIL),
        password: SERVICE_PASSWORD,
      });

      logger.debug('connector.isConnected()');
      const isConnected = await connector.isConnected();
      logger.debug('→', JSON.stringify({ isConnected }, null, 2));

      expect(isConnected).to.be.true;
    });

    it('should return false when not connected', async () => {
      const connector = newService();

      logger.debug('connector.isConnected() - without connection');
      const isConnected = await connector.isConnected();
      logger.debug('→', JSON.stringify({ isConnected }, null, 2));

      expect(isConnected).to.be.false;
    });
  });

  describe('disconnect', () => {
    it('should successfully disconnect from API', async () => {
      const connector = newService();

      await connector.connect({
        email: new Email(SERVICE_EMAIL),
        password: SERVICE_PASSWORD,
      });

      logger.debug('connector.disconnect()');
      await connector.disconnect();
      logger.debug('→ disconnect completed');
    });
  });
});
```

**Benefits**:
- ✅ Tests real API authentication and connection
- ✅ Verifies credentials work correctly
- ✅ Catches network and API-specific issues
- ✅ Debug logging shows actual API responses

### Connected Instance Helpers - Integration Test Common.ts

**CRITICAL: Integration test Common.ts provides real credentials with connection caching**

```typescript
// test/integration/Common.ts
import { config } from 'dotenv';
import { Email } from '@zerobias-org/types-core-js';
import { LoggerEngine } from '@zerobias-org/logger';
import { newService } from '../../src';
import type { ServiceConnector } from '../../src';

// Load .env file explicitly to ensure credentials are available
config();

export const SERVICE_EMAIL = process.env.SERVICE_EMAIL || '';
export const SERVICE_PASSWORD = process.env.SERVICE_PASSWORD || '';

// Test data values - export any test IDs, names, or other values from .env
export const SERVICE_TEST_USER_ID = process.env.SERVICE_TEST_USER_ID || '';
export const SERVICE_TEST_ORGANIZATION_ID = process.env.SERVICE_TEST_ORGANIZATION_ID || '';

/**
 * Get a logger with configurable level from LOG_LEVEL env var.
 * Usage: LOG_LEVEL=debug npm run test:integration
 */
export function getLogger(name: string) {
  return LoggerEngine.root().get(name);
}

if (process.env.LOG_LEVEL) {
  switch (process.env.LOG_LEVEL) {
    case 'trace': {
      getLogger().setLevel(LogLevel.TRACE);
      break;
    }
    case 'debug': {
      getLogger().setLevel(LogLevel.DEBUG);
      break;
    }
    case 'verbose': {
      getLogger().setLevel(LogLevel.VERBOSE);
      break;
    }
    case 'info': {
      getLogger().setLevel(LogLevel.INFO);
      break;
    }
    case 'warn': {
      getLogger().setLevel(LogLevel.WARN);
      break;
    }
    case 'error': {
      getLogger().setLevel(LogLevel.ERROR);
      break;
    }
    case 'crit': {
      getLogger().setLevel(LogLevel.CRIT);
      break;
    }
    default: {
      getLogger().setLevel(LogLevel.INFO);
      break;
    }
  }
}

export function hasCredentials(): boolean {
  return !!SERVICE_EMAIL && !!SERVICE_PASSWORD;
}

// Cached connector instance - connect once, reuse many times
let cachedConnector: ServiceConnector | null = null;

/**
 * Get a connected instance for integration testing.
 * Connects once on first call, then returns cached instance on subsequent calls.
 * This avoids repeated authentication overhead across multiple tests.
 * Uses real credentials from .env file.
 * Makes real API calls.
 */
export async function getConnectedInstance(): Promise<ServiceConnector> {
  if (cachedConnector) {
    return cachedConnector;
  }

  const connector = newService();

  await connector.connect({
    email: new Email(SERVICE_EMAIL),
    password: SERVICE_PASSWORD,
  });

  cachedConnector = connector;
  return connector;
}
```

**Key Points**:
- ✅ Uses dotenv to load real credentials
- ✅ Exports credential constants
- ✅ Exports getLogger() helper that respects LOG_LEVEL env var
- ✅ Has hasCredentials() check
- ✅ **Connection caching**: Connects once on first call, returns cached instance on subsequent calls
- ✅ **Performance**: Avoids repeated authentication overhead across multiple integration tests
- ✅ Makes real API calls
- ✅ Requires .env file to run
- ✅ Run with `LOG_LEVEL=debug npm run test:integration` to see debug logs

**Usage in integration tests**:
```typescript
// test/integration/ServiceProducerTest.ts
import { expect } from 'chai';
import { getConnectedInstance, hasCredentials, getLogger } from './Common';

const logger = getLogger('ServiceProducerTest');

describe('Service Integration', function () {
  before(function () {
    if (!hasCredentials()) {
      this.skip(); // Skip if no credentials
    }
  });

  it('should retrieve access token info from real API', async () => {
    logger.debug('getConnectedInstance()');
    const connector = await getConnectedInstance();

    const api = connector.getAccessApi();

    logger.debug('api.getToken()');
    const tokenInfo = await api.getToken();
    logger.debug('→', JSON.stringify(tokenInfo, null, 2));

    expect(tokenInfo.token).to.exist;
  });
});
```

### Environment Variable Usage

**CRITICAL: ONLY integration tests use environment variables**

- **ONLY ALLOWED IN**: `test/integration/Common.ts`
- **NEVER in**: Test files or unit tests
- **Test files**: Import from Common.ts, NEVER access process.env directly

```typescript
// ✅ CORRECT: test/integration/Common.ts ONLY
import { config } from 'dotenv';

config();

export const TEST_API_KEY = process.env.TEST_API_KEY || '';
export const TEST_BASE_URL = process.env.TEST_BASE_URL || 'https://api.example.com';

export function hasCredentials(): boolean {
  return !!TEST_API_KEY;
}

// ✅ CORRECT: Integration test files
import { TEST_API_KEY, hasCredentials } from './Common';

// ❌ WRONG: Direct access in test files
const apiKey = process.env.TEST_API_KEY;
```

### File Organization

**Integration test structure:**
```
test/
├── integration/
│   ├── Common.ts                    # Real credentials from .env + getConnectedInstance
│   ├── ConnectionTest.ts            # Real API calls, requires .env
│   └── {Resource}ProducerTest.ts    # Real API calls, requires .env
└── .env                             # Credentials (not committed)
```

**Key points**:
- ✅ `test/integration/Common.ts` loads real credentials from .env
- ✅ Has hasCredentials() check
- ✅ Import from `./Common` (same folder)
- ✅ Integration tests skip if no credentials via hasCredentials() check

### Integration Test Pattern

**Standard integration test structure with debug logging:**

```typescript
import { getLogger, hasCredentials } from './Common';

const logger = getLogger('{Resource}ProducerTest');

describe('{Resource} Producer Integration', function () {
  // Set timeout for real API calls
  this.timeout(30000);

  before(function () {
    // Skip entire suite if no credentials
    if (!hasCredentials()) {
      this.skip(); // This is OK - skips whole suite
    }
  });

  it('should perform operation with real API', async function () {
    const connector = newService();

    logger.debug('connector.connect(email, password)');
    await connector.connect({ email, password });
    logger.debug('→', JSON.stringify(connectionState, null, 2));

    const api = connector.getResourceApi();

    logger.debug('api.getResource(id)');
    const result = await api.getResource('123');
    logger.debug('→', JSON.stringify(result, null, 2));

    expect(result).to.have.property('id');
  });
});
```

**Key elements**:
- ✅ Import getLogger from ./Common
- ✅ Set timeout for real API calls
- ✅ Skip suite if no credentials (in before() hook)
- ✅ Debug logging BEFORE and AFTER each operation
- ✅ Use arrow `→` to indicate result
- ✅ JSON.stringify for consistent formatting

**Note**: Using `this.skip()` in `before()` hook is ALLOWED - it gracefully skips the entire suite when credentials missing.

### Test Data Management

**Use real API responses:**

```typescript
it('should retrieve organization', async () => {
  logger.debug('api.getOrganization(id)');
  const org = await api.getOrganization(TEST_ORGANIZATION_ID);
  logger.debug('→', JSON.stringify(org, null, 2));

  // Verify real API response structure
  expect(org).to.have.property('id');
  expect(org).to.have.property('name');
  expect(org.id).to.be.instanceof(UUID);
});
```

**Rules**:
- ✅ Use real API responses
- ✅ Load test IDs from .env via Common.ts
- ✅ Debug logging shows actual API responses
- ✅ Verify response structure and types

### Credential Discovery

**Where to find credentials (in order):**

1. Check `.env` file first
2. Check `.connectionProfile.json` second
3. Ask user if not found
4. Skip integration tests gracefully if no credentials

```typescript
// test/integration/Common.ts
export function hasCredentials(): boolean {
  return !!SERVICE_EMAIL && !!SERVICE_PASSWORD;
}

// Integration tests
before(function () {
  if (!hasCredentials()) {
    this.skip(); // Graceful skip
  }
});
```

## 🟢 GUIDELINES

### Common Failure Diagnoses

**When integration tests fail:**

1. **Wrong API requests**: Log request/response, fix mapping
   - Check debug logs with `LOG_LEVEL=debug npm run test:integration`
   - Compare actual vs expected request format
   - Verify endpoint URLs and HTTP methods

2. **Mapping issues**: Compare API response vs mapped output
   - Look at debug logs showing raw API response
   - Check mapper implementation
   - Verify type conversions

3. **Auth failures**: Verify credentials and method
   - Check .env file has correct credentials
   - Verify authentication flow in ConnectionTest
   - Check if API key/token is expired

4. **Type mismatches**: Check generated types vs implementation
   - Verify OpenAPI spec matches reality
   - Check type generation ran successfully
   - Compare API response structure to TypeScript types

### Final Validation Cycle

**Run full test suite including integration tests:**

```bash
npm run clean
npm run build
npm run test
npm run test:integration  # If credentials available
```

**SUCCESS CRITERIA**:
- Zero test failures
- Zero skipped tests (except integration without creds)
- Build exits with code 0

## Validation

**Validate integration test patterns:**

```bash
# Check integration tests exist
ls -lh test/integration/ConnectionTest.ts
ls -lh test/integration/*ProducerTest.ts

# Check integration Common.ts loads dotenv
grep -i "dotenv" test/integration/Common.ts && echo "✅ PASS" || echo "❌ FAIL: Should use dotenv"

# Check integration tests have debug logging
grep -r "getLogger" test/integration/*Test.ts | wc -l

# Check hasCredentials() is used
grep -r "hasCredentials()" test/integration/*Test.ts | wc -l

# Check .env file exists
ls -lh .env

# Run integration tests (requires .env)
LOG_LEVEL=debug npm run test:integration
```

**Expected results:**
- ✅ Integration tests exist for Connection and all Producers
- ✅ test/integration/Common.ts uses dotenv
- ✅ All integration tests have debug logging
- ✅ All integration tests check hasCredentials()
- ✅ .env file exists with credentials
- ✅ Integration tests pass with real API
