---
name: "phase_03_architecture_design"
description: "You'll transform requirements into a robust, secure, scalable architecture. Through system design, security architecture, data modeling, infrastructure planning, and threat modeling, you'll create the blueprint that guides development. This is where abstract requirements become concrete technical decisions."
phase: 3
phase_name: "Architecture & Design"
owner: "Chief Technology Architect (CTA)"
secondary_owner: "Technical Lead"
participants: ["Tech Lead", "Security Architect", "DevOps", "Data Architect", "Cloud Architect", "SRE", "UX Lead", "Product Designer", "Users"]
entry_criteria: [
  "Functional requirements documented and approved",
  "Non-functional requirements defined",
  "Security requirements documented",
  "Compliance requirements identified",
  "Data requirements documented"
]
exit_criteria: [
  "System architecture approved by CTA",
  "Security architecture approved by CISO",
  "Data architecture approved and validated",
  "Infrastructure design approved and cost-validated",
  "API and integration design completed",
  "UI/UX design validated with users",
  "Technical specifications documented",
  "Threat modeling completed and reviewed",
  "Design review conducted with all stakeholders",
  "ADRs created",
  "Go/no-go decision to proceed to Phase 4"
]
estimated_duration: "1 week"
dependencies: ["phase_02_requirements_scope"]
outputs: [
  "System Architecture Document",
  "Security Architecture Document",
  "Data Architecture (ERD, Schemas)",
  "Cloud Infrastructure Design",
  "API Specifications (OpenAPI/Swagger)",
  "UI/UX Mockups and Prototypes",
  "Technical Specifications",
  "Architecture Decision Records (ADRs)",
  "Threat Models"
]
next_phase: "phase_04_development_planning"
---

# Phase 3: Architecture & Design
## Where Requirements Become Blueprint

---

## Welcome to the Architecture Phase

Congratulations on reaching Phase 3! You've done the hard work of defining clear requirements. Now comes the creative and technical work of designing how to build it.

This is where the abstract becomes concrete. Where "the system must be fast" becomes "we'll use Redis caching with a 5-minute TTL." Where "user data must be secure" becomes "AES-256 encryption at rest with AWS KMS key management."

**Here's what you'll walk away with:**

 A system architecture that meets all your requirements
 Security architecture designed in (not bolted on)
 Data architecture that supports your current and future needs
 Infrastructure design that's cost-optimized and scalable
 API specifications that developers can implement from
 UI/UX designs validated with real users
 Threat models that identify and mitigate security risks

**Time investment**: 14-19 weeks (this is the longest phase—for good reason)

---

## What This Phase Feels Like (A Real Story)

I advised a startup that rushed architecture design. They spent 4 weeks designing and 6 months building. At scale testing, they discovered their architecture couldn't handle 1/10th of their target load. They spent 4 months re-architecting.

Contrast that with a team that spent 16 weeks on architecture:

- **Handled 10x launch-day traffic** without breaking a sweat
- **Security audit passed** in half the usual time (security was designed in)
- **New feature velocity** stayed high (architecture was flexible and clear)
- **Infrastructure costs** were 40% lower than projections (cost optimization was designed in)

Their CTA told me: *"I was impatient to start coding. Now I'm grateful we designed first. Every trade-off decision was made before we wrote a single line of code."*

That's the feeling we're aiming for. You'll enter development confident, not crossing fingers.

---

## Your Journey Through This Phase

Think of this phase as designing a custom home:

| Week | Focus | What You're Doing | Why It Matters |
|------|-------|-------------------|----------------|
| **1-4** | System Architecture | Architecture patterns, components, integrations, ADRs | The foundation everything else builds on |
| **5-7** | Security Architecture | Security controls, threat modeling, encryption, auth | Security designed in, not patched on |
| **8-10** | Data Architecture | Data models, databases, migration, retention | Data architecture is hard to change later |
| **11-14** | Infrastructure & APIs | Cloud design, networks, CI/CD, API specs | Where your code will live and how it will talk |
| **15-18** | UI/UX & Specs | User interface, prototypes, technical specs | What users will see and touch |
| **19** | Design Review & Sign-off | Present to stakeholders, get approvals | Everyone commits to the design |

**Emotional checkpoint**: You'll start excited by the creative challenge, hit complexity overwhelm around week 8 (normal!), work through detailed trade-offs, and end with architectural clarity. The complexity is real—you can navigate it.

---

## Who's on This Journey With You?

This phase needs your most senior technical people. Architecture decisions are expensive to change.

| Role | They're Responsible For | Why They Matter Now |
|------|------------------------|---------------------|
| **CTA** | Overall architecture, technical decisions, trade-offs | They own the "how" from a technical perspective |
| **Security Architect** | Security architecture, threat modeling, controls | Security architecture now = security built in later |
| **Data Architect** | Data models, databases, migration strategy | Data architecture changes are very expensive |
| **Cloud Architect** | Infrastructure design,optimization, scalability | Infrastructure decisions lock you into platforms |
| **UX Lead** | User interface, user experience, prototypes | UX validated now = rebuilt UI avoided later |
| **Tech Lead** | Implementation validation, feasibility | They'll translate architecture to code |

<details>
<summary><strong>Deep Dive: The Architecture Team in Action</strong></summary>

**CTA (Chief Technology Architect)**: This is their time to shine. They'll spend 60-70% of their time on this phase, making decisions that will shape the product for years. One good architecture decision can save millions; one bad one canmillions.

**Security Architect**: They'll design defense-in-depth security, conduct threat modeling, and define security controls. Their work prevents the "we need to add security later" problem (which never ends well).

**Data Architect**: They'll design data models that scale, handle current and future volumes, and support compliance requirements. One well-designed schema can last a decade; one poorly-designed schema gets rewritten in a year.

**Cloud Architect**: They'll design infrastructure that's scalable, reliable, and cost-optimized. They'll ask questions like *"serverless or containers?"* and *"multi-AZ or multi-region?"* that have million-dollar implications.

**UX Lead**: They'll design interfaces that users love, validated through user testing. Good UX increases adoption and reduces support costs; bad UX kills products regardless of technical quality.

**Tech Lead**: They'll validate that the architecture is implementable by the team. They'll catch designs that are theoretically sound but practically difficult.
</details>

---

## Step 1: System Architecture Design

### What You'll Achieve

You'll design the overall system architecture: components, patterns, integrations, and technology choices.

**The outcome**: A system architecture document that guides all development work.

### The Big Question: Monolith or Microservices?

This is the most common architecture question. Here's how to decide:

<details>
<summary><strong>Decision Framework: Monolith vs. Microservices</strong></summary>

**Start with a Monolith If**:
- Team size <20 developers
- You're building an MVP or v1 product
- Time-to-market is critical
- You don't have DevOps expertise for distributed systems
- Your scaling requirements are moderate (<100K users)

**Start with Microservices If**:
- Team size >20 developers (need parallel development)
- You have clear domain boundaries (bounded contexts)
- You have DevOps expertise for distributed systems
- Different components have different scaling needs
- You need independent deployment cadences

**Hybrid Approach (Recommended for Most Teams)**:
- Start with a well-structured monolith
- Design services with clear boundaries
- Extract microservices when you hit a specific pain point

**Real Example**: Shopify started as a monolith. They extracted microservices only when they hit specific scaling bottlenecks. Today, they have thousands of services but grew into it organically.
</details>

### Architecture Decision Records (ADRs)

Every significant architecture decision should be documented in an ADR:

<details>
<summary><strong>ADR Template</strong></summary>

```markdown
# ADR-001: [Decision Title]

## Status
Accepted | Proposed | Deprecated | Superseded by [ADR-XXX]

## Context
[What is the situation that requires a decision? What are the driving forces?]

## Decision
[What did we decide? Be specific.]

## Consequences
- **Positive**: [What benefits does this decision bring?]
- **Negative**: [What are the downsides or risks?]
- **Cost**: [What are theimplications?]

## Alternatives Considered
1. [Alternative 1]: [Why we rejected it]
2. [Alternative 2]: [Why we rejected it]

## Related Decisions
- [ADR-XXX]: [Related decision]
- [PRD-XXX]: [Related requirement]

## Implemented By
[Who is implementing this decision]

## Date
[YYYY-MM-DD]
```

**Example ADR Excerpt**:
```markdown
# ADR-001: PostgreSQL as Primary Database

## Context
We need a relational database with ACID transactions for our e-commerce platform.
Requirements: 100K users at launch, scaling to 1M in year 1.

## Decision
Use PostgreSQL 15+ as our primary database.

## Consequences
- **Positive**: Strong ACID support, excellent JSON support, mature ecosystem
- **Negative**: Vertical scaling limits (will need sharding at ~10M users)
- **Cost**: Moderate ($500/month for managed RDS at launch)

## Alternatives Considered
1. MySQL: Rejected due to weaker JSON support and fewer advanced features
2. MongoDB: Rejected due to lack of ACID guarantees (critical for transactions)
```
</details>

---

## Step 2: Security Architecture Design

### What You'll Achieve

You'll design comprehensive security architecture: authentication, authorization, encryption, network security, and monitoring.

**The outcome**: A security architecture document that implements your security requirements.

### Threat Modeling: Think Like an Attacker

Threat modeling identifies security vulnerabilities before you build. Use the STRIDE methodology:

| Threat Type | Description | Example | Mitigation |
|-------------|-------------|---------|------------|
| **Spoofing** | Impersonating someone else | Attacker logs in as admin | MFA, strong password policies |
| **Tampering** | Modifying data or code | Attacker modifies order total | Digital signatures, integrity checks |
| **Repudiation** | Denying an action | User claims they didn't place order | Comprehensive audit logging |
| **Information Disclosure** | Exposing sensitive data | API returns user PII | Encryption, access controls |
| **Denial of Service** | Disrupting service availability | Attacker floods API with requests | Rate limiting, DDoS protection |
| **Elevation of Privilege** | Gaining unauthorized access | Regular user accesses admin features | RBAC, least privilege |

<details>
<summary><strong>Real Example: How Threat Modeling Saved a Project</strong></summary>

**The Situation**: A team was building a financial services app.

**Threat Model Revealed**:
- An attacker could intercept API calls and replay transactions (Tampering threat)
- User session tokens weren't rotated, enabling session hijacking (Spoofing threat)
- PII was logged in clear text (Information Disclosure threat)

**The Fix** (Before Any Code Was Written):
- Added request signing with nonces to prevent replay attacks
- Implemented short-lived tokens with refresh token rotation
- Configured logging to automatically redact PII

**The Result**: When the security audit came, they passed with zero high-severity findings. The auditor said *"I've never seen a first-time audit this clean."*

**The Cost**: 2 weeks of threat modeling up front.
**The Savings**: 4 months of rework + audit delays + reputation damage.
</details>

---

## Step 3: Data Architecture Design (0)

### What You'll Achieve

You'll design logical and physical data models, database schemas, and data migration strategies.

**The outcome**: A data architecture document that supports your requirements and scales with your growth.

### Database Selection Guide

| Database | Best For | Considerations |
|----------|----------|----------------|
| **PostgreSQL** | General-purpose, ACID transactions, complex queries | Mature, reliable, great JSON support |
| **MySQL** | Traditional relational workloads | Widely supported, slightly less feature-rich than Postgres |
| **MongoDB** | Flexible schemas, document storage, rapid iteration | Schema flexibility is a double-edged sword |
| **Redis** | Caching, session storage, pub/sub | In-memory, not for persistent data |
| **Elasticsearch** | Full-text search, log analytics | Powerful search, but not a primary database |

<details>
<summary><strong>Real Example: How One Team's Data Architecture Scaled</strong></summary>

**The Situation**: A SaaS company started with PostgreSQL for everything.

**At Launch** (10K users):
- PostgreSQL handled everything beautifully
- Simple architecture, easy to maintain

**At 100K Users** (Year 1):
- Added Redis for caching (reduced DB load by 70%)
- Implemented read replicas for reporting queries

**At 1M Users** (Year 2):
- Implemented partitioning for time-series data
- Added Elasticsearch for full-text search

**At 10M Users** (Year 4):
- Extracted analytics to a data warehouse (Snowflake)
- Implemented sharding for user data

**The Key**: They didn't over-engineer at launch. They started simple and evolved the architecture as needed, guided by clear data requirements from Phase 2.
</details>

---

## Step 4: Infrastructure & API Design (1-14)

### What You'll Achieve

You'll design cloud infrastructure, networking, CI/CD pipelines, and API specifications.

**The outcome**: Infrastructure design that's scalable, secure, and cost-optimized.

### Cloud Provider Selection

| Provider | Strengths | Considerations |
|----------|-----------|----------------|
| **AWS** | Most mature, widest service selection, 30%+ market share | Can be complex, pricing can be confusing |
| **Azure** | Enterprise-friendly, strong hybrid cloud, great for .NET | Some services less mature than AWS |
| **GCP** | Strong in data/analytics/AI, developer-friendly | Smaller market share, fewer enterprise features |

**Recommendation**: Choose based on your team's expertise. All three can run your product well. Team familiarity > minor feature differences.

### API Design: REST vs. GraphQL vs. gRPC

| API Style | Best For | Considerations |
|-----------|----------|----------------|
| **REST** | General-purpose APIs, public APIs | Simple, well-understood, widely supported |
| **GraphQL** | Complex data needs, mobile apps, flexible queries | Steeper learning curve, overkill for simple APIs |
| **gRPC** | Microservices communication, internal APIs | High performance, but not browser-friendly |

<details>
<summary><strong>Real Example: How API Design Impacted Development</strong></summary>

**Team A (REST)**:
- Used REST with OpenAPI specification
- Developers could start coding from the spec immediately
- Auto-generated client SDKs for frontend and mobile
- Clear versioning strategy (/api/v1/, /api/v2/)
- Result: Fast development, easy integration

**Team B (GraphQL - Overkill)**:
- Used GraphQL because it was "trendy"
- Simple CRUD operations became complex queries
- Team spent months learning GraphQL nuances
- No clear versioning strategy
- Result: Slower development, unnecessary complexity

**The Lesson**: Use the right tool for the job. REST is the right choice for most applications.
</details>

---

## Quality Gates: Before You Move to Phase 4

Completing this phase means you have a complete blueprint for building your product.

### Exit Criteria Checklist

- ☐ **System architecture approved by CTA** (documented, reviewed, signed off)
- ☐ **Security architecture approved by CISO** (threat models completed, controls defined)
- ☐ **Data architecture approved and validated** (schemas, migrations, retention defined)
- ☐ **Infrastructure design approved and cost-validated** (cloud design,projections reviewed)
- ☐ **API and integration design completed** (specs documented, examples provided)
- ☐ **UI/UX design validated with users** (prototypes tested, feedback incorporated)
- ☐ **Technical specifications documented** (coding standards, testing strategy defined)
- ☐ **Threat modeling completed and reviewed** (all major threats identified and mitigated)
- ☐ **Design review conducted with all stakeholders** (formal presentation, sign-offs obtained)
- ☐ **Architecture Decision Records (ADRs) created** (all major decisions documented)
- ☐ **Go/no-go decision documented** (explicit decision to proceed to Phase 4)

---

## Phase Completion: Celebrate Your Progress

**You've accomplished something monumental**:

 Transformed requirements into a complete architecture
 Designed security in (not bolted on)
 Created data architecture that will scale
 Defined infrastructure that's cost-optimized
 Specified APIs that developers can implement from
 Validated UI/UX with real users
 Identified and mitigated security threats

**Next up**: Phase 4, where you'll plan the development work. Thanks to your architecture, your development team will have clear direction.

---

**Previous Phase**: [Phase 2: Requirements & Scope](../phase_02_requirements_scope/SKILL.md)
**Next Phase**: [Phase 4: Development Planning](../phase_04_development_planning/SKILL.md)

---

**Version:** 2.0.0 (Expert Mentor Edition)
**Reviewed By:** OCTALUME EXPERT MENTOR TEAM

---

*Architecture is the art of drawing lines. You've drawn them beautifully. Time to build.*

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
