# Tidying パターン コード例

## Guard Clauses（早期リターン）

条件分岐のネストを減らし、メインロジックを目立たせる。

```typescript
// Before
function validate(input: Input): Result<void, Error> {
  if (input.name) {
    if (input.email) {
      if (input.age >= 18) {
        return ok(undefined);
      } else {
        return err({ type: 'Underage' });
      }
    } else {
      return err({ type: 'MissingEmail' });
    }
  } else {
    return err({ type: 'MissingName' });
  }
}

// After
function validate(input: Input): Result<void, Error> {
  if (!input.name) return err({ type: 'MissingName' });
  if (!input.email) return err({ type: 'MissingEmail' });
  if (input.age < 18) return err({ type: 'Underage' });

  return ok(undefined);
}
```

## Extract Helper（ヘルパー抽出）

重複コードや長い処理を関数に抽出。

```typescript
// Before: 同じ計算が複数箇所に
const subtotal1 = items1.reduce((sum, item) => sum + item.price * item.quantity, 0);
const subtotal2 = items2.reduce((sum, item) => sum + item.price * item.quantity, 0);

// After: ヘルパー関数に抽出
function calculateSubtotal(items: OrderItem[]): number {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

const subtotal1 = calculateSubtotal(items1);
const subtotal2 = calculateSubtotal(items2);
```

## Normalize Symmetries（対称性の統一）

似た処理を同じパターンで書く。

```typescript
// Before: 異なるスタイルが混在
const activeUsers = users.filter(u => u.active);
const inactiveUsers = [];
for (const u of users) {
  if (!u.active) inactiveUsers.push(u);
}

// After: 同じスタイルに統一
const activeUsers = users.filter(u => u.active);
const inactiveUsers = users.filter(u => !u.active);
```

## Chunk Statements（文のグループ化）

関連する処理を空行で区切り、意味のまとまりを作る。

```typescript
// Before: 関連性がわかりにくい
const user = await findUser(userId);
const order = await findOrder(orderId);
const items = order.items;
const total = calculateTotal(items);
const discount = user.membership === 'PREMIUM' ? 0.1 : 0;
const finalPrice = total * (1 - discount);

// After: 意味のまとまりで区切る
const user = await findUser(userId);
const order = await findOrder(orderId);

const items = order.items;
const total = calculateTotal(items);

const discount = user.membership === 'PREMIUM' ? 0.1 : 0;
const finalPrice = total * (1 - discount);
```

## Rename（名前の改善）

意図が伝わる名前に変更。

```typescript
// Before
const d = new Date();
const res = await api.get(url);
const tmp = process(data);

// After
const createdAt = new Date();
const apiResponse = await api.get(url);
const processedOrder = process(data);
```

## Explicit Parameters（明示的パラメータ）

暗黙の依存（グローバル変数、this、クロージャ）を引数に。

```typescript
// Before: configを暗黙的に参照
function createOrder(items: Item[]) {
  const tax = config.taxRate; // 暗黙の依存
  return { items, tax };
}

// After: 依存を引数で明示
function createOrder(items: Item[], taxRate: number) {
  return { items, tax: taxRate };
}
```

## Move to Model（集約モデルへ移動）

UseCaseに書かれた判定・状態遷移ロジックを、集約モデルの純粋関数に移動する。

**兆候:**
- UseCase内にif文で状態判定が直接書かれている
- 状態遷移（フィールド更新）がUseCase内にある
- モデルがただのデータ入れ物（Anemic Domain Model）になっている

```typescript
// Before: UseCaseに判定と状態遷移が直書き
class CancelOrderUseCase {
  async execute(command: CancelOrderCommand): Promise<Result<Order, CancelOrderError>> {
    const order = await this.orderRepository.findById(command.orderId);
    if (!order) return err({ type: 'NotFound', orderId: command.orderId });

    // ↓ 判定ロジックがUseCaseに直書き
    if (order.status === 'CANCELLED') {
      return err({ type: 'AlreadyCancelled' });
    }
    if (order.status === 'SHIPPED' || order.status === 'DELIVERED') {
      return err({ type: 'AlreadyShipped' });
    }

    // ↓ 状態遷移もUseCase内
    const cancelled = { ...order, status: 'CANCELLED' as const, cancelledAt: new Date() };
    await this.orderRepository.save(cancelled);
    return ok(cancelled);
  }
}

// After: 判定と状態遷移をモデルの純粋関数に移動
// src/ordering/models/order.ts
function canCancel(order: Order): boolean {
  return order.status === 'PENDING' || order.status === 'CONFIRMED';
}

function cancelOrder(order: Order): Result<Order, CancelOrderError> {
  if (order.status === 'CANCELLED') return err({ type: 'AlreadyCancelled' });
  if (!canCancel(order)) return err({ type: 'AlreadyShipped' });
  return ok({ ...order, status: 'CANCELLED' as const, cancelledAt: new Date() });
}

// src/ordering/usecases/cancel-order.usecase.ts（オーケストレーションのみ）
class CancelOrderUseCase {
  async execute(command: CancelOrderCommand): Promise<Result<Order, CancelOrderError>> {
    const order = await this.orderRepository.findById(command.orderId);
    if (!order) return err({ type: 'NotFound', orderId: command.orderId });

    const result = cancelOrder(order); // モデルに委譲
    if (isErr(result)) return result;

    await this.orderRepository.save(result.value);
    return result;
  }
}
```

## Move to Service（サービスへ移動）

複数の集約にまたがるロジックや外部連携をUseCaseから抽出し、ドメインサービスに移動する。

**兆候:**
- UseCase内で複数のリポジトリを組み合わせた判定がある
- 同じ横断ロジックが複数のUseCaseに散在している
- ビジネスルールが特定の集約に属さない

```typescript
// Before: UseCase内に割引計算の横断ロジック
class CreateOrderUseCase {
  async execute(command: CreateOrderCommand): Promise<Result<Order, CreateOrderError>> {
    const customer = await this.customerRepository.findById(command.customerId);
    const campaign = await this.campaignRepository.findActive();

    // ↓ 複数集約にまたがる割引計算がUseCaseに散在
    let discountRate = 0;
    if (customer.membership === 'PREMIUM') discountRate += 0.1;
    if (campaign && campaign.type === 'SEASONAL') discountRate += 0.05;
    if (command.items.length >= 10) discountRate += 0.03;
    const total = subtotal * (1 - discountRate);
    // ...
  }
}

// After: 割引計算をドメインサービスに抽出
// src/ordering/services/discount.service.ts
interface DiscountService {
  calculate(customer: Customer, campaign: Campaign | null, itemCount: number): number;
}

// src/ordering/usecases/create-order.usecase.ts（オーケストレーションのみ）
class CreateOrderUseCase {
  constructor(
    private customerRepository: CustomerRepository,
    private campaignRepository: CampaignRepository,
    private discountService: DiscountService,
  ) {}

  async execute(command: CreateOrderCommand): Promise<Result<Order, CreateOrderError>> {
    const customer = await this.customerRepository.findById(command.customerId);
    const campaign = await this.campaignRepository.findActive();

    const discountRate = this.discountService.calculate(customer, campaign, command.items.length);
    const total = subtotal * (1 - discountRate);
    // ...
  }
}
```

## Delete Dead Code（不要コード削除）

呼ばれない関数、到達しない分岐、コメントアウトされたコードを削除。

```typescript
// Before
function oldMethod() { /* 誰も呼んでいない */ }

function process(status: OrderStatus) {
  if (status === 'LEGACY') { /* 存在しないステータス */ }
  // const debug = true; // 使われていない
}

// After
function process(status: OrderStatus) {
  // 不要なコードを削除
}
```
