---
name: assertion-helper
description: 分析函数逻辑并生成合适的断言。
---

# 断言助手技能

这个技能负责分析函数逻辑并生成合适的断言，确保测试能够准确验证代码的行为。

## 技能能力

### 1. 逻辑分析
- 分析函数的返回值类型和结构
- 识别可能的输出范围
- 检测副作用（如状态修改、事件触发）
- 分析异常和错误情况

### 2. 断言生成
- 生成精确的类型断言
- 创建边界值验证
- 生成深度对象比较
- 添加函数调用验证

### 3. 验证策略
- 精确匹配 vs 模糊匹配
- 部分对象匹配
- 数组包含和顺序验证
- 异常断言

## 使用方式

### 基础断言生成

```typescript
// 为函数生成断言
await generateAssertions('calculateTotal', {
  inputs: [{ items: [{ price: 10, qty: 2 }] }],
  framework: 'vitest'
});

// 生成类方法的断言
await generateAssertions('UserService.createUser', {
  context: 'class',
  framework: 'vitest'
});
```

### 高级选项

```typescript
await generateAssertions(target, {
  framework: 'pytest',
  assertionStyle: 'strict', // 'strict' | 'loose' | 'custom'
  includeSideEffects: true,
  verifyMocks: true,
  customAssertions: {
    'shouldBeValidUser': 'expect(user).toMatchObject({ id: expect.any(Number), name: expect.any(String) })'
  }
});
```

## 断言模板

### Jest断言模板

```javascript
// 基础类型断言
{{#if returns}}
{{#eq returns.type 'string'}}
expect(result).toBeString();
expect(result).toHaveLength({{#if returns.length}}{{returns.length}}{{else}}greaterThan(0){{/if}});
{{/eq}}

{{#eq returns.type 'number'}}
expect(result).toBeNumber();
expect(result).{{#if returns.range}}toBeGreaterThanOrEqual({{returns.range.min}});
expect(result).toBeLessThanOrEqual({{returns.range.max}});{{/if}}
{{/eq}}

{{#eq returns.type 'boolean'}}
expect(result).toBeBoolean();
{{/eq}}

{{#eq returns.type 'array'}}
expect(result).toBeArray();
expect(result).toHaveLength({{#if returns.length}}{{returns.length}}{{else}}greaterThan(0){{/if}});
{{#if returns.items}}
expect(result[0]).toMatchObject({{{json returns.items}}});
{{/if}}
{{/eq}}

{{#eq returns.type 'object'}}
expect(result).toBeObject();
{{#if returns.properties}}
expect(result).toMatchObject({
{{#each returns.properties}}
  {{@key}}: {{#if this.type}}expect.any({{camelCase this.type}}){{else}}{{{json this}}}{{/if}},
{{/each}}
});
{{/if}}
{{/eq}}
{{/if}}

// 异步断言
{{#if isAsync}}
await expect(asyncFunction()).resolves.toBe(expectedValue);
await expect(asyncFunction()).resolves.not.toThrow();

// 错误断言
await expect(asyncFunction()).rejects.toThrow('Expected error message');
{{/if}}

// Mock验证断言
{{#each mocks}}
{{#if this.shouldBeCalled}}
expect({{name}}).toHaveBeenCalled();
expect({{name}}).toHaveBeenCalledTimes({{this.callCount}});
{{#if this.withParams}}
expect({{name}}).toHaveBeenCalledWith({{#each this.withParams}}{{this}}{{#unless @last}}, {{/unless}}{{/each}});
{{/if}}
{{else}}
expect({{name}}).not.toHaveBeenCalled();
{{/if}}
{{/each}}

// 副作用验证
{{#if sideEffects}}
{{#each sideEffects}}
{{#eq this.type 'console'}}
// Console输出验证
expect(console.{{this.method}}).toHaveBeenCalledWith({{{json this.args}}});
{{/eq}}

{{#eq this.type 'event'}}
// 事件触发验证
expect(eventEmitter.emit).toHaveBeenCalledWith('{{this.eventName}}', {{#if this.payload}}{{{json this.payload}}}{{else}}expect.any(Object){{/if}});
{{/eq}}

{{#eq this.type 'state'}}
// 状态变化验证
expect(component.state.{{this.property}}).toBe({{{json this.value}}});
{{/eq}}
{{/each}}
{{/if}}
```

### Vitest断言模板

```typescript
import { expect } from 'vitest';

// 类型断言
{{#if returns}}
expect(result).toBeDefined();
{{#eq returns.type 'string'}}
expect(typeof result).toBe('string');
{{/eq}}

{{#eq returns.type 'number'}}
expect(typeof result).toBe('number');
{{/eq}}

{{#eq returns.type 'object'}}
expect(typeof result).toBe('object');
expect(result).not.toBeNull();
{{/eq}}
{{/if}}

// 精确匹配
expect(result).toEqual(expectedValue);

// 部分匹配
expect(result).toMatchObject(partialExpected);

// 数组断言
expect(result).toContain(expectedItem);
expect(result).toHaveLength(expectedLength);

// 异常断言
expect(() => functionThatThrows()).toThrow();
expect(() => functionThatThrows()).toThrowError('Error message');
```

### Python断言模板

```python
# 基础断言
assert result is not None
{{#eq returns.type 'string'}}
assert isinstance(result, str)
assert len(result) > 0
{{/eq}}

{{#eq returns.type 'number'}}
assert isinstance(result, (int, float))
assert result >= {{#if returns.min}}{{returns.min}}{{else}}0{{/if}}
{{/eq}}

{{#eq returns.type 'list'}}
assert isinstance(result, list)
assert len(result) > 0
{{#if returns.items}}
assert result[0] == {{returns.items}}
{{/if}}
{{/eq}}

{{#eq returns.type 'dict'}}
assert isinstance(result, dict)
{{#if returns.keys}}
for key in {{json returns.keys}}:
    assert key in result
{{/if}}
{{/eq}}

# 异常断言
with pytest.raises({{errorType}}, match="{{errorMessage}}"):
    function_that_raises()

# Mock验证
{{#each mocks}}
{{#if this.shouldBeCalled}}
assert {{name}}.called
assert {{name}}.call_count == {{this.callCount}}
{{#if this.withArgs}}
{{name}}.assert_called_with({{#each this.withArgs}}{{this}}{{#unless @last}}, {{/unless}}{{/each}})
{{/if}}
{{else}}
assert not {{name}}.called
{{/if}}
{{/each}}
```

## 断言生成策略

### 1. 基于返回值的断言

```typescript
class AssertionGenerator {
  static generateForReturn(returnType: TypeInfo, value?: any): string[] {
    const assertions: string[] = [];

    // 类型断言
    switch (returnType.type) {
      case 'string':
        assertions.push('expect(typeof result).toBe("string")');
        if (value) {
          assertions.push(`expect(result).toBe("${value}")`);
        }
        break;

      case 'number':
        assertions.push('expect(typeof result).toBe("number")');
        if (returnType.constraints?.min !== undefined) {
          assertions.push(`expect(result).toBeGreaterThanOrEqual(${returnType.constraints.min})`);
        }
        if (returnType.constraints?.max !== undefined) {
          assertions.push(`expect(result).toBeLessThanOrEqual(${returnType.constraints.max})`);
        }
        break;

      case 'boolean':
        assertions.push('expect(typeof result).toBe("boolean")');
        break;

      case 'array':
        assertions.push('expect(Array.isArray(result)).toBe(true)');
        if (value?.length) {
          assertions.push(`expect(result).toHaveLength(${value.length})`);
        }
        break;

      case 'object':
        assertions.push('expect(typeof result).toBe("object")');
        assertions.push('expect(result).not.toBeNull()');
        if (value) {
          assertions.push(`expect(result).toMatchObject(${JSON.stringify(value)})`);
        }
        break;
    }

    return assertions;
  }

  static generateBoundaryTests(
    functionName: string,
    params: ParameterInfo[]
  ): string[] {
    const tests: string[] = [];

    params.forEach(param => {
      if (param.constraints?.min !== undefined) {
        tests.push(`
it('should handle minimum value for ${param.name}', () => {
  const result = ${functionName}(${param.constraints.min});
  expect(result).toBeDefined();
});
        `);
      }

      if (param.constraints?.max !== undefined) {
        tests.push(`
it('should handle maximum value for ${param.name}', () => {
  const result = ${functionName}(${param.constraints.max});
  expect(result).toBeDefined();
});
        `);
      }
    });

    return tests;
  }
}
```

### 2. 错误处理断言

```javascript
// 错误场景断言生成
function generateErrorAssertions(functionInfo) {
  const assertions = [];

  // 可能的错误条件
  if (functionInfo.params.some(p => p.required)) {
    assertions.push(`
it('should throw error when required parameter is missing', () => {
  expect(() => ${functionInfo.name}()).toThrow();
  expect(() => ${functionInfo.name}(null)).toThrow();
});
    `);
  }

  if (functionInfo.params.some(p => p.type === 'number')) {
    assertions.push(`
it('should handle invalid number inputs', () => {
  expect(() => ${functionInfo.name}(NaN)).toThrow();
  expect(() => ${functionInfo.name}(Infinity)).toThrow();
});
    `);
  }

  return assertions;
}
```

### 3. 异步操作断言

```javascript
// 异步函数断言生成
function generateAsyncAssertions(functionInfo) {
  return `
describe('async behavior', () => {
  it('should resolve with expected value', async () => {
    const result = await ${functionInfo.name}(${generateValidParams(functionInfo)});
    expect(result).toBeDefined();
    ${generateReturnAssertions(functionInfo.returnType)}
  });

  it('should handle rejection', async () => {
    // 测试拒绝情况
    await expect(${functionInfo.name}(${generateErrorParams()}))
      .rejects.toThrow();
  });

  it('should handle timeout', async () => {
    // 如果有超时配置
    await expect(${functionInfo.name}(${generateSlowParams()}))
      .rejects.toThrow('timeout');
  });
});
  `;
}
```

## 复杂场景处理

### 1. 深度对象比较

```javascript
// 深度匹配断言
function generateDeepObjectAssertions(obj: any, path: string = ''): string[] {
  const assertions: string[] = [];

  for (const [key, value] of Object.entries(obj)) {
    const currentPath = path ? `${path}.${key}` : key;

    if (typeof value === 'object' && value !== null) {
      if (Array.isArray(value)) {
        assertions.push(`
expect(result.${currentPath}).toBeArray();
expect(result.${currentPath}).toHaveLength(${value.length});
        `);
      } else {
        assertions.push(`
expect(result.${currentPath}).toBeObject();
        `);
        // 递归处理嵌套对象
        assertions.push(...generateDeepObjectAssertions(value, currentPath));
      }
    } else {
      assertions.push(`
expect(result.${currentPath}).toBe(${JSON.stringify(value)});
      `);
    }
  }

  return assertions;
}
```

### 2. 函数调用验证

```javascript
// Mock函数调用断言
function generateMockAssertions(mocks: MockInfo[]): string[] {
  return mocks.map(mock => {
    const assertions: string[] = [];

    if (mock.expectCall) {
      assertions.push(`expect(${mock.name}).toHaveBeenCalled();`);

      if (mock.expectedCallCount) {
        assertions.push(
          `expect(${mock.name}).toHaveBeenCalledTimes(${mock.expectedCallCount});`
        );
      }

      if (mock.expectedArgs) {
        assertions.push(
          `expect(${mock.name}).toHaveBeenCalledWith(${mock.expectedArgs.join(', ')});`
        );
      }

      if (mock.expectedCalls) {
        mock.expectedCalls.forEach((call, index) => {
          assertions.push(
            `expect(${mock.name}).toHaveBeenNthCalledWith(${index + 1}, ${call.join(', ')});`
          );
        });
      }
    } else {
      assertions.push(`expect(${mock.name}).not.toHaveBeenCalled();`);
    }

    return assertions.join('\n');
  });
}
```

### 3. 副作用验证

```javascript
// 副作用断言生成
function generateSideEffectAssertions(sideEffects: SideEffect[]): string[] {
  return sideEffects.map(effect => {
    switch (effect.type) {
      case 'console':
        return `expect(console.${effect.method}).toHaveBeenCalledWith(${JSON.stringify(effect.args)});`;

      case 'state':
        return `expect(${effect.target}).toBe(${JSON.stringify(effect.value)});`;

      case 'event':
        return `expect(${effect.emitter}.emit).toHaveBeenCalledWith('${effect.event}', ${JSON.stringify(effect.payload)});`;

      case 'storage':
        return `expect(localStorage.getItem('${effect.key}')).toBe('${effect.value}');`;

      default:
        return '';
    }
  }).filter(Boolean);
}
```

## 最佳实践

### 1. 断言选择原则
- 使用最具体的断言
- 避免过度脆弱的断言
- 关注行为而非实现
- 一个测试一个关注点

### 2. 断言可读性
- 使用有意义的变量名
- 添加描述性注释
- 组织相关断言
- 使用自定义匹配器

### 3. 测试覆盖
- 覆盖正常路径
- 测试边界条件
- 验证错误处理
- 检查副作用

### 4. 断言维护
- 保持断言独立
- 避免重复断言
- 使用辅助函数
- 定期更新断言
