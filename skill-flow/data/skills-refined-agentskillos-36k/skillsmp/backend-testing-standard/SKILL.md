---
name: backend-testing-standard
description: Standard for writing backend unit tests. Enforces using Mock Data and verifying business logic without direct database manipulation. Use this when writing or refactoring backend tests.
license: Private
---

# Backend Testing Standard

This skill defines the standard for writing backend unit tests in this project.
**Goal**: Isolate tests, enable parallel execution, and focus on business logic verification.

## Core Rules

### 1. ❌ PROHIBITED: Direct Database Schema Modification

- **DO NOT** use `sequelize.sync({ force: true })`.
- **DO NOT** use `Model.sync()`.
- **DO NOT** use raw SQL to `DROP` or `CREATE` tables/schemas in tests.
- **Reason**: These operations destroy the shared database state, causing race conditions in parallel tests.

### 2. ✅ REQUIRED: Use Mocks for Data

- **DO NOT** rely on pre-seeded database data.
- **DO NOT** rely on other tests' side effects.
- **MOCK** the database calls (e.g., `Model.findOne`, `Model.create`) using `vi.mock` (Vitest) or `jest.mock`.
- **Reason**: Tests must be deterministic and independent.

### 3. ✅ REQUIRED: Derive Mock Data from Specs & Migrations

- **DO NOT** guess the data structure.
- **REFER TO** `docs/spec` and database migrations (or Sequelize Model definitions) to ensure your mock JSON objects match the actual data structure found in production.
- **Reason**: Discrepancies between mock data and real schema lead to false positives/negatives.

### 3. ✅ REQUIRED: Focus on Business Logic

- Test the **Service Layer** and **Controller Layer** logic.
- Verify that:
  - Inputs are validated correctly.
  - Logic branches (if/else) are covered.
  - Correct Service/Model methods are called with expected arguments.
  - Proper Responses/Errors are returned.

## Decision Tree

```
Testing a Feature?
  ├─ Is it pure logic? (e.g. calculation)
  │   └─ Write a simple Unit Test (no database needed).
  │
  └─ Does it involve DB operations?
      └─ Mock the Model methods.
          ├─ `User.findOne` -> return fake user
          ├─ `Transaction.create` -> return fake transaction
          └─ Verify your function handles the return value correctly.
```

## Setup & Examples

### Mocking with Vitest

See [examples/mock_test_example.ts](examples/mock_test_example.ts) for a complete example.

#### Common Pattern

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import * as transactionService from '@/services/transactionServices';
import Transaction from '@/models/transaction';

// 1. Mock the specific model methods
vi.mock('@/models/transaction', () => ({
  default: {
    create: vi.fn(),
    findOne: vi.fn(),
  },
}));

describe('Transaction Service', () => {
  beforeEach(() => {
    vi.clearAllMocks(); // Reset call counts
  });

  it('should create transaction with correct data', async () => {
    // 2. Define Mock Return Value
    const fakeTx = { id: '1', amount: 100 };
    (Transaction.create as any).mockResolvedValue(fakeTx);

    // 3. Call the function under test
    const result = await transactionService.createTransaction({ amount: 100 });

    // 4. Verify Behavior
    expect(Transaction.create).toHaveBeenCalledWith(
      expect.objectContaining({ amount: 100 })
    );
    expect(result).toEqual(fakeTx);
  });
});
```

## Migration Guide (Fixing Old Tests)

If you encounter a test using `sync({ force: true })`:

1. **Remove** the `sync` call.
2. **Identify** which Models are being accessed.
3. **Mock** those Models at the top of the test file.
4. **Replace** real DB calls with `mockResolvedValue`.
