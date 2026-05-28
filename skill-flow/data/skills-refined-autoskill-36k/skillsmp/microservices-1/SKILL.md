---
name: microservices
description: Microservices architecture pattern for distributed, independently deployable services
license: MIT
compatibility: opencode
metadata:
  category: architecture
  pattern: microservices
  deployment: distributed
---

## What I do

I provide guidance on building microservices architecture - independently deployable services with bounded contexts.

## When to use me

Load this skill when:
- Multiple independent teams (> 20 developers)
- Clear bounded contexts
- Need independent scaling of services
- Polyglot persistence requirements
- Can tolerate eventual consistency
- Mature DevOps practices

## Core Principles

### 1. Service Per Bounded Context
Each service owns a bounded context with its own data.

### 2. Database Per Service
No shared databases between services.

### 3. API-First Communication
Services communicate via APIs (REST/gRPC) or messaging.

### 4. Independent Deployment
Deploy services independently without coordinating releases.

### 5. Decentralized Governance
Teams own their service tech stack choices.

## Service Structure

```
services/
├── user-service/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
├── product-service/
│   ├── src/
│   ├── Dockerfile
│   └── package.json
└── order-service/
    ├── src/
    ├── Dockerfile
    └── package.json
```

## Communication Patterns

### Synchronous (REST/gRPC)
```typescript
// Service-to-service HTTP call
class OrderService {
  async createOrder(userId: string, productIds: string[]) {
    // Call user service
    const user = await fetch(`${USER_SERVICE_URL}/users/${userId}`);
    
    // Call product service
    const products = await fetch(`${PRODUCT_SERVICE_URL}/products`, {
      method: 'POST',
      body: JSON.stringify({ ids: productIds }),
    });
    
    // Create order with fetched data
  }
}
```

### Asynchronous (Message Queue)
```typescript
// Publish event to message queue
await messageQueue.publish('order.created', {
  orderId: order.id,
  userId: order.userId,
  items: order.items,
});

// Other services subscribe
messageQueue.subscribe('order.created', async (event) => {
  await inventoryService.reserveItems(event.items);
});
```

## Advantages

1. **Independent Scaling**: Scale services based on load
2. **Technology Diversity**: Choose best tool per service
3. **Team Autonomy**: Teams own services end-to-end
4. **Fault Isolation**: Service failure doesn't crash system
5. **Parallel Development**: Teams work independently

## Challenges

1. **Distributed Complexity**: Network calls, latency
2. **Data Consistency**: Eventual consistency, distributed transactions
3. **Operational Overhead**: More services to deploy/monitor
4. **Testing Complexity**: Integration testing across services
5. **Debugging**: Tracing requests across services

## Patterns

### API Gateway
```
Client → API Gateway → [User Service, Product Service, Order Service]
```

### Service Mesh
For service-to-service communication (Istio, Linkerd)

### Saga Pattern
For distributed transactions across services

### CQRS
Separate read and write models

## Best Practices

1. **Design for failure**: Circuit breakers, retries, timeouts
2. **Observability**: Distributed tracing, centralized logging
3. **API versioning**: Don't break consumers
4. **Service discovery**: Dynamic service registration
5. **Configuration management**: Centralized config
6. **Automated deployment**: CI/CD for each service
