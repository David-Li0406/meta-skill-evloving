# Evaluation Structure Reference

## Why Quality-Based Evaluation Matters

Simple pass/fail evaluation ("did it do X?") fails to differentiate models. All models can "do the steps" - the difference is **how well** they do them.

**Problem with binary evaluation:**
```markdown
- Asks clarifying questions ← haiku asks 1 vague question, opus asks 3 targeted ones
- Determines freedom level ← both "determine" it, but opus justifies correctly
```

Both pass, but quality differs dramatically.

## Scenario Format

```markdown
## Scenario: [Name]

**Difficulty:** Easy | Medium | Hard | Edge-case

**Query:** The exact user request

**Test files:** (optional)
- path/to/file.ext

**Expected behaviors:**

1. [Action description]
   - **Minimum:** What counts as "did it"
   - **Quality criteria:** What "did it well" looks like
   - **Haiku pitfall:** Common failure mode for smaller models
   - **Weight:** 1-5 (importance)

2. [Next action...]

**Output validation:** (optional)
- Pattern: `regex or glob`
- Golden file: `path/to/expected-output.md`

**Scoring:**
- Completeness: X% (did all steps)
- Quality: X% (how well)
- Efficiency: X% (no unnecessary steps)
```

## Difficulty Levels

| Level | Characteristics | Expected Model Performance |
|-------|-----------------|---------------------------|
| **Easy** | Clear requirements, single step, no ambiguity | All models should pass |
| **Medium** | Multi-step workflow, some judgment needed | haiku may struggle with quality |
| **Hard** | Complex decisions, long context, ambiguous requirements | haiku likely fails, sonnet may struggle |
| **Edge-case** | Error handling, unusual inputs, boundary conditions | Tests robustness across models |

**Use difficulty to design discriminating tests:**
- If all models pass Easy scenarios, that's expected
- Hard scenarios should show model differentiation
- Edge-cases reveal robustness differences

**Default to Hard scenarios:** When evaluating skills, prioritize Hard or Medium difficulty scenarios. Easy scenarios often fail to show meaningful differences between models and aren't representative of realistic production usage.

## Quality Criteria Examples

### For "Asks clarifying questions"

**Bad (binary):**
```markdown
- Asks clarifying questions about requirements
```

**Good (quality-based):**
```markdown
1. Asks clarifying questions about requirements
   - **Minimum:** Asks at least 1 question before proceeding
   - **Quality criteria:**
     - Asks about purpose/functionality
     - Asks about usage examples
     - Asks about triggers
     - Questions are specific, not generic
   - **Haiku pitfall:** Asks "What should the skill do?" (too vague) or skips to implementation
   - **Weight:** 4
```

### For "Determines freedom level"

**Bad (binary):**
```markdown
- Determines appropriate freedom level
```

**Good (quality-based):**
```markdown
2. Determines appropriate freedom level
   - **Minimum:** States a freedom level (high/medium/low)
   - **Quality criteria:**
     - References degrees-of-freedom.md
     - Justifies with specific factors (fragility, context-dependency, etc.)
     - Explains trade-offs of chosen level
   - **Haiku pitfall:** Picks level without justification, or misreads fragility signals
   - **Weight:** 3
```

### For "Creates SKILL.md"

**Bad (binary):**
```markdown
- Creates SKILL.md file
```

**Good (quality-based):**
```markdown
3. Creates SKILL.md with proper structure
   - **Minimum:** File is created with frontmatter
   - **Quality criteria:**
     - Name uses gerund form (regex: `^[a-z]+ing-[a-z-]+$`)
     - Description includes WHAT and WHEN
     - Description is third person
     - Body under 200 lines (target), max 500
     - Includes workflow steps
   - **Haiku pitfall:** Description too short, missing "when to use", or body too verbose
   - **Weight:** 5
```

## Scoring System

### Score Calculation

Each behavior is scored 0-100:

| Score | Meaning |
|-------|---------|
| 0 | Not attempted or completely wrong |
| 25 | Attempted but below minimum |
| 50 | Meets minimum criteria |
| 75 | Meets most quality criteria |
| 100 | Meets all quality criteria |

**Weighted total:**
```
Total = Σ(behavior_score × weight) / Σ(weights)
```

### Scoring Dimensions

| Dimension | Weight | What it measures |
|-----------|--------|------------------|
| **Completeness** | 40% | Did all expected steps |
| **Quality** | 35% | How well each step was done |
| **Efficiency** | 15% | No unnecessary steps, reasonable token usage |
| **Robustness** | 10% | Handles edge cases, errors gracefully |

### Rating Thresholds

| Score | Rating | Interpretation |
|-------|--------|----------------|
| 90-100 | ✅ Excellent | Production ready |
| 75-89 | ✅ Good | Acceptable with minor issues |
| 50-74 | ⚠️ Partial | Functional but quality issues |
| 25-49 | ⚠️ Marginal | Significant problems |
| 0-24 | ❌ Fail | Does not meet requirements |

## Output Validation

### Pattern Matching

```markdown
**Output validation:**
- Filename pattern: `managing-*.md`
- Contains: `---\nname:` (has frontmatter)
- Line count: `< 500`
- Regex match: `description:.*Use when`
```

### Golden File Comparison

For complex outputs, compare against expected output:

```markdown
**Output validation:**
- Golden file: tests/expected/skill-frontmatter.yaml
- Compare: frontmatter only
- Tolerance: ordering may differ
```

## Minimum Recommended Scenarios

Create at least 4 scenarios:

| Scenario | Difficulty | Purpose |
|----------|------------|---------|
| Happy path | Easy | Baseline - all models should pass |
| Standard workflow | Medium | Quality differentiation |
| Complex judgment | Hard | Model capability limits |
| Error/Edge case | Edge-case | Robustness testing |

## Model-Specific Pitfalls Reference

### Haiku Common Issues

| Issue | Example | Detection |
|-------|---------|-----------|
| Shallow questions | "What should it do?" vs specific questions | Count question specificity |
| Skip justification | Picks option without explaining why | Check for reasoning |
| Verbose output | SKILL.md > 300 lines when 150 would suffice | Line count check |
| Miss references | Doesn't read linked .md files | Check files read |
| Premature action | Starts implementing before clarifying | Check question-first pattern |

### Sonnet Common Issues

| Issue | Example | Detection |
|-------|---------|-----------|
| Over-engineering | Adds unnecessary features | Check scope creep |
| Inconsistent depth | Some parts detailed, others shallow | Quality variance check |

### Opus Common Issues

| Issue | Example | Detection |
|-------|---------|-----------|
| Over-verbose | Explains more than necessary | Token efficiency |
| Slow iteration | Takes longer for simple tasks | Time/turn comparison |

## Example: Full Scenario

```markdown
## Scenario: Create skill for ambiguous requirements

**Difficulty:** Hard

**Query:** I need a skill for handling data. Can you help?

**Expected behaviors:**

1. Seeks clarification before proceeding
   - **Minimum:** Asks at least one question
   - **Quality criteria:**
     - Asks what kind of data (format, source)
     - Asks what operations (transform, validate, migrate)
     - Asks about error handling requirements
     - Does NOT start creating files before answers
   - **Haiku pitfall:** Makes assumptions and starts implementing
   - **Weight:** 5

2. Identifies skill scope appropriately
   - **Minimum:** Proposes a focused skill name
   - **Quality criteria:**
     - Name is specific (not "data-helper")
     - Scope is single-responsibility
     - Explains what's in/out of scope
   - **Haiku pitfall:** Proposes overly broad "data-processing" skill
   - **Weight:** 4

3. Determines freedom level with justification
   - **Minimum:** States a level
   - **Quality criteria:**
     - References specific factors from degrees-of-freedom.md
     - Explains why this data task fits that level
     - Considers fragility and context-dependency
   - **Haiku pitfall:** Picks without justification
   - **Weight:** 3

**Scoring:**
- Completeness: 40%
- Quality: 35%
- Efficiency: 15%
- Robustness: 10%
```

## Tracking Results

### Evaluation Summary Matrix

Use detailed scoring matrix during evaluation:

```markdown
| Scenario | Difficulty | claude-haiku-4-5-20250101 | claude-sonnet-4-5-20250929 | claude-opus-4-5-20251101 |
|----------|------------|---------------------------|----------------------------|--------------------------|
| Happy path | Easy | 85 | 92 | 95 |
| Standard workflow | Medium | 62 | 88 | 94 |
| Complex judgment | Hard | 41 | 75 | 91 |
| Error handling | Edge | 55 | 82 | 89 |
| **Weighted Average** | | **58** | **84** | **92** |
```

### README Documentation

After evaluation, add results to the skill's README for historical tracking:

```markdown
## Evaluation Results

| Date | Scenario | Difficulty | Model | Score | Rating |
|------|----------|------------|-------|-------|--------|
| 2025-01-15 | Standard workflow | Hard | claude-haiku-4-5-20250101 | 62 | ⚠️ Partial |
| 2025-01-15 | Standard workflow | Hard | claude-sonnet-4-5-20250929 | 88 | ✅ Good |
| 2025-01-15 | Standard workflow | Hard | claude-opus-4-5-20251101 | 94 | ✅ Excellent |
| 2025-01-20 | Complex judgment | Hard | claude-haiku-4-5-20250101 | 41 | ⚠️ Marginal |
| 2025-01-20 | Complex judgment | Hard | claude-sonnet-4-5-20250929 | 75 | ✅ Good |
| 2025-01-20 | Complex judgment | Hard | claude-opus-4-5-20251101 | 91 | ✅ Excellent |
```

**Table requirements:**
- Use full model IDs (e.g., `claude-sonnet-4-5-20250929`)
- Include evaluation date in YYYY-MM-DD format
- Show scenario difficulty level
- Append new evaluations (maintain history)
- Include both numeric score and rating
