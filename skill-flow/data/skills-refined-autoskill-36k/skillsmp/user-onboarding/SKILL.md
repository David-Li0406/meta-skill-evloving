---
name: user-onboarding
description: Design high-converting onboarding flows that get users to their "aha moment" fast. Reduce time-to-value, improve activation rates, and boost Day 1/Day 7 retention through progressive disclosure, empty states, and habit formation.
---

# User Onboarding Optimization

Design onboarding experiences that activate users quickly, build habits, and drive long-term retention.

## When to Use

- Day 1 or Day 7 retention is weak (<30%)
- Users sign up but don't complete core action
- Feature adoption is low (users don't discover value)
- Struggling to explain product value quickly
- High drop-off at specific onboarding steps
- Redesigning first-time user experience
- Launching new product or major feature

## Core Concept

**Onboarding Goal:** Get users to their **"aha moment"** as fast as possible.

**Aha Moment** = The moment users understand and experience your product's core value.

**Examples:**
- Facebook: "Connect with 7 friends in 10 days"
- Slack: "Send 2,000 team messages"
- Dropbox: "Put one file in one folder on one device"
- Twitter: "Follow 30 accounts"
- Duolingo: "Complete first lesson"

**Key Insight:** Onboarding doesn't end at signup. It's the journey from signup to habit formation (weeks, not minutes).

---

## Workflow

### Step 1: Identify Your Aha Moment

**How to Find It:**

```markdown
## Aha Moment Discovery Process

**METHOD 1: Cohort Analysis (Data-Driven)**
1. Segment users by retention (retained vs. churned)
2. Compare early behaviors between groups
3. Find actions that correlate with retention
4. Test: If users do X within Y days, are they Z% more likely to return?

Example:
- Users who add 3+ items in first session → 60% D30 retention
- Users who add 0-2 items in first session → 15% D30 retention
→ Aha moment = "Add 3+ items"

**METHOD 2: User Interviews (Qualitative)**
Ask retained users:
- "When did you realize this product was valuable?"
- "What made you come back after your first visit?"
- "What would you tell a friend this product does?"

**METHOD 3: Feature Correlation**
Track which features correlate with retention:
- Users who use feature X → stay
- Users who don't use feature X → churn
→ Aha moment likely involves feature X

**VALIDATION:**
Once you have a hypothesis:
1. Track % of users reaching aha moment
2. Measure retention difference (aha vs. no aha)
3. If gap is >20%, you've found it
```

**Common Aha Moments by Product Type:**

```markdown
## Aha Moment Patterns

**Social / Network Products:**
- Connect with X friends/colleagues
- Receive first message/notification from someone
- See personalized feed for first time

**Productivity / Tools:**
- Complete first task/workflow
- See time saved or automation working
- Integrate with tool they already use

**Content / Media:**
- Consume 3+ pieces of content
- Find content they couldn't find elsewhere
- Receive personalized recommendation

**Marketplace:**
- Complete first transaction (buy or sell)
- Receive first inquiry/message
- See selection they want at price they like

**SaaS / B2B:**
- Invite team member (collaboration signal)
- Complete setup and see first result
- Integrate with existing workflow/tool
```

---

### Step 2: Measure Time-to-Value

**Time-to-Value (TTV)** = Time from signup to aha moment.

**Why It Matters:**
- Faster TTV = Higher activation
- Higher activation = Better retention
- Every extra step/minute = drop-off

**How to Measure:**

```markdown
## TTV Calculation

**STEP 1: Define "Value Delivered"**
When does user experience core benefit?
- First result shown
- First automation triggered
- First connection made
- First task completed

**STEP 2: Track Funnel**
Signup → [Step 1] → [Step 2] → ... → Value Delivered

**STEP 3: Calculate Metrics**
- Median TTV (time in minutes/hours/days)
- % of users reaching value within [X timeframe]
- Drop-off rate at each step

**BENCHMARKS:**
| Product Type | Good TTV | Great TTV |
|--------------|----------|-----------|
| Consumer app | <5 minutes | <2 minutes |
| SMB SaaS | <1 day | <1 hour |
| Enterprise SaaS | <7 days | <1 day |
| Marketplace | <1 week | <1 day |

**RED FLAG:** If TTV >1 week (consumer) or >1 month (B2B), users will churn before seeing value.
```

---

### Step 3: Design Onboarding Flow

**Progressive Disclosure Framework:**

```markdown
## Three-Phase Onboarding

### PHASE 1: Instant Value (First 60 Seconds)
**Goal:** Show core value immediately, defer everything else.

**Do:**
✅ Show working product (not tutorial)
✅ Pre-populate with example data (not empty state)
✅ Highlight one key benefit (not feature list)
✅ Allow exploration (not forced tour)

**Don't:**
❌ Long signup forms (defer to later)
❌ Video tutorials (nobody watches)
❌ Feature tours (users skip)
❌ Empty dashboards ("Add your first X")

**Example (Good):**
- Figma: Opens to example design with hotspots
- Notion: Pre-filled template showing features
- Linear: Sample project with issues and workflows

**Example (Bad):**
- "Welcome! Here's a 3-minute intro video"
- "Add your first project to get started"
- 5-step modal tour of features

---

### PHASE 2: Activation (First Session)
**Goal:** Guide user to complete aha moment action.

**Do:**
✅ Clear next action ("Add your first task")
✅ Contextual help (tooltips when relevant)
✅ Progress indication ("1 of 3 steps complete")
✅ Celebrate small wins ("Great! You've...")

**Don't:**
❌ Overwhelming choices (paradox of choice)
❌ Asking for info you can infer later
❌ Blocking progress with optional steps
❌ Making them read before doing

**Tactics:**
1. **Input Fields:** Use placeholder examples, smart defaults
2. **Empty States:** Show what it'll look like when populated + CTA
3. **Checklists:** Break aha moment into 3-5 steps, show progress
4. **Quick Wins:** Let them accomplish something in <2 minutes

---

### PHASE 3: Habit Formation (Days 1-30)
**Goal:** Turn one-time user into repeat user.

**Do:**
✅ Email/push triggers to return (value-based, not spam)
✅ Show progress over time (streaks, stats, milestones)
✅ Reveal advanced features progressively
✅ Encourage social/team features (network effects)

**Don't:**
❌ Bombarding with notifications
❌ Showing everything at once (cognitive overload)
❌ Forgetting about users after Day 1
❌ No reason to return daily/weekly

**Tactics:**
1. **Trigger Emails:** Day 1, 3, 7, 14, 30 with specific value props
2. **Feature Discovery:** Introduce one new feature per session
3. **Social Proof:** "X teammates are already using this"
4. **Habit Loops:** Trigger → Action → Reward → Investment
```

---

### Step 4: Onboarding Audit Checklist

**Run through this checklist for your current onboarding:**

```markdown
## Onboarding Health Check

### SIGNUP FLOW (5 points)
- [ ] Can I sign up in <30 seconds? (email/social, not forms)
- [ ] Is signup optional? (Can I use product first, sign up later?)
- [ ] Do I see value BEFORE signup? (demo, example, preview)
- [ ] Is signup form short? (<3 fields)
- [ ] Do you use OAuth / social signup? (reduce friction)

### FIRST IMPRESSION (5 points)
- [ ] Do I see a populated example (not empty state)?
- [ ] Is the core value prop visible in <10 seconds?
- [ ] Can I DO something immediately (not just read)?
- [ ] Is there ONE clear next action (not 5 options)?
- [ ] Do I understand what this product does without docs?

### ACTIVATION PATH (5 points)
- [ ] Is the path to aha moment <5 steps?
- [ ] Does each step have clear benefit/reason?
- [ ] Can I skip optional steps and come back later?
- [ ] Do you celebrate progress/wins along the way?
- [ ] Can I reach aha moment in first session?

### PROGRESSIVE DISCLOSURE (5 points)
- [ ] Do you hide advanced features initially?
- [ ] Are new features revealed contextually (not all at once)?
- [ ] Can users level up as they get comfortable?
- [ ] Do you avoid overwhelming new users?
- [ ] Is onboarding personalized to user type/goal?

### RETENTION MECHANISMS (5 points)
- [ ] Do I get an email within 24 hours with next step?
- [ ] Are notifications value-based (not spammy)?
- [ ] Do you create habits (daily/weekly return triggers)?
- [ ] Is there progress I can see over time?
- [ ] Do you re-engage users who drop off?

**SCORE:**
- 20-25: Excellent onboarding
- 15-19: Good, room for improvement
- 10-14: Needs work
- <10: Major overhaul needed
```

---

### Step 5: Onboarding Funnel Optimization

**Identify and Fix Drop-Off Points:**

```markdown
## Funnel Analysis Framework

**STEP 1: Map Your Funnel**
Example:
1. Land on homepage → 100%
2. Click "Sign up" → 40%
3. Complete signup → 30%
4. See dashboard → 28%
5. Complete first action → 15%
6. Reach aha moment → 10%

**STEP 2: Find Biggest Drop-Offs**
Where are you losing most users?
- Homepage to signup: 60% drop (messaging problem?)
- Signup to dashboard: 7% drop (email verification?)
- Dashboard to action: 46% drop (empty state? unclear next step?)

**STEP 3: Diagnose WHY**
For each drop-off:
- Run user testing (watch 5 users try to complete step)
- Check analytics (how long do they spend? where do they click?)
- Survey users who dropped off (why didn't you continue?)
- A/B test solutions

**STEP 4: Prioritize Fixes**
Fix highest-impact drop-offs first:
- Impact = Drop-off rate × # of users hitting step
- Example: 46% drop at 28 users = 12.8 users lost (HIGH)
- Example: 7% drop at 30 users = 2.1 users lost (LOW)

**COMMON DROP-OFF CAUSES + FIXES:**

| Drop-Off Point | Cause | Fix |
|----------------|-------|-----|
| Homepage → Signup | Unclear value prop | Better headline, demo video, social proof |
| Signup → Dashboard | Email verification wall | Magic link, OAuth, skip verification |
| Dashboard → Action | Empty state | Pre-populate examples, show what's possible |
| Action → Aha moment | Too many steps | Reduce steps, smart defaults, skip optional |
| Aha → Return | Forgot about product | Trigger emails, push notifications, habit loops |
```

---

### Step 6: Onboarding Patterns Library

**Effective Onboarding Tactics:**

```markdown
## Onboarding Pattern Library

### PATTERN 1: Example/Template First
Instead of empty state, show pre-filled example.
- **Example:** Notion gives you template pages, not blank canvas
- **Why it works:** Users see value immediately, understand possibilities
- **When to use:** Complex products with steep learning curve

### PATTERN 2: Minimal Signup
Let users use product first, sign up later.
- **Example:** Figma lets you design without account, prompts save when done
- **Why it works:** Removes friction, users see value before committing
- **When to use:** Products with instant "wow" moment

### PATTERN 3: Checklist Onboarding
Show progress checklist to aha moment.
- **Example:** Slack's "Get started" checklist (create channel, invite team, post message)
- **Why it works:** Gamification, clear path, dopamine hits
- **When to use:** Multi-step activation with clear milestones

### PATTERN 4: Contextual Tooltips
Explain features when user hovers/clicks, not upfront tour.
- **Example:** Linear shows tooltips on first hover, never again
- **Why it works:** Just-in-time learning, low cognitive load
- **When to use:** Feature-rich products where users explore

### PATTERN 5: Personalized Path
Ask user goal/role, customize onboarding to them.
- **Example:** Canva asks "What will you design?" → personalized templates
- **Why it works:** Relevant content, faster path to value for segment
- **When to use:** Product serves multiple use cases/personas

### PATTERN 6: Social Activation
Require inviting others to unlock full value.
- **Example:** Dropbox gives more storage for referrals, Slack useless without team
- **Why it works:** Network effects, viral growth, better retention
- **When to use:** Collaborative/network products

### PATTERN 7: Progressive Feature Discovery
Reveal one new feature per session as user advances.
- **Example:** Duolingo introduces new lesson types every few days
- **Why it works:** Prevents overwhelm, keeps product feeling fresh
- **When to use:** Products with many features/depth

### PATTERN 8: Empty State CTAs
If can't avoid empty state, make CTA compelling + easy.
- **Example:** GitHub's empty repo shows clear instructions + one-click templates
- **Why it works:** Reduces "blank canvas" anxiety, provides starting point
- **When to use:** When examples/templates don't fit product model
```

---

### Step 7: Retention Email Sequence

**Post-Signup Onboarding Emails:**

```markdown
## Onboarding Email Framework

**EMAIL 1: Welcome (Day 0, sent immediately)**
Subject: "Welcome to [Product] — here's how to get started"

Body:
- Warm welcome (1 sentence)
- Core value prop reminder (1 sentence)
- ONE clear next action (CTA button)
- Optional: Quick win tip
- Keep it <100 words

---

**EMAIL 2: Activation Nudge (Day 1, if didn't complete aha moment)**
Subject: "Quick question about [Product]"

Body:
- "Noticed you signed up but haven't [core action]"
- Ask if they need help
- Offer 2-3 specific ways to help (video, example, personal call)
- CTA: "Complete your first [action]"

---

**EMAIL 3: Feature Discovery (Day 3)**
Subject: "3 ways to get more from [Product]"

Body:
- Assume they've completed aha moment
- Introduce 3 advanced features or tips
- Each with specific use case/benefit
- Keep it scannable (bullets, not paragraphs)

---

**EMAIL 4: Social Proof (Day 7)**
Subject: "[Company X] increased [metric] by Y% with [Product]"

Body:
- Customer success story relevant to their use case
- Specific results/metrics
- How they use the product
- CTA: "See how [similar company] does it"

---

**EMAIL 5: Re-engagement (Day 14, if inactive)**
Subject: "We miss you! Here's what's new"

Body:
- Acknowledge they haven't been active
- Highlight new features or improvements
- Offer help: "Reply to this email if you're stuck"
- CTA: "Log back in"

---

**EMAIL 6: Upgrade/Expand (Day 30, if active)**
Subject: "Ready to take [Product] to the next level?"

Body:
- Celebrate their success so far
- Introduce premium features or team plan
- Show value of upgrade (not just feature list)
- CTA: "Upgrade now" or "Invite your team"
```

---

## Common Onboarding Mistakes

```markdown
## Anti-Patterns to Avoid

❌ **Mistake 1: Feature Tour on First Load**
"Welcome! Let me show you all 20 features..."
→ Problem: Nobody reads tours. Users want to DO, not watch.
→ Fix: Let them explore, use contextual tooltips instead.

❌ **Mistake 2: Long Signup Forms**
Asking for company size, role, phone, use case before showing product
→ Problem: Friction before value. Users bounce.
→ Fix: Defer data collection. Ask only for email/name upfront.

❌ **Mistake 3: Empty State Hell**
"Add your first project!" on blank dashboard
→ Problem: Blank canvas paralysis. Users don't know what to do.
→ Fix: Pre-populate examples. Show what's possible.

❌ **Mistake 4: No Clear Next Step**
Dashboard with 10 options, no hierarchy
→ Problem: Decision paralysis. Users freeze.
→ Fix: ONE prominent CTA. Direct them to aha moment.

❌ **Mistake 5: Asking for Setup Before Value**
"Connect your Slack, Google Calendar, and CRM to continue"
→ Problem: Work before payoff. Users abandon.
→ Fix: Show value first with mock data, integrate later.

❌ **Mistake 6: Forgetting About Them After Day 1**
No follow-up emails or re-engagement
→ Problem: Users forget you exist.
→ Fix: Email sequence over Days 1-30. Bring them back.

❌ **Mistake 7: One-Size-Fits-All Onboarding**
Same flow for all user types/personas
→ Problem: Irrelevant content. Slow path to value.
→ Fix: Segment by role/goal, personalize onboarding.
```

---

## Output Format

**When auditing onboarding, provide:**

```markdown
## Onboarding Audit for [Product]

### 1. Current Aha Moment
[What is it? How did you identify it?]

### 2. Time-to-Value
- Median TTV: [X minutes/hours/days]
- % reaching aha in first session: [Y%]

### 3. Activation Funnel
[Map funnel with conversion rates, identify top 3 drop-offs]

### 4. Key Issues
1. [Biggest problem]
2. [Second problem]
3. [Third problem]

### 5. Recommendations (Prioritized)
1. [Highest impact fix]
2. [Second priority]
3. [Third priority]

### 6. A/B Test Ideas
- Test A vs. B: [Hypothesis]
- Expected impact: [Improvement in metric]
```

---

## Related Skills

- `/product-market-fit` - Improve activation to boost retention
- `/retention-engagement` - Turn activated users into retained users
- `/growth-loops` - Build virality into onboarding
- `/north-star-metrics` - Define activation as part of NSM

---

**Last Updated**: 2026-01-22
