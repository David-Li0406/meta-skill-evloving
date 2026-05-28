# ExecPlan Failure Modes

These patterns cause ExecPlans to fail. Study them. The validator (`scripts/validate_plan.py`) detects many automatically, but understanding WHY they fail helps you avoid them in the first place.


## 1. The Amnesia Trap (External References)

**Pattern**: Pointing to docs, blogs, RFCs, or prior discussions.

    See the architecture diagram in Confluence.
    Per RFC 6749, implement the flow.
    As we discussed in the design review...
    According to the architecture doc...

**Why it fails**: The implementer has no access to "the design review" or "the RFC." RFC 6749 is 75 pages. The plan does not contain the knowledge needed to execute. A novice cannot succeed.

**Fix**: Embed the required knowledge directly in the plan in your own words. If OAuth2 is needed, describe the specific flow this system uses, not "see the RFC."

**Validator detection**: Yes—detects "as discussed", "see the doc", "per the RFC"


## 2. The Jargon Wall (Undefined Terms)

**Pattern**: Using technical terms without defining them.

    Use the middleware to intercept RPC calls and apply rate limiting
    via the circuit breaker pattern.

**Why it fails**: "Middleware," "RPC," and "circuit breaker" mean different things in different contexts. Where are these in THIS repository? What files? What functions? A novice cannot navigate.

**Fix**: Define every term and ground it in this repository:

    The rate limiter intercepts incoming requests in src/middleware/rateLimit.ts.
    This file exports an Express middleware function that checks Redis for
    request counts. "Circuit breaker" here means the logic in src/lib/breaker.ts
    that stops forwarding requests to a downstream service after 5 consecutive
    failures, resuming after 30 seconds.

**Validator detection**: Partial—detects common jargon without nearby definitions


## 3. The Wishful Thinking Test (Vague Acceptance)

**Pattern**: Non-verifiable acceptance criteria.

    Tests should pass.
    The system should be fast and reliable.
    Users should have a good experience.

**Why it fails**: "Fast," "reliable," and "good experience" are subjective. "Tests should pass" doesn't specify which tests or expected counts. A novice cannot distinguish success from failure.

**Fix**: Be specific and observable.

    Run `npm test -- --grep auth` and expect 12 passing.
    The new tests in auth.test.ts (3 tests) fail before this change and pass after.
    Response time: GET /api/users/:id returns within 100ms (p95) under load.

**Validator detection**: Yes—detects "should pass", "should work correctly"


## 4. The Trust Me Plan (Outsourced Decisions)

**Pattern**: Deferring choices to the implementer.

    Choose an appropriate database library and configure it as needed.
    Use best judgment for error handling.
    Select a suitable approach.

**Why it fails**: The plan provides no guidance. Different implementers will make different choices, leading to inconsistency or wrong decisions. A novice will be paralyzed.

**Fix**: Make the decision and explain why.

    Use pg (node-postgres) version 8.x for database access. This is the library
    already used elsewhere in the codebase (see src/db/pool.ts). For errors,
    catch connection failures and retry once after 1 second; log and rethrow
    on second failure.

**Validator detection**: Yes—detects "as needed", "best judgment", "appropriate"


## 5. The Letter-of-the-Law Plan (Code Without Behavior)

**Pattern**: Specifying code structure that compiles but does nothing meaningful.

    Add a UserService class with getUser and updateUser methods.
    
    ## Acceptance
    UserService exists with the specified methods.

**Why it fails**: Empty method stubs satisfy this criterion. The plan never specifies what these methods DO or how to verify they work. This produces dead code.

**Fix**: Specify observable behavior, not code structure.

    ## Acceptance
    After starting the server:
    
        curl http://localhost:3000/api/users/123
    
    Returns HTTP 200 with user data:
    
        {"id":"123","name":"Alice","email":"alice@example.com"}

**Validator detection**: Partial—detects missing validation commands


## 6. The Point of No Return (Missing Recovery)

**Pattern**: Risky operations without rollback instructions.

    Run the database migration to add the new column.

**Why it fails**: What if the migration fails halfway? What if the migration succeeds but the code is wrong? A novice will be stuck with a broken system.

**Fix**: Include recovery for every risky operation.

    Run the database migration:
    
        npm run migrate:up
    
    If migration fails, check the error and fix the issue. Migrations are
    idempotent; re-running is safe.
    
    If you need to rollback after the migration succeeds:
    
        npm run migrate:down -- --step 1
    
    This removes the column. Note: rollback loses any data written to the
    new column since the migration ran.

**Validator detection**: No—requires manual review


## 7. The Goldfish Plan (Progress Blindness)

**Pattern**: Progress section not updated as work proceeds.

    ## Progress
    - [ ] Implement feature
    - [ ] Write tests
    - [ ] Deploy

**Why it fails**: After working for 3 hours, the Progress section still shows the original items. If the agent crashes, context is lost, or work is handed off, there's no record of what was actually done. Work cannot resume.

**Fix**: Update Progress at every stopping point with timestamps.

    ## Progress
    - [x] (2025-01-20 14:00Z) Created TokenService skeleton
    - [x] (2025-01-20 14:30Z) Implemented generateToken method
    - [x] (2025-01-20 15:00Z) Added unit tests (3 passing)
    - [ ] Implement verifyToken method (next)
    - [ ] Add integration tests
    - [ ] Wire into login endpoint

**Validator detection**: Yes—detects completed items without timestamps


## 8. The Infinite Plan (No Demonstrable Output)

**Pattern**: Plan keeps growing without reaching demonstrable milestones.

**Why it fails**: A plan with 47 items in Progress, none checked, and no working code after hours of "research." The plan has become a document for its own sake rather than a guide to working software.

**Fix**: Every milestone must produce something demonstrable. If research is needed, make it a milestone with concrete output.

    ### Milestone 0: Validate Library Feasibility
    
    Scope: Determine if pdf-lib can merge PDFs with form fields intact.
    
    Work: Create test/pdf-merge-spike.ts that merges two sample PDFs.
    
    Acceptance: Run the spike; output PDF opens in Adobe Reader with both
    pages and form fields functional. If fields are lost, document finding
    and evaluate alternatives.

**Validator detection**: No—requires milestone review


## 9. The Silent Struggle (Undocumented Discoveries)

**Pattern**: Surprises encountered during implementation are not recorded.

**Why it fails**: Developer discovers that a library throws exceptions instead of returning null, but doesn't write it down. Later, another developer (or agent) hits the same issue and wastes time rediscovering it.

**Fix**: Record every surprise with evidence in Surprises & Discoveries.

    ## Surprises & Discoveries
    
    - Observation: bcrypt.compare() is async but bcrypt.compareSync() exists
      Evidence: TypeError: bcrypt.compare is not a function (was calling wrong method)
      Resolution: Use await bcrypt.compare(password, hash)

**Validator detection**: No—requires diligence during execution


## 10. The Decision Amnesia (Unlogged Choices)

**Pattern**: Decisions made during implementation are not recorded.

**Why it fails**: Six months later, someone asks "why did we use HS256 instead of RS256?" No one remembers. The decision cannot be evaluated or reconsidered with proper context.

**Fix**: Record every significant decision in the Decision Log with rationale.

    ## Decision Log
    
    - Decision: Use HS256 algorithm for JWT signing instead of RS256
      Rationale: The application runs on a single server. RS256's asymmetric keys
      are useful for cross-service verification, which we do not need. HS256 has
      lower computational overhead and simpler key management.
      Date: 2025-01-20

**Validator detection**: No—requires diligence during execution


## Using the Validator

Run `python scripts/validate_plan.py <plan.md>` before starting implementation.

The validator detects:
- Missing required sections
- External reference patterns ("as discussed", "see the doc", "per the RFC")
- Unresolved placeholders ("TBD", "to be determined")
- Vague instructions ("as needed", "configure appropriately", "use best judgment")
- Vague acceptance ("tests should pass" without specifics)
- Completed Progress items without timestamps
- Common jargon without definitions

Fix ALL errors before starting implementation. The validator catches the mechanical failures; you must catch the conceptual ones by understanding why these patterns fail.
