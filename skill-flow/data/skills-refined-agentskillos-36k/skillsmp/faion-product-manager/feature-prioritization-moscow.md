---
id: feature-prioritization-moscow
name: "Feature Prioritization (MoSCoW)"
domain: PRD
skill: faion-product-manager
category: "product"
---

# Feature Prioritization (MoSCoW)

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Beginner |
| **Tags** | #product, #prioritization, #moscow |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-mvp-scope-analyzer-agent |

---

## Problem

Teams struggle to align on what's essential vs. optional. Common issues:
- Everything marked as "high priority"
- No clear trade-off discussions
- Scope creep from "nice to haves"
- Stakeholder conflicts on what matters

**The root cause:** No shared vocabulary for priority levels.

---

## Framework

### What is MoSCoW?

MoSCoW is a prioritization technique that categorizes requirements into four buckets:
- **M**ust Have
- **S**hould Have
- **C**ould Have
- **W**on't Have

### Category Definitions

#### Must Have (M)

**Definition:** Non-negotiable for this release. Without these, the product is not viable.

**Test questions:**
- Will it fail completely without this?
- Is there no workaround?
- Is it legally/contractually required?

**Target:** 60% of effort

**Examples:**
- User authentication for a SaaS
- Payment processing for e-commerce
- Core value proposition feature

#### Should Have (S)

**Definition:** Important but not critical. Has workarounds, can wait briefly.

**Test questions:**
- Is it painful but workable without?
- Can users accomplish goals with workarounds?
- Will it significantly improve experience?

**Target:** 20% of effort

**Examples:**
- Password reset (can use support workaround)
- Search/filter (can scroll manually)
- Notifications (can check manually)

#### Could Have (C)

**Definition:** Nice to have. Low cost to include if time permits.

**Test questions:**
- Is it a minor enhancement?
- Does lack of it not affect core function?
- Is it a delight feature, not necessity?

**Target:** 20% of effort (but first to cut)

**Examples:**
- Dark mode
- Keyboard shortcuts
- Cosmetic improvements
- Secondary integrations

#### Won't Have (W)

**Definition:** Explicitly not in this release. Documented for clarity.

**Why document:**
- Prevents scope creep
- Sets clear expectations
- Saves for future consideration
- Focuses discussions

**Examples:**
- Mobile app (web first)
- Team features (solo focus)
- Advanced analytics (basic first)

### MoSCoW Process

#### Step 1: List All Requirements

Gather everything from:
- Stakeholder requests
- User research
- Technical needs
- Competitive analysis

#### Step 2: Define the Timebox

**Critical:** MoSCoW requires fixed constraints:
- Time: "This sprint" or "This quarter"
- Resources: Team capacity
- Budget: If applicable

#### Step 3: Initial Categorization

For each item, ask:
1. "If we don't have this, does the product work?" → Must if No
2. "Is there a reasonable workaround?" → Should if No
3. "Is this nice but not needed?" → Could
4. "Is this out of scope for this release?" → Won't

#### Step 4: Validate Effort Allocation

Check proportions:
- Must + Should ≤ 80% of capacity
- Buffer 20% for Could or overflow

**If over budget:**
- Move Should to Could
- Move Could to Won't
- NEVER move Must to Should

#### Step 5: Stakeholder Alignment

Review with stakeholders:
- Share categorization
- Discuss disagreements
- Document decisions

#### Step 6: Lock and Track

Once agreed:
- Lock Must Have (change requires escalation)
- Lock Won't Have (prevents scope creep)
- Should/Could can flex

---

## Templates

### MoSCoW Prioritization Matrix

```markdown
## MoSCoW: [Project/Release]

### Context
- **Release:** [Name/Date]
- **Capacity:** [Person-days/weeks]
- **Constraints:** [Any limitations]

### Must Have (60% target)
| Requirement | Effort | Rationale |
|-------------|--------|-----------|
| [Req 1] | [X] days | [Why must] |
| [Req 2] | [X] days | [Why must] |
**Total Effort:** [X] days ([X]% of capacity)

### Should Have (20% target)
| Requirement | Effort | Workaround |
|-------------|--------|------------|
| [Req 1] | [X] days | [Alternative] |
| [Req 2] | [X] days | [Alternative] |
**Total Effort:** [X] days ([X]% of capacity)

### Could Have (20% target)
| Requirement | Effort | Notes |
|-------------|--------|-------|
| [Req 1] | [X] days | [Context] |
| [Req 2] | [X] days | [Context] |
**Total Effort:** [X] days ([X]% of capacity)

### Won't Have (This Release)
| Requirement | Reason | When |
|-------------|--------|------|
| [Req 1] | [Why not] | [Future?] |
| [Req 2] | [Why not] | [Future?] |

### Summary
| Category | Count | Effort | % |
|----------|-------|--------|---|
| Must | [X] | [X] days | [X]% |
| Should | [X] | [X] days | [X]% |
| Could | [X] | [X] days | [X]% |
| Won't | [X] | N/A | N/A |
```

### Prioritization Discussion Guide

```markdown
## MoSCoW Discussion: [Requirement]

### Current Categorization
**Proposed:** [Must/Should/Could/Won't]
**Proposed by:** [Person]

### Debate Points

**Case for Must Have:**
- [Argument 1]
- [Argument 2]

**Case for Should Have:**
- [Argument 1]
- [Argument 2]

**Case for Could Have:**
- [Argument 1]

### Questions to Resolve
1. [Question about impact]
2. [Question about workaround]
3. [Question about effort]

### Decision
**Final Category:** [X]
**Decided by:** [Person/Group]
**Date:** [Date]
**Rationale:** [Summary]
```

---

## Examples

### Example 1: MVP Launch MoSCoW

**Project:** Invoice Management App - MVP Launch
**Capacity:** 40 person-days

| Category | Requirements | Effort |
|----------|--------------|--------|
| Must | User auth, Create invoice, Send invoice, Basic dashboard | 24 days (60%) |
| Should | PDF export, Client management, Payment reminders | 8 days (20%) |
| Could | Templates, Recurring invoices, Analytics | 8 days (20%) |
| Won't | Mobile app, Team features, Integrations | N/A |

**Outcome:** Launched on time with Must + most Should.

### Example 2: Feature Release MoSCoW

**Project:** Search Enhancement - Q2 Release
**Capacity:** 20 person-days

| Category | Requirements | Effort |
|----------|--------------|--------|
| Must | Full-text search, Search results page | 12 days (60%) |
| Should | Filters, Sort options | 4 days (20%) |
| Could | Saved searches, Search suggestions | 4 days (20%) |
| Won't | AI-powered search, Visual search | N/A |

**Outcome:** Delivered Must + Should; saved searches moved to next release.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Everything is Must | Apply strict test: fails without it? |
| No Won't category | Always document exclusions |
| Ignoring effort | Check proportions against capacity |
| Changing Must mid-sprint | Require escalation for changes |
| Not involving stakeholders | Collaborative exercise |
| Vague requirements | Make each item specific and testable |
| No timebox | MoSCoW needs fixed constraints |

---

## Related Methodologies

- **feature-prioritization-rice:** Feature Prioritization (RICE)
- **mvp-scoping:** MVP Scoping
- **roadmap-design:** Roadmap Design
- **writing-specifications:** Writing Specifications
- **requirements-prioritization:** Requirements Prioritization

---

## Agent

**faion-mvp-scope-analyzer-agent** helps with MoSCoW. Invoke with:
- "Categorize these features with MoSCoW: [list]"
- "Is [feature] a Must Have or Should Have?"
- "Help me scope [project] using MoSCoW"
- "What should go in Won't Have for [release]?"

---

*Methodology | Product | Version 1.0*
