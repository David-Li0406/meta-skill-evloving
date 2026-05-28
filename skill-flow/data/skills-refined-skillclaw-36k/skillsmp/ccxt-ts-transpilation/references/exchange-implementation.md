# Exchange Implementation

## Repository Structure

```
ccxt/
├── ts/src/              # TypeScript source (EDIT HERE)
│   ├── base/
│   ├── abstract/        # API endpoint definitions
│   └── [exchange].ts    # Exchange implementations
├── python/              # Auto-generated (DON'T EDIT)
│   ├── ccxt/
│   └── ccxt/async_support/
├── php/                 # Auto-generated (DON'T EDIT except base)
├── go/                  # Auto-generated (DON'T EDIT except base)
├── cs/                  # Auto-generated (DON'T EDIT except base)
├── build/               # Build scripts
├── examples/            # Example code
└── tests/               # Test files
```

## Unified Code Philosophy

**Most Important**: All exchanges must follow UNIFIED patterns. When implementing:

1. Copy from existing certified exchanges
2. Don't invent new patterns
3. Make code pedantically consistent
4. Follow Manual specifications exactly
5. Submit atomic PRs (one exchange per PR)

## Adding a New Exchange

### 1. Create Exchange Files

```bash
cd ccxt/ts/src

# Create main exchange file
cp binance.ts mynewexchange.ts

# Create abstract file
cp abstract/binance.ts abstract/mynewexchange.ts
```

### 2. Update Exchange Class

```typescript
// ts/src/mynewexchange.ts
import Exchange from './base/Exchange.js';
import { ExchangeError, AuthenticationError } from './base/errors.js';
import type { Int, OrderSide, OrderType, Order, Ticker } from './base/types.js';

export default class mynewexchange extends Exchange {
    describe () {
        return this.deepExtend (super.describe (), {
            'id': 'mynewexchange',
            'name': 'MyNewExchange',
            'countries': [ 'US' ],
            'version': '1',
            'rateLimit': 1000,
            'has': {
                'fetchTicker': true,
                'fetchTickers': true,
                'fetchOrderBook': true,
                'fetchTrades': true,
                'fetchOHLCV': true,
                'createOrder': true,
                'cancelOrder': true,
                'fetchBalance': true,
            },
            'urls': {
                'logo': 'https://example.com/logo.png',
                'api': {
                    'public': 'https://api.example.com',
                    'private': 'https://api.example.com',
                },
                'www': 'https://www.example.com',
                'doc': 'https://docs.example.com',
            },
            'api': {
                'public': {
                    'get': [
                        'ticker',
                        'orderbook',
                        'trades',
                    ],
                },
                'private': {
                    'get': [
                        'balance',
                        'orders',
                    ],
                    'post': [
                        'order',
                    ],
                    'delete': [
                        'order/{id}',
                    ],
                },
            },
        });
    }
}
```

### 3. Update Abstract File

Define API structure:

```typescript
// ts/src/abstract/mynewexchange.ts
import { implicitReturnType } from '../base/types.js';

export interface ImplicitAPI {
    public: {
        get: {
            'ticker': implicitReturnType;
            'orderbook': implicitReturnType;
            'trades': implicitReturnType;
        };
    };
    private: {
        get: {
            'balance': implicitReturnType;
            'orders': implicitReturnType;
        };
        post: {
            'order': implicitReturnType;
        };
        delete: {
            'order/{id}': implicitReturnType;
        };
    };
}
```

## Implementing Core Methods

### fetchTicker

```typescript
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    await this.loadMarkets ();
    const market = this.market (symbol);
    const request = {
        'symbol': market['id'],
    };
    const response = await this.publicGetTicker (this.extend (request, params));
    return this.parseTicker (response, market);
}

parseTicker (ticker: object, market: object = undefined): Ticker {
    const timestamp = this.safeInteger (ticker, 'timestamp');
    const marketId = this.safeString (ticker, 'symbol');
    const symbol = this.safeSymbol (marketId, market);
    const last = this.safeFloat (ticker, 'last');
    const bid = this.safeFloat (ticker, 'bid');
    const ask = this.safeFloat (ticker, 'ask');
    const high = this.safeFloat (ticker, 'high');
    const low = this.safeFloat (ticker, 'low');
    const volume = this.safeFloat (ticker, 'volume');
    
    return this.safeTicker ({
        'symbol': symbol,
        'timestamp': timestamp,
        'datetime': this.iso8601 (timestamp),
        'high': high,
        'low': low,
        'bid': bid,
        'ask': ask,
        'last': last,
        'volume': volume,
        'info': ticker,
    }, market);
}
```

### createOrder

```typescript
async createOrder (symbol: string, type: OrderType, side: OrderSide, amount: number, price: number = undefined, params = {}): Promise<Order> {
    await this.loadMarkets ();
    const market = this.market (symbol);
    const request = {
        'symbol': market['id'],
        'side': side.toUpperCase (),
        'type': type.toUpperCase (),
        'quantity': this.amountToPrecision (symbol, amount),
    };
    
    if (type === 'limit') {
        request['price'] = this.priceToPrecision (symbol, price);
    }
    
    const response = await this.privatePostOrder (this.extend (request, params));
    return this.parseOrder (response, market);
}

parseOrder (order: object, market: object = undefined): Order {
    const id = this.safeString (order, 'orderId');
    const timestamp = this.safeInteger (order, 'timestamp');
    const marketId = this.safeString (order, 'symbol');
    const symbol = this.safeSymbol (marketId, market);
    const type = this.safeStringLower (order, 'type');
    const side = this.safeStringLower (order, 'side');
    const price = this.safeFloat (order, 'price');
    const amount = this.safeFloat (order, 'quantity');
    const filled = this.safeFloat (order, 'filledQuantity');
    const status = this.parseOrderStatus (this.safeString (order, 'status'));
    
    return this.safeOrder ({
        'id': id,
        'clientOrderId': undefined,
        'timestamp': timestamp,
        'datetime': this.iso8601 (timestamp),
        'symbol': symbol,
        'type': type,
        'side': side,
        'price': price,
        'amount': amount,
        'filled': filled,
        'remaining': undefined,
        'status': status,
        'info': order,
    }, market);
}
```

## Error Handling

### handleErrors Method

**Critical**: Centralize all error handling in `handleErrors`:

```typescript
handleErrors (code: int, reason: string, url: string, method: string, headers: object, body: string, response: object, requestHeaders: object, requestBody: object): void {
    if (response === undefined) {
        return;
    }
    
    // Extract error information from response
    const error = this.safeString (response, 'error');
    const errorCode = this.safeString (response, 'code');
    const message = this.safeString (response, 'msg');
    
    if (error !== undefined || errorCode !== undefined || message !== undefined) {
        const feedback = this.id + ' ' + body;
        
        // Try exact matches first
        this.throwExactlyMatchedException (this.exceptions['exact'], error, feedback);
        this.throwExactlyMatchedException (this.exceptions['exact'], errorCode, feedback);
        this.throwExactlyMatchedException (this.exceptions['exact'], message, feedback);
        
        // Then broad matches
        this.throwBroadlyMatchedException (this.exceptions['broad'], error, feedback);
        this.throwBroadlyMatchedException (this.exceptions['broad'], message, feedback);
        
        // Default error
        throw new ExchangeError (feedback);
    }
}
```

### Exception Mappings

Define exchange-specific error mappings:

```typescript
describe () {
    return this.deepExtend (super.describe (), {
        // ... other properties
        'exceptions': {
            'exact': {
                'INVALID_API_KEY': AuthenticationError,
                'INVALID_SIGNATURE': AuthenticationError,
                'INSUFFICIENT_BALANCE': InsufficientFunds,
                'INVALID_SYMBOL': BadSymbol,
                'ORDER_NOT_FOUND': OrderNotFound,
                'RATE_LIMIT_EXCEEDED': RateLimitExceeded,
            },
            'broad': {
                'Invalid symbol': BadSymbol,
                'Invalid order': InvalidOrder,
                'Insufficient': InsufficientFunds,
                'Rate limit': RateLimitExceeded,
            },
        },
    });
}
```

## Market IDs vs Unified Symbols

**Critical**: Never send unified symbols directly to exchanges!

### Sending Market IDs to Exchanges

**Exchange-specific market-ids ≠ Unified CCXT symbols**

References:
- https://github.com/ccxt/ccxt/wiki/Manual#markets
- https://github.com/ccxt/ccxt/wiki/Manual#symbols-and-market-ids

```typescript
// ❌ NEVER DO THIS
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    const request = {
        'pair': symbol,  // WRONG! Sending unified symbol directly
    };
    const response = await this.publicGetEndpoint (request);
    // ...
}

// ❌ DON'T DO THIS EITHER
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    const request = {
        'symbol': symbol,  // WRONG! Sending unified symbol directly
    };
    const response = await this.publicGetEndpoint (request);
    // ...
}

// ✅ CORRECT - Use market() to get exchange-specific ID
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    const market = this.market (symbol);  // Get full market structure
    const request = {
        'pair': market['id'],  // Good! Using exchange-specific ID
    };
    const response = await this.publicGetEndpoint (this.extend (request, params));
    return this.parseTicker (response, market);
}

// ✅ ALSO CORRECT - Use marketId() if you only need the ID
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    const marketId = this.marketId (symbol);  // Just the ID
    const request = {
        'symbol': marketId,  // Good! Using exchange-specific ID
    };
    const response = await this.publicGetEndpoint (this.extend (request, params));
    return this.parseTicker (response);
}
```

### Parsing Symbols from Exchange Responses

**Never return exchange-specific market-ids in unified structures!**

```typescript
// ❌ NEVER DO THIS
parseTrade (trade: object, market: object = undefined): Trade {
    return {
        'info': trade,
        'symbol': trade['pair'],  // WRONG! Exchange-specific ID in result
        // ...
    };
}

// ❌ DON'T DO THIS EITHER
parseTrade (trade: object, market: object = undefined): Trade {
    return {
        'info': trade,
        'symbol': trade['symbol'],  // WRONG! Exchange-specific ID in result
        // ...
    };
}

// ✅ CORRECT - Use safeSymbol to convert market ID to unified symbol
parseTrade (trade: object, market: object = undefined): Trade {
    const marketId = this.safeString (trade, 'pair');
    const symbol = this.safeSymbol (marketId, market);  // Convert to unified
    return {
        'info': trade,
        'symbol': symbol,  // Good! Unified symbol
        // ...
    };
}
```

## Safe Methods for Dictionary Access

**Never access dictionary keys directly!** Use safe methods.

### Why Safe Methods Are Required

JavaScript tolerates non-existent keys, but Python/PHP throw exceptions:

```javascript
// JavaScript - works (returns undefined)
const obj = {};
if (obj['nonExistent']) {}  // No error

// Python - BREAKS
some_dict = {}
if some_dict['nonExistent']:  # KeyError exception!

// PHP - BREAKS
$array = array();
if ($array['nonExistent']) {}  // Warning/Notice
```

### Available Safe Methods

```typescript
// For integers (timestamps in milliseconds)
const timestamp = this.safeInteger (obj, 'timestamp');
const time = this.safeInteger2 (obj, 'time', 'timestamp');  // Try multiple keys

// For numbers (amounts, prices, costs)
const amount = this.safeNumber (obj, 'amount');
const price = this.safeNumber2 (obj, 'price', 'last');

// For strings (ids, types, statuses)
const id = this.safeString (obj, 'id');
const status = this.safeString2 (obj, 'status', 'state');

// For strings with case conversion
const side = this.safeStringLower (obj, 'side');
const type = this.safeStringUpper (obj, 'type');

// For booleans
const active = this.safeBool (obj, 'active');

// For lists/arrays
const trades = this.safeList (obj, 'trades', []);

// For dictionaries/objects
const market = this.safeDict (obj, 'market', {});

// For generic values (objects, arrays, booleans)
const data = this.safeValue (obj, 'data');
const info = this.safeValue2 (obj, 'info', 'data');

// For UNIX timestamps in seconds (auto-converts to milliseconds)
const timestamp = this.safeTimestamp (obj, 'timestamp');
const time = this.safeTimestamp2 (obj, 'time', 'timestamp');
```

### Safe Method N (Multiple Keys)

Search multiple keys in order:

```typescript
const price = this.safeStringN (object, [
    'lastPrice',
    'last',
    'price',
    'close'
], defaultValue);

// Equivalent to:
// this.safeString (object, 'lastPrice',
//     this.safeString (object, 'last',
//         this.safeString (object, 'price',
//             this.safeString (object, 'close', defaultValue))))
```

### Safe Method Usage Examples

```typescript
// ❌ NEVER DO THIS
const price = response['price'] || 0;
if (response['available']) {}
const id = data['id'];

// ✅ ALWAYS DO THIS
const price = this.safeNumber (response, 'price', 0);
const available = this.safeBool (response, 'available');
const id = this.safeString (data, 'id');

// ✅ Check for undefined before using
const foo = this.safeValue (params, 'foo');
if (foo !== undefined) {
    // Use foo
}

// ✅ Alternative with key existence check
if ('foo' in params) {
    const foo = params['foo'];
    // Use foo
}
```

## Timestamps

**All timestamps in CCXT are UTC timestamps in milliseconds!**

### Converting Timestamps

```typescript
const data = {
    'unixTimestampInSeconds': 1565242530,
    'unixTimestampInMilliseconds': 1565242530165,
    'unixTimestampAsDecimal': 1565242530.165,
    'stringInSeconds': '1565242530',
};

// Already in milliseconds - use safeInteger
const ts1 = this.safeInteger (data, 'unixTimestampInMilliseconds');
// Result: 1565242530165

// In seconds with decimal - use safeTimestamp (multiplies by 1000)
const ts2 = this.safeTimestamp (data, 'unixTimestampAsDecimal');
// Result: 1565242530165

// In seconds as integer - use safeTimestamp (multiplies by 1000)
const ts3 = this.safeTimestamp (data, 'unixTimestampInSeconds');
// Result: 1565242530000

// In seconds as string - use safeTimestamp (converts and multiplies)
const ts4 = this.safeTimestamp (data, 'stringInSeconds');
// Result: 1565242530000
```

### Converting to ISO8601

```typescript
const timestamp = this.safeTimestamp (order, 'created');
const datetime = this.iso8601 (timestamp);

// In unified structures
return {
    'timestamp': timestamp,
    'datetime': this.iso8601 (timestamp),
    // ...
};
```

## Working with Precision and Decimal Numbers

**Use `Precise` class for all string-based math operations.**

### String-Based Number Handling

CCXT is moving toward string-based representations to avoid float precision issues.

```typescript
// Old approach (being phased out)
const amount = this.safeFloat (order, 'amount');
const remaining = this.safeFloat (order, 'remaining');
if (remaining > 0) {
    status = 'open';
}

// New approach (use this!)
const amount = this.safeNumber (order, 'amount');  // Internal string layer
const remaining = this.safeString (order, 'remaining');  // Internal string layer
if (Precise.stringGt (remaining, '0')) {  // String comparison
    status = 'open';
}

return {
    'amount': amount,  // External layer, to user
    'remaining': this.parseNumber (remaining),  // Convert for user
    'status': status,
};
```

### Precise Class Methods

```typescript
// String comparisons
Precise.stringEq (a, b)   // a === b
Precise.stringGt (a, b)   // a > b
Precise.stringGe (a, b)   // a >= b
Precise.stringLt (a, b)   // a < b
Precise.stringLe (a, b)   // a <= b

// String arithmetic
Precise.stringAdd (a, b)  // a + b
Precise.stringSub (a, b)  // a - b
Precise.stringMul (a, b)  // a * b
Precise.stringDiv (a, b)  // a / b
Precise.stringMod (a, b)  // a % b
Precise.stringAbs (a)     // abs(a)
Precise.stringNeg (a)     // -a
```

### Formatting Decimals

**Never use `.toFixed()`** (has rounding bugs):

```typescript
// ❌ WRONG
const formatted = price.toFixed (2);

// ✅ CORRECT - Use decimalToPrecision
const formatted = this.decimalToPrecision (price, ROUND, 2, DECIMAL_PLACES);

// ✅ Use precision helpers
const amount = this.amountToPrecision (symbol, amountValue);
const price = this.priceToPrecision (symbol, priceValue);
const cost = this.costToPrecision (symbol, costValue);
```

## Base Class Cryptography Methods

**Use base class methods for all cryptography.** Never import external crypto libraries.

### Available Cryptography Methods

```typescript
// Hashing
this.hash (message, 'md5', 'hex')
this.hash (message, 'sha256', 'hex')
this.hash (message, 'sha512', 'hex')
this.hash (message, 'keccak', 'hex')

// HMAC
this.hmac (message, secret, 'sha256', 'hex')
this.hmac (message, secret, 'sha512', 'base64')

// JWT
this.jwt (payload, secret, 'HS256')

// RSA
this.rsa (message, secret, 'RS256')

// ECDSA
this.ecdsa (request, secret, 'p256')
this.ecdsa (request, secret, 'secp256k1')

// OTP 2FA
this.totp (secret)

// Encoding
this.stringToBase64 (string)
this.base64ToBinary (string)
this.binaryToBase64 (binary)
this.encode (string)
this.decode (string)
```

### Hash Algorithms

- `'md5'`
- `'sha1'`
- `'sha256'`
- `'sha384'`
- `'sha512'`
- `'keccak'`
- `'sha3'`

### Digest Encodings

- `'hex'`
- `'binary'`
- `'base64'` (HMAC only)

### Example Authentication

```typescript
sign (path: string, api: string = 'public', method: string = 'GET', params = {}, headers: object = undefined, body: object = undefined): object {
    let url = this.urls['api'][api] + '/' + path;
    
    if (api === 'private') {
        this.checkRequiredCredentials ();
        const timestamp = this.milliseconds ().toString ();
        const auth = timestamp + method + '/' + path;
        
        let query = undefined;
        if (method === 'GET') {
            if (Object.keys (params).length) {
                query = this.urlencode (params);
                url += '?' + query;
            }
        } else {
            body = this.json (params);
        }
        
        const signature = this.hmac (this.encode (auth + (body || '')), this.encode (this.secret), 'sha256', 'hex');
        
        headers = {
            'API-KEY': this.apiKey,
            'API-SIGNATURE': signature,
            'API-TIMESTAMP': timestamp,
        };
    }
    
    return { 'url': url, 'method': method, 'body': body, 'headers': headers };
}
```

## String Operations

### String Concatenation

**The `+` operator is for string concatenation ONLY.**

```typescript
// ✅ CORRECT - String concatenation
const message = 'Hello' + ' ' + 'World';
const path = '/api/' + version + '/ticker';

// ❌ WRONG - Arithmetic with +
const total = amount + fee;  // Use Precise instead!

// ✅ CORRECT - Use Precise for arithmetic
const total = Precise.stringAdd (amount, fee);
```

### Escaped Control Characters

**Use double quotes for escape sequences:**

```typescript
// ✅ CORRECT - Double quotes for control characters
const message = "Line1\nLine2\tTabbed";  // eslint-disable-line quotes
const payload = "GET\n" + path + "\n" + timestamp;  // eslint-disable-line quotes

// ❌ WRONG - Single quotes (won't work in PHP)
const message = 'Line1\nLine2\tTabbed';
```

**↑ The `eslint-disable-line quotes` comment is mandatory!**

### Array Lengths

Hint the transpiler for array lengths:

```typescript
// ✅ CORRECT - Array length with .length; ending
const arrayLength = someArray.length;
// Now use arrayLength for arithmetic

// ✅ CORRECT - In for loops (automatic)
for (let i = 0; i < array.length; i++) {
    // .length here is treated as array length
}

// String length works normally
const strLength = someString.length;
```

## Precision Handling

**Never hardcode precision values.** Always derive from market info.

```typescript
// ❌ WRONG
const amount = amount * 100000000;  // Hardcoded multiplier

// ✅ CORRECT - Use amountToPrecision
const preciseAmount = this.amountToPrecision (symbol, amount);

// ✅ CORRECT - Use priceToPrecision
const precisePrice = this.priceToPrecision (symbol, price);
```

### Setting Market Precision

```typescript
parseTradingFees (response: object): object {
    const fees = {};
    const data = this.safeValue (response, 'symbols', []);
    
    for (let i = 0; i < data.length; i++) {
        const market = data[i];
        const id = this.safeString (market, 'symbol');
        const symbol = this.safeSymbol (id);
        
        fees[symbol] = {
            'maker': this.safeFloat (market, 'makerFee'),
            'taker': this.safeFloat (market, 'takerFee'),
            'precision': {
                'amount': this.safeInteger (market, 'baseAssetPrecision'),
                'price': this.safeInteger (market, 'quotePrecision'),
            },
        };
    }
    
    return fees;
}
```

## Market IDs vs Unified Symbols

**Critical**: Never send unified symbols directly to exchanges!

### Sending Market IDs to Exchanges

**Exchange-specific market-ids ≠ Unified CCXT symbols**

References:
- https://github.com/ccxt/ccxt/wiki/Manual#markets
- https://github.com/ccxt/ccxt/wiki/Manual#symbols-and-market-ids

```typescript
// ❌ NEVER DO THIS
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    const request = {
        'pair': symbol,  // WRONG! Sending unified symbol directly
    };
    const response = await this.publicGetEndpoint (request);
    // ...
}

// ❌ DON'T DO THIS EITHER
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    const request = {
        'symbol': symbol,  // WRONG! Sending unified symbol directly
    };
    const response = await this.publicGetEndpoint (request);
    // ...
}

// ✅ CORRECT - Use market() to get exchange-specific ID
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    const market = this.market (symbol);  // Get full market structure
    const request = {
        'pair': market['id'],  // Good! Using exchange-specific ID
    };
    const response = await this.publicGetEndpoint (this.extend (request, params));
    return this.parseTicker (response, market);
}

// ✅ ALSO CORRECT - Use marketId() if you only need the ID
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    const marketId = this.marketId (symbol);  // Just the ID
    const request = {
        'symbol': marketId,  // Good! Using exchange-specific ID
    };
    const response = await this.publicGetEndpoint (this.extend (request, params));
    return this.parseTicker (response);
}
```

### Parsing Symbols from Exchange Responses

**Never return exchange-specific market-ids in unified structures!**

```typescript
// ❌ NEVER DO THIS
parseTrade (trade: object, market: object = undefined): Trade {
    return {
        'info': trade,
        'symbol': trade['pair'],  // WRONG! Exchange-specific ID in result
        // ...
    };
}

// ❌ DON'T DO THIS EITHER
parseTrade (trade: object, market: object = undefined): Trade {
    return {
        'info': trade,
        'symbol': trade['symbol'],  // WRONG! Exchange-specific ID in result
        // ...
    };
}

// ✅ CORRECT - Use safeSymbol to convert market ID to unified symbol
parseTrade (trade: object, market: object = undefined): Trade {
    const marketId = this.safeString (trade, 'pair');
    const symbol = this.safeSymbol (marketId, market);  // Convert to unified
    return {
        'info': trade,
        'symbol': symbol,  // Good! Unified symbol
        // ...
    };
}
```

## Safe Methods for Dictionary Access

**Never access dictionary keys directly!** Use safe methods.

### Why Safe Methods Are Required

JavaScript tolerates non-existent keys, but Python/PHP throw exceptions. See [Transpilation Rules](transpilation-rules.md) for details.

### Available Safe Methods

```typescript
// For integers (timestamps in milliseconds)
const timestamp = this.safeInteger (obj, 'timestamp');
const time = this.safeInteger2 (obj, 'time', 'timestamp');  // Try multiple keys

// For numbers (amounts, prices, costs)
const amount = this.safeNumber (obj, 'amount');
const price = this.safeNumber2 (obj, 'price', 'last');

// For strings (ids, types, statuses)
const id = this.safeString (obj, 'id');
const status = this.safeString2 (obj, 'status', 'state');

// For strings with case conversion
const side = this.safeStringLower (obj, 'side');
const type = this.safeStringUpper (obj, 'type');

// For booleans
const active = this.safeBool (obj, 'active');

// For lists/arrays
const trades = this.safeList (obj, 'trades', []);

// For dictionaries/objects
const market = this.safeDict (obj, 'market', {});

// For UNIX timestamps in seconds (auto-converts to milliseconds)
const timestamp = this.safeTimestamp (obj, 'timestamp');

// Safe Method N (search multiple keys)
const price = this.safeStringN (object, ['lastPrice', 'last', 'price'], defaultValue);
```

## Timestamps and Precision

See [Transpilation Rules - Additional Rules](transpilation-rules.md#additional-transpilation-rules) for:
- Timestamp conversions (milliseconds/seconds)
- String-based precision handling with `Precise` class
- Formatting decimals with `decimalToPrecision`
- Base class cryptography methods

## Authentication

### Sign Requests

```typescript
sign (path: string, api: string = 'public', method: string = 'GET', params = {}, headers: object = undefined, body: object = undefined): object {
    let url = this.urls['api'][api] + '/' + path;
    
    if (api === 'public') {
        if (Object.keys (params).length) {
            url += '?' + this.urlencode (params);
        }
    } else {
        this.checkRequiredCredentials ();
        const timestamp = this.milliseconds ().toString ();
        const auth = timestamp + method + '/' + path;
        
        let query = undefined;
        if (method === 'GET' || method === 'DELETE') {
            if (Object.keys (params).length) {
                query = this.urlencode (params);
                url += '?' + query;
                auth += '?' + query;
            }
        } else {
            body = this.json (params);
            auth += body;
        }
        
        const signature = this.hmac (this.encode (auth), this.encode (this.secret), 'sha256', 'hex');
        
        headers = {
            'API-KEY': this.apiKey,
            'API-SIGNATURE': signature,
            'API-TIMESTAMP': timestamp,
            'Content-Type': 'application/json',
        };
    }
    
    return { 'url': url, 'method': method, 'body': body, 'headers': headers };
}
```
