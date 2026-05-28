# Anti-Patterns

Reference these examples when explaining what to avoid. Each example shows the problem and the fix.

---

## Naming

### Vague Names

```typescript
// BAD
const d = new Date();
const arr = users.filter(u => u.a);
function process(data) { ... }
function handle(x) { ... }

// GOOD
const createdAt = new Date();
const activeUsers = users.filter(user => user.isActive);
function validateUserInput(formData) { ... }
function handlePaymentFailure(error) { ... }
```

### Misleading Names

```typescript
// BAD: Name doesn't match behavior
function getUser(id) {
    // Actually creates a user if not found!
    let user = db.find(id);
    if (!user) {
        user = db.create({ id });
    }
    return user;
}

// GOOD: Name reflects behavior
function getOrCreateUser(id) { ... }
```

---

## Functions

### God Functions

```typescript
// BAD: Does too many things
async function processOrder(order) {
    // Validation
    if (!order.items.length) throw new Error('Empty order');
    if (!order.customer) throw new Error('No customer');

    // Calculate totals
    let subtotal = 0;
    for (const item of order.items) {
        subtotal += item.price * item.quantity;
    }
    const tax = subtotal * 0.1;
    const total = subtotal + tax;

    // Process payment
    const payment = await stripe.charges.create({
        amount: total * 100,
        currency: 'usd',
        customer: order.customer.stripeId,
    });

    // Send confirmation email
    await sendEmail({
        to: order.customer.email,
        subject: 'Order Confirmation',
        body: `Your order total is $${total}`,
    });

    // Update inventory
    for (const item of order.items) {
        await db.inventory.decrement(item.productId, item.quantity);
    }

    // Log analytics
    analytics.track('order_completed', { orderId: order.id, total });

    return { success: true, paymentId: payment.id };
}

// GOOD: Split into focused functions
async function processOrder(order) {
    validateOrder(order);
    const total = calculateTotal(order);
    const payment = await processPayment(order.customer, total);
    await Promise.all([
        sendOrderConfirmation(order, total),
        updateInventory(order.items),
        trackOrderAnalytics(order, total),
    ]);
    return { success: true, paymentId: payment.id };
}
```

### Deep Nesting

```typescript
// BAD: Pyramid of doom
function processUser(user) {
    if (user) {
        if (user.isActive) {
            if (user.hasPermission('read')) {
                if (user.subscription) {
                    if (user.subscription.isValid()) {
                        return fetchUserData(user);
                    } else {
                        throw new Error('Subscription expired');
                    }
                } else {
                    throw new Error('No subscription');
                }
            } else {
                throw new Error('No permission');
            }
        } else {
            throw new Error('User inactive');
        }
    } else {
        throw new Error('User required');
    }
}

// GOOD: Early returns
function processUser(user) {
    if (!user) throw new Error('User required');
    if (!user.isActive) throw new Error('User inactive');
    if (!user.hasPermission('read')) throw new Error('No permission');
    if (!user.subscription) throw new Error('No subscription');
    if (!user.subscription.isValid()) throw new Error('Subscription expired');

    return fetchUserData(user);
}
```

---

## Error Handling

### Silent Failures

```typescript
// BAD: Error swallowed
try {
    await saveUser(user);
} catch (e) {
    // Nothing happens, data lost silently
}

// BAD: Logged but not handled
try {
    await saveUser(user);
} catch (e) {
    console.log(e);  // Caller thinks it succeeded!
}

// GOOD: Handle or rethrow
try {
    await saveUser(user);
} catch (e) {
    logger.error('Failed to save user', { userId: user.id, error: e });
    throw new UserSaveError('Could not save user', user.id, e);
}
```

### Generic Error Messages

```typescript
// BAD: Unhelpful message
throw new Error('Something went wrong');
throw new Error('Invalid input');

// GOOD: Specific and actionable
throw new ValidationError(`Email "${email}" is not a valid email address`);
throw new AuthorizationError(`User ${userId} does not have permission to delete project ${projectId}`);
```

---

## Security

### Hardcoded Secrets

```typescript
// BAD: Secret in code
const API_KEY = 'sk-1234567890abcdef';
const DB_PASSWORD = 'super_secret_password';

// GOOD: Environment variables
const API_KEY = process.env.API_KEY;
const DB_PASSWORD = process.env.DB_PASSWORD;
```

### SQL Injection

```typescript
// BAD: String concatenation
const query = `SELECT * FROM users WHERE email = '${email}'`;
db.query(query);

// GOOD: Parameterized query
db.query('SELECT * FROM users WHERE email = $1', [email]);
```

### Command Injection

```typescript
// BAD: User input in command
exec(`convert ${uploadedFile} output.png`);

// GOOD: Use execFile with arguments array
execFile('convert', [uploadedFile, 'output.png']);
```

---

## Performance

### N+1 Queries

```typescript
// BAD: Query per item
const users = await db.query('SELECT * FROM users');
for (const user of users) {
    user.orders = await db.query(`SELECT * FROM orders WHERE user_id = ${user.id}`);
}

// GOOD: Single batched query
const users = await db.query('SELECT * FROM users');
const userIds = users.map(u => u.id);
const orders = await db.query('SELECT * FROM orders WHERE user_id = ANY($1)', [userIds]);
const ordersByUser = groupBy(orders, 'user_id');
users.forEach(u => u.orders = ordersByUser[u.id] || []);
```

### Unbounded Queries

```typescript
// BAD: Could return millions of rows
const allUsers = await db.query('SELECT * FROM users');

// GOOD: Paginated
const users = await db.query('SELECT * FROM users LIMIT $1 OFFSET $2', [pageSize, offset]);
```

### Sequential When Parallel Possible

```typescript
// BAD: Waits for each sequentially
const user = await getUser(id);
const orders = await getOrders(id);
const settings = await getSettings(id);

// GOOD: Run in parallel
const [user, orders, settings] = await Promise.all([
    getUser(id),
    getOrders(id),
    getSettings(id),
]);
```

---

## TypeScript-Specific

### Any Abuse

```typescript
// BAD: Defeats type checking
function processData(data: any): any {
    return data.something.value;
}

// GOOD: Proper types
interface DataPayload {
    something: {
        value: string;
    };
}

function processData(data: DataPayload): string {
    return data.something.value;
}
```

### Floating Promises

```typescript
// BAD: Promise ignored, errors lost
saveUser(user);
fetchData().then(process);

// GOOD: Await or handle errors
await saveUser(user);
// OR
saveUser(user).catch(handleError);
// OR void for intentional fire-and-forget
void logAnalytics(event);
```

### Unsafe Type Assertions

```typescript
// BAD: Assuming type without validation
const user = response.data as User;

// GOOD: Validate first
function isUser(data: unknown): data is User {
    return (
        typeof data === 'object' &&
        data !== null &&
        'id' in data &&
        'email' in data
    );
}

if (!isUser(response.data)) {
    throw new Error('Invalid user data');
}
const user = response.data;  // Now safely typed
```

---

## Python-Specific

### Mutable Default Arguments

```python
# BAD: Same list reused across calls!
def append_item(item, items=[]):
    items.append(item)
    return items

# append_item(1) → [1]
# append_item(2) → [1, 2]  # Unexpected!

# GOOD: Use None as default
def append_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Bare Except

```python
# BAD: Catches everything including SystemExit, KeyboardInterrupt
try:
    do_something()
except:
    pass

# GOOD: Catch specific exceptions
try:
    do_something()
except ValueError as e:
    handle_value_error(e)
except IOError as e:
    handle_io_error(e)
```

### Star Imports

```python
# BAD: Pollutes namespace, unclear origins
from utils import *
from helpers import *

result = process(data)  # Where does process come from?

# GOOD: Explicit imports
from utils import validate_email, format_date
from helpers import process

result = process(data)
```

---

## Testing

### No Assertions

```typescript
// BAD: Test passes but verifies nothing
test('creates user', () => {
    createUser({ name: 'Test' });
});

// GOOD: Assert expected behavior
test('creates user with correct data', () => {
    const user = createUser({ name: 'Test' });
    expect(user.name).toBe('Test');
    expect(user.id).toBeDefined();
    expect(user.createdAt).toBeInstanceOf(Date);
});
```

### Test Logic

```typescript
// BAD: Logic in tests can have bugs
test('doubles numbers correctly', () => {
    for (let i = 0; i < 10; i++) {
        expect(double(i)).toBe(i * 2);  // If double is wrong, this hides it
    }
});

// GOOD: Explicit expected values
test('doubles numbers correctly', () => {
    expect(double(0)).toBe(0);
    expect(double(1)).toBe(2);
    expect(double(5)).toBe(10);
    expect(double(-3)).toBe(-6);
});
```

### Shared Mutable State

```typescript
// BAD: Tests affect each other
let testUser;

beforeEach(() => {
    testUser = { name: 'Test', count: 0 };
});

test('first test', () => {
    testUser.count++;
    expect(testUser.count).toBe(1);
});

test('second test', () => {
    // Might fail if tests run in different order
    expect(testUser.count).toBe(0);
});

// GOOD: Create fresh data in each test
test('first test', () => {
    const user = createTestUser();
    user.count++;
    expect(user.count).toBe(1);
});

test('second test', () => {
    const user = createTestUser();
    expect(user.count).toBe(0);
});
```

---

## Documentation

### Obvious Comments

```typescript
// BAD: Comment says what code clearly shows
// Increment counter
counter++;

// Loop through users
for (const user of users) { ... }

// Return the result
return result;

// GOOD: Comment explains WHY
// Use binary search since users are pre-sorted by ID for performance
const user = binarySearch(users, targetId);

// Empty array returns 0 (not undefined) for backward compatibility with v1 API
if (items.length === 0) return 0;
```

### Outdated Comments

```typescript
// BAD: Comment doesn't match code
// Returns user or null if not found
function getUser(id) {
    const user = db.find(id);
    if (!user) throw new UserNotFoundError(id);  // Actually throws!
    return user;
}

// GOOD: Keep comments in sync or remove them
/**
 * @throws {UserNotFoundError} When user doesn't exist
 */
function getUser(id) {
    const user = db.find(id);
    if (!user) throw new UserNotFoundError(id);
    return user;
}
```
