# Design Patterns Reference

Quick reference for common patterns and when to apply them.

## Creational Patterns

### Factory Function

Creates objects without exposing creation logic.

**When to use:**
- Object creation involves logic (validation, defaults, configuration)
- You want to hide implementation details
- Creation might return different types based on input

```typescript
function createLogger(config: LoggerConfig): Logger {
  if (config.destination === 'file') {
    return new FileLogger(config.path);
  }
  if (config.destination === 'cloud') {
    return new CloudLogger(config.endpoint);
  }
  return new ConsoleLogger();
}
```

### Builder Pattern

Constructs complex objects step by step.

**When to use:**
- Object has many optional parameters
- Construction requires multiple steps
- You want to prevent invalid intermediate states

```typescript
const query = new QueryBuilder()
  .from('users')
  .where({ field: 'status', op: '=', value: 'active' })
  .orderBy('created_at', 'desc')
  .build();
```

---

## Structural Patterns

### Adapter

Makes incompatible interfaces work together.

**When to use:**
- Integrating third-party libraries
- Supporting multiple implementations
- Migrating between APIs

```typescript
interface EmailService {
  sendEmail(to: string, subject: string, body: string): Promise<void>;
}

class SendGridAdapter implements EmailService {
  constructor(private client: SendGridClient) {}
  
  async sendEmail(to: string, subject: string, body: string) {
    await this.client.send({ to, subject, html: body });
  }
}
```

### Facade

Simplified interface to a complex subsystem.

**When to use:**
- Subsystem is complex to use directly
- Decoupling clients from internals
- Cleaner API for common cases

```typescript
class MediaPlayer {
  play(file: Buffer): void {
    const video = this.videoDecoder.decode(file);
    const audio = this.audioDecoder.decode(file);
    const stream = this.synchronizer.sync(video, audio);
    this.renderer.render(stream);
  }
}
```

### Decorator

Adds behavior dynamically without affecting other objects.

**When to use:**
- Add responsibilities without subclassing
- Behavior should be addable/removable at runtime
- Combining multiple behaviors

```typescript
// Stack decorators
const source = new CompressionDecorator(
  new EncryptionDecorator(
    new FileDataSource('data.txt')
  )
);

source.write(data);  // Encrypts, then compresses, then writes
```

---

## Behavioral Patterns

### Strategy

Defines a family of algorithms, makes them interchangeable.

**When to use:**
- Multiple algorithms for a task
- Algorithm selection at runtime
- Avoiding conditional logic for behavior selection

```typescript
interface PricingStrategy {
  calculatePrice(basePrice: number, quantity: number): number;
}

class RegularPricing implements PricingStrategy {
  calculatePrice(basePrice: number, quantity: number) {
    return basePrice * quantity;
  }
}

class BulkPricing implements PricingStrategy {
  calculatePrice(basePrice: number, quantity: number) {
    const discount = quantity > 100 ? 0.2 : quantity > 50 ? 0.1 : 0;
    return basePrice * quantity * (1 - discount);
  }
}

class PriceCalculator {
  constructor(private strategy: PricingStrategy) {}
  
  setStrategy(strategy: PricingStrategy) {
    this.strategy = strategy;
  }
  
  calculate(basePrice: number, quantity: number) {
    return this.strategy.calculatePrice(basePrice, quantity);
  }
}
```

### Observer / Event Emitter

Objects subscribe to events from another object.

**When to use:**
- One-to-many dependencies
- Decoupling event producers from consumers
- Plugin/extension systems

```typescript
class EventEmitter<Events extends Record<string, any>> {
  private listeners = new Map<keyof Events, Set<Function>>();
  
  on<E extends keyof Events>(event: E, listener: (data: Events[E]) => void) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(listener);
    return () => this.listeners.get(event)?.delete(listener);
  }
  
  emit<E extends keyof Events>(event: E, data: Events[E]) {
    this.listeners.get(event)?.forEach(listener => listener(data));
  }
}

// Usage
interface OrderEvents {
  'order:created': { orderId: string };
  'order:shipped': { orderId: string; trackingNumber: string };
}

const orderEvents = new EventEmitter<OrderEvents>();
orderEvents.on('order:created', ({ orderId }) => sendConfirmationEmail(orderId));
orderEvents.on('order:shipped', ({ trackingNumber }) => notifyCustomer(trackingNumber));
```

### Command

Encapsulates a request as an object.

**When to use:**
- Undo/redo functionality
- Queuing operations
- Logging/auditing actions

```typescript
interface Command {
  execute(): void;
  undo(): void;
}

class AddTextCommand implements Command {
  constructor(
    private editor: TextEditor,
    private text: string,
    private position: number
  ) {}
  
  execute() {
    this.editor.insert(this.text, this.position);
  }
  
  undo() {
    this.editor.delete(this.position, this.text.length);
  }
}

class CommandHistory {
  private history: Command[] = [];
  private position = -1;
  
  execute(command: Command) {
    command.execute();
    this.history = this.history.slice(0, this.position + 1);
    this.history.push(command);
    this.position++;
  }
  
  undo() {
    if (this.position >= 0) {
      this.history[this.position].undo();
      this.position--;
    }
  }
  
  redo() {
    if (this.position < this.history.length - 1) {
      this.position++;
      this.history[this.position].execute();
    }
  }
}
```

---

## Repository Pattern

Abstracts data access behind a collection-like interface.

**When to use:**
- Decoupling business logic from data access
- Testing with in-memory implementations
- Switching data sources

```typescript
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<void>;
  delete(id: string): Promise<void>;
}

// Production implementation
class PostgresUserRepository implements UserRepository {
  constructor(private db: Database) {}
  
  async findById(id: string) {
    return this.db.query('SELECT * FROM users WHERE id = $1', [id]);
  }
  // ...
}

// Test implementation
class InMemoryUserRepository implements UserRepository {
  private users = new Map<string, User>();
  
  async findById(id: string) {
    return this.users.get(id) ?? null;
  }
  // ...
}
```

---

## Result Type Pattern

Represents success or failure without exceptions.

**When to use:**
- Functions that can fail in expected ways
- Forcing callers to handle errors
- Avoiding exception overhead

```typescript
type Result<T, E = Error> = 
  | { ok: true; value: T }
  | { ok: false; error: E };

function parseJson<T>(text: string): Result<T, SyntaxError> {
  try {
    return { ok: true, value: JSON.parse(text) };
  } catch (e) {
    return { ok: false, error: e as SyntaxError };
  }
}

// Usage forces error handling
const result = parseJson<Config>(text);
if (result.ok) {
  console.log(result.value.setting);
} else {
  console.error('Parse failed:', result.error.message);
}
```

---

## Pattern Selection Guide

| Need | Pattern |
|------|---------|
| Create objects with configuration | Factory |
| Build complex objects step by step | Builder |
| Make incompatible interfaces work | Adapter |
| Simplify complex subsystem | Facade |
| Add behavior without subclassing | Decorator |
| Choose algorithm at runtime | Strategy |
| Decouple event producers/consumers | Observer |
| Undo/redo, command queuing | Command |
| Abstract data access | Repository |
| Handle success/failure explicitly | Result Type |

---

## Anti-Patterns

### Overengineering

Don't add patterns "just in case." Add them when:
- You have a concrete problem the pattern solves
- The complexity is justified by the benefit
- Simpler solutions have proven inadequate

### Pattern Obsession

Patterns are tools, not goals. A simple function is often better than a pattern.

```typescript
// Overengineered
const formatter = new FormatterFactory()
  .createFormatter(new FormattingStrategy())
  .setDecorator(new CurrencyDecorator())
  .format(value);

// Simple
const formatted = formatCurrency(value);
```

### Wrong Pattern for the Job

Each pattern has a specific purpose. Using the wrong one adds complexity without solving the problem.
