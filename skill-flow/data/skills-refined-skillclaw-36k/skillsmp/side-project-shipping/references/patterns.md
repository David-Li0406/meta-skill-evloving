# Side Project Shipping

## Patterns


---
  #### **Name**
The 48-Hour Ship
  #### **Description**
Shipping something meaningful in a weekend
  #### **When To Use**
When you have limited time windows
  #### **Implementation**
    ## 48-Hour Shipping Framework
    
    ### 1. Friday Night (2 hours)
    
    ```
    DEFINE THE ONE THING:
    
    "If this project does ONLY ONE THING,
    what would make it worth existing?"
    
    Write it down. This is your North Star.
    Everything else is distraction.
    ```
    
    ### 2. Saturday Morning (4 hours)
    
    | Task | Time |
    |------|------|
    | Core functionality | 3 hours |
    | Make it actually work | 1 hour |
    
    ```
    RULES:
    - No styling beyond defaults
    - No auth (hardcode if needed)
    - No database (JSON file is fine)
    - No deployment yet
    ```
    
    ### 3. Saturday Afternoon (4 hours)
    
    | Task | Time |
    |------|------|
    | Polish the ONE THING | 2 hours |
    | Basic "it works" UI | 2 hours |
    
    ### 4. Sunday Morning (3 hours)
    
    | Task | Time |
    |------|------|
    | Deploy anywhere | 1 hour |
    | Write README | 30 min |
    | Create launch tweet/post | 30 min |
    | Actually launch | 1 hour |
    
    ### 5. Sunday Afternoon
    
    ```
    CELEBRATE.
    
    You shipped.
    That's more than 99% of side projects.
    ```
    

---
  #### **Name**
The Feature Guillotine
  #### **Description**
Brutally cutting scope to what matters
  #### **When To Use**
When scope is growing
  #### **Implementation**
    ## Feature Guillotine
    
    ### 1. The Kill List
    
    ```
    List every feature you "want" to add.
    
    Now ask for each:
    "Can the project work without this?"
    
    YES → Cut it
    MAYBE → Cut it
    NO → Keep it (for now)
    ```
    
    ### 2. The One-Week Rule
    
    | If feature takes... | Decision |
    |---------------------|----------|
    | < 1 day | Maybe keep |
    | 1-3 days | Probably cut |
    | 3-7 days | Definitely cut |
    | > 1 week | You're building two projects |
    
    ### 3. Version 2 Graveyard
    
    ```
    Create a file: V2_FEATURES.md
    
    Put all cut features there.
    
    Tell yourself: "After I ship, I'll add these."
    
    (You probably won't. That's fine.)
    ```
    
    ### 4. The Embarrassment Test
    
    ```
    If you're not embarrassed by V1,
    you shipped too late.
    
    - Reid Hoffman
    ```
    

---
  #### **Name**
Motivation Preservation
  #### **Description**
Keeping momentum when enthusiasm fades
  #### **When To Use**
When you feel the project dying
  #### **Implementation**
    ## Keeping Side Projects Alive
    
    ### 1. The Motivation Curve
    
    ```
          EXCITEMENT
             /\
            /  \
           /    \
          /      \_____ THE TROUGH
         /              \_________
        /                         \
       Start                    Death
                                (unless you ship)
    ```
    
    ### 2. Trough Survival Tactics
    
    | When you feel... | Do this |
    |------------------|---------|
    | "This is boring now" | Ship immediately |
    | "Just one more feature" | Ship immediately |
    | "I'll work on it later" | Ship today or kill it |
    | "It's not ready" | It's more ready than you think |
    
    ### 3. Commitment Devices
    
    ```
    PUBLIC ACCOUNTABILITY:
    - Tweet "launching X on [DATE]"
    - Tell friends
    - Pre-announce
    
    DEADLINE FORCING:
    - Submit to Product Hunt
    - Schedule demo with someone
    - Buy the domain (sunk cost)
    ```
    
    ### 4. The 15-Minute Rule
    
    | Rule | Benefit |
    |------|---------|
    | Work 15 min daily | Keeps momentum |
    | Any progress counts | Defeats "big chunk" trap |
    | Streak psychology | Hard to break |
    

---
  #### **Name**
Launch Minimalism
  #### **Description**
The least you need to call it "launched"
  #### **When To Use**
When preparing to launch
  #### **Implementation**
    ## Minimum Viable Launch
    
    ### 1. True MVP Launch Checklist
    
    ```
    REQUIRED:
    □ It does the one thing
    □ Someone can access it
    □ You told at least one person
    
    THAT'S IT. YOU'VE LAUNCHED.
    ```
    
    ### 2. What You DON'T Need
    
    | Skip This | Why |
    |-----------|-----|
    | Custom domain | Vercel/Netlify URL is fine |
    | Perfect design | Functional > pretty |
    | Multiple pages | One page can work |
    | User accounts | Hardcode, use magic links |
    | Database | JSON, localStorage, whatever |
    | Analytics | Add after you have users |
    | SEO | You have no traffic yet |
    
    ### 3. Launch Platforms (Effort Ladder)
    
    | Platform | Effort | Reach |
    |----------|--------|-------|
    | Tweet/post | 5 min | Friends |
    | Reddit (relevant sub) | 15 min | Niche |
    | Hacker News | 15 min | Tech |
    | Product Hunt | 1 hour | Startup |
    | Blog post | 2 hours | SEO later |
    
    ### 4. The "Good Enough" Mantra
    
    ```
    Repeat after me:
    
    "Done is better than perfect."
    "Shipped beats polished."
    "Real users beat hypothetical ones."
    "I can always iterate."
    ```
    

## Anti-Patterns


---
  #### **Name**
The Perfect Launch
  #### **Description**
Waiting until everything is ready
  #### **Why Bad**
    "Ready" never comes.
    Motivation dies first.
    You learn nothing until you ship.
    
  #### **What To Do Instead**
    Ship ugly.
    Ship incomplete.
    Ship embarrassing.
    Just ship.
    

---
  #### **Name**
Feature Creep Addiction
  #### **Description**
Adding "just one more thing"
  #### **Why Bad**
    Each feature is a week of delay.
    Compounds complexity.
    Kills motivation.
    
  #### **What To Do Instead**
    V2_FEATURES.md graveyard.
    Ship first.
    Add features never.
    

---
  #### **Name**
The Rewrite Trap
  #### **Description**
Let me just refactor this first
  #### **Why Bad**
    Refactoring feels productive.
    But it doesn't move toward launch.
    It's procrastination in disguise.
    
  #### **What To Do Instead**
    Ship the messy code.
    Refactor only if you get users.
    Ugly shipped > elegant unshipped.
    