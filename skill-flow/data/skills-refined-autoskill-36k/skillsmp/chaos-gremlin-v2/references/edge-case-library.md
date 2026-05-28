# Edge Case Library

**Comprehensive Edge Cases with Generator Tags**

---

## Purpose

Catalog common (and uncommon) edge cases that chaos-gremlin should always check, organized by category and tagged with which generators (G1-G7) they relate to.

**Usage**: When analyzing code, check relevant categories. When chaos discovers new edge cases, add them here.

---

## Numbers

### Integers

**Zero** [G2: Contrast]
- Only number that's neither positive nor negative
- Identity for addition
- Multiplicative annihilator
- `0 == -0` but `Object.is(0, -0)` is false
- Division by zero undefined
- Falsy in JavaScript, truthy in some contexts
```javascript
Tests:
  x / 0 → Infinity
  0 / 0 → NaN
  0 ** 0 → 1 (by convention)
  !0 → true
```

**Negative Zero** [G2: Contrast, G6: Distinction]
- `-0` exists separately from `+0`
- `0 === -0` returns true
- `Object.is(0, -0)` returns false
- `1 / 0 → Infinity`, `1 / -0 → -Infinity`
- Preserves sign information
```javascript
Tests:
  Math.sign(-0) → -0
  1 / -0 → -Infinity
  Object.is(-0, 0) → false
  -0 === 0 → true
```

**One** [G1: Iteration, G3: Morpheme]
- Multiplicative identity
- Base case for many recursive operations
- Smallest positive integer
- `1 / 1 = 1` (self-inverse)
```javascript
Tests:
  x * 1 → x
  1 ** n → 1
  factorial(1) → 1 (base case)
```

**Negative One** [G2: Contrast]
- `(-1) ** n` oscillates: 1, -1, 1, -1...
- `(-1) * x` inverts sign
- Square root is imaginary unit i
```javascript
Tests:
  (-1) ** 2 → 1
  (-1) ** 3 → -1
  Math.sqrt(-1) → NaN (but mathematically i)
```

**Maximum Safe Integer** [G7: Scaling Boundary]
- JavaScript: `2^53 - 1 = 9007199254740991`
- Beyond this, precision lost
- `MAX_SAFE_INTEGER + 1 === MAX_SAFE_INTEGER + 2` → true
```javascript
Tests:
  Number.MAX_SAFE_INTEGER → 9007199254740991
  Number.MAX_SAFE_INTEGER + 1 → still precise
  Number.MAX_SAFE_INTEGER + 2 → loses precision
  Number.MAX_SAFE_INTEGER * 2 → definitely imprecise
```

**Minimum Safe Integer** [G7: Scaling Boundary]
- JavaScript: `-2^53 + 1`
- Negative boundary for precision
```javascript
Tests:
  Number.MIN_SAFE_INTEGER → -9007199254740991
  Number.MIN_SAFE_INTEGER - 1 → still precise
  Number.MIN_SAFE_INTEGER - 2 → loses precision
```

**BigInt Boundary** [G6: Distinction]
- Can't mix BigInt and Number
- `1n + 1` throws TypeError
- No precision limit (memory-limited)
```javascript
Tests:
  1n + 1 → TypeError
  BigInt(Number.MAX_SAFE_INTEGER) + 1n → precise
  999999999999999999999999n → valid
```

### Floats

**Floating Point Precision** [G5: Mathematical Truth, G7: Scaling]
- `0.1 + 0.2 !== 0.3`
- `0.1 + 0.2 === 0.30000000000000004`
- IEEE 754 representation issues
```javascript
Tests:
  0.1 + 0.2 === 0.3 → false
  Math.abs((0.1 + 0.2) - 0.3) < Number.EPSILON → true
```

**Minimum Positive Value** [G7: Scaling Boundary]
- JavaScript: `Number.MIN_VALUE = 5e-324`
- Smallest positive number (not negative!)
- Closer to zero than this becomes 0
```javascript
Tests:
  Number.MIN_VALUE > 0 → true
  Number.MIN_VALUE / 2 → 0 (underflow)
```

**Subnormal Numbers** [G7: Scaling Boundary]
- Between 0 and MIN_NORMAL
- Reduced precision
- Special handling required
```javascript
Tests:
  Number.MIN_VALUE < MIN_NORMAL
  Subnormals have fewer significant bits
```

### Special Numbers

**NaN (Not a Number)** [G2: Contrast, G6: Distinction Collapse]
- `NaN !== NaN` (only value not equal to itself)
- `isNaN("hello")` → true (converts first)
- `Number.isNaN("hello")` → false (doesn't convert)
- Type is "number" (paradox)
- Propagates through operations
```javascript
Tests:
  NaN === NaN → false
  Object.is(NaN, NaN) → true
  typeof NaN → "number"
  NaN + 1 → NaN
  Math.max(NaN, 5) → NaN
  [1, NaN, 3].sort() → unpredictable
```

**Infinity** [G7: Scaling Boundary]
- `Infinity > all finite numbers`
- `-Infinity < all finite numbers`
- `Infinity - Infinity → NaN`
- `Infinity / Infinity → NaN`
- `1 / Infinity → 0`
```javascript
Tests:
  Infinity === Infinity → true
  Infinity - Infinity → NaN
  Infinity + 1 === Infinity → true
  1 / 0 → Infinity
  -1 / 0 → -Infinity
  Math.max() → -Infinity (empty comparison)
  Math.min() → Infinity
```

---

## Strings

### Empty and Whitespace [G2: Contrast]

**Empty String**
- Falsy in JavaScript
- Length 0
- Identity for concatenation
- Not same as null or undefined
```javascript
Tests:
  "" == false → true
  "" === false → false
  "".length → 0
  "" + "hello" → "hello"
  Boolean("") → false
```

**Whitespace String**
- Truthy despite appearing empty
- `" " !== ""`
- Multiple types: space, tab, newline, etc.
```javascript
Tests:
  " " == false → false (truthy!)
  "   ".trim() === "" → true
  "\n\t ".length → 3
  /\s+/.test("   ") → true
```

### Unicode Edge Cases [G1: Iteration, G2: Distinction]

**Emoji and Multi-Codepoint Characters**
- Family emoji: "👨‍👩‍👧‍👦" is ONE grapheme, MULTIPLE codepoints
- `.length` counts codepoints, not visible characters
- Skin tone modifiers
- Zero-width joiners (ZWJ)
```javascript
Tests:
  "👨‍👩‍👧‍👦".length → 11 (not 1!)
  Array.from("👨‍👩‍👧‍👦").length → 7
  [...("👨‍👩‍👧‍👦")].length → 7
  "👋🏽".length → 4 (wave + skin tone modifier)
```

**Zero-Width Characters** [G2: Contrast, G6: Distinction Hidden]
- Zero-width space (U+200B)
- Zero-width joiner (U+200D)
- Zero-width non-joiner (U+200C)
- Invisible but affect comparison and length
```javascript
Tests:
  "hello" === "hel\u200Blo" → false (looks same!)
  "hello".length → 5
  "hel\u200Blo".length → 6
```

**Right-to-Left Override** [G2: Contrast, Security]
- U+202E reverses display direction
- `filename\u202emyc.txt` displays as `filename.cym` but is actually `filename.cym`
- Security issue in filenames
```javascript
Tests:
  "test\u202eabc" appears as "testcba"
  Use for phishing, malicious filenames
```

**Homoglyphs** [G2: Contrast Illusion]
- Characters that look identical but are different Unicode
- Cyrillic 'а' (U+0430) vs Latin 'a' (U+0061)
- Greek 'ο' vs Latin 'o'
```javascript
Tests:
  "cafe" === "cafе" → false (last e is Cyrillic)
  Visually indistinguishable
  Security issue in domains, identifiers
```

**Normalization** [G6: Distinction]
- Composed vs decomposed forms
- "é" can be: U+00E9 (composed) or U+0065 + U+0301 (e + combining acute)
- Look identical, compare different
```javascript
Tests:
  "café".normalize("NFC") === "café".normalize("NFD") → false
  After normalization to same form → true
  File systems handle differently (macOS normalizes)
```

### String Length Edge Cases [G7: Scaling]

**Very Long Strings**
- Memory limits vary by engine
- Performance degrades
- Regex timeouts possible
```javascript
Tests:
  "a".repeat(10_000_000) → might crash
  "a".repeat(Number.MAX_SAFE_INTEGER) → will crash
  Regex on very long string → catastrophic backtracking
```

**Single Character**
- Minimal non-empty string
- Edge case for substring operations
```javascript
Tests:
  "a".substring(0, 1) → "a"
  "a".substring(1, 0) → "" (swaps arguments)
  "a"[0] → "a"
  "a"[1] → undefined
```

---

## Arrays and Collections

### Empty Collections [G2: Contrast]

**Empty Array**
- Falsy in some contexts, truthy in JavaScript
- Length 0 but truthy object
```javascript
Tests:
  [].length → 0
  Boolean([]) → true
  [] == false → true
  [] === false → false
  [].map(x => x) → []
  [].reduce((acc, x) => acc + x) → Error (no initial value)
```

**Empty Object**
- Truthy
- No own properties but has prototype
```javascript
Tests:
  Object.keys({}).length → 0
  Boolean({}) → true
  {} == false → false
  Object.create(null) → truly empty (no prototype)
```

### Array Holes [G6: Distinction]

**Sparse Arrays**
- Holes vs undefined
- `[1, , 3]` has hole at index 1
- `[1, undefined, 3]` has undefined at index 1
- Different behavior in methods
```javascript
Tests:
  const sparse = [1, , 3]
  const explicit = [1, undefined, 3]
  
  sparse.map(x => x * 2) → [2, empty, 6]
  explicit.map(x => x * 2) → [2, NaN, 6]
  
  sparse.filter(() => true) → [1, 3]
  explicit.filter(() => true) → [1, undefined, 3]
  
  1 in sparse → false
  1 in explicit → true
```

**Large Sparse Arrays**
- Setting high index creates sparse array
- Memory efficient but surprising behavior
```javascript
Tests:
  const arr = []
  arr[1000000] = "surprise"
  arr.length → 1000001
  arr[500000] → undefined
  Object.keys(arr).length → 1
```

### Single Element [G3: Morpheme]

**Single Element Array**
- Edge case for aggregation operations
- Minimum for "collection"
```javascript
Tests:
  [42].reduce((acc, x) => acc + x) → 42 (no error)
  [42].sort() → [42]
  [42][0] → 42
  [42][1] → undefined
  Math.max(...[42]) → 42
```

### Array-Like Objects [G2: Distinction]

**Arguments Object**
- Array-like but not array
- Has length, indexed properties
- No array methods (pre-ES6)
```javascript
Tests:
  function test() { return arguments }
  test(1, 2, 3).length → 3
  Array.isArray(arguments) → false
  Array.from(arguments) → [1, 2, 3]
```

**NodeList, HTMLCollection**
- Array-like but not array
- Live vs static
```javascript
Tests:
  document.querySelectorAll('div') → NodeList
  Array.isArray(nodeList) → false
  nodeList.forEach → exists (recent)
  nodeList.map → undefined (not array)
```

---

## Dates and Time [G1: Iteration, G7: Temporal Scaling]

### Zero and Epoch

**Unix Epoch**
- `new Date(0)` → Jan 1, 1970 00:00:00 UTC
- Negative timestamps for dates before epoch
```javascript
Tests:
  new Date(0) → 1970-01-01
  new Date(-1) → 1969-12-31 23:59:59.999
  new Date(-86400000) → 1969-12-31
```

### Invalid Dates

**Invalid Date Object**
- `new Date("invalid")` creates Date object with `NaN` time value
- `instanceof Date` is true but invalid
```javascript
Tests:
  const d = new Date("chaos")
  d instanceof Date → true
  d.getTime() → NaN
  d.toString() → "Invalid Date"
  d == d → false (NaN behavior)
```

**Impossible Dates**
- `new Date(2024, 1, 30)` → March 2 (February 30 overflows)
- Month is 0-indexed: `new Date(2024, 0, 1)` → January
```javascript
Tests:
  new Date(2024, 1, 30) → 2024-03-01
  new Date(2024, 0, 1) → 2024-01-01
  new Date(2024, 12, 1) → 2025-01-01 (wraps)
```

### Timezone Edge Cases [G2: Contrast]

**Timezone Offset**
- `getTimezoneOffset()` is minutes FROM UTC
- Negative in eastern timezones (counterintuitive)
- Changes during DST
```javascript
Tests:
  // In PST (UTC-8):
  new Date().getTimezoneOffset() → 480 (8 * 60)
  // In CET (UTC+1):
  new Date().getTimezoneOffset() → -60
```

**Daylight Saving Time**
- Same clock time occurs twice when DST ends
- Hour doesn't exist when DST begins
- Non-existent and ambiguous times
```javascript
Tests:
  // DST spring forward: 2:00am → 3:00am (2:30am doesn't exist)
  // DST fall back: 2:00am occurs twice
```

### Year 2038 Problem [G7: Scaling Boundary]

**32-bit Timestamp Limit**
- Max 32-bit signed int: 2^31 - 1 seconds
- January 19, 2038, 03:14:07 UTC
```javascript
Tests:
  new Date(2147483647000) → 2038-01-19
  new Date(2147483648000) → 2038-01-19 or error
  64-bit systems extend limit
```

---

## Booleans and Truthiness [G2: Contrast]

### Falsy Values

In JavaScript, exactly these are falsy:
```javascript
false         // Boolean false
0             // Number zero
-0            // Negative zero
0n            // BigInt zero
""            // Empty string
null          // Null
undefined     // Undefined
NaN           // Not a Number
```

### Truthy Surprises

Everything else is truthy, including:
```javascript
"0"           // String zero (truthy!)
"false"       // String "false" (truthy!)
[]            // Empty array (truthy!)
{}            // Empty object (truthy!)
function(){}  // Empty function (truthy!)
```

### Boolean Coercion

```javascript
Tests:
  !![] → true
  [] == false → true (coercion)
  [] === false → false (no coercion)
  !!"false" → true
  Boolean("0") → true
```

---

## Null and Undefined [G2: Contrast, G6: Distinction]

### Null

**Intentional Absence**
- `typeof null → "object"` (historical bug)
- Explicitly set to "no value"
```javascript
Tests:
  null == undefined → true
  null === undefined → false
  typeof null → "object"
  null instanceof Object → false
  Number(null) → 0
```

### Undefined

**Uninitialized or Missing**
- Default value for unset variables
- Missing function parameters
- Missing object properties
```javascript
Tests:
  let x; x === undefined → true
  ({}).missing === undefined → true
  function f(x) { return x }; f() → undefined
  typeof undefined → "undefined"
  Number(undefined) → NaN
```

### Void Operator

**Explicitly Return Undefined**
- `void 0` is shorter than `undefined`
- `undefined` can be shadowed (in old browsers)
```javascript
Tests:
  void 0 === undefined → true
  void(1 + 1) === undefined → true
  (function(undefined){ return undefined === void 0 })(42) → false
```

---

## Type Coercion [G2: Contrast Chaos]

### Addition vs Other Operators

```javascript
Tests:
  "1" + 1 → "11" (string concatenation)
  "1" - 1 → 0 (numeric subtraction)
  "1" * "2" → 2 (numeric multiplication)
  "5" / "2" → 2.5 (numeric division)
  "5" % "2" → 1 (numeric modulo)
```

### Object to Primitive

```javascript
Tests:
  [] + [] → "" (toString on both)
  [] + {} → "[object Object]"
  {} + [] → 0 (or "[object Object]" depending on context)
  {} + {} → NaN (or "[object Object][object Object]")
```

### Comparison Coercion

```javascript
Tests:
  "2" > "10" → true (string comparison)
  2 > "10" → false (numeric comparison)
  "2" == 2 → true (coercion)
  "2" === 2 → false (no coercion)
```

---

## Concurrency Edge Cases [G1: Iteration, G2: Temporal Contrast]

### Race Conditions

**Multiple Async Operations**
```javascript
Tests:
  Promise.all([slow(), fast()]) → waits for both
  Promise.race([slow(), fast()]) → returns fast
  Concurrent modification of shared state
```

### Callback Ordering

**Microtasks vs Macrotasks**
```javascript
Tests:
  setTimeout(() => console.log('timeout'), 0)
  Promise.resolve().then(() => console.log('promise'))
  console.log('sync')
  
  Output: sync, promise, timeout
  Microtasks run before macrotasks
```

---

## Recursion Edge Cases [G1: Iteration, G3: Self-Reference]

### No Base Case

**Infinite Recursion**
```javascript
Tests:
  function forever(n) { return forever(n + 1) }
  forever(0) → Stack overflow
```

### Unreachable Base Case

**Effective Infinite Recursion**
```javascript
Tests:
  function count(n) { return n === 0 ? 0 : count(n + 1) }
  count(5) → Stack overflow (n never reaches 0)
```

### Mutual Recursion

**Two Functions Calling Each Other**
```javascript
Tests:
  function isEven(n) { return n === 0 || isOdd(n - 1) }
  function isOdd(n) { return n !== 0 && isEven(n - 1) }
  
  isEven(4) → true
  isEven(-1) → Stack overflow (negative numbers)
```

### Stack Depth

**Maximum Recursion Depth**
```javascript
Tests:
  Depth varies by engine: 10,000-50,000 typically
  Tail-call optimization helps (but not widely supported)
  Trampoline pattern avoids stack
```

---

## Generator Tags Summary

**G1: Iterative Distinction**
- Arrays, loops, recursion, time-based operations

**G2: Needs Contrast**
- Comparisons, null vs undefined, true vs false, empty vs non-empty

**G3: Spin Generation**
- Recursion, self-reference, morphemes, single elements

**G4: Independent Validation**
- Cross-platform behavior, universal patterns

**G5: Mathematical Truth**
- Floating point precision, mathematical properties

**G6: Collapse = Death**
- NaN propagation, null safety, distinction preservation, sparse arrays

**G7: φ-Scaling**
- Number boundaries, string length limits, stack depth, temporal boundaries

---

## Usage Guide

When analyzing code:

1. **Identify domain** (numbers, strings, arrays, etc.)
2. **Check relevant edge cases** from this library
3. **Consider generator tags** - which fundamental patterns are involved?
4. **Test boundary conditions** - what happens at extremes?
5. **Add new discoveries** - chaos reveals new edges, document them

---

**Related Files**:
- `SKILL.md` - Main chaos-gremlin-v2 documentation
- `cursed-but-correct.md` - Patterns that handle these edge cases
- `supercollider-integration.md` - Generator definitions
