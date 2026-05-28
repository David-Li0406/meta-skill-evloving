# Common JavaScript Mistakes

## Type Coercion Gotchas

```javascript
// Loose equality surprises
"" == false       // true
0 == false        // true
null == undefined // true
[] == false       // true
[] == ![]         // true (!)

// Fix: Always use strict equality
"" === false      // false
0 === false       // false

// Number coercion
+"42"             // 42
+""               // 0
+null             // 0
+undefined        // NaN
+[]               // 0
+{}               // NaN

// String coercion
"" + 42           // "42"
"" + null         // "null"
"" + undefined    // "undefined"
"" + {}           // "[object Object]"
```

## Array Pitfalls

```javascript
// Checking for array
typeof []                    // "object" (not helpful!)
Array.isArray([])            // true (correct way)

// Empty array is truthy
if ([]) console.log("runs")  // This runs!
if ([].length) { }           // Check length instead

// Sparse arrays
const arr = [];
arr[5] = "value";
arr.length                   // 6
arr[0]                       // undefined (but slot exists?)
arr.hasOwnProperty(0)        // false

// Array mutation
const sorted = [3, 1, 2].sort();  // Mutates original!
const sortedCopy = [...arr].sort(); // Safe copy

// Sort is lexicographic by default
[10, 2, 1].sort()            // [1, 10, 2] (!)
[10, 2, 1].sort((a, b) => a - b) // [1, 2, 10]
```

## Object Gotchas

```javascript
// Object.keys() returns strings
const obj = { 1: "a", 2: "b" };
Object.keys(obj)             // ["1", "2"] (strings!)

// Property existence
"toString" in {}             // true (inherited!)
{}.hasOwnProperty("toString") // false

// Object.assign is shallow
const nested = { a: { b: 1 } };
const copy = Object.assign({}, nested);
copy.a.b = 2;
nested.a.b                   // 2 (mutated!)

// Fix: deep copy
const deepCopy = JSON.parse(JSON.stringify(nested));
// Or use structuredClone (modern browsers)
const deepCopy = structuredClone(nested);

// Spread is also shallow
const copy = { ...nested };
copy.a.b = 2;
nested.a.b                   // 2 (still mutated!)
```

## Async/Await Mistakes

```javascript
// Forgetting to await
async function getData() {
  const data = fetchData(); // Oops! Returns Promise, not data
  console.log(data);        // Promise { <pending> }
}

// Sequential when could be parallel
// Slow:
const user = await getUser();
const orders = await getOrders();

// Fast:
const [user, orders] = await Promise.all([
  getUser(),
  getOrders()
]);

// Unhandled rejections
async function risky() {
  const result = await mightFail(); // Throws, but caught where?
}
risky(); // Unhandled rejection!

// Fix: always handle
risky().catch(console.error);
// Or:
try {
  await risky();
} catch (e) {
  console.error(e);
}

// forEach doesn't wait
const ids = [1, 2, 3];
ids.forEach(async (id) => {
  await processId(id); // Doesn't wait!
});
console.log("done"); // Runs immediately

// Fix: use for...of
for (const id of ids) {
  await processId(id);
}
// Or Promise.all for parallel
await Promise.all(ids.map(id => processId(id)));
```

## this Binding

```javascript
// Lost context
const obj = {
  name: "John",
  greet() {
    console.log(this.name);
  }
};
const greet = obj.greet;
greet();                     // undefined (or throws in strict mode)

// Fix: bind
const greet = obj.greet.bind(obj);
// Or: arrow function
const obj = {
  name: "John",
  greet: () => console.log(this.name) // Wrong! Arrow inherits outer this
};

// Callback context
class Counter {
  count = 0;
  increment() {
    this.count++;
  }
}
const counter = new Counter();
button.addEventListener("click", counter.increment); // Broken!

// Fix: bind or arrow
button.addEventListener("click", () => counter.increment());
// Or: arrow function class property
class Counter {
  count = 0;
  increment = () => { this.count++; };
}
```

## Scope Issues

```javascript
// var hoisting
console.log(x);              // undefined (hoisted!)
var x = 5;

// let/const temporal dead zone
console.log(y);              // ReferenceError
let y = 5;

// Closure in loops (var)
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 3, 3, 3

// Fix: use let
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
// Output: 0, 1, 2
```

## Floating Point

```javascript
0.1 + 0.2 === 0.3            // false
0.1 + 0.2                    // 0.30000000000000004

// Fix: compare with epsilon
Math.abs(0.1 + 0.2 - 0.3) < Number.EPSILON // true

// Or use integers (cents instead of dollars)
const cents = 10 + 20;       // 30
const dollars = cents / 100; // 0.30

// For money, use a library
import Decimal from "decimal.js";
new Decimal("0.1").plus("0.2").equals("0.3") // true
```

## null vs undefined

```javascript
// Both are "empty" but different
typeof null                  // "object" (historical bug!)
typeof undefined             // "undefined"

// Default parameter only for undefined
function greet(name = "World") {
  console.log(`Hello ${name}`);
}
greet(undefined);            // "Hello World"
greet(null);                 // "Hello null"

// Nullish coalescing vs OR
const value = 0;
const a = value || "default";  // "default" (0 is falsy)
const b = value ?? "default";  // 0 (only null/undefined)
```

## Common Fix Patterns

| Mistake | Bad | Good |
|---------|-----|------|
| Equality | `==` | `===` |
| Array check | `typeof arr === 'object'` | `Array.isArray(arr)` |
| Object copy | `Object.assign()` for nested | `structuredClone()` |
| Async forEach | `arr.forEach(async ...)` | `for...of` or `Promise.all` |
| this in callback | `obj.method` | `obj.method.bind(obj)` |
| Loop variable | `var i` | `let i` |
| Floating point | `0.1 + 0.2 === 0.3` | Use epsilon or integers |
| Default for 0/'' | `\|\|` | `??` |
