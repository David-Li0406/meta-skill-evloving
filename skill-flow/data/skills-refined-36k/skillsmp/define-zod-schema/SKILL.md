---
name: define-zod-schema
description: このプロジェクトにおけるZodスキーマの定義方法を理解し、適切にスキーマを定義・使用できる。
---

# Define Zod Schema

## 概要

このプロジェクトではバリデーションにZodを使用しますが、バンドルサイズ削減のために **Zod Mini** (`@zod/zod/mini`)
を使用します。

## Zod Miniについて

Zod Miniは、Zod 4で導入された tree-shakable
なバリアントです。通常のZodと同じ機能を提供しますが、関数ベースのAPIを使用することで、バンドラーが未使用のコードを削除できるようになっています。

### 通常のZodとの違い

通常のZodではメソッドチェーンを使用しますが、Zod Miniでは関数を使用します:

```typescript
// 通常のZod
z.string().optional().nullable()

// Zod Mini
z.nullable(z.optional(z.string()))
```

チェック（バリデーション）も同様に関数を使用します:

```typescript
// 通常のZod
z.string().min(5).max(10).trim()

// Zod Mini
z.string().check(z.minLength(5), z.maxLength(10), z.trim())
```

## インポート方法

`deno.jsonc` では `@zod/zod` のみを定義し、コード内では `/mini` サブパスをインポートします:

```typescript
import { z } from '@zod/zod/mini'
```

この方法により、Tree-shakingが可能になり、バンドルサイズを削減できます。

## スキーマの命名規則

Zodスキーマの命名には以下の規則を適用します:

- **PascalCase** を使用します
- `Schema` のサフィックスを付けます

```typescript
// 良い例
const UserSchema = z.object({
  name: z.string(),
  age: z.number(),
})

const EmailSchema = z.string().check(
  z.minLength(1),
  z.regex(/@/),
)

// 悪い例
const userSchema = z.object({/* ... */}) // camelCase
const User = z.object({/* ... */}) // サフィックスなし
```

## 型エイリアスのエクスポート

Zodスキーマを定義した際は、`z.infer` を使用して型エイリアスも同時にエクスポートします。

型エイリアスの命名規則:

- スキーマ名から `Schema` サフィックスを除いた名前を使用します
- 例: `UserSchema` → `User`、`EmailSchema` → `Email`

```typescript
import { z } from '@zod/zod/mini'

// スキーマと型を同時にエクスポート
export const UserSchema = z.object({
  name: z.string(),
  age: z.number(),
  email: z.string(),
})
export type User = z.infer<typeof UserSchema>

// 使用例
const user: User = {
  name: 'John',
  age: 30,
  email: 'john@example.com',
}

// パースも可能
const parsed = UserSchema.parse(user)
```

この規則により、スキーマとその型定義が常にペアで提供され、型安全性が向上します。

## 利用可能なチェック関数

`.check()` メソッドには以下のチェック関数を渡すことができます:

### 数値チェック

- `z.lt(value)` - 未満
- `z.lte(value)` / `z.maximum(value)` - 以下
- `z.gt(value)` - より大きい
- `z.gte(value)` / `z.minimum(value)` - 以上
- `z.positive()` - 正の数
- `z.negative()` - 負の数
- `z.nonpositive()` - 0以下
- `z.nonnegative()` - 0以上
- `z.multipleOf(value)` - 倍数

### 長さ・サイズチェック

- `z.maxSize(value)` - 最大サイズ
- `z.minSize(value)` - 最小サイズ
- `z.size(value)` - サイズ
- `z.maxLength(value)` - 最大長
- `z.minLength(value)` - 最小長
- `z.length(value)` - 長さ

### 文字列チェック

- `z.regex(regex)` - 正規表現
- `z.lowercase()` - 小文字
- `z.uppercase()` - 大文字
- `z.includes(value)` - 含む
- `z.startsWith(value)` - 始まる
- `z.endsWith(value)` - 終わる

### その他

- `z.property(key, schema)` - プロパティ
- `z.mime(value)` - MIMEタイプ
- `z.refine()` - カスタムチェック
- `z.check()` - カスタムチェック（`.superRefine()` の代替）

### 変換（型は変更されません）

- `z.overwrite(value => newValue)` - 値を上書き
- `z.normalize()` - 正規化
- `z.trim()` - トリム
- `z.toLowerCase()` - 小文字に変換
- `z.toUpperCase()` - 大文字に変換

## 使用例

```typescript
import { z } from '@zod/zod/mini'

// 基本的なスキーマ
const StringSchema = z.string()
const NumberSchema = z.number()
const BooleanSchema = z.boolean()

// オプショナル・nullable
const OptionalStringSchema = z.optional(z.string())
const NullableStringSchema = z.nullable(z.string())

// チェック付きスキーマ
const EmailSchema = z.string().check(
  z.minLength(1),
  z.regex(/^[^\s@]+@[^\s@]+\.[^\s@]+$/),
)

const PositiveIntegerSchema = z.number().check(
  z.positive(),
  z.multipleOf(1),
)

// オブジェクトスキーマ
const UserSchema = z.object({
  name: z.string().check(z.minLength(1)),
  age: z.number().check(z.gte(0)),
  email: EmailSchema,
})

// パース
const result = UserSchema.parse({
  name: 'John',
  age: 30,
  email: 'john@example.com',
})

// セーフパース
const safeResult = UserSchema.safeParse({
  name: 'John',
  age: -1, // エラー
  email: 'invalid', // エラー
})

if (!safeResult.success) {
  console.error(safeResult.error)
}
```

## 参考リンク

- [Zod Mini 公式ドキュメント](https://zod.dev/packages/mini)
