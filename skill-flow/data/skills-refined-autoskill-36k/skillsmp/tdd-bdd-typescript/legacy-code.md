# レガシーコード改善手法

t-wada「実録レガシーコード改善」の知見に基づく。

## レガシーコードの定義

> 「テストのないコードは悪いコードである。どれだけうまく書かれているかは関係ない」

テストがなければ、コードの振る舞いが変わっていないことを保証できない。

## レガシーコードのジレンマ

```
コードを変更するためには → テストを整備する必要がある
テストを整備するためには → コードを変更する必要がある
```

この鶏と卵の問題を解決するのが「接合部（Seam）」の概念。

## 接合部（Seam）パターン

接合部とは、コードを直接編集せずに振る舞いを変えられる場所。

### テスト困難な要素

| 要素 | 例 | なぜ困難か |
|------|-----|----------|
| ランダム性 | Math.random(), crypto | 結果が予測不能 |
| 時間依存 | Date.now(), setTimeout | 実行タイミングで変化 |
| 外部I/O | fetch, fs, DB | 環境依存、遅い |
| グローバル状態 | process.env, singleton | 副作用が伝播 |

### 接合部の作り方

#### 1. 関数引数による注入

```typescript
// Before: テスト困難
export function generateOrderId(): string {
  const timestamp = Date.now();
  const random = Math.random().toString(36).substring(2);
  return `ORD-${timestamp}-${random}`;
}

// After: 接合部を追加
export function createOrderIdGenerator(deps: {
  getTimestamp: () => number;
  getRandom: () => string;
}) {
  return function generateOrderId(): string {
    const timestamp = deps.getTimestamp();
    const random = deps.getRandom();
    return `ORD-${timestamp}-${random}`;
  };
}

// 本番
const generateOrderId = createOrderIdGenerator({
  getTimestamp: () => Date.now(),
  getRandom: () => Math.random().toString(36).substring(2),
});

// テスト
const generateOrderId = createOrderIdGenerator({
  getTimestamp: () => 1704067200000, // 固定値
  getRandom: () => 'abc123',          // 固定値
});

expect(generateOrderId()).toBe('ORD-1704067200000-abc123');
```

#### 2. インターフェースによる抽象化

```typescript
// インターフェース定義
interface Clock {
  now(): Date;
}

interface IdGenerator {
  generate(): string;
}

// 本番実装
const realClock: Clock = {
  now: () => new Date(),
};

// テスト用実装
const fakeClock: Clock = {
  now: () => new Date('2024-01-01T00:00:00Z'),
};

// 使用側
class OrderService {
  constructor(
    private clock: Clock,
    private idGenerator: IdGenerator,
  ) {}

  createOrder(input: OrderInput): Order {
    return {
      id: this.idGenerator.generate(),
      createdAt: this.clock.now(),
      ...input,
    };
  }
}
```

#### 3. 環境変数の抽象化

```typescript
// Before: 直接参照
function getApiUrl(): string {
  return process.env.API_URL || 'http://localhost:3000';
}

// After: Config オブジェクト
interface Config {
  apiUrl: string;
  timeout: number;
}

function createConfig(): Config {
  return {
    apiUrl: process.env.API_URL || 'http://localhost:3000',
    timeout: Number(process.env.TIMEOUT) || 5000,
  };
}

// テスト用
const testConfig: Config = {
  apiUrl: 'http://test-api',
  timeout: 100,
};
```

## Humble Object Pattern

テスト困難な要素を「薄いラッパー」に押し込め、ロジックをテスト可能にする。

```typescript
// Before: ロジックとI/Oが混在
async function processOrder(orderId: string) {
  const order = await db.orders.findById(orderId);  // I/O
  
  // ビジネスロジック
  if (order.items.length === 0) {
    throw new Error('Empty order');
  }
  const total = order.items.reduce((sum, item) => sum + item.price, 0);
  const tax = total * 0.1;
  
  await db.orders.update(orderId, { total, tax });  // I/O
  await sendEmail(order.customerEmail, { total });  // I/O
}

// After: ロジックを分離
// 純粋なビジネスロジック（テスト容易）
function calculateOrderTotals(order: Order): OrderTotals {
  if (order.items.length === 0) {
    throw new Error('Empty order');
  }
  const total = order.items.reduce((sum, item) => sum + item.price, 0);
  const tax = total * 0.1;
  return { total, tax };
}

// Humble Object: I/Oのみ
async function processOrder(
  orderId: string,
  deps: { db: Database; emailService: EmailService }
) {
  const order = await deps.db.orders.findById(orderId);
  const totals = calculateOrderTotals(order);  // 純粋関数
  await deps.db.orders.update(orderId, totals);
  await deps.emailService.send(order.customerEmail, totals);
}
```

## スプラウトクラス/メソッド

既存コードを変更せず、新しい機能を「芽」として追加する。

```typescript
// 既存の複雑なコード（テストなし）
class LegacyOrderProcessor {
  process(order: Order) {
    // 100行の複雑な処理...
  }
}

// スプラウトメソッド: 新機能だけテスト付きで追加
class LegacyOrderProcessor {
  process(order: Order) {
    // 既存の複雑な処理...
    
    // 新機能はスプラウトメソッドとして追加
    this.applyLoyaltyDiscount(order);
  }

  // この部分だけTDDで開発
  applyLoyaltyDiscount(order: Order): number {
    if (order.customer.loyaltyPoints > 1000) {
      return order.total * 0.05;
    }
    return 0;
  }
}
```

## テストの書き始め方

### Step 1: 最も外側からテストを書く

リクエスト/レスポンスレベルでテストを書くと、実装詳細から距離を取れる。

```typescript
// Lambda/API のテスト例
describe('POST /orders', () => {
  it('正常なリクエストで注文が作成される', async () => {
    const response = await handler({
      httpMethod: 'POST',
      body: JSON.stringify({ productId: 'p1', quantity: 2 }),
    });

    expect(response.statusCode).toBe(201);
    expect(JSON.parse(response.body)).toMatchObject({
      orderId: expect.any(String),
      status: 'created',
    });
  });
});
```

### Step 2: 雑なテストから始める

最初は「undefined でない」程度でよい。

```typescript
it('レスポンスが返る', () => {
  const result = handler(request);
  expect(result).toBeDefined();  // まずはこれでOK
});
```

### Step 3: 徐々に厳密にする

テストが安定したら、アサーションを厳密化。

```typescript
it('正しいレスポンスが返る', () => {
  const result = handler(request);
  expect(result).toEqual({
    statusCode: 200,
    body: '{"message":"success"}',
  });
});
```

## テストの安定化

### ランダム性の制御

```typescript
// 本番: ランダムな質問を選択
const selectQuestion = createSelector(
  () => Math.floor(Math.random() * questions.length)
);

// テスト: 決定的な選択
const selectQuestion = createSelector(() => 4);
```

### 時間依存の制御

```typescript
// vi.useFakeTimers() を使う
beforeEach(() => {
  vi.useFakeTimers();
  vi.setSystemTime(new Date('2024-01-01'));
});

afterEach(() => {
  vi.useRealTimers();
});

it('作成日時が正しく設定される', () => {
  const order = createOrder();
  expect(order.createdAt).toEqual(new Date('2024-01-01'));
});
```

## 優先順位付け

1. **バージョン管理** — なければ話にならない
2. **自動テスト** — 安全なコード変更の前提
3. **自動化** — ビルド・デプロイの自動化

## チェックリスト

テストを書く前に確認:
- [ ] テスト困難な要素（ランダム、時間、I/O）を特定したか
- [ ] 接合部を用意したか
- [ ] テストの決定性を担保できるか
- [ ] 最小限のセットアップでテストできるか

レガシーコード改善時:
- [ ] 既存の動作を壊していないか確認できるテストがあるか
- [ ] 変更範囲を最小限にしているか
- [ ] スプラウトパターンで新機能を追加できるか
