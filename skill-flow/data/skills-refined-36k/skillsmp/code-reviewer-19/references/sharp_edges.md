# Code Reviewer - Sharp Edges

## Review Fatigue

### **Id**
review-fatigue
### **Summary**
Long PRs cause superficial reviews, bugs slip through
### **Severity**
high
### **Situation**
Pull request with 500+ lines of changes
### **Why**
  Human attention is limited. After 200-400 lines, review quality drops.
  Reviewer skims, misses subtle bugs. "LGTM" becomes rubber stamp.
  The worst bugs hide in large PRs because nobody looks carefully.
  
### **Solution**
  1. Set PR size guidelines:
     # Team agreement: max 400 lines per PR
  
  2. Split large features into stacked PRs:
     - PR 1: Add data model
     - PR 2: Add repository layer
     - PR 3: Add API endpoint
     - PR 4: Add UI
  
  3. Use draft PRs for early feedback:
     # Open draft before implementation is complete
     # Get architecture feedback early
  
  4. If must review large PR:
     - Take breaks between file groups
     - Review over multiple sessions
     - Focus on critical paths first
  
### **Symptoms**
  - "LGTM" on 1000-line PRs after 5 minutes
  - Bugs found in production from "reviewed" code
  - Reviewers skim instead of read
### **Detection Pattern**
lines.*changed|files.*changed|diff.*size

## Review Context Loss

### **Id**
review-context-loss
### **Summary**
Reviewer doesn't understand why code exists
### **Severity**
medium
### **Situation**
Reviewing code without reading linked issue
### **Why**
  Code is correct for the wrong problem. Reviewer checks syntax and style,
  misses that the approach doesn't solve the actual user problem.
  Ships "correct" code that doesn't work for users.
  
### **Solution**
  1. Always read the issue first:
     # Check: What problem is this solving?
     # Check: What alternatives were considered?
     # Check: Are there edge cases mentioned?
  
  2. Require good PR descriptions:
     ## Problem
     What issue does this solve?
  
     ## Solution
     How does this solve it?
  
     ## Testing
     How was this tested?
  
     ## Alternatives Considered
     What else was tried?
  
  3. Ask clarifying questions:
     "I see what this does, but I'm not sure why.
     Can you explain the use case?"
  
### **Symptoms**
  - "This does not do what I expected" after merge
  - Code works but doesn't solve the problem
  - Feature shipped but users still complain
### **Detection Pattern**
issue|ticket|context|why

## Style Wars

### **Id**
style-wars
### **Summary**
Review becomes argument about coding style
### **Severity**
medium
### **Situation**
Disagreement about naming, formatting, patterns
### **Why**
  Tabs vs spaces, camelCase vs snake_case, "if" braces.
  Hours spent arguing about preferences. PR blocked for days.
  Developer morale tanks. Both parties feel "attacked".
  
### **Solution**
  1. Automate style with formatters:
     # Black for Python, Prettier for JS
     # No human decisions on formatting
  
  2. Document team conventions:
     # CONTRIBUTING.md: "We use snake_case for functions"
     # Objective reference, not reviewer preference
  
  3. Use linters for consistency:
     # Enforce with CI, not humans
     eslint, ruff, flake8
  
  4. Agree on "suggestions not blocks":
     # Style comments are [NITPICK], never [BLOCKING]
  
  5. Accept diversity within reason:
     # If it passes lint and is readable, accept it
  
### **Symptoms**
  - PR comments are 90% about style
  - Multiple back-and-forth on naming
  - Developer frustration with review process
### **Detection Pattern**
nitpick|style|format|naming|convention

## Review As Gatekeeper

### **Id**
review-as-gatekeeper
### **Summary**
Reviewer blocks to assert authority, not improve code
### **Severity**
high
### **Situation**
One person repeatedly blocks PRs with minor issues
### **Why**
  Gatekeeper feels important. Team velocity drops. Developers avoid
  getting reviewed by them. Resentment builds. Some people quit.
  The review process becomes feared instead of valued.
  
### **Solution**
  1. Distinguish blocking from suggesting:
     [BLOCKING]: Security vulnerability, logic error
     [SUGGESTION]: Style preference, minor improvement
  
  2. Limit blocking criteria:
     # Block ONLY for: security, bugs, missing tests for critical paths
     # Everything else: suggest and approve
  
  3. Require explanation for blocks:
     # "I'm blocking because..." with concrete reason
     # Not just "I don't like this approach"
  
  4. Review the reviewer:
     # Track: time to review, block rate, comment sentiment
     # Coach reviewers who over-block
  
### **Symptoms**
  - PRs stuck for days on style comments
  - Developers avoid certain reviewers
  - "Just approve it" pressure
### **Detection Pattern**
block|request.*changes|approval

## Missing Context In Feedback

### **Id**
missing-context-in-feedback
### **Summary**
Comment says "fix this" without explaining why or how
### **Severity**
medium
### **Situation**
Leaving vague or unhelpful review comments
### **Why**
  "This is wrong" doesn't help. Developer has to guess what's wrong,
  how to fix it, and why it matters. Back-and-forth comments ensue.
  What could be one clear comment becomes a thread of 10.
  
### **Solution**
  1. Structure feedback:
     # What: "This query is missing a LIMIT clause"
     # Why: "Without LIMIT, a user with 1M memories crashes the app"
     # How: "Add LIMIT 100 here, or implement pagination"
  
  2. Show, don't tell:
     # Instead of: "Use a better approach"
     # Write: "Consider using asyncio.gather() here:
     ```python
     results = await asyncio.gather(*[fetch(id) for id in ids])
     ```"
  
  3. Offer to discuss:
     # "I'm not sure about this approach. Want to chat about it?"
  
  4. Be specific:
     # Not: "This could be improved"
     # Yes: "Line 45: This string concatenation is O(n²). Use join()."
  
### **Symptoms**
  - "What do you mean?" replies to comments
  - Multiple comment threads for one issue
  - Developers frustrated with feedback
### **Detection Pattern**
fix.*this|wrong|bad|improve

## Review Too Late

### **Id**
review-too-late
### **Summary**
Architecture feedback when code is "done"
### **Severity**
high
### **Situation**
Suggesting fundamental changes at PR stage
### **Why**
  Developer spent a week on implementation. Reviewer says "use different
  approach". Now: rewrite or ignore feedback. Either way, bad outcome.
  Early feedback is free; late feedback is expensive.
  
### **Solution**
  1. Design review before implementation:
     # Discuss approach before writing code
     # Use RFC or design doc for significant changes
  
  2. Draft PRs for early feedback:
     # Open PR early with [WIP] prefix
     # Get architecture feedback on skeleton
  
  3. Incremental reviews:
     # Review commit by commit for large changes
     # Catch issues early in the process
  
  4. Time-box architecture feedback:
     # After code is "done", only block on bugs
     # Architecture is suggestion, not block
  
### **Symptoms**
  - "Rewrite this completely" on large PRs
  - Developers feel ambushed
  - Features delayed by architecture debates
### **Detection Pattern**
rewrite|different.*approach|fundamental|architecture

## Approval Without Testing

### **Id**
approval-without-testing
### **Summary**
Approving code without verifying it works
### **Severity**
high
### **Situation**
Approving based on code reading alone
### **Why**
  Code looks correct but doesn't work. Edge case not handled.
  Tests exist but don't test the actual behavior. Bug ships.
  "I approved it because the code looked fine."
  
### **Solution**
  1. Pull and run for risky changes:
     git fetch origin pr/123
     git checkout pr/123
     npm test
     # Try the feature locally
  
  2. Check CI status before approving:
     # Never approve with failing CI
  
  3. Review tests, not just code:
     # Do tests cover the change?
     # Are edge cases tested?
     # Can I break this test and it still passes?
  
  4. Ask for proof:
     # "Can you add a screenshot of this working?"
     # "Can you share test output?"
  
### **Symptoms**
  - Bugs in code that was "approved"
  - Tests pass but feature broken
  - I thought that was tested
### **Detection Pattern**
CI|test.*pass|verified|tested