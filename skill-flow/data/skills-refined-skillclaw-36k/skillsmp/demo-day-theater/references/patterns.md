# Demo Day Theater

## Patterns


---
  #### **Name**
The Demo Arc
  #### **Description**
Structuring demos for maximum impact
  #### **When To Use**
Any stakeholder demo
  #### **Implementation**
    ## Demo Story Arc
    
    ### 1. The Structure
    
    ```
    SETUP (30 seconds)
    "Before, users had to..."
    [Show the pain]
    
    TENSION (30 seconds)
    "We solved this by..."
    [Brief explanation]
    
    PAYOFF (60 seconds)
    "Now watch..."
    [The magic moment]
    
    IMPACT (30 seconds)
    "This means..."
    [Business value]
    ```
    
    ### 2. Timing Guide
    
    | Segment | Time | Purpose |
    |---------|------|---------|
    | Hook | 10 sec | Grab attention |
    | Problem | 20 sec | Create empathy |
    | Solution | 20 sec | Build anticipation |
    | Demo | 60 sec | Deliver payoff |
    | Impact | 20 sec | Cement value |
    | Q&A | Variable | Address concerns |
    
    ### 3. The Golden Rule
    
    ```
    TOTAL DEMO TIME: 3-5 minutes max
    
    Attention drops after 5 minutes.
    Say less, show more.
    Leave them wanting more.
    ```
    
    ### 4. Multiple Features
    
    | Number | Approach |
    |--------|----------|
    | 1-2 | Full arc each |
    | 3-5 | Brief setup, focus on payoff |
    | 5+ | Pick top 3, mention rest |
    

---
  #### **Name**
The Safety Net
  #### **Description**
Preparing for demo failures
  #### **When To Use**
Before any live demo
  #### **Implementation**
    ## Demo Insurance
    
    ### 1. The Demo Environment
    
    ```
    NEVER demo on:
    - Production (can break)
    - Shared dev (others' changes)
    - Your local (machine issues)
    
    ALWAYS demo on:
    - Dedicated demo environment
    - Known good state
    - Pre-tested data
    ```
    
    ### 2. Backup Layers
    
    | Layer | Backup |
    |-------|--------|
    | Live demo | Recorded video |
    | Network calls | Cached responses |
    | Database | Pre-seeded data |
    | Environment | Screenshots |
    
    ### 3. Pre-Demo Checklist
    
    ```
    □ Run full demo twice successfully
    □ Test on presentation machine
    □ Check network/VPN
    □ Clear notifications
    □ Close unrelated tabs
    □ Have backup ready
    □ Know the failure pivot
    ```
    
    ### 4. The Failure Pivot
    
    | When... | Say... | Do... |
    |---------|--------|-------|
    | Loading slow | "While this loads, let me explain..." | Talk through the value |
    | Error appears | "Interesting! Let me show you another way..." | Switch to backup |
    | Complete fail | "Here's a recording from earlier..." | Play video backup |
    

---
  #### **Name**
Audience Translation
  #### **Description**
Adapting demos for different audiences
  #### **When To Use**
When presenting to non-technical stakeholders
  #### **Implementation**
    ## Speaking Their Language
    
    ### 1. Audience Types
    
    | Audience | Care About | Avoid |
    |----------|------------|-------|
    | Executives | Business impact | Technical details |
    | Product | User experience | Code complexity |
    | Sales | Demo-ability | Edge cases |
    | Engineers | How it works | Simplification |
    
    ### 2. Translation Table
    
    | Technical | Executive Version |
    |-----------|-------------------|
    | "Reduced latency by 200ms" | "Feels instant now" |
    | "Refactored the auth system" | "Login is now reliable" |
    | "Implemented caching layer" | "Pages load in half the time" |
    | "Fixed race condition" | "No more weird errors" |
    
    ### 3. The "So What" Test
    
    ```
    For every feature:
    
    "We built X"
    "So what?"
    "It means Y for users"
    "So what?"
    "It saves/makes/enables Z"
    
    Present Z, mention X.
    ```
    
    ### 4. Visual Emphasis
    
    | Show | Don't Show |
    |------|------------|
    | Before/after | Code diffs |
    | User flow | Architecture |
    | Metrics improved | Technical logs |
    | Happy path | Edge cases |
    

---
  #### **Name**
Making Work Visible
  #### **Description**
Showing progress when nothing is demoable
  #### **When To Use**
Infrastructure, refactoring, foundational work
  #### **Implementation**
    ## Invisible Work Made Visible
    
    ### 1. The Iceberg Problem
    
    ```
    What stakeholders see:
    ┌───────────────────┐
    │ Features (10%)    │  ← "What did you do?"
    ├───────────────────┤
    │ Infrastructure    │
    │ Testing           │
    │ Security          │  ← 90% of work
    │ Performance       │
    │ Refactoring       │
    └───────────────────┘
    ```
    
    ### 2. Visualization Techniques
    
    | Invisible Work | Make Visible |
    |----------------|--------------|
    | Performance | Before/after graphs |
    | Reliability | Uptime metrics |
    | Technical debt | Deployment frequency |
    | Refactoring | Code coverage change |
    | Security | Vulnerability count |
    
    ### 3. The Proxy Demo
    
    ```
    CAN'T DEMO THE WORK?
    Demo the EFFECT:
    
    "We refactored auth"
    → Demo: "Adding login took 1 day instead of 2 weeks"
    
    "We improved infrastructure"
    → Demo: "Deploy went from 30min to 3min"
    ```
    
    ### 4. Progress Artifacts
    
    | Artifact | Shows |
    |----------|-------|
    | Dashboard | Health metrics |
    | Diagram | Architecture improvement |
    | Timeline | Delivery velocity |
    | Comparison | Before/after |
    

## Anti-Patterns


---
  #### **Name**
The Feature Dump
  #### **Description**
Showing everything without narrative
  #### **Why Bad**
    Overwhelming.
    Nothing stands out.
    Forgotten immediately.
    
  #### **What To Do Instead**
    Pick 3 things.
    Tell a story.
    Make them memorable.
    

---
  #### **Name**
The Technical Deep Dive
  #### **Description**
Explaining implementation to executives
  #### **Why Bad**
    Wrong audience.
    Loses attention.
    Misses impact.
    
  #### **What To Do Instead**
    Translate to outcomes.
    Show, don't explain.
    Focus on value.
    

---
  #### **Name**
The Live Coding Demo
  #### **Description**
Writing code during a demo
  #### **Why Bad**
    High risk.
    Slow for audience.
    Typos = embarrassment.
    
  #### **What To Do Instead**
    Pre-record if needed.
    Have code ready.
    Demo the result.
    