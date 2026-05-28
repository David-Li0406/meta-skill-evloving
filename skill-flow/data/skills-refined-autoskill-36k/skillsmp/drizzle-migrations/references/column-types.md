# Drizzle Column Types Reference

## Text Types

### text()
```typescript
name: text("name")
```
- Variable-length text
- No length limit
- Best for: names, descriptions, content

### varchar()
```typescript
status: varchar("status", { length: 50 })
```
- Variable-length with max length
- Enforces length constraint
- Best for: status codes, categories, short strings

### char()
```typescript
code: char("code", { length: 10 })
```
- Fixed-length text
- Pads with spaces
- Best for: fixed-format codes

## Numeric Types

### integer()
```typescript
count: integer("count")
```
- 32-bit integer
- Range: -2,147,483,648 to 2,147,483,647
- Best for: counts, IDs, whole numbers

### bigint()
```typescript
largeNumber: bigint("large_number", { mode: "number" })
```
- 64-bit integer
- Use `mode: "bigint"` for JavaScript BigInt
- Best for: large counts, timestamps

### decimal()
```typescript
price: decimal("price", { precision: 10, scale: 2 })
```
- Exact decimal numbers
- `precision`: total digits
- `scale`: digits after decimal
- Best for: money, percentages, precise calculations

### real()
```typescript
rating: real("rating")
```
- Floating point (32-bit)
- Approximate values
- Best for: ratings, measurements

### doublePrecision()
```typescript
coordinate: doublePrecision("coordinate")
```
- Floating point (64-bit)
- More precise than real
- Best for: scientific data, coordinates

## Boolean

### boolean()
```typescript
isActive: boolean("is_active")
```
- True/false values
- Stored as true/false in PostgreSQL
- Best for: flags, toggles

## Date/Time Types

### timestamp()
```typescript
createdAt: timestamp("created_at").defaultNow()
```
- Date and time
- No timezone by default
- Best for: creation times, updates

### timestamp() with timezone
```typescript
scheduledAt: timestamp("scheduled_at", { withTimezone: true })
```
- Date and time with timezone
- Best for: user-facing times across timezones

### date()
```typescript
birthDate: date("birth_date")
```
- Date only (no time)
- Best for: birthdays, deadlines

### time()
```typescript
startTime: time("start_time")
```
- Time only (no date)
- Best for: daily schedules

## UUID

### uuid()
```typescript
id: uuid("id").primaryKey().defaultRandom()
```
- Universally unique identifier
- Use `.defaultRandom()` for auto-generation
- Best for: primary keys, distributed systems

## JSON

### json()
```typescript
metadata: json("metadata")
```
- JSON data
- Stored as text, parsed on retrieval
- Best for: flexible schemas, metadata

### jsonb()
```typescript
settings: jsonb("settings")
```
- Binary JSON
- Faster queries, more storage
- Best for: queried JSON data

## Arrays

### array()
```typescript
tags: text("tags").array()
```
- Array of any type
- PostgreSQL native arrays
- Best for: lists, tags

## Enum

### Custom enum type
```typescript
// Define enum
export const roleEnum = pgEnum("role", ["admin", "user", "guest"])

// Use in schema
role: roleEnum("role").default("user")
```
- Predefined set of values
- Type-safe in TypeScript
- Best for: status codes, categories

## Common Modifiers

### .notNull()
```typescript
name: text("name").notNull()
```
- Prevents NULL values
- Always provide default for existing data

### .default()
```typescript
status: text("status").default("pending")
```
- Default value for new rows
- Can be static value or SQL function

### .defaultNow()
```typescript
createdAt: timestamp("created_at").defaultNow()
```
- Sets current timestamp
- Only for timestamp columns

### .defaultRandom()
```typescript
id: uuid("id").defaultRandom()
```
- Generates random UUID
- Only for uuid columns

### .primaryKey()
```typescript
id: uuid("id").primaryKey()
```
- Marks as primary key
- Automatically creates index

### .unique()
```typescript
email: text("email").unique()
```
- Enforces uniqueness
- Creates unique index

### .references()
```typescript
userId: uuid("user_id").references(() => users.id)
```
- Foreign key constraint
- Links to another table

## Type Selection Guide

| Data Type | Use Case | Drizzle Type |
|-----------|----------|--------------|
| Short text (\<255 chars) | varchar |
| Long text | text |
| Whole numbers | integer |
| Large whole numbers | bigint |
| Money/prices | decimal(10, 2) |
| Percentages | decimal(5, 2) |
| True/false | boolean |
| Timestamps | timestamp |
| Dates only | date |
| UUIDs | uuid |
| Flexible data | jsonb |
| Lists | array |
| Fixed options | enum |

## Examples from Project

```typescript
export const organizations = pgTable("organizations", {
    id: uuid("id").primaryKey().defaultRandom(),
    name: text("name").notNull(),
    slug: text("slug").unique().notNull(),
    handicapPercentage: decimal("handicap_percentage", { precision: 3, scale: 2 }).default("1.00").notNull(),
    minScoresToCalculate: integer("min_scores_to_calculate").default(3).notNull(),
    defaultTeeTime: text("default_tee_time").default("16:00"),
    teeTimeInterval: integer("tee_time_interval").default(10).notNull(),
    defaultHoles: integer("default_holes").default(18).notNull(),
    rotationStrategy: varchar("rotation_strategy", { length: 50 }).default("sequential").notNull(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull(),
})
```
