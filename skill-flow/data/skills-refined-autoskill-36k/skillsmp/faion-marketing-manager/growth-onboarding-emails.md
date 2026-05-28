---
id: onboarding-emails
name: "Onboarding Email Sequences"
domain: MKT
skill: faion-marketing-manager
category: "marketing"
---

# Onboarding Email Sequences

## Metadata

| Field | Value |
|-------|-------|
| **ID** | onboarding-emails |
| **Name** | Onboarding Email Sequences |
| **Category** | Marketing |
| **Difficulty** | Intermediate |
| **Agent** | faion-email-agent |
| **Related** | email-marketing, free-trial-optimization, activation-rate |

---

## Problem

Users sign up and then disappear. They opened your welcome email but never came back. Generic onboarding emails get ignored. Your activation rate is stuck.

Great onboarding email sequences guide users to value step by step. They're triggered by behavior, personalized to context, and focused on outcomes.

---

## Framework

Onboarding emails follow a behavior-driven approach:

```
SEGMENT   -> Different paths for different users
TRIGGER   -> Send based on actions (not just time)
GUIDE     -> One action per email
ESCALATE  -> If stuck, offer more help
```

### Step 1: Map User Segments

**Common segments:**

| Segment | Definition | Messaging Focus |
|---------|------------|-----------------|
| **New + Active** | Engaged, hitting milestones | Accelerate to activation |
| **New + Stuck** | Started but stopped | Remove blockers |
| **New + Inactive** | Signed up, no activity | Re-engage |
| **Activated** | Hit aha moment | Path to conversion |
| **At-risk** | Dropping engagement | Win back |

**Segment by:**
- Signup source (different intent)
- Use case (different needs)
- Company size (different value)
- Behavior (actual actions)

### Step 2: Design Trigger-Based Flows

**Time-based vs Behavior-based:**

| Type | Trigger | Example |
|------|---------|---------|
| **Time** | Days since signup | "Day 3: Feature highlight" |
| **Behavior** | Action completed | "You created a project!" |
| **Inaction** | Action NOT completed | "Did you get stuck?" |
| **Hybrid** | Time + behavior | "Day 3 AND not activated" |

**Behavior triggers to use:**
- Signed up
- Completed step X
- Didn't complete step X in Y days
- First login after gap
- Reached usage threshold
- Invited team member
- Connected integration

### Step 3: Create Email Sequence

**Core onboarding sequence:**

| # | Trigger | Email | Goal |
|---|---------|-------|------|
| 1 | Signup | Welcome | Set expectations, first action |
| 2 | Didn't complete action | Gentle nudge | Remove blocker |
| 3 | Completed first action | Celebration + next step | Build momentum |
| 4 | Day 3 (if not activated) | Feature education | Show value |
| 5 | Completed activation | Path to power use | Deepen engagement |
| 6 | Day 7 (trial) | Mid-point check | Offer help |
| 7 | High usage | Social proof + upgrade | Convert |
| 8 | Low usage | Re-engagement | Rescue |

### Step 4: Write Each Email

**Email structure:**

| Element | Purpose | Length |
|---------|---------|--------|
| Subject | Get opened | 4-7 words |
| Preview text | Enhance open | 40-60 chars |
| Opening | Personal connection | 1-2 sentences |
| Body | Single message | 3-5 sentences |
| CTA | Clear action | 1 action only |
| PS | Secondary info | Optional |

**Writing rules:**
- One email, one action
- Write like a person, not a company
- Short paragraphs (1-2 sentences)
- Button OR link, not both
- Reply-friendly tone

### Step 5: Escalation for Stuck Users

**Escalation ladder:**

| Level | Trigger | Action |
|-------|---------|--------|
| 1 | No action, Day 2 | Helpful email |
| 2 | No action, Day 5 | Different angle email |
| 3 | No action, Day 7 | Video tutorial link |
| 4 | No action, Day 10 | Personal outreach offer |
| 5 | No action, Day 12 | Extension or special offer |
| 6 | Trial ends | Exit survey |

### Step 6: Measure and Optimize

**Key metrics per email:**

| Metric | Target | Action if Below |
|--------|--------|-----------------|
| Open rate | 50%+ | Fix subject line |
| Click rate | 10%+ | Fix CTA/copy |
| Conversion | 5%+ | Reduce friction |
| Unsubscribe | <0.5% | Check frequency |

---

## Templates

### Welcome Email

```markdown
Subject: Welcome - your first step

Hey [Name],

You're in! Here's your first step with [Product]:

**[Single action]**
[Button: Do it now]

Takes 2 minutes. This is what most successful users do first.

Need help? Just reply to this email.

[Your name]
[Title]
```

### Completion Celebration

```markdown
Subject: Nice work on [achievement]

Hey [Name],

You just [completed action]. That's great!

Here's what successful [Product] users do next:

**[Next step]**
[Button: Continue]

You're making great progress.

[Name]
```

### Nudge for Stuck Users

```markdown
Subject: Quick question

Hey [Name],

I noticed you started setting up [Product] but didn't [next step].

Did you run into an issue? Common things that trip people up:

- [Potential blocker 1] → [Solution]
- [Potential blocker 2] → [Solution]

If something else is going on, just reply. Happy to help.

[Name]
```

### Personal Outreach (High-Value Users)

```markdown
Subject: 15 min to get you unstuck?

Hey [Name],

I see you signed up from [company] last week but haven't
[completed activation].

Would a quick 15-min call help? I can show you exactly
how [similar company] uses [Product] for [outcome].

[Button: Book a time]

No pressure - just want to make sure you get value.

[Name]
```

### Trial Ending - Activated User

```markdown
Subject: Your trial ends in 3 days

Hey [Name],

You've been crushing it with [Product]:
- [Achievement 1]
- [Achievement 2]

Your trial ends in 3 days. To keep your [data/progress]:

[Button: Upgrade to Pro - $X/month]

Questions about upgrading? Just reply.

[Name]
```

---

## Examples

### Example 1: SaaS Onboarding

**Sequence:**
1. Welcome (immediate)
2. Didn't connect data (Day 1)
3. Connected data (triggered)
4. Feature education (Day 3)
5. Didn't activate (Day 5)
6. Activated (triggered)
7. Mid-trial (Day 7)
8. Convert (Day 10)

**Results:**
- 65% Day 1 activation
- 40% trial-to-paid
- 15% lift vs time-based only

### Example 2: Freemium Product

**Sequence:**
1. Welcome + quick win
2. First value achieved
3. Usage milestone
4. Upgrade trigger (hit limit)
5. Feature showcase
6. Social proof
7. Conversion push

**Results:**
- 30% free-to-paid
- 3x better than generic sequence

---

## Implementation Checklist

### Planning
- [ ] Define user segments
- [ ] Map ideal user journey
- [ ] Identify key actions/milestones
- [ ] Design trigger logic

### Building
- [ ] Write all email copy
- [ ] Create email templates
- [ ] Set up automation triggers
- [ ] Test full sequence

### Launching
- [ ] QA all emails (links, personalization)
- [ ] Start with subset of users
- [ ] Monitor deliverability
- [ ] Track metrics daily

### Optimizing
- [ ] A/B test subject lines
- [ ] Optimize CTAs
- [ ] Adjust timing
- [ ] Iterate on content

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Too many emails | Overwhelm, unsubscribe | Max 1 per day |
| Multiple CTAs | Confusion | One action per email |
| Time-only triggers | Miss context | Add behavior triggers |
| Generic copy | Not relevant | Personalize by behavior |
| No escalation | Lost users | Add stuck-user path |
| Never testing | Suboptimal | A/B test continuously |

---

## Metrics Dashboard

```markdown
## Onboarding Email Performance

### Overall
- Total users in sequence: [X]
- Completed sequence: [X%]
- Activated via email: [X%]

### By Email
| Email | Opens | Clicks | Conversions |
|-------|-------|--------|-------------|
| Welcome | X% | X% | X% |
| Nudge 1 | X% | X% | X% |
| Feature | X% | X% | X% |
| ...     | ... | ... | ... |

### By Segment
| Segment | Activation | Conversion |
|---------|------------|------------|
| Active users | X% | X% |
| Stuck users | X% | X% |
| Inactive | X% | X% |
```

---

## Tools

| Purpose | Tools |
|---------|-------|
| Email automation | Customer.io, Intercom, ActiveCampaign |
| Behavior tracking | Segment, Mixpanel |
| Template design | Postmark, Sendgrid |
| A/B testing | Built-in to email tools |
| Analytics | Email tool + product analytics |

---

## Related Methodologies

- **email-marketing:** Email Marketing (general email strategy)
- **free-trial-optimization:** Free Trial Optimization (trial context)
- **activation-rate:** Activation Rate (activation strategy)
- **customer-success:** Customer Success (post-activation)

---

*Methodology: onboarding-emails | Marketing | faion-email-agent*
