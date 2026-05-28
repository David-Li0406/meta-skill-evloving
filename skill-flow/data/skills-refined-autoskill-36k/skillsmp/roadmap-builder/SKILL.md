---
name: Roadmap Builder
description: Ruthless feature prioritization using Impact vs Effort matrix and stage-based rules. Prevents feature creep by focusing on retention → core features → monetization → growth. Challenges ideas with validation questions before building.
---

# Roadmap Builder Skill

## Purpose

Helps you decide what to build next by applying ruthless prioritization. Prevents feature creep and keeps you focused on what actually moves the needle for your product.

**Philosophy**: Ship less, validate more. Build for real users, not imaginary ones.

## When to Use

Use this skill to:
- **Prioritize roadmap** - Decide what to build next
- **Challenge feature ideas** - Validate before building
- **Review backlog** - Cut features that don't matter
- **Stage transitions** - Adjust priorities as you grow
- **User requests** - Filter signal from noise

## Prioritization Framework

### Impact vs Effort Matrix

**Scoring System**:
- **Impact**: 1-10 (How much does this move key metrics?)
- **Effort**: 1-10 (Time, complexity, risk)
- **Priority Score**: Impact / Effort

```
High Impact, Low Effort (Score: 5-10)
├─ BUILD NOW - Quick wins, massive value
└─ Examples: Fix critical bug, add login, improve onboarding

High Impact, High Effort (Score: 1-2)
├─ BUILD LATER - Big projects, plan carefully
└─ Examples: New platform, major feature, infrastructure rewrite

Low Impact, Low Effort (Score: 2-5)
├─ MAYBE - Nice to haves, fill gaps
└─ Examples: UI polish, minor improvements, small tweaks

Low Impact, High Effort (Score: <1)
├─ DON'T BUILD - Waste of time
└─ Examples: Premature optimization, edge cases, vanity features
```

### Category Prioritization (In Order)

**1. Retention (Highest Priority)**
- Features that keep users coming back
- Reduce churn, increase engagement
- Fix pain points in existing experience

**Examples**:
- Email reminders for inactive users
- Improve core workflow speed
- Fix frustrating bugs
- Better mobile experience

**2. Core Features (High Priority)**
- Essential functionality for main use case
- Features that unlock more users
- Remove blockers to adoption

**Examples**:
- Critical integrations (Google, Stripe)
- Key workflows that users expect
- Platform parity (web → mobile)

**3. Monetization (Medium Priority)**
- Features that directly generate revenue
- Upgrade incentives for free users
- Reduce payment friction

**Examples**:
- Premium features
- Usage limits for free tier
- Better billing UX
- Enterprise features

**4. Growth (Lower Priority)**
- Features that bring new users
- Viral loops, referrals, sharing
- SEO, content, marketing tools

**Examples**:
- Social sharing
- Referral program
- Public profiles
- Embeds

## Stage-Based Rules

### Pre-Launch (0 users)

**ONLY build**: Core loop features
- Minimum viable product
- Essential user flow
- One use case done well

**DO NOT build**:
- Settings pages
- Advanced features
- Edge cases
- Integrations
- Analytics dashboards
- Admin panels

**Focus**: Get to launchable state ASAP

✅ **Good Pre-Launch Roadmap**:
```
1. User auth (login/signup)
2. Core feature (the ONE thing your app does)
3. Basic UI that works
4. Deploy and launch
```

❌ **Bad Pre-Launch Roadmap**:
```
1. Advanced settings
2. Multiple themes
3. Social sharing
4. Analytics
5. Admin dashboard
6. API
7. Integrations
(Never actually launches)
```

### Post-Launch (1-100 users)

**ONLY build**: Features users explicitly request
- Listen to real feedback
- Fix reported bugs
- Improve existing features

**DO NOT build**:
- Features you think they need
- Features competitors have
- Cool ideas you had

**Focus**: Make early users love it

✅ **Good Post-Launch Prioritization**:
```
User: "I can't export my data"
You: Add export feature (directly requested)

User: "The app is slow on mobile"
You: Optimize mobile performance (retention)
```

❌ **Bad Post-Launch Prioritization**:
```
You: "Let's add dark mode!" (nobody asked)
You: "We need social features!" (imaginary need)
You: "Competitor has X, we need it too!" (not validated)
```

### Growth Phase (100+ users)

**ONLY build**: Features that reduce churn OR increase sharing
- Data-driven decisions
- A/B test before building
- Measure impact

**DO NOT build**:
- Features <5% of users request
- Features with unclear metrics
- Vanity features

**Focus**: Scale what works

✅ **Good Growth Prioritization**:
```
Data: 30% of users churn after day 3
You: Improve day 3 onboarding (retention)

Data: Users who invite friends have 5x retention
You: Make inviting easier (growth)
```

❌ **Bad Growth Prioritization**:
```
You: "Let's rebuild in React!" (no user impact)
You: "We need blockchain integration!" (vanity)
```

## Validation Questions

### Ask These About EVERY Feature Idea:

#### 1. Does this serve the core use case?
- **Yes**: Might be worth building
- **No**: Probably distraction

**Example**:
```
Idea: Add chat feature to a to-do app
Question: Does chat help people manage tasks?
Answer: No, it's a different use case
Decision: ❌ Skip it
```

#### 2. Will users actually use this or just say they want it?
- **Actually use**: Look for existing workarounds, pain points
- **Just say**: Hypothetical, "nice to have", no urgency

**Example**:
```
User: "It would be cool to have custom themes"
You: "How often would you change themes?"
User: "Maybe once when I set it up"
Decision: ⚠️ Low priority - not actually needed
```

#### 3. Can we fake it first to validate demand?

**Fake It Techniques**:
- **Manual process**: Do it by hand before automating
- **Waitlist**: "Coming soon" for feature validation
- **Button test**: Add button, see if anyone clicks
- **Concierge**: White-glove service before building product

**Example**:
```
Idea: Automated report generation
Fake it: Send reports manually for 10 users
Learn: Which reports do they actually read?
Then: Build automation only for used reports
```

### Red Flag Detection

#### 🚩 Feature Creep
**Signs**:
- "Wouldn't it be cool if..."
- "Competitor has this..."
- "This would be easy to add..."
- Feature list keeps growing, never shipping

**Fix**: Apply Impact/Effort score. If <5, don't build.

#### 🚩 Premature Optimization
**Signs**:
- "We need to scale to 1M users"
- "Let's rewrite for performance"
- No actual performance problems yet

**Fix**: Wait until you have the problem. Optimize when real users complain.

#### 🚩 Building for Imaginary Users
**Signs**:
- "Users will want..."
- "People might need..."
- No direct user requests
- No data supporting need

**Fix**: Talk to 5 real users. If none care, don't build.

## Decision Framework

### Feature Evaluation Template

```
Feature: [Name]
Requested by: [Real user quote or "Internal idea"]
Stage: [Pre-launch | Post-launch | Growth]

IMPACT (1-10):
├─ Retention: [Score] - [Explanation]
├─ Revenue: [Score] - [Explanation]
└─ Growth: [Score] - [Explanation]
Total Impact: [Sum/3]

EFFORT (1-10):
├─ Time: [Days/Weeks]
├─ Complexity: [1-10]
└─ Risk: [1-10]
Total Effort: [Average]

PRIORITY SCORE: [Impact / Effort]

VALIDATION:
├─ Serves core use case? [Yes/No]
├─ Users will actually use? [Yes/No/Maybe]
└─ Can we fake it first? [Yes/No]

RED FLAGS:
├─ Feature creep? [Yes/No]
├─ Premature optimization? [Yes/No]
└─ Imaginary users? [Yes/No]

DECISION: [Build Now | Build Later | Maybe | Skip]
```

## Examples

### Example 1: Should Build

```
Feature: Email notifications for new comments
Requested by: 15 users directly asked for this
Stage: Post-launch (50 users)

IMPACT (1-10):
├─ Retention: 8 - Users miss replies, forget to come back
├─ Revenue: 3 - Doesn't directly affect monetization
└─ Growth: 5 - More engagement could lead to referrals
Total Impact: 5.3

EFFORT (1-10):
├─ Time: 2 days
├─ Complexity: 3 - Use email service, simple templates
└─ Risk: 2 - Low risk, standard feature
Total Effort: 2.3

PRIORITY SCORE: 5.3 / 2.3 = 2.3 (Medium priority)

VALIDATION:
├─ Serves core use case? Yes - commenting is core feature
├─ Users will actually use? Yes - explicitly requested by many
└─ Can we fake it first? Already doing it (user pain point)

RED FLAGS:
├─ Feature creep? No - directly serves retention
├─ Premature optimization? No - real user need
└─ Imaginary users? No - 15 real users requested it

DECISION: ✅ Build Now (High impact on retention, low effort)
```

### Example 2: Should Skip

```
Feature: AI-powered task suggestions
Requested by: Internal idea, "users might like it"
Stage: Pre-launch (0 users)

IMPACT (1-10):
├─ Retention: 2 - Unproven, might annoy users
├─ Revenue: 1 - No monetization impact
└─ Growth: 3 - Could be interesting for marketing
Total Impact: 2.0

EFFORT (1-10):
├─ Time: 3-4 weeks
├─ Complexity: 9 - AI integration, training, testing
└─ Risk: 8 - Quality concerns, API costs, uncertainty
Total Effort: 8.7

PRIORITY SCORE: 2.0 / 8.7 = 0.23 (Very low priority)

VALIDATION:
├─ Serves core use case? No - task management works without AI
├─ Users will actually use? Unknown - no user validation
└─ Can we fake it first? Yes - could manually suggest tasks

RED FLAGS:
├─ Feature creep? Yes - "cool" but not essential
├─ Premature optimization? Yes - no users yet
└─ Imaginary users? Yes - assuming users want AI

DECISION: ❌ Skip It (Low impact, high effort, pre-launch)

ALTERNATIVE: Launch without AI. If users ask for suggestions,
manually send them ideas. If >50% engage, then consider AI.
```

### Example 3: Maybe Later

```
Feature: Mobile app (native iOS/Android)
Requested by: 8 users mentioned "would be nice"
Stage: Post-launch (150 users, responsive web app exists)

IMPACT (1-10):
├─ Retention: 7 - Better mobile experience could help
├─ Revenue: 4 - Might unlock mobile-first users
└─ Growth: 6 - App store presence helps discovery
Total Impact: 5.7

EFFORT (1-10):
├─ Time: 8-12 weeks for MVP
├─ Complexity: 9 - New platform, app store, maintenance
└─ Risk: 7 - Resource intensive, ongoing maintenance
Total Effort: 8.3

PRIORITY SCORE: 5.7 / 8.3 = 0.69 (Low priority)

VALIDATION:
├─ Serves core use case? Yes - accessibility improvement
├─ Users will actually use? Maybe - web app works already
└─ Can we fake it first? Already doing it (responsive web)

RED FLAGS:
├─ Feature creep? Maybe - web app might be enough
├─ Premature optimization? Maybe - web could improve first
└─ Imaginary users? Partially - only 8 mentioned it

DECISION: ⏸️ Build Later

REASONING: High effort for uncertain gain.
NEXT STEPS:
1. Track web app mobile usage (are users struggling?)
2. Improve mobile web experience first
3. If >30% of users are mobile AND churn is high, reconsider
4. Consider PWA (progressive web app) as middle ground
```

### Example 4: Fake It First

```
Feature: Automated weekly report emails
Requested by: 3 users asked for "progress summaries"
Stage: Post-launch (80 users)

IMPACT (1-10):
├─ Retention: 6 - Could remind users to come back
├─ Revenue: 3 - Might help conversions
└─ Growth: 2 - Not a growth driver
Total Impact: 3.7

EFFORT (1-10):
├─ Time: 1 week to build automation
├─ Complexity: 5 - Email templates, scheduling, data aggregation
└─ Risk: 4 - Medium complexity
Total Effort: 4.7

PRIORITY SCORE: 3.7 / 4.7 = 0.79 (Low-medium priority)

VALIDATION:
├─ Serves core use case? Maybe - tangential to core feature
├─ Users will actually use? Unknown - might just delete emails
└─ Can we fake it first? YES!

RED FLAGS:
├─ Feature creep? Possibly - not sure if needed
├─ Premature optimization? No - small effort
└─ Imaginary users? Partially - only 3 users mentioned

DECISION: 🧪 Fake It First

ACTION PLAN:
1. Manually send weekly summaries to 10 users
2. Track open rates and engagement
3. Ask recipients: "Would you want this automated?"
4. If >50% open AND engage, build automation
5. If <50%, drop the idea

RESULT: Spend 2 hours testing vs 1 week building something nobody wants.
```

## Roadmap Template

### Quarterly Roadmap Structure

```
Q[X] [Year] - [Stage Name]

🎯 NORTH STAR METRIC: [What we're optimizing for]
Example: DAU (Daily Active Users), Retention Rate, MRR

📊 CURRENT STATE:
├─ Users: [number]
├─ Key Metric: [number]
└─ Biggest Problem: [user pain point]

🚀 THIS QUARTER'S FOCUS:

1. RETENTION (Must Build)
   ├─ [Feature 1] - Impact: X, Effort: Y, Score: Z
   ├─ [Feature 2] - Impact: X, Effort: Y, Score: Z
   └─ Why: [How this improves retention]

2. CORE FEATURES (Should Build)
   ├─ [Feature 3] - Impact: X, Effort: Y, Score: Z
   └─ Why: [How this unlocks users]

3. MONETIZATION (Nice to Have)
   ├─ [Feature 4] - Impact: X, Effort: Y, Score: Z
   └─ Why: [How this drives revenue]

4. GROWTH (If Time Allows)
   └─ [Feature 5] - Impact: X, Effort: Y, Score: Z

📋 BACKLOG (Not Building Yet):
├─ [Deferred Feature 1] - Why: Low priority score
├─ [Deferred Feature 2] - Why: Need validation first
└─ [Deferred Feature 3] - Why: Premature optimization

❌ NOT BUILDING (Ever):
├─ [Rejected Feature 1] - Why: Feature creep
├─ [Rejected Feature 2] - Why: Imaginary users
└─ [Rejected Feature 3] - Why: Low impact, high effort

🧪 VALIDATION EXPERIMENTS:
├─ [Test 1] - Fake it before building
└─ [Test 2] - A/B test to validate demand
```

### Example Roadmap

```
Q1 2025 - Post-Launch Growth

🎯 NORTH STAR METRIC: 7-day Retention Rate
Current: 40% | Goal: 55%

📊 CURRENT STATE:
├─ Users: 250
├─ 7-day Retention: 40%
└─ Biggest Problem: Users sign up but don't complete setup

🚀 THIS QUARTER'S FOCUS:

1. RETENTION (Must Build)
   ├─ Improve onboarding flow - Impact: 9, Effort: 3, Score: 3.0
   │  └─ Why: 60% of users abandon during setup
   ├─ Email nudges for inactive users - Impact: 7, Effort: 2, Score: 3.5
   │  └─ Why: Users forget to come back after day 1
   └─ Mobile web optimization - Impact: 8, Effort: 4, Score: 2.0
      └─ Why: 45% of traffic is mobile, experience is poor

2. CORE FEATURES (Should Build)
   ├─ Google Calendar integration - Impact: 7, Effort: 5, Score: 1.4
   │  └─ Why: 30 users requested it, unlocks power users
   └─ Bulk actions - Impact: 6, Effort: 2, Score: 3.0
      └─ Why: Users with >50 items struggle with UI

3. MONETIZATION (Nice to Have)
   └─ Premium plan page - Impact: 5, Effort: 3, Score: 1.7
      └─ Why: Need upgrade path before hitting free limits

4. GROWTH (If Time Allows)
   └─ Public sharing - Impact: 4, Effort: 6, Score: 0.67
      └─ Why: Could drive referrals, but unproven

📋 BACKLOG (Not Building Yet):
├─ Dark mode - Score: 0.5 (low priority, nice to have)
├─ API access - Score: 0.8 (too early, no demand yet)
└─ Team features - Score: 1.2 (B2B pivot, need validation)

❌ NOT BUILDING (Ever):
├─ Blockchain integration - Why: Feature creep, no user need
├─ AI predictions - Why: Premature, no data yet
└─ Gamification - Why: Distraction from core use case

🧪 VALIDATION EXPERIMENTS:
├─ Test premium pricing - Show upgrade CTA to 50 users, measure clicks
└─ Test sharing - Add "Share" button, track usage before building feature
```

## Integration with Other Skills

1. **Idea Validator** → Validate idea is worth building at all
2. **Roadmap Builder** → Decide what to build and when
3. **Design Guide** → Build it with modern UI
4. **Confidence Check** → Verify technical approach before coding

## Quick Decision Flowchart

```
New Feature Idea
     ↓
Is it core use case? → No → ❌ Skip
     ↓ Yes
What stage are you in?
     ↓
┌────┼────┐
Pre   Post  Growth
↓     ↓     ↓
Core  User  Data
Only  Asked Driven
↓     ↓     ↓
Calculate Impact/Effort Score
     ↓
Score > 2? → No → 📋 Backlog
     ↓ Yes
Can fake first? → Yes → 🧪 Test
     ↓ No
Any red flags? → Yes → ❌ Skip
     ↓ No
✅ Build It
```

## Common Pitfalls

### ❌ Building Too Much

**Symptom**: Roadmap has 50 items for next quarter
**Fix**: Pick top 3-5 by priority score. Defer rest.

### ❌ Building Too Little

**Symptom**: Shipping one tiny feature per month
**Fix**: Increase effort estimates may be too conservative. Ship weekly.

### ❌ Ignoring User Requests

**Symptom**: Building internal ideas, ignoring feedback
**Fix**: Post-launch, ONLY build what users request.

### ❌ Building Every Request

**Symptom**: Saying yes to every user suggestion
**Fix**: Apply validation questions. Most requests aren't worth building.

### ❌ Analysis Paralysis

**Symptom**: Endless planning, no shipping
**Fix**: Make decision in 15 minutes. Build or skip, don't overthink.

## Metrics to Track

### Pre-Launch
- Days until launch
- Core features complete
- Blocker count

### Post-Launch
- User requests count
- Bug reports
- Feature usage rates
- Churn points

### Growth
- Retention by cohort
- Feature adoption rates
- Request frequency (top 5 requests)
- Time from idea → ship

## Summary

**Golden Rules**:
1. Pre-launch: Core only
2. Post-launch: Users only
3. Growth: Data only
4. Impact/Effort > 2 = Build
5. Can't fake it? Build
6. Fake it? Test first
7. Red flags? Skip

**Remember**: Your roadmap is what you say NO to, not what you say yes to. Ruthlessly cut features that don't move the needle.
