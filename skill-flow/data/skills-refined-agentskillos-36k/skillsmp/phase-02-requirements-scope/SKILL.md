---
name: "phase_02_requirements_scope"
description: "You'll transform your PRD into detailed, testable requirements. Through stakeholder workshops and user validation, you'll create crystal-clear functional requirements, solid non-functional requirements, comprehensive security specifications, and a traceability matrix that connects everything. This is where vision becomes buildable."
phase: 2
phase_name: "Requirements & Scope"
owner: "Product Owner (functional), CTA (technical)"
secondary_owner: "Business Analyst / Systems Analyst"
participants: ["Tech Lead", "CTA", "Security Lead", "Compliance Officer", "Data Architect", "DevOps", "SRE", "Performance Engineer", "Users", "Subject Matter Experts"]
entry_criteria: [
  "Business case approved by Executive Sponsor",
  "PRD completed and reviewed",
  "Technical feasibility confirmed",
  "Security considerations documented",
  "Stakeholders aligned and committed"
]
exit_criteria: [
  "Functional requirements documented and approved",
  "Non-functional requirements defined and baselined",
  "Security requirements documented and approved",
  "Compliance requirements identified and validated",
  "Data requirements documented",
  "Requirements traceability matrix created",
  "All requirements signed off by stakeholders",
  "Go/no-go decision to proceed to Phase 3"
]
estimated_duration: "1 week"
dependencies: ["phase_01_vision_strategy"]
outputs: [
  "Functional Requirements Specification",
  "User Stories and Use Cases",
  "Acceptance Criteria",
  "Prioritized Backlog",
  "Non-Functional Requirements Specification",
  "Performance SLAs",
  "Security Requirements Specification",
  "Compliance Requirements Specification",
  "Data Requirements Specification",
  "Requirements Traceability Matrix"
]
next_phase: "phase_03_architecture_design"
---

# Phase 2: Requirements & Scope
## Where Vision Becomes Buildable

---

## Welcome to the Detail Phase

Great work completing Phase 1! You've got funding, alignment, and a clear vision. Now comes the critical work that separates successful products from the *"we built the wrong thing"* disasters.

Here's the truth: **Most failed projects fail in this phase**, not in development. They build beautifully... the wrong thing. You're not going to be one of those projects.

**Here's what you'll walk away with:**

 Requirements so clear a developer could start coding tomorrow
 Non-functional requirements that ensure your product actually works at scale
 Security requirements designed in (not patched on later)
 A traceability matrix that connects every requirement to its source
 Stakeholders who've explicitly signed off on exactly what you're building

**Time investment**: 8-12 weeks (yes, it's substantial—this is where you buy down risk)

---

## What This Phase Feels Like (A Real Story)

I worked with a SaaS company that rushed through requirements. They spent 3 weeks on this phase and 9 months building. At launch, customers said *"this doesn't solve our problem."* They spent 6 months rebuilding.

Contrast that with a team I advised that spent 10 weeks on requirements:

- **Zero scope creep** during development (the developers were amazed)
- **Stakeholder harmony**—no mid-project "that's not what I wanted"
- **Security clearance** obtained in half the usual time (requirements were crystal clear)
- **Launched on schedule** with 94% user satisfaction

Their Tech Lead told me: *"I was frustrated by how long requirements took. Two months later, I was thanking you. Every question I had was already answered."*

That's the feeling we're aiming for. This phase feels slow, but it makes everything else fast.

---

## Your Journey Through This Phase

Think of this phase as building the blueprint for a house:

| Week | Focus | What You're Doing | Why It Matters |
|------|-------|-------------------|----------------|
| **1-3** | Functional Requirements | Detailed feature definitions, user stories, acceptance criteria | These are the "what" everyone will build |
| **4-5** | Non-Functional Requirements | Performance, scalability, availability targets | These ensure it works well under load |
| **6-7** | Security & Compliance | Security controls, regulatory requirements, audit needs | Security first, compliance baked in |
| **8-9** | Data Requirements | Data models, privacy, retention, volumes | Data is your most valuable asset |
| **10-11** | Traceability & Sign-off | RTM creation, stakeholder reviews, formal sign-offs | Everyone commits to the same plan |

**Emotional checkpoint**: You'll start energized from Phase 1, hit the "requirements fatigue" wall around week 6 (totally normal), push through detailed documentation, and end with deep confidence. The wall is real—you can climb it.

---

## Who's on This Journey With You?

This phase needs more specialists than Phase 1. Requirements depth demands expertise.

| Role | They're Responsible For | Why They Matter Now |
|------|------------------------|---------------------|
| **You (Product Owner)** | Functional requirements, user stories, priorities | You own the "what" from the user's perspective |
| **CTA** | Non-functional requirements, technical feasibility | They ensure requirements are actually achievable |
| **Business Analyst** | Eliciting and documenting requirements | They're the requirements translation engine |
| **Security Lead** | Security requirements and controls | Security requirements now = security built in later |
| **Compliance Officer** | Regulatory requirements and mapping | Non-compliance discovered later = project delay |
| **Data Architect** | Data models, privacy, volumes | Data architecture is hard to change later |

<details>
<summary><strong>Deep Dive: The Requirements Team in Action</strong></summary>

**Product Owner (You)**: You'll spend 40-50 hours per week reviewing requirements, meeting with stakeholders, and prioritizing. You're the final arbiter of "what's in scope."

**Business Analyst**: This is their time to shine. They'll run workshops, document requirements, create user stories, and build the RTM. A great BA is worth their weight in gold.

**CTA**: They'll spend 10-15 hours per week reviewing requirements for technical feasibility. They'll catch requirements like *"real-time sync across 10M users"* early, when it's just a conversation.

**Security Lead**: They'll define security requirements like *"all API calls must be authenticated"* and *"PII must be encrypted at rest."* These become architecture drivers in Phase 3.

**Compliance Officer**: They'll map requirements to regulations like GDPR or HIPAA. One compliance requirement missed now can can cause significant delays in delays later.

**Data Architect**: They'll define data entities, relationships, and volumes. They'll ask questions like *"how many users will we have in 3 years?"* that impact infrastructure planning.
</details>

---

## Step 1: Functional Requirements

### What You'll Achieve

You'll transform PRD features into detailed, testable requirements that leave no room for ambiguity.

**The outcome**: A functional requirements specification so clear that developers, testers, and stakeholders all have the same understanding.

### Your Action Plan

| Week | Focus | Key Activities | Deliverable |
|------|-------|----------------|-------------|
| **Week 1** | Requirements Elicitation | Stakeholder workshops, user interviews, requirements gathering | Raw requirements list |
| **Week 2** | User Stories & Acceptance | Create user stories, define acceptance criteria, prioritize (MoSCoW) | User stories, acceptance criteria, prioritized backlog |
| **Week 3** | Documentation & Validation | Write functional requirements spec, review with stakeholders | Functional Requirements Specification |

### What Makes a Requirement "Good"?

<details>
<summary><strong>The Quality Requirements Checklist</strong></summary>

Every requirement should pass this test:

**✓ Specific**: Clear and unambiguous
- Bad: "The system should be fast"
- Good: "The system must respond to user actions within 200 milliseconds"

**✓ Measurable**: Can be tested and verified
- Bad: "The system should be easy to use"
- Good: "New users can complete core workflow within 5 minutes without training"

**✓ Achievable**: Technically feasible with available resources
- Bad: "The system shall support unlimited concurrent users"
- Good: "The system shall support 10,000 concurrent users (scalable to 100,000)"

**✓ Relevant**: Actually needed for the product
- Bad: "The system shall support 47 languages" (if your market is English-only)
- Good: "The system shall support English and Spanish (top 2 user languages)"

**✓ Testable**: Can be verified through testing
- Bad: "The system shall provide a good user experience"
- Good: "User satisfaction score must be ≥ 4.5/5.0 in post-launch survey"

**✓ Traceable**: Linked to source (PRD, user need, regulation)
- Every requirement ID (e.g., REQ-FUNC-001) should link back to a PRD item or user story
</details>

### Real Example: From Vague to Precise

<details>
<summary><strong>See How One Team Transformed Their Requirements</strong></summary>

**Initial PRD Statement**: "Users can search for products."

**First Pass (Still Vague)**:
```
REQ-001: The system shall provide search functionality.
```
*Problem*: What kind of search? What fields? How fast?

**Second Pass (Better)**:
```
REQ-001: The system shall allow users to search for products by name,
category, and SKU. Search results must be returned within 1 second.
```
*Better*: Now we know what and how fast. But still fuzzy on details.

**Final Pass (Testable)**:
```
REQ-001: Product Search

**Description**: Users shall be able to search for products using the following:
- Product name (full-text search)
- Category (dropdown selection)
- SKU (exact match)

**Performance**: Search results must be displayed within 1 second for 95% of queries.

**Scope**: Search shall query the product catalog database containing up to
100,000 products.

**Acceptance Criteria**:
1. User can enter search term in search box
2. System returns products matching search criteria
3. Results are ranked by relevance
4. Results display product name, image, price, and "Add to Cart" button
5. No results state shows helpful message
6. Search is case-insensitive
7. Partial matches are supported (e.g., "phone" matches "smartphone")

**Priority**: Must Have (MVP)
**Source**: PRD-3.2 (Core User Features)
**Owner**: Product Owner
```

*This is a requirement a developer can implement and a tester can verify.*
</details>

---

## Step 2: Non-Functional Requirements

### What You'll Achieve

You'll define the quality attributes that determine how well your system performs: speed, scalability, reliability, usability.

**The outcome**: Clear performance targets that drive architecture and provide acceptance criteria.

### Why NFRs Matter (The Hard Truth)

<details>
<summary><strong>Real Story: When NFRs Were Ignored</strong></summary>

**The Situation**: A team built an e-commerce platform with vague NFRs: *"system should be fast and reliable."*

**What Happened**:
- Launch day: 5,000 users simultaneously hit "Add to Cart"
- Response time: 45 seconds (users abandoned)
- Database crashed under load
- Site was down for 6 hours
- Lost significant revenue in sales in one day
- Company's reputation took a massive hit

**The Post-Mortem**:
- No performance requirements were defined
- No load testing was done (no targets to test against)
- Database couldn't handle concurrent writes
- No caching strategy was designed

**What Good NFRs Would Have Done**:
- "System must support 5,000 concurrent users" → would have driven architecture
- "Response time <500ms for 95% of requests" → would have required caching
- "99.9% uptime (4.3 hours downtime/month)" → would have required high-availability design

**The Lesson**: Vague NFRs = failed launches. Specific NFRs = systems that work.
</details>

### NFR Categories and Examples

| Category | What It Covers | Example Requirements |
|----------|----------------|---------------------|
| **Performance** | Response time, throughput, latency | "API responses <200ms for 95% of requests" |
| **Scalability** | User growth, data growth, transaction volume | "System must scale to 100,000 users without code changes" |
| **Availability** | Uptime, downtime, reliability | "99.9% uptime (max 43 minutes downtime/month)" |
| **Usability** | UI/UX standards, accessibility | "WCAG 2.1 AA compliant, new users onboard in <5 minutes" |
| **Maintainability** | Code quality, documentation, technical debt | "Code coverage ≥80%, all APIs documented" |
| **Operability** | Monitoring, alerting, deployment | "All critical metrics monitored, alerts fired within 1 minute" |

---

## Step 3: Security Requirements

### What You'll Achieve

You'll define comprehensive security requirements that will drive your security architecture.

**The outcome**: Security requirements that ensure compliance and protect your users.

### The Security Requirements Framework

<details>
<summary><strong>Complete Security Requirements Template</strong></summary>

**1. Authentication & Authorization**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| SEC-001 | Users must authenticate using email/password or SSO | Must Have |
| SEC-002 | Multi-factor authentication (MFA) required for admin users | Must Have |
| SEC-003 | MFA optional for standard users (encouraged) | Should Have |
| SEC-004 | Role-based access control (RBAC) with least privilege | Must Have |
| SEC-005 | Session timeout after 30 minutes of inactivity | Must Have |

**2. Data Protection**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| SEC-006 | All PII encrypted at rest using AES-256 | Must Have |
| SEC-007 | All data in transit encrypted using TLS 1.3 | Must Have |
| SEC-008 | Encryption keys managed using AWS KMS or HashiCorp Vault | Must Have |
| SEC-009 | Data masking for PII in logs and non-production environments | Must Have |

**3. Audit & Logging**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| SEC-010 | All authentication attempts logged (success and failure) | Must Have |
| SEC-011 | All authorization changes logged | Must Have |
| SEC-012 | Logs retained for 90 days (compliance requirement) | Must Have |
| SEC-013 | Log integrity protected (immutable or signed) | Should Have |

**4. Network Security**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| SEC-014 | All services deployed within VPC with private subnets | Must Have |
| SEC-015 | Web Application Firewall (WAF) required for all public endpoints | Must Have |
| SEC-016 | DDoS protection implemented (AWS Shield or similar) | Must Have |

**5. Vulnerability Management**

| Requirement | Description | Priority |
|-------------|-------------|----------|
| SEC-017 | Static Application Security Testing (SAST) in CI/CD pipeline | Must Have |
| SEC-018 | Dynamic Application Security Testing (DAST) before release | Must Have |
| SEC-019 | Dependency scanning (SCA) for all third-party libraries | Must Have |
| SEC-020 | Critical vulnerabilities patched within 7 days | Must Have |
</details>

---

## Step 4: Compliance Requirements

### What You'll Achieve

You'll identify all applicable regulations and map them to technical requirements.

**The outcome**: A compliance matrix that ensures you meet all regulatory obligations.

### Common Regulations and Their Implications

| Regulation | Industry | Key Requirements | What It Means for Your Product |
|------------|----------|------------------|-------------------------------|
| **GDPR** | EU data subjects | Data subject rights, breach notification (72h), data protection by design | User data export, consent management, breach response plan |
| **HIPAA** | Healthcare | PHI protection, access controls, audit trails, business associate agreements | Encryption, access logs, BAAs with vendors |
| **PCI DSS** | Payments | Card data protection, vulnerability scanning, quarterly reviews | Tokenization, no card data storage, ASV scans |
| **SOC 2** | SaaS vendors | Security, availability, privacy controls; annual audits | Control documentation, evidence collection, audit readiness |
| **SOX** | Public companies | Financial controls, change management, audit trails | Change approval process, financial data integrity |

---

## Step 5: Data Requirements

### What You'll Achieve

You'll define all data entities, relationships, volumes, and privacy requirements.

**The outcome**: A data requirements specification that drives database design and compliance.

### What to Define

<details>
<summary><strong>Data Requirements Checklist</strong></summary>

**✓ Data Entities**
- List all data entities (User, Order, Product, Transaction, etc.)
- For each entity, define attributes and types
- Example: User (id: UUID, email: string, name: string, created_at: timestamp)

**✓ Data Relationships**
- Entity relationships (one-to-one, one-to-many, many-to-many)
- Example: User → Orders (one-to-many), Order → Products (many-to-many)

**✓ Data Volumes**
- Current volumes (if migrating from existing system)
- Projected volumes (1 year, 3 years, 5 years)
- Example: "10,000 users at launch, 100,000 by year 1, 500,000 by year 3"

**✓ Data Retention**
- How long each data type is retained
- Example: "Transaction data retained for 7 years (tax requirement), user activity logs 90 days"

**✓ Data Privacy**
- Data classification (public, internal, confidential, restricted)
- PII identification and handling
- Example: "User email and name are PII, must be encrypted at rest"

**✓ Data Lifecycle**
- Create, read, update, delete, archive, purge
- Example: "User accounts soft-deleted (archive) for 30 days, then permanently deleted"

**✓ Data Security**
- Encryption requirements (at rest, in transit)
- Access controls (who can access what)
- Example: "Only authorized support staff can access user PII, all access logged"
</details>

---

## The Requirements Traceability Matrix (RTM)

### Why RTMs Matter

The RTM is your most important artifact in this phase. It connects every requirement to its source and tracks it through all phases.

**Without an RTM**:
- "Why did we build this feature?" *crickets*
- "Does this requirement have a test?" *unknown*
- "What happens if we remove this feature?" *cascade of unknown impacts*

**With an RTM**:
- Every requirement traces to a PRD item, user story, or regulation
- Every requirement has tests defined
- Impact analysis is instant (trace forward and backward)

### RTM Structure

| Requirement ID | Source | Description | Owner | Priority | Status | Test Coverage | Phase | Verified |
|----------------|--------|-------------|-------|----------|--------|---------------|-------|----------|
| REQ-FUNC-001 | PRD-3.2 | User authentication | Product Owner | Must | Approved | Yes | P5 | ☐ |
| REQ-FUNC-002 | USER-001 | Password reset | Product Owner | Should | Draft | No | P5 | ☐ |
| REQ-NFR-001 | NFR-2.1 | Response time <200ms | CTA | Must | Baseline | Yes | P6 | ☐ |
| REQ-SEC-001 | SEC-1.1 | MFA required for admins | Security Lead | Must | Approved | Yes | P5 | ☐ |
| REQ-DATA-001 | GDPR-ART-32 | Data export functionality | Product Owner | Must | Approved | Yes | P5 | ☐ |

**Columns Explained**:
- **Requirement ID**: Unique identifier (REQ-{TYPE}-{###})
- **Source**: Where this came from (PRD, user story, regulation)
- **Description**: Brief requirement description
- **Owner**: Who owns this requirement
- **Priority**: Must/Should/Could/Won't
- **Status**: Draft/Under Review/Approved/Implemented
- **Test Coverage**: Yes/No (is there a test for this?)
- **Phase**: Which phase implements this
- **Verified**: Checkbox for verification sign-off

---

## Quality Gates: Before You Move to Phase 3

Completing this phase is exhausting—but you've just dramatically de-risked your project.

### Exit Criteria Checklist

- ☐ **Functional requirements documented and approved** (every feature defined and signed off)
- ☐ **Non-functional requirements defined and baselined** (performance targets set)
- ☐ **Security requirements documented and approved** (security requirements complete)
- ☐ **Compliance requirements identified and validated** (regulations mapped to requirements)
- ☐ **Data requirements documented** (data entities, volumes, privacy defined)
- ☐ **Requirements traceability matrix created** (every requirement traced to source)
- ☐ **All requirements signed off by stakeholders** (explicit sign-offs, not implicit)
- ☐ **Go/no-go decision documented** (explicit decision to proceed to Phase 3)

### The Big Question: Are Requirements Good Enough?

<details>
<summary><strong>Test Your Requirements Quality</strong></summary>

Ask these questions. If you can't answer "yes" to all, your requirements aren't ready:

**1. The Developer Test**
Could a developer who knows nothing about this project read your requirements and start coding without asking clarifying questions?

**2. The Tester Test**
Could a tester write test cases based solely on your requirements, without making assumptions?

**3. The Stakeholder Test**
If a stakeholder said "this isn't what I wanted," could you point to the specific requirement they approved?

**4. The Traceability Test**
Can you trace every requirement back to its source (PRD, user story, regulation)?

**5. The Testability Test**
Does every requirement have at least one test case defined?

**6. The Priority Test**
Is every requirement prioritized (Must/Should/Could/Won't)?

**7. The Feasibility Test**
Has the CTA confirmed that all requirements are technically achievable?

If you answer "no" to any of these, you're not ready for Phase 3. Keep working.
</details>

---

## Templates and Examples

Everything you need is in these directories:

```
./templates/
├── functional_requirements_template.md   # Detailed functional requirements
├── user_story_template.md                # User story format
├── nfr_template.md                       # Non-functional requirements
├── security_requirements_template.md     # Security requirements
├── compliance_matrix_template.md         # Regulation mapping
├── data_requirements_template.md         # Data entities and volumes
└── rtm_template.md                       # Requirements traceability matrix

./examples/
├── sample_requirements_specification.md  # Complete requirements example
├── sample_rtm.xlsx                       # Excel RTM example
└── sample_compliance_mapping.md          # Regulation-to-requirement mapping
```

---

## Phase Completion: Celebrate Your Progress

**You've accomplished something massive**:

 Transformed vision into detailed, testable requirements
 Defined performance and quality targets
 Built security and compliance into requirements
 Created a traceability matrix that connects everything
 Got explicit stakeholder sign-offs

**Next up**: Phase 3, where you'll design the architecture. Thanks to your requirements, your architecture team will have clear direction.

---

**Previous Phase**: [Phase 1: Vision & Strategy](../phase_01_vision_strategy/SKILL.md)
**Next Phase**: [Phase 3: Architecture & Design](../phase_03_architecture_design/SKILL.md)

---

**Questions or need guidance?**

- **Framework Overview**: See `../../README.md`
- **All Phase Details**: See `skills/phase_*/SKILL.md`
- **Role Definitions**: See `skills/shared/roles/SKILL.md`
- **Security Guidance**: See `skills/shared/security/SKILL.md`
- **Compliance Guidance**: See `skills/shared/compliance/SKILL.md`

---

**Version:** 2.0.0 (Expert Mentor Edition)
**Reviewed By:** OCTALUME EXPERT MENTOR TEAM

---

*You're doing the hard work that makes everything else easy. Keep it up.*

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
