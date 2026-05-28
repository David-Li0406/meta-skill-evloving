# ABOUTME: TypeScript patterns for ecommerce architecture
# ABOUTME: Covers advanced DI, repository pattern, and service layer

# TypeScript Architectural Patterns

Advanced patterns for ecommerce TypeScript codebase.

---

## Repository Pattern

### Interface

```typescript
// repositories/interfaces.ts
export interface Repository<T, CreateDto, UpdateDto> {
  findById(id: string): Promise<T | null>;
  findMany(filter?: Partial<T>): Promise<T[]>;
  create(data: CreateDto): Promise<T>;
  update(id: string, data: UpdateDto): Promise<T>;
  delete(id: string): Promise<void>;
}

export interface UserRepository extends Repository<User, CreateUserDto, UpdateUserDto> {
  findByEmail(email: string): Promise<User | null>;
}

export interface ProductRepository extends Repository<Product, CreateProductDto, UpdateProductDto> {
  findByCategory(categoryId: string): Promise<Product[]>;
  search(query: string): Promise<Product[]>;
}
```

### Prisma Implementation

```typescript
// repositories/prisma-user.repository.ts
export class PrismaUserRepository implements UserRepository {
  constructor(private readonly prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { email } });
  }

  async create(data: CreateUserDto): Promise<User> {
    return this.prisma.user.create({ data });
  }

  async update(id: string, data: UpdateUserDto): Promise<User> {
    return this.prisma.user.update({ where: { id }, data });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({ where: { id } });
  }

  async findMany(filter?: Partial<User>): Promise<User[]> {
    return this.prisma.user.findMany({ where: filter });
  }
}
```

---

## Service Layer

### Service with Injected Dependencies

```typescript
// services/order.service.ts
export class OrderService {
  constructor(
    private readonly orderRepo: OrderRepository,
    private readonly productRepo: ProductRepository,
    private readonly paymentService: PaymentService,
    private readonly eventEmitter: EventEmitter,
    private readonly logger: Logger
  ) {}

  async createOrder(userId: string, items: OrderItemDto[]): Promise<Order> {
    // Validate products exist and have stock
    const products = await this.validateProducts(items);

    // Calculate total
    const total = this.calculateTotal(products, items);

    // Create order in transaction
    const order = await this.orderRepo.create({
      userId,
      items: items.map((item) => ({
        productId: item.productId,
        quantity: item.quantity,
        price: products.find((p) => p.id === item.productId)!.price,
      })),
      total,
      status: 'pending',
    });

    // Emit event for other services
    this.eventEmitter.emit('order.created', { orderId: order.id, userId });

    this.logger.info({ orderId: order.id }, 'Order created');
    return order;
  }

  private async validateProducts(items: OrderItemDto[]): Promise<Product[]> {
    const productIds = items.map((i) => i.productId);
    const products = await this.productRepo.findByIds(productIds);

    if (products.length !== productIds.length) {
      throw new ValidationError('Some products not found');
    }

    return products;
  }

  private calculateTotal(products: Product[], items: OrderItemDto[]): number {
    return items.reduce((sum, item) => {
      const product = products.find((p) => p.id === item.productId)!;
      return sum + product.price * item.quantity;
    }, 0);
  }
}
```

---

## Factory Pattern for Service Creation

```typescript
// factories/service.factory.ts
export function createServices(prisma: PrismaClient, redis: Redis, logger: Logger) {
  // Repositories
  const userRepo = new PrismaUserRepository(prisma);
  const productRepo = new PrismaProductRepository(prisma);
  const orderRepo = new PrismaOrderRepository(prisma);

  // Caching decorators
  const cachedProductRepo = new CachedProductRepository(productRepo, redis);

  // Services
  const authService = new AuthService(userRepo, logger);
  const catalogService = new CatalogService(cachedProductRepo, logger);
  const orderService = new OrderService(
    orderRepo,
    cachedProductRepo,
    new PaymentService(),
    new EventEmitter(),
    logger
  );

  return {
    authService,
    catalogService,
    orderService,
  };
}

// Usage in app.ts
const services = createServices(prisma, redis, logger);
app.decorate('services', services);
```

---

## Caching Decorator

```typescript
// repositories/cached-product.repository.ts
export class CachedProductRepository implements ProductRepository {
  private readonly TTL = 300; // 5 minutes

  constructor(
    private readonly inner: ProductRepository,
    private readonly redis: Redis
  ) {}

  async findById(id: string): Promise<Product | null> {
    const cacheKey = `product:${id}`;

    // Try cache first
    const cached = await this.redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    // Fetch from DB
    const product = await this.inner.findById(id);
    if (product) {
      await this.redis.setex(cacheKey, this.TTL, JSON.stringify(product));
    }

    return product;
  }

  async findByCategory(categoryId: string): Promise<Product[]> {
    const cacheKey = `products:category:${categoryId}`;

    const cached = await this.redis.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    const products = await this.inner.findByCategory(categoryId);
    await this.redis.setex(cacheKey, this.TTL, JSON.stringify(products));

    return products;
  }

  // Delegate non-cached methods
  create = this.inner.create.bind(this.inner);
  update = this.inner.update.bind(this.inner);
  delete = this.inner.delete.bind(this.inner);
  findMany = this.inner.findMany.bind(this.inner);
  search = this.inner.search.bind(this.inner);
}
```

---

## Result Type Pattern

```typescript
// types/result.ts
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

// Usage
async function processPayment(orderId: string): Promise<Result<PaymentResult, PaymentError>> {
  try {
    const result = await paymentGateway.charge(orderId);
    return { success: true, data: result };
  } catch (error) {
    if (error instanceof PaymentDeclinedError) {
      return { success: false, error: { code: 'DECLINED', message: error.message } };
    }
    return { success: false, error: { code: 'UNKNOWN', message: 'Payment failed' } };
  }
}

// Consumer
const result = await processPayment(orderId);
if (result.success) {
  console.log('Payment ID:', result.data.paymentId);
} else {
  console.log('Payment failed:', result.error.code);
}
```

---

## Type Guards

```typescript
// types/guards.ts
export function isUser(obj: unknown): obj is User {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'email' in obj &&
    typeof (obj as User).id === 'string' &&
    typeof (obj as User).email === 'string'
  );
}

export function isApiError(error: unknown): error is ApiError {
  return (
    typeof error === 'object' &&
    error !== null &&
    'statusCode' in error &&
    'message' in error
  );
}

// Usage
const response = await fetch('/api/user');
const data = await response.json();

if (isUser(data)) {
  // TypeScript knows data is User
  console.log(data.email);
} else if (isApiError(data)) {
  // TypeScript knows data is ApiError
  throw new Error(data.message);
}
```

---

## Event-Driven Communication

```typescript
// events/types.ts
export interface OrderEvents {
  'order.created': { orderId: string; userId: string };
  'order.paid': { orderId: string; paymentId: string };
  'order.shipped': { orderId: string; trackingNumber: string };
  'order.cancelled': { orderId: string; reason: string };
}

// events/emitter.ts
import { EventEmitter } from 'events';

class TypedEventEmitter<T extends Record<string, unknown>> {
  private emitter = new EventEmitter();

  emit<K extends keyof T>(event: K, data: T[K]): void {
    this.emitter.emit(event as string, data);
  }

  on<K extends keyof T>(event: K, listener: (data: T[K]) => void): void {
    this.emitter.on(event as string, listener);
  }
}

// Usage
const orderEvents = new TypedEventEmitter<OrderEvents>();

orderEvents.on('order.created', (data) => {
  // TypeScript knows data is { orderId: string; userId: string }
  sendConfirmationEmail(data.userId, data.orderId);
});

orderEvents.emit('order.created', { orderId: '123', userId: '456' });
```
