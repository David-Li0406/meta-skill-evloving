---
name: architecture-research
description: "Software architecture research and design toolkit. Research technology stacks, design patterns, system architectures, and create Architecture Decision Records (ADRs) for informed technology choices."
allowed-tools: [Read, Write, Edit, Bash, WebFetch, WebSearch]
---

# Software Architecture Research

## Overview

Architecture research is a systematic process for evaluating technology options, design patterns, and system architectures. Create Architecture Decision Records (ADRs) to document decisions with context, rationale, and trade-offs. Use this skill to make informed technology choices backed by real research.

## When to Use This Skill

This skill should be used when:
- Evaluating technology stack options for a new project
- Researching design patterns and architectural approaches
- Comparing cloud services and infrastructure options
- Creating Architecture Decision Records (ADRs)
- Documenting technology trade-offs and rationale
- Researching integration patterns and best practices

## Visual Enhancement with Project Diagrams

**When documenting architecture decisions, always include diagrams.**

Use the **project-diagrams** skill to generate:
- C4 model diagrams (Context, Container, Component)
- System architecture diagrams
- Integration pattern diagrams
- Deployment architecture diagrams
- Data flow diagrams

```bash
python .claude/skills/project-diagrams/scripts/generate_schematic.py "diagram description" -o diagrams/output.png
```

---

## Architecture Research Process

### Phase 1: Context Gathering

Before researching solutions, understand the problem space.

#### Requirements Analysis

**Functional Requirements:**
- What must the system do?
- What are the core use cases?
- What integrations are required?

**Non-Functional Requirements (Quality Attributes):**

| Attribute | Questions to Answer |
|-----------|-------------------|
| **Performance** | Response time targets? Throughput requirements? |
| **Scalability** | Expected growth? Peak loads? Scaling dimensions? |
| **Availability** | Uptime requirements? Recovery time objectives? |
| **Security** | Authentication needs? Data sensitivity? Compliance? |
| **Maintainability** | Team size? Skill levels? Update frequency? |
| **Cost** | Budget constraints? Operational cost limits? |

#### Constraints Identification

**Technical Constraints:**
- Existing systems to integrate with
- Required technology compatibility
- Infrastructure limitations
- Data residency requirements

**Organizational Constraints:**
- Team skills and experience
- Timeline pressures
- Budget limitations
- Vendor preferences or restrictions

### Phase 2: Technology Research

Research options systematically using real documentation and benchmarks.

#### Research Protocol

**For each technology option:**

1. **Official Documentation Review**
   - Use `research-lookup` to find official docs
   - Verify current version and roadmap
   - Check feature completeness for requirements

2. **Production Case Studies**
   - Search for "X in production" experiences
   - Look for similar-scale deployments
   - Find post-mortems and lessons learned

3. **Benchmark Data**
   - Search for performance benchmarks
   - Find comparison studies
   - Verify benchmark relevance to your use case

4. **Community Health**
   - Check GitHub stars, commits, contributors
   - Review issue resolution time
   - Assess documentation quality

5. **Total Cost of Ownership**
   - Licensing costs
   - Infrastructure requirements
   - Operational overhead
   - Training and hiring costs

#### Technology Comparison Matrix

Create a comparison matrix for each decision area:

```yaml
comparison:
  category: "Database"
  options:
    - name: "PostgreSQL"
      pros:
        - "ACID compliance"
        - "Rich feature set"
        - "Strong community"
      cons:
        - "Vertical scaling primarily"
        - "Operational complexity at scale"
      fit_score: 8  # 1-10
      sources:
        - "Official PostgreSQL documentation"
        - "Benchmark: TPC-C results"
    - name: "MongoDB"
      pros:
        - "Horizontal scaling"
        - "Flexible schema"
        - "Developer friendly"
      cons:
        - "Eventual consistency trade-offs"
        - "Memory usage"
      fit_score: 6
      sources:
        - "MongoDB documentation"
        - "Case study: Company X migration"
```

### Phase 3: Design Pattern Research

Research architectural patterns appropriate for the problem.

#### Common Architectural Patterns

| Pattern | When to Use | Trade-offs |
|---------|-------------|------------|
| **Monolithic** | Small team, simple domain, rapid MVP | Scaling limits, deployment coupling |
| **Microservices** | Large team, complex domain, independent scaling | Operational complexity, network overhead |
| **Event-Driven** | Async workflows, decoupled systems, audit trails | Eventual consistency, debugging complexity |
| **Serverless** | Variable load, simple functions, cost optimization | Cold starts, vendor lock-in, state management |
| **CQRS** | Read/write asymmetry, complex queries | Complexity, eventual consistency |
| **Hexagonal** | Testability, multiple interfaces, long-lived systems | Initial overhead, abstraction complexity |

#### Pattern Evaluation Checklist

For each pattern considered:
- [ ] Does it address the core requirements?
- [ ] Does team have experience with this pattern?
- [ ] What are the operational implications?
- [ ] What are the testing implications?
- [ ] What are the scaling characteristics?
- [ ] What are the failure modes?

### Phase 4: Architecture Decision Records (ADRs)

Document decisions in ADR format for future reference.

#### ADR Template

```markdown
# ADR-NNN: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
What is the issue that we're seeing that is motivating this decision or change?

## Decision Drivers
- [Driver 1]
- [Driver 2]
- [Driver 3]

## Considered Options
1. [Option 1]
2. [Option 2]
3. [Option 3]

## Decision
We will use [Option X] because [reasoning].

## Rationale
Detailed explanation of why this option was chosen over alternatives.

### Option 1: [Name]
**Pros:**
- Pro 1
- Pro 2

**Cons:**
- Con 1
- Con 2

**Evidence:**
- [Source/benchmark/case study]

### Option 2: [Name]
[Same structure]

## Consequences

### Positive
- [Consequence 1]
- [Consequence 2]

### Negative
- [Consequence 1]
- [Mitigation strategy]

### Risks
- [Risk 1] - Mitigation: [Strategy]

## Related Decisions
- [ADR-XXX: Related decision]

## References
- [Link to documentation]
- [Link to benchmark]
- [Link to case study]
```

#### ADR Best Practices

**Do:**
- Write ADRs as you make decisions, not after
- Include context that future readers will need
- Link to evidence and sources
- Document rejected options and why
- Keep ADRs immutable (supersede, don't edit)

**Don't:**
- Write ADRs retrospectively without context
- Omit trade-offs or negative consequences
- Make decisions without research evidence
- Leave ADRs in "Proposed" status indefinitely

### Phase 5: C4 Model Documentation

Use the C4 model to document architecture at multiple levels.

#### Level 1: System Context Diagram

Shows the system in context with users and external systems.

**Include:**
- System under design (single box)
- User types/personas
- External systems
- Relationships and data flows

```bash
python .claude/skills/project-diagrams/scripts/generate_schematic.py \
  "C4 Context diagram: [System Name] in center. \
   Users: [User types]. \
   External systems: [Systems]. \
   Arrows showing relationships." \
  -o diagrams/c4_context.png
```

#### Level 2: Container Diagram

Shows high-level technology choices.

**Include:**
- Applications and services
- Databases and data stores
- Message queues
- Technology choices annotated

```bash
python .claude/skills/project-diagrams/scripts/generate_schematic.py \
  "C4 Container diagram: \
   Web App (React), API (Node.js), Database (PostgreSQL). \
   Show communication protocols between containers." \
  -o diagrams/c4_container.png
```

#### Level 3: Component Diagram

Shows components within a container.

**Include:**
- Major components/modules
- Their responsibilities
- Dependencies between components

#### Level 4: Code (Optional)

UML class diagrams or code structure for complex components.

## Research Output Templates

### Technology Research Report

```markdown
# Technology Research: [Category]

## Executive Summary
[2-3 sentence summary of recommendation]

## Requirements Addressed
- [Requirement 1]
- [Requirement 2]

## Options Evaluated

### Option 1: [Name]
**Overview:** [Brief description]
**Fit Score:** [X/10]

**Strengths:**
- [Strength 1]
- [Strength 2]

**Weaknesses:**
- [Weakness 1]
- [Weakness 2]

**Evidence:**
- [Source 1]: [Finding]
- [Source 2]: [Finding]

**Cost Estimate:** [Monthly/Annual]

[Repeat for each option]

## Comparison Matrix

| Criterion | Weight | Option 1 | Option 2 | Option 3 |
|-----------|--------|----------|----------|----------|
| Performance | 25% | | | |
| Scalability | 20% | | | |
| Cost | 20% | | | |
| Team Fit | 15% | | | |
| Ecosystem | 10% | | | |
| Risk | 10% | | | |
| **Total** | 100% | | | |

## Recommendation
[Recommended option with justification]

## References
1. [Source 1]
2. [Source 2]
```

### Architecture Overview Document

```markdown
# Architecture Overview: [Project Name]

## System Context
[C4 Context diagram]
[Description of system boundaries and external dependencies]

## High-Level Architecture
[C4 Container diagram]
[Description of major components and technology choices]

## Key Architecture Decisions

| Decision | ADR | Status |
|----------|-----|--------|
| Database Selection | ADR-001 | Accepted |
| Authentication | ADR-002 | Accepted |
| Deployment Platform | ADR-003 | Proposed |

## Quality Attributes

### Performance
- Target: [Metrics]
- Approach: [Strategy]

### Scalability
- Target: [Metrics]
- Approach: [Strategy]

### Security
- Requirements: [List]
- Approach: [Strategy]

## Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Frontend | | |
| API | | |
| Database | | |
| Cache | | |
| Queue | | |
| Infrastructure | | |

## Integration Points

| System | Integration Type | Protocol | Notes |
|--------|-----------------|----------|-------|
| | | | |

## References
- [Link to detailed ADRs]
- [Link to C4 diagrams]
```

## Research Best Practices

### Do's
- Use `research-lookup` for every major decision
- Cite real sources, not assumptions
- Include both pros and cons for all options
- Consider total cost of ownership, not just licensing
- Document decisions as ADRs immediately
- Generate diagrams for visual communication

### Don'ts
- Don't make technology choices based on hype
- Don't ignore team skill gaps
- Don't assume "industry standard" without verification
- Don't skip documenting rejected options
- Don't make permanent decisions with temporary data

## Final Checklist

Before completing architecture research:

- [ ] All major technology areas researched
- [ ] At least 3 options evaluated per decision
- [ ] Real sources cited for all recommendations
- [ ] ADRs created for all significant decisions
- [ ] C4 diagrams generated for system overview
- [ ] Trade-offs explicitly documented
- [ ] Costs estimated with sources
- [ ] Team skill gaps identified
- [ ] Risks documented with mitigations
