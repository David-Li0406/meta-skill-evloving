---
name: majestic-monolith
description: Majestic monolith architecture pattern for modular, single-deployment applications
license: MIT
compatibility: opencode
metadata:
  category: architecture
  pattern: monolith
  deployment: single
---

## What I do

I provide guidance on building majestic monolith applications - single deployments with strong modular organization.

## When to use me

Load this skill when:
- Building a single-team application
- Need for ACID transactions across features
- Want simpler deployment and operations
- Have a shared domain model
- Team size < 20 developers
- Moderate scaling requirements

## Principles

### 1. Modular Organization
Organize code into modules with clear boundaries, even though it's a single deployment.

```
src/
├── modules/
│   ├── users/
│   │   ├── domain/          # Business logic
│   │   ├── application/     # Use cases
│   │   ├── infrastructure/  # DB, external APIs
│   │   └── presentation/    # API controllers
│   ├── products/
│   │   ├── domain/
│   │   ├── application/
│   │   ├── infrastructure/
│   │   └── presentation/
│   └── orders/
│       ├── domain/
│       ├── application/
│       ├── infrastructure/
│       └── presentation/
├── shared/                  # Shared utilities
│   ├── database/
│   ├── auth/
│   └── logging/
└── app.ts                   # Application entry
```

### 2. Clear Module Boundaries
Modules should communicate through well-defined interfaces.

```typescript
// ❌ Bad: Direct coupling
import { UserRepository } from '../users/infrastructure/UserRepository';

class OrderService {
  constructor() {
    this.userRepo = new UserRepository(); // Tight coupling!
  }
}

// ✅ Good: Interface-based dependency
interface UserService {
  findById(id: string): Promise<User | null>;
}

class OrderService {
  constructor(private readonly userService: UserService) {}
  
  async createOrder(userId: string, items: OrderItem[]) {
    const user = await this.userService.findById(userId);
    if (!user) throw new Error('User not found');
    // Create order
  }
}
```

### 3. Shared Database with Module Schemas
Use a single database but organize tables by module.

```sql
-- Users module schema
CREATE SCHEMA users;
CREATE TABLE users.users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Products module schema
CREATE SCHEMA products;
CREATE TABLE products.products (
  id UUID PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  price DECIMAL(10,2) NOT NULL
);

-- Orders module schema
CREATE SCHEMA orders;
CREATE TABLE orders.orders (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,  -- Foreign key to users.users
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 4. Dependency Direction
Dependencies should flow inward: Presentation → Application → Domain

```typescript
// Domain layer (no dependencies)
export class Order {
  constructor(
    public readonly id: string,
    public readonly userId: string,
    public readonly items: OrderItem[],
    public readonly status: OrderStatus
  ) {}
  
  // Business logic
  canCancel(): boolean {
    return this.status === 'pending' || this.status === 'confirmed';
  }
}

// Application layer (depends on domain)
export class CreateOrderUseCase {
  constructor(
    private readonly orderRepo: OrderRepository,
    private readonly userService: UserService
  ) {}
  
  async execute(input: CreateOrderInput): Promise<Order> {
    // Validate user exists
    const user = await this.userService.findById(input.userId);
    if (!user) throw new Error('User not found');
    
    // Create and save order
    const order = new Order(/* ... */);
    await this.orderRepo.save(order);
    return order;
  }
}

// Infrastructure layer (depends on application/domain)
export class PostgresOrderRepository implements OrderRepository {
  async save(order: Order): Promise<void> {
    await db.query(
      'INSERT INTO orders.orders (id, user_id, status) VALUES ($1, $2, $3)',
      [order.id, order.userId, order.status]
    );
  }
}

// Presentation layer (depends on application)
export class OrderController {
  constructor(private readonly createOrder: CreateOrderUseCase) {}
  
  async create(req: Request, res: Response) {
    const order = await this.createOrder.execute(req.body);
    res.status(201).json(order);
  }
}
```

## Advantages

1. **Simplicity**: Single codebase, single deployment
2. **ACID Transactions**: Strong consistency across modules
3. **Easier Debugging**: Centralized logs, single process
4. **Lower Latency**: In-process communication
5. **Simpler Operations**: One service to deploy and monitor
6. **Cost Effective**: Lower infrastructure costs

## Challenges

1. **Single Point of Failure**: Entire app goes down if one module fails
2. **Scaling Limits**: Must scale entire application
3. **Deployment Coordination**: All modules deploy together
4. **Module Coupling Risk**: Requires discipline to maintain boundaries

## Migration Path

When you outgrow the monolith:

1. **Identify module boundaries**: Already modular? Good!
2. **Extract module to service**: Start with least coupled module
3. **Introduce API gateway**: Route requests to appropriate service
4. **Migrate data**: Move module's tables to separate database
5. **Repeat**: Gradually extract more modules

## Tools & Patterns

### Module Registration
```typescript
// modules/index.ts
export function registerModules(app: Express) {
  // Each module registers its routes
  registerUserModule(app);
  registerProductModule(app);
  registerOrderModule(app);
}

// modules/users/index.ts
export function registerUserModule(app: Express) {
  const router = Router();
  
  // Dependency injection
  const userRepo = new PostgresUserRepository();
  const createUser = new CreateUserUseCase(userRepo);
  const controller = new UserController(createUser);
  
  router.post('/users', (req, res) => controller.create(req, res));
  
  app.use('/api', router);
}
```

### Dependency Injection Container
```typescript
// container.ts
export class Container {
  private services = new Map<string, any>();
  
  register<T>(key: string, factory: () => T): void {
    this.services.set(key, factory);
  }
  
  resolve<T>(key: string): T {
    const factory = this.services.get(key);
    if (!factory) throw new Error(`Service ${key} not found`);
    return factory();
  }
}

// setup.ts
const container = new Container();

// Register services
container.register('userRepository', () => new PostgresUserRepository());
container.register('createUser', () => 
  new CreateUserUseCase(container.resolve('userRepository'))
);

// Use in controllers
const createUser = container.resolve<CreateUserUseCase>('createUser');
```

### Event Bus for Module Communication
```typescript
// Decouple modules with events
interface DomainEvent {
  type: string;
  payload: any;
  timestamp: Date;
}

class EventBus {
  private handlers = new Map<string, Array<(event: DomainEvent) => void>>();
  
  subscribe(eventType: string, handler: (event: DomainEvent) => void): void {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, []);
    }
    this.handlers.get(eventType)!.push(handler);
  }
  
  publish(event: DomainEvent): void {
    const handlers = this.handlers.get(event.type) || [];
    handlers.forEach(handler => handler(event));
  }
}

// Usage
eventBus.subscribe('user.created', async (event) => {
  // Send welcome email
  await emailService.sendWelcome(event.payload.email);
});

// In user module
await userRepo.save(user);
eventBus.publish({
  type: 'user.created',
  payload: { userId: user.id, email: user.email },
  timestamp: new Date(),
});
```

## Best Practices

1. **Keep modules independent**: Minimize inter-module dependencies
2. **Use interfaces**: Define clear contracts between modules
3. **Avoid shared state**: Each module owns its data
4. **Test modules in isolation**: Unit tests shouldn't cross module boundaries
5. **Document module APIs**: Clear public interface for each module
6. **Monitor module performance**: Track which modules are slowest

## References

- "The Majestic Monolith" by David Heinemeier Hansson
- "Modular Monolith" architectural pattern
- Clean Architecture by Robert C. Martin
