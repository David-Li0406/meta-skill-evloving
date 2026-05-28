# Business Model Design

## Patterns


---
  #### **Name**
Business Model Canvas
  #### **Description**
Mapping the complete business model
  #### **When To Use**
Designing or analyzing business models
  #### **Implementation**
    ## Business Model Canvas
    
    ### 1. The Nine Building Blocks
    
    ```
    ┌──────────────────────────────────────────────────────────────────┐
    │ Key           │ Key           │ Value         │ Customer    │ Customer  │
    │ Partners      │ Activities    │ Propositions  │ Relationships│ Segments │
    │               │               │               │              │           │
    │ Who helps     │ What we       │ What value    │ How we      │ Who we    │
    │ us do this?   │ must do?      │ we deliver?   │ interact?   │ serve?    │
    ├───────────────┼───────────────┼───────────────┤              │           │
    │               │ Key           │               │ Channels     │           │
    │               │ Resources     │               │              │           │
    │               │               │               │ How we      │           │
    │               │ What we need? │               │ reach them? │           │
    ├───────────────┴───────────────┴───────────────┴──────────────┴───────────┤
    │ Cost Structure                    │ Revenue Streams                      │
    │                                   │                                      │
    │ What are the major costs?         │ How do we make money?                │
    └───────────────────────────────────┴──────────────────────────────────────┘
    ```
    
    ### 2. Value Proposition
    
    **The Value Proposition Canvas**
    ```
    Customer Profile:
    - Jobs to be done
    - Pains
    - Gains
    
    Value Map:
    - Products/Services
    - Pain relievers
    - Gain creators
    
    Fit = Value Map addresses Customer Profile
    ```
    
    ### 3. Customer Segments
    
    | Type | Description | Example |
    |------|-------------|---------|
    | Mass Market | Broad, undifferentiated | Consumer goods |
    | Niche | Specialized, specific | Enterprise security |
    | Segmented | Different needs in same market | SMB vs Enterprise |
    | Multi-sided | Distinct interdependent groups | Marketplace |
    
    ### 4. Revenue Streams
    
    | Type | Description | When |
    |------|-------------|------|
    | Subscription | Recurring access | Ongoing value delivery |
    | Transaction | Per-use or per-sale | Clear value per transaction |
    | Licensing | Rights to use | IP-based value |
    | Advertising | Attention monetization | Free user base |
    | Commission | % of transaction | Facilitating transactions |
    | Freemium | Free + Paid tiers | Network effects matter |
    
    ### 5. Cost Structure
    
    ```
    Fixed Costs: Don't change with volume
    - Salaries
    - Rent
    - Software licenses
    
    Variable Costs: Scale with volume
    - COGS
    - Transaction costs
    - Customer support
    
    Business Model Impact:
    - High fixed, low variable = scale economics
    - Low fixed, high variable = flexibility
    ```
    

---
  #### **Name**
Revenue Model Selection
  #### **Description**
Choosing how to monetize
  #### **When To Use**
Designing monetization approach
  #### **Implementation**
    ## Revenue Model Guide
    
    ### 1. Revenue Model Types
    
    | Model | Mechanism | Best For |
    |-------|-----------|----------|
    | SaaS/Subscription | Recurring fee | Ongoing value, predictable |
    | Transactional | Per transaction | Variable usage |
    | Marketplace/Commission | % of GMV | Connecting buyers/sellers |
    | Usage-Based | Pay-per-use | Metered value |
    | Licensing | One-time fee + maintenance | Software, IP |
    | Advertising | CPM/CPC | Attention/audience |
    | Freemium | Free + Premium | Network effects |
    | Hardware + Subscription | Device + Recurring | IoT, hardware products |
    
    ### 2. Selection Criteria
    
    | Factor | Consideration |
    |--------|---------------|
    | Value timing | When is value delivered? |
    | Customer preference | How do they want to buy? |
    | Competition | What's the market norm? |
    | Cash flow | What do you need? |
    | Scalability | Does it scale? |
    | Stickiness | Does it create retention? |
    
    ### 3. Hybrid Models
    
    ```
    Examples:
    - SaaS + Usage-based: Base fee + overages
    - Freemium + Premium: Free tier + paid
    - Product + Services: Core + implementation
    - Hardware + Subscription: Razor/razorblade
    ```
    
    ### 4. Revenue Model Fit
    
    | Product Type | Typical Model |
    |--------------|---------------|
    | Business software | SaaS subscription |
    | Developer tools | Free tier + paid |
    | Marketplaces | Commission |
    | Consumer apps | Freemium or Ads |
    | Enterprise | License or SaaS |
    | Infrastructure | Usage-based |
    
    ### 5. Model Evolution
    
    ```
    Early stage: Simple model
    Growth stage: Add upsell paths
    Scale stage: Multiple revenue streams
    
    Example:
    v1: Single subscription tier
    v2: Multiple tiers (starter, pro, enterprise)
    v3: Platform/marketplace (services, apps)
    ```
    

---
  #### **Name**
Unit Economics Design
  #### **Description**
Understanding the economics of one customer
  #### **When To Use**
Validating business model viability
  #### **Implementation**
    ## Unit Economics Framework
    
    ### 1. Core Metrics
    
    ```
    LTV (Lifetime Value)
    = ARPU × Gross Margin × Customer Lifespan
    = ARPU × Gross Margin / Churn Rate
    
    CAC (Customer Acquisition Cost)
    = Total Sales & Marketing / New Customers
    
    LTV:CAC Ratio
    = LTV / CAC
    Target: > 3:1
    
    Payback Period
    = CAC / (ARPU × Gross Margin)
    Target: < 12 months
    ```
    
    ### 2. Metric Benchmarks
    
    | Metric | Healthy | Concerning |
    |--------|---------|------------|
    | LTV:CAC | > 3:1 | < 2:1 |
    | Payback | < 12 mo | > 18 mo |
    | Gross Margin | > 70% | < 50% |
    | Net Revenue Retention | > 100% | < 90% |
    | Churn (Monthly) | < 2% | > 5% |
    
    ### 3. Unit Economics by Model
    
    **SaaS**
    ```
    ARPU = Monthly subscription
    Gross Margin = ~80-90%
    Churn = Monthly logo churn
    CAC = Sales + Marketing / New logos
    ```
    
    **Marketplace**
    ```
    ARPU = Take rate × GMV per user
    Gross Margin = ~60-80%
    Churn = Seller and buyer churn
    CAC = Cost to acquire both sides
    ```
    
    **E-commerce**
    ```
    ARPU = AOV × Purchase frequency
    Gross Margin = ~30-50%
    Churn = Time between purchases
    CAC = Marketing / New customers
    ```
    
    ### 4. Improving Unit Economics
    
    | Lever | Actions |
    |-------|---------|
    | Increase LTV | Reduce churn, increase ARPU |
    | Reduce CAC | Better targeting, lower cost channels |
    | Improve Margins | Reduce COGS, increase prices |
    | Reduce Payback | Faster activation, upfront payment |
    
    ### 5. Cohort Analysis
    
    ```
    Track unit economics by cohort:
    - Acquisition cohort
    - Channel cohort
    - Segment cohort
    - Pricing cohort
    
    Find best-performing cohorts, focus there.
    ```
    

---
  #### **Name**
Business Model Innovation
  #### **Description**
Creating new business model approaches
  #### **When To Use**
Differentiating or disrupting
  #### **Implementation**
    ## Business Model Innovation
    
    ### 1. Innovation Types
    
    | Type | Description | Example |
    |------|-------------|---------|
    | Revenue model | New way to monetize | Subscription instead of purchase |
    | Value chain | New way to deliver | Direct-to-consumer |
    | Target segment | New customer | Prosumer instead of enterprise |
    | Value proposition | New benefit | Convenience instead of price |
    | Cost structure | New economics | Asset-light vs ownership |
    
    ### 2. Innovation Patterns
    
    **Unbundling**
    - Break apart integrated offering
    - Let customers buy pieces
    - Example: ESPN+ from cable bundle
    
    **Bundling**
    - Combine separate offerings
    - Create integrated solution
    - Example: Microsoft 365
    
    **Platform Shift**
    - From product to platform
    - Others build on you
    - Example: Salesforce AppExchange
    
    **Subscription Shift**
    - From purchase to subscription
    - Recurring relationship
    - Example: Adobe Creative Cloud
    
    **Asset Light**
    - Don't own the assets
    - Orchestrate others' assets
    - Example: Airbnb, Uber
    
    ### 3. When to Innovate
    
    | Situation | Consider |
    |-----------|----------|
    | Market expects model | Copy proven model |
    | Model is competitive advantage | Innovate |
    | Existing models failing | Must innovate |
    | Technology enables new model | Innovate early |
    
    ### 4. Innovation Risk
    
    ```
    Business model innovation carries risk:
    - Customers don't understand
    - Hard to compare
    - Requires education
    
    Mitigate:
    - Test with early adopters
    - Offer transition paths
    - Build proof points
    ```
    

## Anti-Patterns


---
  #### **Name**
Revenue Before Value
  #### **Description**
Monetizing before delivering value
  #### **Why Bad**
    No one pays for unrealized value.
    Damages trust.
    Limits growth potential.
    
  #### **What To Do Instead**
    Prove value first.
    Monetization follows value.
    Free can be strategic.
    

---
  #### **Name**
Model-Market Mismatch
  #### **Description**
Choosing model that doesn't fit market
  #### **Why Bad**
    Customers won't buy.
    Sales cycles lengthen.
    Friction everywhere.
    
  #### **What To Do Instead**
    Understand how customers want to buy.
    Match model to expectations.
    Consider market norms.
    

---
  #### **Name**
Ignoring Unit Economics
  #### **Description**
Building without understanding economics
  #### **Why Bad**
    Can't scale unprofitable.
    VC subsidy hides problems.
    Business isn't viable.
    
  #### **What To Do Instead**
    Model unit economics early.
    Validate before scaling.
    Fix economics at small scale.
    

---
  #### **Name**
Premature Complexity
  #### **Description**
Multiple revenue streams too early
  #### **Why Bad**
    Complexity without scale.
    Dilutes focus.
    Hard to optimize.
    
  #### **What To Do Instead**
    Master one model first.
    Add complexity with scale.
    Simple scales better.
    