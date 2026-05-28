---
name: critical-thinking
description: Proactively challenge implementation plans, architecture decisions, and design assumptions. Use when reviewing plans, designs, or technical decisions. Verifies claims via web search, cross-references documentation, identifies risks and gaps, and surfaces hidden assumptions. Activates automatically when evaluating technical proposals.
---

# Critical Thinking

Systematically question implementation plans, architecture decisions, and technical assumptions to surface risks, gaps, and unverified claims before they become problems.

## Overview

This skill **proactively engages** when reviewing:
- Implementation plans and roadmaps
- Architecture and design decisions
- Technology choices and trade-offs
- Performance and scalability claims
- Security assumptions
- Testing strategies

## Core Principle

> **"What evidence supports this decision? What could make it wrong?"**

Every technical decision rests on assumptions. This skill surfaces those assumptions and verifies them against:
1. **Web search** — Current best practices, known issues, benchmarks
2. **Existing documentation** — CLAUDE.md, design docs, prior decisions
3. **Architectural principles** — From microservices-architect and optima-service-planner skills
4. **First principles** — Does this make logical sense?

## The VERIFY Framework

For every significant claim or decision, apply:

| Step | Action | Question |
|------|--------|----------|
| **V**alidate | Check the source | Where does this claim come from? Is it authoritative? |
| **E**vidence | Seek supporting data | What evidence exists? What's the sample size? |
| **R**isks | Identify failure modes | What happens if this assumption is wrong? |
| **I**mpact | Assess consequences | How severe are the consequences of being wrong? |
| **F**alsify | Try to disprove | What would prove this claim false? |
| **Y**ield | Decide and document | Accept, reject, or flag for more research? |

## Activation Triggers

This skill activates when encountering:

### Direct Triggers
- "Let's use X because it's faster"
- "This should scale to Y users"
- "The best practice is to..."
- "Everyone uses X for this"
- "This is the industry standard"
- "We don't need to worry about..."

### Contextual Triggers
- Reviewing implementation plans
- Evaluating architecture decisions
- Assessing technology choices
- Analyzing performance claims
- Reviewing security approaches

## Critical Questions by Domain

### Architecture & Design
| Question | Why It Matters |
|----------|----------------|
| What problem does this actually solve? | Ensures we're not solving the wrong problem |
| What are the alternatives we didn't choose? | Confirms we've considered options |
| What are the trade-offs we're accepting? | Makes implicit costs explicit |
| How will this evolve in 2 years? | Tests long-term viability |
| What's the blast radius if this fails? | Assesses risk containment |

### Performance & Scalability
| Question | Why It Matters |
|----------|----------------|
| Where does that benchmark come from? | Vendor benchmarks often misleading |
| What's the actual expected load? | Prevents over/under-engineering |
| What's the bottleneck? | Ensures we're optimizing the right thing |
| How was this tested? | Validates methodology |
| What happens at 10x load? | Tests scaling assumptions |

### Security
| Question | Why It Matters |
|----------|----------------|
| What's the threat model? | Ensures we know what we're defending against |
| What's the attack surface? | Identifies exposure points |
| Who has access to what? | Validates least privilege |
| How do we know it's working? | Ensures observability |
| What's the incident response? | Prepares for failure |

### Dependencies & Integration
| Question | Why It Matters |
|----------|----------------|
| What's the maintenance status? | Checks for abandonware |
| What's the license? | Avoids legal issues |
| What happens if this dependency fails? | Tests resilience |
| Can we replace this later? | Avoids lock-in |
| Who else uses this at scale? | Validates production readiness |

## Verification Protocol

When a claim requires verification:

### 1. Identify the Claim
```
Claim: "Redis can handle 100k ops/second easily"
Type: Performance claim
Source: Team assumption
```

### 2. Search for Evidence
```
WebSearch: "Redis performance benchmarks 2024"
WebSearch: "Redis 100k operations per second production"
WebSearch: "Redis performance issues at scale"
```

### 3. Cross-Reference
```
- Check official Redis documentation
- Look for production case studies
- Find contrary evidence (what problems do people report?)
```

### 4. Assess and Document
```
Finding: Redis can achieve 100k+ ops/sec but:
- Depends on operation type (GET vs complex operations)
- Requires proper configuration
- Network latency often the bottleneck
- Persistence mode affects performance significantly

Recommendation: Verify with load test using actual operation mix
```

## Risk Assessment Matrix

| Impact | Probability | Action |
|--------|-------------|--------|
| High | High | **STOP** - Requires resolution before proceeding |
| High | Low | **FLAG** - Document risk and mitigation |
| Low | High | **MONITOR** - Track but don't block |
| Low | Low | **NOTE** - Document for awareness |

## Red Flags to Watch For

### Certainty Without Evidence
- "This will definitely work"
- "There's no way this could fail"
- "Trust me, I've done this before"

### Appeal to Authority
- "Google does it this way"
- "The documentation says..."
- "Best practice is..."

### Premature Optimization
- "We need to optimize for scale from day one"
- "Let's use X because it's faster"
- "We might need this later"

### Hidden Complexity
- "It's just a simple..."
- "We just need to..."
- "It should only take..."

### Missing Failure Modes
- No discussion of what happens when things fail
- No rollback plan
- No monitoring strategy

## Integration with Other Skills

### microservices-architect
Cross-reference against:
- Prime Directives (observability, async-by-default, etc.)
- Pattern applicability
- Operational requirements

### optima-service-planner
Verify alignment with:
- Optima Prime Directives
- Database Gateway pattern
- Append-only contracts
- Deployment requirements

## Output Format

When raising concerns, use this format:

```markdown
## Concern: [Brief title]

**Claim:** [What's being claimed]
**Risk Level:** High | Medium | Low
**Evidence:** [What supports or contradicts]

### Questions
1. [Specific question]
2. [Specific question]

### Verification Needed
- [ ] [What to verify]
- [ ] [What to verify]

### Recommendation
[Accept / Reject / Investigate further]
```

## Supporting Files

- [FRAMEWORKS.md](FRAMEWORKS.md) — Mental models for evaluation
- [QUESTIONS.md](QUESTIONS.md) — Domain-specific question templates
- [VERIFICATION.md](VERIFICATION.md) — Fact-checking procedures
- [BIASES.md](BIASES.md) — Cognitive biases to watch for

## Operating Stance

```
┌─────────────────────────────────────────────────────────────┐
│  Be curious, not adversarial                                │
│  Seek evidence, not opinions                                │
│  Question proportionally to risk                            │
│  Verify claims that matter                                  │
│  Document findings for future reference                     │
│  Suggest alternatives, not just problems                    │
└─────────────────────────────────────────────────────────────┘
```

## When NOT to Challenge

- Trivial decisions with low impact
- Well-documented, battle-tested approaches
- Decisions already backed by evidence
- Time-critical situations (flag for later review)
- Personal preferences that don't affect outcomes
