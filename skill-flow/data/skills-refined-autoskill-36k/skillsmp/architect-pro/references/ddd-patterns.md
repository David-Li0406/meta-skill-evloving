# Domain-Driven Design (DDD) Patterns

*Strategic and Tactical Design for 2026*

## Strategic Design
- **Bounded Contexts**: Explicitly defined boundaries where a particular model applies.
- **Ubiquitous Language**: A shared language between developers and domain experts.

## Tactical Patterns

### 1. Entities
Objects with a thread of continuity and identity.
```typescript
export class User {
  constructor(public readonly id: string, public email: string) {}
  
  equals(other: User): boolean {
    return this.id === other.id;
  }
}
```

### 2. Value Objects
Objects that describe things but have no identity. They are **Immutable**.
```typescript
export class Address {
  constructor(
    public readonly street: string,
    public readonly city: string,
    public readonly zip: string
  ) {
    Object.freeze(this);
  }
}
```

### 3. Aggregates
A cluster of associated objects that we treat as a unit for data changes. The **Aggregate Root** is the only gatekeeper.
```typescript
export class Order {
  private items: OrderItem[] = [];
  
  addItem(product: Product, quantity: number) {
    // Invariant: Total cannot exceed $10,000
    if (this.calculateTotal() + (product.price * quantity) > 10000) {
      throw new Error("Order limit exceeded");
    }
    this.items.push(new OrderItem(product.id, quantity));
  }
}
```

### 4. Domain Events
Capture something that happened in the domain.
```typescript
export class OrderPlacedEvent {
  constructor(public readonly orderId: string, public readonly timestamp: Date) {}
}
```

## 2026 Context: Event-Driven Architectures
With Next.js 16.2 and modern cloud providers, Domain Events are often used to trigger background processes (via Vercel Functions, AWS Lambda, or local event emitters) without blocking the main request-response cycle.

## Common Mistakes
- **Anemic Domain Model**: Entities that only have getters and setters. Logic should be inside the entities or domain services.
- **Ignoring Bounded Contexts**: Trying to create one "User" model for the entire system (Auth, Profile, Billing, Shipping). Instead, have a "User" in each context with only the fields relevant to that context.
