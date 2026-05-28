---
name: prisma-patterns
description: Use this skill when working with Prisma schema changes, unique constraints, decimal precision, or database operations.
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