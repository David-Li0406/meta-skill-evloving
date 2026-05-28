---
name: expense-sharing
description: Use this skill when working with shared expenses, split calculations, payment status transitions, or settlement balances.
---

# Skill body

## Expense Sharing Domain Knowledge

### Schema Overview

#### SharedExpense Model
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

#### ExpenseParticipant Model
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

### Split Types
```typescript
enum SplitType {
  EQUAL      // Divide total equally among all participants + owner
  PERCENTAGE // Each participant gets a specified percentage
  FIXED      // Each participant gets a fixed amount
}
```

### calculateShares Function
Location: `src/app/actions/expense-sharing.ts`
```typescript
export function calculateShares(
  splitType: SplitType,
  totalAmount: number,
  participants: Array<{ email: string; shareAmount?: number; sharePercentage?: number }>,
  validEmails: string[],
): Map<string, { amount: number; percentage: number | null }>
```

#### EQUAL Split Logic
```typescript
// Divide among (numParticipants + 1) to include owner
const equalShare = Math.round((totalAmount / (numParticipants + 1)) * 100) / 100
```

#### PERCENTAGE Split Logic
```typescript
// Validation: total percentage must not exceed 100%
const amount = Math.round(totalAmount * (percentage / 100) * 100) / 100
```

#### FIXED Split Logic
```typescript
// Validation: total fixed amounts cannot exceed totalAmount
// Each participant gets their specified shareAmount
```

### Payment Status Transitions
```
PENDING → PAID      (owner marks as received)
PENDING → DECLINED  (participant declines payment)
```