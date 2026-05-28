# Technical Writer - Sharp Edges

## Documentation as Approval - Writing Docs Nobody Asked For

### **Id**
documentation-as-approval
### **Severity**
medium
### **Situation**
  Developer creates extensive documentation for a feature before validating
  anyone needs it. Spends three days on beautiful API docs. Feature gets
  changed completely in review. All docs are now wrong and wasted.
  
### **Why**
  Documentation is a form of validation. If you write comprehensive docs
  before the design is stable, you're documenting a moving target. Every
  design change means doc changes. This is demoralizing and wasteful.
  
### **Solution**
  1. Match documentation depth to stability:
     - Exploratory phase: Notes only
     - Design stable, code unstable: High-level docs
     - Code stable: Detailed docs
     - Shipped: Comprehensive docs
  
  2. Documentation phases:
     - Phase 1: "We're building X that does Y" (one sentence)
     - Phase 2: "Here's how to use it" (minimal example)
     - Phase 3: "Here's the full reference" (only when stable)
  
  3. Ask before writing:
     - Is this design finalized?
     - Who will read this doc?
     - When will they need it?
  
### **Symptoms**
  - Extensive docs for unshipped features
  - Docs that need major rewrites
  - "Let me update the docs" in every PR
### **Detection Pattern**
comprehensive docs|full documentation|document everything

## Generated Docs as Done - Thinking Auto-Docs Are Sufficient

### **Id**
generated-docs-as-done
### **Severity**
high
### **Situation**
  Team sets up JSDoc/TypeDoc/Swagger generation. Beautiful reference docs
  appear automatically. Team considers documentation "done." Users still
  can't figure out how to use the API because there are no examples,
  no guides, no context.
  
### **Why**
  Generated docs answer "what exists?" but not "how do I use it?" or
  "when should I use this?" They're reference, not guidance. Reference
  without context is a dictionary - technically complete, practically useless
  for learning.
  
### **Solution**
  1. Generated docs are Level 3, not Level 1:
     - Level 1: Quick example (hand-written)
     - Level 2: Common use cases (hand-written)
     - Level 3: Reference (can be generated)
  
  2. Complement generated docs with:
     - Getting started guide
     - Common use case examples
     - Error handling guide
     - "How do I..." sections
  
  3. Minimum viable documentation:
     - Before: "We have auto-generated docs"
     - After: "We have quick start, examples, AND auto-generated reference"
  
### **Symptoms**
  - Users asking "how do I..." for documented features
  - Support questions that should be in docs
  - "It's in the API reference" as the answer to everything
### **Detection Pattern**
auto-generate|JSDoc|TypeDoc|Swagger|OpenAPI

## Docs in Wrong Place - Wiki Syndrome

### **Id**
docs-in-wrong-place
### **Severity**
medium
### **Situation**
  Team uses Confluence/Notion/Wiki for documentation. Code changes.
  Wiki doesn't. Six months later, wiki describes a system that no longer
  exists. Nobody knows which docs are current. New developers follow
  outdated instructions and break things.
  
### **Why**
  Documentation separated from code has no forcing function for updates.
  Code PRs don't touch wiki. Wikis don't have version control that matches
  code versions. The further docs are from code, the faster they drift.
  
### **Solution**
  1. Docs that MUST be in repo:
     - README
     - API reference
     - Configuration reference
     - Getting started
     - ADRs
  
  2. Docs that CAN be in wiki:
     - Team processes
     - Meeting notes
     - Planning documents
     - Onboarding checklists
  
  3. The rule:
     - If it describes code behavior → repo
     - If it describes people/process → wiki
  
  4. Link, don't duplicate:
     - Wiki can link to repo docs
     - Don't copy repo docs to wiki
  
### **Symptoms**
  - "Check the wiki" for technical questions
  - Wiki pages with conflicting information
  - Which doc is correct?
### **Detection Pattern**
confluence|notion|wiki|documentation site

## Screenshot-Heavy Docs - The Maintenance Nightmare

### **Id**
screenshot-heavy-docs
### **Severity**
medium
### **Situation**
  Tutorial includes 30 screenshots showing every button click. UI gets
  redesigned. All 30 screenshots are now wrong. Updating them takes a
  full day. So they don't get updated. Users see screenshots that don't
  match their screen and get confused.
  
### **Why**
  Screenshots are expensive to maintain. Every UI change requires new
  screenshots. They don't diff well in version control. They're not
  searchable. And slight differences between user's screen and screenshot
  cause confusion ("My button is in a different place?").
  
### **Solution**
  1. Minimize screenshots:
     - Use text descriptions when possible
     - Screenshots only for non-obvious UI
     - Never screenshot text (copy the text instead)
  
  2. When you must screenshot:
     - Crop tightly to relevant area
     - Annotate what to look at
     - Use consistent styling/branding (so users know it's intentionally old)
  
  3. Alternatives to screenshots:
     - Code snippets (for developer docs)
     - ASCII diagrams (for architecture)
     - Mermaid/PlantUML (version-controllable)
  
  4. If screenshots are essential:
     - Automate screenshot capture
     - Include screenshot generation in CI
     - Date-stamp screenshots
  
### **Symptoms**
  - That screenshot is outdated
  - Docs with obviously old UI
  - Users can't follow tutorial
### **Detection Pattern**
screenshot|image|png|jpg|gif

## Documenting Internal Code - Wasted Effort

### **Id**
documenting-internal-code
### **Severity**
low
### **Situation**
  Developer documents every internal function, private method, and utility.
  Creates comprehensive JSDoc for code only their team will ever touch.
  Spends hours on documentation that provides no value beyond what the
  code already says.
  
### **Why**
  Internal code documentation has a tiny audience (your team) who can read
  the code directly. The ROI is negative - time spent documenting exceeds
  time saved reading docs. Good code is self-documenting; bad code needs
  refactoring, not comments.
  
### **Solution**
  1. Documentation priority:
     - Public APIs: Comprehensive
     - Exported modules: Moderate
     - Internal utilities: Minimal
     - Private functions: Almost never
  
  2. What to document internally:
     - Non-obvious algorithms
     - Business logic with context
     - Workarounds and why they exist
     - Gotchas for future maintainers
  
  3. The test:
     - "Would someone outside the team need this?" → Document
     - "Could a team member read the code in 5 minutes?" → Don't document
  
### **Symptoms**
  - Every function has JSDoc
  - Comments longer than code
  - Documentation for obvious code
### **Detection Pattern**
@param|@returns|@private|internal documentation

## No Version Matching - Docs for Which Version?

### **Id**
no-version-matching
### **Severity**
high
### **Situation**
  Library is at v3.0. Documentation shows v2.0 examples. User follows docs,
  gets cryptic errors. Spends hour debugging before realizing docs are for
  old version. Trust in documentation permanently damaged.
  
### **Why**
  When docs don't match code version, they become dangerous. Users can't
  tell if an example will work. They don't know if behavior changed.
  The documentation that should help becomes a source of confusion.
  
### **Solution**
  1. Version your documentation:
     - URL includes version: /docs/v3/getting-started
     - Docs site has version switcher
     - Each version is a snapshot
  
  2. In-code solutions:
     - Docs in repo match that commit
     - README shows which version it documents
     - Example code is tested against that version
  
  3. Minimum viable versioning:
     - Top of README: "Documentation for v3.x"
     - Breaking changes: Explicit migration guide
     - Old docs: Still accessible (archived)
  
  4. For tutorials:
     - Pin all dependency versions
     - Test tutorial on fresh environment
     - Date the tutorial
  
### **Symptoms**
  - This worked in the old version
  - Users on wrong version following docs
  - Migration guides missing
### **Detection Pattern**
version|v[0-9]+|outdated|deprecated

## Assuming Context - The Expert Blind Spot

### **Id**
assuming-context
### **Severity**
high
### **Situation**
  Documentation assumes reader knows things they don't. "Configure the
  authentication middleware" - but reader doesn't know what middleware is
  or where it goes. "Set the API key" - but where? In what format? Every
  step has implicit prerequisites that the writer takes for granted.
  
### **Why**
  Writers are experts in their own code. They forgot what it was like not
  to know. Every "obvious" step is actually learned knowledge. When you
  assume context, you exclude exactly the people who need the docs most:
  newcomers.
  
### **Solution**
  1. The newcomer test:
     - Have someone unfamiliar try your docs
     - Watch where they get stuck
     - Those stuck points are missing context
  
  2. Explicit prerequisites:
     """
     ## Prerequisites
     - Node.js 18+ installed
     - npm or yarn package manager
     - Basic familiarity with Express.js
     - A Stripe account (free tier works)
     """
  
  3. First use gets full detail:
     """
     ## First time: Full setup
     1. Create config file at `src/config/auth.ts`
     2. Add the following code: [...]
  
     ## After first time: Quick reference
     Authentication config is in `src/config/auth.ts`
     """
  
  4. Link to prerequisites:
     - Don't re-explain Express
     - Do link to Express docs
     - Do explain your specific usage
  
### **Symptoms**
  - Users stuck on "obvious" steps
  - I did exactly what the docs said
  - Support questions about prerequisites
### **Detection Pattern**
configure|set up|install|add

## Marketing in Tech Docs - Wrong Audience

### **Id**
marketing-in-tech-docs
### **Severity**
medium
### **Situation**
  Technical documentation includes marketing language. "Our revolutionary
  API..." "Unlike competitors..." "Best-in-class performance..." Developer
  just wants to know how to make an API call. Marketing language signals
  the docs aren't for them.
  
### **Why**
  Technical docs and marketing have different audiences. Marketing convinces
  people to try. Docs help people use. Mixing them undermines both. Developers
  find marketing language cringe-worthy and lose trust in the technical content.
  
### **Solution**
  1. Separate marketing from docs:
     - Landing page: Marketing
     - /docs: Technical only
     - Blog: Can mix (but label clearly)
  
  2. Remove from technical docs:
     - Superlatives ("best", "fastest", "revolutionary")
     - Competitor comparisons
     - Vague benefits ("powerful", "flexible")
     - Sales language ("unlock", "leverage", "transform")
  
  3. Keep in technical docs:
     - What it does (factually)
     - How to use it (practically)
     - When to use it (honestly, including limitations)
  
  4. The test:
     - Read your docs as if you're already sold
     - Does every sentence help you USE the product?
     - Delete sentences that only SELL the product
  
### **Symptoms**
  - "Best-in-class" in API docs
  - Feature comparisons in tutorials
  - Vague benefits without examples
### **Detection Pattern**
best|leading|powerful|revolutionary|unlike|better than

## No Troubleshooting - Happy Path Only

### **Id**
no-troubleshooting
### **Severity**
high
### **Situation**
  Documentation shows the perfect path: do A, then B, then C, done!
  But user gets an error at step B. Nothing in docs about errors.
  They search GitHub issues, Stack Overflow, spend an hour on a problem
  that the team knows about and could have documented in 2 minutes.
  
### **Why**
  Real usage isn't the happy path. Users hit errors, edge cases, conflicts.
  Docs that only cover success leave users stranded exactly when they need
  help most. The knowledge exists in support tickets and GitHub issues -
  it just hasn't made it to docs.
  
### **Solution**
  1. Common errors section:
     """
     ## Troubleshooting
  
     ### "Connection refused" error
     **Cause:** Database not running
     **Fix:** Start PostgreSQL with `brew services start postgresql`
  
     ### "Invalid token" error
     **Cause:** API key expired or wrong format
     **Fix:** Generate new key at dashboard.example.com/keys
     """
  
  2. Sources for troubleshooting content:
     - Support tickets (recurring issues)
     - GitHub issues (common reports)
     - Stack Overflow (your tag)
     - Team knowledge (ask: "what trips people up?")
  
  3. Error messages should point to docs:
     - Include doc links in error messages
     - "See docs.example.com/errors/auth-failed for details"
  
  4. Proactive troubleshooting:
     - Prerequisites: "Check these before starting"
     - After each step: "If you see X, do Y"
  
### **Symptoms**
  - Same support questions repeatedly
  - GitHub issues asking about documented features
  - "Works for me" vs user errors
### **Detection Pattern**
error|troubleshoot|common issues|FAQ