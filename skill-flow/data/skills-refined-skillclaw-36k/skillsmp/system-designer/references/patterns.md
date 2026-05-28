# System Designer

## Patterns


---
  #### **Name**
Start Monolith, Evolve to Services
  #### **Description**
Begin with a monolith, extract services when boundaries become clear
  #### **When**
Any new project, especially with uncertain requirements
  #### **Example**
    # Phase 1: Well-structured monolith
    """
    /app
      /users          # User module
      /orders         # Order module
      /payments       # Payment module
      /notifications  # Notification module
    
    Each module has clear interface, could become service later.
    All share one database, one deployment.
    """
    
    # When to extract a service? Only when ALL true:
    # 1. Module has different scaling needs (10x more load)
    # 2. Module needs independent deployment (different release cycle)
    # 3. Team ownership is clear (dedicated team for this domain)
    # 4. Interface is stable (no churn in how other modules call it)
    
    # Phase 2: Extract first service when justified
    """
    /app
      /users
      /orders
      /payments
    
    notifications-service/  # Extracted because:
      - High volume, different scaling
      - Can be async (doesn't block orders)
      - Simple interface (fire and forget)
    """
    
    # Warning signs you extracted too early:
    # - Constantly changing the service interface
    # - Service and monolith deployed together anyway
    # - Debugging requires reading logs from multiple systems
    

---
  #### **Name**
Four Pillars Assessment
  #### **Description**
Evaluate system against scalability, availability, reliability, performance
  #### **When**
Designing or reviewing any system
  #### **Example**
    # For any system, assess these four pillars:
    
    ## SCALABILITY
    # Can the system handle growth?
    """
    Questions:
    - What's 10x current load? 100x?
    - Which component breaks first under load?
    - Can we scale horizontally (add instances)?
    - What's the cost curve for scaling?
    
    Red flags:
    - Single database write path
    - In-memory state in web servers
    - Synchronous calls to slow services
    """
    
    ## AVAILABILITY
    # Is the system operational when needed?
    """
    Questions:
    - What's the SLA/SLO? (99.9% = 8.7 hours/year downtime)
    - What are the single points of failure?
    - How long is recovery from each failure mode?
    - What fails gracefully, what fails completely?
    
    Red flags:
    - No redundancy for critical paths
    - Single region deployment
    - No health checks or circuit breakers
    """
    
    ## RELIABILITY
    # Does the system do what it's supposed to?
    """
    Questions:
    - What happens when components disagree?
    - How do we ensure data consistency?
    - What's the blast radius of a bug?
    - How do we detect silent failures?
    
    Red flags:
    - No data validation at boundaries
    - Optimistic assumptions about external services
    - Missing idempotency for operations
    """
    
    ## PERFORMANCE
    # Is the system fast enough?
    """
    Questions:
    - What's acceptable latency? P50, P99?
    - Where are the hot paths?
    - What can be cached?
    - What can be async?
    
    Red flags:
    - N+1 queries
    - Synchronous chains of network calls
    - No caching layer
    """
    

---
  #### **Name**
C4 Model Documentation
  #### **Description**
Four levels of architecture diagrams from context to code
  #### **When**
Documenting system architecture
  #### **Example**
    # C4 Model: Four levels of zoom
    
    ## Level 1: System Context
    # Who uses it? What external systems?
    """
    +--------+     +----------------+     +----------+
    |  User  | --> |  Our System    | --> | Payment  |
    +--------+     +----------------+     | Provider |
                          |              +----------+
                          v
                   +-----------+
                   | Email     |
                   | Provider  |
                   +-----------+
    
    Keep it simple: one box for your system, boxes for external actors.
    Non-technical stakeholders should understand this.
    """
    
    ## Level 2: Container Diagram
    # What are the major deployable units?
    """
    +------------------+      +------------------+
    | Web App          |      | Mobile App       |
    | (React)          |      | (React Native)   |
    +--------+---------+      +--------+---------+
             |                         |
             +------------+------------+
                          |
                  +-------v--------+
                  | API Server     |
                  | (Node.js)      |
                  +-------+--------+
                          |
             +------------+------------+
             |                         |
     +-------v--------+       +--------v-------+
     | PostgreSQL     |       | Redis          |
     | (Primary DB)   |       | (Cache)        |
     +----------------+       +----------------+
    
    Containers = deployable units (apps, databases, caches)
    Show protocols: HTTPS, SQL, Redis protocol
    """
    
    ## Level 3: Component Diagram
    # What are the major components inside a container?
    """
    API Server contains:
    +--------------------------------------------------+
    | +------------+  +------------+  +-------------+  |
    | | Auth       |  | Orders     |  | Payments    |  |
    | | Controller |  | Controller |  | Controller  |  |
    | +-----+------+  +-----+------+  +------+------+  |
    |       |               |                |         |
    | +-----v------+  +-----v------+  +------v------+  |
    | | Auth       |  | Order      |  | Payment     |  |
    | | Service    |  | Service    |  | Service     |  |
    | +-----+------+  +-----+------+  +------+------+  |
    |       |               |                |         |
    | +-----v---------------v----------------v------+  |
    | |              Repository Layer              |  |
    | +--------------------------------------------+  |
    +--------------------------------------------------+
    """
    
    ## Level 4: Code Diagram
    # Usually skip - your IDE shows this
    # Only draw for critical algorithms or patterns
    
    # Best practice: Context + Container diagrams for most systems.
    # Component only for complex containers.
    # Code almost never.
    

---
  #### **Name**
API Design First
  #### **Description**
Design the API contract before implementation
  #### **When**
Building services that others will consume
  #### **Example**
    # Design the contract, then implement
    
    # Step 1: Define resources and operations
    """
    Resources:
    - Orders (CRUD + search)
    - OrderItems (nested under Order)
    - Users (read-only from our perspective)
    """
    
    # Step 2: Define endpoints with examples
    """
    POST /orders
    {
      "user_id": "u123",
      "items": [{"product_id": "p456", "quantity": 2}]
    }
    
    Response 201:
    {
      "id": "o789",
      "status": "pending",
      "total": 99.99,
      "created_at": "2024-01-15T10:00:00Z"
    }
    """
    
    # Step 3: Define error responses
    """
    400: Validation error (with field-level details)
    401: Not authenticated
    403: Not authorized for this resource
    404: Resource not found
    409: Conflict (e.g., duplicate order)
    500: Internal error (with correlation ID)
    """
    
    # Step 4: Write OpenAPI spec before code
    # - Generates documentation
    # - Generates client SDKs
    # - Enables contract testing
    
    # Anti-pattern: Designing API after implementation
    # Results in leaky abstractions and inconsistent patterns
    

---
  #### **Name**
Data Model First
  #### **Description**
Design the data model before the code
  #### **When**
Starting any feature that involves persistent data
  #### **Example**
    # The data model is the foundation. Get it wrong, everything suffers.
    
    # Step 1: Identify entities and relationships
    """
    User (1) ---< Order (*)
    Order (1) ---< OrderItem (*)
    Product (1) ---< OrderItem (*)
    """
    
    # Step 2: Define fields and constraints
    """
    users:
      id: uuid PRIMARY KEY
      email: text UNIQUE NOT NULL
      created_at: timestamp NOT NULL
    
    orders:
      id: uuid PRIMARY KEY
      user_id: uuid REFERENCES users NOT NULL
      status: enum('pending', 'paid', 'shipped', 'delivered')
      total_cents: integer NOT NULL  # Store money as cents!
      created_at: timestamp NOT NULL
    
    order_items:
      id: uuid PRIMARY KEY
      order_id: uuid REFERENCES orders NOT NULL
      product_id: uuid REFERENCES products NOT NULL
      quantity: integer CHECK (quantity > 0)
      price_cents: integer NOT NULL  # Price at time of order
    """
    
    # Step 3: Consider query patterns
    """
    Common queries:
    - Get all orders for a user (index on user_id)
    - Get orders by status (index on status)
    - Get order with items (join or eager load)
    
    Indexes:
      CREATE INDEX idx_orders_user_id ON orders(user_id);
      CREATE INDEX idx_orders_status ON orders(status);
    """
    
    # Step 4: Consider data lifecycle
    """
    - How long do we keep orders? (Retention policy)
    - Soft delete or hard delete?
    - What about GDPR deletion requests?
    """
    

---
  #### **Name**
Failure Mode Analysis
  #### **Description**
Systematically identify and mitigate failure modes
  #### **When**
Designing any system that needs to be reliable
  #### **Example**
    # For each external dependency, ask: "What if this fails?"
    
    """
    COMPONENT: Payment Service (Stripe)
    
    Failure modes:
    1. Timeout (Stripe slow or unresponsive)
       - Impact: User can't complete checkout
       - Mitigation: 10s timeout, retry with backoff, show "try again"
       - Fallback: Queue payment for retry, show "processing"
    
    2. Error (Stripe rejects request)
       - Impact: Payment fails
       - Mitigation: Parse error, show specific message
       - Fallback: Offer different payment method
    
    3. Partial failure (charge succeeded, webhook failed)
       - Impact: Order not marked as paid
       - Mitigation: Idempotency keys, reconciliation job
       - Fallback: Manual investigation queue
    
    4. Complete outage (Stripe down)
       - Impact: No payments possible
       - Mitigation: Circuit breaker, status page check
       - Fallback: Accept orders, charge later (if business allows)
    """
    
    # For each internal component, ask same questions:
    """
    COMPONENT: Database (PostgreSQL)
    
    Failure modes:
    1. Connection exhaustion
    2. Slow queries
    3. Primary failure
    4. Replication lag
    
    [Same analysis for each]
    """
    
    # Output: Failure mode table
    """
    | Component | Failure    | Impact  | Mitigation        | Fallback       |
    |-----------|------------|---------|-------------------|----------------|
    | Stripe    | Timeout    | High    | Retry + backoff   | Queue + retry  |
    | Stripe    | Outage     | Critical| Circuit breaker   | Defer payment  |
    | DB        | Conn exh.  | Critical| Pool monitoring   | Shed load      |
    """
    

## Anti-Patterns


---
  #### **Name**
Big Ball of Mud
  #### **Description**
System without recognizable architecture
  #### **Why**
    No clear boundaries, everything depends on everything. Change is scary
    because you don't know what will break. New developers take months to
    understand the system. Technical debt accumulates exponentially.
    
  #### **Instead**
Define clear module boundaries. Even in a monolith, enforce interfaces between components.

---
  #### **Name**
Distributed Monolith
  #### **Description**
Microservices that must be deployed together
  #### **Why**
    All the complexity of microservices, none of the benefits. Services are
    tightly coupled through shared databases, synchronous calls, or shared
    models. Can't deploy independently, can't scale independently.
    
  #### **Instead**
If services share a database or always deploy together, merge them. Real microservices have independent data stores.

---
  #### **Name**
Golden Hammer
  #### **Description**
Using familiar technology for every problem
  #### **Why**
    "We know Kafka, so let's use it for everything." But Kafka is overkill
    for 100 events/day. "We know React, so the admin panel uses React."
    But a simple CRUD admin is faster with server-rendered HTML.
    
  #### **Instead**
Match technology to problem. Use boring tech by default, special tech only when justified.

---
  #### **Name**
Resume-Driven Development
  #### **Description**
Choosing technology for career advancement
  #### **Why**
    Kubernetes for 3-person startup. GraphQL for internal tool. Microservices
    for MVP. Technology chosen because it's impressive, not appropriate.
    Team spends more time on infrastructure than product.
    
  #### **Instead**
Optimize for shipping. The most impressive thing on your resume is "system that made $X."

---
  #### **Name**
Premature Decomposition
  #### **Description**
Breaking into services before understanding domain
  #### **Why**
    You're drawing service boundaries before you understand the domain.
    Wrong boundaries are incredibly expensive to fix - you'll need to
    move data, change APIs, and coordinate multiple teams.
    
  #### **Instead**
Build a well-structured monolith. Extract services only when you have evidence for the boundaries.

---
  #### **Name**
Synchronous Chain of Doom
  #### **Description**
Long chains of synchronous service calls
  #### **Why**
    User request calls Service A, which calls B, which calls C, which calls D.
    Latency adds up. Any failure breaks the chain. Debugging spans 4 services.
    This is a distributed monolith with extra steps.
    
  #### **Instead**
Keep critical paths short. Use async for non-critical operations. Consider if you need separate services at all.