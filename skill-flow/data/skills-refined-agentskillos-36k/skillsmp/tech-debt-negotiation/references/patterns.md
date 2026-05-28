# Tech Debt Negotiation

## Patterns


---
  #### **Name**
The Debt Inventory
  #### **Description**
Cataloging and quantifying technical debt
  #### **When To Use**
When you need to understand your debt landscape
  #### **Implementation**
    ## Tech Debt Inventory
    
    ### 1. Debt Categories
    
    | Category | Description | Impact Type |
    |----------|-------------|-------------|
    | Architecture | System design issues | Velocity |
    | Code Quality | Messy, hard-to-read code | Velocity |
    | Dependencies | Outdated libraries | Security/Velocity |
    | Testing | Missing or flaky tests | Quality/Velocity |
    | Documentation | Missing or wrong docs | Onboarding/Velocity |
    | Infrastructure | Manual processes, old tools | Operations |
    
    ### 2. The Debt Card
    
    ```
    For each debt item:
    
    NAME: [What it is]
    CATEGORY: [From above]
    AGE: [How long has this existed?]
    PAIN FREQUENCY: [How often does it hurt?]
    PAIN SEVERITY: [1-5 how much?]
    BLAST RADIUS: [Who/what does it affect?]
    ESTIMATED FIX: [Time to resolve]
    ```
    
    ### 3. Quick Quantification
    
    | Metric | Question |
    |--------|----------|
    | Time tax | Hours/week spent on this? |
    | Incident rate | Outages caused? |
    | Onboarding cost | Days added for new hires? |
    | Change risk | Deployments delayed? |
    | Team morale | Engineer complaints? |
    
    ### 4. Priority Matrix
    
    ```
              HIGH PAIN
                  │
       FIX NOW    │   FIX SOON
       (Quick win)│   (Plan it)
    ──────────────┼──────────────
       CONSIDER   │   IGNORE
       (If cheap) │   (Not worth it)
                  │
              LOW PAIN
         LOW EFFORT ───── HIGH EFFORT
    ```
    

---
  #### **Name**
The Business Translation
  #### **Description**
Converting tech debt to business impact
  #### **When To Use**
When explaining debt to non-technical stakeholders
  #### **Implementation**
    ## Speaking Business Language
    
    ### 1. Translation Table
    
    | Tech Speak | Business Speak |
    |------------|----------------|
    | "Bad code" | "Slower feature delivery" |
    | "Technical debt" | "Accumulated shortcuts" |
    | "Refactoring needed" | "Investment for faster delivery" |
    | "Legacy system" | "Aging infrastructure" |
    | "Code smell" | "Maintenance overhead" |
    | "Spaghetti code" | "Tightly coupled system" |
    
    ### 2. The Money Frame
    
    ```
    Calculate the tax:
    
    MONTHLY DEBT TAX:
    - Engineers affected × hours lost × hourly cost
    - Incidents × average resolution cost
    - Delayed features × opportunity cost
    
    Example:
    "This system costs us ~$15K/month in
    lost velocity and incident response."
    ```
    
    ### 3. The Risk Frame
    
    | Debt Type | Risk Language |
    |-----------|---------------|
    | Security debt | "Vulnerability exposure" |
    | Scaling debt | "Growth constraints" |
    | Quality debt | "Customer-facing defects" |
    | Knowledge debt | "Bus factor risk" |
    
    ### 4. Before/After Framing
    
    ```
    DON'T SAY:
    "We need to refactor the auth system."
    
    DO SAY:
    "Currently: 3 days to add any auth feature
    After: 3 hours for same features
    Investment: 2 weeks
    Payback: 2 months"
    ```
    

---
  #### **Name**
The Negotiation Playbook
  #### **Description**
Getting time allocated for debt reduction
  #### **When To Use**
When asking for maintenance capacity
  #### **Implementation**
    ## Getting Buy-In
    
    ### 1. The 20% Principle
    
    ```
    ASK FOR:
    20% of engineering capacity for maintenance
    
    WHY IT WORKS:
    - Industry standard (credible)
    - Not too scary (negotiable)
    - Sustainable (not a "project")
    ```
    
    ### 2. Negotiation Strategies
    
    | Strategy | How |
    |----------|-----|
    | Bundle it | Include debt work in feature work |
    | Tax it | "2 weeks feature + 3 days cleanup" |
    | Make it visible | Track "debt time" separately |
    | Show the trend | "Velocity dropping, here's why" |
    | Pick your battles | Fix high-impact items only |
    
    ### 3. Stakeholder Mapping
    
    | Stakeholder | Care About | Frame As |
    |-------------|------------|----------|
    | CEO | Revenue, costs | ROI, risk reduction |
    | Product | Features, speed | Faster delivery |
    | CTO | Quality, team | Sustainability |
    | Engineering | Morale, craft | Better DX |
    
    ### 4. The Velocity Graph Argument
    
    ```
          VELOCITY
             │╲
             │ ╲ ← Without maintenance
             │  ╲
             │   ╲___
             │        ╲____
             │              ╲___
             │
    ─────────┴──────────────────── TIME
    
          VELOCITY
             │    _______________
             │   /
             │  /  ← With 20% maintenance
             │ /
             │/
             │
    ─────────┴──────────────────── TIME
    ```
    

---
  #### **Name**
Strategic Debt Management
  #### **Description**
Intentionally taking and paying off debt
  #### **When To Use**
When making debt decisions
  #### **Implementation**
    ## Debt as Strategy
    
    ### 1. Good Debt vs Bad Debt
    
    | Good Debt | Bad Debt |
    |-----------|----------|
    | Intentional | Accidental |
    | Time-boxed | Open-ended |
    | Documented | Hidden |
    | Has payoff plan | Ignored |
    | Enables learning | Just lazy |
    
    ### 2. Debt Decision Framework
    
    ```
    TAKE DEBT IF:
    □ Time-sensitive opportunity
    □ Learning what to build
    □ Know we'll replace it
    □ Have payoff plan
    □ Team understands trade-off
    
    AVOID DEBT IF:
    □ Core system we'll keep
    □ Already high debt area
    □ No plan to address
    □ Team doesn't know
    ```
    
    ### 3. Debt Documentation
    
    | Document | Content |
    |----------|---------|
    | ADR | "We're taking this shortcut because..." |
    | TODO | "DEBT: [reason] - payoff by [date]" |
    | Ticket | Create follow-up immediately |
    | Tech Radar | Track debt items quarterly |
    
    ### 4. Payoff Triggers
    
    | Trigger | Action |
    |---------|--------|
    | Touching this code | Include cleanup |
    | Onboarding new dev | If blocking, prioritize |
    | Incident caused by debt | Fast-track fix |
    | Quarterly review | Reassess priority |
    

## Anti-Patterns


---
  #### **Name**
The Invisible Burden
  #### **Description**
Suffering silently without quantifying
  #### **Why Bad**
    What you can't measure, you can't argue for.
    Management sees "engineering wants to play."
    Never gets prioritized.
    
  #### **What To Do Instead**
    Track time lost.
    Document incidents.
    Make the invisible visible.
    

---
  #### **Name**
The Big Rewrite Pitch
  #### **Description**
Asking for months to "fix everything"
  #### **Why Bad**
    Sounds expensive.
    Sounds risky.
    Usually fails anyway.
    
  #### **What To Do Instead**
    Incremental improvements.
    Bundled with feature work.
    Show quick wins first.
    

---
  #### **Name**
Tech-Only Framing
  #### **Description**
Explaining debt in pure technical terms
  #### **Why Bad**
    Business doesn't understand.
    Sounds like engineer whining.
    No urgency created.
    
  #### **What To Do Instead**
    Translate to business impact.
    Money, time, risk.
    Concrete numbers.
    