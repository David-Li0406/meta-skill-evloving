# Architecture & Code Quality Reference

## Project Structure

```
apps/
├── web/                    # React frontend
│   └── src/
│       ├── features/       # Feature modules
│       │   ├── betting/
│       │   ├── simulin/
│       │   └── farm/
│       ├── shared/         # Shared components
│       └── stores/
└── server/                 # Hono backend
    └── src/
        ├── routers/
        ├── services/
        └── db/
packages/
├── shared/                 # Shared types
└── game-logic/             # Pure game logic
```

## TypeScript Patterns

```typescript
// Branded types (prevent ID mixing)
type UserId = string & { __brand: 'UserId' };
type SeasonId = string & { __brand: 'SeasonId' };

// Discriminated unions
type GamePhase = 
  | { phase: 'morning'; forecast: Weather }
  | { phase: 'action'; betsPlaced: number }
  | { phase: 'resolution'; results: BetResult[] };

// Exhaustive checking
function assertNever(x: never): never {
  throw new Error(`Unexpected: ${x}`);
}

// Zod + TypeScript integration
const BetSchema = z.object({
  potId: z.enum(['water', 'sun', 'pest', 'growth']),
  betType: z.enum(['fold', 'call', 'raise', 'all-in']),
  amount: z.number().int().min(0),
});
type Bet = z.infer<typeof BetSchema>;
```

## Refactoring Patterns

```typescript
// ❌ Long function
function processDayEnd(state: GameState) {
  // 100 lines of mixed concerns
}

// ✅ Composed functions
function processDayEnd(state: GameState) {
  const potResults = calculatePotResults(state);
  const resources = calculateResourceUpdates(state, potResults);
  const achievements = checkAchievements(state, potResults);
  return { ...state, ...resources, achievements };
}
```

## Code Review Checklist

- [ ] Functions < 30 lines
- [ ] No `any` types without justification
- [ ] No magic numbers
- [ ] Single responsibility
- [ ] Edge cases handled
- [ ] Tests for logic
- [ ] Keyboard accessible
- [ ] No memory leaks

## Error Handling

```typescript
type Result<T, E = Error> = 
  | { success: true; data: T }
  | { success: false; error: E };

async function tryAsync<T>(promise: Promise<T>): Promise<Result<T>> {
  try {
    return { success: true, data: await promise };
  } catch (error) {
    return { success: false, error: error as Error };
  }
}
```

---

*Architecture & Quality Reference - Game Engineering Team*
