# Community Analytics

## Patterns


---
  #### **Name**
Community Health Score
  #### **Description**
Composite metric for overall community health
  #### **When To Use**
When establishing health monitoring
  #### **Implementation**
    ## Community Health Score (0-100)
    
    ### Components
    | Metric | Weight | What It Measures |
    |--------|--------|------------------|
    | Activity | 25% | DAU/MAU ratio |
    | Engagement | 25% | Depth of participation |
    | Retention | 25% | Members coming back |
    | Sentiment | 25% | How members feel |
    
    ### Scoring
    ```
    Activity Score (0-25):
    - < 10% DAU/MAU = 5
    - 10-20% = 10
    - 20-30% = 15
    - 30-40% = 20
    - > 40% = 25
    
    Engagement Score (0-25):
    - Based on posts per active member
    - Conversation depth (replies)
    - Contribution diversity
    
    Retention Score (0-25):
    - Week 1: 50%+ = 10
    - Month 1: 30%+ = 10
    - Month 3: 20%+ = 5
    
    Sentiment Score (0-25):
    - Survey/NPS based
    - Sentiment analysis of messages
    - Support ticket trends
    ```
    
    ### Interpretation
    | Score | Status | Action |
    |-------|--------|--------|
    | 80+ | Thriving | Maintain, scale |
    | 60-80 | Healthy | Optimize weak areas |
    | 40-60 | At risk | Intervention needed |
    | < 40 | Critical | Major changes required |
    

---
  #### **Name**
Engagement Metrics Framework
  #### **Description**
Comprehensive engagement measurement
  #### **When To Use**
When tracking member engagement
  #### **Implementation**
    ## Engagement Metrics
    
    ### Core Metrics
    | Metric | Definition | Target |
    |--------|------------|--------|
    | DAU | Unique active/day | Track trend |
    | WAU | Unique active/week | Track trend |
    | MAU | Unique active/month | Track trend |
    | DAU/MAU | Stickiness ratio | 20-40% |
    | Messages/DAU | Activity depth | 3-10 |
    
    ### Engagement Levels
    ```
    LURKER → REACTOR → COMMENTER → CONTRIBUTOR → CREATOR
    ```
    
    Track distribution across levels:
    - Lurkers: View only (target: < 60%)
    - Reactors: Likes/emoji (target: > 20%)
    - Commenters: Reply to others (target: > 10%)
    - Contributors: Start discussions (target: > 5%)
    - Creators: Create value content (target: > 2%)
    
    ### Engagement Quality
    - Thread depth (avg replies per post)
    - Cross-pollination (members in multiple channels)
    - Return conversations (member replied back)
    

---
  #### **Name**
Retention Analysis
  #### **Description**
Tracking member retention by cohort
  #### **When To Use**
When analyzing retention
  #### **Implementation**
    ## Cohort Retention Analysis
    
    ### Retention Table
    ```
    Cohort    | D1   | D7   | D14  | D30  | D60  | D90
    Jan W1    | 80%  | 50%  | 40%  | 30%  | 25%  | 20%
    Jan W2    | 75%  | 45%  | 35%  | 28%  | ...  | ...
    Jan W3    | 82%  | 52%  | 42%  | ...  | ...  | ...
    ```
    
    ### Benchmarks
    | Period | Good | Great | World Class |
    |--------|------|-------|-------------|
    | D1 | 60% | 75% | 85% |
    | D7 | 40% | 50% | 60% |
    | D30 | 25% | 35% | 45% |
    | D90 | 15% | 25% | 35% |
    
    ### Churn Analysis
    - When do members leave? (day X cliff)
    - Why do they leave? (exit surveys)
    - Who leaves? (segment analysis)
    - What predicts churn? (behavioral signals)
    

## Anti-Patterns


---
  #### **Name**
Vanity Dashboard
  #### **Description**
Tracking metrics that look good but don't matter
  #### **Why Bad**
    Big numbers feel good, hide problems.
    Wrong metrics drive wrong behavior.
    Miss actual issues.
    
  #### **What To Do Instead**
    Focus on outcomes over outputs.
    Track depth, not just breadth.
    Tie metrics to member value.
    

---
  #### **Name**
Data Without Action
  #### **Description**
Collecting data but not using it
  #### **Why Bad**
    Wasted effort collecting.
    False sense of being data-driven.
    Data grows stale and irrelevant.
    
  #### **What To Do Instead**
    Every metric should drive a decision.
    Regular data reviews with action items.
    Stop tracking what you don't use.
    