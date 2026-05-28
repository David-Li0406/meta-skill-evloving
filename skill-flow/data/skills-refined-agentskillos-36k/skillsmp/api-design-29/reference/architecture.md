# Architecture and Design Principles

This guideline establishes architectural patterns and SOLID design principles.

## SOLID Principles

Follow SOLID principles for object-oriented design: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.

## Layered Architecture

Separate concerns into distinct layers (presentation, business logic, data access).

## Design Patterns

Apply appropriate design patterns (Factory, Strategy, Observer, etc.) to solve common problems.

## Microservices Considerations

When applicable, design services to be loosely coupled, independently deployable, and organized around business capabilities.

---

## Detailed Examples

### SOLID Principles

<details>
<summary>Single Responsibility Principle (SRP)</summary>

```typescript
// BAD: Class has multiple responsibilities
class User {
    constructor(public name: string, public email: string) {}

    save() {
        // Database logic
        db.query('INSERT INTO users...');
    }

    sendEmail(message: string) {
        // Email logic
        smtp.send(this.email, message);
    }

    generateReport() {
        // Reporting logic
        return `User Report: ${this.name}`;
    }
}

// GOOD: Each class has a single responsibility
class User {
    constructor(public name: string, public email: string) {}
}

class UserRepository {
    async save(user: User): Promise<void> {
        await db.query('INSERT INTO users (name, email) VALUES ($1, $2)',
            [user.name, user.email]);
    }

    async findById(id: string): Promise<User | null> {
        const result = await db.query('SELECT * FROM users WHERE id = $1', [id]);
        return result.rows[0] ? new User(result.rows[0].name, result.rows[0].email) : null;
    }
}

class EmailService {
    async send(to: string, message: string): Promise<void> {
        await smtp.send({ to, subject: 'Notification', body: message });
    }
}

class UserReportGenerator {
    generate(user: User): string {
        return `User Report\nName: ${user.name}\nEmail: ${user.email}`;
    }
}
```
</details>

<details>
<summary>Open/Closed Principle (OCP)</summary>

```kotlin
// BAD: Need to modify class to add new payment methods
class PaymentProcessor {
    fun process(type: String, amount: Double) {
        when (type) {
            "credit_card" -> processCreditCard(amount)
            "paypal" -> processPayPal(amount)
            // Need to modify this class for each new payment method
        }
    }
}

// GOOD: Open for extension, closed for modification
interface PaymentMethod {
    fun process(amount: Double): PaymentResult
}

class CreditCardPayment : PaymentMethod {
    override fun process(amount: Double): PaymentResult {
        // Credit card processing logic
        return PaymentResult.Success(amount)
    }
}

class PayPalPayment : PaymentMethod {
    override fun process(amount: Double): PaymentResult {
        // PayPal processing logic
        return PaymentResult.Success(amount)
    }
}

class CryptoPayment : PaymentMethod {
    override fun process(amount: Double): PaymentResult {
        // Cryptocurrency processing logic
        return PaymentResult.Success(amount)
    }
}

class PaymentProcessor(private val paymentMethod: PaymentMethod) {
    fun process(amount: Double): PaymentResult {
        return paymentMethod.process(amount)
    }
}

// Usage - can add new payment methods without modifying PaymentProcessor
val processor = PaymentProcessor(CryptoPayment())
processor.process(100.0)
```
</details>

<details>
<summary>Dependency Inversion Principle (DIP)</summary>

```python
# BAD: High-level module depends on low-level module
class MySQLDatabase:
    def save(self, data):
        # MySQL specific save logic
        pass

class UserService:
    def __init__(self):
        self.db = MySQLDatabase()  # Tightly coupled to MySQL

    def create_user(self, user):
        self.db.save(user)


# GOOD: Both depend on abstractions
from abc import ABC, abstractmethod

class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

class MySQLDatabase(Database):
    def save(self, data):
        # MySQL implementation
        pass

    def find_by_id(self, id):
        # MySQL implementation
        pass

class PostgreSQLDatabase(Database):
    def save(self, data):
        # PostgreSQL implementation
        pass

    def find_by_id(self, id):
        # PostgreSQL implementation
        pass

class UserService:
    def __init__(self, database: Database):
        self.db = database  # Depends on abstraction

    def create_user(self, user):
        self.db.save(user)

# Usage with dependency injection
mysql_db = MySQLDatabase()
user_service = UserService(mysql_db)

# Easy to swap implementations
postgres_db = PostgreSQLDatabase()
user_service = UserService(postgres_db)
```
</details>

### Layered Architecture

<details>
<summary>Clean Architecture Layers</summary>

```
┌─────────────────────────────────────────┐
│         Presentation Layer              │
│  (Controllers, Views, DTOs)             │
├─────────────────────────────────────────┤
│         Application Layer               │
│  (Use Cases, Business Logic)            │
├─────────────────────────────────────────┤
│         Domain Layer                    │
│  (Entities, Value Objects, Interfaces)  │
├─────────────────────────────────────────┤
│         Infrastructure Layer            │
│  (Database, External APIs, Frameworks)  │
└─────────────────────────────────────────┘
```

```typescript
// Domain Layer - Pure business logic, no dependencies
export class User {
    constructor(
        public readonly id: string,
        public name: string,
        public email: string
    ) {
        this.validateEmail(email);
    }

    private validateEmail(email: string) {
        if (!email.includes('@')) {
            throw new Error('Invalid email');
        }
    }

    changeName(newName: string) {
        if (newName.length < 2) {
            throw new Error('Name too short');
        }
        this.name = newName;
    }
}

export interface UserRepository {
    save(user: User): Promise<void>;
    findById(id: string): Promise<User | null>;
}

// Application Layer - Use cases
export class CreateUserUseCase {
    constructor(private userRepository: UserRepository) {}

    async execute(name: string, email: string): Promise<User> {
        // Business logic
        const user = new User(generateId(), name, email);
        await this.userRepository.save(user);
        return user;
    }
}

// Infrastructure Layer - Database implementation
export class PostgresUserRepository implements UserRepository {
    constructor(private db: Database) {}

    async save(user: User): Promise<void> {
        await this.db.query(
            'INSERT INTO users (id, name, email) VALUES ($1, $2, $3)',
            [user.id, user.name, user.email]
        );
    }

    async findById(id: string): Promise<User | null> {
        const result = await this.db.query(
            'SELECT * FROM users WHERE id = $1',
            [id]
        );

        if (!result.rows[0]) return null;

        return new User(
            result.rows[0].id,
            result.rows[0].name,
            result.rows[0].email
        );
    }
}

// Presentation Layer - HTTP controller
export class UserController {
    constructor(private createUser: CreateUserUseCase) {}

    async create(req: Request, res: Response) {
        try {
            const { name, email } = req.body;
            const user = await this.createUser.execute(name, email);

            res.status(201).json({
                id: user.id,
                name: user.name,
                email: user.email
            });
        } catch (error) {
            res.status(400).json({ error: error.message });
        }
    }
}

// Dependency Injection setup
const db = new Database();
const userRepository = new PostgresUserRepository(db);
const createUserUseCase = new CreateUserUseCase(userRepository);
const userController = new UserController(createUserUseCase);
```
</details>

### Design Patterns

<details>
<summary>Common Design Patterns</summary>

```typescript
// Factory Pattern
interface Animal {
    speak(): string;
}

class Dog implements Animal {
    speak() { return 'Woof!'; }
}

class Cat implements Animal {
    speak() { return 'Meow!'; }
}

class AnimalFactory {
    static create(type: string): Animal {
        switch (type) {
            case 'dog': return new Dog();
            case 'cat': return new Cat();
            default: throw new Error('Unknown animal type');
        }
    }
}

// Strategy Pattern
interface PaymentStrategy {
    pay(amount: number): void;
}

class CreditCardStrategy implements PaymentStrategy {
    pay(amount: number) {
        console.log(`Paid ${amount} with credit card`);
    }
}

class PayPalStrategy implements PaymentStrategy {
    pay(amount: number) {
        console.log(`Paid ${amount} with PayPal`);
    }
}

class PaymentContext {
    constructor(private strategy: PaymentStrategy) {}

    setStrategy(strategy: PaymentStrategy) {
        this.strategy = strategy;
    }

    executePayment(amount: number) {
        this.strategy.pay(amount);
    }
}

// Observer Pattern
interface Observer {
    update(data: any): void;
}

class Subject {
    private observers: Observer[] = [];

    attach(observer: Observer) {
        this.observers.push(observer);
    }

    detach(observer: Observer) {
        const index = this.observers.indexOf(observer);
        if (index > -1) {
            this.observers.splice(index, 1);
        }
    }

    notify(data: any) {
        for (const observer of this.observers) {
            observer.update(data);
        }
    }
}

class EmailObserver implements Observer {
    update(data: any) {
        console.log(`Sending email about: ${data}`);
    }
}

class LogObserver implements Observer {
    update(data: any) {
        console.log(`Logging: ${data}`);
    }
}

// Singleton Pattern (use sparingly!)
class Configuration {
    private static instance: Configuration;
    private settings: Map<string, any>;

    private constructor() {
        this.settings = new Map();
    }

    static getInstance(): Configuration {
        if (!Configuration.instance) {
            Configuration.instance = new Configuration();
        }
        return Configuration.instance;
    }

    get(key: string): any {
        return this.settings.get(key);
    }

    set(key: string, value: any): void {
        this.settings.set(key, value);
    }
}
```
</details>

### Microservices Best Practices

<details>
<summary>Service Design Guidelines</summary>

```
Good Microservice Characteristics:
1. Single Responsibility - one business capability
2. Autonomous - independently deployable
3. Isolated Data - own database/schema
4. API First - well-defined contracts
5. Observable - metrics, logs, traces
6. Resilient - handle failures gracefully

Communication Patterns:
- Synchronous: REST, gRPC
- Asynchronous: Message queues, events
```

```typescript
// Service-to-service communication with circuit breaker
import CircuitBreaker from 'opossum';

class UserService {
    private orderServiceCircuit: CircuitBreaker;

    constructor() {
        this.orderServiceCircuit = new CircuitBreaker(
            this.callOrderService.bind(this),
            {
                timeout: 3000,        // 3 seconds
                errorThresholdPercentage: 50,
                resetTimeout: 30000   // 30 seconds
            }
        );

        // Handle circuit breaker events
        this.orderServiceCircuit.on('open', () => {
            logger.warn('Circuit breaker opened for order service');
        });
    }

    private async callOrderService(userId: string) {
        const response = await fetch(`http://order-service/users/${userId}/orders`);
        return response.json();
    }

    async getUserWithOrders(userId: string) {
        const user = await this.getUser(userId);

        try {
            const orders = await this.orderServiceCircuit.fire(userId);
            return { ...user, orders };
        } catch (error) {
            // Fallback when circuit is open
            logger.warn('Order service unavailable, returning user without orders');
            return { ...user, orders: [] };
        }
    }
}

// Event-driven communication
class OrderCreatedEvent {
    constructor(
        public orderId: string,
        public userId: string,
        public total: number,
        public timestamp: Date
    ) {}
}

class OrderService {
    async createOrder(order: Order) {
        // Save order
        await this.repository.save(order);

        // Publish event
        await eventBus.publish('order.created', new OrderCreatedEvent(
            order.id,
            order.userId,
            order.total,
            new Date()
        ));
    }
}

class NotificationService {
    constructor() {
        // Subscribe to events
        eventBus.subscribe('order.created', this.handleOrderCreated.bind(this));
    }

    async handleOrderCreated(event: OrderCreatedEvent) {
        await this.sendNotification(event.userId, `Order ${event.orderId} created`);
    }
}
```
</details>
