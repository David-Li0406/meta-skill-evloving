---
id: mvp-scoping
name: "MVP Scoping"
domain: PRD
skill: faion-product-manager
category: "product"
---

# MVP Scoping

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Beginner |
| **Tags** | #product, #mvp, #scoping |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-mvp-scope-analyzer-agent |

---

## Problem

Founders build too much for first versions or too little to be useful. Common issues:
- "MVP" that takes 6 months and has 50 features
- Product too minimal to deliver value
- No clear criteria for what's "in" or "out"
- Perfectionism blocking launch

**The root cause:** No framework for determining the right scope.

---

## Framework

### What is MVP?

Minimum Viable Product is the smallest version that:
1. Solves the core problem
2. Delivers value to early adopters
3. Allows you to learn and iterate

**Key insight:** MVP is about learning, not launching a polished product.

### MVP vs MLP

| Concept | Focus | Purpose |
|---------|-------|---------|
| MVP | Minimum viable | Validate hypothesis |
| MLP (Minimum Lovable) | Minimum delightful | Retain early users |

**Rule:** Start with MVP to validate, evolve to MLP for retention.

### MVP Scoping Process

#### Step 1: Define the Core Problem

**Template:**
```
For [target user]
Who [has this problem]
Our MVP will prove that [hypothesis]
By delivering [core outcome]
In [timeframe] with [constraints]
```

**Example:**
```
For freelance designers
Who struggle to track project time
Our MVP will prove that simple time tracking increases billing accuracy
By delivering automatic time logging with one-click invoice generation
In 4 weeks with one developer
```

#### Step 2: Identify the Core Value

**Questions:**
- What's the ONE thing this must do well?
- What's the minimum for users to get value?
- What can users NOT do without?

**Value test:** If you remove it, is the product useless?

#### Step 3: List All Features

Brain dump everything, then categorize:

| Category | Description | Criteria |
|----------|-------------|----------|
| Core | Essential for value | Product doesn't work without it |
| Important | Significantly improves experience | Users would miss it |
| Nice-to-have | Good but not critical | Users can wait for it |
| Out of scope | Maybe later | Not for this version |

#### Step 4: Apply the MoSCoW Method

| Priority | Definition | % of Scope |
|----------|------------|------------|
| Must Have | Non-negotiable, product fails without | 60% |
| Should Have | Important but has workarounds | 20% |
| Could Have | Nice to have if time permits | 15% |
| Won't Have | Explicitly not in MVP | N/A |

**Constraint:** Total effort for Must + Should should fit in timeline.

#### Step 5: Validate Scope

**Checklist:**
- [ ] Solves core problem end-to-end?
- [ ] First user can complete core job?
- [ ] Value delivered without future features?
- [ ] Buildable in target timeframe?
- [ ] Testable hypothesis?

#### Step 6: Define Done

**MVP completion criteria:**
- Feature list with acceptance criteria
- Definition of "good enough" quality
- What to measure/learn
- Next decision after MVP

---

## Templates

### MVP Scope Document

```markdown
## MVP Scope: [Product Name]

### Problem Statement
For [target user]
Who [problem]
Our MVP proves [hypothesis]
By delivering [outcome]

### Core Value
**Primary job to be done:** [Job]
**Success criteria:** [How we'll measure]

### Feature Scope

#### Must Have (MVP)
| Feature | Description | Effort | Acceptance Criteria |
|---------|-------------|--------|---------------------|
| [Feature] | [Brief] | [Days] | [How to verify] |

#### Should Have (Post-MVP)
| Feature | Description | Why Wait |
|---------|-------------|----------|
| [Feature] | [Brief] | [Reason] |

#### Won't Have (Out of Scope)
| Feature | Reason |
|---------|--------|
| [Feature] | [Why explicitly excluded] |

### Constraints
- **Timeline:** [X] weeks
- **Team:** [Resources available]
- **Tech:** [Stack, limitations]
- **Budget:** [If applicable]

### Non-Functional Requirements
- Performance: [Baseline]
- Security: [Minimum]
- Scalability: [Current needs only]

### Learning Goals
What we want to learn:
1. [Question 1]
2. [Question 2]

How we'll measure:
- [Metric 1]
- [Metric 2]

### Definition of Done
- [ ] All Must Have features complete
- [ ] Core flow works end-to-end
- [ ] [X] users can complete core job
- [ ] Analytics in place for learning goals

### Next Steps After MVP
If validated → [Next action]
If not validated → [Pivot plan]
```

### Quick MVP Validator

```markdown
## MVP Quick Check: [Feature List]

### The 5 Questions

1. **Does it solve ONE problem completely?**
   [ ] Yes [ ] No
   Problem: [State it]

2. **Can user get value TODAY?**
   [ ] Yes [ ] No
   Value: [What they get]

3. **What's the MINIMUM to prove this works?**
   Features needed: [List]

4. **What can wait until v1.1?**
   Deferred: [List]

5. **Can you build this in [X] weeks?**
   [ ] Yes [ ] No - Cut: [What to cut]

### Verdict
[ ] Scope is right
[ ] Too big - Cut these: [X]
[ ] Too small - Add: [X]
```

---

## Examples

### Example 1: Time Tracking App MVP

**Problem:** Freelancers forget to track time, lose billable hours

**Initial feature list (40+ features):**
- Time tracking, projects, clients, invoicing, reports, integrations, mobile app, team features, budgets, etc.

**MVP scope (4 weeks):**

| Must Have | Why |
|-----------|-----|
| Start/stop timer | Core functionality |
| Project selection | Assign time |
| Basic report | See tracked time |
| Simple invoice | Get paid |

**Won't have:**
- Mobile app (use responsive web)
- Team features (solo focus)
- Integrations (manual for now)
- Advanced reports (spreadsheet export)

**Learning goal:** Will users actually track time daily?

### Example 2: Course Platform MVP

**Problem:** Course creators struggle with tech setup

**MVP scope (6 weeks):**

| Must Have | Why |
|-----------|-----|
| Upload video/text lessons | Core content |
| Paywall/payment | Must monetize |
| Student access control | Protect content |
| Basic progress tracking | Show value |

**Won't have:**
- Quizzes (manual feedback)
- Certificates (v2)
- Community features (external Discord)
- Mobile app (responsive web)
- Advanced analytics (basic counts only)

**Learning goal:** Will creators pay $29/month for simplicity?

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too many Must Haves | Max 3-5 core features |
| Perfection paralysis | "Good enough" beats perfect |
| No user value | Ensure complete user flow |
| Building in isolation | Get user feedback weekly |
| Scope creep | Document Won't Have explicitly |
| No learning goals | Define what you'll measure |
| Fake MVP | If it takes 6 months, it's not MVP |

---

## Related Methodologies

- **problem-validation:** Problem Validation
- **jobs-to-be-done:** Jobs to Be Done
- **mlp-planning:** MLP Planning
- **feature-prioritization-rice:** Feature Prioritization (RICE)
- **writing-specifications:** Writing Specifications

---

## Agent

**faion-mvp-scope-analyzer-agent** helps scope MVPs. Invoke with:
- "Help me scope an MVP for [product idea]"
- "Is this MVP scope too big? [feature list]"
- "What's the minimum for [problem]?"
- "Prioritize these features for MVP: [list]"

---

*Methodology | Product | Version 1.0*
