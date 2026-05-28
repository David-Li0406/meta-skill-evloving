# Sequence Diagram Templates

Sequence diagrams show interactions between actors and systems over time. Time flows from top to bottom, and messages flow horizontally between participants.

---

## Template 1: Basic API Request Flow

**Purpose**: Show a simple request-response sequence

```
User          Browser         API Server      Database
│               │               │               │
│─ Click Login ─►│               │               │
│               │               │               │
│               │─ POST /login ─►│               │
│               │  (credentials) │               │
│               │               │               │
│               │               │─ Verify ─────►│
│               │               │   password    │
│               │               │◄──── Data ───│
│               │               │               │
│               │               │─ Create ─────►│
│               │               │   session    │
│               │◄─ 200 OK ──────│               │
│               │  (JWT token)   │               │
│               │               │               │
│◄─ Logged In ──│               │               │
│               │               │               │

[Shows successful login flow with credential verification and session creation]
```

### Elements
- **Participants**: Vertical lifelines (actors, systems)
- **Messages**: Horizontal arrows between participants
- **Time**: Flows top to bottom
- **Activations**: Period when participant is active

---

## Template 2: E-Commerce Checkout Flow

**Purpose**: Show multi-step transaction with error handling

```
Customer    Frontend      Backend API    Payment Svc    Email Service
│              │              │              │              │
│─ Add Item ───►│              │              │              │
│              │              │              │              │
│─ Proceed ─────►│              │              │              │
│              │              │              │              │
│              │─ POST /orders►│              │              │
│              │ (items, addr) │              │              │
│              │              │              │              │
│              │              │─ Validate ─┐ │              │
│              │              │  inventory │ │              │
│              │              │◄─────────────┘              │
│              │              │              │              │
│              │              │─ Reserve ────►│              │
│              │              │  items       │              │
│              │              │◄── OK ───────│              │
│              │              │              │              │
│              │◄─ 201 Order ─│              │              │
│              │  (order ID)  │              │              │
│              │              │              │              │
│─ Pay ────────►│              │              │              │
│              │─ POST /pay ──►│              │              │
│              │ (order, card) │              │              │
│              │              │              │              │
│              │              │─ Charge ────►│              │
│              │              │ (amount)     │              │
│              │              │◄─ Success ───│              │
│              │              │              │              │
│              │              │─ Create ────►│              │
│              │              │  shipping    │              │
│              │              │              │              │
│              │              │──────────────┼─ Send ──────►│
│              │              │              │   receipt    │
│              │              │              │              │
│◄─ Success ───│◄─ 200 OK ────│              │              │
│ Confirmation │ (tracking)   │              │              │
│              │              │              │              │

[Shows complete checkout with payment processing and confirmation]
```

### Key Interactions
- **Request-Response**: Solid arrows for synchronous calls
- **Asynchronous**: Dashed arrows for async operations
- **Return values**: Labeled responses
- **Conditions**: [Bracketed notes for conditional flows]

---

## Template 3: Microservices Communication

**Purpose**: Show interaction between multiple services

```
API Gateway   User Service   Product Service   Order Service   Cache
│                 │                │                │            │
│─ GET /user ────►│                │                │            │
│                 │                │                │            │
│                 │─ Check Cache ──┼─────────────┼─ Lookup ────►│
│                 │                │             │              │
│                 │                │             │◄── Found ────│
│                 │                │             │              │
│                 │◄─ User Data ───┼─────────────┼─────────────►│
│◄─ 200 OK ───────│                │                │  (cache it) │
│                 │                │                │            │
│─ GET /products ─┼──────────────────────────┐    │            │
│                 │                │         │    │            │
│                 │              ┌─┴────────►│    │            │
│                 │              │  Product  │    │            │
│                 │              │  Service  │    │            │
│                 │              │   Logic   │    │            │
│                 │              └─┬────────►│    │            │
│                 │                │         │    │            │
│◄─ 200 OK ──────────── Product ──┴────────►│    │            │
│                 │      List      │          │    │            │
│                 │                │          │    │            │
│─ POST /orders ──┼────────────────┼─────────►│    │            │
│                 │                │     Order│    │            │
│                 │                │  Service │    │            │
│                 │                │          │    │            │
│                 │◄─ Order Created┼─────────│    │            │
│◄─ 201 Created ──┤                │          │    │            │
│ (order ID)      │                │          │    │            │
│                 │                │          │    │            │

[Shows how multiple services communicate through API Gateway with caching]
```

---

## Template 4: Event-Driven Architecture

**Purpose**: Show asynchronous event-based communication

```
Producer Service    Message Queue    Service A    Service B    Database
│                       │               │            │            │
│─ Order Created ──────►│               │            │            │
│  (event published)    │               │            │            │
│                       │               │            │            │
│                       │- - Order - - ►│            │            │
│                       │  Placed       │            │            │
│                       │               │            │            │
│                       │               │─ Process ──┐            │
│                       │               │  order     │            │
│                       │               │            ▼            │
│                       │               │         ┌──────┐        │
│                       │               │         │Event │        │
│                       │               │         │Actn: │        │
│                       │               │         └──────┘        │
│                       │               │            │            │
│                       │               │            │            │
│                       │- - - Order - ─┼───────────►│            │
│                       │  Confirmed    │    │       │            │
│                       │               │    └──────►│            │
│                       │               │  Update    │            │
│                       │               │  status    │            │
│                       │               │            │            │
│                       │               │            │─ Save ────►│
│                       │               │            │ (async)    │
│                       │               │            │            │
│◄──ack delivered───────│               │            │            │
│                       │               │            │            │

[Asynchronous flow: dashed arrows represent async message delivery]
```

---

## Template 5: Error Handling and Retry Flow

**Purpose**: Show handling of failures and recovery

```
Client         API Server    Database    Cache    Notification
│                 │            │         │            │
│─ Request ──────►│            │         │            │
│                 │            │         │            │
│                 │─ Query ────►│        │            │
│                 │ ✗ Timeout   │        │            │
│                 │◄─ Error ────│        │            │
│                 │             │        │            │
│                 │─ Retry ─────►│       │            │
│                 │ [After 1s]  │       │            │
│                 │             │       │            │
│                 │             │    Check Cache ───►│
│                 │             │       │ Hit        │
│                 │◄─ Cached ────┼───────┼────────────│
│                 │  Data        │       │            │
│                 │              │       │            │
│◄─ 200 OK ──────────────────────────────────────────│
│ (from cache)    │              │       │            │
│                 │              │       │            │
│                 │──────────────────── Log ────────►│
│                 │    (recovered)      Error         │
│                 │              │       │            │

[Shows retry logic and fallback to cache on failure]
```

---

## Template 6: Authentication & Authorization Flow

**Purpose**: Show token-based authentication flow

```
User        Browser      Auth Service    API Gateway    User Service
│             │              │                │              │
│─ Login ─────►│              │                │              │
│             │              │                │              │
│             │─ POST /auth ─►│                │              │
│             │ (username,    │                │              │
│             │  password)    │                │              │
│             │              │                │              │
│             │◄─ JWT Token ──│                │              │
│             │  (exp: 1hr)   │                │              │
│             │              │                │              │
│─ Request ───►│              │                │              │
│ (w/ JWT)    │              │                │              │
│             │─ GET /data ──────────────────►│              │
│             │  (Authorization: Bearer JWT)  │              │
│             │                               │              │
│             │                               │─ Verify ────►│
│             │                               │  (JWT sig)   │
│             │                               │◄─ Valid ─────│
│             │                               │              │
│             │◄─── 200 OK (data) ────────────│              │
│◄─────────────│                               │              │
│ Protected    │                               │              │
│ Data         │                               │              │
│              │                               │              │

[Shows secure request flow with JWT validation]
```

---

## Best Practices

### Design Guidelines

✓ **Do:**
- Keep time flowing top to bottom
- Label all messages clearly
- Show error conditions
- Include return values/responses
- Keep participants vertically aligned

✗ **Don't:**
- Cross message flows without reason
- Have too many participants (max 6-7)
- Omit response messages
- Use unclear abbreviations
- Make diagrams too tall

### Naming Conventions

- **Messages**: Use clear action names (Get User, Create Order)
- **Actors**: Use role names (User, Admin, System)
- **Services**: Use domain names (Order Service, Payment Svc)
- **Status codes**: Include HTTP status when relevant

### Common Patterns

| Pattern | Usage |
|---------|-------|
| `───►` | Synchronous request |
| `◄───` | Response/return |
| `- - ►` | Asynchronous message |
| `✗` | Error condition |
| `[Note]` | Conditional or explanatory |

---

## Tips for Effective Sequence Diagrams

1. **Identify Key Flows**: Focus on critical user journeys
2. **Show Alternatives**: Include error paths and edge cases
3. **Label Clearly**: Every message needs a label
4. **Group Operations**: Use frames/boxes for complex sequences
5. **Keep It Focused**: One diagram per major flow
6. **Test Readability**: Ensure clear left-to-right flow

---

**Template Version**: 1.0
**Best for**: API documentation, user story flows, integration documentation, testing scenarios
