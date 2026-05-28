# Integration Patterns

## Patterns

### **Golden Rules**
  
---
    ##### **Rule**
Prefer async over sync
    ##### **Reason**
Reduces coupling, improves resilience
  
---
    ##### **Rule**
API-first design
    ##### **Reason**
Contract before implementation
  
---
    ##### **Rule**
Idempotent operations
    ##### **Reason**
Safe retries, exactly-once semantics
  
---
    ##### **Rule**
Schema evolution
    ##### **Reason**
Backward/forward compatibility
  
---
    ##### **Rule**
Circuit breakers everywhere
    ##### **Reason**
Prevent cascade failures
### **Integration Types**
  #### **Synchronous**
    ##### **Rest**
Request-reply over HTTP, user-facing
    ##### **Graphql**
Flexible queries, federated graphs
    ##### **Grpc**
High-performance internal, streaming
  #### **Asynchronous**
    ##### **Events**
Domain events, eventual consistency
    ##### **Commands**
Task queues, work distribution
    ##### **Cqrs**
Separate read/write models
### **Pattern Selection**
  #### **Need Immediate Response**
    ##### **User Facing**
REST or GraphQL
    ##### **Internal**
gRPC
  #### **Eventual Consistency**
    ##### **Ordering Required**
Kafka with partitions
    ##### **Fan Out**
SNS/SQS
    ##### **Routing**
EventBridge
### **Api Gateway Features**
  - Rate limiting
  - Response caching
  - Circuit breaking
  - Request transformation
  - Authentication
  - Authorization
### **Event Patterns**
  #### **Cloudevents**
Standard event format
  #### **Outbox**
Transactional reliability
  #### **Saga**
Distributed transactions
  #### **Cqrs**
Command query separation

## Anti-Patterns


---
  #### **Pattern**
Point-to-point spaghetti
  #### **Problem**
N systems = N*(N-1)/2 connections
  #### **Solution**
Hub-and-spoke or event mesh

---
  #### **Pattern**
Synchronous chains
  #### **Problem**
Cascading failures, high latency
  #### **Solution**
Async events, choreography

---
  #### **Pattern**
Shared database integration
  #### **Problem**
Tight coupling, schema changes break all
  #### **Solution**
API contracts

---
  #### **Pattern**
No schema evolution
  #### **Problem**
Breaking changes on update
  #### **Solution**
Backward/forward compatible schemas

---
  #### **Pattern**
Ignoring idempotency
  #### **Problem**
Duplicate processing on retry
  #### **Solution**
Idempotency keys, deduplication