---
name: implementation-strategy-selection
description: Use this skill when planning an implementation strategy, selecting a development approach, or defining verification criteria for a project.
---

# Implementation Strategy Selection Framework (Meta-cognitive Approach)

## Meta-cognitive Strategy Selection Process

### Phase 1: Comprehensive Current State Analysis

**Core Question**: "What does the existing implementation look like?"

#### Analysis Framework
```yaml
Architecture Analysis: Responsibility separation, data flow, dependencies, technical debt
Implementation Quality Assessment: Code quality, test coverage, performance, security
Historical Context Understanding: Current form rationale, past decision validity, constraint changes, requirement evolution
```

#### Meta-cognitive Question List
- What is the true responsibility of this implementation?
- Which parts are business essence and which derive from technical constraints?
- What dependencies or implicit preconditions are unclear from the code?
- What benefits and constraints does the current design bring?

### Phase 2: Strategy Exploration and Creation

**Core Question**: "When determining before → after, what implementation patterns or strategies should be referenced?"

#### Strategy Discovery Process
```yaml
Research and Exploration: Tech stack examples (WebSearch), similar projects, OSS references, literature/blogs
Creative Thinking: Strategy combinations, constraint-based design, phase division, extension point design
```

#### Reference Strategy Patterns (Creative Combinations Encouraged)

**Legacy Handling Strategies**:
- Strangler Pattern: Gradual migration through phased replacement
- Facade Pattern: Complexity hiding through unified interface
- Adapter Pattern: Bridge with existing systems

**New Development Strategies**:
- Feature-driven Development: Vertical implementation prioritizing user value
- Foundation-driven Development: Foundation-first construction prioritizing stability
- Risk-driven Development: Prioritize addressing maximum risk elements

**Integration/Migration Strategies**:
- Proxy Pattern: Transparent feature extension
- Decorator Pattern: Phased enhancement of existing features
- Bridge Pattern: Flexibility through abstraction

### Phase 3: Risk Assessment and Consideration

**Core Question**: "What risks are associated with the selected strategies?"

#### Risk Assessment Process
- Identify potential risks related to the chosen implementation strategies.
- Evaluate the impact and likelihood of each risk.
- Develop mitigation strategies for high-priority risks.

**Important**: The optimal solution is discovered through creative thinking according to each project's context.