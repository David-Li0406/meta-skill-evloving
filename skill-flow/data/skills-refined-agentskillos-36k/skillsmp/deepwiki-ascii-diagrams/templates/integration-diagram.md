# Integration Diagram Templates

Integration diagrams show how multiple independent systems communicate and integrate with each other. They focus on system boundaries, communication protocols, and integration patterns.

---

## Template 1: Multi-Service E-Commerce Integration

**Purpose**: Show how different systems interact in an e-commerce ecosystem

```
┌──────────────────────────────────────────────────────────────┐
│             E-Commerce System Integration                     │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  External Systems:                                            │
│                                                                │
│  ╔════════════════════════════════════════════════════════╗  │
│  ║ Payment Gateway (Stripe)                               ║  │
│  ║ ├─ Process credit card payments                        ║  │
│  ║ ├─ Handle refunds                                      ║  │
│  ║ └─ Webhooks: charge.succeeded, charge.failed          ║  │
│  ╚════════════════════════╤═════════════════════════════╝  │
│                           │                                  │
│                           │ HTTPS POST                      │
│                           │ {amount, currency, card}        │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │          Core E-Commerce System                    │   │
│  │  (Node.js/Express API)                             │   │
│  │                                                     │   │
│  │  ┌───────────────────────────────────────────┐   │   │
│  │  │ Order Processing Service                 │   │   │
│  │  │ - Create orders                          │   │   │
│  │  │ - Track order status                     │   │   │
│  │  │ - Process payments                       │   │   │
│  │  │ - Update inventory                       │   │   │
│  │  └───────┬───────────────┬───────────────┬──┘   │   │
│  │          │               │               │      │   │
│  └──────────┼───────────────┼───────────────┼──────┘   │
│             │               │               │           │
│  HTTP/REST: │               │               │           │
│             │               │               │           │
│  ┌──────────▼──────┐ ┌──────▼────────┐ ┌───▼──────────┐ │
│  │                 │ │                │ │              │ │
│  ▼                 ▼ ▼                ▼ ▼              ▼ │
│  ╔════════════╗ ╔══════════╗ ╔═════════════════════╗ │  │
│  ║ Inventory  ║ ║Shipping  ║ ║ Email Service      ║ │  │
│  ║ Service    ║ ║ Service  ║ ║ (SendGrid)         ║ │  │
│  ║            ║ ║          ║ ║                    ║ │  │
│  ║ GET /stock ║ ║POST /ship║ ║POST /send-email    ║ │  │
│  ║ PATCH /    ║ ║          ║ ║                    ║ │  │
│  ║ reserve    ║ ║ Response:║ ║ {to, subject,      ║ │  │
│  ║            ║ ║ Tracking#║ ║  body, template}   ║ │  │
│  ║ Response:  ║ ║          ║ ║                    ║ │  │
│  ║ {available,║ ║ Webhook: ║ ║ Response:          ║ │  │
│  ║  reserved} ║ ║ shipment_║ ║ {message_id,       ║ │  │
│  ║            ║ ║ created  ║ ║  status}           ║ │  │
│  ╚════════════╝ ╚══════════╝ ╚═════════════════════╝ │  │
│       │              │                   │            │  │
└───────┼──────────────┼───────────────────┼────────────┘  │
        │              │                   │               │
        │              │                   │               │
        │ REST HTTP    │ REST HTTP         │ REST HTTP     │
        ▼              ▼                   ▼               │
  ╔───────────────────────────────────────────────────╗  │
  ║ Database (PostgreSQL)                            ║  │
  ║ - orders table                                   ║  │
  ║ - order_items table                             ║  │
  ║ - inventory table                               ║  │
  ║ - shipments table                               ║  │
  ║ - email_log table                               ║  │
  ╚───────────────────────────────────────────────────╝  │
        │              │                   │               │
        ▼              ▼                   ▼               │
  ┌────────────┐ ┌────────────┐ ┌──────────────────┐    │
  │ Event Bus  │ │ Message    │ │ Analytics        │    │
  │ (RabbitMQ) │ │ Queue      │ │ (Kafka Streams)  │    │
  │            │ │ (SQS)      │ │                  │    │
  │ Subscribers│ │ Publishers │ │ Listeners:       │    │
  │ - Analytics│ │ - Order    │ │ - Track metrics  │    │
  │ - Reporting│ │   Service  │ │ - Revenue        │    │
  │ - Audit    │ │            │ │ - Conversions    │    │
  └────────────┘ └────────────┘ └──────────────────┘    │
                                                          │
  External Integrations:                                 │
                                                          │
  ╔═════════════════════╗  ╔═════════════════════╗      │
  ║ Analytics Service   ║  ║ Customer CRM        ║      │
  ║ (Google Analytics)  ║  ║ (Salesforce)        ║      │
  ║                     ║  ║                     ║      │
  ║ OAuth 2.0 flow      ║  ║ REST API            ║      │
  ║ Track conversions   ║  ║ POST /contacts      ║      │
  ║ and user behavior   ║  ║ PUT /contacts/{id}  ║      │
  ╚═════════════════════╝  ╚═════════════════════╝      │
       ▲                           ▲                      │
       │                           │                      │
       └─────────────┬─────────────┘                      │
                     │                                   │
                 Webhooks &                              │
                 Sync Events                             │
                                                         │
└──────────────────────────────────────────────────────────┘

Communication Summary:
├─ Stripe → Core System: HTTPS webhooks
├─ Core → Inventory/Shipping/Email: REST HTTP APIs
├─ Core → Database: SQL queries
├─ Core → Message Bus: Event publishing
└─ Analytics → External Services: OAuth + REST APIs
```

### Integration Points
- **Payment Processing**: Stripe webhooks for transaction events
- **Service Communication**: REST APIs with JSON payloads
- **Asynchronous Processing**: Message queues for decoupling
- **Event Distribution**: Event bus for cross-service notifications
- **External Sync**: Webhooks and API calls for third-party systems

---

## Template 2: Microservices API Gateway Integration

**Purpose**: Show how services integrate through an API Gateway

```
┌──────────────────────────────────────────────────────────┐
│      Microservices API Gateway Pattern                   │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  External Clients:                                       │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐        │
│  │ Web    │  │ Mobile │  │ Admin  │  │ Partners       │
│  │ App    │  │ App    │  │ Portal │  │ APIs   │        │
│  └────┬───┘  └────┬───┘  └────┬───┘  └────┬───┘        │
│       │           │           │           │            │
│       │    HTTPS + OAuth 2.0 (JWT tokens)  │            │
│       │                                    │            │
│       └────────────────┬────────────────────┘            │
│                        │                                │
│                        ▼                                │
│       ┌───────────────────────────────────┐            │
│       │   API Gateway (Kong / AWS ALB)    │            │
│       │                                   │            │
│       │ Features:                         │            │
│       │ ├─ Authentication (JWT verify)    │            │
│       │ ├─ Authorization (Scope check)    │            │
│       │ ├─ Rate limiting (100 req/min)   │            │
│       │ ├─ Request validation             │            │
│       │ ├─ Response transformation        │            │
│       │ ├─ Logging & monitoring           │            │
│       │ └─ Request routing                │            │
│       └───┬───────────┬────────┬────────┬─┘            │
│           │           │        │        │              │
│  Micro-   │           │        │        │              │
│  service  │           │        │        │              │
│  routes:  │           │        │        │              │
│       ┌───▼─┐ ┌──────▼─┐ ┌───▼──┐ ┌──▼────┐          │
│       │GET  │ │POST    │ │GET   │ │GET    │          │
│       │/auth│ │/orders │ │/products│/users│ │          │
│       └──┬──┘ └──┬─────┘ └──┬───┘ └───┬──┘          │
│          │       │          │         │              │
│  gRPC /  │       │          │         │              │
│  HTTP2:  │       │          │         │              │
│          ▼       ▼          ▼         ▼              │
│      ┌─────────────────────────────────────────┐    │
│      │  Service Registry (Consul/Eureka)      │    │
│      │  ├─ auth-service:3001                  │    │
│      │ ├─ order-service:3002                  │    │
│      │ ├─ product-service:3003                │    │
│      │ └─ user-service:3004                   │    │
│      └─────────────────────────────────────────┘    │
│             ▲         ▲         ▲        ▲           │
│             │         │         │        │           │
│ ┌───────────┴─────────┴─────────┴────────┴────────┐ │
│ │                                                  │ │
│ ▼                                                  ▼ │
│ ┌─────────────────────┐                ┌─────────────┐
│ │ Auth Service        │                │ Order Svc   │
│ │ (Node.js)           │                │ (Go)        │
│ │                     │                │             │
│ │ POST /login         │◄──────────────►│ Depends on  │
│ │ POST /verify-token  │ gRPC calls     │ Auth Svc    │
│ │ GET /user/:id       │                │             │
│ │                     │                │             │
│ │ Database:           │                │ Database:   │
│ │ ┏━━━━━━━━━━━━━━━━┓ │                │ ┏━━━━━━━━┓ │
│ │ ┃ auth_db        ┃ │                │ ┃ orders │ │
│ │ ┗━━━━━━━━━━━━━━━━┛ │                │ ┗━━━━━━━━┛ │
│ └─────────────────────┘                └─────────────┘
│         │                                       │     │
│         │ Publish events                        │     │
│         │ (user.created, user.updated)          │     │
│         └──────────────┬───────────────────────┘     │
│                        │                             │
│                        ▼                             │
│           ┌─────────────────────────┐               │
│           │ Event Bus (Kafka)       │               │
│           │                         │               │
│           │ Topics:                 │               │
│           │ ├─ user-events          │               │
│           │ ├─ order-events         │               │
│           │ └─ product-events       │               │
│           └─────────────────────────┘               │
│                                                     │
│ ┌───────────────────────────────────────────────┐ │
│ │ Service-to-Service Communication:            │ │
│ │                                               │ │
│ │ Auth Service ─(gRPC)─────► Order Service    │ │
│ │ (verify token)              (check user)     │ │
│ │                                               │ │
│ │ Order Service ─(REST)─────► Product Service │ │
│ │ (get product details)       (price, stock)   │ │
│ │                                               │ │
│ │ Order Service ─(Event)─────► Notification   │ │
│ │ (order.created)              Svc             │ │
│ └───────────────────────────────────────────────┘ │
│                                                    │
└──────────────────────────────────────────────────────┘

Communication Matrix:
┌──────────────────┬──────────┬──────────┬─────────────┐
│ From Service     │ To Svc   │ Protocol │ Async/Sync  │
├──────────────────┼──────────┼──────────┼─────────────┤
│ API Gateway      │ Auth     │ gRPC     │ Synchronous │
│ API Gateway      │ Order    │ REST     │ Synchronous │
│ API Gateway      │ Product  │ REST     │ Synchronous │
│ Order Service    │ Auth     │ gRPC     │ Synchronous │
│ Order Service    │ Product  │ REST     │ Synchronous │
│ Order Service    │ EventBus │ Kafka    │ Async       │
│ Notification Svc │ EventBus │ Kafka    │ Async       │
└──────────────────┴──────────┴──────────┴─────────────┘
```

### Key Patterns
- **API Gateway**: Single entry point, handles routing and auth
- **Service Discovery**: Dynamic service location and health checking
- **Event-Driven**: Async communication via event bus
- **gRPC/HTTP**: Mixed protocols for different needs
- **Circuit Breaker**: Handle service failures gracefully

---

## Template 3: Third-Party SaaS Integration

**Purpose**: Show how to integrate with external SaaS platforms

```
┌──────────────────────────────────────────────────────────┐
│          SaaS Platform Integrations                      │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Our Application                                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Core Business Logic                                │ │
│  └──┬──────────┬──────────┬──────────┬───────────────┘ │
│     │          │          │          │                 │
│     │HTTPS API │HTTPS API │REST API  │API Key Header   │
│     │          │          │          │                 │
│  ┌──▼───┐  ┌──▼────┐ ┌──▼─────┐ ┌──▼────────┐         │
│  │      │  │       │ │        │ │           │         │
│  ▼      ▼  ▼       ▼ ▼        ▼ ▼           ▼         │
│  ╔═════════════╗ ╔══════════════╗ ╔══════════════╗    │
│  ║ Stripe      ║ ║ SendGrid      ║ ║ Slack        ║    │
│  ║             ║ ║               ║ ║              ║    │
│  ║ Payment     ║ ║ Email Delivery║ ║ Team Channel ║    │
│  ║ Processing  ║ ║ & Analytics   ║ ║ Notifications    │
│  ║             ║ ║               ║ ║              ║    │
│  ║ Endpoints:  ║ ║ Endpoints:    ║ ║ Endpoints:   ║    │
│  ║ POST /      ║ ║ POST /mail/   ║ ║ POST /chat.  ║    │
│  ║  charges    ║ ║  send         ║ ║  postMessage ║    │
│  ║ POST /      ║ ║ GET /stats    ║ ║              ║    │
│  ║  refunds    ║ ║               ║ ║ Auth: OAuth  ║    │
│  ║ GET /       ║ ║ Auth: Bearer  ║ ║ 2.0          ║    │
│  ║  balance    ║ ║ Token         ║ ║              ║    │
│  ║             ║ ║               ║ ║              ║    │
│  ║ Auth: API   ║ ║ Rate Limit:   ║ ║ Webhook:     ║    │
│  ║ Key         ║ ║ 50 req/sec    ║ ║ URL validation    │
│  ║             ║ ║               ║ ║ & delivery   ║    │
│  ║ Webhook:    ║ ║               ║ ║              ║    │
│  ║ charge      ║ ║               ║ ║              ║    │
│  ║ .success    ║ ║               ║ ║              ║    │
│  ║ .failed     ║ ║               ║ ║              ║    │
│  ╚═════════════╝ ╚══════════════╝ ╚══════════════╝    │
│       │                │                │              │
│       │ Webhooks       │ Webhooks       │ Webhooks    │
│       │ to our app     │ to our app     │ to our app  │
│       │                │                │              │
│       └────────────────┬────────────────┘              │
│                        │                              │
│                        ▼                              │
│       ┌────────────────────────────────┐              │
│       │ Webhook Handler                │              │
│       │ (Verify signatures, process)   │              │
│       │                                │              │
│       │ ├─ Stripe signature: t, v1     │              │
│       │ ├─ SendGrid signature: auth    │              │
│       │ └─ Slack signature: verify     │              │
│       └────────────────┬───────────────┘              │
│                        │                              │
│                        ▼                              │
│       ┌────────────────────────────────┐              │
│       │ Event Processing               │              │
│       │                                │              │
│       │ ├─ Update order status         │              │
│       │ ├─ Log email delivery         │              │
│       │ ├─ Store notification event   │              │
│       │ └─ Trigger internal events    │              │
│       └────────────────┬───────────────┘              │
│                        │                              │
│                        ▼                              │
│       ┌────────────────────────────────┐              │
│       │ Database / Event Bus            │              │
│       │ Store integration events        │              │
│       └────────────────────────────────┘              │
│                                                       │
│  Additional Integrations:                            │
│                                                       │
│  ╔══════════════╗ ╔════════════════╗ ╔────────────╗  │
│  ║ Datadog      ║ ║ Twilio         ║ ║ Shopify    ║  │
│  ║              ║ ║                ║ ║            ║  │
│  ║ APM & Logs   ║ ║ SMS Alerts &   ║ ║ Inventory  ║  │
│  ║ Monitoring   ║ ║ Voice Calls    ║ ║ Sync       ║  │
│  ║              ║ ║                ║ ║            ║  │
│  ║ API Key      ║ ║ API Key +      ║ ║ OAuth 2.0  ║  │
│  ║ Webhook      ║ ║ Webhook        ║ ║ Private    ║  │
│  ║ Push metrics ║ ║ SMS received   ║ ║ App        ║  │
│  ║ Pull logs    ║ ║                ║ ║            ║  │
│  ╚══════════════╝ ╚════════════════╝ ╚────────────╝  │
│                                                       │
└──────────────────────────────────────────────────────┘

Integration Checklist:
✓ API Documentation reviewed
✓ Authentication method configured (API Key, OAuth, Basic)
✓ Webhook signature verification implemented
✓ Error handling & retry logic
✓ Rate limiting handled
✓ Sensitive data in environment variables
✓ Monitoring & alerting for integration failures
✓ Fallback behavior for outages
```

### Integration Patterns
- **REST APIs**: Standard HTTP/HTTPS for synchronous calls
- **Webhooks**: Async notifications for events
- **OAuth 2.0**: Secure third-party authorization
- **API Keys**: Simple authentication for trusted services
- **Rate Limiting**: Respect API quotas
- **Error Handling**: Retry logic, circuit breakers

---

## Template 4: Legacy System Migration Integration

**Purpose**: Show how to integrate legacy systems during migration

```
┌──────────────────────────────────────────────────────────┐
│      Legacy System Migration Pattern                     │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  Phase 1: Parallel Run (Current State)                  │
│                                                           │
│  Requests ─►  ┌──────────────────┐                      │
│               │ Router/Adapter   │                      │
│               │ (Strangler Fig)  │                      │
│               └────────┬──────┬──┘                      │
│                        │      │                        │
│          New feature?  │      │  Legacy feature?       │
│                   yes  │      │  yes                   │
│                        │      │                        │
│                        ▼      ▼                        │
│           ┌──────────────────┐  ┌──────────────────┐  │
│           │ New System       │  │ Legacy System    │  │
│           │ (Microservices)  │  │ (Mainframe)      │  │
│           │                  │  │                  │  │
│           │ ├─ User Service  │  │ ├─ COBOL Apps   │  │
│           │ ├─ Order Service │  │ ├─ DB2 Database │  │
│           │ ├─ Product Svc   │  │ └─ 3270 Terminal    │  │
│           │ └─ Auth Service  │  │                  │  │
│           └────────────────────┘  └──────┬───────────┘  │
│                     │                    │              │
│          Data sync via                   │              │
│          ETL job (nightly)               │              │
│                     │                    │              │
│                     └────────┬───────────┘              │
│                              │                         │
│                              ▼                         │
│               ┌─────────────────────────┐             │
│               │  Data Warehouse          │             │
│               │  (Single source of truth)│             │
│               │  ├─ Users               │             │
│               │  ├─ Orders              │             │
│               │  └─ Products            │             │
│               └─────────────────────────┘             │
│                                                        │
│  ──────────────────────────────────────────────────  │
│                                                        │
│  Phase 2: Gradual Migration                           │
│                                                        │
│  Feature toggles control routing:                     │
│  ├─ "use_new_auth" - Route auth to New System        │
│  ├─ "use_new_orders" - Route orders to New System    │
│  ├─ "enable_read_from_new" - Read from New System   │
│  └─ "enable_write_to_new" - Write to New System     │
│                                                        │
│  Requests ─►  ┌──────────────────┐                   │
│               │ Router with      │                   │
│               │ Feature Toggles  │                   │
│               └────────┬──────┬──┘                   │
│                        │      │                     │
│              Toggle=1  │      │  Toggle=0           │
│                   ┌────┘      └────┐                │
│                   ▼                 ▼               │
│          ┌──────────────────┐ ┌──────────────────┐ │
│          │ New System       │ │ Legacy System    │ │
│          │ (100% features)  │ │ (Gradual reduce) │ │
│          │                  │ │                  │ │
│          │ Read-Write       │ │ Read-Write       │ │
│          │ All features     │ │ Reduced features │ │
│          └──────────────────┘ └──────────────────┘ │
│                   │                  │              │
│                   └────────┬─────────┘              │
│                            │                       │
│                            ▼                       │
│               ┌─────────────────────────┐          │
│               │  Data Sync Layer         │          │
│               │  (Bi-directional sync)   │          │
│               │  - Log-based CDC         │          │
│               │  - Change Data Capture   │          │
│               │  - Eventual consistency  │          │
│               └─────────────────────────┘          │
│                                                     │
│  ──────────────────────────────────────────────── │
│                                                     │
│  Phase 3: Completion (Target State)                │
│                                                     │
│  Requests ─────────────────────────────┐           │
│                                        │           │
│                                        ▼           │
│                            ┌──────────────────┐    │
│                            │ New System       │    │
│                            │ (100% features)  │    │
│                            │                  │    │
│                            │ Microservices    │    │
│                            │ Cloud Native     │    │
│                            │ Scalable         │    │
│                            └──────────────────┘    │
│                                   │                │
│                                   ▼                │
│                    ┌────────────────────────┐     │
│                    │ Modern Database        │     │
│                    │ (PostgreSQL/MongoDB)   │     │
│                    └────────────────────────┘     │
│                                                    │
│  Legacy System: Decommissioned                    │
│                                                    │
└────────────────────────────────────────────────────┘

Migration Timeline:
├─ Phase 1: Setup (Months 1-2)
│   ├─ Build strangler fig layer
│   ├─ Implement data sync
│   └─ Run in parallel
├─ Phase 2: Gradual (Months 3-12)
│   ├─ Enable toggles per feature
│   ├─ Validate data consistency
│   └─ Monitor metrics
└─ Phase 3: Completion (Month 13+)
    ├─ Disable remaining toggles
    ├─ Verify all data migrated
    └─ Decommission legacy system
```

### Key Principles
- **Strangler Fig Pattern**: Gradually replace legacy systems
- **Feature Flags**: Control which system serves requests
- **Data Synchronization**: Keep both systems in sync
- **Parallel Running**: Test new system with real data
- **Gradual Cutover**: Reduce legacy system load over time
- **Rollback Plan**: Quick recovery if issues occur

---

## Best Practices

### Do's ✓
- Show system boundaries clearly
- Label all communication types (REST, gRPC, Webhooks, etc.)
- Include authentication methods (API Key, OAuth, JWT, etc.)
- Show error/fallback paths
- Include rate limiting and retry logic
- Document webhook/event format
- Show monitoring and alerting points
- Include security considerations (encryption, signature verification)

### Don'ts ✗
- Forget to show external system dependencies
- Omit authentication/security details
- Mix multiple integration patterns confusingly
- Skip error handling and timeouts
- Overcomplicate with too many systems
- Forget about rate limits and quotas
- Omit monitoring and alerting

---

## Tips for Effective Integration Diagrams

1. **System Boundaries**: Clearly separate your systems from external ones
2. **Communication Protocols**: Always specify HTTP, gRPC, Kafka, etc.
3. **Data Flow**: Show what data moves in each direction
4. **Error Handling**: Include retry logic, fallbacks, circuit breakers
5. **Authentication**: Document how each system is authenticated
6. **Async vs Sync**: Differentiate between synchronous and asynchronous calls
7. **Monitoring**: Show where observability points exist
8. **Webhooks**: Include signature verification mechanisms

---

**Template Version**: 1.0
**Best for**: System integration documentation, API design, third-party integration guides, migration planning
