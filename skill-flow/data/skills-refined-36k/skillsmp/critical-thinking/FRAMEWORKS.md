# Critical Thinking Frameworks

Mental models and evaluation frameworks for analyzing technical decisions.

---

## First Principles Thinking

### What It Is
Break down complex problems into fundamental truths, then reason up from there.

### How to Apply
```
1. Identify the assumption
   "We need Redis for caching"

2. Break it down
   - What problem are we solving? → Reduce database load
   - What are the fundamental requirements? → Fast reads, temporary storage
   - What are all possible solutions? → In-memory cache, CDN, read replicas, query optimization

3. Rebuild from fundamentals
   - Do we actually need a separate cache?
   - Could query optimization solve the problem?
   - What's the simplest solution that works?
```

### Questions to Ask
- What are we actually trying to achieve?
- What would we do if we had to start from scratch?
- What constraints are real vs. assumed?

---

## Inversion

### What It Is
Instead of asking "How do I succeed?", ask "How could I fail?"

### How to Apply
```
Goal: Build a reliable microservice

Inverted: How could this microservice fail?
- No health checks → undetected failures
- No circuit breakers → cascade failures
- No retries → transient failures become permanent
- No monitoring → blind to problems
- No rate limiting → resource exhaustion

Now ensure each failure mode is addressed.
```

### Template
| Goal | Inverted Question | Failure Modes |
|------|-------------------|---------------|
| High availability | How could this become unavailable? | Single points of failure, no failover, no health checks |
| Data integrity | How could data be corrupted? | Race conditions, no validation, no transactions |
| Performance | How could this become slow? | N+1 queries, no caching, synchronous blocking |

---

## Second-Order Thinking

### What It Is
Consider the consequences of the consequences.

### How to Apply
```
First-order: "Let's add caching to speed up reads"
Second-order:
  - Cache invalidation complexity
  - Stale data issues
  - Additional infrastructure to maintain
  - New failure modes
  - Debugging becomes harder

Third-order:
  - Team needs caching expertise
  - Monitoring for cache hit rates
  - Cache warming strategies
  - Cost of cache infrastructure
```

### Template
| Decision | 1st Order Effect | 2nd Order Effect | 3rd Order Effect |
|----------|------------------|------------------|------------------|
| Add microservice | Separation of concerns | Inter-service communication | Distributed tracing, eventual consistency |
| Use NoSQL | Flexible schema | No joins | Data denormalization, consistency challenges |

---

## Pre-Mortem Analysis

### What It Is
Imagine the project has failed. Work backwards to identify why.

### How to Apply
```
Scenario: It's 6 months from now. The new service is down and causing
outages. What went wrong?

Possible causes:
1. We didn't account for traffic spikes
2. The third-party API we depend on became unreliable
3. Database migrations took longer than expected
4. The team didn't understand the new technology
5. Monitoring gaps meant we didn't catch issues early

Now address each before starting.
```

### Template
```markdown
## Pre-Mortem: [Project Name]

**Scenario:** It's [timeframe] from now. [Project] has failed. Why?

### Technical Failures
- [ ] [Failure mode 1]
- [ ] [Failure mode 2]

### Process Failures
- [ ] [Failure mode 1]
- [ ] [Failure mode 2]

### External Failures
- [ ] [Failure mode 1]
- [ ] [Failure mode 2]

### Mitigations
| Failure | Mitigation | Owner |
|---------|------------|-------|
| | | |
```

---

## Eisenhower Matrix (for Prioritization)

### What It Is
Categorize concerns by urgency and importance.

### How to Apply
```
                    URGENT              NOT URGENT
              ┌─────────────────┬─────────────────┐
              │                 │                 │
   IMPORTANT  │    DO FIRST     │    SCHEDULE     │
              │  Critical bugs  │  Tech debt      │
              │  Security holes │  Documentation  │
              │                 │                 │
              ├─────────────────┼─────────────────┤
              │                 │                 │
NOT IMPORTANT │    DELEGATE     │    ELIMINATE    │
              │  Nice-to-haves  │  Bikeshedding   │
              │  Minor issues   │  Premature opt  │
              │                 │                 │
              └─────────────────┴─────────────────┘
```

### Questions
- Will this matter in 6 months?
- What's the cost of delay?
- What's the cost of getting it wrong?

---

## The Five Whys

### What It Is
Ask "Why?" repeatedly to find the root cause.

### How to Apply
```
Problem: The API is slow

Why? → Database queries are slow
Why? → We're doing N+1 queries
Why? → The ORM doesn't optimize by default
Why? → We didn't configure eager loading
Why? → We didn't understand the data access patterns

Root cause: Insufficient understanding of data access patterns
Solution: Document expected queries, configure ORM properly, add monitoring
```

### Template
| Level | Question | Answer |
|-------|----------|--------|
| 1 | Why [problem]? | |
| 2 | Why [answer 1]? | |
| 3 | Why [answer 2]? | |
| 4 | Why [answer 3]? | |
| 5 | Why [answer 4]? | Root cause |

---

## Trade-off Analysis

### What It Is
Make implicit trade-offs explicit.

### How to Apply
```
Decision: SQL vs. NoSQL

                SQL                     NoSQL
Consistency:    Strong                  Eventual (typically)
Schema:         Rigid                   Flexible
Joins:          Native                  Application-level
Scaling:        Vertical (mostly)       Horizontal (typically)
Transactions:   ACID                    BASE (typically)
Learning:       Common knowledge        Varies by database
```

### Template
```markdown
## Trade-off Analysis: [Decision]

### Option A: [Name]
| Aspect | Rating | Notes |
|--------|--------|-------|
| Performance | | |
| Complexity | | |
| Maintainability | | |
| Cost | | |
| Risk | | |

### Option B: [Name]
| Aspect | Rating | Notes |
|--------|--------|-------|
| Performance | | |
| Complexity | | |
| Maintainability | | |
| Cost | | |
| Risk | | |

### Decision Criteria
What matters most for this project?
1. [Criterion] - Weight: [High/Medium/Low]
2. [Criterion] - Weight: [High/Medium/Low]

### Recommendation
[Option] because [reason based on weighted criteria]
```

---

## Reversibility Analysis

### What It Is
Assess how easily a decision can be undone.

### Categories
| Type | Description | Examples |
|------|-------------|----------|
| **One-way door** | Irreversible or very costly to reverse | Database choice, public API contract, architecture |
| **Two-way door** | Easy to reverse | Library choice, internal API design, config |

### How to Apply
```
Decision: Use MongoDB for user data

Reversibility: ONE-WAY DOOR
- Data migration would be expensive
- Application code tightly coupled
- Schema changes affect everything

Action: Apply high scrutiny, extensive research, prototype first

---

Decision: Use Lodash vs. native JS methods

Reversibility: TWO-WAY DOOR
- Easy to swap out
- Isolated impact
- No data migration

Action: Make a quick decision, move on
```

### Rule
> Spend analysis time proportional to reversibility.
> One-way doors: extensive analysis.
> Two-way doors: decide and move on.

---

## Opportunity Cost

### What It Is
What are we giving up by choosing this option?

### How to Apply
```
Decision: Build custom analytics system

Direct cost: 3 months engineering time

Opportunity cost:
- 3 months NOT spent on core product features
- 3 months NOT spent reducing tech debt
- 3 months NOT spent on other priorities
- Team learning curve instead of shipping

Is custom analytics worth more than what we're giving up?
```

### Questions
- What else could we do with these resources?
- What's the cost of delay on other priorities?
- Could we buy instead of build?

---

## Chesterton's Fence

### What It Is
Before removing something, understand why it was put there.

### How to Apply
```
Observation: "This code has a weird 500ms delay before retrying"

Wrong approach: "That's stupid, let's remove it"

Right approach:
- Why was this added?
- Git blame: Added in 2023 by engineer X
- Commit message: "Fix rate limiting issues with API Y"
- Conclusion: The delay prevents rate limit errors

Action: Keep the delay, document why it exists
```

### Questions
- Who added this and when?
- What problem was it solving?
- Is that problem still relevant?
- What happens if we remove it?

---

## Occam's Razor

### What It Is
The simplest explanation is usually correct.

### How to Apply
```
Problem: Service is slow

Complex explanation:
- Cosmic rays affecting the CPU
- Quantum effects in the network
- Undocumented OS behavior

Simple explanation:
- Database query missing an index
- N+1 query pattern
- No connection pooling

Start with simple explanations, verify, then consider complex ones.
```

### Application to Design
> The simplest solution that meets requirements is usually best.

- Fewer moving parts = fewer failure modes
- Simpler code = easier maintenance
- Less complexity = faster debugging

---

## MECE (Mutually Exclusive, Collectively Exhaustive)

### What It Is
Ensure analysis covers all possibilities without overlap.

### How to Apply
```
Problem: Why might the service fail?

Non-MECE breakdown:
- Network issues
- Server problems
- Code bugs
- Infrastructure failures
(Overlapping and incomplete)

MECE breakdown:
1. Infrastructure failures
   - Compute (CPU, memory)
   - Storage (disk, database)
   - Network (connectivity, DNS)
2. Application failures
   - Code bugs
   - Configuration errors
   - Dependency issues
3. External failures
   - Third-party APIs
   - Upstream services
   - User-caused (bad input)

Now we can systematically analyze each category.
```

---

## Fermi Estimation

### What It Is
Make rough calculations to validate assumptions.

### How to Apply
```
Claim: "We'll have 1 million requests per day"

Estimation:
- Current users: 10,000
- Requests per user per day: ~20
- Current requests: 200,000/day

To reach 1M:
- Need 5x growth
- Current growth rate: 10%/month
- Time to 5x: ~17 months

Conclusion: 1M requests/day is plausible but not imminent.
Design for 500k now, plan for 1M later.
```

### Questions
- How did we arrive at this number?
- What assumptions underlie it?
- Is the order of magnitude right?

---

## Quick Reference: When to Use Which

| Situation | Framework |
|-----------|-----------|
| Evaluating a technology choice | Trade-off Analysis, Second-Order Thinking |
| Understanding why something exists | Chesterton's Fence, Five Whys |
| Planning a new project | Pre-Mortem, Inversion |
| Prioritizing concerns | Eisenhower Matrix |
| Assessing decision risk | Reversibility Analysis |
| Breaking down a problem | First Principles, MECE |
| Validating estimates | Fermi Estimation |
| Simplifying a solution | Occam's Razor |
