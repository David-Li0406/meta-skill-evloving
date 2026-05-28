# Project Templates and Spec Examples

This reference provides templates and examples for structuring projects according to Linear Method principles.

## Project Spec Template

```markdown
# [Project Name]

**Timeline**: [Start] - [Target completion]
**Owner**: [Your name]
**Status**: [Planning / In Progress / Complete]

## Why

[1-2 sentences on the problem this solves or opportunity it enables]

## What

[2-3 sentences describing what you're building]

## How

[High-level approach, key decisions, main components]

## Success Criteria

- [Measurable outcome 1]
- [Measurable outcome 2]

## Out of Scope (V1)

- [Feature we're explicitly not building yet]
- [Polish that can wait for V2]

## Dependencies

- [Required work that must be done first]

## Issues

[List of 5-15 issues that will deliver this project]
```

## Example Projects

### Example 1: Authentication System (MVP)

```markdown
# User Authentication System

**Timeline**: Nov 4 - Nov 18 (2 weeks)
**Owner**: You
**Status**: Planning

## Why

Users need to save their work and access it across devices. Currently everything 
is ephemeral and lost on browser close.

## What

Email/password authentication with:
- Signup and login flows
- Password reset via email
- Session management
- Protected routes

## How

- Use NextAuth.js for session handling
- Store user data in PostgreSQL
- Use Resend for password reset emails
- JWT tokens in httpOnly cookies

## Success Criteria

- Users can create accounts and log in
- Sessions persist for 30 days
- Password reset flow works end-to-end
- All user data properly associated with accounts

## Out of Scope (V1)

- OAuth providers (Google, GitHub)
- Email verification (not required for V1)
- 2FA
- Account deletion flow

## Dependencies

- PostgreSQL database setup (completed)
- Email service integration (in progress)

## Issues

1. Set up NextAuth.js configuration
2. Create database schema for users and sessions
3. Build signup form and API route
4. Build login form and API route
5. Add session middleware to protect routes
6. Implement password reset request flow
7. Implement password reset completion flow
8. Add error handling and validation
9. Test full authentication flow
10. Update existing features to use user accounts
```

**Breakdown rationale**: Each issue is 1-2 days of focused work. Total is ~10-12 days, fits in 2-week cycle with buffer.

---

### Example 2: Dashboard Analytics (Scoped Down)

```markdown
# Dashboard Analytics V1

**Timeline**: Nov 4 - Nov 11 (1 week)
**Owner**: You
**Status**: Planning

## Why

Users want to see their progress and understand their usage patterns. Currently 
we have the data but no way to visualize it.

## What

Simple dashboard showing:
- Total items created (number + sparkline)
- Activity this week (bar chart)
- Most used features (list)

## How

- Query data from existing database tables
- Use Recharts for visualization
- Server-side data fetching for performance
- Cache results for 5 minutes

## Success Criteria

- Dashboard loads in < 1 second
- Shows accurate data for logged-in user
- Works on mobile and desktop
- Updates when user creates new items

## Out of Scope (V1)

- Custom date ranges
- Export to CSV
- Compare to previous periods
- Team-wide analytics
- Goal tracking

## Dependencies

- User authentication system (must be deployed)

## Issues

1. Design dashboard layout (1 view, 3 cards)
2. Create API endpoint for dashboard data
3. Build total items card with sparkline
4. Build activity chart card
5. Build top features card
6. Add loading states
7. Test with real user data
```

**Breakdown rationale**: Scoped to essentials only. V2 can add fancy features later. Each issue ~1 day = 1 week total.

---

### Example 3: Multi-Stage Project (Payment System)

```markdown
# Payment System - Stage 1: Checkout

**Timeline**: Nov 4 - Nov 18 (2 weeks)
**Owner**: You
**Status**: Planning

## Why

We're ready to monetize. Need way to collect payment and create paid accounts.

## What (Stage 1 Only)

One-time payment checkout flow:
- Pricing page showing plans
- Stripe Checkout integration
- Payment success/failure handling
- Upgrade user to paid status

## How

- Use Stripe Checkout (hosted, not embedded)
- Store Stripe customer ID in our database
- Webhook to handle successful payments
- Redirect back to app after payment

## Success Criteria

- Users can click "Upgrade" and complete payment
- Account automatically upgraded after payment
- Payment failure handled gracefully
- Revenue tracked in Stripe dashboard

## Out of Scope (Stage 1)

❌ Subscriptions (Stage 2)
❌ Self-serve plan changes (Stage 3)
❌ Billing portal (Stage 3)
❌ Invoices/receipts (Stage 3)
❌ Promo codes (Later)

## Future Stages

**Stage 2** (2 weeks): Convert to subscriptions, add cancellation
**Stage 3** (1 week): Billing portal for self-serve management
**Stage 4** (1 week): Invoice generation and email delivery

## Dependencies

- User authentication (deployed)
- Stripe account setup (done)

## Issues

1. Set up Stripe API integration
2. Design pricing page
3. Build pricing page UI
4. Create checkout session API endpoint
5. Build checkout success page
6. Build checkout failure page
7. Add Stripe webhook endpoint
8. Handle payment success webhook
9. Update user status on payment
10. Add "Upgrade" CTA throughout app
11. Test full payment flow with test cards
12. Go live with production Stripe keys
```

**Breakdown rationale**: 
- Stage 1 ships in 2 weeks with minimum viable payment flow
- Future stages clearly scoped and estimated
- Users can start paying immediately, refinements come later

---

### Example 4: Exploration/Research Project

```markdown
# Mobile App Strategy Research

**Timeline**: Nov 4 - Nov 8 (1 week)
**Owner**: You
**Status**: Planning

## Why

We're seeing 40% of users on mobile but our web app isn't great on mobile.
Need to decide: improve web responsive, build PWA, or build native app.

## What

Research project to make informed decision about mobile strategy.

## How

- Test current mobile web experience with real users
- Research PWA capabilities and limitations
- Evaluate React Native vs native development
- Estimate effort for each approach
- Make recommendation with reasoning

## Success Criteria

- Decision document with recommendation
- Pros/cons analysis of each approach
- Rough effort estimate for chosen approach
- Buy-in from team on direction

## Out of Scope

- Building anything (that's next project)
- Detailed technical specs
- Design work

## Issues

1. Test current mobile web with 5 users
2. List must-have mobile features
3. Research PWA capabilities
4. Research React Native approach
5. Get quotes from native developers
6. Write decision document
7. Present to team and get feedback
8. Finalize recommendation
```

**Breakdown rationale**: Pure research/decision-making project. Each issue is investigation or documentation. Ends with clear next steps.

---

## Project Size Guidelines

### 1 Week Projects (5-8 issues)

- Single feature with clear scope
- Improvement to existing feature
- Small integration
- Design system work
- Performance optimization
- Research/exploration

**Examples**:
- "Add search to product catalog"
- "Improve dashboard loading speed"
- "Integrate Slack notifications"
- "Build design system color tokens"

### 2 Week Projects (10-15 issues)

- Medium-sized feature
- Significant refactor
- Multi-step user flow
- Complex integration
- V1 of major feature

**Examples**:
- "User authentication system"
- "Payment checkout flow"
- "Email notification system"
- "Mobile responsive redesign"

### 3-4 Week Projects (15-20 issues)

- Large feature with multiple components
- Significant architectural change
- Multi-stage rollout

**Examples**:
- "Team collaboration features"
- "Admin dashboard"
- "API platform"
- "Multi-tenant architecture"

### Anything Longer → Break Into Stages

**Bad**: "Build entire admin portal" (12 weeks)

**Good**: 
- Stage 1: User management (2 weeks)
- Stage 2: Analytics dashboard (2 weeks)
- Stage 3: Billing management (2 weeks)
- Stage 4: Team settings (1 week)
- Stage 5: Audit logging (1 week)

Ship each stage independently. Learn and adjust between stages.

## Project Spec Principles

### Keep Specs Brief

✅ Good length: 200-400 words
❌ Too long: 2000+ word detailed requirements doc

**Why**: Short specs get read. Long specs get skipped.

### Write Before Building

Linear often spends 1-2 weeks on specs before writing code. This is good!

Better to think deeply upfront than rebuild halfway through.

### Evolve Specs During Building

Specs can change as you learn. That's normal.

Update the spec when you make significant decisions or changes in approach.

### Include "Out of Scope"

Explicitly list what you're NOT building. Prevents scope creep and sets expectations.

## Common Project Anti-Patterns

### ❌ Anti-Pattern 1: Vague Scope

```markdown
# Improve User Experience

Timeline: TBD
Why: Users want better experience
What: Make things better
How: TBD
```

**Fix**: Be specific about what you're improving and how.

### ❌ Anti-Pattern 2: No Timeline

```markdown
# New Feature X

Why: Users requested this
What: Build feature X
How: Standard implementation
Issues: TBD
```

**Fix**: Add target date even if rough. Creates healthy urgency.

### ❌ Anti-Pattern 3: Everything in One Project

```markdown
# Complete App Overhaul

Timeline: 6 months
50 issues covering entire product redesign
```

**Fix**: Break into multiple stages that ship independently.

### ❌ Anti-Pattern 4: No Clear Owner

```markdown
# Team Collaboration

Owner: Engineering team
```

**Fix**: Single person owns each project. They can delegate, but they're responsible.

## Project Status Updates

**Weekly updates** help team stay aligned (even solo, helps you reflect):

```markdown
Week of Nov 4:

✅ Completed
- Set up auth library
- Built signup form
- Created user database schema

🚧 In Progress  
- Building login flow (60% done)
- Password reset logic (blocked on email service)

🔜 Next
- Session middleware
- Protected routes

⚠️ Blockers
- Waiting on email service API keys from IT
```

## Quick Reference

**Good project characteristics:**
- 1-3 weeks max
- 5-15 issues
- Clear owner
- Brief spec (< 500 words)
- Specific scope
- Measurable success criteria
- Ships something usable

**When project seems too big:**
1. Can we scope down to essentials only?
2. Can we break into V1/V2 stages?
3. Can we ship partial functionality first?
4. What's the smallest version that provides value?
