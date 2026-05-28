---
name: architecture-review
description: 软件架构审查和设计模式。用于评估系统架构、设计决策、技术选型、可扩展性和可维护性。包括微服务、分布式系统、设计模式等。
allowed-tools: Read, Grep, Glob
---

# 软件架构审查

## 架构评估维度

### 1. 可扩展性（Scalability）
- 水平扩展能力
- 垂直扩展能力
- 性能瓶颈识别
- 负载均衡策略

### 2. 可维护性（Maintainability）
- 代码组织结构
- 模块化程度
- 文档完整性
- 技术债务

### 3. 可靠性（Reliability）
- 容错机制
- 故障恢复
- 数据一致性
- 监控告警

### 4. 安全性（Security）
- 认证授权
- 数据加密
- 安全审计
- 漏洞防护

### 5. 性能（Performance）
- 响应时间
- 吞吐量
- 资源利用率
- 缓存策略

## 架构模式

### 单体架构（Monolithic）

**适用场景**：
- 小型应用
- 团队规模小
- 业务逻辑简单
- 快速迭代

**优点**：
- 开发简单
- 部署容易
- 调试方便
- 性能好（无网络开销）

**缺点**：
- 扩展困难
- 技术栈固定
- 部署风险高
- 团队协作困难

### 微服务架构（Microservices）

**适用场景**：
- 大型复杂系统
- 团队规模大
- 需要独立部署
- 技术栈多样化

**设计原则**：
```
1. 单一职责：每个服务专注一个业务领域
2. 自治性：独立开发、部署、扩展
3. 去中心化：数据和治理去中心化
4. 容错性：服务间隔离，故障不传播
5. 可观测性：完善的监控和日志
```

**服务拆分策略**：
```
按业务能力拆分：
- 用户服务
- 订单服务
- 支付服务
- 库存服务

按子域拆分（DDD）：
- 核心域
- 支撑域
- 通用域
```

**服务间通信**：
```typescript
// 同步通信：REST API
GET /api/users/123

// 同步通信：gRPC
service UserService {
  rpc GetUser(UserRequest) returns (UserResponse);
}

// 异步通信：消息队列
await messageQueue.publish('order.created', orderData);
```

### 事件驱动架构（Event-Driven）

**核心概念**：
```typescript
// 事件发布
eventBus.publish('OrderCreated', {
  orderId: '123',
  userId: '456',
  amount: 100
});

// 事件订阅
eventBus.subscribe('OrderCreated', async (event) => {
  await sendEmail(event.userId);
  await updateInventory(event.orderId);
});
```

**优点**：
- 松耦合
- 可扩展
- 异步处理
- 事件溯源

**挑战**：
- 最终一致性
- 事件顺序
- 重复处理
- 调试困难

### 分层架构（Layered）

```
┌─────────────────────┐
│  Presentation Layer │ ← UI, API
├─────────────────────┤
│   Business Layer    │ ← 业务逻辑
├─────────────────────┤
│ Data Access Layer   │ ← 数据访问
├─────────────────────┤
│   Database Layer    │ ← 数据存储
└─────────────────────┘
```

**依赖规则**：
- 上层依赖下层
- 下层不依赖上层
- 每层职责单一

### 六边形架构（Hexagonal）

```
        ┌──────────────┐
        │   Adapters   │
        │  (UI, API)   │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │   Ports      │
        │  (Interfaces)│
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │   Domain     │
        │   (Core)     │
        └──────┬───────┘
               │
        ┌──────▼───────┐
        │   Adapters   │
        │ (DB, Queue)  │
        └──────────────┘
```

**优点**：
- 业务逻辑独立
- 易于测试
- 技术无关
- 灵活替换

## 设计模式

### 创建型模式

#### 单例模式（Singleton）
```typescript
class Database {
  private static instance: Database;

  private constructor() {}

  static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }
}
```

#### 工厂模式（Factory）
```typescript
interface Payment {
  process(amount: number): void;
}

class PaymentFactory {
  static create(type: string): Payment {
    switch (type) {
      case 'credit': return new CreditCardPayment();
      case 'paypal': return new PayPalPayment();
      default: throw new Error('Unknown payment type');
    }
  }
}
```

### 结构型模式

#### 适配器模式（Adapter）
```typescript
// 旧接口
class OldPaymentService {
  makePayment(amount: number) { }
}

// 新接口
interface PaymentService {
  processPayment(amount: number): Promise<void>;
}

// 适配器
class PaymentAdapter implements PaymentService {
  constructor(private oldService: OldPaymentService) {}

  async processPayment(amount: number) {
    this.oldService.makePayment(amount);
  }
}
```

#### 装饰器模式（Decorator）
```typescript
interface Coffee {
  cost(): number;
  description(): string;
}

class SimpleCoffee implements Coffee {
  cost() { return 10; }
  description() { return 'Simple coffee'; }
}

class MilkDecorator implements Coffee {
  constructor(private coffee: Coffee) {}

  cost() { return this.coffee.cost() + 2; }
  description() { return this.coffee.description() + ', milk'; }
}
```

### 行为型模式

#### 策略模式（Strategy）
```typescript
interface PricingStrategy {
  calculate(price: number): number;
}

class RegularPricing implements PricingStrategy {
  calculate(price: number) { return price; }
}

class DiscountPricing implements PricingStrategy {
  calculate(price: number) { return price * 0.9; }
}

class ShoppingCart {
  constructor(private strategy: PricingStrategy) {}

  checkout(price: number) {
    return this.strategy.calculate(price);
  }
}
```

#### 观察者模式（Observer）
```typescript
class Subject {
  private observers: Observer[] = [];

  attach(observer: Observer) {
    this.observers.push(observer);
  }

  notify(data: any) {
    this.observers.forEach(o => o.update(data));
  }
}

interface Observer {
  update(data: any): void;
}
```

## 分布式系统设计

### CAP 定理
```
一致性（Consistency）
可用性（Availability）
分区容错性（Partition Tolerance）

只能同时满足两个
```

### 分布式事务

#### 2PC（两阶段提交）
```
准备阶段：协调者询问所有参与者是否可以提交
提交阶段：所有参与者都同意则提交，否则回滚

缺点：阻塞、单点故障
```

#### Saga 模式
```typescript
// 编排式 Saga
async function createOrder(order) {
  try {
    await createOrderService(order);
    await reserveInventory(order);
    await processPayment(order);
  } catch (error) {
    // 补偿事务
    await cancelPayment(order);
    await releaseInventory(order);
    await cancelOrder(order);
  }
}
```

### 服务发现
```typescript
// 客户端发现
const serviceUrl = await registry.discover('user-service');
const response = await fetch(serviceUrl);

// 服务端发现（负载均衡器）
const response = await fetch('http://load-balancer/user-service');
```

### 熔断器模式
```typescript
class CircuitBreaker {
  private failures = 0;
  private state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN

  async call(fn: Function) {
    if (this.state === 'OPEN') {
      throw new Error('Circuit breaker is OPEN');
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  private onFailure() {
    this.failures++;
    if (this.failures >= 5) {
      this.state = 'OPEN';
      setTimeout(() => this.state = 'HALF_OPEN', 60000);
    }
  }
}
```

## 技术选型

### 评估标准
```
1. 功能匹配度
2. 性能要求
3. 学习曲线
4. 社区活跃度
5. 长期维护性
6. 成本
7. 团队熟悉度
```

### 前端框架选择
```
React：
✅ 生态丰富、灵活性高、社区大
❌ 需要额外配置、学习曲线陡

Vue：
✅ 易学易用、文档好、渐进式
❌ 生态相对小、企业采用少

Angular：
✅ 完整框架、TypeScript、企业级
❌ 学习曲线陡、较重
```

### 后端框架选择
```
Node.js + Express：
✅ JavaScript 全栈、高并发、生态好
❌ 单线程、CPU 密集型任务弱

Python + Django/FastAPI：
✅ 开发效率高、AI/ML 支持好
❌ 性能相对低、GIL 限制

Java + Spring Boot：
✅ 企业级、性能好、生态成熟
❌ 开发效率低、较重
```

### 数据库选择
```
PostgreSQL：
✅ 功能强大、ACID、扩展性好
❌ 配置复杂

MySQL：
✅ 简单易用、性能好、生态好
❌ 功能相对少

MongoDB：
✅ 灵活schema、水平扩展、开发快
❌ 事务支持弱、内存占用高
```

## 架构审查清单

### 系统设计
- [ ] 架构模式选择合理
- [ ] 服务边界清晰
- [ ] 依赖关系明确
- [ ] 技术选型恰当

### 可扩展性
- [ ] 支持水平扩展
- [ ] 无状态设计
- [ ] 负载均衡配置
- [ ] 缓存策略合理

### 可靠性
- [ ] 容错机制完善
- [ ] 故障隔离
- [ ] 降级策略
- [ ] 备份恢复方案

### 性能
- [ ] 响应时间达标
- [ ] 吞吐量满足需求
- [ ] 资源利用合理
- [ ] 性能监控完善

### 安全性
- [ ] 认证授权机制
- [ ] 数据加密
- [ ] 安全审计
- [ ] 漏洞扫描

### 可维护性
- [ ] 代码结构清晰
- [ ] 文档完整
- [ ] 日志规范
- [ ] 监控告警

### 可测试性
- [ ] 单元测试覆盖
- [ ] 集成测试
- [ ] 端到端测试
- [ ] 性能测试

## 常见架构问题

### 过度设计
```
问题：为简单需求设计复杂架构
解决：YAGNI 原则，按需设计
```

### 紧耦合
```
问题：模块间依赖过多
解决：依赖注入、接口抽象
```

### 单点故障
```
问题：关键组件无冗余
解决：高可用设计、主从复制
```

### 性能瓶颈
```
问题：未识别性能瓶颈
解决：性能测试、监控分析
```

## 架构演进

### 从单体到微服务
```
1. 识别服务边界
2. 提取独立服务
3. 建立服务通信
4. 数据库拆分
5. 监控和治理
```

### 重构策略
```
1. 绞杀者模式：逐步替换
2. 分支抽象：新旧并存
3. 特性开关：灰度发布
```
