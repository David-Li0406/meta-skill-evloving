# Detailed Instructions for Context Audit

This file provides comprehensive step-by-step instructions for performing
a thorough audit of CLAUDE.md context files.

## Step 1: Parse Parameters

Extract parameters from the user's request:

**Optional:**

- `target`: Path to specific CLAUDE.md file or "all" (default: all)
- `strict`: Enable strict mode (default: true)
- `check-refs`: Validate design doc references (default: true)
- `output`: Output file path for report

**Examples:**

- "Audit all CLAUDE.md files" → target: all, strict: true
- "Audit CLAUDE.md quickly" → target: CLAUDE.md, strict: false
- "Audit effect-type-registry context" → target: pkgs/effect-type-registry/CLAUDE.md

## Step 2: Load Configuration

Read `.claude/design/design.config.json` to get quality standards:

**Required fields:**

```json
{
  "quality": {
    "context": {
      "rootMaxLines": 500,
      "childMaxLines": 300,
      "requireDesignDocPointers": true
    }
  },
  "modules": {
    "module-name": {
      "path": "pkgs/module-name",
      ...
    }
  }
}
```

**Store:**

- `rootMaxLines` (default: 500)
- `childMaxLines` (default: 300)
- `requireDesignDocPointers` (default: true)
- Module paths for child context discovery

## Step 3: Discover CLAUDE.md Files

Use Glob to find all CLAUDE.md files based on target parameter:

**If target is "all":**

```bash
# Find root CLAUDE.md
CLAUDE.md or CLAUDE.local.md

# Find package-level CLAUDE.md in each module
{module-path}/CLAUDE.md
```

**If target is specific path:**

Validate path exists and is a CLAUDE.md file.

**Store file list with metadata:**

- File path
- Role: "root" or "child" (package-level)
- Expected line limit
- Module name (for children)

## Step 4: Validation Checks

For each discovered file, run comprehensive validation:

### 4.1 Structure Validation

Check markdown structure:

- File exists and is readable
- Valid markdown syntax
- Proper heading hierarchy (no skipped levels)
- Code blocks properly closed
- Lists properly formatted

**Use Read tool** to load file content.

**Check:**

- No syntax errors
- Headings follow H1 → H2 → H3 order
- All code fences (```) are closed
- Bullet lists use consistent markers

### 4.2 Line Count Check

Count total lines (excluding blank lines):

```bash
# Count non-blank lines
grep -c -v '^[[:space:]]*$' {file}
```

**Compare:**

- Root CLAUDE.md: ≤ `rootMaxLines` (500)
- Child CLAUDE.md: ≤ `childMaxLines` (300)

**Severity:**

- > limit by 20%: CRITICAL
- > limit by 10%: HIGH
- > limit: MEDIUM

### 4.3 Content Quality Check

Analyze content for efficiency and focus:

**Imperative Instructions:**

- Should contain high-level instructions
- Avoid implementation details
- Use clear, concise language
- Focus on "what" not "how"

**Prohibited Content:**

- Code examples longer than 10 lines
- Detailed implementation walkthroughs
- Historical information ("we changed X to Y")
- Verbose explanations

**Required Style:**

- Lean, imperative tone
- Bullet points over paragraphs where possible
- Links to design docs instead of inline details
- Clear section headings

**Check each section:**

- Is it imperative? (commands, not descriptions)
- Is it high-level? (architecture, not code)
- Is it necessary? (could it be in design docs?)

### 4.4 Design Doc Pointer Check

If `requireDesignDocPointers` is true:

**Look for design doc references:**

- `See .claude/design/{module}/{file}.md`
- `Design: .claude/design/...`
- Links to design documentation

**For each reference:**

- Extract file path
- Verify file exists using Read tool
- Check file has valid frontmatter

**Severity:**

- Missing required pointers: HIGH
- Broken pointer (file doesn't exist): CRITICAL
- Invalid pointer (bad frontmatter): MEDIUM

### 4.5 Formatting Validation

Check markdown formatting:

- Consistent heading style (# Heading)
- Proper list indentation
- Code fence language tags (```bash,```typescript)
- No trailing whitespace
- Consistent line endings

**Use bash commands or grep to check:**

```bash
# Check for trailing whitespace
grep -n ' $' {file}

# Check for inconsistent list markers
grep -E '^[[:space:]]*([-*+])' {file}
```

## Step 5: Content Quality Analysis

Perform deep content analysis:

### 5.1 Efficiency Score (0-100)

Calculate based on:

- Line density: fewer lines = higher score
- Bullet point ratio: more bullets = higher score
- Link ratio: more design doc links = higher score
- Code example ratio: fewer examples = higher score

**Formula:**

```text
efficiency = (
  (1 - lineCount/limit) * 40 +
  (bulletPoints/totalParagraphs) * 30 +
  (designDocLinks/sections) * 20 +
  (1 - codeLines/totalLines) * 10
)
```

### 5.2 Organization Score (0-100)

Evaluate structure:

- Clear section hierarchy
- Logical flow
- Proper grouping of related content
- Navigation aids (TOC if long)

**Scoring:**

- Well-organized: 80-100
- Needs improvement: 50-79
- Poorly organized: 0-49

### 5.3 Token Optimization Score (0-100)

Estimate token efficiency:

- Estimate total tokens (rough: chars / 4)
- Calculate tokens per useful instruction
- Compare to ideal ratio

**Target:** < 2000 tokens for root, < 1000 for child

## Step 6: Calculate Health Scores

### File-Level Health Score

Combine validation results:

```text
health = (
  structureValid * 25 +
  lineLimitPass * 25 +
  contentQuality * 25 +
  pointerStatus * 25
)
```

**Categories:**

- 90-100: Excellent ✅
- 70-89: Good 👍
- 50-69: Fair ⚠️
- 0-49: Needs Work ❌

### Module-Level Health Score

Average health scores of all child CLAUDE.md files in a module.

### Overall Health Score

Weighted average:

- Root CLAUDE.md: 40% weight
- All children: 60% weight (averaged)

## Step 7: Identify Issues

Categorize all findings by severity:

### Critical Issues (Must Fix)

- File exceeds limit by > 20%
- Broken design doc pointers
- Invalid markdown syntax
- Missing required sections

### High Priority (Should Fix)

- File exceeds limit by 10-20%
- Missing design doc pointers
- Inefficient content structure
- Poor token optimization

### Medium Priority (Nice to Have)

- File exceeds limit by < 10%
- Formatting inconsistencies
- Could improve organization
- Minor content issues

### Low Priority (Optional)

- Style improvements
- Additional optimizations
- Enhancement opportunities

## Step 8: Generate Recommendations

For each issue found, provide:

1. **Issue description** - What's wrong
2. **Location** - File and line number if applicable
3. **Severity** - Critical/High/Medium/Low
4. **Recommendation** - How to fix
5. **Related skill** - Which skill can help

**Prioritize:**

- Critical issues first
- Group by file
- Order by impact

**Example recommendations:**

```markdown
1. [CRITICAL] Root CLAUDE.md exceeds limit (650/500 lines)
   - File: CLAUDE.md
   - Fix: Use /context-split to split into child files
   - Impact: Reduces token usage, improves efficiency

2. [HIGH] Missing design doc pointer for architecture
   - File: pkgs/my-package/CLAUDE.md
   - Fix: Add pointer to .claude/design/my-package/architecture.md
   - Impact: Better context separation, cleaner instructions
```

## Step 9: Output Audit Report

Generate comprehensive report in markdown format:

### Report Structure

```markdown
# LLM Context Audit Report

**Date:** YYYY-MM-DD
**Scope:** {all | specific file}
**Mode:** {strict | normal}

## Summary

- **Files Audited:** N
- **Overall Health Score:** X/100 {category}
- **Status:** {PASS | FAIL}

### Issue Distribution

- Critical: N
- High: N
- Medium: N
- Low: N

## File-Level Results

### CLAUDE.md (Root)

- **Line Count:** N/500 {status}
- **Health Score:** X/100 {category}
- **Efficiency Score:** X/100
- **Issues:** N critical, N high, N medium, N low

**Findings:**

1. Issue description...
2. Issue description...

### pkgs/module-name/CLAUDE.md

... (repeat for each file)

## Recommendations

### Critical (Must Fix)

1. Recommendation...
2. Recommendation...

### High Priority (Should Fix)

1. Recommendation...
2. Recommendation...

### Medium Priority (Nice to Have)

1. Recommendation...

### Low Priority (Optional)

1. Recommendation...

## Quality Metrics

- **Average Line Count:** N
- **Design Doc Pointer Coverage:** N%
- **Content Efficiency Score:** X/100
- **Token Optimization Score:** X/100

## Related Skills

- `/context-update` - Update files based on findings
- `/context-split` - Split files exceeding limits
- `/context-validate` - Re-validate after changes
- `/context-review` - Review specific quality aspects

## Next Steps

1. Fix critical issues first
2. Address high priority issues
3. Re-run audit to verify improvements
4. Consider medium/low priority enhancements
```

**If output parameter provided:**

Write report to specified file.

**Otherwise:**

Output report directly to user.

## Step 10: Provide Guidance

After outputting the report, provide actionable next steps:

**If critical issues found:**

"There are N critical issues that must be fixed. Start with:"

1. List critical issues
2. Suggest specific skills to use
3. Offer to help fix issues

**If only high/medium issues:**

"The audit identified N areas for improvement. Consider:"

1. High priority fixes
2. Tools/skills to use
3. Expected impact

**If audit passes:**

"✅ All CLAUDE.md files pass quality standards!"

- Report overall health score
- Highlight any optional improvements
- Mention best practices being followed

## Error Handling

**Configuration Missing:**

If `.claude/design/design.config.json` doesn't exist:

- Use default values (root: 500, child: 300)
- Note in report that defaults were used
- Suggest creating config file

**File Not Found:**

If target file doesn't exist:

- Report error clearly
- Suggest correct path
- Show available CLAUDE.md files

**Invalid Markdown:**

If file has syntax errors:

- Note specific errors (line numbers)
- Mark as CRITICAL issue
- Recommend fixing syntax first before re-auditing

## Strict Mode Differences

When `strict: true` (default):

- Enforce all quality checks
- Lower thresholds for warnings
- Check design doc content quality (not just existence)
- Verify all links and references
- Stricter content quality scoring

When `strict: false`:

- Only check critical issues
- More lenient thresholds
- Skip deep content analysis
- Faster execution
- Good for quick checks

## Performance Considerations

For large repositories:

- Process files in parallel where possible
- Cache file reads
- Skip design doc validation if `check-refs: false`
- Use `--output` to avoid large terminal output
- Consider targeting specific files vs "all"

Typical execution time:

- Single file: 5-10 seconds
- All files (5-10 files): 30-60 seconds
- Large repo (20+ files): 1-3 minutes
