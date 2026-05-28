# Test Data Reference for LucidData

Guide to test fixtures, mocks, and sample data used across the LucidData test suite.

## Table of Contents

1. [Fixture Structure](#fixture-structure)
2. [Sample User Data](#sample-user-data)
3. [Sample Vault Entries](#sample-vault-entries)
4. [Sample Consents](#sample-consents)
5. [Sample Audit Logs](#sample-audit-logs)
6. [Test User Credentials](#test-user-credentials)
7. [Data Generators](#data-generators)

## Fixture Structure

Fixtures are located in [`test/fixtures/`](../../../test/fixtures/) and provide reusable test data.

### Fixture Organization

```
test/fixtures/
├── users.ts          # User data
├── vault-data.ts     # Vault entries
├── consent-data.ts   # Consent records
├── audit-logs.ts     # Audit log entries
└── index.ts          # Re-exports all fixtures
```

### Import Patterns

```typescript
// Import specific fixtures
import { mockVaultEntry, createMockVaultEntries } from '@/test/fixtures/vault-data';
import { mockUser } from '@/test/fixtures/users';

// Import all fixtures
import * as fixtures from '@/test/fixtures';
```

## Sample User Data

### Mock User Object

```typescript
// test/fixtures/users.ts
export const mockUser = {
  id: 'user-123',
  supabaseId: 'supabase-user-123',
  email: 'test@lucid.dev',
  createdAt: new Date('2026-01-01T00:00:00Z'),
  updatedAt: new Date('2026-01-01T00:00:00Z'),
};

export const mockAdminUser = {
  id: 'admin-456',
  supabaseId: 'supabase-admin-456',
  email: 'admin@lucid.dev',
  createdAt: new Date('2026-01-01T00:00:00Z'),
  updatedAt: new Date('2026-01-01T00:00:00Z'),
};

export function createMockUser(overrides?: Partial<typeof mockUser>) {
  return {
    ...mockUser,
    ...overrides,
  };
}
```

### Usage

```typescript
it('should filter vault entries by user', async () => {
  const entries = createMockVaultEntries(3, mockUser.id);
  prismaMock.vaultData.findMany.mockResolvedValue(entries);

  const result = await repository.findByUserId(mockUser.id);

  expect(result).toHaveLength(3);
  expect(result.every((e) => e.userId === mockUser.id)).toBe(true);
});
```

## Sample Vault Entries

### Mock Vault Entry

```typescript
// test/fixtures/vault-data.ts
import { VaultData } from '@prisma/client';

export const mockVaultEntry: VaultData = {
  id: 'vault-1',
  userId: 'user-123',
  label: 'Passport',
  category: 'Identity',
  encryptedData: 'encrypted_base64_data_here',
  iv: 'initialization_vector_base64',
  tag: 'auth_tag_base64',
  encryptionKeyId: 'v2',
  metadata: null,
  createdAt: new Date('2026-01-05T10:00:00Z'),
  updatedAt: new Date('2026-01-05T10:00:00Z'),
};

export const mockVaultEntries: VaultData[] = [
  mockVaultEntry,
  {
    id: 'vault-2',
    userId: 'user-123',
    label: 'Driver License',
    category: 'Identity',
    encryptedData: 'encrypted_data_2',
    iv: 'iv_2',
    tag: 'tag_2',
    encryptionKeyId: 'v2',
    metadata: null,
    createdAt: new Date('2026-01-06T11:00:00Z'),
    updatedAt: new Date('2026-01-06T11:00:00Z'),
  },
  {
    id: 'vault-3',
    userId: 'user-123',
    label: 'Bank Account',
    category: 'Financial',
    encryptedData: 'encrypted_data_3',
    iv: 'iv_3',
    tag: 'tag_3',
    encryptionKeyId: 'v2',
    metadata: null,
    createdAt: new Date('2026-01-07T12:00:00Z'),
    updatedAt: new Date('2026-01-07T12:00:00Z'),
  },
];

// Factory function to create multiple vault entries
export function createMockVaultEntries(count: number, userId: string): VaultData[] {
  return Array.from({ length: count }, (_, i) => ({
    id: `vault-${i + 1}`,
    userId,
    label: `Entry ${i + 1}`,
    category: i % 2 === 0 ? 'Identity' : 'Financial',
    encryptedData: `encrypted_data_${i + 1}`,
    iv: `iv_${i + 1}`,
    tag: `tag_${i + 1}`,
    encryptionKeyId: 'v2',
    metadata: null,
    createdAt: new Date(`2026-01-${String(i + 1).padStart(2, '0')}T10:00:00Z`),
    updatedAt: new Date(`2026-01-${String(i + 1).padStart(2, '0')}T10:00:00Z`),
  }));
}

// Create vault entry with overrides
export function createMockVaultEntry(overrides?: Partial<VaultData>): VaultData {
  return {
    ...mockVaultEntry,
    ...overrides,
  };
}
```

### Usage

```typescript
it('should create vault entry', async () => {
  const input = {
    userId: mockUser.id,
    label: 'New Entry',
    category: 'Health',
    encryptedData: 'encrypted',
    iv: 'iv',
    tag: 'tag',
    encryptionKeyId: 'v2',
  };

  const mockCreated = createMockVaultEntry(input);
  prismaMock.vaultData.create.mockResolvedValue(mockCreated);

  const result = await repository.create(input);

  expect(result.label).toBe('New Entry');
  expect(result.category).toBe('Health');
});
```

## Sample Consents

### Mock Consent Data

```typescript
// test/fixtures/consent-data.ts
import { Consent } from '@prisma/client';

export const mockConsent: Consent = {
  id: 'consent-1',
  userId: 'user-123',
  vaultDataId: 'vault-1',
  grantedTo: 'buyer@example.com',
  purpose: 'Identity verification',
  accessLevel: 'READ',
  startDate: new Date('2026-01-01T00:00:00Z'),
  endDate: new Date('2026-12-31T23:59:59Z'),
  revokedAt: null,
  createdAt: new Date('2026-01-01T00:00:00Z'),
  updatedAt: new Date('2026-01-01T00:00:00Z'),
};

export const mockRevokedConsent: Consent = {
  ...mockConsent,
  id: 'consent-2',
  revokedAt: new Date('2026-06-01T10:00:00Z'),
};

export const mockExpiredConsent: Consent = {
  ...mockConsent,
  id: 'consent-3',
  endDate: new Date('2025-12-31T23:59:59Z'), // Expired
};

export function createMockConsents(count: number, userId: string): Consent[] {
  return Array.from({ length: count }, (_, i) => ({
    id: `consent-${i + 1}`,
    userId,
    vaultDataId: `vault-${i + 1}`,
    grantedTo: `buyer${i + 1}@example.com`,
    purpose: `Purpose ${i + 1}`,
    accessLevel: i % 2 === 0 ? 'READ' : 'EXPORT',
    startDate: new Date('2026-01-01T00:00:00Z'),
    endDate: new Date('2026-12-31T23:59:59Z'),
    revokedAt: i % 3 === 0 ? new Date('2026-06-01T00:00:00Z') : null,
    createdAt: new Date(`2026-01-${String(i + 1).padStart(2, '0')}T00:00:00Z`),
    updatedAt: new Date(`2026-01-${String(i + 1).padStart(2, '0')}T00:00:00Z`),
  }));
}

export function createMockConsent(overrides?: Partial<Consent>): Consent {
  return {
    ...mockConsent,
    ...overrides,
  };
}
```

### Usage

```typescript
it('should filter active consents', async () => {
  const consents = [
    mockConsent, // Active
    mockRevokedConsent, // Revoked
    mockExpiredConsent, // Expired
  ];

  prismaMock.consent.findMany.mockResolvedValue(consents);

  const result = await consentService.getActiveConsents(mockUser.id);

  expect(result).toHaveLength(1);
  expect(result[0].id).toBe('consent-1');
});
```

## Sample Audit Logs

### Mock Audit Log Data

```typescript
// test/fixtures/audit-logs.ts
import { AuditLog } from '@prisma/client';

export const mockAuditLog: AuditLog = {
  id: 'audit-1',
  userId: 'user-123',
  eventType: 'DATA_CREATED',
  entityType: 'VaultData',
  entityId: 'vault-1',
  actorType: 'user',
  actorId: 'user-123',
  metadata: { label: 'Passport', category: 'Identity' },
  ipAddress: '192.168.1.1',
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
  previousHash: null,
  currentHash: 'hash_of_current_entry',
  createdAt: new Date('2026-01-05T10:00:00Z'),
};

export const mockAuditLogChain: AuditLog[] = [
  mockAuditLog,
  {
    id: 'audit-2',
    userId: 'user-123',
    eventType: 'DATA_UPDATED',
    entityType: 'VaultData',
    entityId: 'vault-1',
    actorType: 'user',
    actorId: 'user-123',
    metadata: { updated_fields: ['label'] },
    ipAddress: '192.168.1.1',
    userAgent: 'Mozilla/5.0',
    previousHash: 'hash_of_current_entry', // Links to audit-1
    currentHash: 'new_hash_after_update',
    createdAt: new Date('2026-01-05T11:00:00Z'),
  },
];

export function createMockAuditLogs(count: number, userId: string): AuditLog[] {
  let previousHash: string | null = null;

  return Array.from({ length: count }, (_, i) => {
    const currentHash = `hash_${i + 1}`;
    const log: AuditLog = {
      id: `audit-${i + 1}`,
      userId,
      eventType: i % 2 === 0 ? 'DATA_CREATED' : 'DATA_UPDATED',
      entityType: 'VaultData',
      entityId: `vault-${i + 1}`,
      actorType: 'user',
      actorId: userId,
      metadata: null,
      ipAddress: '192.168.1.1',
      userAgent: 'Mozilla/5.0',
      previousHash,
      currentHash,
      createdAt: new Date(`2026-01-${String(i + 1).padStart(2, '0')}T10:00:00Z`),
    };

    previousHash = currentHash; // Chain to next log
    return log;
  });
}

export function createMockAuditLog(overrides?: Partial<AuditLog>): AuditLog {
  return {
    ...mockAuditLog,
    ...overrides,
  };
}
```

### Usage

```typescript
it('should verify hash chain integrity', () => {
  const logs = createMockAuditLogs(5, mockUser.id);

  const isValid = verifyHashChain(logs);

  expect(isValid).toBe(true);
});
```

## Test User Credentials

### E2E Test Users

```typescript
// __tests__/e2e/helpers/auth.ts
export const TEST_USER = {
  email: 'test@lucid.dev',
  password: 'TestPassword123!',
};

export const TEST_ADMIN = {
  email: 'admin@lucid.dev',
  password: 'AdminPassword123!',
};

export function getUniqueEmail(): string {
  const timestamp = Date.now();
  const random = Math.floor(Math.random() * 1000);
  return `test-${timestamp}-${random}@lucid.dev`;
}
```

### Usage in E2E Tests

```typescript
test('should login with test credentials', async ({ page }) => {
  await page.goto('/login');
  await page.fill('input[name="email"]', TEST_USER.email);
  await page.fill('input[name="password"]', TEST_USER.password);
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/dashboard');
});

test('should create account with unique email', async ({ page }) => {
  const email = getUniqueEmail();

  await page.goto('/signup');
  await page.fill('input[name="email"]', email);
  await page.fill('input[name="password"]', 'NewUser123!');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/dashboard');
});
```

## Data Generators

### E2E Data Generators

```typescript
// __tests__/e2e/helpers/data-generators.ts

export function randomString(length: number = 8): string {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  return Array.from({ length }, () => chars[Math.floor(Math.random() * chars.length)]).join('');
}

export function randomCategory(): string {
  const categories = ['Identity', 'Financial', 'Health', 'Contact', 'Employment', 'Education'];
  return categories[Math.floor(Math.random() * categories.length)];
}

export function generateVaultEntry(overrides?: Partial<any>) {
  return {
    label: `Entry ${randomString(6)}`,
    category: randomCategory(),
    metadata: {
      description: `Test data ${randomString(10)}`,
      tags: ['test', 'generated'],
    },
    ...overrides,
  };
}

export function generateConsent(overrides?: Partial<any>) {
  return {
    grantedTo: `buyer-${randomString(8)}@example.com`,
    purpose: `Test purpose ${randomString(10)}`,
    accessLevel: Math.random() > 0.5 ? 'READ' : 'EXPORT',
    startDate: new Date().toISOString(),
    endDate: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000).toISOString(), // 1 year
    ...overrides,
  };
}

export function generateVaultEntries(count: number) {
  return Array.from({ length: count }, () => generateVaultEntry());
}
```

### Usage in E2E Tests

```typescript
test('should create multiple vault entries', async ({ page }) => {
  await login(page);
  await page.goto('/dashboard/vault');

  const entries = generateVaultEntries(3);

  for (const entry of entries) {
    await page.click('button:has-text("Create Entry")');
    await page.fill('input[name="label"]', entry.label);
    await page.selectOption('select[name="category"]', entry.category);
    await page.fill('textarea[name="metadata"]', JSON.stringify(entry.metadata));
    await page.click('button:has-text("Save")');

    await expect(page.locator(`text=${entry.label}`)).toBeVisible();
  }
});
```

## Environment-Specific Data

### Test Environment Variables

Located in `.env.test`:

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321
SUPABASE_SERVICE_ROLE_KEY=<test-service-role-key>

# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:54322/postgres

# Encryption
ENCRYPTION_KEY=eugsb9sWIyEOcEg5AzHazv0k7CMTjSsGfL1lbLp8duU=

# App
NEXT_PUBLIC_APP_URL=http://localhost:3000
NODE_ENV=test
```

**Important**: These are test-only credentials. Never use production keys in tests.

## Best Practices

### 1. Use Factories for Flexibility

```typescript
// Good: Factory function allows customization
const entry = createMockVaultEntry({ label: 'Custom Label' });

// Less flexible: Hard-coded mock
const entry = mockVaultEntry; // Always the same data
```

### 2. Keep Test Data Realistic

```typescript
// Good: Realistic test data
const entry = {
  label: 'Passport',
  category: 'Identity',
  metadata: { issueDate: '2020-01-15', expiryDate: '2030-01-15' },
};

// Bad: Meaningless test data
const entry = {
  label: 'test',
  category: 'test',
  metadata: { foo: 'bar' },
};
```

### 3. Never Use Real PII

```typescript
// Good: Synthetic data
const user = { email: 'test@lucid.dev', name: 'Test User' };

// Bad: Real user data
const user = { email: 'john.doe@gmail.com', name: 'John Doe' };
```

### 4. Clean Up Generated Data

```typescript
test.afterEach(async () => {
  // Delete test data created with generators
  await deleteTestData();
});
```

### 5. Use Consistent Timestamps

```typescript
// Good: Fixed timestamps for predictable tests
const entry = {
  createdAt: new Date('2026-01-01T00:00:00Z'),
  updatedAt: new Date('2026-01-01T00:00:00Z'),
};

// Avoid: Current timestamp (tests become flaky)
const entry = {
  createdAt: new Date(),
  updatedAt: new Date(),
};
```

## Quick Reference

| Data Type | Location | Import |
|-----------|----------|--------|
| Mock User | `test/fixtures/users.ts` | `import { mockUser } from '@/test/fixtures/users'` |
| Mock Vault Entry | `test/fixtures/vault-data.ts` | `import { mockVaultEntry } from '@/test/fixtures/vault-data'` |
| Mock Consent | `test/fixtures/consent-data.ts` | `import { mockConsent } from '@/test/fixtures/consent-data'` |
| Mock Audit Log | `test/fixtures/audit-logs.ts` | `import { mockAuditLog } from '@/test/fixtures/audit-logs'` |
| Test Credentials | `__tests__/e2e/helpers/auth.ts` | `import { TEST_USER } from '@/__tests__/e2e/helpers/auth'` |
| Data Generators | `__tests__/e2e/helpers/data-generators.ts` | `import { generateVaultEntry } from '@/__tests__/e2e/helpers/data-generators'` |

---

**For more information:**
- [Playwright Patterns](playwright-patterns.md)
- [Vitest Patterns](vitest-patterns.md)
- [Main Skill Documentation](../SKILL.md)
