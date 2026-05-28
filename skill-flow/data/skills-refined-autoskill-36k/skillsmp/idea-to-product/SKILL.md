---
name: idea-to-product
description: "Use when rapidly prototyping ideas into products. Covers MVP scoping, feature prioritization, tech stack selection, timeline estimation, and launch checklist."
---

# Idea to Product

## Overview

Transform ideas into shippable products with systematic MVP scoping, feature prioritization, tech stack selection, and launch planning. Focus on rapid validation and iterative development.

## When to Use

- Starting a new product or side project
- Validating a business idea
- Scoping MVP features
- Planning a launch timeline
- Prioritizing features for limited resources

## Quick Reference

| Phase | Duration | Focus |
|-------|----------|-------|
| **Ideation** | 1-2 days | Problem validation |
| **Scoping** | 1-2 days | MVP definition |
| **Stack Selection** | 0.5 day | Tech choices |
| **Build** | 1-4 weeks | Core features only |
| **Launch** | 1-2 days | Ship and learn |

---

## Phase 1: Problem Validation

### Before Building Anything

```markdown
## Problem Statement

**Who** has this problem?
[Specific persona, not "everyone"]

**What** is the problem?
[Concrete pain point they experience]

**When** does it occur?
[Trigger or context]

**Why** is it painful?
[Consequences of the problem]

**How** do they currently solve it?
[Existing alternatives, workarounds]
```

### Validation Checklist

```markdown
- [ ] Can I describe the problem in one sentence?
- [ ] Have I talked to 5+ potential users?
- [ ] Do they actively search for solutions?
- [ ] Are they willing to pay or invest time?
- [ ] Is the market big enough to matter?
```

### Signal Strength Matrix

| Signal | Weak | Medium | Strong |
|--------|------|--------|--------|
| **Problem acknowledgment** | "Yeah, that's annoying" | "I deal with this weekly" | "I'd pay to fix this" |
| **Current solution** | "I just live with it" | "I use [basic tool]" | "I built my own workaround" |
| **Urgency** | "Eventually..." | "When I have time" | "ASAP, this is killing me" |
| **Budget** | "Free only" | "Maybe $X/month" | "Take my money" |

---

## Phase 2: MVP Scoping

### The MoSCoW Method

```markdown
## Feature Prioritization

### Must Have (Core Value)
Features without which the product has no value.
- [Feature 1] - Delivers core promise
- [Feature 2] - Essential for usability

### Should Have (Important)
Features that significantly enhance value.
- [Feature 3] - Improves experience
- [Feature 4] - Expected by users

### Could Have (Nice to Have)
Features that add polish but aren't essential.
- [Feature 5] - Delights users
- [Feature 6] - Competitive advantage

### Won't Have (Not Now)
Features explicitly deferred to later.
- [Feature 7] - V2 consideration
- [Feature 8] - If demand appears
```

### MVP Definition Template

```markdown
## MVP Definition: [Product Name]

### Core Value Proposition
[One sentence: What you do + for whom + why it matters]

### Must-Ship Features
1. [Feature] - Because [reason]
2. [Feature] - Because [reason]
3. [Feature] - Because [reason]

### Success Metrics
- [ ] [Metric 1]: Target value
- [ ] [Metric 2]: Target value
- [ ] [Metric 3]: Target value

### Explicit Non-Goals (V1)
- NOT building: [feature]
- NOT supporting: [platform/use case]
- NOT optimizing for: [metric]

### Time Budget
- Total: [X days/weeks]
- Build: [Y days]
- Test: [Z days]
- Launch: [W days]
```

### Feature Sizing

```typescript
interface Feature {
  name: string;
  value: 'low' | 'medium' | 'high';  // User value
  effort: 'low' | 'medium' | 'high'; // Dev effort
  risk: 'low' | 'medium' | 'high';   // Technical risk
}

// Priority Score: Value / (Effort * Risk)
// Build high-value, low-effort, low-risk first
```

| Quadrant | Action |
|----------|--------|
| High Value + Low Effort | **Build First** - Quick wins |
| High Value + High Effort | **Plan Carefully** - Core investment |
| Low Value + Low Effort | **Maybe Later** - Nice additions |
| Low Value + High Effort | **Skip** - Waste of time |

---

## Phase 3: Tech Stack Selection

### Decision Framework

```markdown
## Stack Selection Criteria

### Team Factors
- [ ] Team familiarity (Can we ship fast?)
- [ ] Hiring pool (Can we scale the team?)
- [ ] Documentation quality (Can we self-serve?)

### Product Factors
- [ ] Performance requirements (What scale?)
- [ ] Platform targets (Web/mobile/desktop?)
- [ ] Offline requirements (Always connected?)

### Business Factors
- [ ] Time to market (How fast?)
- [ ] Maintenance cost (Long-term burden?)
- [ ] Vendor lock-in (Exit strategy?)
```

### Recommended Stacks by Use Case

| Use Case | Stack | Why |
|----------|-------|-----|
| **SaaS MVP** | Next.js + Supabase + Vercel | Full-stack fast, scales well |
| **AI Product** | Next.js + Python API + Vercel | Best AI libraries in Python |
| **Mobile App** | React Native + Supabase | Cross-platform, shared logic |
| **Landing Page** | Next.js + Tailwind | Fast, SEO-friendly |
| **API Product** | Node.js + PostgreSQL | Simple, well-understood |
| **Real-time** | Next.js + Supabase Realtime | Built-in WebSocket support |

### Stack Template: SaaS MVP

```markdown
## Tech Stack: [Product Name]

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS + shadcn/ui
- **State**: React hooks + Zustand (if needed)

### Backend
- **Database**: Supabase (PostgreSQL + Auth + Storage)
- **API**: Next.js Route Handlers + Server Actions
- **Background Jobs**: Vercel Cron or Inngest

### Infrastructure
- **Hosting**: Vercel
- **Domain**: Namecheap or Cloudflare
- **Email**: Resend or Postmark
- **Analytics**: Plausible or PostHog

### Payments (if needed)
- **Provider**: Stripe or Polar
- **Billing**: Usage-based or subscription

### Rationale
[Why these choices for THIS product]
```

---

## Phase 4: Build Phase

### Sprint Structure

```markdown
## Build Sprint: [Week N]

### Focus
[Single sentence describing this sprint's goal]

### Daily Targets
- Day 1: [Deliverable]
- Day 2: [Deliverable]
- Day 3: [Deliverable]
- Day 4: [Deliverable]
- Day 5: [Buffer + Polish]

### Definition of Done
- [ ] Feature works end-to-end
- [ ] Basic error handling
- [ ] Mobile responsive
- [ ] Tested manually
```

### Implementation Order

```
1. Auth & User Management
   - Sign up / Sign in
   - Basic profile

2. Core Value Feature
   - The ONE thing users came for
   - Make it work, not perfect

3. Essential Infrastructure
   - Error handling
   - Loading states
   - Basic validation

4. Supporting Features
   - Settings
   - Help/FAQ
   - Notifications

5. Polish (if time permits)
   - Animations
   - Edge cases
   - Performance
```

### Code Quality vs Speed

| Phase | Quality Focus |
|-------|---------------|
| **Pre-PMF** | Ship fast, fix later. Working > Perfect. |
| **Post-PMF** | Invest in quality. Stability matters. |

```markdown
## Acceptable Shortcuts (Pre-PMF)
- [ ] Simple error messages (not perfect UX)
- [ ] Manual processes (not automated)
- [ ] Limited customization
- [ ] Basic mobile support
- [ ] Console logging instead of monitoring

## Never Shortcut
- [ ] Security (auth, data protection)
- [ ] Data integrity (backups, validation)
- [ ] Payment handling
- [ ] User privacy
```

---

## Phase 5: Launch Checklist

### Pre-Launch (T-7 days)

```markdown
## Pre-Launch Checklist

### Core Product
- [ ] All Must-Have features working
- [ ] Critical bugs fixed
- [ ] Error handling in place
- [ ] Loading states everywhere

### Legal & Compliance
- [ ] Privacy Policy
- [ ] Terms of Service
- [ ] Cookie consent (if EU)
- [ ] GDPR data export (if EU)

### Infrastructure
- [ ] Production environment setup
- [ ] Domain configured
- [ ] SSL working
- [ ] Email delivery tested
- [ ] Payment flow tested (if applicable)

### Analytics & Monitoring
- [ ] Analytics installed
- [ ] Error tracking (Sentry)
- [ ] Uptime monitoring

### Content
- [ ] Landing page copy finalized
- [ ] Help docs / FAQ
- [ ] Email templates
```

### Launch Day (T-0)

```markdown
## Launch Day Checklist

### Morning
- [ ] Final production deployment
- [ ] Smoke test all critical paths
- [ ] Confirm monitoring is active
- [ ] Prepare social posts

### Announce
- [ ] Social media (Twitter/X, LinkedIn)
- [ ] Product Hunt (if applicable)
- [ ] Hacker News (if applicable)
- [ ] Communities (Reddit, Discord, Slack)
- [ ] Email to waitlist

### Monitor
- [ ] Watch error tracking
- [ ] Monitor response times
- [ ] Track signups in real-time
- [ ] Respond to feedback quickly
```

### Post-Launch (T+1 to T+7)

```markdown
## Post-Launch Checklist

### Day 1
- [ ] Review all error reports
- [ ] Respond to user feedback
- [ ] Hot-fix critical issues
- [ ] Share launch metrics

### Week 1
- [ ] Analyze user behavior
- [ ] Identify top friction points
- [ ] Plan quick wins
- [ ] Gather testimonials
- [ ] Schedule user interviews
```

---

## Timeline Templates

### Weekend MVP (2-3 days)

```
Day 1: Setup + Core feature
- Project scaffolding
- Auth setup
- Main feature MVP

Day 2: Polish + Launch prep
- UI cleanup
- Landing page
- Deploy

Day 3: Launch + Iterate
- Push live
- Announce
- Fix issues
```

### Two-Week MVP

```
Week 1:
- Days 1-2: Setup + Auth
- Days 3-4: Core feature
- Day 5: Secondary features

Week 2:
- Days 1-2: Polish + Edge cases
- Day 3: Landing page
- Day 4: Testing + Fixes
- Day 5: Launch
```

### One-Month MVP

```
Week 1: Foundation
- Project setup
- Auth + Users
- Database schema

Week 2: Core Features
- Primary value feature
- Secondary features
- Basic UI

Week 3: Polish
- Error handling
- Loading states
- Mobile responsive

Week 4: Launch
- Landing page
- Documentation
- Deploy + Launch
```

---

## Common Patterns

### Landing Page Formula

```markdown
1. **Hero**: Clear value prop + CTA
2. **Problem**: Pain point acknowledgment
3. **Solution**: How you solve it
4. **Features**: 3-4 key benefits
5. **Social Proof**: Testimonials/logos
6. **Pricing**: Simple, clear options
7. **FAQ**: Address objections
8. **Final CTA**: Repeat main action
```

### Waitlist Strategy

```typescript
// Simple waitlist with position tracking
interface WaitlistEntry {
  email: string;
  position: number;
  referralCode: string;
  referredBy?: string;
  createdAt: Date;
}

// Incentive: Move up by referring others
// "You're #47. Refer friends to move up!"
```

### Soft Launch Strategy

```markdown
1. **Alpha**: Internal testing only
2. **Closed Beta**: Invite 10-20 users
3. **Open Beta**: Waitlist access
4. **Soft Launch**: Low-key public access
5. **Hard Launch**: Full announcement
```

---

## Red Flags - STOP

**Never:**
- Build for months without user feedback
- Add features "because competitors have them"
- Perfect before shipping
- Build complex infrastructure for V1
- Skip the validation phase

**Always:**
- Talk to users before building
- Define MVP scope explicitly
- Ship embarrassingly early
- Measure what matters
- Iterate based on feedback

---

## Integration

**Related skills:** brainstorm, plan, analytics, payment-processing
**Tools:** Vercel, Supabase, Stripe, Product Hunt
