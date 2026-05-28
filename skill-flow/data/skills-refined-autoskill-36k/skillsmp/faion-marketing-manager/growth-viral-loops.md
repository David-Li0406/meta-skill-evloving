---
id: viral-loops
name: "Viral Loops & Growth Mechanics"
domain: MKT
skill: faion-marketing-manager
category: "marketing"
---

# Viral Loops & Growth Mechanics

## Metadata

| Field | Value |
|-------|-------|
| **ID** | viral-loops |
| **Name** | Viral Loops & Growth Mechanics |
| **Category** | Marketing |
| **Difficulty** | Advanced |
| **Agent** | faion-growth-agent |
| **Related** | viral-coefficient, referral-programs, growth-loops |

---

## Problem

Your growth is linear: you spend money or time, you get users. When you stop, growth stops. You want exponential growth where users bring more users automatically. But most "viral" features flop.

True virality is rare and requires careful design. Even products that aren't inherently viral can build growth loops that compound over time.

---

## Framework

Growth loops are self-reinforcing cycles:

```
INPUT  -> Action by user
OUTPUT -> Creates distribution
RESULT -> Brings new users
REPEAT -> They do the same action
```

### Step 1: Understand Viral Coefficient

**K-factor (viral coefficient):**
```
K = i × c

Where:
i = invitations sent per user
c = conversion rate of invitations
```

**Examples:**

| Product | i | c | K |
|---------|---|---|---|
| Average app | 2 | 5% | 0.1 |
| Good referral | 5 | 10% | 0.5 |
| Viral product | 10 | 20% | 2.0 |

**K > 1:** Exponential growth (rare)
**K = 0.5-1:** Sustainable organic boost
**K < 0.5:** Minimal viral impact

**Goal:** Even K = 0.3 reduces CAC by 30%

### Step 2: Types of Viral Loops

**Loop types:**

| Type | How It Works | Example |
|------|--------------|---------|
| **Inherent** | Product requires sharing | Slack, Zoom |
| **Word of mouth** | Users talk about it | Apple |
| **Incentivized** | Rewards for referrals | Dropbox, Uber |
| **Social** | Visible to others | Wordle, Spotify Wrapped |
| **Collaborative** | Better with others | Figma, Notion |
| **Content** | Users create shareable content | Canva, TikTok |
| **Embedded** | Product in output | "Made with X" |

**Match loop to product:**

| Product Type | Best Loop |
|--------------|-----------|
| B2C, social | Social, content |
| B2B, team | Collaborative, inherent |
| Productivity | Embedded, WOM |
| Marketplace | Inherent, incentivized |

### Step 3: Design Your Loop

**Loop anatomy:**

```
1. USER ACTION
   ↓
2. CREATES ARTIFACT
   ↓
3. SHARED/EXPOSED
   ↓
4. NEW USER SEES
   ↓
5. MOTIVATED TO JOIN
   ↓
6. BECOMES USER → [Back to 1]
```

**Design questions:**

| Element | Question |
|---------|----------|
| Action | What action naturally leads to sharing? |
| Artifact | What do they create/share? |
| Distribution | How does it reach others? |
| Motivation | Why would new person join? |
| Friction | How easy is joining? |

### Step 4: Implementation Patterns

**Referral programs:**
```
Your friend gets: [Reward]
You get: [Reward]
[Share link]
```

**Embedded branding:**
```
"Made with [Product]"
"Sent via [Product]"
"[Link to product] in footer"
```

**Social sharing:**
```
"I just achieved [result] with [Product]!"
[Shareable image/badge]
[Share to Twitter/LinkedIn]
```

**Collaboration invites:**
```
"[Name] invited you to [workspace]"
"Join to view [content]"
[Accept invitation]
```

**Content templates:**
```
User creates: [Content]
Content has: [Branding/watermark]
Viewer sees: [Source attribution]
CTA: [Try it yourself]
```

### Step 5: Reduce Loop Friction

**Optimize each step:**

| Step | Friction Reduction |
|------|-------------------|
| Sharing | Pre-written message, one-click |
| Viewing | No signup to view |
| Joining | Social login, email magic link |
| Activating | Immediate value |

**Remove barriers:**
- Don't require signup to view shared content
- Pre-fill referral messages
- Make rewards instant, not delayed
- Reduce steps to share

### Step 6: Measure and Optimize

**Track funnel:**

| Stage | Metric |
|-------|--------|
| Shares | How many users share |
| Impressions | How many people see |
| Clicks | How many click through |
| Signups | How many join |
| Activation | How many become active |
| Referrers | How many then share |

**Calculate K-factor:**
```
Day 1: 1000 users
Day 7: Track invites sent
Day 14: Track conversions from invites
K = (Invites/Users) × (Conversions/Invites)
```

---

## Templates

### Referral Program Design

```markdown
## [Product] Referral Program

### Value Proposition
Share [Product] with friends and both of you get [reward].

### Mechanics
- Referred friend gets: [X]
- Referrer gets: [Y]
- Reward triggers when: [Event]

### Sharing Options
- Unique referral link
- Pre-written email
- Social share buttons
- Referral code

### Tracking
- Dashboard shows: Sent, Pending, Completed
- Rewards auto-applied

### Rules
- Max X rewards per user
- Fraud detection: [Method]
- Expiration: [Time]
```

### Growth Loop Analysis

```markdown
## Loop: [Name]

### The Loop
1. User does: [Action]
2. Creates: [Artifact]
3. Seen by: [Audience]
4. New user: [Motivation to join]
5. Loop back: [How they continue loop]

### Current Metrics
- % users entering loop: [X%]
- Shares per user: [X]
- Click-through rate: [X%]
- Conversion rate: [X%]
- K-factor: [X]

### Bottlenecks
1. [Identified problem]
2. [Identified problem]

### Experiments
1. [ ] [Experiment to test]
2. [ ] [Experiment to test]
```

---

## Examples

### Example 1: Dropbox Referral

**Loop:**
1. User needs more space
2. Shares referral link
3. Friend signs up
4. Both get 500MB
5. Friend needs more space...

**Key success factors:**
- Clear value exchange
- Obvious placement
- Instant reward
- Shareable link

**Results:**
- 60% of signups from referrals
- 35% permanent increase in growth

### Example 2: Spotify Wrapped

**Loop:**
1. User listens to music all year
2. Spotify creates personalized summary
3. User shares on social media
4. Friends see and want theirs
5. Non-users download Spotify

**Key success factors:**
- Zero effort to create
- Designed for sharing
- FOMO for non-users
- Annual ritual

**Results:**
- Millions of social shares
- Significant December download spike

### Example 3: Notion Templates

**Loop:**
1. Power user creates template
2. Shares publicly or in community
3. Others find template
4. Need Notion to use it
5. Some become template creators

**Key success factors:**
- User-generated content
- SEO-friendly
- Real utility
- Clear attribution

---

## Implementation Checklist

### Analysis
- [ ] Audit current sharing behavior
- [ ] Identify natural sharing moments
- [ ] Calculate current K-factor
- [ ] Research successful loops

### Design
- [ ] Choose loop type
- [ ] Design loop mechanics
- [ ] Create sharing artifacts
- [ ] Plan rewards (if applicable)

### Build
- [ ] Implement sharing features
- [ ] Build tracking
- [ ] Create referral dashboard
- [ ] Set up reward automation

### Launch
- [ ] A/B test with subset
- [ ] Measure loop metrics
- [ ] Optimize based on data
- [ ] Scale if working

---

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Forced sharing | Users resent it | Make sharing natural |
| Weak incentive | Not motivating | Test reward levels |
| Complex mechanics | Too much friction | Simplify to one click |
| Delayed rewards | Doesn't feel real | Instant gratification |
| No tracking | Can't optimize | Measure everything |
| Ignoring fraud | Wasted rewards | Detection from start |

---

## Metrics to Track

| Metric | Definition | Good |
|--------|------------|------|
| K-factor | Virality coefficient | >0.3 |
| Share rate | % users who share | >10% |
| Invitation CTR | Clicks / Impressions | >5% |
| Referral conversion | Signups / Clicks | >10% |
| Viral cycle time | Days for loop to complete | <7 days |

---

## Tools

| Purpose | Tools |
|---------|-------|
| Referral programs | Viral Loops, GrowSurf |
| Social sharing | AddThis, ShareThis |
| Analytics | Mixpanel, Amplitude |
| Fraud detection | SEON, MaxMind |
| A/B testing | Product tool, Optimizely |

---

## Related Methodologies

- **viral-coefficient:** Viral Coefficient (K-factor deep dive)
- **referral-programs:** Referral Programs (referral mechanics)
- **growth-loops:** Growth Loops (strategic loops)
- **retention-loops:** Retention Loops (engagement loops)

---

*Methodology: viral-loops | Marketing | faion-growth-agent*
