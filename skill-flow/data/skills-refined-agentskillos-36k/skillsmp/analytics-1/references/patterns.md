# Analytics

## Patterns


---
  #### **Name**
Event Taxonomy Design
  #### **Description**
Create consistent, hierarchical event naming convention before tracking anything
  #### **When**
Setting up analytics for new product or major feature
  #### **Example**
    Bad: "button_click", "clicked_signup", "user_registered", "signUpComplete"
    Good: Use consistent structure: [Object]_[Action]_[Context]
    
    Examples:
    - signup_started_homepage
    - signup_completed_trial
    - checkout_abandoned_payment
    - feature_enabled_settings
    
    Benefits: Easy to filter, group, and understand. Scales to thousands of events
    

---
  #### **Name**
Leading Indicator Focus
  #### **Description**
Identify and track metrics that predict future outcomes
  #### **When**
Designing dashboard or metric suite for a product area
  #### **Example**
    Lagging (outcome): Monthly recurring revenue
    Leading (predictive):
    - Weekly active users in growth phase
    - Feature adoption rate in first week
    - Support ticket sentiment
    - NPS trend
    
    Leading indicators let you act before outcomes deteriorate.
    Track both, but review leading indicators daily/weekly, lagging monthly
    

---
  #### **Name**
Cohort-Based Analysis
  #### **Description**
Group users by shared characteristics or time period to understand retention
  #### **When**
Analyzing retention, feature adoption, or user lifecycle metrics
  #### **Example**
    Instead of: "30-day retention is 45%"
    Use: Cohort analysis by sign-up week
    
    Week 1: 52% retention
    Week 2: 48% retention
    Week 3: 41% retention (← investigate what changed)
    Week 4: 43% retention
    
    Cohorts reveal trends that aggregate metrics hide.
    Common cohorts: sign-up date, acquisition channel, plan type, user segment
    

---
  #### **Name**
Funnel Decomposition
  #### **Description**
Break down conversion funnels to find highest-impact optimization points
  #### **When**
Investigating conversion issues or prioritizing optimization work
  #### **Example**
    Landing → Sign-up → Activate → Subscribe
    100%  → 12%      → 60%      → 25%
    
    Calculate drop-off at each step:
    - Landing to Sign-up: 88% drop (1,200 users)
    - Sign-up to Activate: 40% drop (105 users)
    - Activate to Subscribe: 75% drop (47 users)
    
    Highest impact: Fix landing to sign-up (12x more users affected)
    
    Also segment by source, device, geography to find which segments struggle where
    

---
  #### **Name**
North Star Metric Framework
  #### **Description**
Define single metric that best captures product value delivery
  #### **When**
Aligning team around what success looks like
  #### **Example**
    Not revenue (lagging), not sign-ups (vanity).
    Choose metric that represents value delivered to users:
    
    Slack: Messages sent in teams
    Airbnb: Nights booked
    Netflix: Hours watched
    Spotify: Time listening
    
    Properties of good North Star:
    - Captures value exchange (user gets benefit)
    - Leading indicator of revenue
    - Actionable by product/eng team
    - Measurable and moveable
    

---
  #### **Name**
Behavioral Segmentation
  #### **Description**
Segment users by what they do, not just who they are
  #### **When**
Personalizing experience or analyzing feature usage patterns
  #### **Example**
    Demographic segments (weak): Enterprise vs SMB, US vs EU
    Behavioral segments (strong):
    - Power users: Daily active, 5+ features used
    - Core users: Weekly active, 2-3 features used
    - Casual users: Monthly active, 1 feature used
    - Dormant: Signed up but never activated
    
    Behavioral segments predict retention and expansion better than demographics.
    Design different experiences and interventions for each segment
    

## Anti-Patterns


---
  #### **Name**
Vanity Metric Obsession
  #### **Description**
Tracking metrics that look good but don't drive decisions
  #### **Why**
    Page views, total sign-ups, total users are vanity metrics. They go up and to
    the right regardless of product quality. They don't tell you if users get value
    
  #### **Instead**
    Track actionable metrics: Daily actives (not total users), activation rate
    (not sign-ups), revenue per user (not total revenue). Ask: "If this metric
    changes, what decision would we make?"
    

---
  #### **Name**
Analysis Paralysis
  #### **Description**
Building complex dashboards that nobody looks at or acts on
  #### **Why**
    More metrics don't mean more insight. Too many dashboards = analysis paralysis.
    Teams stop looking when overwhelmed. "Data-driven" becomes excuse for indecision
    
  #### **Instead**
    One dashboard per team with 5-7 key metrics maximum. Each metric has owner
    and decision it drives. Kill any metric not reviewed weekly. Simplicity wins
    

---
  #### **Name**
Event Tracking Chaos
  #### **Description**
Inconsistent event naming, missing properties, duplicate events
  #### **Why**
    Makes analysis impossible. "Did we track that?" becomes common question.
    Team wastes hours debugging tracking instead of analyzing data
    
  #### **Instead**
    Create and enforce event taxonomy. Review all new events. Use TypeScript
    types or schema validation. Make incorrect tracking fail loudly in dev
    

---
  #### **Name**
Reporting Without Context
  #### **Description**
Sharing metrics without comparison, trends, or explanation
  #### **Why**
    "Conversion is 5%" - Is that good? Compared to what? Trending up or down?
    Numbers without context don't inform decisions
    
  #### **Instead**
    Always include: comparison to last period, trend over time, segmentation
    showing variance, and interpretation explaining what it means. Answer
    "so what?" in every report
    

---
  #### **Name**
Correlation Causation Confusion
  #### **Description**
Seeing correlation in data and assuming one thing caused the other
  #### **Why**
    "Power users have more friends, so we should force everyone to invite friends"
    Maybe power users invite friends because they get value, not the reverse
    
  #### **Instead**
    Use experimentation to establish causation. Correlations generate hypotheses,
    experiments validate them. Be explicit: "We see correlation, testing causation"
    

---
  #### **Name**
Data Quality Neglect
  #### **Description**
Analyzing dirty data without validating accuracy first
  #### **Why**
    Garbage in, garbage out. Wrong decisions from bad data are worse than no data.
    "Data-driven" becomes excuse for shipping bad features based on bad tracking
    
  #### **Instead**
    Validate tracking before trusting it. Check: Are events firing? Are properties
    populated? Do funnels make sense? Set up automated data quality alerts
    