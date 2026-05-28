---
name: structured-debate-workflow
description: Use this skill for structured multi-perspective debates on architectural decisions and complex trade-offs where multiple valid approaches exist.
---

# Structured Debate Workflow Skill

## Purpose

Implement structured multi-perspective debate for important architectural decisions, design trade-offs, and complex problems where multiple valid approaches exist.

## When to Use This Skill

**USE FOR:**
- Major architectural decisions (framework selection, system design)
- Complex trade-offs with no clear winner
- Controversial changes affecting multiple teams
- High-impact decisions requiring buy-in
- When perspectives genuinely conflict

**AVOID FOR:**
- Simple implementation choices
- Decisions with obvious correct answers
- Time-sensitive hot fixes
- Minor refactoring
- Routine feature additions

## Configuration

### Core Parameters

**Number of Perspectives:**
- `3` - Default (security, performance, simplicity)
- `5` - Extended (add: maintainability, user experience)
- `7` - Comprehensive (add: scalability, cost)

**Debate Rounds:**
- `2` - Quick (position + challenge)
- `3` - Standard (position + challenge + synthesis)
- `4-5` - Deep (multiple challenge/response cycles)

**Convergence Criteria:**
- `100%` - Strong consensus (all perspectives agree)
- `2/3` - Majority rule (two-thirds agreement)
- `synthesis` - Facilitator synthesizes best hybrid
- `evidence` - Follow strongest evidence/arguments

## Standard Perspective Profiles

**Security Perspective:**
- Focus: Vulnerabilities, attack vectors, data protection
- Questions: "What could go wrong? How do we prevent breaches?"

**Performance Perspective:**
- Focus: Speed, scalability, resource efficiency
- Questions: "Will this scale? What are the bottlenecks?"

**Simplicity Perspective:**
- Focus: Minimal complexity, ruthless simplification
- Questions: "Is this the simplest solution? Can we remove abstractions?"

**Maintainability Perspective:**
- Focus: Long-term evolution, technical debt
- Questions: "Can future developers understand this? How hard to change?"

**User Experience Perspective:**
- Focus: API design, usability, developer experience
- Questions: "Is this intuitive? How will users interact with this?"

**Scalability Perspective:**
- Focus: Growth capacity, distributed systems
- Questions: "What happens at 10x load? 100x?"

**Cost Perspective:**
- Focus: Resource usage, infrastructure costs, development time
- Questions: "What's the ROI? Are we over-engineering?"

## Execution Process

### Step 1: Frame the Decision

- **Use ambiguity agent** to clarify the decision to be made
- **Use prompt-writer agent** to create clear decision prompt
- Define decision scope and constraints
- Identify stakeholder concerns
- List evaluation criteria
- Document explicit user requirements that constrain options
- **CRITICAL: Frame decision as question, not predetermined answer**

**Decision Framing Template:**
```markdown
# Decision: [Brief Title]

## Question
[One-sentence question to be debated]

## Context
[Why this decision matters, background information]

## Constraints
[Non-negotiable requirements, technical limitations]

## Evaluation Criteria
[How we'll judge proposed solutions]

## Perspectives to Include
[Which viewpoints are most relevant]
```

### Step 2: Initialize Perspectives

- Select N perspectives relevant to decision
- **Spawn subprocess for each perspective**
- Each subprocess receives decision framing doc
- Each subprocess assigned perspective profile
- **No context sharing between perspectives yet**
- Each forms initial position independently

**Initial Position Requirements:**
- State recommended approach
- Provide 3-5 supporting arguments
- Identify risks of alternative approaches
- Quantify claims where possible

### Step 3: Debate Round 1 - Initial Positions

- Collect initial positions from all perspectives
- **Use analyzer agent** to synthesize positions
- Document each perspective's recommendation
- Identify areas of agreement
- Identify areas of conflict
- Surface assumptions made by each perspective

### Step 4: Debate Round 2 - Challenge and Respond

- Share all Round 1 positions with all perspectives
- Each perspective challenges other perspectives' arguments
- Each perspective defends their position against challenges
- **Use analyzer agent** to track argument strength
- Identify which arguments withstand scrutiny
- Document concessions and refinements

### Step 5: Debate Round 3 - Find Common Ground

- Identify points of consensus across perspectives
- Surface remaining disagreements explicitly
- Explore hybrid approaches combining insights
- **Use architect agent** to design synthesis options
- Validate hybrid approaches against all perspectives
- Document convergence or divergence

### Step 6: Facilitator Synthesis

- **Use architect agent** as neutral facilitator
- **Use analyzer agent** to evaluate all arguments
- Review all debate rounds systematically
- Identify strongest evidence-based arguments
- Make recommendation with confidence level
- Document decision rationale thoroughly
- Include dissenting views explicitly

### Step 7: Decision Documentation

- Create decision record: `decisions/YYYY-MM-DD-decision-name.md`
- Document full debate transcript
- Include all perspective arguments
- Record synthesis and final decision

### Step 8: Implement Decision

- **Use builder agent** to implement chosen approach
- Follow the decided path from synthesis
- Implement monitoring for success metrics
- Set up alerts for revisit triggers
- Document decision in code comments
- Create runbook if operational complexity added

## Trade-Offs

**Cost:** Multiple agent cycles, longer decision time  
**Benefit:** Well-reasoned decisions, surface hidden risks  
**Best For:** Decisions that are expensive to reverse

## Examples

### Example 1: API Design - REST vs GraphQL

**Configuration:**
- Perspectives: 5 (Simplicity, Performance, User Experience, Maintainability, Cost)
- Rounds: 3
- Convergence: Synthesis

### Example 2: Testing Strategy - Unit vs Integration Heavy

**Configuration:**
- Perspectives: 3 (Simplicity, Maintainability, Performance)
- Rounds: 2
- Convergence: 2/3 majority

### Example 3: Deployment Strategy - Kubernetes vs Serverless

**Configuration:**
- Perspectives: 5 (Cost, Simplicity, Scalability, Performance, Maintainability)
- Rounds: 4
- Convergence: Synthesis (no majority)

## Philosophy Alignment

This workflow enforces:
- **Perspective Diversity:** Multiple viewpoints surface hidden trade-offs
- **Evidence-Based:** Arguments must be supported, not just opinions
- **Transparent Trade-offs:** Dissent is documented, not hidden
- **Structured Exploration:** Debate format prevents premature convergence
- **Decision Quality:** Better decisions through rigorous analysis
- **Learning:** Debate transcripts become organizational knowledge

## Integration with Default Workflow

This workflow replaces Step 4 (Research and Design) of the DEFAULT_WORKFLOW when complex decisions require multi-perspective analysis. Implementation (Step 5) proceeds with the consensus decision.