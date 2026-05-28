---
name: sys-design
description: Write a comprehensive system design solution document. Use when the user says "/sys-design..." or "Design [system]". Performs research, documents assumptions, calculations, and provides two implementation approaches (cloud-native vs custom). Targets senior/staff architect level depth.
---

# System Design Skill

Creates comprehensive system design documents targeting senior/staff architects. Learning-focused knowledge-sharing articles, not interview prep checklists.

## Invocation

- `/sys-design <topic / summary>`
- `/sys-design URL shortener - focus on scalability and analytics`

## Philosophy

These articles must serve as authoritative references for staff/principal architects. Not interview prep checklists, but deep technical explorations:

### Core Principles
- **Authoritative and assertive**: Make confident statements backed by evidence. "This approach provides X" not "This might provide X"
- **Complete technical depth**: Cover every subtlety, edge case, and failure mode that matters
- **Explore the "why"**: Every decision must explain underlying reasoning, constraints, and assumptions
- **Explicit trade-offs**: Every choice has pros/cons, when to use, when NOT to use
- **Context-dependent**: What works for Twitter doesn't work for a startup—be explicit about scale requirements
- **Historical context**: How did we get here? What problems drove these solutions?
- **Honest about unknowns**: Clearly distinguish verified facts from educated speculation
- **Zero filler**: No obvious statements, no meta-commentary, every paragraph earns its place
- **Operational reality**: Address monitoring, debugging, failure modes, and migration paths

## Workflow

```mermaid
flowchart TD
    A[User Request] --> B[Parse Problem]
    B --> C[Deep Research]
    C --> D[Requirements Analysis]
    D --> E[Back of Envelope]
    E --> F[High-Level Design]
    F --> G[Deep Dive: Data Layer]
    G --> H[Deep Dive: Application Layer]
    H --> I[Deep Dive: Infrastructure]
    I --> J[Two Approaches]
    J --> K[Quality Review]
    K --> L[Save Document]
```

## Document Structure

```markdown
# [System Name]: A Deep Dive into [Core Challenge]

[Engaging intro framing the problem]

[Overview diagram showing core challenge]

## TLDR
[Comprehensive summary]

## The Problem Space
### What Are We Really Solving?
### Why Is This Hard?
### Historical Context

## Requirements & Constraints
### Functional Requirements
### Non-Functional Requirements
### Explicit Non-Goals

## Back of the Envelope
### Assumptions
### Traffic Modeling
### Storage Modeling
### The Numbers That Matter

## High-Level Architecture
### Design Philosophy
### CAP Theorem Position
### System Components

## Deep Dive: Data Layer
### Data Modeling
### Database Selection
### Caching Strategy
### Data Partitioning

## Deep Dive: Application Layer
### API Design
### Service Architecture
### Core Algorithms
### Resilience Patterns

## Deep Dive: Infrastructure
### Deployment Architecture
### Scaling Strategy
### Observability
### Security

## Advanced Considerations
### Consistency Patterns
### Failure Modes
### Evolution & Migration

## Implementation Approaches
### Approach 1: Cloud-Native
### Approach 2: Custom Infrastructure

## Real-World Examples

## What Would Change at Different Scales

## References
```

## Phase 1: The Problem Space

Start by deeply understanding the problem, not jumping to solutions.

```markdown
## The Problem Space

### What Are We Really Solving?

For a URL shortener, it's not "store short URLs"—it's:
- **Bijective mapping** at scale with low latency
- **Read-heavy workload** with extreme fan-out
- **Durability vs availability** trade-off for redirects

### Why Is This Hard?

| Challenge | Why It's Non-Trivial |
|-----------|---------------------|
| [Challenge 1] | [Explanation with numbers] |
| [Challenge 2] | [Explanation with numbers] |

### Historical Context

How have solutions evolved? What did we learn?
```

## Phase 2: Requirements Analysis

### Functional Requirements

Think in user stories and system behaviors:

| Behavior | Description | Complexity | Notes |
|----------|-------------|------------|-------|
| [Behavior 1] | [Description] | [Simple/Medium/Complex] | [Edge cases] |

### Non-Functional Requirements

| Metric | Target | Rationale | Measurement Point |
|--------|--------|-----------|-------------------|
| Read latency (p50) | X ms | [Why] | Client-perceived |
| Read latency (p99) | Y ms | [Why] | Client-perceived |
| Availability | 99.9% | [Downtime: 8.76 hours/year] | |

### Explicit Non-Goals

**Critical**: What we're NOT building:
- **[Non-goal 1]**: [Why excluding simplifies design]

## Phase 3: Back of the Envelope

**This section teaches estimation thinking, not just numbers.**

```markdown
## Back of the Envelope

### Assumptions

| Assumption | Value | Source/Reasoning | Sensitivity |
|------------|-------|------------------|-------------|
| Daily Active Users | X | [Comparable] | High |
| Read:Write ratio | N:1 | [Reasoning] | High |

### Traffic Modeling

```plain
Writes/second   = DAU × actions_per_user / 86,400
                = [X] × [Y] / 86,400
                = [Z] writes/second

Peak writes/sec = [Z] × peak_ratio
                = [P] writes/second (design target)
```

### The Numbers That Actually Matter

| Metric | Value | Why It Matters |
|--------|-------|----------------|
| Peak QPS | [X] | Determines compute |
| Storage growth/day | [Y] GB | Storage strategy |
| Working set size | [Z] GB | Caching strategy |
```

## Phase 4: High-Level Architecture

### Design Philosophy

| Principle | Meaning | Trade-off Accepted |
|-----------|---------|-------------------|
| [Principle 1] | [Concrete meaning] | [What we give up] |

### CAP Theorem Position

```plain
         Consistency
              ▲
              │    CP Systems
              │    (Banking)
              │         ●
    ──────────┼──────────────────► Availability
              │         ●
              │    AP Systems
              │    (Social feeds)
```

**Our position**: [Explanation of where and why]

### Key Design Decisions

| Decision | Options Considered | Choice | Rationale |
|----------|-------------------|--------|-----------|
| [Decision 1] | [A, B, C] | [Choice] | [Why] |

## Phase 5: Deep Dive - Data Layer

### Database Selection

| Database | Strengths | Weaknesses | Best For |
|----------|-----------|------------|----------|
| PostgreSQL | ACID, complex queries | Horizontal scaling | Transactions |
| DynamoDB | Managed, predictable latency | Cost at scale | Serverless |
| Redis | Speed, data structures | Memory-bound | Caching |

**Decision**: [Database] because:
1. [Primary reason]
2. [Secondary reason]

**What would change this**: If [condition], reconsider [alternative]

### Caching Strategy

| Pattern | Pros | Cons |
|---------|------|------|
| Cache-Aside | Simple, caches what's needed | Cache miss penalty |
| Write-Through | Always consistent | Write latency increased |
| Write-Behind | Fast writes | Data loss risk |

### Data Partitioning

| Strategy | Pros | Cons |
|----------|------|------|
| Range-Based | Range queries efficient | Hot spots |
| Hash-Based | Even distribution | No range queries |
| Consistent Hashing | Minimal data movement | More complex |

## Phase 6: Deep Dive - Application Layer

### API Design

```yaml
POST /api/v1/[resources]
Response: 201 Created
  {
    "id": "abc123",
    "field": "value"
  }
```

### Resilience Patterns

**Circuit Breaker States:**
```plain
CLOSED (normal) → OPEN (fast fail) → HALF-OPEN (test)
```

**Retry with Exponential Backoff:**
```plain
Wait = base × 2^attempt × random(0.5, 1.5)
```

## Phase 7: Deep Dive - Infrastructure

### Deployment Architecture

**Single Region:**
```plain
┌─────────────────────────────────────────────────────────────┐
│                         Region A                             │
│  ┌───────────────────────┐  ┌───────────────────────┐       │
│  │   Availability Zone 1  │  │   Availability Zone 2  │       │
│  └───────────────────────┘  └───────────────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

### Observability

**RED method for services:**
- **R**ate: Requests per second
- **E**rrors: Failed requests per second
- **D**uration: Latency distribution

## Phase 8: Two Implementation Approaches

### Approach 1: Cloud-Native

**When to choose:**
- Team < 10 engineers
- Time-to-market critical
- Moderate scale (< 100K QPS)

| Component | Managed Service | Trade-off |
|-----------|-----------------|-----------|
| Compute | ECS/EKS/Lambda | Ops simplicity vs control |
| Database | RDS/Aurora | Cost vs operational burden |
| Cache | ElastiCache | Same pattern |

**Pros:** Time to market, managed ops, built-in HA
**Cons:** 2-5x more expensive at scale, vendor lock-in

### Approach 2: Custom Infrastructure

**When to choose:**
- Scale > 100K QPS
- Cost optimization critical
- Team has systems expertise

| Component | Choice | Why |
|-----------|--------|-----|
| Compute | Kubernetes | Control, cost |
| Database | PostgreSQL self-managed | Flexibility |
| Cache | Redis Cluster | Performance tuning |

**Pros:** 50-80% cheaper at scale, full control
**Cons:** Months vs weeks, significant ops investment

## Phase 9: What Would Change at Different Scales

| Metric | Startup (1K) | Growth (100K) | Scale (10M) |
|--------|-------------|---------------|-------------|
| Architecture | Monolith | Monolith + cache | Services + sharding |
| Database | Single PostgreSQL | + replicas | Sharded |
| Team size | 2-5 | 10-20 | 50-100 |

## Quality Checks

### Technical Accuracy (HIGHEST PRIORITY)
- [ ] All numbers realistic and sourced with references
- [ ] Calculations correct and show work
- [ ] Latency/throughput claims backed by evidence
- [ ] Trade-offs fairly and completely represented
- [ ] Inline references for all significant claims
- [ ] Database/technology capabilities accurately stated
- [ ] No speculation presented as fact

### Authoritative Tone
- [ ] Assertive statements where evidence supports
- [ ] No excessive hedging ("might possibly", "could perhaps")
- [ ] Confident presentation of verified facts
- [ ] Explicit about unknowns and assumptions
- [ ] Reads like staff architect explaining to peers

### Completeness
- [ ] Every design decision has explicit reasoning
- [ ] All significant trade-offs documented
- [ ] Edge cases and failure modes addressed
- [ ] Operational concerns covered (monitoring, debugging)
- [ ] Migration and evolution paths discussed
- [ ] Security considerations addressed
- [ ] Cost implications noted where relevant

### Trade-offs (MANDATORY FOR EVERY DECISION)
- [ ] Pros/cons for every technology choice
- [ ] Pros/cons for every architectural pattern
- [ ] When to use AND when NOT to use each approach
- [ ] Context-dependent recommendations (scale, team size)
- [ ] Nothing presented as universally "best"
- [ ] Alternative approaches mentioned with reasoning

### Conciseness (ZERO FILLER)
- [ ] No padding or filler sentences
- [ ] No meta-commentary ("In this article...")
- [ ] No obvious statements ("Reliability is important")
- [ ] Every section earns its place with new insight
- [ ] Every paragraph advances understanding
- [ ] Reading time reasonable for depth

### Staff/Principal Engineer Standard
- [ ] Could be cited in design review discussions
- [ ] Handles nuance senior architects care about
- [ ] Addresses real production concerns
- [ ] Complete enough for informed decision-making
- [ ] No oversimplification of complex trade-offs

### Formatting
- [ ] No manual ToC
- [ ] Mermaid diagrams render correctly
- [ ] ASCII diagrams use `plain` code blocks
- [ ] Code/config blocks use collapse for non-essential lines (imports, setup, middle sections, helpers)
- [ ] Multiple collapse ranges used when needed: `collapse={1-5, 12-18, 25-30}`
- [ ] References section complete with authoritative sources

### Tags
- [ ] All tags valid (exist in `content/tags.jsonc`)
- [ ] Includes `system-design` and `architecture` tags
- [ ] Domain-specific tags added (caching, scalability, etc.)
- [ ] Technology tags added if discussed (redis, postgres, etc.)
- [ ] New tags added to tags.jsonc if needed
- [ ] Uses tag IDs, not display names

## Anti-Patterns to Avoid (STRICT)

### Content Anti-Patterns
- **Interview checklist style**: Listing components without explaining why
- **Silver bullet thinking**: "Always use X", "This is the best approach"
- **Missing trade-offs**: Any decision without explicit pros/cons
- **Unsourced numbers**: Back-of-envelope without showing assumptions
- **Tutorial-style**: "First, let's understand...", "Before we begin..."
- **Meta-commentary**: "In this article, we will explore..."
- **Obvious statements**: "Scalability is important", "Security matters"
- **Filler transitions**: "Now that we've covered X, let's discuss Y"
- **Incomplete reasoning**: What without explaining why
- **False precision**: "This will handle exactly 1M QPS" without evidence
- **Migration timelines/development plans**: Do NOT include phased rollout plans, week-by-week timelines, or development schedules unless explicitly requested by user

### Technical Anti-Patterns
- **Technology name-dropping**: Mentioning technologies without explaining why
- **Ignoring operational concerns**: No monitoring, debugging, or alerting
- **Missing failure modes**: Not discussing what happens when things break
- **Scale-agnostic advice**: Same recommendation for 100 users and 100M users
- **Outdated patterns**: Recommending deprecated or superseded approaches
- **Oversimplification**: Glossing over important nuances
- **Incomplete comparisons**: Comparing only favorable attributes

### Tone Anti-Patterns
- **Excessive hedging**: "might possibly", "could perhaps"
- **False certainty**: Speculation presented as established fact
- **Preachy**: "You should always...", "Never do..."
- **Dismissive**: "Obviously...", "Simply...", "Just..."
- **Vendor bias**: Promoting one cloud provider without fair comparison

### Structure Anti-Patterns
- **Manual ToC**: Auto-generated by framework
- **Missing diagrams**: No visual representation of architecture
- **Wall of text**: No tables, diagrams, or code breaking up prose
- **Shallow TLDR**: Just a teaser, not comprehensive summary
- **Missing References**: No sources for claims and numbers
- **Invalid tags**: Tags not in tags.jsonc, using display names instead of IDs
- **Missing tags**: No tags or missing system-design/architecture base tags
- **Generic title**: "System Design" or "Architecture Guide" without specific system
- **Tutorial-style title**: "How to Design..." instead of direct topic
- **Generic slug**: "system-design" or "design" without identifying the system
- **Overly long slug**: Including unnecessary words like "designing-a-highly-scalable..."

## Save Document

Location: `content/posts/design-problems/YYYY-MM-DD-[slug]/index.md`

```yaml
---
lastReviewedOn: YYYY-MM-DD
tags:
  - system-design
  - architecture
  - distributed-systems
---
```

### Title Selection (IMPORTANT)

Choose a title that captures the system and core challenge:

1. **Format**: "[System Name]: A Deep Dive into [Core Challenge]"
2. **Be specific**: Focus on the interesting technical challenge, not generic "design"
3. **No clickbait**: Avoid "Ultimate Guide" or "Everything You Need to Know"
4. **Length**: Under 70 characters for SEO, but prioritize clarity

**Good titles:**
- "URL Shortener: Designing for Billions of Redirects"
- "Rate Limiter Design: Distributed Algorithms and Trade-offs"
- "Message Queue Architecture: Durability vs Throughput"
- "Notification System: Real-time Delivery at Scale"

**Bad titles:**
- "How to Design a URL Shortener" (tutorial-style)
- "Complete System Design Guide" (too vague)
- "Building Scalable Systems" (not specific to a system)
- "Everything About Message Queues" (too broad)

### Slug Selection (IMPORTANT)

Choose a folder slug that identifies the system:

1. **Format**: `YYYY-MM-DD-[system-name]` or `YYYY-MM-DD-[system-name]-design`
2. **Concise**: 2-4 words maximum
3. **System-focused**: Name the system, not the challenge
4. **Lowercase**: Use hyphens, no special characters

**Good slugs:**
- `2024-03-15-url-shortener`
- `2024-03-15-rate-limiter`
- `2024-03-15-notification-system`
- `2024-03-15-distributed-cache`

**Bad slugs:**
- `2024-03-15-system-design` (too generic)
- `2024-03-15-designing-a-highly-scalable-url-shortening-service` (too long)
- `2024-03-15-design` (meaningless)

### Tag Selection (IMPORTANT)

1. **Read** `content/tags.jsonc` to get all valid tag IDs
2. **Analyze** document content to identify relevant topics
3. **Add relevant tags** that match the content:
   - Always include: `system-design`, `architecture`
   - Add domain-specific tags (e.g., `caching`, `distributed-systems`, `scalability`)
   - Add technology tags if discussed (e.g., `redis`, `postgres`, `aws`)
   - Use tag `id` values (e.g., `web-performance`, not `Web Performance`)
   - Typically 4-10 tags per system design document
4. **Add new tags to tags.jsonc** if needed:
   - If a relevant topic has no matching tag, add it to `content/tags.jsonc` first
   - Place new tag in appropriate category section
   - Follow existing format: `{ "id": "slug-format", "name": "Display Name" }`
5. **Validate** all tags exist in tags.jsonc before using them

## Internal Linking

When referencing other posts, use relative paths to `.md` files. This enables IDE navigation (Cmd+Click) and the rehype plugin transforms them to proper URLs at build time.

```markdown
[Link Text](../YYYY-MM-DD-slug.md)
[Link Text](../../category/YYYY-MM-DD-slug/index.md)
```

**Examples:**
```markdown
[Caching Strategies](../../system-design-fundamentals/2024-12-06-caching.md)
[URL Shortener Design](../2024-03-15-url-shortener.md)
```

**Key rules:**
- Use relative paths from current file to target `.md` file
- Include the full filename with date prefix
- The rehype plugin transforms these to `/posts/<type>/<category>/<slug>` URLs
- Enables Cmd+Click navigation in VS Code and other IDEs

## Reference Documents

**IMPORTANT**: Before writing, read these documents from the project root:

| Document | Path (from project root) | Purpose |
|----------|--------------------------|---------|
| Content Guidelines | `llm_docs/content-guidelines.md` | Writing standards, conciseness rules, quality checklist |
| Markdown Features | `llm_docs/markdown-features.md` | Expressive Code syntax, Mermaid diagrams, KaTeX |
| Project Instructions | `CLAUDE.md` | Project structure, commands, styling conventions |

**Usage**: Use the Read tool with absolute paths (e.g., `/path/to/project/llm_docs/content-guidelines.md`) to read these files before starting work.

## Tools Available

- `WebSearch` - Research engineering blogs, papers
- `WebFetch` - Fetch detailed content
- `Read` - Read existing content
- `Write` - Create documents
- `Glob` - Find related content
- `Bash` - Build and validation
