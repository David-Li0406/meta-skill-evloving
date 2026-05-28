# Context Audit Examples

This file provides practical examples of using the context-audit skill for
various scenarios.

## Example 1: Audit All Context Files

**Scenario:** You want to perform a comprehensive audit of all CLAUDE.md
files in your repository.

**Command:**

```bash
/context-audit
```

**Expected Output:**

```markdown
# LLM Context Audit Report

**Date:** 2026-01-17
**Scope:** all
**Mode:** strict

## Summary

- **Files Audited:** 4
- **Overall Health Score:** 78/100 (Good 👍)
- **Status:** PASS

### Issue Distribution

- Critical: 0
- High: 2
- Medium: 3
- Low: 1

## File-Level Results

### CLAUDE.md (Root)

- **Line Count:** 485/500 ✅
- **Health Score:** 85/100 (Good 👍)
- **Efficiency Score:** 82/100
- **Issues:** 0 critical, 1 high, 1 medium, 0 low

**Findings:**

1. [HIGH] Missing design doc pointer for architecture section
   - Add reference to .claude/design/architecture.md
2. [MEDIUM] Code example on lines 120-135 could be shortened
   - Consider linking to design docs instead

### pkgs/effect-type-registry/CLAUDE.md

- **Line Count:** 245/300 ✅
- **Health Score:** 90/100 (Excellent ✅)
- **Efficiency Score:** 88/100
- **Issues:** 0 critical, 0 high, 1 medium, 0 low

**Findings:**

1. [MEDIUM] Minor formatting inconsistencies in bullet lists

### pkgs/rspress-plugin-api-extractor/CLAUDE.md

- **Line Count:** 380/300 ⚠️
- **Health Score:** 65/100 (Fair ⚠️)
- **Efficiency Score:** 58/100
- **Issues:** 0 critical, 1 high, 1 medium, 1 low

**Findings:**

1. [HIGH] Exceeds line limit by 27% (380/300 lines)
   - Use /context-split to split into child files
2. [MEDIUM] Verbose explanations could be more concise
3. [LOW] Consider adding more design doc pointers

## Recommendations

### High Priority (Should Fix)

1. Add design doc pointer in root CLAUDE.md for architecture
   - File: CLAUDE.md
   - Skill: /context-update
   - Impact: Better context separation

2. Split rspress-plugin-api-extractor/CLAUDE.md
   - File: pkgs/rspress-plugin-api-extractor/CLAUDE.md
   - Skill: /context-split --strategy=topic
   - Impact: Reduces token usage, improves organization

### Medium Priority (Nice to Have)

1. Shorten code examples in root CLAUDE.md
2. Fix formatting inconsistencies
3. Add more design doc pointers where applicable

## Quality Metrics

- **Average Line Count:** 303
- **Design Doc Pointer Coverage:** 75%
- **Content Efficiency Score:** 76/100
- **Token Optimization Score:** 72/100

## Next Steps

1. Fix high priority issues (2 items)
2. Re-run audit to verify improvements
3. Consider medium priority enhancements
```

## Example 2: Quick Audit of Root CLAUDE.md

**Scenario:** You want to quickly check the root CLAUDE.md file without
strict validation.

**Command:**

```bash
/context-audit CLAUDE.md --strict=false
```

**Expected Output:**

```markdown
# LLM Context Audit Report

**Date:** 2026-01-17
**Scope:** CLAUDE.md
**Mode:** normal

## Summary

- **Files Audited:** 1
- **Overall Health Score:** 85/100 (Good 👍)
- **Status:** PASS

### Issue Distribution

- Critical: 0
- High: 0
- Medium: 1
- Low: 0

## File-Level Results

### CLAUDE.md (Root)

- **Line Count:** 485/500 ✅
- **Health Score:** 85/100 (Good 👍)
- **Efficiency Score:** 82/100
- **Issues:** 0 critical, 0 high, 1 medium, 0 low

**Findings:**

1. [MEDIUM] Code example on lines 120-135 could be shortened

## Recommendations

### Medium Priority (Nice to Have)

1. Shorten code example (lines 120-135)
   - Skill: /context-update
   - Impact: Minor token savings

## Quality Metrics

- **Average Line Count:** 485
- **Design Doc Pointer Coverage:** 80%
- **Content Efficiency Score:** 82/100
- **Token Optimization Score:** 78/100

## Next Steps

✅ File passes quick audit! Consider medium priority improvements.
```

## Example 3: Audit Specific Package Context

**Scenario:** You want to audit the CLAUDE.md file for a specific package.

**Command:**

```bash
/context-audit pkgs/effect-type-registry/CLAUDE.md
```

**Expected Output:**

```markdown
# LLM Context Audit Report

**Date:** 2026-01-17
**Scope:** pkgs/effect-type-registry/CLAUDE.md
**Mode:** strict

## Summary

- **Files Audited:** 1
- **Overall Health Score:** 90/100 (Excellent ✅)
- **Status:** PASS

### Issue Distribution

- Critical: 0
- High: 0
- Medium: 1
- Low: 0

## File-Level Results

### pkgs/effect-type-registry/CLAUDE.md

- **Line Count:** 245/300 ✅
- **Health Score:** 90/100 (Excellent ✅)
- **Efficiency Score:** 88/100
- **Issues:** 0 critical, 0 high, 1 medium, 0 low

**Findings:**

1. [MEDIUM] Minor formatting inconsistencies in bullet lists
   - Lines 45, 67, 89 use mixed markers (- vs *)

## Recommendations

### Medium Priority (Nice to Have)

1. Standardize bullet list markers
   - File: pkgs/effect-type-registry/CLAUDE.md
   - Fix: Use consistent marker (- or *)
   - Impact: Better formatting consistency

## Quality Metrics

- **Average Line Count:** 245
- **Design Doc Pointer Coverage:** 90%
- **Content Efficiency Score:** 88/100
- **Token Optimization Score:** 85/100

## Next Steps

✅ Excellent context file! Only minor formatting improvements suggested.
```

## Example 4: Audit with Critical Issues

**Scenario:** Audit finds critical issues that must be fixed.

**Command:**

```bash
/context-audit pkgs/my-package/CLAUDE.md
```

**Expected Output:**

```markdown
# LLM Context Audit Report

**Date:** 2026-01-17
**Scope:** pkgs/my-package/CLAUDE.md
**Mode:** strict

## Summary

- **Files Audited:** 1
- **Overall Health Score:** 45/100 (Needs Work ❌)
- **Status:** FAIL

### Issue Distribution

- Critical: 2
- High: 3
- Medium: 4
- Low: 2

## File-Level Results

### pkgs/my-package/CLAUDE.md

- **Line Count:** 420/300 ❌
- **Health Score:** 45/100 (Needs Work ❌)
- **Efficiency Score:** 38/100
- **Issues:** 2 critical, 3 high, 4 medium, 2 low

**Findings:**

1. [CRITICAL] Exceeds line limit by 40% (420/300 lines)
   - File is significantly over limit
2. [CRITICAL] Broken design doc pointer at line 78
   - References .claude/design/my-package/missing.md (doesn't exist)
3. [HIGH] Missing design doc pointers for major sections
   - Architecture section (lines 50-120) has no pointer
   - Implementation section (lines 150-200) has no pointer
4. [HIGH] Code examples too verbose (lines 180-220)
   - 40+ lines of implementation details
5. [HIGH] Contains implementation details instead of high-level instructions
   - Lines 250-300 describe specific code implementation
6. [MEDIUM] Poor content organization
   - Sections lack clear hierarchy
7. [MEDIUM] Inconsistent formatting
8. [MEDIUM] No table of contents for long file
9. [MEDIUM] Missing section headers
10. [LOW] Minor style issues
11. [LOW] Could improve bullet point usage

## Recommendations

### Critical (Must Fix)

1. Split file to reduce line count
   - File: pkgs/my-package/CLAUDE.md
   - Skill: /context-split --strategy=topic
   - Impact: Critical - brings under limit, improves efficiency

2. Fix broken design doc pointer
   - File: pkgs/my-package/CLAUDE.md (line 78)
   - Fix: Create .claude/design/my-package/missing.md or update pointer
   - Skill: /design-init or /context-update
   - Impact: Critical - prevents confusion

### High Priority (Should Fix)

1. Add design doc pointers for architecture section
   - Skill: /design-init my-package architecture
   - Then update CLAUDE.md with pointer

2. Replace code examples with design doc links
   - Move detailed examples to design docs
   - Keep only minimal illustrative examples

3. Move implementation details to design docs
   - Replace with high-level imperative instructions
   - Link to design docs for details

## Quality Metrics

- **Average Line Count:** 420
- **Design Doc Pointer Coverage:** 20%
- **Content Efficiency Score:** 38/100
- **Token Optimization Score:** 35/100

## Next Steps

❌ Critical issues found! You must:

1. Split pkgs/my-package/CLAUDE.md immediately
   - Run: /context-split pkgs/my-package/CLAUDE.md --strategy=topic

2. Fix broken design doc pointer
   - Create missing.md or update reference

3. Create design docs for detailed content
   - Run: /design-init my-package architecture
   - Move implementation details there

4. Re-run audit after fixes
   - Run: /context-audit pkgs/my-package/CLAUDE.md

Would you like help fixing these issues?
```

## Example 5: Audit Without Design Doc Reference Checking

**Scenario:** Quick audit without validating design doc pointers.

**Command:**

```bash
/context-audit --check-refs=false
```

**Expected Output:**

```markdown
# LLM Context Audit Report

**Date:** 2026-01-17
**Scope:** all
**Mode:** strict (no reference checking)

## Summary

- **Files Audited:** 4
- **Overall Health Score:** 82/100 (Good 👍)
- **Status:** PASS

### Issue Distribution

- Critical: 0
- High: 1
- Medium: 2
- Low: 1

**Note:** Design doc reference validation was skipped.

[... rest of report ...]
```

## Example 6: Generate Report to File

**Scenario:** Audit and save report to file for later review.

**Command:**

```bash
/context-audit --output=.claude/reports/context-audit-2026-01-17.md
```

**Expected Output:**

```text
✅ Context audit complete

Report saved to: .claude/reports/context-audit-2026-01-17.md

Summary:
- Files Audited: 4
- Overall Health Score: 78/100 (Good 👍)
- Status: PASS
- Issues: 0 critical, 2 high, 3 medium, 1 low

View the full report at .claude/reports/context-audit-2026-01-17.md
```

## Common Follow-Up Actions

After running an audit, you typically want to:

### Fix Critical Issues

```bash
# Split oversized file
/context-split pkgs/my-package/CLAUDE.md --strategy=topic

# Fix broken pointer by creating design doc
/design-init my-package missing-topic
```

### Address High Priority Issues

```bash
# Update context file with design doc pointers
/context-update CLAUDE.md

# Review and improve specific file
/context-review pkgs/my-package/CLAUDE.md
```

### Verify Fixes

```bash
# Re-run audit after making changes
/context-audit

# Validate specific file
/context-validate pkgs/my-package/CLAUDE.md
```

## Tips for Best Results

1. **Run audits regularly** - Before releases, after major changes
2. **Start strict** - Default strict mode catches more issues
3. **Address critical first** - Fix line limits and broken pointers immediately
4. **Use output files** - For large audits, save to file for review
5. **Follow up** - Use related skills to fix identified issues
6. **Re-audit** - Verify improvements after making changes
7. **Track trends** - Compare audit scores over time
