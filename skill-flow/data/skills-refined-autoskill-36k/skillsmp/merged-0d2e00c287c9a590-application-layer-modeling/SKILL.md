---
name: application-layer-modeling
description: Use this skill for expert knowledge in Application Layer modeling to describe application services, components, and interfaces that support business processes and bridge requirements with technical implementation.
---

# Application Layer Skill

**Layer Number:** 04  
**Specification:** Metadata Model Spec v0.7.0  
**Purpose:** Describes application services, components, and interfaces that support business processes and bridge requirements with technical implementation.

---

## Layer Overview

The Application Layer captures **application architecture**:

- **WHAT** - Application services exposed to business
- **HOW** - Application components and functions
- **INTEGRATION** - Application interfaces and interactions
- **DATA** - Data objects processed by applications
- **EVENTS** - Application events for event-driven architecture

This layer uses **ArchiMate 3.2 Application Layer** standard with optional properties for external specifications (OpenAPI, orchestration definitions, event schemas).

---

## Entity Types

| Entity Type                  | Description                                            | Key Attributes                                                                   |
| ---------------------------- | ------------------------------------------------------ | -------------------------------------------------------------------------------- |
| **ApplicationComponent**     | Modular, deployable, replaceable part of a system      | Types: frontend, backend, mobile, desktop, service, library, batch, worker       |
| **ApplicationCollaboration** | Aggregate of application components working together   | Example: Microservices ecosystem, service mesh                                   |
| **ApplicationInterface**     | Point of access where application service is available | Protocols: REST, GraphQL, SOAP, gRPC, WebSocket, Message Queue, Event Bus        |
| **ApplicationFunction**      | Automated behavior performed by application component  | Examples: Authentication, Data Validation, Caching, Logging                      |
| **ApplicationInteraction**   | Unit of collective application behavior                | Patterns: request-response, publish-subscribe, async-messaging, streaming, batch |
| **ApplicationProcess**       | Sequence of application behaviors (orchestration/saga) | Can reference orchestration definitions (Temporal, Conductor, Camunda)           |
| **ApplicationEvent**         | Application state change notification                  | Types: domain-event, integration-event, system-event, audit-event                |
| **ApplicationService**       | Service that exposes application functionality         | Types: synchronous, asynchronous, batch, streaming, webhook                      |
| **DataObject**               | Data structured for automated processing               | Includes schema reference, PII marking, retention policies                       |

---

## Intra-Layer Relationships

### Structural Relationships

| Source Type              | Predicate   | Target Type            | Example                                                                                  |
| ------------------------ | ----------- | ---------------------- | ---------------------------------------------------------------------------------------- |
| ApplicationCollaboration | aggregates  | ApplicationComponent   | "Payment Ecosystem" aggregates "PaymentService", "FraudDetection", "NotificationService" |
| ApplicationComponent     | composes    | ApplicationInterface   | Component exposes interface for external access                                          |
| ApplicationProcess       | composes    | ApplicationProcess     | Workflow composed of sub-processes (saga pattern)                                        |
| ApplicationComponent     | assigned-to | ApplicationFunction    | Component performs specific function                                                     |
| ApplicationCollaboration | assigned-to | ApplicationInteraction | Collaboration executes interaction pattern                                               |
| ApplicationComponent     | realizes    | ApplicationService     | "UserManagementAPI" realizes "User Management Service"                                   |
| ApplicationFunction      | realizes    | ApplicationService     | "Authentication Function" realizes "Auth Service"                                        |
| ApplicationProcess       | realizes    | ApplicationService     | "Order Processing Workflow" realizes "Order Service"                                     |
| ApplicationService       | realizes    | ApplicationInterface   | Service exposes interface                                                                |
| DataObject               | specializes | DataObject             | "CustomerOrder" specializes "Order"                                                      |

### Behavioral Relationships

| Source Type            | Predicate | Target Type          | Example                                         |
| ---------------------- | --------- | -------------------- | ----------------------------------------------- |
| ApplicationEvent       | triggers  | ApplicationComponent | "OrderCreated" triggers "InventoryService"      |
| ApplicationEvent       | triggers  | ApplicationFunction  | "UserLoggedIn" triggers "AuditLogging" function |
| ApplicationEvent       | triggers  | ApplicationProcess   | "PaymentFailed" triggers "RefundProcess"        |
| ApplicationProcess     | triggers  | ApplicationEvent     | Workflow completion triggers event              |
| ApplicationService     | flows-to  | ApplicationService   | Synchronous service-to-service call             |
| ApplicationProcess     | flows-to  | ApplicationProcess   | Sequential process orchestration                |
| ApplicationService     | accesses  | DataObject           | Service reads/writes data                       |
| ApplicationFunction    | accesses  | DataObject           | Function operates on data                       |
| ApplicationProcess     | accesses  | DataObject           | Workflow manipulates data                       |
| ApplicationInteraction | accesses  | DataObject           | Interaction pattern involves data exchange      |
| ApplicationInterface   | serves    | ApplicationComponent | Interface provides access to component          |

---

## Cross-Layer References

### Outgoing References (Application → Other Layers)

| Target Layer             | Reference Type                                          | Example                                    |
| ------------------------ | ------------------------------------------------------- | ------------------------------------------ |
| **Layer 1 (Motivation)** | ApplicationService supports **Goal**                    | Service achieves business goals            |
| **Layer 1 (Motivation)** | ApplicationService delivers **Value**                   | Service delivers business value            |
| **Layer 1 (Motivation)** | ApplicationService governed by **Principle**            | Service follows architectural principles   |
| **Layer 1 (Motivation)** | ApplicationFunction fulfills **Requirement**            | Function implements functional requirement |
| **Layer 2 (Business)**   | ApplicationService realizes **BusinessService**         | Tech realizes business capability          |
| **Layer 2 (Business)**   | ApplicationProcess supports **BusinessProcess**         | Automates business workflow                |
| **Layer 2 (Business)**   | DataObject represents **BusinessObject**                | Technical data represents business concept |
| **Layer 5 (Technology)** | ApplicationComponent deployed-on **Node**               | Service deployed to Kubernetes cluster     |
| **Layer 5 (Technology)** | ApplicationService uses **TechnologyService**           | Application uses database service          |
| **Layer 5 (Technology)** | DataObject stored-in **Artifact**                       | Data persisted in database                 |
| **Layer 6 (API)**        | ApplicationService defined-by **OpenAPI Specification** | Service has OpenAPI contract               |
| **Layer 7 (Data Model)** | DataObject defined-by **JSON Schema**                   | Data structure defined as schema           |
| **Layer 11 (APM)**       | ApplicationService tracked-by **BusinessMetric**        | Service performance monitored              |
| **Layer 11 (APM)**       | ApplicationService has-sla **SLA Target**               | Latency, availability targets              |
| **Layer 11 (APM)**       | ApplicationService traced-by **APM**                    | Distributed tracing enabled                |

### Incoming References (Lower Layers → Application)

Lower layers reference Application layer to show:

- **Technology supports Application** - Infrastructure hosts application components
- **APIs implement Application Services** - OpenAPI specs define service contracts
- **Data schemas define DataObjects** - JSON schemas provide data structure

---

## Codebase Detection Patterns

### Pattern 1: Microservice Component

```python
# FastAPI microservice
from fastapi import FastAPI

app = FastAPI(
    title="User Management Service",
    description="Handles user authentication and profile management",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**Maps to:**

- ApplicationComponent: "UserManagementService" (type: backend, subtype: microservice)
- ApplicationService: "User Management Service" (type: synchronous)
- ApplicationInterface: "REST API" (protocol: REST)

### Pattern 2: Application Function (Utility)

```typescript
// Authentication utility function
export class AuthenticationService {
  /**
   * Validates JWT token and returns user context
   * ApplicationFunction: Token Validation
   */
  async validateToken(token: string): Promise<UserContext> {
    // Implementation
  }
}
```

**Maps to:**

- ApplicationFunction: "Token Validation"
- ApplicationComponent: "AuthenticationService"

### Pattern 3: Event-Driven Architecture

```python
# Event definitions
from dataclasses import dataclass
from enum import Enum

class ApplicationEventType(Enum):
    ORDER_CREATED = "order.created"
    ORDER_FULFILLED = "order.fulfilled"
    PAYMENT_PROCESSED = "payment.processed"

@dataclass
class OrderCreatedEvent:
    """
    Domain event: Order created
    Schema: schemas/events/order-created.json
    Topic: orders.created
    """
    order_id: str
    customer_id: str
    timestamp: datetime
```

**Maps to:**

- ApplicationEvent: "OrderCreated" (type: domain-event, topic: orders.created)
- Properties: schema-ref, event-version
- Triggers other ApplicationComponents

### Pattern 4: Service Orchestration (Saga)

```python
# Temporal workflow (saga pattern)
from temporalio import workflow

@workflow.defn
class OrderFulfillmentWorkflow:
    """
    Order fulfillment orchestration
    ApplicationProcess: Order Fulfillment Saga
    Pattern: Saga with compensation
    """
    @workflow.run
    async def run(self, order_id: str) -> str:
        # Step 1: Reserve inventory
        await workflow.execute_activity(reserve_inventory, order_id)

        # Step 2: Process payment
        await workflow.execute_activity(process_payment, order_id)

        # Step 3: Ship order
        await workflow.execute_activity(ship_order, order_id)

        return "fulfilled"
```

**Maps to:**

- ApplicationProcess: "OrderFulfillmentSaga" (pattern: saga)
- Properties: orchestration-engine=temporal, compensation-enabled=true
- Composes sub-processes (reserve, pay, ship)

### Pattern 5: Data Transfer Object (DTO)

```typescript
// Data object definitions
export interface UserDTO {
  /**
   * User data object
   * Schema: schemas/user.schema.json
   * PII: true (contains email, name)
   * Retention: 7 years
   */
  userId: string;
  email: string;
  name: string;
  createdAt: Date;
}
```

**Maps to:**

- DataObject: "User"
- Properties: schema-ref=user.schema.json, pii=true, retention-period=7y

### Pattern 6: gRPC Service Interface

```protobuf
// gRPC service definition
service UserService {
  // ApplicationInterface: gRPC
  // Protocol: gRPC
  rpc GetUser (GetUserRequest) returns (User);
  rpc CreateUser (CreateUserRequest) returns (User);
  rpc UpdateUser (UpdateUserRequest) returns (User);
}
```

**Maps to:**

- ApplicationInterface: "UserServiceGRPC" (protocol: gRPC)
- ApplicationService: "User Service"
- ApplicationComponent: "UserService"

### Pattern 7: Message Queue Consumer

```python
# RabbitMQ consumer
from kombu import Connection, Queue

class OrderEventConsumer:
    """
    Consumes order events from message queue
    ApplicationComponent: OrderEventConsumer (type: worker)
    ApplicationInterface: Message Queue (protocol: AMQP)
    """
    def __init__(self):
        self.queue = Queue('orders.created', exchange='orders')

    def consume(self):
        with Connection('amqp://localhost') as conn:
            with conn.Consumer(self.queue, callbacks=[self.handle_order]):
                conn.drain_events()

    def handle_order(self, body, message):
        # Process order event
        message.ack()
```

**Maps to:**

- ApplicationComponent: "OrderEventConsumer" (type: worker)
- ApplicationInterface: "OrderQueue" (protocol: AMQP)
- ApplicationEvent: "OrderCreated" (triggers this component)

---

## Modeling Workflow

### Step 1: Identify Application Components

```bash
# Frontend component
dr add application component "web-app" \
  --properties type=frontend,technology=react,repository=github.com/org/web-app \
  --description "Customer-facing web application"

# Backend microservices
dr add application component "user-service" \
  --properties type=backend,subtype=microservice,language=python \
  --description "User management microservice"

dr add application component "order-service" \
  --properties type=backend,subtype=microservice,language=typescript \
  --description "Order processing microservice"

# Worker component
dr add application component "email-worker" \
  --properties type=worker,runtime=nodejs \
  --description "Background worker for email notifications"
```

### Step 2: Define Application Services

```bash
# Synchronous service
dr add application service "user-management-api" \
  --properties type=synchronous,protocol=REST,openapi-spec=specs/user-api.yaml \
  --description "User management REST API"

# Asynchronous service
dr add application service "notification-service" \
  --properties type=asynchronous,pattern=publish-subscribe \
  --description "Asynchronous notification delivery"

# Link component to service
dr relationship add "application/component/user-service" \
  realizes "application/service/user-management-api"
```

### Step 3: Model Application Interfaces

```bash
# REST API interface
dr add application interface "user-api-rest" \
  --properties protocol=REST,base-url=/api/v1/users,authentication=JWT \
  --description "REST interface for user service"

# gRPC interface
dr add application interface "order-grpc" \
  --properties protocol=gRPC,port=50051 \
  --description "gRPC interface for order service"

# Message queue interface
dr add application interface "event-bus" \
  --properties protocol=AMQP,broker=rabbitmq \
  --description "Event bus for async communication"

# Link service to interface
dr relationship add "application/service/user-management-api" \
  realizes "application/interface/user-api-rest"
```

### Step 4: Define Application Functions

```bash
# Core functions
dr add application function "authentication" \
  --properties type=security \
  --description "Validates user credentials and issues tokens"

dr add application function "data-validation" \
  --properties type=business-logic \
  --description "Validates input data against business rules"

dr add application function "caching" \
  --properties type=performance,strategy=redis \
  --description "Caches frequently accessed data"

# Assign function to component
dr relationship add "application/component/user-service" \
  assigned-to "application/function/authentication"
```

### Step 5: Model Application Events

```bash
# Domain events
dr add application event "order-created" \
  --properties type=domain-event,topic=orders.created,schema=schemas/order-created.json \
  --description "Published when new order is created"

dr add application event "payment-processed" \
  --properties type=domain-event,topic=payments.processed,schema=schemas/payment-processed.json \
  --description "Published when payment completes"

# Event triggering
dr relationship add "application/event/order-created" \
  triggers "application/component/inventory-service"

dr relationship add "application/event/order-created" \
  triggers "application/component/email-worker"
```

### Step 6: Define Data Objects

```bash
# Core data objects
dr add application data-object "user" \
  --properties schema-ref=schemas/user.schema.json,pii=true,retention-period=7y \
  --description "User account information"

dr add application data-object "order" \
  --properties schema-ref=schemas/order.schema.json,pii=false,retention-period=10y \
  --description "Customer order data"

# Service access to data
dr relationship add "application/service/user-management-api" \
  accesses "application/data-object/user"

dr relationship add "application/service/order-api" \
  accesses "application/data-object/order"
```

### Step 7: Model Application Processes (Orchestration)

```bash
# Saga workflow
dr add application process "order-fulfillment-saga" \
  --properties pattern=saga,orchestration-engine=temporal,compensation=true \
  --description "End-to-end order fulfillment orchestration"

# Sub-processes
dr add application process "reserve-inventory" \
  --description "Reserve items from inventory"

dr add application process "process-payment" \
  --description "Charge customer payment method"

dr add application process "ship-order" \
  --description "Initiate shipping workflow"

# Process composition
dr relationship add "application/process/order