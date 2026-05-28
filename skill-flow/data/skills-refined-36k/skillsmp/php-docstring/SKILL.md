---
name: php-docstring
description: |
  Write PHP DocBlocks following PSR-5 and PSR-19 PHPDoc standards.
  WHEN: Writing DocBlocks for PHP classes/methods/functions/properties, documenting @param/@return/@throws, type annotations in PHPDoc.
  WHEN NOT: Python docstrings (use python-docstring), JavaScript (use js-docstring), TypeScript (use ts-docstring).
---

# PHP DocBlock Standards

Comprehensive guide for writing high-quality PHP DocBlocks following PSR-5 (PHPDoc) and PSR-19 (PHPDoc tags) standards.

## When to Use This Skill

- Writing DocBlocks for PHP classes, methods, functions, and properties
- Improving existing PHP documentation
- Generating API documentation with phpDocumentor
- Following PSR standards for DocBlocks
- Documenting parameters, return types, exceptions, and type information

## DocBlock Structure

A DocBlock is a special comment block that starts with `/**` and provides documentation.

### Basic Structure

```php
/**
 * Summary line (short description).
 *
 * Detailed description providing more information about the element.
 * Can span multiple lines and paragraphs.
 *
 * @tag-name Description of the tag
 */
```

### Key Components

1. **Summary**: One-line description (required)
2. **Description**: Detailed explanation (optional)
3. **Tags**: Metadata annotations with `@` prefix (optional)

## Common PHPDoc Tags

### @param - Parameter Documentation

```php
/**
 * Calculate the total price with tax.
 *
 * @param float $price The base price before tax
 * @param float $taxRate The tax rate as a decimal (e.g., 0.15 for 15%)
 * @param bool $roundUp Whether to round up the final amount
 *
 * @return float The total price including tax
 */
function calculateTotalPrice(float $price, float $taxRate, bool $roundUp = false): float
{
    $total = $price * (1 + $taxRate);
    return $roundUp ? ceil($total) : $total;
}
```

### @return - Return Value Documentation

```php
/**
 * Fetch user by ID from the database.
 *
 * @param int $userId The user's unique identifier
 *
 * @return User|null The user object if found, null otherwise
 */
function findUser(int $userId): ?User
{
    // Implementation
}

/**
 * Get all active users.
 *
 * @return User[] Array of user objects
 */
function getActiveUsers(): array
{
    // Implementation
}
```

### @throws - Exception Documentation

```php
/**
 * Process a payment transaction.
 *
 * @param int $orderId The order identifier
 * @param float $amount The payment amount
 *
 * @return bool True if payment successful
 *
 * @throws InvalidArgumentException If amount is negative or zero
 * @throws PaymentGatewayException If payment gateway communication fails
 * @throws InsufficientFundsException If user has insufficient funds
 */
function processPayment(int $orderId, float $amount): bool
{
    if ($amount <= 0) {
        throw new InvalidArgumentException('Amount must be positive');
    }
    // Implementation
}
```

### @var - Variable Type Documentation

```php
class UserService
{
    /**
     * @var DatabaseConnection Database connection instance
     */
    private DatabaseConnection $db;

    /**
     * @var int Maximum login attempts allowed
     */
    private const MAX_ATTEMPTS = 5;

    /**
     * @var string[] List of allowed user roles
     */
    private array $allowedRoles;

    public function processUsers(): void
    {
        /** @var User $user */
        foreach ($this->getUsers() as $user) {
            // $user is now type-hinted for IDE
            $user->getName();
        }
    }
}
```

### @property - Magic Property Documentation

```php
/**
 * User model class.
 *
 * @property int $id User's unique identifier
 * @property string $username User's username
 * @property string $email User's email address
 * @property-read string $createdAt Account creation timestamp (read-only)
 * @property-write string $password User's password (write-only)
 */
class User
{
    private array $data = [];

    public function __get(string $name)
    {
        return $this->data[$name] ?? null;
    }

    public function __set(string $name, $value): void
    {
        $this->data[$name] = $value;
    }
}
```

### @method - Magic Method Documentation

```php
/**
 * Repository base class with magic query methods.
 *
 * @method User|null findById(int $id) Find entity by ID
 * @method User[] findByEmail(string $email) Find entities by email
 * @method User|null findOneByUsername(string $username) Find one entity by username
 */
class UserRepository
{
    public function __call(string $name, array $arguments)
    {
        // Magic method implementation
    }
}
```

## Complete Examples

### Function Documentation

```php
/**
 * Validate and sanitize user input.
 *
 * This function performs comprehensive validation and sanitization
 * of user input to prevent XSS and injection attacks.
 *
 * @param string $input The raw user input to validate
 * @param string $type The expected input type ('email', 'url', 'text')
 * @param int $maxLength Maximum allowed length (default: 255)
 *
 * @return string The sanitized input
 *
 * @throws InvalidArgumentException If input type is not supported
 * @throws ValidationException If input fails validation
 *
 * @see sanitizeEmail() For email-specific sanitization
 *
 * @example
 * $clean = validateInput($_POST['email'], 'email');
 */
function validateInput(string $input, string $type, int $maxLength = 255): string
{
    // Implementation
}
```

### Class Documentation

```php
/**
 * Handles user authentication and session management.
 *
 * This class provides methods for user login, logout, session validation,
 * and token-based authentication. It integrates with the database layer
 * and supports multiple authentication strategies.
 *
 * @package App\Auth
 * @author John Doe <john@example.com>
 * @version 2.0.0
 * @since 1.0.0
 *
 * @see SessionManager For session handling
 * @see UserRepository For user data access
 */
class AuthenticationService
{
    /**
     * @var UserRepository Repository for user data access
     */
    private UserRepository $userRepository;

    /**
     * @var SessionManager Manages user sessions
     */
    private SessionManager $sessionManager;

    /**
     * @var int Session timeout in seconds
     */
    private const SESSION_TIMEOUT = 3600;

    /**
     * Initialize the authentication service.
     *
     * @param UserRepository $userRepository Repository for accessing user data
     * @param SessionManager $sessionManager Manager for user sessions
     */
    public function __construct(
        UserRepository $userRepository,
        SessionManager $sessionManager
    ) {
        $this->userRepository = $userRepository;
        $this->sessionManager = $sessionManager;
    }

    /**
     * Authenticate a user with username and password.
     *
     * Validates credentials against the database, creates a session
     * on successful authentication, and logs the login attempt.
     *
     * @param string $username The user's username or email
     * @param string $password The user's password (plain text)
     *
     * @return User The authenticated user object
     *
     * @throws AuthenticationException If credentials are invalid
     * @throws AccountLockedException If account is locked due to failed attempts
     * @throws DatabaseException If database query fails
     */
    public function authenticate(string $username, string $password): User
    {
        // Implementation
    }

    /**
     * Log out the current user.
     *
     * Destroys the user's session and clears authentication cookies.
     *
     * @return void
     */
    public function logout(): void
    {
        $this->sessionManager->destroy();
    }

    /**
     * Check if user is currently authenticated.
     *
     * @return bool True if user has a valid session, false otherwise
     */
    public function isAuthenticated(): bool
    {
        return $this->sessionManager->isValid();
    }
}
```

### Interface Documentation

```php
/**
 * Interface for data repository implementations.
 *
 * Defines the contract for data access objects that interact
 * with the persistence layer.
 *
 * @package App\Repository
 *
 * @template T The entity type this repository manages
 */
interface RepositoryInterface
{
    /**
     * Find an entity by its identifier.
     *
     * @param int $id The entity's unique identifier
     *
     * @return T|null The entity if found, null otherwise
     */
    public function find(int $id): ?object;

    /**
     * Find all entities.
     *
     * @return T[] Array of all entities
     */
    public function findAll(): array;

    /**
     * Save an entity to the persistence layer.
     *
     * @param T $entity The entity to save
     *
     * @return void
     *
     * @throws PersistenceException If save operation fails
     */
    public function save(object $entity): void;
}
```

### Trait Documentation

```php
/**
 * Provides timestamp management for entities.
 *
 * This trait automatically manages created_at and updated_at
 * timestamps for any entity that uses it.
 *
 * @package App\Traits
 */
trait Timestampable
{
    /**
     * @var DateTimeImmutable|null Entity creation timestamp
     */
    protected ?DateTimeImmutable $createdAt = null;

    /**
     * @var DateTimeImmutable|null Entity last update timestamp
     */
    protected ?DateTimeImmutable $updatedAt = null;

    /**
     * Get the creation timestamp.
     *
     * @return DateTimeImmutable|null
     */
    public function getCreatedAt(): ?DateTimeImmutable
    {
        return $this->createdAt;
    }

    /**
     * Set the creation timestamp.
     *
     * This is typically called automatically when entity is persisted.
     *
     * @param DateTimeImmutable $createdAt The creation timestamp
     *
     * @return self For method chaining
     */
    public function setCreatedAt(DateTimeImmutable $createdAt): self
    {
        $this->createdAt = $createdAt;
        return $this;
    }
}
```

## Advanced Tags

### @deprecated - Mark Deprecated Code

```php
/**
 * Calculate discount using old method.
 *
 * @param float $price The original price
 *
 * @return float The discounted price
 *
 * @deprecated 2.0.0 Use calculateDiscountV2() instead
 * @see calculateDiscountV2()
 */
function calculateDiscount(float $price): float
{
    // Old implementation
}
```

### @internal - Internal API

```php
/**
 * Process internal cache refresh.
 *
 * @internal This method is for internal use only and may change without notice
 *
 * @return void
 */
function refreshInternalCache(): void
{
    // Internal implementation
}
```

### @link - External Documentation

```php
/**
 * OAuth2 authentication provider.
 *
 * @link https://oauth.net/2/ OAuth 2.0 Specification
 * @link https://example.com/docs/auth API Documentation
 */
class OAuth2Provider
{
    // Implementation
}
```

### @todo - Pending Tasks

```php
/**
 * Send notification to user.
 *
 * @param User $user The user to notify
 * @param string $message The notification message
 *
 * @return void
 *
 * @todo Add support for email notifications
 * @todo Implement notification preferences
 */
function sendNotification(User $user, string $message): void
{
    // Current implementation (SMS only)
}
```

## Type Declarations

### Complex Types

```php
/**
 * Process batch of orders.
 *
 * @param array<int, Order> $orders Array of order objects indexed by order ID
 * @param array{
 *     priority: string,
 *     notify: bool,
 *     warehouse_id: int
 * } $options Processing options
 *
 * @return array{
 *     processed: int,
 *     failed: int,
 *     errors: string[]
 * } Processing results
 */
function processBatchOrders(array $orders, array $options): array
{
    // Implementation
}
```

### Union Types

```php
/**
 * Format a value for display.
 *
 * @param string|int|float $value The value to format
 *
 * @return string The formatted value
 */
function formatValue(string|int|float $value): string
{
    return (string) $value;
}
```

### Generics with Templates

```php
/**
 * Generic collection class.
 *
 * @template T
 */
class Collection
{
    /**
     * @var T[]
     */
    private array $items = [];

    /**
     * Add an item to the collection.
     *
     * @param T $item The item to add
     *
     * @return void
     */
    public function add($item): void
    {
        $this->items[] = $item;
    }

    /**
     * Get all items.
     *
     * @return T[] All items in the collection
     */
    public function all(): array
    {
        return $this->items;
    }
}
```

## Laravel/Symfony Specific

### Laravel Controller

```php
/**
 * Handle user registration requests.
 *
 * @param RegisterRequest $request The validated registration request
 *
 * @return JsonResponse JSON response with user data or errors
 *
 * @throws ValidationException If validation fails
 *
 * @api
 * @apiGroup Users
 * @apiVersion 1.0.0
 */
public function register(RegisterRequest $request): JsonResponse
{
    // Implementation
}
```

### Symfony Service

```php
/**
 * Email notification service.
 *
 * @package App\Service
 *
 * @service
 * @autowire
 */
class EmailService
{
    /**
     * Send an email message.
     *
     * @param string $to Recipient email address
     * @param string $subject Email subject
     * @param string $body Email body content
     *
     * @return bool True if email sent successfully
     *
     * @throws MailerException If email sending fails
     */
    public function send(string $to, string $subject, string $body): bool
    {
        // Implementation
    }
}
```

## Best Practices

### DO

- Always include a summary line
- Document all public APIs (public methods, classes, functions)
- Use type declarations instead of repeating types in @param/@return when types are declared
- Keep descriptions concise and meaningful
- Update DocBlocks when code changes
- Use @throws for all exceptions that can be thrown
- Add examples for complex functionality
- Follow PSR-5 and PSR-19 standards

### DON'T

- Don't document obvious things excessively
- Don't duplicate type information already in type declarations
- Don't use DocBlocks for commented-out code
- Don't forget to document magic methods and properties
- Don't write overly verbose descriptions
- Don't forget to update tags when method signatures change

## Type Hints vs DocBlocks

With PHP 7.0+ type declarations, reduce redundancy:

```php
// Good: Type declarations + concise DocBlock
/**
 * Calculate order total with tax.
 *
 * @return float The total amount including tax
 */
public function calculateTotal(float $subtotal, float $taxRate): float
{
    return $subtotal * (1 + $taxRate);
}

// Avoid: Redundant type information
/**
 * Calculate order total with tax.
 *
 * @param float $subtotal The subtotal amount  // Redundant!
 * @param float $taxRate The tax rate  // Redundant!
 *
 * @return float The total amount including tax  // Redundant!
 */
public function calculateTotal(float $subtotal, float $taxRate): float
{
    return $subtotal * (1 + $taxRate);
}
```

## Validation and Generation Tools

```bash
# Install phpDocumentor
composer require --dev phpdocumentor/phpdocumentor

# Generate documentation
vendor/bin/phpdoc -d src/ -t docs/

# Install PHPStan for static analysis (validates DocBlocks)
composer require --dev phpstan/phpstan

# Run PHPStan
vendor/bin/phpstan analyse src/

# Install Psalm for additional validation
composer require --dev vimeo/psalm

# Run Psalm
vendor/bin/psalm
```

## Quick Reference

### Standard DocBlock Template

```php
/**
 * One-line summary.
 *
 * Detailed description if needed. Can span multiple
 * lines and paragraphs.
 *
 * @param type $paramName Description
 * @param type $otherParam Description
 *
 * @return type Description
 *
 * @throws ExceptionType When this happens
 *
 * @see RelatedClass
 */
```

### Property DocBlock Template

```php
/**
 * @var type Description of the property
 */
private type $property;
```

### Constant DocBlock Template

```php
/**
 * @var type Description of the constant
 */
public const CONSTANT_NAME = value;
```

## Resources

- **PSR-5**: PHPDoc standard (draft)
- **PSR-19**: PHPDoc tags standard
- **phpDocumentor**: https://www.phpdoc.org/
- **PHPStan**: Static analysis tool
- **Psalm**: Static analysis tool
- **PHP-FIG**: PHP Framework Interop Group standards
