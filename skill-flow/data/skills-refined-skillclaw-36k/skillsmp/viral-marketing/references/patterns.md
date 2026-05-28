# Viral Marketing

## Patterns


---
  #### **Name**
The Viral Loop Formula
  #### **Description**
Calculate and optimize viral coefficient (k-factor) for sustainable growth
  #### **When**
Building or optimizing referral mechanics to achieve viral growth
  #### **Example**
    K = (invites sent per user) × (conversion rate of invites)
    
    Example:
    - Each user invites 5 people (i = 5)
    - 30% of invites sign up (c = 0.3)
    - K = 5 × 0.3 = 1.5
    
    K > 1 = viral growth (each user brings >1 new user)
    K < 1 = paid growth with referral assist
    
    Optimize both variables: make inviting easier, make invites more compelling.
    

---
  #### **Name**
Product-Inherent Virality
  #### **Description**
Build sharing directly into the product value proposition
  #### **When**
Designing products where network effects or collaboration are core value
  #### **Example**
    - Dropbox: File sharing requires inviting others
    - Figma: Real-time collaboration requires team invites
    - Zoom: Host creates value by inviting participants
    - Calendly: Sharing meeting link is the core action
    
    Best virality: Product doesn't work (or works worse) without sharing.
    

---
  #### **Name**
The Six Principles of Contagious Content
  #### **Description**
Framework from Jonah Berger's STEPPS model for shareable content
  #### **When**
Creating content designed to spread organically
  #### **Example**
    Social Currency: Makes sharer look good (insider knowledge, achievement)
    Triggers: Top of mind, easy to remember and recall
    Emotion: High-arousal emotions (awe, excitement, anger, anxiety)
    Public: Observable behavior that others can see and mimic
    Practical Value: Genuinely helpful information people want to share
    Stories: Wrapped in narrative that carries the message
    
    Example: Dollar Shave Club video hit all six.
    

---
  #### **Name**
Double-Sided Incentive Design
  #### **Description**
Reward both referrer and referee to maximize conversion and quality
  #### **When**
Designing referral program incentives
  #### **Example**
    Dropbox: Referrer gets +500MB, Referee gets +500MB (symmetric)
    Uber: Referrer gets $5 credit, Referee gets $20 off first ride (asymmetric)
    Airbnb: Both get travel credit (aligned incentives)
    
    Test incentive amounts. Too small = no motivation. Too large = fraud risk.
    Asymmetric often converts better (bigger reward for new user).
    

---
  #### **Name**
Friction Audit for Sharing
  #### **Description**
Systematically remove obstacles in the sharing flow
  #### **When**
Share feature exists but adoption is low
  #### **Example**
    Measure drop-off at each step:
    1. Click "Share" button: 100%
    2. Choose sharing method: 60% (40% drop)
    3. Customize message: 30% (50% drop)
    4. Send invite: 20% (33% drop)
    
    Fixes:
    - Pre-populate message (remove step 3)
    - One-click sharing to common channels
    - Progress indicator to reduce uncertainty
    - Social proof ("2,340 people shared this today")
    

---
  #### **Name**
Network Effects Moat Building
  #### **Description**
Design mechanics that make product more valuable as more people join
  #### **When**
Building products in competitive markets that need defensibility
  #### **Example**
    Direct network effects: Phone network (more users = more people to call)
    Two-sided marketplace: Uber (more drivers = faster pickups = more riders)
    Data network effects: Waze (more users = better traffic data)
    Platform effects: iOS (more users = more apps = more valuable)
    
    Virality gets people in. Network effects keep them in.
    

---
  #### **Name**
AI-Accelerated Viral Content Pipeline
  #### **Description**
Using AI to increase viral content velocity
  #### **When**
Creating content with viral potential at scale
  #### **Example**
    AI-ACCELERATED VIRAL PIPELINE:
    
    1. TREND DETECTION (AI + Human)
       - AI monitors: Exploding Topics, Google Trends
       - Human judgment: Which trends fit brand?
       - Speed matters: 24-48 hour window
    
    2. CONCEPT GENERATION (AI)
       - Generate 10+ concepts per trend
       - Use Claude: "Generate viral hook variations for [trend]"
       - Filter by brand fit and feasibility
    
    3. RAPID PRODUCTION (AI-assisted)
       For video:
       - Opus Clip for long → short repurposing
       - Vizard AI for auto-captioning
       - CapCut for quick edits
    
       For images:
       - Midjourney for concepts
       - Canva for branded templates
    
    4. A/B HOOK TESTING
       - Post 3-5 variations of same content
       - Different hooks, thumbnails, captions
       - Double down on winner within 2 hours
    
    5. ENGAGEMENT AMPLIFICATION
       - Respond to comments within first hour (critical)
       - Seed to micro-communities (Reddit, Discord)
       - Cross-post to all platforms simultaneously
    
    VIRAL VELOCITY FORMULA:
    Speed × Relevance × Platform Fit × Engagement = Viral Potential
    
    AI accelerates: Speed, Volume of variations
    Human provides: Relevance judgment, Authentic engagement
    

## Anti-Patterns


---
  #### **Name**
Referral Spam
  #### **Description**
Making it easy to spam contact lists with untargeted invites
  #### **Why**
Damages brand reputation and gets you blacklisted by email providers
  #### **Instead**
Selective invites with personalization. Quality over quantity. Rate limiting.

---
  #### **Name**
Incentive-Only Virality
  #### **Description**
Bribing people to share without making product worth sharing
  #### **Why**
Attracts wrong users who churn after collecting rewards
  #### **Instead**
Build product worth sharing first. Incentives amplify, they don't create.

---
  #### **Name**
Ignoring the Cold Start Problem
  #### **Description**
Building network effects without strategy for initial users
  #### **Why**
Network effect products are worthless until network exists
  #### **Instead**
Start with dense subnetwork (single university, city, niche). Expand after saturation.

---
  #### **Name**
Generic Share CTAs
  #### **Description**
Using vague prompts like "Share this" without specific motivation
  #### **Why**
People need a reason WHY they should share and WHO they should share with
  #### **Instead**
Use specific CTAs like "Share with your team" or "Send to a friend who needs this". Specific context converts better.

---
  #### **Name**
One-Way Value Extraction
  #### **Description**
Asking users to share for your benefit with no value to them or their network
  #### **Why**
People share when it makes them look good or helps their friends
  #### **Instead**
Frame sharing as helping others. Use friend-first messaging like "Give your friend $20 off" rather than "Get $5 when friend signs up"

---
  #### **Name**
Measuring Vanity Viral Metrics
  #### **Description**
Tracking shares and impressions without measuring actual conversion
  #### **Why**
Viral "reach" that doesn't convert to users is wasted distribution
  #### **Instead**
Track full funnel (shares → clicks → signups → active users → retained users)