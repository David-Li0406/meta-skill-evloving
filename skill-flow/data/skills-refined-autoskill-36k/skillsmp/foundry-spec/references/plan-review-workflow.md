# Plan Review Workflow

This reference describes how to get AI feedback on specifications using multi-model review.

## Overview

Multi-model review coordinates parallel AI reviewers to provide structured, categorized feedback on SDD specifications. It surfaces consensus findings, diverse perspectives, and prioritized recommendations.

**Core Philosophy:**
- **Diverse Perspectives**: Multiple AI models catch more issues than single review
- **Feedback, Not Gatekeeping**: Provides actionable feedback, not approval/rejection
- **Advisory Only**: Never modifies specifications - all findings are recommendations

## When to Use Review

**Use review when:**
- Spec is ready for implementation (draft complete)
- Complex specifications (>10 tasks, architectural decisions)
- Security-critical designs (auth, data, privacy)
- Tight deadlines requiring estimate validation
- Novel architectures with uncertain risks

**Skip review for:**
- Trivial specs (<5 tasks, standard patterns)
- Specs already in implementation (use `sdd-fidelity-review`)
- Exploratory or prototype work

## MCP Tooling

| Router | Actions | Purpose |
|--------|---------|---------|
| `review` | `spec-review`, `list-tools`, `list-plan-tools` | Execute reviews and list toolchains |
| `spec` | `completeness-check`, `duplicate-detection` | Automated quality checks |

## Review Types

| Type | Models | Duration | Focus | Use When |
|------|--------|----------|-------|----------|
| **quick** | 2 | 10-15 min | Completeness, Clarity | Simple specs, time-constrained |
| **full** | 3-4 | 20-30 min | All 6 dimensions | Complex specs, moderate-high risk |
| **security** | 2-3 | 15-20 min | Risk Management | Auth, data handling, compliance |
| **feasibility** | 2-3 | 10-15 min | Estimates, Dependencies | Tight deadlines, uncertain scope |

### Decision Matrix

| Condition | Review Type |
|-----------|-------------|
| Task count <= 10 AND no auth/payment/PII tasks | `quick` |
| Task count > 10 OR has architectural decisions | `full` |
| Contains auth, payment, encryption, or PII handling | `security` |
| Phase has deadline pressure OR external dependencies | `feasibility` |

**Priority when multiple conditions match:**
1. `security` (always takes precedence for sensitive data)
2. `full` (for complex specs)
3. `feasibility` (for time-constrained work)
4. `quick` (default fallback)

## Workflow Steps

### Step 1: Verify Available Tools

```bash
mcp__plugin_foundry_foundry-mcp__review action="list-tools"
```

Check which AI review toolchains are installed:
- Need at least 1 tool for basic review
- 2+ tools recommended for multi-model feedback
- All available tools ideal for comprehensive analysis

### Step 2: Run Quality Checks

Run automated checks before AI review to catch structural issues:

```bash
# Check spec completeness (metadata, descriptions, estimates)
mcp__plugin_foundry_foundry-mcp__spec action="completeness-check" spec_id="{spec-id}"

# Detect duplicate or overlapping tasks
mcp__plugin_foundry_foundry-mcp__spec action="duplicate-detection" spec_id="{spec-id}"
```

| Review Type | Recommended Quality Checks |
|-------------|---------------------------|
| `quick` | `completeness-check` (fast structural validation) |
| `full` | Both checks before AI review |
| `security` | `completeness-check` (ensure all security requirements specified) |
| `feasibility` | `duplicate-detection` (avoid double-counting estimates) |

### Step 3: Execute Review

```bash
mcp__plugin_foundry_foundry-mcp__review action="spec-review" spec_id="{spec-id}" review_type="{type}"
```

The tool automatically:
1. Initiates each model review in parallel
2. Collects responses as they complete (60-120s per tool)
3. Handles failures gracefully
4. Parses and synthesizes responses

### Step 4: Interpret Results

**Priority Levels:**
- **CRITICAL**: Security vulnerabilities, blockers - Address immediately
- **HIGH**: Design flaws, missing info - Address before implementation
- **MEDIUM**: Improvements, unclear requirements - Consider addressing
- **LOW**: Nice-to-have enhancements - Note for future

See `plan-review-consensus.md` for priority assignment details.

### Step 5: Synthesize & Report

1. Organize feedback by category and priority
2. Note reviewer consensus and diverse perspectives
3. Identify type of downstream work needed
4. Return report path for full context

### Step 6: Handoff

After completing the review:

1. Present summary to user with finding counts by priority level
2. Provide paths to full reports (markdown + JSON)
3. Ask if user wants to apply recommendations
4. Do NOT automatically proceed to modifications without user approval

## Output Format

Reports are written to `specs/.plan-reviews/{spec-id}-review-{type}.md`

Full results go to files; conversation receives summary only.

### Markdown Report Structure

```markdown
## Feedback Summary

### Risk Flags (CRITICAL)
1. Missing authentication on admin endpoints
   Priority: CRITICAL | Flagged by: gemini, codex
   Impact: Unauthorized access to sensitive operations
   Recommendation: Add JWT validation middleware

### Feasibility Questions (HIGH)
2. Time estimates may be unrealistic for Phase 2
   Priority: HIGH | Flagged by: codex
   Impact: Timeline risk - OAuth integration underestimated
   Recommendation: Revisit estimates (+50% suggested)
```

## Configuration Defaults

| Parameter | Value |
|-----------|-------|
| Min models required | 1 |
| Recommended models | 2+ |
| Timeout per model | 120s |
| Max review time | 300s |
