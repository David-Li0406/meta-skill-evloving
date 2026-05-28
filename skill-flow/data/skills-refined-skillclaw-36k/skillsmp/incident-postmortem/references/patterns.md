# Incident Postmortem

## Patterns


---
  #### **Name**
The Blameless Postmortem
  #### **Description**
Investigating without assigning blame
  #### **When To Use**
After any significant incident
  #### **Implementation**
    ## Blameless Postmortem Process
    
    ### 1. The Core Principle
    
    ```
    BLAMELESS ≠ ACCOUNTABLE-LESS
    
    We hold the SYSTEM accountable.
    We don't blame the PERSON.
    
    Because:
    - People make mistakes in bad systems
    - Blame hides information
    - Fear prevents learning
    - Systems can be improved, people can't be "fixed"
    ```
    
    ### 2. The Timeline
    
    | Phase | Timing | Focus |
    |-------|--------|-------|
    | Immediate | During/after | Fix the problem |
    | Documentation | 24-48 hours | Capture while fresh |
    | Analysis | 2-5 days | Deep investigation |
    | Review | 1 week | Share learnings |
    | Follow-up | 30 days | Verify actions done |
    
    ### 3. The Document Structure
    
    ```markdown
    # Incident Postmortem: [Title]
    
    **Date:** [When it happened]
    **Duration:** [How long]
    **Severity:** [Impact level]
    **Author:** [Who wrote this]
    
    ## Summary
    [2-3 sentences: What happened, impact]
    
    ## Timeline
    [Minute-by-minute during incident]
    
    ## Root Cause
    [What actually caused this]
    
    ## Contributing Factors
    [What made it worse/possible]
    
    ## What Went Well
    [Response successes]
    
    ## What Could Be Improved
    [Process/system gaps]
    
    ## Action Items
    [Specific improvements with owners]
    
    ## Lessons Learned
    [What we learned]
    ```
    
    ### 4. Language Guide
    
    | Instead of... | Say... |
    |---------------|--------|
    | "John broke production" | "The deploy included a bug that..." |
    | "Should have known" | "The system didn't surface..." |
    | "Human error" | "Process allowed incorrect..." |
    | "Careless mistake" | "Under time pressure..." |
    

---
  #### **Name**
The Five Whys
  #### **Description**
Getting to root cause, not symptoms
  #### **When To Use**
When investigating why something happened
  #### **Implementation**
    ## Five Whys Analysis
    
    ### 1. The Technique
    
    ```
    PROBLEM: Production went down
    
    Why? → Server ran out of memory
    Why? → Log files grew too large
    Why? → Log rotation wasn't configured
    Why? → No checklist for new services
    Why? → No standard service template
    
    ROOT CAUSE: No standard service template
    ```
    
    ### 2. Rules for Good Whys
    
    | Rule | Why |
    |------|-----|
    | Stay on one thread | Don't branch too early |
    | Ask "why" not "who" | Keeps it blameless |
    | Stop at system | People aren't root causes |
    | Verify each step | Confirm causation |
    | 5 is a guideline | Sometimes 3, sometimes 7 |
    
    ### 3. Common Traps
    
    | Trap | Problem | Fix |
    |------|---------|-----|
    | Stopping too early | "Human error" | Ask why error was possible |
    | Too many branches | Analysis paralysis | Focus on main thread |
    | Blame creeping in | Hides real causes | Reframe to system |
    | Guessing | Wrong conclusions | Verify with evidence |
    
    ### 4. Finding Multiple Roots
    
    ```
    Most incidents have multiple causes:
    
    CONTRIBUTING FACTORS:
    - Direct cause (the trigger)
    - Enabling factors (why trigger was possible)
    - System factors (why not caught earlier)
    
    Address all levels.
    ```
    

---
  #### **Name**
Effective Action Items
  #### **Description**
Creating actions that actually prevent recurrence
  #### **When To Use**
When defining postmortem follow-ups
  #### **Implementation**
    ## Action Items That Work
    
    ### 1. The SMART Action
    
    ```
    BAD: "Improve monitoring"
    GOOD: "Add memory usage alert at 80%
           threshold for all production
           services by [date], owned by [name]"
    
    SPECIFIC: What exactly
    MEASURABLE: How to verify
    ASSIGNED: Who owns it
    RELEVANT: Prevents recurrence
    TIME-BOUND: When by
    ```
    
    ### 2. Action Priority Matrix
    
    | Priority | Criteria |
    |----------|----------|
    | P1 - Now | Would prevent this exact incident |
    | P2 - Soon | Reduces likelihood significantly |
    | P3 - Later | General improvement |
    | P4 - Backlog | Nice to have |
    
    ### 3. Types of Actions
    
    | Type | Example |
    |------|---------|
    | Detection | Add alert for X condition |
    | Prevention | Validate Y before deploy |
    | Mitigation | Auto-scale when Z happens |
    | Process | Add checklist step for A |
    | Documentation | Document how B works |
    
    ### 4. Follow-Through
    
    | Check | When |
    |-------|------|
    | Actions assigned | End of postmortem |
    | Progress update | Weekly |
    | Completion verification | At deadline |
    | Effectiveness review | 30 days later |
    

---
  #### **Name**
The Learning Review
  #### **Description**
Sharing incident learnings broadly
  #### **When To Use**
After completing postmortem
  #### **Implementation**
    ## Spreading the Learning
    
    ### 1. The Review Meeting
    
    ```
    AGENDA (30 min):
    
    1. Context (5 min)
       - What happened, briefly
    
    2. Timeline walkthrough (10 min)
       - Key moments
       - Decision points
    
    3. Root cause discussion (10 min)
       - What we found
       - How it applies elsewhere
    
    4. Actions and questions (5 min)
       - What we're doing
       - Open discussion
    ```
    
    ### 2. Who Should Attend
    
    | Definitely | Maybe | Skip |
    |------------|-------|------|
    | Responders | Related teams | Unrelated teams |
    | System owners | On-call | Executives (unless major) |
    | Relevant leads | New team members | |
    
    ### 3. Making It Safe
    
    ```
    MEETING NORMS:
    
    - No blame, only curiosity
    - "What" not "who"
    - All perspectives valued
    - Focus on system improvement
    - OK to say "I don't know"
    ```
    
    ### 4. Institutional Learning
    
    | Action | Purpose |
    |--------|---------|
    | Postmortem database | Learn from history |
    | Pattern analysis | Find systemic issues |
    | Cross-team sharing | Prevent similar elsewhere |
    | Onboarding reading | Teach new members |
    

## Anti-Patterns


---
  #### **Name**
The Blame Game
  #### **Description**
Focusing on who instead of what
  #### **Why Bad**
    People hide information.
    Fear replaces learning.
    Same problems recur.
    
  #### **What To Do Instead**
    Ask "what" not "who."
    Focus on systems.
    Make it safe to share.
    

---
  #### **Name**
The Action Item Graveyard
  #### **Description**
Creating actions that never get done
  #### **Why Bad**
    Same incidents recur.
    Postmortems feel pointless.
    Trust erodes.
    
  #### **What To Do Instead**
    Fewer, better actions.
    Clear ownership.
    Track completion.
    

---
  #### **Name**
The Shallow Analysis
  #### **Description**
Stopping at the first cause found
  #### **Why Bad**
    Misses real issues.
    Fixes symptoms, not causes.
    Incidents repeat.
    
  #### **What To Do Instead**
    Ask "why" five times.
    Look for system causes.
    Dig deeper.
    