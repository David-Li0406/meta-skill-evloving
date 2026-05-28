# Code Review

## Patterns


---
  #### **Name**
Actionable Feedback
  #### **Description**
Every review comment provides specific, implementable guidance
  #### **When**
Giving any feedback that requires author action
  #### **Example**
    BAD:
    "This is confusing"
    
    GOOD:
    "Consider renaming 'data' to 'userData' to clarify what this
    variable contains. The current name makes line 45 hard to understand."
    
    Template:
    What: [Specific line/file]
    Why: [The problem this causes]
    How: [Suggested fix or direction]
    

---
  #### **Name**
Comment Hierarchy
  #### **Description**
Prioritize and label comments by importance
  #### **When**
PR has multiple issues of varying severity
  #### **Example**
    Comment types in priority order:
    1. BLOCKING: "Security issue - SQL injection on line 23"
    2. BUG: "This will crash if user is null"
    3. DESIGN: "This couples auth to payments - let's discuss"
    4. PERFORMANCE: "N+1 query here, consider eager loading"
    5. CLARITY: "Could use a more descriptive name"
    6. NIT: "nit: trailing comma"
    
    Label your comments so author knows what's blocking vs optional.
    

---
  #### **Name**
Constructive Language
  #### **Description**
Frame feedback to improve, not criticize
  #### **When**
Any situation where feedback could feel personal
  #### **Example**
    BAD:
    "Why would you do it this way?"
    "You always do this wrong"
    "This is obviously broken"
    
    GOOD:
    "What happens if X is null here?"
    "We could optimize this by..."
    "Have we considered the X case?"
    
    Use "we" language. Assume good intent. Ask questions.
    

---
  #### **Name**
Review Checklist
  #### **Description**
Systematic checks to ensure consistent review quality
  #### **When**
Reviewing any PR, especially security-sensitive code
  #### **Example**
    Before approving, verify:
    □ PR does what description claims
    □ Tests exist for new code
    □ CI pipeline passes
    □ No security issues (auth, injection, secrets)
    □ Error handling present
    □ Documentation updated if needed
    □ I would maintain this code
    

---
  #### **Name**
Scope Boundaries
  #### **Description**
Keep review focused on what the PR aims to change
  #### **When**
Tempted to request unrelated improvements
  #### **Example**
    PR: "Fix login button alignment"
    
    IN SCOPE:
    - CSS changes for button
    - Related styling issues noticed
    
    OUT OF SCOPE:
    - "Refactor the auth component"
    - "Add unit tests for everything"
    - "Implement dark mode"
    
    Create follow-up issues for out-of-scope improvements.
    

## Anti-Patterns


---
  #### **Name**
Drive-By Rejection
  #### **Description**
Rejecting PR without actionable feedback
  #### **Why**
Author has no idea what to fix. Review becomes guessing game. Time wasted.
  #### **Instead**
Every rejection comes with specific, actionable items to address.

---
  #### **Name**
Rubber Stamp
  #### **Description**
Approving without actually reading the code
  #### **Why**
Bugs ship, standards erode, reviews become meaningless.
  #### **Instead**
Actually read every line. Run the code if appropriate. Ask questions.

---
  #### **Name**
Nitpick Storm
  #### **Description**
Overwhelming PRs with minor style comments
  #### **Why**
Real issues buried in noise. Author frustrated by trivia.
  #### **Instead**
Automate style checks. Label nits. Limit to 2-3 per PR.

---
  #### **Name**
Personal Attacks
  #### **Description**
Criticizing the author instead of the code
  #### **Why**
Destroys trust, psychological safety, and team culture.
  #### **Instead**
"We" language. Assume good intent. Review code, not people.

---
  #### **Name**
Scope Creep
  #### **Description**
Requesting changes unrelated to PR's purpose
  #### **Why**
PRs never merge, authors burn out, momentum dies.
  #### **Instead**
Evaluate against stated purpose. File issues for other improvements.

---
  #### **Name**
Approval Hostage
  #### **Description**
Blocking for personal preferences, not actual issues
  #### **Why**
Personal taste becomes law, velocity dies.
  #### **Instead**
Distinguish blocking issues from preferences. Mark nits as non-blocking.