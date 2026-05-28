# E2E 测试模板

使用此模板生成 `docs/devdocs/03-test-e2e.md`

---

```markdown
# E2E 测试用例：<功能名称>

## 测试框架

- **框架**：<Playwright / Cypress>
- **语言**：<TypeScript / JavaScript>

## 覆盖要求

- 每个 P0 用户故事至少 1 个 E2E 测试
- 覆盖完整用户流程
- 验证关键验收标准

---

## 测试用例

### F-001: <功能点名称>

| 编号 | 用户故事 | 验收标准 | 测试场景 | 优先级 |
|------|----------|----------|----------|--------|
| E2E-001 | US-001 | AC-001~AC-003 | 完整注册流程 | P0 |
| E2E-002 | US-002 | AC-004, AC-005 | 密码强度校验 | P1 |

#### E2E-001: 完整注册流程

**关联**：
- 用户故事：US-001
- 验收标准：AC-001, AC-002, AC-003

**操作步骤**：
1. 打开注册页面 `/register`
2. 输入有效邮箱
3. 输入符合要求的密码
4. 点击注册按钮

**预期结果**：
- 注册成功，跳转到欢迎页
- 收到验证邮件（可选验证）

**测试代码**：
```typescript
test('E2E-001: 完整注册流程', async ({ page }) => {
  // Arrange
  const testEmail = `test-${Date.now()}@example.com`;

  // Act
  await page.goto('/register');
  await page.fill('[data-testid="email"]', testEmail);
  await page.fill('[data-testid="password"]', 'SecurePass123!');
  await page.click('[data-testid="submit"]');

  // Assert - AC-001: 注册成功
  await expect(page).toHaveURL('/welcome');
  await expect(page.locator('[data-testid="welcome-message"]')).toBeVisible();
});
```

---

### F-002: <功能点名称>

| 编号 | 用户故事 | 验收标准 | 测试场景 | 优先级 |
|------|----------|----------|----------|--------|
| E2E-003 | US-003 | AC-006~AC-008 | 完整登录流程 | P0 |

#### E2E-003: 完整登录流程

**关联**：
- 用户故事：US-003
- 验收标准：AC-006, AC-007, AC-008

**操作步骤**：
1. 打开登录页面 `/login`
2. 输入已注册邮箱
3. 输入正确密码
4. 点击登录按钮

**预期结果**：
- 登录成功，跳转到首页
- 显示用户信息

**测试代码**：
```typescript
test('E2E-003: 完整登录流程', async ({ page }) => {
  // Arrange - 确保用户已存在
  const user = await createTestUser();

  // Act
  await page.goto('/login');
  await page.fill('[data-testid="email"]', user.email);
  await page.fill('[data-testid="password"]', user.password);
  await page.click('[data-testid="submit"]');

  // Assert - AC-006: 登录成功
  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('[data-testid="user-name"]')).toHaveText(user.name);
});
```

---

## 测试数据管理

### 数据准备

| 场景 | 所需数据 | 准备方式 | 清理方式 |
|------|----------|----------|----------|
| 登录 | 测试用户 | API 预创建 | 测试后删除 |
| 注册 | 无 | - | 删除测试用户 |

### 数据隔离

```typescript
test.beforeEach(async ({ request }) => {
  // 创建隔离的测试数据
  const user = await request.post('/api/test/users', {
    data: { email: `test-${Date.now()}@example.com` }
  });
  testUserId = user.id;
});

test.afterEach(async ({ request }) => {
  // 清理测试数据
  await request.delete(`/api/test/users/${testUserId}`);
});
```

---

## Page Object 模式

### 目录结构

```
tests/
├── e2e/
│   ├── pages/
│   │   ├── LoginPage.ts
│   │   ├── RegisterPage.ts
│   │   └── DashboardPage.ts
│   ├── fixtures/
│   │   └── test-data.ts
│   └── specs/
│       ├── auth.spec.ts
│       └── user.spec.ts
```

### Page Object 示例

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.fill('[data-testid="email"]', email);
    await this.page.fill('[data-testid="password"]', password);
    await this.page.click('[data-testid="submit"]');
  }

  async expectError(message: string) {
    await expect(this.page.locator('.error')).toHaveText(message);
  }
}
```

---

## 执行命令

```bash
# 运行所有 E2E 测试
npx playwright test

# 运行特定文件
npx playwright test tests/e2e/auth.spec.ts

# UI 模式
npx playwright test --ui

# 指定浏览器
npx playwright test --project=chromium

# 生成报告
npx playwright show-report
```

---

## 追溯汇总

| 编号 | 用户故事 | 验收标准 | 测试场景 | 状态 |
|------|----------|----------|----------|------|
| E2E-001 | US-001 | AC-001~AC-003 | 完整注册流程 | ✅ |
| E2E-002 | US-002 | AC-004, AC-005 | 密码强度校验 | ✅ |
| E2E-003 | US-003 | AC-006~AC-008 | 完整登录流程 | ✅ |
```

---

## 编号规范

- **格式**：`E2E-XXX`（全局顺序编号）
- **示例**：E2E-001, E2E-002, E2E-003
- **关联**：每个用例必须关联用户故事 (US-XXX) 和验收标准 (AC-XXX)
