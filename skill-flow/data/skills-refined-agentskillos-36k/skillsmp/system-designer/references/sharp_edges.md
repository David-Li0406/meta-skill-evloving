# System Designer - Sharp Edges

## Fallacy #1: The Network is Reliable

### **Id**
fallacy-network-reliable
### **Severity**
critical
### **Situation**
  System assumes network calls always succeed. No retry logic, no timeout
  handling, no circuit breakers. Works fine in development, fails in production
  when network has transient issues.
  
### **Why**
  Networks fail. Packets drop. Connections timeout. Routers restart. DNS fails.
  Your "never fails" network will fail at 3am on launch day. Murphy's Law is
  the only law that's never been broken.
  
### **Solution**
  1. Assume every network call can fail:
     - Add timeouts to all network operations (no default is safe)
     - Implement retry with exponential backoff
     - Use circuit breakers to fail fast when downstream is unhealthy
  
  2. Design for partial failure:
     - What if payment service is down? Can user still browse?
     - What if search is slow? Show cached results?
     - Graceful degradation over complete failure
  
  3. Test failure modes:
     - Use chaos engineering (Netflix Chaos Monkey)
     - Inject network delays in staging
     - Practice failure recovery regularly
  
### **Symptoms**
  - Hanging requests with no timeout
  - Cascading failures from one slow service
  - No retry logic in API clients
  - App completely down when one dependency fails
### **Detection Pattern**
fetch\(|axios\.|http\.|request\(|client\.

## Fallacy #2: Latency is Zero

### **Id**
fallacy-latency-zero
### **Severity**
critical
### **Situation**
  System designed assuming network calls are instant. Makes many small calls
  that work fine locally but are painfully slow across network. N+1 queries
  to remote services. Chatty APIs.
  
### **Why**
  Even same-datacenter calls are 0.5-1ms minimum. Cross-region is 50-100ms.
  Make 100 calls in sequence and you've added 5-10 seconds. Latency kills
  user experience and makes debugging a nightmare.
  
### **Solution**
  1. Minimize network round trips:
     - Batch requests where possible
     - Use GraphQL or batch endpoints
     - Prefetch data before it's needed
  
  2. Make latency visible in development:
     - Add artificial delay in local testing (100ms per call)
     - Measure P50, P95, P99 latency, not just average
     - Alert on latency spikes, not just errors
  
  3. Design for latency:
     - New York to London: ~80ms RTT
     - Use CDN for static content
     - Consider data locality (keep data close to compute)
  
### **Symptoms**
  - Page takes seconds to load in production
  - Works fast locally, slow in staging/prod
  - Many sequential network calls in a request
  - Loading spinners everywhere
### **Detection Pattern**
await.*await.*await|for.*await|loop.*fetch

## Fallacy #3: Bandwidth is Infinite

### **Id**
fallacy-bandwidth-infinite
### **Severity**
high
### **Situation**
  System sends large payloads without considering network capacity. Pushes
  full objects when deltas would suffice. No compression. Mobile users on
  slow connections suffer.
  
### **Why**
  Bandwidth costs money and has limits. Mobile networks are especially
  constrained. Large payloads increase latency (time to transmit) and cost
  (data transfer charges). What's fine at 1000 users breaks at 100,000.
  
### **Solution**
  1. Minimize payload size:
     - Send only needed fields (sparse fieldsets)
     - Use pagination for large lists
     - Compress responses (gzip, brotli)
  
  2. Optimize for different clients:
     - Mobile gets smaller images
     - API clients can request reduced payloads
     - Consider GraphQL for client-driven queries
  
  3. Monitor bandwidth:
     - Track response size distribution
     - Alert on unusually large responses
     - Measure data transfer costs
  
### **Symptoms**
  - Slow on mobile networks
  - High data transfer costs
  - Large JSON responses with unused fields
  - Timeout issues on large requests
### **Detection Pattern**
toJSON|serialize|JSON\.stringify

## Fallacy #4: The Network is Secure

### **Id**
fallacy-network-secure
### **Severity**
critical
### **Situation**
  System trusts data from network without validation. Assumes internal
  network is safe. Uses HTTP instead of HTTPS internally. Doesn't encrypt
  sensitive data in transit.
  
### **Why**
  The network is hostile territory. Even "internal" networks can be
  compromised. Man-in-the-middle attacks are real. Assuming security
  is a matter of "when compromised" not "if compromised."
  
### **Solution**
  1. Encrypt everything:
     - HTTPS everywhere, even internal
     - TLS 1.3 minimum
     - Certificate validation (don't skip!)
  
  2. Validate all input:
     - Don't trust data from any source
     - Validate at service boundaries
     - Sanitize before database or display
  
  3. Defense in depth:
     - Network segmentation
     - Service mesh with mTLS
     - Regular security audits
  
### **Symptoms**
  - HTTP instead of HTTPS anywhere
  - Trust based on source IP
  - Sensitive data logged or transmitted plain
  - No input validation on internal APIs
### **Detection Pattern**
http://|trustAllCerts|InsecureSkipVerify|verify=False

## Fallacy #5: Topology Doesn't Change

### **Id**
fallacy-topology-static
### **Severity**
high
### **Situation**
  Hardcoded IP addresses, hostnames, or service locations. System breaks
  when services move, scale, or failover. Can't add new instances without
  config changes.
  
### **Why**
  In cloud environments, everything moves. Instances come and go. IPs change.
  Services scale up and down. Hardcoding locations creates brittleness that
  contradicts the whole point of cloud-native design.
  
### **Solution**
  1. Use service discovery:
     - DNS-based discovery (Kubernetes services)
     - Service registry (Consul, Eureka)
     - Environment variables for endpoints
  
  2. Design for dynamic topology:
     - Health checks to detect failed instances
     - Load balancing across instances
     - Graceful handling of instance changes
  
  3. Never hardcode:
     - IPs belong in config, not code
     - Use DNS names, not raw IPs
     - Support runtime reconfiguration
  
### **Symptoms**
  - Hardcoded IPs or hostnames in code
  - Deployment requires code changes
  - Manual config updates when scaling
  - Failures after infrastructure changes
### **Detection Pattern**
\d+\.\d+\.\d+\.\d+|localhost:\d+

## Fallacy #6: There is One Administrator

### **Id**
fallacy-one-admin
### **Severity**
medium
### **Situation**
  System assumes single owner with full control. No multi-tenancy
  considerations. No access control granularity. One person's mistake
  affects everyone.
  
### **Why**
  Large systems have multiple stakeholders, teams, and operational roles.
  Different people need different access. Changes in one area shouldn't
  require coordinating with everyone. Blast radius must be limited.
  
### **Solution**
  1. Design for multiple operators:
     - Role-based access control
     - Team-scoped resources
     - Audit logging for changes
  
  2. Limit blast radius:
     - Namespace isolation
     - Resource quotas per team
     - Change approval workflows
  
  3. Enable self-service:
     - Teams can manage their resources
     - Reduce centralized bottlenecks
     - Clear ownership and responsibility
  
### **Symptoms**
  - Single admin account for everything
  - No audit trail of changes
  - All-or-nothing permissions
  - Changes require central team approval
### **Detection Pattern**
admin|root|superuser

## Fallacy #7: Transport Cost is Zero

### **Id**
fallacy-transport-free
### **Severity**
medium
### **Situation**
  System doesn't account for data transfer costs. Shuffles large amounts
  of data between regions or clouds. Ignores egress charges that add up
  to significant monthly bills.
  
### **Why**
  Cloud providers charge for data egress. Cross-region transfer costs more
  than in-region. Cross-cloud is most expensive. What seems like free
  network calls becomes significant at scale.
  
### **Solution**
  1. Minimize cross-region traffic:
     - Keep related services in same region
     - Cache aggressively at the edge
     - Use CDN for static content
  
  2. Monitor and optimize:
     - Track data transfer by source/destination
     - Identify largest flows
     - Consider data locality in architecture
  
  3. Design for cost:
     - Estimate transfer costs before architecture decisions
     - Multi-region adds cost, not just complexity
     - Compress large payloads
  
### **Symptoms**
  - Unexpectedly high cloud bills
  - Lots of cross-region API calls
  - No visibility into data flow
  - Cost surprises at scale
### **Detection Pattern**
region|cross-region|multi-region|egress

## Fallacy #8: The Network is Homogeneous

### **Id**
fallacy-network-homogeneous
### **Severity**
medium
### **Situation**
  Assumes all parts of network are equal. Ignores differences between
  datacenter network, public internet, mobile networks, international
  connectivity. Same timeout for all calls.
  
### **Why**
  Network characteristics vary wildly. Datacenter: 0.1ms, 10Gbps. Home:
  20ms, 100Mbps. Mobile: 100ms, 1Mbps with packet loss. International:
  200ms+. One-size-fits-all settings fail somewhere.
  
### **Solution**
  1. Know your network segments:
     - Internal DC: aggressive timeouts, high throughput
     - Internet: longer timeouts, retry logic
     - Mobile: compression, offline support
  
  2. Adapt to conditions:
     - Client-side: detect network type
     - Server-side: different timeouts for different targets
     - Graceful degradation for poor conditions
  
  3. Test across conditions:
     - Test on slow networks (Chrome DevTools throttling)
     - Test with packet loss
     - Test from different geographic locations
  
### **Symptoms**
  - Works in datacenter, fails from mobile
  - International users complain about slowness
  - Timeouts not tuned to network conditions
  - No consideration of network diversity
### **Detection Pattern**
timeout.*1000|timeout.*5000

## The Shared Database Trap

### **Id**
shared-database-coupling
### **Severity**
critical
### **Situation**
  Multiple services share a database directly. Seems convenient - no need
  for APIs. But now every service is coupled to the schema. Can't change
  one without coordinating with all.
  
### **Why**
  Shared database = shared coupling. Schema changes require coordinated
  deploys. Performance problems in one service affect all. No way to
  scale services independently. This is a distributed monolith.
  
### **Solution**
  1. Each service owns its data:
     - One service = one database (or schema)
     - Other services call APIs, not tables
     - Service is responsible for its data integrity
  
  2. When you need data from another service:
     - Call their API
     - Cache if needed for performance
     - Accept eventual consistency for some reads
  
  3. Migration path:
     - Identify which service owns which tables
     - Create APIs for cross-service data access
     - Gradually remove direct table access
  
### **Symptoms**
  - Multiple services write to same tables
  - Schema changes require multi-team coordination
  - Can't deploy one service without others
  - Database is the integration layer
### **Detection Pattern**
shared.*database|common.*schema|cross.*service.*query

## Synchronous When You Need Async

### **Id**
sync-over-async
### **Severity**
high
### **Situation**
  User request waits for slow operation to complete. Sending email blocks
  checkout. Generating report blocks the API. System is only as fast as
  its slowest synchronous call.
  
### **Why**
  Not everything needs an immediate response. Email can be sent in 30 seconds
  instead of blocking checkout for 2 seconds. Report can be generated async
  and user notified when ready. Sync blocks resources, async frees them.
  
### **Solution**
  1. Identify async candidates:
     - Notifications (email, SMS, push)
     - Report generation
     - Data processing
     - Third-party integrations
  
  2. Implement async patterns:
     - Message queue (Redis, SQS, RabbitMQ)
     - Background workers
     - Webhook callbacks for completion
  
  3. Design UX for async:
     - "Your report is being generated"
     - Progress indicators
     - Notifications when complete
  
### **Symptoms**
  - API times out on complex operations
  - User waits for non-essential operations
  - Single slow service blocks entire flow
  - Horizontal scaling doesn't help response time
### **Detection Pattern**
await sendEmail|await generateReport|await notify

## Non-Idempotent Operations

### **Id**
missing-idempotency
### **Severity**
critical
### **Situation**
  Network hiccup during payment. Client retries. Two charges created.
  User clicks submit twice. Two orders created. No way to safely retry
  failed operations.
  
### **Why**
  Networks fail. Users double-click. Clients retry. If your operations
  aren't idempotent, duplicates happen. For payments and orders, duplicates
  are expensive mistakes.
  
### **Solution**
  1. Use idempotency keys:
     - Client generates unique key per operation
     - Server deduplicates using the key
     - Same key = same result (cached response)
  
  2. Design idempotent operations:
     - "Set X to 5" is idempotent
     - "Add 5 to X" is not
     - Prefer set/replace over increment/append
  
  3. Implement deduplication:
     - Store operation results with their keys
     - Return cached result on duplicate key
     - Key expiry after safe window
  
### **Symptoms**
  - Duplicate records after retries
  - Double charges/orders
  - "Click once" warnings needed
  - Fear of retrying failed operations
### **Detection Pattern**
increment|append|push|add|+=|\+\+

## Unbounded Query Results

### **Id**
missing-pagination
### **Severity**
high
### **Situation**
  API returns all results. Works with 100 users, crashes with 100,000.
  Memory spikes, timeouts, database locks. What was instant becomes
  impossible.
  
### **Why**
  Data grows. What's 100 rows today is 10 million tomorrow. Without
  pagination, queries eventually timeout or OOM. And you won't know
  until production at scale.
  
### **Solution**
  1. Always paginate list endpoints:
     - Limit + offset (simple, inefficient for large offsets)
     - Cursor-based (efficient, more complex)
     - Default limit (e.g., 50), max limit (e.g., 500)
  
  2. Design for large datasets from start:
     - Index columns used for sorting
     - Consider search/filter to reduce result size
     - Stream results for exports
  
  3. Protect against abuse:
     - Rate limiting
     - Maximum page size
     - Timeout for expensive queries
  
### **Symptoms**
  - API endpoint times out at scale
  - Memory spikes on list endpoints
  - "Just add limit" refactoring
  - Database performance degradation
### **Detection Pattern**
SELECT \* FROM|findAll\(\)|find\(\{\}\)