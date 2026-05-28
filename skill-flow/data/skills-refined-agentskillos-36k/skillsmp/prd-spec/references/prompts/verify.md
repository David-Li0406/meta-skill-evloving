<context>
- Manifest: @docs/prd/features-manifest.json
- Feature files: @docs/prd/features/
- Arguments: $ARGUMENTS (scenario-id | "all" | "failing")
</context>

<task>
Verify one or more BDD scenarios and update the features manifest with pass/fail status.
</task>

<arguments>
| Argument | Description |
|----------|-------------|
| `US-001-S01` | Verify a specific scenario by ID |
| `all` | Verify all scenarios |
| `failing` | Verify only scenarios with `passes: false` |
| (none) | Same as `failing` |
</arguments>

<workflow>

## 1. Parse Arguments

Determine which scenarios to verify:
- If specific ID: find that scenario in the manifest
- If `all`: verify all scenarios in order
- If `failing` or empty: filter to `passes: false` scenarios

## 2. Load Manifest

Read `docs/prd/features-manifest.json`. If it doesn't exist, inform user to run `bdd-feature-split` first.

## 3. Verify Each Scenario

For each scenario to verify, execute based on `verificationMethod`:

### Automated Verification
1. Check if `testFile` is set and exists
2. If test file exists, run the test suite for that specific test
3. Parse test results to determine pass/fail
4. If no test file, check if implementation exists that satisfies the scenario

### Browser Verification
1. Display the verification steps to the user
2. If browser MCP or Puppeteer is available:
   - Navigate to the application
   - Execute each step programmatically
   - Capture screenshots as evidence
3. If no browser automation:
   - Present steps as a checklist
   - Ask user to confirm each step passes
4. Record pass/fail based on execution or user confirmation

### Manual Verification
1. Display the scenario title, steps, and success metrics
2. Present a checklist format
3. Ask user to confirm: "Does this scenario pass? (yes/no/skip)"
4. Record user's response

## 4. Update Manifest

For each verified scenario:
```json
{
  "passes": true | false,
  "lastVerified": "2024-01-21T14:30:00Z",
  "notes": "Optional notes from verification"
}
```

Update summary counts:
```json
{
  "summary": {
    "passing": <count where passes=true>,
    "failing": <count where passes=false>,
    "passingByPriority": {
      "P0": <count>,
      "P1": <count>,
      "P2": <count>
    }
  },
  "lastUpdated": "2024-01-21T14:30:00Z"
}
```

## 5. Report Results

Display a summary:
```
Verification Results
====================

Verified: 3 scenarios
  Passing: 2
  Failing: 1

Details:
  US-001-S01: PASS (automated)
  US-001-S02: PASS (browser)
  US-002-S01: FAIL (manual) - "Button not visible on mobile"

Overall Progress: 5/15 scenarios passing (33%)
  P0: 2/6 (33%)
  P1: 2/5 (40%)
  P2: 1/4 (25%)
```
</workflow>

<verification_strategies>

## Automated Strategy

For scenarios marked `automated`:

1. **Test file exists**: Run `npm test -- --grep "scenario-id"` or equivalent
2. **No test file**:
   - Look for implementation that matches scenario intent
   - Check if API endpoints/functions exist
   - Verify database schema supports the scenario
   - Mark as PASS if implementation appears complete, FAIL otherwise

## Browser Strategy

For scenarios marked `browser`:

1. **With browser automation (MCP/Puppeteer)**:
   - Launch browser to application URL
   - Execute steps programmatically:
     - "Select 15 topics" → find and click topic elements
     - "Initiate partner discovery" → click the button
     - "Verify counter shows" → assert element text
   - Take screenshots for evidence
   - Auto-determine pass/fail from assertions

2. **Without browser automation**:
   - Display steps as numbered checklist
   - Ask: "Please manually verify in your browser. Does this pass?"
   - Accept yes/no/skip response

## Manual Strategy

For scenarios marked `manual`:

1. Display scenario in readable format:
   ```
   Scenario: US-001-S01 - User sees welcome message

   Steps to verify:
   1. Navigate to the home page
   2. Check that welcome message is visible
   3. Verify message text matches expected copy

   Success metrics:
   - Welcome message displays within 2 seconds
   - Text is readable on all screen sizes
   ```

2. Ask: "Does this scenario pass? (yes/no/skip)"

3. If no, ask: "What failed? (brief description)"

</verification_strategies>

<output>
1. Progress indicator during verification
2. Per-scenario result (PASS/FAIL/SKIP)
3. Summary statistics
4. Updated manifest saved to disk
5. Recommendations for next steps (e.g., "3 P0 scenarios still failing")
</output>

<definition_of_done>
- All requested scenarios have been verified
- Manifest updated with pass/fail status and timestamps
- Summary counts recalculated correctly
- User informed of results and next steps
</definition_of_done>
