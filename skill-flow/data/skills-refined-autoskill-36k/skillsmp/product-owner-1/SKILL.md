---
name: product-owner
description: Product Owner skill for managing product backlogs, user stories, roadmaps, requirements gathering, and stakeholder communication. Use when working with product strategy, feature prioritization, sprint planning, or user story creation.
---

# Product Owner

A comprehensive skill designed to assist Product Owners in managing product development, defining requirements, prioritizing features, and communicating with stakeholders.

## Quick Start

Basic Product Owner workflow:

```
# Define product vision
# Gather requirements
# Create user stories
# Prioritize backlog
# Plan sprints
# Communicate with stakeholders
```

## Core Capabilities

### 1. Product Vision & Strategy

Define and communicate product direction:

- **Vision Statement**: Articulate the product's purpose and goals
- **Product Goals**: Set measurable objectives (OKRs, KPIs)
- **Value Proposition**: Define what makes the product valuable
- **Market Analysis**: Understand competitors and market position
- **Roadmap Planning**: Strategic feature planning over time

### 2. Requirements Gathering

Collect and document requirements:

- **Stakeholder Interviews**: Extract needs from users and stakeholders
- **User Research**: Conduct surveys, interviews, usability tests
- **Feature Requests**: Capture and evaluate feature ideas
- **Business Requirements**: Document business needs and constraints
- **Technical Constraints**: Understand technical limitations

### 3. User Story Creation

Write effective user stories:

**User Story Format:**
```
As a [type of user]
I want [goal/desire]
So that [benefit/reason]
```

**Acceptance Criteria:**
```
Given [context]
When [action]
Then [expected outcome]
```

**INVEST Principles:**
- **I**ndependent: Stories should be self-contained
- **N**egotiable: Details can be discussed
- **V**aluable: Provides value to users
- **E**stimable: Team can estimate effort
- **S**mall: Fits in one sprint
- **T**estable: Clear acceptance criteria

### 4. Backlog Management

Maintain a healthy product backlog:

- **Backlog Grooming**: Regular refinement sessions
- **Prioritization**: Order items by value and urgency
- **Estimation**: Support team in sizing work
- **Dependencies**: Identify and manage dependencies
- **Technical Debt**: Balance features with tech debt

### 5. Sprint Planning

Plan effective sprints:

- **Sprint Goals**: Define clear objectives
- **Capacity Planning**: Match work to team capacity
- **Story Selection**: Choose right stories for sprint
- **Definition of Done**: Ensure shared understanding
- **Risk Assessment**: Identify potential blockers

### 6. Stakeholder Communication

Keep stakeholders informed:

- **Status Updates**: Regular progress reports
- **Demo Preparation**: Showcase completed work
- **Expectation Management**: Align on timelines
- **Feedback Collection**: Gather stakeholder input
- **Change Communication**: Explain scope or priority changes

## User Story Templates

### Feature Story

```
TITLE: User Login with Email

As a registered user
I want to log in using my email and password
So that I can access my personalized dashboard

Acceptance Criteria:
- Given I'm on the login page
  When I enter valid credentials
  Then I should be redirected to my dashboard

- Given I'm on the login page
  When I enter invalid credentials
  Then I should see an error message "Invalid email or password"

- Given I'm logged in
  When I close and reopen the app within 7 days
  Then I should remain logged in

Technical Notes:
- Use JWT tokens for session management
- Implement rate limiting (5 attempts per 15 minutes)
- Support OAuth as future enhancement

Dependencies:
- User registration must be completed first

Story Points: 5
Priority: High
Sprint: Sprint 12
```

### Bug Story

```
TITLE: Shopping cart total shows incorrect amount

As a customer
I want the cart total to accurately reflect my items
So that I know exactly how much I'll be charged

Current Behavior:
When adding items to cart, the total sometimes shows $0.00

Expected Behavior:
Total should update immediately and show correct sum

Steps to Reproduce:
1. Add item A ($20) to cart
2. Add item B ($15) to cart
3. Observe total shows $0.00 instead of $35.00

Impact: High (blocks purchases)
Frequency: Intermittent (30% of the time)
Browser: Chrome 120, Firefox 115

Story Points: 3
Priority: Critical
Sprint: Sprint 12
```

### Technical Story

```
TITLE: Migrate user database to PostgreSQL

As a development team
We want to migrate from MySQL to PostgreSQL
So that we can use advanced features and improve performance

Acceptance Criteria:
- All user data migrated without loss
- Application works with new database
- Rollback plan tested and documented
- Performance benchmarks show improvement

Technical Approach:
1. Set up PostgreSQL instance
2. Create migration scripts
3. Test in staging environment
4. Schedule maintenance window
5. Execute migration
6. Verify data integrity

Dependencies:
- DevOps team availability
- Stakeholder approval for downtime

Story Points: 13
Priority: Medium
Sprint: Sprint 14
```

## Prioritization Frameworks

### 1. MoSCoW Method

```
Must Have: Critical for release
Should Have: Important but not vital
Could Have: Nice to have if time permits
Won't Have: Not in this release
```

### 2. RICE Score

```
RICE = (Reach × Impact × Confidence) / Effort

Reach: How many users affected (per quarter)
Impact: Scale 0.25 (minimal) to 3 (massive)
Confidence: Percentage (100% = high confidence)
Effort: Person-months of work

Example:
Feature A: (1000 × 2 × 80%) / 2 = 800
Feature B: (500 × 3 × 90%) / 1 = 1350
→ Prioritize Feature B
```

### 3. Value vs Effort Matrix

```
High Value, Low Effort → Do First (Quick Wins)
High Value, High Effort → Plan Carefully (Major Projects)
Low Value, Low Effort → Do Later (Fill-ins)
Low Value, High Effort → Avoid (Money Pits)
```

## Roadmap Planning

### Quarterly Roadmap Template

```markdown
# Q1 2025 Product Roadmap

## Theme: Improve User Engagement

### January
- ✅ User onboarding flow redesign
- ✅ Push notification system
- 🚧 Social sharing features

### February
- 📋 Gamification elements
- 📋 Achievement system
- 📋 User profile enhancements

### March
- 📋 Referral program
- 📋 Community features
- 📋 Analytics dashboard v2

## Key Metrics
- DAU increase: 20%
- Retention rate: +15%
- NPS score: 50+

## Dependencies
- Mobile team capacity (2 developers)
- Design resources (1 designer, 50% allocated)
- Marketing campaign launch (late February)

## Risks
- ⚠️ Third-party API integration delays
- ⚠️ Holiday season team availability
```

## Sprint Planning Template

```markdown
# Sprint 12 Planning (Jan 15 - Jan 29, 2025)

## Sprint Goal
Complete user authentication system and fix critical cart bugs

## Team Capacity
- 2 weeks = 10 working days
- 4 developers × 6 hours/day = 240 hours
- Reserve 20% for meetings/overhead = 192 productive hours
- Story point velocity: ~30 points

## Committed Stories

### High Priority (Must Complete)
1. [5 pts] User login with email (#123)
2. [3 pts] Fix cart total calculation bug (#456)
3. [8 pts] Implement password reset flow (#124)

### Medium Priority (Should Complete)
4. [5 pts] Add OAuth social login (#125)
5. [3 pts] Email verification system (#126)

### Low Priority (If Time Permits)
6. [2 pts] Remember me functionality (#127)
7. [2 pts] Login analytics tracking (#128)

**Total Committed: 28 points** (93% of velocity)

## Definition of Done
- [ ] Code reviewed and approved
- [ ] Unit tests written (80% coverage)
- [ ] Integration tests passing
- [ ] Manually tested in staging
- [ ] Documentation updated
- [ ] PO acceptance obtained

## Risks & Mitigation
- Risk: OAuth integration complexity
  - Mitigation: Spike completed, 3-party library chosen
- Risk: Team member out sick (2 days)
  - Mitigation: Built in 7% capacity buffer

## Demo Plan
- Show complete login flow (happy path + errors)
- Demonstrate cart fix with multiple scenarios
- Show password reset email and flow
```

## Stakeholder Communication Templates

### Weekly Status Update

```markdown
# Weekly Product Update - Week of Jan 15, 2025

## 🎯 This Week's Goals
1. Complete user authentication MVP
2. Fix critical cart bug affecting 30% of users
3. Begin OAuth integration

## ✅ Completed
- User login with email (deployed to production)
- Cart bug identified and fix in QA
- OAuth provider selection completed

## 🚧 In Progress
- Password reset flow (70% complete, on track)
- Email verification system (just started)

## ⚠️ Blockers & Risks
- OAuth API credentials delayed by IT (2 days)
  - **Action**: Escalated to IT director
  - **Impact**: May push OAuth to next sprint
  
## 📊 Metrics
- Active Users: 12,450 (+8% from last week)
- Bug Reports: 23 (-15% from last week)
- Feature Requests: 45 new requests

## 🔜 Next Week
- Deploy password reset to production
- Start OAuth integration (pending credentials)
- Begin user profile enhancements design

## 💬 Feedback Needed
- Please review new login UI mockups (link)
- Approve downtime window for database migration (Feb 1, 2am-4am)

Questions? Slack me or reply to this email.
```

### Sprint Demo Script

```markdown
# Sprint 12 Demo Script

## Introduction (2 min)
"Good afternoon! Today we're showcasing Sprint 12 deliverables. Our goal was to complete the authentication system and fix critical bugs."

## Demo 1: User Login (5 min)

**Scenario: New User Registration & Login**
1. Show registration form
   - "User fills in email, password, name"
   - "Click Register → See success message"
   
2. Show login flow
   - "User enters credentials"
   - "Click Login → Redirected to dashboard"
   
3. Show error handling
   - "Try invalid credentials → See error"
   - "Show rate limiting after 5 attempts"

**Value**: Users can now securely access their accounts

## Demo 2: Cart Bug Fix (3 min)

**Scenario: Shopping Cart Calculation**
1. Add multiple items to cart
   - "Add $20 item, add $15 item"
   - "Total shows $35 ✅ (was showing $0)"
   
2. Show edge cases
   - "Remove items → Total updates correctly"
   - "Apply discount code → Calculation accurate"

**Value**: Unblocked ~300 customers/day from completing purchases

## Demo 3: Password Reset (4 min)

**Scenario: Forgot Password Flow**
1. Click "Forgot Password"
2. Enter email → Show confirmation
3. Check email (show mock email)
4. Click reset link → Show new password form
5. Set new password → Show success
6. Login with new password

**Value**: Reduces support tickets (~20 requests/week)

## Metrics Impact (2 min)
- Login success rate: 85% → 97%
- Cart abandonment: 45% → 38%
- Support tickets: -35%

## Q&A (5 min)
Open floor for questions

**Total Time: ~20 minutes**
```

## Best Practices

### User Story Best Practices

✅ **DO:**
- Write from user's perspective
- Include clear acceptance criteria
- Keep stories small (completable in 1 sprint)
- Focus on value, not implementation
- Use consistent format
- Include testable criteria

❌ **DON'T:**
- Write technical tasks as stories
- Mix multiple features in one story
- Skip acceptance criteria
- Use vague language ("improve", "enhance")
- Forget to estimate
- Create dependencies between stories in same sprint

### Backlog Management Best Practices

✅ **DO:**
- Groom backlog weekly
- Keep top 2 sprints detailed and estimated
- Archive old/irrelevant stories
- Use labels for categorization
- Document decisions in story comments
- Involve team in estimation

❌ **DON'T:**
- Let backlog grow over 3-4 sprints
- Estimate too far ahead
- Change priorities mid-sprint
- Skip refinement sessions
- Prioritize by who asked loudest

## Metrics & KPIs

### Product Health Metrics

```
Acquisition:
- New user signups per week
- Conversion rate (visitor → signup)
- Traffic sources effectiveness

Activation:
- % users completing onboarding
- Time to first value
- Feature adoption rate

Retention:
- DAU/MAU ratio
- Churn rate
- Cohort retention curves

Revenue:
- MRR/ARR growth
- ARPU (Average Revenue Per User)
- LTV (Lifetime Value)

Referral:
- Viral coefficient
- NPS (Net Promoter Score)
- Referral conversion rate
```

### Team Velocity Metrics

```
Sprint Metrics:
- Velocity (story points/sprint)
- Commitment reliability (planned vs completed)
- Sprint goal success rate

Quality Metrics:
- Bug escape rate
- Defect density
- Test coverage

Cycle Time:
- Lead time (idea → production)
- Cycle time (start → done)
- Time in each workflow stage
```

## Tools & Resources

### Recommended Tools

- **Backlog Management**: Jira, Linear, Azure DevOps, GitHub Projects
- **Roadmapping**: ProductBoard, Aha!, Roadmunk
- **User Research**: UserTesting, Hotjar, Maze
- **Analytics**: Mixpanel, Amplitude, Google Analytics
- **Collaboration**: Miro, FigJam, Confluence

### Templates

Ver [EXAMPLES.md](EXAMPLES.md) para ejemplos completos de:
- Epic planning templates
- Release planning templates
- Stakeholder meeting agendas
- Product requirement documents (PRDs)

## Common Scenarios

### Scenario 1: Stakeholder Requests Out-of-Scope Feature Mid-Sprint

**Response:**
1. Acknowledge the request
2. Explain sprint commitment
3. Add to backlog with high priority
4. Offer to discuss in next planning
5. Provide timeline estimate

**Template:**
```
"Thanks for the suggestion! I've added this to our backlog 
with high priority. We're currently committed to Sprint X goals,
but we'll evaluate this in our planning session next Tuesday.

Based on initial assessment, this would likely be a 2-3 sprint effort.
Let's schedule 30 minutes to discuss requirements in detail."
```

### Scenario 2: Team Velocity Drops

**Actions:**
1. Review sprint retrospectives for patterns
2. Check for scope creep or unclear stories
3. Identify blockers (tech debt, dependencies, etc.)
4. Adjust capacity planning
5. Focus on removing impediments

### Scenario 3: Conflicting Priorities from Multiple Stakeholders

**Actions:**
1. Document all requests with business value
2. Use RICE or similar framework for objective scoring
3. Present analysis to stakeholders
4. Facilitate decision-making meeting
5. Communicate final decision with rationale

## Resources

- **Scrum Guide**: https://scrumguides.org/
- **Product Management**: https://www.productplan.com/learn/
- **User Story Mapping**: Jeff Patton's book
- **Inspired**: Marty Cagan's book on product management

---

**Pro Tip**: The best product owners balance user needs, business goals, and technical constraints while maintaining clear communication with all stakeholders.
