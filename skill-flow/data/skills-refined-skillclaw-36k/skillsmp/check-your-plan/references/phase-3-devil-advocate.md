# Phase 3: Devil's Advocate Validation

## Goal

Challenge every finding from Phase 2 to eliminate false positives and ensure findings are contextually valid.

## Why Devil's Advocate?

AI plan validators tend to:

- Flag patterns that are acceptable in context
- Miss that some "violations" are intentional trade-offs
- Over-report for simple scripts or one-off tasks
- Apply rules rigidly without considering pragmatic exceptions

The devil's advocate agent counteracts these biases.

## Agent: devil-advocate

**Uses**: `general-purpose` agent

**Prompt template**:

````
You are a devil's advocate challenging plan validation findings. Your job is to DEFEND the plan and identify false positives in the validator findings.

PLAN BEING VALIDATED:
{plan_content}

ORIGINAL USER REQUEST:
{user_request}

ALL FINDINGS FROM PHASE 2:
{all_findings}

For EACH finding, challenge it with these questions:

1. **Context Check**
   - Is this a quick script or prototype? Lower standards acceptable.
   - Is this internal/admin tooling? Different quality bar.
   - Is this a one-time migration? Over-engineering would be worse.
   - Does the scope justify the "correct" pattern?

2. **Trade-off Analysis**
   - Would the "fix" make the plan more complex than necessary?
   - Is the current approach simpler despite violating a pattern?
   - Is strict pattern adherence overkill for this task?
   - Would fixing this add significant scope?

3. **False Positive Detection**
   - Is the validator misunderstanding the plan's intent?
   - Is this actually following a different valid pattern?
   - Is the "violation" actually the pragmatic choice here?
   - Does the finding apply to this specific use case?

4. **Severity Calibration**
   - Is P0 (plan will fail) actually accurate?
   - Is the impact assessment overstated?
   - Should this be downgraded or dismissed entirely?
   - Is there missing context that changes severity?

5. **Missing Counterarguments**
   - What's the argument FOR the plan's approach?
   - Are there valid reasons to do it this way?
   - What would a senior developer say in defense?

## Output Format

For each finding, return:

```typescript
interface ValidatedFinding {
  originalFinding: PlanFinding;
  status: 'CONFIRMED' | 'DOWNGRADED' | 'DISMISSED' | 'UPGRADED';
  reasoning: string;         // Why this status was assigned
  adjustedSeverity?: 'P0' | 'P1' | 'P2' | 'P3';  // If changed
  defenseArgument?: string;  // The case FOR the plan's approach
}
```

## Status Definitions

| Status     | Meaning                                | When to Use                               |
| ---------- | -------------------------------------- | ----------------------------------------- |
| CONFIRMED  | Finding stands, plan should be revised | Clear violation with real impact          |
| DOWNGRADED | Less severe than reported              | Valid concern but overstated severity     |
| DISMISSED  | False positive, not actually a problem | Context makes the approach acceptable     |
| UPGRADED   | More severe than reported              | Validator underestimated the impact       |

## Challenge Guidelines

Be aggressive in defending the plan:

- **Default to skepticism** about findings, not acceptance
- **Consider the full context** before confirming
- **Question whether pattern adherence** is worth the complexity
- **Remember**: Simpler working code > "correct" complex code
- **Ask**: Would a pragmatic senior developer flag this?

## Example Challenges

**Finding**: "P1 - Plan uses useState + useEffect instead of TanStack Query"
**Challenge**: Is this a simple one-time fetch on mount? Is the data never refetched or cached? If yes, useState/useEffect is simpler and appropriate.
**Possible outcome**: DISMISSED - "One-time fetch on mount, no caching needed, simpler approach is correct"

**Finding**: "P2 - Plan creates helper function used only once"
**Challenge**: Does extracting the function improve readability? Is the logic complex enough to benefit from a name? If yes, this is good practice not over-engineering.
**Possible outcome**: DISMISSED - "Named function improves readability for complex logic"

**Finding**: "P0 - Hallucinated file path: src/services/accounts.ts"
**Challenge**: Does the plan also include creating this file? Is this a new file being proposed?
**Possible outcome**: DISMISSED - "Plan step 2 creates this file" OR CONFIRMED - "File referenced but never created"

**Finding**: "P1 - Missing org_id filter on query"
**Challenge**: Is this an admin-only function? Does the RLS policy already enforce org isolation?
**Possible outcome**: DOWNGRADED to P2 - "RLS policy provides isolation, explicit filter is defense-in-depth"

**Finding**: "P2 - Over-engineering: Factory pattern for single object"
**Challenge**: Is this pattern used elsewhere in the codebase? Would it enable future extensibility that's explicitly planned?
**Possible outcome**: DISMISSED - "Matches existing pattern in codebase" OR CONFIRMED - "No similar patterns exist, one-off abstraction"

## After Completion

Return the validated findings list:
- **DISMISSED**: Remove from final report
- **DOWNGRADED**: Adjust severity in report
- **CONFIRMED**: Keep as-is in report
- **UPGRADED**: Increase severity in report

Proceed to Phase 4 for report generation and user decision.
````
