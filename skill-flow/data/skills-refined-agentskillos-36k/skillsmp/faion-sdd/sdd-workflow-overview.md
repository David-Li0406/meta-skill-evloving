---
id: sdd-workflow-overview
name: "SDD Workflow Overview"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# SDD Workflow Overview

## Metadata

| Field | Value |
|-------|-------|
| **ID** | sdd-workflow-overview |
| **Category** | SDD Foundation |
| **Difficulty** | Beginner |
| **Tags** | #methodology, #sdd, #workflow |
| **Domain Skill** | faion-sdd |
| **Agents** | faion-task-executor-agent |

---

## Problem

Developers and solopreneurs often start coding immediately without proper planning. This leads to:
- Scope creep and endless feature additions
- Technical debt from poor architecture decisions
- Wasted time building the wrong thing
- Difficulty explaining what you're building to others

**The root cause:** No structured process between idea and code.

---

## Framework

### What is SDD?

Specification-Driven Development (SDD) is a methodology where you write documentation before code. Think of it like an architect drawing blueprints before construction.

### The SDD Workflow

```
IDEA → VALIDATION → SPECIFICATION → DESIGN → IMPLEMENTATION → LAUNCH
  ↓         ↓            ↓            ↓           ↓             ↓
niche    problem       spec.md    design.md    tasks        monetize
research  evidence     (what)      (how)       (execute)    (grow)
```

### Six Phases Explained

#### Phase 1: Idea
- Generate ideas using proven frameworks (see idea-generation)
- Score ideas on market size, competition, personal fit
- **Output:** 3-5 candidate ideas ranked

#### Phase 2: Validation
- Test if real people have this problem
- Collect evidence: interviews, surveys, existing solutions
- **Output:** Validation report with go/no-go decision

#### Phase 3: Specification
- Define WHAT you're building (not HOW)
- Write functional requirements (FR-X)
- Define acceptance criteria
- **Output:** spec.md file

#### Phase 4: Design
- Define HOW you'll build it
- Architecture decisions (AD-X)
- File structure, API contracts
- **Output:** design.md file

#### Phase 5: Implementation
- Break design into tasks
- Execute tasks with quality gates
- Test as you go
- **Output:** Working code, tests

#### Phase 6: Launch
- Deploy to production
- Monitor metrics
- Iterate based on feedback
- **Output:** Live product, growth

### Time Allocation

| Phase | Solo Project | Team Project |
|-------|-------------|--------------|
| Idea + Validation | 20% | 15% |
| Specification | 15% | 20% |
| Design | 15% | 20% |
| Implementation | 40% | 35% |
| Launch + Iterate | 10% | 10% |

---

## Templates

### SDD Project Structure

```
project/
├── docs/
│   ├── spec.md           # What to build
│   ├── design.md         # How to build
│   ├── implementation-plan.md
│   └── tasks/
│       ├── todo/
│       ├── in_progress/
│       └── done/
├── src/                  # Code
└── tests/                # Tests
```

### Phase Checklist

```markdown
## SDD Checklist

### Idea Phase
- [ ] Generated 5+ ideas using frameworks
- [ ] Scored each on 5 criteria
- [ ] Selected top 1-2 for validation

### Validation Phase
- [ ] Defined target customer clearly
- [ ] Conducted 5+ interviews or surveys
- [ ] Found existing solutions and gaps
- [ ] Made go/no-go decision with evidence

### Specification Phase
- [ ] Written problem statement
- [ ] Defined user personas
- [ ] Listed all functional requirements
- [ ] Defined acceptance criteria
- [ ] Scoped MVP/MLP

### Design Phase
- [ ] Chose technology stack
- [ ] Made architecture decisions
- [ ] Defined file structure
- [ ] Specified API contracts (if applicable)
- [ ] Identified dependencies

### Implementation Phase
- [ ] Created task breakdown
- [ ] Parallelized independent tasks
- [ ] Passed quality gates
- [ ] Written tests

### Launch Phase
- [ ] Deployed to production
- [ ] Set up monitoring
- [ ] Defined success metrics
- [ ] Created feedback loop
```

---

## Examples

### Example: Building a SaaS Tool

**Bad approach (no SDD):**
1. "I'll build a project management tool"
2. Starts coding immediately
3. 3 months later: bloated app nobody wants

**Good approach (with SDD):**
1. **Idea:** "Project management for solo freelancers"
2. **Validation:** Interview 10 freelancers, find they hate complex tools
3. **Spec:** "Simple task list with time tracking, max 5 features"
4. **Design:** "Next.js + Supabase, deploy on Vercel"
5. **Implementation:** 2 weeks, 10 tasks
6. **Launch:** Beta with 20 users, iterate

**Result:** Focused product, faster delivery, real users.

### Example: SDD for Content Product

**Idea:** "Course on prompt engineering"
**Validation:**
- 50 Reddit comments asking how to write prompts
- No comprehensive guide exists
- Competitors charge $200+

**Spec highlights:**
- FR-1: Course has 10 modules
- FR-2: Each module has video + text
- FR-3: Includes 50 prompt templates
- FR-4: Pricing at $49 (undercut market)

**Design highlights:**
- AD-1: Host on Teachable (no custom code)
- AD-2: Write content in Notion first
- AD-3: Record with Loom

**Implementation:** 4 weeks, methodical execution
**Launch:** $5K first month

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Skipping validation | "I know users want this" → Always validate with evidence |
| Over-engineering spec | Keep spec simple, focus on MVP |
| Designing too early | Don't choose tech stack before understanding problem |
| Coding without tasks | Break design into explicit, small tasks |
| Launching without metrics | Define success criteria before launch |

---

## Related Methodologies

- **writing-specifications:** Writing Specifications
- **writing-design-documents:** Writing Design Documents
- **writing-implementation-plans:** Writing Implementation Plans
- **task-creation-parallelization:** Task Creation & Parallelization
- **idea-generation:** Idea Generation

---

## Agent

**faion-task-executor-agent** orchestrates the SDD workflow. Invoke with:
- "Start SDD workflow for [project idea]"
- "Guide me through specification phase"
- "Create tasks from design document"

---

*Methodology | SDD Foundation | Version 1.0*
