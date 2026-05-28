# 单元测试模板

使用此模板生成 `docs/devdocs/03-test-unit.md`

---

```markdown
# 单元测试用例：<功能名称>

## 覆盖要求

- **行覆盖率**：≥ 80%
- **分支覆盖率**：≥ 80%

## 测试范围

| 模块/文件 | 核心函数 | 关联验收标准 |
|-----------|----------|--------------|
| `src/services/user.ts` | `validateEmail()` | AC-001, AC-002 |
| `src/services/user.ts` | `validatePassword()` | AC-004, AC-005 |
| `src/services/auth.ts` | `hashPassword()` | AC-004 |

---

## 测试用例

### F-001: <功能点名称>

#### validateEmail()

| 编号 | 验收标准 | 场景 | 输入 | 预期输出 | 优先级 |
|------|----------|------|------|----------|--------|
| UT-001 | AC-001 | 有效邮箱 | `"test@example.com"` | `true` | P0 |
| UT-002 | AC-002 | 无效格式 | `"invalid"` | `false` | P0 |
| UT-003 | AC-002 | 空字符串 | `""` | `false` | P1 |

**测试代码**：
```typescript
describe('validateEmail', () => {
  // UT-001: AC-001 - 有效邮箱
  it('应该返回 true 当邮箱格式有效', () => {
    expect(validateEmail('test@example.com')).toBe(true);
  });

  // UT-002: AC-002 - 无效格式
  it('应该返回 false 当邮箱格式无效', () => {
    expect(validateEmail('invalid')).toBe(false);
  });

  // UT-003: AC-002 - 空字符串
  it('应该返回 false 当邮箱为空', () => {
    expect(validateEmail('')).toBe(false);
  });
});
```

#### validatePassword()

| 编号 | 验收标准 | 场景 | 输入 | 预期输出 | 优先级 |
|------|----------|------|------|----------|--------|
| UT-004 | AC-004 | 长度不足 | `"short"` | `{ valid: false, error: "密码过短" }` | P0 |
| UT-005 | AC-004 | 长度足够 | `"password123"` | `{ valid: true }` | P0 |
| UT-006 | AC-005 | 缺少字母 | `"12345678"` | `{ valid: false, error: "需包含字母" }` | P0 |

---

### F-002: <功能点名称>

#### <函数名>()

| 编号 | 验收标准 | 场景 | 输入 | 预期输出 | 优先级 |
|------|----------|------|------|----------|--------|
| UT-007 | AC-006 | <场景描述> | `<输入>` | `<输出>` | P0 |

---

## Mock 策略

| 依赖 | Mock 方式 | 说明 |
|------|-----------|------|
| Database | Mock | 使用内存 Mock，不实际连接数据库 |
| External API | Stub | 返回预定义响应 |
| Logger | Spy | 验证日志调用 |
| Time | Mock | 使用 fake timers |

### Mock 示例

**数据库 Mock**：
```typescript
const mockDb = {
  query: jest.fn().mockResolvedValue([{ id: 1 }]),
  insert: jest.fn().mockResolvedValue({ insertId: 1 }),
};
```

**外部 API Stub**：
```typescript
jest.mock('./externalApi', () => ({
  fetchData: jest.fn().mockResolvedValue({ data: 'mocked' }),
}));
```

---

## 测试数据

### 工厂函数

```typescript
const createTestUser = (overrides = {}) => ({
  id: 'test-id',
  name: 'Test User',
  email: 'test@example.com',
  ...overrides,
});
```

---

## 执行命令

```bash
# 运行单元测试
npm test

# 带覆盖率
npm test -- --coverage

# 运行特定文件
npm test -- src/services/user.test.ts

# Watch 模式
npm test -- --watch
```

---

## 追溯汇总

| 编号 | 验收标准 | 测试对象 | 场景 | 状态 |
|------|----------|----------|------|------|
| UT-001 | AC-001 | validateEmail() | 有效邮箱 | ✅ |
| UT-002 | AC-002 | validateEmail() | 无效格式 | ✅ |
| UT-003 | AC-002 | validateEmail() | 空字符串 | ✅ |
| UT-004 | AC-004 | validatePassword() | 长度不足 | ✅ |
| UT-005 | AC-004 | validatePassword() | 长度足够 | ✅ |
| UT-006 | AC-005 | validatePassword() | 缺少字母 | ✅ |
```

---

## 编号规范

- **格式**：`UT-XXX`（全局顺序编号）
- **示例**：UT-001, UT-002, UT-003
- **关联**：每个用例必须关联验收标准 (AC-XXX)
