# Transpilation Rules

## Hard Constraints

These rules are **absolute requirements** for successful transpilation to Python/Go/PHP/C#.

### No Ternary Operators

**Never use ternaries.** The transpiler cannot convert them reliably.

```typescript
// ❌ FORBIDDEN
const fee = isMaker ? 0.001 : 0.002;
const side = type === 'buy' ? 'BUY' : 'SELL';

// ✅ REQUIRED PATTERN
let fee = undefined;
if (isMaker) {
    fee = 0.001;
} else {
    fee = 0.002;
}

let side = undefined;
if (type === 'buy') {
    side = 'BUY';
} else {
    side = 'SELL';
}
```

### No Type Annotations on Local Variables

**Never add types to local variables.** Transpiler cannot handle them.

```typescript
// ❌ FORBIDDEN
let price: number = 0;
const symbol: string = 'BTC/USDT';
let result: any;

// ✅ REQUIRED PATTERN
let price = 0;
const symbol = 'BTC/USDT';
let result = undefined;
```

**Exception**: Function signatures and class properties CAN have types:
```typescript
// ✅ OK for function parameters/returns
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    // ...
}

// ✅ OK for class properties
fee: object;
precision: object;
```

### No Uninitialized Let

**Always initialize let variables.** Uninitialized lets break transpilation.

```typescript
// ❌ FORBIDDEN
let price;
let result;

// ✅ REQUIRED PATTERN
let price = undefined;
let result = undefined;
```

### Only Undefined Checks (Never Null)

**Never check for null.** Only check undefined.

```typescript
// ❌ FORBIDDEN
if (value !== null) {}
if (value === null) {}

// ✅ REQUIRED PATTERN
if (value !== undefined) {}
if (value === undefined) {}
```

**Why**: Different languages handle null differently. CCXT uses `undefined` consistently.

### Space Before Helper Call Parentheses

**Always add space before parentheses in this.safe* calls.**

```typescript
// ❌ WRONG
const id = this.safeString(obj, 'id');
const price = this.safeFloat(ticker, 'price');

// ✅ CORRECT
const id = this.safeString (obj, 'id');
const price = this.safeFloat (ticker, 'price');
```

**Why**: Transpiler uses this pattern to distinguish helper calls.

### No Typed Arrays

**Avoid typed arrays** (Uint8Array, Int32Array, etc.). Use regular arrays.

```typescript
// ❌ AVOID
const buffer = new Uint8Array(32);

// ✅ USE
const buffer = [];
```

### No Regex Literals (Minimize Use)

**Minimize regex usage.** If needed, use string methods or base helpers.

```typescript
// ❌ AVOID WHEN POSSIBLE
const match = str.match(/\d+/);

// ✅ PREFER
const number = this.safeString (obj, 'number');
```

### No External Static Dependencies

**Don't import external libraries** (lodash, moment, ethers, etc.). Use base Exchange helpers.

```typescript
// ❌ FORBIDDEN
import _ from 'lodash';
import { ethers } from 'ethers';

// ✅ USE BASE HELPERS
this.safeString (obj, 'key');
this.safeFloat (obj, 'value');
this.extend (obj1, obj2);
```

## Source Control Rules

### Never Edit Transpiled Outputs

**Only edit TypeScript sources** in `ts/src/`. Never edit:
- `python/ccxt/*.py` (except base classes)
- `php/*.php` (except base classes)
- `go/*.go` (except base classes)
- `cs/*.cs` (except base classes)

These are **auto-generated** and will be overwritten on next build.

### Single File Per Exchange

Edit **only the exchange file** you're working on:
- Main: `ts/src/{exchange}.ts`
- Abstract: `ts/src/abstract/{exchange}.ts`

Don't commit:
- `/build/*`
- `/js/*` (compiled from TS)
- `/dist/*`
- `/README.md` (auto-generated)
- `/package.json` or `/package-lock.json` (unless adding dependencies)

## Language-Specific Considerations

### Python Transpilation
- `undefined` → `None`
- `let` → variable assignment
- Helper methods keep same names

### PHP Transpilation
- `undefined` → `null`
- Method names use underscores: `fetchTicker` → `fetch_ticker`
- Arrays preserve structure

### Go Transpilation
- `undefined` → `nil`
- Requires strict typing (handled by base)
- Capitalization for exports

### C# Transpilation
- `undefined` → `null`
- PascalCase method names: `fetchTicker` → `FetchTicker`
- Strong typing requirements

## Additional Transpilation Rules

### Code Structure

**Critical formatting requirements**:

```typescript
// ✅ CORRECT - Empty line between methods
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    // method body
}

async fetchBalance (params = {}): Promise<Balances> {
    // method body
}

// ❌ WRONG - No empty line between methods (breaks transpiler)
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    // method body
}
async fetchBalance (params = {}): Promise<Balances> {
    // method body
}

// ❌ WRONG - Empty lines inside method body (breaks transpiler)
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    const market = this.market (symbol);
    
    const request = { 'symbol': market['id'] };  // empty line above breaks it!
    return this.parseTicker (response);
}
```

### Indentation

- Use **4 spaces exactly** (no tabs)
- Python-style indentation preserved for all languages
- Consistent indentation critical for transpiler

### Comments

```typescript
// ✅ CORRECT - Double-slash comments
// This is a comment
const value = this.safeString (obj, 'key');

// ❌ AVOID - Multi-line comments
/* This is a
   multi-line comment */

// ❌ AVOID - Mixed comment styles
```

### Variable Declarations

```typescript
// ✅ CORRECT - Use const/let, never var
const symbol = 'BTC/USDT';
let result = undefined;

// ❌ FORBIDDEN - var keyword
var symbol = 'BTC/USDT';
```

### Semicolons

**Always end statements with semicolons** (PHP/C-style):

```typescript
// ✅ CORRECT
const price = this.safeFloat (ticker, 'price');
const volume = this.safeFloat (ticker, 'volume');

// ❌ WRONG
const price = this.safeFloat (ticker, 'price')
const volume = this.safeFloat (ticker, 'volume')
```

### Dictionary Key Access

**Always use single-quoted string notation** for all dictionary keys:

```typescript
// ✅ CORRECT - Single-quoted string keys
const id = market['id'];
const symbol = ticker['symbol'];
const price = data['price'];

// ❌ FORBIDDEN - Dot notation (doesn't transpile to Python/PHP)
const id = market.id;
const symbol = ticker.symbol;
```

**Why**: In Python/PHP, `object.key` ≠ `object['key']`

### Method Calls and Operators

```typescript
// ❌ FORBIDDEN - .includes() method
if (array.includes('value')) {}

// ✅ CORRECT - .indexOf() method
if (array.indexOf('value') >= 0) {}

// ❌ FORBIDDEN - toString() on floats
const str = (0.00000001).toString();  // becomes '1e-8'

// ✅ CORRECT - Use this.numberToString()
const str = this.numberToString (0.00000001);
```

### Closures and Functional Programming

**Do not use closures in derived exchange classes**:

```typescript
// ❌ FORBIDDEN - map/filter with arrow functions
const ids = symbols.map (x => this.marketId (x));
const filtered = orders.filter (x => x['status'] === 'open');

// ✅ CORRECT - Use explicit loops
const ids = [];
for (let i = 0; i < symbols.length; i++) {
    ids.push (this.marketId (symbols[i]));
}

const filtered = [];
for (let i = 0; i < orders.length; i++) {
    if (orders[i]['status'] === 'open') {
        filtered.push (orders[i]);
    }
}
```

### The `in` Operator

**Do not use `in` for non-associative arrays**:

```typescript
// ❌ WRONG - 'in' with arrays
if ('value' in array) {}

// ✅ CORRECT - Use indexOf
if (array.indexOf ('value') >= 0) {}

// ✅ OK - 'in' with objects/dictionaries
if ('key' in object) {}
```

### Complex Logic

**Keep it simple**:

```typescript
// ❌ AVOID - Complex operators
const result = a && b || c ? d + 80 : e ** f;

// ✅ PREFER - Simple, clear logic
let result = undefined;
if (a && b) {
    result = d + 80;
} else if (c) {
    result = d + 80;
} else {
    result = Math.pow (e, f);
}
```

### Non-Existent Keys

**Never access non-existent keys directly**:

```typescript
// ❌ FORBIDDEN - Direct access with fallback
const value = array['key'] || {};  // breaks in Python/PHP!

// ✅ CORRECT - Use safe methods
const value = this.safeValue (array, 'key', {});
```

## Testing Transpilation

After editing, **always test transpilation**:

```bash
# Test single exchange
npm run emitAPI binance
npm run transpileRest binance

# Test all
npm run build
```

**Check output files** in `python/`, `php/`, `go/`, `cs/` to verify correct transpilation.

## Additional Transpilation Rules

### Timestamps and Time Conversions

**Always use milliseconds** in CCXT. When exchanges use seconds:

```typescript
// ✅ CORRECT - Convert seconds to milliseconds
const timestamp = this.safeTimestamp (ticker, 'timestamp');  // Auto-converts seconds to ms

// ✅ CORRECT - Manual conversion
const timestampInSeconds = this.safeInteger (ticker, 'timestamp');
const timestamp = timestampInSeconds * 1000;

// ❌ WRONG - Using seconds directly
const timestamp = this.safeInteger (ticker, 'timestamp');  // Without conversion
```

**When sending timestamps to exchanges**:
```typescript
// Some exchanges expect seconds
const timestamp = Math.floor (this.milliseconds () / 1000);  // ms to seconds
```

### Handling Precision with the Precise Class

**Never use floats for prices/amounts!** Use `Precise` class for string-based decimal math.

```typescript
// ❌ WRONG - Float arithmetic (precision errors)
const cost = parseFloat (price) * parseFloat (amount);

// ✅ CORRECT - Use Precise class
const cost = Precise.stringMul (price, amount);

// Other Precise operations
const sum = Precise.stringAdd (a, b);
const difference = Precise.stringSub (a, b);
const quotient = Precise.stringDiv (a, b);
const absolute = Precise.stringAbs (a);
const minimum = Precise.stringMin (a, b);
const maximum = Precise.stringMax (a, b);
const equals = Precise.stringEq (a, b);
const greaterThan = Precise.stringGt (a, b);
const lessThan = Precise.stringLt (a, b);
```

### Base Class Cryptography Methods

Available in every exchange class (inherited from base Exchange class):

```typescript
// Hashing
this.hash (string, algorithm = 'md5', digest = 'hex');
// algorithms: 'sha1', 'sha256', 'sha384', 'sha512', 'md5', 'keccak'
// digest: 'hex', 'base64', 'binary'

// HMAC (most common for API authentication)
this.hmac (message, secret, algorithm = 'sha256', digest = 'hex');

// JWT tokens
this.jwt (payload, secret, algorithm = 'HS256');

// RSA signatures
this.rsa (message, secret, algorithm = 'RS256');

// ECDSA signatures
this.ecdsa (message, secret, algorithm = 'p256', hash = undefined);

// TOTP (2FA codes)
this.totp (secret);
```

### String Concatenation and Operators

**Critical**: The `+` operator is ONLY for string concatenation!

```typescript
// ✅ CORRECT - String concatenation
const url = baseUrl + '/path';
const message = timestamp + method + path + body;

// ❌ WRONG - Arithmetic with +
const cost = amount + fee;  // NEVER do this!

// ✅ CORRECT - Use Precise for arithmetic
const cost = Precise.stringAdd (amount, fee);

// ✅ CORRECT - Numeric types can use arithmetic operators directly
const timestamp = this.milliseconds () * 1000;  // OK for numbers
const price = parseFloat (priceString) * 1.5;  // OK but discouraged
```

### Escaped Characters in Strings

**When you need literal quotes or special chars**:

```typescript
// ✅ CORRECT - Double quotes with eslint comment
const query = "SELECT * FROM table WHERE symbol = \"BTC/USDT\""; // eslint-disable-line quotes

// ✅ CORRECT - Template literals for complex strings
const query = `SELECT * FROM table WHERE symbol = "BTC/USDT"`;

// ❌ WRONG - Trying to escape in single quotes
const query = 'SELECT * FROM table WHERE symbol = "BTC/USDT"';  // Won't transpile correctly
```

### Array Length Hints for Transpiler

Help transpiler understand fixed-size arrays:

```typescript
// When unpacking arrays with known length
const [key, secret] = credentials.split (':');  // hints transpiler about array size
const parts = symbol.split ('/');  // [baseId, quoteId]
```

## New Exchange Integration Guidelines

### Step 1: Create Exchange File

Create `ts/src/exchangename.ts` with skeleton:

```typescript
import Exchange from './abstract/exchangename.js';
import type { Int, OrderSide, OrderType, Str, Ticker, Tickers, Order, Trade, Market, Currency, Currencies, Dictionary } from './base/types.js';

export default class exchangename extends Exchange {
    describe () {
        return this.deepExtend (super.describe (), {
            'id': 'exchangename',
            'name': 'Exchange Name',
            'countries': ['US'],  // ISO 3166-1 alpha-2
            'rateLimit': 1000,  // milliseconds between requests
            'version': 'v1',
            'has': {
                'CORS': undefined,
                'spot': true,
                'margin': false,
                'swap': false,
                'future': false,
                'option': false,
                'createOrder': true,
                'fetchBalance': true,
                'fetchMarkets': true,
                'fetchTicker': true,
                'fetchTickers': false,
                'fetchOrderBook': true,
                'fetchOHLCV': true,
                'fetchTrades': true,
                // ... list all supported methods
            },
            'timeframes': {
                '1m': '1',
                '5m': '5',
                '15m': '15',
                '1h': '60',
                '1d': '1440',
            },
            'urls': {
                'logo': 'https://example.com/logo.png',
                'api': {
                    'public': 'https://api.exchange.com',
                    'private': 'https://api.exchange.com',
                },
                'www': 'https://exchange.com',
                'doc': [
                    'https://docs.exchange.com',
                ],
                'fees': 'https://exchange.com/fees',
            },
            'api': {
                'public': {
                    'get': [
                        'markets',
                        'ticker/{symbol}',
                        'orderbook/{symbol}',
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
            'fees': {
                'trading': {
                    'maker': 0.001,
                    'taker': 0.002,
                },
            },
            'exceptions': {
                'exact': {
                    'Invalid API key': 'AuthenticationError',
                    'Insufficient balance': 'InsufficientFunds',
                },
                'broad': {
                    'timeout': 'RequestTimeout',
                    'banned': 'PermissionDenied',
                },
            },
        });
    }
}
```

### Step 2: Generate Implicit API Methods

The `api` definition automatically generates methods:

```typescript
'api': {
    'public': {
        'get': [
            'markets',           // → this.publicGetMarkets (params)
            'ticker/{symbol}',   // → this.publicGetTickerSymbol (params)
        ],
    },
    'private': {
        'post': [
            'order',             // → this.privatePostOrder (params)
        ],
    },
}
```

Naming convention: `{visibility}{Method}{CamelCasePath}`

### Step 3: Implement Core Methods

Implement methods in this order:

1. `fetchMarkets()` - Load trading pairs
2. `fetchTicker()` / `fetchTickers()` - Get market data
3. `fetchOrderBook()` - Get order book
4. `fetchTrades()` - Get recent trades
5. `fetchBalance()` - Get account balance
6. `createOrder()` - Place orders
7. `cancelOrder()` - Cancel orders
8. `fetchOrder()` / `fetchOrders()` - Query orders

### Step 4: Add Docstrings

Document all public methods:

```typescript
/**
 * @method
 * @name exchangename#fetchTicker
 * @description fetches a price ticker for a single market
 * @param {string} symbol unified symbol of the market to fetch the ticker for
 * @param {object} [params] extra parameters specific to the exchange API endpoint
 * @returns {object} a [ticker structure](https://docs.ccxt.com/#/?id=ticker-structure)
 */
async fetchTicker (symbol: string, params = {}): Promise<Ticker> {
    await this.loadMarkets ();
    const market = this.market (symbol);
    const request = {
        'symbol': market['id'],
    };
    const response = await this.publicGetTickerSymbol (this.extend (request, params));
    return this.parseTicker (response, market);
}
```

**Docstring Components**:
- `@method` - Always required
- `@name exchangename#methodName` - Exchange and method
- `@description` - Human-readable description
- `@param {type} name description` - Parameters (include `[param]` for optional)
- `@returns {type} description with [link](url)` - Return value

### Step 5: Add to CI/CD

1. Add exchange to `exchanges.json`
2. Run `npm run export-exchanges` to update metadata
3. Add API keys to `keys.json` (for private testing)
4. Enable in CI: `.github/workflows/` files

### Integration Checklist

- [ ] Create exchange file in `ts/src/`
- [ ] Implement required methods (fetchMarkets, fetchTicker, etc.)
- [ ] Add error mappings in `exceptions`
- [ ] Test transpilation: `npm run transpileRest exchangename`
- [ ] Add docstrings to all public methods
- [ ] Test methods: `npm run test exchangename`
- [ ] Add to `exchanges.json`
- [ ] Update documentation
- [ ] Submit pull request

