# Common Schema Patterns

## Table Definition

```typescript
import { pgTable, uuid, text, timestamp } from "drizzle-orm/pg-core"

export const tableName = pgTable("table_name", {
    id: uuid("id").primaryKey().defaultRandom(),
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull(),
})
```

## Timestamps Pattern

Always include created/updated timestamps:

```typescript
createdAt: timestamp("created_at").defaultNow().notNull(),
updatedAt: timestamp("updated_at").defaultNow().notNull(),
```

Update `updatedAt` in your queries:

```typescript
await db.update(table)
    .set({ ...data, updatedAt: new Date() })
    .where(eq(table.id, id))
```

## Soft Delete Pattern

```typescript
deletedAt: timestamp("deleted_at"),
```

Query only non-deleted:

```typescript
await db.select()
    .from(table)
    .where(isNull(table.deletedAt))
```

## Foreign Keys

```typescript
userId: uuid("user_id")
    .references(() => users.id)
    .notNull(),
```

With cascade delete:

```typescript
userId: uuid("user_id")
    .references(() => users.id, { onDelete: "cascade" })
    .notNull(),
```

## Indexes

```typescript
export const users = pgTable("users", {
    id: uuid("id").primaryKey(),
    email: text("email").unique().notNull(),
    name: text("name"),
}, (table) => ({
    // Single column index
    emailIdx: index("email_idx").on(table.email),
    // Multi-column index
    nameEmailIdx: index("name_email_idx").on(table.name, table.email),
}))
```

## Unique Constraints

```typescript
// Single column
email: text("email").unique().notNull(),

// Multi-column (in table definition)
export const table = pgTable("table", {
    // columns
}, (table) => ({
    uniqueConstraint: unique("unique_name").on(table.col1, table.col2),
}))
```

## Enum Pattern

```typescript
// Define enum
export const statusEnum = pgEnum("status", ["pending", "active", "completed"])

// Use in table
export const tasks = pgTable("tasks", {
    id: uuid("id").primaryKey(),
    status: statusEnum("status").default("pending").notNull(),
})
```

## JSON Fields

```typescript
// For flexible metadata
metadata: jsonb("metadata"),

// With TypeScript typing
metadata: jsonb("metadata").$type<{ 
    key1: string
    key2: number 
}>(),
```

## Self-Referencing

```typescript
export const categories = pgTable("categories", {
    id: uuid("id").primaryKey(),
    name: text("name").notNull(),
    parentId: uuid("parent_id").references((): AnyPgColumn => categories.id),
})
```

## Many-to-Many Junction Table

```typescript
export const userRoles = pgTable("user_roles", {
    userId: uuid("user_id")
        .references(() => users.id, { onDelete: "cascade" })
        .notNull(),
    roleId: uuid("role_id")
        .references(() => roles.id, { onDelete: "cascade" })
        .notNull(),
}, (table) => ({
    pk: primaryKey({ columns: [table.userId, table.roleId] }),
}))
```

## Audit Trail Pattern

```typescript
export const auditLog = pgTable("audit_log", {
    id: uuid("id").primaryKey().defaultRandom(),
    tableName: text("table_name").notNull(),
    recordId: uuid("record_id").notNull(),
    action: text("action").notNull(), // 'create', 'update', 'delete'
    changes: jsonb("changes"),
    userId: uuid("user_id").references(() => users.id),
    createdAt: timestamp("created_at").defaultNow().notNull(),
})
```

## Versioning Pattern

```typescript
export const documents = pgTable("documents", {
    id: uuid("id").primaryKey(),
    version: integer("version").default(1).notNull(),
    content: text("content"),
    updatedAt: timestamp("updated_at").defaultNow().notNull(),
})

// Increment version on update
await db.update(documents)
    .set({ 
        content: newContent,
        version: sql`${documents.version} + 1`,
        updatedAt: new Date()
    })
    .where(eq(documents.id, id))
```

## Composite Primary Key

```typescript
export const table = pgTable("table", {
    key1: text("key1"),
    key2: text("key2"),
    value: text("value"),
}, (table) => ({
    pk: primaryKey({ columns: [table.key1, table.key2] }),
}))
```

## Default Values Pattern

```typescript
// Static default
status: text("status").default("pending"),

// SQL function default
createdAt: timestamp("created_at").default(sql`now()`),

// UUID default
id: uuid("id").default(sql`gen_random_uuid()`),
```

## Nullable vs Not Null

```typescript
// Required field
name: text("name").notNull(),

// Optional field
description: text("description"),

// Optional with default
status: text("status").default("pending"),
```

## Check Constraints

```typescript
export const products = pgTable("products", {
    id: uuid("id").primaryKey(),
    price: decimal("price", { precision: 10, scale: 2 }),
}, (table) => ({
    priceCheck: check("price_check", sql`${table.price} >= 0`),
}))
```

## Full Example: Organizations Table

```typescript
import { pgTable, uuid, text, integer, decimal, timestamp, varchar, index } from "drizzle-orm/pg-core"

export const organizations = pgTable("organizations", {
    // Primary key
    id: uuid("id").primaryKey().defaultRandom(),
    
    // Required fields
    name: text("name").notNull(),
    slug: text("slug").unique().notNull(),
    
    // Numeric fields with defaults
    handicapPercentage: decimal("handicap_percentage", { 
        precision: 3, 
        scale: 2 
    }).default("1.00").notNull(),
    
    minScoresToCalculate: integer("min_scores_to_calculate")
        .default(3)
        .notNull(),
    
    teeTimeInterval: integer("tee_time_interval")
        .default(10)
        .notNull(),
    
    defaultHoles: integer("default_holes")
        .default(18)
        .notNull(),
    
    // Optional fields
    defaultTeeTime: text("default_tee_time").default("16:00"),
    
    // Constrained varchar
    rotationStrategy: varchar("rotation_strategy", { length: 50 })
        .default("sequential")
        .notNull(),
    
    // Timestamps
    createdAt: timestamp("created_at").defaultNow().notNull(),
    updatedAt: timestamp("updated_at").defaultNow().notNull(),
}, (table) => ({
    // Indexes
    slugIdx: index("organizations_slug_idx").on(table.slug),
}))
```
