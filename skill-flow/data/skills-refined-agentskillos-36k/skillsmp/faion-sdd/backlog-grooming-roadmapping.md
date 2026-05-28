---
id: backlog-grooming-roadmapping
name: "Backlog Grooming & Roadmapping"
domain: SDD
skill: faion-sdd
category: "sdd"
---

# Backlog Grooming & Roadmapping

## Metadata

| Field | Value |
|-------|-------|
| **ID** | backlog-grooming-roadmapping |
| **Category** | SDD Foundation |
| **Difficulty** | Beginner |
| **Tags** | #methodology, #sdd, #backlog, #roadmap |
| **Domain Skill** | faion-sdd |
| **Agents** | faion-task-executor-agent |

---

## Problem

Projects lose direction when:
- Feature requests pile up without prioritization
- No clear vision of where the product is going
- Teams work on low-impact items while important features wait
- Stakeholders don't know what's coming when

**The root cause:** No systematic backlog management and roadmap planning.

---

## Framework

### Backlog vs Roadmap

| Aspect | Backlog | Roadmap |
|--------|---------|---------|
| **Question** | What could we build? | What will we build when? |
| **Time horizon** | All potential work | Next 3-12 months |
| **Detail level** | Requirements | Themes/milestones |
| **Audience** | Development team | Stakeholders, users |
| **Updates** | Weekly | Monthly/Quarterly |

### Backlog Structure

```
backlog/
├── ideas/          # Raw ideas, not yet validated
├── validated/      # Validated, ready for spec
├── specified/      # Has spec, ready for design
├── designed/       # Has design, ready for implementation
└── ready/          # Implementation-ready with tasks
```

### Backlog Item Lifecycle

```
IDEA → VALIDATE → SPECIFY → DESIGN → READY → IN PROGRESS → DONE
  ↓        ↓         ↓         ↓        ↓
 DROP    DROP     DROP      DROP    DEFER
```

### Grooming Process

#### Weekly Grooming (30-60 min)

1. **Review new ideas** (10 min)
   - Quick assessment: Is this worth exploring?
   - Move to validated or drop

2. **Prioritize backlog** (20 min)
   - Review top 20 items
   - Re-score based on new information
   - Adjust order

3. **Refine upcoming items** (20 min)
   - Add detail to next sprint's items
   - Clarify acceptance criteria
   - Identify dependencies

4. **Cleanup** (10 min)
   - Archive old items
   - Remove duplicates
   - Update estimates

### Prioritization Frameworks

#### RICE Scoring

| Factor | Question | Score |
|--------|----------|-------|
| **R**each | How many users affected? | 1-10 |
| **I**mpact | How much impact per user? | 0.25, 0.5, 1, 2, 3 |
| **C**onfidence | How confident in estimates? | 50%, 80%, 100% |
| **E**ffort | Person-months to complete | 0.5, 1, 2, 3, 6+ |

**RICE Score = (Reach × Impact × Confidence) / Effort**

#### MoSCoW

| Category | Meaning | Rule |
|----------|---------|------|
| **Must** | Critical for release | ~60% of scope |
| **Should** | Important but not critical | ~20% of scope |
| **Could** | Nice to have | ~20% of scope |
| **Won't** | Explicitly not in this release | Document for future |

#### Value vs Effort Matrix

```
HIGH VALUE
    │
    │  Quick Wins    │    Big Bets
    │  (Do first)    │    (Plan carefully)
    │────────────────┼────────────────
    │  Fill-ins      │    Money Pits
    │  (Do if time)  │    (Avoid)
    │
    └─────────────────────────────────→ HIGH EFFORT
```

### Roadmap Structure

#### Time-Based Roadmap

```
Q1 2026              Q2 2026              Q3 2026
────────────────────────────────────────────────────
[  Auth System  ]    [  Paywall   ]      [ AI Agents ]
[Landing Page]       [Content CMS]       [Mobile App]
                     [ Localization ]    [Analytics]
```

#### Theme-Based Roadmap

```
Theme: User Acquisition
├── Landing page (Q1)
├── SEO optimization (Q1-Q2)
├── Social proof (Q2)
└── Referral program (Q3)

Theme: Monetization
├── Stripe integration (Q1)
├── Subscription tiers (Q2)
├── Annual pricing (Q2)
└── Enterprise tier (Q3)
```

---

## Templates

### Backlog Item Template

```markdown
# BACKLOG: [Item Title]

**ID:** BL-XXX
**Status:** Idea | Validated | Specified | Designed | Ready
**Priority:** P0 | P1 | P2 | P3
**Created:** YYYY-MM-DD
**Updated:** YYYY-MM-DD

## Summary

[1-2 sentence description]

## Problem

[What problem does this solve?]

## Proposed Solution

[High-level approach]

## User Stories

- As a [user], I want [action], so that [benefit]

## RICE Score

| Factor | Value | Notes |
|--------|-------|-------|
| Reach | X | [How many users] |
| Impact | X | [0.25-3] |
| Confidence | X% | [50-100%] |
| Effort | X | [Person-months] |
| **Score** | **X** | |

## MoSCoW

- [ ] Must
- [ ] Should
- [ ] Could
- [ ] Won't

## Dependencies

- [Dependency 1]
- [Dependency 2]

## Risks

- [Risk 1]
- [Risk 2]

## Next Steps

- [ ] [Action needed to move forward]
```

### Grooming Session Template

```markdown
# Backlog Grooming: YYYY-MM-DD

**Attendees:** [Names]
**Duration:** [X minutes]

## New Ideas Reviewed

| ID | Title | Decision |
|----|-------|----------|
| BL-XXX | [Title] | Keep / Drop |
| BL-XXY | [Title] | Keep / Drop |

## Priority Changes

| ID | Title | Old Priority | New Priority | Reason |
|----|-------|--------------|--------------|--------|
| BL-XXX | [Title] | P2 | P1 | [Reason] |

## Items Refined

| ID | Title | Changes Made |
|----|-------|--------------|
| BL-XXX | [Title] | Added acceptance criteria |

## Items Archived

| ID | Title | Reason |
|----|-------|--------|
| BL-XXX | [Title] | No longer relevant |

## Next Sprint Candidates

| Priority | ID | Title | Effort |
|----------|-----|-------|--------|
| 1 | BL-XXX | [Title] | X days |
| 2 | BL-XXY | [Title] | X days |
| 3 | BL-XXZ | [Title] | X days |

## Action Items

- [ ] [Action] - [Owner] - [Due]
```

### Roadmap Template

```markdown
# Product Roadmap: [Product Name]

**Last Updated:** YYYY-MM-DD
**Time Horizon:** [X months]

---

## Vision

[One sentence describing where the product is going]

---

## Now (Current Quarter)

### [Milestone 1 Name]
**Target:** [Month]
**Status:** On Track | At Risk | Delayed

Features:
- [x] [Feature 1] - DONE
- [ ] [Feature 2] - IN PROGRESS
- [ ] [Feature 3] - PLANNED

### [Milestone 2 Name]
...

---

## Next (Next Quarter)

### [Milestone Name]
**Target:** [Month]
**Confidence:** High | Medium | Low

Features:
- [ ] [Feature 1]
- [ ] [Feature 2]

---

## Later (6-12 months)

### [Theme Name]
Features under consideration:
- [Feature 1]
- [Feature 2]

*Note: Later items may change based on learnings*

---

## Not Planned

Items explicitly not on roadmap:
- [Item 1] - Reason: [Why not]
- [Item 2] - Reason: [Why not]

---

## Dependencies

| Item | Depends On | Risk |
|------|------------|------|
| [Item] | [Dependency] | [Risk level] |

---

## Change Log

| Date | Change |
|------|--------|
| YYYY-MM-DD | [What changed] |
```

---

## Examples

### Example: RICE Scoring

**Feature:** Add social login (Google, GitHub)

| Factor | Value | Calculation |
|--------|-------|-------------|
| Reach | 8 | 80% of users would use it |
| Impact | 1 | Medium impact (convenience) |
| Confidence | 80% | Good data from competitors |
| Effort | 1 | ~1 person-month |

**RICE Score = (8 × 1 × 0.8) / 1 = 6.4**

**Feature:** Add dark mode

| Factor | Value | Calculation |
|--------|-------|-------------|
| Reach | 3 | 30% of users requested |
| Impact | 0.5 | Low impact (cosmetic) |
| Confidence | 100% | Clear requirement |
| Effort | 0.5 | ~2 weeks |

**RICE Score = (3 × 0.5 × 1.0) / 0.5 = 3.0**

**Decision:** Social login (6.4) > Dark mode (3.0). Do social login first.

### Example: Quarterly Roadmap

```markdown
# Q1 2026 Roadmap: Faion Network

## January: Foundation

### Week 1-2: Framework Content
- [x] Create domain skills (8)
- [x] Write methodologies (282)
- [x] Update agents (29)

### Week 3-4: Landing Page
- [ ] Design landing page
- [ ] Implement Gatsby frontend
- [ ] Deploy to production

## February: Core Product

### Week 1-2: Backend API
- [ ] Set up Django
- [ ] Implement auth endpoints
- [ ] Deploy to Hetzner

### Week 3-4: Paywall System
- [ ] Stripe integration
- [ ] Subscription tiers
- [ ] Payment flows

## March: Content & Launch

### Week 1-2: Content Platform
- [ ] Methodology viewer
- [ ] Search functionality
- [ ] Progress tracking

### Week 3-4: Localization
- [ ] 8 language support
- [ ] Translation pipeline
- [ ] Regional pricing
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Too many P0s | Only 1-3 items can be "most important" |
| Roadmap as commitment | Roadmap is plan, not promise - update as you learn |
| Never dropping items | Regularly archive old, irrelevant items |
| Grooming as status meeting | Focus on prioritization, not updates |
| No "Won't do" list | Explicitly document what you're NOT doing |

---

## Related Methodologies

- **sdd-workflow-overview:** SDD Workflow Overview
- **feature-prioritization-rice:** Feature Prioritization (RICE)
- **feature-prioritization-moscow:** Feature Prioritization (MoSCoW)
- **roadmap-design:** Roadmap Design

---

## Agent

**faion-task-executor-agent** manages backlog and roadmap. Invoke with:
- "Groom the backlog"
- "Score this feature with RICE"
- "Update the roadmap with Q2 plans"

---

*Methodology | SDD Foundation | Version 1.0*
