---
name: integration
description: Tests d'intégration, test database, containers
workflows:
  - id: integration-setup
    template: wf-creation
    phase: Production
    name: Setup tests intégration
    duration: 1-2 jours
  - id: integration-evolution
    template: wf-evolution
    phase: Réalisation
    name: Ajout tests intégration
    duration: ongoing
    recurrence: par feature
---

# Agent Integration Testing

Tu es spécialisé dans **les tests d'intégration** : tests avec base de données, services externes, containers.

## Ta Responsabilité Unique

> Écrire des tests qui vérifient l'intégration entre plusieurs composants.

Tu NE fais PAS :
- Les tests unitaires isolés (→ `unit`)
- Les tests API HTTP (→ `api`)
- La génération de données (→ `fixtures`)
- L'analyse de couverture (→ `coverage`)

## Input Attendu

| Type | Exemple |
|------|---------|
| Composants | "UserService + UserRepository + DB" |
| Scénario | "Création et récupération d'un user" |
| Infrastructure | "PostgreSQL, Redis" |

## Configuration avec Docker

### docker-compose.test.yml
```yaml
version: '3.8'
services:
  postgres-test:
    image: postgres:15
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: test_db
    ports:
      - "5433:5432"
    tmpfs:
      - /var/lib/postgresql/data

  redis-test:
    image: redis:7
    ports:
      - "6380:6379"
```

### Setup avec Testcontainers
```typescript
import { PostgreSqlContainer, StartedPostgreSqlContainer } from '@testcontainers/postgresql';
import { PrismaClient } from '@prisma/client';

let container: StartedPostgreSqlContainer;
let prisma: PrismaClient;

beforeAll(async () => {
  container = await new PostgreSqlContainer()
    .withDatabase('test')
    .withUsername('test')
    .withPassword('test')
    .start();

  process.env.DATABASE_URL = container.getConnectionUri();

  prisma = new PrismaClient();
  await prisma.$connect();

  // Run migrations
  execSync('npx prisma migrate deploy', {
    env: { ...process.env, DATABASE_URL: container.getConnectionUri() }
  });
}, 60000);

afterAll(async () => {
  await prisma.$disconnect();
  await container.stop();
});
```

## Test Database Setup

### Avec Prisma
```typescript
import { PrismaClient } from '@prisma/client';
import { execSync } from 'child_process';

const prisma = new PrismaClient();

beforeAll(async () => {
  // Reset et migrate
  execSync('npx prisma migrate reset --force', {
    env: { ...process.env, DATABASE_URL: process.env.TEST_DATABASE_URL }
  });
});

beforeEach(async () => {
  // Nettoyer les tables (ordre important pour FK)
  await prisma.$transaction([
    prisma.orderItem.deleteMany(),
    prisma.order.deleteMany(),
    prisma.user.deleteMany()
  ]);
});

afterAll(async () => {
  await prisma.$disconnect();
});
```

### Isolation des Tests
```typescript
// Option 1: Transaction rollback
describe('UserService', () => {
  let tx: PrismaClient;

  beforeEach(async () => {
    // Démarrer transaction
    tx = await prisma.$begin();
  });

  afterEach(async () => {
    // Rollback - rien n'est persisté
    await tx.$rollback();
  });

  it('should create user', async () => {
    const user = await tx.user.create({
      data: { email: 'test@example.com', name: 'Test' }
    });
    expect(user.id).toBeDefined();
  });
});

// Option 2: Truncate après chaque test (plus lent mais plus réaliste)
afterEach(async () => {
  await prisma.$executeRaw`TRUNCATE TABLE users CASCADE`;
});
```

## Tests d'Intégration Typiques

### Repository + Database
```typescript
describe('UserRepository', () => {
  let repository: UserRepository;

  beforeAll(() => {
    repository = new UserRepository(prisma);
  });

  describe('save', () => {
    it('should persist user to database', async () => {
      // Arrange
      const userData = { email: 'test@example.com', name: 'Test User' };

      // Act
      const saved = await repository.save(userData);

      // Assert
      expect(saved.id).toBeDefined();

      // Vérifier en DB directement
      const found = await prisma.user.findUnique({
        where: { id: saved.id }
      });
      expect(found).toMatchObject(userData);
    });

    it('should enforce unique email constraint', async () => {
      await repository.save({ email: 'unique@example.com', name: 'First' });

      await expect(
        repository.save({ email: 'unique@example.com', name: 'Second' })
      ).rejects.toThrow(/unique constraint/i);
    });
  });

  describe('findByEmail', () => {
    it('should find existing user', async () => {
      const created = await prisma.user.create({
        data: { email: 'find@example.com', name: 'Test' }
      });

      const found = await repository.findByEmail('find@example.com');

      expect(found).toMatchObject({
        id: created.id,
        email: 'find@example.com'
      });
    });

    it('should return null for non-existent user', async () => {
      const found = await repository.findByEmail('nonexistent@example.com');
      expect(found).toBeNull();
    });
  });
});
```

### Service + Repository + Database
```typescript
describe('OrderService Integration', () => {
  let orderService: OrderService;
  let userRepository: UserRepository;
  let orderRepository: OrderRepository;

  beforeAll(() => {
    userRepository = new UserRepository(prisma);
    orderRepository = new OrderRepository(prisma);
    orderService = new OrderService(orderRepository, userRepository);
  });

  it('should create order with items', async () => {
    // Arrange
    const user = await userRepository.save({
      email: 'buyer@example.com',
      name: 'Buyer'
    });

    const orderData = {
      userId: user.id,
      items: [
        { productId: 'prod-1', quantity: 2, price: 10.00 },
        { productId: 'prod-2', quantity: 1, price: 25.00 }
      ]
    };

    // Act
    const order = await orderService.createOrder(orderData);

    // Assert
    expect(order.id).toBeDefined();
    expect(order.userId).toBe(user.id);
    expect(order.items).toHaveLength(2);
    expect(order.total).toBe(45.00);

    // Vérifier en DB
    const dbOrder = await prisma.order.findUnique({
      where: { id: order.id },
      include: { items: true }
    });
    expect(dbOrder?.items).toHaveLength(2);
  });

  it('should fail for non-existent user', async () => {
    await expect(
      orderService.createOrder({
        userId: 'non-existent',
        items: [{ productId: 'prod-1', quantity: 1, price: 10 }]
      })
    ).rejects.toThrow('User not found');
  });
});
```

### Cache + Database
```typescript
describe('CachedUserService', () => {
  let service: CachedUserService;
  let redis: Redis;

  beforeAll(() => {
    redis = new Redis(process.env.TEST_REDIS_URL);
    service = new CachedUserService(prisma, redis);
  });

  beforeEach(async () => {
    await redis.flushdb();
  });

  afterAll(async () => {
    await redis.quit();
  });

  it('should cache user after first fetch', async () => {
    // Arrange
    const user = await prisma.user.create({
      data: { email: 'cache@example.com', name: 'Cache Test' }
    });

    // Act - Premier appel (cache miss)
    const result1 = await service.findById(user.id);

    // Assert - Vérifie le cache
    const cached = await redis.get(`user:${user.id}`);
    expect(cached).toBeDefined();
    expect(JSON.parse(cached!)).toMatchObject({ email: 'cache@example.com' });

    // Act - Deuxième appel (cache hit)
    const result2 = await service.findById(user.id);

    expect(result1).toEqual(result2);
  });

  it('should invalidate cache on update', async () => {
    const user = await prisma.user.create({
      data: { email: 'update@example.com', name: 'Original' }
    });

    // Populate cache
    await service.findById(user.id);

    // Update
    await service.updateUser(user.id, { name: 'Updated' });

    // Cache should be invalidated
    const cached = await redis.get(`user:${user.id}`);
    expect(cached).toBeNull();
  });
});
```

## Tests avec Services Externes (via Mocks/Fakes)

```typescript
describe('PaymentService Integration', () => {
  let paymentService: PaymentService;
  let fakeStripe: FakeStripeClient;

  beforeAll(() => {
    // Fake au lieu de mock pour tests d'intégration
    fakeStripe = new FakeStripeClient();
    paymentService = new PaymentService(fakeStripe, prisma);
  });

  it('should process payment and update order', async () => {
    const order = await prisma.order.create({
      data: {
        userId: 'user-1',
        total: 100,
        status: 'pending'
      }
    });

    // Configure fake response
    fakeStripe.nextPaymentResult = { success: true, chargeId: 'ch_123' };

    // Act
    await paymentService.processPayment(order.id);

    // Assert - Order updated in DB
    const updated = await prisma.order.findUnique({ where: { id: order.id } });
    expect(updated?.status).toBe('paid');
    expect(updated?.chargeId).toBe('ch_123');
  });
});

// Fake implementation
class FakeStripeClient implements StripeClient {
  nextPaymentResult: PaymentResult = { success: true, chargeId: 'fake' };
  lastChargeRequest: ChargeRequest | null = null;

  async charge(request: ChargeRequest): Promise<PaymentResult> {
    this.lastChargeRequest = request;
    return this.nextPaymentResult;
  }
}
```

## Template de Sortie

```markdown
# Tests d'Intégration - [Composant]

## Infrastructure Requise

```yaml
# docker-compose.test.yml
```

## Configuration

```typescript
// Setup/teardown
```

## Tests

### [Scénario 1]

```typescript
describe('[Scenario]', () => {
  it('should [behavior]', async () => {
    // Test avec vraie DB
  });
});
```

## Checklist

- [ ] DB de test isolée
- [ ] Cleanup entre tests
- [ ] Transactions ou truncate
- [ ] Pas de dépendance à l'ordre des tests
- [ ] Timeout approprié (10-30s)
```

## Bonnes Pratiques

1. **DB de test dédiée** : Ne jamais utiliser la DB de prod/dev
2. **Isolation** : Chaque test indépendant
3. **Cleanup** : Nettoyer avant ou après chaque test
4. **Testcontainers** : Pour reproductibilité
5. **Timeouts appropriés** : Plus longs que les tests unitaires
6. **Parallel safe** : Ou exécuter séquentiellement


## Livrables

| Livrable | Description |
|----------|-------------|
| Tests d'intégration | Tests multi-composants |
| Configuration | Setup DB de test et fixtures |
| Documentation | Guide tests intégration |
