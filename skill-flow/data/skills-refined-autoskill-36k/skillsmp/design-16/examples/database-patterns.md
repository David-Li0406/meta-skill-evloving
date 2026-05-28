# Pattern: Database Patterns

> Standard patterns for database access, transactions, and data management.

---

## When to Use This Pattern

- Implementing database queries and mutations
- Managing transactions across multiple operations
- Setting up connection pooling
- Handling database migrations

**Do NOT use when:**
- Simple read-only queries (use raw queries)
- One-off scripts (direct connection is fine)

---

## The Pattern

### Repository Pattern (TypeScript/Prisma)

```typescript
// repositories/base.ts
import { PrismaClient } from '@prisma/client';

export abstract class BaseRepository<T, CreateInput, UpdateInput> {
  constructor(protected prisma: PrismaClient) {}

  abstract findById(id: string): Promise<T | null>;
  abstract findAll(options?: { limit?: number; offset?: number }): Promise<T[]>;
  abstract create(data: CreateInput): Promise<T>;
  abstract update(id: string, data: UpdateInput): Promise<T>;
  abstract delete(id: string): Promise<void>;
}

// repositories/user.ts
import { User, Prisma } from '@prisma/client';
import { BaseRepository } from './base';

export class UserRepository extends BaseRepository<
  User,
  Prisma.UserCreateInput,
  Prisma.UserUpdateInput
> {
  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { id },
    });
  }

  async findByEmail(email: string): Promise<User | null> {
    return this.prisma.user.findUnique({
      where: { email },
    });
  }

  async findAll(options?: { limit?: number; offset?: number }): Promise<User[]> {
    return this.prisma.user.findMany({
      take: options?.limit ?? 100,
      skip: options?.offset ?? 0,
      orderBy: { createdAt: 'desc' },
    });
  }

  async create(data: Prisma.UserCreateInput): Promise<User> {
    return this.prisma.user.create({ data });
  }

  async update(id: string, data: Prisma.UserUpdateInput): Promise<User> {
    return this.prisma.user.update({
      where: { id },
      data,
    });
  }

  async delete(id: string): Promise<void> {
    await this.prisma.user.delete({ where: { id } });
  }

  // Complex query example
  async findWithOrders(id: string): Promise<User & { orders: Order[] } | null> {
    return this.prisma.user.findUnique({
      where: { id },
      include: {
        orders: {
          orderBy: { createdAt: 'desc' },
          take: 10,
        },
      },
    });
  }
}
```

### Transaction Pattern

```typescript
// services/order.ts
import { PrismaClient } from '@prisma/client';

export class OrderService {
  constructor(private prisma: PrismaClient) {}

  async createOrder(userId: string, items: OrderItem[]): Promise<Order> {
    // Transaction ensures all-or-nothing
    return this.prisma.$transaction(async (tx) => {
      // 1. Verify user exists
      const user = await tx.user.findUnique({ where: { id: userId } });
      if (!user) {
        throw new NotFoundError('User', userId);
      }

      // 2. Calculate total
      const total = items.reduce((sum, item) => sum + item.price * item.quantity, 0);

      // 3. Create order
      const order = await tx.order.create({
        data: {
          userId,
          total,
          status: 'pending',
        },
      });

      // 4. Create order items
      await tx.orderItem.createMany({
        data: items.map(item => ({
          orderId: order.id,
          productId: item.productId,
          quantity: item.quantity,
          price: item.price,
        })),
      });

      // 5. Update inventory
      for (const item of items) {
        await tx.product.update({
          where: { id: item.productId },
          data: {
            stock: { decrement: item.quantity },
          },
        });
      }

      return order;
    });
  }

  // With explicit transaction timeout and isolation level
  async processPayment(orderId: string, paymentData: PaymentData): Promise<void> {
    await this.prisma.$transaction(
      async (tx) => {
        const order = await tx.order.findUnique({ where: { id: orderId } });

        if (order?.status !== 'pending') {
          throw new ConflictError('Order is not pending');
        }

        // Process payment with external service
        await paymentService.charge(paymentData);

        // Update order status
        await tx.order.update({
          where: { id: orderId },
          data: { status: 'paid' },
        });
      },
      {
        timeout: 30000,  // 30 second timeout
        isolationLevel: 'Serializable',  // Prevent race conditions
      }
    );
  }
}
```

### Python (SQLAlchemy)

```python
# repositories/base.py
from typing import TypeVar, Generic, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar('T')

class BaseRepository(Generic[T]):
    def __init__(self, session: Session, model: type[T]):
        self.session = session
        self.model = model

    def find_by_id(self, id: str) -> Optional[T]:
        return self.session.get(self.model, id)

    def find_all(self, limit: int = 100, offset: int = 0) -> List[T]:
        stmt = select(self.model).limit(limit).offset(offset)
        return list(self.session.scalars(stmt))

    def create(self, **kwargs) -> T:
        instance = self.model(**kwargs)
        self.session.add(instance)
        self.session.commit()
        return instance

    def update(self, id: str, **kwargs) -> T:
        instance = self.find_by_id(id)
        if not instance:
            raise NotFoundError(self.model.__name__, id)
        for key, value in kwargs.items():
            setattr(instance, key, value)
        self.session.commit()
        return instance

    def delete(self, id: str) -> None:
        instance = self.find_by_id(id)
        if instance:
            self.session.delete(instance)
            self.session.commit()

# repositories/user.py
from .base import BaseRepository
from models import User

class UserRepository(BaseRepository[User]):
    def __init__(self, session: Session):
        super().__init__(session, User)

    def find_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.session.scalar(stmt)

# Transaction context manager
from contextlib import contextmanager

@contextmanager
def transaction(session: Session):
    """Provide transactional scope."""
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

# Usage
def create_order(session: Session, user_id: str, items: list) -> Order:
    with transaction(session):
        user = session.get(User, user_id)
        if not user:
            raise NotFoundError('User', user_id)

        order = Order(user_id=user_id, status='pending')
        session.add(order)
        session.flush()  # Get order.id

        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product_id'],
                quantity=item['quantity']
            )
            session.add(order_item)

        return order
```

### Connection Pooling

```typescript
// db/client.ts
import { PrismaClient } from '@prisma/client';

declare global {
  var prisma: PrismaClient | undefined;
}

// Prevent multiple instances in development (hot reload)
export const prisma = global.prisma || new PrismaClient({
  log: process.env.NODE_ENV === 'development'
    ? ['query', 'error', 'warn']
    : ['error'],
});

if (process.env.NODE_ENV !== 'production') {
  global.prisma = prisma;
}

// Graceful shutdown
process.on('beforeExit', async () => {
  await prisma.$disconnect();
});
```

```python
# db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,  # Recycle connections after 30 minutes
)

SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_db():
    """Dependency for FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Query Optimization

```typescript
// Avoid N+1 queries
// BAD - N+1 query
const users = await prisma.user.findMany();
for (const user of users) {
  const orders = await prisma.order.findMany({ where: { userId: user.id } });
  // Process orders...
}

// GOOD - Single query with include
const users = await prisma.user.findMany({
  include: {
    orders: true,
  },
});

// GOOD - Batch loading
const users = await prisma.user.findMany();
const userIds = users.map(u => u.id);
const orders = await prisma.order.findMany({
  where: { userId: { in: userIds } },
});
const ordersByUser = orders.reduce((acc, order) => {
  acc[order.userId] = acc[order.userId] || [];
  acc[order.userId].push(order);
  return acc;
}, {});

// Pagination
async function paginatedUsers(cursor?: string, limit: number = 20) {
  return prisma.user.findMany({
    take: limit + 1,  // Fetch one extra to know if there's more
    ...(cursor && {
      cursor: { id: cursor },
      skip: 1,  // Skip the cursor
    }),
    orderBy: { createdAt: 'desc' },
  });
}
```

### Raw SQL (When Needed)

```typescript
// Complex queries that ORM doesn't handle well
const result = await prisma.$queryRaw`
  SELECT
    u.id,
    u.name,
    COUNT(o.id) as order_count,
    SUM(o.total) as total_spent
  FROM users u
  LEFT JOIN orders o ON o.user_id = u.id
  WHERE u.created_at > ${startDate}
  GROUP BY u.id
  HAVING COUNT(o.id) > 5
  ORDER BY total_spent DESC
  LIMIT 10
`;

// Parameterized to prevent SQL injection
const users = await prisma.$queryRaw`
  SELECT * FROM users WHERE email = ${email}
`;
```

---

## Common Mistakes to Avoid

### 1. Not Using Transactions
```typescript
// BAD - partial failure leaves inconsistent state
await prisma.order.create({ data: orderData });
await prisma.inventory.update({ data: { stock: newStock } });  // Might fail!

// GOOD - transaction ensures consistency
await prisma.$transaction([
  prisma.order.create({ data: orderData }),
  prisma.inventory.update({ data: { stock: newStock } }),
]);
```

### 2. N+1 Queries
```typescript
// BAD - 1 query for users + N queries for orders
const users = await prisma.user.findMany();
const results = await Promise.all(
  users.map(async (user) => ({
    ...user,
    orders: await prisma.order.findMany({ where: { userId: user.id } }),
  }))
);

// GOOD - 1 query total
const users = await prisma.user.findMany({
  include: { orders: true },
});
```

### 3. Not Handling Connection Failures
```typescript
// BAD - no retry on transient failures
const user = await prisma.user.findUnique({ where: { id } });

// GOOD - retry with backoff
import { retry } from './utils';

const user = await retry(
  () => prisma.user.findUnique({ where: { id } }),
  { retries: 3, backoff: 1000 }
);
```

### 4. Exposing Internal IDs
```typescript
// BAD - sequential IDs reveal business info
const user = await prisma.user.create({
  data: { email }
});  // Returns id: 12345 (reveals you have ~12k users)

// GOOD - use UUIDs
const user = await prisma.user.create({
  data: {
    id: crypto.randomUUID(),
    email
  }
});
```

### 5. Not Indexing Query Fields
```sql
-- BAD - slow query on unindexed field
SELECT * FROM users WHERE email = 'test@example.com';

-- GOOD - add index
CREATE INDEX idx_users_email ON users(email);
```

---

## Validation Commands

```bash
# Check for N+1 queries (look for many similar queries)
grep -n "prisma\.\w\+\.find" src/**/*.ts | head -20

# Verify indexes exist for common queries
psql "$DATABASE_URL" -c "\d+ users" | grep -i index

# Check query performance
psql "$DATABASE_URL" -c "EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@test.com'"

# Verify connection pool settings
psql "$DATABASE_URL" -c "SHOW max_connections"

# Run migration status
npx prisma migrate status
```

---

## Related Conventions

- **Transactions**: Use transactions for multi-step operations
- **Pooling**: Always use connection pooling in production
- **Indexes**: Index all fields used in WHERE clauses
- **IDs**: Use UUIDs instead of sequential integers
- **Migrations**: Version all schema changes with migrations

---

## See Also

- [Config Loading](config-loading.md) - For database connection configuration
- [Error Handling](error-handling.md) - For database error handling
- [Test Fixtures](test-fixtures.md) - For database test setup
