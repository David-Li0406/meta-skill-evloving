---
name: analogical-transfer
description: Cross-domain reasoning for novel problems through structured analogy. Use when facing unprecedented problems where the best approach is finding similar solved problems in other domains. Unlike BoT (explores options), AT finds parallels. Example: "Design a new marketplace" → What can we learn from malls, stock exchanges, auctions, dating apps?
license: MIT
---

# Analogical Transfer (AT)

**Purpose**: Solve novel problems by finding structural parallels in domains where solutions exist. AT leverages the insight that many "new" problems have been solved before—just in different contexts.

## When to Use Analogical Transfer

**✅ Use AT when:**
- Problem is genuinely novel (no direct precedent)
- Domain knowledge is limited
- Looking for creative/non-obvious solutions
- Need to explain complex concepts simply
- Cross-pollination might yield insights

**❌ Don't use AT when:**
- Direct solutions exist in the same domain (just research)
- Problem is well-defined with known solution space (use ToT)
- Analogy might mislead more than illuminate
- Precision matters more than insight

**Examples:**
- "How should we design our API rate limiting?" ✅ (learn from traffic engineering, nightclub bouncers, utility pricing)
- "How to structure our startup equity?" ✅ (learn from partnerships, marriage, sports teams)
- "Which database for our use case?" ❌ (direct comparisons exist)

---

## Core Methodology: BRIDGE Framework

### B - Base Problem Articulation

**Goal**: Describe the problem in abstract, domain-neutral terms

**Process:**
1. State the concrete problem
2. Extract abstract structure (entities, relationships, constraints, goals)
3. Remove domain-specific jargon
4. Identify the core challenge in universal terms

**Template:**
```markdown
## Base Problem

### Concrete Statement
[The specific problem in your domain]

### Abstract Structure
- **Entities**: [What things are involved?]
- **Relationships**: [How do entities interact?]
- **Constraints**: [What limits exist?]
- **Goals**: [What outcome is desired?]
- **Tensions**: [What trade-offs are inherent?]

### Core Challenge (Domain-Neutral)
[The fundamental problem in universal terms]
```

**Example:**
```markdown
## Base Problem: API Rate Limiting

### Concrete Statement
Prevent API abuse while maintaining good user experience

### Abstract Structure
- **Entities**: Requesters (good, bad), Resource (finite capacity), Gatekeeper
- **Relationships**: Requesters compete for resource access
- **Constraints**: Resource capacity is limited; can't perfectly distinguish good/bad
- **Goals**: Maximize good access, minimize bad access
- **Tensions**: Strictness (blocks abuse) vs Permissiveness (allows legitimate use)

### Core Challenge (Domain-Neutral)
"How to allocate limited shared resources fairly while preventing abuse"
```

---

### R - Retrieve Analogous Domains

**Goal**: Identify domains that face structurally similar challenges

**Domains to Consider:**

| Category | Example Domains |
|----------|-----------------|
| **Nature** | Ecosystems, evolution, immune systems, swarms |
| **Physical Systems** | Traffic, fluid dynamics, thermodynamics, circuits |
| **Economics** | Markets, auctions, pricing, game theory |
| **Social Systems** | Organizations, governments, communities, families |
| **Games** | Board games, sports, gambling, video games |
| **Architecture** | Buildings, cities, transportation networks |
| **Biology** | Cells, organs, nervous systems, growth patterns |
| **History** | Wars, empires, revolutions, technological transitions |
| **Art/Design** | Music, visual arts, fashion, user experience |

**Process:**
1. For each category, ask: "Does this domain face my Core Challenge?"
2. Generate 5-10 candidate analogies
3. Don't filter yet—quantity over quality initially

**Template:**
```markdown
## Candidate Analogies

| Domain | How It Faces Similar Challenge |
|--------|-------------------------------|
| [Domain 1] | [Connection to core challenge] |
| [Domain 2] | [Connection to core challenge] |
...
```

---

### I - Investigate Analogies Deeply

**Goal**: Explore top 3-5 analogies for transferable insights

**For each promising analogy:**

```markdown
## Analogy: [Source Domain → Target Problem]

### Structural Mapping
| Target Element | Source Element |
|----------------|----------------|
| [Your entity 1] | [Their entity 1] |
| [Your entity 2] | [Their entity 2] |
| [Your relationship] | [Their relationship] |
| [Your constraint] | [Their constraint] |

### How Source Domain Solves It
[Description of solution in source domain]

### Key Mechanisms
1. [Mechanism 1 that makes it work]
2. [Mechanism 2 that makes it work]
3. [Mechanism 3 that makes it work]

### Why It Works in Source Domain
[Underlying principles/conditions]

### Mapping Confidence
- **Strong Parallels**: [Elements that map cleanly]
- **Weak Parallels**: [Elements that don't map well]
- **Unmapped Elements**: [Things in your problem with no analogue]
```

---

### D - Distill Transferable Principles

**Goal**: Extract abstract principles that might transfer

**Process:**
1. Identify what makes each source solution work
2. Abstract to domain-independent principles
3. Check if principles could apply to target domain
4. Note conditions under which principles apply

**Template:**
```markdown
## Transferable Principles

### From [Analogy 1]:
- **Principle**: [Abstract statement]
- **Mechanism**: [Why it works]
- **Transfer Conditions**: [When this applies to target]
- **Transfer Risks**: [How this might fail in target]

### From [Analogy 2]:
...
```

**Example Principles:**
- "Fairness through randomization" (from lotteries → load balancing)
- "Reputation as access control" (from communities → API quotas)
- "Surge pricing to shift demand" (from electricity → rate limiting)

---

### G - Generate Candidate Solutions

**Goal**: Apply transferred principles to generate solutions

**Process:**
1. For each transferable principle, generate concrete implementation
2. Combine principles where compatible
3. Adapt to target domain constraints
4. Don't evaluate yet—generate multiple options

**Template:**
```markdown
## Candidate Solutions

### Solution 1: [Name] (from [Analogy])
- **Principle Applied**: [Which transferable principle]
- **Implementation**: [How it would work in target domain]
- **Adaptation Required**: [What needed to change from source]

### Solution 2: [Name] (combining [Analogy A] + [Analogy B])
...
```

---

### E - Evaluate and Adapt

**Goal**: Assess fit and refine solutions for target domain

**Evaluation Criteria:**

| Criterion | Question |
|-----------|----------|
| **Structural Fit** | Does the solution address the core challenge? |
| **Constraint Compatibility** | Does it work within target domain constraints? |
| **Side Effects** | What unintended consequences might occur? |
| **Implementation** | Is it practical to implement? |
| **Cultural Fit** | Will it be accepted by stakeholders? |

**Disanalogy Check:**
For each solution, explicitly list:
- "This analogy breaks down because..."
- "The target domain is different in that..."
- "This solution might fail if..."

**Template:**
```markdown
## Solution Evaluation

### Solution 1: [Name]

**Structural Fit**: [High/Medium/Low] - [Justification]
**Constraint Compatibility**: [High/Medium/Low] - [Justification]
**Side Effects**: [Known risks and unintended consequences]
**Implementation**: [Practical considerations]
**Cultural Fit**: [Stakeholder acceptance likelihood]

**Disanalogies**:
- [Where the analogy breaks down]
- [Target-specific complications]

**Adaptation Required**:
- [Modifications needed for target context]

**Overall Recommendation**: [Pursue / Modify / Reject]
```

---

## Analogy Quality Heuristics

**Strong Analogies:**
- Deep structural parallel (not just surface similarity)
- Source domain is well-understood with proven solutions
- Mapping is consistent across multiple elements
- Source solution has known failure modes (so we can avoid them)

**Weak Analogies:**
- Surface similarity only (metaphor without structure)
- Source domain is poorly understood
- Mapping is inconsistent or cherry-picked
- "It's like X" but no deeper mechanism

**Dangerous Analogies:**
- Analogy that feels compelling but misleads
- Source domain has fundamentally different dynamics
- The unmapped elements are the important ones

---

## Example: Designing a Developer Platform

### Base Problem
"How to build a platform that external developers want to build on"

### Abstract Structure
- **Entities**: Platform, developers, end users, APIs, apps
- **Constraints**: Must be stable, must evolve, must be secure
- **Core Challenge**: "How to grow an ecosystem where many independent actors thrive"

### Retrieved Analogies
1. Shopping mall (landlord-tenant-shopper)
2. Operating system (platform-app developer-user)
3. Coral reef (substrate-species-ecosystem)
4. City (infrastructure-businesses-citizens)
5. Language (grammar-speakers-communication)

### Deep Investigation: City Analogy

**Structural Mapping:**
| Platform | City |
|----------|------|
| APIs | Infrastructure (roads, utilities) |
| Developers | Businesses |
| End Users | Citizens |
| Documentation | Zoning/maps |
| Rate limits | Traffic laws |

**How Cities Solve It:**
- Stable infrastructure that changes slowly
- Zoning for different types of activity
- Public goods everyone can use
- Private spaces for innovation
- Gradual evolution, not revolution

**Transferable Principles:**
1. "Infrastructure stability enables innovation above it"
2. "Zoning provides predictability without micromanagement"
3. "Public goods create network effects"

### Generated Solution
"API Zoning" - Categorize APIs into stability tiers:
- **Core Infrastructure** (roads): Never changes, 10-year stability commitment
- **Commercial District** (zoned): 2-year deprecation policy, predictable change
- **Innovation Zone** (experimental): Explicit instability, rapid iteration OK

---

## Common Mistakes

1. **Surface Analogy**: "It's like Uber for X" without structural depth
   - Fix: Require structural mapping table

2. **Single Analogy**: Latching onto first promising parallel
   - Fix: Generate 5+ candidates, investigate top 3

3. **Analogy Worship**: Ignoring where analogy breaks down
   - Fix: Explicit disanalogy check for every solution

4. **Domain Confusion**: Using source domain jargon in target
   - Fix: Translate principles to target domain language

5. **Selective Mapping**: Cherry-picking elements that fit
   - Fix: Map ALL elements, note gaps explicitly

---

## Integration with Other Patterns

**When to enter AT**: When BoT yields no good options (solution space seems empty)

**AT → ToT**: After AT generates solutions, use ToT to evaluate and select

**AT → DR**: If AT reveals two analogies suggesting opposite approaches, use DR

**AT → AR**: Use adversarial reasoning to attack analogy-derived solutions

---

## Output Template

```markdown
# Analogical Analysis: [Problem]

## Problem Abstraction
[Domain-neutral core challenge]

## Analogies Investigated
1. [Analogy 1] - [Key insight]
2. [Analogy 2] - [Key insight]
3. [Analogy 3] - [Key insight]

## Transferable Principles
- [Principle 1 with conditions]
- [Principle 2 with conditions]

## Proposed Solutions
1. [Solution from analogy 1]
2. [Combined solution]

## Disanalogies and Risks
- [Where analogies break down]
- [Target-specific complications]

## Recommendation
[Best solution with adaptation notes]

## Confidence: [X]%
[Based on analogy strength and mapping completeness]
```
