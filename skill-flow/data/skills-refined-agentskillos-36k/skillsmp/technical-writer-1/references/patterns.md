# Technical Writer

## Patterns


---
  #### **Name**
The README That Gets Read
  #### **Description**
Structure READMEs for how people actually read them
  #### **When**
Creating or updating a README
  #### **Example**
    # README STRUCTURE THAT WORKS:
    
    ## 1. Title and One-Liner (5 seconds)
    """
    # PaymentFlow
    
    A TypeScript library for handling Stripe payments with retry logic and webhooks.
    """
    # Reader knows: What is this? Is it for me?
    
    ## 2. Quick Start (60 seconds to working)
    """
    ## Quick Start
    
    ```bash
    npm install paymentflow
    ```
    
    ```typescript
    import { PaymentFlow } from 'paymentflow';
    
    const pf = new PaymentFlow({ apiKey: process.env.STRIPE_KEY });
    await pf.charge({ amount: 1000, currency: 'usd' });
    ```
    """
    # Reader has: Something working. Now they're invested.
    
    ## 3. Common Use Cases (2-5 minutes)
    """
    ## Common Use Cases
    
    ### Handling Failed Payments
    ```typescript
    const result = await pf.charge({ ... });
    if (result.failed) {
      // retry logic, notification, etc.
    }
    ```
    
    ### Webhook Setup
    ```typescript
    app.post('/webhook', pf.handleWebhook({
      onPaymentSuccess: (event) => { ... },
      onPaymentFailed: (event) => { ... },
    }));
    ```
    """
    
    ## 4. Reference (when needed)
    - Full API docs link
    - Configuration options
    - Error codes
    
    ## 5. The Rest (rarely read)
    - Contributing
    - License
    - Badges (at bottom, not top)
    

---
  #### **Name**
The Curse of Knowledge
  #### **Description**
Writing for someone who doesn't know what you know
  #### **When**
Writing any documentation
  #### **Example**
    # THE CURSE OF KNOWLEDGE:
    # You know the code. The reader doesn't. Bridge that gap.
    
    ## BAD - Written by Someone Who Knows:
    """
    To configure authentication, set up the auth middleware
    and register the providers.
    """
    # Assumes they know: what middleware, which providers, where to set up
    
    ## GOOD - Written for Someone Who Doesn't Know:
    """
    To configure authentication:
    
    1. Install the auth package:
       ```bash
       npm install @app/auth
       ```
    
    2. Add middleware to your server (src/server.ts):
       ```typescript
       import { authMiddleware } from '@app/auth';
       app.use(authMiddleware({
         providers: ['google', 'github'],
         secret: process.env.AUTH_SECRET,
       }));
       ```
    
    3. Create the login page (see examples/login.tsx)
    """
    
    ## THE CHECKLIST:
    Before publishing documentation, ask:
    
    1. If I knew nothing about this codebase, could I follow this?
    2. Are all prerequisites stated? (dependencies, environment, prior steps)
    3. Is every step actionable? (not just "configure X" but "add this code")
    4. Are file paths explicit? (not "the config file" but "src/config/auth.ts")
    5. What questions will they have? (answer them preemptively)
    

---
  #### **Name**
Architecture Decision Records (ADRs)
  #### **Description**
Lightweight decision documentation that ages well
  #### **When**
Making significant technical decisions
  #### **Example**
    # WHY ADRs BEAT ARCHITECTURE DOCS:
    
    Architecture docs: Comprehensive, become stale, rarely updated
    ADRs: Point-in-time decisions, never stale, accumulate over time
    
    ## ADR STRUCTURE:
    
    """
    # ADR-001: Use PostgreSQL for Primary Database
    
    ## Status
    Accepted (2024-01-15)
    
    ## Context
    We need a database for our SaaS application. Expected load is
    10K users initially, scaling to 100K. Features needed:
    - ACID transactions for payments
    - Full-text search for product catalog
    - JSON storage for user preferences
    
    ## Decision
    Use PostgreSQL with the following setup:
    - Supabase for managed hosting
    - Connection pooling via pgBouncer
    - Full-text search via pg_trgm extension
    
    ## Consequences
    Good:
    - Mature, well-understood technology
    - Supabase handles backups, scaling
    - Team has PostgreSQL experience
    
    Bad:
    - Vendor lock-in to Supabase
    - More complex than SQLite for local dev
    - Full-text search is good, not great (vs Elasticsearch)
    
    ## Alternatives Considered
    - MongoDB: Rejected - we need transactions
    - SQLite: Rejected - not production-ready for our scale
    - MySQL: Viable but team prefers PostgreSQL
    """
    
    ## ADR TIPS:
    
    1. Number them sequentially (ADR-001, ADR-002, ...)
    2. Never edit status after "Accepted" - write new ADR instead
    3. Keep in version control (docs/adr/ or decisions/)
    4. Include "Alternatives Considered" - future you will ask
    5. One decision per ADR - keep them focused
    

---
  #### **Name**
Code Comments That Add Value
  #### **Description**
Knowing when and how to comment code
  #### **When**
Deciding whether to add code comments
  #### **Example**
    # CODE COMMENT DECISION FRAMEWORK:
    
    ## NEVER Comment:
    - What the code does (the code says that)
    - Obvious operations
    - Anything that can be renamed instead
    
    """
    // BAD: Comment says what code says
    // Loop through users and check if active
    for (const user of users) {
      if (user.active) { ... }
    }
    
    // BAD: Comment for obvious operation
    // Increment counter
    counter++;
    """
    
    ## ALWAYS Comment:
    - WHY (non-obvious reasoning)
    - WORKAROUNDS (why something weird exists)
    - EDGE CASES (why this check exists)
    - BUSINESS RULES (context not in code)
    
    """
    // GOOD: Explains WHY, not WHAT
    // Stripe requires amounts in cents, not dollars
    const amountCents = dollars * 100;
    
    // GOOD: Explains workaround
    // Safari has a bug with date parsing - use this format
    // See: webkit.org/b/123456
    const date = parseISO(input);
    
    // GOOD: Business rule context
    // Free trial is 14 days for US, 30 days for EU (GDPR requirement)
    const trialDays = user.region === 'EU' ? 30 : 14;
    
    // GOOD: Warning about non-obvious behavior
    // WARNING: This mutates the input array for performance
    // If you need immutability, clone first
    function sortInPlace(arr) { ... }
    """
    
    ## THE RENAME TEST:
    Before adding a comment, ask: "Could I rename instead?"
    
    """
    // BAD: Comment needed because name is unclear
    let d = 86400; // seconds in a day
    
    // GOOD: Name is clear, no comment needed
    const SECONDS_PER_DAY = 86400;
    """
    

---
  #### **Name**
API Documentation Essentials
  #### **Description**
What developers actually need from API docs
  #### **When**
Documenting APIs (REST, GraphQL, libraries)
  #### **Example**
    # API DOCUMENTATION HIERARCHY:
    
    ## Level 1: Quick Example (90% of visits)
    """
    ## Create a Payment
    
    ```bash
    curl -X POST https://api.example.com/payments \
      -H "Authorization: Bearer $API_KEY" \
      -d '{"amount": 1000, "currency": "usd"}'
    ```
    
    Response:
    ```json
    {
      "id": "pay_123",
      "status": "succeeded",
      "amount": 1000
    }
    ```
    """
    # This is what 90% of developers need. They'll copy-paste and adapt.
    
    ## Level 2: Error Handling (next question)
    """
    ### Errors
    
    | Code | Meaning | What to Do |
    |------|---------|------------|
    | 400 | Invalid request | Check required fields |
    | 401 | Invalid API key | Check Authorization header |
    | 402 | Payment failed | Card declined, try another |
    | 429 | Rate limited | Wait and retry (see headers) |
    """
    
    ## Level 3: Complete Reference (when needed)
    """
    ### Request Body
    
    | Field | Type | Required | Description |
    |-------|------|----------|-------------|
    | amount | integer | Yes | Amount in cents |
    | currency | string | Yes | ISO currency code |
    | customer_id | string | No | Link to customer |
    | metadata | object | No | Custom key-value pairs |
    """
    
    ## Level 4: Edge Cases and Advanced
    """
    ### Idempotency
    
    For retry safety, include Idempotency-Key header:
    ```bash
    curl -X POST ... -H "Idempotency-Key: unique-request-id"
    ```
    Duplicate requests with same key return original response.
    """
    
    ## THE ORDER MATTERS:
    Most docs put reference first (Level 3).
    But developers want working examples first (Level 1).
    Structure for how people actually read, not how docs are "supposed" to be.
    

---
  #### **Name**
Documentation Maintenance
  #### **Description**
Keeping docs current without making it a full-time job
  #### **When**
Establishing documentation practices
  #### **Example**
    # DOCS MAINTENANCE STRATEGY:
    
    ## The Two Types of Documentation:
    
    ### 1. Living Documentation (must be maintained)
    - README (installation, quick start)
    - API reference (auto-generated when possible)
    - Configuration reference
    - Troubleshooting guide
    
    These break if they're wrong. Users notice immediately.
    Keep them in the same repo as code. Review in PRs.
    
    ### 2. Point-in-Time Documentation (never needs updating)
    - ADRs (decisions made at a point in time)
    - Release notes (what happened in v1.2.3)
    - Post-mortems (what happened in the incident)
    - Tutorials (for a specific version)
    
    These are snapshots. They don't become "wrong" - they become "old."
    That's fine. Version them appropriately.
    
    ## MAINTENANCE PRACTICES:
    
    ### 1. Docs-as-Code
    """
    # In PR template or CI:
    
    ## Documentation
    - [ ] README updated if user-facing behavior changed
    - [ ] API docs updated if endpoints changed
    - [ ] Changelog entry added
    
    # Auto-fail CI if:
    - Public API changed without doc update
    - New config option without documentation
    """
    
    ### 2. Documentation Tests
    """
    # Test that examples in docs actually work:
    # Extract code blocks and run them
    
    import doctest
    doctest.testmod(mymodule)  # Tests examples in docstrings
    
    # For README examples:
    npm run test:examples  # Extract and run README code blocks
    """
    
    ### 3. The Freshness Check
    """
    # Quarterly: Review all docs
    # For each doc, ask:
    
    1. Is this still accurate?
       - If no: Fix or delete
    2. Is anyone reading this?
       - If no: Consider deleting
    3. Is this the right level of detail?
       - If too much: Trim
       - If too little: Expand or link
    
    # Track last-reviewed date:
    <!-- Last reviewed: 2024-01-15 -->
    """
    
    ### 4. Delete Dead Docs
    """
    Dead documentation is worse than no documentation.
    It wastes time and erodes trust.
    
    Signs of dead docs:
    - Refers to files/features that don't exist
    - Screenshots of old UI
    - Commands that don't work
    - Links that 404
    
    When you find dead docs: Delete or fix immediately.
    Don't "plan to fix later" - that's how docs die.
    """
    

## Anti-Patterns


---
  #### **Name**
Documentation as Afterthought
  #### **Description**
Writing docs at the end of a project
  #### **Why**
    By then, you've forgotten the context. Why did we make that choice?
    What was the alternative? What gotchas did we discover? That knowledge
    is lost. Write docs as you build, when the context is fresh.
    
  #### **Instead**
Write docs incrementally. ADRs during decisions, API docs during implementation, README during development.

---
  #### **Name**
Documentation Lies
  #### **Description**
Docs that say one thing while code does another
  #### **Why**
    Wrong documentation is worse than no documentation. Users follow the docs,
    hit errors, lose hours debugging. Trust in all documentation erodes.
    One lie damages all docs.
    
  #### **Instead**
Test documentation. Auto-generate when possible. Include docs in PR reviews.

---
  #### **Name**
The Wall of Text
  #### **Description**
Dense paragraphs without structure or examples
  #### **Why**
    Nobody reads walls of text. They scan for what they need. Without structure,
    they can't find it. Without examples, they can't apply it. The documentation
    exists but doesn't help.
    
  #### **Instead**
Use headers, lists, code examples. Make content scannable. Lead with examples.

---
  #### **Name**
Over-Documentation
  #### **Description**
Documenting everything regardless of value
  #### **Why**
    More docs isn't better - it's more to maintain and more to search through.
    Documenting obvious code adds noise. Documenting every internal function
    creates overhead. The important stuff gets lost in the volume.
    
  #### **Instead**
Document decisions, not code. Document interfaces, not internals. Document surprises, not obvious behavior.

---
  #### **Name**
Internal Jargon
  #### **Description**
Using terms only insiders understand
  #### **Why**
    Documentation is for people who don't know yet. Using internal names, project
    codenames, or team terminology excludes the very people who need the docs.
    The expert doesn't need docs; the newcomer does.
    
  #### **Instead**
Define terms on first use. Use industry-standard terminology. Write for someone joining tomorrow.

---
  #### **Name**
No Examples
  #### **Description**
Reference docs without working code samples
  #### **Why**
    Developers learn by example, not by reading specs. An API reference with
    only parameter tables is barely usable. Developers want to copy, paste, adapt.
    No examples means they'll find another library.
    
  #### **Instead**
Every API endpoint needs a working example. Every configuration option needs a sample. Show, don't just tell.

---
  #### **Name**
Tutorial That Can't Be Completed
  #### **Description**
Tutorials with missing steps or broken code
  #### **Why**
    A broken tutorial is a broken promise. User invests time, hits a wall,
    gives up. They'll never try your tool again. One broken step invalidates
    the entire tutorial.
    
  #### **Instead**
Test every tutorial end-to-end. Version your tutorials. Update when dependencies change.