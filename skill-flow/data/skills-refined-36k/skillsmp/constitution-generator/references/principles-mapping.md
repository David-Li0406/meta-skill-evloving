# Principles Mapping Guide

Map project characteristics to appropriate principles. Use this to avoid over-engineering or under-specifying.

## Quick Reference Matrix

### By Project Lifespan

| Lifespan | Include | Avoid |
|----------|---------|-------|
| **Days (hackathon)** | MVP Speed, Demo-First, Manual Testing OK | TDD, Comprehensive Docs, DDD |
| **Weeks (prototype)** | Ship Fast, Good Enough Architecture | Event Sourcing, Microservices |
| **Months (product)** | Modularity, Basic Tests, Clear Naming | Over-abstraction |
| **Years (platform)** | Documentation Standards, Versioning, API Contracts | Cutting corners on interfaces |

### By Team Size

| Size | Include | Avoid |
|------|---------|-------|
| **Solo** | Dogfood Relentlessly, Build for Joy | Formal code review, Complex branching |
| **2-5** | Conventional Commits, PR Reviews, Shared Standards | Overly complex governance |
| **6+** | Clear Ownership, Documentation, Style Guides | Tribal knowledge |
| **Open Source** | Contributor Guidelines, API Stability, Semver | Breaking changes without notice |

### By Risk Profile

| Risk | Include | Avoid |
|------|---------|-------|
| **Experimental** | Fail Fast, YAGNI, Quick Iteration | Security hardening, Audit trails |
| **Internal tool** | Good Enough, Pragmatic Testing | Enterprise-grade security |
| **Business-critical** | Comprehensive Tests, Monitoring, Runbooks | Skipping error handling |
| **Financial/Regulated** | Audit Trails, Input Validation, Security First | Shortcuts on compliance |
| **Public-facing** | Zero Trust, Rate Limiting, Input Sanitization | Trust any input |

### By Architecture Style

| Style | Include | Avoid |
|-------|---------|-------|
| **CLI tool** | Unix Philosophy, Text I/O, Exit Codes | Heavy frameworks |
| **Library/SDK** | API First, Semantic Versioning, Minimal Dependencies | Breaking changes |
| **Monolith** | Modularity, Clear Boundaries | Microservices complexity |
| **Microservices** | Contract Testing, Circuit Breaking, Observability | Tight coupling |
| **Serverless** | Idempotency, Cold Start Awareness | Long-running processes |

---

## Detailed Principle Applicability

### Speed Principles

#### MVP Speed
**When to use:**
- Hackathons
- Prototypes
- Validating ideas
- Time-boxed experiments

**When to skip:**
- Production systems
- Long-lived projects
- When "good enough" creates tech debt you can't afford

---

#### Ship Fast, Fix What Hurts
**When to use:**
- Personal tools
- Internal utilities
- Solo projects
- Early-stage products

**When to skip:**
- Multi-team projects (need alignment)
- Regulated environments
- Customer-facing systems without safety nets

---

### Quality Principles

#### Single Responsibility
**When to use:**
- Always applicable
- Especially important for: teams, long-lived code, testability

**Degree of strictness:**
- Hackathon: Loosely enforced
- Product: Enforced at module level
- Platform: Strictly enforced everywhere

---

#### Integration Tests First
**When to use:**
- Any system with external dependencies
- APIs, databases, third-party services
- When mocked tests have failed you before

**When to relax:**
- Pure utility functions (unit tests fine)
- Hackathons (manual testing acceptable)
- UI components (visual testing may suffice)

---

### Operational Principles

#### Observability First
**When to use:**
- Uptime expectations ≥99%
- Distributed systems
- Production services
- On-call responsibilities

**When to skip:**
- Local-only tools
- Prototypes
- Scripts that run once

---

#### Zero Trust
**When to use:**
- Public-facing systems
- Multi-tenant architectures
- Handling sensitive data
- Financial systems

**When to skip:**
- Local-only tools
- Single-user systems
- Internal prototypes

---

### Documentation Principles

#### README First
**When to use:**
- Always, even for hackathons
- Minimum: what it does, how to run it

**Depth varies:**
- Hackathon: 5 lines
- Team project: Setup, usage, architecture
- Open source: Contributing guide, examples

---

#### Comment the Why
**When to use:**
- Always applicable
- Critical for: workarounds, non-obvious decisions, security measures

**Skip comments for:**
- Self-explanatory code
- The "what" (code shows that)

---

## Common Anti-Patterns by Project Type

### Hackathon Anti-Patterns
- Writing comprehensive test suites
- Setting up CI/CD pipelines
- Designing for scale
- Creating documentation beyond README
- Using Event Sourcing or CQRS
- Implementing full authentication systems

### Personal Tool Anti-Patterns
- Enterprise-grade security
- Formal code review processes
- Complex branching strategies
- Performance SLAs
- Multi-region deployment

### Production System Anti-Patterns
- Skipping error handling
- Hardcoded secrets
- Manual deployments only
- No monitoring
- Ignoring security

### Team Project Anti-Patterns
- No shared coding standards
- Inconsistent commit messages
- No code review
- Tribal knowledge
- "It works on my machine"

---

## Principle Combinations

### "Minimum Viable Constitution" (Hackathon)
1. MVP Speed
2. Demo-First Development
3. Good Enough Architecture
4. Human-Readable Errors (prevent demo failures)

### "Personal Tool Constitution"
1. Ship Fast, Fix What Hurts
2. Build for Joy, Not Scale
3. KISS & YAGNI
4. Dogfood Relentlessly
5. Make It Work, Then Make It Fast

### "Team Product Constitution"
1. Single Responsibility
2. Modularity
3. Integration Tests First
4. Conventional Commits
5. Code Review Required
6. Human-Readable Errors
7. Documentation Standards

### "Production Platform Constitution"
1. Performance Awareness
2. Modularity
3. Comprehensive Testing
4. Observability First
5. Security by Default
6. API Contracts
7. Semantic Versioning
8. Runbooks & Documentation

### "CLI Tool Constitution"
1. Unix Philosophy
2. Text I/O Protocol
3. Single Responsibility
4. Human-Readable Errors
5. KISS
6. Integration Tests First

### "Regulated/Financial Constitution"
1. Security First
2. Input Validation Required
3. Audit Trails
4. No Silent Failures
5. Comprehensive Testing
6. Defense in Depth
7. Least Privilege
8. Documentation Required

---

## Questions That Change Recommendations

| Question | If Yes | If No |
|----------|--------|-------|
| "Will others contribute?" | Add: Conventional Commits, PR Reviews | Skip: Formal process |
| "Handling money/PII?" | Add: Security First, Validation, Auditing | Skip: Heavy compliance |
| "Need to replay/audit events?" | Add: Event Sourcing, Immutability | Skip: Event Sourcing entirely |
| "Complex domain logic?" | Consider: DDD patterns (selectively) | Skip: DDD overhead |
| "High uptime required?" | Add: Observability, Graceful Degradation | Skip: SRE practices |
| "Public API?" | Add: API First, Versioning, Stability | Internal: More flexibility |
| "Demo deadline?" | Add: Demo-First, Happy Path Priority | Long-term: Comprehensive approach |

---

## Red Flags in Constitution Requests

**User asks for X, but project profile suggests skip:**

| Request | Profile Mismatch | Suggestion |
|---------|-----------------|------------|
| "Full TDD" | Hackathon | "Test critical paths only" |
| "Event Sourcing" | CRUD app | "Simple state updates suffice" |
| "Microservices" | Solo project | "Modular monolith scales better" |
| "Zero Trust" | Local CLI tool | "Focus on input validation" |
| "99.99% uptime" | Prototype | "Establish baseline first" |

When mismatches occur, ask: "This seems like [X] might be overkill for [project type]. Want me to suggest a lighter-weight alternative, or is there a specific reason you need this?"
