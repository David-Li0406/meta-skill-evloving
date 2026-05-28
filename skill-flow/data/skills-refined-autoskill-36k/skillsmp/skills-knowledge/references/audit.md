# Skill Quality Audit Framework

## Table of Contents

- [Overview](#overview)
- [Scoring Rubric](#scoring-rubric)
- [Dimension 1: Knowledge Delta (15 points)](#dimension-1-knowledge-delta-15-points)
- [Dimension 2: Autonomy (15 points)](#dimension-2-autonomy-15-points)
- [PDF Processing Workflow](#pdf-processing-workflow)
- [Dimension 3: Discoverability (15 points)](#dimension-3-discoverability-15-points)
- [Dimension 4: Progressive Disclosure (15 points)](#dimension-4-progressive-disclosure-15-points)
- [Dimension 5: Clarity (15 points)](#dimension-5-clarity-15-points)
- [Deploy Workflow](#deploy-workflow)
- [Dimension 6: Completeness (15 points)](#dimension-6-completeness-15-points)
- [Error Handling](#error-handling)
- [Dimension 7: Standards Compliance (15 points)](#dimension-7-standards-compliance-15-points)
- [Dimension 8: Security (10 points)](#dimension-8-security-10-points)
- [Dimension 9: Performance (10 points)](#dimension-9-performance-10-points)
- [Dimension 10: Maintainability (10 points)](#dimension-10-maintainability-10-points)
- [Dimension 11: Innovation (10 points)](#dimension-11-innovation-10-points)
- [Common Failure Patterns](#common-failure-patterns)
- [Audit Checklist](#audit-checklist)
- [Evaluation Protocol](#evaluation-protocol)
- [Example Audit](#example-audit)
- [Using the Audit Results](#using-the-audit-results)
- [Automation Tools](#automation-tools)
- [Best Practices](#best-practices)

Comprehensive 11-dimensional scoring system for evaluating skill quality.

## Overview

Skills are evaluated across 11 dimensions:
- **3 points each**: Dimensions 1-7 (exceptional importance)
- **2 points each**: Dimensions 8-11 (high importance)

**Total Score**: 150 points

## Scoring Rubric

- **A Grade (135-150 points)**: Excellent - Production ready, all best practices
- **B Grade (120-134 points)**: Good - Minor improvements needed
- **C Grade (105-119 points)**: Fair - Significant improvements recommended
- **D Grade (90-104 points)**: Poor - Major rework required
- **F Grade (<90 points)**: Failing - Complete rebuild recommended

## Dimension 1: Knowledge Delta (15 points)

**What it measures**: Expert-only knowledge vs what Claude already knows

**Evaluation criteria**:
- Provides unique value beyond base capabilities
- Contains specialized domain expertise
- Avoids obvious or generic information
- Focuses on expert decisions and trade-offs

**Scoring**:
- **15 points**: Highly specialized expertise, valuable context
- **10 points**: Good domain knowledge with some basics
- **5 points**: Mostly general knowledge
- **0 points**: No unique value

**Example (15 points)**:
```yaml
# Specialized domain knowledge
description: "PCI-DSS compliance patterns for payment processing. Use when implementing payment systems handling credit card data."

# Contains expert-only knowledge about compliance requirements, not general payment processing
```

**Example (0 points)**:
```yaml
# Generic knowledge Claude already knows
description: "Best practices for coding"
```

## Dimension 2: Autonomy (15 points)

**What it measures**: Completes 80-95% of tasks without questions

**Evaluation criteria**:
- Self-sufficient execution
- Clear workflows without ambiguity
- Handles edge cases
- Minimal user interaction required

**Scoring**:
- **15 points**: 95%+ autonomous, handles all scenarios
- **10 points**: 85%+ autonomous, minor clarifications
- **5 points**: 70% autonomous, needs frequent input
- **0 points**: Requires constant guidance

**Example (15 points)**:
```markdown
## PDF Processing Workflow

1. Extract text: Use pdfplumber
2. If scanned, use OCR: pytesseract
3. Handle errors: Check file validity
4. Output: Save to text file

Clear steps, handles edge cases, no questions needed.
```

## Dimension 3: Discoverability (15 points)

**What it measures**: Clear description triggers and activation

**Evaluation criteria**:
- Description includes natural trigger keywords
- Specific enough to avoid false positives
- Covers relevant use cases
- Auto-activates appropriately

**Scoring**:
- **15 points**: Perfect triggers, always found when needed
- **10 points**: Good triggers, occasionally missed
- **5 points**: Vague triggers, unpredictable activation
- **0 points**: No clear triggers

**Example (15 points)**:
```yaml
description: "Extract text and tables from PDF files. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction."

# Triggers: "PDF", "extract text", "forms", "document extraction"
# Natural keywords users actually say
```

## Dimension 4: Progressive Disclosure (15 points)

**What it measures**: Proper Tier 1/2/3 organization

**Evaluation criteria**:
- SKILL.md under 500 lines
- Tier 3 content in references/ and scripts/
- Clear linking between tiers
- Appropriate content distribution

**Scoring**:
- **15 points**: Perfect progressive disclosure, all content organized
- **10 points**: Good organization, minor issues
- **5 points**: Some progressive disclosure, mostly flat
- **0 points**: No progressive disclosure

**Example (15 points)**:
```
skill-name/
├── SKILL.md (200 lines) - Essentials + links
├── references/
│   ├── detailed.md (300 lines) - Full documentation
│   └── examples.md (150 lines) - Examples
└── scripts/
    └── validate.sh - Utility script
```

## Dimension 5: Clarity (15 points)

**What it measures**: Clear instructions and well-defined workflows

**Evaluation criteria**:
- Unambiguous instructions
- Logical workflow structure
- Understandable examples
- Easy to follow

**Scoring**:
- **15 points**: Crystal clear, cannot be misinterpreted
- **10 points**: Clear with minor ambiguities
- **5 points**: Some confusion possible
- **0 points**: Unclear and confusing

**Example (15 points)**:
```markdown
## Deploy Workflow

1. Verify environment is valid (dev/staging/prod)
2. Run tests: `npm test`
3. Build application: `npm run build`
4. Deploy: `kubectl apply -f k8s/$ENV.yaml`
5. Verify: `kubectl rollout status`

Each step is clear and unambiguous.
```

## Dimension 6: Completeness (15 points)

**What it measures**: Covers all scenarios and handles edge cases

**Evaluation criteria**:
- Comprehensive coverage
- Edge cases addressed
- Error handling included
- No critical gaps

**Scoring**:
- **15 points**: Complete coverage, handles everything
- **10 points**: Good coverage, minor gaps
- **5 points**: Partial coverage, some gaps
- **0 points**: Incomplete, many gaps

**Example (15 points)**:
```markdown
## Error Handling

- File not found: Create with default template
- Permission denied: Suggest alternative location
- Invalid format: Show accepted formats
- Network error: Retry with backoff
- All errors: Log details for debugging
```

## Dimension 7: Standards Compliance (15 points)

**What it measures**: Follows Agent Skills specification

**Evaluation criteria**:
- Valid YAML frontmatter
- Correct file structure
- Proper naming conventions
- URL fetching sections

**Scoring**:
- **15 points**: Perfect compliance
- **10 points**: Minor compliance issues
- **5 points**: Some compliance violations
- **0 points**: Major violations

**Checklist**:
- [ ] Valid YAML frontmatter
- [ ] Name matches directory
- [ ] Description follows WHAT+WHEN+NOT
- [ ] Has URL fetching sections
- [ ] Uses proper file paths

## Dimension 8: Security (10 points)

**What it measures**: Tool restrictions and safe execution

**Evaluation criteria**:
- Appropriate tool restrictions
- Input validation
- Safe execution patterns
- No security vulnerabilities

**Scoring**:
- **10 points**: Excellent security practices
- **7 points**: Good security, minor gaps
- **3 points**: Basic security
- **0 points**: Security issues

**Example (10 points)**:
```yaml
---
name: deploy
description: "Deploy to production"
disable-model-invocation: true
allowed-tools: Bash(kubectl:*), Bash(docker:*), Read
---

# Restricts tools to safe subset
# Only bash commands with specific patterns
```

## Dimension 9: Performance (10 points)

**What it measures**: Efficient workflows and minimal token usage

**Evaluation criteria**:
- Efficient tool selection
- Minimal context needed
- Optimized workflows
- Fast execution

**Scoring**:
- **10 points**: Highly optimized
- **7 points**: Good performance
- **3 points**: Acceptable performance
- **0 points**: Performance issues

**Best practices**:
- Use progressive disclosure
- Avoid redundant information
- Choose efficient tools
- Cache when appropriate

## Dimension 10: Maintainability (10 points)

**What it measures**: Well-structured content, easy to update

**Evaluation criteria**:
- Clear organization
- Logical structure
- Easy to modify
- Well-documented

**Scoring**:
- **10 points**: Highly maintainable
- **7 points**: Good structure
- **3 points**: Acceptable structure
- **0 points**: Hard to maintain

**Example (10 points)**:
```
skill-name/
├── SKILL.md - Main instructions
├── references/
│   ├── concepts.md - Core concepts
│   ├── examples.md - Examples
│   └── troubleshooting.md - Common issues
└── scripts/ - Utilities
```

## Dimension 11: Innovation (10 points)

**What it measures**: Unique value and creative solutions

**Evaluation criteria**:
- Novel approach
- Creative problem-solving
- Best-in-class methodology
- Unique contribution

**Scoring**:
- **10 points**: Highly innovative
- **7 points**: Some innovation
- **3 points**: Conventional approach
- **0 points**: No innovation

**Example (10 points)**:
```markdown
# Novel approach: Evaluation-driven skill development

Instead of writing documentation first, create evaluations that test actual gaps. This ensures skills solve real problems.
```

## Common Failure Patterns

### Pattern 1: Kitchen Sink
**Problem**: One skill tries to do everything
**Solution**: Split into focused skills

### Pattern 2: Indecisive Orchestrator
**Problem**: Too many paths, unclear direction
**Solution**: Define clear workflows

### Pattern 3: Pretend Executor
**Problem**: Scripts requiring constant guidance
**Solution**: Make scripts truly autonomous

### Pattern 4: Argumentative Consultant
**Problem**: Opinions without expertise
**Solution**: Focus on expert-only knowledge

### Pattern 5: Over-Documented
**Problem**: Everything in SKILL.md, no progressive disclosure
**Solution**: Move details to references/

### Pattern 6: Under-Documented
**Problem**: Too vague, missing critical information
**Solution**: Add specific examples and workflows

## Audit Checklist

### Pre-Audit
- [ ] Skill loaded and tested
- [ ] Auto-discovery verified
- [ ] Manual invocation tested
- [ ] Arguments tested (if applicable)

### Structural Audit
- [ ] YAML frontmatter valid
- [ ] Name matches directory
- [ ] Description follows formula
- [ ] SKILL.md under 500 lines
- [ ] Progressive disclosure implemented

### Content Audit
- [ ] Clear purpose and scope
- [ ] Specific triggers identified
- [ ] Actionable instructions
- [ ] Concrete examples provided
- [ ] Complete coverage

### Quality Audit
- [ ] Autonomy: Completes without questions
- [ ] Discoverability: Auto-activates correctly
- [ ] Standards: Follows specification
- [ ] Security: Appropriate restrictions

### Performance Audit
- [ ] Efficient tool selection
- [ ] Minimal token usage
- [ ] Fast execution
- [ ] Optimized workflows

## Evaluation Protocol

### Step 1: Load and Review
1. Load the skill
2. Review Tier 1 (metadata)
3. Check discoverability

### Step 2: Test Autonomy
1. Test with real scenarios
2. Verify completion without questions
3. Note any gaps or issues

### Step 3: Review Progressive Disclosure
1. Check SKILL.md length
2. Verify Tier 3 content exists
3. Test link functionality

### Step 4: Validate Standards
1. Check YAML frontmatter
2. Verify naming conventions
3. Review URL fetching

### Step 5: Score All Dimensions
1. Rate each dimension
2. Calculate total score
3. Assign grade

### Step 6: Identify Improvements
1. List high-impact changes
2. Prioritize by points gained
3. Create improvement plan

## Example Audit

### Skill: api-review

**Scores**:
- Knowledge Delta: 15/15 (Expert API design knowledge)
- Autonomy: 12/15 (Handles most cases, occasional clarification)
- Discoverability: 14/15 (Good triggers, sometimes missed)
- Progressive Disclosure: 10/15 (Some content in SKILL.md should be in references)
- Clarity: 13/15 (Clear instructions, minor ambiguities)
- Completeness: 11/15 (Good coverage, some edge cases missing)
- Standards Compliance: 13/15 (Valid YAML, URL fetching present)
- Security: 8/10 (Good tool restrictions)
- Performance: 7/10 (Some inefficiencies)
- Maintainability: 9/10 (Good structure)
- Innovation: 6/10 (Conventional approach)

**Total: 118/150 = C Grade**

**Priority Improvements**:
1. Move detailed content to references/ (+5 points)
2. Add missing edge cases (+4 points)
3. Clarify ambiguous instructions (+2 points)
4. Optimize workflows (+3 points)

**Target**: 132/150 (B Grade)

## Using the Audit Results

### A Grade (135-150)
- Production ready
- Share with team
- Use as example
- Monitor for improvements

### B Grade (120-134)
- Good quality
- Address priority issues
- Test thoroughly
- Consider sharing

### C Grade (105-119)
- Needs improvement
- Address high-priority issues
- Re-audit after changes
- Don't distribute widely

### D Grade (90-104)
- Major rework needed
- Focus on autonomy and discoverability
- Reconsider skill scope
- Significant revision required

### F Grade (<90)
- Complete rebuild
- Start with evaluation-driven approach
- Focus on fundamentals
- Rebuild from scratch

## Automation Tools

### skills-ref Validation
```bash
# Validate skill structure
skills-ref validate ./my-skill

# Check frontmatter
# Verify naming conventions
# Report compliance issues
```

### Custom Audits
Create evaluation files:
```json
{
  "skills": ["my-skill"],
  "query": "Test scenario",
  "expected": "Expected behavior"
}
```

Run automated tests to score autonomy and completeness.

## Best Practices

### DO ✅
- Use all 11 dimensions
- Test with real scenarios
- Prioritize high-impact improvements
- Re-audit after changes
- Share audit results with team
- Document decisions

### DON'T ❌
- Don't skip dimensions
- Don't rely on intuition alone
- Don't ignore low scores
- Don't skip re-auditing
- Don't skip testing
- Don't skip documentation
