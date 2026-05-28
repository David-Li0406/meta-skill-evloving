---
name: investigate-root-cause
description: Use this skill for systematic investigation and root cause analysis of bugs or issues, especially when debugging persistent problems or understanding complex systems.
---

# Skill body

## When to Use

- After validating that a customer issue is reproducible
- When the same bug persists after multiple fix attempts
- When debugging complex system interactions
- Before making architectural decisions or creating fix specifications

## Quick Start

1. Review validation evidence (errors, screenshots, logs)
2. Search codebase for error signatures
3. Analyze code flow and data paths
4. Identify affected components and document findings
5. Check recent changes in the codebase

## Step-by-Step Instructions

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
```

### 5. Document Findings
- Clearly document the root cause, affected components, and any potential fixes or recommendations for future prevention.
```yaml
documentation:
  - Root cause identified
  - Affected components listed
  - Suggested fixes or improvements
```