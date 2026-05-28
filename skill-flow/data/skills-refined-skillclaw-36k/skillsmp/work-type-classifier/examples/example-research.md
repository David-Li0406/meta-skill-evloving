# Example: Research/Audit Classification

## User Request
"Analyze our authentication system for security vulnerabilities"

## Classification Output

### Keyword Analysis

| Keyword | Found | Weight |
|---------|-------|--------|
| analyze | ✅ | +3 RESEARCH |
| authentication | ✅ | neutral |
| security | ✅ | +2 RESEARCH (audit) |
| vulnerabilities | ✅ | +3 RESEARCH (audit) |

### Work Type Decision

```yaml
work_type: RESEARCH
subtype: SECURITY_AUDIT
confidence: 0.95
reasoning: |
  - "analyze" indicates investigation, not implementation
  - "security vulnerabilities" indicates audit task
  - No implementation keywords (create, add, build)
```

### Skills to Invoke

```yaml
skills_to_invoke:
  discipline:
    - superpowers:brainstorming  # For structured analysis
  domain_specific: []  # No implementation skills needed
  research:
    - security-audit-checklist  # Custom if available
```

### Skip Decisions

```yaml
skip:
  - task-decomposer      # No implementation tasks
  - parallel-orchestrator # No parallel execution
  - mutation-tester      # No code changes to test
  - verification-runner  # No code to verify
```

### Output to auto-context.yaml

```yaml
work_type: RESEARCH
subtype: SECURITY_AUDIT
detected_at: "2025-01-18T10:00:00Z"
keywords_found:
  - analyze
  - security
  - vulnerabilities
skills_to_invoke:
  discipline:
    - superpowers:brainstorming
  domain_specific: []
workflow_override:
  use_research_workflow: true
  skip_implementation_phases: true
output_expected:
  - Security audit report
  - Vulnerability assessment
  - Remediation recommendations
```

### Research Workflow Note

For RESEARCH work types, the workflow differs:
1. Skip Phase 3 (Planning for implementation)
2. Skip Phase 4 (Execution)
3. Skip Phase 5 (Integration)
4. Focus on investigation and reporting
