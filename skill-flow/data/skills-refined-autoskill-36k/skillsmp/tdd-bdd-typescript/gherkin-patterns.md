# Given-When-Then パターン集

## 基本構造

```typescript
describe('[機能名]', () => {
  describe('Given: [事前条件]', () => {
    describe('When: [操作/イベント]', () => {
      it('Then: [期待される結果]', () => {
        // テスト実装
      });
    });
  });
});
```

## パターン1: 状態ベースのテスト

```typescript
describe('在庫管理', () => {
  describe('Given: 商品の在庫が10個ある', () => {
    const createFixture = () => ({
      inventory: createInventory({ productId: 'p1', quantity: 10 }),
    });

    describe('When: 3個出庫する', () => {
      it('Then: 在庫が7個になる', () => {
        // Given
        const { inventory } = createFixture();
        
        // When
        const result = inventory.withdraw(3);
        
        // Then
        expect(result.isOk()).toBe(true);
        expect(inventory.quantity).toBe(7);
      });
    });

    describe('When: 15個出庫しようとする', () => {
      it('Then: 在庫不足エラーが返る', () => {
        // Given
        const { inventory } = createFixture();
        
        // When
        const result = inventory.withdraw(15);
        
        // Then
        expect(result.isErr()).toBe(true);
        expect(result.error.type).toBe('INSUFFICIENT_STOCK');
      });
    });
  });
});
```

## パターン2: 振る舞いベースのテスト

```typescript
describe('注文通知', () => {
  describe('Given: メール送信サービスが設定されている', () => {
    describe('When: 注文が確定する', () => {
      it('Then: 確認メールが送信される', () => {
        // Given
        const emailService = { send: vi.fn() };
        const orderService = createOrderService({ emailService });
        const order = createOrder({ email: 'user@example.com' });
        
        // When
        orderService.confirm(order);
        
        // Then
        expect(emailService.send).toHaveBeenCalledWith(
          expect.objectContaining({
            to: 'user@example.com',
            subject: expect.stringContaining('注文確認'),
          })
        );
      });
    });
  });
});
```

## パターン3: 例外・エラーハンドリング

```typescript
describe('ユーザー認証', () => {
  describe('Given: 無効なトークン', () => {
    describe('When: APIにアクセスする', () => {
      it('Then: 401エラーが返る', async () => {
        // Given
        const invalidToken = 'invalid-token';
        const api = createApiClient({ token: invalidToken });
        
        // When
        const result = await api.getUser();
        
        // Then
        expect(result.isErr()).toBe(true);
        expect(result.error.status).toBe(401);
      });
    });
  });
});
```

## パターン4: 非同期処理

```typescript
describe('データ取得', () => {
  describe('Given: APIが正常に応答する', () => {
    describe('When: ユーザー一覧を取得する', () => {
      it('Then: ユーザーリストが返る', async () => {
        // Given
        const mockResponse = [{ id: '1', name: 'Alice' }];
        const fetchUsers = vi.fn().mockResolvedValue(mockResponse);
        const service = createUserService({ fetchUsers });
        
        // When
        const result = await service.getAll();
        
        // Then
        expect(result.isOk()).toBe(true);
        expect(result.value).toEqual(mockResponse);
      });
    });
  });

  describe('Given: APIがタイムアウトする', () => {
    describe('When: ユーザー一覧を取得する', () => {
      it('Then: タイムアウトエラーが返る', async () => {
        // Given
        const fetchUsers = vi.fn().mockRejectedValue(new Error('Timeout'));
        const service = createUserService({ fetchUsers });
        
        // When
        const result = await service.getAll();
        
        // Then
        expect(result.isErr()).toBe(true);
        expect(result.error.type).toBe('TIMEOUT');
      });
    });
  });
});
```

## パターン5: 境界値テスト

```typescript
describe('ページネーション', () => {
  describe('Given: 総件数が25件', () => {
    const createFixture = () => ({
      totalCount: 25,
      pageSize: 10,
    });

    describe('When: 1ページ目を取得', () => {
      it('Then: 10件取得、次ページあり', () => {
        const { totalCount, pageSize } = createFixture();
        const result = paginate({ totalCount, pageSize, page: 1 });
        
        expect(result.items.length).toBe(10);
        expect(result.hasNext).toBe(true);
      });
    });

    describe('When: 3ページ目を取得', () => {
      it('Then: 5件取得、次ページなし', () => {
        const { totalCount, pageSize } = createFixture();
        const result = paginate({ totalCount, pageSize, page: 3 });
        
        expect(result.items.length).toBe(5);
        expect(result.hasNext).toBe(false);
      });
    });

    describe('When: 4ページ目を取得（範囲外）', () => {
      it('Then: 0件取得', () => {
        const { totalCount, pageSize } = createFixture();
        const result = paginate({ totalCount, pageSize, page: 4 });
        
        expect(result.items.length).toBe(0);
      });
    });
  });
});
```

## パターン6: 複数条件の組み合わせ

```typescript
describe('割引計算', () => {
  // テストマトリックス
  const testCases = [
    { memberType: 'gold', amount: 10000, expected: 1500, label: 'ゴールド会員で15%割引' },
    { memberType: 'silver', amount: 10000, expected: 1000, label: 'シルバー会員で10%割引' },
    { memberType: 'regular', amount: 10000, expected: 0, label: '一般会員は割引なし' },
  ];

  testCases.forEach(({ memberType, amount, expected, label }) => {
    describe(`Given: ${memberType}会員`, () => {
      describe(`When: ${amount}円の購入`, () => {
        it(`Then: ${label}`, () => {
          const discount = calculateDiscount({ memberType, amount });
          expect(discount).toBe(expected);
        });
      });
    });
  });
});
```

## パターン7: セットアップの共有（beforeEach）

```typescript
describe('ショッピングカート', () => {
  let cart: Cart;
  let product: Product;

  beforeEach(() => {
    product = createProduct({ id: 'p1', price: 1000 });
    cart = createCart();
  });

  describe('Given: カートが空の状態', () => {
    describe('When: 商品を追加する', () => {
      it('Then: カートに1件追加される', () => {
        cart.add(product, 2);
        
        expect(cart.items).toHaveLength(1);
        expect(cart.items[0].quantity).toBe(2);
      });
    });
  });

  describe('Given: 同じ商品がカートにある状態', () => {
    beforeEach(() => {
      cart.add(product, 1);
    });

    describe('When: 同じ商品を追加する', () => {
      it('Then: 数量が合算される', () => {
        cart.add(product, 2);
        
        expect(cart.items).toHaveLength(1);
        expect(cart.items[0].quantity).toBe(3);
      });
    });
  });
});
```

## パターン8: ファクトリー関数の活用

```typescript
// テストヘルパー
const createTestOrder = (overrides: Partial<Order> = {}): Order => ({
  id: 'order-1',
  customerId: 'customer-1',
  items: [],
  status: 'pending',
  createdAt: new Date('2024-01-01'),
  ...overrides,
});

describe('注文キャンセル', () => {
  describe('Given: ステータスがpendingの注文', () => {
    it('Then: キャンセルできる', () => {
      const order = createTestOrder({ status: 'pending' });
      const result = cancelOrder(order);
      expect(result.isOk()).toBe(true);
    });
  });

  describe('Given: ステータスがshippedの注文', () => {
    it('Then: キャンセルできない', () => {
      const order = createTestOrder({ status: 'shipped' });
      const result = cancelOrder(order);
      expect(result.isErr()).toBe(true);
    });
  });
});
```

## テスト構造のアンチパターン

### NG: 長すぎるGiven

```typescript
// NG: セットアップが複雑すぎる
it('複雑なテスト', () => {
  // 10行以上のセットアップは分割を検討
  const user = createUser();
  const product = createProduct();
  const inventory = createInventory(product);
  const cart = createCart();
  cart.add(product, 1);
  const order = createOrder(user, cart);
  const payment = createPayment(order);
  // ...まだ続く
});

// OK: ファクトリーで抽象化
const createCheckoutFixture = () => ({
  user: createUser(),
  cart: createCartWithItem(),
  payment: createPayment(),
});
```

### NG: 複数のWhen

```typescript
// NG: 1テストに複数のアクション
it('複数操作のテスト', () => {
  cart.add(product);      // When 1
  cart.remove(product);   // When 2
  cart.add(product);      // When 3
  expect(cart.items).toHaveLength(1);
});

// OK: 1テスト1アクション
it('商品追加後に削除すると空になる', () => {
  cart.add(product);
  cart.remove(product);
  expect(cart.items).toHaveLength(0);
});
```
