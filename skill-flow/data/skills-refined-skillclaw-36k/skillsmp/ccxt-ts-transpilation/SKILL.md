---
name: ccxt-ts-transpilation
description: Editing CCXT TypeScript exchange sources with transpilation-safe patterns for Python/Go/PHP/C#
version: 1.0.0
license: MIT
---

# CCXT TypeScript Development

## Overview

CCXT is a cryptocurrency trading library supporting 100+ exchanges. Written in TypeScript, it transpiles to Python, Go, PHP, and C#. When editing exchange implementations in `ccxt/ts/src/`, you must follow strict patterns to ensure successful transpilation across all target languages.

**Most Important Rule**: Code must be UNIFIED across all exchanges. Copy patterns from existing certified exchanges, don't invent new patterns.

## References

- **[Transpilation Rules](references/transpilation-rules.md)**: Hard constraints for multi-language compatibility (ternaries, types, null checks)
- **[Exchange Implementation](references/exchange-implementation.md)**: Adding exchanges, endpoints, error handling, precision
- **[Build & Test](references/build-test.md)**: Transpilation commands, testing patterns, CI workflow

## Key Concepts

### Transpilation System
TypeScript in `ts/src/` → Transpiled to `python/`, `php/`, `go/`, `cs/`

### Exchange Base Class
All exchanges extend `Exchange` from `ts/src/base/Exchange.ts`

### Abstract Files
API endpoint declarations in `ts/src/abstract/{exchange}.ts`

### Safe Coding Patterns
- Explicit if/else (no ternaries)
- No type annotations on locals
- Only undefined checks (never null)
- Space before helper call parentheses

## Common Tasks

### Add New Exchange Endpoint
```typescript
// 1. Add to abstract file: ts/src/abstract/binance.ts
export interface ImplicitAPI {
    public: {
        get: {
            'api/v3/exchangeInfo': object;
            'api/v3/ticker/24hr': object;
        };
    };
}

// 2. Implement in main file: ts/src/binance.ts
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    await this.loadMarkets ();
    const market = this.market (symbol);
    const request = {
        'symbol': market['id'],
    };
    const response = await this.publicGetApiV3Ticker24hr (this.extend (request, params));
    return this.parseTicker (response, market);
}
```

### Handle Exchange Errors
```typescript
handleErrors (code: int, reason: string, url: string, method: string, headers: object, body: string, response: object, requestHeaders: object, requestBody: object): void {
    if (response === undefined) {
        return;
    }
    // Extract error from response body
    const error = this.safeString (response, 'error');
    const message = this.safeString (response, 'msg');
    
    if (error !== undefined || message !== undefined) {
        const feedback = this.id + ' ' + body;
        this.throwExactlyMatchedException (this.exceptions['exact'], error, feedback);
        this.throwExactlyMatchedException (this.exceptions['exact'], message, feedback);
        this.throwBroadlyMatchedException (this.exceptions['broad'], error, feedback);
        this.throwBroadlyMatchedException (this.exceptions['broad'], message, feedback);
        throw new ExchangeError (feedback);
    }
}
```

### Avoid Ternaries (Use Explicit If/Else)
```typescript
// ❌ WRONG - Ternary not allowed
const fee = isMaker ? 0.001 : 0.002;

// ✅ CORRECT - Explicit if/else with let
let fee = undefined;
if (isMaker) {
    fee = 0.001;
} else {
    fee = 0.002;
}
```

## Integration Points

- **OctoBot-Tentacles**: Exchange tentacles use CCXT via `CCXTConnector`
- **CCXT API**: Public/private methods auto-generated from abstract files
- **Build System**: Node.js transpilation to 4 target languages
- **Testing**: Run exchange-specific tests across all languages

## Quick Reference

### Build Commands
```bash
# Build single exchange for Python
npm run emitAPI binance && npm run transpileRest binance

# Build all exchanges
npm run build

# Transpile WebSocket for exchange
npm run transpileWs binance
```

### Safe Patterns
```typescript
// Space before helper parentheses
const id = this.safeString (market, 'id');
const price = this.safeFloat (ticker, 'price');

// No type annotations on locals
let result = undefined;  // ✅
let result: any;         // ❌

// Check undefined, not null
if (value !== undefined) {}  // ✅
if (value !== null) {}       // ❌
```

### Exception Mapping
```typescript
this.exceptions = {
    'exact': {
        'INVALID_API_KEY': AuthenticationError,
        'INSUFFICIENT_BALANCE': InsufficientFunds,
    },
    'broad': {
        'Invalid symbol': BadSymbol,
        'Rate limit': RateLimitExceeded,
    },
};
```

## Checklist

- [ ] Run `git config core.hooksPath .git-templates/hooks` (first time setup)
- [ ] No ternaries anywhere (use explicit if/else with let)
- [ ] No type annotations on local variables
- [ ] No null checks (only undefined checks)
- [ ] Space before parentheses in helper calls
- [ ] Error handling in handleErrors with exception mappings
- [ ] Abstract file updated for new endpoints
- [ ] Precision derived from markets, not hardcoded
- [ ] Use safe* methods for all dictionary access
- [ ] Send market IDs (not symbols) to exchange APIs
- [ ] Parse market IDs back to symbols in responses
- [ ] Run `npm run build` before committing
- [ ] Submit atomic PRs (one exchange per PR)
- [ ] Never commit transpiled outputs (python/, php/, go/, cs/)
- [ ] Test changes across all target languages
