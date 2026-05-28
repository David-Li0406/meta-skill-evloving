---
id: funnel-optimization
name: "Funnel Optimization"
domain: GRO
skill: faion-marketing-manager
category: "growth"
---

# Funnel Optimization

## Metadata

| Field | Value |
|-------|-------|
| **ID** | funnel-optimization |
| **Name** | Funnel Optimization |
| **Category** | Growth |
| **Difficulty** | Intermediate |
| **Agent** | faion-growth-agent |
| **Related** | aarrr-pirate-metrics, ab-testing-framework, activation-rate |

---

## Problem

Users visit your product but do not convert. They start signing up but do not finish. They sign up but do not activate. At each step, you lose people.

Funnel optimization identifies WHERE users drop off and WHY, then tests changes to improve conversion at each step.

---

## Framework

### What is a Funnel?

A funnel is a sequence of steps users take toward a goal. Each step has fewer users than the previous one.

```
VISITORS         ████████████████████ 10,000  (100%)
                        ↓ 30%
SIGNUPS          ██████ 3,000                 (30%)
                        ↓ 40%
ACTIVATED        ███ 1,200                    (12%)
                        ↓ 25%
CONVERTED        █ 300                        (3%)
```

### The Funnel Optimization Process

```
1. MAP THE FUNNEL
   Define all steps from entry to goal
        ↓
2. MEASURE EACH STEP
   Track conversion rates between steps
        ↓
3. FIND THE BIGGEST DROP
   Identify where most users leave
        ↓
4. DIAGNOSE THE CAUSE
   Understand why users drop off
        ↓
5. GENERATE HYPOTHESES
   Ideas to improve that step
        ↓
6. TEST AND ITERATE
   Run A/B tests, measure impact
        ↓
7. REPEAT
   Move to next biggest drop
```

### Common Funnel Types

#### Marketing Funnel
```
Impression → Click → Landing Page → Signup → Activation → Purchase
```

#### SaaS Funnel
```
Visit → Signup → Onboarding → Activation → Engagement → Conversion → Retention
```

#### E-commerce Funnel
```
Visit → View Product → Add to Cart → Checkout Start → Payment → Confirmation
```

#### Mobile App Funnel
```
App Store → Download → Open → Onboarding → Core Action → Retention → Monetization
```

---

## Step-by-Step Process

### Step 1: Map the Funnel

Define every step from first touch to goal.

**Example - SaaS signup funnel:**

| Step | Description | Event Name |
|------|-------------|------------|
| 1 | Land on homepage | `page_view_home` |
| 2 | Click "Get Started" | `cta_clicked` |
| 3 | View signup form | `signup_form_viewed` |
| 4 | Submit email | `email_submitted` |
| 5 | Verify email | `email_verified` |
| 6 | Complete profile | `profile_completed` |
| 7 | First action | `first_action_completed` |

### Step 2: Measure Each Step

Track users at each step and calculate conversion rates.

```
FUNNEL ANALYSIS: Signup Flow (Last 30 Days)
─────────────────────────────────────────────────
Step                   Users    Conv %    Drop %
─────────────────────────────────────────────────
1. Homepage           10,000    100%      -
2. Click CTA           3,500     35%      65%  ← High drop
3. Signup form         3,200     91%       9%
4. Submit email        2,400     75%      25%  ← Moderate drop
5. Verify email        1,920     80%      20%
6. Profile complete    1,536     80%      20%
7. First action        1,075     70%      30%  ← High drop
─────────────────────────────────────────────────
Overall conversion: 10.75% (1,075 / 10,000)
```

### Step 3: Find the Biggest Drop

Identify the step with the largest absolute or percentage drop.

**Analysis:**

| Step | Users Lost | % of Total Lost |
|------|------------|-----------------|
| 1→2 Homepage to CTA | 6,500 | 73% |
| 2→3 CTA to Form | 300 | 3% |
| 3→4 Form to Submit | 800 | 9% |
| 4→5 Submit to Verify | 480 | 5% |
| 5→6 Verify to Profile | 384 | 4% |
| 6→7 Profile to Action | 461 | 5% |

**Priority:** Step 1→2 (Homepage to CTA click) is the biggest leak.

### Step 4: Diagnose the Cause

**Methods to understand why users drop:**

| Method | When to Use | Example |
|--------|------------|---------|
| Session recordings | See user behavior | Hotjar, FullStory |
| Heatmaps | Find attention areas | Crazy Egg, Hotjar |
| User surveys | Ask directly | Exit surveys, polls |
| User interviews | Deep understanding | 5-10 user calls |
| Analytics | Segment by attribute | Mobile vs desktop |

**Common drop-off causes:**

| Step | Common Causes |
|------|---------------|
| Landing → CTA | Unclear value prop, poor design, slow load |
| CTA → Form | Too many fields, scary commitment |
| Form → Submit | Technical errors, confusing UX |
| Submit → Verify | Email goes to spam, delay |
| Onboarding → Activation | Too complex, no guidance, no value shown |

### Step 5: Generate Hypotheses

Create testable hypotheses for the biggest drop.

**Template:**
```
IF we [change X]
THEN [metric] will improve by [Y%]
BECAUSE [reason based on diagnosis]
```

**Example hypotheses for Homepage → CTA drop:**

1. "If we make the CTA button larger and green, CTR will increase by 15% because it's more visible"
2. "If we add social proof above the fold, CTR will increase by 20% because trust increases"
3. "If we simplify the headline to focus on one benefit, CTR will increase by 10% because clarity improves"

### Step 6: Test and Iterate

Prioritize hypotheses and run A/B tests.

**Prioritization framework (ICE):**

| Hypothesis | Impact | Confidence | Ease | ICE Score |
|------------|--------|------------|------|-----------|
| Larger CTA | 7 | 8 | 9 | 24 | ← Test first |
| Social proof | 8 | 6 | 7 | 21 |
| Simpler headline | 6 | 5 | 8 | 19 |

---

## Templates

### Funnel Analysis Template

```markdown
# Funnel Analysis: [Name]

## Funnel Definition

| Step | Description | Event |
|------|-------------|-------|
| 1 | | |
| 2 | | |
| 3 | | |

## Current Performance (Last 30 Days)

| Step | Users | Conversion | Drop-off |
|------|-------|------------|----------|
| 1 | | 100% | - |
| 2 | | | |
| 3 | | | |

Overall conversion: ____%

## Biggest Leaks

| Priority | Step | Users Lost | % of Total |
|----------|------|------------|------------|
| 1 | | | |
| 2 | | | |

## Diagnosis

### Step [X] Analysis

**What we observed:**
- [Session recording insights]
- [Heatmap insights]
- [Survey feedback]

**Root cause hypothesis:**
[Why users are dropping off]

## Optimization Hypotheses

| # | If we... | Then... | Because... | ICE |
|---|----------|---------|------------|-----|
| 1 | | | | |
| 2 | | | | |

## Test Plan

| Priority | Hypothesis | Metric | Duration |
|----------|------------|--------|----------|
| 1 | | | |
| 2 | | | |
```

### Funnel Review Checklist

```markdown
## Weekly Funnel Review

### Overall Health
- [ ] Overall conversion: ____% (Target: ___%)
- [ ] Trend: [Improving / Stable / Declining]

### Step-by-Step Check
- [ ] Step 1→2: ____% (Target: ___%)
- [ ] Step 2→3: ____% (Target: ___%)
- [ ] Step 3→4: ____% (Target: ___%)

### Segment Analysis
- [ ] Mobile vs Desktop: [Any difference?]
- [ ] New vs Returning: [Any difference?]
- [ ] Traffic source: [Any difference?]

### Active Tests
- [ ] Test 1: [Name] - Day X of Y
- [ ] Test 2: [Name] - Day X of Y

### This Week's Focus
[Which step and what action?]
```

---

## Examples

### Example 1: SaaS Signup Funnel

**Problem:** Low overall conversion (2%)

**Funnel:**
```
Homepage    → 10,000 (100%)
Pricing     →  2,000 (20%)   ← 80% drop
Signup      →    800 (8%)    ← 60% drop
Trial       →    400 (4%)    ← 50% drop
Paid        →    200 (2%)    ← 50% drop
```

**Diagnosis:**
1. Homepage → Pricing (80% drop): Value prop unclear
2. Pricing → Signup (60% drop): Pricing confusing

**Tests run:**

| Test | Result |
|------|--------|
| Clearer headline on homepage | +15% to pricing page |
| Simplified pricing (3 → 2 tiers) | +25% signup rate |
| Added "Start free" emphasis | +10% trial start |

**Result:**
```
Before: 2.0% overall conversion
After:  3.8% overall conversion (+90% improvement)
```

### Example 2: E-commerce Checkout

**Funnel:**
```
Product Page → 50,000 (100%)
Add to Cart  → 10,000 (20%)
Checkout     →  4,000 (8%)   ← 60% abandon cart
Payment      →  2,500 (5%)
Confirm      →  2,000 (4%)
```

**Cart abandonment analysis:**
- 35% left at shipping costs reveal
- 25% left at account creation requirement
- 20% left at payment form
- 20% other

**Optimizations:**
1. Show shipping costs on product page → -15% abandonment
2. Add guest checkout → -20% abandonment
3. Express checkout (Apple Pay, Google Pay) → +12% completion

### Example 3: Mobile App Onboarding

**Funnel:**
```
Install     → 10,000 (100%)
Open app    →  7,500 (75%)   ← 25% never open
Screen 1    →  6,000 (60%)   ← 20% drop
Screen 2    →  4,500 (45%)   ← 25% drop
Screen 3    →  3,000 (30%)   ← 33% drop
Core action →  1,500 (15%)   ← 50% drop
```

**Diagnosis:**
- Onboarding too long (3 screens)
- Users not reaching core value

**Solution:**
- Reduce to 1 welcome screen
- Skip to core action immediately
- Show onboarding tips contextually

**Result:**
```
Before: 15% reach core action
After:  42% reach core action (+180%)
```

---

## Funnel Optimization Tactics

### By Stage

#### Top of Funnel (Awareness)
- Clearer headlines
- Faster page load
- Better ad targeting
- Social proof

#### Middle of Funnel (Consideration)
- Reduce form fields
- Progress indicators
- Trust badges
- Clear CTAs

#### Bottom of Funnel (Conversion)
- Guest checkout
- Multiple payment options
- Clear error messages
- Urgency/scarcity

### Quick Wins

| Tactic | Typical Lift | Effort |
|--------|--------------|--------|
| Remove form fields | +10-25% | Low |
| Add progress bar | +5-15% | Low |
| Improve button contrast | +5-20% | Low |
| Add social proof | +5-15% | Medium |
| Speed up load time | +5-20% | Medium |
| Simplify copy | +5-10% | Low |

---

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|---------------|-----|
| Optimizing small leaks first | Wasted effort | Start with biggest drop |
| Guessing causes | Wrong solutions | Diagnose with data |
| Testing too many things | Cannot isolate impact | One change at a time |
| Ignoring mobile | Different experience | Segment analysis |
| Not setting targets | No goal | Set benchmarks |

---

## Funnel Benchmarks

### SaaS

| Step | Good | Great |
|------|------|-------|
| Visitor → Signup | 2-5% | 5-10% |
| Signup → Activated | 30-50% | 50-70% |
| Activated → Paid | 3-5% | 5-10% |
| Visitor → Paid | 0.5-1% | 1-3% |

### E-commerce

| Step | Good | Great |
|------|------|-------|
| Visitor → Cart | 3-8% | 8-15% |
| Cart → Checkout | 40-60% | 60-80% |
| Checkout → Purchase | 50-70% | 70-85% |
| Visitor → Purchase | 1-2% | 2-4% |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Funnel analytics | Mixpanel, Amplitude, Posthog |
| Session recording | Hotjar, FullStory, LogRocket |
| Heatmaps | Crazy Egg, Hotjar |
| A/B testing | Optimizely, VWO |
| Surveys | Hotjar, Typeform |

---

## Related Methodologies

- **aarrr-pirate-metrics:** AARRR Pirate Metrics (funnel framework)
- **ab-testing-framework:** A/B Testing Framework (how to test)
- **activation-rate:** Activation Rate Optimization (activation funnel)

---

*Methodology: funnel-optimization | Growth | faion-growth-agent*
