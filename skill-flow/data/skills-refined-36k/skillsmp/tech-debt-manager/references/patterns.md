# Tech Debt Manager

## Patterns


---
  #### **Name**
The Debt Quadrant
  #### **Description**
Categorize debt by deliberateness and prudence
  #### **When**
Assessing and communicating about technical debt
  #### **Example**
    # Martin Fowler's Technical Debt Quadrant:
    
    #           PRUDENT                    RECKLESS
    #     +------------------+------------------+
    #     | "We must ship   | "We don't have  |
    # D   | now and deal    | time for design"|
    # E   | with consequen- |                 |
    # L   | ces later"      |                 |
    # I   +------------------+------------------+
    # B   | "Now we know    | "What's         |
    # E   | how we should   | layering?"      |
    # R   | have done it"   |                 |
    # A   |                 |                 |
    # T   +------------------+------------------+
    # E   INADVERTENT
    
    # QUADRANT ANALYSIS:
    
    ## Deliberate + Prudent (Top Left) ✓
    - Strategic choice to ship faster
    - Know exactly what's compromised
    - Have a plan to address it
    - Example: "We're using a simple solution now, will scale later"
    
    ## Deliberate + Reckless (Top Right) ✗
    - Cutting corners knowingly
    - No plan to fix
    - Creates danger
    - Example: "Just copy-paste it, we're behind schedule"
    
    ## Inadvertent + Prudent (Bottom Left) ✓
    - Learned something that changes your approach
    - Now understand better design
    - Can plan improvement
    - Example: "Now that we understand the domain, we'd structure it differently"
    
    ## Inadvertent + Reckless (Bottom Right) ✗
    - Don't know what you don't know
    - Poor practices from inexperience
    - Usually not even recognized as debt
    - Example: "I don't see any problems with this code"
    

---
  #### **Name**
Debt Interest Calculation
  #### **Description**
Quantify the ongoing cost of technical debt
  #### **When**
Prioritizing debt or communicating to stakeholders
  #### **Example**
    # INTEREST TYPES:
    
    ## 1. Development Velocity Interest
    """
    BEFORE: Adding feature to clean module: 2 days
    NOW: Adding feature to debt-laden module: 5 days
    
    Interest = 3 days per feature
    Features per quarter: 10
    Quarterly interest: 30 developer-days
    """
    
    ## 2. Bug Rate Interest
    """
    BEFORE: Clean module bug rate: 1 bug/month
    NOW: Debt-laden module bug rate: 5 bugs/month
    
    Extra bugs: 4/month
    Time per bug: 4 hours
    Monthly interest: 16 hours
    """
    
    ## 3. Onboarding Interest
    """
    BEFORE: New dev productive in area: 1 week
    NOW: New dev productive in debt area: 1 month
    
    Interest per new hire: 3 weeks
    New hires per year: 4
    Annual interest: 12 weeks
    """
    
    ## 4. Fear Interest (hardest to quantify)
    """
    Avoided features because "that code is scary"
    Workarounds instead of proper fixes
    Talent leaving because of frustration
    """
    
    # COMMUNICATION FORMAT:
    """
    TECH DEBT: Order Processing System
    
    CURRENT STATE:
    - 15-year-old codebase
    - No tests
    - 3 developers understand it
    
    INTEREST PAID (quarterly):
    - 60 extra dev-days for features
    - 40 hours debugging
    - 2 week onboarding overhead
    
    PRINCIPAL (to pay down):
    - Full rewrite: 6 months
    - Incremental: 3 months spread over 1 year
    
    RECOMMENDATION:
    - If changing frequently: Pay down incrementally
    - If stable: Accept interest (it's cheaper)
    """
    

---
  #### **Name**
Strategic Debt Decisions
  #### **Description**
Framework for deciding when to take on or pay off debt
  #### **When**
Making debt-related decisions
  #### **Example**
    # WHEN TO TAKE ON DEBT (deliberately):
    
    ## Valid reasons:
    - Time-to-market pressure with real business value
    - Learning: Build something to understand problem better
    - Prototype: Validate idea before investing in quality
    - Short-lived code: Will be replaced soon anyway
    
    ## Questions to ask:
    1. Is the business trade-off clear and accepted?
    2. Do we know specifically what we're compromising?
    3. Is there a plan to address it (even if "never")?
    4. Is the "interest" acceptable for expected lifetime?
    
    # WHEN TO PAY DOWN DEBT:
    
    ## Pay now when:
    - You're changing the code anyway (opportunistic)
    - Interest exceeds paydown cost (strategic)
    - It's blocking important work (necessary)
    - Safety/security is at risk (urgent)
    
    ## Don't pay when:
    - Code is stable and rarely touched
    - Rewrite risk exceeds debt risk
    - Interest is acceptable
    - Other work has higher priority
    
    # THE 3-QUESTION FILTER:
    """
    For any debt item, ask:
    
    1. Are we actively working in this area?
       No → Lower priority (debt isn't costing much)
       Yes → Continue to question 2
    
    2. Is the debt causing measurable problems?
       No → Maybe just hindsight, not real debt
       Yes → Continue to question 3
    
    3. Is paydown cost less than interest?
       No → Accept the debt
       Yes → Schedule paydown
    """
    

---
  #### **Name**
Opportunistic Debt Payment
  #### **Description**
Pay debt while doing related work
  #### **When**
Working in an area with existing debt
  #### **Example**
    # THE OPPORTUNISTIC APPROACH:
    
    ## Rule: When touching code, consider improving it
    ## But: Only if improvement is safe and relevant
    
    # EXAMPLE WORKFLOW:
    
    ## Task: Add email notification to order flow
    
    ## Step 1: Assess the area
    """
    ORDER FLOW CODE QUALITY:
    - Last modified: 2 years ago
    - Tests: None
    - Structure: One 500-line function
    - Debt: Yes, significant
    """
    
    ## Step 2: Decide scope
    """
    OPTIONS:
    A. Just add email (2 days)
       + Fast
       - Adds to mess
       - Harder to test email logic
    
    B. Refactor first, then add (5 days)
       + Clean code
       + Testable
       - 2.5x longer
       - More risk
    
    C. Add email, refactor touched parts (3 days)
       + Balanced
       + Leaves code better
       + Limited scope
    """
    
    ## Step 3: Propose to stakeholders
    """
    Recommendation: Option C
    
    Why: We're in this code anyway. Spending 1 extra day
    to refactor the notification section gives us:
    - Testable email logic
    - Cleaner path for next feature
    - Reduced future work in this area
    
    Trade-off: 1 day now saves ~3 days on next 2 features here.
    """
    
    # KEY PRINCIPLE:
    # Don't scope-creep into full refactoring.
    # Improve the specific area you're working in.
    # Leave the rest for when it's touched.
    

---
  #### **Name**
Debt Communication
  #### **Description**
Explaining tech debt to non-technical stakeholders
  #### **When**
Discussing priorities, roadmaps, or asking for time
  #### **Example**
    # EFFECTIVE DEBT COMMUNICATION:
    
    ## Use financial metaphor (Cunningham's intent)
    """
    BAD: "The code is messy and needs refactoring"
    GOOD: "We took a shortcut to ship faster. Now every
           feature in this area costs 3x what it should.
           We can pay down the debt, or keep paying interest."
    """
    
    ## Quantify in business terms
    """
    BAD: "We need 2 weeks to clean up tech debt"
    GOOD: "The order system takes 2 weeks per feature instead
           of 3 days. Spending 2 weeks now makes the next
           5 features cost 1.5 weeks each instead of 10."
    """
    
    ## Present options, not demands
    """
    BAD: "We MUST refactor before adding more features"
    GOOD: "We have options:
           A. Ship now, accept 3x cost on future features
           B. 2-week investment, then normal speed
           C. Incremental: 2 extra days per feature, done in 3 months"
    """
    
    ## Connect to business priorities
    """
    BAD: "The codebase is hard to work with"
    GOOD: "Remember when the checkout feature took 6 weeks?
           That area has significant debt. The new payment
           feature touches the same code. We can:
           - Spend 4 weeks on the feature as-is
           - Spend 2 weeks on debt + 1 week on feature"
    """
    
    # STAKEHOLDER-SPECIFIC FRAMING:
    
    ## To product managers:
    "This debt means features in this area take longer
     and have more bugs. Here are the trade-offs..."
    
    ## To executives:
    "This is an investment decision. Pay now or pay
     interest. Here's the ROI calculation..."
    
    ## To finance:
    "Like a loan - we got to market faster, now we're
     paying interest. Here are our refinancing options..."
    

## Anti-Patterns


---
  #### **Name**
Debt Denial
  #### **Description**
Pretending debt doesn't exist or isn't growing
  #### **Why**
    Ignoring debt doesn't make it go away. Interest accumulates. Development
    slows. Bugs increase. Eventually, something breaks badly and forces
    acknowledgment - usually at the worst time.
    
  #### **Instead**
Track debt openly. Communicate regularly. Make explicit decisions about what to accept vs address.

---
  #### **Name**
The Refactor Everything Urge
  #### **Description**
Treating all old code as debt that must be paid
  #### **Why**
    Not all old code is debt. Code you'd write differently today isn't
    necessarily bad - it's just different. Attempting to modernize everything
    creates endless work, introduces bugs, and delivers no business value.
    
  #### **Instead**
Prioritize ruthlessly. Pay debt only when interest exceeds cost or when working in that area.

---
  #### **Name**
Invisible Debt
  #### **Description**
Debt that nobody tracks or acknowledges
  #### **Why**
    If debt isn't visible, it can't be managed. Decisions are made without
    understanding true costs. New developers don't know where the landmines
    are. Eventually, everything is slower and nobody knows why.
    
  #### **Instead**
Make debt visible. Document known issues. Track time lost to debt. Communicate with stakeholders.

---
  #### **Name**
Debt Perfectionism
  #### **Description**
Refusing to take on any debt ever
  #### **Why**
    Sometimes debt is the right choice. Time-to-market matters. Learning
    happens. Refusing all shortcuts means slower delivery and missing
    opportunities. Deliberate, prudent debt is a valid tool.
    
  #### **Instead**
Make conscious debt decisions. Accept debt when trade-off is worthwhile. Track and plan for paydown.

---
  #### **Name**
Guilt-Driven Backlog
  #### **Description**
Creating tasks for every code smell and never doing them
  #### **Why**
    A 500-item "tech debt backlog" is useless. It creates guilt without
    action. Items rot and become irrelevant. The backlog becomes something
    to ignore rather than manage.
    
  #### **Instead**
Keep debt list short and actionable. Remove items you'll never do. Focus on high-impact debt.

---
  #### **Name**
Boy Scout Overreach
  #### **Description**
Improving unrelated code while doing a task
  #### **Why**
    "Leave code better than you found it" can become scope creep. Fixing
    unrelated issues in a PR increases risk, complicates review, and mixes
    concerns. If your fix introduces a bug, is it the task or the cleanup?
    
  #### **Instead**
Improve code you're actually changing for your task. Log other improvements for later.