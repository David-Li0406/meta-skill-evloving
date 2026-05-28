# Pricing Strategy - Sharp Edges

## The Freemium Trap - Free Is Too Good

### **Id**
freemium-trap
### **Severity**
critical
### **Situation**
  Company launches freemium product. Free tier is generous - most features,
  high limits. Users love it. Growth is great. Problem: 95% stay on free
  forever. Conversion to paid is 1%. Can't fund the business. Free users
  cost money to serve. Company is subsidizing free users with VC money.
  
### **Why**
  Freemium only works when there's a clear value cliff - a point where
  free stops working and paid becomes necessary. If free is "good enough"
  for most use cases, conversion will be terrible. The free tier should
  create desire for paid, not satisfy all needs.
  
### **Solution**
  1. Design the value cliff deliberately:
     - Free: Experience the product
     - Paid: Get real value from it
  
  2. Common value cliffs:
     - Usage limits (storage, API calls, messages)
     - Team features (collaboration, sharing)
     - Time limits (14 days then limited)
     - Brand removal (white-label)
     - Support level
  
  3. Test conversion at each limit:
     - Are users hitting the limit?
     - Do they upgrade or leave when they hit it?
     - If they stay on free, limit is too high
  
  4. Metrics to watch:
     - Free-to-paid conversion rate (target: 2-5%)
     - Time to conversion
     - Feature usage on free vs paid
  
### **Symptoms**
  - Conversion rate < 2%
  - Free users never hit limits
  - "Everyone loves our free tier"
  - High growth, no revenue
### **Detection Pattern**
freemium|free tier|conversion rate|free users

## Underpricing Death Spiral - Too Cheap to Survive

### **Id**
underpricing-death-spiral
### **Severity**
critical
### **Situation**
  Startup prices low to "get traction." Customers love the price. Growth
  happens. But margins are thin. Support costs eat profits. Can't afford
  to hire. Can't invest in product. Competitors with better pricing hire
  faster, build faster, overtake. Low price becomes the trap.
  
### **Why**
  Low prices attract price-sensitive customers who are expensive to serve
  and quick to churn. Low margins mean no money for growth, support, or
  product development. You end up working harder for less. Meanwhile,
  competitors with premium pricing have resources to invest.
  
### **Solution**
  1. Calculate true cost to serve:
     - Hosting, infrastructure
     - Support time per customer
     - Sales cost if applicable
     - Ongoing maintenance
  
  2. Ensure healthy margins:
     - SaaS: Target 70-80% gross margin
     - If margins < 50%, price is too low
  
  3. Premium positioning:
     - Higher price = perceived higher value
     - Attracts customers who value quality
     - Enables investment in product
  
  4. Price increase path:
     - If you're underpriced, raise prices
     - New customers first
     - Grandfather existing
  
### **Symptoms**
  - "We'll raise prices when we're bigger"
  - Margins below 50%
  - Can't afford to hire support
  - Competitors seem to have more resources
### **Detection Pattern**
low price|affordable|cheap|budget|margins

## Enterprise Discount Spiral - Negotiating Away Value

### **Id**
enterprise-discount-spiral
### **Severity**
high
### **Situation**
  Enterprise sales. Procurement asks for discount. Rep gives 30%. Next
  deal, that customer tells others. Everyone expects 30%. New customers
  ask for 40% because they heard about 30%. Price integrity collapses.
  Eventually giving 50% discounts to match "market rate" you created.
  
### **Why**
  Enterprise buyers talk to each other. Procurement benchmarks. Analysts
  publish pricing. One undisciplined discount becomes the new floor.
  Discounting without getting something in return trains buyers that
  your list price is a fiction.
  
### **Solution**
  1. Never discount without getting something:
     - Multi-year commitment
     - Annual prepayment
     - Case study rights
     - Logo usage
     - Reference calls
  
  2. Standard discount bands:
     - 10% for annual prepay
     - 15% for 2-year deal
     - 20% for 3-year with reference
     - Never exceed 25% regardless
  
  3. Alternative to discounts:
     - Extended payment terms
     - Free implementation
     - Additional seats
     - Premium support
  
  4. Sales discipline:
     - Approval required for > 15%
     - Executive approval for > 20%
     - Document reason for every discount
  
### **Symptoms**
  - Average discount > 20%
  - Customers comparing discounts
  - Sales leading with discount
  - Procurement always wins
### **Detection Pattern**
discount|negotiate|procurement|enterprise deal

## Per-Seat Gaming - Customers Cheating Seat Counts

### **Id**
per-seat-gaming
### **Severity**
medium
### **Situation**
  Per-seat pricing at $50/user/month. Customers buy 10 seats for 50 users.
  They share logins. Create "team@company.com" generic accounts. You're
  serving 50 users for the price of 10. Revenue per actual user is $10,
  not $50. Business model broken by user behavior.
  
### **Why**
  Per-seat pricing creates incentive to minimize seats. If price per seat
  is high enough that sharing is worth the hassle, customers will share.
  This is especially true when value doesn't scale linearly with users
  or when enforcement is weak.
  
### **Solution**
  1. Price low enough that sharing isn't worth it:
     - $10-15/seat: Low sharing incentive
     - $50+/seat: High sharing incentive
     - Find the threshold where it's easier to buy seats
  
  2. Technical enforcement:
     - Single active session per user
     - Device fingerprinting
     - Usage tracking per user
     - Fair use policies
  
  3. Alternative pricing models:
     - Usage-based (can't game by sharing)
     - Team tiers (flat rate up to N users)
     - Active user pricing (pay for who actually uses)
  
  4. Align incentives:
     - More users = more value for them
     - Make collaboration features gate to seats
     - Individual user features (personalization, history)
  
### **Symptoms**
  - User logins from multiple locations simultaneously
  - Generic email accounts (team@, sales@)
  - High usage per "seat"
  - Customers resisting seat adds
### **Detection Pattern**
per seat|per user|user count|seat count

## Usage-Based Revenue Volatility - Unpredictable Revenue

### **Id**
usage-revenue-volatility
### **Severity**
high
### **Situation**
  Usage-based pricing. Customers love flexibility. Company loves alignment
  with value. Q1: Revenue $100K. Q2: Revenue $60K. Same customers, less
  usage. CFO can't forecast. Investors worried. Team can't plan. Customer
  usage varies, revenue yo-yos.
  
### **Why**
  Pure usage-based pricing means revenue depends on customer behavior you
  don't control. Seasonality, customer cost-cutting, or product changes
  directly impact your revenue. This is especially painful for
  infrastructure and API companies.
  
### **Solution**
  1. Add committed minimums:
     - "Commit to $1000/month, get 20% off usage"
     - Creates floor on revenue
     - Predictability for both sides
  
  2. Blend subscription + usage:
     - Base platform fee (predictable)
     - Usage on top (variable)
     - 60-70% from subscription, 30-40% from usage
  
  3. Annual contracts with true-ups:
     - Annual commitment at estimated usage
     - Quarterly true-up for overages
     - Rollover for underusage (limited)
  
  4. Land with subscription, expand with usage:
     - Start with flat fee
     - Add usage-based as they scale
  
### **Symptoms**
  - Revenue varies 20%+ quarter to quarter
  - Can't forecast reliably
  - Investors asking about predictability
  - Customer budgets affecting your revenue
### **Detection Pattern**
usage based|consumption|per API call|metered

## Price Localization Complexity - The Global Pricing Maze

### **Id**
price-localization-complexity
### **Severity**
medium
### **Situation**
  Company expands globally. Prices in USD. Indian customers complain it's
  too expensive. European customers expect VAT included. Brazilian customers
  have payment method issues. Each market wants local pricing. Suddenly
  managing 50 price points, currency conversion, tax compliance. Nightmare.
  
### **Why**
  Global markets have wildly different willingness to pay, payment
  preferences, and tax requirements. India might be 1/3 US prices.
  Europe needs VAT. Brazil needs Pix. Managing this complexity can
  overwhelm a small team.
  
### **Solution**
  1. Start simple - tier by region:
     - Tier 1: US, UK, Canada, Australia, Western Europe
     - Tier 2: Eastern Europe, LATAM, Middle East
     - Tier 3: India, Southeast Asia, Africa
     - 100% / 60% / 40% of base price
  
  2. Use purchasing power parity (PPP):
     - Tools: Stripe, Paddle calculate PPP discounts
     - Automatic localized pricing
     - Shows commitment to fairness
  
  3. Let payment provider handle complexity:
     - Stripe handles currency, tax, payment methods
     - Paddle is merchant of record (handles VAT for you)
     - Worth the fees for complexity reduction
  
  4. When to localize:
     - >10% of traffic from a region
     - Conversion rate significantly lower than US
     - Strategic market entry
  
### **Symptoms**
  - Low conversion in specific countries
  - "Too expensive" from specific regions
  - Tax compliance concerns
  - Payment failures in some countries
### **Detection Pattern**
international|global|localization|currency|PPP

## Feature Gating Confusion - What's in Each Tier?

### **Id**
feature-gating-confusion
### **Severity**
medium
### **Situation**
  Three pricing tiers. Each tier has 10+ features. Feature matrix is
  complex. Customers can't tell which tier they need. Sales spends time
  explaining features instead of selling value. Upgrade reasons unclear.
  Customers on wrong tiers - either overpaying or hitting limits.
  
### **Why**
  Complex feature gating creates confusion. Customers don't know what
  they're buying. Decision paralysis kills conversion. Post-purchase,
  they're surprised by limits. This is especially common when features
  are added to tiers without clear strategy.
  
### **Solution**
  1. Simple tier logic:
     - Starter: For individuals
     - Team: For teams
     - Enterprise: For large organizations
  
  2. One primary differentiator:
     - Users/seats
     - OR usage volume
     - OR feature set
     - NOT all three
  
  3. Clear upgrade trigger:
     - Starter → Team: When you add teammates
     - Team → Enterprise: When you need security/compliance
     - Make it obvious when to upgrade
  
  4. Feature matrix rules:
     - Maximum 5-7 features per tier comparison
     - Lead with most important difference
     - Checkmarks, not paragraphs
  
### **Symptoms**
  - Customers asking which tier they need
  - Long sales calls explaining features
  - Customers on wrong tier
  - Feature matrix needs scrolling
### **Detection Pattern**
feature|tier|plan|which plan|pricing page

## Monthly Default Mistake - Leaving Money on Table

### **Id**
monthly-default-mistake
### **Severity**
medium
### **Situation**
  Pricing page shows monthly and annual. Monthly is default/highlighted.
  Most customers pick monthly. Annual customers would give 2 months
  free but you only get 1 month of commitment. Monthly customers churn
  before you recover CAC. Annual could have been easy money.
  
### **Why**
  Monthly subscriptions have higher effective churn (customers re-decide
  every month) and worse cash flow. Annual subscriptions lock in revenue
  and reduce churn. If annual is a better deal for customers (discount)
  and better for you (cash + retention), it should be the default.
  
### **Solution**
  1. Default to annual on pricing page:
     - Annual highlighted, monthly secondary
     - "Most popular" on annual
     - Show monthly as "pay more for flexibility"
  
  2. Right discount for annual:
     - 15-20% off for annual
     - "2 months free" framing
     - Calculate as: monthly × 10 for annual
  
  3. In-app annual conversion:
     - Prompt monthly users to upgrade to annual
     - Offer incentive at renewal
     - "Lock in this price for a year"
  
  4. Metrics to track:
     - Monthly vs annual mix (target: 60%+ annual)
     - Cohort retention by plan type
     - LTV by monthly vs annual
  
### **Symptoms**
  - >50% of customers on monthly
  - High early churn (before month 3)
  - Cash flow concerns
  - Monthly highlighted on pricing page
### **Detection Pattern**
monthly|annual|yearly|subscription|billing

## Price Anchoring Failure - Showing Prices Wrong

### **Id**
price-anchoring-failure
### **Severity**
low
### **Situation**
  Pricing page shows: "$9/mo, $29/mo, $99/mo" left to right, low to high.
  Customer anchors on $9. $29 seems expensive. $99 seems outrageous.
  Most customers buy $9 tier. You wanted them on $29.
  
### **Why**
  The first price seen becomes the anchor. Everything else is compared
  to it. If anchor is low, higher prices feel expensive. If anchor is
  high, lower prices feel like deals. The order you present prices
  shapes perception.
  
### **Solution**
  1. Show highest price first:
     - "$99/mo | $29/mo | $9/mo"
     - Enterprise | Team | Starter
     - Now $29 seems reasonable vs $99
  
  2. Decoy pricing:
     - Add a tier that makes target tier look good
     - If you want them on $29, make $39 tier minimal upgrade
     - $9 vs $29 vs $39: $29 looks like best value
  
  3. Highlight the target tier:
     - "Most popular" badge
     - Visual emphasis (larger, different color)
     - Default selection
  
  4. Show value first, price second:
     - Features and benefits above price
     - By the time they see price, value is anchored
  
### **Symptoms**
  - Most customers on cheapest tier
  - Middle tier underperforms
  - "Your prices seem high" feedback
### **Detection Pattern**
pricing page|price order|tiers|plans