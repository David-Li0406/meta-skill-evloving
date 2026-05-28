# Phase 3: Severity Validation (Up to 3 Parallel Agents)

## Goal

Validate findings by severity level. Launch one agent per severity level that has findings (max 3 agents).

## Trigger Condition

Only run if Phase 2 found P0, P1, or P2 issues.

## Why This Phase Exists

Agents often flag issues based on pattern matching without understanding context. This phase validates severity claims before alarming the user.

## Agents (Launch in Parallel)

For each severity level with findings, launch a validator agent:

### p0-validator (if P0 findings exist)

**Uses**: `general-purpose` agent

**Prompt template**:

```
You are the P0 validator. Your job is to verify that these CRITICAL findings are actually critical.

P0 FINDINGS TO VALIDATE:
{p0_findings_list}

FILES TO CHECK:
{file_list}

For each P0 finding, investigate:

1. **Pattern Context**: Does the violated pattern actually apply here?
   - Is this admin-only code?
   - Is org_id filtered upstream?
   - Is this a utility function with different rules?

2. **Actual Impact**: What would actually happen?
   - Will it break functionality?
   - Will it expose data to wrong users?
   - Can you trace the actual data flow?

3. **Codebase Patterns**: Is there existing code that intentionally follows this pattern?

For each finding, return one of:
- CONFIRMED: Severity accurate, genuine critical issue with evidence
- DOWNGRADED: Issue exists but less severe (provide correct severity P1/P2/P3 + reasoning)
- FALSE_POSITIVE: Not actually an issue in this context (provide explanation)
```

### p1-validator (if P1 findings exist)

**Uses**: `general-purpose` agent

Same validation approach as p0-validator but for P1 findings.

### p2-validator (if P2 findings exist)

**Uses**: `general-purpose` agent

Same validation approach as p0-validator but for P2 findings.

## Execution

1. Count findings by severity level (P0, P1, P2)
2. For each level with findings, launch a validator agent
3. Launch all validators in a single message with multiple Task calls
4. Wait for all validators to complete

## Output Format

Each validator returns:

```typescript
interface ValidationResult {
  severity: "P0" | "P1" | "P2";
  findings: Array<{
    originalFinding: Finding;
    status: "CONFIRMED" | "DOWNGRADED" | "FALSE_POSITIVE";
    newSeverity?: "P1" | "P2" | "P3"; // Only if DOWNGRADED
    reasoning: string;
  }>;
}
```

## Example Flow

```
Phase 2 finds:
- 2 P0 issues
- 3 P1 issues
- 0 P2 issues

Phase 3 launches 2 agents:
- p0-validator (validates 2 P0 findings)
- p1-validator (validates 3 P1 findings)
- (no p2-validator - no P2 findings)

Results:
- P0 #1: CONFIRMED (genuine security issue)
- P0 #2: DOWNGRADED to P2 (admin-only code, not user-facing)
- P1 #1: FALSE_POSITIVE (upstream validation handles this)
- P1 #2: CONFIRMED
- P1 #3: CONFIRMED
```

## After Completion

Update findings list based on validation results:

- CONFIRMED: Keep original severity
- DOWNGRADED: Update to new severity
- FALSE_POSITIVE: Remove from report

Proceed to Phase 4 (if validated P0 findings) or Phase 5 (report).
