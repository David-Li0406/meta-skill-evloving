---
name: backend-patterns
description: |
  このスキルは、ユーザーが「API設計」「Repository」「サービス層」「キャッシュ」「バックエンド」「サーバーサイド」について質問したとき、またはバックエンドパターンを実装する必要があるときに使用する。
---

# Backend Patterns

## API 設計

### RESTful API

```typescript
// エンドポイント設計
GET    /api/users          # 一覧取得
GET    /api/users/:id      # 詳細取得
POST   /api/users          # 作成
PUT    /api/users/:id      # 更新
DELETE /api/users/:id      # 削除
```

### レスポンス形式

```typescript
// 成功レスポンス
type SuccessResponse<T> = {
  success: true;
  data: T;
};

// エラーレスポンス
type ErrorResponse = {
  success: false;
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
};

type ApiResponse<T> = SuccessResponse<T> | ErrorResponse;
```

### エラーハンドリング

```typescript
// HTTP ステータスコード
200: 成功
201: 作成成功
400: バリデーションエラー
401: 認証エラー
403: 認可エラー
404: リソース未発見
500: サーバーエラー
```

## Repository パターン

### インターフェース定義

```typescript
interface Repository<T, ID> {
  findById(id: ID): Promise<T | null>;
  findAll(): Promise<T[]>;
  save(entity: T): Promise<T>;
  delete(id: ID): Promise<void>;
}
```

### 実装例（Prisma）

```typescript
class PrismaUserRepository implements UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string): Promise<User | null> {
    return this.prisma.user.findUnique({ where: { id } });
  }

  async save(user: User): Promise<User> {
    return this.prisma.user.upsert({
      where: { id: user.id },
      create: user,
      update: user,
    });
  }
}
```

## サービス層

### ユースケース実装

```typescript
class CreateUserUseCase {
  constructor(
    private userRepository: UserRepository,
    private emailService: EmailService
  ) {}

  async execute(input: CreateUserInput): Promise<User> {
    // バリデーション
    const validated = CreateUserSchema.parse(input);

    // ビジネスロジック
    const user = User.create(validated);

    // 永続化
    const saved = await this.userRepository.save(user);

    // 副作用
    await this.emailService.sendWelcome(saved.email);

    return saved;
  }
}
```

## キャッシュ戦略

### キャッシュパターン

```typescript
// Cache-Aside パターン
async function getUser(id: string): Promise<User> {
  // 1. キャッシュ確認
  const cached = await cache.get(`user:${id}`);
  if (cached) return cached;

  // 2. DB から取得
  const user = await userRepository.findById(id);

  // 3. キャッシュに保存
  await cache.set(`user:${id}`, user, { ttl: 3600 });

  return user;
}
```

### キャッシュ無効化

```typescript
// 更新時のキャッシュ無効化
async function updateUser(id: string, data: UpdateUserInput): Promise<User> {
  const updated = await userRepository.update(id, data);

  // キャッシュ無効化
  await cache.delete(`user:${id}`);

  return updated;
}
```

## エラーハンドリング

### Result パターン

```typescript
type Result<T, E = Error> =
  | { success: true; value: T }
  | { success: false; error: E };

function ok<T>(value: T): Result<T, never> {
  return { success: true, value };
}

function err<E>(error: E): Result<never, E> {
  return { success: false, error };
}
```

## トランザクション

```typescript
// Prisma でのトランザクション
async function transferFunds(from: string, to: string, amount: number) {
  return prisma.$transaction(async (tx) => {
    const sender = await tx.account.update({
      where: { id: from },
      data: { balance: { decrement: amount } },
    });

    const receiver = await tx.account.update({
      where: { id: to },
      data: { balance: { increment: amount } },
    });

    return { sender, receiver };
  });
}
```
