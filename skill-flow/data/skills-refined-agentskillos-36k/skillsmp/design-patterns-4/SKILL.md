---
name: design-patterns
description: TypeScript refactoring patterns and code smell detection. Based on Martin Fowler's refactoring catalog - language-agnostic patterns adapted for TypeScript/JavaScript.
priority: medium-high
rule_count: 13
sources:
  - "Refactoring: Improving the Design of Existing Code (Martin Fowler)"
  - "Clean Code (Robert C. Martin)"
  - "Refactoring.Guru"
---

# Design Patterns & Refactoring - TypeScript Best Practices

Detect code smells and apply proven refactoring patterns to improve maintainability.

## When to Use

- Refactoring complex or legacy code
- Reducing technical debt
- Simplifying large functions
- Improving code readability
- Extracting reusable patterns

**Trigger Phrases:**
- "Refactor this code"
- "Find code smells"
- "Reduce complexity"
- "Improve maintainability"

## Rules Overview

### High Priority (2 rules)
Critical refactoring needs:

1. **high-god-object** - Extract logic from 300+ line functions
2. **high-extract-method** - Name complex code blocks with descriptive methods

### Medium Priority (11 rules)
Code quality improvements:

3. **medium-primitive-obsession** - Replace primitives with value objects
4. **medium-long-parameter-list** - Use parameter objects for >5 params
5. **medium-data-clumps** - Extract repeated parameter groups  
6. **medium-feature-envy** - Move logic closer to data
7. **medium-magic-constants** - Replace magic numbers with named constants
8. **medium-builder-pattern** - Fluent API for complex construction
9. **medium-factory-constructor** - Validated object creation
10. **medium-introduce-parameter-object** - Group related parameters
11. **medium-switch-to-strategy** - Replace type switches with polymorphism
12. **medium-callback-hell** - Replace nested callbacks with async/await
13. **medium-law-of-demeter** - Reduce coupling, avoid message chains

---

## Rule Details

### 1. high-god-object

**Why it matters:** Functions over 300 lines are hard to understand, test, and maintain.

**Detection:**
- Count lines in functions
- Look for multiple responsibilities
- Check for many local variables

**❌ Incorrect:**
```typescript
async function processOrder(orderId: string) {
  // 500+ lines of code doing everything:
  // - Validation
  // - Price calculation
  // - Inventory check
  // - Payment processing
  // - Email notification
  // - Logging
  // ... many more responsibilities
}
```

**✅ Correct:**
```typescript
class OrderProcessor {
  async processOrder(orderId: string) {
    const order = await this.validateOrder(orderId);
    const total = this.calculateTotal(order);
    await this.checkInventory(order);
    await this.processPayment(order, total);
    await this.sendConfirmation(order);
    this.logOrderProcessed(order);
  }
  
  private async validateOrder(orderId: string) {
    // Single responsibility: validation only
  }
  
  private calculateTotal(order: Order): number {
    // Single responsibility: calculation
  }
  
  // ... other focused methods
}
```

**Impact:** HIGH - Dramatically improves readability and testability

**Reference:** Refactoring: Extract Method

---

### 2. high-extract-method

**Why it matters:** Named methods document intent and improve code comprehension.

**Detection:**
- Look for comments explaining code blocks
- Check for complex expressions
- Search for multi-line if/loop bodies

**❌ Incorrect:**
```typescript
function analyzeUser(user: User) {
  // Calculate user's lifetime value
  let totalSpent = 0;
  for (const order of user.orders) {
    if (order.status === 'completed') {
      totalSpent += order.total;
    }
  }
  
  // Determine user tier
  let tier = 'bronze';
  if (totalSpent > 10000) tier = 'gold';
  else if (totalSpent > 5000) tier = 'silver';
  
  return { totalSpent, tier };
}
```

**✅ Correct:**
```typescript
function analyzeUser(user: User) {
  const totalSpent = calculateLifetimeValue(user);
  const tier = determineUserTier(totalSpent);
  return { totalSpent, tier };
}

function calculateLifetimeValue(user: User): number {
  return user.orders
    .filter(order => order.status === 'completed')
    .reduce((sum, order) => sum + order.total, 0);
}

function determineUserTier(totalSpent: number): string {
  if (totalSpent > 10000) return 'gold';
  if (totalSpent > 5000) return 'silver';
  return 'bronze';
}
```

**Impact:** HIGH - Self-documenting code

**Reference:** Refactoring: Extract Method

---

### 3. medium-primitive-obsession

**Why it matters:** Primitives lack validation and business rules.

**Detection:**
- Look for string/number types representing domain concepts
- Check for validation scattered across codebase
- Search for repeated validation logic

**❌ Incorrect:**
```typescript
function sendEmail(to: string, subject: string, body: string) {
  // Email validation scattered everywhere
  if (!to.includes('@')) {
    throw new Error('Invalid email');
  }
  // ...
}

function subscribeUser(email: string) {
  if (!email.includes('@') || email.length < 3) {
    throw new Error('Invalid email');
  }
  // ...
}
```

**✅ Correct:**
```typescript
class Email {
  private constructor(private readonly value: string) {}
  
  static create(value: string): Email {
    if (!value.includes('@') || value.length < 3) {
      throw new Error('Invalid email format');
    }
    return new Email(value);
  }
  
  toString(): string {
    return this.value;
  }
}

function sendEmail(to: Email, subject: string, body: string) {
  // No validation needed - Email guarantees validity
}

function subscribeUser(email: Email) {
  // Validation centralized in Email class
}
```

**Impact:** MEDIUM-HIGH - Centralizes validation and business rules

**Reference:** Refactoring: Replace Data Value with Object

---

### 4. medium-long-parameter-list

**Why it matters:** Functions with >5 parameters are hard to call and understand.

**Detection:**
- Count function parameters
- Look for related parameters passed together
- Check for optional parameter proliferation

**❌ Incorrect:**
```typescript
function createUser(
  firstName: string,
  lastName: string,
  email: string,
  phone: string,
  address: string,
  city: string,
  zipCode: string,
  country: string
) {
  // Too many parameters!
}

// Hard to call
createUser('John', 'Doe', 'john@example.com', '555-1234', '123 Main St', 'NYC', '10001', 'USA');
```

**✅ Correct:**
```typescript
interface UserData {
  personalInfo: {
    firstName: string;
    lastName: string;
  };
  contact: {
    email: string;
    phone: string;
  };
  address: {
    street: string;
    city: string;
    zipCode: string;
    country: string;
  };
}

function createUser(userData: UserData) {
  // Clear, organized parameters
}

// Easy to call with named fields
createUser({
  personalInfo: { firstName: 'John', lastName: 'Doe' },
  contact: { email: 'john@example.com', phone: '555-1234' },
  address: { street: '123 Main St', city: 'NYC', zipCode: '10001', country: 'USA' }
});
```

**Impact:** MEDIUM - Improves call sites and extensibility

**Reference:** Refactoring: Introduce Parameter Object

---

### 5. medium-data-clumps

**Why it matters:** Parameters that always appear together suggest a missing abstraction.

**Detection:**
- Find same 3+ parameters in multiple functions
- Check for related data passed separately
- Search for parallel parameter lists

**❌ Incorrect:**
```typescript
function calculateShipping(weight: number, length: number, width: number, height: number) {}
function estimateCost(weight: number, length: number, width: number, height: number) {}
function validatePackage(weight: number, length: number, width: number, height: number) {}
```

**✅ Correct:**
```typescript
interface PackageDimensions {
  weight: number;
  length: number;
  width: number;
  height: number;
}

function calculateShipping(dimensions: PackageDimensions) {}
function estimateCost(dimensions: PackageDimensions) {}
function validatePackage(dimensions: PackageDimensions) {}
```

**Impact:** MEDIUM - Reduces parameter duplication

**Reference:** Refactoring: Extract Class

---

### 6. medium-feature-envy

**Why it matters:** Methods that primarily use data from another class should move there.

**Detection:**
- Find methods using more external data than local
- Check for chains of property access
- Look for methods that don't use `this`

**❌ Incorrect:**
```typescript
class OrderReport {
  generateSummary(order: Order) {
    // Uses all Order data
    const total = order.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const tax = total * order.taxRate;
    const shipping = order.shippingCost;
    return total + tax + shipping;
  }
}
```

**✅ Correct:**
```typescript
class Order {
  calculateTotal(): number {
    const subtotal = this.items.reduce((sum, item) => sum + item.price * item.quantity, 0);
    const tax = subtotal * this.taxRate;
    return subtotal + tax + this.shippingCost;
  }
}

class OrderReport {
  generateSummary(order: Order) {
    return order.calculateTotal(); // Delegates to Order
  }
}
```

**Impact:** MEDIUM - Improves cohesion

**Reference:** Refactoring: Move Method

---

### 7. medium-magic-constants

**Why it matters:** Unnamed numbers lack context and are hard to change.

**Detection:**
- Look for numeric literals (except 0, 1)
- Check for repeated string literals
- Search for unexplained thresholds

**❌ Incorrect:**
```typescript
function calculateDiscount(total: number, userType: string) {
  if (userType === 'premium') {
    return total * 0.15;
  }
  if (total > 100) {
    return total * 0.10;
  }
  return 0;
}
```

**✅ Correct:**
```typescript
const PREMIUM_DISCOUNT_RATE = 0.15;
const STANDARD_DISCOUNT_RATE = 0.10;
const MINIMUM_ORDER_FOR_DISCOUNT = 100;
const USER_TYPE_PREMIUM = 'premium';

function calculateDiscount(total: number, userType: string) {
  if (userType === USER_TYPE_PREMIUM) {
    return total * PREMIUM_DISCOUNT_RATE;
  }
  if (total > MINIMUM_ORDER_FOR_DISCOUNT) {
    return total * STANDARD_DISCOUNT_RATE;
  }
  return 0;
}
```

**Impact:** MEDIUM - Improves clarity and maintainability

**Reference:** Refactoring: Replace Magic Number with Symbolic Constant

---

### 8. medium-builder-pattern

**Why it matters:** Complex object construction with many optional fields benefits from fluent API.

**Detection:**
- Look for constructors with many optional parameters
- Check for step-by-step object building
- Search for configuration objects

**❌ Incorrect:**
```typescript
const request = new HttpRequest({
  url: '/api/users',
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(data),
  timeout: 5000,
  retries: 3,
  cache: false
});
```

**✅ Correct:**
```typescript
class HttpRequestBuilder {
  private config: Partial<HttpRequestConfig> = {};
  
  url(url: string) {
    this.config.url = url;
    return this;
  }
  
  post(body: any) {
    this.config.method = 'POST';
    this.config.body = JSON.stringify(body);
    return this;
  }
  
  withTimeout(ms: number) {
    this.config.timeout = ms;
    return this;
  }
  
  withRetries(count: number) {
    this.config.retries = count;
    return this;
  }
  
  build(): HttpRequest {
    return new HttpRequest(this.config);
  }
}

const request = new HttpRequestBuilder()
  .url('/api/users')
  .post(data)
  .withTimeout(5000)
  .withRetries(3)
  .build();
```

**Impact:** MEDIUM - Improves complex object construction

**Reference:** Design Patterns: Builder

---

### 9. medium-factory-constructor

**Why it matters:** Factory methods enable validation and polymorphic construction.

**Detection:**
- Look for constructor validation that can fail
- Check for conditional object creation
- Search for subclass selection logic

**❌ Incorrect:**
```typescript
class User {
  constructor(email: string, role: string) {
    // Validation in constructor - throws!
    if (!email.includes('@')) {
      throw new Error('Invalid email');
    }
    this.email = email;
    this.role = role;
  }
}

const user = new User('invalid-email', 'admin'); // Runtime error!
```

**✅ Correct:**
```typescript
class User {
  private constructor(
    private email: string,
    private role: string
  ) {}
  
  static create(email: string, role: string): User | Error {
    if (!email.includes('@')) {
      return new Error('Invalid email format');
    }
    if (!['admin', 'user'].includes(role)) {
      return new Error('Invalid role');
    }
    return new User(email, role);
  }
}

const userResult = User.create('user@example.com', 'admin');
if (userResult instanceof Error) {
  console.error(userResult.message);
} else {
  // userResult is User
}
```

**Impact:** MEDIUM - Safer object creation

**Reference:** Design Patterns: Factory Method

---

### 10. medium-introduce-parameter-object

**Why it matters:** Related parameters suggest a cohesive concept.

**Detection:**
- Find 3+ parameters that represent a concept
- Check for parameters validated together
- Look for parameters transformed together

**❌ Incorrect:**
```typescript
function scheduleTask(
  name: string,
  hour: number,
  minute: number,
  dayOfWeek: number
) {
  // Related time parameters scattered
}
```

**✅ Correct:**
```typescript
interface ScheduleTime {
  hour: number;
  minute: number;
  dayOfWeek: number;
}

function scheduleTask(name: string, time: ScheduleTime) {
  // Time parameters grouped
}
```

**Impact:** MEDIUM - Reduces parameter count

**Reference:** Refactoring: Introduce Parameter Object

---

### 11. medium-switch-to-strategy

**Why it matters:** Type switches are hard to extend and violate Open/Closed Principle.

**Detection:**
- Look for switch/if-else on type field
- Check for parallel conditionals
- Search for type checking with typeof/instanceof

**❌ Incorrect:**
```typescript
function calculateArea(shape: Shape) {
  switch (shape.type) {
    case 'circle':
      return Math.PI * shape.radius ** 2;
    case 'square':
      return shape.side ** 2;
    case 'rectangle':
      return shape.width * shape.height;
    default:
      throw new Error('Unknown shape');
  }
}
```

**✅ Correct:**
```typescript
interface Shape {
  calculateArea(): number;
}

class Circle implements Shape {
  constructor(private radius: number) {}
  calculateArea() {
    return Math.PI * this.radius ** 2;
  }
}

class Square implements Shape {
  constructor(private side: number) {}
  calculateArea() {
    return this.side ** 2;
  }
}

function calculateArea(shape: Shape) {
  return shape.calculateArea(); // Polymorphic!
}
```

**Impact:** MEDIUM - Improves extensibility

**Reference:** Refactoring: Replace Conditional with Polymorphism

---

### 12. medium-callback-hell

**Why it matters:** Nested callbacks are hard to read and error-prone.

**Detection:**
- Count callback nesting depth (>3 is bad)
- Look for pyramid-shaped code
- Check for error handling duplication

**❌ Incorrect:**
```typescript
function loadUserData(userId: string, callback: Function) {
  db.users.find(userId, (err, user) => {
    if (err) return callback(err);
    db.posts.findByUser(user.id, (err, posts) => {
      if (err) return callback(err);
      db.comments.findByPosts(posts, (err, comments) => {
        if (err) return callback(err);
        callback(null, { user, posts, comments });
      });
    });
  });
}
```

**✅ Correct:**
```typescript
async function loadUserData(userId: string) {
  const user = await db.users.find(userId);
  const posts = await db.posts.findByUser(user.id);
  const comments = await db.comments.findByPosts(posts);
  return { user, posts, comments };
}
```

**Impact:** MEDIUM - Dramatically improves readability

**Reference:** Node.js Best Practices: Async/Await

---

### 13. medium-law-of-demeter

**Why it matters:** Chained calls create tight coupling and fragile code.

**Detection:**
- Look for chains like `a.b.c.d()`
- Check for property access through multiple objects
- Search for repeated navigation paths

**❌ Incorrect:**
```typescript
function getStreetName(user: User): string {
  return user.profile.address.street.name; // Chain of 4!
}

// Breaks if any intermediate is null/undefined
```

**✅ Correct:**
```typescript
class User {
  getStreetName(): string | undefined {
    return this.profile?.getStreetName();
  }
}

class Profile {
  getStreetName(): string | undefined {
    return this.address?.getStreetName();
  }
}

class Address {
  getStreetName(): string {
    return this.street.name;
  }
}

function getStreetName(user: User): string | undefined {
  return user.getStreetName(); // Single call!
}
```

**Impact:** LOW-MEDIUM - Reduces coupling

**Reference:** Refactoring: Hide Delegate

---

## Usage Examples

**Refactor complex function:**
```
Find code smells in this function and suggest refactoring
```

**Review for maintainability:**
```
Check this code for design pattern improvements
```

**Simplify legacy code:**
```
Reduce complexity in this module
```

## Summary

Design patterns and refactoring improve:
- ✅ Code readability (Extract Method, Named Concepts)
- ✅ Maintainability (Single Responsibility)
- ✅ Extensibility (Strategy Pattern, Builder)
- ✅ Testability (Smaller Functions, Clear Dependencies)

Apply patterns when they simplify code, not dogmatically.
