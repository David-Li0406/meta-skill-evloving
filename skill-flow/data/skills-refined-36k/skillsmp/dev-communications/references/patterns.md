# Developer Communications

## Patterns


---
  #### **Name**
Code First Documentation
  #### **Description**
Start with working code examples, then explain why it works
  #### **When**
Writing any developer tutorial or getting started guide
  #### **Example**
    ```typescript
    // Working example first
    import { createClient } from '@your/sdk';
    
    const client = createClient({
      apiKey: process.env.API_KEY
    });
    
    const result = await client.users.create({
      email: 'user@example.com'
    });
    
    // Now explain: This creates an authenticated client...
    ```
    

---
  #### **Name**
Progressive Disclosure
  #### **Description**
Layer information by urgency - quick start first, deep dive later
  #### **When**
Writing comprehensive API documentation or feature guides
  #### **Example**
    # Quick Start (5 minutes to first API call)
    # Common Use Cases (solve 80% of needs)
    # Advanced Configuration (power users)
    # API Reference (complete details)
    

---
  #### **Name**
Fail Fast Examples
  #### **Description**
Show error cases and how to fix them, not just happy paths
  #### **When**
Documenting APIs with common failure modes
  #### **Example**
    ```typescript
    try {
      await api.charge({ amount: 5000 });
    } catch (error) {
      if (error.code === 'insufficient_funds') {
        // Show the user a top-up flow
      }
      // Document actual errors developers will see
    }
    ```
    

---
  #### **Name**
Runnable Documentation
  #### **Description**
Every code example should be copy-paste runnable
  #### **When**
Writing code examples in docs
  #### **Example**
    # Include all imports, environment setup, and teardown
    # Use realistic data that makes sense in context
    # Add comments showing expected output
    # Link to working CodeSandbox/StackBlitz
    

---
  #### **Name**
Decision Trees Over Walls of Text
  #### **Description**
Help developers choose the right path with flowcharts and decision matrices
  #### **When**
Multiple ways to solve a problem or configure a feature
  #### **Example**
    Need authentication?
    ├─ Simple MVP? → API Keys
    ├─ User-facing app? → OAuth 2.0
    └─ Embedded in customer systems? → JWT
    

---
  #### **Name**
Changelog as Communication
  #### **Description**
Treat changelogs as developer relationship management
  #### **When**
Writing release notes and changelogs
  #### **Example**
    ## v2.1.0
    
    **Breaking:** Removed deprecated `createUser()`. Use `users.create()` instead.
    Migration guide: [link]
    
    **New:** Webhook signatures now use SHA-256. Old webhooks work until June 1.
    
    **Fixed:** Race condition in concurrent requests. No action needed.
    

## Anti-Patterns


---
  #### **Name**
Marketing Voice in Docs
  #### **Description**
Using sales language instead of technical precision
  #### **Why**
Developers detect and hate marketing speak in technical documentation
  #### **Instead**
    Bad: "Our blazing-fast API delivers unparalleled performance!"
    Good: "Typical response time: 150ms (p95). Rate limit: 100 req/sec."
    

---
  #### **Name**
Placeholder Hell
  #### **Description**
Examples filled with foo, bar, example.com that don't relate to real use
  #### **Why**
Developers have to mentally translate every example to their domain
  #### **Instead**
    Bad: const foo = api.bar('example')
    Good: const subscription = api.subscriptions.create({ plan: 'pro' })
    

---
  #### **Name**
Assuming Context
  #### **Description**
Documentation that assumes you've read everything before it
  #### **Why**
Developers jump to the page they need, not reading sequentially
  #### **Instead**
    Every page should be self-contained with links to prerequisites.
    Include "Before you begin" sections with required context.
    

---
  #### **Name**
Stale Examples
  #### **Description**
Code examples that don't work with current version
  #### **Why**
Instant trust destruction when copy-paste fails
  #### **Instead**
    Automate example testing in CI. Version examples to match docs.
    Add "Last verified: [date]" to complex examples.
    

---
  #### **Name**
Feature List Documentation
  #### **Description**
Documenting what it does instead of how to use it
  #### **Why**
Developers need task-oriented guidance, not feature tours
  #### **Instead**
    Bad: "Our API supports pagination, filtering, and sorting"
    Good: "To fetch users in pages of 50: api.users.list({ limit: 50 })"
    

---
  #### **Name**
Hidden Prerequisites
  #### **Description**
Tutorials that fail because of undocumented setup requirements
  #### **Why**
Nothing kills momentum like discovering Step 0 at Step 5
  #### **Instead**
    Lead with complete requirements checklist:
    - Node.js 18+
    - PostgreSQL running locally
    - Environment variables: API_KEY, DATABASE_URL
    