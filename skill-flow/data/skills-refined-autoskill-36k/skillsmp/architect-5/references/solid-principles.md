# SOLID Principles Reference

Practical guide to applying SOLID principles in real codebases.

## S - Single Responsibility Principle

> A class should have only one reason to change.

### Anti-Pattern

```typescript
// ❌ BAD: User class does too much
class User {
  constructor(private db: Database) {}

  save() { /* database logic */ }
  sendEmail() { /* email logic */ }
  generateReport() { /* reporting logic */ }
  validatePassword() { /* validation logic */ }
}
```

### Correct Pattern

```typescript
// ✅ GOOD: Separated responsibilities
class User {
  constructor(
    public id: string,
    public email: string,
    public name: string
  ) {}
}

class UserRepository {
  constructor(private db: Database) {}
  save(user: User): Promise<void> { /* ... */ }
  findById(id: string): Promise<User | null> { /* ... */ }
}

class UserNotificationService {
  constructor(private emailClient: EmailClient) {}
  sendWelcomeEmail(user: User): Promise<void> { /* ... */ }
}

class PasswordValidator {
  validate(password: string): ValidationResult { /* ... */ }
}
```

### Detection Signals
- Class has methods for unrelated operations
- Changes to one feature require changes to unrelated code
- Class name includes "And" or "Manager" (e.g., `UserAndOrderManager`)
- More than 5-7 public methods
- Class requires many different dependencies

## O - Open/Closed Principle

> Software entities should be open for extension but closed for modification.

### Anti-Pattern

```typescript
// ❌ BAD: Must modify class to add new payment types
class PaymentProcessor {
  process(payment: Payment) {
    if (payment.type === 'credit') {
      // credit card logic
    } else if (payment.type === 'paypal') {
      // paypal logic
    } else if (payment.type === 'crypto') {
      // crypto logic - had to modify this class!
    }
  }
}
```

### Correct Pattern

```typescript
// ✅ GOOD: Extend via new implementations
interface PaymentHandler {
  canHandle(payment: Payment): boolean;
  process(payment: Payment): Promise<PaymentResult>;
}

class CreditCardHandler implements PaymentHandler {
  canHandle(payment: Payment) { return payment.type === 'credit'; }
  process(payment: Payment) { /* ... */ }
}

class PayPalHandler implements PaymentHandler {
  canHandle(payment: Payment) { return payment.type === 'paypal'; }
  process(payment: Payment) { /* ... */ }
}

// Adding crypto doesn't modify existing code
class CryptoHandler implements PaymentHandler {
  canHandle(payment: Payment) { return payment.type === 'crypto'; }
  process(payment: Payment) { /* ... */ }
}

class PaymentProcessor {
  constructor(private handlers: PaymentHandler[]) {}

  process(payment: Payment) {
    const handler = this.handlers.find(h => h.canHandle(payment));
    if (!handler) throw new Error('No handler for payment type');
    return handler.process(payment);
  }
}
```

### Detection Signals
- Switch/if statements on type fields
- Frequent modifications to add new cases
- God classes that handle many scenarios

## L - Liskov Substitution Principle

> Subtypes must be substitutable for their base types.

### Anti-Pattern

```typescript
// ❌ BAD: Square violates Rectangle contract
class Rectangle {
  constructor(protected width: number, protected height: number) {}

  setWidth(w: number) { this.width = w; }
  setHeight(h: number) { this.height = h; }
  getArea() { return this.width * this.height; }
}

class Square extends Rectangle {
  setWidth(w: number) {
    this.width = w;
    this.height = w;  // Violates expected behavior!
  }
  setHeight(h: number) {
    this.width = h;
    this.height = h;  // Violates expected behavior!
  }
}

// This test fails for Square:
function testRectangle(rect: Rectangle) {
  rect.setWidth(5);
  rect.setHeight(4);
  assert(rect.getArea() === 20);  // Fails for Square (returns 16)
}
```

### Correct Pattern

```typescript
// ✅ GOOD: Separate types, shared interface
interface Shape {
  getArea(): number;
}

class Rectangle implements Shape {
  constructor(private width: number, private height: number) {}
  getArea() { return this.width * this.height; }
}

class Square implements Shape {
  constructor(private side: number) {}
  getArea() { return this.side * this.side; }
}
```

### Detection Signals
- Subclass throws exceptions for inherited methods
- Subclass overrides methods with different behavior
- Type checks in code using base class (`instanceof`)
- Comments like "don't call this method on X"

## I - Interface Segregation Principle

> Clients should not be forced to depend on interfaces they don't use.

### Anti-Pattern

```typescript
// ❌ BAD: Fat interface
interface Worker {
  work(): void;
  eat(): void;
  sleep(): void;
  attendMeeting(): void;
  writeReport(): void;
}

// Robot can't eat or sleep!
class Robot implements Worker {
  work() { /* ... */ }
  eat() { throw new Error('Robots do not eat'); }
  sleep() { throw new Error('Robots do not sleep'); }
  attendMeeting() { /* ... */ }
  writeReport() { throw new Error('Robots do not write reports'); }
}
```

### Correct Pattern

```typescript
// ✅ GOOD: Segregated interfaces
interface Workable {
  work(): void;
}

interface Feedable {
  eat(): void;
}

interface Restable {
  sleep(): void;
}

interface MeetingAttendee {
  attendMeeting(): void;
}

class Human implements Workable, Feedable, Restable, MeetingAttendee {
  work() { /* ... */ }
  eat() { /* ... */ }
  sleep() { /* ... */ }
  attendMeeting() { /* ... */ }
}

class Robot implements Workable, MeetingAttendee {
  work() { /* ... */ }
  attendMeeting() { /* ... */ }
}
```

### Detection Signals
- Classes implement interfaces but throw "not implemented"
- Interfaces have many methods (> 5-7)
- Different clients use different subsets of methods
- Interface changes affect unrelated implementers

## D - Dependency Inversion Principle

> High-level modules should not depend on low-level modules. Both should depend on abstractions.

### Anti-Pattern

```typescript
// ❌ BAD: Direct dependency on concrete class
class UserService {
  private database = new MySQLDatabase();  // Tightly coupled!

  getUser(id: string) {
    return this.database.query(`SELECT * FROM users WHERE id = ?`, [id]);
  }
}
```

### Correct Pattern

```typescript
// ✅ GOOD: Depend on abstraction
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

class MySQLUserRepository implements UserRepository {
  constructor(private db: MySQLConnection) {}
  async findById(id: string) { /* ... */ }
  async save(user: User) { /* ... */ }
}

class UserService {
  constructor(private userRepo: UserRepository) {}  // Injected!

  async getUser(id: string) {
    return this.userRepo.findById(id);
  }
}

// Easy to test with mock
const mockRepo: UserRepository = {
  findById: jest.fn().mockResolvedValue({ id: '1', name: 'Test' }),
  save: jest.fn()
};
const service = new UserService(mockRepo);
```

### Detection Signals
- `new` keyword inside business logic classes
- Hard to test without real database/API
- Changing infrastructure requires changing business logic
- Import statements for concrete implementations in services

## Quick Reference Table

| Principle | Smell | Fix |
|-----------|-------|-----|
| **SRP** | Class does unrelated things | Split into focused classes |
| **OCP** | Switch on type field | Use polymorphism/strategy |
| **LSP** | Subclass breaks parent behavior | Rethink inheritance |
| **ISP** | "Not implemented" exceptions | Split interface |
| **DIP** | `new` in business logic | Inject dependencies |

## When to Apply

**Apply Strictly:**
- Core domain logic
- Code that changes frequently
- Code that needs testing

**Apply Pragmatically:**
- Simple CRUD operations
- Glue code
- Scripts and utilities
- Early prototypes (refactor later)
