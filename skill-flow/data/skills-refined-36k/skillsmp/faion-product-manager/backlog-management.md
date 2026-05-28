---
id: backlog-management
name: "Backlog Management"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Backlog Management

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Beginner |
| **Tags** | #product, #backlog, #agile |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-task-creator-agent |

---

## Problem

Backlogs become dumping grounds for ideas. Issues:
- Hundreds of items, no prioritization
- Stale items never cleaned up
- Unclear requirements
- No connection to goals

**The root cause:** Backlogs treated as storage instead of strategic tools.

---

## Framework

### What is Backlog Management?

Backlog management is maintaining a prioritized, healthy list of work that connects to product goals. It answers: "What should we build and in what order?"

### Backlog Health Principles

| Principle | Description |
|-----------|-------------|
| **DEEP** | Detailed (top), Emergent (bottom), Estimated, Prioritized |
| **INVEST** | Independent, Negotiable, Valuable, Estimable, Small, Testable |
| **Living** | Continuously refined, not static |

### Backlog Structure

```
Priority
   ↑
   │ ┌─────────────────────┐
   │ │ Ready (Next Sprint) │ ← Detailed, estimated, acceptance criteria
   │ └─────────────────────┘
   │ ┌─────────────────────┐
   │ │ Upcoming (1-3 sprints)│ ← Defined, some detail
   │ └─────────────────────┘
   │ ┌─────────────────────┐
   │ │ Backlog (Future)    │ ← Ideas, rough
   │ └─────────────────────┘
   │ ┌─────────────────────┐
   │ │ Icebox (Maybe/Later)│ ← Parked, low priority
   │ └─────────────────────┘
```

### Backlog Item Quality

**Good backlog item:**
- Clear user value
- Acceptance criteria
- Size estimate
- Priority/rank
- No dependencies (or documented)

**Template:**
```
Title: [Action-oriented title]
As a [user type]
I want [action]
So that [benefit]

Acceptance Criteria:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

Size: [XS/S/M/L/XL]
Priority: [P1/P2/P3]
```

### Backlog Management Process

#### Step 1: Capture Everything

**Sources:**
- Feature requests
- Bug reports
- Technical debt
- Research outcomes
- Stakeholder input
- Team ideas

**Rule:** Capture quickly, evaluate later.

#### Step 2: Regular Grooming

**Grooming session (weekly):**
- Review new items
- Refine top items
- Estimate if needed
- Reprioritize based on learning
- Archive stale items

**Time:** 1-2 hours per week

#### Step 3: Prioritization

**Methods:**
- RICE scoring (feature-prioritization-rice)
- MoSCoW (feature-prioritization-moscow)
- Weighted scoring
- Stack ranking

**Review priority when:**
- New information arrives
- Goals change
- Sprint planning

#### Step 4: Refinement

**For top-of-backlog items:**
- Break into smaller stories
- Add acceptance criteria
- Clarify requirements
- Estimate effort
- Identify dependencies

**"Ready" definition:**
- Clear scope
- Acceptance criteria
- Estimate
- No blockers

#### Step 5: Cleanup

**Regular hygiene:**
- Delete duplicates
- Archive stale items (6+ months untouched)
- Merge related items
- Update outdated items

**Healthy backlog:**
- 2-4 sprints worth of ready items
- <100 total items (or grouped)
- <10% stale items

---

## Templates

### Backlog Health Check

```markdown
## Backlog Health Check: [Product]

### Snapshot
- **Date:** [Date]
- **Total items:** [X]
- **Ready items:** [X]
- **Stale items (6+ mo):** [X]

### By Status

| Status | Count | % |
|--------|-------|---|
| Ready | [X] | [X]% |
| Upcoming | [X] | [X]% |
| Backlog | [X] | [X]% |
| Icebox | [X] | [X]% |

### By Type

| Type | Count |
|------|-------|
| Feature | [X] |
| Bug | [X] |
| Tech debt | [X] |
| Research | [X] |

### Health Metrics

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Ready items | [X] | 10-20 | OK/Not |
| Avg item age | [X] days | <90 | OK/Not |
| Stale % | [X]% | <10% | OK/Not |
| Items with AC | [X]% | >80% | OK/Not |

### Actions Needed
- [ ] [Action 1]
- [ ] [Action 2]
```

### Backlog Grooming Agenda

```markdown
## Grooming Session: [Date]

### Attendees
- Product: [Name]
- Engineering: [Name]
- Design: [Name]

### New Items to Triage ([X] items)

| Item | Type | Decision | Priority |
|------|------|----------|----------|
| [Item] | [Type] | Add/Reject/Combine | [P1/2/3] |

### Top of Backlog Review

| Item | Status | Ready? | Notes |
|------|--------|--------|-------|
| [Item] | [Status] | Y/N | [What's needed] |

### Items to Refine

#### [Item 1]
**Current state:** [Description]
**Questions:**
- [Question 1]
- [Question 2]
**Refined:**
- [Updated scope]
- [Acceptance criteria added]

### Estimates

| Item | Current Est | New Est | Notes |
|------|-------------|---------|-------|
| [Item] | None | M | [Rationale] |

### Cleanup

- Archived: [X] stale items
- Merged: [Items combined]
- Deleted: [Duplicates removed]

### Next Session: [Date]
```

### Backlog Item Template

```markdown
## [Title]

### Type
[ ] Feature [ ] Bug [ ] Tech Debt [ ] Research

### User Story
**As a** [user type]
**I want** [action]
**So that** [benefit]

### Context
[Background information]

### Acceptance Criteria
- [ ] Given [context], when [action], then [result]
- [ ] Given [context], when [action], then [result]
- [ ] [Additional criterion]

### Out of Scope
- [What this doesn't include]

### Dependencies
- [Dependency if any]

### Estimate
[XS/S/M/L/XL] - [X points/days]

### Priority
[P1/P2/P3] - [Rationale]

### Links
- Design: [Link]
- Research: [Link]
```

---

## Examples

### Example 1: Weekly Grooming Outcomes

**Before:**
- 180 backlog items
- 40 stale items
- 5 ready items
- Average age: 120 days

**Actions taken:**
- Archived 30 stale items
- Merged 15 duplicates
- Refined top 10 items
- Added acceptance criteria to 8 items

**After:**
- 135 backlog items
- 10 stale items
- 15 ready items
- Average age: 80 days

### Example 2: Backlog Item Refinement

**Before:**
```
Title: Better search
Description: Search doesn't work well
```

**After:**
```
Title: Add autocomplete to product search
As a customer
I want to see suggestions as I type
So that I find products faster

Acceptance Criteria:
- [ ] Suggestions appear after 2 characters
- [ ] Top 5 products shown
- [ ] Clicking suggestion goes to product
- [ ] Works on mobile

Estimate: M (3-5 days)
Priority: P2 (high usage feature)
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Backlog as dumping ground | Regular cleanup |
| No prioritization | Stack rank everything |
| Vague items | Require clear format |
| Too detailed too early | DEEP principle |
| Never deleting | Archive aggressively |
| Grooming skipped | Weekly commitment |
| Solo grooming | Include team |

---

## Related Methodologies

- **feature-prioritization-rice:** Feature Prioritization (RICE)
- **user-story-mapping:** User Story Mapping
- **backlog-grooming-roadmapping:** Backlog Grooming & Roadmapping
- **jira-workflow-management:** Jira Workflow Management
- **linear-issue-tracking:** Linear Issue Tracking

---

## Agent

**faion-task-creator-agent** helps with backlogs. Invoke with:
- "Review my backlog health: [metrics]"
- "Refine this backlog item: [content]"
- "Prioritize these items: [list]"
- "Create backlog items from [requirements]"

---

*Methodology | Product | Version 1.0*
