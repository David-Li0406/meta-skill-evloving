---
id: mlp-planning
name: "MLP Planning"
domain: PRD
skill: faion-product-manager
category: "product"
---

# MLP Planning

## Metadata

| Field | Value |
|-------|-------|
| **ID** | (semantic) |
| **Category** | Product |
| **Difficulty** | Intermediate |
| **Tags** | #product, #mlp, #planning |
| **Domain Skill** | faion-product-manager |
| **Agents** | faion-mlp-gap-finder-agent |

---

## Problem

MVP validates ideas but often fails to retain users. Common issues:
- Users try MVP, get value, but leave for better UX
- "Minimum" becomes "mediocre"
- No clear path from validation to retention
- Competing on features instead of experience

**The root cause:** No framework for evolving from viable to lovable.

---

## Framework

### What is MLP?

Minimum Lovable Product is the smallest version that:
1. Delivers core value (like MVP)
2. Creates emotional connection
3. Gives users a reason to stay AND recommend

**Key insight:** MLP = MVP + delight. Not more features, better experience.

### MVP vs MLP Comparison

| Aspect | MVP | MLP |
|--------|-----|-----|
| Goal | Validate | Retain |
| Focus | Functionality | Experience |
| Quality | Good enough | Polished |
| Emotion | "It works" | "I love it" |
| Word of mouth | Unlikely | Likely |

### The MLP Framework

#### Layer 1: Functional (MVP baseline)

**Must satisfy:**
- Core job gets done
- No blocking bugs
- Acceptable performance

#### Layer 2: Reliable

**Adds:**
- Consistent experience
- Error handling
- Edge cases covered
- Works as expected

#### Layer 3: Usable

**Adds:**
- Easy to learn
- Efficient to use
- Minimal friction
- Good defaults

#### Layer 4: Delightful (MLP target)

**Adds:**
- Emotional satisfaction
- Surprising moments
- Premium feel
- Shareable moments

### MLP Planning Process

#### Step 1: Audit Your MVP

**For each core feature, rate 1-5:**

| Feature | Functional | Reliable | Usable | Delightful |
|---------|------------|----------|--------|------------|
| [Feature 1] | ? | ? | ? | ? |
| [Feature 2] | ? | ? | ? | ? |

**MLP threshold:** All features at 4+ on all layers.

#### Step 2: Identify Delight Opportunities

**Where can you add delight:**
- First impression (onboarding)
- Core action (the main thing they do)
- Success moments (when they win)
- Recovery moments (when things go wrong)

**Delight categories:**

| Type | Description | Example |
|------|-------------|---------|
| Speed | Faster than expected | Instant search results |
| Simplicity | Easier than expected | One-click checkout |
| Personality | Unexpected charm | Clever copywriting |
| Anticipation | Knows what they need | Smart defaults |
| Celebration | Acknowledges success | Confetti on completion |

#### Step 3: Prioritize Polish

**Polish priority = User pain × Frequency × Visibility**

| Task | Pain (1-5) | Frequency | Visibility | Priority |
|------|------------|-----------|------------|----------|
| [Task] | ? | ? | ? | ? |

**Focus on:** High frequency, high visibility interactions.

#### Step 4: Define MLP Criteria

**Template:**
```
For [user segment]
MLP means [specific outcomes]:
1. [Functional criteria]
2. [Reliable criteria]
3. [Usable criteria]
4. [Delightful criteria]

Measured by: [How to verify]
```

#### Step 5: Plan the Gap

**Gap analysis:**

| Feature | Current State | MLP Target | Gap | Effort |
|---------|---------------|------------|-----|--------|
| [Feature] | [Description] | [Target] | [What's missing] | [Days] |

---

## Templates

### MLP Planning Document

```markdown
## MLP Plan: [Product Name]

### Current State (MVP)
**Version:** [Current]
**Users:** [Count]
**Retention:** [Day 7, Day 30]
**NPS:** [Score]

### MLP Goal
**Target retention:** [Day 30 target]
**Target NPS:** [Score target]
**Timeline:** [X] weeks

### Feature Audit

| Feature | Func | Reliable | Usable | Delight | Priority |
|---------|------|----------|--------|---------|----------|
| [Core 1] | 5 | 4 | 3 | 2 | High |
| [Core 2] | 5 | 5 | 4 | 3 | Medium |

### Delight Opportunities

#### First Impression
- Current: [What happens now]
- MLP: [What should happen]
- Tasks: [What to do]

#### Core Action: [Action Name]
- Current: [What happens now]
- MLP: [What should happen]
- Tasks: [What to do]

#### Success Moments
- Current: [What happens now]
- MLP: [What should happen]
- Tasks: [What to do]

### Polish Backlog

| Task | Layer | Effort | Impact | Priority |
|------|-------|--------|--------|----------|
| [Task 1] | Usable | 1 day | High | P1 |
| [Task 2] | Delight | 2 days | Medium | P2 |

### MLP Completion Criteria

- [ ] All core features at 4+ on all layers
- [ ] Onboarding completion > [X]%
- [ ] Core action time < [X] seconds
- [ ] Zero UX blockers
- [ ] 3 delight moments implemented
- [ ] [X]% of users would recommend (survey)

### Measurement Plan

| Metric | MVP Baseline | MLP Target |
|--------|--------------|------------|
| Day 7 retention | [X]% | [Y]% |
| Day 30 retention | [X]% | [Y]% |
| NPS | [X] | [Y] |
| Core action completion | [X]% | [Y]% |
```

### Delight Sprint Template

```markdown
## Delight Sprint: [Focus Area]

### Scope
**Area:** [Part of product]
**Duration:** [X] days
**Goal:** Add delight to [specific workflow]

### Current Experience
[Description of current state]
User quote: "[What users say]"

### Target Experience
[Description of desired state]
User reaction: "[What we want them to feel]"

### Tasks

| Task | Type | Effort | Owner |
|------|------|--------|-------|
| [Task 1] | Copy | 2 hrs | [Name] |
| [Task 2] | UI | 4 hrs | [Name] |
| [Task 3] | Animation | 1 day | [Name] |

### Success Criteria
- [ ] [Specific outcome]
- [ ] User testing: [X] of [Y] smile/react positively
```

---

## Examples

### Example 1: Note-Taking App MVP to MLP

**MVP state:**
- Create, edit, delete notes
- Basic formatting
- Functional but bland

**MLP additions:**

| Layer | Improvement |
|-------|-------------|
| Reliable | Auto-save with visual confirmation |
| Usable | Keyboard shortcuts, quick capture |
| Delight | Smooth animations, satisfying sounds |
| Delight | "Zen mode" for focused writing |
| Delight | Clever empty states |

**Result:** Retention increased 40%, NPS from 30 to 55.

### Example 2: Invoicing Tool MVP to MLP

**MVP state:**
- Create invoices
- Send to clients
- Basic but clunky

**MLP additions:**

| Layer | Improvement |
|-------|-------------|
| Reliable | Payment confirmation notifications |
| Usable | Templates from past invoices |
| Usable | Client auto-fill |
| Delight | Celebration on payment received |
| Delight | "You've earned $X this month" dashboard |

**Result:** Users create 2x more invoices, 60% NPS.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Adding more features | Polish existing features first |
| Skipping MVP | Validate before beautifying |
| Surface-level polish | Focus on interaction quality |
| Ignoring speed | Performance is delight |
| Generic delight | Tailor to your audience |
| Delight without function | Layer 4 requires layers 1-3 |

---

## Related Methodologies

- **mvp-scoping:** MVP Scoping
- **usability-heuristics:** 10 Usability Heuristics
- **usability-testing:** Usability Testing
- **activation-rate-optimization:** Activation Rate Optimization
- **retention-loops:** Retention Loops

---

## Agent

**faion-mlp-gap-finder-agent** helps plan MLP. Invoke with:
- "Audit my MVP for MLP readiness"
- "Find delight opportunities in [workflow]"
- "What's the gap between MVP and MLP for [product]?"
- "Prioritize polish tasks for [feature list]"

---

*Methodology | Product | Version 1.0*
