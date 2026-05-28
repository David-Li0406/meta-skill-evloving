# ドメインエラー

## 概要

ドメイン層で発生するエラーを定義。
ビジネスルール違反やリポジトリ操作の失敗を表現する。

## エラー階層

```
Error (JavaScript 標準)
└── DomainError (ドメイン層エラーの基底)
    ├── RepositoryError (リポジトリ操作エラー)
    │   ├── EntityCreationError (作成失敗)
    │   ├── EntityUpdateError (更新失敗)
    │   └── EntityDeletionError (削除失敗)
    └── EntityNotFoundError (エンティティ見つからない)
```

## 実装

```ts
// domain/errors/domain-error.ts

/**
 * ドメインエラーの基底クラス
 */
export class DomainError extends Error {
  constructor(message: string) {
    super(message)
    this.name = this.constructor.name
  }
}

/**
 * リポジトリ操作エラー
 */
export class RepositoryError extends DomainError {
  constructor(
    readonly operation: string,
    readonly cause?: Error,
  ) {
    super(`リポジトリ操作 (${operation}) に失敗しました`)
  }
}

/**
 * エンティティ作成エラー
 */
export class EntityCreationError extends RepositoryError {
  constructor(
    readonly entityName: string,
    cause?: Error,
  ) {
    super(`${entityName} の作成`, cause)
  }
}

/**
 * エンティティ更新エラー
 */
export class EntityUpdateError extends RepositoryError {
  constructor(
    readonly entityName: string,
    readonly id: string,
    cause?: Error,
  ) {
    super(`${entityName} (ID: ${id}) の更新`, cause)
  }
}

/**
 * エンティティ削除エラー
 */
export class EntityDeletionError extends RepositoryError {
  constructor(
    readonly entityName: string,
    readonly id: string,
    cause?: Error,
  ) {
    super(`${entityName} (ID: ${id}) の削除`, cause)
  }
}

/**
 * エンティティが見つからない
 */
export class EntityNotFoundError extends DomainError {
  constructor(
    readonly entityName: string,
    readonly id: string,
  ) {
    super(`${entityName} (ID: ${id}) が見つかりません`)
  }
}
```

## 使い分け

| エラー | 使用場面 |
|-------|---------|
| `EntityCreationError` | INSERT 失敗時 |
| `EntityUpdateError` | UPDATE 失敗時 |
| `EntityDeletionError` | DELETE 失敗時 |
| `EntityNotFoundError` | SELECT で見つからない時 |

## 使用例

### Repository での使用

```ts
async save(entity: CustomerEntity): Promise<void> {
  try {
    await this.db.insert(customers).values(this.toData(entity)).run()
  } catch (error) {
    throw new EntityCreationError("Customer", error as Error)
  }
}

async findById(id: string): Promise<CustomerEntity> {
  const record = await this.db.query.customers.findFirst({
    where: eq(customers.id, id),
  })

  if (!record) {
    throw new EntityNotFoundError("Customer", id)
  }

  return this.toDomain(record)
}
```

### Use Case での使用

```ts
async execute(props: Props) {
  try {
    const customer = await this.customerRepository.findById(props.id)
    // ...
  } catch (error) {
    if (error instanceof EntityNotFoundError) {
      return new NotFoundError("顧客が見つかりません")
    }
    throw error
  }
}
```
