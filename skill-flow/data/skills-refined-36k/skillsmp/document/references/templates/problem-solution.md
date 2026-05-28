# Problem-Solution Template

Use this template for documenting difficult problems that were solved, including complex bugs, race conditions, or significant technical challenges.

## When to Use

- Documenting a complex bug fix
- Recording resolution of a race condition or concurrency issue
- Capturing solution to a difficult technical challenge
- Sharing lessons learned from debugging a hard problem

## Template Structure

```markdown
# {problem_title}

## Metadata

- **Timestamp**: {YYYY-MM-DD HH:MM:SS}
- **Project**: {project_name}
- **Category**: Problem-Solution
- **Tags**: {comma_separated_tags}
- **Related Commit**: {commit_hash if available}
- **Severity**: {Low/Medium/High/Critical}

## Problem Statement

Clear problem description:

- What was failing?
- What was the observable symptom?
- What was the impact?

## Context

Context information:

- When did it occur?
- Under what conditions?
- Which components were involved?

## Investigation Process

Steps taken to investigate:

1. Step 1: findings
2. Step 2: findings
3. Step 3: findings

### Root Cause

Detailed explanation of the problem's root cause.

## Solution

### Approach

Solution approach description:

- Why was this solution chosen?
- What alternatives were considered?

### Implementation

\`\`\`{language}
// Code showing the solution
\`\`\`

### Files Modified

- `path/to/file1.ext` - Changes made
- `path/to/file2.ext` - Changes made

## Verification

How the problem resolution was verified:

- Tests added
- Manual validation
- Metrics monitored

## Prevention

Measures to prevent similar problems in the future:

- Process changes
- Additional tests
- Updated documentation

## Lessons Learned

- Lesson 1
- Lesson 2
- Lesson 3
```

## Field Descriptions

### Metadata
- **Timestamp**: Auto-generated current date/time
- **Project**: Auto-detected from directory or git repo
- **Category**: Always "Problem-Solution"
- **Tags**: Relevant tags (bug type, component, severity)
- **Related Commit**: Git commit hash with the fix
- **Severity**: Impact level (Low/Medium/High/Critical)

### Problem Statement
Clear, concise description of what went wrong. Focus on observable behavior and impact.

### Context
Environmental and situational details:
- When/where did it occur?
- What conditions triggered it?
- What systems were affected?

### Investigation Process
Step-by-step investigation journey. Include:
- Hypotheses tested
- Tools used (logs, profilers, debuggers)
- Key findings at each step
- Dead ends explored

### Root Cause
Fundamental reason for the problem. Be specific and technical.

### Solution
Complete solution description:
- **Approach**: Why this solution over alternatives
- **Implementation**: Code showing the fix
- **Files Modified**: What changed and why

### Verification
Evidence the problem is solved:
- Automated tests added
- Manual testing performed
- Metrics showing improvement

### Prevention
Future-proofing measures:
- New tests to catch regressions
- Process improvements
- Documentation updates
- Monitoring additions

### Lessons Learned
Key takeaways from this experience. What would you do differently next time?
