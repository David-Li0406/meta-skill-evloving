---
name: Unit Testing
description: Generates consistent unit tests for Next.js API routes, services, and repositories using Vitest
---

# Unit Testing Skill

This skill provides patterns and guidelines for creating consistent unit tests in the golf-league application.

## Test Framework

- **Test Runner**: Vitest
- **Mocking**: Vitest's built-in `vi` API
- **Assertions**: Vitest's `expect` API
- **Environment**: Node.js (configured in `vitest.config.mjs`)

## File Naming Convention

- Place tests in the same directory as the code being tested
- Use `.test.ts` or `.test.tsx` extension
- Example: `route.ts` → `route.test.ts` or descriptive name like `mobile-auth.test.ts`

## Standard Test Structure

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { FunctionToTest } from './file-under-test';

// Mock external dependencies
vi.mock('@/external-module', () => ({
    externalFunction: vi.fn(),
}));

describe('Component/Feature Name', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    describe('functionName', () => {
        it('should handle success case', async () => {
            // Arrange
            const mockData = { id: '1', name: 'Test' };
            
            // Act
            const result = await FunctionToTest(input);
            
            // Assert
            expect(result).toEqual(mockData);
        });

        it('should handle error case', async () => {
            // Test error scenarios
        });
    });
});
```

## Testing Next.js API Routes

### Pattern for GET Requests

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { GET } from './route';

// Mock dependencies
vi.mock('@/lib/auth-utils', () => ({
    getAuthenticatedSession: vi.fn(),
}));

vi.mock('@/db', () => ({
    db: {
        select: vi.fn(),
    },
}));

// Helper for chained Drizzle select
const createSelectMock = (result: unknown[]) => {
    const from = vi.fn().mockResolvedValue(result);
    return { from };
};

describe('GET /api/resource', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should return resources successfully', async () => {
        const { getAuthenticatedSession } = await import('@/lib/auth-utils');
        const { db } = await import('@/db');
        
        vi.mocked(getAuthenticatedSession).mockResolvedValueOnce({
            user: { id: 'user-1' }
        } as never);

        const mockData = [{ id: '1', name: 'Item 1' }];
        vi.mocked(db.select).mockReturnValueOnce(createSelectMock(mockData) as never);

        const response = await GET();
        const data = await response.json();

        expect(response.status).toBe(200);
        expect(data).toEqual(mockData);
    });

    it('should return 401 if not authenticated', async () => {
        const { getAuthenticatedSession } = await import('@/lib/auth-utils');
        
        const authError = new Error('Unauthorized');
        authError.name = 'AuthError';
        vi.mocked(getAuthenticatedSession).mockRejectedValueOnce(authError);

        const response = await GET();
        expect(response.status).toBe(401);
    });

    it('should return 500 on database error', async () => {
        const { getAuthenticatedSession } = await import('@/lib/auth-utils');
        const { db } = await import('@/db');
        
        vi.mocked(getAuthenticatedSession).mockResolvedValueOnce({
            user: { id: 'user-1' }
        } as never);

        vi.mocked(db.select).mockReturnValueOnce({
            from: vi.fn().mockRejectedValueOnce(new Error('DB Error'))
        } as never);

        const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => { });
        const response = await GET();
        
        expect(response.status).toBe(500);
        consoleSpy.mockRestore();
    });
});
```

### Pattern for POST Requests

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { POST } from './route';

// Mock dependencies
vi.mock('@/lib/auth-utils', () => ({
    getAuthenticatedSession: vi.fn(),
}));

vi.mock('@/db', () => ({
    db: {
        insert: vi.fn(),
    },
}));

describe('POST /api/resource', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should create resource successfully', async () => {
        const { getAuthenticatedSession } = await import('@/lib/auth-utils');
        const { db } = await import('@/db');
        
        vi.mocked(getAuthenticatedSession).mockResolvedValueOnce({
            user: { id: 'user-1' }
        } as never);

        const mockCreated = { id: '1', name: 'New Item' };
        vi.mocked(db.insert).mockReturnValueOnce({
            values: vi.fn().mockReturnValueOnce({
                returning: vi.fn().mockResolvedValueOnce([mockCreated])
            })
        } as never);

        const req = new Request('http://localhost/api/resource', {
            method: 'POST',
            body: JSON.stringify({ name: 'New Item' }),
        });

        const response = await POST(req);
        const data = await response.json();

        expect(response.status).toBe(200);
        expect(data).toEqual(mockCreated);
    });

    it('should return 400 for missing required fields', async () => {
        const req = new Request('http://localhost/api/resource', {
            method: 'POST',
            body: JSON.stringify({}),
        });

        const response = await POST(req);
        const data = await response.json();

        expect(response.status).toBe(400);
        expect(data.error).toBeDefined();
    });
});
```

### Pattern for PUT/PATCH Requests

```typescript
it('should update resource successfully', async () => {
    const { db } = await import('@/db');
    
    const mockUpdated = { id: '1', name: 'Updated' };
    vi.mocked(db.update).mockReturnValueOnce({
        set: vi.fn().mockReturnValueOnce({
            where: vi.fn().mockReturnValueOnce({
                returning: vi.fn().mockResolvedValueOnce([mockUpdated])
            })
        })
    } as never);

    const req = new Request('http://localhost/api/resource', {
        method: 'PUT',
        body: JSON.stringify({ name: 'Updated' }),
    });

    const response = await PUT(req);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data).toEqual(mockUpdated);
});
```

## Drizzle ORM Mock Helpers

### Simple Select (returns array directly)

```typescript
const createSelectMock = (result: unknown[]) => {
    const from = vi.fn().mockResolvedValue(result);
    return { from };
};
```

### Select with Where Clause

```typescript
const createSelectWithWhereMock = (result: unknown[]) => {
    const where = vi.fn().mockResolvedValue(result);
    const from = vi.fn(() => ({ where }));
    return { from };
};
```

### Select with Where and Limit

```typescript
const createDetailSelectMock = (result: unknown[]) => {
    const limit = vi.fn().mockResolvedValue(result);
    const where = vi.fn(() => ({ limit }));
    const from = vi.fn(() => ({ where }));
    return { from };
};
```

### Complex Queries (with joins, orderBy, etc.)

```typescript
const createComplexSelectMock = (result: unknown[]) => {
    const orderBy = vi.fn().mockResolvedValue(result);
    const leftJoin = vi.fn(() => ({ orderBy }));
    const where = vi.fn(() => ({ leftJoin, orderBy }));
    const from = vi.fn(() => ({ where }));
    return { from };
};
```

## Testing Services and Repositories

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ServiceClass } from './service-under-test';

// Mock repository
vi.mock('@/db/repositories/example.repository', () => ({
    exampleRepository: {
        findById: vi.fn(),
        create: vi.fn(),
        update: vi.fn(),
    },
}));

describe('ServiceClass', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should call repository method correctly', async () => {
        const { exampleRepository } = await import('@/db/repositories/example.repository');
        const mockData = { id: '1', name: 'Test' };
        
        vi.mocked(exampleRepository.findById).mockResolvedValueOnce(mockData);

        const result = await ServiceClass.getById('1');

        expect(result).toEqual(mockData);
        expect(exampleRepository.findById).toHaveBeenCalledWith('1');
    });
});
```

## Essential Test Cases

Every API route should test:

1. **Success Case**: Happy path with valid data
2. **Authentication Error**: 401 when not authenticated (if protected)
3. **Authorization Error**: 403 when user lacks permission (if applicable)
4. **Validation Error**: 400 when required fields are missing
5. **Not Found**: 404 when resource doesn't exist (for detail routes)
6. **Server Error**: 500 when unexpected errors occur

## Console Error Handling

When testing error scenarios that log to console:

```typescript
const consoleSpy = vi.spyOn(console, 'error').mockImplementation(() => { });
// ... code that logs errors
expect(consoleSpy).toHaveBeenCalled();
consoleSpy.mockRestore();
```

## Dynamic Imports for Mocked Modules

Always use dynamic imports when accessing mocked modules:

```typescript
const { mockFunction } = await import('@/mocked-module');
vi.mocked(mockFunction).mockResolvedValue(result);
```

## Coverage Goals

- **Statements**: 80%+
- **Functions**: 80%+
- **Branches**: 80%+
- **Lines**: 80%+

Focus on testing critical business logic and error paths.
