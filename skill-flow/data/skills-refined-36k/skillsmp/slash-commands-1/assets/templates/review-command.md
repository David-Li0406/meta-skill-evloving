# Review Command Template

Use this template for comprehensive analysis and review workflows.

```markdown
---
description: "[Review type] with optional focus areas"
argument-hint: "[review-aspects]"
allowed-tools: ["Bash", "Glob", "Grep", "Read", "Task"]
---

# [Review Type]

[High-level description of what this review does]

**Focus Areas (optional):** "$ARGUMENTS"

## Review Workflow:

1. **Determine Scope**
   - [How to identify what to review]
   - Parse arguments for specific focus areas
   - Default: [default behavior]

2. **Available Aspects:**
   - **aspect1** - [Description]
   - **aspect2** - [Description]
   - **aspect3** - [Description]
   - **all** - Run all reviews (default)

3. **Execute Reviews**
   - [Review execution details]

4. **Aggregate Results**
   - [How to combine findings]

## Output Format:

# Review Summary

## Critical Issues (X found)
- [aspect]: Issue description [file:line]

## Important Issues (X found)
- [aspect]: Issue description [file:line]

## Suggestions (X found)
- [aspect]: Suggestion [file:line]

## Strengths
- [What's done well]

## Usage Examples:

/command
/command aspect1 aspect2
/command all

## Tips:

- [Best practice 1]
- [Best practice 2]
```

## Example: Code Review

```markdown
---
description: "Comprehensive code review for recent changes"
argument-hint: "[security|performance|style|tests|all]"
allowed-tools: ["Bash", "Glob", "Grep", "Read"]
---

# Code Review

Review recent code changes for quality, security, and best practices.

**Focus Areas (optional):** "$ARGUMENTS"

## Changed Files

!`git diff --name-only HEAD~1`

## Review Workflow:

1. **Determine Scope**
   - Review files changed in last commit
   - If arguments provided, focus on those aspects only
   - Default: Run all applicable reviews

2. **Available Aspects:**
   - **security** - Check for vulnerabilities, input validation, auth issues
   - **performance** - Analyze complexity, memory, query efficiency
   - **style** - Verify naming, organization, documentation
   - **tests** - Evaluate test coverage and quality
   - **all** - Run all reviews (default)

3. **Execute Reviews**
   For each applicable aspect, analyze the changed files and identify issues.

4. **Aggregate Results**
   Combine findings by severity level.

## Output Format:

```markdown
# Code Review Summary

## Critical Issues
- [aspect]: Issue description [file:line]

## Important Issues  
- [aspect]: Issue description [file:line]

## Suggestions
- [aspect]: Suggestion [file:line]

## Strengths
- What's well-implemented
```

## Usage Examples:

```
/review                    # Full review
/review security           # Security only
/review security tests     # Security and tests
```

## Tips:

- Run before creating PR, not after
- Address critical issues first
- Re-run after making fixes
```

## Example: Documentation Review

```markdown
---
description: "Review documentation for accuracy and completeness"
argument-hint: "[api|readme|comments|all]"
allowed-tools: ["Bash", "Glob", "Grep", "Read"]
---

# Documentation Review

Check documentation for accuracy, completeness, and clarity.

**Focus Areas (optional):** "$ARGUMENTS"

## Review Workflow:

1. **Identify Documentation**
   - README files: !`find . -name "README*" -type f`
   - API docs: !`find . -path "*/docs/*" -name "*.md"`
   - Code comments in changed files

2. **Available Aspects:**
   - **api** - API documentation accuracy vs implementation
   - **readme** - README completeness and accuracy
   - **comments** - Code comment accuracy vs code behavior
   - **all** - Review all documentation (default)

3. **Check Each Aspect:**

   **API Documentation:**
   - Do endpoints match implementation?
   - Are parameters documented correctly?
   - Are examples current and working?

   **README:**
   - Is setup/installation current?
   - Are usage examples working?
   - Is the project description accurate?

   **Comments:**
   - Do comments match code behavior?
   - Are complex sections explained?
   - Is outdated information present?

## Output Format:

```markdown
# Documentation Review

## Inaccuracies Found
- [file:line] Description of mismatch

## Missing Documentation
- [area] What needs to be documented

## Outdated Content
- [file:line] What needs updating

## Well Documented
- [area] What's well-documented
```
```

## Example: Triage/Processing Review

```markdown
---
description: "Triage and label issues based on criteria"
allowed-tools: Bash(gh issue:*), TodoWrite
---

# Issue Triage

Systematically review and label issues based on defined criteria.

## Criteria

**Critical (needs-attention label):**
- Keywords: "crash", "data loss", "security", "broken"
- High engagement (50+ reactions/comments)
- Blocking core functionality

**Bug (bug label):**
- Reproducible issues
- Unexpected behavior
- Error messages

**Enhancement (enhancement label):**
- Feature requests
- Improvement suggestions
- "Would be nice" language

## Workflow:

1. **Get Issues to Triage**
   ```bash
   gh issue list --state open --limit 50 --json number,title,labels
   ```

2. **Create TODO List**
   Save all issue numbers and process each systematically.

3. **For Each Issue:**
   - View full details: `gh issue view <number> --json title,body,labels,comments`
   - Evaluate against criteria
   - Apply appropriate label if missing

4. **Summarize**
   - Issues labeled as critical
   - Issues labeled as bugs
   - Issues labeled as enhancements
   - Issues skipped (already labeled or unclear)

## Constraints:

- Process ALL issues in TODO list
- Don't comment on issues
- Only add labels, never remove
- Be conservative with critical label
```

## Tips

1. **Optional arguments** - Let users focus on specific aspects
2. **Show available options** - List what aspects are available
3. **Clear output format** - Define how results should be structured
4. **Usage examples** - Show different invocation patterns
5. **Practical tips** - Include workflow integration advice
6. **Severity levels** - Categorize findings by importance
