---
name: skill-validator
description: Validate skills against production-level criteria. Use when reviewing, auditing, or improving skills to ensure they meet quality standards. Evaluates structure, content quality, user interaction patterns, documentation completeness, domain standards compliance, and technical robustness. Returns actionable validation report with scores and improvement recommendations.
---

# Skill Validator

Validate any skill against production-level quality criteria.

## Validation Workflow

### Phase 1: Gather Context

1. **Read the skill's SKILL.md** completely
2. **Identify skill type** from frontmatter description:
   - Builder skill (creates artifacts)
   - Guide skill (provides instructions)
   - Automation skill (executes workflows)
   - Hybrid skill (combination)
3. **Read all reference files** in `references/` directory
4. **Check for assets/scripts** directories

### Phase 2: Apply Criteria

Evaluate against **7 criteria categories**. Each criterion scores 0-3:
- **0**: Missing/Absent
- **1**: Present but inadequate
- **2**: Adequate implementation
- **3**: Excellent implementation

---

## Criteria Categories

### 1. Structure & Anatomy (Weight: 15%)

| Criterion | What to Check |
|-----------|---------------|
| **SKILL.md exists** | Root file present |
| **Line count** | <500 lines (context is precious) |
| **Frontmatter** | `name` and `description` present in YAML |
| **Description quality** | Triggers: when to use, what it does, key features |
| **No extraneous files** | No README.md, CHANGELOG.md, LICENSE in skill dir |
| **Progressive disclosure** | Details in `references/`, not bloated SKILL.md |
| **Asset organization** | Templates in `assets/`, scripts in `scripts/` |

**Fail condition**: Missing SKILL.md or >800 lines = automatic fail

### 2. Content Quality (Weight: 20%)

| Criterion | What to Check |
|-----------|---------------|
| **Conciseness** | No verbose explanations, context is public good |
| **Imperative form** | Instructions use "Do X" not "You should do X" |
| **Appropriate freedom** | Constraints where needed, flexibility where safe |
| **Scope clarity** | Clear what skill does AND does not do |
| **No hallucination risk** | No instructions that encourage making up info |
| **Output specification** | Clear expected outputs defined |

### 3. User Interaction (Weight: 15%)

| Criterion | What to Check |
|-----------|---------------|
| **Clarification triggers** | Asks questions before acting on ambiguity |
| **Required vs optional** | Distinguishes must-know from nice-to-know |
| **Graceful handling** | What to do when user doesn't answer |
| **No over-asking** | Doesn't ask obvious or inferrable questions |
| **Context awareness** | Uses available context before asking |

**Key pattern to look for**:
```markdown
## Required Clarifications
1. Question about X
2. Question about Y

## Optional Clarifications
3. Question about Z (if relevant)
```

### 4. Documentation & References (Weight: 15%)

| Criterion | What to Check |
|-----------|---------------|
| **Source URLs** | Official documentation links provided |
| **Reference files** | Complex details in `references/` not main file |
| **Fetch guidance** | Instructions to fetch docs for unlisted patterns |
| **Version awareness** | Notes about checking for latest patterns |
| **Example coverage** | Good/bad examples for key patterns |

**Key pattern to look for**:
```markdown
| Resource | URL | Use For |
|----------|-----|---------|
| Official Docs | https://... | Complex cases |
```

### 5. Domain Standards (Weight: 15%)

| Criterion | What to Check |
|-----------|---------------|
| **Best practices** | Follows domain conventions (e.g., WCAG, OWASP) |
| **Enforcement mechanism** | Checklists, validation steps, must-verify items |
| **Anti-patterns** | Lists what NOT to do |
| **Quality gates** | Output checklist before delivery |

**Key pattern to look for**:
```markdown
### Must Follow
- [ ] Requirement 1
- [ ] Requirement 2

### Must Avoid
- Antipattern 1
- Antipattern 2
```

### 6. Technical Robustness (Weight: 10%)

| Criterion | What to Check |
|-----------|---------------|
| **Error handling** | Guidance for failure scenarios |
| **Security considerations** | Input validation, secrets handling if relevant |
| **Dependencies** | External tools/APIs documented |
| **Edge cases** | Common edge cases addressed |
| **Testability** | Can outputs be verified? |

### 7. Maintainability (Weight: 10%)

| Criterion | What to Check |
|-----------|---------------|
| **Modularity** | References are self-contained topics |
| **Update path** | Easy to update when standards change |
| **No hardcoded values** | Uses placeholders/variables where appropriate |
| **Clear organization** | Logical section ordering |

---

## Scoring Guide

### Category Scores

Calculate each category score:
```
Category Score = (Sum of criterion scores) / (Max possible) * 100
```

### Overall Score

```
Overall = Σ(Category Score × Weight)
```

### Rating Thresholds

| Score | Rating | Meaning |
|-------|--------|---------|
| 90-100 | **Production** | Ready for wide use |
| 75-89 | **Good** | Minor improvements needed |
| 60-74 | **Adequate** | Functional but needs work |
| 40-59 | **Developing** | Significant gaps |
| 0-39 | **Incomplete** | Major rework required |

---

## Output Format

Generate validation report:

```markdown
# Skill Validation Report: [skill-name]

**Rating**: [Production/Good/Adequate/Developing/Incomplete]
**Overall Score**: [X]/100

## Summary
[2-3 sentence assessment]

## Category Scores

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Structure & Anatomy | X/100 | 15% | X |
| Content Quality | X/100 | 20% | X |
| User Interaction | X/100 | 15% | X |
| Documentation | X/100 | 15% | X |
| Domain Standards | X/100 | 15% | X |
| Technical Robustness | X/100 | 10% | X |
| Maintainability | X/100 | 10% | X |

## Critical Issues (if any)
- [Issue requiring immediate fix]

## Improvement Recommendations
1. **High Priority**: [Specific action]
2. **Medium Priority**: [Specific action]
3. **Low Priority**: [Specific action]

## Strengths
- [What skill does well]
```

---

## Quick Validation Checklist

For rapid assessment, check these critical items:

- [ ] SKILL.md <500 lines
- [ ] Frontmatter has name + description
- [ ] No README.md/CHANGELOG.md in skill directory
- [ ] Has clarification questions for builder skills
- [ ] Has official documentation links
- [ ] Has enforcement checklist (if domain standards exist)
- [ ] Has output specification
- [ ] References exist for complex details

**If 6+ checked**: Likely Good or better
**If 4-5 checked**: Likely Adequate
**If <4 checked**: Needs significant work

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/detailed-criteria.md` | Deep evaluation of specific criterion |
| `references/scoring-examples.md` | Example validations for calibration |
| `references/improvement-patterns.md` | Common fixes for common issues |

---

## Usage Examples

### Validate a skill
```
Validate the chatgpt-widget-creator skill against production criteria
```

### Quick audit
```
Quick validation check on mcp-builder skill
```

### Focused review
```
Check if skill-creator skill has proper user interaction patterns
```
