---
name: jikime-marketing-onboarding
description: User onboarding and activation specialist for optimizing post-signup experience, reducing time-to-value, and improving user activation rates.
version: 1.0.0
tags: ["marketing", "onboarding", "activation", "user-experience", "retention"]
triggers:
  keywords: ["onboarding", "activation", "first-run", "aha moment", "time to value", "empty state", "user activation", "온보딩", "활성화", "첫 사용"]
  phases: ["plan", "run"]
  agents: ["frontend", "manager-strategy"]
  languages: []
# Progressive Disclosure Configuration
progressive_disclosure:
  enabled: true
  level1_tokens: ~100
  level2_tokens: ~7000
user-invocable: true
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Task
  - TodoWrite
---

# User Onboarding & Activation

## Quick Reference (30 seconds)

Onboarding Specialist - Help users reach their "aha moment" quickly and establish habits for long-term retention.

Core Principles:
- **Time-to-Value Is Everything**: Remove every step between signup and first value
- **One Goal Per Session**: Don't try to teach everything at once
- **Do, Don't Show**: Interactive > Tutorial, Doing > Learning
- **Progress Creates Motivation**: Show advancement, celebrate completions

Key Metrics:
- Activation rate (% reaching activation event)
- Time to activation
- Day 1/7/30 retention

---

## Defining Activation

### Find Your Aha Moment

The action that correlates most strongly with retention:

| Product Type | Typical Aha Moment |
|--------------|-------------------|
| **Project management** | Create first project + add team member |
| **Analytics** | Install tracking + see first report |
| **Design tool** | Create first design + export/share |
| **Collaboration** | Invite first teammate |
| **Marketplace** | Complete first transaction |

### Activation Metrics

```
┌─────────────────────────────────────────────────────────────────┐
│  ACTIVATION FUNNEL                                               │
├─────────────────────────────────────────────────────────────────┤
│  Signup → Step 1 → Step 2 → Activation → Retention              │
│  100%      80%       60%       40%         25%                  │
│                                                                  │
│  Identify biggest drops and focus there                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Post-Signup Flow Options

### Immediate Post-Signup (First 30 Seconds)

| Approach | Best For | Risk |
|----------|----------|------|
| **Product-first** | Simple products, B2C, mobile | Blank slate overwhelm |
| **Guided setup** | Products needing personalization | Adds friction before value |
| **Value-first** | Products with demo data | May not feel "real" |

### Whatever You Choose

```
□ Clear single next action
□ No dead ends
□ Progress indication if multi-step
```

---

## Onboarding Patterns

### Onboarding Checklist

**When to use:**
- Multiple setup steps required
- Product has several features to discover
- Self-serve B2B products

**Best practices:**

| Element | Guideline |
|---------|-----------|
| **Items** | 3-7 (not overwhelming) |
| **Order** | Most impactful first |
| **Start** | Quick wins early |
| **Progress** | Bar or completion % |
| **Completion** | Celebration moment |
| **Escape** | Dismiss option (don't trap) |

**Checklist item structure:**
```
☐ Connect your first data source (2 min)
  Get real-time insights from your existing tools
  [Connect Now]
```

### Empty States

Empty states are onboarding opportunities, not dead ends.

```
┌─────────────────────────────────────────────────────────────────┐
│  EMPTY STATE STRUCTURE                                           │
├─────────────────────────────────────────────────────────────────┤
│  1. Illustration or preview                                      │
│  2. Brief explanation of value                                   │
│  3. Primary CTA to add first item                               │
│  4. Optional: Secondary action (import, template)               │
└─────────────────────────────────────────────────────────────────┘
```

### Tooltips & Guided Tours

| When to Use | When to Avoid |
|-------------|---------------|
| Complex UI needing orientation | Simple, intuitive interfaces |
| Features not self-evident | Mobile apps (limited space) |
| Power features users might miss | Interrupting important flows |

**Best practices:**
- Max 3-5 steps per tour
- Point to actual UI elements
- Dismissable at any time
- Don't repeat for returning users

### Progress Indicators

| Type | Use Case |
|------|----------|
| **Checklist** | Discrete tasks |
| **Progress bar** | % complete |
| **Level/stage** | Gamified progression |
| **Profile completeness** | User info gathering |

**Key insight**: Show early progress (start at 20%, not 0%)

---

## Multi-Channel Coordination

### Email + In-App

| Email Type | Timing | Purpose |
|------------|--------|---------|
| Welcome | Immediate | Confirm, set expectations |
| Incomplete onboarding | 24h, 72h | Nudge return |
| Activation achieved | On event | Celebrate + next step |
| Feature discovery | Days 3, 7, 14 | Expand usage |
| Stalled re-engagement | After X days inactive | Win back |

**Email should:**
- Reinforce in-app actions (not duplicate)
- Drive back to product with specific CTA
- Be personalized based on actions taken

---

## Engagement Loops

### Building Habits

```
┌─────────────────────────────────────────────────────────────────┐
│  HABIT LOOP STRUCTURE                                            │
├─────────────────────────────────────────────────────────────────┤
│  Trigger → Action → Variable Reward → Investment                │
│                                                                  │
│  Example:                                                        │
│  Email digest → Log in to respond → Social engagement →         │
│  Add more content/connections                                    │
└─────────────────────────────────────────────────────────────────┘
```

### Milestone Celebrations

- Acknowledge meaningful achievements
- Show progress relative to journey
- Suggest next milestone
- Create shareable moments (social proof)

---

## Handling Stalled Users

### Detection Criteria
- X days inactive
- Incomplete setup
- Dropped at specific step

### Re-engagement Tactics

| Tactic | Approach |
|--------|----------|
| **Email sequence** | Remind value, address blockers, offer help |
| **In-app recovery** | Welcome back, pick up where left off |
| **Human touch** | For high-value accounts: personal outreach |

---

## Common Patterns by Product Type

### B2B SaaS Tool
```
1. Short setup wizard (use case selection)
2. First value-generating action
3. Team invitation prompt
4. Checklist for deeper setup
```

### Marketplace/Platform
```
1. Complete profile
2. First search/browse
3. First transaction
4. Repeat engagement loop
```

### Mobile App
```
1. Permission requests (strategic timing)
2. Quick win in first session
3. Push notification setup
4. Habit loop establishment
```

### Content/Social Platform
```
1. Follow/customize feed
2. First content consumption
3. First content creation
4. Social connection
```

---

## Experiment Ideas

### Flow Simplification
```
□ Add/remove email verification during onboarding
□ Test empty states vs. pre-populated dummy data
□ Provide pre-filled templates
□ Add OAuth options for faster linking
□ Reduce number of required steps
```

### Progress & Motivation
```
□ Add progress bars or completion %
□ Test checklist length (3-5 vs 5-7 items)
□ Gamify with badges or rewards
□ Show "X% complete" messaging
```

### Personalization
```
□ Segment users by role for relevant features
□ Segment by goal for custom paths
□ Create role-specific dashboards
□ Ask use-case question to personalize
```

---

## Measurement

### Key Metrics

| Metric | Definition |
|--------|------------|
| **Activation rate** | % reaching activation event |
| **Time to activation** | Duration to first value |
| **Onboarding completion** | % completing setup |
| **Day 1/7/30 retention** | Return rate by timeframe |
| **Feature adoption** | Which features get used |

### Funnel Analysis

Track drop-off at each step to identify biggest improvements.

---

## Output Format

### Onboarding Audit
```
Finding: [What's happening]
Impact: [Why it matters]
Recommendation: [Specific fix]
Priority: High / Medium / Low
```

### Onboarding Flow Design
```
Activation goal: [What they should achieve]
Step-by-step flow: [Each screen/state]
Checklist items: [If applicable]
Empty states: [Copy and CTA]
Email sequence: [Triggers and content]
Metrics plan: [What to measure]
```

---

## Works Well With

Skills:
- `jikime-marketing-email` - Onboarding email sequences
- `jikime-marketing-ab-test` - Testing onboarding changes
- `jikime-marketing-psychology` - Behavioral triggers for activation
- `jikime-marketing-page-cro` - Optimizing signup before onboarding

---

Version: 1.0.0
Last Updated: 2026-01-25
Attribution: Enhanced from marketingskills by Corey Haines (MIT License)
