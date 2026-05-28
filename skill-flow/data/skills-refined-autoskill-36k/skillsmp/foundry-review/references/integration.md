# Integration with SDD Workflow

## When to Invoke

Fidelity reviews can be triggered at multiple points in the development workflow:

**1. After task completion (Optional verification):**
   - Optional verification step for critical tasks
   - Ensures task acceptance criteria fully met
   - Particularly useful for high-risk tasks (auth, data handling, API contracts)
   - Can be automated via verification task metadata

**2. Phase completion (Recommended):**
   - Review entire phase before moving to next phase
   - Catch drift early before it compounds
   - Best practice: Use at phase boundaries
   - Prevents accumulated technical debt

**3. Spec completion (Pre-PR audit):**
   - Final comprehensive audit before PR creation
   - Run phase-by-phase reviews for better quality
   - Ensures PR matches spec intent
   - Documents any deviations for PR description

**4. PR review (Automated compliance):**
   - Automated or manual PR compliance checks
   - Verify changes align with original specification
   - Useful for reviewer context and validation

## Review Outcome Handling

The `foundry-review` skill hands its synthesized results—JSON findings plus the saved JSON report reference—directly back to the caller. The invoking workflow decides what to do next. Common follow-up actions the main agent may optionally consider include journaling deviations, planning remediation work, running regression tests, or proposing spec updates after stakeholder review. No automatic delegation occurs; the fidelity-review skill's responsibility ends once it delivers the consensus results and report pointer.

## Report Handoff

Fidelity review generates a detailed report comparing implementation against specification:

**Usage Pattern:**
1. Skill executes `mcp__plugin_foundry_foundry-mcp__review action="fidelity"` directly via MCP
2. The tool analyzes implementation, generates JSON output, and saves the JSON consensus report in `.fidelity-reviews/`
3. Skill parses the JSON, presents the summarized findings, and surfaces the stored report path to the caller
