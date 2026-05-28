---
name: solid-principles
description: Use during implementation when designing modules, functions, and components requiring SOLID principles for maintainable, flexible architecture.
---

# SOLID Principles

Apply SOLID design principles for maintainable, flexible code architecture.

## The Five Principles

### 1. Single Responsibility Principle (SRP)

### A module should have one, and only one, reason to change

### TypeScript Pattern

```typescript
// BAD - Multiple responsibilities
class UserComponent {
  render() { /* UI */ }
  fetchData() { /* API */ }
  formatDate() { /* Formatting */ }
  validateInput() { /* Validation */ }
}

// GOOD - Single responsibility
function UserProfile({ user }: Props) {
  return <View>{/* UI only */}</View>;
}

function useUserData(id: string) {
  // Data fetching only
}

function formatUserDate(date: Date): string {
  // Formatting only
}
```

**Ask yourself:** "What is the ONE thing this module does?"

### 2. Open/Closed Principle (OCP)

**Software entities should be open for extension, closed for modification.**

### TypeScript Pattern (Composition)

```typescript
// BAD - Requires modification for new types
function renderItem(item: Item) {
  if (item.type === 'gig') {
    return <TaskCard />;
  } else if (item.type === 'shift') {
    return <WorkPeriodCard />;
  }
  // Have to modify this function for new types
}

// GOOD - Extension through props
interface CardRenderer {
  (item: Item): ReactElement;
}

const renderers: Record<string, CardRenderer> = {
  gig: (item) => <TaskCard gig={item} />,
  shift: (item) => <WorkPeriodCard shift={item} />,
  // Add new types here without modifying renderItem
};

function renderItem(item: Item) {
  const renderer = renderers[item.type];
  return renderer ? renderer(item) : <DefaultCard item={item} />;
}
```

**Ask yourself:** "Can I add new functionality without changing existing code?"

### 3. Liskov Substitution Principle (LSP)

### Subtypes must be substitutable for their base types

### TypeScript Pattern (LSP)

```typescript
// BAD - Violates LSP
class Bird {
  fly(): void {
    /* flies */
  }
}

class Penguin extends Bird {
  fly(): void {
    throw new Error("Penguins cannot fly"); // Breaks contract
  }
}

// GOOD - Correct abstraction
interface Bird {
  move(): void;
}

class FlyingBird implements Bird {
  move(): void {
    this.fly();
  }
  private fly(): void {
    /* flies */
  }
}

class SwimmingBird implements Bird {
  move(): void {
    this.swim();
  }
  private swim(): void {
    /* swims */
  }
}
```

**Ask yourself:** "Can I replace this with its parent/interface without
breaking behavior?"

### 4. Interface Segregation Principle (ISP)

**Clients should not be forced to depend on interfaces they don't use.**

### TypeScript Pattern (ISP)

```typescript
// BAD - Fat interface
interface User {
  work(): void;
  takeBreak(): void;
  clockIn(): void;
  clockOut(): void;
  receiveBenefits(): void;
  // Not all users need all methods
}

// GOOD - Segregated interfaces
interface Workable {
  work(): void;
}

interface TimeTrackable {
  clockIn(): void;
  clockOut(): void;
}

interface BenefitsEligible {
  receiveBenefits(): void;
}

// Compose only what you need
type FullTimeUser = Workable & TimeTrackable & BenefitsEligible;
type ContractUser = Workable & TimeTrackable;
type TaskUser = Workable;
```

**Ask yourself:** "Does this interface force implementations to define unused methods?"

### 5. Dependency Inversion Principle (DIP)

### Depend on abstractions, not concretions

### TypeScript Pattern (DIP)

```typescript
// BAD - Direct dependency
class UserManager {
  private api = new StripeAPI(); // Tightly coupled

  async processPayment(amount: number) {
    return this.api.charge(amount);
  }
}

// GOOD - Depend on abstraction
interface PaymentAPI {
  charge(amount: number): Promise<Transaction>;
}

class UserManager {
  constructor(private paymentAPI: PaymentAPI) {} // Injected

  async processPayment(amount: number) {
    return this.paymentAPI.charge(amount);
  }
}

// Usage
const stripeAPI: PaymentAPI = new StripeAPI();
const manager = new UserManager(stripeAPI);
```

**Ask yourself:** "Can I swap implementations without changing dependent code?"

## Application Checklist

### Before writing new code

- [ ] Identify the single responsibility
- [ ] Design for extension points (behaviours, interfaces)
- [ ] Define abstractions before implementations
- [ ] Keep interfaces minimal and focused

### During implementation

- [ ] Each module has ONE reason to change (SRP)
- [ ] New features extend, don't modify (OCP)
- [ ] Implementations honor contracts (LSP)
- [ ] Interfaces are minimal (ISP)
- [ ] Dependencies are injected/configurable (DIP)

### During code review

- [ ] Are responsibilities clearly separated?
- [ ] Can we add features without modifying existing code?
- [ ] Do all implementations fulfill their contracts?
- [ ] Are interfaces focused and minimal?
- [ ] Are dependencies abstracted?

## Common Violations in Codebase

### SRP Violation

- GraphQL resolvers that also contain business logic (use command handlers)
- Components that fetch data AND render (use hooks + presentation components)

### OCP Violation

- Long if/else or case statements for types (use behaviours/polymorphism)
- Hardcoded provider logic (use dependency injection)

### LSP Violation

- Raising exceptions in implementations when base would return nil/error tuple
- Changing return types between implementations

### ISP Violation

- Fat GraphQL types requiring all fields (use fragments)
- Monolithic component props (split into focused interfaces)

### DIP Violation

- Direct calls to external services (wrap in behaviours)
- Hardcoded Repo calls (inject repository)

## Integration with Existing Skills

### Works with

- `boy-scout-rule`: Apply SOLID when improving code
- `test-driven-development`: Write tests for each responsibility
- `typescript-code-quality-enforcer`: TypeScript interfaces support ISP/DIP

## Remember

**SOLID is about managing dependencies and responsibilities, not about
creating more code.**

Good design emerges from applying these principles pragmatically, not dogmatically.
