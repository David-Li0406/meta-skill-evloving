# Result型パターン集

## 目次
- [Railway Oriented Programming](#railway-oriented-programming)
- [neverthrowを使った実装](#neverthrowを使った実装)
- [自作Result型の完全実装](#自作result型の完全実装)
- [エラー変換パターン](#エラー変換パターン)
- [アンチパターン](#アンチパターン)

## Railway Oriented Programming

Result型を返す関数をチェーンし、失敗時は即座にエラーへ分岐する。

```
  ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐
──┤ 検証 ├────┤ 在庫 ├────┤ 決済 ├────┤ 注文 ├──→ 成功
  └──┬───┘    └──┬───┘    └──┬───┘    └──┬───┘
     │          │          │          │
     ▼          ▼          ▼          ▼
  エラー     エラー     エラー     エラー
```

### 基本パターン

```typescript
// 各ステップがResult<T, E>を返す
const processOrder = (input: OrderInput): Result<Order, OrderError> =>
  validateInput(input)
    .andThen(validated => checkInventory(validated))
    .andThen(checked => processPayment(checked))
    .andThen(paid => createOrder(paid));
```

### 値の変換（map）

```typescript
// 成功値のみ変換、エラーはそのまま通過
const getOrderId = (input: OrderInput): Result<string, OrderError> =>
  processOrder(input).map(order => order.id);
```

### エラーの変換（mapErr）

```typescript
// エラーを別の型に変換
const processWithGenericError = (input: OrderInput): Result<Order, AppError> =>
  processOrder(input).mapErr(orderError => ({
    code: 'ORDER_FAILED',
    message: toMessage(orderError),
    original: orderError
  }));
```

## neverthrowを使った実装

```typescript
import { ok, err, Result, ResultAsync } from 'neverthrow';

// 同期処理
function validateQuantity(qty: number): Result<Quantity, ValidationError> {
  if (qty <= 0) {
    return err({ type: 'INVALID_QUANTITY', message: '数量は1以上' });
  }
  return ok(new Quantity(qty));
}

// 非同期処理
function fetchProduct(id: string): ResultAsync<Product, FetchError> {
  return ResultAsync.fromPromise(
    fetch(`/api/products/${id}`).then(r => r.json()),
    (e) => ({ type: 'FETCH_FAILED', cause: e })
  );
}

// チェーン
const result = await validateQuantity(5)
  .asyncAndThen(qty => fetchProduct(productId))
  .andThen(product => checkStock(product, qty))
  .map(stock => ({ available: stock > 0 }));

// 結果の処理
result.match(
  (data) => console.log('成功:', data),
  (error) => console.error('失敗:', error)
);
```

### neverthrow + combine

複数のResultを並列で処理：

```typescript
import { Result, combine } from 'neverthrow';

const results: Result<Order, OrderError>[] = [
  createOrder(input1),
  createOrder(input2),
  createOrder(input3)
];

// 全て成功した場合のみOk<Order[]>、一つでも失敗したらErr
const combined = combine(results);
```

## 自作Result型の完全実装

```typescript
type Result<T, E> = Ok<T, E> | Err<T, E>;

class Ok<T, E> {
  readonly _tag = 'ok' as const;
  constructor(readonly value: T) {}

  isOk(): this is Ok<T, E> { return true; }
  isErr(): this is Err<T, E> { return false; }

  map<U>(fn: (value: T) => U): Result<U, E> {
    return new Ok(fn(this.value));
  }

  mapErr<F>(_fn: (error: E) => F): Result<T, F> {
    return new Ok(this.value);
  }

  andThen<U>(fn: (value: T) => Result<U, E>): Result<U, E> {
    return fn(this.value);
  }

  orElse<F>(_fn: (error: E) => Result<T, F>): Result<T, F> {
    return new Ok(this.value);
  }

  unwrapOr(_defaultValue: T): T {
    return this.value;
  }

  match<U>(onOk: (value: T) => U, _onErr: (error: E) => U): U {
    return onOk(this.value);
  }
}

class Err<T, E> {
  readonly _tag = 'err' as const;
  constructor(readonly error: E) {}

  isOk(): this is Ok<T, E> { return false; }
  isErr(): this is Err<T, E> { return true; }

  map<U>(_fn: (value: T) => U): Result<U, E> {
    return new Err(this.error);
  }

  mapErr<F>(fn: (error: E) => F): Result<T, F> {
    return new Err(fn(this.error));
  }

  andThen<U>(_fn: (value: T) => Result<U, E>): Result<U, E> {
    return new Err(this.error);
  }

  orElse<F>(fn: (error: E) => Result<T, F>): Result<T, F> {
    return fn(this.error);
  }

  unwrapOr(defaultValue: T): T {
    return defaultValue;
  }

  match<U>(_onOk: (value: T) => U, onErr: (error: E) => U): U {
    return onErr(this.error);
  }
}

// ファクトリ関数
const ok = <T, E = never>(value: T): Result<T, E> => new Ok(value);
const err = <E, T = never>(error: E): Result<T, E> => new Err(error);

// try-catchをResultに変換
const tryCatch = <T, E>(
  fn: () => T,
  onError: (e: unknown) => E
): Result<T, E> => {
  try {
    return ok(fn());
  } catch (e) {
    return err(onError(e));
  }
};

// Promiseを ResultAsync風に変換
const fromPromise = async <T, E>(
  promise: Promise<T>,
  onError: (e: unknown) => E
): Promise<Result<T, E>> => {
  try {
    return ok(await promise);
  } catch (e) {
    return err(onError(e));
  }
};
```

## エラー変換パターン

### Infrastructure → Domain

```typescript
// リポジトリでDBエラーをドメインエラーに変換
class OrderRepository {
  async findById(id: string): Promise<Result<Order, OrderNotFoundError>> {
    try {
      const row = await this.db.query('SELECT * FROM orders WHERE id = ?', [id]);
      if (!row) {
        return err({ type: 'ORDER_NOT_FOUND', orderId: id });
      }
      return ok(this.toEntity(row));
    } catch (e) {
      // 技術的エラーは例外のまま上位へ
      throw e;
    }
  }
}
```

### Domain → Application → Presentation

```typescript
// UseCase層でドメインエラーをHTTP例外に変換
function domainErrorToHttpException(error: DomainError): HttpException {
  const mapping: Record<DomainError['type'], () => HttpException> = {
    'NOT_FOUND': () => new NotFoundException(error.message),
    'CONFLICT': () => new ConflictException(error.message),
    'VALIDATION': () => new BadRequestException(error.message),
    'FORBIDDEN': () => new ForbiddenException(error.message),
  };
  return mapping[error.type]();
}
```

## アンチパターン

### ❌ エラーを握りつぶす

```typescript
// BAD: エラーを無視してデフォルト値を返す
const getUser = (id: string): User => {
  const result = findUser(id);
  return result.unwrapOr(defaultUser); // エラー原因が不明になる
};
```

### ❌ 全てをResult型にする

```typescript
// BAD: 技術的エラーまでResult型にすると冗長
function readConfig(): Result<Config, ConfigError | IOError | ParseError> {
  // エラー型が爆発し、呼び出し側の負担が増える
}

// GOOD: 技術的エラーは例外に任せる
function readConfig(): Config {
  // IOError, ParseErrorは例外として伝播
  // 設定ファイルが読めないのはアプリ起動不可の致命的エラー
}
```

### ❌ Result型の中で例外を投げる

```typescript
// BAD: Result型を返すのに例外を投げる
function validate(input: Input): Result<Valid, ValidationError> {
  if (!input) {
    throw new Error('input is required'); // ❌
  }
  // ...
}

// GOOD: 全てResult型で返す
function validate(input: Input): Result<Valid, ValidationError> {
  if (!input) {
    return err({ type: 'REQUIRED', field: 'input' });
  }
  // ...
}
```

### ❌ 過度なネスト

```typescript
// BAD: ネストが深くなる
const result1 = step1();
if (result1.isOk()) {
  const result2 = step2(result1.value);
  if (result2.isOk()) {
    const result3 = step3(result2.value);
    // ...
  }
}

// GOOD: andThenでフラットに
const result = step1()
  .andThen(step2)
  .andThen(step3);
```
