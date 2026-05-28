---
name: test-generation
description: 分析源代码并生成对应的单元测试用例。
---

# 单元测试生成技能

这个技能负责分析源代码并生成对应的单元测试用例。支持多种编程语言和测试框架。

## 核心能力

### 1. 代码分析
- AST解析，识别函数、类、方法
- 分析函数签名和参数类型
- 识别依赖关系和导入模块
- 检测异步函数和Promise使用

### 2. 测试场景生成
- 正常流程测试（Happy Path）
- 边界条件测试（Boundary Values）
- 异常情况测试（Error Cases）
- 参数验证测试

### 3. 测试代码生成
- 根据选择的框架生成测试代码
- 生成合适的测试名称和描述
- 添加必要的设置和清理代码
- 生成有意义的断言

## 支持的框架

### JavaScript/TypeScript
- **Jest** - 最流行的JavaScript测试框架
- **Vitest** - 现代化的Vite原生测试框架
- **Mocha** - 灵活的测试框架
- **Jasmine** - 行为驱动的开发框架

### Python
- **pytest** - 功能强大的测试框架
- **unittest** - Python标准库测试框架
- **nose2** - unittest的扩展

### Java
- **JUnit 5** - 现代Java测试框架
- **TestNG** - 测试下一代框架
- **Mockito** - 强大的Mock框架

### 其他语言
- Go (testing)
- C# (xUnit, NUnit)
- Ruby (RSpec, Minitest)

## 使用方法

### 基础使用
```bash
# 生成单个函数的测试
/test src/utils/calculator.js --function add --framework vitest

# 生成整个文件的测试
/test src/services/userService.js --framework jest --mocks
```

### 高级选项
```bash
# 包含覆盖率分析
/test src/api/userController.js --framework jest --coverage

# 生成边界值测试
/test src/utils/validator.js --edge-cases

# 只生成异常测试
/test src/services/payment.js --error-only
```

## 测试模板示例

### JavaScript/TypeScript - Vitest
```typescript
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { UserService } from '../src/services/UserService';

describe('UserService', () => {
  let userService: UserService;
  let mockDb: any;

  beforeEach(() => {
    mockDb = {
      find: vi.fn(),
      create: vi.fn(),
      update: vi.fn(),
      delete: vi.fn()
    };
    userService = new UserService(mockDb);
  });

  describe('getUserById', () => {
    it('should return user when found', async () => {
      // Arrange
      const userId = '123';
      const expectedUser = { id: userId, name: 'John' };
      mockDb.find.mockResolvedValue(expectedUser);

      // Act
      const result = await userService.getUserById(userId);

      // Assert
      expect(result).toEqual(expectedUser);
      expect(mockDb.find).toHaveBeenCalledWith({ id: userId });
    });

    it('should return null when user not found', async () => {
      // Arrange
      const userId = '999';
      mockDb.find.mockResolvedValue(null);

      // Act
      const result = await userService.getUserById(userId);

      // Assert
      expect(result).toBeNull();
    });
  });
});
```

### Python - pytest
```python
import pytest
from unittest.mock import Mock, patch
from services.user_service import UserService

class TestUserService:
    @pytest.fixture
    def user_service(self):
        with patch('services.user_service.Database') as mock_db:
            yield UserService(mock_db)

    def test_get_user_by_id_success(self, user_service):
        """Test getting user with valid ID"""
        # Arrange
        user_id = 123
        expected_user = {"id": user_id, "name": "John"}
        user_service.db.find.return_value = expected_user

        # Act
        result = user_service.get_user_by_id(user_id)

        # Assert
        assert result == expected_user
        user_service.db.find.assert_called_once_with({"id": user_id})

    def test_get_user_by_id_not_found(self, user_service):
        """Test getting non-existent user"""
        # Arrange
        user_id = 999
        user_service.db.find.return_value = None

        # Act
        result = user_service.get_user_by_id(user_id)

        # Assert
        assert result is None
```

## 测试数据生成

### 自动生成测试数据
```typescript
// 根据类型生成测试数据
const testData = {
  string: ["hello", "", "a".repeat(255), "特殊字符"],
  number: [0, 1, -1, 100, Number.MAX_SAFE_INTEGER],
  boolean: [true, false],
  array: [[], [1], [1, 2, 3], Array(1000).fill(0)],
  object: [{}, { key: "value" }, null, undefined]
};

// 边界值生成
const boundaries = {
  string: ["", "a", "a".repeat(255), "a".repeat(256)],
  number: [Number.MIN_VALUE, -1, 0, 1, Number.MAX_VALUE],
  array: [[] , [1], [1000]],
};
```

## Mock策略

### 自动Mock外部依赖
- 识别外部模块导入
- 自动生成Mock代码
- 配置Mock返回值
- 验证Mock调用

### Mock示例
```typescript
// 自动生成的Mock
jest.mock('../src/utils/logger', () => ({
  logger: {
    info: jest.fn(),
    error: jest.fn(),
    warn: jest.fn()
  }
}));

// 测试中验证Mock调用
expect(logger.info).toHaveBeenCalledWith('User created successfully');
```

## 覆盖率优化

### 智能测试补充
- 分析代码覆盖率报告
- 识别未测试的分支
- 自动生成补充测试用例
- 优化测试数据组合

### 覆盖率目标
- 语句覆盖率 > 90%
- 分支覆盖率 > 85%
- 函数覆盖率 > 95%
- 行覆盖率 > 90%

## 最佳实践

### 1. 测试命名规范
```typescript
// ✅ 好的命名
it('should create user with valid data');
it('should throw error when email already exists');

// ❌ 避免的命名
it('test1');
it('user creation test');
```

### 2. AAA模式
```typescript
it('should calculate discount correctly', () => {
  // Arrange - 准备测试数据
  const price = 100;
  const discountRate = 0.1;

  // Act - 执行被测代码
  const result = calculateDiscount(price, discountRate);

  // Assert - 验证结果
  expect(result).toBe(90);
});
```

### 3. 测试隔离
- 每个测试独立运行
- 使用beforeEach/afterEach清理
- 避免测试间的依赖

### 4. 有意义的断言
```typescript
// ✅ 具体的断言
expect(user.email).toMatch(/^[^\s@]+@[^\s@]+\.[^\s@]+$/);

// ❌ 模糊的断言
expect(user).toBeDefined();
```

## 常见问题处理

### 1. 异步代码测试
```typescript
// Promise
it('should resolve with data', async () => {
  const result = await fetchData();
  expect(result).toEqual(expectedData);
});

// Callback
it('should call callback', (done) => {
  fetchData((data) => {
    expect(data).toBeDefined();
    done();
  });
});
```

### 2. 错误处理测试
```typescript
it('should throw error for invalid input', () => {
  expect(() => validateEmail('invalid')).toThrow();
});

it('should reject promise on error', async () => {
  await expect(asyncOperation()).rejects.toThrow('Error message');
});
```

### 3. 时间相关测试
```typescript
// 使用假时间
beforeEach(() => {
  vi.useFakeTimers();
});

afterEach(() => {
  vi.useRealTimers();
});

it('should debounce function calls', async () => {
  const debouncedFn = debounce(originalFn, 100);

  debouncedFn();
  vi.advanceTimersByTime(50);
  expect(originalFn).not.toHaveBeenCalled();

  vi.advanceTimersByTime(50);
  expect(originalFn).toHaveBeenCalledTimes(1);
});
```

## 集成命令

这个技能与其他命令集成：
- `/test` - 生成测试用例
- `/mock` - 生成Mock数据
- `/coverage` - 分析测试覆盖率

通过智能分析和模板化生成，帮助开发者快速编写高质量的单元测试。
