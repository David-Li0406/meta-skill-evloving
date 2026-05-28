# Common Mistakes in Agent Creation

Anti-pattern catalog with real examples and fixes.

## Top 10 Agent Creation Mistakes

### 1. Missing Temporal Awareness ❌

**Severity**: CRITICAL  
**Frequency**: 95% of initial agent drafts  
**Impact**: Legal/compliance risk, wrong document dates

**Mistake**:
```markdown
## Phase 1: Requirements Gathering

**Actions**:
1. Understand user needs
2. Identify scope
3. Define deliverables
```

**Fix**:
```markdown
## Phase 1: Requirements Gathering & Temporal Awareness

**Actions**:
1. **Establish Temporal Context** (REQUIRED):
   ```bash
   CURRENT_DATE=$(date '+%Y-%m-%d')
   READABLE_DATE=$(date '+%B %d, %Y')
   ```
2. Understand user needs
3. Identify scope
```

**Why it matters**: The pizza baker contract bug (January vs November 2025) showed that wrong dates in legal documents create serious validity questions.

---

### 2. Vague Success Criteria ❌

**Severity**: HIGH  
**Frequency**: 80% of agents  
**Impact**: Can't validate if agent succeeded

**Mistake**:
```markdown
## Success Criteria

- ✅ Agent works correctly
- ✅ Output is good quality
- ✅ Task completed successfully
- ✅ User is satisfied
```

**Fix**:
```markdown
## Success Criteria

- ✅ Generated report includes 5 sections: summary, findings, evidence, recommendations, confidence
- ✅ All 47 identified patterns include line numbers and file paths
- ✅ Confidence level >85% with 3+ pieces of supporting evidence
- ✅ False positive rate <10% based on validation sample
- ✅ Report generated in <10 minutes
- ✅ Output format matches template (JSON with required fields)
- ✅ All recommendations are actionable (what to fix + where + how)
[12 total - all specific and measurable]
```

**Rule**: If you can't objectively verify a criterion, it's too vague.

---

### 3. Generic Self-Critique ❌

**Severity**: HIGH  
**Frequency**: 70% of agents  
**Impact**: Doesn't catch domain-specific errors

**Mistake**:
```markdown
## Self-Critique

1. Did I understand the requirements?
2. Did I complete the task?
3. Is the output good quality?
4. Did I make any mistakes?
5. Should I improve anything?
```

**Fix**:
```markdown
## Self-Critique

1. **Coverage**: Did I audit ALL feature engineering files, not just main pipeline?
2. **False Positives**: Could any flagged rolling operations be safe in context?
3. **False Negatives**: Did I miss subtle patterns like `.shift(-n)` negative shifts?
4. **Confidence**: What evidence supports my 92% confidence in each violation?
5. **Verification**: How can user independently verify findings (reproduce leak)?
6. **Temporal**: Did I use correct current date for timestamps?
[6 questions - all specific to Kaggle leak auditing]
```

**Rule**: Self-critique questions should only make sense for THIS agent, not all agents.

---

### 4. Tool Overload ❌

**Severity**: MEDIUM  
**Frequency**: 60% of agents  
**Impact**: Confusing, suggests agent does more than it actually does

**Mistake**:
```yaml
---
tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Task, TodoWrite
---
```
```markdown
## Phase 1
**Actions**:
1. Use Read to load file
2. Use Write to save output
```

**Fix**:
```yaml
---
tools: Read, Write
---
```

**Rule**: Only declare tools that are explicitly mentioned in phase actions.

---

### 5. No Edge Case Handling ❌

**Severity**: HIGH  
**Frequency**: 90% of agents  
**Impact**: Agent fails ungracefully on unexpected inputs

**Mistake**:
```markdown
## Phase 1: Process Files

**Actions**:
1. Read input file
2. Parse CSV data
3. Generate markdown table
```

**Fix**:
```markdown
## Phase 1: Process Files

**Actions**:
1. Read input file
   - If file doesn't exist: Log error, skip, continue with remaining files
   - If file >1GB: Use streaming parser instead of loading full file
2. Parse CSV data
   - If malformed: Attempt partial parse, report which rows failed
   - If empty: Return empty result (not error)
3. Generate markdown table
   - If >1000 rows: Add pagination or summary view
   - If special characters: Escape properly for markdown

## Edge Cases

**Missing Files**: Skip with error log, don't crash
**Invalid Data**: Partial parse + detailed error report
**Large Files**: Stream processing for >1GB
**Empty Input**: Return empty result with warning log
**Timeout**: Retry with exponential backoff (max 3 attempts)
```

**Rule**: Think "what could go wrong?" and document handling for each scenario.

---

### 6. Too Many Phases ❌

**Severity**: MEDIUM  
**Frequency**: 30% of complex agents  
**Impact**: Confusing workflow, hard to maintain

**Mistake**:
```markdown
## Phase 1: Initial Setup
## Phase 2: Data Loading
## Phase 3: Data Validation
## Phase 4: Data Transformation
## Phase 5: Analysis
## Phase 6: Aggregation
## Phase 7: Report Generation
## Phase 8: Output Formatting
[8 phases - too many]
```

**Fix**:
```markdown
## Phase 1: Data Ingestion & Validation
[Combined loading + validation]

## Phase 2: Analysis & Transformation
[Combined analysis + transformation]

## Phase 3: Report Generation
[Combined generation + formatting]

[3 phases - optimal]
```

**Rule**: 3-5 phases optimal. If >5, consider combining related steps.

---

### 7. Missing Progressive Disclosure ❌

**Severity**: MEDIUM  
**Frequency**: 40% of agents >250 lines  
**Impact**: Agent file becomes unreadable, hard to maintain

**Mistake**:
```markdown
# Agent Name (450 lines total)

## Pattern Detection

**Pattern A: Rolling Operations with center=True**

[100 lines of detailed explanation with examples]

**Pattern B: Negative Shifts**

[80 lines of detailed explanation]

**Pattern C: Future Indexing**

[90 lines of detailed explanation]

[All inline - no references]
```

**Fix**:
```markdown
# Agent Name (200 lines total)

## Pattern Detection

**Reference Documentation**: `/refs/leak-patterns.md` (500 lines)

**Key patterns** (see reference for details):
1. Rolling operations with `center=True` (CRITICAL)
2. Negative shifts `.shift(-n)` (CRITICAL)
3. Future indexing `df.loc[future_dates]` (CRITICAL)

[Concise main file, details in references]
```

**Rule**: If agent >250 lines, extract details to references.

---

### 8. Missing Frontmatter Description Triggers ❌

**Severity**: LOW  
**Frequency**: 50% of agents  
**Impact**: Agent may not trigger when needed

**Mistake**:
```yaml
---
name: data-analyzer
description: Analyzes data
---
```

**Fix**:
```yaml
---
name: data-analyzer
description: Analyzes structured data for patterns and anomalies. Use when exploring CSV/JSON datasets, detecting outliers, or generating summary statistics. Examples: "Analyze this sales data", "Find anomalies in user behavior"
---
```

**Rule**: Include WHEN to use + concrete example questions.

---

### 9. No Confidence Thresholds ❌

**Severity**: MEDIUM  
**Frequency**: 40% of agents  
**Impact**: Can't assess reliability of outputs

**Mistake**:
```markdown
[No Confidence Thresholds section]
```

**Fix**:
```markdown
## Confidence Thresholds

- **High (85-95%)**: Direct evidence in logs/stack traces, successfully reproduced, known bug in specific version, 3+ pieces of corroborating evidence
- **Medium (70-84%)**: Circumstantial evidence, timing correlation, similar issues reported, code pattern could cause observed behavior
- **Low (<70%)**: Educated guess, no direct evidence, multiple alternative explanations equally plausible - user should validate
```

**Rule**: Define concrete conditions for each confidence level.

---

### 10. Phases Missing Deliverables ❌

**Severity**: MEDIUM  
**Frequency**: 60% of agents  
**Impact**: Unclear what each phase produces

**Mistake**:
```markdown
## Phase 1: Static Analysis

**Objective**: Analyze code for patterns

**Actions**:
1. Search for suspicious patterns
2. Validate findings
3. Categorize by severity
```

**Fix**:
```markdown
## Phase 1: Static Analysis

**Objective**: Analyze code for patterns

**Actions**:
1. Search for suspicious patterns
2. Validate findings
3. Categorize by severity

**Deliverable**: List of 20-50 potential violations, each with:
- Pattern type (rolling/shift/indexing)
- File path and line number
- Code snippet (5 lines context)
- Severity (CRITICAL/WARNING/INFO)
- Confidence (0-100%)
```

**Rule**: Every phase should have concrete deliverable (artifact or decision).

---

## Detection Strategies

### How to Find These Mistakes

**1. Missing Temporal Awareness**:
```bash
grep -i "CURRENT_DATE\|REQUIRED.*date" agent.md
# If empty, you're missing it
```

**2. Vague Success Criteria**:
```bash
grep -A 20 "## Success Criteria" agent.md | grep -E "works|good|correct|acceptable"
# If matches, criteria too vague
```

**3. Generic Self-Critique**:
```bash
grep -A 15 "## Self-Critique" agent.md | grep -E "understand|complete|good|mistake"
# If matches, questions too generic
```

**4. Tool Overload**:
```bash
# Compare declared vs used
grep "tools:" agent.md
grep -E "Use (Read|Write|Edit|Bash|Grep)" agent.md
# Should match closely
```

**5. No Edge Cases**:
```bash
grep -iE "error|fail|exception|missing|invalid|edge" agent.md | wc -l
# If <5, insufficient edge case handling
```

---

## Prevention Checklist

Before deploying an agent, verify:

- [ ] Phase 1 includes temporal awareness with REQUIRED label
- [ ] 10-16 success criteria, all specific and measurable
- [ ] 6-10 self-critique questions, all domain-specific
- [ ] Tools in frontmatter match phase usage (no extras)
- [ ] Edge cases documented (5+ scenarios)
- [ ] If >250 lines, details extracted to references
- [ ] Description includes WHEN to use + examples
- [ ] Confidence thresholds defined with concrete conditions
- [ ] Every phase has deliverable specified
- [ ] No generic phrases like "works correctly", "good quality"

---

## Real Production Examples

### Before Fixes (Legal Agent v1)
- **Score**: 52/70 (Fair)
- **Issues**: 843 lines (no progressive disclosure), missing language QC, no citation validation

### After Fixes (Legal Agent v2)
- **Score**: 68/70 (Excellent)
- **Changes**: Refactored to 264 lines + references, added 3 skill plugins, comprehensive edge cases
- **Impact**: +16 points, production ready

---

## Quick Reference: Common Mistake Patterns

| Mistake | Detection Pattern | Fix Pattern |
|---------|------------------|-------------|
| Missing temporal | No `CURRENT_DATE` in Phase 1 | Add REQUIRED temporal block |
| Vague criteria | Contains "works", "good", "correct" | Replace with measurable outcomes |
| Generic critique | Applies to all agents | Make domain-specific |
| Tool overload | Declared > used | Remove unused tools |
| No edge cases | <5 error mentions | Document 5+ scenarios |
| Too many phases | >5 phases | Combine related phases |
| No disclosure | >250 lines, no refs | Extract to references/ |
| No triggers | Description too short | Add WHEN + examples |
| No confidence | Missing thresholds section | Define 3-tier system |
| No deliverables | Phase missing output | Specify concrete artifact |

---

**Remember**: These mistakes are learned from real production agents. The validate_agent.py script checks for most of these automatically!
