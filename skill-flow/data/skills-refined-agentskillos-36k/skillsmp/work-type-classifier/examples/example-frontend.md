# Example: Frontend Work Classification

## User Request
"Create a new user profile page with avatar upload"

## Classification Output

### Keyword Analysis

| Keyword | Found | Weight |
|---------|-------|--------|
| page | ✅ | +3 FRONTEND |
| user | ❌ | neutral |
| profile | ❌ | neutral |
| avatar | ❌ | neutral |
| upload | ✅ | +1 FRONTEND |

### Work Type Decision

```yaml
work_type: FRONTEND
confidence: 0.85
reasoning: |
  - "page" indicates UI component work
  - "upload" typically involves frontend file handling
  - No API/database keywords detected
```

### Skills to Invoke

```yaml
skills_to_invoke:
  discipline:
    - superpowers:brainstorming
    - superpowers:test-driven-development
    - superpowers:verification-before-completion
  domain_specific:
    - frontend-design  # For UI/UX decisions
    - webapp-testing   # For visual verification
```

### Output to auto-context.yaml

```yaml
work_type: FRONTEND
detected_at: "2025-01-18T10:00:00Z"
keywords_found:
  - page
  - upload
skills_to_invoke:
  discipline:
    - superpowers:brainstorming
    - superpowers:test-driven-development
  domain_specific:
    - frontend-design
    - webapp-testing
```
