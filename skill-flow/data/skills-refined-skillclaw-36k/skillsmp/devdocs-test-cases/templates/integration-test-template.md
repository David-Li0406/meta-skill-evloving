# 集成测试模板

使用此模板生成 `docs/devdocs/03-test-integration.md`

---

```markdown
# 集成测试用例：<功能名称>

## 测试范围

集成测试验证多个组件协作的正确性，包括：
- 服务间调用
- 数据库操作
- 外部服务集成（邮件、支付等）
- API 端到端调用

## 覆盖要求

- 每个功能点至少 1 个集成测试
- 覆盖核心业务流程
- 验证组件间数据传递

---

## 测试用例

### F-001: <功能点名称>

| 编号 | 验收标准 | 测试场景 | 涉及组件 | 预期结果 | 优先级 |
|------|----------|----------|----------|----------|--------|
| IT-001 | AC-003 | <场景描述> | <组件A + 组件B> | <预期结果> | P0 |

**测试步骤**：
1. <准备步骤>
2. <执行步骤>
3. <验证步骤>

**测试代码示例**：
```typescript
describe('IT-001: <测试场景>', () => {
  it('应该 <预期行为> 当 <条件>', async () => {
    // Arrange
    const user = await createTestUser();

    // Act
    const result = await userService.register(user);

    // Assert
    expect(result.id).toBeDefined();
    const savedUser = await db.users.findById(result.id);
    expect(savedUser.email).toBe(user.email);
  });
});
```

---

### F-002: <功能点名称>

| 编号 | 验收标准 | 测试场景 | 涉及组件 | 预期结果 | 优先级 |
|------|----------|----------|----------|----------|--------|
| IT-002 | AC-006 | <场景描述> | <组件A + 组件B> | <预期结果> | P0 |

---

## Mock 策略

集成测试中的 Mock 策略：

| 组件类型 | 策略 | 说明 |
|----------|------|------|
| 数据库 | 真实连接 | 使用测试数据库 |
| 内部服务 | 真实调用 | 验证服务间协作 |
| 外部 API | Mock/Stub | 使用 nock/msw 模拟 |
| 邮件服务 | Mock | 验证调用参数，不实际发送 |

### 外部服务 Mock 示例

```typescript
// 使用 msw 模拟外部 API
import { rest } from 'msw';

const handlers = [
  rest.post('https://api.email.com/send', (req, res, ctx) => {
    return res(ctx.json({ messageId: 'mock-id' }));
  }),
];
```

---

## 测试数据管理

### 数据隔离

```typescript
beforeEach(async () => {
  // 清理测试数据
  await db.users.deleteMany({ email: /@test\.com$/ });
});

afterAll(async () => {
  // 关闭连接
  await db.disconnect();
});
```

### 测试数据工厂

```typescript
const createTestUser = (overrides = {}) => ({
  email: `test-${Date.now()}@test.com`,
  password: 'TestPass123!',
  ...overrides,
});
```

---

## 执行命令

```bash
# 运行集成测试
npm run test:integration

# 运行特定文件
npm run test:integration -- auth.integration.test.ts

# 带覆盖率
npm run test:integration -- --coverage
```

---

## 追溯汇总

| 编号 | 验收标准 | 测试场景 | 状态 |
|------|----------|----------|------|
| IT-001 | AC-003 | <场景> | ✅ |
| IT-002 | AC-006 | <场景> | ✅ |
```

---

## 示例：用户认证功能

```markdown
# 集成测试用例：用户认证

## 测试范围

- UserService + Database：用户数据持久化
- AuthService + EmailService：认证邮件发送
- TokenService + Database：Token 存储和验证

---

## 测试用例

### F-001: 用户注册

| 编号 | 验收标准 | 测试场景 | 涉及组件 | 预期结果 | 优先级 |
|------|----------|----------|----------|----------|--------|
| IT-001 | AC-003 | 注册后发送验证邮件 | UserService + EmailService + DB | 用户创建成功，邮件发送调用正确 | P0 |

**测试代码**：
```typescript
describe('IT-001: 注册后发送验证邮件', () => {
  const mockEmailService = {
    sendVerificationEmail: jest.fn().mockResolvedValue({ messageId: 'test' }),
  };

  it('应该创建用户并发送验证邮件', async () => {
    // Arrange
    const userData = createTestUser();

    // Act
    const user = await userService.register(userData);

    // Assert - 用户已创建
    const savedUser = await db.users.findById(user.id);
    expect(savedUser).not.toBeNull();
    expect(savedUser.email).toBe(userData.email);

    // Assert - 邮件已发送
    expect(mockEmailService.sendVerificationEmail).toHaveBeenCalledWith(
      expect.objectContaining({ email: userData.email })
    );
  });
});
```

---

### F-002: 用户登录

| 编号 | 验收标准 | 测试场景 | 涉及组件 | 预期结果 | 优先级 |
|------|----------|----------|----------|----------|--------|
| IT-002 | AC-006~AC-008 | 完整登录流程 | AuthService + UserService + TokenService | 返回有效 Token，刷新 Token 存储 | P0 |

**测试代码**：
```typescript
describe('IT-002: 完整登录流程', () => {
  it('应该返回有效 Token 当凭证正确', async () => {
    // Arrange
    const user = await createAndSaveTestUser();

    // Act
    const result = await authService.login(user.email, 'TestPass123!');

    // Assert
    expect(result.accessToken).toBeDefined();
    expect(result.refreshToken).toBeDefined();

    // 验证 Token 已存储
    const storedToken = await db.refreshTokens.findOne({ userId: user.id });
    expect(storedToken).not.toBeNull();
  });

  it('应该锁定账号当连续失败 5 次', async () => {
    // Arrange
    const user = await createAndSaveTestUser();

    // Act - 连续 5 次错误密码
    for (let i = 0; i < 5; i++) {
      await authService.login(user.email, 'WrongPassword').catch(() => {});
    }

    // Assert
    const lockedUser = await db.users.findById(user.id);
    expect(lockedUser.lockedUntil).toBeDefined();
    expect(lockedUser.lockedUntil.getTime()).toBeGreaterThan(Date.now());
  });
});
```

---

### F-003: 密码找回

| 编号 | 验收标准 | 测试场景 | 涉及组件 | 预期结果 | 优先级 |
|------|----------|----------|----------|----------|--------|
| IT-003 | AC-011~AC-013 | 密码重置流程 | AuthService + EmailService + TokenService | Token 生成、邮件发送、密码更新 | P1 |

---

## 追溯汇总

| 编号 | 验收标准 | 测试场景 | 状态 |
|------|----------|----------|------|
| IT-001 | AC-003 | 注册后发送验证邮件 | ✅ |
| IT-002 | AC-006~AC-008 | 完整登录流程 | ✅ |
| IT-003 | AC-011~AC-013 | 密码重置流程 | ✅ |
```
