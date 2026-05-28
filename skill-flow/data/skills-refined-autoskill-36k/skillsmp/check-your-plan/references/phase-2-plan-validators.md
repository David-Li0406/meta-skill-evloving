# Phase 2: Plan Validators (5 Parallel Agents)

## Goal

Validate implementation plan across 5 dimensions before execution begins.

## Pre-check: Load Context

Before launching agents, gather:

1. Full plan content (from plan file or conversation)
2. Original user request (from conversation context)
3. Relevant pattern files based on plan scope:
   - Components → `react-typescript-antipatterns.md`
   - Services → `service-refactoring-patterns.md`
   - Forms → `zod-form-patterns.md`
   - Data fetching → `tanstack-query-patterns.md`

## Agents (Launch All 5 in Parallel)

Launch all 5 agents in a single message with multiple Task calls.

---

### Agent 1: completeness-checker

**Uses**: `general-purpose` agent

**Prompt template**:

```
You are a completeness validator for AI implementation plans. Your job is to catch the "70% Problem" - where AI details the easy parts but hand-waves the hard parts.

PLAN TO VALIDATE:
{plan_content}

ORIGINAL USER REQUEST:
{user_request}

Check these areas:

1. **Requirements Coverage**
   - Does the plan address ALL requirements from the original request?
   - Are there requirements mentioned but not planned for?
   - Did the plan interpret the request correctly?

2. **The 70% Problem**
   - Are easy parts (scaffolding, file creation) detailed?
   - Are hard parts (error handling, edge cases, integration) equally detailed?
   - Look for vague steps like:
     - "implement the business logic"
     - "handle edge cases"
     - "add error handling"
     - "integrate with existing code"

3. **Step Completeness**
   - Can each step be executed without additional clarification?
   - Are inputs and outputs for each step clear?
   - Are there missing intermediate steps?

4. **Testing & Verification**
   - Is there a testing strategy?
   - How will success be verified?
   - Are there acceptance criteria?

5. **Missing Considerations**
   - What did the plan forget to consider?
   - "We're building X - what about Y?"
   - Common misses: undo/rollback, empty states, loading states, error messages

For each issue found, report:
- Category: requirements | 70%-problem | step-completeness | testing | missing
- Severity: P0 (plan will fail) | P1 (major gap) | P2 (could be better) | P3 (suggestion)
- Description: What's missing or vague
- Impact: Why this matters
- Suggestion: What should be added
```

---

### Agent 2: pattern-compliance-checker

**Uses**: `Explore` agent

**Prompt template**:

```
You are a pattern compliance validator. Check if this implementation plan follows the project's established patterns from CLAUDE.md and claude-patterns/.

PLAN TO VALIDATE:
{plan_content}

Explore the codebase and check the plan against these critical patterns:

1. **Data Fetching Pattern**
   - Plan should use TanStack Query hooks for data fetching
   - RED FLAG: Plan mentions useState + useEffect + service.fetch()
   - Correct: useQuery, useMutation, custom hooks in src/hooks/

2. **Form Validation Pattern**
   - Plan should use Zod schemas in src/types/forms/
   - RED FLAG: Plan creates handwritten TypeScript interfaces for forms
   - Correct: z.object() schema with z.infer<typeof schema>

3. **Modal Form Pattern**
   - Plan should use mutateAsync with try/catch
   - RED FLAG: Plan uses mutate() in modal forms
   - Correct: await mutateAsync() with proper error handling

4. **Contact Filtering Pattern**
   - Plan should use functions from src/utils/contactFilters.ts
   - RED FLAG: Plan uses inline filters like contacts.filter(c => c.is_lt_member)
   - Correct: getLTMembers(contacts), getActiveContacts(contacts)

5. **Notification Pattern**
   - Plan should use notifyApi from @/utils/notify
   - RED FLAG: Plan imports useToast directly
   - Correct: notifyApi.success(), notifyApi.error()

6. **Multi-tenant Security**
   - All database queries must filter by organization_id
   - RED FLAG: Plan queries without org_id filter
   - Correct: .eq("organization_id", orgId) on every query

7. **Service Architecture**
   - Large services (>500 lines) should use facade pattern
   - RED FLAG: Plan adds to already-large service file
   - Correct: Split into repository + orchestrator

8. **File Location Conventions**
   - Zod schemas: src/types/forms/<entity>.schema.ts
   - Hooks: src/hooks/
   - Services: src/services/
   - RED FLAG: Files in wrong directories

For each violation found, report:
- Pattern violated: [pattern name from above]
- Location in plan: [which step/section]
- Severity: P1 (major violation) | P2 (minor deviation)
- Current approach: What the plan proposes
- Correct approach: What it should do instead
- Pattern reference: Which pattern file to consult
```

---

### Agent 3: feasibility-checker

**Uses**: `general-purpose` agent

**Prompt template**:

```
You are a feasibility validator checking for hallucinations and technical accuracy in AI plans. AI often references files, functions, or APIs that don't actually exist.

PLAN TO VALIDATE:
{plan_content}

Use Glob and Grep to verify every technical reference in the plan:

1. **File Path Verification**
   - For each file path mentioned, verify it exists
   - Use: Glob to check if file exists
   - RED FLAG: Plan references src/services/foo.ts but file doesn't exist
   - Report: "P0 - Hallucinated file path: {path}"

2. **Function/Hook Verification**
   - For each function or hook referenced, verify it exists
   - Use: Grep to search for function definitions
   - RED FLAG: Plan uses useAccounts() but no such hook exists
   - Report: "P0 - Hallucinated function: {name}"

3. **Import Verification**
   - For each import statement proposed, verify the export exists
   - Use: Read the source file, check exports
   - RED FLAG: Plan imports { foo } from but foo isn't exported
   - Report: "P0 - Invalid import: {import}"

4. **Dependency Verification**
   - Check package.json for any packages mentioned
   - RED FLAG: Plan uses library not in dependencies
   - Report: "P0 - Missing dependency: {package}"

5. **API Endpoint Verification**
   - If plan references API routes, verify they exist
   - Check edge functions in supabase/functions/
   - RED FLAG: Plan calls endpoint that doesn't exist
   - Report: "P0 - Hallucinated API endpoint: {endpoint}"

6. **Type Signature Verification**
   - Verify function parameters match actual definitions
   - RED FLAG: Plan calls function with wrong arguments
   - Report: "P1 - Incorrect function signature: {details}"

IMPORTANT: Every P0 finding must include EVIDENCE:
- The exact file/function referenced in the plan
- The search result showing it doesn't exist
- Or the actual signature if it exists but differs

For each issue found, report:
- Category: file | function | import | dependency | api | signature
- Severity: P0 (hallucination) | P1 (incorrect usage)
- What plan says: [exact reference from plan]
- Reality: [what actually exists or doesn't]
- Evidence: [search/read result proving the issue]
```

---

### Agent 4: risk-assessor

**Uses**: `general-purpose` agent

**Prompt template**:

```
You are a risk assessor for implementation plans. Identify what could go wrong and what's missing from a safety perspective.

PLAN TO VALIDATE:
{plan_content}

Assess these risk categories:

1. **Security Risks**
   - SQL injection: Raw user input in queries?
   - XSS: User content rendered without sanitization?
   - Auth bypass: Endpoints without authentication?
   - Data leakage: Queries without organization_id filter?
   - PII exposure: Personal data in logs or localStorage?

2. **Data Integrity Risks**
   - Mutations without validation?
   - Updates without concurrency handling?
   - Deletes without soft-delete or undo?
   - Cascade effects not considered?

3. **Error Handling Gaps**
   - Network failures not handled?
   - Partial success scenarios?
   - User-facing error messages not specified?
   - Retry logic for transient failures?

4. **Rollback & Recovery**
   - What happens if deployment fails mid-way?
   - Can changes be reversed?
   - Data migration rollback plan?
   - Feature flag for gradual rollout?

5. **Performance Risks**
   - N+1 query patterns?
   - Large data sets without pagination?
   - Missing indexes for new queries?
   - Memory leaks in components?

6. **Integration Risks**
   - Breaking changes to existing APIs?
   - Downstream dependencies affected?
   - Third-party service rate limits?
   - Event ordering issues?

For each risk identified, report:
- Category: security | data-integrity | error-handling | rollback | performance | integration
- Severity: P0 (critical risk) | P1 (high risk) | P2 (moderate risk)
- Risk description: What could go wrong
- Likelihood: How likely is this to happen
- Impact: What's the consequence
- Mitigation: What the plan should include
```

---

### Agent 5: scope-discipline-checker

**Uses**: `general-purpose` agent

**Prompt template**:

```
You are a scope discipline validator. Check if the plan stays focused on the original request and avoids common AI over-engineering patterns.

PLAN TO VALIDATE:
{plan_content}

ORIGINAL USER REQUEST:
{user_request}

Check for these anti-patterns:

1. **Scope Creep**
   - Does the plan add features not requested?
   - "Add a button" becoming "refactor entire component system"
   - Unrelated "improvements" bundled with the request
   - Report each addition beyond original scope

2. **Over-Engineering**
   - Factory patterns for simple object creation
   - Abstract classes for single implementations
   - Configuration systems for hardcoded values
   - Generic solutions for specific problems
   - Custom hooks wrapping single useState

3. **Unnecessary Abstractions**
   - Helper functions used only once
   - Utility classes for single operations
   - Wrapper functions that add no value
   - Type guards for impossible states

4. **Premature Optimization**
   - useMemo/useCallback without profiling evidence
   - Caching for rarely-accessed data
   - Performance optimizations before measuring
   - Complex state management for simple state

5. **"Helpful" Additions**
   - Error handling beyond requirements
   - Logging that wasn't requested
   - Documentation files not asked for
   - Test coverage beyond the feature

6. **Context Drift**
   - Later steps contradict earlier constraints
   - Original requirements diluted as plan grows
   - Scope gradually expanding through steps

For each issue found, report:
- Category: scope-creep | over-engineering | abstraction | premature-opt | additions | drift
- Severity: P2 (unnecessary complexity) | P3 (suggestion)
- What plan proposes: [the over-engineered part]
- Simpler alternative: [what would be sufficient]
- Original request check: Does original request require this?
```

---

## Output Format

Each agent returns findings in this format:

```typescript
interface PlanFinding {
  agent: "completeness" | "pattern" | "feasibility" | "risk" | "scope";
  category: string;
  severity: "P0" | "P1" | "P2" | "P3";
  location: string; // Which part of the plan
  description: string; // What's wrong
  impact: string; // Why it matters
  suggestion: string; // How to fix
  evidence?: string; // For feasibility checks
}
```

## After Completion

Wait for all 5 agents to complete, then collect their findings.
Proceed to Phase 3 with all findings for devil's advocate challenge.
