# Retention Framework

## Purpose

Keep users coming back. Retention is the foundation of sustainable growth—without it, acquisition is pouring water into a leaky bucket.

---

## Why Retention Matters

### The Math

```
Scenario A: 10% monthly churn
- Month 0: 1000 users
- Month 6: 531 users
- Month 12: 282 users

Scenario B: 5% monthly churn
- Month 0: 1000 users
- Month 6: 735 users
- Month 12: 540 users
```

**Small retention improvements have huge compounding effects.**

### Retention vs Acquisition

| Factor | Acquisition | Retention |
|--------|-------------|-----------|
| Cost | 5-25x more expensive | Cheaper |
| Impact | Linear | Compounding |
| Focus | New users | Existing users |
| Timing | Early stage | All stages |

---

## Retention Metrics

### Time-Based Retention

| Metric | Formula | What it Shows |
|--------|---------|---------------|
| D1 | Users Day 1 / Signups | First experience |
| D7 | Users Day 7 / Signups | Short-term value |
| D30 | Users Day 30 / Signups | Product-market fit |
| D90 | Users Day 90 / Signups | Long-term stickiness |

### Engagement Metrics

| Metric | Formula | What it Shows |
|--------|---------|---------------|
| DAU/MAU | Daily / Monthly users | Engagement intensity |
| Sessions/user | Total sessions / Users | Usage frequency |
| Time in app | Avg session duration | Engagement depth |
| Actions/session | Actions / Sessions | Engagement quality |

### Churn Metrics

| Metric | Formula | What it Shows |
|--------|---------|---------------|
| Monthly churn | Lost / Start of month | Customer loss rate |
| Revenue churn | Lost MRR / Start MRR | Revenue loss rate |
| Net churn | (Lost - Expansion) / Start | Net customer change |

---

## Retention Benchmarks

### By Product Type

| Product Type | D1 | D7 | D30 |
|--------------|----|----|-----|
| Social | 25-30% | 15-20% | 8-15% |
| SaaS | 30-40% | 20-30% | 15-25% |
| Productivity | 20-30% | 10-20% | 5-15% |
| Gaming | 35-45% | 20-30% | 10-20% |

### DAU/MAU Benchmarks

| Ratio | Meaning |
|-------|---------|
| < 10% | Low engagement |
| 10-20% | Average |
| 20-30% | Good |
| 30-50% | Very engaged |
| > 50% | Daily habit |

---

## Retention Levers

### The Retention Equation

```
Retention = Value + Habit - Friction - Competition
```

### 1. Increase Value

**Strategies:**
- Deliver core value faster
- Add features users want
- Improve existing features
- Personalization

**Questions:**
- What's the "aha moment"?
- How fast do users get there?
- What makes users stay?

### 2. Build Habit

**Hook Model:**
```
Trigger → Action → Variable Reward → Investment
```

**Internal triggers:**
- Boredom
- Fear of missing out
- Anxiety
- Seeking validation

**External triggers:**
- Notifications
- Emails
- Calendar events

### 3. Reduce Friction

**Common friction points:**
- Slow loading
- Complex UI
- Too many steps
- Confusing navigation
- Bugs and errors

**How to find friction:**
- Watch session recordings
- Talk to churned users
- Track drop-off points

### 4. Beat Competition

**Switching costs:**
- Data lock-in
- Learning curve
- Social network
- Integrations
- Content created

---

## Onboarding Optimization

### First Session Critical

```
New User → First Value → Setup Complete → Habit Formed
```

### Onboarding Checklist

**Must have:**
- [ ] Clear next step always visible
- [ ] Quick win in first session
- [ ] Progress indication
- [ ] Skip option for experienced users

**Should have:**
- [ ] Personalized path
- [ ] Sample data/templates
- [ ] Contextual help
- [ ] Success celebration

### Measuring Onboarding

| Metric | Target |
|--------|--------|
| Time to first value | < 5 minutes |
| Onboarding completion | > 60% |
| Setup completion | > 40% |
| First session retention | > 70% |

---

## Re-engagement Strategies

### Email Campaigns

| Trigger | Email | Timing |
|---------|-------|--------|
| Signed up, no activation | "Need help getting started?" | Day 1 |
| Used once, dropped off | "Did you know about X?" | Day 3 |
| Was active, now inactive | "We miss you" | Day 7 |
| About to churn | Win-back offer | Day 14 |

### Notification Strategy

| Type | Use For | Don't Overuse |
|------|---------|---------------|
| Transactional | Confirmations, alerts | Never |
| Engagement | New content, features | 1-2/week |
| Re-activation | Inactive users | 1/week max |
| Marketing | Promotions | Monthly |

### In-App Engagement

- Feature announcements
- Tips and suggestions
- Progress celebrations
- Social proof

---

## Churn Analysis

### Understanding Why Users Leave

**Methods:**
1. Exit surveys
2. Churn interviews
3. Usage pattern analysis
4. Support ticket analysis

### Common Churn Reasons

| Reason | Signal | Solution |
|--------|--------|----------|
| Didn't get value | Low usage before churn | Improve onboarding |
| Too complex | High error rate | Simplify UX |
| Missing feature | Feature request before churn | Roadmap communication |
| Found alternative | Competitor mention | Competitive positioning |
| Price | Price objection | Pricing/value alignment |
| No longer needed | Business change | Expand use cases |

### Churn Prediction

**High-risk signals:**
- Usage decline
- No login in X days
- Reduced feature usage
- Support frustration
- Downgrade inquiry

---

## Cohort Analysis

### Building Retention Cohorts

```sql
-- Weekly retention cohort
SELECT
  date_trunc('week', signup_date) as cohort,
  date_trunc('week', activity_date) as activity_week,
  COUNT(DISTINCT user_id) as users
FROM user_activity
GROUP BY 1, 2
ORDER BY 1, 2;
```

### Reading Cohorts

**Look for:**
- Are later cohorts improving?
- Where is the biggest drop-off?
- When does retention stabilize?

**Action based on findings:**
- Early drop-off → Onboarding problem
- Late drop-off → Value problem
- All cohorts similar → Systemic issue
- Improving cohorts → Changes working

---

## Retention Experiments

### High-Impact Tests

| Experiment | Expected Impact | Effort |
|------------|-----------------|--------|
| Reduce time to value | High | Medium |
| Add onboarding checklist | Medium-High | Low |
| Re-engagement emails | Medium | Low |
| Feature discovery prompts | Medium | Low |
| Simplify core action | High | Medium |

### Testing Process

```
1. Hypothesis: {change} will improve {metric} by {X}%
2. Metric: {specific retention metric}
3. Segment: {who to test on}
4. Duration: {how long}
5. Sample size: {minimum needed}
```

---

## Output Format

```markdown
## Retention Analysis

### Current State
| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| D1 | {%} | {%} | {🟢/🟡/🔴} |
| D7 | {%} | {%} | {🟢/🟡/🔴} |
| D30 | {%} | {%} | {🟢/🟡/🔴} |
| Monthly churn | {%} | {%} | {🟢/🟡/🔴} |

### Biggest Drop-off
**Stage:** {where users drop}
**Cause:** {why - based on analysis}
**Solution:** {proposed fix}

### Retention Levers
1. **Value:** {improvement}
2. **Habit:** {trigger to add}
3. **Friction:** {friction to remove}

### Experiments
| Experiment | Hypothesis | Priority |
|------------|------------|----------|
| {exp} | {hypothesis} | {H/M/L} |

### 30-Day Plan
Week 1: {focus}
Week 2: {focus}
Week 3: {focus}
Week 4: {focus}
```
