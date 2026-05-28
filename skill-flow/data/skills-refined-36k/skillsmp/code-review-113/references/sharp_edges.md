# Code Review - Sharp Edges

## Drive By Rejection

### **Id**
drive-by-rejection
### **Summary**
Reviewer leaves "Needs work" without actionable feedback
### **Severity**
critical
### **Situation**
PR rejected with vague comments like "This doesn't look right"
### **Why**
  Author has no idea what to fix. Review becomes a guessing game. Time wasted
  on back-and-forth. Resentment builds. Author makes random changes hoping
  to please the reviewer.
  
### **Solution**
  # Every comment must be actionable
  BAD: "This is confusing"
  GOOD: "Consider renaming 'data' to 'userData' to clarify what this contains"
  
  # Point to specific lines
  BAD: "The error handling needs work"
  GOOD: "Line 45: This catch block swallows the error. Consider logging it."
  
  # Explain why, not just what
  BAD: "Use const instead of let"
  GOOD: "Use const here—the value is never reassigned, and const signals intent"
  
  # Actionable feedback template
  What: [Specific line/file]
  Why: [The problem this causes]
  How: [Suggested fix or direction]
  
  # If you can't articulate the issue, maybe there isn't one
  
### **Symptoms**
  - Vague rejection comments
  - Multiple revision cycles
  - Author frustration
  - PRs sitting open for days
### **Detection Pattern**


## Rubber Stamp Approval

### **Id**
rubber-stamp-approval
### **Summary**
Approving PRs without actually reading the code
### **Severity**
critical
### **Situation**
Reviewer approves without examining the diff or understanding changes
### **Why**
  Bugs ship. Standards erode. Reviews become meaningless. Security vulnerabilities
  get deployed. Team learns that reviews don't matter.
  
### **Solution**
  # Actually read the diff
  Every file, every line
  If PR is too big, request split
  
  # Run the code when appropriate
  Checkout the branch
  Test the feature manually
  Verify it works as described
  
  # Ask questions if unclear
  "How does this handle X case?"
  Shows you read it
  
  # If you don't have time, say so
  "I can't review this properly right now.
  Can someone else take it?"
  
  # Approval means:
  - I read and understood the code
  - I believe it does what it claims
  - I would maintain this code
  - I'm comfortable if this ships
  
  If any are false, don't approve.
  
### **Symptoms**
  - Quick approvals without comments
  - Bugs found after merge
  - No questions asked
  - Reviewer doesn't understand changes
### **Detection Pattern**


## Nitpick Storm

### **Id**
nitpick-storm
### **Summary**
Overwhelming PRs with minor style comments while missing real issues
### **Severity**
high
### **Situation**
Review has dozens of formatting/style comments but misses bugs
### **Why**
  Author drowns in trivia. Real problems slip through. Signal lost in noise.
  Team frustrated with review process. Important issues get buried.
  
### **Solution**
  # Automate style checking
  ESLint, Prettier, rubocop
  Don't manually enforce what tools catch
  
  # Label nitpicks as nitpicks
  "nit: trailing comma"
  Author knows it's low priority
  
  # Separate blocking from non-blocking
  BLOCKING: "This will crash in production"
  NON-BLOCKING: "Consider a clearer name"
  
  # Limit nitpicks per review
  Max 2-3 style comments per PR
  More than that = tooling problem
  
  # Comment hierarchy
  1. Security issues (must fix)
  2. Bugs (must fix)
  3. Design problems (should discuss)
  4. Performance (should fix)
  5. Clarity (could improve)
  6. Style (nit)
  
### **Symptoms**
  - Many style comments
  - Few substantive comments
  - Security issues missed
  - Long review cycles over formatting
### **Detection Pattern**


## Personal Attack

### **Id**
personal-attack
### **Summary**
Criticizing the author instead of the code
### **Severity**
critical
### **Situation**
Review comments attack the developer personally
### **Why**
  Destroys trust, psychological safety, and team culture. Developer feels attacked,
  becomes defensive, stops asking for feedback, hides mistakes, or leaves the team.
  
### **Solution**
  # Review the code, not the coder
  BAD: "You always do this wrong"
  GOOD: "This pattern has issues because..."
  
  # Use "we" language
  BAD: "Your code is inefficient"
  GOOD: "We could optimize this by..."
  
  # Assume good intent
  BAD: "Why didn't you handle this?"
  GOOD: "Did we consider the X case here?"
  
  # Ask questions, don't accuse
  BAD: "This will break everything"
  GOOD: "What happens if X is null?"
  
  # Toxic patterns to avoid:
  - Sarcasm
  - "Obviously" / "Clearly"
  - Question marks as accusations
  - Comparing to other developers
  - Bringing up past mistakes
  
### **Symptoms**
  - Defensive responses
  - Escalating tensions
  - Developer turnover
  - Review avoidance
### **Detection Pattern**
why would you|obviously|clearly you|always do this

## Scope Creep Demand

### **Id**
scope-creep-demand
### **Summary**
Requesting changes unrelated to the PR's purpose
### **Severity**
high
### **Situation**
Reviewer asks for refactoring/features outside PR scope
### **Why**
  PRs never merge. Authors burn out. Momentum dies. A simple 10-line fix becomes
  a multi-week project. Code review becomes dreaded.
  
### **Solution**
  # Evaluate against stated purpose
  Does PR do what it claims?
  If yes, that's enough.
  
  # Create follow-up issues
  "This is fine as-is. Created issue #456 for the refactoring."
  
  # Separate "must have" from "nice to have"
  Must have: Works correctly
  Nice to have: File issue for later
  
  # Resist "while you're in here"
  Different concerns = different PRs
  Cleaner history, easier reverts
  
  # Scope check
  Original PR scope: [X]
  Requested addition: [Y]
  Is Y required for X to work? No → Separate issue
  
  "Leave the campsite cleaner" doesn't mean "rebuild the campground"
  
### **Symptoms**
  - PRs grow during review
  - "While you're in here" comments
  - Simple PRs take weeks
  - Author frustration
### **Detection Pattern**
while you.*here|also add|could you also|might as well

## Knowledge Gatekeeper

### **Id**
knowledge-gatekeeper
### **Summary**
Using review to prove superiority rather than improve code
### **Severity**
high
### **Situation**
Reviewer overwhelms junior with advanced patterns without explanation
### **Why**
  Juniors stop learning. Knowledge silos form. Toxic culture develops. Developer
  rewrites code 5 times without understanding why.
  
### **Solution**
  # Explain at their level
  Meet them where they are
  Build up from their understanding
  
  # Link to learning resources
  "Here's a good explanation: [link]
  Happy to pair on this if helpful."
  
  # Offer to discuss
  "This is a complex area. Want to
  jump on a call to walk through it?"
  
  # Choose battles wisely
  Not every PR needs architecture lessons
  Focus on what matters for this change
  
  # Teaching framework
  1. What's the issue? (specific)
  2. Why does it matter? (impact)
  3. What's better? (alternative)
  4. How to learn more? (resources)
  5. Need help? (offer)
  
  Goal: They can explain this to the next person.
  
### **Symptoms**
  - Jargon-heavy comments
  - No explanations offered
  - Junior confusion
  - Long revision cycles
### **Detection Pattern**


## Premature Approve

### **Id**
premature-approve
### **Summary**
Approving before CI passes or discussions resolve
### **Severity**
high
### **Situation**
PR approved while CI is red or threads are unresolved
### **Why**
  Broken code merges. Discussions cut short. Missing tests forgotten.
  Technical debt added. CI failures now in main branch.
  
### **Solution**
  # Wait for CI to pass
  Green pipeline = prerequisite
  Don't approve red builds
  
  # Resolve all threads
  Every discussion should conclude
  "Resolved" or "Won't fix" with reason
  
  # Verify test coverage
  New code needs new tests
  No tests = not done
  
  # Use "Approve with comments"
  "LGTM after CI passes"
  "Approve pending test addition"
  
  # Approval checklist
  □ CI pipeline green
  □ All discussions resolved
  □ Tests exist for new code
  □ Documentation updated if needed
  □ No security concerns
  □ I would maintain this code
  
### **Symptoms**
  - Merges with failing CI
  - Unresolved comment threads
  - Missing test coverage
  - Post-merge fixes needed
### **Detection Pattern**


## Asynch Hole

### **Id**
asynch-hole
### **Summary**
Days of comment back-and-forth when a call would resolve it
### **Severity**
high
### **Situation**
Complex discussion drags on for days in PR comments
### **Why**
  Days of comments when 10-minute call would resolve it. Context lost between
  responses. Momentum dies. Simple misunderstanding becomes week-long debate.
  
### **Solution**
  # Recognize complex discussions early
  Multiple valid approaches?
  Architecture decisions?
  → Needs real-time discussion
  
  # Suggest synchronous when needed
  "This is getting complex. Can we
  do a quick call to align?"
  
  # Document outcomes
  After call, update PR:
  "Discussed with @reviewer. Agreed
  to approach X because Y."
  
  # Set timeboxes for async
  If not resolved in 2 round-trips,
  escalate to meeting.
  
  # ASYNC (comments):
  - Clear issues with obvious fixes
  - Style and naming suggestions
  - Documentation requests
  
  # SYNC (call):
  - Design disagreements
  - Multiple valid approaches
  - Complex explanations
  - Repeated back-and-forth
  
### **Symptoms**
  - Week-long PR discussions
  - Multiple comment threads
  - No resolution in sight
  - Same points repeated
### **Detection Pattern**


## Context Ignorer

### **Id**
context-ignorer
### **Summary**
Reviewing code without understanding the problem it solves
### **Severity**
high
### **Situation**
Reviewer suggests changes without reading PR description
### **Why**
  Wrong feedback given. Important context missed. Author frustrated by irrelevant
  comments. Time wasted on moot points.
  
### **Solution**
  # Read description before code
  What problem does this solve?
  What approach was chosen?
  What alternatives were considered?
  
  # Understand requirements
  What are the constraints?
  Performance needs?
  Scale expectations?
  
  # Check linked issues/tickets
  Original requirements
  Discussion history
  Design decisions
  
  # Ask for context if missing
  "Can you add context about why
  this approach was chosen?"
  
  # Context checklist
  □ Read PR description
  □ Understand problem being solved
  □ Check linked issues
  □ Know constraints/requirements
  □ Understand chosen approach reasoning
  
  THEN review the code.
  
### **Symptoms**
  - Questions already answered in description
  - Irrelevant suggestions
  - Missing the point
  - Author re-explains repeatedly
### **Detection Pattern**


## Ghost Reviewer

### **Id**
ghost-reviewer
### **Summary**
Assigned as reviewer but never responds
### **Severity**
high
### **Situation**
PR waits days or weeks for review with no response
### **Why**
  PRs age. Authors blocked. Resentment builds. Context is lost. Momentum dies.
  Major changes requested after author has moved on.
  
### **Solution**
  # Set review SLAs
  Review within 24 hours (business)
  Or explicitly decline
  
  # If too busy, say so immediately
  "Can't review this week.
  Please reassign to @other"
  
  # Partial reviews > no reviews
  "Looked at auth changes (LGTM).
  Will review API changes tomorrow."
  
  # Use review request properly
  Don't accept if you can't do it
  Reassign quickly if blocked
  
  # Automate reminders
  PR older than 24h → Slack reminder
  Make aging visible
  
  # Reviewer responsibilities:
  - Respond within SLA
  - If blocked, communicate immediately
  - If need reassignment, arrange it
  - If doing later, commit to timeframe
  
  "I'll get to it" is not a commitment.
  "I'll review by EOD Thursday" is.
  
### **Symptoms**
  - PRs waiting days for review
  - No reviewer response
  - Pings ignored
  - Review requested just before merge
### **Detection Pattern**


## Approval Hostage

### **Id**
approval-hostage
### **Summary**
Blocking merge for personal preferences, not actual issues
### **Severity**
high
### **Situation**
Reviewer won't approve because they'd do it differently
### **Why**
  Personal taste becomes law. Velocity dies. Authors can't ship working code.
  Team frustrated. Good solutions blocked for arbitrary reasons.
  
### **Solution**
  # Distinguish blocking from preference
  BLOCKING: Will break, is insecure, violates standard
  PREFERENCE: I would do it differently
  
  # Mark preferences as non-blocking
  "nit: I'd prefer X, but fine either way"
  "suggestion: Consider Y, not blocking"
  
  # Accept multiple valid solutions
  Your way isn't the only way
  Working code > your preferences
  
  # BLOCKING:
  - Security vulnerability
  - Clear bugs
  - Breaks existing functionality
  - Missing requirements
  - Violates team standards
  
  # NON-BLOCKING:
  - Style preferences
  - Alternative approaches
  - Different naming
  - "I would have..."
  
  If it's not in the blocking list, don't block the merge.
  
### **Symptoms**
  - "I prefer" as blocking comment
  - Style-only rejections
  - Working code blocked
  - No standards cited
### **Detection Pattern**
I would|I prefer|I usually|my preference

## Missing Security Eye

### **Id**
missing-security-eye
### **Summary**
Reviewing code without checking for security issues
### **Severity**
critical
### **Situation**
Security vulnerabilities not caught in review
### **Why**
  Vulnerabilities ship to production. SQL injection, XSS, hardcoded credentials
  all missed because review focused only on logic and style.
  
### **Solution**
  # Security checklist per PR
  □ Input validation present
  □ Output encoding (XSS prevention)
  □ Authentication required
  □ Authorization checked
  □ No secrets in code
  □ SQL parameterized
  □ Dependencies vetted
  
  # Know OWASP Top 10
  - SQL injection
  - XSS
  - Broken authentication
  - Sensitive data exposure
  
  # Check common patterns
  User input → database? (SQL injection)
  User input → HTML output? (XSS)
  User input → system command? (command injection)
  External data → trust? (trust boundary)
  
  # Security review minimum
  □ Auth/authz on all endpoints
  □ Input validated before use
  □ No SQL string concatenation
  □ No eval() with user data
  □ No secrets in code
  □ Dependencies up to date
  □ Sensitive data handled properly
  
### **Symptoms**
  - No security comments
  - Vulnerabilities in merged code
  - Security team finds issues post-merge
  - No auth checks reviewed
### **Detection Pattern**
