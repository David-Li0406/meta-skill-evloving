# 测试代码示例

各种常见场景的测试代码示例，展示如何编写有效的测试。

---

## 单元测试示例

### 纯函数测试

```typescript
// src/utils/calculator.ts
export function calculateDiscount(total: number, couponCode?: string): number {
  if (total <= 0) {
    throw new Error('Total must be positive');
  }

  let discount = 0;

  // 阶梯折扣
  if (total >= 1000) {
    discount = 0.1;
  } else if (total >= 500) {
    discount = 0.05;
  }

  // 优惠券额外折扣
  if (couponCode === 'VIP20') {
    discount += 0.2;
  } else if (couponCode === 'NEW10') {
    discount += 0.1;
  }

  return Math.min(discount, 0.3); // 最高30%折扣
}

// src/utils/calculator.test.ts
import { calculateDiscount } from './calculator';

describe('calculateDiscount', () => {
  describe('阶梯折扣', () => {
    it('应该返回 0% 折扣当金额小于 500', () => {
      expect(calculateDiscount(499)).toBe(0);
      expect(calculateDiscount(100)).toBe(0);
    });

    it('应该返回 5% 折扣当金额在 500-999 之间', () => {
      expect(calculateDiscount(500)).toBe(0.05);
      expect(calculateDiscount(999)).toBe(0.05);
    });

    it('应该返回 10% 折扣当金额大于等于 1000', () => {
      expect(calculateDiscount(1000)).toBe(0.1);
      expect(calculateDiscount(5000)).toBe(0.1);
    });
  });

  describe('优惠券折扣', () => {
    it('应该叠加 VIP20 优惠券的 20% 折扣', () => {
      expect(calculateDiscount(100, 'VIP20')).toBe(0.2);
      expect(calculateDiscount(1000, 'VIP20')).toBe(0.3); // 10% + 20% = 30%
    });

    it('应该叠加 NEW10 优惠券的 10% 折扣', () => {
      expect(calculateDiscount(100, 'NEW10')).toBe(0.1);
      expect(calculateDiscount(500, 'NEW10')).toBe(0.15); // 5% + 10% = 15%
    });

    it('应该忽略无效的优惠券', () => {
      expect(calculateDiscount(1000, 'INVALID')).toBe(0.1);
      expect(calculateDiscount(1000, '')).toBe(0.1);
    });
  });

  describe('折扣上限', () => {
    it('应该限制最高折扣为 30%', () => {
      // 1000元(10%) + VIP20(20%) = 30%，不应超过
      expect(calculateDiscount(1000, 'VIP20')).toBe(0.3);
    });
  });

  describe('异常情况', () => {
    it('应该抛出错误当金额为 0', () => {
      expect(() => calculateDiscount(0)).toThrow('Total must be positive');
    });

    it('应该抛出错误当金额为负数', () => {
      expect(() => calculateDiscount(-100)).toThrow('Total must be positive');
    });
  });
});
```

### 类方法测试（依赖注入）

```typescript
// src/services/user.service.ts
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<User>;
}

interface EmailService {
  sendWelcome(email: string): Promise<void>;
}

export class UserService {
  constructor(
    private userRepo: UserRepository,
    private emailService: EmailService
  ) {}

  async createUser(data: CreateUserDTO): Promise<User> {
    // 检查邮箱是否已存在
    const existing = await this.userRepo.findByEmail(data.email);
    if (existing) {
      throw new DuplicateEmailError('邮箱已存在');
    }

    // 创建用户
    const user = await this.userRepo.save({
      id: generateId(),
      email: data.email,
      name: data.name,
      createdAt: new Date(),
    });

    // 发送欢迎邮件
    await this.emailService.sendWelcome(user.email);

    return user;
  }

  async getUserById(id: string): Promise<User | null> {
    return this.userRepo.findById(id);
  }
}

// src/services/user.service.test.ts
import { UserService, DuplicateEmailError } from './user.service';

describe('UserService', () => {
  let service: UserService;
  let mockUserRepo: jest.Mocked<UserRepository>;
  let mockEmailService: jest.Mocked<EmailService>;

  beforeEach(() => {
    mockUserRepo = {
      findById: jest.fn(),
      findByEmail: jest.fn(),
      save: jest.fn(),
    };
    mockEmailService = {
      sendWelcome: jest.fn(),
    };
    service = new UserService(mockUserRepo, mockEmailService);
  });

  describe('createUser', () => {
    const validInput = { email: 'test@example.com', name: 'Test User' };

    it('应该创建用户并返回用户对象', async () => {
      mockUserRepo.findByEmail.mockResolvedValue(null);
      mockUserRepo.save.mockImplementation(async (user) => ({
        ...user,
        id: 'new-id',
      }));
      mockEmailService.sendWelcome.mockResolvedValue(undefined);

      const result = await service.createUser(validInput);

      expect(result).toMatchObject({
        email: 'test@example.com',
        name: 'Test User',
      });
      expect(result.id).toBeDefined();
    });

    it('应该检查邮箱是否已存在', async () => {
      mockUserRepo.findByEmail.mockResolvedValue(null);
      mockUserRepo.save.mockResolvedValue({ id: '1', ...validInput });

      await service.createUser(validInput);

      expect(mockUserRepo.findByEmail).toHaveBeenCalledWith('test@example.com');
    });

    it('应该在邮箱重复时抛出 DuplicateEmailError', async () => {
      mockUserRepo.findByEmail.mockResolvedValue({
        id: 'existing',
        email: 'test@example.com',
      });

      await expect(service.createUser(validInput))
        .rejects.toThrow(DuplicateEmailError);

      expect(mockUserRepo.save).not.toHaveBeenCalled();
    });

    it('应该发送欢迎邮件', async () => {
      mockUserRepo.findByEmail.mockResolvedValue(null);
      mockUserRepo.save.mockResolvedValue({ id: '1', ...validInput });

      await service.createUser(validInput);

      expect(mockEmailService.sendWelcome).toHaveBeenCalledWith('test@example.com');
    });

    it('应该在发送邮件失败时仍然创建用户', async () => {
      mockUserRepo.findByEmail.mockResolvedValue(null);
      mockUserRepo.save.mockResolvedValue({ id: '1', ...validInput });
      mockEmailService.sendWelcome.mockRejectedValue(new Error('SMTP Error'));

      // 根据业务需求，这里可能需要不同的行为
      await expect(service.createUser(validInput)).rejects.toThrow('SMTP Error');
    });
  });

  describe('getUserById', () => {
    it('应该返回用户当用户存在时', async () => {
      const mockUser = { id: '1', email: 'test@example.com', name: 'Test' };
      mockUserRepo.findById.mockResolvedValue(mockUser);

      const result = await service.getUserById('1');

      expect(result).toEqual(mockUser);
      expect(mockUserRepo.findById).toHaveBeenCalledWith('1');
    });

    it('应该返回 null 当用户不存在时', async () => {
      mockUserRepo.findById.mockResolvedValue(null);

      const result = await service.getUserById('999');

      expect(result).toBeNull();
    });
  });
});
```

---

## 集成测试示例

### API 端点测试

```typescript
// src/api/users.test.ts
import request from 'supertest';
import { app } from '../app';
import { db } from '../db';

describe('Users API', () => {
  beforeEach(async () => {
    // 清理数据库
    await db.query('DELETE FROM users');
  });

  afterAll(async () => {
    await db.close();
  });

  describe('POST /api/users', () => {
    it('应该创建用户并返回 201', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'test@example.com', name: 'Test', password: 'password123' })
        .expect(201);

      expect(response.body).toMatchObject({
        id: expect.any(String),
        email: 'test@example.com',
        name: 'Test',
      });
      expect(response.body.password).toBeUndefined(); // 不返回密码
    });

    it('应该返回 400 当邮箱格式无效', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'invalid', name: 'Test', password: 'password123' })
        .expect(400);

      expect(response.body.error).toBe('Invalid email format');
    });

    it('应该返回 409 当邮箱已存在', async () => {
      // 先创建一个用户
      await request(app)
        .post('/api/users')
        .send({ email: 'test@example.com', name: 'First', password: 'pass123' });

      // 再次创建相同邮箱
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'test@example.com', name: 'Second', password: 'pass123' })
        .expect(409);

      expect(response.body.error).toBe('Email already exists');
    });
  });

  describe('GET /api/users/:id', () => {
    it('应该返回用户信息', async () => {
      // 先创建用户
      const createResponse = await request(app)
        .post('/api/users')
        .send({ email: 'test@example.com', name: 'Test', password: 'pass123' });

      const userId = createResponse.body.id;

      // 获取用户
      const response = await request(app)
        .get(`/api/users/${userId}`)
        .expect(200);

      expect(response.body).toMatchObject({
        id: userId,
        email: 'test@example.com',
        name: 'Test',
      });
    });

    it('应该返回 404 当用户不存在', async () => {
      const response = await request(app)
        .get('/api/users/non-existent-id')
        .expect(404);

      expect(response.body.error).toBe('User not found');
    });
  });

  describe('GET /api/users', () => {
    it('应该返回用户列表', async () => {
      // 创建多个用户
      await request(app)
        .post('/api/users')
        .send({ email: 'user1@example.com', name: 'User 1', password: 'pass123' });
      await request(app)
        .post('/api/users')
        .send({ email: 'user2@example.com', name: 'User 2', password: 'pass123' });

      const response = await request(app)
        .get('/api/users')
        .expect(200);

      expect(response.body).toHaveLength(2);
      expect(response.body[0]).toMatchObject({ email: 'user1@example.com' });
      expect(response.body[1]).toMatchObject({ email: 'user2@example.com' });
    });

    it('应该支持分页', async () => {
      // 创建 5 个用户
      for (let i = 1; i <= 5; i++) {
        await request(app)
          .post('/api/users')
          .send({ email: `user${i}@example.com`, name: `User ${i}`, password: 'pass' });
      }

      const response = await request(app)
        .get('/api/users?page=1&limit=2')
        .expect(200);

      expect(response.body.data).toHaveLength(2);
      expect(response.body.pagination).toMatchObject({
        page: 1,
        limit: 2,
        total: 5,
        totalPages: 3,
      });
    });
  });
});
```

### 数据库仓储测试

```typescript
// src/repositories/user.repository.test.ts
import { UserRepository } from './user.repository';
import { db } from '../db';

describe('UserRepository', () => {
  let repository: UserRepository;

  beforeAll(async () => {
    await db.migrate();
  });

  beforeEach(async () => {
    await db.query('DELETE FROM users');
    repository = new UserRepository(db);
  });

  afterAll(async () => {
    await db.close();
  });

  describe('save', () => {
    it('应该插入新用户并返回带 ID 的用户', async () => {
      const user = await repository.save({
        email: 'test@example.com',
        name: 'Test',
        passwordHash: 'hashed',
      });

      expect(user.id).toBeDefined();
      expect(user.email).toBe('test@example.com');
      expect(user.createdAt).toBeInstanceOf(Date);
    });

    it('应该更新已存在的用户', async () => {
      const created = await repository.save({
        email: 'test@example.com',
        name: 'Original',
        passwordHash: 'hashed',
      });

      const updated = await repository.save({
        ...created,
        name: 'Updated',
      });

      expect(updated.id).toBe(created.id);
      expect(updated.name).toBe('Updated');
    });
  });

  describe('findById', () => {
    it('应该返回存在的用户', async () => {
      const saved = await repository.save({
        email: 'test@example.com',
        name: 'Test',
        passwordHash: 'hashed',
      });

      const found = await repository.findById(saved.id);

      expect(found).toMatchObject({
        id: saved.id,
        email: 'test@example.com',
        name: 'Test',
      });
    });

    it('应该返回 null 当用户不存在', async () => {
      const found = await repository.findById('non-existent');
      expect(found).toBeNull();
    });
  });

  describe('findByEmail', () => {
    it('应该按邮箱查找用户', async () => {
      await repository.save({
        email: 'test@example.com',
        name: 'Test',
        passwordHash: 'hashed',
      });

      const found = await repository.findByEmail('test@example.com');

      expect(found).not.toBeNull();
      expect(found?.email).toBe('test@example.com');
    });

    it('应该忽略邮箱大小写', async () => {
      await repository.save({
        email: 'Test@Example.com',
        name: 'Test',
        passwordHash: 'hashed',
      });

      const found = await repository.findByEmail('test@example.com');

      expect(found).not.toBeNull();
    });
  });
});
```

---

## E2E 测试示例

### Playwright 测试

```typescript
// e2e/login.spec.ts
import { test, expect } from '@playwright/test';

test.describe('登录流程', () => {
  test.beforeEach(async ({ page }) => {
    // 每个测试前访问登录页
    await page.goto('/login');
  });

  test('应该成功登录有效用户', async ({ page }) => {
    // 填写表单
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'password123');

    // 点击登录
    await page.click('button[type="submit"]');

    // 等待跳转
    await expect(page).toHaveURL('/dashboard');

    // 验证用户信息显示
    await expect(page.locator('.user-name')).toHaveText('Test User');
  });

  test('应该显示错误信息当密码错误', async ({ page }) => {
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    // 验证错误消息
    await expect(page.locator('.error-message')).toHaveText('邮箱或密码错误');

    // 应该停留在登录页
    await expect(page).toHaveURL('/login');
  });

  test('应该显示验证错误当邮箱为空', async ({ page }) => {
    await page.fill('[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await expect(page.locator('[name="email"]:invalid')).toBeVisible();
  });

  test('应该支持记住我功能', async ({ page, context }) => {
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'password123');
    await page.check('[name="remember"]');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');

    // 关闭并重新打开
    const cookies = await context.cookies();
    expect(cookies.find(c => c.name === 'remember_token')).toBeDefined();
  });

  test('应该在多次失败后锁定账号', async ({ page }) => {
    // 尝试5次错误登录
    for (let i = 0; i < 5; i++) {
      await page.fill('[name="email"]', 'user@example.com');
      await page.fill('[name="password"]', 'wrong');
      await page.click('button[type="submit"]');
      await page.waitForSelector('.error-message');
    }

    // 第6次尝试
    await page.fill('[name="email"]', 'user@example.com');
    await page.fill('[name="password"]', 'wrong');
    await page.click('button[type="submit"]');

    await expect(page.locator('.error-message'))
      .toHaveText('账号已锁定，请15分钟后重试');
  });
});

test.describe('注册流程', () => {
  test('应该完成完整的注册流程', async ({ page }) => {
    await page.goto('/register');

    // Step 1: 填写基本信息
    await page.fill('[name="email"]', 'newuser@example.com');
    await page.fill('[name="password"]', 'SecurePass123!');
    await page.fill('[name="confirmPassword"]', 'SecurePass123!');
    await page.click('button:has-text("下一步")');

    // Step 2: 填写个人资料
    await expect(page.locator('h2')).toHaveText('个人资料');
    await page.fill('[name="name"]', 'New User');
    await page.selectOption('[name="country"]', 'CN');
    await page.click('button:has-text("下一步")');

    // Step 3: 确认并提交
    await expect(page.locator('h2')).toHaveText('确认信息');
    await page.check('[name="terms"]');
    await page.click('button:has-text("完成注册")');

    // 验证成功
    await expect(page).toHaveURL('/welcome');
    await expect(page.locator('h1')).toHaveText('欢迎, New User!');
  });
});
```

### Cypress 测试

```typescript
// cypress/e2e/shopping-cart.cy.ts
describe('购物车流程', () => {
  beforeEach(() => {
    cy.login('user@example.com', 'password');
    cy.visit('/products');
  });

  it('应该添加商品到购物车', () => {
    // 点击第一个商品的添加按钮
    cy.get('[data-testid="product-card"]').first()
      .find('[data-testid="add-to-cart"]')
      .click();

    // 验证购物车图标显示数量
    cy.get('[data-testid="cart-badge"]').should('have.text', '1');

    // 打开购物车
    cy.get('[data-testid="cart-icon"]').click();

    // 验证商品在购物车中
    cy.get('[data-testid="cart-item"]').should('have.length', 1);
  });

  it('应该更新商品数量', () => {
    // 添加商品
    cy.get('[data-testid="product-card"]').first()
      .find('[data-testid="add-to-cart"]')
      .click();

    cy.get('[data-testid="cart-icon"]').click();

    // 增加数量
    cy.get('[data-testid="quantity-increase"]').click();
    cy.get('[data-testid="quantity-input"]').should('have.value', '2');

    // 验证总价更新
    cy.get('[data-testid="cart-total"]')
      .invoke('text')
      .then((total) => {
        const price = parseFloat(total.replace('¥', ''));
        expect(price).to.be.greaterThan(0);
      });
  });

  it('应该完成结账流程', () => {
    // 添加商品
    cy.get('[data-testid="product-card"]').first()
      .find('[data-testid="add-to-cart"]')
      .click();

    // 进入结账
    cy.get('[data-testid="cart-icon"]').click();
    cy.get('[data-testid="checkout-button"]').click();

    // 填写收货地址
    cy.get('[name="address"]').type('北京市朝阳区xxx路123号');
    cy.get('[name="phone"]').type('13800138000');

    // 选择支付方式
    cy.get('[data-testid="payment-alipay"]').click();

    // 确认订单
    cy.get('[data-testid="confirm-order"]').click();

    // 验证跳转到支付页面
    cy.url().should('include', '/payment');
    cy.get('[data-testid="order-number"]').should('be.visible');
  });
});

// cypress/support/commands.ts
Cypress.Commands.add('login', (email: string, password: string) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('[name="email"]').type(email);
    cy.get('[name="password"]').type(password);
    cy.get('button[type="submit"]').click();
    cy.url().should('not.include', '/login');
  });
});
```

---

## React 组件测试示例

```typescript
// src/components/UserProfile.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { UserProfile } from './UserProfile';
import { getUser, updateUser } from '../api/users';

jest.mock('../api/users');

const mockGetUser = getUser as jest.MockedFunction<typeof getUser>;
const mockUpdateUser = updateUser as jest.MockedFunction<typeof updateUser>;

describe('UserProfile', () => {
  const mockUser = {
    id: '1',
    name: 'Test User',
    email: 'test@example.com',
    bio: 'Hello world',
  };

  beforeEach(() => {
    mockGetUser.mockResolvedValue(mockUser);
    mockUpdateUser.mockResolvedValue(mockUser);
  });

  it('应该显示加载状态', () => {
    mockGetUser.mockImplementation(() => new Promise(() => {})); // 永不 resolve

    render(<UserProfile userId="1" />);

    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
  });

  it('应该显示用户信息', async () => {
    render(<UserProfile userId="1" />);

    await waitFor(() => {
      expect(screen.getByText('Test User')).toBeInTheDocument();
    });

    expect(screen.getByText('test@example.com')).toBeInTheDocument();
    expect(screen.getByText('Hello world')).toBeInTheDocument();
  });

  it('应该显示错误信息当加载失败', async () => {
    mockGetUser.mockRejectedValue(new Error('Failed to load'));

    render(<UserProfile userId="1" />);

    await waitFor(() => {
      expect(screen.getByText('加载失败')).toBeInTheDocument();
    });
  });

  it('应该允许编辑用户信息', async () => {
    const user = userEvent.setup();
    render(<UserProfile userId="1" />);

    // 等待加载完成
    await waitFor(() => {
      expect(screen.getByText('Test User')).toBeInTheDocument();
    });

    // 点击编辑按钮
    await user.click(screen.getByRole('button', { name: '编辑' }));

    // 修改名字
    const nameInput = screen.getByLabelText('名字');
    await user.clear(nameInput);
    await user.type(nameInput, 'New Name');

    // 保存
    await user.click(screen.getByRole('button', { name: '保存' }));

    // 验证 API 调用
    expect(mockUpdateUser).toHaveBeenCalledWith('1', {
      name: 'New Name',
      bio: 'Hello world',
    });
  });

  it('应该在保存失败时显示错误', async () => {
    mockUpdateUser.mockRejectedValue(new Error('Save failed'));
    const user = userEvent.setup();

    render(<UserProfile userId="1" />);

    await waitFor(() => {
      expect(screen.getByText('Test User')).toBeInTheDocument();
    });

    await user.click(screen.getByRole('button', { name: '编辑' }));
    await user.click(screen.getByRole('button', { name: '保存' }));

    await waitFor(() => {
      expect(screen.getByText('保存失败')).toBeInTheDocument();
    });
  });
});
```

---

## Python 测试示例

```python
# tests/unit/test_order_service.py
import pytest
from datetime import datetime
from decimal import Decimal
from unittest.mock import Mock, AsyncMock

from myapp.services.order_service import OrderService
from myapp.models import Order, OrderItem, OrderStatus
from myapp.exceptions import InsufficientStockError, OrderNotFoundError


class TestOrderServiceCreateOrder:
    """创建订单测试"""

    @pytest.fixture
    def order_service(self, mock_order_repo, mock_inventory_service, mock_payment_service):
        return OrderService(
            order_repo=mock_order_repo,
            inventory_service=mock_inventory_service,
            payment_service=mock_payment_service,
        )

    @pytest.fixture
    def mock_order_repo(self):
        repo = Mock()
        repo.save = AsyncMock()
        return repo

    @pytest.fixture
    def mock_inventory_service(self):
        service = Mock()
        service.check_stock = AsyncMock(return_value=True)
        service.reserve_stock = AsyncMock()
        return service

    @pytest.fixture
    def mock_payment_service(self):
        service = Mock()
        service.create_payment = AsyncMock(return_value={"payment_id": "pay_123"})
        return service

    @pytest.fixture
    def valid_order_data(self):
        return {
            "user_id": "user_1",
            "items": [
                {"product_id": "prod_1", "quantity": 2, "price": Decimal("10.00")},
                {"product_id": "prod_2", "quantity": 1, "price": Decimal("20.00")},
            ],
        }

    async def test_应该创建订单并返回订单对象(
        self, order_service, mock_order_repo, valid_order_data
    ):
        mock_order_repo.save.return_value = Order(
            id="order_1",
            user_id="user_1",
            items=[],
            total=Decimal("40.00"),
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
        )

        result = await order_service.create_order(valid_order_data)

        assert result.id == "order_1"
        assert result.status == OrderStatus.PENDING
        mock_order_repo.save.assert_called_once()

    async def test_应该计算正确的订单总价(
        self, order_service, mock_order_repo, valid_order_data
    ):
        await order_service.create_order(valid_order_data)

        # 检查保存时的订单总价
        saved_order = mock_order_repo.save.call_args[0][0]
        assert saved_order.total == Decimal("40.00")  # 2*10 + 1*20

    async def test_应该检查库存(
        self, order_service, mock_inventory_service, valid_order_data
    ):
        await order_service.create_order(valid_order_data)

        assert mock_inventory_service.check_stock.call_count == 2
        mock_inventory_service.check_stock.assert_any_call("prod_1", 2)
        mock_inventory_service.check_stock.assert_any_call("prod_2", 1)

    async def test_应该在库存不足时抛出异常(
        self, order_service, mock_inventory_service, valid_order_data
    ):
        mock_inventory_service.check_stock.return_value = False

        with pytest.raises(InsufficientStockError, match="库存不足"):
            await order_service.create_order(valid_order_data)

    async def test_应该预留库存(
        self, order_service, mock_inventory_service, valid_order_data
    ):
        await order_service.create_order(valid_order_data)

        assert mock_inventory_service.reserve_stock.call_count == 2


class TestOrderServiceGetOrder:
    """获取订单测试"""

    @pytest.fixture
    def order_service(self, mock_order_repo):
        return OrderService(order_repo=mock_order_repo)

    @pytest.fixture
    def mock_order_repo(self):
        repo = Mock()
        repo.find_by_id = AsyncMock()
        return repo

    async def test_应该返回存在的订单(self, order_service, mock_order_repo):
        mock_order = Order(
            id="order_1",
            user_id="user_1",
            items=[],
            total=Decimal("100.00"),
            status=OrderStatus.COMPLETED,
            created_at=datetime.now(),
        )
        mock_order_repo.find_by_id.return_value = mock_order

        result = await order_service.get_order("order_1")

        assert result.id == "order_1"
        assert result.status == OrderStatus.COMPLETED

    async def test_应该在订单不存在时抛出异常(self, order_service, mock_order_repo):
        mock_order_repo.find_by_id.return_value = None

        with pytest.raises(OrderNotFoundError):
            await order_service.get_order("non_existent")


# 参数化测试示例
class TestOrderStatusTransitions:
    """订单状态转换测试"""

    @pytest.mark.parametrize(
        "current_status,action,expected_status",
        [
            (OrderStatus.PENDING, "pay", OrderStatus.PAID),
            (OrderStatus.PAID, "ship", OrderStatus.SHIPPED),
            (OrderStatus.SHIPPED, "deliver", OrderStatus.DELIVERED),
            (OrderStatus.PENDING, "cancel", OrderStatus.CANCELLED),
            (OrderStatus.PAID, "cancel", OrderStatus.CANCELLED),
        ],
    )
    def test_有效的状态转换(self, current_status, action, expected_status):
        order = Order(id="1", status=current_status)

        order.transition(action)

        assert order.status == expected_status

    @pytest.mark.parametrize(
        "current_status,action",
        [
            (OrderStatus.SHIPPED, "cancel"),  # 已发货不能取消
            (OrderStatus.DELIVERED, "ship"),  # 已送达不能再发货
            (OrderStatus.CANCELLED, "pay"),   # 已取消不能支付
        ],
    )
    def test_无效的状态转换(self, current_status, action):
        order = Order(id="1", status=current_status)

        with pytest.raises(ValueError, match="无效的状态转换"):
            order.transition(action)
```

---

## 测试命名总结

```
格式: [被测方法/场景] 应该 [预期行为] 当 [条件]

示例:
- createUser 应该创建用户并返回用户对象
- createUser 应该抛出错误当邮箱已存在
- calculateDiscount 应该返回10%折扣当金额超过1000
- 登录流程 应该跳转到首页当凭证有效
- 购物车 应该更新总价当数量改变
```
