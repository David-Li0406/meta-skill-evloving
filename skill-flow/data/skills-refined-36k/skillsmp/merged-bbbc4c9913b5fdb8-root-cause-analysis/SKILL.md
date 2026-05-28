---
name: root-cause-analysis
description: Use this skill for systematic investigation and root cause analysis of bugs or issues, especially when debugging persistent problems or understanding complex systems.
---

# Root Cause Analysis

This skill provides a structured approach to investigate and identify the root cause of issues through systematic analysis and debugging.

## When to Use

- After validating that a customer issue is reproducible
- When the same bug persists after multiple fix attempts
- When debugging complex system interactions
- Before making architectural decisions
- When error messages need tracing to source code
- When investigating production incidents

## Quick Start

1. Review validation evidence (errors, screenshots, logs)
2. Search codebase for error signatures
3. Trace through call paths and data flow
4. Identify affected components
5. Document root cause and affected areas

## Investigation Workflow

### 1. Review Validation Evidence
```yaml
evidence_review:
  - Console errors from validation
  - Network failures and API responses  
  - Screenshots showing the issue state
  - Timing data (performance issues)
  - Stack traces if available
```

### 2. Search for Error Signatures
Use search tools to find related code:
```yaml
search_patterns:
  error_messages:
    - Search for exact error text from console
    - Look for exception messages
    - Find logging statements near the error
  
  component_search:
    - Identify UI component from screenshots
    - Search for element IDs/classes
    - Find event handlers for user actions
  
  api_endpoints:
    - Locate controller/endpoint from network logs
    - Find service methods being called
    - Trace database queries involved
```

### 3. Analyze Code Flow
```yaml
code_analysis:
  entry_point:
    - Start from user action (button click, form submit)
    - Trace through event handlers
    - Follow API calls
  
  data_flow:
    - Track data from input to processing
    - Identify transformations
    - Find validation points
  
  error_points:
    - Locate try/catch blocks
    - Find error handling logic
    - Identify missing error cases
```

### 4. Check Recent Changes
```yaml
change_investigation:
  git_history:
    - Check commits to affected files (last 30 days)
    - Review PRs that touched this area
    - Look for related deployments
  
  dependency_updates:
    - Package updates that might affect behavior
    - API version changes
    - Database schema modifications
```

### 5. Root Cause Identification
#### Common Root Cause Patterns
- **Race Conditions**: Missing await on async operations.
- **Null Reference**: Not checking for null before accessing properties.
- **Timeout Issues**: Default timeout too short for operations.
- **State Management**: State not updating correctly due to async operations.

### 6. Document Findings
```yaml
root_cause_report:
  issue_summary: "Description of the issue"
  
  root_cause:
    description: "Detailed explanation of the root cause"
    file: "File where the issue was found"
    line: "Line number"
    method: "Method name"
    
  code_snippet: |
    // Code snippet illustrating the issue
    
  why_it_fails:
    - "Explanation of why the issue occurs"
    
  when_introduced:
    commit: "Commit hash"
    date: "Date of introduction"
    pr: "Pull request number"
    author: "Author's email"
```

### 7. Impact Analysis
```yaml
impact_assessment:
  direct_impact:
    - Files that need modification
    - Methods that need updates
    - Tests that will be affected
  
  side_effects:
    - Other features using the same code
    - Performance implications
    - Security considerations
  
  risk_level:
    low: "Isolated change, well-tested area"
    medium: "Affects shared components"
    high: "Core system change, multiple dependencies"
```

### 8. Investigation Queries
#### Find Error Patterns
```bash
# Search for error message
grep -r "error_message" --include="*.cs" --include="*.js"

# Find recent changes to relevant code
git log -p --since="30 days ago" -- "path/to/file"
```

#### Analyze Dependencies
```bash
# Check package versions
cat package.json | grep -A2 -B2 "dependency_name"

# Find API calls
grep -r "fetch.*api_call" --include="*.js"
```

## Success Criteria
- [ ] Root cause identified with specific code location
- [ ] Understanding of why the issue occurs
- [ ] Timeline of when the issue was introduced
- [ ] Impact assessment completed
- [ ] Fix approach identified

## Output
- Root cause analysis document
- Affected code locations
- Recommended fix approach
- Risk assessment for changes

## References
- [How to Debug](https://blog.regehr.org/archives/199) - Systematic debugging by John Regehr
- [The Scientific Method of Debugging](https://www.brendangregg.com/blog/2016-02-08/linux-load-averages.html) - Brendan Gregg
- [Debugging: The 9 Indispensable Rules](https://debuggingrules.com/)
- [Systems Performance](https://www.brendangregg.com/systems-performance-2nd-edition-book.html) - Investigation methodologies