# Clarification Guide

Use this guide to ensure thorough requirements gathering during the planning process.

---

## Contents
- The Clarification Loop
- Question Categories
- Zero Uncertainty Checklist
- Asking Good Questions

## The Clarification Loop

Planning is not linear. Each answer reveals new questions. Continue until zero uncertainty.

```
┌─────────────────────────────────────────────────────────────┐
│                    CLARIFICATION LOOP                       │
│                                                             │
│    ┌──────────┐    ┌───────────┐    ┌──────────┐           │
│    │ EXPLORE  │───▶│ CLARIFY   │───▶│ REFINE   │           │
│    │ codebase │    │ with user │    │ understanding        │
│    └──────────┘    └───────────┘    └────┬─────┘           │
│         ▲                                │                  │
│         │         New questions?         │                  │
│         │              YES ◀─────────────┘                  │
│         │                                                   │
│         └────────────────────────────────                   │
│                                                             │
│    Exit when: ALL uncertainty domains = RESOLVED            │
│    Minimum: 3 rounds              │
└─────────────────────────────────────────────────────────────┘
```

**Key principle:** Each user answer may spawn new questions. A "scope" answer might reveal design questions. A design decision might raise testing concerns. Follow the thread until exhausted.

---

## Question Categories

### 1. Scope & Boundaries

**Purpose:** Define what's in and out of scope clearly.

**Key Questions:**
- What specific functionality must be included?
- What should explicitly NOT be part of this work?
- Are there related features that might be affected?
- What are the system boundaries? (e.g., frontend only, backend only, full-stack)
- Should this work with existing data or start fresh?

**Example questions:**
- "Should the rate limiter apply to all endpoints or specific ones?"
- "Are we including the admin UI for configuration, or just the backend logic?"
- "Should this handle both authenticated and unauthenticated requests?"

---

### 2. Design Decisions

**Purpose:** Make architectural and technical choices explicit.

**Key Questions:**
- What architectural pattern should we follow?
- Are there existing patterns in the codebase we should match?
- What libraries or frameworks are preferred/required?
- How should this integrate with existing systems?
- What's the data model? Where is state stored?
- Are there performance requirements? (latency, throughput)
- Are there security requirements? (auth, encryption, audit)

**Example questions:**
- "Should we use Redis or in-memory storage for rate limit counters?"
- "Do you prefer token bucket or sliding window algorithm?"
- "Should this be a middleware or a decorator pattern?"

---

### 3. Implementation Preferences

**Purpose:** Understand coding style and approach preferences.

**Key Questions:**
- Should we prioritize simplicity or extensibility?
- Are there coding conventions to follow?
- How should errors be handled and reported?
- What logging level is appropriate?
- Should this be configurable? How? (env vars, config file, admin UI)

**Example questions:**
- "Should rate limits be configurable per-endpoint or global?"
- "How verbose should the logging be for debugging?"
- "Should we return detailed error messages or generic ones?"

---

### 4. Priority & Ordering

**Purpose:** Understand what to tackle first and dependencies.

**Key Questions:**
- What's the most critical part to get right?
- Is there a minimum viable version we should target first?
- What are the dependencies between features?
- Are there any hard deadlines or milestones?
- Should we deliver incrementally or all at once?

**Example questions:**
- "Should we implement basic rate limiting first, then add per-user limits?"
- "What's the priority: accuracy of limits or performance?"
- "Can we ship without the admin UI initially?"

---

### 5. Risk Tolerance

**Purpose:** Understand acceptable trade-offs.

**Key Questions:**
- How important is backwards compatibility?
- What's the impact if this fails? (Is it critical path?)
- How much testing is required before deployment?
- Should we build for scale now or optimize later?
- What's the rollback strategy if issues arise?

**Example questions:**
- "Is it acceptable to briefly exceed rate limits during high load?"
- "Should we include a kill switch to disable this in production?"
- "How thoroughly should this be tested before deploying?"

---

### 6. Testing Requirements

**Purpose:** Define what testing is expected.

**Key Questions:**
- What types of tests are required? (unit, integration, e2e)
- Are there existing test patterns to follow?
- What edge cases must be covered?
- Is performance testing required?
- Should we include load testing?

**Example questions:**
- "Should we add integration tests with Redis, or mock it?"
- "Do we need to test concurrent request handling?"
- "What's the expected behavior at exactly the rate limit?"

---

### 7. Performance Constraints

**Purpose:** Understand performance expectations.

**Key Questions:**
- What's the expected load? (requests/second)
- What's the acceptable latency impact?
- Are there memory constraints?
- Should this work in distributed environments?
- What's the data volume expectation?

**Example questions:**
- "What's the maximum acceptable latency overhead per request?"
- "Should rate limits be synchronized across multiple servers?"
- "How many unique users/IPs should we expect to track?"

---

### 8. Security Considerations

**Purpose:** Identify security requirements and concerns.

**Key Questions:**
- Is authentication required?
- What data is sensitive?
- Are there compliance requirements? (GDPR, SOC2, etc.)
- Should actions be audited?
- What are the trust boundaries?

**Example questions:**
- "Should rate limit data include any PII?"
- "Do we need to log rate limit violations for security review?"
- "How should we handle attempts to bypass rate limits?"

---

## Zero Uncertainty Checklist

Before finalizing the plan, verify ALL domains are resolved:

### Scope Uncertainty
- [ ] What's included is explicitly listed
- [ ] What's excluded is explicitly listed
- [ ] Boundary conditions are defined
- [ ] Edge cases are identified

### Design Uncertainty
- [ ] Architecture approach is decided
- [ ] Technology/library choices are made
- [ ] Integration points are mapped
- [ ] Data flow is understood

### Implementation Uncertainty
- [ ] File/function targets are identified
- [ ] Order of operations is clear
- [ ] Dependencies between steps are mapped
- [ ] Fallback strategies exist for risky steps

### Verification Uncertainty
- [ ] Success criteria are specific and testable
- [ ] Test approach is agreed upon
- [ ] Manual verification steps are defined
- [ ] Rollback strategy exists

### Outcome Uncertainty
- [ ] Expected behavior is documented
- [ ] Performance expectations are set
- [ ] Error handling approach is clear
- [ ] User-facing changes are described

**Exit condition:** Every checkbox above can be answered with confidence. If ANY domain has uncertainty, ask more questions.

---

## Asking Good Questions

### CRITICAL: Mark Your Recommendation

When presenting options, ALWAYS indicate which you recommend:

```
Question: "How should we store rate limit data?"

Options:
1. **In-memory (Recommended)** - Simple, fast, resets on restart
2. Redis - Persistent, multi-instance, requires setup
3. Database - Most durable, highest latency

Why recommended: In-memory is simplest for single-instance deployments
and matches your current architecture. Choose Redis only if you need
multi-instance coordination.
```

**Format requirements:**
- Bold the recommended option OR append "(Recommended)"
- Briefly explain WHY it's recommended given the context
- Present trade-offs honestly - don't hide downsides of your recommendation

### Do:
- Ask one question at a time when using AskUserQuestion
- Provide context for why you're asking
- Offer 2-4 concrete options when applicable
- Mark your recommended option with "(Recommended)"
- Explain trade-offs briefly

### Don't:
- Ask vague, open-ended questions
- Assume requirements without confirming
- Skip categories that seem obvious
- Rush through clarification to start coding
