# Code Review Diplomacy - Sharp Edges

## Toxic Reviewer

### **Id**
toxic-reviewer
### **Summary**
Review behavior that damages team trust
### **Severity**
high
### **Situation**
Reviewer consistently demoralizing others
### **Why**
  Ego-driven feedback.
  Power dynamics abused.
  No empathy for author.
  
### **Solution**
  ## Addressing Toxic Review Behavior
  
  ### Warning Signs
  
  | Behavior | Impact |
  |----------|--------|
  | "Obviously wrong" | Shames author |
  | Public corrections | Humiliates |
  | Personal attacks | Destroys trust |
  | Blocking without reason | Power play |
  | Never approves | Gatekeeping |
  
  ### If You're the Reviewer
  
  ```
  ASK YOURSELF:
  
  - Would I say this in person?
  - Am I helping or judging?
  - Is this about the code or the person?
  - Would I want this comment on my PR?
  ```
  
  ### If You're the Author
  
  | Situation | Response |
  |-----------|----------|
  | Harsh comment | "Can you help me understand what you'd suggest?" |
  | Personal attack | "Let's focus on the code" |
  | Pattern behavior | Talk to manager privately |
  | Blocking unfairly | Escalate to tech lead |
  
  ### If You're a Manager
  
  ```
  INTERVENTION STEPS:
  
  1. Review the review history
  2. Private conversation
  3. Specific examples
  4. Clear expectations
  5. Follow up on changes
  ```
  
  ### Team-Level Fixes
  
  | Fix | How |
  |-----|-----|
  | Review training | Teach empathetic feedback |
  | Comment templates | Provide good examples |
  | Anonymized reviews | Where appropriate |
  | Feedback on feedback | Review the reviews |
  
### **Symptoms**
  - People avoid asking for reviews
  - PRs sit waiting
  - Low morale after reviews
  - Fear of opening PRs
### **Detection Pattern**
harsh|brutal|afraid to|don't want to

## Review Avoidance

### **Id**
review-avoidance
### **Summary**
Team avoiding code review entirely
### **Severity**
high
### **Situation**
Reviews seen as obstacle, not value
### **Why**
  Reviews too slow.
  Process too painful.
  Value not understood.
  
### **Solution**
  ## Reviving Review Culture
  
  ### Diagnosis
  
  | Symptom | Root Cause |
  |---------|------------|
  | PRs merged unreviewed | Pressure > process |
  | Minimal comments | Nobody cares |
  | Days to review | No SLA, not prioritized |
  | Rubber stamps | Going through motions |
  
  ### Quick Wins
  
  ```
  1. REVIEW SLA
     "All PRs get first look in 4 hours"
  
  2. SMALLER PRs
     "Max 400 lines changed"
  
  3. PR ROULETTE
     Automate reviewer assignment
  
  4. REVIEW TIME
     Block calendar for reviews
  ```
  
  ### Making Review Valuable
  
  | Show Value By | How |
  |---------------|-----|
  | Catching bugs | Track bugs caught in review |
  | Teaching | Juniors learn from feedback |
  | Sharing knowledge | Spread context |
  | Improving quality | Metric improvements |
  
  ### Culture Shift
  
  ```
  OLD MINDSET:
  "Review is a gate to pass"
  
  NEW MINDSET:
  "Review is where we learn together"
  
  REINFORCE BY:
  - Praising good reviews
  - Celebrating catches
  - Rotating reviewers
  - Making it fast
  ```
  
### **Symptoms**
  - Self-merging
  - Can you just approve
  - Reviews seen as waste
  - LGTM without looking
### **Detection Pattern**
just merge|skip review|takes too long

## Bikeshedding

### **Id**
bikeshedding
### **Summary**
Spending review time on trivial issues
### **Severity**
medium
### **Situation**
Big issues ignored while style debated
### **Why**
  Easy to have opinions on style.
  Hard to catch real bugs.
  No priority guidance.
  
### **Solution**
  ## Focusing Review on What Matters
  
  ### The Bikeshed Problem
  
  ```
  WHAT HAPPENS:
  20 comments on variable names
  0 comments on the race condition
  
  WHY:
  - Style is easy to see
  - Bugs are hard to find
  - Opinions on style are cheap
  ```
  
  ### Review Priority Ladder
  
  | Priority | Focus Area |
  |----------|------------|
  | 1. Critical | Security, data loss, crashes |
  | 2. Important | Logic errors, edge cases |
  | 3. Moderate | Performance, maintainability |
  | 4. Minor | Style, naming, formatting |
  
  ### Process Fixes
  
  | Problem | Solution |
  |---------|----------|
  | Style debates | Auto-formatter (Prettier, etc.) |
  | Naming debates | Conventions doc |
  | Trivial comments | Use [nit] prefix |
  | Missing priorities | Review checklist |
  
  ### The Checklist Approach
  
  ```markdown
  ## Review Checklist
  
  Before commenting on style, verify:
  
  - [ ] No security issues
  - [ ] No data corruption risk
  - [ ] Error handling exists
  - [ ] Tests cover new code
  - [ ] No obvious bugs
  
  THEN worry about naming.
  ```
  
  ### Comment Quota
  
  ```
  RULE OF THUMB:
  
  For every [nit], require yourself to:
  - Look for one actual bug
  - Or leave one genuine praise
  
  Keeps focus on what matters.
  ```
  
### **Symptoms**
  - 50 comments, all style
  - Production bugs post-merge
  - Reviews take forever on trivial
  - Author frustration
### **Detection Pattern**
should rename|formatting|style|whitespace

## Knowledge Gatekeeping

### **Id**
knowledge-gatekeeping
### **Summary**
Using reviews to assert dominance
### **Severity**
high
### **Situation**
Senior devs weaponizing review
### **Why**
  Ego protection.
  Power dynamics.
  Fear of being replaced.
  
### **Solution**
  ## Inclusive Review Culture
  
  ### Gatekeeping Signs
  
  | Behavior | Translation |
  |----------|-------------|
  | "You should know this" | Making you feel small |
  | "Just do it my way" | Refusing to explain |
  | Always finding issues | Perfectionism as control |
  | Rejecting new patterns | Resisting change |
  
  ### Healthy Senior Behavior
  
  ```
  INSTEAD OF:             DO:
  "Wrong"                 "Have you considered X?"
  "Always do it this way" "We typically do X because Y"
  "Should know this"      "Here's a good resource"
  Blocking                Explaining, teaching
  ```
  
  ### For Authors
  
  | When facing... | Try |
  |----------------|-----|
  | No explanation | "Can you help me understand why?" |
  | "Just do it" | "I'd like to learn the reasoning" |
  | Consistent blocks | Document and escalate |
  
  ### For Teams
  
  | Fix | How |
  |-----|-----|
  | Rotate reviewers | No single gatekeeper |
  | Junior reviewers | Everyone's feedback valued |
  | Written standards | Not in one person's head |
  | Anonymous feedback | On review quality |
  
### **Symptoms**
  - One person always blocks
  - Fear of certain reviewers
  - Knowledge hoarding
  - Only X understands this
### **Detection Pattern**
only I|you should know|just do it|always block