---
name: typescript-advanced-types
description: Advanced TypeScript patterns including generics, conditional types, mapped types, and type inference
license: MIT
compatibility: opencode
metadata:
  category: language
  language: typescript
  level: advanced
---

## What I do

I provide expertise in advanced TypeScript patterns and type system features:

- **Generics & Constraints**: Complex generic patterns with multiple type parameters and constraints
- **Conditional Types**: Type-level logic using conditional types and distributive conditional types
- **Mapped Types**: Transformation types using mapped types and key remapping
- **Template Literal Types**: String manipulation at the type level
- **Utility Types**: Custom utility types and advanced usage of built-in utilities
- **Type Inference**: Advanced inference patterns with `infer` keyword
- **Discriminated Unions**: Type-safe state machines and exhaustive checking
- **Brand Types**: Nominal typing patterns for enhanced type safety

## When to use me

Load this skill when you need to:
- Implement complex type-safe APIs or libraries
- Create reusable utility types
- Build type-safe state management
- Ensure exhaustive pattern matching
- Implement dependency injection with strong typing
- Create branded/nominal types for domain primitives

## Best Practices

### 1. Dependency Injection Pattern
```typescript
// Define service interfaces
interface Logger {
  log(message: string): void;
}

interface Database {
  query<T>(sql: string): Promise<T>;
}

// Use constructor injection
class UserService {
  constructor(
    private readonly logger: Logger,
    private readonly db: Database
  ) {}
  
  async findUser(id: string) {
    this.logger.log(`Finding user ${id}`);
    return this.db.query<User>(`SELECT * FROM users WHERE id = $1`);
  }
}
```

### 2. Discriminated Unions for Type-Safe State
```typescript
type AsyncData<T, E = Error> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: E };

function handleData<T>(data: AsyncData<T>) {
  switch (data.status) {
    case 'idle':
      return 'No data yet';
    case 'loading':
      return 'Loading...';
    case 'success':
      return data.data; // TypeScript knows data exists here
    case 'error':
      return data.error.message; // TypeScript knows error exists here
  }
}
```

### 3. Branded Types for Domain Primitives
```typescript
type Brand<K, T> = K & { __brand: T };
type UserId = Brand<string, 'UserId'>;
type Email = Brand<string, 'Email'>;

const createUserId = (id: string): UserId => id as UserId;
const createEmail = (email: string): Email => {
  if (!email.includes('@')) throw new Error('Invalid email');
  return email as Email;
};

// This prevents mixing up primitives
function sendEmail(userId: UserId, email: Email) {
  // userId and email are both strings, but can't be mixed up
}
```

### 4. Advanced Generics with Constraints
```typescript
// Extract methods from a type
type Methods<T> = {
  [K in keyof T]: T[K] extends (...args: any[]) => any ? K : never;
}[keyof T];

// Create a type-safe builder pattern
class Builder<T extends Record<string, any>> {
  private data: Partial<T> = {};
  
  set<K extends keyof T>(key: K, value: T[K]): Builder<T> {
    this.data[key] = value;
    return this;
  }
  
  build(): T {
    return this.data as T;
  }
}
```

## Type Safety Principles

1. **Prefer `unknown` over `any`**: Force explicit type checking
2. **Use `readonly` by default**: Immutability prevents bugs
3. **Leverage `const` assertions**: For literal types and readonly tuples
4. **Enable strict mode**: `strict: true` in tsconfig.json
5. **Avoid type assertions**: Use type guards instead
6. **Use discriminated unions**: Instead of optional properties for state

## Common Patterns

### Result Type (Railway Oriented Programming)
```typescript
type Result<T, E = Error> =
  | { ok: true; value: T }
  | { ok: false; error: E };

const divide = (a: number, b: number): Result<number> =>
  b === 0
    ? { ok: false, error: new Error('Division by zero') }
    : { ok: true, value: a / b };
```

### Builder Pattern with Fluent API
```typescript
interface Config {
  host: string;
  port: number;
  ssl: boolean;
}

class ConfigBuilder {
  private config: Partial<Config> = {};
  
  host(host: string): this {
    this.config.host = host;
    return this;
  }
  
  port(port: number): this {
    this.config.port = port;
    return this;
  }
  
  ssl(enabled: boolean): this {
    this.config.ssl = enabled;
    return this;
  }
  
  build(): Config {
    if (!this.config.host || !this.config.port) {
      throw new Error('Missing required fields');
    }
    return this.config as Config;
  }
}
```

## References

- TypeScript Handbook: Advanced Types
- Effective TypeScript by Dan Vanderkam
- Type Challenges: github.com/type-challenges/type-challenges
