# Good Patterns

Reference these examples when explaining what good code looks like.

---

## Naming

### Descriptive Variable Names

```typescript
// Good: Intent is clear
const activeUserCount = users.filter(u => u.isActive).length;
const maxRetryAttempts = 3;
const isEmailVerified = user.emailVerifiedAt !== null;

// Good: Domain terminology
const invoiceLineItems = invoice.items;
const shippingAddress = order.addresses.find(a => a.type === 'shipping');
```

### Function Names as Actions

```typescript
// Good: Verb + noun describes what it does
function calculateOrderTotal(order: Order): number { ... }
function validateEmailFormat(email: string): boolean { ... }
function sendPasswordResetEmail(user: User): Promise<void> { ... }
function parseConfigurationFile(path: string): Config { ... }
```

---

## Functions

### Single Responsibility

```typescript
// Good: Each function does one thing
function validateOrder(order: Order): ValidationResult {
    const errors: string[] = [];

    if (!order.items.length) {
        errors.push('Order must have at least one item');
    }
    if (!order.shippingAddress) {
        errors.push('Shipping address is required');
    }

    return { isValid: errors.length === 0, errors };
}

function calculateOrderTotal(order: Order): number {
    const subtotal = order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const tax = subtotal * order.taxRate;
    const shipping = calculateShipping(order);
    return subtotal + tax + shipping;
}

async function processOrder(order: Order): Promise<OrderResult> {
    const validation = validateOrder(order);
    if (!validation.isValid) {
        return { success: false, errors: validation.errors };
    }

    const total = calculateOrderTotal(order);
    const result = await chargePayment(order.paymentMethod, total);

    return { success: result.success, orderId: result.orderId };
}
```

### Early Returns (Guard Clauses)

```typescript
// Good: Reduces nesting, handles edge cases first
function getUserDisplayName(user: User | null): string {
    if (!user) {
        return 'Anonymous';
    }

    if (user.nickname) {
        return user.nickname;
    }

    if (user.firstName && user.lastName) {
        return `${user.firstName} ${user.lastName}`;
    }

    return user.email.split('@')[0];
}
```

---

## Error Handling

### Specific Errors with Context

```typescript
// Good: Custom error types with context
class OrderValidationError extends Error {
    constructor(
        message: string,
        public readonly orderId: string,
        public readonly field: string
    ) {
        super(message);
        this.name = 'OrderValidationError';
    }
}

class PaymentFailedError extends Error {
    constructor(
        message: string,
        public readonly orderId: string,
        public readonly paymentProvider: string,
        public readonly providerErrorCode?: string
    ) {
        super(message);
        this.name = 'PaymentFailedError';
    }
}

// Usage
throw new OrderValidationError(
    'Invalid quantity',
    order.id,
    'items[0].quantity'
);
```

### Proper Async Error Handling

```typescript
// Good: Try/catch with proper error handling
async function fetchUserData(userId: string): Promise<UserData> {
    try {
        const response = await fetch(`/api/users/${userId}`);

        if (!response.ok) {
            throw new ApiError(`Failed to fetch user: ${response.statusText}`, response.status);
        }

        return await response.json();
    } catch (error) {
        if (error instanceof ApiError) {
            throw error; // Re-throw known errors
        }

        // Wrap unknown errors with context
        throw new ApiError(`Network error fetching user ${userId}`, 0, error);
    }
}
```

---

## Security

### Parameterized Queries

```typescript
// Good: SQL injection safe
async function getUserByEmail(email: string): Promise<User | null> {
    const result = await db.query(
        'SELECT * FROM users WHERE email = $1',
        [email]
    );
    return result.rows[0] ?? null;
}

// Good: ORM with proper escaping
const user = await prisma.user.findUnique({
    where: { email }
});
```

### Input Validation

```typescript
// Good: Schema-based validation
import { z } from 'zod';

const CreateUserSchema = z.object({
    email: z.string().email(),
    password: z.string().min(8).max(100),
    name: z.string().min(1).max(200),
    age: z.number().int().min(0).max(150).optional(),
});

function createUser(input: unknown): User {
    const validated = CreateUserSchema.parse(input);
    return userRepository.create(validated);
}
```

---

## Performance

### Parallel Async Operations

```typescript
// Good: Independent operations run in parallel
async function loadDashboardData(userId: string): Promise<DashboardData> {
    const [user, orders, notifications, settings] = await Promise.all([
        fetchUser(userId),
        fetchUserOrders(userId),
        fetchNotifications(userId),
        fetchUserSettings(userId),
    ]);

    return { user, orders, notifications, settings };
}
```

### Efficient Data Structures

```typescript
// Good: Set for O(1) lookups
function filterBlockedUsers(users: User[], blockedIds: string[]): User[] {
    const blockedSet = new Set(blockedIds);
    return users.filter(user => !blockedSet.has(user.id));
}

// Good: Map for O(1) key-based access
function groupOrdersByCustomer(orders: Order[]): Map<string, Order[]> {
    const grouped = new Map<string, Order[]>();

    for (const order of orders) {
        const existing = grouped.get(order.customerId) ?? [];
        existing.push(order);
        grouped.set(order.customerId, existing);
    }

    return grouped;
}
```

---

## TypeScript-Specific

### Discriminated Unions

```typescript
// Good: Type-safe state handling
type RequestState<T> =
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'success'; data: T }
    | { status: 'error'; error: Error };

function renderUserState(state: RequestState<User>): JSX.Element {
    switch (state.status) {
        case 'idle':
            return <div>Click to load</div>;
        case 'loading':
            return <Spinner />;
        case 'success':
            return <UserCard user={state.data} />;
        case 'error':
            return <ErrorMessage error={state.error} />;
    }
}
```

### Type Guards

```typescript
// Good: Runtime type checking with type narrowing
function isApiError(error: unknown): error is ApiError {
    return (
        error instanceof Error &&
        'statusCode' in error &&
        typeof (error as ApiError).statusCode === 'number'
    );
}

// Usage
try {
    await fetchData();
} catch (error) {
    if (isApiError(error) && error.statusCode === 404) {
        return null;
    }
    throw error;
}
```

---

## Python-Specific

### Context Managers

```python
# Good: Automatic resource cleanup
from contextlib import contextmanager

@contextmanager
def database_transaction():
    conn = get_connection()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

# Usage
with database_transaction() as conn:
    conn.execute("INSERT INTO users ...")
```

### Dataclasses with Validation

```python
# Good: Structured data with type hints
from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    id: str
    email: str
    name: str
    age: Optional[int] = None

    def __post_init__(self):
        if not self.email or '@' not in self.email:
            raise ValueError(f"Invalid email: {self.email}")
        if self.age is not None and (self.age < 0 or self.age > 150):
            raise ValueError(f"Invalid age: {self.age}")
```

### List Comprehensions

```python
# Good: Clear and Pythonic
active_user_emails = [
    user.email
    for user in users
    if user.is_active and user.email_verified
]

# Good: Dict comprehension
user_by_id = {user.id: user for user in users}

# Good: Generator for large datasets
def process_large_file(path):
    with open(path) as f:
        for line in f:  # Lazy iteration
            yield parse_line(line)
```

---

## Testing

### Focused Test Cases

```typescript
// Good: One concept per test
describe('calculateOrderTotal', () => {
    it('returns 0 for empty order', () => {
        const order = createOrder({ items: [] });
        expect(calculateOrderTotal(order)).toBe(0);
    });

    it('sums item prices correctly', () => {
        const order = createOrder({
            items: [
                { price: 10, quantity: 2 },
                { price: 5, quantity: 1 },
            ]
        });
        expect(calculateOrderTotal(order)).toBe(25);
    });

    it('applies tax rate', () => {
        const order = createOrder({
            items: [{ price: 100, quantity: 1 }],
            taxRate: 0.1
        });
        expect(calculateOrderTotal(order)).toBe(110);
    });
});
```

### Test Helpers

```typescript
// Good: Reusable test fixtures
function createTestUser(overrides: Partial<User> = {}): User {
    return {
        id: 'test-user-id',
        email: 'test@example.com',
        name: 'Test User',
        createdAt: new Date('2024-01-01'),
        ...overrides,
    };
}

// Usage
const activeUser = createTestUser({ isActive: true });
const adminUser = createTestUser({ role: 'admin' });
```
