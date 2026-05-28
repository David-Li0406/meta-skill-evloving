# Design Patterns Quick Reference

Common patterns for solving recurring software design problems.

## Creational Patterns

### Factory Pattern

Use when: Object creation logic is complex or needs to be centralized.

```typescript
interface Logger {
  log(message: string): void;
}

class ConsoleLogger implements Logger {
  log(message: string) { console.log(message); }
}

class FileLogger implements Logger {
  log(message: string) { /* write to file */ }
}

class CloudLogger implements Logger {
  log(message: string) { /* send to cloud service */ }
}

// Factory
class LoggerFactory {
  static create(type: 'console' | 'file' | 'cloud'): Logger {
    switch (type) {
      case 'console': return new ConsoleLogger();
      case 'file': return new FileLogger();
      case 'cloud': return new CloudLogger();
      default: throw new Error(`Unknown logger type: ${type}`);
    }
  }
}

// Usage
const logger = LoggerFactory.create(process.env.LOG_TYPE);
```

### Builder Pattern

Use when: Object has many optional parameters or complex construction.

```typescript
class QueryBuilder {
  private table: string = '';
  private columns: string[] = ['*'];
  private conditions: string[] = [];
  private orderBy: string[] = [];
  private limitValue?: number;

  from(table: string) {
    this.table = table;
    return this;
  }

  select(...columns: string[]) {
    this.columns = columns;
    return this;
  }

  where(condition: string) {
    this.conditions.push(condition);
    return this;
  }

  order(column: string, direction: 'ASC' | 'DESC' = 'ASC') {
    this.orderBy.push(`${column} ${direction}`);
    return this;
  }

  limit(n: number) {
    this.limitValue = n;
    return this;
  }

  build(): string {
    let query = `SELECT ${this.columns.join(', ')} FROM ${this.table}`;
    if (this.conditions.length) {
      query += ` WHERE ${this.conditions.join(' AND ')}`;
    }
    if (this.orderBy.length) {
      query += ` ORDER BY ${this.orderBy.join(', ')}`;
    }
    if (this.limitValue) {
      query += ` LIMIT ${this.limitValue}`;
    }
    return query;
  }
}

// Usage
const query = new QueryBuilder()
  .from('users')
  .select('id', 'name', 'email')
  .where('active = true')
  .where('role = "admin"')
  .order('created_at', 'DESC')
  .limit(10)
  .build();
```

### Singleton Pattern

Use when: Exactly one instance should exist (use sparingly!).

```typescript
// Modern approach: module-level singleton
// database.ts
class Database {
  private constructor() { /* private */ }

  private static instance: Database;

  static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }

  query(sql: string) { /* ... */ }
}

export const db = Database.getInstance();

// Better: Just export an instance
// config.ts
export const config = {
  apiUrl: process.env.API_URL,
  debug: process.env.DEBUG === 'true'
};
```

⚠️ **Warning**: Singletons make testing difficult. Prefer dependency injection.

## Structural Patterns

### Adapter Pattern

Use when: You need to use a class with an incompatible interface.

```typescript
// Third-party payment SDK with awkward interface
class LegacyPaymentSDK {
  makePayment(cents: number, cardNum: string, exp: string, cvv: string) {
    // ...
  }
}

// Our expected interface
interface PaymentGateway {
  charge(amount: number, card: CreditCard): Promise<PaymentResult>;
}

interface CreditCard {
  number: string;
  expiry: string;
  cvv: string;
}

// Adapter
class LegacyPaymentAdapter implements PaymentGateway {
  constructor(private sdk: LegacyPaymentSDK) {}

  async charge(amount: number, card: CreditCard): Promise<PaymentResult> {
    const cents = Math.round(amount * 100);
    this.sdk.makePayment(cents, card.number, card.expiry, card.cvv);
    return { success: true };
  }
}

// Usage
const gateway: PaymentGateway = new LegacyPaymentAdapter(new LegacyPaymentSDK());
```

### Decorator Pattern

Use when: You need to add behavior to objects dynamically.

```typescript
interface Coffee {
  cost(): number;
  description(): string;
}

class SimpleCoffee implements Coffee {
  cost() { return 2; }
  description() { return 'Coffee'; }
}

// Decorators
class MilkDecorator implements Coffee {
  constructor(private coffee: Coffee) {}
  cost() { return this.coffee.cost() + 0.5; }
  description() { return this.coffee.description() + ', Milk'; }
}

class SugarDecorator implements Coffee {
  constructor(private coffee: Coffee) {}
  cost() { return this.coffee.cost() + 0.25; }
  description() { return this.coffee.description() + ', Sugar'; }
}

// Usage
let coffee: Coffee = new SimpleCoffee();
coffee = new MilkDecorator(coffee);
coffee = new SugarDecorator(coffee);
console.log(coffee.description()); // "Coffee, Milk, Sugar"
console.log(coffee.cost()); // 2.75
```

### Facade Pattern

Use when: You need to simplify a complex subsystem.

```typescript
// Complex subsystems
class VideoDecoder { decode(file: string) { /* ... */ } }
class AudioDecoder { decode(file: string) { /* ... */ } }
class SubtitleParser { parse(file: string) { /* ... */ } }
class VideoRenderer { render(frames: Frame[]) { /* ... */ } }

// Facade
class VideoPlayer {
  private videoDecoder = new VideoDecoder();
  private audioDecoder = new AudioDecoder();
  private subtitleParser = new SubtitleParser();
  private renderer = new VideoRenderer();

  play(videoFile: string, subtitleFile?: string) {
    const videoFrames = this.videoDecoder.decode(videoFile);
    const audioStream = this.audioDecoder.decode(videoFile);
    const subtitles = subtitleFile
      ? this.subtitleParser.parse(subtitleFile)
      : null;
    this.renderer.render(videoFrames);
  }

  pause() { /* ... */ }
  stop() { /* ... */ }
}

// Usage - simple interface
const player = new VideoPlayer();
player.play('movie.mp4', 'movie.srt');
```

## Behavioral Patterns

### Strategy Pattern

Use when: You need interchangeable algorithms.

```typescript
interface CompressionStrategy {
  compress(data: Buffer): Buffer;
  decompress(data: Buffer): Buffer;
}

class ZipCompression implements CompressionStrategy {
  compress(data: Buffer) { /* zip logic */ return data; }
  decompress(data: Buffer) { /* unzip logic */ return data; }
}

class GzipCompression implements CompressionStrategy {
  compress(data: Buffer) { /* gzip logic */ return data; }
  decompress(data: Buffer) { /* gunzip logic */ return data; }
}

class FileProcessor {
  constructor(private compression: CompressionStrategy) {}

  processFile(file: Buffer): Buffer {
    const compressed = this.compression.compress(file);
    // ... do something
    return compressed;
  }

  setStrategy(strategy: CompressionStrategy) {
    this.compression = strategy;
  }
}

// Usage
const processor = new FileProcessor(new ZipCompression());
processor.processFile(buffer);
processor.setStrategy(new GzipCompression());  // Switch at runtime
```

### Observer Pattern

Use when: Objects need to be notified of changes.

```typescript
type Listener<T> = (event: T) => void;

class EventEmitter<Events extends Record<string, any>> {
  private listeners = new Map<keyof Events, Set<Listener<any>>>();

  on<K extends keyof Events>(event: K, listener: Listener<Events[K]>) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(listener);
    return () => this.off(event, listener);  // Return unsubscribe
  }

  off<K extends keyof Events>(event: K, listener: Listener<Events[K]>) {
    this.listeners.get(event)?.delete(listener);
  }

  emit<K extends keyof Events>(event: K, data: Events[K]) {
    this.listeners.get(event)?.forEach(listener => listener(data));
  }
}

// Usage
interface AppEvents {
  userLoggedIn: { userId: string };
  orderPlaced: { orderId: string; total: number };
}

const events = new EventEmitter<AppEvents>();

const unsubscribe = events.on('orderPlaced', (data) => {
  console.log(`Order ${data.orderId} for $${data.total}`);
});

events.emit('orderPlaced', { orderId: '123', total: 99.99 });
unsubscribe();  // Clean up
```

### Command Pattern

Use when: You need to encapsulate operations (undo, queue, log).

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
    this.editor.insertAt(this.position, this.text);
  }

  undo() {
    this.editor.deleteAt(this.position, this.text.length);
  }
}

class CommandHistory {
  private history: Command[] = [];
  private position = -1;

  execute(command: Command) {
    // Remove any "future" commands if we're not at the end
    this.history = this.history.slice(0, this.position + 1);
    command.execute();
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

## Pattern Selection Guide

| Problem | Pattern |
|---------|---------|
| Complex object creation | Factory, Builder |
| Need exactly one instance | Singleton (prefer DI) |
| Incompatible interfaces | Adapter |
| Add behavior dynamically | Decorator |
| Simplify complex system | Facade |
| Swappable algorithms | Strategy |
| React to state changes | Observer |
| Undo/redo, queuing | Command |
| Tree structures | Composite |
| Lazy initialization | Proxy |
