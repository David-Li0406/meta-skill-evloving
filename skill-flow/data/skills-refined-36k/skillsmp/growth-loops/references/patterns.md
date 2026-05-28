# Growth Loops

## Patterns


---
  #### **Name**
Viral Loop Architecture
  #### **Description**
User actions that bring in new users
  #### **When To Use**
Products with inherent shareability
  #### **Implementation**
    ## Viral Loop Components
    
    ### 1. The Basic Viral Loop
    ```
    New User → Uses Product → Shares/Invites → New User
       ↑                                           |
       └───────────────────────────────────────────┘
    ```
    
    ### 2. Key Metrics
    - **K-factor** = Invites sent × Conversion rate
      - K > 1 = Exponential growth
      - K < 1 = Needs other acquisition
    - **Cycle time** = Time from signup to invite
      - Shorter = Faster compounding
    
    ### 3. Viral Loop Types
    
    **Word-of-Mouth (WOM)**
    - Trigger: Product is so good users tell others
    - Example: "You have to try this"
    - Optimization: Remarkable moments, easy to describe
    
    **Incentivized Referral**
    - Trigger: Reward for referring
    - Example: "Give $20, Get $20"
    - Optimization: Two-sided rewards, milestone bonuses
    
    **Inherent Virality**
    - Trigger: Using product requires sharing
    - Example: Calendly (recipient sees tool)
    - Optimization: Make shared artifact valuable
    
    **Social Proof**
    - Trigger: Public usage signals value
    - Example: "Made with Notion" badges
    - Optimization: Visible in user's network
    
    ### 4. Optimization Levers
    
    | Stage | Metric | Optimization |
    |-------|--------|--------------|
    | Trigger | % who reach share moment | Faster time-to-value |
    | Share | % who actually share | Reduce friction, add incentive |
    | Click | % of recipients who click | Compelling preview/message |
    | Convert | % who sign up | Landing page, social proof |
    
    ### 5. Viral Loop Formula
    ```
    Growth = Initial Users × K^(t/cycle_time)
    
    Example:
    - 1000 users, K=0.8, 7-day cycle
    - After 30 days: 1000 × 0.8^(30/7) = ~1000 × 0.8^4.3 = ~380 new users
    
    - Same K=0.8, but 2-day cycle
    - After 30 days: 1000 × 0.8^(30/2) = ~1000 × 0.8^15 = ~35 new users
    ```
    
    Wait, that math shows shorter cycles with K<1 decay faster!
    
    Corrected understanding:
    - K<1: Loop decays (need other acquisition)
    - K>1: Loop grows (shorter cycle = faster growth)
    - K=1: Sustains (each user replaces themselves)
    

---
  #### **Name**
Content Loop Design
  #### **Description**
Content that attracts users who create more content
  #### **When To Use**
UGC platforms, SEO-driven products
  #### **Implementation**
    ## Content Loop Mechanics
    
    ### 1. The Content Flywheel
    ```
    User Creates Content → Content Indexed/Shared
           ↑                        |
           |                        ↓
    User Signs Up ← New Visitor Discovers Content
    ```
    
    ### 2. Content Loop Types
    
    **SEO Content Loop**
    - User creates content (reviews, posts, questions)
    - Google indexes content
    - Searchers find and click
    - Some convert to creators
    - Example: Reddit, Quora, G2
    
    **Social Content Loop**
    - User creates content
    - Content shared on social
    - Viewers click through
    - Some become creators
    - Example: TikTok, Twitter, Pinterest
    
    **Embedded Content Loop**
    - User creates embeddable content
    - Embedded on external sites
    - Viewers see "Made with X"
    - Click through and create
    - Example: Typeform, Canva, Loom
    
    ### 3. Key Metrics
    
    | Metric | Definition | Target |
    |--------|------------|--------|
    | Content Velocity | New content/day | Growing |
    | Index Rate | % indexed by search | >80% |
    | CTR | Click-through rate | >2% |
    | Creator Conversion | % visitors who create | >1% |
    
    ### 4. Optimization Strategies
    
    **Increase Creation**
    - Lower barrier to create (templates, AI assist)
    - Incentivize creation (badges, visibility)
    - Make creation part of core job-to-be-done
    
    **Improve Distribution**
    - SEO: Schema markup, internal linking
    - Social: Native sharing, preview optimization
    - Embed: Beautiful embeds, clear attribution
    
    **Boost Conversion**
    - Show creation value proposition on landing
    - Reduce signup friction
    - Offer templates from discovered content
    

---
  #### **Name**
Paid Loop Optimization
  #### **Description**
Revenue funds acquisition that generates more revenue
  #### **When To Use**
When unit economics work
  #### **Implementation**
    ## Paid Acquisition Loop
    
    ### 1. The Paid Loop
    ```
    Revenue → Fund Ads → Acquire Users → Revenue
       ↑                                    |
       └────────────────────────────────────┘
    ```
    
    ### 2. When Paid Loops Work
    - LTV > 3× CAC (healthy margin)
    - Payback period < 12 months
    - Scalable channels exist
    - Creative refresh is sustainable
    
    ### 3. Key Metrics
    
    | Metric | Formula | Healthy |
    |--------|---------|---------|
    | CAC | Total spend / Customers | < LTV/3 |
    | LTV | ARPU × Lifespan | > 3× CAC |
    | Payback | CAC / Monthly Revenue | < 12 mo |
    | ROAS | Revenue / Ad Spend | > 3× |
    
    ### 4. Paid Loop Layers
    
    **Blended Paid Loop**
    - Paid brings awareness
    - Organic/viral converts portion
    - Measure blended CAC vs paid CAC
    
    **Retargeting Layer**
    - Paid brings visitors
    - Retargeting converts
    - Often 10× more efficient
    
    **Lookalike Expansion**
    - Convert customers
    - Build lookalike audiences
    - Expand to similar users
    
    ### 5. Reinvestment Strategy
    ```
    Month 1: $10K spend → $30K LTV (eventual)
    Month 2: Reinvest $10K from Month 1 payback
    Month 3: Compound continues
    
    Key: Speed of payback = Speed of compounding
    ```
    

---
  #### **Name**
Product Loop Integration
  #### **Description**
Product usage drives more usage
  #### **When To Use**
Products with network or data effects
  #### **Implementation**
    ## Product-Driven Loops
    
    ### 1. Network Effect Loop
    ```
    User Joins → Product More Valuable → Attracts More Users
         ↑                                        |
         └────────────────────────────────────────┘
    ```
    
    Examples:
    - Slack: More teammates = more valuable
    - Figma: More collaborators = more valuable
    - LinkedIn: More connections = more valuable
    
    ### 2. Data Loop
    ```
    User Uses Product → Data Improves Product → Better Experience
           ↑                                           |
           └─────────────────── User Returns ──────────┘
    ```
    
    Examples:
    - Spotify: Usage improves recommendations
    - Waze: Usage improves maps
    - Grammarly: Usage improves suggestions
    
    ### 3. Habit Loop
    ```
    Trigger → Action → Variable Reward → Investment
       ↑                                      |
       └───────── Increased Trigger ──────────┘
    ```
    
    Examples:
    - Twitter: Notification → Check → New content → Follow more
    - Duolingo: Reminder → Lesson → Streak → Come back
    
    ### 4. Platform Loop
    ```
    Users → Attract Developers → More Features → More Users
      ↑                                              |
      └──────────────────────────────────────────────┘
    ```
    
    Examples:
    - Shopify: Merchants attract app developers
    - Salesforce: Users attract ecosystem
    - Slack: Teams attract integration builders
    

---
  #### **Name**
Loop Measurement Framework
  #### **Description**
How to track and optimize loops
  #### **When To Use**
Any loop-based growth
  #### **Implementation**
    ## Loop Metrics System
    
    ### 1. Loop Health Dashboard
    
    | Metric | What It Measures | How to Calculate |
    |--------|------------------|------------------|
    | Loop Velocity | Speed of one cycle | Avg days trigger → conversion |
    | Loop Efficiency | Conversion through loop | End/Start of cycle |
    | Loop Contribution | % growth from loop | Loop-attributed / Total |
    | Loop Trend | Is loop strengthening? | Week-over-week efficiency |
    
    ### 2. Attribution Model
    
    **First-Touch Loop Attribution**
    - Credit loop that first acquired user
    - Good for: Understanding acquisition mix
    
    **Last-Touch Loop Attribution**
    - Credit loop that converted user
    - Good for: Optimizing conversion
    
    **Multi-Touch Loop Attribution**
    - Fractional credit across loops
    - Good for: Understanding full journey
    
    ### 3. Loop Experiments
    
    **A/B Test Framework**
    1. Identify loop stage to test
    2. Hypothesis: "If we X, then Y increases by Z%"
    3. Calculate sample size for significance
    4. Run test for full loop cycle (minimum)
    5. Measure downstream effects
    
    **Loop Bottleneck Analysis**
    1. Map all loop stages
    2. Measure conversion at each stage
    3. Identify biggest drop-offs
    4. Prioritize by: Drop-off × Volume × Ease
    
    ### 4. Loop Reporting Cadence
    
    | Timeframe | Focus |
    |-----------|-------|
    | Daily | Anomaly detection |
    | Weekly | Stage conversion rates |
    | Monthly | Loop efficiency trends |
    | Quarterly | Loop portfolio review |
    

## Anti-Patterns


---
  #### **Name**
Loop Theater
  #### **Description**
Calling any growth tactic a "loop"
  #### **Why Bad**
    Not everything is a loop.
    Misidentifying loops wastes resources.
    One-time tactics don't compound.
    
  #### **What To Do Instead**
    True loops have: Input → Process → Output → Feeds Input
    If output doesn't feed input, it's not a loop.
    Test: "Does success in this create more success?"
    

---
  #### **Name**
K-Factor Obsession
  #### **Description**
Optimizing only for viral coefficient
  #### **Why Bad**
    Ignores cycle time (often more important).
    Ignores quality of referred users.
    Can incentivize spammy behavior.
    
  #### **What To Do Instead**
    Optimize for: K-factor × (1/cycle time) × LTV of referred
    A slower loop with higher-quality users often wins.
    

---
  #### **Name**
Forced Virality
  #### **Description**
Adding share mechanics that don't fit product
  #### **Why Bad**
    Users resent forced sharing.
    Damages brand perception.
    Short-term gains, long-term losses.
    
  #### **What To Do Instead**
    Build loops into natural product usage.
    Ask: "Would sharing genuinely help this user?"
    Inherent > Incentivized > Forced
    

---
  #### **Name**
Loop Neglect
  #### **Description**
Building loop once and forgetting it
  #### **Why Bad**
    Loops decay over time.
    Channels get saturated.
    Competition copies mechanics.
    
  #### **What To Do Instead**
    Continuous loop optimization.
    Monitor loop health weekly.
    Refresh mechanics before decay.
    

---
  #### **Name**
Premature Loop Scaling
  #### **Description**
Investing heavily in loop before it works
  #### **Why Bad**
    Amplifies broken mechanics.
    Wastes resources.
    Harder to fix at scale.
    
  #### **What To Do Instead**
    Prove loop works at small scale first.
    Look for organic loop signals.
    Scale only when unit economics proven.
    