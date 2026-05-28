---
name: js-docstring
description: |
  JSDoc documentation standards for JavaScript following jsdoc.app conventions.
  WHEN: Writing JSDoc comments, documenting JavaScript functions/classes/modules, generating API docs with JSDoc, improving existing JS documentation.
  WHEN NOT: TypeScript code (use ts-docstring), Python (use python-docstring), PHP (use php-docstring), runtime logic without documentation needs.
---

# JavaScript JSDoc Standards

Comprehensive guide for writing high-quality JavaScript documentation using JSDoc following jsdoc.app standards.

## When to Use This Skill

- Writing JSDoc comments for JavaScript functions, classes, and modules
- Improving existing JavaScript documentation
- Generating API documentation with JSDoc
- Documenting parameters, return values, types, and exceptions
- Supporting IDE autocomplete and type checking

## JSDoc Comment Structure

JSDoc comments begin with `/**` and end with `*/`. Each line typically starts with an asterisk.

### Basic Structure

```javascript
/**
 * Brief description of the function.
 *
 * Longer description providing more details about the
 * function's purpose and behavior.
 *
 * @param {type} paramName - Description of parameter
 * @returns {type} Description of return value
 */
```

## Common JSDoc Tags

### @param - Parameter Documentation

```javascript
/**
 * Calculate the total price including tax.
 *
 * @param {number} price - The base price before tax
 * @param {number} taxRate - The tax rate (e.g., 0.15 for 15%)
 * @param {boolean} [roundUp=false] - Whether to round up (optional)
 * @returns {number} The total price including tax
 */
function calculateTotalPrice(price, taxRate, roundUp = false) {
  const total = price * (1 + taxRate);
  return roundUp ? Math.ceil(total) : total;
}
```

### @returns or @return - Return Value

```javascript
/**
 * Find a user by ID.
 *
 * @param {number} userId - The user's unique identifier
 * @returns {User|null} The user object if found, null otherwise
 */
function findUser(userId) {
  // Implementation
}

/**
 * Get all active users.
 *
 * @returns {User[]} Array of user objects
 */
function getActiveUsers() {
  // Implementation
}

/**
 * Log a message (no return value).
 *
 * @param {string} message - The message to log
 * @returns {void}
 */
function logMessage(message) {
  console.log(message);
}
```

### @throws - Exception Documentation

```javascript
/**
 * Process a payment transaction.
 *
 * @param {number} orderId - The order identifier
 * @param {number} amount - The payment amount
 * @returns {boolean} True if payment successful
 * @throws {Error} If amount is negative or zero
 * @throws {PaymentError} If payment gateway communication fails
 */
function processPayment(orderId, amount) {
  if (amount <= 0) {
    throw new Error('Amount must be positive');
  }
  // Implementation
}
```

### @type - Variable Type

```javascript
/**
 * @type {string}
 */
let userName;

/**
 * @type {number[]}
 */
const scores = [95, 87, 92];

/**
 * @type {Object.<string, number>}
 */
const userAges = {
  john: 25,
  jane: 30
};

/**
 * @type {{ name: string, age: number, email: string }}
 */
const user = {
  name: 'John',
  age: 25,
  email: 'john@example.com'
};
```

### @typedef - Custom Type Definitions

```javascript
/**
 * User object type definition.
 *
 * @typedef {Object} User
 * @property {number} id - User's unique identifier
 * @property {string} username - User's username
 * @property {string} email - User's email address
 * @property {Date} createdAt - Account creation date
 */

/**
 * Create a new user.
 *
 * @param {string} username - The username
 * @param {string} email - The email address
 * @returns {User} The created user object
 */
function createUser(username, email) {
  return {
    id: generateId(),
    username,
    email,
    createdAt: new Date()
  };
}
```

### @callback - Callback Function Type

```javascript
/**
 * Callback for processing items.
 *
 * @callback ItemProcessor
 * @param {*} item - The item to process
 * @param {number} index - The item's index
 * @returns {*} The processed item
 */

/**
 * Process each item in an array.
 *
 * @param {Array} items - Array of items to process
 * @param {ItemProcessor} processor - Callback to process each item
 * @returns {Array} Array of processed items
 */
function processItems(items, processor) {
  return items.map(processor);
}
```

## Complete Examples

### Function Documentation

```javascript
/**
 * Validate and sanitize user input.
 *
 * Performs comprehensive validation and sanitization of user input
 * to prevent XSS and injection attacks.
 *
 * @param {string} input - The raw user input to validate
 * @param {('email'|'url'|'text')} type - The expected input type
 * @param {number} [maxLength=255] - Maximum allowed length
 * @returns {string} The sanitized input
 * @throws {TypeError} If input type is not supported
 * @throws {ValidationError} If input fails validation
 *
 * @example
 * const clean = validateInput(userInput, 'email');
 *
 * @example
 * const clean = validateInput(userInput, 'text', 100);
 */
function validateInput(input, type, maxLength = 255) {
  // Implementation
}
```

### Class Documentation

```javascript
/**
 * Manages user authentication and sessions.
 *
 * Provides methods for user login, logout, session validation,
 * and token-based authentication.
 *
 * @class
 * @classdesc Handles all authentication-related operations
 *
 * @example
 * const auth = new AuthService(userRepo, sessionManager);
 * const user = await auth.authenticate('john', 'password123');
 */
class AuthService {
  /**
   * Session timeout in seconds.
   *
   * @type {number}
   * @static
   * @readonly
   */
  static SESSION_TIMEOUT = 3600;

  /**
   * Create an authentication service instance.
   *
   * @param {UserRepository} userRepository - Repository for user data
   * @param {SessionManager} sessionManager - Manager for user sessions
   */
  constructor(userRepository, sessionManager) {
    /**
     * @type {UserRepository}
     * @private
     */
    this.userRepository = userRepository;

    /**
     * @type {SessionManager}
     * @private
     */
    this.sessionManager = sessionManager;
  }

  /**
   * Authenticate a user with credentials.
   *
   * Validates credentials against the database and creates a session
   * on successful authentication.
   *
   * @param {string} username - The user's username or email
   * @param {string} password - The user's password
   * @returns {Promise<User>} The authenticated user object
   * @throws {AuthenticationError} If credentials are invalid
   * @throws {AccountLockedException} If account is locked
   *
   * @async
   */
  async authenticate(username, password) {
    // Implementation
  }

  /**
   * Log out the current user.
   *
   * @returns {void}
   */
  logout() {
    this.sessionManager.destroy();
  }

  /**
   * Check if user is authenticated.
   *
   * @returns {boolean} True if user has valid session
   */
  isAuthenticated() {
    return this.sessionManager.isValid();
  }
}
```

### ES6 Module Documentation

```javascript
/**
 * User management module.
 *
 * Provides utilities for user authentication, authorization,
 * and profile management.
 *
 * @module users
 * @author John Doe <john@example.com>
 * @version 1.2.0
 * @since 1.0.0
 */

/**
 * Default user role.
 *
 * @constant {string}
 * @default
 */
export const DEFAULT_ROLE = 'user';

/**
 * Maximum login attempts.
 *
 * @constant {number}
 * @default
 */
export const MAX_LOGIN_ATTEMPTS = 5;

/**
 * User validation schema.
 *
 * @type {Object}
 * @property {Object} username - Username validation rules
 * @property {number} username.minLength - Minimum username length
 * @property {number} username.maxLength - Maximum username length
 */
export const userSchema = {
  username: {
    minLength: 3,
    maxLength: 20
  }
};
```

### Async/Promise Documentation

```javascript
/**
 * Fetch user data from the API.
 *
 * Makes an HTTP request to retrieve user information.
 * Implements retry logic with exponential backoff.
 *
 * @async
 * @param {number} userId - The user ID to fetch
 * @param {Object} [options] - Request options
 * @param {number} [options.timeout=30000] - Request timeout in ms
 * @param {boolean} [options.includeProfile=false] - Include full profile
 * @returns {Promise<User>} Resolves with user data
 * @throws {TimeoutError} If request exceeds timeout
 * @throws {NotFoundError} If user doesn't exist
 *
 * @example
 * const user = await fetchUser(123);
 *
 * @example
 * const user = await fetchUser(123, { includeProfile: true });
 */
async function fetchUser(userId, options = {}) {
  // Implementation
}

/**
 * Load user preferences.
 *
 * @param {number} userId - The user ID
 * @returns {Promise<Object>} Promise resolving to user preferences
 */
function loadPreferences(userId) {
  return new Promise((resolve, reject) => {
    // Implementation
  });
}
```

### Generator Function Documentation

```javascript
/**
 * Generate Fibonacci sequence.
 *
 * @generator
 * @param {number} n - Number of Fibonacci numbers to generate
 * @yields {number} Next number in the Fibonacci sequence
 *
 * @example
 * const fib = fibonacci(5);
 * console.log([...fib]); // [0, 1, 1, 2, 3]
 */
function* fibonacci(n) {
  let a = 0, b = 1;
  for (let i = 0; i < n; i++) {
    yield a;
    [a, b] = [b, a + b];
  }
}
```

## Advanced Type Syntax

### Union Types

```javascript
/**
 * Format a value for display.
 *
 * @param {string|number|boolean} value - The value to format
 * @returns {string} The formatted value
 */
function formatValue(value) {
  return String(value);
}
```

### Array Types

```javascript
/**
 * Process user list.
 *
 * @param {User[]} users - Array of user objects
 * @param {number[]} ids - Array of user IDs
 * @param {Array<string|number>} mixed - Mixed type array
 * @returns {void}
 */
function processUsers(users, ids, mixed) {
  // Implementation
}
```

### Object Types

```javascript
/**
 * Update user settings.
 *
 * @param {Object} settings - User settings
 * @param {string} settings.theme - UI theme preference
 * @param {boolean} settings.notifications - Enable notifications
 * @param {number} settings.fontSize - Font size in pixels
 * @returns {void}
 */
function updateSettings(settings) {
  // Implementation
}

/**
 * Get user scores.
 *
 * @returns {Object.<string, number>} Object mapping user IDs to scores
 */
function getUserScores() {
  return { user1: 95, user2: 87 };
}
```

### Nullable and Optional Types

```javascript
/**
 * Find user by email.
 *
 * @param {string} email - Email to search for
 * @returns {?User} User object or null if not found
 */
function findByEmail(email) {
  // Implementation
}

/**
 * Create configuration.
 *
 * @param {Object} options - Configuration options
 * @param {string} options.name - Required name
 * @param {number} [options.port] - Optional port number
 * @param {string} [options.host='localhost'] - Optional host with default
 * @returns {Object} Configuration object
 */
function createConfig(options) {
  // Implementation
}
```

### Generic Types

```javascript
/**
 * Generic collection class.
 *
 * @template T
 */
class Collection {
  /**
   * @type {T[]}
   * @private
   */
  items = [];

  /**
   * Add an item to the collection.
   *
   * @param {T} item - The item to add
   * @returns {void}
   */
  add(item) {
    this.items.push(item);
  }

  /**
   * Get all items.
   *
   * @returns {T[]} All items in the collection
   */
  all() {
    return this.items;
  }
}
```

## Special Tags

### @deprecated

```javascript
/**
 * Calculate discount using old method.
 *
 * @deprecated Since version 2.0.0. Use calculateDiscountV2() instead.
 * @param {number} price - The original price
 * @returns {number} The discounted price
 */
function calculateDiscount(price) {
  // Old implementation
}
```

### @see and @link

```javascript
/**
 * Authenticate user.
 *
 * @param {string} username - Username
 * @param {string} password - Password
 * @returns {Promise<User>} Authenticated user
 *
 * @see {@link SessionManager} for session handling
 * @see https://example.com/docs/auth for authentication docs
 */
async function authenticate(username, password) {
  // Implementation
}
```

### @todo

```javascript
/**
 * Send notification to user.
 *
 * @param {User} user - The user to notify
 * @param {string} message - Notification message
 * @returns {void}
 *
 * @todo Add support for email notifications
 * @todo Implement notification preferences
 */
function sendNotification(user, message) {
  // Current implementation
}
```

### @private, @protected, @public

```javascript
class UserService {
  /**
   * Validate user input.
   *
   * @private
   * @param {Object} data - Data to validate
   * @returns {boolean} True if valid
   */
  _validateInput(data) {
    // Internal validation
  }

  /**
   * Process user data.
   *
   * @protected
   * @param {User} user - User to process
   * @returns {void}
   */
  _processUser(user) {
    // Protected method
  }

  /**
   * Create a new user.
   *
   * @public
   * @param {string} username - Username
   * @returns {Promise<User>} Created user
   */
  async createUser(username) {
    // Public method
  }
}
```

## React/JSX Documentation

### React Component

```javascript
/**
 * User profile card component.
 *
 * Displays user information in a card format with avatar,
 * name, and email.
 *
 * @component
 *
 * @param {Object} props - Component props
 * @param {User} props.user - User object to display
 * @param {boolean} [props.showEmail=true] - Whether to show email
 * @param {Function} [props.onEdit] - Callback when edit button clicked
 *
 * @returns {React.ReactElement} The rendered component
 *
 * @example
 * <UserCard user={user} onEdit={handleEdit} />
 */
function UserCard({ user, showEmail = true, onEdit }) {
  return (
    <div className="user-card">
      <h2>{user.name}</h2>
      {showEmail && <p>{user.email}</p>}
      {onEdit && <button onClick={onEdit}>Edit</button>}
    </div>
  );
}
```

### React Hook

```javascript
/**
 * Custom hook for fetching user data.
 *
 * @param {number} userId - The user ID to fetch
 * @returns {Object} Hook return value
 * @returns {User|null} returns.user - The fetched user or null
 * @returns {boolean} returns.loading - Loading state
 * @returns {Error|null} returns.error - Error if fetch failed
 *
 * @example
 * const { user, loading, error } = useUser(123);
 */
function useUser(userId) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Implementation

  return { user, loading, error };
}
```

## Node.js Specific

### Module Exports

```javascript
/**
 * Database connection module.
 *
 * @module database
 */

/**
 * Connect to database.
 *
 * @param {string} connectionString - Database connection string
 * @returns {Promise<Connection>} Database connection
 */
exports.connect = async function(connectionString) {
  // Implementation
};

/**
 * Close database connection.
 *
 * @returns {Promise<void>}
 */
exports.disconnect = async function() {
  // Implementation
};
```

## Best Practices

### DO

- Always include a description for functions and classes
- Document all parameters and return values
- Use type annotations for better IDE support
- Include examples for complex functions
- Document thrown exceptions
- Keep comments concise and meaningful
- Use @example tags to show usage

### DON'T

- Don't document obvious things excessively
- Don't forget to update JSDoc when code changes
- Don't use JSDoc for inline code comments
- Don't repeat information that's obvious from code
- Don't omit parameter descriptions
- Don't forget optional parameter syntax `[param]`

## Generating Documentation

```bash
# Install JSDoc
npm install --save-dev jsdoc

# Generate documentation
npx jsdoc src/ -d docs/

# With configuration file
npx jsdoc -c jsdoc.json

# Generate with README
npx jsdoc src/ -R README.md -d docs/
```

### JSDoc Configuration (jsdoc.json)

```json
{
  "source": {
    "include": ["src"],
    "includePattern": ".+\\.js(doc|x)?$",
    "excludePattern": "(node_modules/|docs)"
  },
  "opts": {
    "destination": "./docs",
    "recurse": true,
    "template": "default"
  },
  "plugins": ["plugins/markdown"]
}
```

## Type Checking with JSDoc

JSDoc can be used for type checking with TypeScript compiler:

```javascript
// @ts-check

/**
 * Add two numbers.
 *
 * @param {number} a - First number
 * @param {number} b - Second number
 * @returns {number} Sum of a and b
 */
function add(a, b) {
  return a + b;
}

add(1, 2);     // OK
add('1', '2'); // Error: Type checking enabled
```

## Quick Reference

### Function Template

```javascript
/**
 * Brief description.
 *
 * @param {type} param1 - Description
 * @param {type} [param2] - Optional parameter
 * @returns {type} Description
 * @throws {ErrorType} When error occurs
 *
 * @example
 * functionName(value1, value2);
 */
function functionName(param1, param2) {
  // Implementation
}
```

### Class Template

```javascript
/**
 * Class description.
 *
 * @class
 */
class ClassName {
  /**
   * Constructor description.
   *
   * @param {type} param - Description
   */
  constructor(param) {
    /** @type {type} */
    this.property = param;
  }

  /**
   * Method description.
   *
   * @param {type} param - Description
   * @returns {type} Description
   */
  methodName(param) {
    // Implementation
  }
}
```

## Resources

- **JSDoc Official**: https://jsdoc.app/
- **Type Expressions**: https://jsdoc.app/tags-type.html
- **Google JavaScript Style Guide**: Includes JSDoc conventions
- **TypeScript JSDoc**: Use JSDoc with TypeScript
- **Better Docs**: Enhanced JSDoc template
