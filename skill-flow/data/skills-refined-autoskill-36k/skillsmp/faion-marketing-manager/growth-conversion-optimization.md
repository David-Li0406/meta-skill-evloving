---
id: conversion-optimization
name: "Conversion Rate Optimization (CRO)"
domain: MKT
skill: faion-marketing-manager
category: "marketing"
---

# Conversion Rate Optimization (CRO)

## Metadata

| Field | Value |
|-------|-------|
| **ID** | conversion-optimization |
| **Name** | Conversion Rate Optimization |
| **Category** | Marketing |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | landing-page-design, ab-testing-framework, funnel-optimization |

---

## Problem

You're getting traffic but not conversions. Visitors land on your site and leave without signing up, buying, or taking action. Every visitor costs you money or time to acquire - wasted if they don't convert.

CRO is the practice of systematically improving conversion rates. A 1% to 2% improvement doubles your effective marketing spend.

---

## Framework

CRO follows a research-driven cycle:

```
ANALYZE   -> Where are people dropping off?
RESEARCH  -> Why are they dropping off?
HYPOTHESIZE -> What might fix it?
TEST      -> Run A/B tests
LEARN     -> Document and iterate
```

### Step 1: Measure Your Funnel

**Define conversion funnel:**

```
Visit -> [Page View]
    ↓
Engage -> [Scroll, Click, Time on page]
    ↓
Action -> [Signup, Add to cart, Start trial]
    ↓
Convert -> [Purchase, Activate, Complete onboarding]
```

**Key metrics at each stage:**

| Stage | Metric | Benchmark |
|-------|--------|-----------|
| Landing page | Bounce rate | <50% |
| Signup form | Form completion | >30% |
| Pricing page | CTA click rate | >5% |
| Checkout | Cart completion | >60% |
| Overall | Visitor to customer | 1-5% |

**Track drop-offs:**
- Use funnel visualization (GA4, Mixpanel)
- Identify biggest leaks
- Prioritize highest-impact fixes

### Step 2: Research Why People Leave

**Quantitative research:**

| Method | What It Reveals |
|--------|-----------------|
| Heatmaps | Where people click and scroll |
| Session recordings | How people navigate |
| Funnel analytics | Where they drop off |
| Form analytics | Which fields cause abandonment |
| Exit surveys | Why they're leaving |

**Qualitative research:**

| Method | What It Reveals |
|--------|-----------------|
| User interviews | Deep understanding of friction |
| Usability testing | Where people get confused |
| Customer surveys | Post-conversion feedback |
| Support tickets | Common questions/objections |
| Chat transcripts | Real-time concerns |

**Questions to answer:**
- What are visitors trying to accomplish?
- What's stopping them?
- What would make it easier?

### Step 3: Prioritize Opportunities

**Use the PIE framework:**

| Factor | Question | Score 1-10 |
|--------|----------|------------|
| **Potential** | How much can this improve? | |
| **Importance** | How much traffic does this page get? | |
| **Ease** | How easy to test? | |

**Priority score = (P + I + E) / 3**

**Focus on:**
- High-traffic pages with low conversion
- Simple changes with big impact potential
- Objection-clearing content

### Step 4: Form Hypotheses

**Hypothesis template:**
```
We believe that [change]
will cause [effect]
because [rationale].

We'll measure this by [metric]
and consider it successful if [target].
```

**Example:**
```
We believe that adding customer logos above the fold
will cause more visitors to start a trial
because social proof reduces perceived risk.

We'll measure this by trial signup rate
and consider it successful if it increases by 10%.
```

**Common CRO levers:**

| Lever | Examples |
|-------|----------|
| **Clarity** | Clearer headlines, simpler copy |
| **Value prop** | Better benefit communication |
| **Trust** | Testimonials, logos, guarantees |
| **Urgency** | Limited offers, countdown timers |
| **Friction** | Fewer form fields, simpler process |
| **Risk reversal** | Money-back guarantees, free trials |

### Step 5: Run A/B Tests

**Test requirements:**

| Factor | Minimum |
|--------|---------|
| Sample size | 100+ conversions per variant |
| Duration | 2+ weeks (cover weekly cycles) |
| Statistical significance | 95%+ |

**What to test:**

| Element | Impact Potential |
|---------|------------------|
| Headlines | High |
| CTA buttons | High |
| Hero section | High |
| Form length | High |
| Social proof | Medium |
| Layout | Medium |
| Copy length | Medium |
| Images | Medium |
| Colors | Low |

**Testing rules:**
- Test one thing at a time (or use multivariate)
- Don't peek at results early
- Run to statistical significance
- Document everything

### Step 6: Implement and Iterate

**After a test:**
1. If winner: Implement permanently
2. If loser: Document learnings
3. If inconclusive: Try bigger change

**Build a learning library:**
```markdown
## Test: [Name]
- Date: [When]
- Hypothesis: [What we thought]
- Change: [What we tested]
- Result: [Winner/Loser/Inconclusive]
- Lift: [+X% or -X%]
- Learning: [What we learned]
- Next: [What to test next]
```

---

## Templates

### CRO Audit Template

```markdown
## CRO Audit: [Page/Funnel]

### Current State
- Traffic: [X] visitors/month
- Conversion rate: [X]%
- Revenue impact: $[X]/month

### Funnel Analysis
| Stage | Visitors | Conv. Rate | Drop-off |
|-------|----------|------------|----------|
| Land  | X        | -          | -        |
| View  | X        | X%         | X%       |
| CTA   | X        | X%         | X%       |
| Conv. | X        | X%         | X%       |

### Research Findings
**Heatmaps:**
- [Finding 1]
- [Finding 2]

**Session Recordings:**
- [Finding 1]
- [Finding 2]

**User Feedback:**
- [Finding 1]
- [Finding 2]

### Opportunities (PIE Score)
| Opportunity | P | I | E | Score |
|-------------|---|---|---|-------|
| [Opp 1]     | X | X | X | X.X   |
| [Opp 2]     | X | X | X | X.X   |

### Recommended Tests
1. [Test 1] - [Expected impact]
2. [Test 2] - [Expected impact]
3. [Test 3] - [Expected impact]
```

### A/B Test Brief

```markdown
## Test: [Name]

### Hypothesis
We believe that [change]
will cause [effect]
because [rationale].

### Variants
- Control: [Current state]
- Variant: [Change description]

### Metrics
- Primary: [What we're measuring]
- Secondary: [Supporting metrics]

### Requirements
- Traffic: [X] visitors needed
- Duration: [X] weeks
- Significance: 95%

### Design
[Screenshot or mockup of variant]

### Implementation
- [ ] Design approved
- [ ] Development complete
- [ ] QA passed
- [ ] Test launched
- [ ] Results analyzed
```

---

## Examples

### Example 1: Signup Form Optimization

**Problem:** 15% form completion rate

**Research findings:**
- Heatmaps showed users hesitating at password field
- Session recordings showed confusion about requirements
- Exit surveys mentioned "too many fields"

**Test:**
- Control: 6 fields including password
- Variant: 3 fields (email only), set password later

**Result:**
- 45% increase in form completion
- No negative impact on activation

### Example 2: Pricing Page

**Problem:** 2% pricing page to trial conversion

**Research findings:**
- Users wanted to compare plans easily
- FAQ questions suggested confusion about features
- Mobile experience was poor

**Tests run:**
1. Added comparison table (no impact)
2. Added FAQ section (+15% conversion)
3. Redesigned for mobile (+20% mobile conversion)

---

## Implementation Checklist

### Setup
- [ ] Install analytics (GA4, Mixpanel)
- [ ] Set up heatmaps (Hotjar, FullStory)
- [ ] Define conversion events
- [ ] Create funnel visualization
- [ ] Install A/B testing tool

### Research Phase
- [ ] Run quantitative analysis
- [ ] Conduct 5 user interviews
- [ ] Review support tickets
- [ ] Create opportunity list
- [ ] Prioritize with PIE

### Testing Phase
- [ ] Write hypothesis
- [ ] Design variant
- [ ] Calculate sample size
- [ ] Launch test
- [ ] Monitor for errors
- [ ] Analyze results

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Testing without research | Random changes | Research first |
| Small sample sizes | Unreliable results | Wait for significance |
| Stopping early | False positives | Run full duration |
| Testing tiny changes | Negligible impact | Test big ideas |
| No documentation | Lost learnings | Document everything |
| Testing too many things | Can't isolate effect | One thing at a time |

---

## Metrics to Track

| Metric | What It Tells You |
|--------|-------------------|
| Conversion rate | Overall effectiveness |
| Bounce rate | First impression quality |
| Time on page | Engagement level |
| Scroll depth | Content consumption |
| Form abandonment | Friction points |
| Click maps | User attention |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Analytics | GA4, Mixpanel, Amplitude |
| Heatmaps | Hotjar, FullStory, Microsoft Clarity |
| A/B testing | Optimizely, VWO, Google Optimize |
| Form analytics | Formisimo, Hotjar |
| Session recording | FullStory, LogRocket |
| Surveys | Hotjar, Typeform |

---

## Related Methodologies

- **landing-page-design:** Landing Page Design (page optimization)
- **ab-testing-framework:** A/B Testing Framework (testing methodology)
- **funnel-optimization:** Funnel Optimization (full funnel)
- **usability-testing:** Usability Testing (user research)

---

*Methodology: conversion-optimization | Marketing | faion-growth-agent*
