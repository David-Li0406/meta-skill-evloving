# Documentation That Slaps - Sharp Edges

## Docs Rot

### **Id**
docs-rot
### **Summary**
Documentation becomes outdated and wrong
### **Severity**
high
### **Situation**
Docs say one thing, code does another
### **Why**
  Docs not updated with code.
  No ownership.
  No review process.
  
### **Solution**
  ## Preventing Doc Rot
  
  ### The Coupling Problem
  
  ```
  Code changes → Docs stay same → Docs lie
  
  BAD:
  Docs live separately from code.
  Updating is "someone else's job."
  No one notices when they diverge.
  ```
  
  ### Solutions
  
  | Strategy | How |
  |----------|-----|
  | Docs-as-code | Docs in same repo as code |
  | PR checklist | "Did you update docs?" |
  | Doc tests | Code examples that run |
  | Ownership | Named maintainer for docs |
  
  ### The Freshness Check
  
  ```markdown
  Add to every doc:
  
  ---
  Last verified: 2024-01-15
  Verified by: @username
  ---
  
  Set calendar reminder to verify quarterly.
  Delete if no one verifies.
  ```
  
  ### Doc Test Pattern
  
  ```javascript
  // In tests/docs.test.js
  // Test every code example in README
  
  test('README quick start works', () => {
    // Copy-paste from README
    const result = doTheThing();
    expect(result).toBe('expected');
  });
  ```
  
  ### Ruthless Deletion
  
  | If doc is... | Action |
  |--------------|--------|
  | > 6 months unverified | Review or delete |
  | Contradicts code | Fix or delete |
  | Never accessed | Consider deleting |
  | Duplicated elsewhere | Delete one |
  
### **Symptoms**
  - The docs are wrong
  - Ignore the wiki
  - Ask [person] instead
  - Outdated screenshots
### **Detection Pattern**
docs are wrong|outdated|don't trust

## Write Only Docs

### **Id**
write-only-docs
### **Summary**
Docs written but never read
### **Severity**
medium
### **Situation**
Lots of documentation that no one uses
### **Why**
  Written for completion, not users.
  No user research.
  Wrong format or location.
  
### **Solution**
  ## Docs People Actually Read
  
  ### The Usage Test
  
  ```
  BEFORE writing docs, ask:
  
  - Who will read this?
  - When will they need it?
  - How will they find it?
  - What will they do with it?
  
  If no clear answers → don't write it.
  ```
  
  ### User Research for Docs
  
  | Method | How |
  |--------|-----|
  | Watch onboarding | What do they search for? |
  | Support tickets | What questions repeat? |
  | Analytics | What pages get traffic? |
  | Ask directly | "Did docs help?" |
  
  ### Location Strategy
  
  | Doc Type | Location |
  |----------|----------|
  | Getting started | README (top) |
  | API reference | Near the code |
  | Troubleshooting | Error messages link to it |
  | How-to guides | Search-optimized titles |
  
  ### The Right Format
  
  ```
  DECISION MAKING:
  → Short doc with bullet points
  
  LEARNING:
  → Tutorial with examples
  
  REFERENCE:
  → Searchable, structured, complete
  
  TROUBLESHOOTING:
  → Error code indexed, solutions first
  ```
  
  ### Kill Metrics
  
  | Signal | Action |
  |--------|--------|
  | Zero visits | Delete or move |
  | High bounce | Improve content |
  | Long time | Too complex |
  | Support still asked | Missing info |
  
### **Symptoms**
  - Thousands of pages, low traffic
  - Same questions in Slack
  - "Did you check the docs?" / "Where?"
  - Beautiful docs no one sees
### **Detection Pattern**
where is|can't find|is there docs

## Over Documentation

### **Id**
over-documentation
### **Summary**
Documentation becomes maintenance burden
### **Severity**
medium
### **Situation**
So much docs that keeping them current is impossible
### **Why**
  "Document everything" culture.
  No prioritization.
  Docs debt compounds.
  
### **Solution**
  ## Right-Sized Documentation
  
  ### The Minimum Viable Doc
  
  ```
  MUST HAVE:
  - README with quick start
  - How to contribute
  - Where to get help
  
  NICE TO HAVE:
  - Tutorials
  - Architecture overview
  - ADRs
  
  PROBABLY DON'T NEED:
  - Documenting obvious code
  - Redundant with type system
  - Internal implementation details
  ```
  
  ### The Cost-Benefit Check
  
  | Question | If no clear answer... |
  |----------|----------------------|
  | Who needs this? | Don't write it |
  | How often used? | Consider deleting |
  | Who maintains it? | Don't write it |
  
  ### Docs Budget
  
  ```
  Treat docs like features:
  
  - Time to write = investment
  - Time to maintain = ongoing cost
  - Outdated docs = negative value
  
  Budget accordingly.
  ```
  
  ### The Link-Don't-Write Rule
  
  | Instead of... | Do this |
  |---------------|---------|
  | Copying content | Link to source |
  | Explaining library | Link to their docs |
  | Repeating info | Single source of truth |
  
### **Symptoms**
  - Too much to maintain
  - Duplicated information
  - Wiki sprawl
  - Outdated everywhere
### **Detection Pattern**
too many|where is the|which is right

## Expertise Curse

### **Id**
expertise-curse
### **Summary**
Docs assume reader knows too much
### **Severity**
medium
### **Situation**
Experts write docs beginners can't understand
### **Why**
  Writer forgot being a beginner.
  Assumed knowledge not stated.
  Jargon everywhere.
  
### **Solution**
  ## Writing for Fresh Eyes
  
  ### The Beginner Test
  
  ```
  For every doc, ask:
  
  "Would I understand this on day 1?"
  
  If not, you're missing:
  - Context
  - Prerequisites
  - Definitions
  - Links to learn more
  ```
  
  ### Assumed Knowledge Box
  
  ```markdown
  ## Prerequisites
  
  Before starting, you should know:
  - Basic JavaScript (functions, objects)
  - npm/yarn package management
  - Command line basics
  
  New to these? Start with [link].
  ```
  
  ### Jargon Handling
  
  | Strategy | Example |
  |----------|---------|
  | Define on first use | "The ORM (Object-Relational Mapper) handles..." |
  | Link to glossary | "Configure the [webhook](#glossary-webhook)" |
  | Avoid if possible | "The database connector" vs "The ORM" |
  
  ### Fresh Eyes Review
  
  ```
  BEFORE publishing:
  
  1. Have a new team member read it
  2. Watch them try to follow it
  3. Note where they get stuck
  4. Fix those parts
  
  If no new person available:
  Wait a week, read it yourself.
  ```
  
  ### Progressive Disclosure
  
  | Level | Content |
  |-------|---------|
  | 1. Quick Start | Minimum to get going |
  | 2. Basic Usage | Common scenarios |
  | 3. Deep Dive | Explain the why |
  | 4. Advanced | Edge cases, internals |
  
### **Symptoms**
  - I don't understand this
  - Questions about basics
  - High bounce rate on docs
  - What does X mean?
### **Detection Pattern**
what is|don't understand|confused