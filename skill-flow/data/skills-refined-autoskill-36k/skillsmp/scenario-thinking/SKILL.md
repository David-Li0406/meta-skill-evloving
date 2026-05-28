---
name: scenario-thinking
description: Scenario-driven solution design that focuses on future use cases, dimensional analysis, and explicit trade-offs
---

# Scenario-Driven Thinking

## When to Use

Use this skill whenever you are designing solutions, making architectural decisions, or choosing between different approaches. This skill ensures that solutions are grounded in real-world usage scenarios and that trade-offs are made consciously and explicitly.

**Always apply this skill when:**
- Designing new features or systems
- Making technology or architecture choices
- Refactoring existing code
- Optimizing performance or structure
- Choosing between multiple implementation approaches
- Any decision that has multiple viable options

## Core Concepts

### 1. Scenario-First Thinking
Solutions should be driven by concrete future usage scenarios, not abstract ideals. Before proposing any solution, understand how it will actually be used.

### 2. Dimensional Analysis
Every scenario has multiple dimensions to consider (performance, maintainability, scalability, cost, complexity, etc.). Different scenarios prioritize different dimensions.

### 3. Conscious Trade-offs
There is no perfect solution - every choice sacrifices something. The key is to make these sacrifices intentionally based on the scenario's priorities.

### 4. Explicit Communication
Users must understand what they're gaining and what they're giving up with each decision.

## How to Use

### Step 1: Request Future Usage Scenarios

**Always start by asking the user about their intended usage scenarios.** Never proceed with a solution until you understand the context.

**Questions to ask:**
- "What are the expected usage scenarios for this feature?"
- "How will this be used in production?"
- "What are the typical and edge case scenarios?"
- "How frequently will this be used?"
- "Who are the users and what are their constraints?"

### Step 2: Identify Scenario Dimensions

For each scenario, analyze the relevant dimensions. Common dimensions include:

**Performance Dimensions:**
- Latency (response time)
- Throughput (requests per second)
- Resource usage (CPU, memory, disk)
- Concurrency (number of simultaneous operations)

**Maintainability Dimensions:**
- Code readability and clarity
- Test coverage and testability
- Documentation completeness
- Debugging ease
- Onboarding time for new developers

**Scalability Dimensions:**
- Horizontal scalability (add more machines)
- Vertical scalability (add more resources)
- Data growth handling
- User growth handling

**Complexity Dimensions:**
- Implementation complexity
- Operational complexity
- Learning curve
- Number of dependencies

**Cost Dimensions:**
- Development time
- Infrastructure cost
- Maintenance cost
- Technical debt

**Reliability Dimensions:**
- Fault tolerance
- Data consistency
- Error handling
- Recovery mechanisms

**Flexibility Dimensions:**
- Extensibility
- Configuration options
- Integration capabilities
- Future-proofing

### Step 3: Prioritize Dimensions Based on Scenario

Based on the usage scenario, determine which dimensions are:
- **Critical**: Must be optimized, cannot be sacrificed
- **Important**: Should be balanced, some compromise acceptable
- **Acceptable**: Can be sacrificed if needed for critical dimensions

**Example:**
```
Scenario: Real-time trading system
Critical: Latency, reliability, data consistency
Important: Monitoring, error handling
Acceptable: Development speed, code simplicity (can use complex optimizations)
```

### Step 4: Propose Solutions with Explicit Trade-offs

For each solution option, clearly state:
1. **What it optimizes for** (which dimensions it prioritizes)
2. **What it sacrifices** (which dimensions are compromised)
3. **Why this makes sense** (how it aligns with the scenario)

**Template:**
```
Option [X]: [Solution Name]

Optimizes for:
- [Dimension 1]: [How/Why]
- [Dimension 2]: [How/Why]

Sacrifices:
- [Dimension 3]: [What is compromised and to what extent]
- [Dimension 4]: [What is compromised and to what extent]

Scenario fit:
[Explain why this trade-off makes sense for the stated scenario]
```

### Step 5: Provide Comparison Table (for multiple options)

When presenting multiple options, provide a clear comparison:

```markdown
| Dimension       | Option A | Option B | Option C |
|-----------------|----------|----------|----------|
| Performance     | ★★★★★    | ★★★☆☆    | ★★☆☆☆    |
| Maintainability | ★★☆☆☆    | ★★★★☆    | ★★★★★    |
| Complexity      | ★☆☆☆☆    | ★★★☆☆    | ★★★★☆    |
| Cost            | ★★☆☆☆    | ★★★★☆    | ★★★★★    |

Recommendation: [Option X] because [scenario requires Y and Z]
```

## Common Scenario Patterns

### Pattern 1: MVP / Early Stage Product
**Prioritize:** Development speed, flexibility, cost
**Sacrifice:** Performance optimization, scalability (can refactor later)
**Reasoning:** Need to validate product-market fit quickly

### Pattern 2: High-Traffic Production System
**Prioritize:** Performance, reliability, scalability
**Sacrifice:** Development speed, code simplicity
**Reasoning:** System maturity justifies investment in optimization

### Pattern 3: Internal Tool
**Prioritize:** Simplicity, maintainability, development speed
**Sacrifice:** Polish, performance optimization, edge case handling
**Reasoning:** Limited users, can fix issues as they arise

### Pattern 4: Library/Framework
**Prioritize:** Flexibility, documentation, backward compatibility
**Sacrifice:** Specific optimizations, opinionated design
**Reasoning:** Must serve diverse use cases

### Pattern 5: Data Pipeline / Batch Processing
**Prioritize:** Throughput, cost efficiency, fault tolerance
**Sacrifice:** Latency (can be slower as long as it completes)
**Reasoning:** Eventual completion more important than speed

### Pattern 6: Prototype / Proof of Concept
**Prioritize:** Speed of implementation, demonstration of core concept
**Sacrifice:** Production quality, error handling, testing
**Reasoning:** Exploratory phase, may be discarded

## Best Practices

### DO:
✓ Always ask about usage scenarios before proposing solutions
✓ Make trade-offs explicit and conscious
✓ Revisit scenarios if requirements change
✓ Document the reasoning behind trade-off decisions
✓ Validate assumptions about scenarios with users
✓ Consider both current and future scenarios (6-12 months)
✓ Be honest about limitations of proposed solutions

### DON'T:
✗ Propose solutions before understanding the scenario
✗ Hide or downplay trade-offs
✗ Optimize for dimensions that don't matter for the scenario
✗ Assume one-size-fits-all solutions
✗ Over-engineer for hypothetical future needs
✗ Under-engineer for known near-term needs
✗ Make decisions based on personal preferences rather than scenario needs

## Example: Complete Scenario Analysis

### User Request
"I need to add a caching layer to our API."

### Scenario Discovery
**Question:** "What are the expected usage scenarios for this cache?"

**User Response:** "Our API serves product catalog data. We have 10,000 products, each product is viewed 50-100 times per day on average, and product data is updated once per day during a nightly batch job. We have about 5,000 concurrent users during peak hours."

### Dimensional Analysis
Based on this scenario:

**Critical Dimensions:**
- Read performance (high read frequency)
- Cost efficiency (predictable access patterns allow optimization)
- Staleness tolerance (data changes only daily)

**Important Dimensions:**
- Cache hit rate
- Memory usage
- Simplicity (small team)

**Acceptable to Sacrifice:**
- Write performance (only nightly updates)
- Immediate consistency (daily updates are acceptable)
- Distributed cache complexity (single instance may suffice)

### Solution Proposal

**Option A: In-Memory Cache with Daily Refresh**

Optimizes for:
- Read performance: Sub-millisecond latency from memory
- Cost efficiency: No external cache infrastructure needed
- Simplicity: Single-process cache, easy to maintain

Sacrifices:
- Cache durability: Lost on restart (acceptable since data refreshes daily)
- Distributed scalability: Single instance only (may need change if traffic grows 10x)
- Fine-grained updates: Cannot update individual products mid-day

Scenario fit:
This is ideal for your scenario because:
1. Daily refresh matches your update frequency perfectly
2. 10,000 products easily fit in memory (~100MB with product details)
3. Simplicity reduces operational overhead for small team
4. Cost is minimal (just memory on existing servers)

**Option B: Redis Distributed Cache**

Optimizes for:
- Scalability: Multiple API servers can share cache
- Durability: Cache persists across restarts
- Fine-grained updates: Can invalidate specific products

Sacrifices:
- Complexity: Additional infrastructure to manage
- Cost: Redis hosting/management overhead
- Latency: Network hop adds 1-2ms vs in-memory

Scenario fit:
Over-engineered for current scenario, but consider if:
1. You plan to scale to 10+ API servers
2. You need to update specific products outside the nightly batch
3. You have ops team to manage Redis

**Option C: CDN Edge Caching**

Optimizes for:
- Global latency: Cache at edge locations
- Scalability: Handles massive traffic spikes
- Offload: Reduces origin server load

Sacrifices:
- Cost: CDN fees
- Control: Cache invalidation can be delayed
- Complexity: Configuration and debugging

Scenario fit:
Not recommended for your scenario because:
1. Your traffic (5K concurrent) doesn't require CDN
2. All users likely in same region
3. Cost doesn't justify the benefit

### Comparison Table

| Dimension           | In-Memory | Redis | CDN   |
|---------------------|-----------|-------|-------|
| Read Performance    | ★★★★★     | ★★★★☆ | ★★★★★ |
| Cost Efficiency     | ★★★★★     | ★★★☆☆ | ★★☆☆☆ |
| Simplicity          | ★★★★★     | ★★★☆☆ | ★★☆☆☆ |
| Scalability         | ★★☆☆☆     | ★★★★★ | ★★★★★ |
| Durability          | ★★☆☆☆     | ★★★★★ | ★★★★☆ |
| Setup Time          | ★★★★★     | ★★★☆☆ | ★★☆☆☆ |

**Recommendation:** Option A (In-Memory Cache) because:
- Matches your daily refresh pattern perfectly
- Minimal complexity for small team
- Best cost-performance ratio for your traffic level
- Can migrate to Redis later if you need distribution

**Migration Path:** If traffic grows 10x or you add multiple API servers, consider Redis at that time. The code changes will be minimal.

---

## Summary

Scenario-driven thinking ensures that solutions are practical, well-reasoned, and aligned with actual needs. By always starting with usage scenarios, analyzing relevant dimensions, and making explicit trade-offs, you create solutions that are fit for purpose rather than theoretically optimal but impractical.

**Remember: There is no perfect solution, only the right solution for the specific scenario.**
