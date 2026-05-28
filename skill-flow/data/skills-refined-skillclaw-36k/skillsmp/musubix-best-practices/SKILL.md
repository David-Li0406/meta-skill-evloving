---
name: musubix-best-practices
description: Guide for applying MUSUBIX's 17 learned best practices. Use this when asked about coding patterns, design patterns, or testing patterns that MUSUBIX recommends.
license: MIT
---

# MUSUBIX Best Practices Skill

This skill guides you through applying the 17 best practices learned from MUSUBIX virtual projects.

## Overview

MUSUBIX has learned these best practices from implementing 14+ virtual projects. Apply them consistently for high-quality code.

## Code Patterns (5)

### BP-CODE-001: Entity Input DTO

Use Input DTO objects for entity creation instead of multiple parameters.

```typescript
// ✅ Recommended: Input DTO
interface CreatePetInput {
  name: string;
  species: string;
  ownerId: string;
}

function createPet(input: CreatePetInput): Pet {
  return new Pet(input);
}

// ❌ Avoid: Multiple parameters
function createPet(name: string, species: string, ownerId: string): Pet {
  // Hard to extend, easy to mix up parameter order
}
```

### BP-CODE-002: Date-based ID Format

Generate IDs with PREFIX-YYYYMMDD-NNN format for sortability.

```typescript
// ✅ Recommended: Date-based ID
const id = `PET-20260104-001`;  // Sortable, traceable

// ❌ Avoid: UUID only
const id = crypto.randomUUID();  // Not human-readable
```

### BP-CODE-003: Value Objects

Use Value Objects for domain concepts.

```typescript
// ✅ Recommended: Value Object
interface Price {
  readonly amount: number;
  readonly currency: 'JPY';
}

// ❌ Avoid: Primitive types
const price: number = 1000;  // No currency context
```

### BP-CODE-004: Function-based Value Objects

Use interface + factory function instead of classes for Value Objects.

```typescript
// ✅ Recommended: Interface + Factory Function
interface Price {
  readonly amount: number;
  readonly currency: 'JPY';
}

function createPrice(amount: number): Result<Price, ValidationError> {
  if (amount < 100 || amount > 1_000_000) {
    return err(new ValidationError('Price must be between 100 and 1,000,000 JPY'));
  }
  return ok({ amount, currency: 'JPY' });
}

// ❌ Avoid: Class-based (doesn't work well with TypeScript structural typing)
class Price {
  private constructor(readonly amount: number) {}
  static create(amount: number): Price { ... }
}
```

### BP-CODE-005: Result Type

Use Result<T, E> for operations that can fail.

```typescript
// ✅ Recommended: Result type
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

function divide(a: number, b: number): Result<number, Error> {
  if (b === 0) return { ok: false, error: new Error('Division by zero') };
  return { ok: true, value: a / b };
}

// ❌ Avoid: Throwing exceptions for expected errors
function divide(a: number, b: number): number {
  if (b === 0) throw new Error('Division by zero');
  return a / b;
}
```

## Design Patterns (7)

### BP-DESIGN-001: Status Transition Map

Define valid status transitions in a Map.

```typescript
// ✅ Recommended: Transition map
const validTransitions: Record<Status, Status[]> = {
  draft: ['active', 'cancelled'],
  active: ['completed', 'cancelled'],
  completed: [],
  cancelled: [],
};

function canTransition(from: Status, to: Status): boolean {
  return validTransitions[from].includes(to);
}
```

### BP-DESIGN-002: Repository Async Pattern

Make repositories async for future DB migration.

```typescript
// ✅ Recommended: Async repository
interface PetRepository {
  findById(id: PetId): Promise<Pet | null>;
  save(pet: Pet): Promise<void>;
}

// ❌ Avoid: Sync repository (hard to migrate later)
interface PetRepository {
  findById(id: PetId): Pet | null;
}
```

### BP-DESIGN-003: Service Layer with DI

Use dependency injection for services.

```typescript
// ✅ Recommended: Constructor DI
class PetService {
  constructor(
    private readonly petRepository: PetRepository,
    private readonly auditService: AuditService
  ) {}
}
```

### BP-DESIGN-004: Optimistic Locking

Use version field for concurrent edit detection.

```typescript
// ✅ Recommended: Version field
interface Entity {
  id: string;
  version: number;
  updatedAt: Date;
}

function update(entity: Entity, currentVersion: number): Result<Entity, ConcurrencyError> {
  if (entity.version !== currentVersion) {
    return err(new ConcurrencyError('Entity was modified'));
  }
  return ok({ ...entity, version: entity.version + 1 });
}
```

### BP-DESIGN-005: AuditService

Record data changes in audit logs.

```typescript
// ✅ Recommended: Audit logging
interface AuditEntry {
  id: string;
  entityType: string;
  entityId: string;
  action: 'CREATE' | 'UPDATE' | 'DELETE';
  changes: object;
  userId: string;
  timestamp: Date;
}
```

### BP-DESIGN-006: Entity Counter Reset

Provide reset functions for test isolation.

```typescript
// ✅ Recommended: Resettable counter
let petCounter = 0;

export function generatePetId(): string {
  return `PET-${Date.now()}-${++petCounter}`;
}

export function resetPetCounter(): void {
  petCounter = 0;  // For tests
}
```

### BP-DESIGN-007: Expiry Time Logic

Use expiresAt field for time-limited entities.

```typescript
// ✅ Recommended: Explicit expiry
interface Reservation {
  id: string;
  createdAt: Date;
  expiresAt: Date;  // Explicit expiry time
}

function isExpired(reservation: Reservation): boolean {
  return new Date() > reservation.expiresAt;
}
```

## Test Patterns (5)

### BP-TEST-001: Test Counter Reset

Reset ID counters in beforeEach.

```typescript
beforeEach(() => {
  resetPetCounter();
  resetReservationCounter();
});
```

### BP-TEST-002: Verify API Before Test

Check method signatures before writing tests.

### BP-TEST-003: Vitest ESM Configuration

Use proper ESM setup for Vitest.

```typescript
// vitest.config.ts
export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
  },
});
```

### BP-TEST-004: Result Type Test Pattern

Test both success and error cases.

```typescript
it('should succeed with valid input', () => {
  const result = createPrice(1000);
  expect(result.isOk()).toBe(true);
});

it('should fail with invalid input', () => {
  const result = createPrice(-1);
  expect(result.isErr()).toBe(true);
});
```

### BP-TEST-005: Status Transition Testing

Test all valid and invalid transitions.

```typescript
describe('status transitions', () => {
  it.each([
    ['draft', 'active', true],
    ['draft', 'completed', false],
    ['active', 'completed', true],
  ])('%s -> %s should be %s', (from, to, valid) => {
    expect(canTransition(from, to)).toBe(valid);
  });
});
```

## CLI Commands

```bash
# Show all best practices
npx musubix learn best-practices

# Filter by category
npx musubix learn best-practices --category code
npx musubix learn best-practices --category design
npx musubix learn best-practices --category test

# High confidence only
npx musubix learn best-practices --high-confidence
```

## Related Skills

- `musubix-code-generation` - Apply patterns in code
- `musubix-test-generation` - Apply test patterns
- `musubix-sdd-workflow` - Full workflow with patterns
