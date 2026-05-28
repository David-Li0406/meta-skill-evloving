---
name: multi-currency
description: Use this skill when managing exchange rates, performing currency conversions, or integrating with the Frankfurter API for USD/EUR/ILS transactions.
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
- Concurrent requests for the same base currency return the same Promise
- Automatic cleanup after request completes

### getExchangeRate

```typescript
export async function getExchangeRate(from: Currency, to: Currency, date?: Date): Promise<number>
```

Strategy:
1. Return 1 if the same currency is provided (no conversion needed).
2. Check the cache (ExchangeRate table) for today's rate.
3. Fetch from the API if not cached.
4. Upsert to cache.
5. Fallback to the most recent cached rate if the API fails.

### convertAmount

```typescript
export async function convertAmount(
  amount: number,
  from: Currency,
  to: Currency,
  date?: Date
): Promise<number>
```

- Returns the amount unchanged if the same currency is provided.
- Rounds to 2 decimal places: `Math.round(converted * 100) / 100`.

## Batch Loading Pattern (N+1 Prevention)

For dashboard aggregations, use batch loading:

### batchLoadExchangeRates

```typescript
export async function batchLoadExchangeRates(date?: Date): Promise<RateCache>
// Returns Map<string, number> for O(1) lookups
```

### convertAmountWithCache

```typescript
export function convertAmountWithCache(
  amount: number,
  from: Currency,
  to: Currency,
  cache: RateCache
): number
```

- **No database calls** (uses preloaded cache).
- Logs a warning if the rate is missing and returns the original amount.
- Use in loops/aggregations to avoid N+1 queries.

## Cache Key Format

```typescript
function rateCacheKey(from: Currency, to: Currency): string {
  return `${from}:${to}` // e.g., "USD:EUR"
}
```