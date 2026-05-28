# Architecture Examples

Software architecture examples including microservices design, system design, and architectural patterns.

## How to Use

Each example includes:
- **📝 Prompt**: The exact prompt to use
- **🏗️ Architecture Diagrams**: Visual representations (mermaid syntax)
- **📐 Design Decisions**: Rationale and trade-offs
- **💡 Best Practices**: Architectural guidelines
- **🔧 Implementation**: Code examples and configurations

## Examples

1. [Microservices Architecture](./01-microservices-design.md) - E-commerce platform with microservices
2. [System Design](./02-system-design.md) - Real-time chat application with scalability

## Architecture Principles

### 1. Scalability
- Horizontal scaling
- Load balancing
- Caching strategies
- Database sharding

### 2. Reliability
- High availability (99.9%+)
- Fault tolerance
- Graceful degradation
- Circuit breakers

### 3. Maintainability
- Loose coupling
- High cohesion
- Clear interfaces
- Documentation

### 4. Security
- Defense in depth
- Principle of least privilege
- Encryption at rest and in transit
- Regular security audits

### 5. Performance
- Response time optimization
- Throughput maximization
- Resource efficiency
- Caching strategies

## Common Patterns

### Microservices Patterns
- API Gateway
- Service Discovery
- Circuit Breaker
- Event Sourcing
- CQRS
- Saga Pattern

### Data Patterns
- Database per Service
- Shared Database (anti-pattern)
- Event Sourcing
- CQRS
- Data Lake

### Communication Patterns
- Synchronous (REST, gRPC)
- Asynchronous (Message Queue, Events)
- Request-Response
- Publish-Subscribe

## Tools & Technologies

### Orchestration
- Kubernetes
- Docker Swarm
- AWS ECS/EKS

### Service Mesh
- Istio
- Linkerd
- Consul Connect

### API Gateway
- Kong
- AWS API Gateway
- NGINX

### Message Brokers
- RabbitMQ
- Apache Kafka
- AWS SQS/SNS

### Databases
- PostgreSQL (relational)
- MongoDB (document)
- Redis (cache)
- Elasticsearch (search)

## Quick Start

```bash
# Clone architecture example
git clone <repo>

# Review architecture diagram
cat 01-microservices-design.md

# Deploy sample architecture
kubectl apply -f k8s/

# Access services
curl https://api.example.com/health
```

## Resources

- [System Design Primer](https://github.com/donnemartin/system-design-primer)
- [Microservices Patterns](https://microservices.io/patterns/)
- [AWS Architecture Center](https://aws.amazon.com/architecture/)
- [Azure Architecture Center](https://docs.microsoft.com/en-us/azure/architecture/)
