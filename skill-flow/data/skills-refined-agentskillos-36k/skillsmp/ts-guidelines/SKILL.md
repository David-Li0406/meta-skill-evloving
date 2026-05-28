---
name: ts-guidelines
description: TypeScriptコードを書く際のコーディングガイドライン。型安全性、モダンな構文、可読性を重視したベストプラクティス。
---

# TypeScript Coding Guidelines

## 基本方針

- JavaScriptが含まれるすべてのコードベースでTypeScriptを使用する
- **`strict: true`** を必ず有効にする
- 状態を内包するクラスの使用を避け、関数を優先する（意味のある状態管理や依存注入が必要な場合を除く）

## 型システム

### any を避け、unknown で絞り込む

```typescript
// Bad
catch (error: any) {
  console.log(error.message)
}

// Good
catch (error: unknown) {
  if (error instanceof Error) {
    console.log(error.message)
  } else if (typeof error === "object" && error !== null && "message" in error) {
    console.log((error as { message: string }).message)
  } else {
    console.log(String(error))
  }
}
```

### Type vs Interface

- **オブジェクト型**: `interface` を使用
- **プリミティブ・Union・Tuple**: `type` を使用

```typescript
// Object shape -> interface
interface User {
  id: string
  name: string
}

// Union/Primitive -> type
type Status = "pending" | "success" | "error"
type ID = string | number
```

### 型推論を活用

推論可能な場所では型注釈を省略:

```typescript
// Good
const items = [1, 2, 3]
const user = { name: "John", age: 30 }

// Bad - 冗長
const items: number[] = [1, 2, 3]
```

### Utility Types を活用

`Partial<T>`, `Required<T>`, `Pick<T, K>`, `Omit<T, K>`, `Record<K, V>`, `ReturnType<T>`

使用するプロパティが一部で済む場合は `Pick` で必要なプロパティのみ受け取る:

```typescript
interface User {
  id: string
  name: string
  email: string
}

function findUser({ id }: Pick<User, "id">) {
  // ...
}
```

## 型アサーション・型ガード

### 型ガードを優先

型アサーション（constアサーションを除く）はやむを得ない場合のみ使う:

```typescript
// Good - 型ガード
if (value instanceof Error) {
  // value is Error
}

// Avoid - 型アサーション
const error = value as Error
```

### 型ガード関数

複雑な絞り込みや使い回す場合は関数に纏める:

```typescript
function isKeyboardEvent(event: Event): event is KeyboardEvent {
  return "key" in event
}
```

### 非Nullアサーション

`!` はやむを得ない場合のみ。適切なnullチェックを優先:

```typescript
// Avoid
const name = user!.name

// Good
const name = user?.name ?? "Anonymous"
```

## enum を避ける

リテラル型と const アサーション、またはユニオン型を使用:

```typescript
// Good
const STATUS = {
  Loading: "loading",
  Success: "success",
  Error: "error",
} as const

type Status = (typeof STATUS)[keyof typeof STATUS]

// Also Good - シンプルな場合
type Status = "loading" | "success" | "error"

// Bad
enum Status {
  Loading = "loading",
  Success = "success",
  Error = "error",
}
```

## Discriminated Unions

ユニオン型の絞り込みが複雑になった際はディスクリミネータで分岐:

```typescript
type Shape =
  | { kind: "circle"; radius: number }
  | { kind: "square"; size: number }

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.radius ** 2
    case "square":
      return shape.size ** 2
  }
}
```

## 関数

### Options Object パターン

複数の引数を渡すときはオブジェクトにまとめる:

```typescript
// Good
function createUser(options: { name: string; email: string; role?: string }) {
  // ...
}

// Bad
function createUser(name: string, email: string, role?: string) {
  // ...
}
```

### Arrow Functions

- コールバック・短い関数: arrow function
- メソッド定義: shorthand method syntax

```typescript
// Callbacks
items.filter((item) => item.active)

// Object methods
const service = {
  fetch() {
    return api.get("/data")
  },
}
```

### 戻り値の型

- Public API: 明示的に記述
- 内部関数: 推論に任せる

## エラー処理

### Result Pattern

例外の代わりに Result 型を検討:

```typescript
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E }

function parseJson(text: string): Result<unknown> {
  try {
    return { ok: true, value: JSON.parse(text) }
  } catch (error) {
    return { ok: false, error: error instanceof Error ? error : new Error(String(error)) }
  }
}
```

## Async/Await

- Promise chain より async/await を優先
- 並列処理は `Promise.all()` / `Promise.allSettled()`

```typescript
// Parallel execution
const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()])
```

## モダン構文

### Optional Chaining & Nullish Coalescing

```typescript
// Good
const name = user?.profile?.name ?? "Anonymous"

// Bad
const name = user && user.profile && user.profile.name ? user.profile.name : "Anonymous"
```

### ES Modules

```typescript
// Named exports を優先
export { UserService, createUser }

// Default export は避ける（リファクタリング時に追跡困難）
```

## Import 順序

1. Node.js built-in modules
2. External packages
3. Internal modules (absolute path)
4. Relative imports

```typescript
import { readFile } from "node:fs/promises"

import { z } from "zod"

import { config } from "@/config"

import { helper } from "./helper"
```

## 命名規則

> **Note**: 新規PJではこれを採用。既存PJではそのPJの規約に従う。

| 種類 | 規則 | 例 |
|------|------|-----|
| 変数・関数 | camelCase | `getUserById` |
| クラス・型・interface | PascalCase | `UserService` |
| 定数 | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT` |
| Boolean | is/has/can prefix | `isActive`, `hasPermission` |
| Private | `#` prefix (ES2022) | `#cache` |

## 避けるべきもの

- `enum` → Union型 or `as const` オブジェクト
- `namespace` → ES Modules
- `!` (non-null assertion) → 適切なnullチェック
- `any` → `unknown` + 型ガード
- Class乱用 → 関数で十分な場合が多い
- Default export → Named export

## 参考

- https://google.github.io/styleguide/tsguide.html
