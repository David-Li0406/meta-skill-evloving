# Engineering Principles & Laws Reference

Comprehensive catalog of principles, laws, and patterns. Use when user asks for specific principles or when explaining why a recommendation applies.

## Table of Contents
1. [Classic Laws & Theorems](#classic-laws--theorems)
2. [SOLID Principles](#solid-principles)
3. [Design Patterns](#design-patterns)
4. [Testing Patterns](#testing-patterns)
5. [Security Patterns](#security-patterns)
6. [Operational Patterns](#operational-patterns)
7. [Data Patterns](#data-patterns)
8. [Delivery Patterns](#delivery-patterns)

---

## Classic Laws & Theorems

### Conway's Law
> Organizations design systems that mirror their communication structure.

**Implication**: Team structure affects architecture. Align teams with desired system boundaries.

### Gall's Law
> Complex systems that work evolved from simple systems that worked.

**Implication**: Start simple. Don't design the "final" complex system upfront.

### Brooks's Law
> Adding manpower to a late project makes it later.

**Implication**: Communication overhead grows quadratically with team size.

### Hofstadter's Law
> It always takes longer than you expect, even when accounting for Hofstadter's Law.

**Implication**: Pad estimates. Scope down rather than schedule out.

### Postel's Law (Robustness Principle)
> Be conservative in what you send, liberal in what you accept.

**Implication**: Strict output, tolerant input. Handle edge cases gracefully.

### Law of Leaky Abstractions
> All non-trivial abstractions leak.

**Implication**: Know what's under the abstraction. Prepare for when it leaks.

### Pareto Principle (80/20 Rule)
> 80% of effects come from 20% of causes.

**Implication**: Focus on the vital few. Optimize the hot path.

### Occam's Razor
> The simplest explanation is usually correct.

**Implication**: Prefer simple solutions. Complexity needs justification.

### Amdahl's Law
> Speedup limited by the sequential portion of the program.

**Implication**: Parallelization has diminishing returns. Optimize the sequential bottleneck.

### CAP Theorem
> Distributed systems can only guarantee two of: Consistency, Availability, Partition tolerance.

**Implication**: Pick two. Know your tradeoffs. Usually: CP or AP.

---

## SOLID Principles

### Single Responsibility (SRP)
> A class should have one, and only one, reason to change.

**In constitutions**: "Each component MUST do one thing well."

### Open/Closed (OCP)
> Open for extension, closed for modification.

**In constitutions**: Use composition, interfaces, strategy patterns.

### Liskov Substitution (LSP)
> Subtypes must be substitutable for their base types.

**In constitutions**: "Interface contracts MUST be honored by all implementations."

### Interface Segregation (ISP)
> Many specific interfaces better than one general-purpose interface.

**In constitutions**: "Don't force components to depend on methods they don't use."

### Dependency Inversion (DIP)
> Depend on abstractions, not concretions.

**In constitutions**: "High-level modules MUST NOT depend on low-level modules."

---

## GRASP Principles

### Information Expert
> Assign responsibility to the class with the information needed.

### Creator
> Assign creation responsibility to the class that has the data to initialize.

### Controller
> Assign system event handling to a use-case controller.

### Low Coupling
> Minimize dependencies between classes.

### High Cohesion
> Keep related responsibilities together.

### Polymorphism
> Handle variation through polymorphism, not conditionals.

### Pure Fabrication
> Create classes that don't represent domain concepts when needed for cohesion.

### Indirection
> Introduce intermediate objects to decouple.

### Protected Variations
> Design to protect against variation in other components.

---

## Design Patterns

### Creational
- **Factory**: Create objects without specifying exact class
- **Builder**: Construct complex objects step by step
- **Singleton**: Ensure single instance (use sparingly)
- **Prototype**: Clone existing objects

### Structural
- **Adapter**: Make incompatible interfaces compatible
- **Facade**: Simplified interface to complex subsystem
- **Decorator**: Add behavior dynamically
- **Proxy**: Control access to an object
- **Composite**: Tree structures of objects

### Behavioral
- **Strategy**: Interchangeable algorithms
- **Observer**: Notify dependents of state changes
- **Command**: Encapsulate requests as objects
- **State**: Behavior changes with internal state
- **Template Method**: Define skeleton, let subclasses fill in steps

---

## Testing Patterns

### Test Pyramid
- **Unit Tests** (base): Fast, isolated, many
- **Integration Tests** (middle): Real dependencies, fewer
- **E2E Tests** (top): Full system, fewest

### Contract Testing
> Test that services honor their API contracts.

**When to use**: Microservices, public APIs.

### Mutation Testing
> Verify tests catch changes to code.

**When to use**: Critical code paths, high-risk logic.

### Fuzzing
> Throw random/malformed input at system.

**When to use**: Parsers, security-sensitive code, input handling.

### Test Doubles
- **Stub**: Returns canned answers
- **Mock**: Verifies interactions
- **Fake**: Working implementation (in-memory DB)
- **Spy**: Records calls for later verification

### Patterns to Avoid
- **Testing implementation details**: Brittle tests
- **100% coverage obsession**: Diminishing returns
- **Mocking everything**: Tests that only test mocks
- **Flaky tests**: Worse than no tests

---

## Security Patterns

### Defense in Depth
> Multiple layers of security controls.

**Implement**: Input validation + authentication + authorization + encryption + monitoring.

### Least Privilege
> Grant minimum permissions necessary.

**Implement**: Role-based access, time-limited tokens, scoped credentials.

### Secure by Default
> Safe configuration out of the box.

**Implement**: Deny by default, explicit opt-in for risky features.

### Zero Trust
> Never trust, always verify.

**Implement**: Authenticate every request, verify every token, encrypt everything.

### Input Validation
> Validate all external input.

**Implement**: Schema validation (Zod), sanitization, allowlists over blocklists.

### Fail Secure
> On error, fail to secure state.

**Implement**: Default deny on auth failure, safe error messages (no stack traces to users).

---

## Operational Patterns

### Observability (Three Pillars)
- **Logs**: Events that happened
- **Metrics**: Aggregated measurements
- **Traces**: Request paths through system

### RED Method (Request-driven services)
- **Rate**: Requests per second
- **Errors**: Failed requests per second
- **Duration**: Distribution of request latencies

### USE Method (Resource-focused)
- **Utilization**: How busy is the resource?
- **Saturation**: How much work is queued?
- **Errors**: How many errors?

### Circuit Breaker
> Stop calling failing service temporarily.

**When to use**: Distributed systems, external dependencies.

### Bulkhead
> Isolate failures to prevent cascade.

**When to use**: Multi-tenant systems, resource isolation.

### Retry with Backoff
> Retry failed operations with increasing delays.

**Implement**: Exponential backoff + jitter.

### Health Checks
- **Liveness**: Is the process running?
- **Readiness**: Can it handle requests?
- **Startup**: Has it finished initializing?

---

## Data Patterns

### Event Sourcing
> Store state changes as sequence of events.

**When to use**: Audit requirements, replay capability, complex domain.

**When to skip**: Simple CRUD, no audit needs, tight deadlines.

### CQRS
> Separate read and write models.

**When to use**: Different read/write patterns, complex queries, event sourcing.

**When to skip**: Simple domains, small teams.

### Idempotency
> Same request produces same result.

**When to use**: Distributed systems, retry scenarios, payment processing.

### Optimistic Concurrency
> Assume no conflict, detect at commit.

**When to use**: Low contention scenarios.

### Pessimistic Locking
> Lock resources before modification.

**When to use**: High contention, critical sections.

### Saga Pattern
> Manage distributed transactions through compensating actions.

**When to use**: Microservices, long-running transactions.

### Caching Strategies
- **Cache-aside**: App manages cache
- **Read-through**: Cache manages reads
- **Write-through**: Cache manages writes
- **Write-behind**: Async write to store

---

## Delivery Patterns

### Trunk-Based Development
> Short-lived branches, frequent merges to main.

**When to use**: CI/CD, small teams, fast iteration.

### Feature Flags
> Deploy code without enabling features.

**When to use**: Gradual rollout, A/B testing, kill switches.

### Blue-Green Deployment
> Two identical environments, switch traffic.

**When to use**: Zero-downtime deploys, instant rollback needed.

### Canary Deployment
> Route small percentage of traffic to new version.

**When to use**: Risk mitigation, gradual rollout.

### Semantic Versioning
> MAJOR.MINOR.PATCH

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

---

## Short Rules & Heuristics

### Development
- **DTSTTCPW**: Do The Simplest Thing That Could Possibly Work
- **Rule of Three**: Generalize on third repetition
- **Boy Scout Rule**: Leave code cleaner than you found it
- **Pit of Success**: Make correct usage easy, mistakes hard

### Decision Making
- **If you can't explain it, it's too complex**
- **Ask "Why Now?" before adding anything**
- **Always try subtraction first**
- **Evidence over opinions**

### Quality
- **Dirty but deterministic beats clean but abstract**
- **Comments don't replace readability**
- **Refactor only when it hurts**
- **Temporary hacks must be predictable**

### Product
- **If it's not used, it doesn't exist**
- **Build for what users do, not what they say**
- **Constraints are a feature**
- **The best product removes steps**
