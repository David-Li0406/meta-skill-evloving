---
name: result-type-error-handling
description: Result型を使ったエラーハンドリング設計ガイド（TypeScript）。コード生成・レビュー・リファクタリング時に適用。例外とResult型の使い分け、ドメインエラーと技術的エラーの分類、レイヤーごとのエラー処理責務を判断する際に参照。
---

# Result型エラーハンドリング

例外処理は副作用であり制御フローに使うべきでない。Result型はエラーを値として明示的に扱い、型で失敗の可能性を表現する。

## 基本原則

### 例外 vs Result型の使い分け

| 状況 | 使用する手法 |
|------|-------------|
| ドメインロジック上で想定できる失敗 | Result型 |
| 回復不能なエラー（プログラム終了レベル） | 例外 |
| 外部ライブラリからの例外 | catchしてResult型に変換 |
| インフラ層の技術的エラー（DB接続失敗等） | 例外 |

### ドメインエラー vs 技術的エラー

**ドメインエラー**（Result型で扱う）
- ドメインエキスパートとの会話で出てくる失敗
- ビジネスルール違反（在庫不足、重複登録、権限不足）
- ユーザー操作で回復可能

**技術的エラー**（例外で扱う）
- 開発者のみが関心を持つ失敗
- システムの異常状態（DB接続断、ネットワークタイムアウト）
- 実装ミス（NullPointerException相当）

## レイヤーごとの責務

```
┌─────────────────────────────────────────────────────────┐
│ Presentation層                                          │
│  - フレームワークのバリデーション（形式検証）               │
│  - 例外ハンドラでHTTPステータスに変換                      │
├─────────────────────────────────────────────────────────┤
│ Application層（UseCase）                                │
│  - Result型のエラーを例外に変換                           │
│  - トランザクション管理                                   │
├─────────────────────────────────────────────────────────┤
│ Domain層                                                │
│  - ビジネスルール検証 → Result型                         │
│  - ValueObjectのコンストラクタ → 例外（実装ミス検出）      │
├─────────────────────────────────────────────────────────┤
│ Infrastructure層                                        │
│  - 技術的エラー → 例外                                   │
│  - 外部APIエラー → catchしてResult型に変換も可            │
└─────────────────────────────────────────────────────────┘
```

## 実装パターン

### Result型の基本構造

```typescript
type Result<T, E> = Ok<T> | Err<E>;

class Ok<T> {
  readonly _tag = 'ok';
  constructor(readonly value: T) {}
}

class Err<E> {
  readonly _tag = 'err';
  constructor(readonly error: E) {}
}

const ok = <T>(value: T): Result<T, never> => new Ok(value);
const err = <E>(error: E): Result<never, E> => new Err(error);

const isOk = <T, E>(result: Result<T, E>): result is Ok<T> => result._tag === 'ok';
const isErr = <T, E>(result: Result<T, E>): result is Err<E> => result._tag === 'err';
```

### ドメインエラーの定義

```typescript
// エラーの種類をUnion型で明示
type OrderError =
  | { type: 'INSUFFICIENT_STOCK'; productId: string; requested: number; available: number }
  | { type: 'INVALID_QUANTITY'; reason: string }
  | { type: 'CUSTOMER_NOT_FOUND'; customerId: string };
```

### ドメインロジックでの使用

```typescript
function createOrder(
  productId: ProductId,
  quantity: Quantity,
  customerId: CustomerId
): Result<Order, OrderError> {
  const stock = getStock(productId);
  if (stock < quantity.value) {
    return err({
      type: 'INSUFFICIENT_STOCK',
      productId: productId.value,
      requested: quantity.value,
      available: stock
    });
  }
  return ok(new Order(productId, quantity, customerId));
}
```

### UseCase層での変換

```typescript
class CreateOrderUseCase {
  execute(input: CreateOrderInput): OrderDto {
    const result = this.orderFactory.create(
      new ProductId(input.productId),
      new Quantity(input.quantity),
      new CustomerId(input.customerId)
    );

    if (isErr(result)) {
      // Result型のエラーをHTTP例外に変換
      throw this.toHttpException(result.error);
    }

    // 技術的エラーはそのまま例外として伝播
    this.orderRepository.save(result.value);
    return OrderDto.from(result.value);
  }

  private toHttpException(error: OrderError): HttpException {
    switch (error.type) {
      case 'INSUFFICIENT_STOCK':
        return new ConflictException(`在庫不足: ${error.available}個のみ在庫あり`);
      case 'INVALID_QUANTITY':
        return new BadRequestException(error.reason);
      case 'CUSTOMER_NOT_FOUND':
        return new NotFoundException(`顧客が見つかりません: ${error.customerId}`);
    }
  }
}
```

### ValueObjectでの例外使用

```typescript
// 構文的バリデーション → 例外（実装ミスの早期検出）
class Quantity {
  constructor(readonly value: number) {
    if (value <= 0) {
      throw new Error(`数量は1以上を指定してください: ${value}`);
    }
  }
}
```

## 判断フローチャート

```
エラーが発生しうる箇所を特定
           │
           ▼
  ドメインエキスパートが
  この失敗を認識している？
     │           │
    Yes          No
     │           │
     ▼           ▼
 Result型     例外を使用
  を使用
```

## ライブラリ

本番プロジェクトでは以下を検討：
- **neverthrow**: 軽量でTypeScript向け。`andThen`, `map`, `mapErr`等のメソッドチェーン対応
- **fp-ts**: 関数型プログラミング志向。Either型として提供
- **ts-results**: Rust風のAPI

詳細な実装例とRailway Oriented Programmingパターンは [references/patterns.md](references/patterns.md) を参照。
