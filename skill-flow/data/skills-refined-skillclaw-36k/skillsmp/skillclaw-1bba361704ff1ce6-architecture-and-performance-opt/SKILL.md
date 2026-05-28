---
name: architecture-and-performance-optimization
description: Use this skill when you need to evaluate system architecture and optimize performance, including scalability, maintainability, and various optimization strategies for both front-end and back-end systems.
---

# Architecture Review and Performance Optimization

## Architecture Evaluation Dimensions

### 1. Scalability
- Horizontal scaling capabilities
- Vertical scaling capabilities
- Performance bottleneck identification
- Load balancing strategies

### 2. Maintainability
- Code organization structure
- Degree of modularity
- Completeness of documentation
- Technical debt

### 3. Reliability
- Fault tolerance mechanisms
- Disaster recovery
- Data consistency
- Monitoring and alerting

### 4. Security
- Authentication and authorization
- Data encryption
- Security auditing
- Vulnerability protection

### 5. Performance
- Response time
- Throughput
- Resource utilization
- Caching strategies

## Performance Metrics

### Front-end Performance Metrics

#### Core Web Vitals
```
LCP (Largest Contentful Paint): Target < 2.5s
FID (First Input Delay): Target < 100ms
CLS (Cumulative Layout Shift): Target < 0.1
```

### Back-end Performance Metrics
```
Response Time: P50, P95, P99
Throughput: QPS, TPS
Error Rate: 4xx, 5xx
Resource Utilization: CPU, Memory, Disk I/O, Network Bandwidth
```

## Architectural Patterns

### Monolithic Architecture
**Use Cases**: Small applications, small teams, simple business logic, rapid iteration.
**Pros**: Simple development, easy deployment, convenient debugging, good performance.
**Cons**: Difficult to scale, fixed tech stack, high deployment risk, challenging team collaboration.

### Microservices Architecture
**Use Cases**: Large complex systems, large teams, independent deployment, diverse tech stacks.
**Design Principles**:
1. Single Responsibility: Each service focuses on one business area.
2. Autonomy: Independent development, deployment, and scaling.
3. Decentralization: Data and governance are decentralized.
4. Fault Tolerance: Isolation between services to prevent failure propagation.
5. Observability: Comprehensive monitoring and logging.

### Event-Driven Architecture
**Core Concepts**:
```typescript
// Event publishing
eventBus.publish('OrderCreated', { orderId: '123', userId: '456', amount: 100 });

// Event subscription
eventBus.subscribe('OrderCreated', async (event) => {
  await sendEmail(event.userId);
  await updateInventory(event.orderId);
});
```

## Performance Optimization Strategies

### Front-end Optimization

#### Resource Loading Optimization
- **Code Splitting**: Use React lazy loading or Webpack for dynamic imports.
- **Resource Compression**: Configure Webpack for minification and enable Gzip compression.
- **Image Optimization**: Use responsive images and lazy loading techniques.

#### Rendering Optimization
- **Virtual Scrolling**: Implement virtual lists for large datasets.
- **Debouncing and Throttling**: Use techniques to optimize event handling.

### Back-end Optimization
- Optimize database queries and implement caching strategies to improve response times and throughput.

This skill combines architectural review and performance optimization to provide a comprehensive approach to system design and efficiency.