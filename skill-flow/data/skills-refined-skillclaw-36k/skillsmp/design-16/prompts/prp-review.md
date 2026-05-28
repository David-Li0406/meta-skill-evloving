# PRP Intelligent Review Prompt

You are reviewing a Product Requirements Prompt (PRP) for quality and completeness.

## Review Criteria

### 1. Clarity & Specificity
- [ ] Problem statement is concrete with quantified pain
- [ ] No vague terms: "properly", "quickly", "as needed", "etc."
- [ ] Scope boundaries are explicit (in/out of scope table)

### 2. Measurability
- [ ] All success metrics have current AND target values
- [ ] Targets are specific numbers, not ranges or "improved"
- [ ] Measurement methods are specified and practical

### 3. Validation Gates
- [ ] Each phase ends with a gate
- [ ] Gates have explicit pass/fail conditions (not just "review")
- [ ] Gate conditions use concrete thresholds
- [ ] "If gate fails" action is specified

### 4. Executable Commands
- [ ] Validation commands are copy-pasteable
- [ ] Commands match the specified tech stack
- [ ] Commands cover: tests, types, lint, build, health check

### 5. Risk Coverage
- [ ] External dependencies have fallbacks
- [ ] Security concerns are addressed
- [ ] Circuit breakers have specific thresholds

### 6. Internal Consistency
- [ ] Resources match phase requirements
- [ ] Timeline is realistic for scope
- [ ] Stakeholders cover all decision types
- [ ] State transitions match phases

### 7. Completeness
- [ ] No [FILL_THIS_IN] or {{VARIABLE}} placeholders remain
- [ ] All required sections are present
- [ ] Confidence score is calculated

## Severity Levels

- **BLOCKER**: Cannot proceed until fixed (missing gates, vague metrics)
- **MAJOR**: Significantly impacts quality (incomplete risks, missing commands)
- **MINOR**: Should fix but not blocking (formatting, minor gaps)
- **SUGGESTION**: Improvements for future iterations

## Review Output Format

```json
{
  "overall_status": "PASS" | "NEEDS_REVISION" | "REJECTED",
  "quality_score": 0-100,
  "issues": [
    {
      "severity": "BLOCKER|MAJOR|MINOR|SUGGESTION",
      "section": "section name",
      "line_hint": "relevant text snippet",
      "issue": "description of the problem",
      "fix": "specific suggestion to resolve"
    }
  ],
  "strengths": [
    "What the PRP does well"
  ],
  "summary": "1-2 sentence overall assessment"
}
```

## Example Review

**PRP Excerpt:**
```markdown
### Success Criteria
| Metric | Target |
|--------|--------|
| Page load | Fast |
| Errors | Reduced |

### Phase 1 Gate
Review with team and ensure quality.
```

**Review Output:**
```json
{
  "overall_status": "NEEDS_REVISION",
  "quality_score": 45,
  "issues": [
    {
      "severity": "BLOCKER",
      "section": "Success Criteria",
      "line_hint": "Page load | Fast",
      "issue": "Metric 'Fast' is not measurable - no specific threshold",
      "fix": "Change to: Page load (p95) | Current: unknown | Target: < 2s | Method: Datadog APM"
    },
    {
      "severity": "BLOCKER",
      "section": "Success Criteria",
      "line_hint": "Errors | Reduced",
      "issue": "Metric 'Reduced' is not measurable - no baseline or target",
      "fix": "Change to: Error rate | Current: 2.3% | Target: < 0.5% | Method: Error tracking"
    },
    {
      "severity": "BLOCKER",
      "section": "Phase 1 Gate",
      "line_hint": "Review with team and ensure quality",
      "issue": "Gate has no concrete pass/fail condition",
      "fix": "Add: GATE_1_PASS := tests_passing AND coverage > 0.8 AND security_review_approved"
    }
  ],
  "strengths": [],
  "summary": "PRP lacks measurable criteria and concrete gates. Cannot be executed as written."
}
```

## Your Task

Review the following PRP and provide structured feedback.

**Source Spec (for context):**
```markdown
{{SPEC_CONTENT}}
```

**PRP to Review:**
```markdown
{{PRP_CONTENT}}
```

**Output only valid JSON matching the review format above.**
