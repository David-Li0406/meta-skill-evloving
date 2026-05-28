# Community Operations

## Patterns


---
  #### **Name**
Moderation Framework
  #### **Description**
Comprehensive moderation system design
  #### **When To Use**
When establishing or revamping moderation
  #### **Implementation**
    ## Moderation System Design
    
    ### Moderation Tiers
    | Level | Action | Who | Response Time |
    |-------|--------|-----|---------------|
    | 1 | Spam, obvious violations | Automod/bots | Instant |
    | 2 | Minor violations | Junior mods | < 1 hour |
    | 3 | Serious violations | Senior mods | < 4 hours |
    | 4 | Bans, legal issues | Lead/Admin | < 24 hours |
    
    ### Escalation Path
    ```
    Automod → Junior Mod → Senior Mod → Lead → Admin → Legal
    ```
    
    ### Moderation Actions
    | Severity | First Offense | Second | Third |
    |----------|---------------|--------|-------|
    | Minor | Warning | 24h mute | 7d mute |
    | Moderate | 24h mute | 7d ban | Permanent |
    | Severe | 7d ban | Permanent | Report to platform |
    | Critical | Immediate ban | N/A | N/A |
    
    ### Documentation Required
    - Screenshot of violation
    - Rule violated
    - Action taken
    - Mod who took action
    - Appeals process communicated
    

---
  #### **Name**
Onboarding Flow Design
  #### **Description**
First-time member experience
  #### **When To Use**
When setting up or optimizing new member experience
  #### **Implementation**
    ## Member Onboarding
    
    ### The First 5 Minutes
    ```
    JOIN → WELCOME → RULES → INTRO → FIRST VALUE → FIRST CONNECTION
    ```
    
    ### Onboarding Checklist
    - [ ] Automated welcome message (immediate)
    - [ ] Rules acknowledgment (before access)
    - [ ] Self-introduction prompt (guided)
    - [ ] Channel orientation (where to go)
    - [ ] First quick win (value in < 5 min)
    - [ ] Human connection (staff or member reply)
    
    ### Welcome Message Template
    ```
    Hey [name]! Welcome to [community]!
    
    Quick start:
    1. Introduce yourself in #introductions
    2. Check out #start-here for orientation
    3. Ask questions in #help
    
    Our values: [brief values]
    
    Need anything? Ping @community-team
    ```
    
    ### Tracking Onboarding Success
    | Metric | Target | How to Measure |
    |--------|--------|----------------|
    | Intro completion | 60%+ | Posted in intros |
    | First message | 40%+ | Any message in 48h |
    | First week return | 50%+ | Active day 7 |
    | First value | < 5 min | Time to first reply |
    

---
  #### **Name**
Crisis Response Protocol
  #### **Description**
Handling community incidents and crises
  #### **When To Use**
When serious issues arise
  #### **Implementation**
    ## Crisis Response Framework
    
    ### Crisis Levels
    | Level | Example | Response |
    |-------|---------|----------|
    | 1 | Heated argument | Mod intervention |
    | 2 | Harassment report | Senior mod, documentation |
    | 3 | Coordinated attack | All hands, lockdown option |
    | 4 | Legal/safety threat | Leadership, legal, platform |
    
    ### Immediate Actions (First 15 Minutes)
    1. Assess severity level
    2. Document everything (screenshots)
    3. Contain if possible (mute, slow mode)
    4. Alert appropriate team members
    5. Do NOT engage emotionally
    
    ### Communication Template
    ```
    Team - we have a Level [X] situation:
    
    What happened: [brief factual summary]
    Current status: [contained/ongoing]
    Immediate needs: [what help needed]
    Next steps: [planned actions]
    
    Thread for updates: [link]
    ```
    
    ### Post-Crisis
    - Incident report within 24h
    - Team debrief within 48h
    - Process improvements identified
    - Community update if needed
    - Support for affected members
    

---
  #### **Name**
Scaling Operations
  #### **Description**
Growing ops without burning out
  #### **When To Use**
When community growth outpaces team capacity
  #### **Implementation**
    ## Scaling Framework
    
    ### Team Structure by Size
    | Community Size | Team Structure |
    |----------------|----------------|
    | 0-500 | 1 community manager |
    | 500-2K | CM + 2-3 volunteer mods |
    | 2K-10K | CM + mod lead + 5-10 mods |
    | 10K-50K | Community team + regional mods |
    | 50K+ | Full community org |
    
    ### Automation Priorities
    | Automate First | Keep Human |
    |----------------|------------|
    | Spam filtering | Appeals |
    | Welcome messages | Introductions |
    | FAQ responses | Complex questions |
    | Role assignment | Culture enforcement |
    | Metrics collection | Relationship building |
    
    ### Mod Team Management
    - Clear roles and responsibilities
    - Regular syncs (weekly minimum)
    - Recognition and appreciation
    - Burnout monitoring
    - Growth paths (mod → senior → lead)
    

## Anti-Patterns


---
  #### **Name**
Mod Burnout Factory
  #### **Description**
Overworking volunteer moderators
  #### **Why Bad**
    Volunteers have limits. Burned out mods quit or become toxic.
    No recognition leads to resentment. Inconsistent coverage hurts community.
    
  #### **What To Do Instead**
    Set clear shift expectations. Rotate responsibilities.
    Recognize contributions publicly. Check in on mental health.
    Build mod team, not mod heroes.
    

---
  #### **Name**
Rule Lawyer Moderation
  #### **Description**
Applying rules without context or empathy
  #### **Why Bad**
    Communities are human, not courtrooms.
    Technically correct but emotionally wrong damages trust.
    Members feel policed, not supported.
    
  #### **What To Do Instead**
    Train mods on intent behind rules. Empower judgment calls.
    Default to empathy, escalate edge cases.
    Focus on outcomes, not just rules.
    

---
  #### **Name**
Invisible Until Crisis
  #### **Description**
Mods only visible when enforcing rules
  #### **Why Bad**
    Members see mods as police, not community members.
    No relationship built before conflict.
    Enforcement feels punitive, not protective.
    
  #### **What To Do Instead**
    Mods participate as regular members too.
    Positive interactions outnumber enforcement.
    Build relationships before needing to moderate.
    