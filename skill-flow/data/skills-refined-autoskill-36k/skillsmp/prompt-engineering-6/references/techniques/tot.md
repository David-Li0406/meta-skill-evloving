# Tree-of-Thoughts (ToT)

Explore multiple solution paths. For complex problems with no obvious answer.

## Template

```xml
<task>
[Complex problem requiring exploration]
</task>

<instructions>
Step 1: Generate 3 different approaches
- Approach A: [Strategy]
- Approach B: [Strategy]
- Approach C: [Strategy]

Step 2: Evaluate each (rate 1-10)
For each approach:
- Feasibility: [Score]
- Likelihood of success: [Score]
- Potential issues: [List]

Step 3: Expand best approach into detailed steps

Step 4: If dead end, backtrack to next best approach

Step 5: Deliver final solution with rationale
</instructions>
```

## Example

```xml
<task>
Design authentication system for our new API. Must support both B2B (API keys) and B2C (user login) while keeping codebase simple.
</task>

<instructions>
Step 1: Generate approaches

Approach A: Unified auth middleware
- Single middleware handles both API keys and JWT tokens
- Route decorators specify which auth type(s) accepted
- Pro: Simple, one code path
- Con: May become complex with edge cases

Approach B: Separate auth services
- API key service for B2B
- OAuth/JWT service for B2C
- Gateway routes to appropriate service
- Pro: Clean separation
- Con: Two systems to maintain

Approach C: Third-party auth (Auth0/Clerk)
- Outsource auth entirely
- Both B2B and B2C handled by provider
- Pro: Battle-tested, less code
- Con: Vendor dependency, cost

Step 2: Evaluate

| Approach | Feasibility | Success | Issues |
|----------|-------------|---------|--------|
| A: Unified | 8 | 7 | Complex edge cases |
| B: Separate | 7 | 8 | Maintenance burden |
| C: Third-party | 9 | 9 | Cost, vendor lock-in |

Step 3: Expand Approach C (highest scores)
[Detailed implementation plan...]

Step 5: Final recommendation
Recommend Approach C (Auth0) because...
</instructions>
```

## When to Use

- Architecture decisions
- Complex debugging with multiple possible causes
- Strategy planning
- Creative problem-solving
- No obvious "right" answer

## When NOT to Use

- Simple tasks (massive overkill)
- Time-critical responses
- Tasks with clear single approach
