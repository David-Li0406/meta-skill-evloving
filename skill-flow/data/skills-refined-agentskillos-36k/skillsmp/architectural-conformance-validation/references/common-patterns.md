# Common Design Patterns Reference

Quick reference for recognizing and validating standard design patterns in code.

---

## Creational Patterns

### Singleton

**Intent**: Ensure a class has only one instance and provide global access point

**Structure**:
```typescript
class Singleton {
  private static instance?: Singleton;

  private constructor() {
    // Private constructor prevents instantiation
  }

  public static getInstance(): Singleton {
    if (!Singleton.instance) {
      Singleton.instance = new Singleton();
    }
    return Singleton.instance;
  }
}
```

**Recognition Checklist**:
- [ ] Private constructor
- [ ] Static instance variable
- [ ] Static getInstance() method
- [ ] Thread-safe (if needed)

**Common Violations**:
- ❌ Public constructor
- ❌ No getInstance() method
- ❌ Multiple instance creation possible

**Use Cases**: Configuration managers, logging services, database connections

---

### Factory Method

**Intent**: Define interface for creating objects, let subclasses decide which class to instantiate

**Structure**:
```typescript
interface Product {
  operation(): string;
}

class ConcreteProductA implements Product {
  operation() { return "Product A"; }
}

class ConcreteProductB implements Product {
  operation() { return "Product B"; }
}

abstract class Creator {
  abstract factoryMethod(): Product;

  someOperation() {
    const product = this.factoryMethod();
    return product.operation();
  }
}

class ConcreteCreatorA extends Creator {
  factoryMethod() { return new ConcreteProductA(); }
}
```

**Recognition Checklist**:
- [ ] Abstract creator class/interface
- [ ] Factory method declared (abstract or default)
- [ ] Concrete creators override factory method
- [ ] Returns product interface, not concrete class

**Common Violations**:
- ❌ Direct instantiation (new ConcreteProduct)
- ❌ Factory returns concrete type, not interface
- ❌ Creator depends on concrete products

**Use Cases**: UI component creation, document parsers, database connections

---

### Builder

**Intent**: Separate construction of complex object from representation

**Structure**:
```typescript
class Product {
  parts: string[] = [];
}

interface Builder {
  buildPartA(): void;
  buildPartB(): void;
  getResult(): Product;
}

class ConcreteBuilder implements Builder {
  private product = new Product();

  buildPartA() { this.product.parts.push("PartA"); }
  buildPartB() { this.product.parts.push("PartB"); }
  getResult() { return this.product; }
}

class Director {
  construct(builder: Builder) {
    builder.buildPartA();
    builder.buildPartB();
  }
}
```

**Recognition Checklist**:
- [ ] Builder interface with build methods
- [ ] Concrete builder implements interface
- [ ] Director orchestrates building steps
- [ ] getResult() returns constructed product

**Common Violations**:
- ❌ Constructor with many parameters instead of builder
- ❌ No method chaining for fluent API
- ❌ Mutable product after build

**Use Cases**: Complex configuration objects, query builders, document construction

---

### Dependency Injection

**Intent**: Provide dependencies from outside rather than creating them internally

**Structure**:
```typescript
interface Logger {
  log(message: string): void;
}

class ConsoleLogger implements Logger {
  log(message: string) { console.log(message); }
}

// ❌ BAD: Direct instantiation
class ServiceBad {
  private logger = new ConsoleLogger();
}

// ✅ GOOD: Dependency injected
class ServiceGood {
  constructor(private logger: Logger) {}
}

// Usage
const logger = new ConsoleLogger();
const service = new ServiceGood(logger);
```

**Recognition Checklist**:
- [ ] Dependencies passed via constructor
- [ ] Dependencies are interfaces, not concrete classes
- [ ] No direct instantiation of dependencies
- [ ] Dependencies mockable/testable

**Common Violations**:
- ❌ new DependencyClass() inside component
- ❌ Depending on concrete classes
- ❌ Global state or singletons

**Use Cases**: Services, repositories, business logic

---

## Structural Patterns

### Adapter

**Intent**: Convert interface of class into another interface clients expect

**Structure**:
```typescript
class Target {
  request(): string { return "Target"; }
}

class Adaptee {
  specificRequest(): string { return "Adaptee"; }
}

class Adapter extends Target {
  constructor(private adaptee: Adaptee) { super(); }

  request(): string {
    return `Adapter: ${this.adaptee.specificRequest()}`;
  }
}
```

**Recognition Checklist**:
- [ ] Target interface defines domain-specific interface
- [ ] Adaptee has incompatible interface
- [ ] Adapter implements Target interface
- [ ] Adapter delegates to Adaptee

**Common Violations**:
- ❌ Modifying Adaptee directly
- ❌ Adapter exposes Adaptee methods
- ❌ Not implementing target interface

**Use Cases**: Legacy system integration, third-party library wrapping

---

### Decorator

**Intent**: Attach additional responsibilities to object dynamically

**Structure**:
```typescript
interface Component {
  operation(): string;
}

class ConcreteComponent implements Component {
  operation() { return "ConcreteComponent"; }
}

abstract class Decorator implements Component {
  constructor(protected component: Component) {}
  operation() { return this.component.operation(); }
}

class ConcreteDecoratorA extends Decorator {
  operation() {
    return `ConcreteDecoratorA(${super.operation()})`;
  }
}
```

**Recognition Checklist**:
- [ ] Component interface defines operations
- [ ] Concrete component implements interface
- [ ] Decorator has component reference
- [ ] Decorator forwards requests to component

**Common Violations**:
- ❌ Modifying original class instead of wrapping
- ❌ Decorator doesn't implement same interface
- ❌ Breaking decorator chain

**Use Cases**: UI components, stream processing, logging wrappers

---

### Facade

**Intent**: Provide unified interface to set of interfaces in subsystem

**Structure**:
```typescript
class SubsystemA {
  operationA() { return "A"; }
}

class SubsystemB {
  operationB() { return "B"; }
}

class Facade {
  constructor(
    private a: SubsystemA,
    private b: SubsystemB
  ) {}

  operation() {
    return `${this.a.operationA()}, ${this.b.operationB()}`;
  }
}
```

**Recognition Checklist**:
- [ ] Complex subsystem with many classes
- [ ] Facade provides simple interface
- [ ] Facade delegates to subsystem
- [ ] Clients use facade, not subsystem directly

**Common Violations**:
- ❌ Exposing all subsystem complexity
- ❌ Facade has business logic
- ❌ Facade becomes god object

**Use Cases**: Library wrappers, API clients, complex initialization

---

### Proxy

**Intent**: Provide surrogate or placeholder for another object to control access

**Structure**:
```typescript
interface Subject {
  request(): void;
}

class RealSubject implements Subject {
  request() { console.log("RealSubject"); }
}

class Proxy implements Subject {
  constructor(private realSubject: RealSubject) {}

  request() {
    if (this.checkAccess()) {
      this.realSubject.request();
      this.logAccess();
    }
  }

  private checkAccess() { return true; }
  private logAccess() { console.log("Logged"); }
}
```

**Recognition Checklist**:
- [ ] Subject interface defines operations
- [ ] Real subject implements interface
- [ ] Proxy implements same interface
- [ ] Proxy controls access to real subject

**Common Violations**:
- ❌ Proxy doesn't implement subject interface
- ❌ Direct access to real subject possible
- ❌ Proxy has duplicate logic

**Use Cases**: Lazy loading, access control, caching, logging

---

## Behavioral Patterns

### Observer

**Intent**: Define one-to-many dependency so when one object changes state, dependents notified

**Structure**:
```typescript
interface Observer {
  update(subject: Subject): void;
}

class Subject {
  private observers: Observer[] = [];
  private state: number = 0;

  attach(observer: Observer) {
    this.observers.push(observer);
  }

  setState(state: number) {
    this.state = state;
    this.notify();
  }

  private notify() {
    for (const observer of this.observers) {
      observer.update(this);
    }
  }
}

class ConcreteObserver implements Observer {
  update(subject: Subject) {
    console.log("Observer notified");
  }
}
```

**Recognition Checklist**:
- [ ] Subject maintains list of observers
- [ ] attach/detach methods for observers
- [ ] notify() calls update() on all observers
- [ ] Observer interface with update method

**Common Violations**:
- ❌ Tight coupling between subject and observers
- ❌ No way to unsubscribe
- ❌ Circular update loops

**Use Cases**: Event handling, MVC, pub/sub systems

---

### Strategy

**Intent**: Define family of algorithms, encapsulate each, make them interchangeable

**Structure**:
```typescript
interface Strategy {
  execute(data: string[]): string[];
}

class ConcreteStrategyA implements Strategy {
  execute(data: string[]) { return data.sort(); }
}

class ConcreteStrategyB implements Strategy {
  execute(data: string[]) { return data.reverse(); }
}

class Context {
  constructor(private strategy: Strategy) {}

  setStrategy(strategy: Strategy) {
    this.strategy = strategy;
  }

  executeStrategy(data: string[]) {
    return this.strategy.execute(data);
  }
}
```

**Recognition Checklist**:
- [ ] Strategy interface defines algorithm
- [ ] Concrete strategies implement interface
- [ ] Context has strategy reference
- [ ] Strategy changeable at runtime

**Common Violations**:
- ❌ If/else or switch for algorithm selection
- ❌ Context knows about concrete strategies
- ❌ Strategy not changeable at runtime

**Use Cases**: Sorting algorithms, validation rules, payment methods

---

### Command

**Intent**: Encapsulate request as object

**Structure**:
```typescript
interface Command {
  execute(): void;
}

class Receiver {
  action() { console.log("Action"); }
}

class ConcreteCommand implements Command {
  constructor(private receiver: Receiver) {}
  execute() { this.receiver.action(); }
}

class Invoker {
  private command?: Command;

  setCommand(command: Command) {
    this.command = command;
  }

  executeCommand() {
    this.command?.execute();
  }
}
```

**Recognition Checklist**:
- [ ] Command interface with execute method
- [ ] Concrete commands implement interface
- [ ] Commands hold receiver reference
- [ ] Invoker triggers commands

**Common Violations**:
- ❌ Direct method calls instead of commands
- ❌ Command has business logic
- ❌ No undo support when needed

**Use Cases**: UI actions, transaction management, undo/redo

---

### State

**Intent**: Allow object to alter behavior when internal state changes

**Structure**:
```typescript
interface State {
  handle(context: Context): void;
}

class ConcreteStateA implements State {
  handle(context: Context) {
    context.setState(new ConcreteStateB());
  }
}

class ConcreteStateB implements State {
  handle(context: Context) {
    context.setState(new ConcreteStateA());
  }
}

class Context {
  private state: State = new ConcreteStateA();

  setState(state: State) {
    this.state = state;
  }

  request() {
    this.state.handle(this);
  }
}
```

**Recognition Checklist**:
- [ ] State interface defines behavior
- [ ] Concrete states implement interface
- [ ] Context maintains state reference
- [ ] State transitions change behavior

**Common Violations**:
- ❌ Large if/else for state checks
- ❌ State logic in context
- ❌ Invalid state transitions possible

**Use Cases**: Workflow, TCP connection, document lifecycle

---

### Template Method

**Intent**: Define skeleton of algorithm, let subclasses override steps

**Structure**:
```typescript
abstract class AbstractClass {
  templateMethod() {
    this.stepOne();
    this.stepTwo();
    this.stepThree();
  }

  protected stepOne() { console.log("Default step 1"); }
  protected abstract stepTwo(): void;
  protected stepThree() { console.log("Default step 3"); }
}

class ConcreteClass extends AbstractClass {
  protected stepTwo() { console.log("Custom step 2"); }
}
```

**Recognition Checklist**:
- [ ] Template method defines algorithm skeleton
- [ ] Some steps are abstract (must override)
- [ ] Some steps have default implementation
- [ ] Subclasses override primitive operations

**Common Violations**:
- ❌ Overriding template method itself
- ❌ No abstract steps to customize
- ❌ Algorithm not reusable

**Use Cases**: Frameworks, data processing pipelines, test fixtures

---

## Architectural Patterns

### Model-View-Controller (MVC)

**Structure**:
```typescript
// Model
class UserModel {
  constructor(public name: string, public email: string) {}
}

// View
class UserView {
  render(user: UserModel) {
    console.log(`Name: ${user.name}, Email: ${user.email}`);
  }
}

// Controller
class UserController {
  constructor(
    private model: UserModel,
    private view: UserView
  ) {}

  updateUserName(name: string) {
    this.model.name = name;
    this.view.render(this.model);
  }
}
```

**Recognition Checklist**:
- [ ] Model holds data and business logic
- [ ] View displays data
- [ ] Controller handles input and updates
- [ ] Separation of concerns maintained

---

### Repository Pattern

**Structure**:
```typescript
interface UserRepository {
  findById(id: string): User | null;
  save(user: User): void;
  delete(id: string): void;
}

class UserRepositoryImpl implements UserRepository {
  constructor(private db: Database) {}

  findById(id: string) {
    return this.db.query("SELECT * FROM users WHERE id = ?", [id]);
  }

  save(user: User) {
    this.db.execute("INSERT INTO users ...", user);
  }

  delete(id: string) {
    this.db.execute("DELETE FROM users WHERE id = ?", [id]);
  }
}
```

**Recognition Checklist**:
- [ ] Repository interface defines data operations
- [ ] Implementation encapsulates data access
- [ ] No SQL in business logic
- [ ] Repository returns domain objects

---

## Pattern Validation Questions

For any identified pattern, ask:

1. **Is the pattern necessary?** Does it solve a real problem?
2. **Is it correctly implemented?** Follows canonical structure?
3. **Is it the right pattern?** Could simpler solution work?
4. **Is it documented?** Others can recognize it?
5. **Is it testable?** Can mock dependencies?

---

**Last Updated**: 2025-01-21
