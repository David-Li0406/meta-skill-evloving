# Burn Rate Management

## Patterns


---
  #### **Name**
Weekly Cash Dashboard
  #### **Description**
Track actual vs. projected burn every single week
  #### **When**
From day 1 of first dollar raised through profitability
  #### **Example**
    Every Monday morning review:
    
    Current bank balance: $847K
    This month's burn (actual): $62K (projected: $58K)
    Last month's burn: $54K
    Runway at current burn: 13.7 months
    Runway at projected burn: 12.1 months
    
    Red flags:
    - Burn up 15% MoM without revenue increase
    - Runway under 12 months
    - Actual > projected 2 months in a row
    
    This takes 10 minutes. It prevents death.
    

---
  #### **Name**
Default Alive Calculation
  #### **Description**
Calculate if you'll reach profitability before running out of money
  #### **When**
Monthly, or when making hiring/spending decisions
  #### **Example**
    Current burn: $50K/month
    Current revenue: $15K/month (growing 12% MoM)
    Bank balance: $600K
    
    Formula:
    Months to profitability = log(burn/revenue) / log(1 + growth_rate)
    = log(50/15) / log(1.12) = 10.6 months
    
    Runway = bank / burn = 600 / 50 = 12 months
    
    12 > 10.6 = DEFAULT ALIVE ✓
    
    If runway < months to profitability = DEFAULT DEAD
    Then: cut burn or raise money NOW.
    

---
  #### **Name**
Zero-Based Budgeting
  #### **Description**
Every expense must justify itself from zero, not just incremental increases
  #### **When**
Quarterly, and when runway gets below 18 months
  #### **Example**
    Don't ask: "Should we increase AWS from $5K to $7K?"
    Ask: "If we were starting today, would we spend $7K on AWS?"
    
    Review every line item:
    - Tools: $12K/month - which ones are actually used?
    - Office: $8K/month - could we be remote?
    - Contractors: $20K/month - could we hire FTE?
    
    Kill 20% of spend every quarter.
    Forces prioritization, kills zombie costs.
    

---
  #### **Name**
Pre-Mortem Before Hiring
  #### **Description**
Before every hire, calculate the full cost and risk
  #### **When**
Before extending any offer
  #### **Example**
    Hire: Senior Engineer at $180K
    
    Full annual cost:
    - Salary: $180K
    - Benefits: $27K (15%)
    - Recruiter: $36K (20% fee)
    - Equipment: $5K
    - Tools/licenses: $3K
    Total: $251K first year, $210K ongoing
    
    Questions:
    - What metric does this 2x?
    - What breaks if we don't hire them?
    - Can we contract this for 6 months first?
    - Do we have 24 months runway after this hire?
    
    If you can't answer clearly: don't hire.
    

---
  #### **Name**
Cut Once, Cut Deep
  #### **Description**
When you need to reduce burn, cut hard enough that you never have to do it again
  #### **When**
When runway drops below 12 months without path to revenue
  #### **Example**
    Bad: Cut 10%, see if it works, cut 10% more, repeat
    Good: Calculate needed runway, cut to that number, done
    
    Math:
    Current burn: $80K/month
    Runway: 10 months
    Need: 18 months minimum
    Target burn: $800K / 18 = $44K/month
    
    Must cut: $36K/month (45% reduction)
    
    Make the full cut now. Team needs clarity.
    Multiple cuts destroy morale worse than one big one.
    

---
  #### **Name**
Revenue as Oxygen
  #### **Description**
Every dollar of revenue extends runway disproportionately
  #### **When**
Always, but especially when default dead
  #### **Example**
    Scenario A (no revenue):
    Burn: $50K/month, bank: $600K
    Runway: 12 months
    
    Scenario B ($20K MRR):
    Net burn: $30K/month, bank: $600K
    Runway: 20 months
    
    $20K/month revenue = +8 months runway
    
    Even small revenue is huge leverage.
    Prioritize revenue over perfection.
    $1 recurring revenue > $100 one-time.
    

## Anti-Patterns


---
  #### **Name**
Hope-Driven Burn Planning
  #### **Description**
Assuming revenue will materialize or fundraising will work out
  #### **Why**
Revenue is always later than you think. Fundraising takes 3-6 months. Hope is not a plan.
  #### **Instead**
    Plan for zero new revenue.
    Plan for fundraising taking 6 months.
    Build 18-month runway buffer.
    Treat revenue as upside, not assumption.
    

---
  #### **Name**
Fully Loaded Cost Blindness
  #### **Description**
Only looking at salary, ignoring benefits, taxes, equipment, tools
  #### **Why**
A $100K hire costs $130-150K all-in. You're underestimating burn by 30%.
  #### **Instead**
    Calculate full annual cost:
    - Salary
    - Benefits (health, 401k): +15%
    - Payroll taxes: +10%
    - Equipment: $3-5K
    - Software/tools: $2-4K
    
    Use fully loaded cost in all burn calculations.
    

---
  #### **Name**
Incremental Budgeting
  #### **Description**
Starting from last month's spend and tweaking up/down
  #### **Why**
Locks in waste. Never questions if you should be spending at all. Costs only grow.
  #### **Instead**
    Zero-based budgeting quarterly.
    Every line item justifies from zero.
    "We spent it last month" is not a reason.
    Kill 20% of spend every quarter.
    

---
  #### **Name**
Vanity Hiring
  #### **Description**
Hiring because competitors are hiring or to look legitimate
  #### **Why**
Competitors' cash situation isn't yours. Headcount doesn't impress customers. Burns runway.
  #### **Instead**
    Hire only when:
    - Specific metric is blocked by capacity
    - You've personally done the job and it's crushing you
    - The hire will 2x a key metric
    
    Stay small as long as possible.
    

---
  #### **Name**
Raising When Desperate
  #### **Description**
Starting fundraising with 6 months runway or less
  #### **Why**
Desperation shows. Bad terms. Takes 3-6 months. High failure risk. Bridge rounds are expensive.
  #### **Instead**
    Start raising with 18+ months runway.
    Give yourself 6 months to close.
    If you must bridge, note with 20% discount + warrants.
    Better: cut burn aggressively and extend runway.
    

---
  #### **Name**
Celebrating the Raise
  #### **Description**
Treating fundraising as success and relaxing on burn
  #### **Why**
Fundraising isn't success, it's buying time. Money in bank creates false comfort. Burn tends to expand.
  #### **Instead**
    Fundraise = runway, not validation.
    Keep burn discipline post-raise.
    Revenue is the real milestone.
    Act like you have half what you raised.
    