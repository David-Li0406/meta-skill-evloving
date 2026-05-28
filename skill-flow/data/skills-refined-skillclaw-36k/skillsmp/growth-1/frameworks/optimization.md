# Optimization Framework

## Purpose

Systematically improve conversion and engagement through experimentation. Stop guessing, start testing.

---

## Optimization Principles

### Core Truths

1. **Test, don't guess** - Intuition is often wrong
2. **One variable at a time** - Otherwise you can't learn
3. **Statistical significance matters** - Small samples lie
4. **Document everything** - Build institutional knowledge
5. **Big wins come from big changes** - Button colors rarely matter

### What to Optimize

**High impact (focus here):**
- Core conversion points
- Onboarding flow
- Pricing page
- Activation moments

**Low impact (don't bother):**
- Button colors
- Font sizes
- Minor copy tweaks
- Non-critical pages

---

## A/B Testing

### When to A/B Test

**Good candidates:**
- Changes to high-traffic pages
- Unclear which option is better
- Risk of negative impact
- Need to prove hypothesis

**Don't A/B test:**
- Low traffic (won't reach significance)
- Obviously broken things (just fix)
- Minor changes (not worth effort)
- Complex features (use qualitative)

### A/B Test Process

```
1. HYPOTHESIS
   "If we [change], then [metric] will [improve] because [reason]"

2. DESIGN
   - Control: Current version
   - Variant: Changed version
   - Metric: Primary + secondary
   - Sample size needed
   - Duration estimate

3. IMPLEMENT
   - Build variant
   - Set up tracking
   - QA both versions
   - Launch to % of traffic

4. RUN
   - Wait for significance
   - Don't peek too often
   - Monitor for bugs

5. ANALYZE
   - Was it significant?
   - What was the lift?
   - Any segment differences?

6. DECIDE
   - Winner: Roll out
   - Loser: Document and move on
   - Inconclusive: Extend or kill
```

### Sample Size Calculator

```
n = (16 × p × (1-p)) / (lift)²

Where:
- p = baseline conversion rate
- lift = minimum detectable effect

Example:
- Baseline: 5% conversion
- Want to detect: 20% relative lift (5% → 6%)
- n = (16 × 0.05 × 0.95) / (0.01)² = 7,600 per variant
```

### Statistical Significance

| Confidence | p-value | When to Use |
|------------|---------|-------------|
| 90% | p < 0.10 | Directional insight |
| 95% | p < 0.05 | Standard decision |
| 99% | p < 0.01 | High-stakes changes |

**Rule of thumb:** Don't call it until 95% confidence.

---

## Conversion Rate Optimization (CRO)

### Conversion Funnel Analysis

```
Visitors → Landing → Signup → Activation → Conversion

Track drop-off at each stage:
100% → 40% → 15% → 8% → 2%

Find biggest % drop = biggest opportunity
```

### Landing Page Optimization

| Element | Test Ideas |
|---------|------------|
| Headline | Value prop variants |
| CTA | Copy, color, placement |
| Social proof | With/without, type |
| Form | Fields, steps |
| Hero image | With/without, type |

### Signup Flow Optimization

| Element | Test Ideas |
|---------|------------|
| Form fields | Fewer vs more |
| Social login | With/without |
| Progress indicator | With/without |
| Value reminder | During signup |

### Pricing Page Optimization

| Element | Test Ideas |
|---------|------------|
| Tier names | Different positioning |
| Price anchoring | Order of tiers |
| Feature display | What to highlight |
| CTA copy | Different urgency |
| FAQ | What to include |

---

## Qualitative Methods

### User Interviews

**When:**
- Understanding why (not just what)
- Exploring new ideas
- Debugging low conversion

**Questions:**
- "Walk me through your experience..."
- "What were you trying to accomplish?"
- "What was confusing?"
- "What almost made you leave?"

### Session Recordings

**Watch for:**
- Rage clicks
- Hesitation points
- Abandonment moments
- Navigation confusion

**Tools:** Hotjar, FullStory, PostHog

### Surveys

**Types:**
| Type | When | Questions |
|------|------|-----------|
| Exit survey | User leaves | "Why are you leaving?" |
| NPS | After value | "How likely to recommend?" |
| Feature | Using feature | "How useful was this?" |
| Onboarding | After setup | "How easy was setup?" |

---

## ICE Prioritization

### Framework

| Factor | Question | Score |
|--------|----------|-------|
| **Impact** | How much will this move the metric? | 1-10 |
| **Confidence** | How sure are we it'll work? | 1-10 |
| **Ease** | How easy is it to implement? | 1-10 |

**ICE Score = (I + C + E) / 3**

### Scoring Guide

**Impact:**
- 10: 50%+ improvement
- 7-9: 20-50% improvement
- 4-6: 10-20% improvement
- 1-3: <10% improvement

**Confidence:**
- 10: Proven elsewhere, data supports
- 7-9: Strong hypothesis, good evidence
- 4-6: Reasonable hypothesis
- 1-3: Just a guess

**Ease:**
- 10: Hours to implement
- 7-9: Days
- 4-6: Weeks
- 1-3: Months

### Example ICE Table

| Experiment | Impact | Confidence | Ease | Score |
|------------|--------|------------|------|-------|
| Simplify signup form | 7 | 8 | 9 | 8.0 |
| Add social proof | 6 | 7 | 9 | 7.3 |
| Redesign pricing page | 8 | 5 | 4 | 5.7 |
| Change CTA color | 2 | 3 | 10 | 5.0 |

---

## Experimentation Velocity

### Running More Experiments

**Bottleneck:** Usually it's time and traffic

**Solutions:**
- Run tests simultaneously (different pages)
- Use smaller samples for directional insights
- Pre-launch tests (design review, 5-user tests)
- Reduce scope of each test

### Experiment Cadence

| Stage | Tests/Month | Focus |
|-------|-------------|-------|
| Pre-PMF | 2-4 | Big directional bets |
| Early growth | 4-8 | Funnel optimization |
| Scale | 8-16 | Continuous improvement |

---

## Documentation

### Experiment Log Template

```markdown
## Experiment: {Name}

**Date:** {start} - {end}
**Page/Flow:** {where}

### Hypothesis
If we {change}, then {metric} will {improve} because {reason}.

### Setup
- Control: {description}
- Variant: {description}
- Primary metric: {metric}
- Sample size: {n per variant}

### Results
| Variant | Conversions | Rate | vs Control |
|---------|-------------|------|------------|
| Control | {n} | {%} | - |
| Variant | {n} | {%} | {+/-X%} |

**Confidence:** {%}

### Decision
{Ship / Kill / Extend}

### Learnings
{What we learned, regardless of outcome}
```

---

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Peeking | False positives | Wait for full sample |
| Testing everything | Nothing conclusive | Focus on high-impact |
| No hypothesis | Can't learn | Always have one |
| Testing tiny changes | Waste of time | Test big changes |
| No documentation | Lost learnings | Log everything |
| Shipping losers | Harm users | Respect results |

---

## Output Format

```markdown
## Optimization Plan

### Current Funnel
| Stage | Rate | vs Benchmark |
|-------|------|--------------|
| {stage} | {%} | {🟢/🟡/🔴} |

### Biggest Opportunity
**Stage:** {where}
**Current:** {rate}
**Potential:** {rate if improved}
**Impact:** {$ or users}

### Experiment Queue
| Priority | Experiment | ICE | Status |
|----------|------------|-----|--------|
| 1 | {exp} | {score} | {status} |
| 2 | {exp} | {score} | {status} |
| 3 | {exp} | {score} | {status} |

### Active Experiments
| Experiment | Started | Est. Complete | Metric |
|------------|---------|---------------|--------|
| {exp} | {date} | {date} | {metric} |

### Recent Results
| Experiment | Result | Lift | Shipped |
|------------|--------|------|---------|
| {exp} | {W/L} | {%} | {Y/N} |
```
