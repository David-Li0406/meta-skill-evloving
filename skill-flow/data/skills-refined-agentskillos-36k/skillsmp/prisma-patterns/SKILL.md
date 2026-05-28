---
name: prisma-patterns
description: Prisma schema constraints, decimal handling, soft delete patterns, and database conventions. Use when working with schema changes, unique constraints, decimal precision, or database operations.
---

# Prisma Patterns Domain Knowledge

## Decimal Handling

### Storage Precision
```prisma
// Financial amounts: 12 digits total, 2 decimal places
amount      Decimal @db.Decimal(12, 2)

// Exchange rates: 12 digits total, 6 decimal places
rate        Decimal @db.Decimal(12, 6)

// Percentages: 5 digits total, 2 decimal places
sharePercentage Decimal? @db.Decimal(5, 2)

// Stock quantities: 18 digits total, 6 decimal places (fractional shares)
quantity    Decimal @db.Decimal(18, 6)
```

### toDecimalString Helper

Location: `src/app/actions/shared.ts`

```typescript
const DECIMAL_PRECISION = 2
const AMOUNT_SCALE = Math.pow(10, DECIMAL_PRECISION)

export function toDecimalString(input: number): string {
  return (Math.round(input * AMOUNT_SCALE) / AMOUNT_SCALE).toFixed(DECIMAL_PRECISION)
}
```

**Usage:**
```typescript
amount: new Prisma.Decimal(toDecimalString(data.amount))
```

**Why:** JavaScript floats have precision issues (0.1 + 0.2 !== 0.3). Convert to safe string before creating Prisma.Decimal.

## Unique Constraints

### Composite Unique Keys

```prisma
// Budget: one per account+category+month
model Budget {
  @@unique([accountId, categoryId, month])
}

// Account: unique name per user
model Account {
  @@unique([userId, name])
}

// Category: unique name+type per user
model Category {
  @@unique([userId, name, type])
}

// Holding: unique symbol per account+category
model Holding {
  @@unique([accountId, categoryId, symbol])
}

// Exchange rate: one rate per currency pair per day
model ExchangeRate {
  @@unique([baseCurrency, targetCurrency, date])
}

// Expense participant: one entry per expense+user
model ExpenseParticipant {
  @@unique([sharedExpenseId, userId])
}
```

### Handling Unique Constraint Errors

Use `handlePrismaError` from `src/lib/prisma-errors.ts`:

```typescript
return handlePrismaError(error, {
  action: 'upsertBudget',
  accountId: data.accountId,
  input: data,
  uniqueMessage: 'Budget already exists for this account, category, and month',
  foreignKeyMessage: 'The selected account or category no longer exists',
  fallbackMessage: 'Unable to save budget',
})
```

## Soft Delete Pattern

Categories use `isArchived` instead of hard delete:

```prisma
model Category {
  isArchived Boolean @default(false)
}
```

**Why soft delete:**
- Preserves referential integrity (transactions reference categories)
- Allows unarchive if needed
- Historical data remains intact

**Query pattern:**
```typescript
const categories = await prisma.category.findMany({
  where: { userId: authUser.id, isArchived: false }
})
```

## Transaction Date Pattern

Transactions store both `date` and `month`:

```prisma
model Transaction {
  date  DateTime  // Actual transaction date
  month DateTime  // First day of month for aggregation
}
```

**Why both fields:**
- `date`: Precise transaction timestamp
- `month`: Normalized for efficient monthly aggregations/indexing

**Setting month:**
```typescript
import { getMonthStart } from '@/utils/date'

const monthStart = getMonthStart(data.date)
await prisma.transaction.create({
  data: {
    date: data.date,
    month: monthStart,
    // ...
  }
})
```

## Upsert Pattern

For budget and recurring templates:

```typescript
await prisma.budget.upsert({
  where: {
    accountId_categoryId_month: {
      accountId: data.accountId,
      categoryId: data.categoryId,
      month: monthStart,
    },
  },
  update: {
    planned: new Prisma.Decimal(toDecimalString(data.planned)),
    currency: data.currency,
    notes: data.notes,
  },
  create: {
    accountId: data.accountId,
    categoryId: data.categoryId,
    month: monthStart,
    planned: new Prisma.Decimal(toDecimalString(data.planned)),
    currency: data.currency,
    notes: data.notes,
  },
})
```

## Cascade Deletes

```prisma
model Account {
  user User @relation(fields: [userId], references: [id], onDelete: Cascade)
}
```

Deleting a User cascades to:
- Accounts → Budgets, Holdings, RecurringTemplates, Transactions
- Categories → (soft deleted, not cascade)
- RefreshTokens, Subscription, SharedExpenses

## Schema Change Workflow

After modifying `prisma/schema.prisma`:

```bash
npm run db:push && npm run prisma:generate
```

- `db:push`: Push schema changes to database (dev)
- `prisma:generate`: Regenerate TypeScript types

## Key Files

- `prisma/schema.prisma` - Schema definition
- `src/lib/prisma.ts` - Prisma client instance
- `src/lib/prisma-errors.ts` - Error handling utilities
- `src/app/actions/shared.ts` - toDecimalString helper
- `src/utils/date.ts` - getMonthStart, getMonthKey
