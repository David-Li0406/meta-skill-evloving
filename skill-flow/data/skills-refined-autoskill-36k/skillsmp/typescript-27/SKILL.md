---
name: typescript
description: TypeScript and unicorn linting patterns. Use for typescript, array, for-of, reduce, forEach, throw, catch, modern js, es modules, string, number, error handling
---

# TypeScript & Unicorn Patterns

This project uses `unicorn.configs.recommended` which enforces 100+ rules for modern JavaScript/TypeScript.

## Arrays (IMPORTANT - Common Errors)

```ts
// NO reduce - use for-of or other methods
array.reduce((acc, item) => acc + item, 0); // Bad
let sum = 0;
for (const item of array) sum += item; // Good

// NO forEach - use for-of
array.forEach((item) => console.log(item)); // Bad
for (const item of array) console.log(item); // Good

// NO traditional for loops
for (let i = 0; i < array.length; i++) {} // Bad
for (const item of array) {
} // Good
for (const [index, item] of array.entries()) {
} // Good

// NO new Array()
new Array(10); // Bad
Array.from({ length: 10 }); // Good

// Use modern array methods
array.at(-1); // not array[array.length - 1]
array.includes(x); // not array.indexOf(x) !== -1
array.find((x) => x.id === id); // not array.filter(...)[0]
array.some((x) => x.valid); // not array.filter(...).length > 0
array.flat(); // not [].concat(...array)
array.flatMap((x) => x.items); // not array.map(...).flat()
array.toSorted(); // not [...array].sort()
array.toReversed(); // not [...array].reverse()
```

## Strings

```ts
// Use modern string methods
str.replaceAll('a', 'b'); // not str.replace(/a/g, 'b')
str.slice(1, 3); // not str.substr() or str.substring()
str.startsWith('x'); // not str.indexOf('x') === 0
str.endsWith('x'); // not str.slice(-1) === 'x'
str.trimStart(); // not str.trimLeft()
str.trimEnd(); // not str.trimRight()
str.codePointAt(0); // not str.charCodeAt(0)
str.at(-1); // not str.charAt(str.length - 1)
```

## Errors

```ts
// Always use "throw new Error" with message
throw new Error('Something went wrong'); // Good
throw Error('msg');     // Bad - missing "new"
throw 'error';          // Bad - not an Error object
throw new Error();      // Bad - missing message

// Catch variable must be named "error"
catch (error) {}  // Good
catch (e) {}      // Bad
catch (err) {}    // Bad

// Use TypeError for type errors
if (typeof x !== 'string') throw new TypeError('Expected string');
```

## Modern JavaScript

```ts
// Use ES modules
import x from 'module'; // Good
export { x }; // Good
const x = require('module'); // Bad - CommonJS
module.exports = x; // Bad - CommonJS

// Use node: protocol for Node.js builtins
import fs from 'node:fs'; // Good
import fs from 'fs'; // Bad

// Use globalThis
globalThis.setTimeout; // Good
window.setTimeout; // Bad - browser-specific
global.setTimeout; // Bad - Node-specific

// Prefer spread
[...array]; // Good
Array.from(array); // Bad

// Use .at() for negative indices
array.at(-1); // Good
array[array.length - 1]; // Bad

// Use top-level await in modules
const data = await fetchData(); // Good
(async () => {
  const data = await fetchData();
})(); // Bad - Wrapping in async IIFE
```

## Ternary & Conditionals

```ts
// NO nested ternaries
const x = a ? (b ? 1 : 2) : 3; // Bad
// Use if-else or extract to functions

// Prefer ternary for simple assignments
const x = condition ? 'a' : 'b'; // Good

// Prefer logical operators over ternary
const x = a ?? b; // not a !== null ? a : b
const x = a || b; // not a ? a : b

// NO negated conditions
if (!condition) {
} else {
} // Bad
if (condition) {
} else {
} // Good - Flip the condition
```

## Functions & Classes

```ts
// Move functions to highest possible scope

// NO static-only classes
class Utils {
  static helper() {}
} // Bad
const utils = { helper() {} }; // Good
function helper() {} // Good

// Use class fields
class Foo {
  bar = 'value';
} // Good
```

## DOM (Browser Code)

```ts
// Use modern DOM APIs
element.append(child); // not appendChild
element.remove(); // not parent.removeChild(element)
element.querySelector('.x'); // not getElementById/getElementsByClassName
element.closest('.x'); // not manual parent traversal
element.dataset.value; // not getAttribute('data-value')
element.addEventListener('click', fn); // not onclick = fn
element.classList.toggle('active'); // not manual add/remove

// Use KeyboardEvent.key
event.key === 'Enter'; // Good
event.keyCode === 13; // Bad
```

## Number & Math

```ts
// Use Number properties
Number.isNaN(x); // not isNaN(x)
Number.isFinite(x); // not isFinite(x)
Number.parseInt(x); // not parseInt(x)

// Use Math.trunc
Math.trunc(x); // Good
x | 0; // Bad - Bitwise for truncation
~~x; // Bad

// Use numeric separators
const billion = 1_000_000_000;
```

## Miscellaneous

```ts
// Explicit length check
if (array.length > 0) {
} // Good
if (array.length) {
} // Bad

// Use Set for has() checks
const set = new Set(array);
set.has(x);

// Use Object.fromEntries
Object.fromEntries(entries);

// Optional catch binding
try {
} catch {}

// Prefer export from
export { x } from './module';

// NO process.exit() - throw errors instead
// NO document.cookie - use a cookie library
// NO empty files
```

## Common Mistakes

| Mistake                   | Correct Pattern                   |
| ------------------------- | --------------------------------- |
| `array.reduce()`          | Use `for-of` loop                 |
| `array.forEach()`         | Use `for-of` loop                 |
| `for (let i = 0; ...)`    | Use `for-of` or `array.entries()` |
| `catch (e)`               | Use `catch (error)`               |
| `throw 'error'`           | Use `throw new Error('message')`  |
| `array[array.length - 1]` | Use `array.at(-1)`                |
| `[...array].sort()`       | Use `array.toSorted()`            |
| `import fs from 'fs'`     | Use `import fs from 'node:fs'`    |

## Delegation

- **Pattern discovery**: Use `Explore` agent to find existing patterns
- **Linting issues**: Run `pnpm lint:fix` to auto-fix
