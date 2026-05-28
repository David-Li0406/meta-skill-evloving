# Legacy Archaeology

## Patterns


---
  #### **Name**
The Archaeological Dig
  #### **Description**
Systematic approach to understanding legacy code
  #### **When To Use**
First encountering an unknown codebase
  #### **Implementation**
    ## Archaeological Dig Process
    
    ### 1. Survey Phase (Day 1)
    
    ```
    DON'T read code yet. Gather context:
    
    □ README (even if outdated)
    □ Deployment config (what runs where)
    □ Database schema (the truth)
    □ Environment variables (integration points)
    □ Dependencies (package.json, etc.)
    ```
    
    | Artifact | Reveals |
    |----------|---------|
    | Package versions | When last updated |
    | Config files | What services connect |
    | Database schema | True data model |
    | Test files | Actual behavior |
    
    ### 2. Excavation Phase (Week 1)
    
    ```
    ENTRY POINTS:
    
    1. Start from HTTP routes / CLI commands
    2. Follow the happy path first
    3. Note patterns, don't judge yet
    4. Map what calls what
    ```
    
    | Technique | Tool |
    |-----------|------|
    | Call graph | IDE "Find References" |
    | Data flow | Follow variables |
    | Entry points | Routes, main(), handlers |
    
    ### 3. Documentation Phase (Ongoing)
    
    ```
    AS YOU LEARN:
    
    - Create system diagram
    - Note "here be dragons" areas
    - Document what ISN'T obvious
    - Write the onboarding doc you wish you had
    ```
    
    ### 4. Risk Assessment
    
    | Risk Level | Signs |
    |------------|-------|
    | Low | Tests exist, clear patterns |
    | Medium | Some tests, mixed patterns |
    | High | No tests, confusing logic |
    | Critical | Nobody understands, production critical |
    

---
  #### **Name**
Git Archaeology
  #### **Description**
Using version control history as documentation
  #### **When To Use**
When trying to understand why code exists
  #### **Implementation**
    ## Reading Git History
    
    ### 1. Key Commands
    
    ```bash
    # Who knows this file?
    git shortlog -sn -- path/to/file
    
    # When did this function change?
    git log -p -S "functionName" -- path/
    
    # What was the context of this line?
    git blame -w -C -C -C path/to/file
    
    # What changed together?
    git log --stat --oneline -- path/
    ```
    
    ### 2. What History Reveals
    
    | Pattern | Meaning |
    |---------|---------|
    | Many authors, one file | Hot spot, high risk |
    | Recent changes | Active development |
    | Old commits only | Abandoned or stable |
    | Revert commits | Problem area |
    | Long messages | Complex context |
    
    ### 3. The "Why" Hunt
    
    ```
    FINDING CONTEXT:
    
    1. git blame → find the commit
    2. Read the full commit message
    3. Look for ticket/PR references
    4. Check if PR exists with discussion
    5. Search Slack/email archives
    ```
    
    ### 4. Author Archaeology
    
    | If author... | Try |
    |--------------|-----|
    | Still at company | Ask them |
    | Left recently | Ask their manager |
    | Long gone | Check their PRs |
    | Multiple authors | Find the most recent |
    

---
  #### **Name**
Test-Driven Understanding
  #### **Description**
Using tests to understand behavior
  #### **When To Use**
When code is complex but has tests
  #### **Implementation**
    ## Tests as Documentation
    
    ### 1. Test Hierarchy
    
    ```
    MOST USEFUL FOR UNDERSTANDING:
    
    1. Integration tests → What the system does
    2. Unit tests → What components do
    3. E2E tests → User flows
    4. Fixtures → Valid data shapes
    ```
    
    ### 2. Reading Tests
    
    | Test Element | Reveals |
    |--------------|---------|
    | Test name | Intended behavior |
    | Setup/arrange | Required state |
    | Assertions | Expected outcomes |
    | Mocks | External dependencies |
    
    ### 3. Exploration via Tests
    
    ```javascript
    // Add console.logs to understand flow
    test('existing test', () => {
      console.log('Input:', input);
      const result = mysteryFunction(input);
      console.log('Output:', result);
      // existing assertions
    });
    ```
    
    ### 4. Creating Understanding Tests
    
    ```javascript
    // Write tests to document discoveries
    describe('DISCOVERY: mysteryFunction', () => {
      test('returns X when given Y', () => {
        // Documents your understanding
        // If it breaks, understanding was wrong
      });
    });
    ```
    

---
  #### **Name**
Dependency Mapping
  #### **Description**
Understanding system interconnections
  #### **When To Use**
When understanding system boundaries
  #### **Implementation**
    ## Mapping Dependencies
    
    ### 1. External Dependencies
    
    ```
    FIND:
    
    □ Environment variables → External services
    □ HTTP calls → APIs consumed
    □ Database connections → Data stores
    □ Message queues → Async dependencies
    □ File paths → Filesystem dependencies
    ```
    
    | Config Type | Check |
    |-------------|-------|
    | .env files | Connection strings |
    | docker-compose | Services required |
    | kubernetes | External services |
    | config/*.json | Integration points |
    
    ### 2. Internal Dependencies
    
    ```
    CREATE DIAGRAM:
    
    ┌─────────┐    ┌──────────┐    ┌──────────┐
    │ Routes  │───▶│ Services │───▶│  Models  │
    └─────────┘    └──────────┘    └──────────┘
                        │
                        ▼
                   ┌──────────┐
                   │ External │
                   │   APIs   │
                   └──────────┘
    ```
    
    ### 3. Data Flow Tracing
    
    | Trace | Method |
    |-------|--------|
    | Request → Response | Follow handler |
    | Write → Read | Follow data ID |
    | Event → Handler | Search for subscribers |
    
    ### 4. Coupling Assessment
    
    | Coupling Level | Sign |
    |----------------|------|
    | Low | Clear interfaces |
    | Medium | Shared utilities |
    | High | Direct database access |
    | Dangerous | Circular dependencies |
    

## Anti-Patterns


---
  #### **Name**
The Premature Rewrite
  #### **Description**
Deciding to rewrite before understanding
  #### **Why Bad**
    You'll repeat mistakes.
    Lose hidden requirements.
    Likely fail anyway.
    
  #### **What To Do Instead**
    Understand first.
    Document what you learn.
    Incremental improvement.
    

---
  #### **Name**
The Judgment Trap
  #### **Description**
Dismissing code as "bad" without context
  #### **Why Bad**
    Miss the real constraints.
    Disrespect previous work.
    Create same problems.
    
  #### **What To Do Instead**
    Assume good intent.
    Find the context.
    Learn from decisions.
    

---
  #### **Name**
The Isolation Dig
  #### **Description**
Trying to understand alone
  #### **Why Bad**
    Slower than asking.
    Miss tribal knowledge.
    Reinvent understanding.
    
  #### **What To Do Instead**
    Find who knows.
    Ask questions.
    Pair on exploration.
    