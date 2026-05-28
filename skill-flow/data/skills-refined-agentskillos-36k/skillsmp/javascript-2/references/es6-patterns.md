# Modern JavaScript Patterns (ES6+)

## Destructuring

### Array Destructuring

```javascript
// Basic
const [first, second] = [1, 2, 3];
// first = 1, second = 2

// Skip elements
const [, , third] = [1, 2, 3];
// third = 3

// Rest operator
const [head, ...tail] = [1, 2, 3, 4];
// head = 1, tail = [2, 3, 4]

// Default values
const [a, b = 10] = [1];
// a = 1, b = 10

// Swap variables
let x = 1, y = 2;
[x, y] = [y, x];
```

### Object Destructuring

```javascript
// Basic
const { name, age } = { name: 'John', age: 30 };

// Rename
const { name: userName } = { name: 'John' };
// userName = 'John'

// Default values
const { name, role = 'user' } = { name: 'John' };
// role = 'user'

// Nested destructuring
const { address: { city } } = {
  address: { city: 'NYC', zip: '10001' }
};

// Rest in objects
const { id, ...rest } = { id: 1, name: 'John', age: 30 };
// rest = { name: 'John', age: 30 }

// Function parameters
function createUser({ name, email, role = 'user' }) {
  return { name, email, role };
}
```

## Spread Operator

### Arrays

```javascript
// Combine arrays
const all = [...arr1, ...arr2];

// Clone array (shallow)
const clone = [...original];

// Convert iterable to array
const chars = [...'hello'];  // ['h', 'e', 'l', 'l', 'o']

// Function arguments
const numbers = [1, 2, 3];
Math.max(...numbers);  // 3
```

### Objects

```javascript
// Merge objects (later wins)
const merged = { ...defaults, ...options };

// Clone object (shallow)
const clone = { ...original };

// Add/override properties
const updated = { ...user, updatedAt: new Date() };

// Conditional properties
const user = {
  name: 'John',
  ...(includeEmail && { email: 'john@test.com' })
};
```

## Arrow Functions

### Syntax

```javascript
// Basic
const add = (a, b) => a + b;

// Single parameter (no parens needed)
const double = x => x * 2;

// No parameters
const greet = () => 'Hello';

// Multi-line (requires braces and return)
const process = (data) => {
  const cleaned = clean(data);
  return transform(cleaned);
};

// Return object (wrap in parens)
const makeUser = (name) => ({ name, createdAt: new Date() });
```

### When to Use

```javascript
// ✅ Callbacks
const doubled = numbers.map(n => n * 2);
const adults = users.filter(u => u.age >= 18);

// ✅ Short functions
const sum = (a, b) => a + b;

// ❌ Methods (loses this binding)
const obj = {
  name: 'Object',
  greet: () => {
    console.log(this.name);  // undefined!
  }
};

// ✅ Use regular function for methods
const obj = {
  name: 'Object',
  greet() {
    console.log(this.name);  // 'Object'
  }
};
```

## Template Literals

```javascript
// Interpolation
const message = `Hello, ${name}!`;

// Multi-line
const html = `
  <div class="card">
    <h1>${title}</h1>
    <p>${body}</p>
  </div>
`;

// Expressions
const result = `Total: ${items.reduce((a, b) => a + b, 0)}`;

// Tagged templates
function sql(strings, ...values) {
  // strings: ['SELECT * FROM users WHERE id = ', '']
  // values: [userId]
  return { text: strings.join('$1'), values };
}
const query = sql`SELECT * FROM users WHERE id = ${userId}`;
```

## Classes

### Basic Syntax

```javascript
class User {
  // Private field
  #password;

  // Public field
  role = 'user';

  // Static field
  static count = 0;

  constructor(name, email) {
    this.name = name;
    this.email = email;
    User.count++;
  }

  // Instance method
  greet() {
    return `Hello, ${this.name}`;
  }

  // Getter
  get displayName() {
    return `${this.name} (${this.role})`;
  }

  // Setter
  set password(value) {
    this.#password = hash(value);
  }

  // Static method
  static create(data) {
    return new User(data.name, data.email);
  }
}
```

### Inheritance

```javascript
class Admin extends User {
  constructor(name, email, permissions) {
    super(name, email);  // Call parent constructor
    this.role = 'admin';
    this.permissions = permissions;
  }

  // Override method
  greet() {
    return `${super.greet()} (Admin)`;
  }
}
```

## Modules

### Named Exports

```javascript
// math.js
export const PI = 3.14159;
export function add(a, b) { return a + b; }
export class Calculator { /* ... */ }

// Import
import { PI, add, Calculator } from './math.js';
import { add as sum } from './math.js';  // Rename
import * as math from './math.js';  // Namespace
```

### Default Export

```javascript
// user.js
export default class User { /* ... */ }

// Import
import User from './user.js';
import MyUser from './user.js';  // Any name works
```

### Re-exports

```javascript
// index.js - barrel file
export { User } from './user.js';
export { Order } from './order.js';
export * from './utils.js';
export { default as Config } from './config.js';
```

## Optional Chaining

```javascript
// Property access
const city = user?.address?.city;

// Method calls
const result = obj?.method?.();

// Array access
const first = arr?.[0];

// With nullish coalescing
const name = user?.profile?.name ?? 'Anonymous';

// Short-circuit evaluation
// If user is nullish, nothing after ?. executes
user?.address?.city?.toUpperCase();
```

## Nullish Coalescing

```javascript
// ?? only checks null/undefined (not falsy)
const value = input ?? 'default';

// Different from ||
const count = 0;
count || 10;   // 10 (0 is falsy)
count ?? 10;   // 0 (0 is not nullish)

// Common use cases
const port = config.port ?? 3000;
const name = user.name ?? 'Anonymous';

// Assignment operator
let x;
x ??= 'default';  // Assign if nullish
```

## Array Methods

```javascript
// map - transform elements
const doubled = [1, 2, 3].map(n => n * 2);

// filter - select elements
const adults = users.filter(u => u.age >= 18);

// find - first match
const admin = users.find(u => u.role === 'admin');

// findIndex - index of first match
const index = users.findIndex(u => u.id === targetId);

// some - any match
const hasAdmin = users.some(u => u.role === 'admin');

// every - all match
const allActive = users.every(u => u.active);

// reduce - accumulate
const total = orders.reduce((sum, o) => sum + o.amount, 0);

// flat - flatten nested arrays
[[1, 2], [3, 4]].flat();  // [1, 2, 3, 4]

// flatMap - map then flat
users.flatMap(u => u.orders);  // All orders in one array

// includes - check existence
[1, 2, 3].includes(2);  // true

// at - index from end
const last = arr.at(-1);
const secondLast = arr.at(-2);
```

## Object Methods

```javascript
// Object.entries - to key-value pairs
const entries = Object.entries({ a: 1, b: 2 });
// [['a', 1], ['b', 2]]

// Object.fromEntries - from key-value pairs
const obj = Object.fromEntries([['a', 1], ['b', 2]]);
// { a: 1, b: 2 }

// Object.keys / Object.values
Object.keys({ a: 1, b: 2 });   // ['a', 'b']
Object.values({ a: 1, b: 2 }); // [1, 2]

// Object.assign - merge
const merged = Object.assign({}, defaults, options);

// Transform object
const doubled = Object.fromEntries(
  Object.entries(obj).map(([k, v]) => [k, v * 2])
);
```

## String Methods

```javascript
// includes, startsWith, endsWith
'hello world'.includes('world');    // true
'hello world'.startsWith('hello');  // true
'hello world'.endsWith('world');    // true

// padStart, padEnd
'5'.padStart(3, '0');   // '005'
'5'.padEnd(3, '0');     // '500'

// repeat
'ab'.repeat(3);  // 'ababab'

// trim variants
'  hello  '.trim();       // 'hello'
'  hello  '.trimStart();  // 'hello  '
'  hello  '.trimEnd();    // '  hello'

// replaceAll
'a-b-c'.replaceAll('-', '_');  // 'a_b_c'
```

## New Data Structures

### Map

```javascript
const map = new Map();
map.set('key', 'value');
map.set(objKey, 'works with objects');

map.get('key');      // 'value'
map.has('key');      // true
map.delete('key');
map.size;            // number of entries

// Iterate
for (const [key, value] of map) {
  console.log(key, value);
}
```

### Set

```javascript
const set = new Set([1, 2, 2, 3]);  // {1, 2, 3}

set.add(4);
set.has(2);     // true
set.delete(2);
set.size;       // 3

// Unique values
const unique = [...new Set(array)];
```

### WeakMap / WeakSet

```javascript
// Keys must be objects, allows garbage collection
const weakMap = new WeakMap();
let obj = { data: 'value' };
weakMap.set(obj, 'metadata');

obj = null;  // Entry can be garbage collected
```
