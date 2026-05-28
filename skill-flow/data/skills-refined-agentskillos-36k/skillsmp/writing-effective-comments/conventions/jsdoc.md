# JSDoc (JavaScript/TypeScript)

Documentation convention for JavaScript and TypeScript codebases.

## Overview

JSDoc uses specially formatted comments to document code. Comments begin with `/**` and support tags prefixed with `@`. TypeScript can also infer types from JSDoc annotations.

## Basic Syntax

```javascript
/**
 * Brief description of what this function does.
 *
 * Longer description if needed, explaining behavior,
 * constraints, or usage patterns.
 *
 * @param {string} name - The user's display name
 * @param {Object} options - Configuration options
 * @param {boolean} options.notify - Whether to send notification
 * @returns {Promise<User>} The created user object
 * @throws {ValidationError} If name is empty or invalid
 *
 * @example
 * const user = await createUser('Alice', { notify: true });
 */
function createUser(name, options) {
  // ...
}
```

## Common Tags

| Tag | Purpose | Example |
|-----|---------|---------|
| `@param` | Document a parameter | `@param {string} id - User identifier` |
| `@returns` | Document return value | `@returns {boolean} True if valid` |
| `@throws` | Document exceptions | `@throws {Error} If connection fails` |
| `@example` | Show usage example | `@example\nconst x = fn();` |
| `@async` | Mark async function | `@async` |
| `@deprecated` | Mark as deprecated | `@deprecated Use newFn() instead` |
| `@see` | Reference related code | `@see OtherClass` |
| `@since` | Version introduced | `@since 2.0.0` |
| `@private` | Mark as private | `@private` |
| `@typedef` | Define custom type | `@typedef {Object} Config` |

## Applying Core Principles

### Don't Repeat Types Already in TypeScript

```typescript
// Bad: Redundant with TypeScript types
/**
 * @param {string} name - The name
 * @param {number} age - The age
 * @returns {User}
 */
function createUser(name: string, age: number): User

// Good: Add meaning, not type info
/**
 * Create a new user account with default permissions.
 *
 * @param name - Display name shown in UI (max 50 chars)
 * @param age - Used for age-restricted content filtering
 * @returns Newly created user with pending verification status
 */
function createUser(name: string, age: number): User
```

### Use Different Vocabulary

```javascript
// Bad: Restates the function name
/**
 * Send a notification to a user.
 * @param userId - The user ID
 * @param message - The message
 */
function sendNotification(userId, message)

// Good: Explains the abstraction
/**
 * Queue an in-app alert for the user's next session.
 *
 * Notifications are batched and delivered when the user
 * returns to the app. For immediate delivery, use pushNotification().
 *
 * @param userId - Target user's account identifier
 * @param message - Alert content (supports markdown, max 500 chars)
 */
function sendNotification(userId, message)
```

### Document Non-Obvious Behavior

```javascript
/**
 * Fetch user's recent orders with pagination.
 *
 * Results are cached for 60 seconds. Stale orders may appear
 * briefly after new orders are placed.
 *
 * @param userId - Account to fetch orders for
 * @param options - Pagination and filtering options
 * @param options.limit - Max orders to return (default: 20, max: 100)
 * @param options.status - Filter by order status (default: all)
 * @returns Orders sorted by date descending, empty array if none
 *
 * @example
 * // Get pending orders only
 * const orders = await getOrders(userId, { status: 'pending' });
 */
async function getOrders(userId, options = {}) {
  // ...
}
```

## Class Documentation

```javascript
/**
 * Manages WebSocket connection with automatic reconnection.
 *
 * Handles connection lifecycle, message queuing during disconnects,
 * and exponential backoff for reconnection attempts.
 *
 * @example
 * const socket = new ReconnectingSocket('wss://api.example.com');
 * socket.on('message', (data) => console.log(data));
 * socket.send({ type: 'subscribe', channel: 'updates' });
 */
class ReconnectingSocket {
  /**
   * Create a new reconnecting WebSocket.
   *
   * @param {string} url - WebSocket server URL
   * @param {Object} options - Connection options
   * @param {number} options.maxRetries - Max reconnection attempts (default: 10)
   * @param {number} options.baseDelay - Initial retry delay in ms (default: 1000)
   */
  constructor(url, options = {}) {
    // ...
  }

  /**
   * Send a message, queuing if currently disconnected.
   *
   * @param {Object} data - Message payload (will be JSON serialized)
   * @returns {boolean} True if sent immediately, false if queued
   */
  send(data) {
    // ...
  }
}
```

## Module Documentation

```javascript
/**
 * @module authentication
 *
 * User authentication and session management.
 *
 * Supports OAuth 2.0, SAML, and username/password authentication.
 * Sessions are stored in Redis with configurable TTL.
 *
 * @example
 * import { authenticate, validateSession } from './auth';
 *
 * const session = await authenticate(credentials);
 * const isValid = await validateSession(session.token);
 */
```

## TypeScript-Specific Patterns

### Documenting Generics

```typescript
/**
 * Transform array elements while preserving order.
 *
 * @typeParam T - Input element type
 * @typeParam U - Output element type
 * @param items - Source array to transform
 * @param transform - Function applied to each element
 * @returns New array with transformed elements
 */
function map<T, U>(items: T[], transform: (item: T) => U): U[] {
  // ...
}
```

### Documenting Interfaces

```typescript
/**
 * Configuration for API client initialization.
 *
 * All timeouts are in milliseconds.
 */
interface ApiConfig {
  /** Base URL for all API requests */
  baseUrl: string;

  /** Request timeout (default: 30000) */
  timeout?: number;

  /**
   * Retry configuration for failed requests.
   * Set to null to disable retries.
   */
  retry?: RetryConfig | null;
}
```

## Tools and IDE Integration

- **VS Code**: Built-in JSDoc support with IntelliSense
- **TypeScript**: Extracts types from JSDoc in `.js` files
- **ESLint**: `eslint-plugin-jsdoc` for validation
- **Documentation generators**: TypeDoc, JSDoc, documentation.js
