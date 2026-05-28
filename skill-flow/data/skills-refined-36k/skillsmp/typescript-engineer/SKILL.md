---
name: typescript-engineer
description: Expert TypeScript engineering with advanced patterns, architectural design, performance optimization, testing strategies, and production-grade code quality. Use when building scalable TypeScript applications, implementing complex type systems, optimizing performance, designing maintainable architectures, or when the user asks for TypeScript engineering excellence, advanced patterns, or professional-grade code practices.
---

# World Class TypeScript Engineer

## Quick Start

Apply these principles for production-grade TypeScript:

1. **Type Safety First**: Leverage advanced types, utility types, and type-level programming
2. **Architecture Matters**: Design for scalability, maintainability, and testability
3. **Performance Conscious**: Optimize bundle size, runtime performance, and developer experience
4. **Error Resilience**: Implement comprehensive error handling with typed error boundaries
5. **Testing Strategy**: Write testable code with proper abstractions and mocking
6. **Developer Experience**: Prioritize ergonomics, autocomplete, and debugging support

## Core Philosophy

TypeScript is a language for building **maintainable systems at scale**. Every design decision should consider:

- **Type safety** prevents runtime errors before deployment
- **Modularity** enables independent development and testing
- **Performance** ensures production readiness
- **Developer experience** accelerates development velocity

## Advanced Type Patterns

### Utility Types Mastery

Use TypeScript's built-in utility types effectively:

```typescript
// Partial<T> - All properties optional
type UpdateUserDto = Partial<User>;

// Pick<T, K> - Select specific properties
type UserPublic = Pick<User, 'id' | 'name' | 'email'>;

// Omit<T, K> - Exclude specific properties
type UserWithoutPassword = Omit<User, 'password' | 'salt'>;

// Record<K, V> - Map keys to values
type RolePermissions = Record<UserRole, Permission[]>;

// Extract<T, U> - Extract union members matching type
type StringKeys = Extract<keyof User, string>;

// Exclude<T, U> - Exclude union members matching type
type NonMethodKeys = Exclude<keyof User, Function>;
```

### Conditional Types

Use conditional types for type-level logic:

```typescript
// Conditional return types based on input
type ApiResponse<T> = T extends Error 
  ? { error: true; message: string }
  : { error: false; data: T };

// Extract promise type
type UnwrapPromise<T> = T extends Promise<infer U> ? U : T;

// Deep readonly
type DeepReadonly<T> = {
  readonly [P in keyof T]: T[P] extends object ? DeepReadonly<T[P]> : T[P];
};
```

### Template Literal Types

Leverage template literal types for type-safe string manipulation:

```typescript
// Type-safe API routes
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type ApiRoute = `/api/${string}`;
type FullRoute = `${HttpMethod} ${ApiRoute}`;

// Type-safe CSS classes
type ComponentSize = 'sm' | 'md' | 'lg';
type ComponentVariant = 'primary' | 'secondary' | 'danger';
type ButtonClass = `btn-${ComponentSize}-${ComponentVariant}`;
```

### Branded Types & Newtype Pattern

Prevent primitive type confusion:

```typescript
// Branded types for type safety
type UserId = string & { readonly __brand: unique symbol };
type ProductId = string & { readonly __brand: unique symbol };

function createUserId(id: string): UserId {
  return id as UserId;
}

// Usage prevents mixing up IDs
function fetchUser(id: UserId): Promise<User> {
  // Type system prevents passing ProductId
}
```

## Architecture Patterns

### Dependency Injection

Design for testability with explicit dependencies:

```typescript
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

interface EmailService {
  send(to: string, subject: string, body: string): Promise<void>;
}

class UserService {
  constructor(
    private readonly userRepo: UserRepository,
    private readonly emailService: EmailService
  ) {}

  async registerUser(email: string): Promise<User> {
    const user = await this.userRepo.save({ email });
    await this.emailService.send(email, 'Welcome', '...');
    return user;
  }
}
```

### Result Type Pattern

Replace exceptions with explicit error handling:

```typescript
type Result<T, E = Error> = 
  | { success: true; data: T }
  | { success: false; error: E };

async function fetchUser(id: string): Promise<Result<User, 'NOT_FOUND' | 'NETWORK_ERROR'>> {
  try {
    const user = await api.get(`/users/${id}`);
    return { success: true, data: user };
  } catch (error) {
    return { success: false, error: 'NOT_FOUND' };
  }
}

// Usage forces explicit error handling
const result = await fetchUser('123');
if (result.success) {
  console.log(result.data.email);
} else {
  console.error(result.error);
}
```

### Repository Pattern

Abstract data access for flexibility:

```typescript
interface Repository<T, ID = string> {
  findById(id: ID): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: ID): Promise<void>;
}

class InMemoryUserRepository implements Repository<User> {
  private users = new Map<string, User>();
  
  async findById(id: string): Promise<User | null> {
    return this.users.get(id) ?? null;
  }
  
  // ... other methods
}

// Easy to swap implementations
const userRepo: Repository<User> = new InMemoryUserRepository();
// Later: const userRepo = new PostgresUserRepository();
```

## Performance Optimization

### Bundle Size Optimization

Minimize bundle size impact:

```typescript
// Use tree-shaking friendly exports
export { specificFunction } from './utils';
// Avoid: export * from './utils';

// Lazy load heavy dependencies
const loadHeavyLibrary = async () => {
  const { HeavyLibrary } = await import('./heavy-library');
  return HeavyLibrary;
};

// Use const enums for compile-time inlining
const enum Status {
  Active = 1,
  Inactive = 2,
}
```

### Runtime Performance

Optimize hot paths:

```typescript
// Memoize expensive computations
function memoize<Args extends unknown[], Return>(
  fn: (...args: Args) => Return
): (...args: Args) => Return {
  const cache = new Map<string, Return>();
  return (...args: Args) => {
    const key = JSON.stringify(args);
    if (!cache.has(key)) {
      cache.set(key, fn(...args));
    }
    return cache.get(key)!;
  };
}

// Batch operations
async function batchProcess<T>(
  items: T[],
  batchSize: number,
  processor: (batch: T[]) => Promise<void>
): Promise<void> {
  for (let i = 0; i < items.length; i += batchSize) {
    await processor(items.slice(i, i + batchSize));
  }
}
```

## Error Handling

### Typed Error Boundaries

Define domain-specific error types:

```typescript
class DomainError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

class NotFoundError extends DomainError {
  constructor(resource: string) {
    super(`${resource} not found`, 'NOT_FOUND', 404);
  }
}

class ValidationError extends DomainError {
  constructor(message: string, public readonly fields: string[]) {
    super(message, 'VALIDATION_ERROR', 400);
  }
}

// Type-safe error handling
function handleError(error: unknown): DomainError {
  if (error instanceof DomainError) {
    return error;
  }
  return new DomainError('Internal server error', 'INTERNAL_ERROR');
}
```

### Error Recovery

Implement graceful degradation:

```typescript
async function fetchWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
  delay = 1000
): Promise<Result<T, Error>> {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const data = await fn();
      return { success: true, data };
    } catch (error) {
      if (attempt === maxRetries - 1) {
        return { success: false, error: error as Error };
      }
      await new Promise(resolve => setTimeout(resolve, delay * (attempt + 1)));
    }
  }
  return { success: false, error: new Error('Max retries exceeded') };
}
```

## Testing Strategy

### Testable Design

Write code that's easy to test:

```typescript
// Separate pure functions from side effects
// Pure function - easy to test
function calculateTotal(items: LineItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

// Side effect - inject dependencies for testing
class OrderService {
  constructor(
    private readonly taxCalculator: TaxCalculator,
    private readonly logger: Logger
  ) {}
  
  async processOrder(order: Order): Promise<void> {
    const tax = this.taxCalculator.calculate(order);
    this.logger.info(`Processing order with tax: ${tax}`);
    // ... process order
  }
}
```

### Test Utilities

Create reusable test helpers:

```typescript
// Test utilities
export function createMockRepository<T>(
  initialData: T[] = []
): Repository<T> {
  const data = new Map<string, T>();
  initialData.forEach(item => {
    data.set((item as any).id, item);
  });
  
  return {
    findById: async (id: string) => data.get(id) ?? null,
    findAll: async () => Array.from(data.values()),
    save: async (entity: T) => {
      const id = (entity as any).id;
      data.set(id, entity);
      return entity;
    },
    delete: async (id: string) => {
      data.delete(id);
    },
  };
}
```

## Code Organization

### Feature-Based Structure

Organize by feature, not by file type:

```
src/
├── features/
│   ├── users/
│   │   ├── user.entity.ts
│   │   ├── user.repository.ts
│   │   ├── user.service.ts
│   │   ├── user.controller.ts
│   │   └── index.ts
│   └── orders/
│       └── ...
├── shared/
│   ├── types/
│   ├── utils/
│   └── errors/
└── infrastructure/
    ├── database/
    └── http/
```

### Barrel Exports

Use index files for clean imports:

```typescript
// features/users/index.ts
export { User } from './user.entity';
export { UserRepository } from './user.repository';
export { UserService } from './user.service';
export type { UserDto, CreateUserDto } from './user.types';

// Usage
import { UserService, User, CreateUserDto } from '@/features/users';
```

## Developer Experience

### Type-Safe Configuration

Make configuration errors compile-time errors:

```typescript
interface AppConfig {
  database: {
    host: string;
    port: number;
  };
  api: {
    baseUrl: string;
    timeout: number;
  };
}

function loadConfig(): AppConfig {
  const config = {
    database: {
      host: process.env.DB_HOST ?? (() => {
        throw new Error('DB_HOST is required');
      })(),
      port: Number(process.env.DB_PORT ?? 5432),
    },
    api: {
      baseUrl: process.env.API_BASE_URL!,
      timeout: Number(process.env.API_TIMEOUT ?? 5000),
    },
  };
  
  // Type system ensures all required fields are present
  return config satisfies AppConfig;
}
```

### JSDoc for Better DX

Enhance IDE experience with JSDoc:

```typescript
/**
 * Calculates the total price including tax.
 * 
 * @param items - Array of line items with price and quantity
 * @param taxRate - Tax rate as a decimal (e.g., 0.08 for 8%)
 * @returns Total price including tax
 * 
 * @example
 * ```ts
 * const total = calculateTotalWithTax(
 *   [{ price: 10, quantity: 2 }],
 *   0.08
 * ); // Returns 21.6
 * ```
 */
function calculateTotalWithTax(
  items: Array<{ price: number; quantity: number }>,
  taxRate: number
): number {
  const subtotal = items.reduce((sum, item) => sum + item.price * item.quantity, 0);
  return subtotal * (1 + taxRate);
}
```

### Linting with Biome

Use Biome for fast, integrated linting and formatting:

**Installation:**
```bash
npm install --save-dev @biomejs/biome
```

**Configuration (`biome.json`):**
```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "correctness": {
        "noUnusedVariables": "error",
        "useExhaustiveDependencies": "warn"
      },
      "style": {
        "useImportType": "error",
        "useConst": "error",
        "noParameterAssign": "error"
      },
      "suspicious": {
        "noExplicitAny": "error",
        "noArrayIndexKey": "warn",
        "noAssignInExpressions": "error"
      },
      "performance": {
        "noDelete": "error"
      },
      "complexity": {
        "noForEach": "off",
        "useSimplifiedLogicExpression": "warn"
      }
    }
  },
  "formatter": {
    "enabled": true,
    "formatWithErrors": false,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100,
    "lineEnding": "lf",
    "ignore": ["node_modules", "dist", "build"]
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "jsxQuoteStyle": "double",
      "trailingCommas": "es5",
      "semicolons": "always",
      "arrowParentheses": "always"
    }
  },
  "overrides": [
    {
      "include": ["*.test.ts", "*.spec.ts"],
      "linter": {
        "rules": {
          "suspicious": {
            "noExplicitAny": "off"
          }
        }
      }
    }
  ]
}
```

**Package.json scripts:**
```json
{
  "scripts": {
    "lint": "biome lint .",
    "lint:fix": "biome lint --write .",
    "format": "biome format --write .",
    "check": "biome check .",
    "check:fix": "biome check --write ."
  }
}
```

**Key Benefits:**
- Single tool for linting and formatting (replaces ESLint + Prettier)
- Extremely fast (written in Rust)
- Zero configuration by default
- TypeScript-first support
- Organizes imports automatically

**VS Code Integration:**
```json
// .vscode/settings.json
{
  "[typescript]": {
    "editor.defaultFormatter": "biomejs.biome",
    "editor.formatOnSave": true
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "biomejs.biome",
    "editor.formatOnSave": true
  },
  "editor.codeActionsOnSave": {
    "quickfix.biome": "explicit",
    "source.organizeImports.biome": "explicit"
  }
}
```

For detailed Biome configuration and rule customization, see [references/biome.md](references/biome.md).

## Additional Resources

- **Advanced Patterns**: See [references/advanced-patterns.md](references/advanced-patterns.md) for template literal types, recursive types, and type-level computation
- **Architecture**: See [references/architecture.md](references/architecture.md) for detailed architectural patterns and design decisions
- **Performance**: See [references/performance.md](references/performance.md) for bundle optimization, runtime performance, and profiling techniques
- **Testing**: See [references/testing.md](references/testing.md) for testing strategies, mocking patterns, and test organization
- **Biome**: See [references/biome.md](references/biome.md) for comprehensive Biome linting and formatting configuration
