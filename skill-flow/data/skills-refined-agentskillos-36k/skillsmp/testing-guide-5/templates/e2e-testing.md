# E2E 测试指南

## E2E 测试的关注点

E2E 测试验证**用户场景**，从用户视角验证系统行为。

```
E2E 测试 = 用户能完成他们的目标

关注:
✅ 用户能否完成核心流程
✅ 页面交互是否正确
✅ 数据是否正确保存和展示
✅ 错误提示是否清晰

不关注:
❌ 内部实现细节
❌ 单个组件的边界条件
❌ API 的详细响应结构
```

## 场景优先级

| 优先级 | 场景类型 | 覆盖要求 | 示例 |
|--------|----------|----------|------|
| **P0** | 核心业务流程 | 100% | 注册、登录、支付、核心功能 |
| **P1** | 重要功能 | ≥80% | 搜索、筛选、设置 |
| **P2** | 辅助功能 | 可选 | 帮助页面、偏好设置 |

## 测试粒度

```typescript
// ❌ 粒度太细：像单元测试
test('登录按钮应该有正确的文本', () => {
  expect(page.locator('button')).toHaveText('登录');
});

// ❌ 粒度太粗：一个测试做太多事
test('用户流程', async () => {
  await register();
  await login();
  await createOrder();
  await pay();
  await viewHistory();
});

// ✅ 合适的粒度：一个用户目标
test('新用户应该能够完成注册流程', async () => {
  await page.goto('/register');
  await page.fill('[name="email"]', 'test@example.com');
  await page.fill('[name="password"]', 'SecurePass123');
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL('/dashboard');
  await expect(page.locator('.welcome')).toContainText('欢迎');
});
```

## 测试可靠性

### 等待策略

```typescript
// ❌ 不可靠：硬编码等待时间
await page.click('button');
await page.waitForTimeout(3000);  // 可能太短或太长

// ✅ 可靠：等待具体条件
await page.click('button');
await page.waitForSelector('.success-message');
await expect(page.locator('.success-message')).toBeVisible();

// ✅ 更好：使用自动等待
await page.click('button');
await expect(page.locator('.result')).toHaveText('完成', {
  timeout: 10000,  // 最大等待时间
});
```

### 选择器策略

```typescript
// ❌ 脆弱的选择器
await page.click('.btn-primary');  // 样式可能变化
await page.click('div > div > button');  // 结构可能变化

// ✅ 稳定的选择器
await page.click('[data-testid="submit-button"]');
await page.click('button[type="submit"]');
await page.getByRole('button', { name: '提交' });
```

## 测试数据策略

```
E2E 测试数据原则:

1. 测试数据独立
   - 每个测试使用唯一数据
   - 不依赖其他测试创建的数据

2. 测试后清理
   - 使用 API 清理测试数据
   - 或使用专门的测试账号

3. 避免测试间依赖
   - 测试可以独立运行
   - 测试顺序不影响结果
```

### 数据隔离示例

```typescript
describe('Order', () => {
  let testUser: User;

  beforeEach(async () => {
    // 每个测试创建独立用户
    testUser = await api.createTestUser({
      email: `test-${Date.now()}@example.com`,
    });
    await loginAs(testUser);
  });

  afterEach(async () => {
    // 清理测试数据
    await api.deleteUser(testUser.id);
  });

  test('should create order', async () => {
    // 使用独立的测试用户
  });
});
```

## Playwright 示例

```typescript
import { test, expect } from '@playwright/test';

test.describe('用户登录', () => {
  test('应该成功登录并跳转到仪表盘', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[data-testid="email"]', 'user@example.com');
    await page.fill('[data-testid="password"]', 'password123');
    await page.click('[data-testid="login-button"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="user-name"]')).toHaveText('User');
  });

  test('应该显示错误信息当密码错误', async ({ page }) => {
    await page.goto('/login');

    await page.fill('[data-testid="email"]', 'user@example.com');
    await page.fill('[data-testid="password"]', 'wrongpassword');
    await page.click('[data-testid="login-button"]');

    await expect(page.locator('[data-testid="error-message"]'))
      .toHaveText('用户名或密码错误');
    await expect(page).toHaveURL('/login');
  });
});
```

## Cypress 示例

```typescript
describe('购物车', () => {
  beforeEach(() => {
    cy.login('user@example.com', 'password');
    cy.visit('/products');
  });

  it('应该添加商品到购物车', () => {
    cy.get('[data-testid="product-card"]').first().click();
    cy.get('[data-testid="add-to-cart"]').click();

    cy.get('[data-testid="cart-count"]').should('have.text', '1');
  });

  it('应该从购物车移除商品', () => {
    // 先添加商品
    cy.get('[data-testid="product-card"]').first().click();
    cy.get('[data-testid="add-to-cart"]').click();

    // 打开购物车
    cy.get('[data-testid="cart-icon"]').click();
    cy.get('[data-testid="remove-item"]').click();

    cy.get('[data-testid="cart-empty"]').should('be.visible');
  });
});
```

## Page Object 模式

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
    await this.page.click('[data-testid="login-button"]');
  }

  async getErrorMessage() {
    return this.page.locator('[data-testid="error-message"]');
  }
}

// tests/login.spec.ts
test('登录测试', async ({ page }) => {
  const loginPage = new LoginPage(page);

  await loginPage.goto();
  await loginPage.login('user@example.com', 'password');

  await expect(page).toHaveURL('/dashboard');
});
```

## 视觉回归测试

```typescript
test('首页应该匹配快照', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png');
});

test('登录表单应该匹配快照', async ({ page }) => {
  await page.goto('/login');
  await expect(page.locator('form')).toHaveScreenshot('login-form.png');
});
```

## CI 配置要点

```yaml
# 并行运行
- run: npx playwright test --workers=4

# 重试失败的测试
- run: npx playwright test --retries=2

# 只在 PR 时运行 E2E
- if: github.event_name == 'pull_request'
  run: npx playwright test

# 保存失败截图
- uses: actions/upload-artifact@v3
  if: failure()
  with:
    name: playwright-screenshots
    path: test-results/
```
