---
name: ultrathink
description: Ultra-deep multi-perspective analysis for complex architectural and strategic decisions requiring systematic reasoning across technical, business, user, and system perspectives
license: MIT
compatibility:
  - runtime:any
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
metadata:
  author: thoreinstein
  version: 1.0.0
---

# Ultrathink

Ultra-deep multi-perspective analysis for complex architectural and strategic decisions. Use this mode for problems requiring comprehensive, systematic reasoning.

## When to Use

- Complex architectural decisions (monolith vs microservices, technology stack choices)
- Strategic planning with multiple stakeholders and constraints
- Problems requiring multi-dimensional trade-off analysis
- Decisions with long-term implications and high cost of reversal
- Situations where conventional thinking has failed

## Instructions

### 1. Initialize Ultra Think Mode

- Acknowledge the request for enhanced analytical thinking
- Set context for deep, systematic reasoning
- Prepare to explore the problem space comprehensively

### 2. Parse the Problem

- Extract the core challenge from the input
- Identify all stakeholders and constraints
- Recognize implicit requirements and hidden complexities
- Question assumptions and surface unknowns

### 3. Multi-Dimensional Analysis

Approach the problem from multiple angles:

**Technical Perspective**
- Analyze technical feasibility and constraints
- Consider scalability, performance, and maintainability
- Evaluate security implications
- Assess technical debt and future-proofing

**Business Perspective**
- Understand business value and ROI
- Consider time-to-market pressures
- Evaluate competitive advantages
- Assess risk vs. reward trade-offs

**User Perspective**
- Analyze user needs and pain points
- Consider usability and accessibility
- Evaluate user experience implications
- Think about edge cases and user journeys

**System Perspective**
- Consider system-wide impacts
- Analyze integration points
- Evaluate dependencies and coupling
- Think about emergent behaviors

### 4. Generate Multiple Solutions

- Brainstorm at least 3-5 different approaches
- For each approach, consider:
  - Pros and cons
  - Implementation complexity
  - Resource requirements
  - Potential risks
  - Long-term implications
- Include both conventional and creative solutions
- Consider hybrid approaches

### 5. Deep Dive Analysis

For the most promising solutions:
- Create detailed implementation plans
- Identify potential pitfalls and mitigation strategies
- Consider phased approaches and MVPs
- Analyze second and third-order effects
- Think through failure modes and recovery

### 6. Cross-Domain Thinking

- Draw parallels from other industries or domains
- Apply design patterns from different contexts
- Consider biological or natural system analogies
- Look for innovative combinations of existing solutions

### 7. Challenge and Refine

- Play devil's advocate with each solution
- Identify weaknesses and blind spots
- Consider "what if" scenarios
- Stress-test assumptions
- Look for unintended consequences

### 8. Synthesize Insights

- Combine insights from all perspectives
- Identify key decision factors
- Highlight critical trade-offs
- Summarize innovative discoveries
- Present a nuanced view of the problem space

### 9. Provide Structured Recommendations

Present findings clearly:

```
## Problem Analysis
- Core challenge
- Key constraints
- Critical success factors

## Solution Options
### Option 1: [Name]
- Description
- Pros/Cons
- Implementation approach
- Risk assessment

### Option 2: [Name]
[Similar structure]

## Recommendation
- Recommended approach
- Rationale
- Implementation roadmap
- Success metrics
- Risk mitigation plan

## Alternative Perspectives
- Contrarian view
- Future considerations
- Areas for further research
```

### 10. Meta-Analysis

- Reflect on the thinking process itself
- Identify areas of uncertainty
- Acknowledge biases or limitations
- Suggest additional expertise needed
- Provide confidence levels for recommendations

## Key Principles

| Principle | Description |
|-----------|-------------|
| First Principles | Break down to fundamental truths |
| Systems Thinking | Consider interconnections and feedback loops |
| Probabilistic Thinking | Work with uncertainties and ranges |
| Inversion | Consider what to avoid, not just what to do |
| Second-Order Thinking | Consider consequences of consequences |

## Output

Use the template at `references/templates/thinking-session.md` to document the analysis.

### Output Expectations

- Comprehensive analysis (typically 2-4 pages of insights)
- Multiple viable solutions with trade-offs
- Clear reasoning chains
- Acknowledgment of uncertainties
- Actionable recommendations
- Novel insights or perspectives

## Constraints

- **Depth over speed**: Take time to explore thoroughly
- **Multiple perspectives**: Never analyze from only one angle
- **Acknowledge uncertainty**: Be explicit about confidence levels
- **Actionable output**: End with concrete recommendations
- **Challenge assumptions**: Question the problem framing itself

## Example

```
Input: "Should we migrate to microservices or improve our monolith?"

Problem Understanding:
- Core challenge: Scaling development velocity and system performance
- Constraints: 12-person team, 3-month runway, existing monolith is 4 years old
- Success criteria: 2x deployment frequency, <100ms p99 latency
- Risk of wrong decision: 6+ months wasted effort, team morale impact

Multi-Dimensional Analysis:

Technical Perspective:
- Monolith: Simple deployment, shared database, tight coupling
- Microservices: Independent scaling, complexity overhead, network latency

Business Perspective:
- Time-to-market pressure favors incremental improvement
- Team size insufficient for full microservices adoption
- Competitive pressure moderate (6-month window)

System Perspective:
- Current pain points: deployment conflicts, test suite speed
- Integration points: 3 external APIs, 2 internal services
- Database: single PostgreSQL, becoming bottleneck

Solutions Generated:
1. Full microservices migration
2. Modular monolith (strangler pattern)
3. Selective extraction (2-3 bounded contexts)
4. Performance optimization of current monolith
5. Hybrid: Extract one service + optimize monolith

Recommendation: Option 5 (Hybrid approach)
- Extract authentication service (clear boundary, high value)
- Optimize monolith database queries (quick wins)
- Establish service communication patterns for future extraction
- Rationale: De-risks microservices, delivers value incrementally
- Timeline: 2 months for auth service, ongoing optimization
- Success metrics: 50% reduction in deployment conflicts

Open Questions:
- [ ] Team microservices experience level?
- [ ] Kubernetes/container infrastructure ready?
- [ ] Monitoring/observability maturity?
```

Begin by restating the problem and identifying all stakeholders and constraints.
