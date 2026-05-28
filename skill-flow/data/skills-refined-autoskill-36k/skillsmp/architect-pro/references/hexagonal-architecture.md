# Hexagonal Architecture (Ports & Adapters)

*Optimized for Microservices and Serverless 2026*

## The Hexagon
The application is seen as a hexagon where the **Core Logic** is at the center. The Core defines **Ports** (Interfaces) to communicate with the outside world.

## Types of Ports
1. **Driving Ports (Primary)**: How the outside world triggers the application (API, CLI, Test).
2. **Driven Ports (Secondary)**: How the application triggers the outside world (Database, Messaging, Mail).

## Implementation with TypeScript

### The Port (Interface)
```typescript
// core/ports/IMessageBroker.ts
export interface IMessageBroker {
  publish(topic: string, message: any): Promise<void>;
}
```

### The Core Service
```typescript
// core/services/OrderService.ts
import { IMessageBroker } from '../ports/IMessageBroker';

export class OrderService {
  constructor(private broker: IMessageBroker) {}

  async completeOrder(orderId: string) {
    // ... logic ...
    await this.broker.publish('order_completed', { orderId });
  }
}
```

### The Adapter (Implementation)
```typescript
// infrastructure/adapters/RabbitMQAdapter.ts
import { IMessageBroker } from '@/core/ports/IMessageBroker';

export class RabbitMQAdapter implements IMessageBroker {
  async publish(topic: string, message: any) {
    // Actual RabbitMQ implementation
    console.log(`Publishing to ${topic}`, message);
  }
}

// infrastructure/adapters/MockBrokerAdapter.ts (For Testing)
export class MockBrokerAdapter implements IMessageBroker {
  public publishedMessages: any[] = [];
  async publish(topic: string, message: any) {
    this.publishedMessages.push({ topic, message });
  }
}
```

## 2026 Advantage: Technology Portability
In 2026, switching from a monolithic database to a distributed one, or from REST to gRPC, should not require changes to your business logic. Hexagonal architecture makes this possible by only requiring a new **Adapter**.

## Best Practices
- **Dependency Injection**: Use a DI container or simple constructor injection to swap adapters.
- **Test the Core in Isolation**: Use Mock adapters for all Driven Ports to ensure unit tests are fast and reliable.
