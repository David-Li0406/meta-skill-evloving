---
name: multi-currency
description: Exchange rate management, currency conversion, and Frankfurter API integration. Use when working with USD/EUR/ILS conversions, exchange rates, or multi-currency dashboard displays.
---

# Multi-Currency Domain Knowledge

## Supported Currencies

```typescript
enum Currency {
  USD  // US Dollar
  EUR  // Euro
  ILS  // Israeli Shekel
}
```

## Exchange Rate Storage

```prisma
model ExchangeRate {
  id             String   @id @default(cuid())
  baseCurrency   Currency
  targetCurrency Currency
  rate           Decimal  @db.Decimal(12, 6)  // 6 decimal precision
  date           DateTime
  fetchedAt      DateTime @default(now())

  @@unique([baseCurrency, targetCurrency, date])
}
```

## Frankfurter API Integration

Location: `src/lib/currency.ts`

**Base URL:** `https://api.frankfurter.dev/v1`

### fetchExchangeRates

```typescript
export async function fetchExchangeRates(baseCurrency: Currency): Promise<FrankfurterResponse>
```

Features:

- Request deduplication via `inFlightRequests` Map
- Concurrent requests for same base currency return same Promise
- Automatic cleanup after request completes

### getExchangeRate

```typescript
export async function getExchangeRate(from: Currency, to: Currency, date?: Date): Promise<number>
```

Strategy:

1. Same currency returns 1 (no conversion needed)
2. Check cache (ExchangeRate table) for today's rate
3. Fetch from API if not cached
4. Upsert to cache
5. Fallback to most recent cached rate if API fails

### convertAmount

```typescript
export async function convertAmount(amount: number, from: Currency, to: Currency, date?: Date): Promise<number>
```

- Returns amount unchanged if same currency
- Rounds to 2 decimal places: `Math.round(converted * 100) / 100`

## Batch Loading Pattern (N+1 Prevention)

For dashboard aggregations, use batch loading:

### batchLoadExchangeRates

```typescript
export async function batchLoadExchangeRates(date?: Date): Promise<RateCache>
// Returns Map<string, number> for O(1) lookups
```

### convertAmountWithCache

```typescript
export function convertAmountWithCache(amount: number, from: Currency, to: Currency, cache: RateCache): number
```

- **No database calls** (uses preloaded cache)
- Logs warning if rate missing, returns original amount
- Use in loops/aggregations to avoid N+1 queries

## Cache Key Format

```typescript
function rateCacheKey(from: Currency, to: Currency): string {
  return `${from}:${to}` // e.g., "USD:EUR"
}
```

## Refresh Workflow

```typescript
export async function refreshExchangeRates(): Promise<
  { success: true; updatedAt: Date } | { error: { general: string[] }; updatedAt: Date }
>
```

- Fetches rates for ALL base currencies
- Upserts all currency pairs for today
- Called via `refreshExchangeRatesAction` from dashboard UI

## User Preference

```prisma
model User {
  preferredCurrency Currency @default(USD)
}
```

Dashboard displays amounts in user's preferred currency via conversion.

## Key Files

- `src/lib/currency.ts` - All currency functions
- `src/app/actions/misc.ts` - refreshExchangeRatesAction
- `src/lib/dashboard-ux.ts` - Uses batchLoadExchangeRates for aggregation
