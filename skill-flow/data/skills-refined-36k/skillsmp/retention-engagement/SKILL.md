---
name: retention-engagement
description: Build habit-forming products using Hook Model (trigger-action-reward-investment), cohort analysis, feature adoption tracking, and re-engagement strategies. Turn one-time users into daily/weekly active users with sustainable retention mechanics.
---

# Retention & Engagement Strategies

Build products users return to regularly through habit formation, engagement loops, and retention mechanics.

## When to Use

- Day 30 retention is weak (<20%)
- Users activate but don't return
- High churn rate
- Low DAU/MAU ratio (<20%)
- Need to build habit-forming product
- Designing features to increase stickiness
- Re-engaging dormant users

## Core Concept

**Retention is the foundation of growth.** Without retention, acquisition is pouring water into a leaky bucket.

**Key Framework: The Hook Model** (Nir Eyal)
1. **Trigger** - Internal or external cue to use product
2. **Action** - Simplest behavior in anticipation of reward
3. **Reward** - Variable reward that satisfies need
4. **Investment** - User puts something in, increasing likelihood of return

---

## Workflow

### Step 1: Diagnose Retention Problems

```markdown
## Retention Diagnostic Framework

**COHORT ANALYSIS:**
Track retention by cohort (signup week/month):
- D1, D7, D30, D60, D90 retention rates
- Look for: When does curve flatten? Is it improving cohort-over-cohort?

**BENCHMARKS:**
| Product Type | Good D30 | Strong D30 | Good DAU/MAU | Strong DAU/MAU |
|--------------|----------|------------|--------------|----------------|
| Social | 25% | 40%+ | 20% | 40%+ |
| Content | 20% | 35%+ | 15% | 30%+ |
| Productivity | 30% | 50%+ | 25% | 45%+ |
| B2B SaaS | 60% | 80%+ | 30% | 50%+ |

**RED FLAGS:**
❌ Curve never flattens (continuous decline)
❌ Retention getting worse cohort-over-cohort
❌ DAU/MAU <10% (low habit formation)
❌ Resurrection rate <5% (users don't come back once churned)

**DIAGNOSE THE PROBLEM:**

IF retention drops immediately (D1-D7):
→ Onboarding problem. Users don't reach aha moment.
→ Fix: Improve activation flow (see `/user-onboarding`)

IF retention drops gradually (D7-D30):
→ Lack of habit formation. No reason to return.
→ Fix: Build engagement loops, triggers, rewards

IF retention plateaus but low (<20%):
→ Product is nice-to-have, not must-have.
→ Fix: Deepen value prop, add use cases, improve core product

IF retention drops suddenly after plateau:
→ External factor (competitor, market shift, seasonal)
→ Fix: Win-back campaign, feature parity with competitor
```

---

### Step 2: Build The Hook (Habit Loop)

**Apply Nir Eyal's Hook Model:**

```markdown
## Hook Model Implementation

### COMPONENT 1: Trigger (Why do users return?)

**EXTERNAL TRIGGERS (Get them back):**
- Email: Daily digest, milestone achieved, social activity
- Push: New content, friend activity, reminder
- SMS: Time-sensitive (appointments, deadlines)
- In-app: Badge notifications, unread counts

**INTERNAL TRIGGERS (Habit formed):**
- Emotional state: Bored → Instagram, Lonely → Twitter
- Situational: Commute → Podcast, Morning → News
- Goal: Learn → Duolingo, Fit → Fitness app

**BEST PRACTICES:**
✅ Use external triggers early (email/push) to create habit
✅ Reduce external triggers as internal triggers form
✅ Make triggers valuable (not spammy)
✅ Personalize based on user behavior

❌ Don't spam (multiple emails/day)
❌ Don't send generic "We miss you" (be specific)
❌ Don't trigger without value (no reason to return)

---

### COMPONENT 2: Action (Make it easy)

**Simplify the return action:**
- Deep link to relevant content (not homepage)
- Show new activity immediately (not empty state)
- Reduce friction (stay logged in, magic links)
- Mobile-optimized (most returns happen on mobile)

**Formula:** Motivation × Ability × Trigger = Action
- High motivation + Low ability = Action happens
- Low motivation + Low ability = Needs strong trigger
- Low motivation + High ability = Won't happen

**EXAMPLES:**
✅ Twitter: Tap notification → see reply immediately
✅ Slack: Push says "John mentioned you" → tap → direct to message
✅ LinkedIn: "You appeared in 15 searches" → tap → see who viewed

❌ Generic: "You have updates" → tap → login wall → homepage

---

### COMPONENT 3: Reward (Variable reinforcement)

**Types of Variable Rewards:**

1. **Rewards of the Tribe** (Social validation)
   - Likes, comments, shares
   - Followers, connections
   - Leaderboards, badges

2. **Rewards of the Hunt** (Material gain)
   - Discovering new content/products
   - Earning points, coins, rewards
   - Unlocking features, levels

3. **Rewards of the Self** (Mastery)
   - Completing task, checking off item
   - Leveling up skill, hitting milestone
   - Streak maintenance, progress bars

**CRITICAL:** Rewards must be **variable** (unpredictable).
- Fixed reward: "Check email, nothing new" → boring
- Variable reward: "Check email, might have interesting message" → addictive

**EXAMPLES:**
✅ Instagram: Variable reward (feed shows different content each time)
✅ Duolingo: Variable reward (lessons vary, streaks gamified)
✅ LinkedIn: Variable reward ("You appeared in X searches" varies)

❌ Fixed: Same content every time you open app (boring)

---

### COMPONENT 4: Investment (Commitment increases)

**Get users to invest so they return:**
- Add content (photos, posts, tasks)
- Build profile (bio, preferences, settings)
- Connect accounts (integrations, imports)
- Invite others (network effects)
- Customize (personalization, saved preferences)

**Why it works:** Sunk cost fallacy. The more they invest, the more they value it.

**EXAMPLES:**
✅ Notion: You build elaborate workspace → can't leave
✅ Spotify: You curate playlists → invested in content
✅ GitHub: You host repos → locked in by data

**TIMING:** Ask for investment AFTER reward (not before).
- Bad: "Set up profile before using app" (friction)
- Good: "You just completed first task! Add more tasks?" (investment after reward)
```

---

### Step 3: Feature Adoption Strategies

```markdown
## Drive Feature Adoption

**WHY IT MATTERS:**
- More features used = Higher retention
- Users who use 3+ features → 2x retention vs. 1 feature

**FEATURE ADOPTION FUNNEL:**
1. Aware (know feature exists) → 80% of users
2. Tried (used once) → 40% of aware users
3. Adopted (used 3+ times) → 20% of tried users
4. Habitual (use weekly) → 10% of adopted users

**TACTICS TO INCREASE ADOPTION:**

1. **Contextual Discovery**
   - Show feature when relevant (not random tooltip)
   - Example: Slack shows "Add reaction" when hovering over message

2. **Progressive Disclosure**
   - Introduce one new feature per session
   - Duolingo unlocks new lesson types gradually

3. **Social Proof**
   - "3 teammates are using [feature]"
   - "Most popular feature for teams like yours"

4. **Quick Win**
   - Let users get value from feature in <2 minutes
   - Example: Loom's "Record screen in one click"

5. **Email/Push Prompts**
   - "Did you know you can [feature]?"
   - Include GIF or screenshot showing it

6. **In-App Prompts**
   - Empty state CTAs: "Try [feature] to solve [problem]"
   - Checklist: "Unlock advanced features"
```

---

### Step 4: Re-Engagement Campaigns

**Win back churned/dormant users:**

```markdown
## Re-Engagement Framework

**SEGMENT USERS BY ACTIVITY:**
- Active: Used in last 7 days
- At-Risk: Used 8-30 days ago
- Dormant: Used 31-90 days ago
- Churned: >90 days inactive

**CAMPAIGN BY SEGMENT:**

### AT-RISK USERS (8-30 days)
**Goal:** Prevent churn before they leave

Email Subject: "We noticed you haven't been around..."
Body:
- Acknowledge absence (empathetic)
- Highlight what they're missing (new content, activity from connections)
- Offer help ("Reply if you're stuck")
- CTA: "Come back and see what's new"

Push: "You have 3 unread [items]"

---

### DORMANT USERS (31-90 days)
**Goal:** Remind them why they signed up

Email Subject: "We've made [Product] even better"
Body:
- Show new features/improvements
- Customer success story
- Incentive (bonus credits, trial extension)
- CTA: "Log back in"

Push: Consider skip (high uninstall risk)

---

### CHURNED USERS (>90 days)
**Goal:** Last-ditch effort to win them back

Email Subject: "We'd love to have you back"
Body:
- Acknowledge they left
- Ask why (survey link)
- Major product updates since they left
- Generous incentive (free month, discount)
- CTA: "Give us another try"

**Timing:**
- At-Risk: Email weekly until they return or go dormant
- Dormant: Email bi-weekly for 6 weeks, then monthly
- Churned: One final email, then stop (don't spam)
```

---

### Step 5: Retention Mechanics Toolbox

```markdown
## Proven Retention Tactics

### TACTIC 1: Streaks
Show consecutive days/weeks of usage.
- Example: Duolingo (learning streak), Snapchat (snap streak)
- Why it works: Loss aversion (don't want to break streak)
- Caution: Can feel manipulative if not genuine value

### TACTIC 2: Progress Bars
Show completion status toward goal.
- Example: LinkedIn profile strength, Todoist karma
- Why it works: Zeigarnik effect (incomplete tasks nag us)
- Best: Tie to real value, not vanity metric

### TACTIC 3: Leaderboards
Rank users competitively.
- Example: Strava (segment leaderboards), Peloton
- Why it works: Social comparison, status
- Caution: Can demotivate low performers (use cohorts)

### TACTIC 4: Notifications (Judiciously)
Alert users to new activity.
- Example: "John mentioned you", "New message", "Daily summary"
- Why it works: FOMO, curiosity
- Caution: Overuse = uninstalls (let users control frequency)

### TACTIC 5: Content Freshness
New content daily/weekly gives reason to return.
- Example: News apps, social feeds, content platforms
- Why it works: Variable reward (never know what's new)
- Best: Personalized (not generic)

### TACTIC 6: Network Effects
More valuable as more people join.
- Example: Slack (more teammates), Marketplace (more listings)
- Why it works: Switching cost increases with usage
- Best: Encourage invites, team features

### TACTIC 7: Data Lock-In
User data makes product more valuable over time.
- Example: Spotify playlists, Notion workspaces
- Why it works: Sunk cost, hard to replicate elsewhere
- Caution: Allow exports (trust signal)

### TACTIC 8: Habit Stacking
Integrate into existing routine.
- Example: "Log workout after gym", "Review tasks with morning coffee"
- Why it works: Piggyback on existing habits
- Best: Suggest specific habit triggers
```

---

### Step 6: Measure What Matters

```markdown
## Key Retention Metrics

**PRIMARY METRICS:**
1. **D1, D7, D30 Retention** - % of users who return
2. **DAU/MAU Ratio** - Daily active / monthly active (stickiness)
3. **L30 (Last 30 days active)** - Rolling 30-day retention

**SECONDARY METRICS:**
4. **Session Frequency** - Visits per week/month
5. **Session Length** - Time spent per session
6. **Feature Adoption** - % using 3+ features
7. **Resurrection Rate** - % of churned users who return

**COHORT METRICS:**
8. **Cohort Retention Curves** - By signup week/month
9. **Retention by Segment** - Power users vs. casual
10. **Retention by Channel** - Organic vs. paid

**LEADING INDICATORS:**
11. **Aha Moment Completion** - % reaching activation
12. **Time to Aha** - Days from signup to activation
13. **Trigger Engagement** - Email/push open rates
```

---

## Common Retention Mistakes

```markdown
## Anti-Patterns

❌ **Notification Spam**
Sending daily "We miss you" emails without value
→ Fix: Valuable triggers only (new content, social activity)

❌ **Growth Over Retention**
Acquiring users faster than you're retaining them
→ Fix: Retention first, then scale acquisition

❌ **Dark Patterns**
Manipulative streaks, fake urgency, hard unsubscribe
→ Fix: Ethical engagement (user can always leave)

❌ **One-Size-Fits-All**
Same triggers/content for all user segments
→ Fix: Personalize based on behavior, preferences

❌ **Ignoring Churn Reasons**
Not talking to churned users
→ Fix: Exit surveys, churn interviews
```

---

## Related Skills

- `/product-market-fit` - Retention is core PMF signal
- `/user-onboarding` - Fix activation to improve D1/D7
- `/growth-loops` - Retention enables viral growth
- `/north-star-metrics` - Retention as NSM component

---

**Last Updated**: 2026-01-22
