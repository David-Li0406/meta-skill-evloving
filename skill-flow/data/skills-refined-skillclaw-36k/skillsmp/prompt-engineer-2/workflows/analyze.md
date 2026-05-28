# Analyze Workflow

## Purpose

Analyze input prompt or requirements to determine optimization strategy.

---

## Transform Mode Analysis

**Analyze existing prompt for:**

### Structure Assessment

| Element | Check | Score |
|---------|-------|-------|
| Role definition | Clear persona? | 0-2 |
| Instructions | Step-by-step? | 0-2 |
| Format spec | Output defined? | 0-2 |
| Examples | Present? Quality? | 0-2 |
| Constraints | What not to do? | 0-2 |

**Total Score: X/10**

### Quality Issues

| Issue | Detection | Impact |
|-------|-----------|--------|
| Vague language | "should", "might", "could" | Inconsistent output |
| Missing context | No background | Hallucination risk |
| No examples | Zero examples | Format drift |
| Unclear format | No structure | Parsing difficulty |
| Missing constraints | No negatives | Edge case failures |

### Claude-Specific Check

- [ ] Uses XML tags
- [ ] Has thinking blocks (if complex)
- [ ] Leverages prefill
- [ ] Appropriate length
- [ ] Clear section separation

---

## Debug Mode Analysis

**Root Cause Analysis (RCA):**

```markdown
## Debug Analysis

### Symptom
[What's going wrong - user description]

### Expected Behavior
[What should happen]

### Actual Behavior
[What's happening]

### Hypothesis
1. [Possible cause 1]
2. [Possible cause 2]
3. [Possible cause 3]

### Evidence
- [Support for/against each hypothesis]

### Root Cause
[Most likely cause with evidence]

### Fix Strategy
[How to address]
```

### Common Root Causes

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| Wrong format | Unclear format spec | Add explicit format section |
| Hallucination | Missing context | Add context section |
| Inconsistent | No examples | Add 2-3 examples |
| Too verbose | No length constraint | Add length limit |
| Ignores instructions | Instruction order | Put critical rules first |

---

## Create Mode Analysis

**Requirements Extraction:**

```markdown
## Requirements Analysis

### Task Classification
- **Type**: [system/task/agent]
- **Domain**: [technical/creative/analytical/hybrid]
- **Complexity**: [simple/moderate/complex]

### Inputs
- Expected input format
- Input examples
- Edge cases

### Outputs
- Expected output format
- Success criteria
- Quality standards

### Constraints
- What to avoid
- Limitations
- Guardrails

### Context Needed
- Background info
- Domain knowledge
- Prior conversation
```

---

## Output: Analysis Report

```markdown
## Analysis Report

**Mode**: [transform/debug/create]
**Date**: [timestamp]

### Summary
[One paragraph assessment]

### Issues Found
1. [Issue 1] - [severity: HIGH/MEDIUM/LOW]
2. [Issue 2] - [severity]

### Recommendations
1. [Recommendation 1]
2. [Recommendation 2]

### Pattern Suggestion
[Recommended pattern based on analysis]

### Research Needed
- [Topic 1 for research subagent]
- [Topic 2]
```

---

## Version

**Version**: 1.0.0
