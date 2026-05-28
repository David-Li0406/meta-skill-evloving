---
name: mock-generation
description: 生成测试所需的 Mock 数据与 Stub 函数。
---

# Mock生成技能

这个技能专门负责生成测试所需的Mock数据和Stub函数，帮助隔离测试环境并提高测试效率。

## 技能能力

### 1. 依赖分析
- 自动识别需要Mock的外部依赖
- 分析函数签名和返回值类型
- 检测数据库操作、API调用等外部交互
- 识别时间和随机等不可控因素

### 2. Mock数据生成
- 生成符合类型定义的Mock对象
- 创建真实的测试数据集
- 支持复杂嵌套对象的生成
- 生成边界值和异常数据

### 3. Stub函数创建
- 创建可控的函数替代品
- 支持多种返回值模式
- 记录调用历史和参数
- 模拟异步操作

## 使用方式

### 基础Mock生成

```typescript
// 为模块生成Mock
await generateMock('src/api/userService', {
  framework: 'vitest',
  includeReturnValues: true
});

// 为特定函数生成Mock
await generateFunctionMock('fetchUserData', {
  returnType: 'User',
  async: true,
  errorScenarios: true
});
```

### 高级选项

```typescript
await generateMock(target, {
  framework: 'vitest',
  mockType: 'auto', // 'auto' | 'partial' | 'full'
  includeSpies: true,
  generateTestData: true,
  customReturnValues: {
    'getUser': () => ({ id: 1, name: 'Test User' }),
    'createUser': () => Promise.resolve({ success: true })
  }
});
```

## Mock模板

### Jest模板

```javascript
// Mock整个模块
jest.mock('{{modulePath}}', () => ({
  {{#each exports}}
  {{name}}: jest.fn(),
  {{/each}}
}));

// Mock实现
{{#each exports}}
{{name}}.mockImplementation(({{
  #if isAsync}}
  {{#if hasParams}}
  async ({ {{join params ", "}} }) => {
    // Mock implementation
    return {{defaultValue}};
  }
  {{else}}
  async () => {
    return {{defaultValue}};
  }
  {{/if}}
  {{else}}
  {{#if hasParams}}
  ({ {{join params ", "}} }) => {
    // Mock implementation
    return {{defaultValue}};
  }
  {{else}}
  () => {
    return {{defaultValue}};
  }
  {{/if}}
  {{/if}}
}));
{{/each}}

// 在测试中使用
beforeEach(() => {
  {{#each exports}}
  {{name}}.mockClear();
  {{/each}}
});
```

### Vitest模板

```typescript
import { vi } from 'vitest';

// Mock整个模块
vi.mock('{{modulePath}}', () => ({
  {{#each exports}}
  {{name}}: vi.fn(),
  {{/each}}
}));

// Mock实现
{{#each exports}}
export const {{name}} = vi.fn();
{{#if isAsync}}
{{name}}.mockResolvedValue({{defaultValue}});
{{else}}
{{name}}.mockReturnValue({{defaultValue}});
{{/if}}
{{/each}}
```

### Python Mock模板

```python
from unittest.mock import Mock, patch
import pytest

{{#each functions}}
# Mock decorator
@patch('{{modulePath}}.{{name}}')
def test_{{testName}}(mock_{{name}}):
    # Setup mock return value
    mock_{{name}}.return_value = {{defaultValue}}

    # Test implementation
    result = function_under_test()

    # Assertions
    assert result is not None
    {{#if verifyCalled}}
    mock_{{name}}.assert_called_once()
    {{/if}}
{{/each}}
```

## 数据生成器

### 基础类型生成器

```typescript
class DataGenerator {
  static generateString(options?: {
    length?: number;
    pattern?: string;
    enum?: string[];
  }): string {
    if (options?.enum) {
      return options.enum[0];
    }

    if (options?.pattern) {
      return this.matchPattern(options.pattern);
    }

    const length = options?.length || 10;
    return this.randomString(length);
  }

  static generateNumber(options?: {
    min?: number;
    max?: number;
    integer?: boolean;
    enum?: number[];
  }): number {
    if (options?.enum) {
      return options.enum[0];
    }

    const min = options?.min || 0;
    const max = options?.max || 100;

    if (options?.integer) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    return Math.random() * (max - min) + min;
  }

  static generateArray<T>(itemGenerator: () => T, options?: {
    length?: number;
    minLength?: number;
    maxLength?: number;
  }): T[] {
    const length = options?.length ||
      Math.floor(Math.random() * (options?.maxLength || 5)) + (options?.minLength || 0);

    return Array.from({ length }, itemGenerator);
  }

  static generateObject(schema: ObjectSchema): any {
    const obj: any = {};

    for (const [key, value] of Object.entries(schema)) {
      if (typeof value === 'function') {
        obj[key] = value();
      } else if (Array.isArray(value)) {
        obj[key] = this.generateArray(() => value[0]);
      } else if (typeof value === 'object') {
        obj[key] = this.generateObject(value);
      } else {
        obj[key] = value;
      }
    }

    return obj;
  }
}
```

### 复杂对象生成

```typescript
// 用户对象生成器
const UserGenerator = {
  generate: (overrides?: Partial<User>): User => ({
    id: DataGenerator.generateNumber({ integer: true, min: 1 }),
    name: DataGenerator.generateString({ length: 10 }),
    email: DataGenerator.generateEmail(),
    age: DataGenerator.generateNumber({ min: 18, max: 65, integer: true }),
    isActive: true,
    createdAt: new Date().toISOString(),
    ...overrides
  }),

  generateList: (count: number = 3): User[] =>
    DataGenerator.generateArray(() => UserGenerator.generate(), { length: count }),

  generateWithInvalidData: (): User => ({
    id: -1,
    name: '',
    email: 'invalid-email',
    age: -1,
    isActive: false,
    createdAt: 'invalid-date'
  })
};
```

## API Mock生成

### REST API Mock

```typescript
// API响应生成器
class APIResponseGenerator {
  static generateSuccessResponse<T>(data: T): APIResponse<T> {
    return {
      success: true,
      data,
      message: 'Success',
      timestamp: new Date().toISOString()
    };
  }

  static generateErrorResponse(errorCode: string, message: string): APIResponse<null> {
    return {
      success: false,
      data: null,
      error: {
        code: errorCode,
        message,
        details: {}
      },
      timestamp: new Date().toISOString()
    };
  }

  static generatePaginatedResponse<T>(
    items: T[],
    page: number = 1,
    limit: number = 10
  ): PaginatedResponse<T> {
    return {
      success: true,
      data: items,
      pagination: {
        page,
        limit,
        total: items.length,
        totalPages: Math.ceil(items.length / limit)
      }
    };
  }
}

// Fetch Mock
const mockFetch = jest.fn();
mockFetch.mockImplementation(async (url: string, options?: RequestInit) => {
  if (url.includes('/users')) {
    return {
      ok: true,
      status: 200,
      json: async () => APIResponseGenerator.generateSuccessResponse(
        UserGenerator.generateList()
      )
    };
  }

  if (url.includes('/error')) {
    return {
      ok: false,
      status: 500,
      json: async () => APIResponseGenerator.generateErrorResponse(
        'INTERNAL_ERROR',
        'Something went wrong'
      )
    };
  }

  return {
    ok: false,
    status: 404,
    json: async () => ({})
  };
});
```

## 数据库Mock

### 数据库操作Mock

```typescript
// 数据库连接Mock
const mockDb = {
  users: {
    findById: jest.fn(),
    create: jest.fn(),
    update: jest.fn(),
    delete: jest.fn(),
    findMany: jest.fn()
  },
  transactions: {
    begin: jest.fn(),
    commit: jest.fn(),
    rollback: jest.fn()
  }
};

// 设置Mock返回值
mockDb.users.findById.mockImplementation(async (id: number) => {
  if (id === 999) {
    return null;
  }
  return UserGenerator.generate({ id });
});

mockDb.users.create.mockImplementation(async (userData: Partial<User>) => {
  return UserGenerator.generate(userData);
});
```

## 时间Mock

### 时间相关测试

```javascript
// Jest时间Mock
beforeEach(() => {
  jest.useFakeTimers();
});

afterEach(() => {
  jest.useRealTimers();
});

// 测试中的时间控制
it('should execute callback after delay', () => {
  const callback = jest.fn();

  setTimeout(callback, 1000);

  // 快进时间
  jest.advanceTimersByTime(1000);

  expect(callback).toHaveBeenCalled();
});

// Vitest时间Mock
import { vi } from 'vitest';

beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});
```

## 特殊场景Mock

### 错误场景

```typescript
// 错误Mock生成器
class ErrorMockGenerator {
  static generateNetworkError(): Error {
    const error = new Error('Network Error');
    error.name = 'NetworkError';
    error.code = 'NETWORK_ERROR';
    return error;
  }

  static generateTimeoutError(): Error {
    const error = new Error('Request timeout');
    error.name = 'TimeoutError';
    error.code = 'TIMEOUT';
    return error;
  }

  static generateValidationError(field: string): Error {
    const error = new Error(`Validation failed for field: ${field}`);
    error.name = 'ValidationError';
    error.field = field;
    return error;
  }
}

// 使用错误Mock
mockApi.getUser.mockRejectedValue(ErrorMockGenerator.generateNetworkError());
```

### 异步操作

```typescript
// 异步操作Mock
const asyncMock = jest.fn();
asyncMock
  .mockResolvedValueOnce('first call result')
  .mockRejectedValueOnce(new Error('second call error'))
  .mockResolvedValueOnce('third call result');

// Promise链测试
it('should handle promise chain', async () => {
  const result = await promiseChain();

  expect(result).toBe('final result');
  expect(asyncMock).toHaveBeenCalledTimes(3);
});
```

## 最佳实践

### 1. Mock范围控制
- 只Mock外部依赖
- 避免过度Mock
- 保持Mock简单

### 2. Mock数据管理
- 使用工厂模式生成测试数据
- 创建可重用的数据集
- 保持数据一致性

### 3. Mock验证
- 验证Mock的调用
- 检查调用参数
- 确保Mock被正确使用

### 4. 清理和重置
- 在每个测试后重置Mock
- 避免测试间的干扰
- 使用beforeEach/afterEach
