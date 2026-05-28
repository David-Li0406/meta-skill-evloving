# Easter Egg Design

## Patterns


---
  #### **Name**
Easter Egg Types
  #### **Description**
Categories of hidden features
  #### **When To Use**
Choosing what kind of easter egg to create
  #### **Implementation**
    ## Easter Egg Categories
    
    ### 1. Type Taxonomy
    
    | Type | Description | Example |
    |------|-------------|---------|
    | Code Triggered | Specific input sequence | Konami code |
    | Exploration | Found by poking around | Hidden pages |
    | Time-based | Appears at specific times | Holiday themes |
    | Cumulative | Unlocked by usage | Achievement unlock |
    | Social | Requires multiple users | Collaborative unlock |
    | Contextual | Appears in specific conditions | Empty state jokes |
    
    ### 2. Reward Types
    
    | Reward | Impact | Shareability |
    |--------|--------|--------------|
    | Visual change | Medium | High (screenshot-able) |
    | Sound effect | Low-Medium | Medium |
    | Hidden game | High | Very high |
    | Secret mode | High | High |
    | Message/joke | Low | Medium |
    | Functional unlock | High | Varies |
    
    ### 3. Effort vs Reward Matrix
    
    ```
    High Reward
         │
         │  [Hidden game]    [Secret mode]
         │
         │  [Rare unlock]    [Visual easter egg]
         │
         ├─────────────────────────────────
         │                    Easy Discovery
    Hard │
    Discovery  [Dev signature]  [Loading joke]
         │
         │  [Secret API]      [Empty state fun]
         │
    Low Reward
    ```
    
    ### 4. Selection Criteria
    
    ```
    Choose type based on:
    
    - Audience: Who will find this?
    - Platform: What's possible here?
    - Brand: Does it fit personality?
    - Effort: Worth the dev time?
    - Longevity: Will it age well?
    ```
    

---
  #### **Name**
Discovery Design
  #### **Description**
How users find easter eggs
  #### **When To Use**
Engineering the discovery experience
  #### **Implementation**
    ## Discovery Mechanics
    
    ### 1. Discovery Methods
    
    | Method | How Found | Example |
    |--------|-----------|---------|
    | Accidental | Random user action | Clicking logo 7 times |
    | Curious | Exploring UI | Hidden menu item |
    | Informed | Hints or rumors | "Type this phrase" |
    | Social | Others share | Friend shows you |
    | Seasonal | Time-limited | Holiday appearance |
    
    ### 2. Discoverability Calibration
    
    ```
    Too Hidden                    Too Obvious
    ─────────────────────────────────────────
    Never found ← Sweet Spot → Not special
    
    Sweet spot factors:
    - Some people find naturally
    - Those who find share
    - Feels exclusive but findable
    - Hints exist if you look
    ```
    
    ### 3. Hint Design
    
    | Hint Level | Example |
    |------------|---------|
    | None | Pure exploration reward |
    | Subtle | Unusual UI element |
    | Moderate | Tooltip or hover text |
    | Explicit | "Try [action] for a surprise" |
    
    ### 4. Discovery Journey
    
    ```
    Ideal discovery arc:
    
    1. CURIOSITY
       "What happens if I..."
    
    2. EXPERIMENTATION
       Trying different things
    
    3. DISCOVERY
       The reveal moment
    
    4. DELIGHT
       Emotional payoff
    
    5. SHARING
       "You have to see this!"
    ```
    

---
  #### **Name**
Shareability Engineering
  #### **Description**
Making discoveries spread
  #### **When To Use**
Maximizing word-of-mouth from easter eggs
  #### **Implementation**
    ## Shareability Design
    
    ### 1. Share Triggers
    
    ```
    People share when they feel:
    
    - Special (I found this!)
    - Generous (You'll love this!)
    - Smart (I figured it out!)
    - Connected (Remember this?)
    - Amused (This is hilarious!)
    ```
    
    ### 2. Share Format Optimization
    
    | Format | Shareability | Design For |
    |--------|--------------|------------|
    | Screenshot | High | Visual impact |
    | Video | Very high | Motion/sound |
    | Story | High | Memorable moment |
    | Demo | Highest | "Try this" |
    
    ### 3. Share-Friendly Features
    
    ```
    Make sharing easy:
    
    1. VISUAL CLARITY
       - Clear in screenshot
       - Works out of context
       - Interesting at a glance
    
    2. DEMONSTRABLE
       - Others can try it
       - Steps are simple
       - Works reliably
    
    3. CONTEXTUAL HOOK
       - "In [product], try..."
       - Clear what product is
       - Brand visible
    ```
    
    ### 4. Viral Easter Egg Anatomy
    
    | Element | Purpose |
    |---------|---------|
    | Discoverable | Some people find it |
    | Shareable | Format spreads easily |
    | Reproducible | Others can try it |
    | Delightful | Worth sharing |
    | On-brand | Reinforces product |
    

---
  #### **Name**
Famous Easter Eggs
  #### **Description**
Learn from the best
  #### **When To Use**
Inspiration and patterns
  #### **Implementation**
    ## Easter Egg Hall of Fame
    
    ### 1. Classic Examples
    
    | Product | Easter Egg | Why It Works |
    |---------|------------|--------------|
    | Google | "Do a barrel roll" | Simple, visual, shareable |
    | Slack | Loading messages | Personality, discovery |
    | GitHub | 404 pages | Brand personality |
    | Chrome | Dinosaur game | Utility in frustration |
    | Spotify | Star Wars theme | Cultural reference |
    
    ### 2. Pattern Analysis
    
    **Google "Do a barrel roll"**
    ```
    Trigger: Search specific phrase
    Reward: Visual animation
    Discovery: Word of mouth
    Shareability: Easy to show/tell
    Brand fit: Playful, surprising
    ```
    
    **Chrome Dinosaur Game**
    ```
    Trigger: No internet connection
    Reward: Full game
    Discovery: Accidental
    Shareability: Screenshot scores
    Brand fit: Helpful, human
    ```
    
    ### 3. Easter Egg Principles
    
    ```
    From the best examples:
    
    1. Reward curiosity
    2. Match brand personality
    3. Be genuinely delightful
    4. Enable sharing naturally
    5. Don't break main experience
    6. Age gracefully
    ```
    
    ### 4. Anti-Patterns from History
    
    | Anti-Pattern | Problem |
    |--------------|---------|
    | Too complex trigger | Never discovered |
    | Inside joke only | Alienates most users |
    | Dated reference | Ages badly |
    | Breaks accessibility | Excludes users |
    | One-time only | Limits sharing |
    

## Anti-Patterns


---
  #### **Name**
Over-Hidden
  #### **Description**
Easter eggs no one ever finds
  #### **Why Bad**
    Wasted effort.
    No delight delivered.
    No word of mouth.
    
  #### **What To Do Instead**
    Calibrate discoverability.
    Seed hints.
    Monitor discovery rate.
    

---
  #### **Name**
Breaking Core Experience
  #### **Description**
Easter eggs that interfere with main product
  #### **Why Bad**
    Confuses users.
    Damages usability.
    Unprofessional.
    
  #### **What To Do Instead**
    Keep easter eggs separate.
    Never affect critical paths.
    Easy to exit.
    

---
  #### **Name**
Inside Jokes Only
  #### **Description**
References only developers get
  #### **Why Bad**
    Alienates users.
    Feels exclusionary.
    Misses opportunity.
    
  #### **What To Do Instead**
    Test with real users.
    Universal references.
    Brand-relevant humor.
    