# 单元测试指南

## 断言质量

### 禁止弱断言

```typescript
// ❌ 弱断言：几乎不验证任何东西
expect(result).toBeDefined();
expect(result).toBeTruthy();
expect(result).not.toBeNull();
expect(typeof result).toBe('object');

// ✅ 强断言：验证具体的值和行为
expect(result.status).toBe('success');
expect(result.total).toBe(150);
expect(result.items).toHaveLength(3);
expect(result.user.email).toBe('test@example.com');
```

### 断言分类

| 断言类型 | 强度 | 使用场景 | 示例 |
|----------|------|----------|------|
| **值相等** | 强 | 验证具体返回值 | `toBe(100)`, `toEqual({...})` |
| **结构验证** | 强 | 验证对象结构 | `toMatchObject({...})` |
| **集合验证** | 强 | 验证数组内容 | `toContain()`, `toHaveLength()` |
| **异常验证** | 强 | 验证错误抛出 | `toThrow(ErrorType)` |
| **类型验证** | 弱 | 仅作为辅助 | `toBeDefined()`, `toBeInstanceOf()` |
| **存在性验证** | 弱 | ⚠️ 避免单独使用 | `toBeTruthy()`, `not.toBeNull()` |

## 测试命名规范

```typescript
// ❌ 不好的命名：不清楚测试什么
test('getUser', () => {});
test('test1', () => {});
test('should work', () => {});

// ✅ 好的命名：描述预期行为
test('getUser 应该返回用户信息当用户存在时', () => {});
test('getUser 应该返回 null 当用户不存在时', () => {});
test('getUser 应该抛出 InvalidIdError 当 ID 为负数时', () => {});

// 推荐格式
// [被测方法] 应该 [预期行为] 当 [条件]
// [Subject] should [expected behavior] when [condition]
```

## 测试结构

### AAA 模式

```typescript
test('calculateDiscount 应该返回10%折扣当订单金额超过1000时', () => {
  // Arrange - 准备测试数据
  const order = {
    items: [{ price: 500 }, { price: 600 }],
    total: 1100,
  };

  // Act - 执行被测行为
  const result = calculateDiscount(order);

  // Assert - 验证结果
  expect(result.discountRate).toBe(0.1);
  expect(result.discountAmount).toBe(110);
  expect(result.finalTotal).toBe(990);
});
```

### 单一职责

```typescript
// ❌ 一个测试验证多个行为
test('用户服务', () => {
  const user = createUser({ name: 'test' });
  expect(user.id).toBeDefined();

  const updated = updateUser(user.id, { name: 'updated' });
  expect(updated.name).toBe('updated');

  deleteUser(user.id);
  expect(getUser(user.id)).toBeNull();
});

// ✅ 每个测试只验证一个行为
test('createUser 应该创建用户并返回ID', () => {});
test('updateUser 应该更新用户名称', () => {});
test('deleteUser 应该删除用户', () => {});
```

## Mock 策略

### Mock 原则

```
只 Mock 你不拥有的东西:
✅ 外部 API
✅ 数据库
✅ 文件系统
✅ 网络请求
✅ 第三方服务

不要 Mock:
❌ 被测模块的内部实现
❌ 纯函数
❌ 你自己的业务逻辑
```

### Mock 质量检查

```typescript
// ❌ Mock 返回值但不验证调用
jest.mock('./api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: 1, name: 'test' }),
}));

test('loadUser', async () => {
  const result = await loadUser(1);
  expect(result.name).toBe('test');
  // 没有验证 fetchUser 是否被正确调用！
});

// ✅ Mock 并验证调用参数
test('loadUser 应该用正确的ID调用API', async () => {
  const mockFetch = jest.fn().mockResolvedValue({ id: 1, name: 'test' });

  const result = await loadUser(1, { fetchUser: mockFetch });

  expect(mockFetch).toHaveBeenCalledWith(1);  // 验证调用
  expect(mockFetch).toHaveBeenCalledTimes(1); // 验证次数
  expect(result.name).toBe('test');
});
```

## 测试数据

### 使用工厂函数

```typescript
// ❌ 在每个测试中硬编码数据
test('test1', () => {
  const user = { id: 1, name: 'Test', email: 'test@example.com', role: 'admin' };
  // ...
});

test('test2', () => {
  const user = { id: 2, name: 'Test2', email: 'test2@example.com', role: 'user' };
  // ...
});

// ✅ 使用工厂函数
function createTestUser(overrides = {}) {
  return {
    id: 1,
    name: 'Test User',
    email: 'test@example.com',
    role: 'user',
    ...overrides,
  };
}

test('admin user can delete', () => {
  const admin = createTestUser({ role: 'admin' });
  // ...
});

test('regular user cannot delete', () => {
  const user = createTestUser({ role: 'user' });
  // ...
});
```

## 常见反模式

### 1. 测试实现而非行为

```typescript
// ❌ 测试内部实现
test('should call internal method', () => {
  const spy = jest.spyOn(service, '_internalMethod');
  service.publicMethod();
  expect(spy).toHaveBeenCalled();
});

// ✅ 测试外部可观察的行为
test('publicMethod should return calculated result', () => {
  const result = service.publicMethod();
  expect(result).toBe(expectedValue);
});
```

### 2. 过度 Mock

```typescript
// ❌ Mock 太多，测试变得无意义
test('calculate', () => {
  jest.mock('./math', () => ({ add: () => 10 }));
  jest.mock('./validator', () => ({ isValid: () => true }));
  const result = calculate(5, 5);
  expect(result).toBe(10);  // 这只是在测试 mock！
});

// ✅ 只 Mock 外部依赖
test('calculate should add valid numbers', () => {
  const result = calculate(5, 5);
  expect(result).toBe(10);
});
```

### 3. 无断言测试

```typescript
// ❌ 没有断言
test('create user', async () => {
  await userService.create({ name: 'test' });
  // 什么都没验证！
});

// ✅ 明确的断言
test('create user should return user with id', async () => {
  const user = await userService.create({ name: 'test' });
  expect(user.id).toBeDefined();
  expect(user.name).toBe('test');
});
```
