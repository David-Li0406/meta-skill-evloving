---
name: jikime-marketing-launch
description: Product launch and go-to-market strategy specialist for planning phased launches, channel strategy, Product Hunt launches, and ongoing launch momentum.
version: 1.0.0
tags: ["marketing", "launch", "go-to-market", "product-hunt", "beta"]
triggers:
  keywords: ["launch", "Product Hunt", "go-to-market", "beta launch", "early access", "waitlist", "product release", "출시", "런칭", "베타"]
  phases: ["plan"]
  agents: ["manager-strategy", "frontend"]
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

# Launch Strategy

## Quick Reference (30 seconds)

Launch Strategy Specialist - Plan launches that build momentum, capture attention, and convert interest into users.

Core Philosophy:
- **Launch Again and Again**: Every feature update is a launch opportunity
- **Phased Approach**: Build momentum across internal → alpha → beta → early access → full launch
- **Channel Strategy**: Own → Rent → Borrow (ORB framework)

Key Deliverables:
- 5-phase launch plan
- Channel strategy (ORB framework)
- Product Hunt launch playbook
- Post-launch momentum tactics

---

## The ORB Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                    CHANNEL STRATEGY (ORB)                        │
├─────────────────────────────────────────────────────────────────┤
│  OWNED              RENTED              BORROWED                │
│  ──────             ──────              ────────                │
│  You control        You rent visibility  You tap others'        │
│  the channel        from platforms       audiences              │
│                                                                  │
│  • Email list       • Social media       • Guest content        │
│  • Blog             • App stores         • Podcast interviews   │
│  • Podcast          • YouTube            • Collaborations       │
│  • Community        • Reddit             • Influencer partners  │
│  • Website          • Marketplaces       • Speaking events      │
│                                                                  │
│  [Most Valuable] ────────────────────── [Speed but Volatile]    │
└─────────────────────────────────────────────────────────────────┘
```

### Channel Selection Guide

| Your Situation | Start With |
|----------------|------------|
| Industry lacks quality content | Blog |
| People want direct updates | Email newsletter |
| Engagement matters most | Community (Slack/Discord) |
| Audience on Twitter/LinkedIn | Social + Newsletter funnel |
| B2B with complex product | Podcast/YouTube + Gated content |

---

## Five-Phase Launch Approach

### Phase Overview

| Phase | Goal | Key Actions |
|-------|------|-------------|
| **1. Internal** | Validate core functionality | Recruit 5-10 friendly testers |
| **2. Alpha** | First external validation | Landing page, waitlist, individual invites |
| **3. Beta** | Build buzz + broader feedback | Work through waitlist, teaser marketing |
| **4. Early Access** | Validate at scale | Throttled invites, user research, PMF survey |
| **5. Full Launch** | Maximum visibility | Open signups, charge, announce everywhere |

### Phase 1: Internal Launch

**Actions:**
- Recruit 5-10 early users one-on-one
- Collect feedback on usability gaps
- Ensure prototype is demo-ready

**Exit Criteria:** Core functionality validated with friendly users

### Phase 2: Alpha Launch

**Actions:**
- Create landing page with early access signup
- Announce product exists
- Invite users individually
- MVP working in production

**Exit Criteria:** First external signups, initial waitlist built

### Phase 3: Beta Launch

**Actions:**
- Work through early access list (some free, some paid)
- Start marketing with problem-focused teasers
- Recruit friends, investors, influencers to test

**Add These Elements:**
- "Beta" sticker in dashboard
- Coming soon landing page
- Email invites to waitlist
- Early access toggle for experimental features

**Exit Criteria:** Buzz building, product refined with broader feedback

### Phase 4: Early Access Launch

**Actions:**
- Leak product details: screenshots, GIFs, demos
- Gather quantitative usage data
- Run user research with engaged users
- Optional: Product-market fit survey

**Expansion Options:**
- Option A: Throttle invites in 5-10% batches
- Option B: Invite all at once under "early access" framing

**Exit Criteria:** Validated at scale, ready for full launch

### Phase 5: Full Launch

**Actions:**
- Open self-serve signups
- Start charging (if not already)
- Announce general availability

**Launch Touchpoints:**
```
□ Customer emails
□ In-app popups/tours
□ Website banner
□ "New" sticker in nav
□ Blog post announcement
□ Social posts
□ Product Hunt / BetaList / Hacker News
```

---

## Product Hunt Launch Strategy

### Pros vs Cons

| Pros | Cons |
|------|------|
| Tech-savvy early adopter audience | Very competitive to rank well |
| Credibility bump (if top product) | Short-lived traffic spikes |
| PR coverage and backlinks | Requires significant preparation |

### Before Launch Day

```
□ Build relationships with supporters and content hubs
□ Optimize listing: compelling tagline, polished visuals
□ Create short demo video (< 2 min)
□ Study successful launches for insights
□ Engage in relevant communities first
□ Prepare team for all-day engagement
```

### On Launch Day

```
□ Treat it as an all-day event
□ Respond to every comment in real-time
□ Answer questions, spark discussions
□ Encourage existing audience to engage
□ Direct traffic to site to capture signups
```

### After Launch Day

```
□ Follow up with everyone who engaged
□ Convert PH traffic into email signups
□ Continue momentum with post-launch content
```

### Case Studies

| Product | Strategy | Result |
|---------|----------|--------|
| **SavvyCal** | Optimized LP, built influencer relationships, responded to every comment | #2 Product of the Month |
| **Reform** | Studied successful launches, polished assets, treated as all-day event | #1 Product of the Day |

---

## Post-Launch Marketing

### Immediate Actions

| Action | Purpose |
|--------|---------|
| Onboarding email sequence | Educate new users |
| Include in roundup email | Catch people who missed launch |
| Comparison pages | Differentiate vs competitors |
| Update web pages | Add new feature sections |
| Interactive demo | Let visitors explore before signup |

### Ongoing Launch Strategy

Not all updates deserve the same marketing effort:

| Update Type | Examples | Marketing Level |
|-------------|----------|-----------------|
| **Major** | New features, product overhauls | Full campaign: blog, email, social, in-app |
| **Medium** | New integrations, UI enhancements | Targeted: email to relevant segments, in-app banner |
| **Minor** | Bug fixes, small tweaks | Changelog only: signal active development |

### Momentum Tactics

- **Space out releases**: Stagger announcements to maintain momentum
- **Reuse high-performers**: Apply insights from successful announcements
- **Signal active development**: Even changelog updates build retention
- **Keep engaging**: Email, social, in-app messaging for improvements

---

## Launch Checklist

### Pre-Launch
```
□ Landing page with clear value proposition
□ Email capture / waitlist signup
□ Early access list built
□ Owned channels established
□ Social profiles optimized
□ Borrowed channel opportunities identified
□ Product Hunt listing prepared (if using)
□ Launch assets created (screenshots, video, GIFs)
□ Onboarding flow ready
□ Analytics/tracking in place
```

### Launch Day
```
□ Announcement email to list
□ Blog post published
□ Social posts scheduled and posted
□ Product Hunt listing live (if using)
□ In-app announcement for existing users
□ Website banner active
□ Team ready to engage and respond
□ Monitor for issues and feedback
```

### Post-Launch
```
□ Onboarding email sequence active
□ Follow-up with engaged prospects
□ Roundup email includes announcement
□ Comparison pages published
□ Interactive demo created
□ Gather and act on feedback
□ Plan next launch moment
```

---

## Works Well With

Skills:
- `jikime-marketing-email` - Launch and onboarding sequences
- `jikime-marketing-page-cro` - Optimize launch landing pages
- `jikime-marketing-psychology` - Waitlist and exclusivity psychology
- `jikime-marketing-copywriting` - Launch copy and announcements

---

Version: 1.0.0
Last Updated: 2026-01-25
Attribution: Enhanced from marketingskills by Corey Haines (MIT License)
