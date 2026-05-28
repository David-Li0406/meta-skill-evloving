---
name: ts-docstring
description: |
  TSDoc documentation standards for TypeScript following tsdoc.org conventions.
  WHEN: Writing TSDoc comments, documenting TypeScript functions/classes/interfaces/types, generating docs with TypeDoc, improving existing TS documentation.
  WHEN NOT: JavaScript code (use js-docstring), Python (use python-docstring), PHP (use php-docstring), runtime logic without documentation needs.
---

# TypeScript TSDoc Standards

Comprehensive guide for writing high-quality TypeScript documentation using TSDoc following tsdoc.org standards.

## When to Use This Skill

- Writing TSDoc comments for TypeScript functions, classes, interfaces, and types
- Improving existing TypeScript documentation
- Generating API documentation with TypeDoc or API Extractor
- Documenting complex types and generics
- Leveraging TypeScript's type system with documentation

## TSDoc vs JSDoc

TSDoc is a standardized documentation format for TypeScript that:
- Works seamlessly with TypeScript's type system
- Provides stricter parsing rules than JSDoc
- Is designed for API documentation tools like TypeDoc and API Extractor
- Supports modern TypeScript features (generics, decorators, etc.)

**Key Difference**: With TypeScript, types are already defined in the code, so TSDoc focuses on _why_ and _how_, not _what type_.

## TSDoc Comment Structure

TSDoc comments use the same `/** */` syntax as JSDoc:

```typescript
/**
 * Brief description of the function.
 *
 * More detailed description providing additional context
 * about behavior, usage, or implementation details.
 *
 * @param paramName - Description of the parameter
 * @returns Description of the return value
 */
```

## Core TSDoc Tags

### @param - Parameter Documentation

```typescript
/**
 * Calculate the total price including tax.
 *
 * @param price - The base price before tax
 * @param taxRate - The tax rate as a decimal (e.g., 0.15 for 15%)
 * @param roundUp - Whether to round up the final amount (default: false)
 * @returns The total price including tax
 */
function calculateTotalPrice(
  price: number,
  taxRate: number,
  roundUp: boolean = false
): number {
  const total = price * (1 + taxRate);
  return roundUp ? Math.ceil(total) : total;
}
```

### @returns - Return Value

```typescript
/**
 * Find a user by their unique identifier.
 *
 * @param userId - The user's unique identifier
 * @returns The user object if found, undefined otherwise
 */
function findUser(userId: number): User | undefined {
  // Implementation
}

/**
 * Get all active users from the database.
 *
 * @returns Array of active user objects
 */
function getActiveUsers(): User[] {
  // Implementation
}

/**
 * Log a message to the console.
 *
 * @param message - The message to log
 */
function logMessage(message: string): void {
  console.log(message);
}
```

### @throws - Exception Documentation

```typescript
/**
 * Process a payment transaction.
 *
 * @param orderId - The order identifier
 * @param amount - The payment amount in dollars
 * @returns True if payment was successful
 *
 * @throws {@link ValidationError}
 * Thrown if the amount is negative or zero
 *
 * @throws {@link PaymentGatewayError}
 * Thrown if communication with the payment gateway fails
 */
function processPayment(orderId: number, amount: number): boolean {
  if (amount <= 0) {
    throw new ValidationError('Amount must be positive');
  }
  // Implementation
}
```

### @remarks - Additional Details

```typescript
/**
 * Fetch user data from the API.
 *
 * @param userId - The user ID to fetch
 * @returns Promise resolving to user data
 *
 * @remarks
 * This function implements retry logic with exponential backoff.
 * The maximum number of retries is 3, with delays of 1s, 2s, and 4s.
 *
 * Caching is enabled by default with a TTL of 5 minutes.
 */
async function fetchUser(userId: number): Promise<User> {
  // Implementation
}
```

### @example - Usage Examples

```typescript
/**
 * Validate an email address format.
 *
 * @param email - The email address to validate
 * @returns True if the email format is valid
 *
 * @example
 * Basic usage:
 * ```ts
 * const isValid = validateEmail('user@example.com');
 * console.log(isValid); // true
 * ```
 *
 * @example
 * Invalid email:
 * ```ts
 * const isValid = validateEmail('invalid.email');
 * console.log(isValid); // false
 * ```
 */
function validateEmail(email: string): boolean {
  const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return pattern.test(email);
}
```

## Complete Examples

### Function Documentation

```typescript
/**
 * Searches for items matching the specified criteria.
 *
 * @param query - The search query string
 * @param options - Search options
 * @returns Promise resolving to search results
 *
 * @remarks
 * This function performs a full-text search across all indexed fields.
 * Results are ranked by relevance score and returned in descending order.
 *
 * @example
 * Search with default options:
 * ```ts
 * const results = await search('typescript tutorial');
 * ```
 *
 * @example
 * Search with custom options:
 * ```ts
 * const results = await search('typescript', {
 *   limit: 10,
 *   includeArchived: false
 * });
 * ```
 */
async function search(
  query: string,
  options?: SearchOptions
): Promise<SearchResult[]> {
  // Implementation
}
```

### Interface Documentation

```typescript
/**
 * Configuration options for the application.
 *
 * @remarks
 * This interface defines all configurable settings for the application.
 * Settings can be loaded from environment variables or a configuration file.
 *
 * @example
 * ```ts
 * const config: AppConfig = {
 *   port: 3000,
 *   database: {
 *     host: 'localhost',
 *     port: 5432,
 *     name: 'myapp'
 *   },
 *   features: {
 *     enableCache: true
 *   }
 * };
 * ```
 */
interface AppConfig {
  /**
   * The port number the server will listen on.
   * @defaultValue 3000
   */
  port: number;

  /**
   * Database connection configuration.
   */
  database: DatabaseConfig;

  /**
   * Feature flags for enabling/disabling functionality.
   */
  features?: FeatureFlags;
}

/**
 * Database connection settings.
 */
interface DatabaseConfig {
  /** Database server hostname or IP address */
  host: string;

  /** Database server port number */
  port: number;

  /** Name of the database to connect to */
  name: string;

  /**
   * Optional connection pool size.
   * @defaultValue 10
   */
  poolSize?: number;
}
```

### Class Documentation

```typescript
/**
 * Manages user authentication and session handling.
 *
 * @remarks
 * This class provides comprehensive authentication services including:
 * - Username/password authentication
 * - Session management with automatic renewal
 * - Token-based authentication (JWT)
 * - Multi-factor authentication support
 *
 * Sessions are stored in Redis for scalability and persistence.
 *
 * @example
 * Creating and using the auth service:
 * ```ts
 * const authService = new AuthService(userRepo, sessionManager);
 *
 * // Authenticate user
 * const user = await authService.authenticate('john', 'password123');
 *
 * // Check authentication status
 * if (authService.isAuthenticated()) {
 *   console.log('User is logged in');
 * }
 * ```
 */
class AuthService {
  /**
   * Session timeout duration in seconds.
   */
  private static readonly SESSION_TIMEOUT = 3600;

  /**
   * Repository for user data access.
   */
  private readonly userRepository: UserRepository;

  /**
   * Manager for session operations.
   */
  private readonly sessionManager: SessionManager;

  /**
   * Creates a new authentication service instance.
   *
   * @param userRepository - Repository for accessing user data
   * @param sessionManager - Manager for handling user sessions
   */
  constructor(
    userRepository: UserRepository,
    sessionManager: SessionManager
  ) {
    this.userRepository = userRepository;
    this.sessionManager = sessionManager;
  }

  /**
   * Authenticates a user with username and password.
   *
   * @param username - The user's username or email
   * @param password - The user's password (plain text)
   * @returns Promise resolving to the authenticated user
   *
   * @throws {@link AuthenticationError}
   * Thrown if the credentials are invalid
   *
   * @throws {@link AccountLockedException}
   * Thrown if the account is locked due to too many failed attempts
   *
   * @remarks
   * Passwords are automatically hashed using bcrypt before comparison.
   * Failed login attempts are tracked and the account is locked after
   * 5 consecutive failures.
   */
  async authenticate(username: string, password: string): Promise<User> {
    // Implementation
  }

  /**
   * Logs out the currently authenticated user.
   *
   * @remarks
   * This destroys the user's session and invalidates all tokens.
   */
  logout(): void {
    this.sessionManager.destroy();
  }

  /**
   * Checks if a user is currently authenticated.
   *
   * @returns True if the user has a valid session
   */
  isAuthenticated(): boolean {
    return this.sessionManager.isValid();
  }
}
```

### Generic Types

```typescript
/**
 * A generic collection that stores items of type T.
 *
 * @typeParam T - The type of items stored in the collection
 *
 * @remarks
 * This collection provides type-safe storage and retrieval of items.
 * Items can be added, removed, and accessed by index.
 *
 * @example
 * Using with a specific type:
 * ```ts
 * const users = new Collection<User>();
 * users.add(new User('John'));
 * const first = users.get(0);
 * ```
 */
class Collection<T> {
  /**
   * Internal storage for collection items.
   */
  private items: T[] = [];

  /**
   * Adds an item to the collection.
   *
   * @param item - The item to add
   */
  add(item: T): void {
    this.items.push(item);
  }

  /**
   * Retrieves an item by index.
   *
   * @param index - The zero-based index of the item
   * @returns The item at the specified index, or undefined if not found
   */
  get(index: number): T | undefined {
    return this.items[index];
  }

  /**
   * Returns all items in the collection.
   *
   * @returns Array of all items
   */
  all(): T[] {
    return [...this.items];
  }

  /**
   * Gets the number of items in the collection.
   */
  get size(): number {
    return this.items.length;
  }
}
```

### Type Aliases

```typescript
/**
 * Represents a user identifier.
 *
 * @remarks
 * User IDs can be either numeric (database ID) or string (UUID).
 */
type UserId = number | string;

/**
 * HTTP request methods.
 */
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

/**
 * Callback function for event handlers.
 *
 * @param event - The event object
 * @returns Optional return value from the handler
 */
type EventHandler<T> = (event: T) => void | Promise<void>;

/**
 * Makes all properties of T optional and nullable.
 *
 * @typeParam T - The type to make partial and nullable
 *
 * @example
 * ```ts
 * type User = { id: number; name: string };
 * type PartialUser = Nullable<Partial<User>>;
 * // Result: { id?: number | null; name?: string | null }
 * ```
 */
type Nullable<T> = {
  [P in keyof T]?: T[P] | null;
};
```

### Enums

```typescript
/**
 * User account status values.
 *
 * @remarks
 * These statuses represent the lifecycle states of a user account.
 */
enum UserStatus {
  /**
   * Account is active and can be used normally.
   */
  Active = 'active',

  /**
   * Account is temporarily suspended.
   */
  Suspended = 'suspended',

  /**
   * Account is pending email verification.
   */
  Pending = 'pending',

  /**
   * Account has been permanently deleted.
   */
  Deleted = 'deleted'
}
```

## Advanced TSDoc Tags

### @deprecated

```typescript
/**
 * Calculate discount using the legacy algorithm.
 *
 * @param price - The original price
 * @returns The discounted price
 *
 * @deprecated Use {@link calculateDiscountV2} instead.
 * This method will be removed in version 3.0.0.
 */
function calculateDiscount(price: number): number {
  // Old implementation
}
```

### @see - Cross References

```typescript
/**
 * Authenticate a user.
 *
 * @param username - The username
 * @param password - The password
 * @returns The authenticated user
 *
 * @see {@link SessionManager} for session handling
 * @see {@link https://example.com/docs/auth | Authentication Documentation}
 */
async function authenticate(username: string, password: string): Promise<User> {
  // Implementation
}
```

### @internal - Internal APIs

```typescript
/**
 * Validates internal cache consistency.
 *
 * @internal
 * This method is for internal use only and may change without notice.
 *
 * @returns True if cache is consistent
 */
function validateCache(): boolean {
  // Internal implementation
}
```

### @beta - Beta APIs

```typescript
/**
 * Experimental feature for real-time collaboration.
 *
 * @beta
 * This API is experimental and may change in future releases.
 *
 * @param documentId - The document to collaborate on
 * @returns Collaboration session
 */
function startCollaboration(documentId: string): CollaborationSession {
  // Beta implementation
}
```

### @public, @private, @protected

```typescript
class UserService {
  /**
   * Validates user input data.
   *
   * @private
   * @param data - The data to validate
   * @returns True if valid
   */
  private validateInput(data: unknown): boolean {
    // Implementation
  }

  /**
   * Processes user data after validation.
   *
   * @protected
   * @param user - The user to process
   */
  protected processUser(user: User): void {
    // Implementation
  }

  /**
   * Creates a new user account.
   *
   * @public
   * @param username - The desired username
   * @returns Promise resolving to the created user
   */
  public async createUser(username: string): Promise<User> {
    // Implementation
  }
}
```

## React/TypeScript Documentation

### React Component Props

```typescript
/**
 * Props for the UserCard component.
 */
interface UserCardProps {
  /**
   * The user object to display.
   */
  user: User;

  /**
   * Whether to show the user's email address.
   * @defaultValue true
   */
  showEmail?: boolean;

  /**
   * Callback invoked when the edit button is clicked.
   */
  onEdit?: (user: User) => void;

  /**
   * Additional CSS classes to apply.
   */
  className?: string;
}

/**
 * Displays user information in a card format.
 *
 * @param props - Component props
 * @returns The rendered component
 *
 * @remarks
 * This component provides a consistent UI for displaying user profiles
 * throughout the application.
 *
 * @example
 * Basic usage:
 * ```tsx
 * <UserCard user={user} onEdit={handleEdit} />
 * ```
 */
function UserCard({ user, showEmail = true, onEdit, className }: UserCardProps) {
  return (
    <div className={className}>
      <h2>{user.name}</h2>
      {showEmail && <p>{user.email}</p>}
      {onEdit && <button onClick={() => onEdit(user)}>Edit</button>}
    </div>
  );
}
```

### Custom Hooks

```typescript
/**
 * Return type for the useUser hook.
 */
interface UseUserResult {
  /** The fetched user data, or null if not yet loaded */
  user: User | null;

  /** Whether the data is currently being fetched */
  loading: boolean;

  /** Error object if the fetch failed */
  error: Error | null;

  /** Function to refetch the user data */
  refetch: () => void;
}

/**
 * Custom hook for fetching and managing user data.
 *
 * @param userId - The ID of the user to fetch
 * @returns Object containing user data, loading state, and error
 *
 * @remarks
 * This hook automatically fetches user data when the component mounts
 * and re-fetches when the userId changes. It includes automatic error
 * handling and retry logic.
 *
 * @example
 * ```tsx
 * function UserProfile({ userId }: { userId: number }) {
 *   const { user, loading, error } = useUser(userId);
 *
 *   if (loading) return <Spinner />;
 *   if (error) return <ErrorMessage error={error} />;
 *   if (!user) return null;
 *
 *   return <div>{user.name}</div>;
 * }
 * ```
 */
function useUser(userId: number): UseUserResult {
  // Implementation
}
```

## Decorators

```typescript
/**
 * Logs method execution time to the console.
 *
 * @remarks
 * This decorator wraps the method and logs the execution duration
 * whenever the method is called.
 *
 * @example
 * ```ts
 * class Service {
 *   @logTime
 *   async fetchData() {
 *     // Implementation
 *   }
 * }
 * ```
 */
function logTime(
  target: any,
  propertyKey: string,
  descriptor: PropertyDescriptor
) {
  // Implementation
}
```

## Best Practices

### DO

- Leverage TypeScript's type system - let types speak for themselves
- Focus documentation on _why_ and _how_, not _what type_
- Use `@remarks` for detailed implementation notes
- Include `@example` tags for complex APIs
- Document exceptions with `@throws`
- Use `@defaultValue` for optional parameters with defaults
- Cross-reference related APIs with `@see`
- Provide complete examples in code blocks

### DON'T

- Don't repeat type information already in the signature
- Don't document every single parameter if types are self-explanatory
- Don't forget to update docs when implementation changes
- Don't use JSDoc tags that aren't part of TSDoc standard
- Don't document private implementation details in public APIs
- Don't omit documentation for exported APIs

## Type Information in Comments

Since TypeScript has type declarations, avoid redundancy:

```typescript
// ❌ Bad: Redundant type information
/**
 * Add two numbers.
 *
 * @param a - The first number (number)
 * @param b - The second number (number)
 * @returns The sum (number)
 */
function add(a: number, b: number): number {
  return a + b;
}

// ✅ Good: Focus on purpose, not types
/**
 * Add two numbers.
 *
 * @param a - First addend
 * @param b - Second addend
 * @returns Sum of a and b
 */
function add(a: number, b: number): number {
  return a + b;
}

// ✅ Better: Only document when adding value
/**
 * Add two numbers with overflow checking.
 *
 * @remarks
 * Throws an error if the result would exceed Number.MAX_SAFE_INTEGER.
 */
function add(a: number, b: number): number {
  const result = a + b;
  if (result > Number.MAX_SAFE_INTEGER) {
    throw new Error('Overflow detected');
  }
  return result;
}
```

## Generating Documentation

### Using TypeDoc

```bash
# Install TypeDoc
npm install --save-dev typedoc

# Generate documentation
npx typedoc src/

# With custom options
npx typedoc --out docs --exclude "**/*+(test|spec).ts" src/
```

### TypeDoc Configuration (typedoc.json)

```json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs",
  "exclude": ["**/*+(test|spec).ts", "node_modules"],
  "excludePrivate": true,
  "excludeProtected": false,
  "excludeExternals": true,
  "includeVersion": true,
  "readme": "README.md",
  "plugin": ["typedoc-plugin-markdown"]
}
```

### Using API Extractor

```bash
# Install API Extractor
npm install --save-dev @microsoft/api-extractor

# Initialize configuration
npx api-extractor init

# Run extraction
npx api-extractor run
```

## Quick Reference

### Function Template

```typescript
/**
 * Brief description.
 *
 * @param param1 - Description
 * @param param2 - Description
 * @returns Description
 *
 * @throws {ErrorType} When this happens
 *
 * @example
 * ```ts
 * functionName(value1, value2);
 * ```
 */
function functionName(param1: Type1, param2: Type2): ReturnType {
  // Implementation
}
```

### Interface Template

```typescript
/**
 * Interface description.
 *
 * @remarks
 * Additional details about usage.
 */
interface InterfaceName {
  /**
   * Property description.
   * @defaultValue value
   */
  property: Type;
}
```

### Class Template

```typescript
/**
 * Class description.
 *
 * @remarks
 * Detailed information about the class.
 *
 * @example
 * ```ts
 * const instance = new ClassName();
 * ```
 */
class ClassName {
  /**
   * Constructor description.
   *
   * @param param - Description
   */
  constructor(param: Type) {
    // Implementation
  }

  /**
   * Method description.
   *
   * @param param - Description
   * @returns Description
   */
  methodName(param: Type): ReturnType {
    // Implementation
  }
}
```

## Resources

- **TSDoc Official**: https://tsdoc.org/
- **TSDoc Playground**: https://tsdoc.org/play
- **TypeDoc**: https://typedoc.org/
- **API Extractor**: https://api-extractor.com/
- **TypeScript Handbook**: Documentation best practices
- **Microsoft TSDoc**: Official Microsoft implementation
