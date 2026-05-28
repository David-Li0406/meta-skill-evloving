# Product-Led Growth

## Patterns


---
  #### **Name**
Self-Serve Funnel Design
  #### **Description**
Optimizing the path from visitor to activated user
  #### **When To Use**
Building or improving PLG motion
  #### **Implementation**
    ## PLG Funnel Architecture
    
    ### 1. The PLG Funnel Stages
    
    ```
    Visitor → Signup → Setup → Aha Moment → Habit → Paid → Expand
                ↓        ↓        ↓            ↓       ↓       ↓
            [Friction] [Friction] [Value]   [Retention] [Convert] [Grow]
    ```
    
    ### 2. Key Metrics by Stage
    
    | Stage | Metric | Target | Optimization |
    |-------|--------|--------|--------------|
    | Visit→Signup | Conversion Rate | 2-5% | Landing page, social proof |
    | Signup→Setup | Completion Rate | 70-90% | Onboarding flow, progressive |
    | Setup→Aha | Activation Rate | 40-60% | Time-to-value, guidance |
    | Aha→Habit | Week 1 Retention | 30-50% | Engagement hooks, notifications |
    | Habit→Paid | Free→Paid Conv | 2-5% | Paywall placement, value gates |
    | Paid→Expand | Net Revenue Ret | 100-120% | Usage growth, seat expansion |
    
    ### 3. Signup Optimization
    
    **Remove Friction**
    - SSO/OAuth options (Google, GitHub, etc.)
    - Minimal required fields
    - No email verification before value
    - No credit card for free tier
    
    **Add Motivation**
    - Clear value proposition above fold
    - Social proof (logos, numbers)
    - Specific use case messaging
    - Immediate value preview
    
    ### 4. Setup Optimization
    
    **Progressive Disclosure**
    - Only ask what's needed NOW
    - Defer optional setup
    - Show progress (1 of 3)
    - Allow skipping
    
    **Template/Import Magic**
    - Pre-built templates
    - Import from competitors
    - AI-assisted setup
    - Clone from team
    
    ### 5. Activation Optimization
    
    **Define Your Aha Moment**
    - What action correlates with retention?
    - When do users "get it"?
    - Can you measure it?
    
    Examples:
    - Slack: Send 2000 messages as team
    - Dropbox: Upload 1 file, access from 2 devices
    - Zoom: Complete first meeting
    
    **Reduce Time to Aha**
    - Guided tours with real actions
    - Pre-populated data/content
    - Contextual help
    - Success celebrations
    

---
  #### **Name**
Freemium Model Design
  #### **Description**
Designing the free tier for conversion
  #### **When To Use**
Deciding what to offer for free
  #### **Implementation**
    ## Freemium Strategy
    
    ### 1. Freemium Types
    
    | Type | What's Limited | Best For |
    |------|----------------|----------|
    | Feature-limited | Advanced features locked | Clear feature tiers |
    | Usage-limited | Volume/quantity caps | Usage-based products |
    | Time-limited | Trial period | High-value, complex products |
    | Capacity-limited | Seats/users limited | Collaboration tools |
    | Hybrid | Combination | Most PLG products |
    
    ### 2. What to Include in Free
    
    **MUST Include**
    - Core aha moment experience
    - Enough to demonstrate value
    - Shareable/viral features
    - Enough to create habit
    
    **MUST Exclude**
    - Features only valuable at scale
    - Team/admin features
    - Advanced integrations
    - SLA/support
    
    ### 3. Free-to-Paid Triggers
    
    **Natural Limits**
    ```
    User hits limit → Sees value → Willing to pay
    
    Examples:
    - Slack: Message history limit
    - Zoom: 40-min meeting limit
    - Notion: Guest collaborator limit
    ```
    
    **Team Expansion**
    ```
    Individual → Invites team → Team needs paid
    
    Examples:
    - Figma: Free for individuals, paid for teams
    - Linear: Free for small, paid for larger
    ```
    
    **Enterprise Requirements**
    ```
    Free works → Need SSO/security → Must upgrade
    
    Examples:
    - Every PLG tool with Enterprise tier
    ```
    
    ### 4. Paywall Placement
    
    **When to Show Upgrade Prompt**
    - At natural friction points
    - When user hits limits
    - After aha moment achieved
    - When team features needed
    
    **How to Show**
    - Clear what they get
    - Show value already received
    - Social proof from upgraders
    - Easy path to paid
    

---
  #### **Name**
PQL (Product Qualified Lead) System
  #### **Description**
Identifying sales-ready users from product usage
  #### **When To Use**
Scaling PLG with sales assist
  #### **Implementation**
    ## PQL Architecture
    
    ### 1. What Makes a PQL
    
    ```
    PQL = Usage Signals + Fit Signals + Intent Signals
    ```
    
    **Usage Signals (Product Behavior)**
    - Activation complete
    - High engagement frequency
    - Using advanced features
    - Growing usage over time
    
    **Fit Signals (Company Match)**
    - Company size matches ICP
    - Industry/vertical fit
    - Tech stack compatibility
    - Budget indicators
    
    **Intent Signals (Buying Behavior)**
    - Viewed pricing page
    - Clicked "Contact Sales"
    - Added team members
    - Approaching limits
    
    ### 2. PQL Scoring Model
    
    | Signal Category | Weight | Example Signals |
    |----------------|--------|-----------------|
    | Activation | 25% | Completed onboarding, hit aha moment |
    | Engagement | 25% | DAU/WAU ratio, feature breadth |
    | Growth | 20% | Adding users, increasing usage |
    | Fit | 15% | Company size, industry match |
    | Intent | 15% | Pricing views, upgrade attempts |
    
    ### 3. PQL Tiers
    
    **Tier 1: High-Touch PQLs**
    - Score > 80
    - Enterprise fit
    - Immediate sales outreach
    - Personalized demo offer
    
    **Tier 2: Mid-Touch PQLs**
    - Score 50-80
    - Growth potential
    - Automated + human touch
    - Self-serve upgrade path
    
    **Tier 3: Low-Touch PQLs**
    - Score 30-50
    - SMB/individual
    - Fully automated nurture
    - In-app upgrade prompts
    
    ### 4. Sales Handoff
    
    **Context to Provide Sales**
    - Specific product usage
    - Features used/not used
    - Team size and growth
    - Engagement trends
    - Potential use cases
    
    **Outreach Best Practices**
    - Reference actual usage
    - Offer value (not just "check in")
    - Suggest next steps in product
    - Time based on activity
    

---
  #### **Name**
Activation Metric Design
  #### **Description**
Defining and measuring activation
  #### **When To Use**
Setting up PLG analytics
  #### **Implementation**
    ## Activation Metrics
    
    ### 1. Finding Your Aha Moment
    
    **Data Analysis Method**
    1. Export cohort of retained users (Week 4+)
    2. Export cohort of churned users
    3. Compare actions taken in Week 1
    4. Find actions with highest correlation to retention
    
    **Interview Method**
    1. Ask retained users: "When did you know this was for you?"
    2. Look for common patterns
    3. Translate to measurable action
    
    ### 2. Activation Metric Criteria
    
    **Good Activation Metrics**
    - Strongly correlated with retention
    - Achievable in first session/day
    - Measurable automatically
    - Something user controls
    
    **Bad Activation Metrics**
    - Vanity (just signed up)
    - Too easy (no value delivered)
    - Too hard (takes weeks)
    - Outside user control
    
    ### 3. Example Activation Metrics
    
    | Product | Activation Metric | Rationale |
    |---------|-------------------|-----------|
    | Slack | 2000 team messages | Indicates team adoption |
    | Dropbox | File on 2+ devices | Core value demonstrated |
    | HubSpot | 1 form submission | Lead capture proven |
    | Calendly | 1 meeting booked | Scheduling value shown |
    | Notion | 5 pages created | Personal wiki started |
    
    ### 4. Activation Funnel Dashboard
    
    ```
    Activation Funnel (Cohort: Last 7 Days)
    
    Signed Up:        1,000   100%
    Completed Setup:    750    75%  ← Onboarding friction
    Core Action #1:     500    50%  ← Value confusion
    Core Action #2:     300    30%  ← Complexity barrier
    Aha Moment:         200    20%  ← TARGET: 40%+
    
    Time to Aha:
    - P50: 2.3 days
    - P75: 5.1 days
    - P90: 11 days
    ```
    

---
  #### **Name**
PLG Organizational Design
  #### **Description**
Structuring teams for product-led growth
  #### **When To Use**
Building PLG org or transitioning from sales-led
  #### **Implementation**
    ## PLG Organization
    
    ### 1. Key PLG Roles
    
    | Role | Focus | Metrics |
    |------|-------|---------|
    | Growth PM | Acquisition + Activation | Signup→Activated |
    | Growth Engineer | Experiments + Instrumentation | Velocity + Impact |
    | PLG Marketing | Demand + Content | Signups + MQLs |
    | PLG Sales (PLS) | PQL conversion | PQL→Paid, Expansion |
    | Rev Ops | Metrics + Tools | Data quality, Automation |
    
    ### 2. Team Structures
    
    **Embedded Model**
    ```
    Product Team
    └── Growth PM
    └── Growth Engineer
    └── Designer
    
    Marketing Team
    └── PLG Marketing
    
    Sales Team
    └── PLS Reps
    ```
    
    **Growth Pod Model**
    ```
    Growth Pod (cross-functional)
    ├── Growth PM
    ├── Growth Engineer
    ├── PLG Marketing
    ├── Data Analyst
    └── Designer
    ```
    
    ### 3. Metrics Ownership
    
    **Growth Team Owns**
    - Visitor → Signup
    - Signup → Activated
    - Activation Rate
    - Time to Value
    
    **Product Team Owns**
    - Core product experience
    - Feature development
    - Retention (post-activation)
    
    **Sales Team Owns**
    - PQL conversion
    - Enterprise deals
    - Expansion revenue
    
    ### 4. Common Org Tensions
    
    **Sales vs Self-Serve**
    Problem: Sales comp on deals self-serve would win
    Solution: Segment by deal size, adjust comp
    
    **Product vs Growth**
    Problem: Growth "hacks" vs product quality
    Solution: Growth team in product org, shared metrics
    
    **Marketing vs Product**
    Problem: Who owns in-product messaging?
    Solution: Clear ownership by funnel stage
    

## Anti-Patterns


---
  #### **Name**
Premature PLG
  #### **Description**
Forcing PLG before product-market fit
  #### **Why Bad**
    PLG amplifies whatever you have.
    No PMF = amplifying confusion.
    Users churn faster than you can acquire.
    
  #### **What To Do Instead**
    Prove PMF with high-touch first.
    Understand ideal activation path.
    Then systematize for self-serve.
    

---
  #### **Name**
Free-for-Free's Sake
  #### **Description**
Giving away too much in free tier
  #### **Why Bad**
    Users never need to pay.
    Attracts wrong customers.
    Revenue suffers.
    
  #### **What To Do Instead**
    Free tier exists to create paying customers.
    Give enough to prove value, limit at need.
    Track free→paid conversion relentlessly.
    

---
  #### **Name**
Ignoring Activation
  #### **Description**
Measuring signups but not activation
  #### **Why Bad**
    Signups are vanity metric.
    Unactivated users churn.
    CAC wasted on churned users.
    
  #### **What To Do Instead**
    Define clear activation metric.
    Optimize for activated users, not signups.
    Measure CAC per activated user.
    

---
  #### **Name**
PLG Without Data
  #### **Description**
Doing PLG without instrumentation
  #### **Why Bad**
    Can't find friction points.
    Can't identify PQLs.
    Can't measure improvements.
    
  #### **What To Do Instead**
    Instrument every step of funnel.
    Build activation funnel dashboard.
    Track cohorts through expansion.
    

---
  #### **Name**
Sales-Led Org Doing PLG
  #### **Description**
Keeping sales-led comp/process with PLG product
  #### **Why Bad**
    Sales intercepts self-serve deals.
    Poor handoff to product.
    Metrics conflict.
    
  #### **What To Do Instead**
    Redesign comp for PLG.
    Clear rules on when sales engages.
    Align incentives with self-serve success.
    