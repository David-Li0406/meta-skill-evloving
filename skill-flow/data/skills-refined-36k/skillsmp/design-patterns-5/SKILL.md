---
name: design-patterns
description: >-
  Architectural patterns for TypeScript/Node.js ecommerce project. Covers
  dependency injection, error handling, configuration, testing patterns.
  Triggers on "dependency injection", "DI pattern", "error handling",
  "architectural pattern", "design pattern", "testing pattern", "anti-pattern".
allowed-tools: Read
---

# ABOUTME: Architectural patterns skill for TypeScript ecommerce
# ABOUTME: Covers DI, error handling, testing, and common anti-patterns

# Design Patterns (Ecommerce)

Architectural patterns for the TypeScript/Node.js ecommerce stack.

## Quick Reference

| Pattern | Frontend (Next.js) | Backend (Fastify) |
|---------|-------------------|-------------------|
| DI | React Context | Constructor injection |
| Errors | Error boundaries | Fastify error handler |
| Config | env.local | dotenv + config module |
| State | React Query | In-memory + Redis |
| Testing | Testing Library | Testcontainers |

---

## 1. Dependency Injection

### Backend (Fastify)

```typescript
// Define interface
interface UserRepository {
  findById(id: string): Promise<User | null>;
  create(data: CreateUserDto): Promise<User>;
}

// Constructor injection
class UserService {
  constructor(
    private readonly userRepo: UserRepository,
    private readonly logger: Logger
  ) {}

  async getUser(id: string): Promise<User> {
    this.logger.info({ id }, 'Getting user');
    const user = await this.userRepo.findById(id);
    if (!user) throw new NotFoundError(`User ${id} not found`);
    return user;
  }
}

// Wire up in app
const userRepo = new PrismaUserRepository(prisma);
const userService = new UserService(userRepo, logger);
```

### Frontend (React Context)

```typescript
// Context for dependency injection
const CartContext = createContext<CartContextValue | null>(null);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [items, setItems] = useState<CartItem[]>([]);

  const addItem = useCallback((product: Product, quantity: number) => {
    setItems((prev) => [...prev, { product, quantity }]);
  }, []);

  return (
    <CartContext.Provider value={{ items, addItem }}>
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within CartProvider');
  return context;
}
```

---

## 2. Error Handling

### Backend (Fastify)

```typescript
// Custom error classes
class AppError extends Error {
  constructor(
    message: string,
    public statusCode: number = 500,
    public code: string = 'INTERNAL_ERROR'
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class NotFoundError extends AppError {
  constructor(message: string) {
    super(message, 404, 'NOT_FOUND');
  }
}

class ValidationError extends AppError {
  constructor(message: string) {
    super(message, 400, 'VALIDATION_ERROR');
  }
}

// Error handler middleware
function errorHandler(error: Error, request: FastifyRequest, reply: FastifyReply) {
  if (error instanceof AppError) {
    return reply.status(error.statusCode).send({
      statusCode: error.statusCode,
      error: error.code,
      message: error.message,
    });
  }

  // Log unexpected errors
  request.log.error(error);
  return reply.status(500).send({
    statusCode: 500,
    error: 'INTERNAL_ERROR',
    message: 'An unexpected error occurred',
  });
}
```

### Frontend (Error Boundaries)

```typescript
// Error boundary for React
class ErrorBoundary extends React.Component<Props, State> {
  state = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error) {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error('Error caught:', error, info);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback error={this.state.error} />;
    }
    return this.props.children;
  }
}

// React Query error handling
const { data, error } = useQuery({
  queryKey: ['products'],
  queryFn: fetchProducts,
  retry: 3,
  onError: (error) => {
    toast.error(error.message);
  },
});
```

---

## 3. Configuration

### Backend

```typescript
// config/index.ts
import { z } from 'zod';

const ConfigSchema = z.object({
  NODE_ENV: z.enum(['development', 'production', 'test']).default('development'),
  PORT: z.coerce.number().default(4000),
  DATABASE_URL: z.string(),
  REDIS_HOST: z.string().default('localhost'),
  REDIS_PORT: z.coerce.number().default(6379),
  JWT_SECRET: z.string(),
});

export type Config = z.infer<typeof ConfigSchema>;

export function loadConfig(): Config {
  const result = ConfigSchema.safeParse(process.env);
  if (!result.success) {
    console.error('Invalid configuration:', result.error.format());
    process.exit(1);
  }
  return result.data;
}

export const config = loadConfig();
```

### Frontend

```typescript
// next.config.js handles env
// Access via process.env.NEXT_PUBLIC_*

// For runtime config
const config = {
  apiUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000',
  environment: process.env.NODE_ENV,
};
```

---

## 4. Testing Patterns

### Prefer Real Over Mocks

```typescript
// GOOD: Real database with Testcontainers
describe('UserRepository', () => {
  let container: StartedPostgreSqlContainer;
  let prisma: PrismaClient;

  beforeAll(async () => {
    container = await new PostgreSqlContainer().start();
    prisma = new PrismaClient({
      datasources: { db: { url: container.getConnectionUri() } },
    });
  });

  afterAll(async () => {
    await prisma.$disconnect();
    await container.stop();
  });

  it('creates a user', async () => {
    const repo = new PrismaUserRepository(prisma);
    const user = await repo.create({ email: 'test@example.com' });
    expect(user.email).toBe('test@example.com');
  });
});

// BAD: Excessive mocking
it('creates a user', async () => {
  const mockPrisma = { user: { create: jest.fn().mockResolvedValue({ id: '1' }) } };
  // This tests mock behavior, not real behavior
});
```

### Test Behavior, Not Implementation

```typescript
// GOOD: Tests observable behavior
it('rejects invalid email', async () => {
  const response = await app.inject({
    method: 'POST',
    url: '/auth/register',
    payload: { email: 'invalid', password: 'secret123' },
  });
  expect(response.statusCode).toBe(400);
  expect(response.json()).toMatchObject({
    error: 'VALIDATION_ERROR',
  });
});

// BAD: Tests internal implementation
it('calls validateEmail function', async () => {
  const spy = jest.spyOn(validator, 'validateEmail');
  await register({ email: 'test@example.com' });
  expect(spy).toHaveBeenCalled(); // Who cares?
});
```

---

## 5. Common Anti-Patterns

### TypeScript

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `any` type | No type safety | Use `unknown` + guards |
| `// @ts-ignore` | Hidden bugs | Fix the type issue |
| Optional chaining abuse | Hides nulls | Explicit null checks |
| `as` casting | Runtime errors | Type guards |

### React

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Prop drilling | Coupling | Context or state lib |
| useEffect for data | Race conditions | React Query |
| Inline styles | No reuse | Tailwind classes |
| Index as key | Render bugs | Stable IDs |

### Fastify

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Sync in handlers | Blocks event loop | Always async |
| Global state | Race conditions | Inject dependencies |
| No validation | Security risk | Zod schemas |
| Catching all errors | Hides bugs | Let Fastify handle |

---

## 6. Naming Conventions

### Files

```
# Components: PascalCase
src/components/ProductCard.tsx
src/components/CartSummary.tsx

# Hooks: camelCase with use prefix
src/hooks/useProducts.ts
src/hooks/useCart.ts

# Modules: kebab-case
src/modules/auth/auth.routes.ts
src/modules/catalog/catalog.service.ts

# Types: PascalCase
src/types/Product.ts
src/types/Order.ts
```

### Variables

```typescript
// Constants: SCREAMING_SNAKE_CASE
const MAX_RETRIES = 3;
const DEFAULT_PAGE_SIZE = 20;

// Functions: camelCase
function calculateTotal(items: CartItem[]): number {}
async function fetchProducts(categoryId?: string): Promise<Product[]> {}

// Classes: PascalCase
class OrderService {}
class ProductRepository {}

// Interfaces: PascalCase (no I prefix)
interface User {}
interface CartItem {}
```

---

## Resources

See `references/typescript-patterns.md` for more detailed examples.
