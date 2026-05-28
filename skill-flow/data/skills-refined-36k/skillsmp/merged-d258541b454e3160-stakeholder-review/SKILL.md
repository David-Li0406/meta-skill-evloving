---
name: stakeholder-review
description: Use this skill to conduct multi-perspective quality reviews of implementation changes, ensuring validation from various stakeholders before user approval.
---

# Skill: stakeholder-review

Multi-perspective stakeholder review gate for implementation quality assurance.

## Purpose

Run parallel stakeholder reviews of implementation changes to identify concerns from multiple perspectives (architecture, security, quality, testing, performance, legal, UX, sales, and marketing) before user approval.

## When to Use

- After implementation phase completes in `/cat:work`
- Before the user approval gate
- When significant code changes need multi-perspective validation

## Stakeholders

| Stakeholder | Reference | Focus |
|-------------|-----------|-------|
| requirements | @stakeholders/requirements.md | Requirement satisfaction verification |
| architect | @stakeholders/architect.md | System design, module boundaries, APIs |
| security | @stakeholders/security.md | Vulnerabilities, input validation |
| quality | @stakeholders/quality.md | Code quality, complexity, duplication |
| tester | @stakeholders/tester.md | Test coverage, edge cases |
| performance | @stakeholders/performance.md | Efficiency, resource usage |
| ux | @stakeholders/ux.md | Usability, accessibility, interaction design |
| sales | @stakeholders/sales.md | Customer value, competitive positioning |
| marketing | @stakeholders/marketing.md | Positioning, messaging, go-to-market |
| legal | @stakeholders/legal.md | Licensing, compliance, IP, data privacy |

## Process

<step name="analyze_context">

**Context-Aware Stakeholder Selection**

Analyze task context to determine which stakeholders are relevant, reducing token usage by skipping irrelevant reviewers.

### Selection Algorithm

1. Start with base set: [requirements] (always included)
2. Detect task type from PLAN.md or commit messages
3. Apply task type inclusions/exclusions
4. Scan task description/goal for keywords
5. Apply keyword inclusions
6. Check version PLAN.md for focus keywords
7. Apply version focus inclusions
8. Output: selected_stakeholders, skipped_with_reasons

### Task Type Mappings

Detect task type from PLAN.md `## Type` field or infer from commit messages/description:

| Task Type | Include | Exclude |
|-----------|---------|---------|
| documentation | requirements | architect, security, quality, tester, performance, ux, sales, marketing |
| refactor | architect, quality, tester | ux, sales, marketing |
| bugfix | requirements, quality, tester, security | sales, marketing |
| performance | performance, architect, tester | ux, sales, marketing |

### Keyword Mappings

Scan task description, goal, and PLAN.md for keywords:

| Keywords | Include |
|----------|---------|
| "license", "compliance", "legal" | legal |
| "UI", "frontend", "user interface" | ux |
| "API", "endpoint", "public" | architect, security, marketing |
| "internal", "tooling", "CLI" | architect, quality (exclude ux, sales, marketing) |
| "security", "auth", "permission" | security |

### Version Focus Mapping

Check version PLAN.md for strategic focus:

- If version PLAN.md mentions "commercialization" → include legal, sales, marketing

### File-Based Overrides (Review Mode Only)

In review mode, file changes can override context exclusions.

</step>

<step name="prepare">

**Prepare review context:**

1. Identify files changed in implementation
2. Get diff summary for reviewers
3. Use stakeholder selection from analyze_context step

```bash
# Get changed files
CHANGED_FILES=$(git diff --name-only HEAD~1..HEAD 2>/dev/null || git diff --name-only --cached)

# Detect primary language from file extensions
PRIMARY_LANG=$(echo "$CHANGED_FILES" | grep -oE '\.[a-z]+$' | sort | uniq -c | sort -rn | head -1 | awk '{print $2}' | tr -d '.')
# Maps: java, py, ts, js, go, rs, etc.

# Categorize by type (language-agnostic patterns)
SOURCE_FILES=$(echo "$CHANGED_FILES" | grep -E '\.(java|py|ts|js|go|rs|c|cpp|cs)$' || true)
TEST_FILES=$(echo "$CHANGED_FILES" | grep -E '(Test|Spec|_test|_spec)\.' || true)
CONFIG_FILES=$(echo "$CHANGED_FILES" | grep -E '\.(json|yaml|yml|xml|properties|toml)$' || true)

# Check for language supplement
LANG_SUPPLEMENT=""
if [[ -f ".claude/cat/references/stakeholders/lang/${PRIMARY_LANG}.md" ]]; then
    LANG_SUPPLEMENT=$(cat ".claude/cat/references/stakeholders/lang/${PRIMARY_LANG}.md")
fi
```

</step>

<step name="spawn_reviewers">

**Spawn stakeholder subagents in parallel:**

For each relevant stakeholder, spawn a subagent with:

```
You are the {stakeholder} stakeholder reviewing an implementation.

## Your Role
{content of stakeholders/{stakeholder}.md}

## Language-Specific Patterns
{content of LANG_SUPPLEMENT if available, otherwise "No language supplement loaded."}

## Files to Review
{list of changed files relevant to this stakeholder}

## Diff Summary
{git diff output or summary}

## Instructions
1. Review the implementation against your stakeholder criteria
2. Apply language-specific red flags from the supplement (if loaded)
3. Identify concerns at CRITICAL, HIGH, or MEDIUM severity
4. Return your assessment in the specified JSON format
5. Be specific about locations and recommendations

Return ONLY valid JSON matching the format in your stakeholder definition.
```

Use `/cat:spawn-subagent` or `Task` tool with subagent_type for each stakeholder.

</step>

<step name="collect_reviews">

**Collect and parse stakeholder reviews:**

Wait for all stakeholder subagents to complete. Parse each response as JSON:

```json
{
  "stakeholder": "architect|security|quality|tester|performance|ux|sales|marketing|legal",
  "approval": "APPROVED|CONCERNS|REJECTED",
  "concerns": [...],
  "summary": "..."
}
```

Handle parse failures gracefully - if a stakeholder returns invalid JSON, treat as CONCERNS with a note about the parse failure.

</step>

<step name="aggregate">

**Aggregate and evaluate severity:**

Count concerns across all stakeholders:

```bash
CRITICAL_COUNT=0
HIGH_COUNT=0
REJECTED_COUNT=0

for review in reviews:
    if review.approval == "REJECTED":
        REJECTED_COUNT++
    for concern in review.concerns:
        if concern.severity == "CRITICAL":
            CRITICAL_COUNT++
        elif concern.severity == "HIGH":
            HIGH_COUNT++
```

**Decision rules:**

| Condition | Decision |
|-----------|----------|
| CRITICAL_COUNT > 0 | REJECTED - Must fix critical issues |
| REJECTED_COUNT > 0 | REJECTED - Stakeholder rejected |
| HIGH_COUNT >= 3 | REJECTED - Too many high concerns |
| HIGH_COUNT > 0 | CONCERNS - Document but proceed |
| Otherwise | APPROVED - Proceed to user approval |

</step>

<step name="report">

**Generate review report:**

```markdown
## Stakeholder Review Summary

**Status:** {APPROVED|CONCERNS|REJECTED}

### Stakeholder Results

| Stakeholder | Status | Critical | High | Medium |
|-------------|--------|----------|------|--------|
| requirements | {status} | {count} | {count} | {count} |
| architect | {status} | {count} | {count} | {count} |
| security | {status} | {count} | {count} | {count} |
| quality | {status} | {count} | {count} | {count} |
| tester | {status} | {count} | {count} | {count} |
| performance | {status} | {count} | {count} | {count} |
| ux | {status} | {count} | {count} | {count} |
| sales | {status} | {count} | {count} | {count} |
| marketing | {status} | {count} | {count} | {count} |
| legal | {status} | {count} | {count} | {count} |

### Critical Concerns (Must Fix)
{list of critical concerns with locations and recommendations}

### High Priority Concerns
{list of high concerns}

### Medium Priority Concerns (Informational)
{list of medium concerns}
```

</step>

<step name="decide">

**Take action based on result:**

**If REJECTED:**

Behavior depends on trust level:

| Trust | Rejection Behavior |
|-------|-------------------|
| `low` | Ask user: Fix / Override / Abort |
| `medium` | Auto-loop to fix (up to 3 iterations) |

Note: `trust: "high"` skips review entirely, so rejection handling doesn't apply.

For `trust: "low"`:
1. Present concerns to user with clear explanation
2. Ask user how to proceed:
   - "Fix concerns" → Return to implementation phase with concern list
   - "Override and proceed" → Continue to user approval with concerns noted
   - "Abort task" → Stop execution

For `trust: "medium"`:
1. Automatically loop back to implementation phase with concern list
2. No user prompt required
3. Escalate to user only after 3 failed fix attempts

**If CONCERNS:**
1. Note concerns in task documentation
2. Proceed to user approval gate
3. Include concern summary in approval presentation

**If APPROVED:**
1. Proceed directly to user approval gate
2. Note that stakeholder review passed

</step>

## Output Format

Return structured result for integration with work:

```json
{
  "review_status": "APPROVED|CONCERNS|REJECTED",
  "stakeholder_results": {
    "requirements": {"status": "...", "concerns": [...]},
    "architect": {"status": "...", "concerns": [...]},
    "security": {"status": "...", "concerns": [...]},
    "quality": {"status": "...", "concerns": [...]},
    "tester": {"status": "...", "concerns": [...]},
    "performance": {"status": "...", "concerns": [...]},
    "ux": {"status": "...", "concerns": [...]},
    "sales": {"status": "...", "concerns": [...]},
    "marketing": {"status": "...", "concerns": [...]},
    "legal": {"status": "...", "concerns": [...]}
  },
  "aggregated_concerns": {
    "critical": [...],
    "high": [...],
    "medium": [...]
  },
  "summary": "Brief summary of review outcome",
  "action_required": "none|fix_concerns|user_decision"
}
```

## Integration with work

This skill is invoked automatically after the implementation phase:

```
Implementation Phase
       ↓
  Build Verification
       ↓
  Stakeholder Review ← This skill
       ↓
  [If REJECTED] → Fix concerns → Loop back to implementation
       ↓
  [If APPROVED/CONCERNS] → User Approval Gate
       ↓
  Merge to main
```

## When to Run (Automatic Triggering)

Review triggering depends on verify level (NOT trust level):

| Verify | Action |
|--------|--------|
| `none` | Skip all stakeholder reviews |
| `changed` | Run stakeholder reviews |
| `all` | Run stakeholder reviews |

```bash
VERIFY_LEVEL=$(jq -r '.verify // "changed"' .claude/cat/cat-config.json)
if [[ "$VERIFY_LEVEL" == "none" ]]; then
  # Skip stakeholder review entirely
fi
```

**High-risk detection** (informational, for risk assessment display):
- Risk section mentions "breaking change", "data loss", "security", "production"
- Task modifies authentication, authorization, or payment code
- Task touches 5+ files
- Task modifies public APIs or interfaces
- Task involves database schema changes