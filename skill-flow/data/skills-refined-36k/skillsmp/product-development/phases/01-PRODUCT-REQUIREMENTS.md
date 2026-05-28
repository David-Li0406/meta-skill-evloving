# Phase 1: Product Requirements

## Objective

Define WHO uses the product, WHAT they expect, and the boundaries of the product.

## Step 1: Identify User Personas

Present each potential user type to the user for validation:

```markdown
### User Persona: [Name]

| Attribute | Description |
|-----------|-------------|
| **Role** | [Job title or function] |
| **Technical Level** | [Novice / Intermediate / Expert] |
| **Primary Goal** | [What they want to achieve] |
| **Pain Points** | [Current frustrations] |
| **Success Metric** | [How they measure success] |

Is this persona accurate? Should we add/remove/modify any personas?
```

### Persona Discovery Questions

Ask the user:
1. Who will use this product directly?
2. Who will be affected by this product indirectly?
3. Who should explicitly NOT use this product?
4. Are there different user segments with different needs?

## Step 2: Write User Stories

For each persona, create user stories:

```markdown
### User Story: [ID]

**As a** [persona]
**I expect to** [action/capability]
**So that** [benefit/outcome]

**Acceptance Criteria**:
- [ ] [Measurable criterion 1]
- [ ] [Measurable criterion 2]
- [ ] [Measurable criterion 3]

**Priority**: [Must Have / Should Have / Nice to Have]
**Complexity**: [Low / Medium / High]
```

### User Story Quality Checklist

Each story must be:
- [ ] **Independent**: Can be implemented separately
- [ ] **Negotiable**: Details can be discussed
- [ ] **Valuable**: Delivers value to user
- [ ] **Estimable**: Can gauge complexity
- [ ] **Small**: Fits in one iteration
- [ ] **Testable**: Clear pass/fail criteria

## Step 3: Define Product Boundaries

Present boundary decisions:

```markdown
### Product Boundary Decision

| In Scope | Out of Scope | Rationale |
|----------|--------------|-----------|
| [Feature A] | [Feature X] | [Why] |
| [Feature B] | [Feature Y] | [Why] |

**Boundary Trade-off**: [What we're giving up and why]
```

### Boundary Questions

1. What is the minimum viable product (MVP)?
2. What features are explicitly deferred to future versions?
3. What integrations are required vs optional?
4. What platforms/environments must be supported?

## Step 4: Establish Constraints

Document all constraints:

```markdown
### Constraint: [Name]

| Type | Description | Impact | Flexibility |
|------|-------------|--------|-------------|
| **Technical** | [e.g., Must use Python 3.10+] | [Impact] | [Fixed/Negotiable] |
| **Business** | [e.g., Must launch by Q2] | [Impact] | [Fixed/Negotiable] |
| **Regulatory** | [e.g., GDPR compliance] | [Impact] | [Fixed/Negotiable] |
| **Resource** | [e.g., 2 developers] | [Impact] | [Fixed/Negotiable] |
```

## Step 5: Critical Reflection

Before seeking approval, ask these reflection questions:

### Completeness Check
- Are all user personas represented?
- Does every persona have at least one user story?
- Are acceptance criteria measurable?

### Conflict Check
- Do any user stories conflict with each other?
- Are there personas with opposing needs?
- How do we resolve conflicts?

### Feasibility Check
- Are expectations realistic given constraints?
- Are there any "impossible" requirements?
- What happens if a constraint changes?

### Edge Case Check
- What happens when the happy path fails?
- How do users recover from errors?
- What are the worst-case scenarios?

## Phase 1 Approval Gate

Present to user:

```markdown
## Phase 1 Summary: Product Requirements

### User Personas Identified: [N]
[List personas with one-line descriptions]

### User Stories Created: [N]
| Priority | Count |
|----------|-------|
| Must Have | [X] |
| Should Have | [Y] |
| Nice to Have | [Z] |

### Key Boundaries
- In Scope: [Summary]
- Out of Scope: [Summary]

### Constraints
[List key constraints]

### Open Questions
[Any unresolved items]

---

**Do you approve Phase 1? Any changes needed before proceeding to Technical Requirements?**
```
