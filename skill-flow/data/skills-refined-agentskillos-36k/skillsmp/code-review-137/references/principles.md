# Clean Code Principles Reference

## SOLID Principles

### S - Single Responsibility Principle (SRP)
**Definition**: A class should have one, and only one, reason to change.

**What it means**: Each module, class, or function should have responsibility over a single part of functionality, and that responsibility should be entirely encapsulated by the class.

**Why it matters**:
- Changes to one aspect don't affect others
- Easier to understand, test, and maintain
- Reduces coupling between components

**Example - Violation**:
```typescript
class UserManager {
  createUser(data) { /* database logic */ }
  sendWelcomeEmail(user) { /* email logic */ }
  generateReport(user) { /* reporting logic */ }
  validateInput(data) { /* validation logic */ }
}
```
Four responsibilities: database, email, reporting, validation.

**Example - Fixed**:
```typescript
class UserRepository {
  createUser(data) { /* only database logic */ }
}

class EmailService {
  sendWelcomeEmail(user) { /* only email logic */ }
}

class ReportGenerator {
  generateReport(user) { /* only reporting logic */ }
}

class UserValidator {
  validateInput(data) { /* only validation logic */ }
}
```

### O - Open/Closed Principle (OCP)
**Definition**: Software entities should be open for extension but closed for modification.

**What it means**: Add new functionality by extending existing code, not modifying it.

**Why it matters**:
- Reduces risk of breaking existing functionality
- Promotes code reuse
- Enables plugin architectures

**Example - Violation**:
```typescript
class PaymentProcessor {
  processPayment(type: string, amount: number) {
    if (type === 'credit-card') {
      // credit card logic
    } else if (type === 'paypal') {
      // paypal logic
    } else if (type === 'crypto') {
      // crypto logic - requires modifying existing code
    }
  }
}
```

**Example - Fixed**:
```typescript
interface PaymentMethod {
  process(amount: number): void;
}

class CreditCardPayment implements PaymentMethod {
  process(amount: number) { /* credit card logic */ }
}

class PayPalPayment implements PaymentMethod {
  process(amount: number) { /* paypal logic */ }
}

class CryptoPayment implements PaymentMethod {
  process(amount: number) { /* crypto logic */ }
}

class PaymentProcessor {
  processPayment(method: PaymentMethod, amount: number) {
    method.process(amount);
  }
}
```
Adding new payment methods doesn't require modifying existing code.

### L - Liskov Substitution Principle (LSP)
**Definition**: Objects of a superclass should be replaceable with objects of its subclasses without breaking functionality.

**What it means**: Subclasses must be substitutable for their base classes without altering program correctness.

**Why it matters**:
- Ensures inheritance hierarchies are designed correctly
- Prevents surprises when using polymorphism
- Maintains contracts defined by base classes

**Example - Violation**:
```typescript
class Bird {
  fly() { /* flying logic */ }
}

class Penguin extends Bird {
  fly() {
    throw new Error("Penguins can't fly!");
  }
}

function makeBirdFly(bird: Bird) {
  bird.fly(); // Breaks when bird is a Penguin
}
```

**Example - Fixed**:
```typescript
interface Bird {
  move(): void;
}

class FlyingBird implements Bird {
  move() { this.fly(); }
  private fly() { /* flying logic */ }
}

class Penguin implements Bird {
  move() { this.swim(); }
  private swim() { /* swimming logic */ }
}

function moveBird(bird: Bird) {
  bird.move(); // Works for all birds
}
```

### I - Interface Segregation Principle (ISP)
**Definition**: No client should be forced to depend on methods it does not use.

**What it means**: Create specific interfaces rather than one large general-purpose interface.

**Why it matters**:
- Reduces coupling
- Makes code more flexible
- Prevents implementing unused methods

**Example - Violation**:
```typescript
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
}

class Robot implements Worker {
  work() { /* work logic */ }
  eat() { throw new Error("Robots don't eat"); }
  sleep() { throw new Error("Robots don't sleep"); }
}
```

**Example - Fixed**:
```typescript
interface Workable {
  work(): void;
}

interface Eatable {
  eat(): void;
}

interface Sleepable {
  sleep(): void;
}

class Human implements Workable, Eatable, Sleepable {
  work() { /* work logic */ }
  eat() { /* eat logic */ }
  sleep() { /* sleep logic */ }
}

class Robot implements Workable {
  work() { /* work logic */ }
}
```

### D - Dependency Inversion Principle (DIP)
**Definition**: High-level modules should not depend on low-level modules. Both should depend on abstractions.

**What it means**: Depend on interfaces or abstract classes, not concrete implementations.

**Why it matters**:
- Reduces coupling between modules
- Makes code more testable (easier to mock dependencies)
- Enables flexibility in implementation choices

**Example - Violation**:
```typescript
class MySQLDatabase {
  save(data: any) { /* MySQL-specific logic */ }
}

class UserService {
  private db = new MySQLDatabase(); // Tight coupling

  createUser(user: User) {
    this.db.save(user);
  }
}
```

**Example - Fixed**:
```typescript
interface Database {
  save(data: any): void;
}

class MySQLDatabase implements Database {
  save(data: any) { /* MySQL-specific logic */ }
}

class PostgreSQLDatabase implements Database {
  save(data: any) { /* PostgreSQL-specific logic */ }
}

class UserService {
  constructor(private db: Database) {} // Depends on abstraction

  createUser(user: User) {
    this.db.save(user);
  }
}

// Inject dependency
const userService = new UserService(new MySQLDatabase());
```

---

## DRY - Don't Repeat Yourself

**Definition**: Every piece of knowledge must have a single, unambiguous, authoritative representation within a system.

**What it means**: Avoid code duplication. Extract repeated logic into reusable functions/classes.

**Why it matters**:
- Changes only need to be made once
- Reduces bugs from inconsistent updates
- Improves maintainability

**Example - Violation**:
```typescript
function calculateOrderTotal(items: Item[]) {
  let total = 0;
  for (const item of items) {
    total += item.price * item.quantity;
  }
  total = total * 1.1; // 10% tax
  return total;
}

function calculateCartTotal(products: Product[]) {
  let total = 0;
  for (const product of products) {
    total += product.price * product.quantity;
  }
  total = total * 1.1; // 10% tax (duplicated logic)
  return total;
}
```

**Example - Fixed**:
```typescript
function calculateSubtotal(items: Array<{price: number, quantity: number}>) {
  return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function applyTax(subtotal: number, taxRate: number = 0.1) {
  return subtotal * (1 + taxRate);
}

function calculateTotal(items: Array<{price: number, quantity: number}>) {
  const subtotal = calculateSubtotal(items);
  return applyTax(subtotal);
}

// Now both can use the same logic
const orderTotal = calculateTotal(orderItems);
const cartTotal = calculateTotal(cartProducts);
```

**When NOT to apply DRY**:
- Coincidental duplication (similar code, different purposes)
- Premature abstraction (forces unnatural coupling)

---

## KISS - Keep It Simple, Stupid

**Definition**: Most systems work best if they are kept simple rather than made complicated.

**What it means**: Favor simple solutions over complex ones. Avoid unnecessary cleverness.

**Why it matters**:
- Easier to understand and maintain
- Fewer bugs
- Faster development
- Better collaboration

**Example - Violation**:
```typescript
// Overly complex one-liner
const result = data.reduce((acc, curr) => ({
  ...acc,
  [curr.id]: {
    ...curr,
    items: (acc[curr.id]?.items || []).concat(
      curr.tags.filter(t => !acc[curr.id]?.items?.some(i => i.id === t.id))
    )
  }
}), {});
```

**Example - Fixed**:
```typescript
// Simple, clear, step-by-step
const result = {};

for (const item of data) {
  if (!result[item.id]) {
    result[item.id] = { ...item, items: [] };
  }

  for (const tag of item.tags) {
    const exists = result[item.id].items.some(i => i.id === tag.id);
    if (!exists) {
      result[item.id].items.push(tag);
    }
  }
}
```

**Guidelines**:
- Use clear variable names over abbreviated ones
- Break complex logic into small functions
- Avoid nested ternaries and complex one-liners
- Prefer readability over cleverness

---

## YAGNI - You Aren't Gonna Need It

**Definition**: Don't implement something until it is necessary.

**What it means**: Only add functionality when there's an immediate need, not when you anticipate future requirements.

**Why it matters**:
- Reduces code complexity
- Saves development time
- Avoids maintaining unused code
- Requirements often change before future features are needed

**Example - Violation**:
```typescript
class UserService {
  createUser(data: UserData) { /* ... */ }
  updateUser(id: string, data: UserData) { /* ... */ }
  deleteUser(id: string) { /* ... */ }

  // Added "just in case" - not currently needed
  bulkCreateUsers(users: UserData[]) { /* ... */ }
  exportUsersToCSV() { /* ... */ }
  exportUsersToXML() { /* ... */ }
  exportUsersToJSON() { /* ... */ }
  scheduleUserDeletion(id: string, date: Date) { /* ... */ }
  archiveInactiveUsers(days: number) { /* ... */ }
}
```

**Example - Fixed**:
```typescript
class UserService {
  // Only implement what's currently needed
  createUser(data: UserData) { /* ... */ }
  updateUser(id: string, data: UserData) { /* ... */ }
  deleteUser(id: string) { /* ... */ }
}

// Add other methods only when requirements demand them
```

**When NOT to apply YAGNI**:
- Security features (implement upfront)
- Scalability concerns for known load
- Proven patterns with minimal cost

---

## Common Code Smells

### 1. Long Method / Function
**Smell**: Functions > 20-30 lines or doing multiple things
**Fix**: Extract smaller, focused functions

### 2. Large Class
**Smell**: Classes with many responsibilities or fields
**Fix**: Split into multiple classes following SRP

### 3. Duplicated Code
**Smell**: Same code in multiple places
**Fix**: Extract to shared function/module (DRY)

### 4. Long Parameter List
**Smell**: Functions taking > 3-4 parameters
**Fix**: Use parameter objects or builder pattern

### 5. Primitive Obsession
**Smell**: Using primitives instead of small objects for domain concepts
**Fix**: Create value objects (e.g., `Email`, `Money`, `PhoneNumber`)

### 6. Shotgun Surgery
**Smell**: Single change requires modifications in many classes
**Fix**: Move related code into single module

### 7. Feature Envy
**Smell**: Method uses more features of another class than its own
**Fix**: Move method to the class it envies

### 8. Deep Nesting
**Smell**: Code nested > 3 levels deep
**Fix**: Early returns, extract functions, guard clauses

### 9. Magic Numbers
**Smell**: Unexplained literals in code
**Fix**: Use named constants

```typescript
// Bad
if (user.age > 18) { /* ... */ }

// Good
const LEGAL_AGE = 18;
if (user.age > LEGAL_AGE) { /* ... */ }
```

### 10. Boolean Flags in Functions
**Smell**: Function behavior changes drastically based on boolean parameter
**Fix**: Split into two functions

```typescript
// Bad
function getUsers(includeInactive: boolean) {
  if (includeInactive) {
    return allUsers;
  } else {
    return activeUsers;
  }
}

// Good
function getAllUsers() { return allUsers; }
function getActiveUsers() { return activeUsers; }
```

---

## Anti-Patterns to Avoid

### God Object
Single class that knows/does too much
**Fix**: Apply SRP, distribute responsibilities

### Spaghetti Code
Tangled, unstructured code with no clear flow
**Fix**: Refactor into modular, well-organized structure

### Premature Optimization
Optimizing before measuring or confirming bottlenecks
**Fix**: Make it work, make it right, then make it fast

### Golden Hammer
Using one solution for every problem
**Fix**: Choose appropriate tools for each problem

### Cargo Cult Programming
Using patterns without understanding why
**Fix**: Understand the principles, not just the pattern
