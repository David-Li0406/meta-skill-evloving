# Pricing Strategy

## Patterns


---
  #### **Name**
Value-Based Pricing Foundation
  #### **Description**
Price based on customer value, not your costs
  #### **When**
Setting prices for any product or feature
  #### **Example**
    # THE VALUE PRICING FRAMEWORK:
    
    ## Step 1: Quantify Customer Value
    """
    What does the customer gain from your product?
    
    Example - Sales automation tool:
    - Saves 10 hours/week per rep
    - Rep costs $50/hour fully loaded
    - Value created: $500/week = $26,000/year per rep
    
    Your price ceiling: ~$26,000/year/rep
    """
    
    ## Step 2: Apply Value Capture Ratio
    """
    Rule of thumb: Capture 10-25% of value created
    
    Example:
    - Value created: $26,000/year
    - 10% capture: $2,600/year
    - 20% capture: $5,200/year
    
    Price range: $2,600 - $5,200/year per seat
    """
    
    ## Step 3: Validate with Willingness to Pay
    """
    Ask: "At what price would this be..."
    - Too expensive to consider?
    - Getting expensive but still consider?
    - A bargain?
    - So cheap you'd question quality?
    
    (Van Westendorp Price Sensitivity Meter)
    """
    
    ## Cost-Plus is Wrong
    """
    DON'T: "Our costs are $10, add 50% margin = $15"
    DO: "We create $1000 in value, capture 15% = $150"
    
    Your costs are irrelevant to customer willingness to pay.
    """
    

---
  #### **Name**
The Pricing Model Decision Tree
  #### **Description**
Choosing between pricing models
  #### **When**
Deciding how to structure pricing
  #### **Example**
    # PRICING MODEL SELECTION:
    
    ## Usage-Based Pricing
    """
    WHEN TO USE:
    - Value scales with usage (API calls, data processed, messages)
    - Variable cost structure on your side
    - Customers have variable needs
    - Land-and-expand motion
    
    EXAMPLES: AWS, Twilio, Stripe, OpenAI
    
    GOTCHA: Revenue unpredictable. Enterprise budgeting hard.
    FIX: Offer committed use discounts.
    """
    
    ## Per-Seat Pricing
    """
    WHEN TO USE:
    - Value increases with more users
    - Easy to understand and budget
    - Network effects within organization
    - Sales wants predictable expansion
    
    EXAMPLES: Slack, Salesforce, Notion
    
    GOTCHA: Incentivizes seat minimization.
    FIX: Price low enough per seat that sharing isn't worth hassle.
    """
    
    ## Flat Rate / Tiered
    """
    WHEN TO USE:
    - Simple product with clear value
    - SMB market (budget certainty matters)
    - Self-serve motion
    - Early stage (simplicity > optimization)
    
    EXAMPLES: Basecamp, Netflix, many SaaS
    
    GOTCHA: Leaves money on table with large customers.
    FIX: Add enterprise tier or usage limits.
    """
    
    ## Freemium
    """
    WHEN TO USE:
    - Product has viral/network effects
    - Low marginal cost to serve free users
    - Free users provide value (content, data, referrals)
    - Long consideration cycle
    
    EXAMPLES: Dropbox, Spotify, LinkedIn
    
    GOTCHA: Free tier can be "good enough" forever.
    FIX: Clear value cliff. Time limits. Feature gates.
    """
    
    ## Free Trial
    """
    WHEN TO USE:
    - Product requires experience to understand value
    - High activation effort (worth it once invested)
    - B2B with stakeholder buy-in needed
    - Confident in activation and retention
    
    EXAMPLES: Salesforce, HubSpot, most B2B SaaS
    
    GOTCHA: Trial doesn't convert if time-to-value > trial length.
    FIX: Shorten time-to-value or extend trial.
    """
    

---
  #### **Name**
Early Stage Pricing
  #### **Description**
Pricing when you don't have data yet
  #### **When**
Pre-PMF or very early stage
  #### **Example**
    # EARLY STAGE PRICING RULES:
    
    ## Rule 1: Just Charge Something
    """
    Free is dangerous. It attracts wrong customers.
    Any price > $0 validates willingness to pay.
    
    Start paid from day one, even if price is wrong.
    You can always adjust. You can't undo "always been free."
    """
    
    ## Rule 2: Start Higher Than Comfortable
    """
    You're probably underpriced.
    Start at a price that makes you slightly uncomfortable.
    
    If no one complains about price, you're too cheap.
    If everyone complains, you're too expensive.
    Some complaints = probably right.
    """
    
    ## Rule 3: Price in Conversations
    """
    Early pricing is discovered, not calculated.
    
    Ask customers directly:
    - "What would you pay for this?"
    - "At what price would you not consider it?"
    - "What are you paying now for alternatives?"
    - "What budget do you have for this category?"
    
    10 conversations > 10,000 spreadsheet cells
    """
    
    ## Rule 4: Don't Anchor to Costs
    """
    Your costs are irrelevant to customers.
    A feature that took 6 months might be worth $0.
    A feature that took 1 day might be worth $10,000.
    
    Price on value, not effort.
    """
    
    ## Rule 5: Be Willing to Lose Deals on Price
    """
    If you win every deal, price is too low.
    Target: Win 60-70% of qualified opportunities.
    
    Losing some deals on price = healthy.
    Losing no deals on price = underpriced.
    """
    

---
  #### **Name**
Price Psychology Levers
  #### **Description**
Psychological factors that affect price perception
  #### **When**
Optimizing pricing presentation and structure
  #### **Example**
    # PRICING PSYCHOLOGY TOOLKIT:
    
    ## Anchoring
    """
    First number seen becomes the reference point.
    
    TACTIC: Show highest tier first.
    "Enterprise: $500/mo | Team: $100/mo | Starter: $20/mo"
    $100 feels reasonable compared to $500.
    
    TACTIC: Show "value" or "savings"
    "Worth $1000, yours for $199" anchors to $1000.
    """
    
    ## Decoy Effect
    """
    Add an option to make another option look better.
    
    CLASSIC EXAMPLE (The Economist):
    - Web only: $59
    - Print only: $125
    - Print + Web: $125  ← Decoy makes this obvious choice
    
    Your middle tier should be the decoy or the target.
    """
    
    ## Charm Pricing
    """
    $99 vs $100 - the left digit effect
    
    USE FOR: Consumer, SMB, self-serve
    AVOID FOR: Enterprise (looks unserious)
    
    $9.99 says "cheap"
    $10.00 says "round number"
    $9 says "simple and fair"
    """
    
    ## Price-Quality Signaling
    """
    Higher price = assumed higher quality
    (When customers can't evaluate quality directly)
    
    Premium positioning requires premium pricing.
    Cheap price signals cheap product.
    
    If you're the best, price like it.
    """
    
    ## Loss Aversion
    """
    Losses hurt 2x more than gains feel good.
    
    "Save $500/year" < "Stop losing $500/year"
    "Get 20% off" < "Don't miss 20% off, ends Friday"
    
    Frame around what they'll lose without you.
    """
    
    ## Grandfathering
    """
    Existing customers keep old price on price increase.
    
    Builds loyalty. Reduces churn.
    New customers pay new (higher) price.
    
    "You're locked in at the original rate."
    """
    

---
  #### **Name**
Enterprise Pricing Strategy
  #### **Description**
Pricing for large customers and sales-led motion
  #### **When**
Selling to enterprise or negotiating large deals
  #### **Example**
    # ENTERPRISE PRICING PLAYBOOK:
    
    ## Don't Put Enterprise Pricing on Website
    """
    "Contact Sales" for enterprise tier
    
    Why:
    1. Every enterprise deal is custom
    2. Avoids anchoring too low
    3. Creates human relationship opportunity
    4. Allows value discovery conversation
    """
    
    ## Value Discovery Before Price
    """
    Never quote price before understanding:
    - How many users/seats/units?
    - What's the problem costing them today?
    - What's the budget for this category?
    - Who else are they evaluating?
    - What's their timeline?
    
    Prescription before diagnosis is malpractice.
    """
    
    ## The 3x Rule
    """
    Enterprise should pay ~3x your standard price
    (for the same core product)
    
    They get: SLAs, support, security, customization
    You get: 3x revenue, longer contracts, references
    """
    
    ## Annual Contracts Default
    """
    Enterprise = Annual or multi-year
    - Reduces churn
    - Improves cash flow
    - Increases commitment
    
    Offer 10-20% discount for annual vs monthly.
    """
    
    ## Discounting Discipline
    """
    Never discount without getting something:
    - Annual commitment
    - Case study rights
    - Multi-year deal
    - Reference customer
    
    "I can offer 15% off for a 2-year commitment."
    Never: "Sure, 15% off, no problem."
    """
    
    ## Procurement Negotiation
    """
    Procurement's job is to get discounts.
    Your job is to protect value.
    
    TACTICS:
    - Have a "best price" you won't go below
    - Offer payment terms instead of discounts
    - Add services instead of reducing price
    - Use "list price" and "your price" framing
    
    They'll ask for 30%. Settle at 10-15%.
    """
    

---
  #### **Name**
Price Increase Execution
  #### **Description**
How to raise prices without losing customers
  #### **When**
Prices are too low and need adjustment
  #### **Example**
    # PRICE INCREASE PLAYBOOK:
    
    ## When to Raise Prices
    """
    Signals you're underpriced:
    - Win rate > 80% (too easy)
    - No price complaints ever
    - Customers say "it's a no-brainer"
    - Competitors charge 2x+ for similar
    - Margins are thin despite growth
    """
    
    ## How to Raise Prices
    """
    1. GRANDFATHER EXISTING CUSTOMERS
       - They keep old price for 12 months
       - Or keep forever if on annual plan
       - Reduces backlash, buys time
    
    2. ADD VALUE WITH INCREASE
       - New features launching
       - Better support tier
       - More storage/limits
       - "New pricing reflects new capabilities"
    
    3. COMMUNICATE EARLY
       - 60-90 days notice for B2B
       - Explain the why (costs, value, investment)
       - Offer annual lock-in at old price
    
    4. START WITH NEW CUSTOMERS
       - Test new pricing on new signups first
       - See conversion impact
       - Adjust before touching existing
    """
    
    ## Price Increase Email Template
    """
    Subject: Changes to [Product] pricing
    
    Hi [Name],
    
    We're writing to let you know about upcoming changes to
    our pricing, effective [Date].
    
    Over the past year, we've added [features], improved
    [capabilities], and [value additions]. To continue
    investing in making [Product] better, we're updating
    our pricing.
    
    Starting [Date], new pricing will be [X].
    
    As a valued customer, you're grandfathered at your
    current rate for the next 12 months. If you'd like to
    lock in your current rate longer, you can switch to
    annual billing before [Date].
    
    Thank you for being a [Product] customer.
    
    [Signature]
    """
    
    ## Common Mistakes
    """
    DON'T: Surprise customers with immediate increase
    DON'T: Increase without adding value
    DON'T: Raise prices during customer crisis
    DON'T: Apologize excessively (confidence matters)
    """
    

## Anti-Patterns


---
  #### **Name**
Race to the Bottom
  #### **Description**
Competing primarily on price
  #### **Why**
    Lowest price is not a sustainable moat. There's always someone cheaper.
    Price competition destroys margins for everyone. It attracts
    price-sensitive customers who churn when cheaper option appears.
    
  #### **Instead**
Compete on value, not price. Differentiate. Premium positioning.

---
  #### **Name**
Cost-Plus Pricing
  #### **Description**
Setting price as cost + margin
  #### **Why**
    Your costs are irrelevant to customer value. A feature that cost
    $100K to build might be worth $0 or $10M to customers. Cost-plus
    either leaves money on table or overprices commodity features.
    
  #### **Instead**
Price based on value to customer. Costs set floor, not price.

---
  #### **Name**
Competitor Matching
  #### **Description**
Setting price based on what competitors charge
  #### **Why**
    Competitors might be wrong. They might have different cost structure,
    different positioning, different customers. Your value prop is unique;
    your pricing should reflect that.
    
  #### **Instead**
Understand competitor pricing but set based on your value.

---
  #### **Name**
Pricing Once and Forgetting
  #### **Description**
Setting price at launch and never revisiting
  #### **Why**
    Markets change. Your product improves. Costs change. Customer value
    perception evolves. Static pricing leaves massive money on table
    or slowly kills the business as costs rise.
    
  #### **Instead**
Review pricing quarterly. Test continuously. Evolve.

---
  #### **Name**
Free Forever
  #### **Description**
Building without monetization plan
  #### **Why**
    Free attracts wrong users. Validates nothing about willingness to pay.
    Creates expectation of free. Makes eventual monetization harder.
    "We'll figure out monetization later" usually means "we never will."
    
  #### **Instead**
Charge from day one, even if price is experimental.

---
  #### **Name**
Complex Pricing
  #### **Description**
Too many tiers, options, add-ons, exceptions
  #### **Why**
    Confusion kills conversion. If customer can't understand price in
    30 seconds, they bounce. Cognitive load is conversion friction.
    Complex pricing suggests complex product.
    
  #### **Instead**
Maximum 3-4 tiers. Clear differentiation. Simple decision.

---
  #### **Name**
One-Size-Fits-All
  #### **Description**
Same price for all customer segments
  #### **Why**
    Enterprise customer getting $1M value pays same as startup getting
    $1K value. Massive money left on table. Or SMBs priced out.
    Different segments have different willingness to pay.
    
  #### **Instead**
Segment pricing. Tiers based on usage, features, or support.

---
  #### **Name**
Discounting as Default
  #### **Description**
Training customers to expect discounts
  #### **Why**
    Destroys price integrity. Customers wait for sales. Early adopters
    feel punished. Sales becomes discount negotiation, not value selling.
    Margins erode permanently.
    
  #### **Instead**
Discount only for commitment. Hold prices. Compete on value.