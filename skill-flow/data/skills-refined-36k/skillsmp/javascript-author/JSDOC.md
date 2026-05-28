# JSDoc Documentation Guide

## Class Documentation

```javascript
/**
 * @class ComponentName
 * @extends HTMLElement
 * @description A component that handles user preferences and displays settings
 * @fires settings-change - Fired when user changes a setting
 * @fires debug-log - Emits debug information for logging
 *
 * @example
 * <settings-panel lang="en"></settings-panel>
 */
class ComponentName extends HTMLElement {
```

## Method Documentation

### Public Methods

```javascript
/**
 * Updates the component's displayed value
 * @param {string} value - The new value to display
 * @returns {void}
 */
setValue(value) {
    this.setAttribute('value', value);
}
```

### Private Methods

```javascript
/**
 * @private
 * Internal handler for click events
 * @param {MouseEvent} event - The click event
 */
handleClick(event) {
    event.preventDefault();
    this.processClick();
}
```

### Async Methods

```javascript
/**
 * Fetches data from the API
 * @async
 * @param {string} endpoint - The API endpoint
 * @returns {Promise<Object>} The fetched data
 * @throws {Error} If the fetch fails
 */
async fetchData(endpoint) {
    const response = await fetch(endpoint);
    if (!response.ok) {
        throw new Error(`Fetch failed: ${response.status}`);
    }
    return response.json();
}
```

## Getter Documentation

```javascript
/**
 * @readonly
 * @returns {string} The current language code from attribute, ancestor, or document
 */
get lang() {
    return this.getAttribute('lang') ||
           this.closest('[lang]')?.getAttribute('lang') ||
           document.documentElement.lang ||
           'en';
}
```

## Setter Documentation

```javascript
/**
 * @param {string} value - The message to display
 */
set message(value) {
    this.setAttribute('message', value);
}
```

## Static Methods

```javascript
/**
 * @static
 * @returns {string[]} List of attributes that trigger attributeChangedCallback
 */
static get observedAttributes() {
    return ['lang', 'value', 'disabled'];
}
```

## Type Annotations

| Type | Syntax | Example |
|------|--------|---------|
| String | `{string}` | `@param {string} name` |
| Number | `{number}` | `@param {number} count` |
| Boolean | `{boolean}` | `@param {boolean} enabled` |
| Object | `{Object}` | `@param {Object} options` |
| Array of strings | `{string[]}` | `@param {string[]} items` |
| Array of objects | `{Object[]}` | `@param {Object[]} users` |
| Custom Event | `{CustomEvent}` | `@param {CustomEvent} event` |
| HTML Element | `{HTMLElement}` | `@param {HTMLElement} element` |
| Specific Element | `{HTMLInputElement}` | `@param {HTMLInputElement} input` |
| Optional | `{string} [name]` | `@param {string} [name]` |
| With Default | `{string} [name='default']` | `@param {string} [name='guest']` |
| Nullable | `{?string}` | `@param {?string} nickname` |
| Union Type | `{string\|number}` | `@param {string\|number} id` |

## Event Documentation

Document custom events fired by the component:

```javascript
/**
 * @fires component-update
 * @type {CustomEvent}
 * @property {Object} detail - Event detail object
 * @property {string} detail.value - The updated value
 * @property {string} detail.previousValue - The previous value
 * @property {string} detail.source - Source of the update ('user' or 'api')
 */
```

## Callback Documentation

```javascript
/**
 * @callback FilterCallback
 * @param {Object} item - The item to filter
 * @param {number} index - The item's index
 * @returns {boolean} True if item should be included
 */

/**
 * Filters items using the provided callback
 * @param {FilterCallback} callback - The filter function
 * @returns {Object[]} Filtered items
 */
filterItems(callback) {
    return this.items.filter(callback);
}
```

## Common Tags Reference

| Tag | Purpose |
|-----|---------|
| `@class` | Class declaration |
| `@extends` | Parent class |
| `@description` | Detailed explanation |
| `@fires` | Events the component dispatches |
| `@param` | Function/method parameter |
| `@returns` | Return value |
| `@private` | Internal use only |
| `@readonly` | Getter property |
| `@static` | Static method/property |
| `@async` | Async function |
| `@throws` | Exceptions thrown |
| `@example` | Usage example |
| `@see` | Related documentation |
| `@deprecated` | Marked for removal |
| `@typedef` | Custom type definition |
| `@template` | Generic type parameter |

---

## Advanced Type Patterns

JSDoc provides TypeScript-like type checking in editors without requiring a build step.

### Type Definitions

Define reusable types with `@typedef`:

```javascript
/**
 * @typedef {Object} User
 * @property {string} id - Unique identifier
 * @property {string} name - Display name
 * @property {string} [email] - Optional email address
 * @property {UserRole} role - User's role
 */

/**
 * @typedef {'admin' | 'editor' | 'viewer'} UserRole
 */

/**
 * Fetch user by ID
 * @param {string} id
 * @returns {Promise<User>}
 */
async function getUser(id) {
  const response = await fetch(`/api/users/${id}`);
  return response.json();
}
```

### Generic Types

Use `@template` for generic functions:

```javascript
/**
 * @template T
 * @param {T[]} items - Array of items
 * @param {(item: T) => boolean} predicate - Filter function
 * @returns {T | undefined}
 */
function findFirst(items, predicate) {
  return items.find(predicate);
}

/**
 * @template K, V
 * @param {Map<K, V>} map - The map to search
 * @param {V} value - Value to find
 * @returns {K | undefined}
 */
function findKeyByValue(map, value) {
  for (const [k, v] of map.entries()) {
    if (v === value) return k;
  }
  return undefined;
}
```

### Union and Intersection Types

```javascript
/**
 * @typedef {User & { permissions: string[] }} AuthenticatedUser
 */

/**
 * @param {string | number} id - Can be string or number
 * @returns {string}
 */
function normalizeId(id) {
  return String(id);
}

/**
 * @typedef {HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement} FormField
 */

/**
 * @param {FormField} field
 * @returns {string}
 */
function getFieldValue(field) {
  return field.value;
}
```

### Import Types from Other Files

Reference types defined elsewhere:

```javascript
/**
 * @typedef {import('./types.js').Config} Config
 * @typedef {import('./api.js').ApiResponse} ApiResponse
 */

/**
 * @param {Config} config - Configuration object
 * @returns {Promise<ApiResponse>}
 */
async function initialize(config) {
  // ...
}
```

### Function Types

Define callback signatures:

```javascript
/**
 * @typedef {(event: CustomEvent) => void} EventHandler
 * @typedef {(error: Error) => void} ErrorCallback
 * @typedef {(value: string, index: number) => boolean} FilterFn
 */

/**
 * @param {EventHandler} handler - Callback for update events
 */
function onUpdate(handler) {
  this.addEventListener('update', handler);
}

/**
 * @param {(item: User) => string} keyFn - Function to extract key
 * @returns {Map<string, User>}
 */
function indexUsers(keyFn) {
  return new Map(this.users.map(u => [keyFn(u), u]));
}
```

### Record/Dictionary Types

For objects with dynamic keys:

```javascript
/**
 * @typedef {Object<string, number>} ScoreMap
 * @typedef {Record<string, User>} UserIndex
 */

/**
 * @param {ScoreMap} scores - Map of player names to scores
 * @returns {number}
 */
function calculateAverage(scores) {
  const values = Object.values(scores);
  return values.reduce((a, b) => a + b, 0) / values.length;
}
```

### Type Guards

Narrow types with return type predicates:

```javascript
/**
 * @param {unknown} value
 * @returns {value is string}
 */
function isString(value) {
  return typeof value === 'string';
}

/**
 * @param {unknown} value
 * @returns {value is User}
 */
function isUser(value) {
  return value !== null &&
         typeof value === 'object' &&
         'id' in value &&
         'name' in value;
}
```

### Nullable and Optional

```javascript
/**
 * @param {?string} name - Can be null
 * @param {string} [title] - Optional parameter
 * @param {string} [prefix='Mr.'] - Optional with default
 * @returns {string}
 */
function greet(name, title, prefix = 'Mr.') {
  if (name === null) return 'Hello, guest!';
  return `Hello, ${prefix} ${title ? title + ' ' : ''}${name}`;
}
```

### Complex Object Shapes

Inline object types for one-off use:

```javascript
/**
 * @param {Array<{id: string, value: number, label?: string}>} items
 * @returns {{total: number, count: number, average: number}}
 */
function summarize(items) {
  const total = items.reduce((sum, item) => sum + item.value, 0);
  return {
    total,
    count: items.length,
    average: items.length ? total / items.length : 0
  };
}
```

### Enum-like Constants

Document constant objects with `@readonly` and `@enum`:

```javascript
/**
 * @readonly
 * @enum {string}
 */
const Status = {
  PENDING: 'pending',
  ACTIVE: 'active',
  COMPLETED: 'completed',
  CANCELLED: 'cancelled'
};

/**
 * @readonly
 * @enum {number}
 */
const Priority = {
  LOW: 0,
  MEDIUM: 1,
  HIGH: 2,
  CRITICAL: 3
};

/**
 * @param {Status} status - Current status
 * @param {Priority} [priority=Priority.MEDIUM] - Task priority
 */
function createTask(status, priority = Priority.MEDIUM) {
  // ...
}
```

### This Type in Classes

Document `this` type for method chaining:

```javascript
/**
 * @class QueryBuilder
 */
class QueryBuilder {
  /**
   * Add WHERE clause
   * @param {string} condition
   * @returns {this}
   */
  where(condition) {
    this.conditions.push(condition);
    return this;
  }

  /**
   * Add ORDER BY clause
   * @param {string} column
   * @param {'asc' | 'desc'} [direction='asc']
   * @returns {this}
   */
  orderBy(column, direction = 'asc') {
    this.ordering = { column, direction };
    return this;
  }
}
```

### Literal Types

Restrict values to specific literals:

```javascript
/**
 * @typedef {'small' | 'medium' | 'large'} Size
 * @typedef {'primary' | 'secondary' | 'danger' | 'success'} Variant
 */

/**
 * @param {Size} size - Button size
 * @param {Variant} variant - Button style variant
 */
function createButton(size, variant) {
  // ...
}
```

### Tuple Types

For fixed-length arrays:

```javascript
/**
 * @typedef {[number, number]} Point2D
 * @typedef {[number, number, number]} Point3D
 * @typedef {[string, number]} NamedValue
 */

/**
 * Calculate distance between points
 * @param {Point2D} a - First point
 * @param {Point2D} b - Second point
 * @returns {number}
 */
function distance(a, b) {
  return Math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2);
}
```

---

## Editor Support

To enable type checking in VS Code:

1. Add `// @ts-check` at the top of JavaScript files
2. Or create `jsconfig.json`:
   ```json
   {
     "compilerOptions": {
       "checkJs": true,
       "strict": true
     }
   }
   ```

This enables TypeScript's type inference on JSDoc-annotated JavaScript.
