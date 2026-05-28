---
name: expense-sharing
description: Expense sharing calculations, split types (EQUAL/PERCENTAGE/FIXED), participant state management, and settlement tracking. Use when working with shared expenses, split calculations, payment status transitions, or settlement balances.
---

# Expense Sharing Domain Knowledge

## Schema Overview

### SharedExpense Model
```prisma
model SharedExpense {
  id            String               @id @default(cuid())
  transactionId String               @unique
  ownerId       String
  splitType     SplitType            @default(EQUAL)
  totalAmount   Decimal              @db.Decimal(12, 2)
  currency      Currency             @default(USD)
  description   String?

  transaction   Transaction          @relation(...)
  owner         User                 @relation("SharedExpensesOwned", ...)
  participants  ExpenseParticipant[]
}
```

### ExpenseParticipant Model
```prisma
model ExpenseParticipant {
  id              String        @id @default(cuid())
  sharedExpenseId String
  userId          String
  shareAmount     Decimal       @db.Decimal(12, 2)
  sharePercentage Decimal?      @db.Decimal(5, 2)
  status          PaymentStatus @default(PENDING)
  paidAt          DateTime?
  reminderSentAt  DateTime?

  @@unique([sharedExpenseId, userId])
}
```

## Split Types

```typescript
enum SplitType {
  EQUAL      // Divide total equally among all participants + owner
  PERCENTAGE // Each participant gets a specified percentage
  FIXED      // Each participant gets a fixed amount
}
```

## calculateShares Function

Location: `src/app/actions/expense-sharing.ts`

```typescript
export function calculateShares(
  splitType: SplitType,
  totalAmount: number,
  participants: Array<{ email: string; shareAmount?: number; sharePercentage?: number }>,
  validEmails: string[],
): Map<string, { amount: number; percentage: number | null }>
```

### EQUAL Split Logic
```typescript
// Divide among (numParticipants + 1) to include owner
const equalShare = Math.round((totalAmount / (numParticipants + 1)) * 100) / 100
```

### PERCENTAGE Split Logic
```typescript
// Validation: total percentage must not exceed 100%
const amount = Math.round(totalAmount * (percentage / 100) * 100) / 100
```

### FIXED Split Logic
```typescript
// Validation: total fixed amounts cannot exceed totalAmount
// Each participant gets their specified shareAmount
```

## Payment Status Transitions

```
PENDING → PAID      (owner marks as received)
PENDING → DECLINED  (participant declines)
PAID → (terminal)
DECLINED → (terminal)
```

**Transition Rules:**
- Only owner can mark PENDING → PAID via `markSharePaidAction`
- Only participant can DECLINE their own share via `declineShareAction`
- Cannot mark DECLINED share as PAID

## Action Pipeline

All expense sharing actions follow:
```typescript
1. parseInput(schema, input)      // Zod validation
2. requireCsrfToken(csrfToken)    // CSRF protection
3. requireActiveSubscription()    // Subscription gate
4. requireAuthUser()              // Authentication
5. Authorization check            // Ownership/participant verification
6. Business logic
7. revalidatePath('/')            // Cache invalidation
8. return success/error
```

## Email Notifications

- `sendExpenseSharedEmail`: Sent to each participant when expense is shared
- `sendPaymentReminderEmail`: 24-hour cooldown (REMINDER_COOLDOWN_HOURS = 24)

## Settlement Balance Calculation

Location: `src/lib/finance.ts` (getSettlementBalances)

Groups by user AND currency to avoid mixing currencies:
```typescript
// Returns for each user:
{
  userId: string
  youOwe: number    // What you owe them (PENDING expenses they shared with you)
  theyOwe: number   // What they owe you (PENDING expenses you shared with them)
  netBalance: number // theyOwe - youOwe
}
```

## Key Files

- `src/app/actions/expense-sharing.ts` - All sharing actions
- `src/lib/finance.ts` - calculateShares, getSettlementBalances
- `src/schemas/index.ts` - shareExpenseSchema, participantSchema
- `tests/calculate-shares.test.ts` - Unit tests for split calculations
