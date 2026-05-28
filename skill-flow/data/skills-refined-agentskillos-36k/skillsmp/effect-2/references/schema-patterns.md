# Schema Patterns

## Branded Types for IDs

Always brand entity IDs to prevent mixing incompatible types:

```typescript
// Define branded ID
const UserId = Schema.String.pipe(Schema.brand("@App/UserId"))
type UserId = typeof UserId.Type

const OrderId = Schema.String.pipe(Schema.brand("@App/OrderId"))
type OrderId = typeof OrderId.Type

// Compile error - can't pass OrderId where UserId expected
const findUser = (id: UserId) => /* ... */
findUser(orderId) // Type error!

// Create branded value
const userId = UserId.make("user_123")
```

## UUID Branded Types

```typescript
const UserId = Schema.UUID.pipe(Schema.brand("@App/UserId"))

// Or with validation message
const UserId = Schema.String.pipe(
  Schema.pattern(/^user_[a-z0-9]+$/),
  Schema.brand("@App/UserId"),
  Schema.annotations({ description: "User identifier" })
)
```

## Structs for Domain Types

```typescript
const UserInput = Schema.Struct({
  email: Schema.String.pipe(Schema.pattern(/@/)),
  name: Schema.String.pipe(Schema.minLength(1)),
  age: Schema.Number.pipe(Schema.int(), Schema.positive()),
})
type UserInput = typeof UserInput.Type

// Encoded type for serialization
type UserInputEncoded = typeof UserInput.Encoded
```

## Schema.Class for Entities with Methods

```typescript
class User extends Schema.Class<User>("User")({
  id: UserId,
  email: Schema.String,
  firstName: Schema.String,
  lastName: Schema.String,
  createdAt: Schema.DateFromSelf,
}) {
  get fullName() {
    return `${this.firstName} ${this.lastName}`
  }

  get isNew() {
    const oneWeekAgo = Date.now() - 7 * 24 * 60 * 60 * 1000
    return this.createdAt.getTime() > oneWeekAgo
  }
}

// Schema.Class provides:
// - Automatic Equal/Hash implementation
// - Schema validation
// - Methods on instances
```

## Transforms

```typescript
// String to Date
const DateFromString = Schema.transform(
  Schema.String,
  Schema.DateFromSelf,
  {
    decode: (s) => new Date(s),
    encode: (d) => d.toISOString(),
  }
)

// Cents to Dollars
const DollarsFromCents = Schema.transform(
  Schema.Number,
  Schema.Number,
  {
    decode: (cents) => cents / 100,
    encode: (dollars) => Math.round(dollars * 100),
  }
)

// Fallible transform
const SafeJson = Schema.transformOrFail(
  Schema.String,
  Schema.Unknown,
  {
    decode: (s, _, ast) =>
      Effect.try({
        try: () => JSON.parse(s),
        catch: () => new ParseResult.Type(ast, s, "Invalid JSON"),
      }),
    encode: (obj) => Effect.succeed(JSON.stringify(obj)),
  }
)
```

## Optional Fields with Defaults

```typescript
const Config = Schema.Struct({
  host: Schema.String,
  port: Schema.optional(Schema.Number, { default: () => 3000 }),
  debug: Schema.optional(Schema.Boolean, { default: () => false }),
})

// Decoding adds defaults
const config = Schema.decodeUnknownSync(Config)({ host: "localhost" })
// { host: "localhost", port: 3000, debug: false }
```

## Discriminated Unions

```typescript
const PaymentMethod = Schema.Union(
  Schema.Struct({
    _tag: Schema.Literal("CreditCard"),
    cardNumber: Schema.String,
    expiry: Schema.String,
  }),
  Schema.Struct({
    _tag: Schema.Literal("BankTransfer"),
    accountNumber: Schema.String,
    routingNumber: Schema.String,
  }),
  Schema.Struct({
    _tag: Schema.Literal("Crypto"),
    walletAddress: Schema.String,
  })
)

// Pattern match
const describe = (pm: typeof PaymentMethod.Type) => {
  switch (pm._tag) {
    case "CreditCard": return `Card ending ${pm.cardNumber.slice(-4)}`
    case "BankTransfer": return `Bank account ${pm.accountNumber}`
    case "Crypto": return `Wallet ${pm.walletAddress.slice(0, 8)}...`
  }
}
```

## Enums vs Literals

```typescript
// Literals for small fixed sets
const Status = Schema.Literal("pending", "active", "archived")

// Enums for larger sets or when you need runtime values
enum OrderStatus {
  Pending = "pending",
  Processing = "processing",
  Shipped = "shipped",
  Delivered = "delivered",
  Cancelled = "cancelled",
}
const OrderStatusSchema = Schema.Enums(OrderStatus)
```

## Recursive Schemas

```typescript
interface Category {
  name: string
  children: readonly Category[]
}

const Category: Schema.Schema<Category> = Schema.Struct({
  name: Schema.String,
  children: Schema.Array(Schema.suspend(() => Category)),
})
```

## Decoding with Effect

```typescript
// Async decoding - preferred
const user = yield* Schema.decodeUnknown(User)(rawData)

// With error handling
const user = yield* Schema.decodeUnknown(User)(rawData).pipe(
  Effect.mapError((e) => new ValidationError({ issues: e.issues }))
)

// Sync decoding (only when Effect context unavailable)
const user = Schema.decodeUnknownSync(User)(rawData)
```

## Annotations for Documentation

```typescript
const Email = Schema.String.pipe(
  Schema.pattern(/@/),
  Schema.annotations({
    title: "Email Address",
    description: "A valid email address",
    examples: ["user@example.com"],
  })
)

const UserId = Schema.UUID.pipe(
  Schema.brand("@App/UserId"),
  Schema.annotations({
    description: "Unique identifier for a user",
  })
)
```

## Use Chunk Instead of Array

For structural equality and Effect integration:

```typescript
import { Chunk } from "effect"

const UserList = Schema.Struct({
  users: Schema.Chunk(User),
})

// Chunk provides:
// - Structural equality (Equal trait)
// - Immutable operations
// - Better Effect integration
```
