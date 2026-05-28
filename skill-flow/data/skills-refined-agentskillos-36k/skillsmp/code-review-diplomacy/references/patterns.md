# Code Review Diplomacy

## Patterns


---
  #### **Name**
The Feedback Sandwich (Evolved)
  #### **Description**
Structuring review comments effectively
  #### **When To Use**
Writing any review comment
  #### **Implementation**
    ## Feedback That Lands
    
    ### 1. The Classic Sandwich (And Why It's Weak)
    
    ```
    OLD WAY:
    Positive → Negative → Positive
    
    WHY IT FAILS:
    - Transparent
    - Positive feels fake
    - Message gets lost
    ```
    
    ### 2. The Better Framework
    
    | Element | Example |
    |---------|---------|
    | Observation | "I see this function handles X" |
    | Impact | "This could cause Y under Z conditions" |
    | Suggestion | "Consider A, or alternatively B" |
    | Context | "I've seen this pattern cause issues in..." |
    
    ### 3. Comment Types
    
    | Type | Prefix | Meaning |
    |------|--------|---------|
    | Blocking | `[blocking]` | Must fix before merge |
    | Suggestion | `[suggestion]` | Better but not required |
    | Question | `[question]` | Curious, not critical |
    | Nitpick | `[nit]` | Trivial, take or leave |
    | Praise | `:+1:` | Genuinely good work |
    
    ### 4. Language Patterns
    
    ```
    INSTEAD OF:                     SAY:
    "This is wrong"                 "I think this might..."
    "You should"                    "Consider..."
    "Why did you"                   "What was the thinking behind..."
    "This doesn't work"             "I noticed that in X case..."
    "Obviously"                     [delete this word]
    ```
    

---
  #### **Name**
Receiving Reviews
  #### **Description**
Taking feedback without getting defensive
  #### **When To Use**
When your code is being reviewed
  #### **Implementation**
    ## Receiving Feedback Gracefully
    
    ### 1. The Emotional Response
    
    ```
    NORMAL TO FEEL:
    - Defensive
    - Annoyed
    - Attacked
    
    WHAT TO DO:
    1. Wait 5 minutes before responding
    2. Assume good intent
    3. Separate code from self
    ```
    
    ### 2. Response Framework
    
    | Feedback Type | Response |
    |---------------|----------|
    | Valid point | "Good catch, fixed" |
    | Disagreement | "I see it differently because X, thoughts?" |
    | Unclear | "Can you clarify what you mean by X?" |
    | Wrong | "Actually X because Y, but I see how it looks" |
    
    ### 3. Ego Management
    
    ```
    REMEMBER:
    
    - Code is not you
    - Feedback is about code, not character
    - Everyone gets feedback
    - Getting feedback = opportunity to improve
    - Reviewer spent time to help
    ```
    
    ### 4. Productive Disagreement
    
    | Approach | Example |
    |----------|---------|
    | Understand first | "Let me make sure I understand your concern..." |
    | Explain reasoning | "I went with X because..." |
    | Propose compromise | "What if we did X now and Y as follow-up?" |
    | Escalate kindly | "Want to sync on a call? Might be faster." |
    

---
  #### **Name**
Conflict Resolution
  #### **Description**
Handling heated review disagreements
  #### **When To Use**
When reviews become contentious
  #### **Implementation**
    ## De-Escalating Review Conflicts
    
    ### 1. Warning Signs
    
    | Signal | Meaning |
    |--------|---------|
    | Multiple replies | Escalating |
    | Longer comments | Getting heated |
    | "Actually" | Defensive mode |
    | All caps | Emotions high |
    | Third parties tagged | Going public |
    
    ### 2. De-Escalation Moves
    
    ```
    STEP 1: Change medium
    "This is getting complex. Quick call?"
    
    STEP 2: Acknowledge their view
    "I see why you'd prefer X, it does solve Y..."
    
    STEP 3: Find common ground
    "We both want Z, right? Let's work backwards."
    
    STEP 4: Propose options
    "What about A? Or we could try B?"
    ```
    
    ### 3. The Tie-Breaker
    
    | Situation | Resolution |
    |-----------|------------|
    | Style preference | Go with author's choice |
    | Performance concern | Benchmark it |
    | Architecture question | Tech lead decides |
    | Deadlocked | Ship it, revisit later |
    
    ### 4. Post-Conflict Recovery
    
    ```
    AFTER RESOLUTION:
    
    1. Don't hold grudges
    2. Thank them for the discussion
    3. Apply learnings to future reviews
    4. Document if it reveals a process gap
    ```
    

---
  #### **Name**
Building Review Culture
  #### **Description**
Creating a healthy team review environment
  #### **When To Use**
Improving team review practices
  #### **Implementation**
    ## Healthy Review Culture
    
    ### 1. Culture Signals
    
    | Healthy | Unhealthy |
    |---------|-----------|
    | Everyone reviews | Only seniors review |
    | Questions welcomed | Questions judged |
    | Praise given | Only criticism |
    | Fast turnaround | PRs rot for days |
    | Author learns | Author just fixes |
    
    ### 2. Team Agreements
    
    ```markdown
    ## Review Norms
    
    - Respond within [X hours]
    - Use prefixes: [blocking], [nit], [question]
    - Approve with suggestions OK
    - Discuss, don't dictate
    - Praise genuinely
    ```
    
    ### 3. Review Training
    
    | For | Teach |
    |-----|-------|
    | New reviewers | What to look for |
    | New authors | How to prepare PRs |
    | Everyone | Giving/receiving feedback |
    
    ### 4. Process Improvements
    
    | Problem | Solution |
    |---------|----------|
    | PRs too big | Size limits, stacked PRs |
    | Review bottleneck | Spread reviewers |
    | Inconsistent standards | Written guidelines |
    | Slow reviews | Review SLA |
    | Harsh reviews | Feedback training |
    

## Anti-Patterns


---
  #### **Name**
The Nitpicker
  #### **Description**
Blocking on minor style issues
  #### **Why Bad**
    Demoralizes authors.
    Slows down shipping.
    Creates resentment.
    
  #### **What To Do Instead**
    Use [nit] prefix.
    Auto-format with tools.
    Reserve blocking for real issues.
    

---
  #### **Name**
The Drive-By
  #### **Description**
Dropping critical comments without context
  #### **Why Bad**
    No explanation.
    Leaves author confused.
    Feels like attack.
    
  #### **What To Do Instead**
    Explain why.
    Offer alternatives.
    Be available for questions.
    

---
  #### **Name**
The Rubber Stamp
  #### **Description**
Approving without actually reviewing
  #### **Why Bad**
    Defeats the purpose.
    Misses real issues.
    False confidence.
    
  #### **What To Do Instead**
    Actually read the code.
    Leave meaningful comments.
    Ask questions if confused.
    