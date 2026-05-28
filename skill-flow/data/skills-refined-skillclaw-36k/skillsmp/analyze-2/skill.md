---
name: analyze
description: Analyze a specific topic and produce a comprehensive markdown report in docs/analysis/
allowed-tools: Bash, Task, Read, Edit, Write, Grep, Glob, WebSearch, WebFetch
---

# Analysis Skill

Conducts in-depth analysis on a specified topic and produces a comprehensive markdown report saved to `docs/analysis/`.

## Arguments

The skill takes a single argument: the analysis prompt describing what to analyze.

Examples:
- `/analyze the test coverage gaps in the iOS codebase`
- `/analyze authentication security patterns used in the backend`
- `/analyze performance bottlenecks in the question generation service`
- `/analyze code duplication across the project`

## Execution Steps

### Step 1: Parse the Analysis Request

Extract the topic from the user's prompt. The topic should describe what needs to be analyzed.

### Step 2: Generate Output Filename

Create a descriptive filename based on the topic:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Add timestamp prefix for uniqueness
- Example: `2024-01-15-ios-test-coverage-gaps.md`

```bash
# Generate timestamp
TIMESTAMP=$(date +%Y-%m-%d)
# The filename will be: docs/analysis/${TIMESTAMP}-<slugified-topic>.md
```

### Step 3: Conduct the Analysis

Based on the topic, gather relevant information by:

1. **Searching the codebase** using Glob and Grep tools to find relevant files and patterns
2. **Reading key files** to understand implementation details
3. **Using specialized agents** via the Task tool when needed:
   - Use `Explore` agent for codebase exploration
   - Use domain-specific agents for specialized analysis (e.g., `statistical-analysis-scientist` for statistical topics)
4. **Web research** if the topic requires external context or best practices comparison

### Step 4: Structure the Analysis

The analysis report should follow this structure:

```markdown
# Analysis: <Topic Title>

**Date:** <YYYY-MM-DD>
**Scope:** <Brief description of what was analyzed>

## Executive Summary

<2-3 paragraph high-level summary of findings>

## Methodology

<How the analysis was conducted>
- Tools and techniques used
- Files and directories examined
- External resources consulted (if any)

## Findings

### <Finding Category 1>

<Detailed findings with evidence>

#### Evidence
- File references with line numbers
- Code snippets where relevant
- Metrics or statistics

### <Finding Category 2>

<Continue with additional findings...>

## Recommendations

| Priority | Recommendation | Effort | Impact |
|----------|---------------|--------|--------|
| High | ... | ... | ... |
| Medium | ... | ... | ... |
| Low | ... | ... | ... |

### Detailed Recommendations

#### 1. <Recommendation Title>

**Problem:** <What issue this addresses>
**Solution:** <Proposed approach>
**Files Affected:** <List of files>

## Appendix

### Files Analyzed
<List of all files that were examined>

### Related Resources
<Links to documentation, best practices, etc.>
```

### Step 5: Write the Analysis File

Write the complete analysis to `docs/analysis/<filename>.md`:

```bash
# Ensure directory exists
mkdir -p docs/analysis
```

Then use the Write tool to create the file at `docs/analysis/${TIMESTAMP}-<topic-slug>.md`.

### Step 6: Summarize and Report

After writing the file, provide the user with:
1. The path to the generated analysis file
2. A brief summary of key findings
3. The top 3 recommendations

## Quality Standards

- **Thoroughness**: Examine all relevant areas of the codebase
- **Evidence-based**: Support all findings with specific file references and code examples
- **Actionable**: Recommendations should be concrete and implementable
- **Organized**: Use clear headings and consistent formatting
- **Balanced**: Present both strengths and areas for improvement

## Example Output Summary

After completing the analysis, report to the user:

```
Analysis complete. Report saved to: docs/analysis/2024-01-15-ios-test-coverage-gaps.md

Key Findings:
1. Test coverage is 45% overall, with ViewModels at 62% and Services at 38%
2. No tests exist for 12 critical authentication flows
3. UI snapshot tests are missing for all custom components

Top Recommendations:
1. [High] Add unit tests for AuthenticationService (estimated 15 test cases)
2. [High] Implement snapshot tests for reusable UI components
3. [Medium] Increase ViewModel test coverage to 80%
```

## Important Guidelines

1. **Be comprehensive**: Don't rush the analysis - examine all relevant code paths
2. **Cite sources**: Always include file paths and line numbers for findings
3. **Prioritize findings**: Not all issues are equally important
4. **Stay focused**: Keep the analysis relevant to the requested topic
5. **Use agents appropriately**: Delegate specialized analysis to domain experts via Task tool

Begin by parsing the analysis request and planning the investigation approach.
