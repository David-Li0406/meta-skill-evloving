# Jest / Vitest 最佳实践

JavaScript/TypeScript 测试框架的质量约束和最佳实践。

## 框架选择

| 框架 | 适用场景 | 特点 |
|------|----------|------|
| **Jest** | React、Node.js、通用项目 | 生态丰富、开箱即用 |
| **Vitest** | Vite 项目、现代前端 | 极速、ESM 原生支持 |

---

## 项目配置

### Jest 配置

```javascript
// jest.config.js
module.exports = {
  // 测试环境
  testEnvironment: 'node', // 或 'jsdom' for 浏览器

  // 文件匹配
  testMatch: [
    '**/__tests__/**/*.test.[jt]s?(x)',
    '**/*.spec.[jt]s?(x)',
  ],

  // 覆盖率配置
  collectCoverageFrom: [
    'src/**/*.{js,ts,jsx,tsx}',
    '!src/**/*.d.ts',
    '!src/**/index.{js,ts}',
    '!src/**/*.stories.{js,ts,jsx,tsx}',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },

  // 模块解析
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },

  // 设置文件
  setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],

  // 转换
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest',
  },

  // 超时
  testTimeout: 10000,

  // 并行
  maxWorkers: '50%',
};
```

### Vitest 配置

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    // 测试环境
    environment: 'node', // 或 'jsdom', 'happy-dom'

    // 全局 API
    globals: true,

    // 文件匹配
    include: ['src/**/*.{test,spec}.{js,ts,jsx,tsx}'],
    exclude: ['node_modules', 'dist'],

    // 覆盖率
    coverage: {
      provider: 'v8', // 或 'istanbul'
      reporter: ['text', 'html', 'lcov'],
      include: ['src/**/*.{js,ts,jsx,tsx}'],
      exclude: [
        'src/**/*.d.ts',
        'src/**/*.stories.{js,ts,jsx,tsx}',
        'src/**/index.{js,ts}',
      ],
      thresholds: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80,
      },
    },

    // 设置文件
    setupFiles: ['./vitest.setup.ts'],

    // 超时
    testTimeout: 10000,

    // 并行
    pool: 'threads',
    poolOptions: {
      threads: {
        singleThread: false,
      },
    },
  },

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

---

## 测试结构规范

### 文件组织

```
src/
├── services/
│   ├── user.service.ts
│   └── user.service.test.ts      # 同级测试文件
├── utils/
│   ├── format.ts
│   └── __tests__/                # 或使用 __tests__ 目录
│       └── format.test.ts
└── components/
    ├── Button/
    │   ├── Button.tsx
    │   ├── Button.test.tsx
    │   └── Button.stories.tsx
```

### 测试文件结构

```typescript
// user.service.test.ts
import { UserService } from './user.service';
import { createMockDatabase } from '../__mocks__/database';

// 1. 描述被测模块
describe('UserService', () => {
  // 2. 共享设置
  let service: UserService;
  let mockDb: MockDatabase;

  beforeEach(() => {
    mockDb = createMockDatabase();
    service = new UserService(mockDb);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  // 3. 按方法分组
  describe('createUser', () => {
    // 4. 正常路径
    it('应该创建用户并返回用户对象', async () => {
      const input = { email: 'test@example.com', name: 'Test' };

      const result = await service.createUser(input);

      expect(result).toMatchObject({
        id: expect.any(String),
        email: 'test@example.com',
        name: 'Test',
      });
      expect(mockDb.insert).toHaveBeenCalledWith('users', expect.objectContaining(input));
    });

    // 5. 边界条件
    it('应该拒绝重复的邮箱', async () => {
      mockDb.findOne.mockResolvedValue({ id: '1', email: 'test@example.com' });

      await expect(service.createUser({ email: 'test@example.com' }))
        .rejects.toThrow('邮箱已存在');
    });

    // 6. 错误路径
    it('应该在数据库错误时抛出异常', async () => {
      mockDb.insert.mockRejectedValue(new Error('DB Error'));

      await expect(service.createUser({ email: 'test@example.com' }))
        .rejects.toThrow('DB Error');
    });
  });

  describe('getUserById', () => {
    it('应该返回用户当用户存在时', async () => {
      // ...
    });

    it('应该返回 null 当用户不存在时', async () => {
      // ...
    });
  });
});
```

---

## 断言最佳实践

### 推荐的断言方式

```typescript
// ✅ 具体值断言
expect(result.status).toBe('success');
expect(result.count).toBe(5);
expect(result.name).toBe('Test User');

// ✅ 对象结构断言
expect(result).toEqual({
  id: '123',
  name: 'Test',
  email: 'test@example.com',
});

// ✅ 部分匹配（忽略动态字段）
expect(result).toMatchObject({
  name: 'Test',
  email: 'test@example.com',
});
expect(result).toEqual(expect.objectContaining({
  name: 'Test',
}));

// ✅ 数组断言
expect(result.items).toHaveLength(3);
expect(result.items).toContain('apple');
expect(result.items).toEqual(expect.arrayContaining(['apple', 'banana']));

// ✅ 异常断言
expect(() => validate(null)).toThrow();
expect(() => validate(null)).toThrow(ValidationError);
expect(() => validate(null)).toThrow('Invalid input');

// ✅ 异步异常断言
await expect(asyncFn()).rejects.toThrow();
await expect(asyncFn()).rejects.toThrow(NotFoundError);

// ✅ 快照断言（适用于 UI 组件）
expect(component).toMatchSnapshot();
expect(result).toMatchInlineSnapshot(`
  {
    "id": "123",
    "name": "Test",
  }
`);
```

### 禁止的断言方式

```typescript
// ❌ 弱断言 - 几乎不验证任何东西
expect(result).toBeDefined();
expect(result).toBeTruthy();
expect(result).not.toBeNull();
expect(result).not.toBeUndefined();
expect(typeof result).toBe('object');

// ❌ 只检查长度不检查内容
expect(result.items.length).toBeGreaterThan(0);

// ❌ 无断言的测试
it('should work', () => {
  const result = doSomething();
  // 没有 expect！
});

// ❌ 过于宽松的断言
expect(result).toEqual(expect.anything());
```

### 断言数量指南

```typescript
// ✅ 一个测试聚焦一个行为，但可以有多个相关断言
it('应该创建订单并计算总价', () => {
  const order = createOrder(items);

  // 多个断言验证同一个行为的不同方面
  expect(order.id).toBeDefined();
  expect(order.items).toHaveLength(3);
  expect(order.subtotal).toBe(100);
  expect(order.tax).toBe(10);
  expect(order.total).toBe(110);
});

// ❌ 一个测试验证多个不相关的行为
it('should work', () => {
  // 测试创建
  const created = createUser();
  expect(created.id).toBeDefined();

  // 测试更新（应该是独立的测试）
  const updated = updateUser(created.id, { name: 'New' });
  expect(updated.name).toBe('New');

  // 测试删除（应该是独立的测试）
  deleteUser(created.id);
  expect(getUser(created.id)).toBeNull();
});
```

---

## Mock 最佳实践

### Mock 模块

```typescript
// __mocks__/axios.ts
export default {
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
};

// 测试文件中
jest.mock('axios');
import axios from 'axios';

const mockedAxios = axios as jest.Mocked<typeof axios>;

beforeEach(() => {
  mockedAxios.get.mockResolvedValue({ data: { id: 1 } });
});
```

### Mock 函数

```typescript
// 创建 Mock 函数
const mockCallback = jest.fn();
const mockCallback = vi.fn(); // Vitest

// 设置返回值
mockFn.mockReturnValue('value');
mockFn.mockReturnValueOnce('first').mockReturnValueOnce('second');
mockFn.mockResolvedValue({ data: 'async' });
mockFn.mockRejectedValue(new Error('failed'));

// 实现
mockFn.mockImplementation((x) => x * 2);

// 验证调用
expect(mockFn).toHaveBeenCalled();
expect(mockFn).toHaveBeenCalledTimes(2);
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2');
expect(mockFn).toHaveBeenLastCalledWith('lastArg');
expect(mockFn).toHaveBeenNthCalledWith(1, 'firstArg');

// 清理
mockFn.mockClear();   // 清除调用记录
mockFn.mockReset();   // 清除调用记录 + 返回值
mockFn.mockRestore(); // 恢复原始实现
```

### Mock 类

```typescript
// 手动 Mock
class MockUserRepository {
  findById = jest.fn();
  save = jest.fn();
  delete = jest.fn();
}

// 使用工厂函数
const createMockUserRepository = () => ({
  findById: jest.fn(),
  save: jest.fn(),
  delete: jest.fn(),
});

// 测试中使用
const mockRepo = createMockUserRepository();
mockRepo.findById.mockResolvedValue({ id: '1', name: 'Test' });

const service = new UserService(mockRepo);
```

### Spy

```typescript
// Spy 真实对象的方法
const spy = jest.spyOn(console, 'log');
spy.mockImplementation(() => {}); // 静默

doSomething();

expect(spy).toHaveBeenCalledWith('expected message');

spy.mockRestore(); // 恢复原始行为
```

### Mock 时间

```typescript
// Jest
beforeEach(() => {
  jest.useFakeTimers();
  jest.setSystemTime(new Date('2024-01-01'));
});

afterEach(() => {
  jest.useRealTimers();
});

it('应该使用当前时间', () => {
  const result = getCurrentDate();
  expect(result).toEqual(new Date('2024-01-01'));
});

// 快进时间
it('应该在1秒后执行', () => {
  const callback = jest.fn();
  setTimeout(callback, 1000);

  jest.advanceTimersByTime(1000);

  expect(callback).toHaveBeenCalled();
});

// Vitest
import { vi } from 'vitest';

beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date('2024-01-01'));
});

afterEach(() => {
  vi.useRealTimers();
});
```

---

## 异步测试

### Promise

```typescript
// ✅ 使用 async/await（推荐）
it('应该返回用户', async () => {
  const user = await getUser(1);
  expect(user.name).toBe('Test');
});

// ✅ 使用 rejects
it('应该抛出错误', async () => {
  await expect(getUser(-1)).rejects.toThrow('Invalid ID');
});

// ✅ 使用 resolves
it('应该解析为用户', async () => {
  await expect(getUser(1)).resolves.toMatchObject({ name: 'Test' });
});

// ❌ 不要忘记 return 或 await
it('should return user', () => {
  // 这个测试会立即通过，不会等待 Promise！
  getUser(1).then(user => {
    expect(user.name).toBe('Test');
  });
});
```

### 回调

```typescript
// 使用 done 回调
it('应该在回调中返回数据', (done) => {
  fetchDataWithCallback((error, data) => {
    expect(error).toBeNull();
    expect(data).toBe('result');
    done();
  });
});

// 或者 promisify
it('应该返回数据', async () => {
  const data = await new Promise((resolve, reject) => {
    fetchDataWithCallback((error, data) => {
      if (error) reject(error);
      else resolve(data);
    });
  });

  expect(data).toBe('result');
});
```

### 等待条件

```typescript
// 使用 waitFor（适用于 React Testing Library）
import { waitFor } from '@testing-library/react';

it('应该最终显示数据', async () => {
  render(<UserProfile id={1} />);

  await waitFor(() => {
    expect(screen.getByText('Test User')).toBeInTheDocument();
  });
});

// 使用 retry（Vitest）
import { vi } from 'vitest';

it('应该最终成功', async () => {
  await vi.waitFor(() => {
    expect(getStatus()).toBe('ready');
  }, { timeout: 5000, interval: 100 });
});
```

---

## 测试数据管理

### Factory 函数

```typescript
// factories/user.factory.ts
interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'user';
  createdAt: Date;
}

export const createTestUser = (overrides: Partial<User> = {}): User => ({
  id: 'test-id-' + Math.random().toString(36).slice(2),
  email: 'test@example.com',
  name: 'Test User',
  role: 'user',
  createdAt: new Date('2024-01-01'),
  ...overrides,
});

// 使用
it('应该处理管理员用户', () => {
  const admin = createTestUser({ role: 'admin' });
  expect(hasAdminAccess(admin)).toBe(true);
});

it('应该处理普通用户', () => {
  const user = createTestUser({ role: 'user' });
  expect(hasAdminAccess(user)).toBe(false);
});
```

### Builder 模式

```typescript
// builders/order.builder.ts
class OrderBuilder {
  private order: Partial<Order> = {
    items: [],
    status: 'pending',
  };

  withItem(item: OrderItem): this {
    this.order.items!.push(item);
    return this;
  }

  withStatus(status: OrderStatus): this {
    this.order.status = status;
    return this;
  }

  withCustomer(customer: Customer): this {
    this.order.customer = customer;
    return this;
  }

  build(): Order {
    return {
      id: 'order-' + Math.random().toString(36).slice(2),
      createdAt: new Date(),
      ...this.order,
    } as Order;
  }
}

// 使用
it('应该计算订单总价', () => {
  const order = new OrderBuilder()
    .withItem({ name: 'Apple', price: 10, quantity: 2 })
    .withItem({ name: 'Banana', price: 5, quantity: 3 })
    .build();

  expect(calculateTotal(order)).toBe(35);
});
```

### Fixtures

```typescript
// __fixtures__/users.ts
export const validUser = {
  id: '1',
  email: 'valid@example.com',
  name: 'Valid User',
};

export const adminUser = {
  id: '2',
  email: 'admin@example.com',
  name: 'Admin User',
  role: 'admin',
};

export const invalidUsers = [
  { email: '', name: 'No Email' },
  { email: 'invalid', name: 'Invalid Email' },
  { email: 'test@test.com', name: '' },
];

// 使用
import { validUser, invalidUsers } from './__fixtures__/users';

it('应该验证有效用户', () => {
  expect(validateUser(validUser)).toBe(true);
});

it.each(invalidUsers)('应该拒绝无效用户: %o', (user) => {
  expect(validateUser(user)).toBe(false);
});
```

---

## 参数化测试

```typescript
// Jest / Vitest
describe('validateEmail', () => {
  it.each([
    ['test@example.com', true],
    ['user@domain.org', true],
    ['invalid', false],
    ['@nodomain.com', false],
    ['noat.com', false],
  ])('validateEmail("%s") 应该返回 %s', (email, expected) => {
    expect(validateEmail(email)).toBe(expected);
  });

  // 使用对象数组（更清晰）
  it.each([
    { input: 'test@example.com', expected: true, desc: '有效邮箱' },
    { input: 'invalid', expected: false, desc: '无效格式' },
    { input: '', expected: false, desc: '空字符串' },
  ])('$desc: validateEmail("$input") = $expected', ({ input, expected }) => {
    expect(validateEmail(input)).toBe(expected);
  });
});

// 使用 describe.each 参数化整个测试套件
describe.each([
  { role: 'admin', canDelete: true, canEdit: true },
  { role: 'editor', canDelete: false, canEdit: true },
  { role: 'viewer', canDelete: false, canEdit: false },
])('角色权限: $role', ({ role, canDelete, canEdit }) => {
  const user = createTestUser({ role });

  it(`canDelete = ${canDelete}`, () => {
    expect(hasPermission(user, 'delete')).toBe(canDelete);
  });

  it(`canEdit = ${canEdit}`, () => {
    expect(hasPermission(user, 'edit')).toBe(canEdit);
  });
});
```

---

## 测试隔离

### 清理

```typescript
// 全局清理
beforeEach(() => {
  jest.clearAllMocks();  // 清除所有 Mock 的调用记录
});

afterEach(() => {
  jest.restoreAllMocks(); // 恢复所有 Spy
});

// 数据库清理
beforeEach(async () => {
  await db.query('DELETE FROM users');
});

// 或使用事务回滚
let transaction: Transaction;

beforeEach(async () => {
  transaction = await db.beginTransaction();
});

afterEach(async () => {
  await transaction.rollback();
});
```

### 避免测试污染

```typescript
// ❌ 测试间共享状态
let counter = 0;

it('test 1', () => {
  counter++;
  expect(counter).toBe(1);
});

it('test 2', () => {
  counter++;
  expect(counter).toBe(2); // 依赖 test 1 的执行
});

// ✅ 每个测试独立
it('test 1', () => {
  let counter = 0;
  counter++;
  expect(counter).toBe(1);
});

it('test 2', () => {
  let counter = 0;
  counter++;
  expect(counter).toBe(1); // 独立
});
```

---

## 运行命令

```bash
# Jest
npm test                           # 运行所有测试
npm test -- --watch                # 监视模式
npm test -- --coverage             # 覆盖率报告
npm test -- --testPathPattern=user # 匹配文件名
npm test -- --testNamePattern="创建用户" # 匹配测试名
npm test -- --runInBand            # 串行运行（调试用）
npm test -- --detectOpenHandles    # 检测未关闭的句柄

# Vitest
npx vitest                         # 监视模式
npx vitest run                     # 单次运行
npx vitest --coverage              # 覆盖率报告
npx vitest --ui                    # UI 界面
npx vitest user.service            # 匹配文件名
npx vitest --reporter=verbose      # 详细输出
```

---

## 调试技巧

```typescript
// 只运行特定测试
it.only('这个测试会单独运行', () => {});
describe.only('这个套件会单独运行', () => {});

// 跳过测试
it.skip('这个测试会被跳过', () => {});
describe.skip('这个套件会被跳过', () => {});

// 标记待实现
it.todo('需要实现这个测试');

// 调试输出
it('debug test', () => {
  const result = complexFunction();
  console.log('Result:', JSON.stringify(result, null, 2));
  expect(result).toBeDefined();
});

// 使用 debugger（需要 --inspect）
it('debug with breakpoint', () => {
  debugger; // 断点
  const result = complexFunction();
  expect(result).toBeDefined();
});
```

```bash
# 调试 Jest 测试
node --inspect-brk node_modules/.bin/jest --runInBand

# 调试 Vitest 测试
vitest --inspect-brk --single-thread
```
