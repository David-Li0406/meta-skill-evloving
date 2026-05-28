# Go-to-Market Strategy

## Patterns


---
  #### **Name**
GTM Motion Selection
  #### **Description**
Choosing the right go-to-market motion for your situation
  #### **When**
Starting GTM planning or changing motions
  #### **Example**
    # GTM MOTION SELECTION:
    
    ## Product-Led Growth (PLG)
    """
    DEFINITION: Product is the primary driver of acquisition, conversion,
    and expansion. Users experience value before talking to anyone.
    
    CHARACTERISTICS:
    - Self-serve signup and onboarding
    - Free tier or trial as entry point
    - In-product upsells
    - Usage-based or seat-based pricing
    - Viral or word-of-mouth spread
    
    WHEN IT WORKS:
    - Simple product with fast time-to-value
    - Low price point (<$50/month at entry)
    - End users are buyers (or strong influence)
    - Product can demonstrate value quickly
    - Wide market with many potential users
    
    WHEN IT DOESN'T:
    - Complex products requiring implementation
    - Long sales cycles (6+ months)
    - Enterprise buyers who need relationships
    - High price points requiring justification
    - Small market where you know every customer
    
    EXAMPLES: Slack, Figma, Notion, Calendly, Loom
    
    METRICS:
    - Activation rate (key milestone completion)
    - Free-to-paid conversion
    - Expansion revenue (seat adds, upgrades)
    - Viral coefficient (invites per user)
    """
    
    ## Sales-Led Growth (SLG)
    """
    DEFINITION: Human salespeople drive customer acquisition.
    Product supports sales process but doesn't replace it.
    
    CHARACTERISTICS:
    - Demo requests instead of self-serve
    - Sales development (SDR → AE flow)
    - Negotiated pricing and contracts
    - Implementation and success teams
    - Relationship-driven expansion
    
    WHEN IT WORKS:
    - Complex products requiring explanation
    - High price points (>$10K/year)
    - Enterprise buyers with procurement
    - Long implementation or migration
    - Technical or security requirements
    
    WHEN IT DOESN'T:
    - Low price points (unit economics won't work)
    - Simple products (sales is friction)
    - End-user adoption without IT approval
    - Markets too fragmented for direct sales
    - Founders who can't sell
    
    EXAMPLES: Salesforce, Workday, Snowflake, Databricks
    
    METRICS:
    - SQL to opportunity conversion
    - Win rate
    - Average contract value (ACV)
    - Sales cycle length
    - CAC payback period
    """
    
    ## Community-Led Growth
    """
    DEFINITION: Community is the engine for awareness, trust, and
    adoption. Product serves community needs.
    
    CHARACTERISTICS:
    - Community before product (often)
    - User-generated content and help
    - Events, forums, or social presence
    - Strong brand and cultural identity
    - Members recruiting members
    
    WHEN IT WORKS:
    - Developer tools (natural communities)
    - Hobby/passion categories
    - Professional identity categories
    - Open source with commercial layer
    - Products solving community problems
    
    WHEN IT DOESN'T:
    - B2B without natural community
    - Transactional products
    - Products people don't talk about
    - Time-sensitive purchase decisions
    - No founder community DNA
    
    EXAMPLES: Figma, Notion, dbt, Hashicorp, Substack
    
    METRICS:
    - Community size and engagement
    - Content/discussion volume
    - Member-generated support
    - Event attendance
    - Community-attributed pipeline
    """
    
    ## Choosing Your Motion
    """
    ASK THESE QUESTIONS:
    
    1. What's your price point?
       - <$50/mo: PLG likely optimal
       - $50-500/mo: Could be either
       - >$500/mo: Likely needs sales touch
    
    2. What's time-to-value?
       - Minutes: PLG
       - Days: PLG with sales assist
       - Weeks/months: Sales-led
    
    3. Who's the buyer?
       - End user: PLG
       - Manager: Either
       - Executive/IT: Sales-led
    
    4. What's founder DNA?
       - Product/engineering: PLG
       - Sales/BD background: Sales-led
       - Community builder: Community-led
    
    5. What's the market?
       - Horizontal (many buyers): PLG scales better
       - Vertical (fewer buyers): Sales-led works
       - Tribal (identity-based): Community-led
    """
    

---
  #### **Name**
Channel Strategy
  #### **Description**
Selecting and prioritizing acquisition channels
  #### **When**
Planning customer acquisition
  #### **Example**
    # CHANNEL STRATEGY:
    
    ## The Channel Portfolio
    """
    OWNED CHANNELS (you control):
    - Website and SEO
    - Email/newsletter
    - Product (viral, referral)
    - Community (Discord, Slack)
    - Content (blog, YouTube)
    
    EARNED CHANNELS (you influence):
    - Word of mouth
    - Press/media coverage
    - Influencer mentions
    - Social sharing
    - App store discovery
    
    PAID CHANNELS (you buy):
    - Search ads (Google, Bing)
    - Social ads (FB, LinkedIn, Twitter)
    - Display/retargeting
    - Sponsorships
    - Affiliate/referral programs
    """
    
    ## Channel Selection Framework
    """
    SCORE EACH CHANNEL (1-5):
    
    1. TARGETING
       Can you reach your specific customer?
       - LinkedIn: Great for B2B job titles
       - Instagram: Great for consumer demographics
       - SEO: Great for intent-based targeting
    
    2. COST
       What's the CAC through this channel?
       - Consider both $ and time investment
       - Early stage: time is often cheaper
       - Scale: $ efficiency matters more
    
    3. CONTROL
       How much can you optimize and test?
       - Paid: High control, fast iteration
       - PR: Low control, unpredictable
       - SEO: Medium control, slow feedback
    
    4. SCALABILITY
       Can this channel grow with you?
       - Content: Compounds but slow
       - Paid: Scales but costs increase
       - Referral: Scales if K>1
    
    5. FIT
       Does this channel match your product?
       - Developer tools: GitHub, Hacker News
       - B2B SaaS: LinkedIn, industry content
       - Consumer: TikTok, Instagram, influencers
    """
    
    ## Channel Sequencing
    """
    STAGE 1 - VALIDATION (0-100 customers):
    - Manual outreach (founder sales)
    - Personal networks
    - Warm intros
    - Community participation
    - PURPOSE: Learn, don't scale
    
    STAGE 2 - EARLY TRACTION (100-1000):
    - Double down on what worked
    - One or two channels max
    - Content as multiplier
    - Referral program seed
    - PURPOSE: Find repeatable channel
    
    STAGE 3 - GROWTH (1000+):
    - Add second channel
    - Invest in content/SEO (compounding)
    - Paid experimentation
    - Channel-specific hires
    - PURPOSE: Diversify and scale
    
    RULE: Master one channel before adding another.
    Most startups spread too thin too early.
    """
    
    ## Channel Exhaustion
    """
    Every channel has a ceiling:
    - Early adopter networks: Small but efficient
    - Paid: Costs increase with scale
    - Organic social: Algorithm changes
    - PR: Diminishing novelty
    
    SIGNS OF EXHAUSTION:
    - CAC increasing despite optimization
    - Conversion rates declining
    - Audience fatigue (lower engagement)
    - Competitor saturation
    
    RESPONSE:
    - Plan for it, don't be surprised
    - Start next channel before exhaustion
    - Focus on owned channels that compound
    """
    

---
  #### **Name**
Launch Sequencing
  #### **Description**
How to sequence a product launch for maximum impact
  #### **When**
Planning a launch
  #### **Example**
    # LAUNCH SEQUENCING:
    
    ## Launch Types
    """
    1. STEALTH LAUNCH
       - No announcement
       - Direct outreach to early users
       - Learn before you're visible
       - Good for: Unproven ideas, competitive markets
    
    2. SOFT LAUNCH
       - Limited audience
       - Waitlist or invite-only
       - Build social proof before scale
       - Good for: Building anticipation, finding bugs
    
    3. BIG BANG LAUNCH
       - Coordinated announcement
       - Press, Product Hunt, social
       - Maximum initial visibility
       - Good for: Crowded markets, newsworthy products
    
    4. ROLLING LAUNCH
       - Gradual expansion
       - Geographic or segment rollout
       - Learn and iterate between waves
       - Good for: Operational complexity, marketplace
    """
    
    ## Pre-Launch Checklist
    """
    4 WEEKS OUT:
    - [ ] Core product ready (not perfect)
    - [ ] Pricing and packaging decided
    - [ ] Landing page and positioning
    - [ ] Analytics and tracking setup
    - [ ] Support process defined
    
    2 WEEKS OUT:
    - [ ] Early users seeded
    - [ ] Testimonials/case studies ready
    - [ ] Press/influencer relationships warm
    - [ ] Launch assets created
    - [ ] Team roles assigned
    
    1 WEEK OUT:
    - [ ] Product Hunt scheduled
    - [ ] Press embargoes set
    - [ ] Social content scheduled
    - [ ] Email sequences ready
    - [ ] War room planned
    
    LAUNCH DAY:
    - [ ] All hands on deck
    - [ ] Monitor and respond in real-time
    - [ ] Fix critical bugs immediately
    - [ ] Engage with every user
    """
    
    ## Product Hunt Strategy
    """
    PRE-HUNT:
    - Build hunter relationship 2+ weeks early
    - Collect upvotes commitments
    - Prepare all assets (GIFs, video)
    - Write compelling tagline (<60 chars)
    - Draft comment responses
    
    LAUNCH DAY:
    - Launch at 12:01 AM PT
    - First comment with context immediately
    - Respond to every comment within 1 hour
    - Share across social (but don't beg for votes)
    - Update team hourly on status
    
    POST-HUNT:
    - Download all leads
    - Personal outreach to engaged users
    - Write retrospective
    - Follow up with hunters
    
    WHAT ACTUALLY MATTERS:
    - Engagement > upvotes
    - Comments show interest
    - Top 5 gets featured
    - Featured gets long-tail traffic
    - But direct conversions are low
    """
    
    ## Post-Launch Reality
    """
    COMMON PATTERN:
    Day 1: Spike (launch hype)
    Day 2-7: Drop (no more novelty)
    Week 2+: Steady state (reality)
    
    THE SPIKE IS NOT THE BUSINESS.
    What matters is the steady state.
    
    POST-LAUNCH PRIORITIES:
    1. Activate launched users (most will churn)
    2. Identify which segment retained
    3. Double down on that segment
    4. Build repeatable acquisition
    
    Launch is chapter 1, not the whole book.
    """
    

---
  #### **Name**
First 100 Customers
  #### **Description**
Tactical playbook for getting early customers
  #### **When**
Pre-product-market fit acquisition
  #### **Example**
    # FIRST 100 CUSTOMERS:
    
    ## Why First 100 Are Different
    """
    First 100 customers are NOT scale customers.
    
    They are:
    - More tolerant of bugs
    - More accessible for feedback
    - More likely to be early adopters
    - Willing to take a chance
    
    They are also:
    - NOT representative of the market
    - Often have different needs
    - Sometimes too nice (won't churn)
    - May want custom things
    
    USE THEM TO LEARN, not to prove scale.
    """
    
    ## Tactical Playbook
    """
    TIER 1: Your Network (Customers 1-10)
    - Friends who have the problem
    - Former colleagues
    - LinkedIn first-degree connections
    - Warm intros from investors/advisors
    
    Approach: "I'm building X. You're exactly who I built it for.
    Can I give you early access and get your feedback?"
    
    TIER 2: Extended Network (11-30)
    - Second-degree connections
    - Twitter/LinkedIn cold outreach
    - Industry communities you're in
    - Founder networks
    
    Approach: Personalized outreach referencing their specific
    situation. No automation at this stage.
    
    TIER 3: Community Engagement (31-50)
    - Subreddits for your audience
    - Slack/Discord communities
    - Industry forums
    - Indie Hackers, HN, Twitter
    
    Approach: Genuine participation first, then mention product
    when genuinely relevant. Never spam.
    
    TIER 4: Content and Inbound (51-100)
    - Blog posts about the problem
    - Twitter presence building
    - SEO for pain-point queries
    - Podcast/newsletter appearances
    
    Approach: Be helpful publicly. Product becomes natural next step.
    """
    
    ## What "Selling" Looks Like at This Stage
    """
    DON'T:
    - Automate outreach
    - Send cold templates
    - Focus on efficiency
    - Worry about "scale"
    
    DO:
    - Personal emails to specific people
    - Listen more than pitch
    - Ask about their problems
    - Let them shape the product
    - Do things that don't scale
    
    SCRIPT:
    "Hey [Name], I noticed you're [specific thing].
    
    I'm building [product] to solve [problem]. Based on
    [their specific situation], you might find it useful.
    
    Happy to give you early access - no strings attached.
    Would love 15 min to learn about your workflow.
    
    [Your name]"
    """
    
    ## Knowing When to Stop
    """
    FIRST 100 IS NOT:
    - Validation of scalable GTM
    - Proof of product-market fit
    - Representative of real CAC
    
    SIGNALS TO TRANSITION:
    - Retention is strong (>20% weekly active)
    - Users asking for features (not leaving)
    - Word of mouth starting
    - You're repeating yourself in sales
    
    Then: Document what works, build playbook, start hiring.
    """
    

---
  #### **Name**
GTM Motion Transitions
  #### **Description**
When and how to add or switch GTM motions
  #### **When**
Scaling or pivoting GTM approach
  #### **Example**
    # GTM MOTION TRANSITIONS:
    
    ## Common Transitions
    """
    PLG → PLG + SALES (Product-Led Sales)
    - Most common transition at scale
    - Add sales to capture enterprise
    - Sales serves product-qualified leads (PQLs)
    - Product remains primary driver
    
    SALES → SALES + PLG
    - Add self-serve for smaller customers
    - Reduce CAC on long tail
    - Free tier as lead gen for sales
    - Complex - often fails
    
    COMMUNITY → PLG
    - Community validates need
    - Product serves community
    - Launch to built-in audience
    - Maintain community as moat
    
    SINGLE MOTION → HYBRID
    - Only after first motion proven
    - Second motion serves different segment
    - Clear handoff rules required
    - Organization complexity increases
    """
    
    ## Product-Led Sales (PLS) Deep Dive
    """
    WHAT IT IS:
    Sales team that serves product-qualified leads.
    Not cold calling - following up on usage signals.
    
    WHEN TO ADD:
    - Strong PLG foundation
    - Enterprise demand from PLG users
    - Need to capture larger deals
    - Usage patterns indicate upsell opportunity
    
    HOW IT WORKS:
    1. Free/self-serve captures wide top-of-funnel
    2. Product usage generates PQLs:
       - Hitting usage limits
       - Team size growing
       - Enterprise features requested
       - High engagement patterns
    3. Sales reaches out at right moment
    4. Sales accelerates, doesn't replace
    
    PQL DEFINITION:
    - Company: 10+ active users
    - Usage: Using 3+ core features
    - Behavior: Hitting usage limits
    - Fit: ICP company characteristics
    
    COMMON MISTAKES:
    - Adding sales too early (before PLG works)
    - Sales hijacking product roadmap
    - Eliminating self-serve for enterprise
    - Confusing PQL with MQL
    """
    
    ## Transition Challenges
    """
    1. ORGANIZATIONAL CONFLICT
       - Sales wants features for deals
       - Product wants features for users
       - Marketing caught in middle
       - Compensation misalignment
    
       FIX: Clear segment ownership and metrics
    
    2. CUSTOMER CONFUSION
       - "Do I self-serve or talk to sales?"
       - Different experiences for same product
       - Pricing inconsistency
    
       FIX: Clear paths based on need/size
    
    3. METRICS CHAOS
       - What's a "customer"?
       - Attribution wars
       - Conflicting goals
    
       FIX: Unified customer definition, shared goals
    
    4. CULTURE CLASH
       - PLG culture: product-obsessed
       - Sales culture: revenue-obsessed
       - Community: mission-obsessed
    
       FIX: Hire bridges, explicit values, patience
    """
    
    ## When NOT to Transition
    """
    DON'T ADD SALES IF:
    - PLG isn't working yet
    - You're doing it because it's hard
    - Investors are pushing it
    - Just to hit revenue faster
    
    DON'T ADD PLG IF:
    - Product genuinely needs sales
    - Self-serve would hurt value perception
    - It would require different product
    - Market doesn't want self-serve
    
    RULE: First motion must work before adding second.
    """
    

## Anti-Patterns


---
  #### **Name**
Build It and They Will Come
  #### **Description**
Assuming a great product doesn't need distribution
  #### **Why**
    Distribution is half the equation. The world is full of great products
    nobody uses. A mediocre product with great distribution beats a great
    product with no distribution. You need both.
    
  #### **Instead**
Plan distribution from day one. Who are first 100 customers and how do you reach them?

---
  #### **Name**
Premature Scaling
  #### **Description**
Investing in channels before product-market fit
  #### **Why**
    Paid acquisition, sales hires, and channel investments only work when
    the product is ready. Scaling acquisition for a product that doesn't
    retain is lighting money on fire.
    
  #### **Instead**
First 100 customers manually. Then prove retention. Then scale acquisition.

---
  #### **Name**
Channel Sprawl
  #### **Description**
Trying to be everywhere at once
  #### **Why**
    Every channel requires investment to work. Spreading across many channels
    means none work well. You end up with mediocre presence everywhere instead
    of dominant position somewhere.
    
  #### **Instead**
Master one channel before adding another. Go deep, then wide.

---
  #### **Name**
Copy Competitor GTM
  #### **Description**
Assuming their motion works for you
  #### **Why**
    Competitors have different products, teams, funding, and timing. Their
    motion worked for their situation. Your situation is different. What
    looks like their GTM is probably different under the hood.
    
  #### **Instead**
Start from your product, customers, and team. Design motion for your situation.

---
  #### **Name**
Sales Before Self-Serve Proof
  #### **Description**
Hiring sales because self-serve is hard
  #### **Why**
    If self-serve isn't working, adding sales probably won't fix it. Sales
    adds friction. If the product doesn't sell itself to some users, sales
    will struggle too. Sales fixes scale, not product.
    
  #### **Instead**
Fix the product first. Get some users to convert self-serve. Then add sales.

---
  #### **Name**
Launch-as-Strategy
  #### **Description**
Treating the launch as the whole GTM strategy
  #### **Why**
    Launch gets attention for a moment. Then you need sustainable acquisition.
    Many founders over-invest in launch and under-invest in the 364 other days.
    The spike is not the business.
    
  #### **Instead**
Launch is one day. Build repeatable channels. Steady state matters more than spike.

---
  #### **Name**
Paid-First Mentality
  #### **Description**
Starting with paid acquisition before organic proof
  #### **Why**
    Paid acquisition only works when the product already converts. Starting
    with paid means you're paying to learn if the product works. That's
    expensive learning. Organic proves the product, paid scales it.
    
  #### **Instead**
Prove conversion with organic/manual first. Use paid to scale what already works.