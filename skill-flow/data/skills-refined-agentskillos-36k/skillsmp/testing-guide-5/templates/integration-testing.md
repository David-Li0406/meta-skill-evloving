# 集成测试指南

## 集成测试的关注点

集成测试验证**模块之间的协作**，不是验证单个模块的逻辑。

| 关注点 | 验证内容 | 不验证 |
|--------|----------|--------|
| **数据流** | 数据在模块间正确传递 | 单个模块内部逻辑 |
| **接口契约** | 模块间调用参数和返回值符合约定 | 参数的详细验证 |
| **错误传播** | 错误正确地跨模块传播 | 错误的详细处理 |
| **事务边界** | 数据库事务正确提交/回滚 | 单条SQL正确性 |

## 集成测试策略

### 边界定义

```
系统边界图:

┌─────────────────────────────────────────────────────────┐
│                    Application                          │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐             │
│  │ Handler │───▶│ Service │───▶│  Repo   │             │
│  └─────────┘    └─────────┘    └─────────┘             │
│                      │              │                   │
│                      ▼              ▼                   │
│              ┌─────────────┐ ┌─────────────┐           │
│              │ External API│ │  Database   │           │
│              └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────┘

集成测试边界:
- Handler → Service → Repo（真实调用，Mock 数据库）
- Service → External API（Mock API，验证请求格式）
```

## 测试数据库策略

| 策略 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| **内存数据库** | 快速测试 | 速度快、无状态 | 可能与生产不一致 |
| **Docker 容器** | CI 环境 | 与生产一致 | 启动较慢 |
| **测试专用库** | 本地开发 | 真实环境 | 需要清理数据 |
| **事务回滚** | 任何场景 | 自动清理 | 无法测试事务本身 |

### 事务回滚模式

```typescript
describe('UserRepository', () => {
  let transaction: Transaction;

  beforeEach(async () => {
    transaction = await db.beginTransaction();
  });

  afterEach(async () => {
    await transaction.rollback();  // 自动清理
  });

  test('createUser 应该插入数据库记录', async () => {
    const repo = new UserRepository(transaction);
    const user = await repo.create({ name: 'test' });

    const found = await repo.findById(user.id);
    expect(found.name).toBe('test');
  });
});
```

## 契约测试

### 消费者驱动契约

```typescript
// Consumer 定义期望的契约
const userApiContract = {
  request: {
    method: 'GET',
    path: '/users/1',
  },
  response: {
    status: 200,
    body: {
      id: 1,
      name: Matchers.string(),
      email: Matchers.email(),
      createdAt: Matchers.iso8601DateTime(),
    },
  },
};

// Provider 验证是否满足契约
describe('User API Contract', () => {
  it('GET /users/:id 应该符合契约', async () => {
    const response = await api.get('/users/1');
    expect(response).toMatchContract(userApiContract);
  });
});
```

## API 集成测试

### HTTP 端点测试

```typescript
describe('POST /api/users', () => {
  test('应该创建用户并返回201', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'test@example.com' })
      .expect(201);

    expect(response.body.id).toBeDefined();
    expect(response.body.name).toBe('Test');
    expect(response.body.email).toBe('test@example.com');
  });

  test('应该返回400当邮箱格式无效', async () => {
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Test', email: 'invalid' })
      .expect(400);

    expect(response.body.error).toContain('email');
  });

  test('应该返回409当邮箱已存在', async () => {
    // 先创建一个用户
    await request(app)
      .post('/api/users')
      .send({ name: 'First', email: 'duplicate@example.com' });

    // 尝试创建相同邮箱
    const response = await request(app)
      .post('/api/users')
      .send({ name: 'Second', email: 'duplicate@example.com' })
      .expect(409);

    expect(response.body.error).toContain('exists');
  });
});
```

## 数据库集成测试

### Repository 测试

```typescript
describe('UserRepository', () => {
  let repo: UserRepository;
  let testDb: TestDatabase;

  beforeAll(async () => {
    testDb = await TestDatabase.create();
    await testDb.migrate();
  });

  afterAll(async () => {
    await testDb.destroy();
  });

  beforeEach(async () => {
    repo = new UserRepository(testDb.connection);
    await testDb.truncate('users');
  });

  test('save 应该持久化用户', async () => {
    const user = new User({ name: 'Test', email: 'test@example.com' });

    await repo.save(user);

    const found = await repo.findByEmail('test@example.com');
    expect(found).not.toBeNull();
    expect(found!.name).toBe('Test');
  });

  test('findById 应该返回null当用户不存在', async () => {
    const found = await repo.findById('non-existent-id');
    expect(found).toBeNull();
  });
});
```

## 外部服务集成测试

### Mock 外部 API

```typescript
import nock from 'nock';

describe('PaymentService', () => {
  afterEach(() => {
    nock.cleanAll();
  });

  test('processPayment 应该调用支付网关', async () => {
    // Mock 外部 API
    const scope = nock('https://api.payment.com')
      .post('/charge', {
        amount: 1000,
        currency: 'USD',
        source: 'tok_test',
      })
      .reply(200, {
        id: 'ch_123',
        status: 'succeeded',
      });

    const service = new PaymentService();
    const result = await service.processPayment({
      amount: 1000,
      currency: 'USD',
      source: 'tok_test',
    });

    expect(result.status).toBe('succeeded');
    expect(scope.isDone()).toBe(true);  // 验证 API 被调用
  });

  test('processPayment 应该处理网关错误', async () => {
    nock('https://api.payment.com')
      .post('/charge')
      .reply(500, { error: 'Gateway error' });

    const service = new PaymentService();

    await expect(service.processPayment({
      amount: 1000,
      currency: 'USD',
      source: 'tok_test',
    })).rejects.toThrow('Payment failed');
  });
});
```

## 测试隔离

### 确保测试独立

```typescript
// ❌ 测试间有依赖
describe('Order flow', () => {
  let userId: string;

  test('create user', async () => {
    const user = await createUser({ name: 'test' });
    userId = user.id;  // 后续测试依赖这个
  });

  test('create order', async () => {
    const order = await createOrder({ userId });  // 依赖上一个测试
    expect(order.userId).toBe(userId);
  });
});

// ✅ 每个测试独立
describe('Order', () => {
  test('create order should associate with user', async () => {
    // 在测试内创建所需数据
    const user = await createUser({ name: 'test' });
    const order = await createOrder({ userId: user.id });

    expect(order.userId).toBe(user.id);
  });
});
```
